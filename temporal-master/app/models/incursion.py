"""
incursion.py — Catálogo de Incursiones del Nexo (D021 — Mapa de Niebla)

Una Incursión es una disciplina de entrenamiento de alto nivel (Códice).
Es la entidad visible en el Hub: el usuario ve todas las Incursiones pero
solo puede entrar a las que están 'ACTIVE'.

Diseñada para escalar sin tocar el frontend:
  ENCRYPTED → ACTIVE  =  cambiar una fila en la BD.
  No se requieren deploys de frontend, migraciones de schema ni cache-busting.

Relación con otras entidades:
  - Challenge.codex_id  → string que referencia el slug de la Incursión.
  - context_router.py   → usa system_prompt_id como alias para resolve_stance().
  - CampaignMap.tsx     → nodos más granulares DENTRO de una Incursión activa.

Migración Alembic necesaria:
  CREATE TABLE incursions (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug             VARCHAR(60)  NOT NULL UNIQUE,
    titulo           VARCHAR(200) NOT NULL,
    descripcion      TEXT         NOT NULL,
    status           VARCHAR(20)  NOT NULL DEFAULT 'ENCRYPTED',
    system_prompt_id VARCHAR(40),
    ruta             VARCHAR(120),
    color_acento     VARCHAR(7)   NOT NULL DEFAULT '#00FF41',
    icono            VARCHAR(10)  NOT NULL DEFAULT '⬡',
    orden            SMALLINT     NOT NULL DEFAULT 99,
    created_at       TIMESTAMPTZ  NOT NULL DEFAULT now()
  );
  CREATE INDEX ix_incursions_status ON incursions(status);
  CREATE INDEX ix_incursions_orden  ON incursions(orden);
"""

from __future__ import annotations

import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Integer, SmallInteger, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


# ─── Status enum ──────────────────────────────────────────────────────────────

class IncursionStatus(str, enum.Enum):
    """
    Estado de publicación de una Incursión.

    ACTIVE    — Contenido disponible. El Operador puede entrar si tiene acceso.
    ENCRYPTED — Visible como "nodo fantasma" (hype building), acceso denegado.

    Para activar una Incursión: UPDATE incursions SET status='ACTIVE' WHERE slug='...';
    No se requiere ningún otro cambio de código o despliegue.
    """
    ACTIVE    = "ACTIVE"
    ENCRYPTED = "ENCRYPTED"


# ─── Modelo ───────────────────────────────────────────────────────────────────

class Incursion(Base):
    """
    Disciplina de entrenamiento de alto nivel visible en el Hub.

    Cada Incursión agrupa uno o más Códices (series de Challenges).
    El campo `slug` es la clave natural: único, inmutable, legible.
    """
    __tablename__ = "incursions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    # ── Identificación ────────────────────────────────────────────────────────
    slug: Mapped[str] = mapped_column(
        String(60), unique=True, nullable=False, index=True
    )
    titulo: Mapped[str] = mapped_column(String(200), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)

    # ── Estado — el único campo que importa para "desencriptar" ──────────────
    #
    # Para pasar de ENCRYPTED a ACTIVE:
    #   UPDATE incursions SET status = 'ACTIVE' WHERE slug = '<slug>';
    # No se requieren más cambios.
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, server_default="ENCRYPTED", index=True
    )

    # ── Integración con el motor de IA ────────────────────────────────────────
    # Alias que context_router.resolve_stance() acepta como incursion_id.
    # Ej: "python" | "sales" | "tpm" | "cybersec"
    # NULL = no tiene motor de chat asociado aún.
    system_prompt_id: Mapped[str | None] = mapped_column(String(40), nullable=True)

    # ── Navegación del frontend ───────────────────────────────────────────────
    # Ruta Next.js a la que navega el botón "INICIAR INCURSIÓN".
    # Ej: "/misiones" | "/codex/tpm" | "/codex/sales"
    # NULL = no navegable aún (ENCRYPTED sin ruta definida).
    ruta: Mapped[str | None] = mapped_column(String(120), nullable=True)

    # ── Presentación visual ───────────────────────────────────────────────────
    color_acento: Mapped[str] = mapped_column(
        String(7), nullable=False, server_default="#00FF41"
    )
    icono: Mapped[str] = mapped_column(
        String(10), nullable=False, server_default="⬡"
    )

    # Orden de visualización en el Hub (menor = más arriba / más prominente)
    orden: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, server_default="99"
    )

    # ── D030 — Progresión entre Incursiones ───────────────────────────────────
    #
    # prerequisite_incursion_slug:
    #   Slug de la Incursión que el Operador debe completar antes de desbloquear
    #   esta. NULL = sin requisito (accesible desde el inicio).
    #   Ej: "python-core" → el Operador debe derrotar al Boss de Python Core
    #       (medalla SYSTEM_KILLER) para desbloquear QA Automation.
    #
    # total_levels:
    #   Cantidad total de misiones/niveles que contiene la Incursión.
    #   Permite mostrar el progreso "X/N completadas" en el Hub sin
    #   necesitar un COUNT(*) dinámico en cada request.
    #   NULL = contenido aún no definido (ENCRYPTED sin fases especificadas).
    #
    # Migración: ADD COLUMN IF NOT EXISTS en database.py (init_db).
    prerequisite_incursion_slug: Mapped[str | None] = mapped_column(
        String(60), nullable=True, index=False
    )
    total_levels: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )

    # ── Auditoría ─────────────────────────────────────────────────────────────
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
