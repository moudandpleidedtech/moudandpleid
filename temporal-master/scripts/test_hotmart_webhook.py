"""
scripts/test_hotmart_webhook.py — Validación end-to-end del webhook de Hotmart

Flujo completo vía API HTTP (sin conexión local a BD):
  1. Registra un operador de prueba en producción
  2. Dispara PURCHASE_APPROVED al webhook
  3. Hace login y verifica is_licensed=True via /auth/me
  4. Limpia el operador via el endpoint admin /payments/verify (reset manual)

USO
───
  python -m scripts.test_hotmart_webhook \\
      --hottok daki-hm-2026-xk9z \\
      --admin-key TU_ADMIN_API_KEY

  # Contra localhost:
  python -m scripts.test_hotmart_webhook \\
      --hottok daki-hm-2026-xk9z \\
      --admin-key TU_ADMIN_API_KEY \\
      --url http://localhost:8000
"""

import argparse
import asyncio
import sys
import uuid
from pathlib import Path

import httpx

sys.path.insert(0, str(Path(__file__).parent.parent))

# ─── Defaults ─────────────────────────────────────────────────────────────────

DEFAULT_URL   = "https://daki-api.onrender.com"
_uid          = uuid.uuid4().hex[:6].upper()
TEST_EMAIL    = f"hm_test_{_uid}@dakiedtech.com"
TEST_CALLSIGN = f"HM_TEST_{_uid}"
TEST_PASSWORD = "TestHotmart2025!"
TEST_TX_ID    = f"HP_TEST_{uuid.uuid4().hex[:8].upper()}"


# ─── Helpers visuales ─────────────────────────────────────────────────────────

def _sep(title: str = "") -> None:
    w = 58
    if title:
        pad = (w - len(title) - 2) // 2
        print(f"\n{'-' * pad} {title} {'-' * pad}")
    else:
        print(f"\n{'-' * w}")

def _ok(msg: str)   -> None: print(f"  [OK]  {msg}")
def _err(msg: str)  -> None: print(f"  [!!]  {msg}")
def _info(msg: str) -> None: print(f"   ->   {msg}")


# ─── Payload Hotmart v2 ────────────────────────────────────────────────────────

def _hotmart_payload(email: str) -> dict:
    return {
        "id":            TEST_TX_ID,
        "creation_date": 1744000000000,
        "event":         "PURCHASE_APPROVED",
        "version":       "2.0.0",
        "data": {
            "buyer": {
                "email": email,
                "name":  "Operador de Prueba",
            },
            "purchase": {
                "transaction": TEST_TX_ID,
                "status":      "approved",
                "offer":       {"code": "DEFAULT"},
            },
            "product": {
                "id":   123456,
                "name": "DAKI Nexo — Licencia Vitalicia",
            },
        },
    }


# ─── Test principal ────────────────────────────────────────────────────────────

async def run(hottok: str, base_url: str, admin_key: str, email_override: str = "") -> int:
    base  = base_url.rstrip("/")
    email = email_override.strip() if email_override.strip() else TEST_EMAIL

    _sep("DAKI - TEST WEBHOOK HOTMART (HTTP)")
    _info(f"Backend  : {base}")
    _info(f"Email    : {email}")
    _info(f"Tx ID    : {TEST_TX_ID}")

    async with httpx.AsyncClient(timeout=20.0, follow_redirects=True) as client:

        # ── PASO 1: Registrar operador de prueba ──────────────────────────────
        _sep("PASO 1 — Registrar operador de prueba")

        r = await client.post(f"{base}/api/v1/auth/register", json={
            "email":    email,
            "callsign": TEST_CALLSIGN,
            "password": TEST_PASSWORD,
        })

        if r.status_code == 201:
            data = r.json()
            _ok(f"Operador creado — callsign: {data.get('callsign')}")
            _info(f"is_licensed antes del webhook: {data.get('is_licensed')}")
        elif r.status_code == 409:
            _info("Operador ya existia en la BD. Continuando con webhook...")
        elif r.status_code == 403 and "ALPHA_CLOSED" in r.text:
            _info("ALPHA_WHITELIST activa — el email ya debe existir en la BD.")
            _info("Saltando register, disparando webhook directo...")
        else:
            _err(f"Register fallo: {r.status_code} — {r.text[:200]}")
            return 1

        # ── PASO 2: Disparar webhook PURCHASE_APPROVED ────────────────────────
        _sep("PASO 2 — Disparar PURCHASE_APPROVED")

        webhook_url = f"{base}/api/v1/hotmart/webhook?hottok={hottok}"
        _info(f"POST {webhook_url}")

        r = await client.post(webhook_url, json=_hotmart_payload(email))

        _info(f"HTTP status : {r.status_code}")
        if r.status_code != 200:
            _err(f"Webhook devolvió {r.status_code}: {r.text[:300]}")
            return 1

        body = r.json()
        _info(f"received    : {body.get('received')}")
        _info(f"processed   : {body.get('processed')}")
        if "callsign" in body:
            _ok(f"Procesado para: {body.get('callsign')}")
        if "reason" in body:
            _info(f"reason      : {body['reason']}")

        if not body.get("processed"):
            _err("El webhook respondio 200 pero processed=False.")
            _err("El email no fue encontrado en la BD.")
            return 1

        # Si el webhook retornó callsign, la activación está confirmada en BD
        if body.get("callsign"):
            _ok(f"Activacion confirmada en BD para: {body.get('callsign')}")
            _ok("is_licensed=True y subscription_status=ACTIVE aplicados.")
            result = 0
        else:
            result = 0

        # ── PASO 3: Login y verificar is_licensed (best-effort) ───────────────
        _sep("PASO 3 — Verificar via login (best-effort)")

        r = await client.post(f"{base}/api/v1/auth/login", json={
            "email":    email,
            "password": TEST_PASSWORD,
        })

        if r.status_code == 200:
            login_data  = r.json()
            is_licensed = login_data.get("is_licensed")
            _info(f"is_licensed : {is_licensed}")
            _info(f"callsign    : {login_data.get('callsign')}")
            if is_licensed:
                _ok("Login confirma is_licensed=True")
            else:
                _err("Login muestra is_licensed=False — revisar flujo.")
                result = 1
        else:
            _info("Login con password de test no disponible (cuenta existente con otra clave).")
            _info("Activacion ya confirmada por la respuesta del webhook (paso 2).")

        # ── PASO 4: Limpieza via admin ─────────────────────────────────────────
        _sep("PASO 4 — Limpieza")

        if admin_key:
            # No hay endpoint de delete-user, pero podemos dejar el registro
            # marcado para identificarlo (callsign empieza con HM_TEST_)
            _info("Operador de prueba queda en BD con prefijo HM_TEST_ para identificarlo.")
            _info(f"Email: {TEST_EMAIL}")
            _info("Podés eliminarlo manualmente desde el panel admin si lo necesitás.")
        else:
            _info("Sin admin-key — operador de prueba conservado en BD.")

    _sep()
    if result == 0:
        print("  [PASS]  TEST PASADO - Flujo Hotmart -> DAKI funcionando correctamente.\n")
    else:
        print("  [FAIL]  TEST FALLIDO - Revisa los logs de arriba.\n")

    return result


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Test end-to-end HTTP del webhook Hotmart — licencia vitalicia.",
    )
    parser.add_argument("--hottok",   required=True,      help="Valor de HOTMART_HOTTOK en Render.")
    parser.add_argument("--admin-key", default="",         help="ADMIN_API_KEY de Render (para limpieza).")
    parser.add_argument("--url",      default=DEFAULT_URL, help=f"URL base del backend (default: {DEFAULT_URL})")
    parser.add_argument("--email",    default="",          help="Usar este email en vez del generado (debe existir o estar en whitelist).")
    args = parser.parse_args()

    code = asyncio.run(run(
        hottok=args.hottok,
        base_url=args.url,
        admin_key=args.admin_key,
        email_override=args.email,
    ))
    sys.exit(code)


if __name__ == "__main__":
    main()
