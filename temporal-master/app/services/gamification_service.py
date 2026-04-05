import math
import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.challenge import Challenge, DifficultyTier
from app.models.user import User
from app.models.user_progress import UserProgress
from app.schemas.gamification import ChallengeAttemptResult
from app.services import activity_service, mastery_service
from app.services.memory_service import record_event
from app.services.rank_service import compute_rank, rank_promotes

EFFICIENCY_BONUS_RATE = 0.20
EFFICIENCY_TIME_THRESHOLD_MS = 50


class GamificationEngine:

    @staticmethod
    def calculate_level_from_xp(total_xp: int) -> int:
        """Level = floor(0.1 * sqrt(XP)) + 1"""
        if total_xp < 0:
            total_xp = 0
        return math.floor(0.1 * math.sqrt(total_xp)) + 1

    @staticmethod
    def _calculate_xp_reward(
        base_xp: int, difficulty_tier: DifficultyTier, execution_time_ms: int
    ) -> tuple[int, bool]:
        """Returns (total_xp, efficiency_bonus_applied)."""
        efficiency_bonus = (
            difficulty_tier == DifficultyTier.BEGINNER
            and execution_time_ms < EFFICIENCY_TIME_THRESHOLD_MS
        )
        bonus = math.floor(base_xp * EFFICIENCY_BONUS_RATE) if efficiency_bonus else 0
        return base_xp + bonus, efficiency_bonus

    async def process_challenge_completion(
        self,
        db: AsyncSession,
        user_id: uuid.UUID,
        challenge_id: uuid.UUID,
        is_success: bool,
        execution_time_ms: int,
        syntax_errors_count: int = 0,
        hints_used_this_session: int = 0,
    ) -> ChallengeAttemptResult:
        user = await db.get(User, user_id)
        if user is None:
            raise ValueError(f"User {user_id} not found")

        challenge = await db.get(Challenge, challenge_id)
        if challenge is None:
            raise ValueError(f"Challenge {challenge_id} not found")

        # Fetch or create UserProgress — with_for_update() previene race condition
        # de doble-submit que otorgaría XP dos veces en submits simultáneos.
        result = await db.execute(
            select(UserProgress).where(
                UserProgress.user_id == user_id,
                UserProgress.challenge_id == challenge_id,
            ).with_for_update()
        )
        progress = result.scalar_one_or_none()

        if progress is None:
            progress = UserProgress(
                user_id=user_id,
                challenge_id=challenge_id,
                attempts=0,
                hints_used=0,
                syntax_errors_total=0,
                completed=False,
            )
            db.add(progress)

        progress.attempts += 1
        progress.syntax_errors_total += syntax_errors_count
        # hints_used accumulates across hint-endpoint calls; only add session hints
        # if they weren't already counted there (compiler can pass delta of 0)
        if hints_used_this_session > 0:
            progress.hints_used = max(progress.hints_used, hints_used_this_session)

        already_completed = progress.completed
        xp_earned = 0
        efficiency_bonus_applied = False
        level_up = False

        if is_success and not already_completed:
            xp_earned, efficiency_bonus_applied = self._calculate_xp_reward(
                challenge.base_xp_reward, challenge.difficulty_tier, execution_time_ms
            )
            progress.completed = True
            progress.completed_at = datetime.now(timezone.utc)

            old_level = user.current_level
            user.total_xp += xp_earned
            user.current_level = self.calculate_level_from_xp(user.total_xp)
            level_up = user.current_level > old_level

            # ── Rango y points curriculares ───────────────────────────────────
            new_rank = compute_rank(challenge.level_order)
            old_rank = user.current_rank
            if rank_promotes(old_rank, new_rank):
                user.current_rank = new_rank
                await record_event(
                    db=db,
                    user_id=user_id,
                    event_type="subida_rango",
                    context_data={"old_rank": old_rank, "new_rank": new_rank},
                    challenge_id=challenge_id,
                )
            user.points += challenge.level_order or 0

            # ── Memoria: exito_rapido si es el primer intento ─────────────────
            if progress.attempts == 1:
                await record_event(
                    db=db,
                    user_id=user_id,
                    event_type="exito_rapido",
                    context_data={"challenge_title": challenge.title},
                    challenge_id=challenge_id,
                )

            # Actualiza mapa de maestría con esfuerzo cognitivo real
            await mastery_service.update_mastery_on_completion(
                db=db,
                user_id=user_id,
                concepts_taught_json=challenge.concepts_taught_json,
                attempts=progress.attempts,
                hints_used=progress.hints_used,
            )

        await db.flush()

        # Emitir eventos de actividad global (fire-and-forget)
        if is_success and not already_completed:
            await activity_service.emit_challenge_complete(user.callsign, challenge.title)
            if level_up:
                await activity_service.emit_level_up(user.callsign, user.current_level)

        return ChallengeAttemptResult(
            user_id=user_id,
            challenge_id=challenge_id,
            is_success=is_success,
            attempts=progress.attempts,
            xp_earned=xp_earned,
            efficiency_bonus_applied=efficiency_bonus_applied,
            already_completed=already_completed,
            level_up=level_up,
            new_level=user.current_level,
            new_total_xp=user.total_xp,
        )


gamification_engine = GamificationEngine()
