"""
lemonsqueezy.py — Integración Lemon Squeezy (Directiva 011-LS)

Rutas:

  POST /api/v1/lemon/checkout
    Genera la URL de checkout de Lemon Squeezy para el plan elegido.
    Embeds user_id como custom_data para identificar al operador en el webhook.
    Requiere JWT del Operador.

  POST /api/v1/lemon/webhook
    Recibe eventos de Lemon Squeezy.
    Verifica firma HMAC-SHA256 en header X-Signature.
    Eventos procesados:
      • order_created        → Licencia Vitalicia — activa is_licensed + subscription_status=ACTIVE
      • subscription_created → Plan mensual — activa subscription_status=ACTIVE
      • subscription_updated → Actualiza estado (active/cancelled/expired/past_due)
      • subscription_expired → subscription_status=EXPIRED

Variables de entorno requeridas (Render → Environment):
    LEMONSQUEEZY_API_KEY             — lmsk_... (Settings → API)
    LEMONSQUEEZY_WEBHOOK_SECRET      — signing secret del webhook configurado
    LEMONSQUEEZY_MONTHLY_VARIANT_ID  — variant ID del plan $29/mes
    LEMONSQUEEZY_LIFETIME_VARIANT_ID — variant ID de la licencia vitalicia $97
    LEMONSQUEEZY_STORE_SLUG          — slug de la tienda (ej: "daki-nexo")
"""

import asyncio
import hashlib
import hmac
import json
import uuid
from urllib.parse import urlencode

from fastapi import APIRouter, Depends, Header, HTTPException, Request, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.core.security import get_current_operator
from app.models.user import User
from app.services.alerts import fire_sale_alert
from app.services.email import send_subscription_active

router = APIRouter(prefix="/lemon", tags=["lemon-squeezy"])


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _verify_ls_signature(secret: str, payload: bytes, signature: str) -> bool:
    """Verifica la firma HMAC-SHA256 que Lemon Squeezy envía en X-Signature."""
    expected = hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


def _build_checkout_url(store_slug: str, variant_id: str, email: str, user_id: str) -> str:
    """
    Construye la URL de checkout de Lemon Squeezy con datos del operador.
    El user_id viaja como custom_data y regresa en el webhook para identificar al usuario.
    """
    base = f"https://{store_slug}.lemonsqueezy.com/checkout/buy/{variant_id}"
    params = {
        "checkout[email]": email,
        "checkout[custom][user_id]": user_id,
        # Pre-fill name si está disponible — mejora UX
    }
    return f"{base}?{urlencode(params)}"


async def _activate_user(
    db: AsyncSession,
    user_id: str | None,
    email: str | None,
    plan: str,           # "monthly" | "lifetime"
    ls_order_id: str,
) -> User:
    """
    Busca al operador por user_id (preferido) o por email (fallback),
    y activa su acceso según el plan.
    """
    user: User | None = None

    # Prioridad: user_id embebido en custom_data
    if user_id:
        try:
            uid = uuid.UUID(user_id)
            result = await db.execute(select(User).where(User.id == uid))
            user = result.scalar_one_or_none()
        except ValueError:
            pass

    # Fallback: email del comprador
    if user is None and email:
        result = await db.execute(
            select(User).where(User.email == email.lower().strip())
        )
        user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Operador no encontrado (user_id={user_id}, email={email}).",
        )

    user.subscription_status = "ACTIVE"
    user.is_licensed         = True
    user.payment_id          = ls_order_id

    await db.flush()
    return user


# ─── Ruta 1: Generar URL de checkout ─────────────────────────────────────────

class CheckoutRequest(BaseModel):
    plan: str = "monthly"   # "monthly" | "lifetime"


class CheckoutResponse(BaseModel):
    checkout_url: str


@router.post(
    "/checkout",
    response_model=CheckoutResponse,
    status_code=status.HTTP_200_OK,
    summary="Genera URL de checkout de Lemon Squeezy con user_id embebido",
)
async def create_ls_checkout(
    body:     CheckoutRequest,
    operator: User = Depends(get_current_operator),
) -> CheckoutResponse:
    missing = []
    if not settings.LEMONSQUEEZY_STORE_SLUG:
        missing.append("LEMONSQUEEZY_STORE_SLUG")
    if body.plan == "lifetime" and not settings.LEMONSQUEEZY_LIFETIME_VARIANT_ID:
        missing.append("LEMONSQUEEZY_LIFETIME_VARIANT_ID")
    if body.plan == "monthly" and not settings.LEMONSQUEEZY_MONTHLY_VARIANT_ID:
        missing.append("LEMONSQUEEZY_MONTHLY_VARIANT_ID")

    if missing:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Pasarela no configurada. Variables faltantes: {', '.join(missing)}",
        )

    variant_id = (
        settings.LEMONSQUEEZY_LIFETIME_VARIANT_ID
        if body.plan == "lifetime"
        else settings.LEMONSQUEEZY_MONTHLY_VARIANT_ID
    )

    url = _build_checkout_url(
        store_slug=settings.LEMONSQUEEZY_STORE_SLUG,
        variant_id=variant_id,
        email=operator.email,
        user_id=str(operator.id),
    )

    return CheckoutResponse(checkout_url=url)


# ─── Ruta 2: Webhook de Lemon Squeezy ────────────────────────────────────────

# Mapeo de estados de suscripción LS → estados internos
_LS_SUB_STATUS_MAP: dict[str, str] = {
    "active":    "ACTIVE",
    "past_due":  "PAST_DUE",
    "unpaid":    "PAST_DUE",
    "cancelled": "CANCELLED",
    "expired":   "EXPIRED",
    "paused":    "PAUSED",
    "on_trial":  "TRIAL",
}


@router.post(
    "/webhook",
    status_code=status.HTTP_200_OK,
    summary="Webhook de Lemon Squeezy — activa licencias tras pago exitoso",
)
async def ls_webhook(
    request:     Request,
    db:          AsyncSession = Depends(get_db),
    x_signature: str | None   = Header(None, alias="X-Signature"),
) -> dict:
    body = await request.body()

    # ── Verificación de firma ─────────────────────────────────────────────────
    if not settings.LEMONSQUEEZY_WEBHOOK_SECRET:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="LEMONSQUEEZY_WEBHOOK_SECRET no configurado.",
        )

    if not x_signature:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Falta el header X-Signature.",
        )

    if not _verify_ls_signature(settings.LEMONSQUEEZY_WEBHOOK_SECRET, body, x_signature):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Firma X-Signature inválida — evento rechazado.",
        )

    # ── Parseo del payload ────────────────────────────────────────────────────
    try:
        payload: dict = json.loads(body)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Payload no es JSON válido.",
        )

    meta       = payload.get("meta", {})
    event_name = meta.get("event_name", "")
    custom     = meta.get("custom_data") or {}
    data_attrs = payload.get("data", {}).get("attributes", {})

    user_id_raw: str | None = custom.get("user_id")
    email: str | None = data_attrs.get("user_email") or data_attrs.get("email")

    # ── order_created → Licencia Vitalicia ───────────────────────────────────
    if event_name == "order_created":
        order_status = data_attrs.get("status", "")
        if order_status != "paid":
            return {"received": True, "processed": False, "reason": f"order status '{order_status}' ignorado"}

        ls_order_id = str(payload.get("data", {}).get("id", "ls-order"))

        user = await _activate_user(db, user_id_raw, email, "lifetime", ls_order_id)
        asyncio.create_task(fire_sale_alert(user.email))
        asyncio.create_task(send_subscription_active(user.email, user.callsign))

        return {
            "received":  True,
            "processed": True,
            "event":     event_name,
            "plan":      "lifetime",
            "user_id":   str(user.id),
            "callsign":  user.callsign,
        }

    # ── subscription_created → Plan mensual activado ─────────────────────────
    if event_name == "subscription_created":
        ls_sub_id = str(payload.get("data", {}).get("id", "ls-sub"))

        user = await _activate_user(db, user_id_raw, email, "monthly", ls_sub_id)
        asyncio.create_task(fire_sale_alert(user.email))
        asyncio.create_task(send_subscription_active(user.email, user.callsign))

        return {
            "received":  True,
            "processed": True,
            "event":     event_name,
            "plan":      "monthly",
            "user_id":   str(user.id),
            "callsign":  user.callsign,
        }

    # ── subscription_updated / subscription_expired → sincronizar estado ─────
    if event_name in ("subscription_updated", "subscription_expired", "subscription_cancelled"):
        ls_status    = data_attrs.get("status", "")
        internal_status = _LS_SUB_STATUS_MAP.get(ls_status, "UNKNOWN")

        if not user_id_raw and not email:
            return {"received": True, "processed": False, "reason": "sin user_id ni email para identificar operador"}

        user: User | None = None
        if user_id_raw:
            try:
                result = await db.execute(select(User).where(User.id == uuid.UUID(user_id_raw)))
                user = result.scalar_one_or_none()
            except ValueError:
                pass
        if user is None and email:
            result = await db.execute(select(User).where(User.email == email.lower().strip()))
            user = result.scalar_one_or_none()

        if user is None:
            return {"received": True, "processed": False, "reason": "operador no encontrado"}

        user.subscription_status = internal_status
        # Si la suscripción se cancela o expira, revocar acceso pago
        if internal_status in ("CANCELLED", "EXPIRED"):
            user.is_licensed = False
        await db.flush()

        return {
            "received":       True,
            "processed":      True,
            "event":          event_name,
            "ls_status":      ls_status,
            "internal_status": internal_status,
            "user_id":        str(user.id),
        }

    # ── Eventos no procesados — confirmar recepción (LS reintenta en 5xx) ─────
    return {"received": True, "processed": False, "event": event_name}
