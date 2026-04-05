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

from sqlalchemy import text

# Asegura que el import funcione desde la raíz del proyecto
sys.path.insert(0, ".")

from app.core.database import AsyncSessionLocal

# Todos los codex_id no-Python conocidos (incluyendo variantes sin sufijo _v1)
NON_PYTHON_CODEX = (
    "tpm_mastery_v1",
    "tpm_mastery",
    "sales_mastery_v1",
    "qa_senior_architect",
    "qa_automation_ops",
)


async def run(dry_run: bool) -> None:
    async with AsyncSessionLocal() as db:
        placeholders = ", ".join(f"'{c}'" for c in NON_PYTHON_CODEX)

        # ── Contar desafíos a eliminar ────────────────────────────────────────
        count_del = await db.execute(
            text(f"SELECT COUNT(*) FROM challenges WHERE codex_id IN ({placeholders})")
        )
        to_delete = count_del.scalar_one()

        count_keep = await db.execute(
            text("SELECT COUNT(*) FROM challenges WHERE codex_id IS NULL OR codex_id = 'python_core'")
        )
        to_keep = count_keep.scalar_one()

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

        # ── 1. Eliminar UserProgress de challenges no-Python ──────────────────
        del_prog = await db.execute(text(f"""
            DELETE FROM user_progress
            WHERE challenge_id IN (
                SELECT id FROM challenges WHERE codex_id IN ({placeholders})
            )
        """))
        print(f"\n  UserProgress eliminados : {del_prog.rowcount}")

        # ── 2. Eliminar challenges no-Python ──────────────────────────────────
        del_ch = await db.execute(text(f"""
            DELETE FROM challenges WHERE codex_id IN ({placeholders})
        """))
        print(f"  Challenges eliminados  : {del_ch.rowcount}")

        await db.commit()
        print("\n[DONE] Limpieza completada. Solo queda Python Core.\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Elimina contenido no-Python de la BD")
    parser.add_argument("--dry-run", action="store_true", help="Solo cuenta, no borra")
    args = parser.parse_args()

    asyncio.run(run(dry_run=args.dry_run))


if __name__ == "__main__":
    main()
