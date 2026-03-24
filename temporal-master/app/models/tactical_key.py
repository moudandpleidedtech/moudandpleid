"""
tactical_key.py — Modelo de Llaves de Override Táctico (Prompt 66)

Permite a beta testers e invitados especiales bypasear el muro de pago
y obtener la Licencia de Fundador (is_paid=True) gratuitamente.

Ciclo de vida:
  1. Admin crea una llave con code_string + max_uses (ej. "BETA-QA-2026", max_uses=50).
  2. Operador ingresa el código en PaywallModal → POST /api/v1/checkout/redeem.
  3. El endpoint valida, incrementa current_uses, y activa is_paid en el usuario.
  4. Cuando current_uses >= max_uses la llave queda agotada (el endpoint devuelve 400).
"""

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class TacticalAccessKey(Base):
    __tablename__ = "tactical_access_keys"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    # El código que el operador introduce (ej. "BETA-QA-2026", "PROMO-LATAM-50")
    code_string: Mapped[str] = mapped_column(
        String(80), unique=True, nullable=False, index=True
    )
    # Límite de activaciones. 0 = sin límite (útil solo para admin)
    max_uses: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    # Activaciones consumidas hasta ahora
    current_uses: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
    # Si es False, el código no acepta más activaciones aunque no esté agotado
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")
    # Operador que reclamó este código — FK a users(id), NULL si no fue reclamado aún
    claimed_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        default=None,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
