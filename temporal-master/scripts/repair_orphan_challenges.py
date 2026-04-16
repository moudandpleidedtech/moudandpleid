"""
repair_orphan_challenges.py — Repara challenges huérfanos preservando UserProgress.

Para cada challenge en DB cuya posición (sector_id, level_order) NO está en el
catálogo canónico:
  - Si tiene UserProgress: busca su "gemelo canónico" por título,
    borra el gemelo (0 UserProgress) y mueve el huérfano a la posición correcta.
  - Si no tiene UserProgress: lo borra directamente.

Con --force: borra TODOS los huérfanos restantes (incluso los con UserProgress
que no se pudieron resolver automáticamente). Usar junto con --apply.
Después de --force, correr complete_founder --no-dry-run para restaurar progreso.

Uso:
    python -m scripts.repair_orphan_challenges                    # dry-run
    python -m scripts.repair_orphan_challenges --apply            # aplica cambios (modo seguro)
    python -m scripts.repair_orphan_challenges --apply --force    # elimina TODO lo que sobra
"""

import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.models.user import User          # noqa: F401 — must load before UserProgress
from app.models.challenge import Challenge
from app.models.user_progress import UserProgress
from scripts.seed_master import load_sectors


async def run(apply: bool, force: bool = False) -> None:
    # ── 1. Posiciones canónicas del catálogo ──────────────────────────────────
    catalog = load_sectors()
    canon_positions: set[tuple] = {
        (c["sector_id"], c["level_order"])
        for c in catalog
        if c.get("sector_id") is not None and c.get("level_order") is not None
    }
    # Mapa título → posición canónica
    title_to_canon: dict[str, tuple] = {
        c["title"]: (c["sector_id"], c["level_order"])
        for c in catalog
        if c.get("title") and c.get("sector_id") is not None
    }
    print(f"\nPosiciones canónicas : {len(canon_positions)}")

    # ── 2. Conectar a DB ──────────────────────────────────────────────────────
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    Session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with Session() as session:
        # Todos los challenges
        res = await session.execute(select(Challenge))
        all_ch: list[Challenge] = res.scalars().all()
        print(f"Challenges en DB     : {len(all_ch)}")

        # Índice por (sector_id, level_order) → challenge
        pos_to_ch: dict[tuple, Challenge] = {}
        for ch in all_ch:
            if ch.sector_id is not None and ch.level_order is not None:
                pos_to_ch[(ch.sector_id, ch.level_order)] = ch

        # Identificar huérfanos
        orphans = [
            ch for ch in all_ch
            if ch.sector_id is not None
            and (ch.sector_id, ch.level_order) not in canon_positions
        ]

        # Contar UserProgress por orphan
        to_move:   list[tuple[Challenge, tuple]] = []   # (orphan, canon_pos)
        to_delete: list[Challenge] = []
        cant_fix:  list[Challenge] = []

        for ch in orphans:
            r = await session.execute(
                select(func.count()).where(UserProgress.challenge_id == ch.id)
            )
            prog_count = r.scalar_one()

            if prog_count == 0:
                to_delete.append(ch)
                continue

            # Tiene UserProgress → buscar posición canónica por título
            canon_pos = title_to_canon.get(ch.title)
            if canon_pos is None:
                cant_fix.append(ch)
                print(f"  SIN MATCH en catálogo: '{ch.title}' (S{ch.sector_id} L{ch.level_order})")
                continue

            # Verificar que el gemelo canónico exista y no tenga UserProgress
            twin = pos_to_ch.get(canon_pos)
            if twin is None:
                # La posición canónica está vacía → solo mover
                to_move.append((ch, canon_pos))
            else:
                r2 = await session.execute(
                    select(func.count()).where(UserProgress.challenge_id == twin.id)
                )
                twin_prog = r2.scalar_one()
                if twin_prog == 0:
                    to_move.append((ch, canon_pos))
                else:
                    cant_fix.append(ch)
                    print(f"  CONFLICTO: '{ch.title}' — gemelo en {canon_pos} también tiene UserProgress")

        # ── Resumen ────────────────────────────────────────────────────────────
        print(f"\n  Borrar  (sin UserProgress) : {len(to_delete)}")
        for ch in to_delete:
            print(f"    S{ch.sector_id:02d} L{ch.level_order:03d}  {ch.title[:50]}")

        print(f"\n  Mover   (con UserProgress) : {len(to_move)}")
        for ch, canon in to_move:
            twin = pos_to_ch.get(canon)
            twin_info = f"→ borra gemelo {canon}" if twin else f"→ posición libre {canon}"
            print(f"    S{ch.sector_id:02d} L{ch.level_order:03d}  {ch.title[:40]}  {twin_info}")

        if cant_fix:
            print(f"\n  Sin solución automática    : {len(cant_fix)}")
            for ch in cant_fix:
                r = await session.execute(
                    select(func.count()).where(UserProgress.challenge_id == ch.id)
                )
                prog_count = r.scalar_one()
                print(f"    S{ch.sector_id:02d} L{ch.level_order:03d}  {ch.title[:40]}  ({prog_count} progress entries)")
            if force:
                print(f"  --force: estos {len(cant_fix)} también serán eliminados (UserProgress incluido)")

        twins_to_delete = sum(1 for ch, canon in to_move if pos_to_ch.get(canon))
        force_delete_count = len(cant_fix) if force else 0
        expected_final = len(all_ch) - len(to_delete) - twins_to_delete - force_delete_count
        print(f"\n  Challenges esperados post-repair: {expected_final}")

        if not apply:
            hint = " --force" if force else ""
            print(f"\n[DRY-RUN] Pasar --apply{hint} para ejecutar los cambios.")
            await engine.dispose()
            return

        # ── Aplicar ────────────────────────────────────────────────────────────
        deleted = 0
        moved = 0

        # Borrar sin UserProgress
        for ch in to_delete:
            await session.delete(ch)
            deleted += 1

        # Mover con UserProgress
        for ch, (canon_sid, canon_lo) in to_move:
            twin = pos_to_ch.get((canon_sid, canon_lo))
            if twin:
                await session.delete(twin)
                deleted += 1
            ch.sector_id   = canon_sid
            ch.level_order = canon_lo
            moved += 1

        # --force: borrar los que no se pudieron resolver automáticamente
        if force and cant_fix:
            for ch in cant_fix:
                # Primero borrar UserProgress asociado para evitar FK violation
                await session.execute(
                    delete(UserProgress).where(UserProgress.challenge_id == ch.id)
                )
                await session.delete(ch)
                deleted += 1

        await session.commit()

        # Verificar total final
        res2 = await session.execute(select(func.count()).select_from(Challenge))
        final_count = res2.scalar_one()

        print(f"\n  Borrados : {deleted}")
        print(f"  Movidos  : {moved}")
        print(f"  Total DB : {final_count}")
        if final_count == len(canon_positions):
            print(f"  OK — DB alineada con el catálogo ({final_count} challenges)")
        else:
            diff = final_count - len(canon_positions)
            print(f"  ATENCION — quedan {diff} extra sin resolver (ver cant_fix arriba)")

    await engine.dispose()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true",
                        help="Aplica los cambios (sin esto es dry-run)")
    parser.add_argument("--force", action="store_true",
                        help="Elimina también los huérfanos irresolubles (borra su UserProgress)")
    args = parser.parse_args()
    asyncio.run(run(apply=args.apply, force=args.force))
