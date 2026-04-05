"""
seed_master.py — Orquestador de Inyección DAKI EdTech
========================================================

Carga TODOS los niveles de los 10 sectores actuales (hasta level_order 100)
en la base de datos PostgreSQL usando lógica de UPSERT:

  • Si el nivel YA EXISTE  → actualiza campos de contenido (preserva el UUID y
                             la telemetría en user_metrics).
  • Si el nivel NO EXISTE  → lo crea con un UUID nuevo.

La clave natural del upsert es (sector_id, level_order).

Uso desde la raíz del proyecto:
    python -m scripts.seed_master
    python -m scripts.seed_master --dry-run   # muestra el plan sin tocar la DB
    python -m scripts.seed_master --sector 3  # solo recarga un sector específico

Variables de entorno requeridas (o en .env):
    DATABASE_URL  postgresql+asyncpg://user:password@host:5432/dbname
"""

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.models.challenge import Challenge, DifficultyTier

# ─────────────────────────────────────────────────────────────────────────────
# Importamos los catálogos de cada sector (datos canónicos).
# Si un archivo aún no existe, lo saltamos con una advertencia.
# ─────────────────────────────────────────────────────────────────────────────

def _safe_import_catalog(module: str, attr: str) -> list[dict]:
    """Importa ATTR del módulo de forma segura; devuelve [] si falla."""
    try:
        import importlib
        mod = importlib.import_module(module)
        return getattr(mod, attr, [])
    except Exception as exc:
        print(f"  ⚠️  No se pudo importar {module}.{attr}: {exc}")
        return []


def load_sectors(filter_sector: int | None = None) -> list[dict[str, Any]]:
    """
    Retorna la lista maestra de todos los challenges de DAKI EdTech.

    Cada dict tiene exactamente los campos que acepta el modelo Challenge
    (excepto `id`, que se genera en DB o se preserva en el upsert).

    Args:
        filter_sector: si se pasa, devuelve solo los challenges de ese sector_id.
    """
    catalog: list[dict[str, Any]] = []

    sources = [
        ("scripts.seed_sector_00", "SECTOR_00"),
        ("scripts.seed_sector_01", "SECTOR_01"),
        ("scripts.seed_sector_02", "SECTOR_02"),
        ("scripts.seed_sector_03", "SECTOR_03"),
        ("scripts.seed_sector_04", "SECTOR_04"),
        ("scripts.seed_sector_05", "SECTOR_05"),
        ("scripts.seed_sector_06", "SECTOR_06"),
        ("scripts.seed_sector_07", "SECTOR_07"),
        ("scripts.seed_sector_08", "SECTOR_08"),
        ("scripts.seed_sector_09", "SECTOR_09"),
        ("scripts.seed_sector_10", "SECTOR_10"),
    ]

    for module, attr in sources:
        batch = _safe_import_catalog(module, attr)
        if batch:
            catalog.extend(batch)
            sector_tag = batch[0].get("sector_id", "?")
            print(f"  📦  {attr:<12} → {len(batch):>3} misiones  (sector_id={sector_tag})")
        else:
            print(f"  ⚠️  {attr:<12} → 0 misiones (vacío o no encontrado)")

    if filter_sector is not None:
        catalog = [c for c in catalog if c.get("sector_id") == filter_sector]

    # ── Normalización: los campos *_json deben ser strings, no listas/dicts ──
    # Algunos seeds antiguos ya usan json.dumps(); los nuevos pasan listas crudas.
    JSON_FIELDS = ("test_inputs_json", "concepts_taught_json", "hints_json", "grid_map_json")
    for entry in catalog:
        for field in JSON_FIELDS:
            val = entry.get(field)
            if isinstance(val, (list, dict)):
                entry[field] = json.dumps(val, ensure_ascii=False)

    return catalog


# ─────────────────────────────────────────────────────────────────────────────
# Campos que se actualizan en un upsert (todo contenido editable).
# NO están: id (PK), sector_id y level_order (clave natural del upsert).
# ─────────────────────────────────────────────────────────────────────────────

UPSERTABLE_FIELDS = [
    "title",
    "description",
    "difficulty_tier",
    "difficulty",
    "base_xp_reward",
    "is_project",
    "telemetry_goal_time",
    "challenge_type",
    "phase",
    "concepts_taught_json",
    "initial_code",
    "expected_output",
    "test_inputs_json",
    "lore_briefing",
    "pedagogical_objective",
    "syntax_hint",
    "theory_content",
    "hints_json",
    "grid_map_json",
    "strict_match",
]


# ─────────────────────────────────────────────────────────────────────────────
# Lógica de upsert
# ─────────────────────────────────────────────────────────────────────────────

async def upsert_challenges(
    session: AsyncSession,
    catalog: list[dict[str, Any]],
    dry_run: bool = False,
) -> tuple[int, int]:
    """
    Itera el catálogo y hace upsert en DB.

    Clave natural: (sector_id, level_order).

    Returns:
        (created_count, updated_count)
    """
    # Carga todos los challenges existentes en memoria (evita N+1 queries)
    result = await session.execute(select(Challenge))
    existing: dict[tuple[int | str, int], Challenge] = {
        (ch.sector_id if ch.sector_id is not None else ch.codex_id, ch.level_order): ch
        for ch in result.scalars().all()
        if (ch.sector_id is not None or ch.codex_id is not None) and ch.level_order is not None
    }

    created = updated = skipped = 0
    errors: list[str] = []

    for data in catalog:
        sector_id   = data.get("sector_id")
        codex_id    = data.get("codex_id")
        level_order = data.get("level_order")
        title       = data.get("title", "?")

        if (sector_id is None and codex_id is None) or level_order is None:
            print(f"  ⚠️  SKIP — '{title}' no tiene sector_id/codex_id o level_order.")
            skipped += 1
            continue

        key = (sector_id if sector_id is not None else codex_id, level_order)

        try:
            if key in existing:
                # ── UPDATE ───────────────────────────────────────────────────
                challenge = existing[key]
                changed_fields: list[str] = []

                for field in UPSERTABLE_FIELDS:
                    if field not in data:
                        continue
                    new_val = data[field]
                    old_val = getattr(challenge, field, None)
                    if new_val != old_val:
                        if not dry_run:
                            setattr(challenge, field, new_val)
                        changed_fields.append(field)

                if changed_fields:
                    status = "[DRY-RUN] " if dry_run else ""
                    id_tag = f"S{sector_id:02d}" if sector_id is not None else f"C[{codex_id}]"
                    print(
                        f"  {status}🔄  {id_tag}-L{level_order:02d}  "
                        f"{title:<40}  ACTUALIZADO  ({', '.join(changed_fields[:4])}"
                        f"{'…' if len(changed_fields) > 4 else ''})"
                    )
                    updated += 1
                else:
                    id_tag = f"S{sector_id:02d}" if sector_id is not None else f"C[{codex_id}]"
                    print(
                        f"  ✅  {id_tag}-L{level_order:02d}  "
                        f"{title:<40}  sin cambios"
                    )

            else:
                # ── INSERT ───────────────────────────────────────────────────
                if not dry_run:
                    challenge = Challenge(**data)
                    session.add(challenge)

                status = "[DRY-RUN] " if dry_run else ""
                id_tag = f"S{sector_id:02d}" if sector_id is not None else f"C[{codex_id}]"
                print(
                    f"  {status}➕  {id_tag}-L{level_order:02d}  "
                    f"{title:<40}  CREADO  ({data.get('difficulty', '?').upper()}, "
                    f"{data.get('base_xp_reward', 0)} XP)"
                )
                created += 1

        except Exception as exc:
            id_tag = f"S{sector_id:02d}" if sector_id is not None else f"C[{codex_id}]"
            msg = f"{id_tag}-L{level_order:02d} '{title}' — {exc}"
            print(f"  ❌  ERROR: {msg}")
            errors.append(msg)

    if errors:
        print(f"\n  ⛔  {len(errors)} error(s) registrados. Ver detalle arriba.")
        if not dry_run:
            raise RuntimeError(f"{len(errors)} challenge(s) fallaron durante el upsert.")

    return created, updated


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────

async def seed(filter_sector: int | None = None, dry_run: bool = False) -> None:
    print("\n" + "═" * 65)
    print("  ⚡ DAKI EdTech — Orquestador de Inyección (seed_master)")
    print("═" * 65)

    if dry_run:
        print("  MODE: DRY-RUN — no se escribirá nada en la base de datos.\n")
    if filter_sector:
        print(f"  FILTRO: solo sector_id = {filter_sector}\n")

    # ── 1. Carga el catálogo ──────────────────────────────────────────────────
    print("📋  Cargando catálogo de misiones...\n")
    catalog = load_sectors(filter_sector=filter_sector)
    print(f"\n  Total misiones en catálogo: {len(catalog)}")

    if not catalog:
        print("\n⚠️  Catálogo vacío. Verifica que los archivos de seed existen.")
        return

    # ── 2. Conecta a la DB ────────────────────────────────────────────────────
    print(f"\n🔌  Conectando a la base de datos...")
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    SessionLocal = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )

    # ── 3. Upsert con rollback de seguridad ───────────────────────────────────
    created = updated = 0
    async with SessionLocal() as session:
        try:
            print(f"\n🌱  Iniciando upsert de {len(catalog)} misiones...\n")
            created, updated = await upsert_challenges(session, catalog, dry_run=dry_run)

            if not dry_run:
                await session.commit()
                print(f"\n  💾  Commit ejecutado correctamente.")

        except Exception as exc:
            if not dry_run:
                await session.rollback()
                print(f"\n  🔴  ROLLBACK ejecutado — la base de datos quedó intacta.")
            print(f"  Causa: {exc}")
            await engine.dispose()
            sys.exit(1)

    await engine.dispose()

    # ── 4. Resumen ────────────────────────────────────────────────────────────
    skipped = len(catalog) - created - updated
    # "skipped" here = unchanged rows (no delta), not actual skips
    unchanged = len(catalog) - created - updated

    print("\n" + "─" * 65)
    print("  📊  RESUMEN DE INYECCIÓN")
    print("─" * 65)
    print(f"  Total procesados : {len(catalog)}")
    print(f"  ➕  Creados       : {created}")
    print(f"  🔄  Actualizados  : {updated}")
    print(f"  ✅  Sin cambios   : {unchanged}")
    print("─" * 65)

    if dry_run:
        print("  ⚠️  DRY-RUN: ningún cambio fue persistido.")
    else:
        print("  ✅  Inyección completada. La telemetría existente fue preservada.")
    print("═" * 65 + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="DAKI EdTech — Master Seed (upsert seguro de todos los niveles)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Muestra el plan sin escribir en la base de datos.",
    )
    parser.add_argument(
        "--sector",
        type=int,
        default=None,
        metavar="N",
        help="Limita el upsert a un sector_id específico (ej. --sector 3).",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(seed(filter_sector=args.sector, dry_run=args.dry_run))
