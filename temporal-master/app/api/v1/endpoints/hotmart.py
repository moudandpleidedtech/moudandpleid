"""
hotmart.py — Integración Hotmart (Directiva 011-HM)

Rutas:

  POST /api/v1/hotmart/checkout
    Genera la URL de checkout de Hotmart con email del operador pre-cargado.
    Requiere JWT del Operador.
    Body: { "plan": "lifetime" | "monthly" }

  POST /api/v1/hotmart/webhook?hottok={HOTMART_HOTTOK}
    Recibe eventos de Hotmart v2.0.
    Verifica el parámetro hottok contra HOTMART_HOTTOK configurado en Render.
    Eventos procesados:
      • PURCHASE_APPROVED        → activa is_licensed + subscription_status=ACTIVE
      • PURCHASE_COMPLETE        → ídem (evento final de pago único)
      • PURCHASE_REFUNDED        → revoca acceso
      • PURCHASE_CANCELED        → revoca acceso
      • SUBSCRIPTION_CANCELLATION → subscription_status=CANCELLED

Variables de entorno requeridas (Render → Environment):
    HOTMART_HOTTOK              — secreto de verificación (mismo para ambos productos)
    HOTMART_PRODUCT_KEY         — product key del producto Vitalicio (pago único $97)
    HOTMART_LIFETIME_OFFER      — offer code del plan vitalicio (opcional)
    HOTMART_SUBSCRIPTION_KEY    — product key del producto Mensual (suscripción $29)
    HOTMART_MONTHLY_OFFER       — offer code del plan mensual (opcional)
    HOTMART_REDIRECT_URL        — URL de página de agradecimiento post-pago

Cómo configurar los webhooks en Hotmart (hacerlo en AMBOS productos):
    Dashboard → Ferramentas → Webhooks → Adicionar webhook
    URL: https://tu-backend.onrender.com/api/v1/hotmart/webhook
    Hottok: el valor de HOTMART_HOTTOK
    Eventos: PURCHASE_APPROVED, PURCHASE_COMPLETE, PURCHASE_REFUNDED,
             PURCHASE_CANCELED, SUBSCRIPTION_CANCELLATION

Cómo configurar la página de agradecimiento (en AMBOS productos):
    Dashboard → Productos → tu producto → Configuraciones → Página de Agradecimiento
    URL: https://tu-frontend.vercel.app/hub?checkout=success
"""

import asyncio
from urllib.parse import urlencode

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.core.security import get_current_operator
from app.models.pending_activation import PendingActivation
from app.models.user import User
from app.services.alerts import fire_sale_alert
from app.services.email import send_subscription_active

router = APIRouter(prefix="/hotmart", tags=["hotmart"])


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _build_checkout_url(plan: str, email: str) -> str:
    """
    Construye la URL de checkout de Hotmart.
    Hotmart pre-llena el email del comprador para reducir fricción.

    - plan "lifetime"  → usa HOTMART_PRODUCT_KEY      (producto pago único $97)
    - plan "monthly"   → usa HOTMART_SUBSCRIPTION_KEY (producto suscripción $29/mes)
    """
    params: dict[str, str] = {
        "buyerEmail": email,
        "checkoutMode": "2",   # modo checkout moderno de Hotmart
    }

    if plan == "monthly":
        if not settings.HOTMART_SUBSCRIPTION_KEY:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="HOTMART_SUBSCRIPTION_KEY no configurado.",
            )
        product_key = settings.HOTMART_SUBSCRIPTION_KEY
        if settings.HOTMART_MONTHLY_OFFER:
            params["off"] = settings.HOTMART_MONTHLY_OFFER
    else:
        # "lifetime" es el default
        if not settings.HOTMART_PRODUCT_KEY:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="HOTMART_PRODUCT_KEY no configurado.",
            )
        product_key = settings.HOTMART_PRODUCT_KEY
        if settings.HOTMART_LIFETIME_OFFER:
            params["off"] = settings.HOTMART_LIFETIME_OFFER

    return f"https://pay.hotmart.com/{product_key}?{urlencode(params)}"


async def _activate_user_by_email(
    db: AsyncSession,
    email: str,
    transaction_id: str,
    status_value: str = "ACTIVE",
) -> User | None:
    """Busca al operador por email y actualiza su estado de suscripción."""
    result = await db.execute(
        select(User).where(User.email == email.lower().strip())
    )
    user = result.scalar_one_or_none()
    if user is None:
        return None

    user.subscription_status = status_value
    user.is_licensed         = (status_value == "ACTIVE")
    user.payment_id          = transaction_id
    await db.flush()
    return user


# ─── Ruta 1: Generar URL de checkout ─────────────────────────────────────────

class CheckoutRequest(BaseModel):
    plan: str = "lifetime"   # "monthly" | "lifetime"


class CheckoutResponse(BaseModel):
    checkout_url: str


@router.post(
    "/checkout",
    response_model=CheckoutResponse,
    status_code=status.HTTP_200_OK,
    summary="Genera URL de checkout de Hotmart con email pre-cargado",
)
async def create_hotmart_checkout(
    body:     CheckoutRequest,
    operator: User = Depends(get_current_operator),
) -> CheckoutResponse:
    url = _build_checkout_url(plan=body.plan, email=operator.email)
    return CheckoutResponse(checkout_url=url)


# ─── Ruta 2: Webhook de Hotmart ───────────────────────────────────────────────

# Eventos que activan la licencia
_ACTIVATE_EVENTS = {"PURCHASE_APPROVED", "PURCHASE_COMPLETE"}

# Eventos que revocan el acceso
_REVOKE_EVENTS   = {"PURCHASE_REFUNDED", "PURCHASE_CANCELED", "SUBSCRIPTION_CANCELLATION"}


@router.post(
    "/webhook",
    status_code=status.HTTP_200_OK,
    summary="Webhook de Hotmart — activa licencias tras pago exitoso",
)
async def hotmart_webhook(
    request: Request,
    db:      AsyncSession = Depends(get_db),
    hottok:  str | None   = Query(None),
) -> dict:
    # ── Verificación de hottok ────────────────────────────────────────────────
    if not settings.HOTMART_HOTTOK:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="HOTMART_HOTTOK no configurado.",
        )

    if hottok != settings.HOTMART_HOTTOK:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Hottok inválido — evento rechazado.",
        )

    # ── Parseo del payload ────────────────────────────────────────────────────
    try:
        payload: dict = await request.json()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Payload no es JSON válido.",
        )

    event = payload.get("event", "").upper()
    data  = payload.get("data", {})

    # Email del comprador — campo principal en Hotmart v2
    buyer       = data.get("buyer", {})
    email: str  = (buyer.get("email") or "").lower().strip()

    # ID de transacción para trazabilidad
    purchase       = data.get("purchase", {})
    transaction_id = purchase.get("transaction") or payload.get("id") or "hotmart-unknown"

    if not email:
        # Hotmart a veces envía eventos de prueba sin email real
        return {"received": True, "processed": False, "reason": "email ausente en payload"}

    # ── Activar licencia ──────────────────────────────────────────────────────
    if event in _ACTIVATE_EVENTS:
        user = await _activate_user_by_email(db, email, transaction_id, "ACTIVE")

        if user is None:
            # El comprador pagó antes de crear su cuenta en DAKI.
            # Guardamos la activación pendiente: cuando se registre con este email,
            # auth.py la detecta y activa la licencia automáticamente.
            pending = PendingActivation(
                email=email,
                transaction_id=transaction_id,
                event=event,
            )
            db.add(pending)
            await db.flush()
            return {
                "received":    True,
                "processed":   False,
                "reason":      f"operador '{email}' no registrado aún — activación guardada para auto-aplicar al registro",
                "event":       event,
                "pending_id":  str(pending.id),
            }

        asyncio.create_task(fire_sale_alert(user.email))
        asyncio.create_task(send_subscription_active(user.email, user.callsign))

        return {
            "received":  True,
            "processed": True,
            "event":     event,
            "user_id":   str(user.id),
            "callsign":  user.callsign,
        }

    # ── Revocar acceso ────────────────────────────────────────────────────────
    if event in _REVOKE_EVENTS:
        status_map = {
            "PURCHASE_REFUNDED":        "REFUNDED",
            "PURCHASE_CANCELED":        "CANCELLED",
            "SUBSCRIPTION_CANCELLATION": "CANCELLED",
        }
        new_status = status_map.get(event, "CANCELLED")
        user = await _activate_user_by_email(db, email, transaction_id, new_status)

        if user is None:
            return {"received": True, "processed": False, "reason": "operador no encontrado", "event": event}

        return {
            "received":  True,
            "processed": True,
            "event":     event,
            "status":    new_status,
            "user_id":   str(user.id),
        }

    # ── Evento no procesado ───────────────────────────────────────────────────
    return {"received": True, "processed": False, "event": event}
