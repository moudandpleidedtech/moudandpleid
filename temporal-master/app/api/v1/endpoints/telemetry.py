"""
Endpoint de Telemetría — El Ojo de DAKI.

POST /api/v1/telemetry/log
    Upsert de métricas de aprendizaje por (user_id, challenge_id).
    Llamado por el frontend cada vez que el usuario presiona "Ejecutar Código".

GET /api/v1/telemetry/{user_id}/{challenge_id}
    Estado actual de telemetría para un nivel específico.
"""

import json
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.user_metrics import UserMetric

router = APIRouter(prefix="/telemetry", tags=["telemetry"])

_MAX_ERROR_LOG = 50   # máximo de entradas en syntax_errors_log para no crecer sin límite


# ─── Schemas ─────────────────────────────────────────────────────────────────

class TelemetryLogRequest(BaseModel):
    user_id: uuid.UUID
    challenge_id: uuid.UUID
    time_spent_ms: int = Field(ge=0, description="Duración del intento en milisegundos")
    is_success: bool = Field(description="True si el código pasó todos los tests")
    hints_used: int = Field(default=0, ge=0, le=3, description="Pistas usadas hasta este punto (acumulado)")
    error_type: str | None = Field(default=None, description="Tipo de error Python si falló (ej. 'SyntaxError')")


class TelemetryLogResponse(BaseModel):
    user_id: uuid.UUID
    challenge_id: uuid.UUID
    attempts: int
    time_spent_ms: int
    status: str
    hints_used: int
    syntax_errors_log: list[str]
    first_attempt_at: datetime
    last_attempt_at: datetime
    created: bool   # True = registro nuevo, False = actualizado


# ─── Endpoint ────────────────────────────────────────────────────────────────

@router.post(
    "/log",
    response_model=TelemetryLogResponse,
    status_code=status.HTTP_200_OK,
    summary="Registra un intento de ejecución",
    description=(
        "Upsert de métricas por (user_id, challenge_id). "
        "Si ya existe el registro, incrementa el contador de intentos, "
        "suma el tiempo, actualiza el estado y agrega el error al log. "
        "Llamar en cada 'Ejecutar Código'."
    ),
)
async def log_telemetry(
    body: TelemetryLogRequest,
    db: AsyncSession = Depends(get_db),
) -> TelemetryLogResponse:
    now = datetime.now(timezone.utc)

    result = await db.execute(
        select(UserMetric).where(
            UserMetric.user_id == body.user_id,
            UserMetric.challenge_id == body.challenge_id,
        )
    )
    existing = result.scalar_one_or_none()
    created = existing is None

    if created:
        # INSERT — primer intento
        errors_log = [body.error_type] if body.error_type else []
        metric = UserMetric(
            user_id=body.user_id,
            challenge_id=body.challenge_id,
            attempts=1,
            time_spent_ms=body.time_spent_ms,
            status="success" if body.is_success else "fail",
            hints_used=body.hints_used,
            syntax_errors_log=json.dumps(errors_log),
            first_attempt_at=now,
            last_attempt_at=now,
        )
        db.add(metric)
    else:
        # UPDATE — intento subsiguiente
        existing.attempts += 1
        existing.time_spent_ms += body.time_spent_ms
        existing.status = "success" if body.is_success else "fail"
        existing.hints_used = max(existing.hints_used, body.hints_used)  # nunca decrece
        existing.last_attempt_at = now

        # Agrega el nuevo error al log (sin duplicar el tipo, con límite de tamaño)
        if body.error_type:
            current_log: list[str] = json.loads(existing.syntax_errors_log or "[]")
            current_log.append(body.error_type)
            existing.syntax_errors_log = json.dumps(current_log[-_MAX_ERROR_LOG:])

        metric = existing

    await db.flush()

    return TelemetryLogResponse(
        user_id=metric.user_id,
        challenge_id=metric.challenge_id,
        attempts=metric.attempts,
        time_spent_ms=metric.time_spent_ms,
        status=metric.status,
        hints_used=metric.hints_used,
        syntax_errors_log=json.loads(metric.syntax_errors_log or "[]"),
        first_attempt_at=metric.first_attempt_at,
        last_attempt_at=metric.last_attempt_at,
        created=created,
    )


@router.get(
    "/{user_id}/{challenge_id}",
    response_model=TelemetryLogResponse,
    summary="Telemetría de un nivel para un usuario",
)
async def get_telemetry(
    user_id: uuid.UUID,
    challenge_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> TelemetryLogResponse:
    result = await db.execute(
        select(UserMetric).where(
            UserMetric.user_id == user_id,
            UserMetric.challenge_id == challenge_id,
        )
    )
    metric = result.scalar_one_or_none()
    if metric is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay telemetría registrada para este usuario y nivel.",
        )
    return TelemetryLogResponse(
        user_id=metric.user_id,
        challenge_id=metric.challenge_id,
        attempts=metric.attempts,
        time_spent_ms=metric.time_spent_ms,
        status=metric.status,
        hints_used=metric.hints_used,
        syntax_errors_log=json.loads(metric.syntax_errors_log or "[]"),
        first_attempt_at=metric.first_attempt_at,
        last_attempt_at=metric.last_attempt_at,
        created=False,
    )
