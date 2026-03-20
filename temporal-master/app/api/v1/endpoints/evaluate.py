"""
POST /api/v1/evaluate  — Motor de Evaluación Universal (exec()-based)

Recibe código del usuario + challenge_id, ejecuta en sandbox aislado,
compara contra expected_output del nivel y devuelve resultado estructurado
con el mensaje narrativo de DAKI Intel.
"""

import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.access import require_paid
from app.core.database import get_db
from app.models.user import User
from app.services.daki_intel import get_daki_message
from app.services.evaluation_service import EvaluacionResult, evaluar_incursion
from app.services.progression import resolve_level_status

router = APIRouter()


# ─── Modelos Pydantic ─────────────────────────────────────────────────────────

class EvaluateRequest(BaseModel):
    challenge_id: uuid.UUID
    code: str
    daki_level: int = 1                     # nivel evolutivo de DAKI (1 robótico, 2 amistoso, 3 compañero)
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


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _resolve_daki_event(status: str, error_type: str | None) -> str:
    """
    Determina el evento DAKI a partir del resultado de evaluación.

    - Si hay error_type específico ("SyntaxError", "NameError", …) → úsalo.
    - Si status es "timeout" → "timeout".
    - Si status es "failed"  → "failed".
    - Si status es "success" → "success".
    - Fallback: "RuntimeError".
    """
    if error_type and error_type not in ("", "None"):
        return error_type
    if status == "timeout":
        return "timeout"
    if status == "success":
        return "success"
    if status == "failed":
        return "failed"
    return "RuntimeError"


# ─── Endpoint ─────────────────────────────────────────────────────────────────

@router.post(
    "/evaluate",
    response_model=EvaluateResponse,
    summary="Evalúa el código del usuario contra el expected_output del nivel",
)
async def evaluate_code(
    payload: EvaluateRequest,
    db: AsyncSession = Depends(get_db),
    _user: User | None = Depends(require_paid),
) -> EvaluateResponse:
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

    result: EvaluacionResult = await evaluar_incursion(
        codigo_usuario=payload.code,
        challenge_id=payload.challenge_id,
        db=db,
    )
    raw       = result.as_dict
    ei        = raw.get("error_info") or {}
    event     = _resolve_daki_event(raw["status"], ei.get("error_type"))
    daki_msg  = get_daki_message(event, payload.daki_level)

    return EvaluateResponse(
        status=raw["status"],
        output_matched=raw["output_matched"],
        stdout=raw["stdout"],
        stderr=raw["stderr"],
        execution_time_ms=raw["execution_time_ms"],
        error_info=ErrorInfo(**raw["error_info"]) if raw.get("error_info") else None,
        daki_message=daki_msg,
    )
