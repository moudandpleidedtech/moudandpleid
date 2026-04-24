"""
tests/test_access_control.py
=============================
Tests de la compuerta de acceso freemium (app/core/access.py).

Cubre check_freemium_access con todos los estados posibles:
  - Challenge gratuito → siempre pasa
  - Challenge de pago + sin user_id → 402
  - Challenge de pago + usuario sin licencia → 402 LICENSE_REQUIRED
  - Challenge de pago + trial activo → pasa
  - Challenge de pago + trial expirado → 402 TRIAL_EXPIRED
  - Challenge de pago + subscription_status=ACTIVE → pasa
  - Challenge de pago + is_licensed=True (flag legacy) → pasa
  - Challenge de pago + rol FOUNDER → bypassa (God Mode)
  - Challenge inexistente → 404

Ejecutar:
    cd temporal-master
    pytest tests/test_access_control.py -v
"""

import uuid
from datetime import datetime, timedelta, timezone
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from fastapi import HTTPException

from tests.conftest import needs_db

pytestmark = [pytest.mark.integration, needs_db]
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.access import check_freemium_access
from app.core.config import settings
from app.models.challenge import Challenge, DifficultyTier
from app.models.user import User


# ─── Infraestructura ──────────────────────────────────────────────────────────

@pytest_asyncio.fixture(scope="session")
async def engine():
    e = create_async_engine(settings.DATABASE_URL, echo=False, pool_pre_ping=True)
    yield e
    await e.dispose()


@pytest_asyncio.fixture(scope="session")
def factory(engine):
    return async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


@pytest_asyncio.fixture
async def db(factory):
    async with factory() as s:
        yield s
        await s.rollback()


# ─── Helpers de fixtures ──────────────────────────────────────────────────────

async def _make_challenge(factory, is_free: bool) -> Challenge:
    ch = Challenge(
        id=uuid.uuid4(),
        title=f"Access Test {'Free' if is_free else 'Paid'}",
        description="test",
        difficulty_tier=DifficultyTier.BEGINNER,
        base_xp_reward=50,
        initial_code="print(1)",
        expected_output="1",
        test_inputs_json="[]",
        is_free=is_free,
        sector_id=None,
        level_order=None,
        is_project=False,
        concepts_taught_json="[]",
        hints_json="[]",
        challenge_type="python",
        difficulty="easy",
        strict_match=False,
    )
    async with factory() as s:
        s.add(ch)
        await s.commit()
    return ch


async def _make_user(factory, **kwargs) -> User:
    uid = uuid.uuid4()
    defaults = dict(
        id=uid,
        email=f"access_{uid.hex[:8]}@test.local",
        password_hash="hash",
        callsign=f"AC{uid.hex[:8]}",
        is_licensed=False,
        subscription_status="INACTIVE",
        current_level=1,
        total_xp=0,
    )
    defaults.update(kwargs)
    user = User(**defaults)
    async with factory() as s:
        s.add(user)
        await s.commit()
    return user


async def _cleanup(factory, *objects):
    ids = [o.id for o in objects]
    async with factory() as s:
        for obj in objects:
            if isinstance(obj, User):
                await s.execute(delete(User).where(User.id == obj.id))
            elif isinstance(obj, Challenge):
                await s.execute(delete(Challenge).where(Challenge.id == obj.id))
        await s.commit()


# ─── Tests ────────────────────────────────────────────────────────────────────

class TestChallengeGratuito:

    @pytest.mark.asyncio
    async def test_free_challenge_sin_user_id_pasa(self, factory, db):
        ch = await _make_challenge(factory, is_free=True)
        result = await check_freemium_access(db, ch.id, user_id=None)
        assert result is None  # None = acceso libre, sin cargar usuario
        await _cleanup(factory, ch)

    @pytest.mark.asyncio
    async def test_free_challenge_con_usuario_sin_licencia_pasa(self, factory, db):
        ch = await _make_challenge(factory, is_free=True)
        user = await _make_user(factory, is_licensed=False)
        result = await check_freemium_access(db, ch.id, user_id=user.id)
        assert result is None
        await _cleanup(factory, ch, user)


class TestChallengeDePageo:

    @pytest.mark.asyncio
    async def test_pago_sin_user_id_retorna_402(self, factory, db):
        ch = await _make_challenge(factory, is_free=False)
        with pytest.raises(HTTPException) as exc_info:
            await check_freemium_access(db, ch.id, user_id=None)
        assert exc_info.value.status_code == 402
        await _cleanup(factory, ch)

    @pytest.mark.asyncio
    async def test_pago_usuario_inactivo_retorna_402(self, factory, db):
        ch = await _make_challenge(factory, is_free=False)
        user = await _make_user(factory, is_licensed=False, subscription_status="INACTIVE")
        with pytest.raises(HTTPException) as exc_info:
            await check_freemium_access(db, ch.id, user_id=user.id)
        assert exc_info.value.status_code == 402
        assert exc_info.value.detail["code"] == "LICENSE_REQUIRED"
        await _cleanup(factory, ch, user)

    @pytest.mark.asyncio
    async def test_pago_subscription_active_pasa(self, factory, db):
        ch = await _make_challenge(factory, is_free=False)
        user = await _make_user(factory, subscription_status="ACTIVE")
        result = await check_freemium_access(db, ch.id, user_id=user.id)
        assert isinstance(result, User)
        await _cleanup(factory, ch, user)

    @pytest.mark.asyncio
    async def test_pago_is_licensed_legacy_pasa(self, factory, db):
        """El flag booleano is_licensed=True mantiene compatibilidad con cuentas antiguas."""
        ch = await _make_challenge(factory, is_free=False)
        user = await _make_user(factory, is_licensed=True, subscription_status="INACTIVE")
        result = await check_freemium_access(db, ch.id, user_id=user.id)
        assert isinstance(result, User)
        await _cleanup(factory, ch, user)

    @pytest.mark.asyncio
    async def test_pago_trial_activo_pasa(self, factory, db):
        ch = await _make_challenge(factory, is_free=False)
        user = await _make_user(
            factory,
            subscription_status="TRIAL",
            trial_end_date=datetime.now(timezone.utc) + timedelta(days=7),
        )
        result = await check_freemium_access(db, ch.id, user_id=user.id)
        assert isinstance(result, User)
        await _cleanup(factory, ch, user)

    @pytest.mark.asyncio
    async def test_pago_trial_expirado_retorna_402(self, factory, db):
        ch = await _make_challenge(factory, is_free=False)
        user = await _make_user(
            factory,
            subscription_status="TRIAL",
            trial_end_date=datetime.now(timezone.utc) - timedelta(days=1),
        )
        with pytest.raises(HTTPException) as exc_info:
            await check_freemium_access(db, ch.id, user_id=user.id)
        assert exc_info.value.status_code == 402
        assert exc_info.value.detail["code"] == "TRIAL_EXPIRED"
        await _cleanup(factory, ch, user)

    @pytest.mark.asyncio
    async def test_pago_founder_bypassa_paywall(self, factory, db):
        """Rol FOUNDER bypassa todas las compuertas (God Mode)."""
        ch = await _make_challenge(factory, is_free=False)
        user = await _make_user(
            factory,
            role="FOUNDER",
            is_licensed=False,
            subscription_status="INACTIVE",
        )
        result = await check_freemium_access(db, ch.id, user_id=user.id)
        assert isinstance(result, User)
        assert result.role == "FOUNDER"
        await _cleanup(factory, ch, user)


class TestEdgeCases:

    @pytest.mark.asyncio
    async def test_challenge_inexistente_retorna_404(self, factory, db):
        with pytest.raises(HTTPException) as exc_info:
            await check_freemium_access(db, uuid.uuid4(), user_id=None)
        assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_usuario_inexistente_retorna_404(self, factory, db):
        ch = await _make_challenge(factory, is_free=False)
        with pytest.raises(HTTPException) as exc_info:
            await check_freemium_access(db, ch.id, user_id=uuid.uuid4())
        assert exc_info.value.status_code == 404
        await _cleanup(factory, ch)
