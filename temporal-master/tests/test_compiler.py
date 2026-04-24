"""
tests/test_compiler.py
======================
Tests del endpoint POST /api/v1/execute (compiler.py).

Cubre:
  - Paywall: challenge gratuito pasa, challenge de pago bloquea con 402
  - Paywall: usuario con is_licensed=True accede a challenges de pago
  - user_id mismatch → 403
  - Challenge inexistente → 404
  - Sandbox caído → 200 con mensaje neutral, attempts=0 (no penaliza)
  - Código correcto → output_matched=True
  - Mismatch sin error → failed_case poblado, output_matched=False
  - Error de sintaxis → error_info poblado
  - DAKI hints por tolerancia: se activan en intentos 3, 6, 10
  - Regresión: paywall faltaba en /execute antes del fix (PR paywall+redeem)

Ejecutar:
    cd temporal-master
    pytest tests/test_compiler.py -v
"""

import uuid
from typing import AsyncGenerator
from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from tests.conftest import needs_db

pytestmark = [pytest.mark.integration, needs_db]
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.config import settings
from app.core.database import get_db
from app.core.security import get_current_operator
from app.models.challenge import Challenge, DifficultyTier
from app.models.user import User
from app.models.user_metrics import UserMetric
from main import app


# ─── Infraestructura ──────────────────────────────────────────────────────────

@pytest_asyncio.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(settings.DATABASE_URL, echo=False, pool_pre_ping=True)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="session")
def session_factory(test_engine):
    return async_sessionmaker(test_engine, expire_on_commit=False, class_=AsyncSession)


@pytest_asyncio.fixture
async def db_session(session_factory):
    async with session_factory() as s:
        yield s
        await s.rollback()


# ─── Fixtures de datos ────────────────────────────────────────────────────────

@pytest_asyncio.fixture
async def unlicensed_user(session_factory) -> AsyncGenerator[User, None]:
    uid = uuid.uuid4()
    user = User(
        id=uid,
        email=f"compiler_test_{uid.hex[:8]}@test.local",
        password_hash="test_hash",
        callsign=f"CompTest{uid.hex[:6]}",
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
        await s.execute(delete(UserMetric).where(UserMetric.user_id == uid))
        await s.execute(delete(User).where(User.id == uid))
        await s.commit()


@pytest_asyncio.fixture
async def licensed_user(session_factory) -> AsyncGenerator[User, None]:
    uid = uuid.uuid4()
    user = User(
        id=uid,
        email=f"licensed_{uid.hex[:8]}@test.local",
        password_hash="test_hash",
        callsign=f"Licensed{uid.hex[:6]}",
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
        await s.execute(delete(UserMetric).where(UserMetric.user_id == uid))
        await s.execute(delete(User).where(User.id == uid))
        await s.commit()


@pytest_asyncio.fixture
async def free_challenge(session_factory) -> AsyncGenerator[Challenge, None]:
    ch = Challenge(
        id=uuid.uuid4(),
        title="Compiler Test — Free",
        description="Imprimí 42.",
        difficulty_tier=DifficultyTier.BEGINNER,
        base_xp_reward=50,
        initial_code="print(42)",
        expected_output="42",
        test_inputs_json="[]",
        is_free=True,
        sector_id=None,
        level_order=None,
        is_project=False,
        concepts_taught_json='["variables"]',
        hints_json='["Pista 1", "Pista 2", "Pista 3"]',
        challenge_type="python",
        difficulty="easy",
        strict_match=False,
    )
    async with session_factory() as s:
        s.add(ch)
        await s.commit()
    yield ch
    async with session_factory() as s:
        await s.execute(delete(UserMetric).where(UserMetric.challenge_id == ch.id))
        await s.execute(delete(Challenge).where(Challenge.id == ch.id))
        await s.commit()


@pytest_asyncio.fixture
async def paid_challenge(session_factory) -> AsyncGenerator[Challenge, None]:
    ch = Challenge(
        id=uuid.uuid4(),
        title="Compiler Test — Paid",
        description="Challenge de pago.",
        difficulty_tier=DifficultyTier.INTERMEDIATE,
        base_xp_reward=120,
        initial_code="print('paid')",
        expected_output="paid",
        test_inputs_json="[]",
        is_free=False,
        sector_id=None,
        level_order=None,
        is_project=False,
        concepts_taught_json="[]",
        hints_json="[]",
        challenge_type="python",
        difficulty="medium",
        strict_match=False,
    )
    async with session_factory() as s:
        s.add(ch)
        await s.commit()
    yield ch
    async with session_factory() as s:
        await s.execute(delete(UserMetric).where(UserMetric.challenge_id == ch.id))
        await s.execute(delete(Challenge).where(Challenge.id == ch.id))
        await s.commit()


# ─── Cliente con overrides ─────────────────────────────────────────────────────

def _make_client(session_factory, operator: User):
    """Crea un AsyncClient con get_db y get_current_operator sobrescritos."""
    async def _db() -> AsyncGenerator[AsyncSession, None]:
        async with session_factory() as s:
            try:
                yield s
                await s.commit()
            except Exception:
                await s.rollback()
                raise

    async def _operator():
        return operator

    app.dependency_overrides[get_db] = _db
    app.dependency_overrides[get_current_operator] = _operator
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://test")


def _exec_payload(user: User, challenge: Challenge, source_code: str = "print(42)") -> dict:
    return {
        "user_id": str(user.id),
        "challenge_id": str(challenge.id),
        "source_code": source_code,
        "test_inputs": [],
        "hints_used": 0,
        "time_spent_ms": 100,
    }


# ─── Mocks de servicios externos ─────────────────────────────────────────────

def _mock_exec(stdout: str = "42", success: bool = True, stderr: str = "") -> dict:
    return {
        "stdout": stdout,
        "stderr": stderr,
        "execution_time_ms": 10.0,
        "success": success,
        "sandbox_unavailable": False,
        "error_info": None,
    }


DAKI_MSG_PATCH = "app.api.v1.endpoints.compiler.get_execute_feedback"
EXEC_PATCH     = "app.api.v1.endpoints.compiler.execute_python_code"
ACHIEVE_PATCH  = "app.api.v1.endpoints.compiler.check_and_grant"


# ─── Tests ────────────────────────────────────────────────────────────────────

class TestPaywall:

    @pytest.mark.asyncio
    async def test_challenge_gratuito_no_requiere_licencia(
        self, session_factory, unlicensed_user, free_challenge
    ):
        """Usuario sin licencia puede ejecutar challenges is_free=True."""
        async with _make_client(session_factory, unlicensed_user) as c:
            with patch(EXEC_PATCH, return_value=_mock_exec("42")), \
                 patch(DAKI_MSG_PATCH, new_callable=AsyncMock, return_value="ok"), \
                 patch(ACHIEVE_PATCH, new_callable=AsyncMock, return_value=[]):
                r = await c.post("/api/v1/execute",
                                 json=_exec_payload(unlicensed_user, free_challenge))
        assert r.status_code == 200
        app.dependency_overrides.clear()

    @pytest.mark.asyncio
    async def test_challenge_pago_bloquea_sin_licencia(
        self, session_factory, unlicensed_user, paid_challenge
    ):
        """Usuario sin licencia recibe 402 en challenge is_free=False. Regresión del bug paywall."""
        async with _make_client(session_factory, unlicensed_user) as c:
            r = await c.post("/api/v1/execute",
                             json=_exec_payload(unlicensed_user, paid_challenge))
        assert r.status_code == 402, \
            f"Paywall roto: usuario sin licencia accedió a challenge de pago (HTTP {r.status_code})"
        body = r.json()
        assert body["detail"]["code"] == "LICENSE_REQUIRED"
        app.dependency_overrides.clear()

    @pytest.mark.asyncio
    async def test_challenge_pago_permite_con_licencia(
        self, session_factory, licensed_user, paid_challenge
    ):
        """Usuario con is_licensed=True puede ejecutar challenges de pago."""
        async with _make_client(session_factory, licensed_user) as c:
            with patch(EXEC_PATCH, return_value=_mock_exec("paid")), \
                 patch(DAKI_MSG_PATCH, new_callable=AsyncMock, return_value="ok"), \
                 patch(ACHIEVE_PATCH, new_callable=AsyncMock, return_value=[]):
                r = await c.post("/api/v1/execute",
                                 json=_exec_payload(licensed_user, paid_challenge,
                                                    source_code="print('paid')"))
        assert r.status_code == 200
        app.dependency_overrides.clear()


class TestValidaciones:

    @pytest.mark.asyncio
    async def test_user_id_mismatch_retorna_403(
        self, session_factory, unlicensed_user, free_challenge
    ):
        """El user_id del payload debe coincidir con el JWT del operador."""
        async with _make_client(session_factory, unlicensed_user) as c:
            payload = _exec_payload(unlicensed_user, free_challenge)
            payload["user_id"] = str(uuid.uuid4())  # UUID diferente
            r = await c.post("/api/v1/execute", json=payload)
        assert r.status_code == 403
        app.dependency_overrides.clear()

    @pytest.mark.asyncio
    async def test_challenge_inexistente_retorna_404(
        self, session_factory, unlicensed_user
    ):
        async with _make_client(session_factory, unlicensed_user) as c:
            payload = {
                "user_id": str(unlicensed_user.id),
                "challenge_id": str(uuid.uuid4()),
                "source_code": "print(1)",
                "test_inputs": [], "hints_used": 0, "time_spent_ms": 0,
            }
            r = await c.post("/api/v1/execute", json=payload)
        assert r.status_code == 404
        app.dependency_overrides.clear()


class TestEjecucion:

    @pytest.mark.asyncio
    async def test_codigo_correcto_output_matched_true(
        self, session_factory, unlicensed_user, free_challenge
    ):
        async with _make_client(session_factory, unlicensed_user) as c:
            with patch(EXEC_PATCH, return_value=_mock_exec("42")), \
                 patch(DAKI_MSG_PATCH, new_callable=AsyncMock, return_value="ok"), \
                 patch(ACHIEVE_PATCH, new_callable=AsyncMock, return_value=[]):
                r = await c.post("/api/v1/execute",
                                 json=_exec_payload(unlicensed_user, free_challenge,
                                                    source_code="print(42)"))
        assert r.status_code == 200
        body = r.json()
        assert body["output_matched"] is True
        assert body["gamification"]["is_success"] is True
        assert body["error_info"] is None
        app.dependency_overrides.clear()

    @pytest.mark.asyncio
    async def test_mismatch_sin_error_popula_failed_case(
        self, session_factory, unlicensed_user, free_challenge
    ):
        async with _make_client(session_factory, unlicensed_user) as c:
            with patch(EXEC_PATCH, return_value=_mock_exec("99", success=True)), \
                 patch(DAKI_MSG_PATCH, new_callable=AsyncMock, return_value="ok"), \
                 patch(ACHIEVE_PATCH, new_callable=AsyncMock, return_value=[]):
                r = await c.post("/api/v1/execute",
                                 json=_exec_payload(unlicensed_user, free_challenge,
                                                    source_code="print(99)"))
        assert r.status_code == 200
        body = r.json()
        assert body["output_matched"] is False
        assert body["failed_case"] is not None
        assert body["failed_case"]["got"] == "99"
        assert body["failed_case"]["expected"] == "42"
        app.dependency_overrides.clear()

    @pytest.mark.asyncio
    async def test_error_sintaxis_popula_error_info(
        self, session_factory, unlicensed_user, free_challenge
    ):
        exec_result = {
            "stdout": "",
            "stderr": 'File "tmp.py", line 1\n    print(\n         ^\nSyntaxError: unexpected EOF while parsing',
            "execution_time_ms": 5.0,
            "success": False,
            "sandbox_unavailable": False,
            "error_info": {
                "error_type": "SyntaxError",
                "line": 1,
                "detail": "unexpected EOF while parsing",
            },
        }
        async with _make_client(session_factory, unlicensed_user) as c:
            with patch(EXEC_PATCH, return_value=exec_result), \
                 patch(DAKI_MSG_PATCH, new_callable=AsyncMock, return_value="ok"), \
                 patch(ACHIEVE_PATCH, new_callable=AsyncMock, return_value=[]):
                r = await c.post("/api/v1/execute",
                                 json=_exec_payload(unlicensed_user, free_challenge,
                                                    source_code="print("))
        assert r.status_code == 200
        body = r.json()
        assert body["output_matched"] is False
        assert body["error_info"]["error_type"] == "SyntaxError"
        assert body["failed_case"] is None  # no hay mismatch limpio cuando hay error
        app.dependency_overrides.clear()

    @pytest.mark.asyncio
    async def test_sandbox_caido_retorna_200_neutral(
        self, session_factory, unlicensed_user, free_challenge
    ):
        """Sandbox unavailable → HTTP 200 con mensaje neutral, attempts=0 (no penaliza)."""
        sandbox_down = {
            "stdout": "", "stderr": "",
            "execution_time_ms": 0.0,
            "success": False,
            "sandbox_unavailable": True,
            "error_info": None,
        }
        async with _make_client(session_factory, unlicensed_user) as c:
            with patch(EXEC_PATCH, return_value=sandbox_down):
                r = await c.post("/api/v1/execute",
                                 json=_exec_payload(unlicensed_user, free_challenge))
        assert r.status_code == 200
        body = r.json()
        assert body["gamification"]["attempts"] == 0, \
            "Sandbox caído no debe contar el intento"
        assert "Entorno" in body["daki_message"] or "línea" in body["daki_message"]
        app.dependency_overrides.clear()


class TestDakiHintsPorTolerancia:
    """Los hints se activan en los intentos 3, 6, 10 (thresholds de _HINT_THRESHOLDS)."""

    async def _ejecutar_n_veces(self, client, user, challenge, n: int):
        for _ in range(n):
            with patch(EXEC_PATCH, return_value=_mock_exec("99", success=True)), \
                 patch(DAKI_MSG_PATCH, new_callable=AsyncMock, return_value="ok"), \
                 patch(ACHIEVE_PATCH, new_callable=AsyncMock, return_value=[]):
                await client.post("/api/v1/execute",
                                  json=_exec_payload(user, challenge,
                                                     source_code="print(99)"))

    @pytest.mark.asyncio
    async def test_sin_hints_antes_de_3_intentos(
        self, session_factory, unlicensed_user, free_challenge
    ):
        async with _make_client(session_factory, unlicensed_user) as c:
            await self._ejecutar_n_veces(c, unlicensed_user, free_challenge, 1)
            with patch(EXEC_PATCH, return_value=_mock_exec("99")), \
                 patch(DAKI_MSG_PATCH, new_callable=AsyncMock, return_value="ok"), \
                 patch(ACHIEVE_PATCH, new_callable=AsyncMock, return_value=[]):
                r = await c.post("/api/v1/execute",
                                 json=_exec_payload(unlicensed_user, free_challenge,
                                                    source_code="print(99)"))
        assert r.status_code == 200
        assert r.json()["daki_intervention"] is None
        app.dependency_overrides.clear()

    @pytest.mark.asyncio
    async def test_pista_1_en_intento_3(
        self, session_factory, unlicensed_user, free_challenge
    ):
        async with _make_client(session_factory, unlicensed_user) as c:
            await self._ejecutar_n_veces(c, unlicensed_user, free_challenge, 2)
            with patch(EXEC_PATCH, return_value=_mock_exec("99")), \
                 patch(DAKI_MSG_PATCH, new_callable=AsyncMock, return_value="ok"), \
                 patch(ACHIEVE_PATCH, new_callable=AsyncMock, return_value=[]):
                r = await c.post("/api/v1/execute",
                                 json=_exec_payload(unlicensed_user, free_challenge,
                                                    source_code="print(99)"))
        body = r.json()
        assert body["daki_intervention"] is not None
        hint = body["daki_intervention"]
        assert hint["hint_index"] == 0
        assert hint["hint_number"] == 1
        assert hint["text"] == "Pista 1"
        app.dependency_overrides.clear()
