"""
payments.py — Pasarela de Pagos Global (Directiva 011)

Rutas:

  POST /api/v1/payments/create-checkout-session
    Crea una Stripe Checkout Session para suscripción mensual ($25/mes).
    Requiere JWT del Operador.
    Envía user_id como client_reference_id para que el webhook identifique al usuario.

  POST /api/v1/payments/webhook
    Recibe eventos de pasarelas de pago.
    — Stripe-Signature presente: valida con stripe.Webhook.construct_event() (STRIPE_WEBHOOK_SECRET).
        • checkout.session.completed → subscription_status='ACTIVE', guarda stripe_customer_id
    — X-Webhook-Signature presente: valida con HMAC-SHA256 (PAYMENT_WEBHOOK_SECRET).
        • Procesadores genéricos (PayPal, Hotmart) → is_licensed=True por email

  POST /api/v1/payments/verify
    Activación manual admin. Requiere header X-Admin-Key.

Variables de entorno requeridas:
    STRIPE_SECRET_KEY         — sk_test_... o sk_live_...
    STRIPE_WEBHOOK_SECRET     — whsec_... (Dashboard → Developers → Webhooks)
    STRIPE_PRICE_ID           — price_... (producto mensual $25 USD)
    PAYMENT_WEBHOOK_SECRET    — secreto HMAC para pasarelas genéricas
    SECRET_KEY                — admin key de fallback
"""

import asyncio
import hashlib
import hmac
import json
import uuid
from typing import Any

import stripe
from fastapi import APIRouter, Depends, Header, HTTPException, Request, status
from pydantic import BaseModel, field_validator
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.core.security import get_current_operator
from app.models.user import User
from app.services.alerts import fire_sale_alert
from app.services.email import send_subscription_active

router = APIRouter(prefix="/payments", tags=["payments"])


# ─── Helpers internos ─────────────────────────────────────────────────────────

def _verify_hmac(secret: str, payload: bytes, signature: str) -> bool:
    """Verifica firma HMAC-SHA256 para pasarelas genéricas (PayPal, Hotmart, etc.)."""
    expected = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    # Stripe envía "t=timestamp,v1=firma" — extraemos solo la firma si se usa esta ruta
    sig = signature.split("v1=")[-1] if "v1=" in signature else signature
    return hmac.compare_digest(expected, sig)


async def _activate_user_by_email(db: AsyncSession, email: str, payment_id: str) -> User:
    """Busca al usuario por email y activa su licencia (flujo pasarelas genéricas)."""
    result = await db.execute(
        select(User).where(User.email == email.lower().strip())
    )
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe ningún operador con el email '{email}'.",
        )
    user.is_licensed = True
    user.payment_id  = payment_id
    await db.flush()
    return user


def _extract_email(payload: dict[str, Any]) -> str | None:
    """Extrae el email del comprador de payloads de distintas pasarelas."""
    if "email" in payload:
        return payload["email"]
    obj = payload.get("data", {}).get("object", {})
    if obj.get("customer_email"):
        return obj["customer_email"]
    if obj.get("billing_details", {}).get("email"):
        return obj["billing_details"]["email"]
    if obj.get("receipt_email"):
        return obj["receipt_email"]
    payer = payload.get("resource", {}).get("payer", {})
    if payer.get("email_address"):
        return payer["email_address"]
    buyer = payload.get("data", {}).get("buyer", {})
    if buyer.get("email"):
        return buyer["email"]
    return None


# ─── Ruta 1: Crear Stripe Checkout Session ────────────────────────────────────

class CheckoutSessionResponse(BaseModel):
    checkout_url: str


@router.post(
    "/create-checkout-session",
    response_model=CheckoutSessionResponse,
    status_code=status.HTTP_200_OK,
    summary="Crea una Stripe Checkout Session para suscripción mensual ($25/mes)",
)
async def create_checkout_session(
    operator: User = Depends(get_current_operator),
) -> CheckoutSessionResponse:
    if not settings.STRIPE_SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Pasarela de pagos no configurada. Contacta al administrador del Nexo.",
        )
    if not settings.STRIPE_PRICE_ID:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Precio de suscripción no configurado. Contacta al administrador del Nexo.",
        )

    stripe.api_key = settings.STRIPE_SECRET_KEY
    frontend_base  = (settings.FRONTEND_URL or "http://localhost:3000").rstrip("/")

    # Si el operador ya tiene un stripe_customer_id, lo reutilizamos para evitar
    # crear clientes duplicados en el dashboard de Stripe.
    create_kwargs: dict[str, Any] = {
        "mode":               "subscription",
        "line_items":         [{"price": settings.STRIPE_PRICE_ID, "quantity": 1}],
        "client_reference_id": str(operator.id),
        "success_url":        f"{frontend_base}/hub?checkout=success",
        "cancel_url":         f"{frontend_base}/hub?checkout=cancelled",
        "metadata": {
            "user_id":  str(operator.id),
            "callsign": operator.callsign,
        },
    }

    if operator.stripe_customer_id:
        create_kwargs["customer"] = operator.stripe_customer_id
    else:
        create_kwargs["customer_email"] = operator.email

    try:
        session = stripe.checkout.Session.create(**create_kwargs)
    except stripe.StripeError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Error al crear sesión de pago: {getattr(e, 'user_message', None) or str(e)}",
        )

    return CheckoutSessionResponse(checkout_url=session.url)


# ─── Ruta 2: Webhook de pasarela de pagos ─────────────────────────────────────

@router.post(
    "/webhook",
    status_code=status.HTTP_200_OK,
    summary="Webhook de pasarela — activa suscripción tras pago exitoso",
    description=(
        "Acepta eventos de Stripe (Stripe-Signature) o de pasarelas genéricas "
        "(X-Webhook-Signature). Para Stripe, usa stripe.Webhook.construct_event() "
        "con validación de timestamp para prevenir replay attacks."
    ),
)
async def payment_webhook(
    request:             Request,
    db:                  AsyncSession = Depends(get_db),
    x_webhook_signature: str | None   = Header(None, alias="X-Webhook-Signature"),
    stripe_signature:    str | None   = Header(None, alias="Stripe-Signature"),
) -> dict:
    body = await request.body()

    # ── Rama Stripe — construct_event con validación de timestamp ─────────────
    if stripe_signature:
        if not settings.STRIPE_WEBHOOK_SECRET:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="STRIPE_WEBHOOK_SECRET no configurado.",
            )
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            event = stripe.Webhook.construct_event(
                body, stripe_signature, settings.STRIPE_WEBHOOK_SECRET
            )
        except (ValueError, stripe.error.SignatureVerificationError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Firma Stripe inválida — evento rechazado.",
            )

        event_type: str = event.get("type", "")

        if event_type == "checkout.session.completed":
            session_obj = event["data"]["object"]
            client_ref  = session_obj.get("client_reference_id")
            customer_id = session_obj.get("customer")

            if not client_ref:
                return {"received": True, "processed": False, "reason": "client_reference_id ausente"}

            try:
                user_uuid = uuid.UUID(client_ref)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="client_reference_id no es un UUID válido.",
                )

            result = await db.execute(select(User).where(User.id == user_uuid))
            user   = result.scalar_one_or_none()

            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Operador con id '{client_ref}' no encontrado en el Nexo.",
                )

            user.subscription_status = "ACTIVE"
            user.is_licensed         = True
            if customer_id:
                user.stripe_customer_id = customer_id
            await db.flush()

            asyncio.create_task(fire_sale_alert(user.email))
            asyncio.create_task(send_subscription_active(user.email, user.callsign))

            return {
                "received":  True,
                "processed": True,
                "type":      event_type,
                "user_id":   str(user.id),
                "callsign":  user.callsign,
            }

        # Eventos Stripe no procesados — confirmar recepción (Stripe reintenta en 3xx/5xx)
        return {"received": True, "processed": False, "type": event_type}

    # ── Rama genérica — HMAC-SHA256 para PayPal / Hotmart / otros ────────────
    if not x_webhook_signature:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Falta la firma del webhook (X-Webhook-Signature o Stripe-Signature).",
        )

    if not _verify_hmac(settings.PAYMENT_WEBHOOK_SECRET, body, x_webhook_signature):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Firma del webhook inválida.",
        )

    payload: dict[str, Any] = json.loads(body)

    event_type = (
        payload.get("type")
        or payload.get("event")
        or payload.get("event_type")
        or ""
    ).lower()

    SUCCESS_EVENTS = {
        "payment_intent.succeeded",
        "charge.succeeded",
        "checkout.session.completed",
        "payment.approved",
        "purchase.complete",
        "payment.succeeded",
    }

    if event_type not in SUCCESS_EVENTS:
        return {"received": True, "processed": False, "reason": f"event_type '{event_type}' ignorado"}

    email = _extract_email(payload)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No se pudo extraer el email del comprador del payload.",
        )

    payment_id = (
        payload.get("id")
        or payload.get("data", {}).get("object", {}).get("id")
        or payload.get("resource", {}).get("id")
        or str(uuid.uuid4())
    )

    user = await _activate_user_by_email(db, email, payment_id)
    asyncio.create_task(fire_sale_alert(email))

    return {
        "received":    True,
        "processed":   True,
        "user_id":     str(user.id),
        "callsign":    user.callsign,
        "is_licensed": user.is_licensed,
        "payment_id":  payment_id,
    }


# ─── Ruta 3: Verificación manual / admin ─────────────────────────────────────

class ManualVerifyRequest(BaseModel):
    email:      str
    payment_id: str = "manual-activation"

    @field_validator("email")
    @classmethod
    def email_not_empty(cls, v: str) -> str:
        v = v.strip().lower()
        if "@" not in v or "." not in v.split("@")[-1]:
            raise ValueError("email inválido")
        return v


@router.post(
    "/verify",
    status_code=status.HTTP_200_OK,
    summary="Activación manual de licencia (solo admin)",
    description=(
        "Activa is_licensed=True para un usuario por su email. "
        "Requiere el header `X-Admin-Key` con el valor de `SECRET_KEY`."
    ),
)
async def manual_verify(
    payload:     ManualVerifyRequest,
    db:          AsyncSession = Depends(get_db),
    x_admin_key: str          = Header(..., alias="X-Admin-Key"),
) -> dict:
    if not hmac.compare_digest(x_admin_key, settings.ADMIN_API_KEY):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Clave de administrador inválida.",
        )

    user = await _activate_user_by_email(db, payload.email, payload.payment_id)
    asyncio.create_task(fire_sale_alert(payload.email))

    return {
        "activated":   True,
        "user_id":     str(user.id),
        "callsign":    user.callsign,
        "email":       user.email,
        "is_licensed": user.is_licensed,
        "payment_id":  user.payment_id,
    }
