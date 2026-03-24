"""
app/api/v1/endpoints/auth.py — Autenticación de Operadores · DAKI EdTech

POST /api/v1/auth/register  { email, callsign, password }
    → crea usuario, devuelve JWT enriquecido

POST /api/v1/auth/login     { email, password }
    → verifica credenciales, actualiza last_login, devuelve JWT enriquecido

JWT payload:  sub | callsign | level | is_licensed | role | exp
"""

import re
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, EmailStr, field_validator
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.rate_limit import limiter
from app.core.security import create_user_token, hash_password, verify_password
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])

_CALLSIGN_RE = re.compile(r"^[a-zA-Z0-9_\-]{3,20}$")


# ─── Schemas ──────────────────────────────────────────────────────────────────

class RegisterRequest(BaseModel):
    email:    EmailStr
    callsign: str
    password: str

    @field_validator("callsign")
    @classmethod
    def callsign_format(cls, v: str) -> str:
        v = v.strip()
        if not _CALLSIGN_RE.match(v):
            raise ValueError(
                "El callsign solo puede contener letras, números, guiones "
                "o guión bajo (3-20 caracteres, sin espacios)."
            )
        return v

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres.")
        return v


class LoginRequest(BaseModel):
    email:    EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type:   str  = "bearer"
    user_id:      str
    callsign:     str
    level:        int
    is_licensed:  bool


# ─── Endpoints ────────────────────────────────────────────────────────────────

@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nuevo Operador",
    description=(
        "Crea una cuenta con email + callsign + password. "
        "El callsign es el nombre de operador único (3-20 chars, sin espacios). "
        "Devuelve un JWT listo para usar en el header Authorization."
    ),
)
@limiter.limit("10/minute")
async def register(
    request: Request,
    payload: RegisterRequest,
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    # ── Unicidad de email ────────────────────────────────────────────────────
    result = await db.execute(select(User).where(User.email == payload.email))
    if result.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Este email ya está registrado.",
        )

    # ── Unicidad de callsign ─────────────────────────────────────────────────
    result = await db.execute(select(User).where(User.callsign == payload.callsign))
    if result.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Este callsign ya está en uso. Elige otro identificador de Operador.",
        )

    user = User(
        email=payload.email,
        callsign=payload.callsign,
        password_hash=hash_password(payload.password),
        last_login=datetime.now(timezone.utc),
    )
    db.add(user)
    await db.flush()
    await db.commit()
    await db.refresh(user)

    token = create_user_token(
        user_id=str(user.id),
        callsign=user.callsign,
        level=user.current_level,
        is_licensed=user.is_licensed,
    )
    return TokenResponse(
        access_token=token,
        user_id=str(user.id),
        callsign=user.callsign,
        level=user.current_level,
        is_licensed=user.is_licensed,
    )


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Autenticar Operador con email y contraseña",
    description=(
        "Verifica credenciales, actualiza last_login y devuelve un JWT enriquecido "
        "con callsign, level e is_licensed para personalización inmediata en el frontend."
    ),
)
@limiter.limit("20/minute")
async def login(
    request: Request,
    payload: LoginRequest,
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    result = await db.execute(select(User).where(User.email == payload.email))
    user = result.scalar_one_or_none()

    # Mismo mensaje para email no encontrado y contraseña incorrecta (anti-enumeración)
    _invalid = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if user is None or not verify_password(payload.password, user.password_hash):
        raise _invalid

    # ── Actualizar last_login ────────────────────────────────────────────────
    user.last_login = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(user)

    token = create_user_token(
        user_id=str(user.id),
        callsign=user.callsign,
        level=user.current_level,
        is_licensed=user.is_licensed,
    )
    return TokenResponse(
        access_token=token,
        user_id=str(user.id),
        callsign=user.callsign,
        level=user.current_level,
        is_licensed=user.is_licensed,
    )
