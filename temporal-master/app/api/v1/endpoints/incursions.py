"""
incursions.py — Catálogo de Incursiones del Nexo (D021 + D030)

GET /api/v1/incursions?user_id=<uuid>
  → Lista todas las Incursiones ordenadas por `orden`.
  → Si se provee `user_id`, calcula `is_unlocked` por incursión:
      - Sin prerequisito           → siempre desbloqueada.
      - Con prerequisito python-core → desbloqueada si el Operador tiene
        la medalla SYSTEM_KILLER (Boss final de Python Core derrotado).
      - FOUNDER                    → bypassa todas las compuertas.
  → Sin `user_id`: `is_unlocked` refleja solo si no hay prerequisito.
  → No requiere autenticación: el catálogo es público.
    El acceso real se verifica en evaluación / chat, no aquí.
"""

import json
import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.incursion import Incursion
from app.models.user import User

router = APIRouter(prefix="/incursions", tags=["incursions"])


# ─── Schema de respuesta ──────────────────────────────────────────────────────

class IncursionOut(BaseModel):
    id:                          uuid.UUID
    slug:                        str
    titulo:                      str
    descripcion:                 str
    status:                      str          # "ACTIVE" | "ENCRYPTED"
    system_prompt_id:            Optional[str]
    ruta:                        Optional[str]
    color_acento:                str
    icono:                       str
    orden:                       int
    created_at:                  datetime
    # D030 — Progresión entre Incursiones
    prerequisite_incursion_slug: Optional[str] = None
    total_levels:                Optional[int] = None
    is_unlocked:                 bool = True   # calculado por el endpoint

    model_config = {"from_attributes": True}


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _has_badge(user: User, badge: str) -> bool:
    """Devuelve True si el usuario tiene la medalla `badge` en badges_json."""
    try:
        badges: list[str] = json.loads(user.badges_json or "[]")
    except (ValueError, TypeError):
        badges = []
    return badge in badges


def _compute_is_unlocked(incursion: Incursion, user: Optional[User]) -> bool:
    """
    Determina si el Operador `user` tiene acceso a la `incursion`.

    Reglas (en orden de prioridad):
      1. Sin prerequisito → siempre desbloqueada.
      2. FOUNDER           → bypassa toda compuerta.
      3. prerequisite_incursion_slug == "python-core"
           → desbloqueada si user tiene medalla SYSTEM_KILLER
             (Boss ∞ LOOPER derrotado).
      4. Prerequisito desconocido / sin usuario → bloqueada por defecto.
    """
    if incursion.prerequisite_incursion_slug is None:
        return True

    if user is None:
        return False

    if getattr(user, "role", "USER") == "FOUNDER":
        return True

    if incursion.prerequisite_incursion_slug == "python-core":
        return _has_badge(user, "SYSTEM_KILLER")

    # Prerequisito definido pero sin lógica de desbloqueo implementada
    return False


# ─── Endpoint ─────────────────────────────────────────────────────────────────

@router.get(
    "",
    response_model=list[IncursionOut],
    status_code=status.HTTP_200_OK,
    summary="Catálogo de Incursiones — Mapa de Niebla (D021 + D030)",
    description=(
        "Devuelve todas las Incursiones del Nexo ordenadas por `orden`. "
        "Con `user_id` calcula `is_unlocked` según progreso del Operador. "
        "SYSTEM_KILLER (Boss Python Core) desbloquea QA Automation. "
        "FOUNDER bypassa todas las compuertas."
    ),
)
async def list_incursions(
    user_id: Optional[uuid.UUID] = Query(None, description="UUID del Operador para calcular is_unlocked"),
    db: AsyncSession = Depends(get_db),
) -> list[IncursionOut]:
    # Cargar todas las incursiones ordenadas
    result = await db.execute(
        select(Incursion).order_by(Incursion.orden.asc())
    )
    rows = result.scalars().all()

    # Cargar el usuario si se proveyó user_id
    user: Optional[User] = None
    if user_id is not None:
        user = await db.get(User, user_id)

    # Construir respuesta con is_unlocked calculado
    out: list[IncursionOut] = []
    for inc in rows:
        data = IncursionOut.model_validate(inc)
        data.is_unlocked = _compute_is_unlocked(inc, user)
        out.append(data)

    return out
