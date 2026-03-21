"""
admin.py — API Administrativa (CEO Dashboard)

Todos los endpoints requieren JWT con role=ADMIN.

Endpoints:
  POST /api/v1/admin/auth/token     — Login admin → JWT
  GET  /api/v1/admin/overview       — KPIs globales (usuarios, ingresos, retención)
  GET  /api/v1/admin/drop-off       — Usuarios estancados por nivel
  GET  /api/v1/admin/daki-stats     — Estadísticas de uso de DAKI por nivel
  GET  /api/v1/admin/recent-users   — Últimos 10 usuarios registrados
  GET  /api/v1/admin/dashboard      — Telemetría completa por nivel (legacy, mantenida)
"""

import json
import uuid
from collections import defaultdict
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.core.security import create_admin_token, require_admin
from app.models.challenge import Challenge
from app.models.user import User
from app.models.user_metrics import UserMetric
from app.models.user_progress import UserProgress

router = APIRouter(prefix="/admin", tags=["admin"])


# ═══════════════════════════════════════════════════════════════════════════════
# AUTH — Obtención del JWT de admin
# ═══════════════════════════════════════════════════════════════════════════════

class AdminLoginRequest(BaseModel):
    username: str
    password: str   # Se verifica contra hashed_password en el futuro;
                    # por ahora acepta cualquier password si is_admin=True
                    # (el único admin sos vos, protegido por is_admin en BD).


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in_minutes: int
    username: str


@router.post(
    "/auth/token",
    response_model=TokenResponse,
    summary="Login admin → JWT (role=ADMIN)",
    description=(
        "Recibe username + password. Verifica que el usuario tenga `is_admin=True`. "
        "Devuelve un JWT válido por ADMIN_TOKEN_EXPIRE_MINUTES minutos (default 8h)."
    ),
)
async def admin_login(
    payload: AdminLoginRequest,
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    result = await db.execute(select(User).where(User.username == payload.username))
    user = result.scalar_one_or_none()

    if user is None or not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas o usuario sin permisos de administrador.",
        )

    token = create_admin_token(str(user.id), user.username)
    return TokenResponse(
        access_token=token,
        expires_in_minutes=settings.ADMIN_TOKEN_EXPIRE_MINUTES,
        username=user.username,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# ENDPOINT 1 — Overview: KPIs globales del negocio
# ═══════════════════════════════════════════════════════════════════════════════

class OverviewResponse(BaseModel):
    # Usuarios
    total_users: int
    paid_users: int
    unpaid_users: int
    conversion_rate: float          # paid / total * 100

    # Ingresos (proyectados)
    license_price_usd: float
    projected_revenue_usd: float    # paid_users * license_price

    # Retención
    users_with_progress: int        # usuarios que completaron ≥ 1 nivel
    users_who_started: int          # usuarios con ≥ 1 intento
    users_completed_all: int        # usuarios con level_order 100 completado

    # Actividad reciente (últimas 24h)
    active_last_24h: int

    generated_at: str               # ISO timestamp UTC


@router.get(
    "/overview",
    response_model=OverviewResponse,
    summary="KPIs globales — usuarios, ingresos y retención",
    dependencies=[Depends(require_admin)],
)
async def get_overview(
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(require_admin),
) -> OverviewResponse:
    now = datetime.now(timezone.utc)

    # Totales de usuarios
    r = await db.execute(select(func.count()).select_from(User))
    total_users: int = r.scalar_one()

    r = await db.execute(select(func.count()).select_from(User).where(User.is_paid == True))  # noqa: E712
    paid_users: int = r.scalar_one()

    # Usuarios con progreso (completaron ≥ 1 nivel)
    r = await db.execute(
        select(func.count(UserProgress.user_id.distinct()))
        .where(UserProgress.completed == True)  # noqa: E712
    )
    users_with_progress: int = r.scalar_one()

    # Usuarios que intentaron al menos un nivel
    r = await db.execute(select(func.count(UserProgress.user_id.distinct())))
    users_who_started: int = r.scalar_one()

    # Usuarios que completaron el nivel 100 (BOSS FINAL)
    r = await db.execute(
        select(func.count(UserProgress.user_id.distinct()))
        .join(Challenge, Challenge.id == UserProgress.challenge_id)
        .where(Challenge.level_order == 100, UserProgress.completed == True)  # noqa: E712
    )
    users_completed_all: int = r.scalar_one()

    # Actividad últimas 24h (métricas con last_attempt_at reciente)
    from datetime import timedelta
    cutoff = now - timedelta(hours=24)
    r = await db.execute(
        select(func.count(UserMetric.user_id.distinct()))
        .where(UserMetric.last_attempt_at >= cutoff)
    )
    active_last_24h: int = r.scalar_one()

    unpaid = total_users - paid_users
    conversion = round(paid_users / total_users * 100, 1) if total_users else 0.0

    return OverviewResponse(
        total_users=total_users,
        paid_users=paid_users,
        unpaid_users=unpaid,
        conversion_rate=conversion,
        license_price_usd=settings.LICENSE_PRICE_USD,
        projected_revenue_usd=round(paid_users * settings.LICENSE_PRICE_USD, 2),
        users_with_progress=users_with_progress,
        users_who_started=users_who_started,
        users_completed_all=users_completed_all,
        active_last_24h=active_last_24h,
        generated_at=now.isoformat(),
    )


# ═══════════════════════════════════════════════════════════════════════════════
# ENDPOINT 2 — Drop-off: usuarios estancados por nivel
# ═══════════════════════════════════════════════════════════════════════════════

class DropOffLevel(BaseModel):
    level_order: int
    challenge_id: str
    title: str
    sector_id: int | None
    difficulty: str | None

    users_attempted: int        # usuarios que intentaron este nivel
    users_completed: int        # usuarios que lo completaron
    users_stuck: int            # intentaron pero NO completaron
    drop_off_rate: float        # users_stuck / users_attempted * 100
    avg_attempts_stuck: float   # promedio de intentos de los que se trabaron
    is_bottleneck: bool         # drop_off_rate > 40%


class DropOffResponse(BaseModel):
    total_levels_with_data: int
    top_bottlenecks: list[str]          # títulos de los 3 peores cuellos de botella
    levels: list[DropOffLevel]


@router.get(
    "/drop-off",
    response_model=DropOffResponse,
    summary="Usuarios estancados por nivel — identifica cuellos de botella",
    dependencies=[Depends(require_admin)],
)
async def get_drop_off(
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(require_admin),
) -> DropOffResponse:
    # Carga UserProgress con su Challenge en una sola query
    result = await db.execute(
        select(UserProgress, Challenge)
        .join(Challenge, Challenge.id == UserProgress.challenge_id)
        .order_by(Challenge.level_order)
    )
    rows = result.all()

    # Agrupa por challenge
    by_challenge: dict[str, dict] = {}
    for progress, challenge in rows:
        cid = str(challenge.id)
        if cid not in by_challenge:
            by_challenge[cid] = {
                "challenge": challenge,
                "attempted": [],   # (user_id, attempts, completed)
            }
        by_challenge[cid]["attempted"].append((
            str(progress.user_id),
            progress.attempts,
            progress.completed,
        ))

    levels: list[DropOffLevel] = []
    for cid, data in by_challenge.items():
        ch: Challenge = data["challenge"]
        records = data["attempted"]

        attempted = len(records)
        completed = sum(1 for _, _, c in records if c)
        stuck = attempted - completed
        drop_rate = round(stuck / attempted * 100, 1) if attempted else 0.0

        stuck_attempts = [att for _, att, c in records if not c]
        avg_stuck = round(sum(stuck_attempts) / len(stuck_attempts), 1) if stuck_attempts else 0.0

        levels.append(DropOffLevel(
            level_order=ch.level_order or 0,
            challenge_id=cid,
            title=ch.title,
            sector_id=ch.sector_id,
            difficulty=ch.difficulty,
            users_attempted=attempted,
            users_completed=completed,
            users_stuck=stuck,
            drop_off_rate=drop_rate,
            avg_attempts_stuck=avg_stuck,
            is_bottleneck=drop_rate > 40.0,
        ))

    levels.sort(key=lambda x: x.level_order)

    bottlenecks = sorted(
        [lv for lv in levels if lv.is_bottleneck],
        key=lambda x: -x.drop_off_rate,
    )[:3]

    return DropOffResponse(
        total_levels_with_data=len(levels),
        top_bottlenecks=[b.title for b in bottlenecks],
        levels=levels,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# ENDPOINT 3 — DAKI Stats: uso de pistas e independencia por nivel
# ═══════════════════════════════════════════════════════════════════════════════

class DakiLevelStat(BaseModel):
    level_order: int
    challenge_id: str
    title: str
    sector_id: int | None

    total_users: int
    avg_hints: float            # promedio de pistas usadas (0-3)
    pct_no_hints: float         # % que NO necesitó pistas
    pct_one_hint: float         # % que usó solo 1 pista
    pct_max_hints: float        # % que agotó las 3 pistas
    daki_dependency_score: float  # 0-100 (más alto = más dependencia)
    autonomy_alert: bool        # True si daki_dependency_score > 60


class DakiStatsResponse(BaseModel):
    most_independent_level: str | None   # nivel con menor dependencia
    most_dependent_level: str | None     # nivel con mayor dependencia
    global_avg_hints: float
    levels: list[DakiLevelStat]


@router.get(
    "/daki-stats",
    response_model=DakiStatsResponse,
    summary="Estadísticas de uso de DAKI por nivel — autonomía vs dependencia",
    dependencies=[Depends(require_admin)],
)
async def get_daki_stats(
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(require_admin),
) -> DakiStatsResponse:
    # Query: UserMetric + Challenge en una pasada
    result = await db.execute(
        select(UserMetric, Challenge)
        .join(Challenge, Challenge.id == UserMetric.challenge_id)
        .order_by(Challenge.level_order)
    )
    rows = result.all()

    by_challenge: dict[str, dict] = {}
    for metric, challenge in rows:
        cid = str(challenge.id)
        if cid not in by_challenge:
            by_challenge[cid] = {"challenge": challenge, "hints": []}
        by_challenge[cid]["hints"].append(metric.hints_used)

    stats: list[DakiLevelStat] = []
    all_hints: list[float] = []

    for cid, data in by_challenge.items():
        ch: Challenge = data["challenge"]
        hints: list[int] = data["hints"]
        n = len(hints)

        avg = round(sum(hints) / n, 2) if n else 0.0
        all_hints.extend(hints)

        no_hints  = round(sum(1 for h in hints if h == 0) / n * 100, 1) if n else 0.0
        one_hint  = round(sum(1 for h in hints if h == 1) / n * 100, 1) if n else 0.0
        max_hints = round(sum(1 for h in hints if h >= 3) / n * 100, 1) if n else 0.0

        # Dependency score: weighted avg (1 hint=33, 2=66, 3=100) normalized
        dependency = round(avg / 3 * 100, 1)

        stats.append(DakiLevelStat(
            level_order=ch.level_order or 0,
            challenge_id=cid,
            title=ch.title,
            sector_id=ch.sector_id,
            total_users=n,
            avg_hints=avg,
            pct_no_hints=no_hints,
            pct_one_hint=one_hint,
            pct_max_hints=max_hints,
            daki_dependency_score=dependency,
            autonomy_alert=dependency > 60.0,
        ))

    stats.sort(key=lambda x: x.level_order)

    global_avg = round(sum(all_hints) / len(all_hints), 2) if all_hints else 0.0

    most_independent = min(stats, key=lambda x: x.daki_dependency_score, default=None)
    most_dependent   = max(stats, key=lambda x: x.daki_dependency_score, default=None)

    return DakiStatsResponse(
        most_independent_level=most_independent.title if most_independent else None,
        most_dependent_level=most_dependent.title if most_dependent else None,
        global_avg_hints=global_avg,
        levels=stats,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# ENDPOINT 4 — Recent Users: últimos 10 usuarios registrados
# ═══════════════════════════════════════════════════════════════════════════════

class RecentUserItem(BaseModel):
    id: str
    username: str
    email: str
    current_level: int
    total_xp: int
    is_paid: bool
    league_tier: str
    created_at: str


class RecentUsersResponse(BaseModel):
    users: list[RecentUserItem]


@router.get(
    "/recent-users",
    response_model=RecentUsersResponse,
    summary="Últimos 10 usuarios registrados",
    dependencies=[Depends(require_admin)],
)
async def get_recent_users(
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(require_admin),
) -> RecentUsersResponse:
    result = await db.execute(
        select(User).order_by(User.created_at.desc()).limit(10)
    )
    users = result.scalars().all()
    return RecentUsersResponse(
        users=[
            RecentUserItem(
                id=str(u.id),
                username=u.username,
                email=u.email,
                current_level=u.current_level,
                total_xp=u.total_xp,
                is_paid=u.is_paid,
                league_tier=u.league_tier,
                created_at=u.created_at.isoformat(),
            )
            for u in users
        ]
    )


# ═══════════════════════════════════════════════════════════════════════════════
# ENDPOINT LEGACY — Dashboard completo (migrado a JWT, antes era X-Admin-Secret)
# ═══════════════════════════════════════════════════════════════════════════════

class LevelMetric(BaseModel):
    challenge_id: str
    title: str
    sector_id: int | None
    level_order: int | None
    difficulty: str | None
    total_users: int
    resolved_users: int
    success_rate: float
    avg_attempts: float
    avg_time_min: float
    max_attempts: int
    daki_dependency: float
    avg_hints: float
    top_errors: list[str]
    friction_alert: bool
    daki_overload: bool


class DashboardStats(BaseModel):
    total_users: int
    total_attempts: int
    global_success_rate: float
    most_played_level: str | None
    hardest_level: str | None


class AdminDashboardResponse(BaseModel):
    stats: DashboardStats
    levels: list[LevelMetric]


@router.get(
    "/dashboard",
    response_model=AdminDashboardResponse,
    summary="Telemetría completa por nivel (legacy)",
    dependencies=[Depends(require_admin)],
)
async def get_admin_dashboard(
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(require_admin),
) -> AdminDashboardResponse:
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

    groups: dict[str, list[UserMetric]] = defaultdict(list)
    for m in all_metrics:
        groups[str(m.challenge_id)].append(m)

    challenge_ids = list(groups.keys())
    ch_result = await db.execute(
        select(Challenge).where(
            Challenge.id.in_([uuid.UUID(cid) for cid in challenge_ids])
        )
    )
    challenges: dict[str, Challenge] = {
        str(ch.id): ch for ch in ch_result.scalars().all()
    }

    level_metrics: list[LevelMetric] = []
    for cid, rows in groups.items():
        ch = challenges.get(cid)
        title = ch.title if ch else f"(nivel eliminado {cid[:8]})"
        total = len(rows)
        resolved = sum(1 for r in rows if r.status == "success")

        all_attempts = [r.attempts for r in rows]
        avg_attempts = round(sum(all_attempts) / total, 1)
        avg_time_min = round(sum(r.time_spent_ms for r in rows) / total / 60_000, 1)

        hints_list = [r.hints_used for r in rows]
        avg_hints = round(sum(hints_list) / total, 1)
        daki_dep  = round(sum(1 for h in hints_list if h >= 3) / total * 100, 1)

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
            success_rate=round(resolved / total * 100, 1),
            avg_attempts=avg_attempts,
            avg_time_min=avg_time_min,
            max_attempts=max(all_attempts),
            daki_dependency=daki_dep,
            avg_hints=avg_hints,
            top_errors=top_errors,
            friction_alert=avg_attempts > 10,
            daki_overload=daki_dep > 50.0,
        ))

    level_metrics.sort(key=lambda x: (x.level_order is None, x.level_order or 0))

    unique_users   = len({str(m.user_id) for m in all_metrics})
    total_attempts = sum(m.attempts for m in all_metrics)
    global_success = round(
        sum(1 for m in all_metrics if m.status == "success") / len(all_metrics) * 100, 1
    )
    most_played = max(level_metrics, key=lambda x: x.total_users)
    hardest     = max(level_metrics, key=lambda x: x.avg_attempts)

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
