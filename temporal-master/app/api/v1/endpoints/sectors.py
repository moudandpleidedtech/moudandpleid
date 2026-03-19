"""
Endpoints de Sectores — GlitchAndGold 100-level architecture.

GET /api/v1/levels/sectors              → lista de sectores disponibles con progreso
GET /api/v1/levels/sector/{sector_id}   → niveles de un sector específico con estado
"""

import json
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.challenge import Challenge
from app.models.user_progress import UserProgress
from app.services.daki_service import compute_daki_state, refresh_daki_level
from app.services.progression import bulk_resolve_sector

router = APIRouter(prefix="/levels", tags=["sectors"])


# ─── Schemas de respuesta ─────────────────────────────────────────────────────

class LevelOut(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    level_order: Optional[int]
    difficulty: Optional[str]
    difficulty_tier: int
    base_xp_reward: int
    telemetry_goal_time: Optional[int]
    is_project: bool
    sector_id: Optional[int]
    phase: Optional[str]
    concepts_taught: list[str]
    challenge_type: str
    lore_briefing: Optional[str]
    pedagogical_objective: Optional[str]
    syntax_hint: Optional[str]
    hints: list[str]
    theory_content: Optional[str]
    initial_code: str
    test_inputs: list[str]
    strict_match: bool
    # Estado del usuario
    completed: bool
    attempts: int
    unlocked: bool
    status: str      # "locked" | "unlocked" | "completed"


class DakiStateOut(BaseModel):
    daki_level: int
    mood: str
    label: str
    description: str
    completed_sectors: int
    next_threshold: Optional[int]


class SectorResponse(BaseModel):
    """Wrapper del endpoint GET /sector/{id}: niveles + estado DAKI del usuario."""
    levels: list["LevelOut"]
    daki_state: Optional[DakiStateOut]   # None si no se pasa user_id


class SectorSummary(BaseModel):
    sector_id: int
    total_levels: int
    completed_levels: int
    has_project: bool
    is_unlocked: bool      # True si el sector anterior fue completado (o es el sector 1)
    is_completed: bool     # True cuando todos los niveles del sector están completados


# ─── Helper ───────────────────────────────────────────────────────────────────

def _build_level(
    challenge: Challenge,
    completed: bool,
    attempts: int,
    unlocked: bool,
    level_status: str = "",
) -> LevelOut:
    return LevelOut(
        id=challenge.id,
        title=challenge.title,
        description=challenge.description,
        level_order=challenge.level_order,
        difficulty=challenge.difficulty,
        difficulty_tier=challenge.difficulty_tier.value,
        base_xp_reward=challenge.base_xp_reward,
        telemetry_goal_time=challenge.telemetry_goal_time,
        is_project=challenge.is_project,
        sector_id=challenge.sector_id,
        phase=challenge.phase,
        concepts_taught=json.loads(challenge.concepts_taught_json) if challenge.concepts_taught_json else [],
        challenge_type=challenge.challenge_type or "python",
        lore_briefing=challenge.lore_briefing,
        pedagogical_objective=challenge.pedagogical_objective,
        syntax_hint=challenge.syntax_hint,
        hints=json.loads(challenge.hints_json) if challenge.hints_json else [],
        theory_content=challenge.theory_content,
        initial_code=challenge.initial_code,
        test_inputs=json.loads(challenge.test_inputs_json),
        strict_match=challenge.strict_match,
        completed=completed,
        attempts=attempts,
        unlocked=unlocked,
        status=level_status or ("completed" if completed else ("unlocked" if unlocked else "locked")),
    )


def _build_progress_map(progresses: list[UserProgress]) -> dict[uuid.UUID, UserProgress]:
    return {p.challenge_id: p for p in progresses}


# ─── Endpoints ────────────────────────────────────────────────────────────────

@router.get(
    "/sector/{sector_id}",
    response_model=SectorResponse,
    summary="Niveles de un sector con estado DAKI",
    description=(
        "Devuelve los niveles del sector + el estado evolutivo de DAKI para el usuario. "
        "El desbloqueo es secuencial dentro del sector. "
        "El primer nivel del sector requiere completar el proyecto del sector anterior. "
        "Devuelve 404 si el sector no existe o no tiene niveles."
    ),
)
async def get_sector_levels(
    sector_id: int,
    user_id: Optional[uuid.UUID] = Query(None, description="UUID del operador para calcular progreso"),
    db: AsyncSession = Depends(get_db),
) -> SectorResponse:
    # Carga los niveles del sector ordenados
    result = await db.execute(
        select(Challenge)
        .where(Challenge.sector_id == sector_id)
        .order_by(Challenge.level_order)
    )
    levels = result.scalars().all()

    if not levels:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El sector {sector_id} no existe o no tiene niveles cargados.",
        )

    # Progreso del usuario
    progress_map: dict[uuid.UUID, UserProgress] = {}
    if user_id:
        prog_result = await db.execute(
            select(UserProgress).where(UserProgress.user_id == user_id)
        )
        progress_map = _build_progress_map(prog_result.scalars().all())

    # Calcula status de progresión para todos los niveles del sector
    statuses = await bulk_resolve_sector(db, user_id, sector_id, list(levels), progress_map)

    out: list[LevelOut] = []
    for level, lvl_status in zip(levels, statuses):
        prog = progress_map.get(level.id)
        completed = prog.completed if prog else False
        attempts = prog.attempts if prog else 0
        out.append(_build_level(
            level,
            completed=completed,
            attempts=attempts,
            unlocked=(lvl_status != "locked"),
            level_status=lvl_status,
        ))

    # Estado de DAKI — calcula y persiste en BD si hay usuario
    daki_state_out: DakiStateOut | None = None
    if user_id:
        state = await compute_daki_state(db, user_id)
        await refresh_daki_level(db, user_id)
        daki_state_out = DakiStateOut(
            daki_level=state.daki_level,
            mood=state.mood,
            label=state.label,
            description=state.description,
            completed_sectors=state.completed_sectors,
            next_threshold=state.next_threshold,
        )

    return SectorResponse(levels=out, daki_state=daki_state_out)


@router.get(
    "/sectors",
    response_model=list[SectorSummary],
    summary="Resumen de todos los sectores",
    description=(
        "Lista los sectores disponibles con su progreso. "
        "Útil para renderizar el Mapa de Sectores en el frontend."
    ),
)
async def list_sectors(
    user_id: Optional[uuid.UUID] = Query(None),
    db: AsyncSession = Depends(get_db),
) -> list[SectorSummary]:
    # Obtiene todos los sector_id distintos que tienen niveles
    sector_ids_result = await db.execute(
        select(Challenge.sector_id)
        .where(Challenge.sector_id.isnot(None))
        .distinct()
        .order_by(Challenge.sector_id)
    )
    sector_ids: list[int] = [row[0] for row in sector_ids_result.all()]

    if not sector_ids:
        return []

    # Todos los niveles con sector
    levels_result = await db.execute(
        select(Challenge).where(Challenge.sector_id.isnot(None)).order_by(
            Challenge.sector_id, Challenge.level_order
        )
    )
    all_levels = levels_result.scalars().all()

    # Progreso del usuario
    progress_map: dict[uuid.UUID, UserProgress] = {}
    if user_id:
        prog_result = await db.execute(
            select(UserProgress).where(UserProgress.user_id == user_id)
        )
        progress_map = _build_progress_map(prog_result.scalars().all())

    # Agrupa niveles por sector
    from collections import defaultdict
    levels_by_sector: dict[int, list[Challenge]] = defaultdict(list)
    for level in all_levels:
        levels_by_sector[level.sector_id].append(level)

    summaries: list[SectorSummary] = []
    prev_sector_completed = True  # Sector 1 siempre desbloqueado

    for sid in sector_ids:
        sector_levels = levels_by_sector[sid]
        completed_count = sum(
            1 for lv in sector_levels
            if (progress_map.get(lv.id) or UserProgress()).completed
        )
        has_project = any(lv.is_project for lv in sector_levels)
        is_completed = completed_count == len(sector_levels)

        summaries.append(SectorSummary(
            sector_id=sid,
            total_levels=len(sector_levels),
            completed_levels=completed_count,
            has_project=has_project,
            is_unlocked=prev_sector_completed,
            is_completed=is_completed,
        ))

        prev_sector_completed = is_completed

    return summaries
