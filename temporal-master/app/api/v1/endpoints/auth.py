"""
app/api/v1/endpoints/auth.py — Autenticación de Operadores · DAKI EdTech

POST /api/v1/auth/register  { email, password }
    → crea usuario, devuelve JWT

POST /api/v1/auth/login     { email, password }
    → verifica credenciales, devuelve JWT
"""

import uuid

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, EmailStr, field_validator
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.rate_limit import limiter
from app.core.security import create_user_token, hash_password, verify_password
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])


# ─── Schemas ──────────────────────────────────────────────────────────────────

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres.")
        return v


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    level: int


# ─── Endpoints ────────────────────────────────────────────────────────────────

@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nuevo Operador",
)
@limiter.limit("10/minute")
async def register(
    request: Request,
    payload: RegisterRequest,
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    # Verificar que el email no existe ya
    result = await db.execute(select(User).where(User.email == payload.email))
    if result.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Este email ya está registrado.",
        )

    # Derivar callsign del email (parte antes del @, hasta 46 chars) + sufijo único
    base = payload.email.split("@")[0][:46].lower().replace(".", "_")
    callsign = f"{base}_{str(uuid.uuid4())[:3]}"

    user = User(
        callsign=callsign,
        email=payload.email,
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    await db.flush()
    await db.commit()
    await db.refresh(user)

    token = create_user_token(str(user.id), user.current_level)
    return TokenResponse(
        access_token=token,
        user_id=str(user.id),
        level=user.current_level,
    )


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Autenticar Operador con email y contraseña",
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

    token = create_user_token(str(user.id), user.current_level)
    return TokenResponse(
        access_token=token,
        user_id=str(user.id),
        level=user.current_level,
    )
