"""
Endpoint de analíticas de aprendizaje (Prompt 13).
GET /api/v1/analytics/user-profile?user_id=...

Devuelve un mapa de radar con maestría por concepto y flags de refuerzo.
"""
import uuid

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.mastery_service import get_reinforcement_concepts, get_user_mastery

router = APIRouter()


class ConceptRadarPoint(BaseModel):
    concept: str
    mastery_score: float
    needs_reinforcement: bool


class UserProfileResponse(BaseModel):
    user_id: uuid.UUID
    radar_data: list[ConceptRadarPoint]
    reinforcement_needed: list[str]
    total_concepts_tracked: int
    average_mastery: float


@router.get(
    "/analytics/user-profile",
    response_model=UserProfileResponse,
    summary="Mapa de maestría del jugador",
    description=(
        "Retorna los puntajes de maestría por concepto del usuario, "
        "aptos para renderizar un Radar Chart en el frontend. "
        "Los conceptos con mastery_score < 40 tienen needs_reinforcement=true."
    ),
)
async def get_user_profile(
    user_id: uuid.UUID = Query(..., description="UUID del usuario"),
    db: AsyncSession = Depends(get_db),
) -> UserProfileResponse:
    mastery_records = await get_user_mastery(db, user_id)
    reinforcement = await get_reinforcement_concepts(db, user_id)

    radar_data = [
        ConceptRadarPoint(
            concept=r.concept_name,
            mastery_score=round(r.mastery_score, 1),
            needs_reinforcement=r.needs_reinforcement,
        )
        for r in mastery_records
    ]

    total = len(radar_data)
    average = round(sum(p.mastery_score for p in radar_data) / total, 1) if total else 0.0

    return UserProfileResponse(
        user_id=user_id,
        radar_data=radar_data,
        reinforcement_needed=reinforcement,
        total_concepts_tracked=total,
        average_mastery=average,
    )
