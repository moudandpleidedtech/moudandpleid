"""
checkout.py — Endpoint de Redención de Llaves de Override Táctico (Prompt 66)

POST /api/v1/checkout/redeem
    Valida un código promocional e inyecta la Licencia de Fundador al Operador.

Lógica:
    1. Busca la llave por code_string (case-insensitive via UPPER normalization).
    2. Valida: existe + is_active + current_uses < max_uses.
    3. Incrementa current_uses (atómico — evita race conditions con SELECT FOR UPDATE).
    4. Activa is_paid = True en el usuario.
    5. Devuelve 200 con mensaje de acceso concedido.

Errores:
    400 — Código inválido, inactivo, o agotado.
    404 — Usuario no encontrado.
"""

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.tactical_key import TacticalAccessKey
from app.models.user import User

router = APIRouter(prefix="/checkout", tags=["checkout"])


# ─── Schemas ──────────────────────────────────────────────────────────────────

class RedeemRequest(BaseModel):
    user_id: uuid.UUID
    code_string: str


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
    payload: RedeemRequest,
    db: AsyncSession = Depends(get_db),
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

    # ── 3. Buscar al usuario ──────────────────────────────────────────────────
    user = await db.get(User, payload.user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Operador no encontrado en los registros del Nexo.",
        )

    # ── 4. Activar licencia + consumir uso ────────────────────────────────────
    key.current_uses += 1
    user.is_licensed = True

    # ── 5. Respuesta ──────────────────────────────────────────────────────────
    return RedeemResponse(
        status="granted",
        message="Acceso concedido. Bienvenido a la Red Central, Operador.",
    )
