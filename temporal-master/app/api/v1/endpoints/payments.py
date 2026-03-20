"""
payments.py — Validador de Transacciones (Prompt 39)

Dos rutas:

  POST /api/v1/payments/webhook
    Recibe el evento de la pasarela (Stripe, PayPal, Hotmart, etc.).
    Valida la firma HMAC-SHA256 antes de tocar la BD.
    Activa is_paid=True y guarda payment_id en el usuario.

  POST /api/v1/payments/verify
    Ruta manual/admin para activar un usuario por email sin webhook.
    Protegida por API key interna (header X-Admin-Key).
    Útil para activaciones manuales, demos, y pruebas.

Variables de entorno requeridas:
    PAYMENT_WEBHOOK_SECRET   — secreto HMAC compartido con la pasarela
    SECRET_KEY               — también usado como admin key de fallback

Compatibilidad de pasarelas (campo email en payload):
    Stripe:  event.data.object.customer_email  o  billing_details.email
    PayPal:  resource.payer.email_address
    Hotmart: data.buyer.email
    Genérico: email  (campo directo en el JSON)
"""

import hashlib
import hmac
import uuid
from typing import Any

from fastapi import APIRouter, Body, Depends, Header, HTTPException, Request, status
from pydantic import BaseModel, field_validator
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User

router = APIRouter(prefix="/payments", tags=["payments"])


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _verify_hmac(secret: str, payload: bytes, signature: str) -> bool:
    """
    Verifica la firma HMAC-SHA256 enviada por la pasarela.
    Compatible con:
      - Stripe:  header Stripe-Signature  (t=...,v1=<hex>)
      - Genérico: header X-Webhook-Signature  (<hex>)
    """
    expected = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()

    # Stripe envía "t=timestamp,v1=firma" — extraemos solo la firma
    sig = signature.split("v1=")[-1] if "v1=" in signature else signature

    return hmac.compare_digest(expected, sig)


async def _activate_user(db: AsyncSession, email: str, payment_id: str) -> User:
    """Busca al usuario por email y activa su licencia."""
    result = await db.execute(
        select(User).where(User.email == email.lower().strip())
    )
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe ningún operador con el email '{email}'.",
        )

    user.is_paid   = True
    user.payment_id = payment_id
    await db.flush()
    return user


def _extract_email(payload: dict[str, Any]) -> str | None:
    """
    Intenta extraer el email del comprador de payloads de distintas pasarelas.
    Devuelve None si no encuentra ninguno.
    """
    # Campo directo (pasarela genérica / manual)
    if "email" in payload:
        return payload["email"]

    # Stripe: event.data.object
    obj = payload.get("data", {}).get("object", {})
    if obj.get("customer_email"):
        return obj["customer_email"]
    if obj.get("billing_details", {}).get("email"):
        return obj["billing_details"]["email"]
    if obj.get("receipt_email"):
        return obj["receipt_email"]

    # PayPal: resource.payer.email_address
    payer = payload.get("resource", {}).get("payer", {})
    if payer.get("email_address"):
        return payer["email_address"]

    # Hotmart: data.buyer.email
    buyer = payload.get("data", {}).get("buyer", {})
    if buyer.get("email"):
        return buyer["email"]

    return None


# ─── Ruta 1: Webhook de pasarela de pagos ─────────────────────────────────────

@router.post(
    "/webhook",
    status_code=status.HTTP_200_OK,
    summary="Webhook de pasarela — activa licencia tras pago exitoso",
    description=(
        "Recibe el evento POST de la pasarela. "
        "Valida firma HMAC-SHA256 (header `X-Webhook-Signature` o `Stripe-Signature`). "
        "Solo procesa eventos de tipo `payment.succeeded` / `charge.succeeded` / `payment_intent.succeeded`."
    ),
)
async def payment_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db),
    x_webhook_signature: str | None = Header(None, alias="X-Webhook-Signature"),
    stripe_signature:    str | None = Header(None, alias="Stripe-Signature"),
) -> dict:
    body = await request.body()
    payload = await request.json()

    # ── Validación de firma ───────────────────────────────────────────────────
    signature = x_webhook_signature or stripe_signature

    if not signature:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Falta la firma del webhook (X-Webhook-Signature o Stripe-Signature).",
        )

    if not _verify_hmac(settings.PAYMENT_WEBHOOK_SECRET, body, signature):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Firma del webhook inválida.",
        )

    # ── Filtro de eventos ─────────────────────────────────────────────────────
    event_type = (
        payload.get("type")               # Stripe
        or payload.get("event")           # Hotmart
        or payload.get("event_type")      # PayPal
        or ""
    ).lower()

    SUCCESS_EVENTS = {
        "payment_intent.succeeded",
        "charge.succeeded",
        "checkout.session.completed",
        "payment.approved",             # PayPal
        "purchase.complete",            # Hotmart
        "payment.succeeded",            # genérico
    }

    if event_type not in SUCCESS_EVENTS:
        # Ignorar silenciosamente eventos que no son de pago exitoso
        return {"received": True, "processed": False, "reason": f"event_type '{event_type}' ignorado"}

    # ── Extracción del email ──────────────────────────────────────────────────
    email = _extract_email(payload)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No se pudo extraer el email del comprador del payload.",
        )

    # payment_id: ID único del cargo para auditoría
    payment_id = (
        payload.get("id")                              # Stripe event id
        or payload.get("data", {}).get("object", {}).get("id")
        or payload.get("resource", {}).get("id")       # PayPal
        or str(uuid.uuid4())                           # fallback
    )

    user = await _activate_user(db, email, payment_id)

    return {
        "received":   True,
        "processed":  True,
        "user_id":    str(user.id),
        "username":   user.username,
        "is_paid":    user.is_paid,
        "payment_id": payment_id,
    }


# ─── Ruta 2: Verificación manual / admin ─────────────────────────────────────

class ManualVerifyRequest(BaseModel):
    email: str
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
        "Activa is_paid=True para un usuario por su email. "
        "Requiere el header `X-Admin-Key` con el valor de `SECRET_KEY`."
    ),
)
async def manual_verify(
    payload: ManualVerifyRequest,
    db: AsyncSession = Depends(get_db),
    x_admin_key: str = Header(..., alias="X-Admin-Key"),
) -> dict:
    if not hmac.compare_digest(x_admin_key, settings.SECRET_KEY):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Clave de administrador inválida.",
        )

    user = await _activate_user(db, payload.email, payload.payment_id)

    return {
        "activated": True,
        "user_id":   str(user.id),
        "username":  user.username,
        "email":     user.email,
        "is_paid":   user.is_paid,
        "payment_id": user.payment_id,
    }
