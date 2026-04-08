"""
scripts/complete_founder.py — Completa TODAS las misiones para el usuario Founder.

Marca como completadas todas las misiones Python Core (incluyendo Contratos)
para el email especificado (default: adrianadroco@gmail.com).

No borra ni recrea el usuario — solo inserta los UserProgress y UserMetric
que faltan, y actualiza nivel + XP si el valor actual es menor.

Uso:
    # Dry-run (solo muestra qué haría):
    python -m scripts.complete_founder

    # Aplicar en BD:
    python -m scripts.complete_founder --no-dry-run

    # Otro email:
    python -m scripts.complete_founder --email otro@email.com --no-dry-run
"""

import argparse
import asyncio
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import or_, select

from app.core.database import AsyncSessionLocal, init_db
from app.models.challenge import Challenge
from app.models.user import User
from app.models.user_metrics import UserMetric
from app.models.user_progress import UserProgress
from app.services.gamification_service import GamificationEngine

# ─── Configuración ────────────────────────────────────────────────────────────

FOUNDER_EMAIL = "adrianadroco@gmail.com"

# XP mínimo garantizado para el founder (si ya tiene más, no se toca)
FOUNDER_MIN_XP = 50_000


# ─── Core ─────────────────────────────────────────────────────────────────────


async def run(email: str, dry_run: bool) -> None:
    await init_db()

    async with AsyncSessionLocal() as session:

        # ── Buscar founder ─────────────────────────────────────────────────────
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()

        if user is None:
            print(f"\n✗  Operador no encontrado: {email!r}")
            print("   Verificá que el email sea correcto y que el usuario exista en la BD.")
            sys.exit(1)

        print(f"\n  Founder encontrado: {user.callsign!r} (nivel {user.current_level}, XP {user.total_xp:,})")

        # ── Cargar TODOS los challenges Python Core (incluye Contratos) ────────
        python_only = or_(Challenge.codex_id.is_(None), Challenge.codex_id == "python_core")
        ch_result = await session.execute(
            select(Challenge)
            .where(python_only)
            .order_by(Challenge.level_order.nulls_last(), Challenge.base_xp_reward)
        )
        all_challenges = ch_result.scalars().all()

        if not all_challenges:
            print("⚠  No se encontraron challenges de Python Core en la BD.")
            sys.exit(1)

        # ── Challenges ya completados por el founder ───────────────────────────
        prog_result = await session.execute(
            select(UserProgress.challenge_id)
            .where(UserProgress.user_id == user.id, UserProgress.completed == True)  # noqa: E712
        )
        already_done = {row[0] for row in prog_result.all()}

        pending = [c for c in all_challenges if c.id not in already_done]

        print(f"\n  Total challenges Python Core : {len(all_challenges)}")
        print(f"  Ya completados               : {len(already_done)}")
        print(f"  A completar ahora            : {len(pending)}")

        if not pending:
            print("\n  ✅  El Founder ya tiene todos los challenges completados. Sin cambios.")
            return

        # ── Preview de XP y nivel resultante ──────────────────────────────────
        xp_from_pending = sum(c.base_xp_reward or 0 for c in pending)
        new_xp          = max(user.total_xp + xp_from_pending, FOUNDER_MIN_XP)
        new_level       = max(GamificationEngine.calculate_level_from_xp(new_xp), len(all_challenges) + 1)

        print(f"\n  XP actual       : {user.total_xp:>10,}")
        print(f"  XP de pendientes: {xp_from_pending:>10,}")
        print(f"  XP resultante   : {new_xp:>10,}  (mínimo garantizado: {FOUNDER_MIN_XP:,})")
        print(f"  Nivel resultante: {new_level}")

        if dry_run:
            print("\n[DRY RUN] Sin cambios. Pasá --no-dry-run para aplicar.\n")
            return

        # ── Insertar UserProgress y UserMetric para los pendientes ─────────────
        now = datetime.now(timezone.utc)
        n   = len(pending)

        for i, challenge in enumerate(pending):
            is_boss = challenge.challenge_type == "boss" if challenge.challenge_type else False
            codex   = challenge.codex_id or "python_core"

            # Stats de élite distribuidas en los últimos 30 días
            attempts = 1 if i % 5 != 3 else 2
            hints    = 0 if i < n * 0.7 else (1 if not is_boss else 0)
            time_ms  = max(45_000, (180 - (i % 180)) * 800)

            days_ago     = (n - i) * (30.0 / max(n, 1))
            completed_at = now - timedelta(days=days_ago)

            session.add(UserProgress(
                user_id=user.id,
                challenge_id=challenge.id,
                completed=True,
                boss_completed=is_boss,
                attempts=attempts,
                hints_used=hints,
                completed_at=completed_at,
                codex_id=codex,
            ))

            session.add(UserMetric(
                user_id=user.id,
                challenge_id=challenge.id,
                attempts=attempts,
                hints_used=hints,
                time_spent_ms=time_ms,
                status="success",
                syntax_errors_log="[]",
                last_attempt_at=completed_at,
            ))

        # ── Actualizar XP y nivel del founder ─────────────────────────────────
        user.total_xp      = new_xp
        user.current_level = new_level

        await session.commit()
        await session.refresh(user)

        # ── Resultado ──────────────────────────────────────────────────────────
        w = 58
        print(f"\n{'=' * w}")
        print(f"  ✅  FOUNDER COMPLETADO EXITOSAMENTE")
        print(f"{'=' * w}")
        print(f"  Callsign : {user.callsign}")
        print(f"  Email    : {email}")
        print(f"  Nivel    : {user.current_level}  |  XP: {user.total_xp:,}")
        print(f"  Progreso : {len(all_challenges)} challenges completados (TODOS)")
        print(f"  Contratos: ✓ C50 / C60 / C70 / C130 / C175 desbloqueados")
        print(f"\n  El Founder debe cerrar sesión y volver a entrar para")
        print(f"  que el JWT refleje el nuevo nivel.")
        print(f"{'=' * w}\n")


# ─── CLI ──────────────────────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Completa TODAS las misiones Python Core para el Founder.",
    )
    parser.add_argument(
        "--email", default=FOUNDER_EMAIL,
        help=f"Email del Founder (default: {FOUNDER_EMAIL})",
    )
    parser.add_argument(
        "--dry-run", action="store_true", default=True,
        help="Muestra qué se haría sin tocar la BD (default: True).",
    )
    parser.add_argument(
        "--no-dry-run", dest="dry_run", action="store_false",
        help="Aplica los cambios en la BD.",
    )
    args = parser.parse_args()

    asyncio.run(run(email=args.email, dry_run=args.dry_run))


if __name__ == "__main__":
    main()
