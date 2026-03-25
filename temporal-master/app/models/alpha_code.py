"""
alpha_code.py — Modelo de Alpha Codes (Operación Vanguardia)
─────────────────────────────────────────────────────────────
Tokens únicos de un solo uso para la Bóveda Alpha.

Propiedades de seguridad:
  - Cada código es válido exactamente UNA vez (is_used + used_by_user_id).
  - El endpoint de redención debe usar SELECT FOR UPDATE para prevenir
    condiciones de carrera (dos requests simultáneos redimiendo el mismo token).
  - El formato "VANG-XXXX-XXXX" es alfanumérico uppercase, generado con
    secrets.token_hex() — no predecible ni enumerable.
  - used_at registra el timestamp exacto de la redención para auditoría.

Ciclo de vida:
  1. Admin genera N códigos vía script → INSERT batch en alpha_codes.
  2. Operador introduce el código → POST /api/v1/alpha/redeem.
  3. El endpoint (atomic): SELECT FOR UPDATE → valida is_used=False
     → SET is_used=True, used_by_user_id, used_at
     → SET users.subscription_status='ACTIVE'.
  4. Código agotado: cualquier reintento devuelve 409 CONFLICT.
"""

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class AlphaCode(Base):
    __tablename__ = "alpha_codes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    # Token único — formato "VANG-8X9P-L2MQ" (14 chars)
    # Generado externamente con generate_alpha_code() en el script de seed
    code: Mapped[str] = mapped_column(
        String(24), unique=True, nullable=False, index=True
    )

    # Estado de uso — FALSE hasta que sea redimido (nunca vuelve a FALSE)
    is_used: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
    )

    # Quién lo redimió — NULL hasta la redención, nunca se puede cambiar
    used_by_user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        default=None,
    )

    # Cuándo fue redimido — NULL hasta la redención
    used_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Cuándo fue generado — para auditoría y expiración futura
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
