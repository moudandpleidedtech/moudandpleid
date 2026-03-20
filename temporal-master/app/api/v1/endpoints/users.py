import uuid

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.user import User

router = APIRouter()


class LoginRequest(BaseModel):
    username: str


class UserOut(BaseModel):
    id: uuid.UUID
    username: str
    total_xp: int
    current_level: int
    streak_days: int
    is_paid: bool
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
    result = await db.execute(select(User).where(User.username == payload.username))
    user = result.scalar_one_or_none()

    if user is None:
        user = User(
            username=payload.username,
            email=f"{payload.username.lower()}@quest.local",
            hashed_password=str(uuid.uuid4()),
        )
        db.add(user)
        await db.flush()

    return user
