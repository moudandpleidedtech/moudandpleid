"""
POST /api/v1/evaluate  — Motor de Evaluación Universal (exec()-based)

Recibe código del usuario + challenge_id, ejecuta en sandbox aislado,
compara contra expected_output del nivel y devuelve resultado estructurado
con el mensaje narrativo de DAKI Intel.
"""

import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.access import check_freemium_access
from app.core.database import get_db
from app.core.rate_limit import limiter
from app.models.challenge import Challenge
from app.services.ai_mentor import get_execute_feedback
from app.services.evaluation_service import EvaluacionResult, evaluar_incursion
from app.services.progression import resolve_level_status

router = APIRouter()


# ─── Modelos Pydantic ─────────────────────────────────────────────────────────

class EvaluateRequest(BaseModel):
    challenge_id: uuid.UUID
    code: str = Field(max_length=20_000)
    daki_level: int = Field(default=1, ge=1, le=3)
    user_id: Optional[uuid.UUID] = None     # UUID del operador para verificar acceso


class ErrorInfo(BaseModel):
    error_type: str | None = None
    line: int | None = None
    detail: str = ""


class EvaluateResponse(BaseModel):
    status: str                        # "success" | "failed" | "error" | "timeout"
    output_matched: bool = False
    stdout: str = ""
    stderr: str = ""
    execution_time_ms: float = 0.0
    error_info: ErrorInfo | None = None
    daki_message: str = ""             # frase narrativa de DAKI para UI y voz


# ─── Endpoint ─────────────────────────────────────────────────────────────────

@router.post(
    "/evaluate",
    response_model=EvaluateResponse,
    summary="Evalúa el código del usuario contra el expected_output del nivel",
)
@limiter.limit("20/minute")
async def evaluate_code(
    request: Request,
    payload: EvaluateRequest,
    db: AsyncSession = Depends(get_db),
) -> EvaluateResponse:
    # ── Compuerta Freemium: libre en L0–L10, licencia requerida en L11–L100 ───
    await check_freemium_access(db, payload.challenge_id, payload.user_id)

    # ── Guardián del Nexo: bloquea intentos en niveles no accesibles ──────────
    lvl_status = await resolve_level_status(db, payload.user_id, payload.challenge_id)
    if lvl_status == "locked":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code": "LEVEL_LOCKED",
                "message": (
                    "Acceso denegado. Completa el nivel anterior para desbloquear esta misión."
                ),
            },
        )

    challenge = await db.get(Challenge, payload.challenge_id)

    result: EvaluacionResult = await evaluar_incursion(
        codigo_usuario=payload.code,
        challenge_id=payload.challenge_id,
        db=db,
    )
    raw      = result.as_dict
    daki_msg = await get_execute_feedback(
        challenge_title=challenge.title if challenge else "Misión",
        challenge_description=challenge.description if challenge else "",
        source_code=payload.code,
        error_output=raw.get("stderr", ""),
        attempt_number=1,
        is_success=(raw["status"] == "success"),
    )

    return EvaluateResponse(
        status=raw["status"],
        output_matched=raw["output_matched"],
        stdout=raw["stdout"],
        stderr=raw["stderr"],
        execution_time_ms=raw["execution_time_ms"],
        error_info=ErrorInfo(**raw["error_info"]) if raw.get("error_info") else None,
        daki_message=daki_msg,
    )
