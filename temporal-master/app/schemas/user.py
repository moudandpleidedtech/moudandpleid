import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    username: str | None = Field(None, min_length=3, max_length=50)
    email: EmailStr | None = None


class UserPublic(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    total_xp: int
    current_level: int
    streak_days: int
    created_at: datetime


class UserInDB(UserPublic):
    hashed_password: str
