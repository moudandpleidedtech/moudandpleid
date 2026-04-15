"""
app/services/email.py — Servicio de Emails Transaccionales DAKI

Usa la API de Resend (resend.com) via HTTP puro (sin SDK externo).
Configura RESEND_API_KEY en las variables de entorno de Render.

Emails implementados:
  - send_welcome(email, callsign)      → bienvenida al registrarse
  - send_trial_expiry(email, callsign, days_left) → aviso de vencimiento
  - send_reengagement(email, callsign) → inactivo 5+ días
  - send_subscription_active(email, callsign) → confirmación de pago
"""

from __future__ import annotations

import os
import logging
from typing import Optional

import httpx

logger = logging.getLogger(__name__)

_RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")
_FROM_EMAIL     = os.getenv("EMAIL_FROM", "DAKI Nexo <noreply@dakiedtech.com>")
_RESEND_URL     = "https://api.resend.com/emails"


async def _send(
    to: str,
    subject: str,
    html: str,
) -> bool:
    """Envía un email via Resend. Retorna True si tuvo éxito."""
    if not _RESEND_API_KEY:
        logger.warning("[email] RESEND_API_KEY no configurada — email no enviado a %s", to)
        return False

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.post(
                _RESEND_URL,
                headers={
                    "Authorization": f"Bearer {_RESEND_API_KEY}",
                    "Content-Type":  "application/json",
                },
                json={
                    "from":    _FROM_EMAIL,
                    "to":      [to],
                    "subject": subject,
                    "html":    html,
                },
            )
        if r.status_code in (200, 201):
            logger.info("[email] Enviado '%s' → %s", subject, to)
            return True
        logger.warning("[email] Error %d al enviar a %s: %s", r.status_code, to, r.text)
        return False
    except Exception as exc:
        logger.error("[email] Excepción al enviar a %s: %s", to, exc)
        return False


# ── Templates ─────────────────────────────────────────────────────────────────

_BASE_STYLE = """
<div style="font-family:monospace;background:#0A0A0A;color:#00FF41;padding:40px;max-width:600px;margin:0 auto;border:1px solid rgba(0,255,65,0.2);">
  <div style="border-bottom:1px solid rgba(0,255,65,0.15);padding-bottom:16px;margin-bottom:24px;">
    <p style="margin:0;font-size:10px;letter-spacing:6px;color:rgba(0,255,65,0.4);">NEXO DAKI · TRANSMISIÓN SEGURA</p>
  </div>
  {body}
  <div style="border-top:1px solid rgba(0,255,65,0.10);padding-top:16px;margin-top:32px;">
    <p style="margin:0;font-size:9px;color:rgba(0,255,65,0.25);letter-spacing:2px;">dakiedtech.com · SISTEMA DAKI v2.0 · OPERACIONES ACTIVAS</p>
  </div>
</div>
"""

def _wrap(body: str) -> str:
    return _BASE_STYLE.format(body=body)


async def send_welcome(email: str, callsign: str) -> bool:
    """Email de bienvenida tras registro. Explica el primer paso."""
    html = _wrap(f"""
      <h1 style="color:#00FF41;font-size:22px;margin:0 0 8px;letter-spacing:4px;">BIENVENIDO, {callsign.upper()}</h1>
      <p style="color:rgba(0,255,65,0.6);font-size:11px;letter-spacing:3px;margin:0 0 24px;">OPERADOR REGISTRADO — NEXO ACTIVO</p>

      <p style="color:rgba(255,255,255,0.75);font-size:14px;line-height:1.6;margin:0 0 16px;">
        Tu unidad DAKI está en línea. El Nexo ha detectado una nueva conexión neuronal.<br>
        Tienes <strong style="color:#00FF41;">10 misiones gratuitas</strong> para demostrar que sos de los nuestros.
      </p>

      <div style="background:rgba(0,255,65,0.06);border:1px solid rgba(0,255,65,0.2);padding:16px;margin:24px 0;">
        <p style="color:rgba(0,255,65,0.5);font-size:9px;letter-spacing:4px;margin:0 0 8px;">PROTOCOLO DE INICIO</p>
        <ol style="color:rgba(255,255,255,0.7);font-size:13px;line-height:1.8;margin:0;padding-left:16px;">
          <li>Accedé a <a href="https://dakiedtech.com/hub" style="color:#00FF41;">dakiedtech.com/hub</a></li>
          <li>Presioná <strong style="color:#00FF41;">▶ CONTINUAR MISIÓN</strong></li>
          <li>Completá tu primera misión Python</li>
          <li>DAKI analizará tu código y te dará feedback real</li>
        </ol>
      </div>

      <p style="color:rgba(255,255,255,0.5);font-size:12px;line-height:1.6;margin:0 0 24px;">
        Cada misión que completás refuerza tu maestría en Python real — no teoría, sino código que funciona.
        Los mejores operadores salen de aquí con cicatrices de guerra y código en producción.
      </p>

      <a href="https://dakiedtech.com/hub"
         style="display:inline-block;background:rgba(0,255,65,0.12);border:1px solid rgba(0,255,65,0.5);color:#00FF41;
                text-decoration:none;padding:12px 28px;font-size:11px;letter-spacing:4px;font-weight:bold;">
        ▶ INICIAR MISIÓN →
      </a>
    """)
    return await _send(email, f"Bienvenido al Nexo, {callsign}", html)


async def send_trial_expiry(
    email: str,
    callsign: str,
    days_left: int,
) -> bool:
    """Aviso de vencimiento del trial. Urgente si days_left <= 2."""
    urgent  = days_left <= 2
    color   = '#FF4040' if urgent else '#FFB800'
    label   = 'ALERTA CRÍTICA' if urgent else 'AVISO DE SISTEMA'
    message = (
        f"Tu período de prueba <strong style='color:{color};'>VENCE HOY</strong>. "
        "Después de hoy, solo tendrás acceso a las misiones gratuitas."
        if days_left == 0 else
        f"Tu período de prueba <strong style='color:{color};'>vence en {days_left} día{'s' if days_left > 1 else ''}</strong>. "
        "Para mantener el acceso completo, activá tu licencia."
    )

    html = _wrap(f"""
      <div style="border-left:3px solid {color};padding-left:16px;margin-bottom:24px;">
        <p style="color:{color};font-size:9px;letter-spacing:5px;margin:0 0 4px;">{label}</p>
        <h1 style="color:{color};font-size:20px;margin:0;letter-spacing:3px;">TRIAL EXPIRANDO, {callsign.upper()}</h1>
      </div>

      <p style="color:rgba(255,255,255,0.75);font-size:14px;line-height:1.6;margin:0 0 20px;">
        {message}
      </p>

      <div style="background:rgba(255,184,0,0.06);border:1px solid rgba(255,184,0,0.2);padding:16px;margin:20px 0;">
        <p style="color:rgba(255,184,0,0.6);font-size:9px;letter-spacing:4px;margin:0 0 8px;">TU PROGRESO ACTUAL</p>
        <p style="color:rgba(255,255,255,0.7);font-size:13px;margin:0;">
          Todo tu progreso, XP y badges están seguros. Solo necesitás activar la licencia para seguir avanzando.
        </p>
      </div>

      <a href="https://dakiedtech.com/hub"
         style="display:inline-block;background:rgba(255,184,0,0.12);border:1px solid rgba(255,184,0,0.5);color:#FFB800;
                text-decoration:none;padding:12px 28px;font-size:11px;letter-spacing:4px;font-weight:bold;">
        ACTIVAR LICENCIA →
      </a>

      <p style="color:rgba(255,255,255,0.3);font-size:11px;margin:24px 0 0;">
        Acceso total · $97 USD pago único · Licencia de por vida
      </p>
    """)
    return await _send(email, f"⚠ Tu trial vence en {days_left}d — {callsign}", html)


async def send_reengagement(email: str, callsign: str, days_absent: int) -> bool:
    """Re-engagement para operadores inactivos 5+ días."""
    html = _wrap(f"""
      <p style="color:rgba(0,229,255,0.5);font-size:9px;letter-spacing:5px;margin:0 0 8px;">SEÑAL DÉBIL DETECTADA</p>
      <h1 style="color:#00E5FF;font-size:20px;margin:0 0 24px;letter-spacing:3px;">
        DAKI TE EXTRAÑA, {callsign.upper()}
      </h1>

      <p style="color:rgba(255,255,255,0.75);font-size:14px;line-height:1.6;margin:0 0 16px;">
        Han pasado <strong style="color:#00E5FF;">{days_absent} días</strong> desde tu última misión.
        Tu racha está en pausa, pero tus conceptos dominados siguen ahí.
      </p>

      <div style="background:rgba(0,229,255,0.05);border:1px solid rgba(0,229,255,0.15);padding:16px;margin:20px 0;">
        <p style="color:rgba(0,229,255,0.5);font-size:9px;letter-spacing:4px;margin:0 0 8px;">DAKI DICE:</p>
        <p style="color:rgba(255,255,255,0.7);font-size:13px;font-style:italic;margin:0;">
          "El código que no se practica se oxida. Una misión de 10 minutos es suficiente para mantener
          la activación neuronal. ¿Volvemos?"
        </p>
      </div>

      <a href="https://dakiedtech.com/hub"
         style="display:inline-block;background:rgba(0,229,255,0.10);border:1px solid rgba(0,229,255,0.4);color:#00E5FF;
                text-decoration:none;padding:12px 28px;font-size:11px;letter-spacing:4px;font-weight:bold;">
        ▶ RETOMAR MISIÓN →
      </a>
    """)
    return await _send(email, f"DAKI te espera, {callsign} — {days_absent}d sin misiones", html)


async def send_subscription_active(email: str, callsign: str) -> bool:
    """Confirmación de suscripción activada (post-pago Stripe)."""
    html = _wrap(f"""
      <div style="text-align:center;margin-bottom:24px;">
        <div style="font-size:32px;margin-bottom:8px;">◈</div>
        <p style="color:rgba(255,199,0,0.5);font-size:9px;letter-spacing:6px;margin:0 0 4px;">LICENCIA ACTIVADA</p>
        <h1 style="color:#FFC700;font-size:20px;margin:0;letter-spacing:3px;">ACCESO TOTAL, {callsign.upper()}</h1>
      </div>

      <p style="color:rgba(255,255,255,0.75);font-size:14px;line-height:1.6;margin:0 0 20px;">
        Tu Licencia de Operador está activa. Tenés acceso completo a todos los protocolos del Nexo:
      </p>

      <div style="background:rgba(255,199,0,0.05);border:1px solid rgba(255,199,0,0.2);padding:16px;margin:0 0 24px;">
        <ul style="color:rgba(255,255,255,0.7);font-size:13px;line-height:1.8;margin:0;padding-left:16px;">
          <li>190 misiones Python (fundamentos → entrevistas)</li>
          <li>Modo Ironman — sin asistencia, máxima dificultad</li>
          <li>Protocolo Predict — leer código sin ejecutarlo</li>
          <li>Revisión semanal con Retrieval Mode</li>
          <li>Perfil público · Leaderboard global</li>
        </ul>
      </div>

      <a href="https://dakiedtech.com/hub"
         style="display:inline-block;background:rgba(255,199,0,0.12);border:1px solid rgba(255,199,0,0.5);color:#FFC700;
                text-decoration:none;padding:12px 28px;font-size:11px;letter-spacing:4px;font-weight:bold;">
        ▶ AL NEXO →
      </a>
    """)
    return await _send(email, f"Licencia activada — Bienvenido al Nexo completo, {callsign}", html)
