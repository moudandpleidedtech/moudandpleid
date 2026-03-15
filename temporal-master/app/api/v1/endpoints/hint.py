import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.challenge import Challenge
from app.models.user_progress import UserProgress
from app.services import ai_mentor

router = APIRouter()


class HintRequest(BaseModel):
    user_id: uuid.UUID
    challenge_id: uuid.UUID
    source_code: str
    error_output: str = ""


class HintResponse(BaseModel):
    hint: str


@router.post(
    "/hint",
    response_model=HintResponse,
    status_code=status.HTTP_200_OK,
    summary="Solicita una pista de ENIGMA para el desafío actual",
    description=(
        "Llama al mentor IA (ENIGMA) para obtener una pista de máximo 2 líneas "
        "cuando el usuario lleva 3 o más intentos fallidos en un desafío Python."
    ),
)
async def request_hint(
    payload: HintRequest,
    db: AsyncSession = Depends(get_db),
) -> HintResponse:
    challenge = await db.get(Challenge, payload.challenge_id)
    if challenge is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Desafío no encontrado.",
        )

    # Registra la pista en la telemetría del progreso del usuario
    prog_result = await db.execute(
        select(UserProgress).where(
            UserProgress.user_id == payload.user_id,
            UserProgress.challenge_id == payload.challenge_id,
        )
    )
    progress = prog_result.scalar_one_or_none()
    if progress is None:
        progress = UserProgress(user_id=payload.user_id, challenge_id=payload.challenge_id)
        db.add(progress)
    progress.hints_used += 1

    hint = await ai_mentor.get_hint(
        challenge_title=challenge.title,
        challenge_description=challenge.description,
        source_code=payload.source_code,
        error_output=payload.error_output,
    )

    return HintResponse(hint=hint)
