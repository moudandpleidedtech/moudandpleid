import uuid

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.rate_limit import limiter
from app.models.challenge import Challenge
from app.models.user_progress import UserProgress
from app.services import ai_mentor
from app.services.memory_service import (
    format_operator_history,
    get_recent_events,
    record_event,
)

router = APIRouter()


class HintRequest(BaseModel):
    user_id: uuid.UUID
    challenge_id: uuid.UUID
    source_code: str
    error_output: str = ""
    fail_count: int = 1    # número de intentos fallidos → calibra el nivel de pista DAKI


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
@limiter.limit("10/minute")
async def request_hint(
    request: Request,
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
        progress = UserProgress(
            user_id=payload.user_id,
            challenge_id=payload.challenge_id,
            hints_used=0,
        )
        db.add(progress)
    progress.hints_used = (progress.hints_used or 0) + 1

    # ── Memoria Evolutiva: registrar error_frecuente y recuperar historial ─────
    if payload.fail_count >= 2:
        await record_event(
            db=db,
            user_id=payload.user_id,
            event_type="error_frecuente",
            context_data={
                "challenge_title": challenge.title,
                "fail_count": payload.fail_count,
                "error_type": payload.error_output[:120] if payload.error_output else "",
            },
            challenge_id=payload.challenge_id,
        )

    recent_events = await get_recent_events(db, payload.user_id, limit=5)
    operator_history = format_operator_history(recent_events)

    hint = await ai_mentor.get_hint(
        challenge_title=challenge.title,
        challenge_description=challenge.description,
        source_code=payload.source_code,
        error_output=payload.error_output,
        fail_count=max(1, payload.fail_count),
        operator_history=operator_history,
    )

    return HintResponse(hint=hint)
