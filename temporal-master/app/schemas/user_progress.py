import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserProgressBase(BaseModel):
    user_id: uuid.UUID
    challenge_id: uuid.UUID


class UserProgressCreate(UserProgressBase):
    pass


class UserProgressUpdate(BaseModel):
    completed: bool | None = None
    attempts: int | None = None
    completed_at: datetime | None = None


class UserProgressPublic(UserProgressBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    completed: bool
    attempts: int
    completed_at: datetime | None
