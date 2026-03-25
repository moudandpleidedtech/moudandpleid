"""
incursions.py — Catálogo Público de Incursiones del Nexo (D021)

GET /api/v1/incursions
  → Lista todas las Incursiones ordenadas por `orden`.
  → No requiere autenticación: el catálogo es público (el acceso real
    se verifica en el endpoint de chat / evaluación, no aquí).
  → Responde con status ACTIVE o ENCRYPTED para que el frontend
    pueda renderizar "nodos fantasma" o botones de entrada.
"""

import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.incursion import Incursion

router = APIRouter(prefix="/incursions", tags=["incursions"])


# ─── Schema de respuesta ──────────────────────────────────────────────────────

class IncursionOut(BaseModel):
    id:               uuid.UUID
    slug:             str
    titulo:           str
    descripcion:      str
    status:           str          # "ACTIVE" | "ENCRYPTED"
    system_prompt_id: Optional[str]
    ruta:             Optional[str]
    color_acento:     str
    icono:            str
    orden:            int
    created_at:       datetime

    model_config = {"from_attributes": True}


# ─── Endpoint ─────────────────────────────────────────────────────────────────

@router.get(
    "",
    response_model=list[IncursionOut],
    status_code=status.HTTP_200_OK,
    summary="Catálogo de Incursiones — Mapa de Niebla",
    description=(
        "Devuelve todas las Incursiones del Nexo ordenadas por `orden`. "
        "Las Incursiones con status='ENCRYPTED' son nodos fantasma visibles "
        "pero no accesibles — se muestran en el Hub para hype building. "
        "Las Incursiones con status='ACTIVE' tienen botón de entrada habilitado. "
        "No requiere autenticación."
    ),
)
async def list_incursions(
    db: AsyncSession = Depends(get_db),
) -> list[IncursionOut]:
    result = await db.execute(
        select(Incursion).order_by(Incursion.orden.asc())
    )
    rows = result.scalars().all()
    return [IncursionOut.model_validate(r) for r in rows]
