from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.gamification import ChallengeAttemptRequest, ChallengeAttemptResult
from app.services.gamification_service import GamificationEngine, gamification_engine

router = APIRouter()


@router.post(
    "/attempt",
    response_model=ChallengeAttemptResult,
    status_code=status.HTTP_200_OK,
    summary="Submit a challenge attempt",
    description=(
        "Processes a challenge attempt. Awards XP on first success, "
        "applies efficiency bonus for Tier 1 challenges completed under 50ms, "
        "and updates the user's level automatically."
    ),
)
async def submit_challenge_attempt(
    payload: ChallengeAttemptRequest,
    db: AsyncSession = Depends(get_db),
) -> ChallengeAttemptResult:
    try:
        return await gamification_engine.process_challenge_completion(
            db=db,
            user_id=payload.user_id,
            challenge_id=payload.challenge_id,
            is_success=payload.is_success,
            execution_time_ms=payload.execution_time_ms,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get(
    "/level",
    summary="Calculate level from XP",
    description="Returns the level corresponding to a given XP value using the progression formula.",
)
async def get_level_from_xp(xp: int) -> dict:
    if xp < 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="XP cannot be negative",
        )
    level = GamificationEngine.calculate_level_from_xp(xp)
    return {"xp": xp, "level": level}
