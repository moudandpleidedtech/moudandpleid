"""
pending_activations — Activaciones de Hotmart en espera de registro

Cuando el webhook de Hotmart recibe un PURCHASE_APPROVED para un email
que aún no existe en la base de datos, se guarda un PendingActivation.
Al registrarse, auth.py verifica este registro y activa la licencia automáticamente.
"""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class PendingActivation(Base):
    __tablename__ = "pending_activations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    # Email del comprador (normalizado a minúsculas)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    # ID de transacción de Hotmart para trazabilidad
    transaction_id: Mapped[str] = mapped_column(String(255), nullable=False)
    # Evento que originó la activación (PURCHASE_APPROVED, PURCHASE_COMPLETE)
    event: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
