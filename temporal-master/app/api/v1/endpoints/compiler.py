import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.challenge import Challenge
from app.models.user_metrics import UserMetric
from app.schemas.gamification import ChallengeAttemptResult
from app.services.execution_service import execute_python_code
from app.services.gamification_service import gamification_engine

router = APIRouter()


def _normalize_output(text: str) -> str:
    """
    Normalización agresiva antes de comparar stdout con expected_output.

    Pasos:
    1. Unifica saltos de línea  (CRLF → LF, CR suelto → LF)
    2. Recorta espacios al inicio/fin de cada línea
    3. Elimina líneas vacías sobrantes al inicio y al final del bloque
    """
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.strip() for line in normalized.splitlines()]
    return "\n".join(lines).strip()


class CodeExecuteRequest(BaseModel):
    user_id: uuid.UUID
    challenge_id: uuid.UUID
    source_code: str
    test_inputs: list[str] = []
    hints_used: int = 0       # pistas solicitadas a ENIGMA antes de este intento
    time_spent_ms: int = 0    # tiempo en ms desde que el usuario abrió el reto (opcional)


class ErrorInfo(BaseModel):
    error_type: str
    line: Optional[int]
    detail: str


class CodeExecuteResponse(BaseModel):
    stdout: str
    stderr: str
    execution_time_ms: float
    output_matched: bool
    gamification: ChallengeAttemptResult
    error_info: Optional[ErrorInfo] = None


async def _upsert_metric(
    db: AsyncSession,
    user_id: uuid.UUID,
    challenge_id: uuid.UUID,
    time_spent_ms: int,
    success: bool,
) -> None:
    """
    Inserta o actualiza la fila de telemetría para (user_id, challenge_id).
    Si ya existe, incrementa attempts, acumula time_spent_ms y actualiza status.
    Falla silenciosamente para no bloquear la respuesta al jugador.
    """
    try:
        result = await db.execute(
            select(UserMetric).where(
                UserMetric.user_id == user_id,
                UserMetric.challenge_id == challenge_id,
            )
        )
        metric = result.scalar_one_or_none()
        now = datetime.now(timezone.utc)

        if metric is None:
            db.add(UserMetric(
                user_id=user_id,
                challenge_id=challenge_id,
                attempts=1,
                time_spent_ms=time_spent_ms,
                status="success" if success else "fail",
                first_attempt_at=now,
                last_attempt_at=now,
            ))
        else:
            metric.attempts += 1
            metric.time_spent_ms += time_spent_ms
            metric.status = "success" if success else metric.status  # una vez exitoso, queda exitoso
            metric.last_attempt_at = now

        await db.flush()
    except Exception:
        pass  # telemetría no crítica


@router.post(
    "/execute",
    response_model=CodeExecuteResponse,
    status_code=status.HTTP_200_OK,
    summary="Execute user code for a challenge",
    description=(
        "Runs the submitted source code via Piston API (or local subprocess fallback), "
        "validates stdout against the challenge's expected_output, "
        "and automatically triggers gamification scoring."
    ),
)
async def execute_challenge_code(
    payload: CodeExecuteRequest,
    db: AsyncSession = Depends(get_db),
) -> CodeExecuteResponse:
    challenge = await db.get(Challenge, payload.challenge_id)
    if challenge is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Challenge {payload.challenge_id} not found",
        )

    exec_result = await execute_python_code(payload.source_code, payload.test_inputs)

    # Cuenta errores de sintaxis detectados en stderr de este intento
    syntax_errors_count = exec_result["stderr"].count("SyntaxError")

    output_matched = _normalize_output(exec_result["stdout"]) == _normalize_output(challenge.expected_output)
    is_success = exec_result["success"] and output_matched

    try:
        gamification_result = await gamification_engine.process_challenge_completion(
            db=db,
            user_id=payload.user_id,
            challenge_id=payload.challenge_id,
            is_success=is_success,
            execution_time_ms=int(exec_result["execution_time_ms"]),
            syntax_errors_count=syntax_errors_count,
            hints_used_this_session=payload.hints_used,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    # ── Telemetría: upsert en user_metrics ───────────────────────────────────
    await _upsert_metric(
        db=db,
        user_id=payload.user_id,
        challenge_id=payload.challenge_id,
        time_spent_ms=payload.time_spent_ms,
        success=is_success,
    )

    # Parsear error info si existe
    raw_ei = exec_result.get("error_info")
    error_info = ErrorInfo(**raw_ei) if raw_ei else None

    return CodeExecuteResponse(
        stdout=exec_result["stdout"],
        stderr=exec_result["stderr"],
        execution_time_ms=exec_result["execution_time_ms"],
        output_matched=output_matched,
        gamification=gamification_result,
        error_info=error_info,
    )
