import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import Boolean, DateTime, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    # Nombre de operador visible (único, gamertag estilo)
    callsign: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    current_level: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    # Progreso granular por misión: { "alfa": { "completed": true, "attempts": 3 }, ... }
    mission_state: Mapped[dict[str, Any]] = mapped_column(
        JSONB, nullable=False, default=dict, server_default="'{}'::jsonb"
    )
    # Licencia de acceso — False hasta que el pago sea verificado (o código redimido)
    is_licensed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, server_default="false")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    last_login: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # ── Gamificación ───────────────────────────────────────────────────────────
    total_xp: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    streak_days: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    league_tier: Mapped[str] = mapped_column(
        String(30), nullable=False, default="Bronce", server_default="Bronce"
    )
    elo_rating: Mapped[int] = mapped_column(Integer, default=1200, nullable=False, server_default="1200")
    badges_json: Mapped[str] = mapped_column(String, nullable=False, default="[]", server_default="[]")
    daki_level: Mapped[int] = mapped_column(Integer, default=1, nullable=False, server_default="1")
    # ID externo de la pasarela de pagos (Stripe charge_id, PayPal order_id, etc.)
    payment_id: Mapped[str | None] = mapped_column(String(255), nullable=True, default=None)

    # ── Operación Vanguardia — Suscripción Alpha ───────────────────────────────
    # Valores válidos: 'INACTIVE' | 'TRIAL' | 'ACTIVE'
    # INACTIVE: sin acceso premium. TRIAL: período de prueba. ACTIVE: licencia plena.
    subscription_status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="INACTIVE", server_default="INACTIVE"
    )
    # Fecha de expiración del período TRIAL — NULL si no está en trial o si es ACTIVE
    trial_end_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, default=None
    )
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, server_default="false")
    # Rol de acceso: 'USER' (default), 'FOUNDER' (God Mode — bypassa compuertas de catálogo)
    # Alembic: ALTER TABLE users ADD COLUMN role VARCHAR(20) NOT NULL DEFAULT 'USER';
    #          CREATE INDEX ix_users_role ON users(role);
    role: Mapped[str] = mapped_column(
        String(20), nullable=False, default="USER", server_default="USER", index=True
    )
    # Google OAuth — ID único de la cuenta de Google del operador (sub claim)
    google_id: Mapped[str | None] = mapped_column(String(255), nullable=True, default=None, index=True)

    # ── Sistema de Rangos ─────────────────────────────────────────────────────
    points: Mapped[int] = mapped_column(Integer, default=0, nullable=False, server_default="0")
    current_rank: Mapped[str] = mapped_column(
        String(60), nullable=False, default="Trainee", server_default="Trainee"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
