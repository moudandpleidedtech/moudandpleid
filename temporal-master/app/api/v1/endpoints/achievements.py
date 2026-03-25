"""
GET /api/v1/achievements?user_id=<uuid>
Retorna todos los logros desbloqueados por el usuario + el catálogo completo
con estado locked/unlocked para mostrar la galería en el frontend.
"""
import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.achievement_service import ACHIEVEMENTS, get_user_achievements

router = APIRouter(prefix="/achievements", tags=["achievements"])


@router.get("")
async def list_achievements(
    user_id: uuid.UUID = Query(..., description="UUID del operador"),
    db: AsyncSession = Depends(get_db),
):
    unlocked = await get_user_achievements(db, user_id)
    unlocked_ids = {a["id"] for a in unlocked}

    catalog = [
        {
            **meta,
            "id": aid,
            "unlocked": aid in unlocked_ids,
            "unlocked_at": next((a["unlocked_at"] for a in unlocked if a["id"] == aid), None),
        }
        for aid, meta in ACHIEVEMENTS.items()
    ]

    return {
        "unlocked_count": len(unlocked_ids),
        "total_count": len(ACHIEVEMENTS),
        "achievements": catalog,
    }
