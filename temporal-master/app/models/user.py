import uuid
from datetime import datetime

from sqlalchemy import DateTime, Integer, String, func
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
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
