import uuid
from datetime import datetime

from sqlalchemy import DateTime, Integer, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class UserMetric(Base):
    """
    Telemetría de intentos por usuario y desafío.

    Patrón upsert: una fila por (user_id, challenge_id).
    Cada nuevo intento incrementa `attempts` y actualiza `status` y
    `time_spent_ms`.  La columna `last_attempt_at` siempre refleja el
    momento del último envío.
    """

    __tablename__ = "user_metrics"
    __table_args__ = (
        UniqueConstraint("user_id", "challenge_id", name="uq_metrics_user_challenge"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True
    )
    challenge_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True
    )
    attempts: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    # Tiempo acumulado en milisegundos (suma de todos los intentos)
    time_spent_ms: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    # Último estado registrado: "success" | "fail"
    status: Mapped[str] = mapped_column(String(10), nullable=False, default="fail")
    first_attempt_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    last_attempt_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
