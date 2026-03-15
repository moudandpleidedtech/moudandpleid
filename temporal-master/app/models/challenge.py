import enum
import uuid

from sqlalchemy import Enum, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class DifficultyTier(int, enum.Enum):
    BEGINNER = 1
    INTERMEDIATE = 2
    ADVANCED = 3


class Challenge(Base):
    __tablename__ = "challenges"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    difficulty_tier: Mapped[DifficultyTier] = mapped_column(
        Enum(DifficultyTier, name="difficulty_tier_enum"), nullable=False
    )
    base_xp_reward: Mapped[int] = mapped_column(Integer, nullable=False)
    initial_code: Mapped[str] = mapped_column(Text, nullable=False, default="")
    expected_output: Mapped[str] = mapped_column(Text, nullable=False)
    test_inputs_json: Mapped[str] = mapped_column(Text, nullable=False, server_default="[]")

    # ── Campos de currículo (Prompt 12) ──────────────────────────────────────
    level_order: Mapped[int | None] = mapped_column(Integer, nullable=True)
    phase: Mapped[str | None] = mapped_column(String(20), nullable=True)
    concepts_taught_json: Mapped[str] = mapped_column(Text, nullable=False, server_default="[]")
    grid_map_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    challenge_type: Mapped[str] = mapped_column(String(20), nullable=False, server_default="python")

    # ── Contenido teórico (Prompt 18) ─────────────────────────────────────────
    theory_content: Mapped[str | None] = mapped_column(Text, nullable=True)
