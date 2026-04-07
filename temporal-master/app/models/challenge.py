import enum
import uuid

from sqlalchemy import Boolean, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class DifficultyTier(int, enum.Enum):
    BEGINNER = 1
    INTERMEDIATE = 2
    ADVANCED = 3


class Challenge(Base):
    __tablename__ = "challenges"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    difficulty_tier: Mapped[DifficultyTier] = mapped_column(
        Enum(DifficultyTier, name="difficulty_tier_enum"), nullable=False
    )
    base_xp_reward: Mapped[int] = mapped_column(Integer, nullable=False)
    initial_code: Mapped[str] = mapped_column(Text, nullable=False, default="")
    expected_output: Mapped[str] = mapped_column(Text, nullable=False)
    test_inputs_json: Mapped[str] = mapped_column(Text, nullable=False, server_default="[]")

    # ── Campos de currículo (Prompt 12) ──────────────────────────────────────
    level_order: Mapped[int | None] = mapped_column(Integer, nullable=True)
    phase: Mapped[str | None] = mapped_column(String(20), nullable=True)
    concepts_taught_json: Mapped[str] = mapped_column(Text, nullable=False, server_default="[]")
    grid_map_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    challenge_type: Mapped[str] = mapped_column(String(20), nullable=False, server_default="python")

    # ── Contenido teórico (Prompt 18) ─────────────────────────────────────────
    theory_content: Mapped[str | None] = mapped_column(Text, nullable=True)

    # ── Briefing de misión (Prompt B) ─────────────────────────────────────────
    lore_briefing: Mapped[str | None] = mapped_column(Text, nullable=True)
    pedagogical_objective: Mapped[str | None] = mapped_column(Text, nullable=True)
    syntax_hint: Mapped[str | None] = mapped_column(Text, nullable=True)

    # ── Pistas progresivas (array JSON de 3 strings) ──────────────────────────
    hints_json: Mapped[str] = mapped_column(Text, nullable=False, server_default="[]")

    # ── Arquitectura GG 100 niveles ───────────────────────────────────────────
    sector_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    difficulty: Mapped[str | None] = mapped_column(String(10), nullable=True)   # easy | medium | hard | expert
    is_project: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")
    telemetry_goal_time: Mapped[int | None] = mapped_column(Integer, nullable=True)  # segundos

    # ── Motor de evaluación ───────────────────────────────────────────────────
    # strict_match=True  → comparación exacta (solo normaliza CRLF→LF + strip global)
    # strict_match=False → normalización tolerante (colapsa whitespace redundante)
    strict_match: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")

    # ── Freemium — Gancho Narrativo ────────────────────────────────────────────
    # is_free=True  → accesible sin licencia (L0–L10, demo de enganche)
    # is_free=False → requiere is_paid=True en el usuario (default para todos)
    is_free: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")

    # ── Pedagogía avanzada ────────────────────────────────────────────────────────
    #
    # is_ironman:
    #   True en challenges sin asistencia (1 por sector a partir del sector 8).
    #   Cuando True: ENIGMA deshabilitado, error explainer suprimido,
    #   DAKI proactivo silenciado. Completarlo otorga badge "Cicatriz de Ironman".
    #
    # edge_cases_json:
    #   Array JSON de {description: str} — casos extremos que se revelan
    #   en consola post-victoria para entrenar código de producción.
    #   Ej: [{"description": "lista vacía → ¿qué retorna?"}]

    is_ironman: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default="false"
    )
    edge_cases_json: Mapped[str | None] = mapped_column(Text, nullable=True)

    # ── Árbol de Habilidades — Correlatividades (D018) ─────────────────────────
    #
    # codex_id:
    #   Agrupa challenges por Códice. Valores canónicos:
    #   'python_core' | 'sales_mastery_v1' | 'tpm_mastery_v1' | None (legacy)
    #   NULL = challenge del sistema original (Python Core, compatibilidad hacia atrás).
    #
    # prerequisite_challenge_id:
    #   FK self-referencial simple. Expresa: "para entrar aquí, debes haber
    #   completado esta otra incursión primero". Cubre el 95% de los casos
    #   (cadena lineal dentro de un módulo, gate de fase).
    #   Para prerrequisitos múltiples, usar la tabla challenge_prerequisites.
    #
    # is_phase_boss:
    #   True en Boss Battles que actúan como gate de fase.
    #   Cuando una incursión X tiene prerequisite_challenge_id → boss Y,
    #   el check valida UserProgress.boss_completed (no solo .completed).
    #
    # Migración Alembic necesaria:
    #   ALTER TABLE challenges ADD COLUMN codex_id VARCHAR(50);
    #   ALTER TABLE challenges ADD COLUMN prerequisite_challenge_id UUID
    #     REFERENCES challenges(id) ON DELETE SET NULL;
    #   ALTER TABLE challenges ADD COLUMN is_phase_boss BOOLEAN NOT NULL DEFAULT FALSE;
    #   CREATE INDEX ix_challenges_codex_id ON challenges(codex_id);
    #   CREATE INDEX ix_challenges_prereq ON challenges(prerequisite_challenge_id);

    codex_id: Mapped[str | None] = mapped_column(
        String(50), nullable=True, index=True
    )
    prerequisite_challenge_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("challenges.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    is_phase_boss: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default="false"
    )
