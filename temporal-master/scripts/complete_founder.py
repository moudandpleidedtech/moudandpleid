"""
scripts/complete_founder.py — Completa TODAS las misiones, logros y medallas del Founder.

Para el email especificado (default: adrianadroco@gmail.com):
  1. Marca como completadas todas las misiones Python Core + Contratos.
  2. Otorga los 35 logros del catálogo (UserAchievement).
  3. Añade la medalla SYSTEM_KILLER al badges_json del usuario.
  4. Actualiza nivel y XP al máximo alcanzable.

No borra ni recrea el usuario — solo inserta lo que falte (idempotente).

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
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import or_, select

from app.core.database import AsyncSessionLocal, init_db
from app.models.achievement import UserAchievement
from app.models.challenge import Challenge
from app.models.user import User
from app.models.user_metrics import UserMetric
from app.models.user_progress import UserProgress
from app.services.achievement_service import ACHIEVEMENTS
from app.services.gamification_service import GamificationEngine

# ─── Configuración ────────────────────────────────────────────────────────────

FOUNDER_EMAIL = "adrianadroco@gmail.com"

# XP mínimo garantizado (si el founder ya tiene más, no se toca)
FOUNDER_MIN_XP = 50_000

# Racha mínima garantizada
FOUNDER_MIN_STREAK = 30

# Todos los badges que puede existir en el sistema
ALL_BADGES = ["SYSTEM_KILLER"]


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

        print(f"\n  Founder encontrado: {user.callsign!r}")
        print(f"  Nivel: {user.current_level}  |  XP: {user.total_xp:,}  |  Racha: {user.streak_days}d")

        # ──────────────────────────────────────────────────────────────────────
        # 1. MISIONES — Challenges Python Core (incluye Contratos)
        # ──────────────────────────────────────────────────────────────────────
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

        prog_result = await session.execute(
            select(UserProgress.challenge_id)
            .where(UserProgress.user_id == user.id, UserProgress.completed == True)  # noqa: E712
        )
        already_done = {row[0] for row in prog_result.all()}
        pending_challenges = [c for c in all_challenges if c.id not in already_done]

        # ──────────────────────────────────────────────────────────────────────
        # 2. LOGROS — UserAchievement
        # ──────────────────────────────────────────────────────────────────────
        ach_result = await session.execute(
            select(UserAchievement.achievement_id)
            .where(UserAchievement.user_id == user.id)
        )
        already_unlocked = {row[0] for row in ach_result.all()}
        pending_achievements = [aid for aid in ACHIEVEMENTS if aid not in already_unlocked]

        # ──────────────────────────────────────────────────────────────────────
        # 3. BADGES — badges_json
        # ──────────────────────────────────────────────────────────────────────
        try:
            current_badges: list[str] = json.loads(user.badges_json or "[]")
        except (ValueError, TypeError):
            current_badges = []
        pending_badges = [b for b in ALL_BADGES if b not in current_badges]

        # ──────────────────────────────────────────────────────────────────────
        # Preview
        # ──────────────────────────────────────────────────────────────────────
        xp_from_pending = sum(c.base_xp_reward or 0 for c in pending_challenges)
        xp_from_achievements = sum(
            ACHIEVEMENTS[aid]["xp_bonus"] for aid in pending_achievements
        )
        new_xp    = max(user.total_xp + xp_from_pending + xp_from_achievements, FOUNDER_MIN_XP)
        new_level = max(
            GamificationEngine.calculate_level_from_xp(new_xp),
            len(all_challenges) + 1,
        )
        new_streak = max(user.streak_days, FOUNDER_MIN_STREAK)

        print(f"\n  ── MISIONES ──────────────────────────────────────────")
        print(f"  Total Python Core       : {len(all_challenges)}")
        print(f"  Ya completadas          : {len(already_done)}")
        print(f"  A completar             : {len(pending_challenges)}")

        print(f"\n  ── LOGROS ────────────────────────────────────────────")
        print(f"  Total en catálogo       : {len(ACHIEVEMENTS)}")
        print(f"  Ya desbloqueados        : {len(already_unlocked)}")
        print(f"  A otorgar               : {len(pending_achievements)}")
        if pending_achievements:
            for aid in pending_achievements:
                a = ACHIEVEMENTS[aid]
                print(f"    {a['icon']}  {a['name']} (+{a['xp_bonus']} XP)")

        print(f"\n  ── MEDALLAS (badges_json) ────────────────────────────")
        print(f"  Actuales                : {current_badges or ['ninguna']}")
        print(f"  A añadir                : {pending_badges or ['ninguna']}")

        print(f"\n  ── XP / NIVEL / RACHA ───────────────────────────────")
        print(f"  XP actual               : {user.total_xp:>10,}")
        print(f"  XP de misiones nuevas   : {xp_from_pending:>10,}")
        print(f"  XP de logros nuevos     : {xp_from_achievements:>10,}")
        print(f"  XP resultante           : {new_xp:>10,}")
        print(f"  Nivel resultante        : {new_level}")
        print(f"  Racha resultante        : {new_streak}d")

        if dry_run:
            print("\n[DRY RUN] Sin cambios. Pasá --no-dry-run para aplicar.\n")
            return

        now = datetime.now(timezone.utc)

        # ── Insertar misiones pendientes ───────────────────────────────────────
        n = len(pending_challenges)
        for i, challenge in enumerate(pending_challenges):
            is_boss = challenge.challenge_type == "boss" if challenge.challenge_type else False
            codex   = challenge.codex_id or "python_core"

            attempts     = 1 if i % 5 != 3 else 2
            hints        = 0 if i < n * 0.7 else (1 if not is_boss else 0)
            time_ms      = max(45_000, (180 - (i % 180)) * 800)
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

        # ── Insertar logros pendientes ─────────────────────────────────────────
        for i, achievement_id in enumerate(pending_achievements):
            # Distribuir unlocked_at a lo largo de los últimos 30 días
            days_ago     = (len(pending_achievements) - i) * (30.0 / max(len(pending_achievements), 1))
            unlocked_at  = now - timedelta(days=days_ago)
            session.add(UserAchievement(
                user_id=user.id,
                achievement_id=achievement_id,
                unlocked_at=unlocked_at,
            ))

        # ── Añadir badges al JSON ──────────────────────────────────────────────
        if pending_badges:
            updated_badges = current_badges + pending_badges
            user.badges_json = json.dumps(updated_badges)

        # ── Actualizar XP, nivel y racha ──────────────────────────────────────
        user.total_xp      = new_xp
        user.current_level = new_level
        user.streak_days   = new_streak

        await session.commit()
        await session.refresh(user)

        # ── Resultado final ────────────────────────────────────────────────────
        final_badges: list[str] = json.loads(user.badges_json or "[]")
        w = 60
        print(f"\n{'=' * w}")
        print(f"  ✅  FOUNDER COMPLETADO — TODAS LAS DISTINCIONES OTORGADAS")
        print(f"{'=' * w}")
        print(f"  Callsign  : {user.callsign}")
        print(f"  Email     : {email}")
        print(f"  Nivel     : {user.current_level}  |  XP: {user.total_xp:,}  |  Racha: {user.streak_days}d")
        print(f"  Misiones  : {len(all_challenges)} completadas (TODAS — incluye 5 Contratos)")
        print(f"  Logros    : {len(ACHIEVEMENTS)} / {len(ACHIEVEMENTS)} desbloqueados")
        print(f"  Medallas  : {final_badges}")
        print(f"\n  El Founder debe cerrar sesión y volver a entrar para")
        print(f"  que el JWT refleje el nuevo estado.")
        print(f"{'=' * w}\n")


# ─── CLI ──────────────────────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Completa TODAS las misiones, logros y medallas para el Founder.",
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
