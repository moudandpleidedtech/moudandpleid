"""
cleanup_orphan_challenges.py — Elimina challenges huérfanos de la DB.

"Huérfano" = challenge en DB cuya posición (sector_id, level_order)
NO existe en el catálogo canónico del seed_master.

Seguro: solo borra challenges sin UserProgress asociado.
Reporta los que SÍ tienen UserProgress para revisión manual.

Uso:
    python -m scripts.cleanup_orphan_challenges            # dry-run
    python -m scripts.cleanup_orphan_challenges --apply    # aplica borrado
"""

import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.models.challenge import Challenge
from app.models.user_progress import UserProgress
from scripts.seed_master import load_sectors


async def run(apply: bool) -> None:
    # 1. Posiciones canónicas del catálogo
    catalog = load_sectors()
    canon: set[tuple] = {
        (c["sector_id"], c["level_order"])
        for c in catalog
        if c.get("sector_id") is not None and c.get("level_order") is not None
    }
    print(f"\nPosiciones canónicas en seed catalog: {len(canon)}")

    # 2. Conectar a DB
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    Session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with Session() as session:
        # 3. Todos los challenges
        res = await session.execute(select(Challenge))
        all_ch = res.scalars().all()
        print(f"Challenges en DB: {len(all_ch)}")

        # 4. Identificar huérfanos
        orphans = [
            ch for ch in all_ch
            if ch.sector_id is not None
            and (ch.sector_id, ch.level_order) not in canon
        ]
        print(f"Huérfanos (posición no canónica): {len(orphans)}")

        # 5. Separar con/sin UserProgress
        safe_to_delete = []
        has_progress = []
        for ch in orphans:
            r = await session.execute(
                select(func.count()).where(UserProgress.challenge_id == ch.id)
            )
            count = r.scalar_one()
            if count == 0:
                safe_to_delete.append(ch)
            else:
                has_progress.append((ch, count))

        print(f"\n  Sin UserProgress (se pueden borrar): {len(safe_to_delete)}")
        for ch in safe_to_delete[:5]:
            print(f"    S{ch.sector_id:02d} L{ch.level_order:03d}  {ch.title[:50]}")
        if len(safe_to_delete) > 5:
            print(f"    ... y {len(safe_to_delete) - 5} más")

        if has_progress:
            print(f"\n  CON UserProgress (NO se borran — revisar manual): {len(has_progress)}")
            for ch, cnt in has_progress:
                print(f"    S{ch.sector_id:02d} L{ch.level_order:03d}  {ch.title[:40]}  ({cnt} progress entries)")

        if not apply:
            print("\n[DRY-RUN] Pasar --apply para ejecutar el borrado.")
            await engine.dispose()
            return

        # 6. Borrar los seguros
        deleted = 0
        for ch in safe_to_delete:
            await session.delete(ch)
            deleted += 1

        await session.commit()
        print(f"\n  Eliminados: {deleted} challenges huérfanos.")
        remaining = len(all_ch) - deleted
        print(f"  Challenges restantes en DB: {remaining}")
        if remaining == len(canon):
            print(f"  OK — DB alineada con el catálogo ({remaining} == {len(canon)})")
        else:
            print(f"  ATENCION — quedan {remaining - len(canon)} extra con UserProgress (ver arriba)")

    await engine.dispose()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Aplica el borrado (sin esto es dry-run)")
    args = parser.parse_args()
    asyncio.run(run(apply=args.apply))
