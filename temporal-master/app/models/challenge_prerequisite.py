"""
challenge_prerequisite.py — Tabla de Correlatividades Multi-Prerrequisito (D018)

Expresa relaciones N:M entre Incursiones: "para entrar a X, necesitas
haber completado Y1, Y2, Y3..."

CUÁNDO USAR ESTA TABLA vs. Challenge.prerequisite_challenge_id:
  - prerequisite_challenge_id (FK simple en Challenge):
      Cadena lineal: L02 requiere L01, L03 requiere L02...
      Cubre el 95% de los casos. Preferir este.

  - challenge_prerequisites (esta tabla):
      Casos donde una Incursión necesita MÚLTIPLES prerrequisitos que
      no forman una cadena lineal. Ejemplo:
        - El Boss Final del Códice requiere completar los 3 bosses anteriores.
        - Una Incursión opcional se desbloquea al completar 2 módulos
          distintos simultáneamente.

Migración Alembic necesaria:
  CREATE TABLE challenge_prerequisites (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    challenge_id UUID NOT NULL REFERENCES challenges(id) ON DELETE CASCADE,
    required_challenge_id UUID NOT NULL REFERENCES challenges(id) ON DELETE CASCADE,
    CONSTRAINT uq_challenge_prereq UNIQUE (challenge_id, required_challenge_id)
  );
  CREATE INDEX ix_cp_challenge_id ON challenge_prerequisites(challenge_id);
"""

import uuid

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ChallengePrerequisite(Base):
    """
    Fila = "challenge_id NO se puede intentar hasta que required_challenge_id
    esté completado por el usuario."

    La semántica de 'completado' depende del tipo del prerrequisito:
      - Si required_challenge.is_phase_boss = True  → necesita boss_completed = True
      - Si required_challenge.is_phase_boss = False → necesita completed = True
    Esta regla la aplica check_incursion_access en access.py, NO esta tabla.
    """

    __tablename__ = "challenge_prerequisites"
    __table_args__ = (
        UniqueConstraint(
            "challenge_id",
            "required_challenge_id",
            name="uq_challenge_prereq",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    # La incursión que tiene el prerrequisito (la que se quiere desbloquear)
    challenge_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("challenges.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # La incursión que debe estar completada primero
    required_challenge_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("challenges.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Relaciones (lazy para no impactar queries que no las necesitan)
    challenge = relationship(
        "Challenge",
        foreign_keys=[challenge_id],
        backref="multi_prerequisites",
    )
    required_challenge = relationship(
        "Challenge",
        foreign_keys=[required_challenge_id],
    )
