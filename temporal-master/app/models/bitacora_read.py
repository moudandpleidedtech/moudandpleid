"""
Modelo: UserBitacoraRead
------------------------
Registra qué archivos del Códice de Infiltración (BitacoraModal)
ha leído cada usuario. Permite persistir el estado de notificación
(ping verde en Hub) en base de datos en lugar de localStorage.

Migration: add_daki_bitacora_tracking
"""
import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, ForeignKey, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class UserBitacoraRead(Base):
    __tablename__ = "user_bitacora_read"
    __table_args__ = (
        UniqueConstraint("user_id", "archivo_id", name="uq_user_archivo"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    # ID del archivo en BitacoraModal (ej. "archivo-01", "archivo-02", ...)
    archivo_id: Mapped[str] = mapped_column(
        String(50), nullable=False
    )
    read_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user = relationship("User", backref="bitacora_reads")
