"""
access.py — Dependencias de acceso que protegen las rutas de niveles.

Uso en cualquier endpoint que requiera licencia activa:

    from app.core.access import require_paid

    @router.post("/evaluate")
    async def evaluate(
        payload: EvaluateRequest,
        _: None = Depends(require_paid),          # si no es paid → 402
        db: AsyncSession = Depends(get_db),
    ): ...

La dependencia recibe el user_id del body o del query param.
Si el usuario no existe o is_paid=False devuelve 402 Payment Required.
Si user_id es None (invitado sin sesión), deja pasar para que el
endpoint decida qué mostrar (acceso demo/preview sin score).
"""

import uuid
from typing import Optional

from fastapi import Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.user import User


async def require_paid(
    user_id: Optional[uuid.UUID] = Query(None, description="UUID del operador autenticado"),
    db: AsyncSession = Depends(get_db),
) -> Optional[User]:
    """
    Devuelve el objeto User si tiene licencia activa.
    Devuelve None si user_id es None (modo invitado — sin bloqueo).
    Lanza 402 si el usuario existe pero is_paid=False.
    Lanza 404 si user_id está presente pero no existe en la BD.
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

    if not user.is_paid:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail={
                "code": "LICENSE_REQUIRED",
                "message": (
                    "Tu enlace neuronal no ha sido financiado. "
                    "Adquiere una Licencia de Operador para acceder al Nexo."
                ),
                "action_url": "https://pay.dakiedtech.com",
            },
        )

    return user
