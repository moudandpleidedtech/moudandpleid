"""
tests/test_hotmart_webhook.py
==============================
Tests del webhook de Hotmart (POST /api/v1/hotmart/webhook).

Cubre el ciclo de vida completo de la licencia:
  - PURCHASE_APPROVED → activa is_licensed + subscription_status=ACTIVE
  - PURCHASE_COMPLETE → ídem
  - PURCHASE_REFUNDED → revoca acceso (subscription_status=REFUNDED)
  - PURCHASE_CANCELED → revoca acceso (subscription_status=CANCELLED)
  - Hottok inválido → 401 (rechazado)
  - Email sin cuenta registrada → PendingActivation guardada
  - Auto-activación al registrarse con email que tiene PendingActivation

Ejecutar:
    cd temporal-master
    pytest tests/test_hotmart_webhook.py -v
"""

import uuid
from typing import AsyncGenerator
from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from tests.conftest import needs_db

pytestmark = [pytest.mark.integration, needs_db]
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.config import settings
from app.core.database import get_db
from app.models.pending_activation import PendingActivation
from app.models.user import User
from main import app

# ─── Infraestructura ──────────────────────────────────────────────────────────

TEST_HOTTOK = "test-hottok-webhook-abc123"


@pytest_asyncio.fixture(scope="session")
async def test_engine():
    e = create_async_engine(settings.DATABASE_URL, echo=False, pool_pre_ping=True)
    yield e
    await e.dispose()


@pytest_asyncio.fixture(scope="session")
def session_factory(test_engine):
    return async_sessionmaker(test_engine, expire_on_commit=False, class_=AsyncSession)


@pytest_asyncio.fixture
async def client(session_factory):
    async def _db() -> AsyncGenerator[AsyncSession, None]:
        async with session_factory() as s:
            try:
                yield s
                await s.commit()
            except Exception:
                await s.rollback()
                raise

    app.dependency_overrides[get_db] = _db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def registered_user(session_factory) -> AsyncGenerator[User, None]:
    uid = uuid.uuid4()
    user = User(
        id=uid,
        email=f"hotmart_{uid.hex[:8]}@example.com",
        password_hash="hash",
        callsign=f"HM{uid.hex[:8]}",
        is_licensed=False,
        subscription_status="INACTIVE",
        current_level=1,
        total_xp=0,
    )
    async with session_factory() as s:
        s.add(user)
        await s.commit()
    yield user
    async with session_factory() as s:
        await s.execute(delete(User).where(User.id == uid))
        await s.commit()


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _payload(event: str, email: str, transaction: str = "TXN-TEST-001") -> dict:
    return {
        "event": event,
        "data": {
            "buyer": {"email": email},
            "purchase": {"transaction": transaction},
        },
    }


async def _get_user(session_factory, user_id: uuid.UUID) -> User | None:
    async with session_factory() as s:
        result = await s.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()


# ─── Tests ────────────────────────────────────────────────────────────────────

class TestHottokValidacion:

    @pytest.mark.asyncio
    async def test_hottok_invalido_retorna_401(self, client, registered_user):
        with patch.object(settings, "HOTMART_HOTTOK", TEST_HOTTOK):
            r = await client.post(
                "/api/v1/hotmart/webhook?hottok=WRONG-TOKEN",
                json=_payload("PURCHASE_APPROVED", registered_user.email),
            )
        assert r.status_code == 401

    @pytest.mark.asyncio
    async def test_hottok_valido_retorna_200(self, client, registered_user):
        with patch.object(settings, "HOTMART_HOTTOK", TEST_HOTTOK), \
             patch("app.api.v1.endpoints.hotmart.fire_sale_alert"), \
             patch("app.api.v1.endpoints.hotmart.send_subscription_active"):
            r = await client.post(
                f"/api/v1/hotmart/webhook?hottok={TEST_HOTTOK}",
                json=_payload("PURCHASE_APPROVED", registered_user.email),
            )
        assert r.status_code == 200


class TestActivacionDeLicencia:

    @pytest.mark.asyncio
    async def test_purchase_approved_activa_licencia(
        self, client, session_factory, registered_user
    ):
        with patch.object(settings, "HOTMART_HOTTOK", TEST_HOTTOK), \
             patch("app.api.v1.endpoints.hotmart.fire_sale_alert"), \
             patch("app.api.v1.endpoints.hotmart.send_subscription_active"):
            r = await client.post(
                f"/api/v1/hotmart/webhook?hottok={TEST_HOTTOK}",
                json=_payload("PURCHASE_APPROVED", registered_user.email),
            )
        assert r.status_code == 200
        body = r.json()
        assert body["processed"] is True

        user = await _get_user(session_factory, registered_user.id)
        assert user.is_licensed is True
        assert user.subscription_status == "ACTIVE"

    @pytest.mark.asyncio
    async def test_purchase_complete_activa_licencia(
        self, client, session_factory, registered_user
    ):
        with patch.object(settings, "HOTMART_HOTTOK", TEST_HOTTOK), \
             patch("app.api.v1.endpoints.hotmart.fire_sale_alert"), \
             patch("app.api.v1.endpoints.hotmart.send_subscription_active"):
            r = await client.post(
                f"/api/v1/hotmart/webhook?hottok={TEST_HOTTOK}",
                json=_payload("PURCHASE_COMPLETE", registered_user.email),
            )
        assert r.status_code == 200
        user = await _get_user(session_factory, registered_user.id)
        assert user.is_licensed is True


class TestRevocacionDeLicencia:

    @pytest_asyncio.fixture
    async def licensed_user(self, session_factory) -> AsyncGenerator[User, None]:
        uid = uuid.uuid4()
        user = User(
            id=uid,
            email=f"revoke_{uid.hex[:8]}@example.com",
            password_hash="hash",
            callsign=f"RV{uid.hex[:8]}",
            is_licensed=True,
            subscription_status="ACTIVE",
            current_level=1,
            total_xp=0,
        )
        async with session_factory() as s:
            s.add(user)
            await s.commit()
        yield user
        async with session_factory() as s:
            await s.execute(delete(User).where(User.id == uid))
            await s.commit()

    @pytest.mark.asyncio
    async def test_refund_revoca_acceso(
        self, client, session_factory, licensed_user
    ):
        with patch.object(settings, "HOTMART_HOTTOK", TEST_HOTTOK):
            r = await client.post(
                f"/api/v1/hotmart/webhook?hottok={TEST_HOTTOK}",
                json=_payload("PURCHASE_REFUNDED", licensed_user.email),
            )
        assert r.status_code == 200
        assert r.json()["processed"] is True

        user = await _get_user(session_factory, licensed_user.id)
        assert user.is_licensed is False
        assert user.subscription_status == "REFUNDED"

    @pytest.mark.asyncio
    async def test_cancelacion_revoca_acceso(
        self, client, session_factory, licensed_user
    ):
        with patch.object(settings, "HOTMART_HOTTOK", TEST_HOTTOK):
            r = await client.post(
                f"/api/v1/hotmart/webhook?hottok={TEST_HOTTOK}",
                json=_payload("PURCHASE_CANCELED", licensed_user.email),
            )
        assert r.status_code == 200
        user = await _get_user(session_factory, licensed_user.id)
        assert user.is_licensed is False
        assert user.subscription_status == "CANCELLED"


class TestActivacionPendiente:

    @pytest.mark.asyncio
    async def test_pago_antes_de_registro_crea_pending_activation(
        self, client, session_factory
    ):
        """Comprador paga antes de crear cuenta → PendingActivation guardada."""
        email = f"pending_{uuid.uuid4().hex[:8]}@example.com"
        with patch.object(settings, "HOTMART_HOTTOK", TEST_HOTTOK):
            r = await client.post(
                f"/api/v1/hotmart/webhook?hottok={TEST_HOTTOK}",
                json=_payload("PURCHASE_APPROVED", email, "TXN-PENDING-001"),
            )
        assert r.status_code == 200
        body = r.json()
        assert body["processed"] is False
        assert "pending_id" in body

        # Verificar que PendingActivation existe en DB
        async with session_factory() as s:
            result = await s.execute(
                select(PendingActivation).where(PendingActivation.email == email)
            )
            pending = result.scalar_one_or_none()
        assert pending is not None
        assert pending.transaction_id == "TXN-PENDING-001"

        # Cleanup
        async with session_factory() as s:
            await s.execute(
                delete(PendingActivation).where(PendingActivation.email == email)
            )
            await s.commit()

    @pytest.mark.asyncio
    async def test_evento_desconocido_retorna_200_sin_procesar(
        self, client, registered_user
    ):
        with patch.object(settings, "HOTMART_HOTTOK", TEST_HOTTOK):
            r = await client.post(
                f"/api/v1/hotmart/webhook?hottok={TEST_HOTTOK}",
                json=_payload("UNKNOWN_EVENT_XYZ", registered_user.email),
            )
        assert r.status_code == 200
        body = r.json()
        assert body["received"] is True
        assert body["processed"] is False

    @pytest.mark.asyncio
    async def test_payload_sin_email_retorna_200_sin_procesar(self, client):
        with patch.object(settings, "HOTMART_HOTTOK", TEST_HOTTOK):
            r = await client.post(
                f"/api/v1/hotmart/webhook?hottok={TEST_HOTTOK}",
                json={"event": "PURCHASE_APPROVED", "data": {}},
            )
        assert r.status_code == 200
        assert r.json()["processed"] is False
