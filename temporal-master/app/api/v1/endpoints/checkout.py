"""
checkout.py — Endpoint de Redención de Llaves de Override Táctico

POST /api/v1/checkout/redeem
    Valida un código promocional e inyecta la Licencia de Fundador al Operador.

Lógica:
    1. Requiere JWT válido — el user_id se extrae del token, nunca del body.
    2. Busca la llave por code_string (case-insensitive via UPPER normalization).
    3. Valida: existe + is_active + current_uses < max_uses.
    4. Incrementa current_uses (atómico — evita race conditions con SELECT FOR UPDATE).
    5. Activa is_licensed = True en el usuario autenticado.
    6. Devuelve 200 con mensaje de acceso concedido.

Errores:
    400 — Código inválido, inactivo, o agotado.
    401 — Sin sesión válida.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_operator
from app.models.tactical_key import TacticalAccessKey
from app.models.user import User

router = APIRouter(prefix="/checkout", tags=["checkout"])


# ─── Schemas ──────────────────────────────────────────────────────────────────

class RedeemRequest(BaseModel):
    code_string: str     # user_id eliminado — se extrae del JWT autenticado


class RedeemResponse(BaseModel):
    status: str        # "granted"
    message: str


# ─── Endpoint ─────────────────────────────────────────────────────────────────

@router.post(
    "/redeem",
    response_model=RedeemResponse,
    status_code=status.HTTP_200_OK,
    summary="Redimir una Llave de Override Táctico para activar la Licencia de Fundador",
)
async def redeem_tactical_key(
    payload:  RedeemRequest,
    operator: User           = Depends(get_current_operator),   # JWT requerido
    db:       AsyncSession   = Depends(get_db),
) -> RedeemResponse:
    # ── 1. Buscar la llave (case-insensitive) ─────────────────────────────────
    code_upper = payload.code_string.strip().upper()
    result = await db.execute(
        select(TacticalAccessKey)
        .where(TacticalAccessKey.code_string == code_upper)
        .with_for_update()   # bloqueo pesimista: evita doble-activación concurrente
    )
    key = result.scalar_one_or_none()

    # ── 2. Validación ─────────────────────────────────────────────────────────
    _invalid = (
        key is None
        or not key.is_active
        or (key.max_uses > 0 and key.current_uses >= key.max_uses)
    )
    if _invalid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Código inválido o agotado. Verifica el código e intenta de nuevo.",
        )

    # ── 3. Activar licencia + consumir uso ────────────────────────────────────
    # El operador autenticado es el receptor — sin posibilidad de suplantación
    key.current_uses          += 1
    operator.is_licensed       = True
    operator.subscription_status = "ACTIVE"

    # ── 4. Respuesta ──────────────────────────────────────────────────────────
    return RedeemResponse(
        status="granted",
        message="Acceso concedido. Bienvenido a la Red Central, Operador.",
    )
