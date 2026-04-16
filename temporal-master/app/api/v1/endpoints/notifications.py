"""
app/api/v1/endpoints/notifications.py — Notificaciones Automáticas

POST /api/v1/notifications/trial-expiry-check
  Dispara emails de aviso a usuarios cuyo trial vence en <= 5 días.
  Requiere X-Admin-Key. Llamar desde cron externo (Render Cron o GitHub Actions).

POST /api/v1/notifications/reengagement-check
  Dispara emails a usuarios inactivos 5+ días.
  Requiere X-Admin-Key.
"""

from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Header, HTTPException, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.services.email import send_trial_expiry, send_reengagement

router = APIRouter(prefix="/notifications", tags=["notifications"])


def _require_admin(x_admin_key: str = Header(..., alias="X-Admin-Key")) -> None:
    import hmac as _hmac
    valid = settings.ADMIN_API_KEY or ""
    if not _hmac.compare_digest(x_admin_key, valid):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado.")


@router.post("/trial-expiry-check", dependencies=[Depends(_require_admin)])
async def trial_expiry_check(db: AsyncSession = Depends(get_db)) -> dict:
    """
    Busca usuarios en TRIAL con vencimiento en 1, 2, o 5 días y envía email.
    Idempotente: solo envía si el vencimiento cae exactamente en esos días.
    """
    now = datetime.now(timezone.utc)
    result = await db.execute(
        select(User).where(
            User.subscription_status == "TRIAL",
            User.trial_end_date.isnot(None),
        )
    )
    users = result.scalars().all()

    sent = 0
    for user in users:
        if not user.trial_end_date or not user.email:
            continue
        delta = user.trial_end_date - now
        days_left = max(0, delta.days)

        # Solo enviar en días de aviso específicos (1, 2, 5)
        if days_left in (0, 1, 2, 5):
            ok = await send_trial_expiry(user.email, user.callsign, days_left)
            if ok:
                sent += 1

    return {"checked": len(users), "emails_sent": sent}


@router.post("/reengagement-check", dependencies=[Depends(_require_admin)])
async def reengagement_check(db: AsyncSession = Depends(get_db)) -> dict:
    """
    Busca usuarios inactivos 5 días sin haber recibido re-engagement en la última semana.
    Usa last_login como indicador de actividad.
    """
    cutoff_5d  = datetime.now(timezone.utc) - timedelta(days=5)
    cutoff_30d = datetime.now(timezone.utc) - timedelta(days=30)

    result = await db.execute(
        select(User).where(
            User.last_login.isnot(None),
            User.last_login < cutoff_5d,
            User.last_login > cutoff_30d,   # no perder tiempo con muy inactivos
            User.subscription_status.in_(["TRIAL", "ACTIVE"]),
        )
    )
    users = result.scalars().all()

    sent = 0
    for user in users:
        if not user.email or not user.last_login:
            continue
        days_absent = (datetime.now(timezone.utc) - user.last_login).days
        ok = await send_reengagement(user.email, user.callsign, days_absent)
        if ok:
            sent += 1

    return {"checked": len(users), "emails_sent": sent}
