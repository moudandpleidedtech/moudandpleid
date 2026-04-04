"""
security.py — JWT helpers para autenticación de usuarios y administrador.

Flujo usuario:
  1. POST /api/v1/auth/register  { email, callsign, password }
     POST /api/v1/auth/login     { email, password }
     → devuelve { access_token, callsign, level, is_licensed }

  2. Endpoints privados usan get_current_operator como dependencia.
     Endpoints con auth opcional usan get_current_operator_optional.

Flujo admin:
  1. POST /api/v1/admin/auth/token  { callsign, password }
  2. Endpoints admin usan require_admin como dependencia.
"""

from datetime import datetime, timedelta, timezone

from fastapi import Cookie, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User

# ── Esquemas de seguridad ──────────────────────────────────────────────────────
# oauth2_scheme: registra el flujo en OpenAPI → habilita "Authorize" en Swagger UI
oauth2_scheme          = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)

# _bearer: para admin (HTTPBearer mantiene compatibilidad con el flujo existente)
_bearer = HTTPBearer(auto_error=False)

ADMIN_ROLE   = "ADMIN"
USER_ROLE    = "USER"
FOUNDER_ROLE = "FOUNDER"

# ─── Password hashing ─────────────────────────────────────────────────────────

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


# ─── Creación de tokens ───────────────────────────────────────────────────────

def create_user_token(
    user_id: str,
    callsign: str,
    level: int,
    is_licensed: bool,
    role: str = USER_ROLE,
) -> str:
    """
    JWT para Operadores.  Payload enriquecido:
      sub          → user_id (estándar JWT)
      callsign     → nombre de operador (para contexto de DAKI sin hit a BD)
      level        → nivel actual (para paywall y personalización)
      is_licensed  → acceso completo (para paywall de nivel 11+)
      role         → USER | FOUNDER (distingue de ADMIN; FOUNDER bypassa compuertas de catálogo)
    """
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {
        "sub":         user_id,
        "callsign":    callsign,
        "level":       level,
        "is_licensed": is_licensed,
        "role":        role,
        "exp":         expire,
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_admin_token(user_id: str, callsign: str) -> str:
    """JWT de admin — caduca en ADMIN_TOKEN_EXPIRE_MINUTES (8h por defecto)."""
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ADMIN_TOKEN_EXPIRE_MINUTES
    )
    payload = {
        "sub":      user_id,
        "callsign": callsign,
        "role":     ADMIN_ROLE,
        "exp":      expire,
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


# ─── Helpers internos ─────────────────────────────────────────────────────────

def _decode_user_token(token: str) -> str:
    """
    Decodifica y valida el JWT de usuario.
    Lanza HTTPException 401 si el token es inválido, expirado o no tiene role USER.
    Devuelve el user_id (claim 'sub').
    """
    _unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token de operador inválido o expirado.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        raise _unauthorized

    if payload.get("role") not in (USER_ROLE, FOUNDER_ROLE):
        raise _unauthorized

    user_id: str | None = payload.get("sub")
    if not user_id:
        raise _unauthorized

    return user_id


# ─── Dependencias de usuario ──────────────────────────────────────────────────

async def get_current_operator(
    token: str | None = Depends(oauth2_scheme_optional),
    daki_auth: str | None = Cookie(default=None),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Dependencia estándar — requiere JWT válido (cookie httpOnly o Authorization header).
    Uso: endpoints que SIEMPRE necesitan un usuario autenticado.

        @router.get("/secure")
        async def endpoint(operator: User = Depends(get_current_operator)): ...
    """
    resolved = token or daki_auth
    if not resolved:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de operador inválido o expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id = _decode_user_token(resolved)

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de operador inválido o expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_operator_optional(
    token: str | None = Depends(oauth2_scheme_optional),
    daki_auth: str | None = Cookie(default=None),
    db: AsyncSession = Depends(get_db),
) -> User | None:
    """
    Dependencia opcional — no falla si no hay token.
    Acepta cookie httpOnly o Authorization header.
    Devuelve el User si el token es válido, None si no hay token o es inválido.
    """
    resolved = token or daki_auth
    if resolved is None:
        return None
    try:
        user_id = _decode_user_token(resolved)
        result  = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
    except HTTPException:
        return None


# Alias para backward-compatibility con endpoints que ya importan require_user
require_user = get_current_operator


# ─── Dependencia de Founder ───────────────────────────────────────────────────

async def require_founder(
    token: str | None = Depends(oauth2_scheme_optional),
    daki_auth: str | None = Cookie(default=None),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Dependencia que protege endpoints exclusivos del Founder.
    Acepta cookie httpOnly (daki_auth) o Authorization header.
    Verifica role == 'FOUNDER' en el token Y en la BD.
    """
    resolved = token or daki_auth
    if not resolved:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sesión requerida.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id = _decode_user_token(resolved)  # valida firma y expiry

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None or user.role != FOUNDER_ROLE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso exclusivo para el Founder.",
        )
    return user


# ─── Dependencia de admin ─────────────────────────────────────────────────────

async def require_admin(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Dependencia FastAPI que protege los endpoints de admin.

    Verifica:
      1. Header Authorization: Bearer <token> presente.
      2. Token firmado con SECRET_KEY y no expirado.
      3. Payload contiene role == 'ADMIN'.
      4. Usuario existe en BD y sigue teniendo is_admin=True.
    """
    _unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token de administrador inválido o ausente.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    _forbidden = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Acceso denegado. Se requiere rol ADMIN.",
    )

    if not credentials:
        raise _unauthorized

    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
    except JWTError:
        raise _unauthorized

    if payload.get("role") != ADMIN_ROLE:
        raise _forbidden

    user_id: str | None = payload.get("sub")
    if not user_id:
        raise _unauthorized

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None or not user.is_admin:
        raise _forbidden

    return user
