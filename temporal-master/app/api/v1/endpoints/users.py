import json
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import require_user
from app.models.user import User
from app.models.user_progress import UserProgress

router = APIRouter()


class UserOut(BaseModel):
    id: uuid.UUID
    callsign: str
    email: str
    total_xp: int
    current_level: int
    streak_days: int
    is_licensed: bool
    points: int = 0
    current_rank: str = "Trainee"
    subscription_status: str = "INACTIVE"
    trial_end_date: str | None = None
    role: str = "USER"
    league_tier: str = "Bronce"
    model_config = ConfigDict(from_attributes=True)


@router.post(
    "/users/login",
    status_code=status.HTTP_410_GONE,
    summary="[DEPRECATED] Endpoint legacy deshabilitado",
    include_in_schema=False,   # oculto del OpenAPI/Swagger
)
async def login_or_create_deprecated() -> None:
    """
    Endpoint legacy eliminado por razones de seguridad.
    Permite crear cuentas sin contraseña — reemplazado por POST /api/v1/auth/register.
    """
    raise HTTPException(
        status_code=status.HTTP_410_GONE,
        detail="Endpoint deshabilitado. Usa POST /api/v1/auth/register.",
    )


@router.get(
    "/user/me",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
    summary="Perfil del Operador autenticado",
)
async def get_my_profile(
    current_user: User = Depends(require_user),
) -> UserOut:
    return current_user


# ─── GET /api/v1/users/profile/{callsign} — Perfil público ──────────────────

class PublicProfileOut(BaseModel):
    callsign: str
    current_level: int
    total_xp: int
    streak_days: int
    league_tier: str
    current_rank: str
    completed_challenges: int
    badges: list[str]


@router.get(
    "/users/profile/{callsign}",
    response_model=PublicProfileOut,
    status_code=status.HTTP_200_OK,
    summary="Perfil público del Operador — sin autenticación",
)
async def get_public_profile(
    callsign: str,
    db: AsyncSession = Depends(get_db),
) -> PublicProfileOut:
    """
    Devuelve datos públicos de un Operador por su callsign.
    No requiere autenticación. Usado por la página /p/[callsign].
    """
    result = await db.execute(select(User).where(User.callsign == callsign))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Operador no encontrado.")

    count_result = await db.execute(
        select(func.count()).select_from(UserProgress).where(
            UserProgress.user_id == user.id,
            UserProgress.completed.is_(True),
        )
    )
    completed_count = count_result.scalar_one() or 0

    try:
        badges = json.loads(user.badges_json or "[]")
    except Exception:
        badges = []

    return PublicProfileOut(
        callsign=user.callsign,
        current_level=user.current_level,
        total_xp=user.total_xp,
        streak_days=user.streak_days,
        league_tier=user.league_tier or "Bronce",
        current_rank=user.current_rank or "Trainee",
        completed_challenges=completed_count,
        badges=badges,
    )
