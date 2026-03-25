import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, SmallInteger, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class UserProgress(Base):
    __tablename__ = "user_progress"
    __table_args__ = (
        UniqueConstraint("user_id", "challenge_id", name="uq_user_challenge"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    challenge_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("challenges.id", ondelete="CASCADE"), nullable=False, index=True
    )
    completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    attempts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    # Telemetry fields (Prompt 13)
    hints_used: Mapped[int] = mapped_column(Integer, default=0, nullable=False, server_default="0")
    syntax_errors_total: Mapped[int] = mapped_column(Integer, default=0, nullable=False, server_default="0")

    # ── Árbol de Habilidades — Campos de Correlatividad (D018) ────────────────
    #
    # boss_completed:
    #   Separado de 'completed' porque un Boss Battle puede tener múltiples
    #   intentos. 'completed=True' significa que se intentó y finalizó el flujo.
    #   'boss_completed=True' significa que se GANÓ — condición para desbloquear
    #   la siguiente fase. Un boss puede estar completed=True, boss_completed=False
    #   (se llegó al final pero no se ganó en la ronda requerida).
    #
    # codex_id:
    #   Desnormalizado desde Challenge para queries eficientes de progreso
    #   por Códice sin necesitar un JOIN adicional.
    #   Ej: "¿cuántas misiones completó el usuario en tpm_mastery_v1?"
    #
    # score:
    #   Puntuación 0-100 para incursiones evaluadas cuantitativamente
    #   (Boss Battles con rúbrica, ejercicios de roleplay del TPM Codex).
    #   NULL para niveles Python Core donde solo importa pass/fail.
    #
    # Migración Alembic necesaria:
    #   ALTER TABLE user_progress ADD COLUMN boss_completed BOOLEAN NOT NULL DEFAULT FALSE;
    #   ALTER TABLE user_progress ADD COLUMN codex_id VARCHAR(50);
    #   ALTER TABLE user_progress ADD COLUMN score SMALLINT;
    #   CREATE INDEX ix_up_codex ON user_progress(user_id, codex_id);

    boss_completed: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False, server_default="false"
    )
    codex_id: Mapped[str | None] = mapped_column(
        String(50), nullable=True, index=False
    )
    score: Mapped[int | None] = mapped_column(
        SmallInteger, nullable=True
    )

    user = relationship("User", backref="progress")
    challenge = relationship("Challenge", backref="user_progress")
