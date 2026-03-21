import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    total_xp: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    current_level: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    streak_days: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    # Liga competitiva (Prompt 19)
    league_tier: Mapped[str] = mapped_column(
        String(30), nullable=False, default="Bronce", server_default="Bronce"
    )
    # Sistema PvP Elo (Prompt 20)
    elo_rating: Mapped[int] = mapped_column(Integer, default=1200, nullable=False, server_default="1200")
    # Medallas de logro — JSON array, ej: ["SYSTEM_KILLER"]
    badges_json: Mapped[str] = mapped_column(String, nullable=False, default="[]", server_default="[]")
    # Nivel evolutivo de DAKI (1=Robótico, 2=Amistoso, 3=Compañero)
    daki_level: Mapped[int] = mapped_column(Integer, default=1, nullable=False, server_default="1")
    # Licencia de acceso — False hasta que el pago sea verificado
    is_paid: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, server_default="false")
    # ID externo de la pasarela de pagos (Stripe charge_id, PayPal order_id, etc.)
    payment_id: Mapped[str | None] = mapped_column(String(255), nullable=True, default=None)
    # Rol administrativo — solo el CEO/admin tiene acceso al dashboard
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, server_default="false")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
