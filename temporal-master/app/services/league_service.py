"""
Servicio de Ligas Competitivas (Prompt 19).

Lógica:
  - Las ligas se calculan por percentil de XP frente al total de usuarios.
  - La actualización es lazy: se ejecuta como máximo una vez por hora.
  - Percentiles (0 = menor XP, 100 = mayor XP):
      ≥ 95 → Arquitecto Supremo
      ≥ 85 → Diamante
      ≥ 60 → Oro
      ≥ 30 → Plata
         < 30 → Bronce
"""

from datetime import datetime, timedelta, timezone

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User

# ─── Constantes ───────────────────────────────────────────────────────────────

LEAGUE_TIERS = ["Bronce", "Plata", "Oro", "Diamante", "Arquitecto Supremo"]

# Intervalo mínimo entre actualizaciones completas de liga
_UPDATE_INTERVAL = timedelta(hours=1)
_last_update: datetime | None = None


# ─── API pública ──────────────────────────────────────────────────────────────

def tier_from_percentile(percentile: float) -> str:
    """Devuelve el nombre de la liga dado un percentil 0–100."""
    if percentile >= 95:
        return "Arquitecto Supremo"
    if percentile >= 85:
        return "Diamante"
    if percentile >= 60:
        return "Oro"
    if percentile >= 30:
        return "Plata"
    return "Bronce"


async def maybe_update_leagues(db: AsyncSession) -> None:
    """Actualiza las ligas de todos los usuarios si ha pasado el intervalo."""
    global _last_update
    now = datetime.now(timezone.utc)
    if _last_update and (now - _last_update) < _UPDATE_INTERVAL:
        return
    await _recalculate_all_leagues(db)
    _last_update = now


async def _recalculate_all_leagues(db: AsyncSession) -> None:
    """Recalcula y persiste el league_tier de cada usuario."""
    result = await db.execute(
        select(User.id, User.total_xp).order_by(User.total_xp.asc())
    )
    rows = result.all()
    if not rows:
        return

    n = len(rows)
    for rank_asc, (user_id, _) in enumerate(rows, start=1):
        # percentile: 0 = menor XP, 100 = mayor XP
        percentile = (rank_asc / n) * 100
        tier = tier_from_percentile(percentile)
        await db.execute(
            update(User).where(User.id == user_id).values(league_tier=tier)
        )
    # La sesión se commitea en get_db al salir del endpoint
