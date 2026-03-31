import json
import unicodedata
import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.rate_limit import limiter
from app.models.challenge import Challenge
from app.models.user_metrics import UserMetric
from app.schemas.gamification import ChallengeAttemptResult
from app.services.achievement_service import check_and_grant, get_insight_for_concepts
from app.services.ai_mentor import get_execute_feedback
from app.services.execution_service import execute_python_code
from app.services.gamification_service import gamification_engine

router = APIRouter()

# attempts → índice de pista (0-based). Una vez desbloqueada, persiste.
_HINT_THRESHOLDS: list[int] = [3, 6, 10]


def _normalize_output(text: str) -> str:
    """
    Normalización agresiva antes de comparar stdout con expected_output.

    Pasos:
    1. Normaliza Unicode a NFC (evita diferencias NFC/NFD invisibles)
    2. Unifica variantes de guión: em-dash (—) y en-dash (–) → hyphen-minus (-)
    3. Unifica saltos de línea  (CRLF → LF, CR suelto → LF)
    4. Recorta espacios al inicio/fin de cada línea
    5. Elimina líneas vacías sobrantes al inicio y al final del bloque
    """
    text = unicodedata.normalize("NFC", text)
    text = text.replace("\u2014", "-").replace("\u2013", "-")  # em-dash, en-dash → hyphen
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
    daki_level: int = 1       # nivel evolutivo de DAKI (1 robótico, 2 amistoso, 3 compañero)


class ErrorInfo(BaseModel):
    error_type: str
    line: Optional[int]
    detail: str


class DakiIntervention(BaseModel):
    hint_index: int           # 0-based
    hint_number: int          # 1-based (para mostrar "Pista 1/3")
    total_hints: int
    text: str


class AchievementUnlocked(BaseModel):
    id: str
    name: str
    description: str
    icon: str
    xp_bonus: int
    rarity: str
    unlocked_at: str


class CodeExecuteResponse(BaseModel):
    stdout: str
    stderr: str
    execution_time_ms: float
    output_matched: bool
    gamification: ChallengeAttemptResult
    error_info: Optional[ErrorInfo] = None
    daki_intervention: Optional[DakiIntervention] = None   # pista automática por tolerancia
    daki_message: str = ""                                  # frase narrativa de DAKI Intel
    achievements_unlocked: list[AchievementUnlocked] = []  # logros recién desbloqueados
    insight: Optional[str] = None                          # conexión mundo real post-nivel


async def _upsert_metric(
    db: AsyncSession,
    user_id: uuid.UUID,
    challenge_id: uuid.UUID,
    time_spent_ms: int,
    success: bool,
    hints_used: int = 0,
    error_type: Optional[str] = None,
) -> int:
    """
    Inserta o actualiza telemetría para (user_id, challenge_id).
    Retorna el attempts total DESPUÉS del upsert (usado para lógica DAKI).
    Falla silenciosamente si hay error — la telemetría no es crítica.
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
            errors_log = [error_type] if error_type else []
            metric = UserMetric(
                user_id=user_id,
                challenge_id=challenge_id,
                attempts=1,
                time_spent_ms=time_spent_ms,
                status="success" if success else "fail",
                hints_used=hints_used,
                syntax_errors_log=json.dumps(errors_log),
                first_attempt_at=now,
                last_attempt_at=now,
            )
            db.add(metric)
        else:
            metric.attempts += 1
            metric.time_spent_ms += time_spent_ms
            metric.status = "success" if success else metric.status
            metric.hints_used = max(metric.hints_used, hints_used)
            metric.last_attempt_at = now
            if error_type:
                log: list[str] = json.loads(metric.syntax_errors_log or "[]")
                log.append(error_type)
                metric.syntax_errors_log = json.dumps(log[-50:])

        await db.flush()
        return metric.attempts
    except Exception:
        return 0  # telemetría no crítica — retorna 0 para no activar pistas por error


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
@limiter.limit("20/minute")
async def execute_challenge_code(
    request: Request,
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
    raw_ei = exec_result.get("error_info")
    error_info = ErrorInfo(**raw_ei) if raw_ei else None

    total_attempts = await _upsert_metric(
        db=db,
        user_id=payload.user_id,
        challenge_id=payload.challenge_id,
        time_spent_ms=payload.time_spent_ms,
        success=is_success,
        hints_used=payload.hints_used,
        error_type=error_info.error_type if error_info else None,
    )

    # ── Intervención DAKI por tolerancia ─────────────────────────────────────
    daki_intervention: Optional[DakiIntervention] = None
    if not is_success and total_attempts > 0:
        hints: list[str] = json.loads(challenge.hints_json) if challenge.hints_json else []
        if hints:
            # Determina qué índice de pista corresponde a este número de intentos
            hint_idx = -1
            for threshold_idx, threshold in enumerate(_HINT_THRESHOLDS):
                if total_attempts >= threshold:
                    hint_idx = threshold_idx

            if hint_idx >= 0:
                hint_idx = min(hint_idx, len(hints) - 1)
                daki_intervention = DakiIntervention(
                    hint_index=hint_idx,
                    hint_number=hint_idx + 1,
                    total_hints=len(hints),
                    text=hints[hint_idx],
                )

    # ── DAKI: reacción contextual vía LLM (stacktrace real → respuesta dinámica) ─
    daki_message = await get_execute_feedback(
        challenge_title=challenge.title,
        challenge_description=challenge.description,
        source_code=payload.source_code,
        error_output=exec_result["stderr"],
        attempt_number=total_attempts,
        is_success=is_success,
    )

    # ── Logros + Insight (solo en primera compleción exitosa) ─────────────────
    achievements_unlocked: list[dict] = []
    insight: Optional[str] = None

    if is_success:
        try:
            import json as _json
            concepts: list[str] = _json.loads(challenge.concepts_taught_json or "[]") if hasattr(challenge, "concepts_taught_json") else []

            # Insight de mundo real
            insight = get_insight_for_concepts(concepts)

            # Logros
            achievements_unlocked = await check_and_grant(
                db=db,
                user_id=payload.user_id,
                trigger="level_complete",
                context={
                    "already_completed": gamification_result.already_completed,
                    "hints_used": payload.hints_used,
                    "attempts": total_attempts,
                    "execution_time_ms": exec_result["execution_time_ms"],
                    "user_level": gamification_result.new_level,
                    "user_streak": 0,  # streak se actualiza en login; aquí solo nivel
                    "total_completed": gamification_result.new_level * 2,  # aproximación
                    "level_order": challenge.level_order or 0,
                },
            )
            await db.commit()
        except Exception:
            pass  # Logros no son críticos — nunca bloquean la respuesta

    return CodeExecuteResponse(
        stdout=exec_result["stdout"],
        stderr=exec_result["stderr"],
        execution_time_ms=exec_result["execution_time_ms"],
        output_matched=output_matched,
        gamification=gamification_result,
        error_info=error_info,
        daki_intervention=daki_intervention,
        daki_message=daki_message,
        achievements_unlocked=[AchievementUnlocked(**a) for a in achievements_unlocked],
        insight=insight if (is_success and not gamification_result.already_completed) else None,
    )
