"""
Modelo de Duelo PvP (Prompt 20).

Ciclo de vida:
  active          → challenger solucionando
  awaiting_defender → challenger sometió, esperando al defensor
  completed       → ambos sometieron, ganador determinado
  expired         → defensor no respondió (24h)
"""
import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Duel(Base):
    __tablename__ = "duels"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    challenger_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    defender_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    challenge_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("challenges.id", ondelete="CASCADE"), nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(30), nullable=False, default="active", server_default="active"
    )
    winner_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    # Challenger submission
    challenger_code: Mapped[str | None] = mapped_column(Text, nullable=True)
    challenger_time_ms: Mapped[float | None] = mapped_column(Float, nullable=True)
    challenger_correct: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    # Defender submission
    defender_code: Mapped[str | None] = mapped_column(Text, nullable=True)
    defender_time_ms: Mapped[float | None] = mapped_column(Float, nullable=True)
    defender_correct: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    # Elo transfer on completion
    elo_delta: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    challenger = relationship("User", foreign_keys=[challenger_id])
    defender = relationship("User", foreign_keys=[defender_id])
    challenge_obj = relationship("Challenge", foreign_keys=[challenge_id])
