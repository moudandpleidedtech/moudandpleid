"""
session.py — Endpoints de Sesión DAKI
──────────────────────────────────────
POST /session/open       → apertura personalizada con voz DAKI
POST /session/close      → briefing de cierre 3 líneas
GET  /session/boss-check → pre-anuncio de Boss Battle
"""

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services import daki_session_service

router = APIRouter(prefix="/session", tags=["session"])


# ── Schemas ───────────────────────────────────────────────────────────────────

class SessionOpenRequest(BaseModel):
    user_id:        uuid.UUID
    operator_level: int = Field(default=1, ge=1, description="Nivel actual del Operador")
    streak_days:    int = Field(default=0, ge=0, description="Días de racha activa")
    callsign:       str = Field(..., min_length=1, max_length=50, description="Nombre táctico del Operador")
    hour:           int = Field(default=12, ge=0, le=23, description="Hora local (0–23) para calibrar tono")


class SessionOpenResponse(BaseModel):
    session_id:      str
    opening_message: str
    weak_concept:    str | None


class SessionCloseRequest(BaseModel):
    session_id:           uuid.UUID
    challenges_completed: int = Field(default=0, ge=0)
    challenges_attempted: int = Field(default=0, ge=0)
    hints_requested:      int = Field(default=0, ge=0)
    dominant_error_type:  str | None = Field(default=None, max_length=120)


class SessionCloseResponse(BaseModel):
    briefing: str


class BossWarningResponse(BaseModel):
    warning:     bool
    boss_level:  int | None
    levels_away: int | None
    message:     str | None


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.post(
    "/open",
    response_model=SessionOpenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Apertura de sesión DAKI con mensaje personalizado",
)
async def open_session(
    payload: SessionOpenRequest,
    db: AsyncSession = Depends(get_db),
) -> SessionOpenResponse:
    """
    Abre una nueva sesión DAKI para el Operador.

    - Recupera el concepto más débil del historial de maestría.
    - Genera un mensaje de bienvenida personalizado calibrado por hora, racha y nivel.
    - Persiste el registro en daki_session_logs.
    - Retorna session_id para usar en el endpoint /close.
    """
    try:
        result = await daki_session_service.open_session(
            db=db,
            user_id=payload.user_id,
            operator_level=payload.operator_level,
            streak_days=payload.streak_days,
            callsign=payload.callsign,
            hour=payload.hour,
        )
        return SessionOpenResponse(**result)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al abrir sesión: {exc}",
        ) from exc


@router.post(
    "/close",
    response_model=SessionCloseResponse,
    status_code=status.HTTP_200_OK,
    summary="Cierre de sesión con briefing táctico de 3 líneas",
)
async def close_session(
    payload: SessionCloseRequest,
    db: AsyncSession = Depends(get_db),
) -> SessionCloseResponse:
    """
    Cierra la sesión y genera un briefing de 3 líneas:
      1. Lo que el Operador consolidó hoy.
      2. El frente abierto más urgente.
      3. La siguiente misión táctica.

    El briefing queda persistido en daki_session_logs para referencia futura.
    """
    try:
        result = await daki_session_service.close_session(
            db=db,
            session_id=payload.session_id,
            challenges_completed=payload.challenges_completed,
            challenges_attempted=payload.challenges_attempted,
            hints_requested=payload.hints_requested,
            dominant_error_type=payload.dominant_error_type,
        )
        return SessionCloseResponse(**result)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al cerrar sesión: {exc}",
        ) from exc


@router.get(
    "/boss-check/{operator_level}",
    response_model=BossWarningResponse,
    summary="Verifica proximidad a Boss Battle",
)
async def boss_check(operator_level: int) -> BossWarningResponse:
    """
    Verifica si el Operador está a <= 2 niveles de un Boss Battle (10, 25, 50).

    Sin DB — cálculo local inmediato.
    El frontend debe mostrar la alerta si warning=True.
    """
    result = daki_session_service.check_boss_warning(operator_level)
    return BossWarningResponse(**result)
