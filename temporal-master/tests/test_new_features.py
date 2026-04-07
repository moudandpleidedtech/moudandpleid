"""
tests/test_new_features.py
============================
Tests para las features nuevas — sesiones 4 y 5 del Protocolo Guerrero.

Cubre:
  - GET /api/v1/campaign/map       — estructura y progreso de nodos
  - GET /api/v1/intel/weekly-review — conceptos para revisión semanal
  - GET /api/v1/intel/mastery-radar — radar de maestría
  - GET /api/v1/intel/pattern-callout — callout de patrones entre challenges
  - GET /api/v1/intel/retrieval-challenge — challenge de recuperación
  - GET /api/v1/leaderboard        — tabla de clasificación
  - ChallengeOut: campos is_ironman, edge_cases, expected_output
  - Predict challenge: challenge_type='predict', expected_output presente
  - GET /api/v1/users/profile/{callsign} — perfil público

Ejecutar:
    cd temporal-master
    pytest tests/test_new_features.py -v
"""

import uuid
import json
from typing import AsyncGenerator

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
from app.models.concept_mastery import ConceptMastery
from app.models.user import User
from app.models.user_progress import UserProgress
from main import app


# ── Fixtures de infraestructura ───────────────────────────────────────────────

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


@pytest_asyncio.fixture
async def test_user(session_factory) -> AsyncGenerator[User, None]:
    uid = uuid.uuid4()
    user = User(
        id=uid,
        callsign=f"nf_test_{uid.hex[:8]}",
        email=f"nf_test_{uid.hex[:8]}@test.local",
        password_hash="test_hash",
        total_xp=500,
        current_level=5,
        daki_level=1,
    )
    async with session_factory() as s:
        s.add(user)
        await s.commit()
    yield user
    async with session_factory() as s:
        await s.execute(delete(ConceptMastery).where(ConceptMastery.user_id == uid))
        await s.execute(delete(UserProgress).where(UserProgress.user_id == uid))
        await s.execute(delete(User).where(User.id == uid))
        await s.commit()


@pytest_asyncio.fixture
async def ironman_challenge(session_factory) -> AsyncGenerator[Challenge, None]:
    """Challenge ironman=True para tests de ChallengeOut."""
    ch = Challenge(
        id=uuid.uuid4(),
        title="Test Ironman",
        description="Sin pistas.",
        difficulty_tier=DifficultyTier.ADVANCED,
        base_xp_reward=300,
        initial_code="print('ok')",
        expected_output="ok",
        test_inputs_json="[]",
        sector_id=None,
        level_order=None,
        is_project=False,
        is_ironman=True,
        edge_cases_json=json.dumps([
            {"description": "¿Qué pasa con lista vacía?"},
            {"description": "¿Qué pasa con None?"},
        ]),
        concepts_taught_json='["test_concept"]',
        hints_json="[]",
        challenge_type="python",
        difficulty="hard",
        strict_match=False,
        is_free=True,
    )
    async with session_factory() as s:
        s.add(ch)
        await s.commit()
    yield ch
    async with session_factory() as s:
        await s.execute(delete(Challenge).where(Challenge.id == ch.id))
        await s.commit()


@pytest_asyncio.fixture
async def predict_challenge(session_factory) -> AsyncGenerator[Challenge, None]:
    """Challenge de tipo predict para tests específicos."""
    ch = Challenge(
        id=uuid.uuid4(),
        title="Test Predict",
        description="Predecí el output.",
        difficulty_tier=DifficultyTier.INTERMEDIATE,
        base_xp_reward=150,
        initial_code="print(2 + 3)",
        expected_output="5",
        test_inputs_json="[]",
        sector_id=21,
        level_order=199,   # fuera del rango real para no interferir
        is_project=False,
        is_ironman=False,
        edge_cases_json=None,
        concepts_taught_json='["arithmetic"]',
        hints_json="[]",
        challenge_type="predict",
        difficulty="medium",
        strict_match=True,
        is_free=False,
    )
    async with session_factory() as s:
        s.add(ch)
        await s.commit()
    yield ch
    async with session_factory() as s:
        await s.execute(delete(Challenge).where(Challenge.id == ch.id))
        await s.commit()


# ── Tests: Campaign Map ───────────────────────────────────────────────────────

class TestCampaignMap:
    async def test_campaign_map_sin_user_devuelve_zonas(self, client):
        r = await client.get("/api/v1/campaign/map")
        assert r.status_code == 200
        data = r.json()
        assert "zones" in data
        assert "python_core" in data["zones"]

    async def test_campaign_map_tiene_4_zonas(self, client):
        r = await client.get("/api/v1/campaign/map")
        data = r.json()
        zonas = data["zones"]
        assert "python_core"       in zonas
        assert "python_avanzado"   in zonas
        assert "python_elite"      in zonas
        assert "protocolos_elite"  in zonas

    async def test_campaign_map_protocolos_tiene_3_nodos(self, client):
        r = await client.get("/api/v1/campaign/map")
        protocolos = r.json()["zones"]["protocolos_elite"]
        assert "s19_debug"     in protocolos
        assert "s20_interview" in protocolos
        assert "s21_predict"   in protocolos

    async def test_campaign_map_primer_nodo_desbloqueado(self, client, test_user):
        r = await client.get(f"/api/v1/campaign/map?user_id={test_user.id}")
        assert r.status_code == 200
        zonas = r.json()["zones"]
        # El primer nodo de python_core siempre desbloqueado
        primer_nodo = zonas["python_core"]["s00_s03"]
        assert primer_nodo["unlocked"] is True

    async def test_campaign_map_total_completed_presente(self, client, test_user):
        r = await client.get(f"/api/v1/campaign/map?user_id={test_user.id}")
        assert "total_completed" in r.json()


# ── Tests: Intel Endpoints ────────────────────────────────────────────────────

class TestIntelWeeklyReview:
    async def test_weekly_review_sin_datos_devuelve_lista_vacia(self, client, test_user):
        r = await client.get(f"/api/v1/intel/weekly-review?user_id={test_user.id}")
        assert r.status_code == 200
        data = r.json()
        assert "concepts" in data
        assert "total" in data
        assert "cutoff_days" in data
        assert data["cutoff_days"] == 7

    async def test_weekly_review_campo_requerido(self, client):
        r = await client.get("/api/v1/intel/weekly-review")
        # user_id es requerido
        assert r.status_code == 422


class TestIntelMasteryRadar:
    async def test_mastery_radar_sin_datos_devuelve_ejes(self, client, test_user):
        r = await client.get(f"/api/v1/intel/mastery-radar?user_id={test_user.id}")
        assert r.status_code == 200
        data = r.json()
        assert "axes" in data
        assert len(data["axes"]) == 7   # 7 categorías definidas en _ORDERED_CATEGORIES
        assert "total_concepts" in data

    async def test_mastery_radar_ejes_tienen_score(self, client, test_user):
        r = await client.get(f"/api/v1/intel/mastery-radar?user_id={test_user.id}")
        for axis in r.json()["axes"]:
            assert "category" in axis
            assert "score"    in axis
            assert "count"    in axis
            assert 0 <= axis["score"] <= 100


class TestIntelPatternCallout:
    async def test_pattern_callout_sin_challenge_devuelve_vacio(self, client, test_user, predict_challenge):
        r = await client.get(
            f"/api/v1/intel/pattern-callout"
            f"?user_id={test_user.id}&challenge_id={predict_challenge.id}"
        )
        assert r.status_code == 200
        # Sin challenges completados → no hay overlap → dict vacío
        assert r.json() == {} or "concept" not in r.json()

    async def test_pattern_callout_campos_requeridos(self, client):
        r = await client.get("/api/v1/intel/pattern-callout?user_id=" + str(uuid.uuid4()))
        assert r.status_code == 422


class TestIntelRetrievalChallenge:
    async def test_retrieval_challenge_sin_completados_devuelve_vacio(self, client, test_user):
        r = await client.get(
            f"/api/v1/intel/retrieval-challenge"
            f"?user_id={test_user.id}&concept=variables"
        )
        assert r.status_code == 200
        # Sin challenges completados → vacío
        assert r.json() == {}


# ── Tests: ChallengeOut — Campos Nuevos ──────────────────────────────────────

class TestChallengeOutNuevosCampos:
    async def test_ironman_challenge_tiene_campo_is_ironman(self, client, ironman_challenge):
        r = await client.get(f"/api/v1/challenges/{ironman_challenge.id}")
        assert r.status_code == 200
        data = r.json()
        assert "is_ironman"    in data
        assert "edge_cases"    in data
        assert "expected_output" in data
        assert data["is_ironman"] is True

    async def test_ironman_challenge_tiene_edge_cases(self, client, ironman_challenge):
        r = await client.get(f"/api/v1/challenges/{ironman_challenge.id}")
        edge_cases = r.json()["edge_cases"]
        assert isinstance(edge_cases, list)
        assert len(edge_cases) == 2
        assert "description" in edge_cases[0]

    async def test_predict_challenge_tiene_expected_output(self, client, predict_challenge):
        r = await client.get(f"/api/v1/challenges/{predict_challenge.id}")
        assert r.status_code == 200
        data = r.json()
        assert data["challenge_type"]   == "predict"
        assert data["expected_output"]  == "5"
        assert data["is_ironman"]       is False

    async def test_challenge_sin_edge_cases_retorna_lista_vacia(self, client, predict_challenge):
        r = await client.get(f"/api/v1/challenges/{predict_challenge.id}")
        assert r.json()["edge_cases"] == []


# ── Tests: Leaderboard ────────────────────────────────────────────────────────

class TestLeaderboard:
    async def test_leaderboard_devuelve_estructura_correcta(self, client):
        r = await client.get("/api/v1/leaderboard")
        assert r.status_code == 200
        data = r.json()
        assert "top50"         in data
        assert "total_players" in data
        assert isinstance(data["top50"], list)

    async def test_leaderboard_con_user_devuelve_rank(self, client, test_user):
        r = await client.get(f"/api/v1/leaderboard?user_id={test_user.id}")
        assert r.status_code == 200
        data = r.json()
        assert "user_rank" in data
        if data["user_rank"]:
            assert "rank"       in data["user_rank"]
            assert "total_xp"   in data["user_rank"]
            assert "league_tier" in data["user_rank"]

    async def test_leaderboard_top50_max_50_entries(self, client):
        r = await client.get("/api/v1/leaderboard")
        assert len(r.json()["top50"]) <= 50


# ── Tests: Perfil Público ─────────────────────────────────────────────────────

class TestPublicProfile:
    async def test_profile_existente_devuelve_datos(self, client, test_user):
        r = await client.get(f"/api/v1/users/profile/{test_user.callsign}")
        assert r.status_code == 200
        data = r.json()
        assert data["callsign"]  == test_user.callsign
        assert "total_xp"        in data
        assert "current_level"   in data
        assert "completed_challenges" in data
        assert "badges"          in data

    async def test_profile_inexistente_da_404(self, client):
        r = await client.get("/api/v1/users/profile/OPERADOR_QUE_NO_EXISTE_JAMAS")
        assert r.status_code == 404


# ── Tests: Campaign Map — Progresión ─────────────────────────────────────────

class TestCampaignMapProgresion:
    async def test_nodo_siguiente_bloqueado_sin_completar_primero(self, client, test_user):
        """Sin completar s00_s03, el nodo s04_s07 debe estar bloqueado."""
        r = await client.get(f"/api/v1/campaign/map?user_id={test_user.id}")
        zonas = r.json()["zones"]
        # Segundo nodo de python_core debe estar bloqueado (usuario nuevo sin progreso)
        segundo_nodo = zonas["python_core"]["s04_s07"]
        assert segundo_nodo["unlocked"] is False

    async def test_protocolos_elite_bloqueados_por_defecto(self, client, test_user):
        """Protocolos de élite deben estar bloqueados para usuario sin progreso."""
        r = await client.get(f"/api/v1/campaign/map?user_id={test_user.id}")
        protocolos = r.json()["zones"]["protocolos_elite"]
        for nodo in protocolos.values():
            assert nodo["unlocked"] is False
