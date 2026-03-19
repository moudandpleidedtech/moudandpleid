"""
tests/test_api_integration.py
==============================
Suite de Tests de Integración — GlitchAndGold API

Cubre el "viaje del Operador" completo a nivel de red:

  Escenario 1 — Acceso a nivel bloqueado (403 LEVEL_LOCKED)
  Escenario 2 — Flujo de completar nivel → desbloqueo del siguiente
  Escenario 3 — DAKI message en evaluación fallida/exitosa
  Escenario 4 — Pistas de ENIGMA (POST /hint + telemetría)
  Escenario 5 — Evaluación exitosa (output_matched + schema)
  Escenario 6 — Health check y contratos básicos

Decisiones de diseño:
  • `evaluar_incursion` se mockea en la mayoría de tests de integración.
    El sandbox (subprocess/fork) se prueba aisladamente en test_evaluator.py.
    Aquí nos interesa la capa HTTP: routing, validación, DB, schemas.
  • Los challenges de prueba usan sector_id=9999 (fixtures) y sector_id=9998
    (proyecto previo) para respetar las reglas de progresión.
  • Cada fixture crea y limpia sus propios datos — sin side-effects entre tests.

Ejecutar:
    cd temporal-master
    pytest tests/test_api_integration.py -v

    # Incluye test de sandbox real (fork): --timeout 15
    pytest tests/test_api_integration.py -v -m slow --timeout 15
"""

import uuid
from typing import AsyncGenerator
from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.config import settings
from app.core.database import get_db
from app.models.challenge import Challenge, DifficultyTier
from app.models.user import User
from app.models.user_progress import UserProgress
from app.services.evaluation_service import EvaluacionResult
from main import app


# ─────────────────────────────────────────────────────────────────────────────
# IDs reservados para tests (nunca usados por datos de producción)
# ─────────────────────────────────────────────────────────────────────────────

_SECTOR_PREV = 9998   # proyecto "completado" del sector anterior (pre-requisito)
_SECTOR_TEST = 9999   # sector con L1 y L2 que usamos para probar el flujo


# ─────────────────────────────────────────────────────────────────────────────
# Fixtures de infraestructura
# ─────────────────────────────────────────────────────────────────────────────

@pytest_asyncio.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(settings.DATABASE_URL, echo=False, pool_pre_ping=True)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="session")
def session_factory(test_engine):
    return async_sessionmaker(test_engine, expire_on_commit=False, class_=AsyncSession)


@pytest_asyncio.fixture
async def client(session_factory):
    """
    Cliente HTTP en memoria con get_db sobrescrito.
    Cada request del endpoint recibe su propia sesión (igual que producción).
    """
    async def _override_get_db() -> AsyncGenerator[AsyncSession, None]:
        async with session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    app.dependency_overrides[get_db] = _override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.pop(get_db, None)


# ─────────────────────────────────────────────────────────────────────────────
# Fixtures de datos
# ─────────────────────────────────────────────────────────────────────────────

@pytest_asyncio.fixture
async def test_user(session_factory) -> AsyncGenerator[User, None]:
    uid = uuid.uuid4()
    user = User(
        id=uid,
        username=f"gg_test_{uid.hex[:8]}",
        email=f"gg_test_{uid.hex[:8]}@test.local",
        hashed_password="test_hash",
        total_xp=0,
        current_level=1,
        daki_level=1,
    )
    async with session_factory() as s:
        s.add(user)
        await s.commit()
    yield user
    async with session_factory() as s:
        await s.execute(delete(UserProgress).where(UserProgress.user_id == uid))
        await s.execute(delete(User).where(User.id == uid))
        await s.commit()


@pytest_asyncio.fixture
async def isolated_challenge(session_factory) -> AsyncGenerator[Challenge, None]:
    """
    Un challenge SIN sector_id.  resolve_level_status siempre devuelve "unlocked"
    para este tipo → ideal para tests de evaluación sin lógica de bloqueo.
    """
    ch = Challenge(
        id=uuid.uuid4(),
        title="Test Challenge Aislado",
        description="Imprime el número 1.",
        difficulty_tier=DifficultyTier.BEGINNER,
        base_xp_reward=50,
        initial_code="print(1)",
        expected_output="1",
        test_inputs_json="[]",
        sector_id=None,             # ← sin sector, siempre accesible
        level_order=None,
        is_project=False,
        concepts_taught_json="[]",
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
        await s.execute(delete(UserProgress).where(UserProgress.challenge_id == ch.id))
        await s.execute(delete(Challenge).where(Challenge.id == ch.id))
        await s.commit()


@pytest_asyncio.fixture
async def sector_pair(session_factory, test_user) -> AsyncGenerator[tuple, None]:
    """
    Crea el mínimo necesario para probar la progresión entre sectores:

      • sector 9998 — un proyecto (is_project=True), ya completado por test_user
        → esto hace que sector 9999 sea accesible
      • sector 9999 — L1 (level_order=1) y L2 (level_order=2)
        → L1 desbloqueado, L2 bloqueado hasta que L1 se complete

    Returns (prev_project, l1, l2).
    """
    prev_proj = Challenge(
        id=uuid.uuid4(),
        title="Proyecto Sector Previo (test)",
        description="Proyecto del sector previo.",
        difficulty_tier=DifficultyTier.INTERMEDIATE,
        base_xp_reward=100,
        initial_code="pass",
        expected_output="",
        test_inputs_json="[]",
        sector_id=_SECTOR_PREV,
        level_order=1,
        is_project=True,            # ← proyecto que desbloquea el sector siguiente
        concepts_taught_json="[]",
        hints_json="[]",
        challenge_type="python",
        difficulty="easy",
        strict_match=False,
    )
    l1 = Challenge(
        id=uuid.uuid4(),
        title="Test L1 — Nexo Inicial",
        description="Imprime el número 1.",
        difficulty_tier=DifficultyTier.BEGINNER,
        base_xp_reward=50,
        initial_code="print(1)",
        expected_output="1",
        test_inputs_json="[]",
        sector_id=_SECTOR_TEST,
        level_order=1,
        is_project=False,
        concepts_taught_json="[]",
        hints_json='["Pista 1", "Pista 2", "Pista 3"]',
        challenge_type="python",
        difficulty="easy",
        strict_match=False,
    )
    l2 = Challenge(
        id=uuid.uuid4(),
        title="Test L2 — Misión Bloqueada",
        description="Imprime el número 2.",
        difficulty_tier=DifficultyTier.BEGINNER,
        base_xp_reward=50,
        initial_code="print(2)",
        expected_output="2",
        test_inputs_json="[]",
        sector_id=_SECTOR_TEST,
        level_order=2,
        is_project=False,
        concepts_taught_json="[]",
        hints_json="[]",
        challenge_type="python",
        difficulty="easy",
        strict_match=False,
    )

    async with session_factory() as s:
        s.add_all([prev_proj, l1, l2])
        await s.commit()

    # Marca el proyecto previo como COMPLETADO para test_user
    # → sector 9999 queda accesible, L1 desbloqueado
    async with session_factory() as s:
        prog = UserProgress(
            user_id=test_user.id,
            challenge_id=prev_proj.id,
            completed=True,
            attempts=1,
            hints_used=0,
        )
        s.add(prog)
        await s.commit()

    yield prev_proj, l1, l2

    # Teardown completo
    all_ids = [prev_proj.id, l1.id, l2.id]
    async with session_factory() as s:
        await s.execute(delete(UserProgress).where(UserProgress.challenge_id.in_(all_ids)))
        await s.execute(
            delete(Challenge).where(
                Challenge.sector_id.in_([_SECTOR_PREV, _SECTOR_TEST])
            )
        )
        await s.commit()


# ─────────────────────────────────────────────────────────────────────────────
# Helper: resultado de evaluación mock
# ─────────────────────────────────────────────────────────────────────────────

def _mock_success(stdout: str = "1") -> EvaluacionResult:
    return EvaluacionResult(
        status="success",
        output_got=stdout,
        output_expected=stdout,
        output_matched=True,
        execution_time_ms=12.5,
    )


def _mock_failed(stdout: str = "incorrecto") -> EvaluacionResult:
    return EvaluacionResult(
        status="failed",
        output_got=stdout,
        output_expected="1",
        output_matched=False,
        execution_time_ms=11.0,
    )


# ─────────────────────────────────────────────────────────────────────────────
# ── ESCENARIO 1: Acceso a nivel bloqueado ─────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────

class TestAccesoNivelBloqueado:

    async def test_nivel_2_bloqueado_para_usuario_sin_progreso(
        self, client, test_user, sector_pair
    ):
        """
        Un usuario que nunca completó L1 del sector de prueba intenta
        evaluar L2.  Debe recibir 403 LEVEL_LOCKED.
        """
        _, l1, l2 = sector_pair

        resp = await client.post("/api/v1/evaluate", json={
            "challenge_id": str(l2.id),
            "code":         "print(2)",
            "user_id":      str(test_user.id),
        })

        assert resp.status_code == 403
        body = resp.json()
        assert body["detail"]["code"] == "LEVEL_LOCKED"

    async def test_nivel_2_bloqueado_contiene_mensaje_descriptivo(
        self, client, test_user, sector_pair
    ):
        """El cuerpo del 403 incluye un mensaje legible."""
        _, _, l2 = sector_pair

        resp = await client.post("/api/v1/evaluate", json={
            "challenge_id": str(l2.id),
            "code":         "print(2)",
            "user_id":      str(test_user.id),
        })

        assert resp.status_code == 403
        assert len(resp.json()["detail"]["message"]) > 10

    async def test_nivel_1_accesible_para_usuario(
        self, client, test_user, sector_pair
    ):
        """
        L1 debe ser accesible para test_user porque el proyecto del sector
        anterior (9998) está marcado como completado en el fixture.
        """
        _, l1, _ = sector_pair

        with patch(
            "app.api.v1.endpoints.evaluate.evaluar_incursion",
            new_callable=AsyncMock,
            return_value=_mock_success("1"),
        ):
            resp = await client.post("/api/v1/evaluate", json={
                "challenge_id": str(l1.id),
                "code":         "print(1)",
                "user_id":      str(test_user.id),
            })

        assert resp.status_code == 200, (
            f"L1 no debe estar bloqueado. Respuesta: {resp.text}"
        )

    async def test_modo_invitado_sin_user_id_siempre_accesible(
        self, client, sector_pair
    ):
        """
        Sin user_id (modo invitado), resolve_level_status devuelve "unlocked"
        sin importar el sector.  Cualquier nivel debe ser evaluable.
        """
        _, _, l2 = sector_pair

        with patch(
            "app.api.v1.endpoints.evaluate.evaluar_incursion",
            new_callable=AsyncMock,
            return_value=_mock_success("2"),
        ):
            resp = await client.post("/api/v1/evaluate", json={
                "challenge_id": str(l2.id),
                "code":         "print(2)",
                # Sin user_id
            })

        assert resp.status_code == 200


# ─────────────────────────────────────────────────────────────────────────────
# ── ESCENARIO 2: Completar nivel → desbloqueo del siguiente ──────────────────
# ─────────────────────────────────────────────────────────────────────────────

class TestFlujoProgresion:

    async def test_l2_bloqueado_sin_completar_l1(
        self, client, test_user, sector_pair
    ):
        """Sin completar L1, GET /levels/sector muestra L2 como 'locked'."""
        resp = await client.get(
            f"/api/v1/levels/sector/{_SECTOR_TEST}",
            params={"user_id": str(test_user.id)},
        )
        assert resp.status_code == 200

        level_map = {lv["level_order"]: lv for lv in resp.json()["levels"]}
        assert level_map[1]["status"] == "unlocked"
        assert level_map[2]["status"] == "locked"

    async def test_l2_unlocked_tras_completar_l1(
        self, client, test_user, sector_pair, session_factory
    ):
        """Después de marcar L1 como completado, L2 pasa a 'unlocked'."""
        _, l1, l2 = sector_pair

        async with session_factory() as s:
            s.add(UserProgress(
                user_id=test_user.id,
                challenge_id=l1.id,
                completed=True,
                attempts=1,
                hints_used=0,
            ))
            await s.commit()

        resp = await client.get(
            f"/api/v1/levels/sector/{_SECTOR_TEST}",
            params={"user_id": str(test_user.id)},
        )
        assert resp.status_code == 200

        level_map = {lv["level_order"]: lv for lv in resp.json()["levels"]}
        assert level_map[1]["status"] == "completed"
        assert level_map[2]["status"] == "unlocked"

    async def test_evaluate_l2_desbloqueado_no_da_403(
        self, client, test_user, sector_pair, session_factory
    ):
        """L2 desbloqueado: evaluarlo con código incorrecto devuelve 200, no 403."""
        _, l1, l2 = sector_pair

        async with session_factory() as s:
            s.add(UserProgress(
                user_id=test_user.id,
                challenge_id=l1.id,
                completed=True,
                attempts=1,
                hints_used=0,
            ))
            await s.commit()

        with patch(
            "app.api.v1.endpoints.evaluate.evaluar_incursion",
            new_callable=AsyncMock,
            return_value=_mock_failed("incorrecto"),
        ):
            resp = await client.post("/api/v1/evaluate", json={
                "challenge_id": str(l2.id),
                "code":         "print('incorrecto')",
                "user_id":      str(test_user.id),
            })

        assert resp.status_code == 200
        assert resp.json()["output_matched"] is False

    async def test_sector_response_incluye_strict_match(
        self, client, sector_pair
    ):
        """El campo strict_match debe estar presente en cada nivel del sector."""
        resp = await client.get(f"/api/v1/levels/sector/{_SECTOR_TEST}")
        assert resp.status_code == 200

        for level in resp.json()["levels"]:
            assert "strict_match" in level


# ─────────────────────────────────────────────────────────────────────────────
# ── ESCENARIO 3: DAKI message en evaluaciones ────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────

class TestDakiMessage:

    async def test_daki_message_presente_en_fallo(
        self, client, isolated_challenge
    ):
        """daki_message es un string no vacío cuando el código falla."""
        with patch(
            "app.api.v1.endpoints.evaluate.evaluar_incursion",
            new_callable=AsyncMock,
            return_value=_mock_failed(),
        ):
            resp = await client.post("/api/v1/evaluate", json={
                "challenge_id": str(isolated_challenge.id),
                "code":         "print('incorrecto')",
            })

        assert resp.status_code == 200
        body = resp.json()
        assert body["output_matched"] is False
        assert "daki_message" in body
        assert len(body["daki_message"]) > 0

    async def test_daki_message_presente_en_exito(
        self, client, isolated_challenge
    ):
        """daki_message también viene en respuestas exitosas."""
        with patch(
            "app.api.v1.endpoints.evaluate.evaluar_incursion",
            new_callable=AsyncMock,
            return_value=_mock_success(),
        ):
            resp = await client.post("/api/v1/evaluate", json={
                "challenge_id": str(isolated_challenge.id),
                "code":         "print(1)",
            })

        assert resp.status_code == 200
        body = resp.json()
        assert body["output_matched"] is True
        assert len(body["daki_message"]) > 0

    async def test_daki_level_1_y_3_producen_mensajes(
        self, client, isolated_challenge
    ):
        """daki_level 1 (robótico) y 3 (compañero) devuelven strings no vacíos."""
        with patch(
            "app.api.v1.endpoints.evaluate.evaluar_incursion",
            new_callable=AsyncMock,
            return_value=_mock_failed(),
        ):
            r1 = await client.post("/api/v1/evaluate", json={
                "challenge_id": str(isolated_challenge.id),
                "code": "print('x')",
                "daki_level": 1,
            })
            r3 = await client.post("/api/v1/evaluate", json={
                "challenge_id": str(isolated_challenge.id),
                "code": "print('x')",
                "daki_level": 3,
            })

        assert r1.status_code == r3.status_code == 200
        assert len(r1.json()["daki_message"]) > 0
        assert len(r3.json()["daki_message"]) > 0

    async def test_error_info_presente_en_syntax_error(
        self, client, isolated_challenge
    ):
        """error_info viene poblado para SyntaxError."""
        with patch(
            "app.api.v1.endpoints.evaluate.evaluar_incursion",
            new_callable=AsyncMock,
            return_value=EvaluacionResult(
                status="error",
                output_got="",
                output_expected="1",
                output_matched=False,
                execution_time_ms=1.0,
                error="SyntaxError",
                error_detail="EOL while scanning string literal",
                error_line=1,
            ),
        ):
            resp = await client.post("/api/v1/evaluate", json={
                "challenge_id": str(isolated_challenge.id),
                "code":         "print('sin cerrar",
            })

        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "error"
        assert body["error_info"]["error_type"] == "SyntaxError"
        assert body["error_info"]["line"] == 1

    async def test_timeout_sandbox_real(
        self, client, isolated_challenge
    ):
        """
        Bucle infinito real — usa el sandbox completo (no mock).
        Marcado como slow: tarda ~3 s.
        """
        resp = await client.post(
            "/api/v1/evaluate",
            json={
                "challenge_id": str(isolated_challenge.id),
                "code":         "while True: pass",
            },
            timeout=10.0,
        )

        assert resp.status_code == 200
        assert resp.json()["status"] == "timeout"

    test_timeout_sandbox_real = pytest.mark.slow(test_timeout_sandbox_real)


# ─────────────────────────────────────────────────────────────────────────────
# ── ESCENARIO 4: Pistas de ENIGMA (POST /hint) ────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────

class TestHintEnigma:

    async def test_hint_devuelve_texto(
        self, client, test_user, isolated_challenge
    ):
        """POST /hint con IA mockeada devuelve {"hint": "<texto>"}."""
        with patch(
            "app.services.ai_mentor.get_hint",
            new_callable=AsyncMock,
            return_value="Usa print() con el valor correcto.",
        ):
            resp = await client.post("/api/v1/hint", json={
                "user_id":      str(test_user.id),
                "challenge_id": str(isolated_challenge.id),
                "source_code":  "print('incorrecto')",
                "error_output": "Salida: 'incorrecto'",
            })

        assert resp.status_code == 200
        body = resp.json()
        assert "hint" in body
        assert len(body["hint"]) > 0

    async def test_hint_acumula_telemetria(
        self, client, test_user, isolated_challenge, session_factory
    ):
        """
        Tres solicitudes de pista → hints_used=3 en UserProgress.
        También verifica el fix del bug hints_used=None (TypeError).
        """
        with patch(
            "app.services.ai_mentor.get_hint",
            new_callable=AsyncMock,
            return_value="Pista de ENIGMA.",
        ):
            for i in range(3):
                resp = await client.post("/api/v1/hint", json={
                    "user_id":      str(test_user.id),
                    "challenge_id": str(isolated_challenge.id),
                    "source_code":  f"# intento {i + 1}",
                    "error_output": "",
                })
                assert resp.status_code == 200, (
                    f"Intento {i+1} falló: {resp.text}"
                )

        # Verifica la telemetría en BD
        from sqlalchemy import select
        async with session_factory() as s:
            result = await s.execute(
                select(UserProgress).where(
                    UserProgress.user_id == test_user.id,
                    UserProgress.challenge_id == isolated_challenge.id,
                )
            )
            progress = result.scalar_one_or_none()

        assert progress is not None, "UserProgress no fue creado"
        assert progress.hints_used == 3

    async def test_hint_challenge_inexistente_da_404(
        self, client, test_user
    ):
        """UUID inexistente → 404 Not Found."""
        resp = await client.post("/api/v1/hint", json={
            "user_id":      str(test_user.id),
            "challenge_id": str(uuid.uuid4()),
            "source_code":  "print(1)",
            "error_output": "",
        })

        assert resp.status_code == 404

    async def test_hint_incrementa_desde_valor_previo(
        self, client, test_user, isolated_challenge, session_factory
    ):
        """
        Si el usuario ya tiene 2 pistas usadas y pide una más, hints_used=3.
        Verifica que el endpoint acumula correctamente.
        """
        from sqlalchemy import select

        # Pre-condición: hints_used=2 en BD
        async with session_factory() as s:
            s.add(UserProgress(
                user_id=test_user.id,
                challenge_id=isolated_challenge.id,
                completed=False,
                attempts=4,
                hints_used=2,
            ))
            await s.commit()

        with patch(
            "app.services.ai_mentor.get_hint",
            new_callable=AsyncMock,
            return_value="Tercera pista.",
        ):
            resp = await client.post("/api/v1/hint", json={
                "user_id":      str(test_user.id),
                "challenge_id": str(isolated_challenge.id),
                "source_code":  "print('intento')",
                "error_output": "",
            })

        assert resp.status_code == 200

        async with session_factory() as s:
            result = await s.execute(
                select(UserProgress).where(
                    UserProgress.user_id == test_user.id,
                    UserProgress.challenge_id == isolated_challenge.id,
                )
            )
            progress = result.scalar_one_or_none()

        assert progress.hints_used == 3


# ─────────────────────────────────────────────────────────────────────────────
# ── ESCENARIO 5: Evaluación exitosa (schema + campos) ────────────────────────
# ─────────────────────────────────────────────────────────────────────────────

class TestEvaluacionSchema:

    async def test_respuesta_incluye_campos_requeridos(
        self, client, isolated_challenge
    ):
        """EvaluateResponse debe tener todos los campos del contrato."""
        with patch(
            "app.api.v1.endpoints.evaluate.evaluar_incursion",
            new_callable=AsyncMock,
            return_value=_mock_success(),
        ):
            resp = await client.post("/api/v1/evaluate", json={
                "challenge_id": str(isolated_challenge.id),
                "code":         "print(1)",
            })

        assert resp.status_code == 200
        body = resp.json()

        required = {"status", "output_matched", "stdout", "stderr", "execution_time_ms", "daki_message"}
        assert not (required - body.keys()), f"Faltan: {required - body.keys()}"

    async def test_codigo_correcto_output_matched_true(
        self, client, isolated_challenge
    ):
        with patch(
            "app.api.v1.endpoints.evaluate.evaluar_incursion",
            new_callable=AsyncMock,
            return_value=_mock_success(),
        ):
            resp = await client.post("/api/v1/evaluate", json={
                "challenge_id": str(isolated_challenge.id),
                "code":         "print(1)",
            })

        assert resp.json()["output_matched"] is True
        assert resp.json()["status"] == "success"

    async def test_codigo_incorrecto_output_matched_false(
        self, client, isolated_challenge
    ):
        with patch(
            "app.api.v1.endpoints.evaluate.evaluar_incursion",
            new_callable=AsyncMock,
            return_value=_mock_failed("999"),
        ):
            resp = await client.post("/api/v1/evaluate", json={
                "challenge_id": str(isolated_challenge.id),
                "code":         "print(999)",
            })

        assert resp.json()["output_matched"] is False
        assert resp.json()["status"] == "failed"

    async def test_execution_time_ms_positivo(
        self, client, isolated_challenge
    ):
        with patch(
            "app.api.v1.endpoints.evaluate.evaluar_incursion",
            new_callable=AsyncMock,
            return_value=_mock_success(),
        ):
            resp = await client.post("/api/v1/evaluate", json={
                "challenge_id": str(isolated_challenge.id),
                "code":         "x = 1",
            })

        assert resp.json()["execution_time_ms"] >= 0.0

    async def test_error_info_none_en_exito(
        self, client, isolated_challenge
    ):
        """En una ejecución exitosa, error_info debe ser null."""
        with patch(
            "app.api.v1.endpoints.evaluate.evaluar_incursion",
            new_callable=AsyncMock,
            return_value=_mock_success(),
        ):
            resp = await client.post("/api/v1/evaluate", json={
                "challenge_id": str(isolated_challenge.id),
                "code":         "print(1)",
            })

        assert resp.json()["error_info"] is None


# ─────────────────────────────────────────────────────────────────────────────
# ── ESCENARIO 6: Health check y contratos básicos ────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────

class TestHealthYContratos:

    async def test_health_endpoint(self, client):
        resp = await client.get("/api/v1/health")
        assert resp.status_code == 200

    async def test_evaluate_sin_body_da_422(self, client):
        """Body vacío → 422 Unprocessable Entity (validación Pydantic)."""
        resp = await client.post("/api/v1/evaluate", json={})
        assert resp.status_code == 422

    async def test_evaluate_challenge_inexistente_no_da_500(self, client):
        """challenge_id inexistente → respuesta < 500 (el servidor no explota)."""
        with patch(
            "app.api.v1.endpoints.evaluate.evaluar_incursion",
            new_callable=AsyncMock,
            return_value=EvaluacionResult(
                status="error",
                error="NotFound",
                error_detail="Challenge not found.",
            ),
        ):
            resp = await client.post("/api/v1/evaluate", json={
                "challenge_id": str(uuid.uuid4()),
                "code":         "print(1)",
            })

        assert resp.status_code < 500

    async def test_sectors_endpoint_devuelve_lista(self, client):
        resp = await client.get("/api/v1/levels/sectors")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    async def test_hint_sin_body_da_422(self, client):
        resp = await client.post("/api/v1/hint", json={})
        assert resp.status_code == 422
