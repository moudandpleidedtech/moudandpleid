"""
access.py — Dependencias de acceso que protegen las rutas de niveles.

Lógica Freemium (Gancho Narrativo):
  - Niveles con is_free=True  (L0–L10) → cualquier usuario puede acceder.
  - Niveles con is_free=False (L11–L100) → requiere is_licensed=True en el usuario.

Uso en evaluate.py (ejemplo):

    from app.core.access import check_freemium_access

    @router.post("/evaluate")
    async def evaluate_code(payload: EvaluateRequest, db=Depends(get_db)):
        await check_freemium_access(db, payload.challenge_id, payload.user_id)
        ...

Para rutas que siguen requiriendo licencia completa sin importar el nivel:

    from app.core.access import require_paid
    @router.get("/...") async def f(_=Depends(require_paid)): ...
"""

import uuid
from typing import Optional

from fastapi import Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.challenge import Challenge
from app.models.user import User

# ─── Mensaje de paywall (reutilizado en ambas funciones) ──────────────────────

_PAYWALL = {
    "code": "LICENSE_REQUIRED",
    "message": (
        "Tu enlace neuronal no ha sido financiado. "
        "Adquiere una Licencia de Fundador para acceder al Nexo completo."
    ),
    "action_url": "https://pay.dakiedtech.com",
}


# ─── require_paid — compuerta total (sin freemium) ───────────────────────────

async def require_paid(
    user_id: Optional[uuid.UUID] = Query(None, description="UUID del operador autenticado"),
    db: AsyncSession = Depends(get_db),
) -> Optional[User]:
    """
    Dependencia de licencia total — no distingue niveles gratuitos.
    Útil para rutas que SIEMPRE requieren is_licensed (admin, certificados, etc.).

    - user_id ausente → devuelve None (modo invitado, sin bloqueo).
    - user_id presente, is_licensed=False → 402 Payment Required.
    - user_id presente, is_licensed=True  → devuelve el objeto User.
    """
    if user_id is None:
        return None

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Operador no encontrado.",
        )

    if not user.is_licensed:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=_PAYWALL,
        )

    return user


# ─── check_freemium_access — compuerta inteligente por nivel ─────────────────

async def check_freemium_access(
    db: AsyncSession,
    challenge_id: uuid.UUID,
    user_id: Optional[uuid.UUID],
) -> Optional[User]:
    """
    Verifica el acceso freemium para un nivel concreto.

    Reglas:
      1. Si challenge.is_free=True  → devuelve None (acceso libre, sin validar usuario).
      2. Si challenge.is_free=False y user_id=None  → 402 (invitado intenta nivel de pago).
      3. Si challenge.is_free=False y usuario no encontrado → 404.
      4. Si challenge.is_free=False y is_licensed=False → 402.
      5. Si challenge.is_free=False y is_licensed=True  → devuelve el objeto User.

    Llamar directamente desde el cuerpo del endpoint (no como dependencia FastAPI,
    porque challenge_id está en el body y no en Query/Path).
    """
    # Carga el challenge para leer is_free
    challenge: Optional[Challenge] = await db.get(Challenge, challenge_id)
    if challenge is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Misión no encontrada.",
        )

    # Nivel del demo — acceso libre sin validar usuario
    if challenge.is_free:
        return None

    # Nivel de pago — user_id obligatorio
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=_PAYWALL,
        )

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Operador no encontrado.",
        )

    if not user.is_licensed:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=_PAYWALL,
        )

    return user
