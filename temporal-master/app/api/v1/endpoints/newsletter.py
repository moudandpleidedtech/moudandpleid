"""
POST /api/v1/newsletter/subscribe

Captura de emails para "Transmisiones del Nexo".
Envía email de bienvenida al suscriptor vía Resend.
No requiere autenticación — endpoint público.
"""

import re
import os
import logging

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, field_validator

from app.services.email import _send

logger = logging.getLogger(__name__)

router = APIRouter()

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_ADMIN_EMAIL = os.getenv("EMAIL_ADMIN", "moundandpleidedtech@gmail.com")


class NewsletterSignup(BaseModel):
    email: str
    source: str = "blog"

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        v = v.strip().lower()
        if not _EMAIL_RE.match(v):
            raise ValueError("Email inválido")
        if len(v) > 254:
            raise ValueError("Email demasiado largo")
        return v


_WELCOME_HTML = """\
<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"></head>
<body style="background:#020202;color:#00FF41;font-family:monospace;padding:32px;max-width:560px;margin:auto">
  <p style="font-size:10px;letter-spacing:.4em;color:rgba(0,255,65,.4);text-transform:uppercase;margin-bottom:24px">
    // TRANSMISIONES DEL NEXO
  </p>
  <h1 style="font-size:22px;font-weight:900;text-transform:uppercase;color:rgba(255,255,255,.85);letter-spacing:.05em;margin-bottom:8px">
    Sos parte del Nexo.
  </h1>
  <p style="color:rgba(255,255,255,.45);font-size:13px;line-height:1.7;margin-bottom:24px">
    Cada semana vas a recibir un despacho con artículos de Python aplicado,
    novedades de la plataforma y los movimientos del leaderboard.
    Sin spam. Sin teoría muerta.
  </p>
  <a href="https://dakiedtech.com/register"
     style="display:inline-block;border:1px solid rgba(0,255,65,.45);color:#00FF41;text-decoration:none;
            font-size:10px;letter-spacing:.4em;text-transform:uppercase;padding:12px 24px">
    EMPEZAR MISIONES GRATIS →
  </a>
  <p style="color:rgba(255,255,255,.15);font-size:9px;letter-spacing:.3em;margin-top:32px">
    © 2026 DAKIedtech · dakiedtech.com
  </p>
</body>
</html>
"""


@router.post(
    "/newsletter/subscribe",
    status_code=status.HTTP_200_OK,
    summary="Suscripción a Transmisiones del Nexo",
)
async def subscribe(payload: NewsletterSignup) -> dict:
    ok = await _send(
        to=payload.email,
        subject="Bienvenido al Nexo — Transmisiones de DAKI",
        html=_WELCOME_HTML,
    )

    await _send(
        to=_ADMIN_EMAIL,
        subject=f"[Nexo] Nueva suscripción: {payload.email} ({payload.source})",
        html=f"<p>Nuevo suscriptor: <strong>{payload.email}</strong> — fuente: {payload.source}</p>",
    )

    if not ok:
        logger.warning("[newsletter] Email no enviado a %s (Resend no configurado)", payload.email)

    return {"status": "ok", "message": "Suscripción registrada"}
