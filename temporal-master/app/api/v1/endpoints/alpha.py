"""
alpha.py — Endpoint de Canje Alpha (Operación Vanguardia)
──────────────────────────────────────────────────────────
POST /api/v1/alpha/redeem

Candado Atómico: un código = una activación, nunca reutilizable.
Prevención de Race Conditions via SELECT ... FOR UPDATE (bloqueo pesimista de fila).

Flujo de transacción:
  1. SELECT alpha_codes WHERE code=? FOR UPDATE  → bloqueo exclusivo de fila
  2. Validar: existe (404) + is_used=False (409)
  3. SELECT users WHERE id=? FOR UPDATE          → bloqueo del usuario
  4. Validar: usuario existe (401 — token inválido si no está en DB)
  5. Marcar código: is_used=True, used_by_user_id, used_at=now()
  6. Activar usuario: subscription_status='TRIAL', trial_end_date=now()+30d
  7. Commit → ambos locks se liberan simultáneamente

Concurrent request scenario:
  - Request A y B llegan con el mismo código en el mismo ms.
  - Uno de ellos adquiere el FOR UPDATE lock primero.
  - El otro espera. Cuando obtiene el lock, ve is_used=True → 409.
  - Resultado: exactamente UNA activación, nunca dos.
"""

from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.rate_limit import limiter
from app.core.security import get_current_operator
from app.models.alpha_code import AlphaCode
from app.models.user import User

router = APIRouter(prefix="/alpha", tags=["alpha"])

_TRIAL_DAYS_DEFAULT = 30  # fallback si days_granted no está seteado


# ── Schemas ───────────────────────────────────────────────────────────────────

class RedeemAlphaRequest(BaseModel):
    code: str = Field(..., min_length=1, max_length=24, description="Alpha Code en formato VANG-XXXX-XXXX")


class RedeemAlphaResponse(BaseModel):
    status:           str   # "granted"
    message:          str
    subscription:     str   # "TRIAL"
    trial_end_date:   str   # ISO 8601


# ── Endpoint ──────────────────────────────────────────────────────────────────

@router.post(
    "/redeem",
    response_model=RedeemAlphaResponse,
    status_code=status.HTTP_200_OK,
    summary="Canje de Alpha Code — Operación Vanguardia",
    description=(
        "Valida y consume un Alpha Code de un solo uso. "
        "Activa subscription_status='TRIAL' con 30 días de acceso al Operador autenticado. "
        "Usa SELECT FOR UPDATE para prevenir canjes concurrentes del mismo código."
    ),
)
@limiter.limit("5/minute")   # anti-brute-force: 5 intentos por minuto por IP
async def redeem_alpha_code(
    request:  Request,                                   # requerido por slowapi limiter
    payload:  RedeemAlphaRequest,
    operator: User           = Depends(get_current_operator),
    db:       AsyncSession   = Depends(get_db),
) -> RedeemAlphaResponse:
    """
    Canjea un Alpha Code de un solo uso.

    Requiere JWT válido (Bearer token). El user_id se extrae del token —
    no se acepta como parámetro en el body para evitar suplantación.

    Errores posibles:
        401 — Token ausente, inválido o expirado.
        404 — El código no existe en la Bóveda Alpha.
        409 — El código ya fue utilizado por otro Operador.
        429 — Demasiados intentos (anti-brute-force).
    """
    code_normalized = payload.code.strip().upper()

    # ── 1. SELECT FOR UPDATE — bloqueo exclusivo de fila ──────────────────────
    # Ninguna otra transacción concurrente puede leer NI modificar esta fila
    # hasta que se haga commit o rollback. Esto garantiza que dos requests
    # simultáneos no puedan canjear el mismo código.
    result = await db.execute(
        select(AlphaCode)
        .where(AlphaCode.code == code_normalized)
        .with_for_update()
    )
    alpha = result.scalar_one_or_none()

    # ── 2. Validar existencia ─────────────────────────────────────────────────
    if alpha is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Código no encontrado en la Bóveda Alpha. Verifica el formato e intenta de nuevo.",
        )

    # ── 3. Validar que no fue usado ───────────────────────────────────────────
    if alpha.is_used:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Código ya utilizado o inválido. Este token fue consumido por otro Operador.",
        )

    # ── 4. Calcular fecha de expiración del TRIAL ─────────────────────────────
    now           = datetime.now(timezone.utc)
    days          = alpha.days_granted if alpha.days_granted else _TRIAL_DAYS_DEFAULT
    trial_end     = now + timedelta(days=days)

    # ── 5. Marcar el Alpha Code como consumido ────────────────────────────────
    alpha.is_used          = True
    alpha.used_by_user_id  = operator.id
    alpha.used_at          = now

    # ── 6. Activar TRIAL en el Operador ──────────────────────────────────────
    operator.subscription_status = "TRIAL"
    operator.trial_end_date      = trial_end

    # db.commit() se ejecuta automáticamente al salir del contexto get_db()
    # Ambas filas se actualizan en la misma transacción — o las dos o ninguna.

    # ── 7. Respuesta ──────────────────────────────────────────────────────────
    return RedeemAlphaResponse(
        status         = "granted",
        message        = "Acceso Nivel Vanguardia Concedido. Bienvenido al Nexo.",
        subscription   = "TRIAL",
        trial_end_date = trial_end.isoformat(),
    )
