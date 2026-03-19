"""
GET /api/v1/admin/dashboard  — God Mode: Telemetría agregada por nivel.

Protegido con la variable de entorno ADMIN_SECRET (header X-Admin-Secret).
Sin este header correcto, devuelve 403.

Retorna métricas por challenge_id cruzadas con la tabla challenges para
obtener título, sector, dificultad y level_order.
"""

import json
import os

from fastapi import APIRouter, Depends, Header, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.challenge import Challenge
from app.models.user_metrics import UserMetric

router = APIRouter(prefix="/admin", tags=["admin"])

_ADMIN_SECRET = os.getenv("ADMIN_SECRET", "gg-god-mode-2024")


# ─── Autenticación básica ─────────────────────────────────────────────────────

def _verify_admin(x_admin_secret: str = Header(default="")) -> None:
    if x_admin_secret != _ADMIN_SECRET:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado. Header X-Admin-Secret inválido.",
        )


# ─── Schemas de respuesta ─────────────────────────────────────────────────────

class LevelMetric(BaseModel):
    challenge_id: str
    title: str
    sector_id: int | None
    level_order: int | None
    difficulty: str | None

    # Participación
    total_users: int          # usuarios únicos que intentaron el nivel
    resolved_users: int       # usuarios que llegaron a status="success"
    success_rate: float       # resolved_users / total_users * 100

    # Esfuerzo
    avg_attempts: float       # promedio de intentos por usuario
    avg_time_min: float       # promedio de tiempo (minutos)
    max_attempts: int         # usuario que más intentó

    # Dependencia de DAKI
    daki_dependency: float    # % de usuarios que usaron la pista 3 (hints_used == 3)
    avg_hints: float          # promedio de pistas usadas

    # Top errores
    top_errors: list[str]     # 3 tipos de error más frecuentes

    # Alertas
    friction_alert: bool      # True si avg_attempts > 10
    daki_overload: bool       # True si daki_dependency > 50%


class DashboardStats(BaseModel):
    total_users: int
    total_attempts: int
    global_success_rate: float
    most_played_level: str | None
    hardest_level: str | None     # mayor avg_attempts


class AdminDashboardResponse(BaseModel):
    stats: DashboardStats
    levels: list[LevelMetric]


# ─── Endpoint ─────────────────────────────────────────────────────────────────

@router.get(
    "/dashboard",
    response_model=AdminDashboardResponse,
    summary="God Mode — Telemetría agregada por nivel",
    dependencies=[Depends(_verify_admin)],
)
async def get_admin_dashboard(
    db: AsyncSession = Depends(get_db),
) -> AdminDashboardResponse:
    """
    Agrega user_metrics por challenge_id y los cruza con la tabla challenges.
    Calcula: tasa de éxito, intentos promedio, dependencia de DAKI y top errores.
    """

    # ── 1. Carga todos los registros de user_metrics ──────────────────────────
    metrics_result = await db.execute(select(UserMetric))
    all_metrics: list[UserMetric] = list(metrics_result.scalars().all())

    if not all_metrics:
        return AdminDashboardResponse(
            stats=DashboardStats(
                total_users=0, total_attempts=0,
                global_success_rate=0.0,
                most_played_level=None, hardest_level=None,
            ),
            levels=[],
        )

    # ── 2. Agrupa por challenge_id en Python (evita N+1 y es más flexible) ───
    from collections import defaultdict
    groups: dict[str, list[UserMetric]] = defaultdict(list)
    for m in all_metrics:
        groups[str(m.challenge_id)].append(m)

    # ── 3. Carga los challenges referenciados ─────────────────────────────────
    challenge_ids = list(groups.keys())
    ch_result = await db.execute(
        select(Challenge).where(
            Challenge.id.in_([__import__('uuid').UUID(cid) for cid in challenge_ids])
        )
    )
    challenges: dict[str, Challenge] = {
        str(ch.id): ch for ch in ch_result.scalars().all()
    }

    # ── 4. Calcula métricas por nivel ─────────────────────────────────────────
    level_metrics: list[LevelMetric] = []

    for cid, rows in groups.items():
        ch = challenges.get(cid)
        title = ch.title if ch else f"(nivel eliminado {cid[:8]})"

        total       = len(rows)
        resolved    = sum(1 for r in rows if r.status == "success")
        success_rate = round(resolved / total * 100, 1) if total else 0.0

        all_attempts    = [r.attempts for r in rows]
        avg_attempts    = round(sum(all_attempts) / total, 1)
        max_attempts    = max(all_attempts)

        avg_time_ms     = sum(r.time_spent_ms for r in rows) / total
        avg_time_min    = round(avg_time_ms / 60_000, 1)

        hints_list      = [r.hints_used for r in rows]
        avg_hints       = round(sum(hints_list) / total, 1)
        daki_full       = sum(1 for h in hints_list if h >= 3)
        daki_dependency = round(daki_full / total * 100, 1) if total else 0.0

        # Top 3 errores más frecuentes
        error_counts: dict[str, int] = defaultdict(int)
        for r in rows:
            for err in json.loads(r.syntax_errors_log or "[]"):
                if err:
                    error_counts[err] += 1
        top_errors = [e for e, _ in sorted(error_counts.items(), key=lambda x: -x[1])[:3]]

        level_metrics.append(LevelMetric(
            challenge_id=cid,
            title=title,
            sector_id=ch.sector_id if ch else None,
            level_order=ch.level_order if ch else None,
            difficulty=ch.difficulty if ch else None,
            total_users=total,
            resolved_users=resolved,
            success_rate=success_rate,
            avg_attempts=avg_attempts,
            avg_time_min=avg_time_min,
            max_attempts=max_attempts,
            daki_dependency=daki_dependency,
            avg_hints=avg_hints,
            top_errors=top_errors,
            friction_alert=avg_attempts > 10,
            daki_overload=daki_dependency > 50.0,
        ))

    # Ordena por level_order (None al final)
    level_metrics.sort(key=lambda x: (x.level_order is None, x.level_order or 0))

    # ── 5. Stats globales ─────────────────────────────────────────────────────
    unique_users   = len({str(m.user_id) for m in all_metrics})
    total_attempts = sum(m.attempts for m in all_metrics)
    global_success = round(
        sum(1 for m in all_metrics if m.status == "success") / len(all_metrics) * 100, 1
    )
    most_played    = max(level_metrics, key=lambda x: x.total_users)
    hardest        = max(level_metrics, key=lambda x: x.avg_attempts)

    return AdminDashboardResponse(
        stats=DashboardStats(
            total_users=unique_users,
            total_attempts=total_attempts,
            global_success_rate=global_success,
            most_played_level=most_played.title,
            hardest_level=hardest.title,
        ),
        levels=level_metrics,
    )
