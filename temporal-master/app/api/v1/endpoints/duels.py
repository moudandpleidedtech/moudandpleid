"""
Endpoints de Duelos PvP (Prompt 20).

POST  /api/v1/duels/challenge          – buscar oponente y crear duelo
POST  /api/v1/duels/{duel_id}/submit   – enviar solución
GET   /api/v1/duels/inbox              – duelos pendientes como defensor
GET   /api/v1/duels/{duel_id}          – estado completo del duelo
"""

import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.challenge import Challenge
from app.models.duel import Duel
from app.models.user import User
from app.services import activity_service
from app.services.elo_service import compute_elo_delta
from app.services.execution_service import execute_python_code

router = APIRouter(prefix="/duels", tags=["duels"])

ELO_WINDOW = 200  # ±200 Elo para emparejamiento


# ─── Schemas ──────────────────────────────────────────────────────────────────

class ChallengeRequest(BaseModel):
    user_id: uuid.UUID


class SubmitRequest(BaseModel):
    user_id: uuid.UUID
    source_code: str


class DuelOut(BaseModel):
    duel_id: uuid.UUID
    status: str
    challenger_id: uuid.UUID
    defender_id: uuid.UUID
    challenge_id: uuid.UUID
    challenge_title: Optional[str] = None
    challenge_description: Optional[str] = None
    challenge_initial_code: Optional[str] = None
    challenge_expected_output: Optional[str] = None
    challenger_elo: int
    defender_elo: int
    challenger_correct: Optional[bool]
    challenger_time_ms: Optional[float]
    defender_correct: Optional[bool]
    defender_time_ms: Optional[float]
    winner_id: Optional[uuid.UUID]
    elo_delta: int
    created_at: datetime
    completed_at: Optional[datetime]


class SubmitOut(BaseModel):
    duel_id: uuid.UUID
    correct: bool
    execution_time_ms: float
    stdout: str
    stderr: str
    status: str
    winner_id: Optional[uuid.UUID] = None
    elo_delta: int = 0
    your_new_elo: Optional[int] = None


class InboxItem(BaseModel):
    duel_id: uuid.UUID
    challenger_id: uuid.UUID
    challenger_username: str
    challenger_elo: int
    challenge_title: str
    created_at: datetime


# ─── Helpers ──────────────────────────────────────────────────────────────────

async def _get_user_or_404(db: AsyncSession, user_id: uuid.UUID) -> User:
    user = await db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


async def _get_duel_or_404(db: AsyncSession, duel_id: uuid.UUID) -> Duel:
    duel = await db.get(Duel, duel_id)
    if duel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Duel not found")
    return duel


async def _build_duel_out(db: AsyncSession, duel: Duel) -> DuelOut:
    challenger = await db.get(User, duel.challenger_id)
    defender = await db.get(User, duel.defender_id)
    challenge = await db.get(Challenge, duel.challenge_id)
    return DuelOut(
        duel_id=duel.id,
        status=duel.status,
        challenger_id=duel.challenger_id,
        defender_id=duel.defender_id,
        challenge_id=duel.challenge_id,
        challenge_title=challenge.title if challenge else None,
        challenge_description=challenge.description if challenge else None,
        challenge_initial_code=challenge.initial_code if challenge else None,
        challenge_expected_output=challenge.expected_output if challenge else None,
        challenger_elo=challenger.elo_rating if challenger else 1200,
        defender_elo=defender.elo_rating if defender else 1200,
        challenger_correct=duel.challenger_correct,
        challenger_time_ms=duel.challenger_time_ms,
        defender_correct=duel.defender_correct,
        defender_time_ms=duel.defender_time_ms,
        winner_id=duel.winner_id,
        elo_delta=duel.elo_delta,
        created_at=duel.created_at,
        completed_at=duel.completed_at,
    )


# ─── Endpoints ────────────────────────────────────────────────────────────────

@router.post(
    "/challenge",
    response_model=DuelOut,
    status_code=status.HTTP_201_CREATED,
    summary="Retar a un oponente aleatorio dentro del rango Elo",
)
async def create_duel(
    payload: ChallengeRequest,
    db: AsyncSession = Depends(get_db),
) -> DuelOut:
    challenger = await _get_user_or_404(db, payload.user_id)

    # Buscar oponente dentro de ±ELO_WINDOW que no sea el propio usuario
    # y que no tenga ya un duelo activo contra el challenger
    lo = challenger.elo_rating - ELO_WINDOW
    hi = challenger.elo_rating + ELO_WINDOW

    opponent_result = await db.execute(
        select(User)
        .where(
            and_(
                User.id != challenger.id,
                User.elo_rating >= lo,
                User.elo_rating <= hi,
            )
        )
        .order_by(func.random())
        .limit(1)
    )
    defender = opponent_result.scalar_one_or_none()
    if defender is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró oponente en tu rango Elo (±200). Inténtalo más tarde.",
        )

    # Seleccionar un reto aleatorio para el duelo
    challenge_result = await db.execute(
        select(Challenge).order_by(func.random()).limit(1)
    )
    challenge = challenge_result.scalar_one_or_none()
    if challenge is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay retos disponibles para el duelo.",
        )

    duel = Duel(
        challenger_id=challenger.id,
        defender_id=defender.id,
        challenge_id=challenge.id,
        status="active",
    )
    db.add(duel)
    await db.flush()

    return await _build_duel_out(db, duel)


@router.post(
    "/{duel_id}/submit",
    response_model=SubmitOut,
    summary="Enviar solución al duelo",
)
async def submit_duel(
    duel_id: uuid.UUID,
    payload: SubmitRequest,
    db: AsyncSession = Depends(get_db),
) -> SubmitOut:
    duel = await _get_duel_or_404(db, duel_id)

    if duel.status in ("completed", "expired"):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Este duelo ya finalizó.",
        )

    # Determinar si es challenger o defender
    is_challenger = duel.challenger_id == payload.user_id
    is_defender = duel.defender_id == payload.user_id
    if not is_challenger and not is_defender:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No formas parte de este duelo.",
        )

    # Evitar doble envío
    if is_challenger and duel.challenger_code is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya enviaste tu solución.")
    if is_defender and duel.defender_code is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya enviaste tu solución.")

    # Ejecutar código
    challenge = await db.get(Challenge, duel.challenge_id)
    if challenge is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reto no encontrado.")

    import json as _json
    test_inputs: list[str] = _json.loads(challenge.test_inputs_json or "[]")
    exec_result = await execute_python_code(payload.source_code, test_inputs)
    correct = exec_result["success"] and exec_result["stdout"].strip() == challenge.expected_output.strip()
    time_ms: float = exec_result["execution_time_ms"]

    # Guardar resultados
    if is_challenger:
        duel.challenger_code = payload.source_code
        duel.challenger_time_ms = time_ms
        duel.challenger_correct = correct
        duel.status = "awaiting_defender"
    else:
        duel.defender_code = payload.source_code
        duel.defender_time_ms = time_ms
        duel.defender_correct = correct

    # Si ambos enviaron → resolver duelo
    winner_id: Optional[uuid.UUID] = None
    elo_delta = 0
    new_elo: Optional[int] = None

    both_submitted = (
        duel.challenger_code is not None and duel.defender_code is not None
    )
    if both_submitted:
        winner_id = _resolve_winner(duel)
        duel.winner_id = winner_id
        duel.status = "completed"
        duel.completed_at = datetime.now(timezone.utc)

        # Aplicar Elo
        challenger_user = await db.get(User, duel.challenger_id)
        defender_user = await db.get(User, duel.defender_id)
        if challenger_user and defender_user and winner_id:
            if winner_id == challenger_user.id:
                delta = compute_elo_delta(challenger_user.elo_rating, defender_user.elo_rating)
                challenger_user.elo_rating += delta
                defender_user.elo_rating = max(0, defender_user.elo_rating - delta)
            else:
                delta = compute_elo_delta(defender_user.elo_rating, challenger_user.elo_rating)
                defender_user.elo_rating += delta
                challenger_user.elo_rating = max(0, challenger_user.elo_rating - delta)
            duel.elo_delta = delta
            elo_delta = delta
            new_elo = (
                challenger_user.elo_rating if payload.user_id == challenger_user.id
                else defender_user.elo_rating
            )
            # Emit activity event
            winner_user = challenger_user if winner_id == challenger_user.id else defender_user
            loser_user = defender_user if winner_id == challenger_user.id else challenger_user
            await activity_service.emit_duel_result(
                winner_user.username, loser_user.username, delta
            )

    return SubmitOut(
        duel_id=duel.id,
        correct=correct,
        execution_time_ms=time_ms,
        stdout=exec_result["stdout"],
        stderr=exec_result["stderr"],
        status=duel.status,
        winner_id=winner_id,
        elo_delta=elo_delta,
        your_new_elo=new_elo,
    )


def _resolve_winner(duel: Duel) -> Optional[uuid.UUID]:
    """
    Lógica de desempate:
      1. Quien resolvió correctamente gana.
      2. Si ambos correctos → menor tiempo gana.
      3. Si ninguno correcto → empate (None).
    """
    c_ok = duel.challenger_correct or False
    d_ok = duel.defender_correct or False

    if c_ok and not d_ok:
        return duel.challenger_id
    if d_ok and not c_ok:
        return duel.defender_id
    if c_ok and d_ok:
        ct = duel.challenger_time_ms or float("inf")
        dt = duel.defender_time_ms or float("inf")
        return duel.challenger_id if ct <= dt else duel.defender_id
    return None  # empate


@router.get(
    "/inbox",
    response_model=list[InboxItem],
    summary="Duelos pendientes donde eres el defensor",
)
async def get_inbox(
    user_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db),
) -> list[InboxItem]:
    result = await db.execute(
        select(Duel)
        .where(
            and_(
                Duel.defender_id == user_id,
                Duel.status == "awaiting_defender",
            )
        )
        .order_by(Duel.created_at.desc())
    )
    duels = result.scalars().all()

    items: list[InboxItem] = []
    for d in duels:
        challenger = await db.get(User, d.challenger_id)
        challenge = await db.get(Challenge, d.challenge_id)
        if challenger and challenge:
            items.append(
                InboxItem(
                    duel_id=d.id,
                    challenger_id=d.challenger_id,
                    challenger_username=challenger.username,
                    challenger_elo=challenger.elo_rating,
                    challenge_title=challenge.title,
                    created_at=d.created_at,
                )
            )
    return items


@router.get(
    "/{duel_id}",
    response_model=DuelOut,
    summary="Estado completo del duelo",
)
async def get_duel(
    duel_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> DuelOut:
    duel = await _get_duel_or_404(db, duel_id)
    return await _build_duel_out(db, duel)
