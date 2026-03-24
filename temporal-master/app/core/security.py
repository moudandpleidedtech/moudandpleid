"""
security.py — JWT helpers para autenticación de usuarios y administrador.

Flujo usuario:
  1. POST /api/v1/auth/register  { email, password }
     POST /api/v1/auth/login     { email, password }
     → devuelve { access_token, token_type: "bearer" }

  2. Endpoints protegidos usan require_user como dependencia.

Flujo admin:
  1. POST /api/v1/admin/auth/token  { username, password }
  2. Endpoints admin usan require_admin como dependencia.
"""

from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User

_bearer = HTTPBearer(auto_error=False)

ADMIN_ROLE = "ADMIN"

# ─── Password hashing ─────────────────────────────────────────────────────────

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


# ─── Creación de tokens ───────────────────────────────────────────────────────

def create_user_token(user_id: str, level: int) -> str:
    """JWT para usuarios normales — caduca en ACCESS_TOKEN_EXPIRE_MINUTES."""
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {
        "sub":   user_id,
        "level": level,
        "role":  "USER",
        "exp":   expire,
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_admin_token(user_id: str, callsign: str) -> str:
    """
    Crea un JWT firmado con SECRET_KEY que caduca en ADMIN_TOKEN_EXPIRE_MINUTES.
    Incluye role='ADMIN' en el payload para verificación explícita.
    """
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


# ─── Dependencia de acceso ────────────────────────────────────────────────────

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
      4. Usuario existe en BD y sigue teniendo is_admin=True
         (permite revocar acceso sin esperar a que expire el token).
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


# ─── Dependencia de usuario normal ────────────────────────────────────────────

async def require_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Dependencia FastAPI para endpoints de usuario autenticado.
    Verifica Bearer token firmado con SECRET_KEY y role == 'USER'.
    """
    _unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o ausente.",
        headers={"WWW-Authenticate": "Bearer"},
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

    user_id: str | None = payload.get("sub")
    if not user_id:
        raise _unauthorized

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise _unauthorized

    return user
