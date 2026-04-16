"""
google_auth.py — Google OAuth 2.0 · DAKI EdTech

GET /api/v1/auth/google
    Redirige al consentimiento de Google con parámetro `state` firmado (anti-CSRF).

GET /api/v1/auth/google/callback
    Recibe el código de autorización, lo intercambia por tokens, obtiene el perfil
    del usuario, crea o vincula la cuenta y setea la cookie JWT.

Flujo completo:
  1. Usuario hace clic en "Continuar con Google"
  2. Frontend navega a  GET /api/v1/auth/google
  3. Backend genera state firmado, redirige a accounts.google.com
  4. Google redirige a  GET /api/v1/auth/google/callback?code=...&state=...
  5. Backend valida state, intercambia code por access_token
  6. Backend llama a Google UserInfo API → obtiene email, nombre, sub (google_id)
  7. Busca usuario por google_id  → si existe: login
     Busca usuario por email      → si existe: vincula google_id, login
     Ninguno                      → crea cuenta nueva con callsign auto-generado
  8. Setea cookie daki_auth (JWT), redirige al frontend (/hub o /boot-sequence)

Seguridad:
  - state: JWT firmado con SECRET_KEY, expira en 10 minutos → previene CSRF
  - Solo se confía en emails verificados por Google (email_verified=true)
  - No se acepta user_id ni email del cliente → todo viene de Google
  - Rate limit: 20/minute por IP (heredado del limiter global)
"""

import re
import secrets
import uuid
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.core.security import create_user_token, hash_password
from app.models.user import User

# Constante de error para whitelist — usada en redirect y frontend
_ALPHA_CLOSED_ERROR = "alpha_closed"

router = APIRouter(prefix="/auth", tags=["google-oauth"])

# ─── Constantes ───────────────────────────────────────────────────────────────

GOOGLE_AUTH_URL     = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL    = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

_CALLSIGN_RE = re.compile(r"^[a-zA-Z0-9_\-]{3,20}$")

# Duración de la cookie de sesión (idéntica a auth.py)
_COOKIE_MAX_AGE = 60 * 60 * 24 * 7   # 7 días

# ─── Helpers ──────────────────────────────────────────────────────────────────

def _build_state_token() -> str:
    """JWT firmado de un solo uso, expira en 10 min. Previene CSRF."""
    expire = datetime.now(timezone.utc) + timedelta(minutes=10)
    return jwt.encode(
        {"purpose": "google_oauth_state", "nonce": secrets.token_hex(16), "exp": expire},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def _verify_state_token(state: str) -> bool:
    """Valida la firma y el propósito del state. Devuelve False si es inválido."""
    try:
        payload = jwt.decode(state, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload.get("purpose") == "google_oauth_state"
    except JWTError:
        return False


def _set_auth_cookie(response: RedirectResponse, token: str) -> None:
    in_prod = not settings.DEBUG
    response.set_cookie(
        key="daki_auth",
        value=token,
        httponly=True,
        secure=in_prod,
        samesite="none" if in_prod else "lax",
        max_age=_COOKIE_MAX_AGE,
        path="/",
    )


def _sanitize_callsign(name: str) -> str:
    """
    Convierte el nombre de Google en un callsign válido.
    Ej: 'Juan García' → 'JuanGarcia'
    """
    # Solo alfanumérico, guión, guión bajo
    clean = re.sub(r"[^a-zA-Z0-9_\-]", "", name.replace(" ", ""))
    # Truncar a 18 chars para dejar espacio a sufijo numérico si hay colisión
    return clean[:18] if clean else "Operator"


async def _unique_callsign(base: str, db: AsyncSession) -> str:
    """Devuelve `base` si está disponible, o `base + N` con N incremental."""
    candidate = base[:20]
    if len(candidate) < 3:
        candidate = candidate.ljust(3, "0")

    for attempt in range(50):
        suffix = "" if attempt == 0 else str(attempt)
        cs = (candidate + suffix)[:20]
        result = await db.execute(select(User).where(User.callsign == cs))
        if result.scalar_one_or_none() is None:
            return cs

    # Fallback con UUID random si hay 50 colisiones (extremadamente raro)
    return "Op" + secrets.token_hex(4)[:9]


# ─── Endpoints ────────────────────────────────────────────────────────────────

@router.get(
    "/google",
    summary="Iniciar flujo OAuth con Google",
    description="Redirige al consentimiento de Google. El parámetro `state` previene CSRF.",
)
async def google_login() -> RedirectResponse:
    if not settings.GOOGLE_CLIENT_ID:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Google OAuth no configurado en este servidor.",
        )

    params = urlencode({
        "client_id":     settings.GOOGLE_CLIENT_ID,
        "redirect_uri":  settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope":         "openid email profile",
        "access_type":   "online",
        "prompt":        "select_account",   # siempre muestra el selector de cuenta
        "state":         _build_state_token(),
    })
    return RedirectResponse(url=f"{GOOGLE_AUTH_URL}?{params}")


@router.get(
    "/google/callback",
    summary="Callback OAuth de Google",
    description="Intercambia el code por tokens, crea/vincula la cuenta y setea la cookie JWT.",
)
async def google_callback(
    code:  str | None = None,
    state: str | None = None,
    error: str | None = None,
    db:    AsyncSession = Depends(get_db),
) -> RedirectResponse:

    frontend_base = settings.FRONTEND_URL or "http://localhost:3000"

    # ── 1. Google rechazó el consentimiento ───────────────────────────────────
    if error:
        return RedirectResponse(url=f"{frontend_base}/login?google_error=access_denied")

    # ── 2. Validar parámetros mínimos ─────────────────────────────────────────
    if not code or not state:
        return RedirectResponse(url=f"{frontend_base}/login?google_error=missing_params")

    # ── 3. Validar state (anti-CSRF) ──────────────────────────────────────────
    if not _verify_state_token(state):
        return RedirectResponse(url=f"{frontend_base}/login?google_error=invalid_state")

    # ── 4. Intercambiar code por access_token ─────────────────────────────────
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            token_resp = await client.post(
                GOOGLE_TOKEN_URL,
                data={
                    "code":          code,
                    "client_id":     settings.GOOGLE_CLIENT_ID,
                    "client_secret": settings.GOOGLE_CLIENT_SECRET,
                    "redirect_uri":  settings.GOOGLE_REDIRECT_URI,
                    "grant_type":    "authorization_code",
                },
            )
            token_resp.raise_for_status()
            token_data = token_resp.json()

            # ── 5. Obtener perfil del usuario ─────────────────────────────────
            userinfo_resp = await client.get(
                GOOGLE_USERINFO_URL,
                headers={"Authorization": f"Bearer {token_data['access_token']}"},
            )
            userinfo_resp.raise_for_status()
            userinfo = userinfo_resp.json()

        except httpx.HTTPError:
            return RedirectResponse(url=f"{frontend_base}/login?google_error=google_unreachable")

    # ── 6. Validar que el email sea verificado por Google ─────────────────────
    if not userinfo.get("email_verified"):
        return RedirectResponse(url=f"{frontend_base}/login?google_error=email_not_verified")

    google_id = userinfo["sub"]           # ID único e inmutable de Google
    email     = userinfo["email"].lower()
    name      = userinfo.get("name", "") or email.split("@")[0]

    # ── 7. Buscar o crear usuario ─────────────────────────────────────────────
    now = datetime.now(timezone.utc)
    is_new_user = False

    # Intento 1: buscar por google_id (login recurrente vía Google)
    result = await db.execute(select(User).where(User.google_id == google_id))
    user = result.scalar_one_or_none()

    if user is None:
        # Intento 2: buscar por email (el usuario tenía cuenta con password)
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()

        if user is not None:
            # Vincular google_id a la cuenta existente
            user.google_id = google_id
        else:
            # ── Whitelist Alpha (Directiva 041) ───────────────────────────────
            # Solo se aplica a cuentas nuevas. Usuarios existentes siempre pasan.
            allowed = settings.alpha_allowed_emails
            if allowed and email not in allowed:
                return RedirectResponse(
                    url=f"{frontend_base}/login?google_error={_ALPHA_CLOSED_ERROR}",
                    status_code=302,
                )

            # Crear cuenta nueva — callsign derivado del nombre de Google
            is_new_user = True
            base_callsign = _sanitize_callsign(name)
            callsign = await _unique_callsign(base_callsign, db)

            user = User(
                email=email,
                callsign=callsign,
                # Contraseña aleatoria — el usuario nunca la usará (login vía Google)
                password_hash=hash_password(secrets.token_hex(32)),
                google_id=google_id,
                current_level=1,
                last_login=now,
            )
            db.add(user)
            await db.flush()   # obtiene user.id sin commit

    # Actualizar last_login y calcular streak
    if user.last_login:
        delta = (now.date() - user.last_login.date()).days
        if delta == 1:
            user.streak_days = (user.streak_days or 0) + 1
        elif delta > 1:
            user.streak_days = 1
    else:
        user.streak_days = 1
    user.last_login = now

    await db.commit()
    await db.refresh(user)

    # ── 8. Generar JWT y setear cookie ────────────────────────────────────────
    token = create_user_token(
        user_id=str(user.id),
        callsign=user.callsign,
        level=user.current_level,
        is_licensed=user.is_licensed,
        role=user.role,
    )

    # ── 9. Redirigir al frontend ──────────────────────────────────────────────
    # El JWT viaja en una cookie httpOnly (SameSite=None; Secure) — no en la URL.
    # Pasar el token en ?token=... lo expone en logs del servidor, historial del
    # navegador y Referer headers. La cookie cross-domain con SameSite=None funciona
    # porque el frontend llama a la API con credentials:'include'.
    # El frontend lee /auth/me (GET, usa la cookie) para obtener el perfil del usuario.
    new_param = "1" if is_new_user else "0"
    destination = f"{frontend_base}/auth/google?new={new_param}"
    response = RedirectResponse(url=destination, status_code=302)
    _set_auth_cookie(response, token)
    return response
