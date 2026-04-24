"""
tests/e2e/test_production.py
============================
Smoke tests E2E contra la API de producción.

Cubren el viaje completo del Operador:
  1. Health check
  2. Registro
  3. Login
  4. Lista de challenges (10 free, 195+ paid)
  5. Ejecución de challenge gratuito (sandbox vivo)
  6. Paywall: challenge de pago → 402 para usuario sin licencia
  7. Hotmart checkout → URL válida generada
  8. Redeem llave táctica inválida → 400 (no 500)

Ejecutar:
    cd temporal-master
    pip install httpx pytest
    pytest tests/e2e/test_production.py -v

    # Con URL custom (para staging o preview):
    API_URL=https://staging.onrender.com pytest tests/e2e/test_production.py -v
"""

import os
import time
import uuid

import httpx
import pytest

# ─── Configuración ────────────────────────────────────────────────────────────

BASE = os.getenv("API_URL", "https://daki-api.onrender.com")
TIMEOUT = 40  # Render puede tener cold start de ~20s

# Credenciales de un usuario de prueba creado durante la sesión
_ts = int(time.time())
_EMAIL = f"e2e_smoke_{_ts}@example.com"
_PASSWORD = "E2ESmoke2025!X"
_CALLSIGN = f"Smoke{_ts}"


# ─── Fixtures ─────────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def client():
    with httpx.Client(base_url=BASE, timeout=TIMEOUT) as c:
        yield c


@pytest.fixture(scope="session")
def registered_user(client):
    """Registra un usuario nuevo y devuelve {token, user_id}."""
    r = client.post("/api/v1/auth/register", json={
        "email": _EMAIL,
        "password": _PASSWORD,
        "callsign": _CALLSIGN,
    })
    assert r.status_code == 201, f"Registro falló: {r.text[:200]}"
    data = r.json()
    return {"token": data["access_token"], "user_id": data["user_id"]}


@pytest.fixture(scope="session")
def auth_headers(registered_user):
    return {"Authorization": f"Bearer {registered_user['token']}"}


@pytest.fixture(scope="session")
def challenges(client, registered_user, auth_headers):
    """Carga la lista de challenges una vez para toda la sesión."""
    r = client.get(
        f"/api/v1/challenges?user_id={registered_user['user_id']}",
        headers=auth_headers,
    )
    assert r.status_code == 200
    return r.json()


# ─── Tests ────────────────────────────────────────────────────────────────────

class TestHealth:
    def test_api_live(self, client):
        r = client.get("/health")
        assert r.status_code == 200
        body = r.json()
        assert body.get("status") == "ok"
        assert "app" in body


class TestAuth:
    def test_registro_retorna_token(self, registered_user):
        assert registered_user["token"]
        assert registered_user["user_id"]

    def test_login_con_credenciales_validas(self, client):
        r = client.post("/api/v1/auth/login", json={
            "email": _EMAIL,
            "password": _PASSWORD,
        })
        assert r.status_code == 200
        assert "access_token" in r.json()

    def test_login_credenciales_invalidas_retorna_401(self, client):
        r = client.post("/api/v1/auth/login", json={
            "email": _EMAIL,
            "password": "wrong-password-xyz",
        })
        assert r.status_code in (401, 400)


class TestChallenges:
    def test_lista_retorna_200(self, challenges):
        assert isinstance(challenges, list)
        assert len(challenges) > 0

    def test_hay_exactamente_10_challenges_gratuitos(self, challenges):
        free = [c for c in challenges if c.get("is_free")]
        assert len(free) == 10, f"Esperados 10 free, encontrados {len(free)}"

    def test_hay_challenges_de_pago(self, challenges):
        paid = [c for c in challenges if not c.get("is_free")]
        assert len(paid) >= 100, f"Esperados ≥100 paid, encontrados {len(paid)}"

    def test_challenges_tienen_campos_requeridos(self, challenges):
        required = {"id", "title", "description", "is_free", "level_order", "initial_code"}
        for c in challenges[:5]:  # valida los primeros 5
            missing = required - set(c.keys())
            assert not missing, f"Challenge sin campos: {missing}"

    def test_expected_output_oculto_en_lista(self, challenges):
        """El expected_output no debe exponerse en la lista (solo en detalle)."""
        for c in challenges[:10]:
            assert c.get("expected_output") == "", \
                f"expected_output expuesto en lista para {c['id']}"


class TestExecution:
    def _first_free_challenge(self, challenges):
        free = sorted(
            [c for c in challenges if c.get("is_free")],
            key=lambda c: c.get("level_order") or 999,
        )
        return free[0]

    def test_ejecutar_challenge_gratuito_retorna_200(self, client, challenges, registered_user, auth_headers):
        ch = self._first_free_challenge(challenges)
        r = client.post("/api/v1/execute", json={
            "user_id": registered_user["user_id"],
            "challenge_id": ch["id"],
            "source_code": ch.get("initial_code", "print('hola')"),
            "test_inputs": ch.get("test_inputs") or [],
            "hints_used": 0,
            "time_spent_ms": 500,
        }, headers=auth_headers)
        assert r.status_code == 200
        body = r.json()
        assert "stdout" in body
        assert "output_matched" in body
        assert "gamification" in body

    def test_sandbox_no_esta_caido(self, client, challenges, registered_user, auth_headers):
        """Si el sandbox cayó, daki_message empieza con 'Entorno'."""
        ch = self._first_free_challenge(challenges)
        # Enviamos código que produce output determinístico
        r = client.post("/api/v1/execute", json={
            "user_id": registered_user["user_id"],
            "challenge_id": ch["id"],
            "source_code": "print(2 + 2)",
            "test_inputs": [],
            "hints_used": 0,
            "time_spent_ms": 100,
        }, headers=auth_headers)
        assert r.status_code == 200
        body = r.json()
        sandbox_dead = body.get("daki_message", "").startswith("Entorno")
        assert not sandbox_dead, "Sandbox caído: " + body.get("daki_message", "")
        assert body.get("stdout", "").strip() == "4"

    def test_paywall_challenge_pago_retorna_402(self, client, challenges, registered_user, auth_headers):
        """Usuario sin licencia no puede ejecutar challenges de pago."""
        paid = sorted(
            [c for c in challenges if not c.get("is_free")],
            key=lambda c: c.get("level_order") or 999,
        )
        assert paid, "No hay challenges de pago en la lista"
        ch = paid[0]
        r = client.post("/api/v1/execute", json={
            "user_id": registered_user["user_id"],
            "challenge_id": ch["id"],
            "source_code": "print('test')",
            "test_inputs": [],
            "hints_used": 0,
            "time_spent_ms": 100,
        }, headers=auth_headers)
        assert r.status_code == 402, \
            f"Paywall roto: challenge de pago devolvió HTTP {r.status_code}"

    def test_mismatch_output_expone_failed_case(self, client, challenges, registered_user, auth_headers):
        """Código con output incorrecto (sin error) debe retornar failed_case."""
        ch = self._first_free_challenge(challenges)
        r = client.post("/api/v1/execute", json={
            "user_id": registered_user["user_id"],
            "challenge_id": ch["id"],
            "source_code": "print('output_incorrecto_definitivamente')",
            "test_inputs": [],
            "hints_used": 0,
            "time_spent_ms": 100,
        }, headers=auth_headers)
        assert r.status_code == 200
        body = r.json()
        assert body["output_matched"] is False
        # failed_case debe estar presente cuando hay mismatch sin error de ejecución
        if not body.get("stderr"):
            assert body.get("failed_case") is not None


class TestCheckout:
    def test_hotmart_checkout_lifetime_genera_url(self, client, auth_headers):
        r = client.post("/api/v1/hotmart/checkout",
                        json={"plan": "lifetime"}, headers=auth_headers)
        assert r.status_code == 200
        url = r.json().get("checkout_url", "")
        assert url.startswith("https://pay.hotmart.com/"), \
            f"URL inesperada: {url}"

    def test_hotmart_checkout_monthly_genera_url(self, client, auth_headers):
        r = client.post("/api/v1/hotmart/checkout",
                        json={"plan": "monthly"}, headers=auth_headers)
        assert r.status_code == 200
        url = r.json().get("checkout_url", "")
        assert url.startswith("https://pay.hotmart.com/"), \
            f"URL mensual inesperada: {url}"

    def test_checkout_sin_jwt_retorna_401(self):
        # Cliente limpio sin cookies de sesión previas
        with httpx.Client(base_url=BASE, timeout=TIMEOUT) as fresh:
            r = fresh.post("/api/v1/hotmart/checkout", json={"plan": "lifetime"})
        assert r.status_code == 401

    def test_redeem_llave_invalida_retorna_400_no_500(self, client, auth_headers):
        """Regresión: antes retornaba 500 por columna claimed_by faltante."""
        r = client.post("/api/v1/checkout/redeem",
                        json={"code_string": "INVALID-XXXX-TEST"},
                        headers=auth_headers)
        assert r.status_code == 400, \
            f"Redeem retornó {r.status_code} — esperado 400 (código inválido)"
        assert "detail" in r.json()
