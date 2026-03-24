"""
Endpoint de Clasificación Global (Prompt 19).

GET /api/v1/leaderboard?user_id=<uuid>

Devuelve:
  - top50: primeros 50 jugadores ordenados por total_xp desc
  - user_rank: posición del usuario actual + XP necesaria para superar al siguiente
"""

import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.user import User
from app.models.user_progress import UserProgress
from app.services.league_service import maybe_update_leagues

router = APIRouter()


# ─── Schemas ──────────────────────────────────────────────────────────────────

class LeaderboardEntry(BaseModel):
    rank: int
    user_id: uuid.UUID
    callsign: str
    total_xp: int
    current_level: int
    streak_days: int
    league_tier: str
    completed_challenges: int


class UserRankInfo(BaseModel):
    rank: int
    total_xp: int
    league_tier: str
    xp_to_next: Optional[int] = None
    next_callsign: Optional[str] = None


class LeaderboardResponse(BaseModel):
    top50: list[LeaderboardEntry]
    user_rank: Optional[UserRankInfo] = None
    total_players: int


# ─── Endpoint ─────────────────────────────────────────────────────────────────

@router.get(
    "/leaderboard",
    response_model=LeaderboardResponse,
    summary="Tabla de clasificación global Top 50",
)
async def get_leaderboard(
    user_id: Optional[uuid.UUID] = Query(None),
    db: AsyncSession = Depends(get_db),
) -> LeaderboardResponse:
    # Actualiza las ligas si corresponde (lazy, máx 1 vez/hora)
    await maybe_update_leagues(db)

    # ── Top 50 con conteo de retos completados ────────────────────────────────
    top_result = await db.execute(
        select(
            User,
            func.count(UserProgress.id)
            .filter(UserProgress.completed.is_(True))
            .label("completed_challenges"),
        )
        .outerjoin(UserProgress, UserProgress.user_id == User.id)
        .group_by(User.id)
        .order_by(User.total_xp.desc())
        .limit(50)
    )

    entries: list[LeaderboardEntry] = []
    for rank, row in enumerate(top_result.all(), start=1):
        user_obj, completed = row
        entries.append(
            LeaderboardEntry(
                rank=rank,
                user_id=user_obj.id,
                callsign=user_obj.callsign,
                total_xp=user_obj.total_xp,
                current_level=user_obj.current_level,
                streak_days=user_obj.streak_days,
                league_tier=user_obj.league_tier,
                completed_challenges=completed or 0,
            )
        )

    # ── Total de jugadores ────────────────────────────────────────────────────
    total_result = await db.execute(select(func.count(User.id)))
    total_players: int = total_result.scalar() or 0

    # ── Posición del usuario actual ───────────────────────────────────────────
    user_rank: Optional[UserRankInfo] = None
    if user_id:
        current_user = await db.get(User, user_id)
        if current_user:
            # Cuántos usuarios tienen más XP que yo
            above_result = await db.execute(
                select(func.count(User.id)).where(User.total_xp > current_user.total_xp)
            )
            rank_num: int = (above_result.scalar() or 0) + 1

            # Siguiente usuario a superar (el de menor XP que me supere)
            next_result = await db.execute(
                select(User)
                .where(User.total_xp > current_user.total_xp)
                .order_by(User.total_xp.asc())
                .limit(1)
            )
            next_user = next_result.scalar_one_or_none()

            user_rank = UserRankInfo(
                rank=rank_num,
                total_xp=current_user.total_xp,
                league_tier=current_user.league_tier,
                xp_to_next=(next_user.total_xp - current_user.total_xp) if next_user else None,
                next_callsign=next_user.callsign if next_user else None,
            )

    return LeaderboardResponse(
        top50=entries,
        user_rank=user_rank,
        total_players=total_players,
    )
