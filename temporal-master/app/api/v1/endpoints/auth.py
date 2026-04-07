"""
app/api/v1/endpoints/auth.py — Autenticación de Operadores · DAKI EdTech

POST /api/v1/auth/register  { email, callsign, password, [migrated_level],
                              [migrated_mission_state], [founder_code] }
    → crea usuario con soporte de migración para Alpha/Beta Testers

POST /api/v1/auth/login     { email, password }
    → verifica credenciales, actualiza last_login, devuelve JWT enriquecido

JWT payload:  sub | callsign | level | is_licensed | role | exp

── Flujo de Migración ────────────────────────────────────────────────────────
Los Beta Testers que ya tenían progreso pueden registrarse pasando:
  - migrated_level         → restaura su nivel actual
  - migrated_mission_state → restaura el estado exacto de cada misión
  - founder_code           → si es un código beta/tactical válido,
                             activa is_licensed=True como recompensa Alpha
"""

import re
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from pydantic import BaseModel, EmailStr, Field, field_validator
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.core.rate_limit import limiter
from app.core.security import create_user_token, hash_password, verify_password
from app.models.beta_code import BetaCode
from app.models.tactical_key import TacticalAccessKey
from app.services.email import send_welcome
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])

_CALLSIGN_RE = re.compile(r"^[a-zA-Z0-9_\-]{3,20}$")

# Duración de la cookie de sesión: 7 días
_COOKIE_MAX_AGE = 60 * 60 * 24 * 7


def _set_auth_cookie(response: Response, token: str) -> None:
    """Establece el JWT en una cookie HttpOnly para protección contra XSS."""
    response.set_cookie(
        key="daki_auth",
        value=token,
        httponly=True,
        secure=not settings.DEBUG,   # Secure en producción (HTTPS)
        samesite="lax",              # lax: permite navegación normal, bloquea CSRF cross-site
        max_age=_COOKIE_MAX_AGE,
        path="/",
    )

# ─── Schemas ──────────────────────────────────────────────────────────────────

class RegisterRequest(BaseModel):
    email:    EmailStr
    callsign: str
    password: str

    # ── Campos de migración (opcionales — para Alpha/Beta Testers) ─────────────
    migrated_level:         int | None            = Field(None, ge=1, le=100)
    migrated_mission_state: dict[str, Any] | None = None
    # Código de fundador: activa is_licensed si pertenece a un código beta activo
    founder_code:           str | None            = None

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
    access_token:        str
    token_type:          str  = "bearer"
    user_id:             str
    callsign:            str
    level:               int
    is_licensed:         bool
    role:                str  = "USER"
    # Indica si el founder_code fue válido y activó la licencia
    founder_code_applied: bool = False


# ─── Helper: validar founder_code ─────────────────────────────────────────────

async def _resolve_founder_code(
    code: str,
    db: AsyncSession,
) -> tuple[bool, TacticalAccessKey | None]:
    """
    Valida el founder_code contra beta_codes y tactical_access_keys.

    Retorna (is_licensed, tak_to_consume):
      - is_licensed=True  si el código es válido en cualquiera de las dos tablas
      - tak_to_consume    es el TacticalAccessKey si fue ahí donde matchó
                          (para incrementar current_uses y registrar claimed_by)
    """
    code_upper = code.upper().strip()

    # ── 1. Verificar en beta_codes (los códigos de acceso de la fase beta) ──────
    bc_result = await db.execute(
        select(BetaCode).where(
            BetaCode.code == code_upper,
            BetaCode.is_active == True,          # noqa: E712
        )
    )
    bc = bc_result.scalar_one_or_none()
    if bc is not None and bc.current_uses < bc.max_uses:
        return True, None   # válido en beta_codes; no consume TAK

    # ── 2. Verificar en tactical_access_keys (códigos de licencia de pago) ─────
    tak_result = await db.execute(
        select(TacticalAccessKey)
        .where(
            TacticalAccessKey.code_string == code_upper,
            TacticalAccessKey.is_active   == True,       # noqa: E712
        )
        .with_for_update()   # lock fila para evitar race conditions
    )
    tak = tak_result.scalar_one_or_none()
    if tak is not None and tak.current_uses < tak.max_uses:
        return True, tak     # válido en TAK; caller debe consumir

    return False, None       # código no encontrado o agotado


# ─── Endpoints ────────────────────────────────────────────────────────────────

@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nuevo Operador (con soporte de migración)",
    description=(
        "Crea una cuenta con email + callsign + password. "
        "Si se incluyen `migrated_level` y `migrated_mission_state`, "
        "el progreso del Alpha Tester queda restaurado. "
        "Si se incluye un `founder_code` válido, "
        "is_licensed se activa automáticamente como recompensa."
    ),
)
@limiter.limit("10/minute")
async def register(
    request: Request,
    response: Response,
    payload: RegisterRequest,
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    # ── Unicidad de email y callsign (mensaje unificado para evitar enumeración) ─
    _conflict = HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Credenciales ya en uso. Verifica tu email o callsign.",
    )
    result = await db.execute(select(User).where(User.email == payload.email))
    if result.scalar_one_or_none() is not None:
        raise _conflict

    result = await db.execute(select(User).where(User.callsign == payload.callsign))
    if result.scalar_one_or_none() is not None:
        raise _conflict

    # ── Resolver founder_code (antes de crear usuario para evitar flush parcial)
    founder_code_applied = False
    tak_to_consume: TacticalAccessKey | None = None

    if payload.founder_code:
        founder_code_applied, tak_to_consume = await _resolve_founder_code(
            payload.founder_code, db
        )

    # ── Crear usuario con valores de migración si se proporcionaron ───────────
    user = User(
        email=payload.email,
        callsign=payload.callsign,
        password_hash=hash_password(payload.password),
        current_level=payload.migrated_level         or 1,
        mission_state=payload.migrated_mission_state or {},
        is_licensed=founder_code_applied,
        last_login=datetime.now(timezone.utc),
    )
    db.add(user)
    await db.flush()   # obtiene user.id sin commit para el FK

    # ── Consumir el código táctico si matchó en tactical_access_keys ─────────
    if tak_to_consume is not None:
        tak_to_consume.current_uses += 1
        tak_to_consume.claimed_by    = user.id

    await db.commit()
    await db.refresh(user)

    # ── Email de bienvenida (fire-and-forget) ──────────────────────────────
    import asyncio
    asyncio.create_task(send_welcome(user.email, user.callsign))

    token = create_user_token(
        user_id=str(user.id),
        callsign=user.callsign,
        level=user.current_level,
        is_licensed=user.is_licensed,
        role=user.role,
    )
    _set_auth_cookie(response, token)
    return TokenResponse(
        access_token=token,
        user_id=str(user.id),
        callsign=user.callsign,
        level=user.current_level,
        is_licensed=user.is_licensed,
        role=user.role,
        founder_code_applied=founder_code_applied,
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
    response: Response,
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

    # ── Actualizar streak y last_login ──────────────────────────────────────
    now_utc = datetime.now(timezone.utc)
    if user.last_login:
        delta_days = (now_utc.date() - user.last_login.date()).days
        if delta_days == 1:
            user.streak_days = (user.streak_days or 0) + 1
        elif delta_days > 1:
            user.streak_days = 1
        # delta_days == 0: mismo día — no cambia la racha
    else:
        user.streak_days = 1
    user.last_login = now_utc
    await db.commit()
    await db.refresh(user)

    # ── Logros de racha ──────────────────────────────────────────────────────
    try:
        from app.services.achievement_service import check_and_grant
        await check_and_grant(db, user.id, "login", {"user_streak": user.streak_days})
        await db.commit()
    except Exception:
        pass  # logros no son críticos — no bloquean el login

    token = create_user_token(
        user_id=str(user.id),
        callsign=user.callsign,
        level=user.current_level,
        is_licensed=user.is_licensed,
        role=user.role,
    )
    _set_auth_cookie(response, token)
    return TokenResponse(
        access_token=token,
        user_id=str(user.id),
        callsign=user.callsign,
        level=user.current_level,
        is_licensed=user.is_licensed,
        role=user.role,
    )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT, summary="Cerrar sesión")
async def logout(response: Response) -> None:
    """Elimina la cookie httpOnly de autenticación."""
    response.delete_cookie(
        key="daki_auth", path="/",
        samesite="none" if not settings.DEBUG else "lax",
    )
