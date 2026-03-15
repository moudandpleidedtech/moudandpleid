"""
Motor de Evaluación de Aprendizaje (Prompt 13).

Calcula y actualiza el puntaje de maestría por concepto cuando el usuario
completa un nivel por primera vez, usando la fórmula de esfuerzo cognitivo.
"""
import json
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.concept_mastery import ConceptMastery

# ── Umbrales ─────────────────────────────────────────────────────────────────

REINFORCEMENT_THRESHOLD = 40.0  # debajo de este score → needs_reinforcement


def _mastery_delta(attempts: int, hints_used: int) -> float:
    """
    Puntos a sumar al concepto según esfuerzo cognitivo:
      < 3 intentos, 0 pistas  → +15  (maestría alta)
      < 3 intentos, con pistas → +10
      3-5 intentos, 0 pistas  → +5
      3-5 intentos, con pistas → +3
      > 5 intentos             → +2  (aprendizaje con dificultad)
    """
    if attempts <= 2:
        return 15.0 if hints_used == 0 else 10.0
    elif attempts <= 5:
        return 5.0 if hints_used == 0 else 3.0
    return 2.0


async def update_mastery_on_completion(
    db: AsyncSession,
    user_id: uuid.UUID,
    concepts_taught_json: str,
    attempts: int,
    hints_used: int,
) -> list[ConceptMastery]:
    """
    Actualiza ConceptMastery para cada concepto enseñado en el nivel completado.
    Retorna la lista de registros actualizados (útil para incluir en la respuesta).
    """
    concepts: list[str] = json.loads(concepts_taught_json) if concepts_taught_json else []
    if not concepts:
        return []

    delta = _mastery_delta(attempts, hints_used)
    updated: list[ConceptMastery] = []

    for concept in concepts:
        result = await db.execute(
            select(ConceptMastery).where(
                ConceptMastery.user_id == user_id,
                ConceptMastery.concept_name == concept,
            )
        )
        record = result.scalar_one_or_none()

        if record is None:
            record = ConceptMastery(user_id=user_id, concept_name=concept, mastery_score=0.0)
            db.add(record)

        record.mastery_score = min(100.0, record.mastery_score + delta)
        record.needs_reinforcement = record.mastery_score < REINFORCEMENT_THRESHOLD
        updated.append(record)

    await db.flush()
    return updated


async def get_user_mastery(
    db: AsyncSession,
    user_id: uuid.UUID,
) -> list[ConceptMastery]:
    """Retorna todos los registros de maestría del usuario, ordenados por concepto."""
    result = await db.execute(
        select(ConceptMastery)
        .where(ConceptMastery.user_id == user_id)
        .order_by(ConceptMastery.concept_name)
    )
    return list(result.scalars().all())


async def get_reinforcement_concepts(
    db: AsyncSession,
    user_id: uuid.UUID,
) -> list[str]:
    """Retorna los nombres de conceptos que necesitan refuerzo (score < 40)."""
    result = await db.execute(
        select(ConceptMastery.concept_name)
        .where(
            ConceptMastery.user_id == user_id,
            ConceptMastery.needs_reinforcement.is_(True),
        )
        .order_by(ConceptMastery.mastery_score)
    )
    return [row[0] for row in result.all()]
