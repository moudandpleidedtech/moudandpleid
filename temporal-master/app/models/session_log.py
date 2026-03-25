import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class DakiSessionLog(Base):
    """
    Registro de sesión DAKI — memoria persistente inter-sesión.

    Captura lo que el Operador hizo en cada sesión:
    nivel, racha, concepto débil, errores dominantes, briefing de cierre.
    La apertura de la siguiente sesión usa estos datos para personalizar
    el mensaje de bienvenida.
    """

    __tablename__ = "daki_session_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    opened_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    closed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Estado del Operador al abrir la sesión
    operator_level: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    streak_days: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Actividad de la sesión (actualizada al cerrar)
    challenges_attempted: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    challenges_completed: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    hints_requested: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Inteligencia de aprendizaje
    dominant_error_type: Mapped[str | None] = mapped_column(String(120), nullable=True)
    weak_concept: Mapped[str | None] = mapped_column(String(120), nullable=True)

    # Mensajes generados por DAKI
    opening_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    closing_briefing: Mapped[str | None] = mapped_column(Text, nullable=True)
