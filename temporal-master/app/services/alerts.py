"""
alerts.py — CEO Alert System para DAKI EdTech

Canales soportados (configura en .env los que uses):
  • Discord webhook  → ALERT_DISCORD_WEBHOOK=https://discord.com/api/webhooks/ID/TOKEN
  • Telegram bot     → ALERT_TELEGRAM_BOT_TOKEN=123:ABC... + ALERT_TELEGRAM_CHAT_ID=@canal

Uso (fire-and-forget — no bloquea el response del endpoint):
    import asyncio
    from app.services.alerts import fire_sale_alert, fire_security_alert

    asyncio.create_task(fire_sale_alert("usuario@email.com"))
    asyncio.create_task(fire_security_alert(
        challenge_id="uuid-...",
        detail="El identificador 'exec' está bloqueado por el Nexo.",
        snippet="exec('rm -rf /')",
    ))

Si ningún canal está configurado las funciones son no-ops silenciosos.
Ambos canales se intentan en paralelo; un fallo en uno no cancela el otro.
"""

import asyncio
import logging
from datetime import datetime, timezone

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


# ─── Patrones de inyección real (excluye "import math" estudiantil) ───────────

_INJECTION_PATTERNS: frozenset[str] = frozenset({
    # Ejecución dinámica — siempre intencional
    "exec", "eval", "compile",
    # Bypass de importación  — claramente ofensivo
    "__import__",
    # Acceso a dunders de clase — escape de sandbox clásico
    "__class__", "__subclasses__", "__bases__", "__builtins__",
    # Reflexión en tiempo de ejecución
    "getattr", "setattr", "delattr",
    # Otros vectores avanzados
    "memoryview", "breakpoint",
})


def is_injection_attempt(error_detail: str) -> bool:
    """
    Devuelve True si el error del AST Guard sugiere un intento de escape del sandbox.
    Un simple `import os` de un estudiante no activa esta función.
    Un `exec(...)` o `getattr(obj, '__class__')` sí lo hace.
    """
    return any(pattern in error_detail for pattern in _INJECTION_PATTERNS)


# ─── Timestamp ISO 8601 ────────────────────────────────────────────────────────

def _ts() -> str:
    return datetime.now(timezone.utc).isoformat()


# ─── Formateadores Discord ─────────────────────────────────────────────────────

def _embed_sale(email: str) -> dict:
    return {
        "embeds": [{
            "title": "💰 ¡Nueva Incursión Financiada!",
            "description": (
                f"**{email}** se ha unido a DAKI EdTech.\n"
                f"La licencia fue activada automáticamente."
            ),
            "color": 5763719,     # verde éxito
            "footer": {"text": "DAKI EdTech · Sistema de Ventas"},
            "timestamp": _ts(),
        }]
    }


def _embed_security(challenge_id: str, detail: str, snippet: str) -> dict:
    clean = snippet[:300].strip()
    snippet_block = f"```python\n{clean}\n```" if clean else "*(fragmento no disponible)*"
    return {
        "embeds": [{
            "title": "⚠️ Intento de Violación de Seguridad",
            "description": (
                f"**Nivel:** `{challenge_id}`\n"
                f"**Detección AST:** {detail}\n\n"
                f"**Fragmento enviado:**\n{snippet_block}"
            ),
            "color": 15548997,    # rojo alarma
            "footer": {"text": "DAKI EdTech · Sandbox Guardian"},
            "timestamp": _ts(),
        }]
    }


# ─── Senders por canal ─────────────────────────────────────────────────────────

async def _send_discord(payload: dict) -> None:
    if not settings.ALERT_DISCORD_WEBHOOK:
        return
    async with httpx.AsyncClient(timeout=8.0) as client:
        r = await client.post(settings.ALERT_DISCORD_WEBHOOK, json=payload)
        r.raise_for_status()


async def _send_telegram(html: str) -> None:
    if not settings.ALERT_TELEGRAM_BOT_TOKEN or not settings.ALERT_TELEGRAM_CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{settings.ALERT_TELEGRAM_BOT_TOKEN}/sendMessage"
    async with httpx.AsyncClient(timeout=8.0) as client:
        r = await client.post(url, json={
            "chat_id": settings.ALERT_TELEGRAM_CHAT_ID,
            "text": html,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        })
        r.raise_for_status()


# ─── Dispatcher ───────────────────────────────────────────────────────────────

async def _dispatch(discord_payload: dict, telegram_html: str) -> None:
    """
    Envía a todos los canales configurados en paralelo.
    Los errores de red o HTTP se loguean pero nunca se propagan al caller.
    """
    # Early exit si no hay ningún canal configurado
    if not settings.ALERT_DISCORD_WEBHOOK and not settings.ALERT_TELEGRAM_BOT_TOKEN:
        return

    results = await asyncio.gather(
        _send_discord(discord_payload),
        _send_telegram(telegram_html),
        return_exceptions=True,
    )
    for exc in results:
        if isinstance(exc, Exception):
            logger.warning("DAKI Alert — error en canal: %s", exc)


# ─── API pública ──────────────────────────────────────────────────────────────

async def fire_sale_alert(email: str) -> None:
    """
    Alerta de nueva venta / activación de licencia.

    Uso recomendado (fire-and-forget):
        asyncio.create_task(fire_sale_alert(email))
    """
    await _dispatch(
        _embed_sale(email),
        (
            f"💰 <b>¡Nueva Incursión Financiada!</b>\n"
            f"Usuario <code>{email}</code> se ha unido a DAKI EdTech.\n"
            f"Licencia activada automáticamente."
        ),
    )


async def fire_security_alert(
    challenge_id: str,
    detail: str,
    snippet: str = "",
) -> None:
    """
    Alerta de intento de inyección / escape del sandbox bloqueado por el AST Guard.

    Uso recomendado (fire-and-forget):
        asyncio.create_task(fire_security_alert(str(challenge_id), detail, codigo))
    """
    await _dispatch(
        _embed_security(challenge_id, detail, snippet),
        (
            f"⚠️ <b>Intento de violación de seguridad detectado en Nivel "
            f"<code>{challenge_id}</code></b>\n"
            f"<b>Detección:</b> {detail}"
        ),
    )


# ─── Alerta: Anthropic sin créditos / API key inválida ────────────────────────
# Throttle local para no spamear el webhook si el satélite está caído largo rato.
_CREDIT_ALERT_THROTTLE_S: float = 600.0   # 10 min entre notificaciones del mismo tipo
_credit_alert_last_sent: dict[str, float] = {}


def _embed_satellite(reason: str, detail: str) -> dict:
    return {
        "embeds": [{
            "title": "🛰️ DAKI · Satélite IA fuera de línea",
            "description": (
                f"**Motivo:** {reason}\n"
                f"**Detalle:** {detail[:500]}\n\n"
                f"Las consultas a DAKI están degradadas hasta que se restaure el canal."
            ),
            "color": 16753920,    # naranja crítico
            "footer": {"text": "DAKI EdTech · Anthropic API Monitor"},
            "timestamp": _ts(),
        }]
    }


async def fire_satellite_alert(reason: str, detail: str = "") -> None:
    """
    Alerta de degradación del satélite IA (Anthropic).

    `reason` ∈ {'credit_balance_low', 'auth_failed', 'rate_limited', 'api_error'}
    Aplica throttle de 10 min por motivo para evitar spam si la condición persiste.

    Uso (fire-and-forget):
        asyncio.create_task(fire_satellite_alert("credit_balance_low", str(exc)))
    """
    import time
    now = time.monotonic()
    last = _credit_alert_last_sent.get(reason, 0.0)
    if now - last < _CREDIT_ALERT_THROTTLE_S:
        return
    _credit_alert_last_sent[reason] = now

    await _dispatch(
        _embed_satellite(reason, detail),
        (
            f"🛰️ <b>DAKI · Satélite IA fuera de línea</b>\n"
            f"<b>Motivo:</b> <code>{reason}</code>\n"
            f"<b>Detalle:</b> {detail[:300]}"
        ),
    )
