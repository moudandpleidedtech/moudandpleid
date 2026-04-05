"""
beta.py — Validación de Códigos Beta · DAKI EdTech
────────────────────────────────────────────────────
POST /api/v1/auth/verify-beta-code

Flujo:
  1. Busca el código (case-insensitive) en la tabla beta_codes.
  2. Si no existe o is_active=False → 404 Código inválido.
  3. Si current_uses >= max_uses   → 403 Código agotado.
  4. Incrementa current_uses y retorna token de acceso.
"""

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, field_validator
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.rate_limit import limiter
from app.models.beta_code import BetaCode

router = APIRouter(prefix="/auth", tags=["beta"])


# ── Schemas ───────────────────────────────────────────────────────────────────

class BetaCodeRequest(BaseModel):
    code: str

    @field_validator("code")
    @classmethod
    def normalize(cls, v: str) -> str:
        return v.strip().upper()


class BetaCodeResponse(BaseModel):
    status:  str
    message: str
    token:   str


# ── Endpoint ──────────────────────────────────────────────────────────────────

@router.post(
    "/verify-beta-code",
    response_model=BetaCodeResponse,
    summary="Valida un código de acceso Beta",
)
@limiter.limit("5/minute")
async def verify_beta_code(
    request: Request,
    payload: BetaCodeRequest,
    db: AsyncSession = Depends(get_db),
) -> BetaCodeResponse:
    """
    Valida el código recibido contra la tabla beta_codes.

    - **404** si el código no existe o está desactivado.
    - **403** si el código alcanzó su límite de usos.
    - **200** si es válido: incrementa `current_uses` y retorna token.
    """
    result = await db.execute(
        select(BetaCode).where(
            func.upper(BetaCode.code) == payload.code
        )
    )
    record: BetaCode | None = result.scalar_one_or_none()

    if record is None or not record.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code":    "INVALID_BETA_CODE",
                "message": "Código de acceso inválido o desactivado.",
            },
        )

    if record.current_uses >= record.max_uses:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code":    "CODE_EXHAUSTED",
                "message": "Este código de acceso ha alcanzado su límite de usos.",
            },
        )

    # Incrementar contador de usos
    record.current_uses += 1
    await db.commit()

    return BetaCodeResponse(
        status="success",
        message="Acceso concedido. Bienvenido al Nexo.",
        token="mock_token_temporal",
    )
