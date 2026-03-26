"""
app/models/intelligence_report.py — D026 Reporte de Inteligencia

Tabla que almacena el feedback in-app de los Alpha Testers.
Tipos: BUG | UX_UI | TACTICAL_IDEA
Severidad: LOW | HIGH | CRITICAL
Estado: OPEN | IN_PROGRESS | RESOLVED
"""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class IntelligenceReport(Base):
    __tablename__ = "intelligence_reports"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Tipo de reporte
    type: Mapped[str] = mapped_column(
        String(20), nullable=False
    )  # BUG | UX_UI | TACTICAL_IDEA

    # Severidad del reporte
    severity: Mapped[str] = mapped_column(
        String(10), nullable=False, default="LOW"
    )  # LOW | HIGH | CRITICAL

    # Descripción del problema / idea
    description: Mapped[str] = mapped_column(Text, nullable=False)

    # Solo para BUGs — pasos para reproducir (opcional)
    steps_to_reproduce: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Estado de resolución (gestionado desde admin)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="OPEN", server_default="OPEN"
    )  # OPEN | IN_PROGRESS | RESOLVED

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
