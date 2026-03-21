"""
progression.py — Guardián del Nexo

Lógica canónica de desbloqueo de niveles para DAKI EdTech.

Reglas:
  1. El primer nivel del Sector 1 siempre está desbloqueado.
  2. Dentro de un sector, el nivel N se desbloquea cuando N-1 está completado.
  3. El primer nivel del Sector N (N > 1) se desbloquea cuando el nivel
     is_project=True del Sector N-1 está completado.
  4. Challenges sin sector_id → siempre "unlocked" (compatibilidad legacy).

Status devuelto:
  "completed"  — el usuario ya completó el nivel
  "unlocked"   — accesible pero no completado
  "locked"     — prerrequisito no cumplido

Si user_id es None se devuelve "unlocked" (modo invitado / sin autenticación).
"""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.challenge import Challenge
from app.models.user_progress import UserProgress


def compute_status(completed: bool, unlocked: bool) -> str:
    """Convierte los flags booleanos al literal de estado."""
    if completed:
        return "completed"
    if unlocked:
        return "unlocked"
    return "locked"


async def resolve_level_status(
    db: AsyncSession,
    user_id: uuid.UUID | None,
    challenge_id: uuid.UUID,
) -> str:
    """
    Devuelve el estado de progresión de UN nivel específico para el usuario.

    Carga todos los challenges con sector en un único SELECT y recorre la
    cadena de desbloqueo en Python — O(n) por llamada, sin N+1 queries.

    Usado principalmente por POST /evaluate para bloquear intentos en
    niveles no accesibles.
    """
    if user_id is None:
        return "unlocked"  # Sin usuario → sin restricciones

    # ── 1. Todos los challenges con sector (orden global) ─────────────────────
    result = await db.execute(
        select(Challenge)
        .where(Challenge.sector_id.isnot(None))
        .order_by(Challenge.sector_id, Challenge.level_order)
    )
    all_challenges: list[Challenge] = list(result.scalars().all())

    # Challenge sin sector → legacy, siempre accesible
    target_has_sector = any(ch.id == challenge_id for ch in all_challenges)
    if not target_has_sector:
        return "unlocked"

    # ── 2. Progreso del usuario ───────────────────────────────────────────────
    prog_result = await db.execute(
        select(UserProgress).where(UserProgress.user_id == user_id)
    )
    progress_map: dict[uuid.UUID, bool] = {
        p.challenge_id: p.completed for p in prog_result.scalars().all()
    }

    # ── 3. Pre-calcula qué proyecto de cada sector fue completado ─────────────
    #       (regla de frontera entre sectores)
    sector_project_done: dict[int, bool] = {}
    for ch in all_challenges:
        if ch.is_project:
            sector_project_done[ch.sector_id] = progress_map.get(ch.id, False)

    # ── 4. Recorre la cadena calculando unlocked para cada nivel ──────────────
    prev_completed = True   # El primer nivel siempre está accesible
    current_sector: int | None = None

    for ch in all_challenges:
        # Al cruzar la frontera de sector aplicamos la regla del proyecto previo
        if ch.sector_id != current_sector:
            if current_sector is not None and ch.sector_id > 1:
                prev_sector = ch.sector_id - 1
                prev_completed = sector_project_done.get(prev_sector, False)
            current_sector = ch.sector_id

        completed = progress_map.get(ch.id, False)

        if ch.id == challenge_id:
            return compute_status(completed, unlocked=prev_completed)

        prev_completed = completed

    # No debería llegar aquí dado el target_has_sector check previo
    return "unlocked"


async def bulk_resolve_sector(
    db: AsyncSession,
    user_id: uuid.UUID | None,
    sector_id: int,
    challenges: list[Challenge],
    progress_map: dict[uuid.UUID, "UserProgress"],
) -> list[str]:
    """
    Calcula el status de todos los niveles de UN sector en bulk.

    Recibe los challenges del sector YA cargados y su progress_map para
    evitar queries extra. Devuelve una lista de status en el mismo orden
    que `challenges`.

    Usado por GET /levels/sector/{id}.
    """
    if user_id is None:
        return [
            compute_status(
                completed=(progress_map.get(ch.id).completed if progress_map.get(ch.id) else False),
                unlocked=True,
            )
            for ch in challenges
        ]

    # Determina si el primer nivel del sector está desbloqueado
    first_unlocked = True
    if sector_id > 1:
        # Busca el proyecto del sector anterior en los challenges del progress_map
        prev_project_result = await db.execute(
            select(Challenge)
            .where(Challenge.sector_id == sector_id - 1, Challenge.is_project == True)  # noqa: E712
            .order_by(Challenge.level_order.desc())
            .limit(1)
        )
        prev_project = prev_project_result.scalar_one_or_none()
        if prev_project:
            prog = progress_map.get(prev_project.id)
            first_unlocked = prog.completed if prog else False

    statuses: list[str] = []
    prev_completed = first_unlocked

    for ch in challenges:
        prog = progress_map.get(ch.id)
        completed = prog.completed if prog else False
        statuses.append(compute_status(completed, unlocked=prev_completed))
        prev_completed = completed

    return statuses
