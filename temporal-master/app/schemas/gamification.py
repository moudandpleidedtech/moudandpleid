import uuid

from pydantic import BaseModel, Field


class ChallengeAttemptRequest(BaseModel):
    user_id: uuid.UUID
    challenge_id: uuid.UUID
    is_success: bool
    execution_time_ms: int = Field(..., ge=0)


class ChallengeAttemptResult(BaseModel):
    user_id: uuid.UUID
    challenge_id: uuid.UUID
    is_success: bool
    attempts: int
    xp_earned: int
    efficiency_bonus_applied: bool
    already_completed: bool
    level_up: bool
    new_level: int
    new_total_xp: int
