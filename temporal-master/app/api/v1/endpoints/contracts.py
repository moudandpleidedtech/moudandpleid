"""
contracts.py — Sala de Contratos DAKI

GET  /api/v1/contracts              — Lista contratos con estado de progreso del Operador
POST /api/v1/contracts/review       — DAKI revisa el código del Operador contra criterios del contrato
GET  /api/v1/contracts/{level}/info — Detalles del contrato + criterios de evaluación
"""

import uuid

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.rate_limit import limiter
from app.models.challenge import Challenge
from app.models.user_progress import UserProgress
from app.services.daki_reviewer import CONTRACT_KNOWLEDGE, review_contract

router = APIRouter(prefix="/contracts", tags=["contracts"])


# ─── Schemas ──────────────────────────────────────────────────────────────────

class ContractSummary(BaseModel):
    id: str
    level_order: int
    title: str
    description: str
    difficulty: str
    base_xp_reward: int
    telemetry_goal_time: int | None
    concepts_taught: list[str]
    lore_briefing: str | None
    pedagogical_objective: str | None
    initial_code: str
    expected_output: str
    test_inputs: list[str]
    completed: bool
    unlocked: bool          # True si el operador tiene nivel suficiente
    criteria_count: int     # Número de criterios de evaluación


class ReviewRequest(BaseModel):
    user_id: uuid.UUID
    challenge_id: uuid.UUID
    code: str
    operator_level: int = 1


class CriterionResult(BaseModel):
    criterio: str
    estado: str      # OK | FALLA | MEJORA
    detalle: str


class ReviewResponse(BaseModel):
    veredicto: str           # CONTRATO_VALIDADO | REQUIERE_AJUSTE
    puntuacion: int
    fortalezas: list[str]
    observaciones: list[CriterionResult]
    sugerencias: list[str]
    listo_para_github: bool
    contract_title: str


# ─── Helpers ──────────────────────────────────────────────────────────────────

import json as _json

def _parse_concepts(raw: str | None) -> list[str]:
    try:
        parsed = _json.loads(raw or "[]")
        return [str(c) for c in parsed] if isinstance(parsed, list) else []
    except Exception:
        return []

def _parse_inputs(raw: str | None) -> list[str]:
    try:
        parsed = _json.loads(raw or "[]")
        return [str(i) for i in parsed] if isinstance(parsed, list) else []
    except Exception:
        return []


# ─── Endpoints ────────────────────────────────────────────────────────────────

@router.get(
    "",
    response_model=list[ContractSummary],
    summary="Lista los Contratos de Certificación con estado del Operador",
)
async def list_contracts(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> list[ContractSummary]:
    """
    Devuelve los 3 contratos (L50, L60, L70) con su estado de completado.
    El campo 'unlocked' indica si el operador alcanzó el nivel requerido.
    Requiere ?user_id=<uuid> del operador autenticado.
    """
    # Obtener contratos (phase='contrato')
    result = await db.execute(
        select(Challenge)
        .where(Challenge.phase == "contrato")
        .order_by(Challenge.level_order)
    )
    challenges = list(result.scalars().all())

    if not challenges:
        return []

    # Obtener progreso del operador para estos contratos
    challenge_ids = [c.id for c in challenges]
    prog_result = await db.execute(
        select(UserProgress).where(
            UserProgress.user_id == user_id,
            UserProgress.challenge_id.in_(challenge_ids),
        )
    )
    progress_map: dict[uuid.UUID, bool] = {
        p.challenge_id: p.completed
        for p in prog_result.scalars().all()
    }

    # Obtener nivel actual del operador
    from app.models.user import User
    user_result = await db.execute(select(User).where(User.id == user_id))
    user = user_result.scalar_one_or_none()
    operator_level = user.current_level if user else 1

    summaries: list[ContractSummary] = []
    for ch in challenges:
        level = ch.level_order or 0
        knowledge = CONTRACT_KNOWLEDGE.get(level, {})
        criteria_count = len(knowledge.get("criteria", []))

        # Unlock logic: el operador necesita haber alcanzado (level - 10) para desbloquear
        # C50 → necesita L40+, C60 → L50+, C70 → L60+
        required_level = max(0, level - 10)
        unlocked = operator_level >= required_level

        summaries.append(ContractSummary(
            id=str(ch.id),
            level_order=level,
            title=ch.title,
            description=ch.description,
            difficulty=ch.difficulty or "expert",
            base_xp_reward=ch.base_xp_reward,
            telemetry_goal_time=ch.telemetry_goal_time,
            concepts_taught=_parse_concepts(ch.concepts_taught_json),
            lore_briefing=ch.lore_briefing,
            pedagogical_objective=ch.pedagogical_objective,
            initial_code=ch.initial_code,
            expected_output=ch.expected_output,
            test_inputs=_parse_inputs(ch.test_inputs_json),
            completed=progress_map.get(ch.id, False),
            unlocked=unlocked,
            criteria_count=criteria_count,
        ))

    return summaries


@router.post(
    "/review",
    response_model=ReviewResponse,
    status_code=status.HTTP_200_OK,
    summary="DAKI revisa el código del Operador para un Contrato",
    description=(
        "Envía el código del Operador para revisión completa por DAKI. "
        "DAKI evalúa contra los criterios del contrato y retorna un veredicto estructurado. "
        "Si el contrato es VALIDADO, el campo listo_para_github será true."
    ),
)
@limiter.limit("8/minute")
async def review_contract_code(
    request: Request,
    payload: ReviewRequest,
    db: AsyncSession = Depends(get_db),
) -> ReviewResponse:
    # Verificar que el desafío existe y es un contrato
    challenge = await db.get(Challenge, payload.challenge_id)
    if challenge is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contrato no encontrado.",
        )
    if challenge.phase != "contrato":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este desafío no es un Contrato de Certificación.",
        )

    level_order = challenge.level_order or 0

    # Verificar que el operador tiene nivel suficiente
    from app.models.user import User
    user_result = await db.execute(select(User).where(User.id == payload.user_id))
    user = user_result.scalar_one_or_none()
    operator_level = user.current_level if user else payload.operator_level

    required_level = max(0, level_order - 10)
    if operator_level < required_level:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code": "LEVEL_GATE",
                "message": f"Necesitas alcanzar el Nivel {required_level} para acceder a este contrato.",
                "required_level": required_level,
                "current_level": operator_level,
            },
        )

    # Ejecutar revisión DAKI
    result = await review_contract(
        level_order=level_order,
        code=payload.code,
        operator_level=operator_level,
    )

    # Si el contrato fue validado, registrar en progreso
    if result.get("veredicto") == "CONTRATO_VALIDADO":
        prog_result = await db.execute(
            select(UserProgress).where(
                UserProgress.user_id == payload.user_id,
                UserProgress.challenge_id == payload.challenge_id,
            )
        )
        progress = prog_result.scalar_one_or_none()
        if progress is None:
            progress = UserProgress(
                user_id=payload.user_id,
                challenge_id=payload.challenge_id,
                completed=True,
                attempts=1,
                hints_used=0,
            )
            db.add(progress)
        elif not progress.completed:
            progress.completed = True
        await db.commit()

    # Formatear observaciones
    observaciones = [
        CriterionResult(
            criterio=obs.get("criterio", ""),
            estado=obs.get("estado", "FALLA"),
            detalle=obs.get("detalle", ""),
        )
        for obs in result.get("observaciones", [])
    ]

    knowledge = CONTRACT_KNOWLEDGE.get(level_order, {})
    contract_title = knowledge.get("title", challenge.title)

    return ReviewResponse(
        veredicto=result.get("veredicto", "REQUIERE_AJUSTE"),
        puntuacion=int(result.get("puntuacion", 0)),
        fortalezas=result.get("fortalezas", []),
        observaciones=observaciones,
        sugerencias=result.get("sugerencias", []),
        listo_para_github=bool(result.get("listo_para_github", False)),
        contract_title=contract_title,
    )
