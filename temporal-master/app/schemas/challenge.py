import uuid

from pydantic import BaseModel, Field, ConfigDict

from app.models.challenge import DifficultyTier


class ChallengeBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    description: str
    difficulty_tier: DifficultyTier
    base_xp_reward: int = Field(..., gt=0)
    initial_code: str = ""
    expected_output: str


class ChallengeCreate(ChallengeBase):
    pass


class ChallengeUpdate(BaseModel):
    title: str | None = Field(None, min_length=3, max_length=200)
    description: str | None = None
    difficulty_tier: DifficultyTier | None = None
    base_xp_reward: int | None = Field(None, gt=0)
    initial_code: str | None = None
    expected_output: str | None = None


class ChallengePublic(ChallengeBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
