"""
seed_incursions.py — Datos iniciales del Catálogo de Incursiones (D021)

Inserta 4 Incursiones en la BD:
  1 ACTIVE    — "Operación Vanguardia: Fundamentos de Élite"  (Python Core)
  3 ENCRYPTED — TPM Mastery, Ciberseguridad Red Team, Technical Sales Mastery

Lógica: UPSERT por slug — idempotente.
  Si la fila ya existe → actualiza titulo, descripcion, color_acento, icono, ruta.
  El campo `status` NUNCA se sobreescribe si ya existe en la BD,
  para preservar activaciones manuales hechas en producción.

Uso standalone:
  python -m scripts.seed_incursions

Uso programático (desde main.py):
  from scripts.seed_incursions import seed
  await seed()
"""

from __future__ import annotations

import asyncio

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert as pg_insert

from app.core.database import AsyncSessionLocal, init_db
from app.models.incursion import Incursion  # noqa: F401 — registra el modelo en Base


# ─── Datos canónicos ──────────────────────────────────────────────────────────

INCURSIONS: list[dict] = [
    {
        "slug":             "python-core",
        "titulo":           "Operación Vanguardia: Fundamentos de Élite",
        "descripcion": (
            "El protocolo de iniciación del Nexo. "
            "Domina Python desde los fundamentos hasta la arquitectura de sistemas. "
            "100 misiones. 4 sectores. 1 Boss Final. "
            "La base de todo lo que viene después."
        ),
        "status":           "ACTIVE",
        "system_prompt_id": "python",
        "ruta":             "/misiones",
        "color_acento":     "#00FF41",
        "icono":            "⬡",
        "orden":            1,
    },
]


# ─── Función principal ────────────────────────────────────────────────────────

async def seed() -> None:
    """
    UPSERT idempotente de las Incursiones canónicas.

    Todos los campos —incluyendo `status`— se sincronizan con INCURSIONS en cada
    ejecución. Esto permite abrir o cerrar Incursiones editando este archivo y
    volviendo a desplegar sin intervención manual en la BD.
    """
    async with AsyncSessionLocal() as session:
        for data in INCURSIONS:
            result = await session.execute(
                select(Incursion).where(Incursion.slug == data["slug"])
            )
            existing = result.scalar_one_or_none()

            if existing is None:
                # INSERT — primera vez
                session.add(Incursion(**data))
                print(f"  ➕ [seed_incursions] INSERT: {data['slug']} [{data['status']}]")
            else:
                # UPDATE — sincroniza todos los campos incluyendo status y D030
                await session.execute(
                    update(Incursion)
                    .where(Incursion.slug == data["slug"])
                    .values(
                        titulo                       = data["titulo"],
                        descripcion                  = data["descripcion"],
                        system_prompt_id             = data["system_prompt_id"],
                        ruta                         = data["ruta"],
                        color_acento                 = data["color_acento"],
                        icono                        = data["icono"],
                        orden                        = data["orden"],
                        status                       = data["status"],
                        prerequisite_incursion_slug  = data.get("prerequisite_incursion_slug"),
                        total_levels                 = data.get("total_levels"),
                    )
                )
                print(f"  ♻️  [seed_incursions] UPDATE: {data['slug']} → status={data['status']}")

        await session.commit()

    print("✅  [seed_incursions] Catálogo de Incursiones sincronizado.")


# ─── Entrada directa ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    async def _main() -> None:
        await init_db()
        await seed()

    asyncio.run(_main())
