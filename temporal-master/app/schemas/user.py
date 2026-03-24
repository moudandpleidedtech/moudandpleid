import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserBase(BaseModel):
    callsign: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    callsign: str | None = Field(None, min_length=3, max_length=50)
    email: EmailStr | None = None


class UserPublic(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    total_xp: int
    current_level: int
    streak_days: int
    is_licensed: bool
    mission_state: dict[str, Any] = {}
    created_at: datetime
    last_login: datetime | None = None


class UserInDB(UserPublic):
    password_hash: str
