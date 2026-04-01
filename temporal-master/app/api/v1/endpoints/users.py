import uuid

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import require_user
from app.models.user import User

router = APIRouter()


class LoginRequest(BaseModel):
    callsign: str


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
    model_config = ConfigDict(from_attributes=True)


@router.post(
    "/users/login",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
    summary="Crear o recuperar usuario por nombre",
)
async def login_or_create(
    payload: LoginRequest,
    db: AsyncSession = Depends(get_db),
) -> UserOut:
    result = await db.execute(select(User).where(User.callsign == payload.callsign))
    user = result.scalar_one_or_none()

    if user is None:
        user = User(
            callsign=payload.callsign,
            email=f"{payload.callsign.lower()}@quest.local",
            password_hash=str(uuid.uuid4()),
        )
        db.add(user)
        await db.flush()

    return user


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
