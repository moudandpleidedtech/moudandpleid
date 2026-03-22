import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class UserCoreMemory(Base):
    """
    Registro de eventos clave del Operador — Módulo de Memoria Evolutiva (Prompt 56).

    event_type values:
        error_frecuente   — Operador falla repetidamente en la misma incursión
        exito_rapido      — Operador resuelve en el primer intento
        tiempo_estancado  — Operador inactivo ≥ 2 minutos en una incursión
        subida_rango      — Operador asciende de rango
    """

    __tablename__ = "user_core_memory"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    challenge_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("challenges.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    # error_frecuente | exito_rapido | tiempo_estancado | subida_rango
    event_type: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    # JSON con detalles del evento (challenge_title, error_type, idle_minutes, etc.)
    context_data: Mapped[str] = mapped_column(Text, nullable=False, default="{}")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user = relationship("User", backref="core_memories")
