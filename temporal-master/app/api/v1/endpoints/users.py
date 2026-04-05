import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict

from app.core.security import require_user
from app.models.user import User

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
