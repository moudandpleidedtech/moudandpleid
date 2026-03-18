import json
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy import nulls_last, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.challenge import Challenge
from app.models.user_progress import UserProgress

router = APIRouter()


class ChallengeOut(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    difficulty_tier: int
    base_xp_reward: int
    initial_code: str
    test_inputs: list[str]
    completed: bool
    attempts: int
    unlocked: bool
    # Curriculum fields (Prompt 12)
    level_order: Optional[int]
    phase: Optional[str]
    concepts_taught: list[str]
    challenge_type: str
    # Theory content (Prompt 18)
    theory_content: Optional[str]
    # Mission briefing (Prompt B)
    lore_briefing: Optional[str]
    pedagogical_objective: Optional[str]
    syntax_hint: Optional[str]
    hints: list[str]
    model_config = ConfigDict(from_attributes=True)


def _build_out(
    challenge: Challenge,
    completed: bool,
    attempts: int,
    unlocked: bool,
) -> ChallengeOut:
    return ChallengeOut(
        id=challenge.id,
        title=challenge.title,
        description=challenge.description,
        difficulty_tier=challenge.difficulty_tier.value,
        base_xp_reward=challenge.base_xp_reward,
        initial_code=challenge.initial_code,
        test_inputs=json.loads(challenge.test_inputs_json),
        completed=completed,
        attempts=attempts,
        unlocked=unlocked,
        level_order=challenge.level_order,
        phase=challenge.phase,
        concepts_taught=json.loads(challenge.concepts_taught_json) if challenge.concepts_taught_json else [],
        challenge_type=challenge.challenge_type or "python",
        theory_content=challenge.theory_content,
        lore_briefing=challenge.lore_briefing,
        pedagogical_objective=challenge.pedagogical_objective,
        syntax_hint=challenge.syntax_hint,
        hints=json.loads(challenge.hints_json) if challenge.hints_json else [],
    )


@router.get(
    "/challenges",
    response_model=list[ChallengeOut],
    summary="Lista todas las misiones",
)
async def list_challenges(
    user_id: Optional[uuid.UUID] = Query(None),
    db: AsyncSession = Depends(get_db),
) -> list[ChallengeOut]:
    result = await db.execute(
        select(Challenge).order_by(nulls_last(Challenge.level_order), Challenge.base_xp_reward)
    )
    challenges = result.scalars().all()

    progress_map: dict[uuid.UUID, UserProgress] = {}
    if user_id:
        prog_result = await db.execute(
            select(UserProgress).where(UserProgress.user_id == user_id)
        )
        for p in prog_result.scalars().all():
            progress_map[p.challenge_id] = p

    out: list[ChallengeOut] = []
    prev_completed = True  # la primera misión siempre está desbloqueada
    for challenge in challenges:
        prog = progress_map.get(challenge.id)
        completed = prog.completed if prog else False
        attempts = prog.attempts if prog else 0
        out.append(_build_out(challenge, completed, attempts, unlocked=prev_completed))
        # Toda misión (incluyendo tutoriales) debe completarse para desbloquear la siguiente
        prev_completed = completed

    return out


@router.get(
    "/challenges/{challenge_id}",
    response_model=ChallengeOut,
    summary="Obtiene una misión por ID",
)
async def get_challenge(
    challenge_id: uuid.UUID,
    user_id: Optional[uuid.UUID] = Query(None),
    db: AsyncSession = Depends(get_db),
) -> ChallengeOut:
    # Carga la lista ordenada para calcular el estado de desbloqueo correctamente
    all_result = await db.execute(
        select(Challenge).order_by(nulls_last(Challenge.level_order), Challenge.base_xp_reward)
    )
    all_challenges = all_result.scalars().all()

    challenge = next((c for c in all_challenges if c.id == challenge_id), None)
    if challenge is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Misión no encontrada",
        )

    progress_map: dict[uuid.UUID, UserProgress] = {}
    if user_id:
        prog_result = await db.execute(
            select(UserProgress).where(UserProgress.user_id == user_id)
        )
        for p in prog_result.scalars().all():
            progress_map[p.challenge_id] = p

    # Recorre la cadena ordenada para determinar si esta misión está desbloqueada
    prev_completed = True
    unlocked = True
    for c in all_challenges:
        if c.id == challenge_id:
            unlocked = prev_completed
            break
        prog = progress_map.get(c.id)
        prev_completed = prog.completed if prog else False

    prog = progress_map.get(challenge_id)
    return _build_out(
        challenge,
        completed=prog.completed if prog else False,
        attempts=prog.attempts if prog else 0,
        unlocked=unlocked,
    )
