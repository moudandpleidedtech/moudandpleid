"""
daki_interception.py — Registro de Intercepciones del Protocolo Memoria Muscular

Una intercepción es un evento donde DAKI detects concept degradation en el
Operador y genera una Micro-Misión de repaso antes de permitir el avance.

Ciclo de vida:
  1. DAKI detecta degradación → se crea un registro (status="pending")
  2. El Operador recibe la Micro-Misión y la completa (status="passed")
     ó la ignora/falla repetidamente (status="expired" al vencer expires_at)
  3. Una vez "passed", el avance está desbloqueado y la intercepción no vuelve
     a activarse para ese concepto hasta que el mastery_score baje de nuevo.

Una sola intercepción activa por usuario a la vez — no se apila el sistema.
"""

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class DakiInterception(Base):
    __tablename__ = "daki_interceptions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    # ── Quién y qué ───────────────────────────────────────────────────────────
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # El concepto débil detectado (ej. "for", "if", "variables")
    concept_name: Mapped[str] = mapped_column(String(100), nullable=False)

    # El challenge que el usuario intentó acceder y fue interceptado
    triggered_on_challenge_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False
    )

    # El sector en el que estaba el usuario cuando fue interceptado
    triggered_on_sector: Mapped[int] = mapped_column(Integer, nullable=False)

    # ── La Micro-Misión ───────────────────────────────────────────────────────
    # JSON con todos los campos de la misión generada:
    # { title, description, lore_briefing, initial_code, expected_output,
    #   hints, difficulty, estimated_lines }
    mision_flash_json: Mapped[str] = mapped_column(Text, nullable=False)

    # Mensaje narrativo de DAKI que acompaña la intercepción
    daki_message: Mapped[str] = mapped_column(Text, nullable=False)

    # ── Estado ────────────────────────────────────────────────────────────────
    # "pending"  → Micro-Misión asignada, aún no completada
    # "passed"   → Operador la completó correctamente
    # "expired"  → Venció el tiempo límite sin completarla
    status: Mapped[str] = mapped_column(
        String(10), nullable=False, default="pending"
    )

    # Intentos sobre la Micro-Misión (para telemetría)
    flash_attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # ── Timestamps ────────────────────────────────────────────────────────────
    triggered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    # La intercepción expira en 24h — pasado ese tiempo se puede ignorar
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
