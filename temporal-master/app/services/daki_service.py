"""
DAKI State Machine — calcula y persiste el nivel evolutivo de DAKI
basado en los sectores completados por el usuario.

Niveles:
  1 — ROBÓTICO  (0–1 sectores completados)
  2 — AMISTOSO  (2–3 sectores completados)
  3 — COMPAÑERO (4+ sectores completados)
"""

import uuid
from dataclasses import dataclass

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.challenge import Challenge
from app.models.user import User
from app.models.user_progress import UserProgress


# ─── Definición de niveles ────────────────────────────────────────────────────

@dataclass(frozen=True)
class _DakiLevelDef:
    level: int
    mood: str
    label: str
    description: str
    min_sectors: int   # sectores completos necesarios para alcanzar este nivel
    next_threshold: int | None  # sectores para el siguiente nivel (None = máximo)


_DAKI_LEVELS: list[_DakiLevelDef] = [
    _DakiLevelDef(
        level=1,
        mood="ROBÓTICO",
        label="DAKI v1.0 — Protocolo Básico",
        description=(
            "Sistema de apoyo en modo diagnóstico. "
            "Respuestas estructuradas, sin adaptación emocional. "
            "Operador, sigue el protocolo."
        ),
        min_sectors=0,
        next_threshold=2,
    ),
    _DakiLevelDef(
        level=2,
        mood="AMISTOSO",
        label="DAKI v2.0 — Protocolo Social",
        description=(
            "Patrones de aprendizaje detectados. "
            "DAKI adapta su tono y anticipa los errores más frecuentes del Operador."
        ),
        min_sectors=2,
        next_threshold=4,
    ),
    _DakiLevelDef(
        level=3,
        mood="COMPAÑERO",
        label="DAKI v3.0 — Protocolo Sincronía",
        description=(
            "Sincronía neuronal completa. "
            "DAKI y el Operador operan como una unidad táctica de élite."
        ),
        min_sectors=4,
        next_threshold=None,
    ),
]


# ─── Schema de respuesta (Pydantic-free, dataclass pura) ─────────────────────

@dataclass
class DakiStateResult:
    daki_level: int
    mood: str
    label: str
    description: str
    completed_sectors: int
    next_threshold: int | None   # None si ya está al máximo


# ─── Lógica de cálculo ────────────────────────────────────────────────────────

async def compute_daki_state(
    db: AsyncSession,
    user_id: uuid.UUID,
) -> DakiStateResult:
    """
    Calcula el estado de DAKI contando cuántos sectores completó el usuario.
    Un sector está completo cuando TODOS sus niveles tienen completed=True.
    """
    completed_sectors = await _count_completed_sectors(db, user_id)
    level_def = _resolve_level(completed_sectors)

    return DakiStateResult(
        daki_level=level_def.level,
        mood=level_def.mood,
        label=level_def.label,
        description=level_def.description,
        completed_sectors=completed_sectors,
        next_threshold=level_def.next_threshold,
    )


async def refresh_daki_level(
    db: AsyncSession,
    user_id: uuid.UUID,
) -> int:
    """
    Calcula el daki_level y lo persiste en users.daki_level.
    Retorna el nuevo nivel. Falla silenciosamente si el user no existe.
    """
    try:
        state = await compute_daki_state(db, user_id)
        user = await db.get(User, user_id)
        if user and user.daki_level != state.daki_level:
            user.daki_level = state.daki_level
            await db.flush()
        return state.daki_level
    except Exception:
        return 1


# ─── Helpers privados ─────────────────────────────────────────────────────────

def _resolve_level(completed_sectors: int) -> _DakiLevelDef:
    """Retorna la definición de nivel más alta alcanzada."""
    resolved = _DAKI_LEVELS[0]
    for level_def in _DAKI_LEVELS:
        if completed_sectors >= level_def.min_sectors:
            resolved = level_def
    return resolved


async def _count_completed_sectors(
    db: AsyncSession,
    user_id: uuid.UUID,
) -> int:
    """
    Cuenta los sectores donde el usuario completó TODOS los niveles.
    Un sector sin niveles no cuenta como completado.
    """
    # Obtiene todos los sector_id distintos con niveles reales
    sector_ids_result = await db.execute(
        select(Challenge.sector_id)
        .where(Challenge.sector_id.isnot(None))
        .distinct()
    )
    sector_ids: list[int] = [row[0] for row in sector_ids_result.all()]

    if not sector_ids:
        return 0

    completed_count = 0
    for sid in sector_ids:
        # Total de niveles en el sector
        total_result = await db.execute(
            select(func.count()).where(Challenge.sector_id == sid)
        )
        total: int = total_result.scalar_one()
        if total == 0:
            continue

        # Completados por este usuario en este sector
        done_result = await db.execute(
            select(func.count())
            .select_from(Challenge)
            .join(
                UserProgress,
                (UserProgress.challenge_id == Challenge.id)
                & (UserProgress.user_id == user_id)
                & (UserProgress.completed == True),  # noqa: E712
            )
            .where(Challenge.sector_id == sid)
        )
        done: int = done_result.scalar_one()

        if done >= total:
            completed_count += 1

    return completed_count
