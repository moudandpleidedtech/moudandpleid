"""
cleanup_non_python.py — Elimina todo el contenido no-Python de la BD.

Codex IDs a eliminar:
  - 'tpm_mastery_v1'
  - 'sales_mastery_v1'
  - 'qa_senior_architect'
  - 'qa_automation_ops'

Se preserva:
  - codex_id IS NULL  (Python Core legacy — sectores 0–10)
  - codex_id = 'python_core' (Python Core explícito)

Uso:
  python scripts/cleanup_non_python.py [--dry-run]

  --dry-run  Solo muestra cuántos registros se eliminarían, sin borrar nada.
"""

import argparse
import asyncio
import sys

from sqlalchemy import delete, func, or_, select

# Asegura que el import funcione desde la raíz del proyecto
sys.path.insert(0, ".")

from app.core.database import AsyncSessionLocal
from app.models.challenge import Challenge
from app.models.user_progress import UserProgress

NON_PYTHON_CODEX = [
    "tpm_mastery_v1",
    "sales_mastery_v1",
    "qa_senior_architect",
    "qa_automation_ops",
]


async def run(dry_run: bool) -> None:
    async with AsyncSessionLocal() as db:
        # ── Contar desafíos a eliminar ────────────────────────────────────────
        count_result = await db.execute(
            select(func.count()).select_from(Challenge)
            .where(Challenge.codex_id.in_(NON_PYTHON_CODEX))
        )
        to_delete = count_result.scalar_one()

        # ── Contar desafíos Python que se conservan ───────────────────────────
        python_only = or_(Challenge.codex_id.is_(None), Challenge.codex_id == "python_core")
        keep_result = await db.execute(
            select(func.count()).select_from(Challenge).where(python_only)
        )
        to_keep = keep_result.scalar_one()

        print(f"\n{'='*50}")
        print(f"  Challenges a ELIMINAR : {to_delete}")
        print(f"  Challenges a CONSERVAR: {to_keep}  (Python Core)")
        print(f"{'='*50}")

        if dry_run:
            print("\n[DRY-RUN] Sin cambios en la BD. Pasa sin --dry-run para ejecutar.\n")
            return

        if to_delete == 0:
            print("\n[OK] Nada que eliminar. La BD ya está limpia.\n")
            return

        # ── Obtener IDs de challenges no-Python ───────────────────────────────
        ids_result = await db.execute(
            select(Challenge.id).where(Challenge.codex_id.in_(NON_PYTHON_CODEX))
        )
        ids_to_delete = [row[0] for row in ids_result.all()]

        # ── 1. Eliminar UserProgress asociados ────────────────────────────────
        del_progress = await db.execute(
            delete(UserProgress).where(UserProgress.challenge_id.in_(ids_to_delete))
        )
        print(f"\n  UserProgress eliminados : {del_progress.rowcount}")

        # ── 2. Eliminar las challenges ─────────────────────────────────────────
        del_challenges = await db.execute(
            delete(Challenge).where(Challenge.id.in_(ids_to_delete))
        )
        print(f"  Challenges eliminados  : {del_challenges.rowcount}")

        await db.commit()
        print("\n[DONE] Limpieza completada. Solo queda Python Core.\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Elimina contenido no-Python de la BD")
    parser.add_argument("--dry-run", action="store_true", help="Solo cuenta, no borra")
    args = parser.parse_args()

    asyncio.run(run(dry_run=args.dry_run))


if __name__ == "__main__":
    main()
