"""
Endpoint de Misiones Bounty generadas por IA (Prompts 22–23).

POST /api/v1/bounty/generate  — genera una misión bounty con DDA
GET  /api/v1/bounty/{id}      — recupera los datos de un bounty
"""

import json
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.challenge import Challenge, DifficultyTier
from app.services.dda_service import DDAResult, analyze_player_profile
from app.services.level_generator import generate_dynamic_bounty

router = APIRouter(prefix="/bounty", tags=["bounty"])


# ─── Schemas ──────────────────────────────────────────────────────────────────

class BountyGenerateRequest(BaseModel):
    user_id: uuid.UUID
    user_level: int = Field(1, ge=1, le=100)
    target_concept: str = Field(..., min_length=1, max_length=100)
    difficulty_modifier: float = Field(5.0, ge=1.0, le=10.0)


class LootOut(BaseModel):
    key: str
    label: str
    rarity: str
    color: str


class BountyOut(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    initial_code: str
    expected_output: str
    difficulty_tier: int
    base_xp_reward: int
    xp_multiplier: float
    challenge_type: str
    # DDA metadata
    dda_mode: str                       # standard | mastery_push | stealth_review
    dda_override: bool
    adjusted_difficulty: float
    second_concept: str | None
    mastery_score: float
    loot: LootOut


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _tier_from_modifier(modifier: float) -> DifficultyTier:
    if modifier <= 3.5:
        return DifficultyTier.BEGINNER
    if modifier <= 7.0:
        return DifficultyTier.INTERMEDIATE
    return DifficultyTier.ADVANCED


def _base_xp(tier: DifficultyTier, modifier: float) -> int:
    base = {
        DifficultyTier.BEGINNER: 40,
        DifficultyTier.INTERMEDIATE: 100,
        DifficultyTier.ADVANCED: 200,
    }[tier]
    return base + round(modifier * 12)


def _concepts_json(primary: str, secondary: str | None) -> str:
    concepts = [primary]
    if secondary:
        concepts.append(secondary)
    return json.dumps(concepts)


def _build_out(challenge: Challenge, dda: DDAResult) -> BountyOut:
    return BountyOut(
        id=challenge.id,
        title=challenge.title,
        description=challenge.description,
        initial_code=challenge.initial_code,
        expected_output=challenge.expected_output,
        difficulty_tier=challenge.difficulty_tier.value,
        base_xp_reward=challenge.base_xp_reward,
        xp_multiplier=dda.xp_multiplier,
        challenge_type="bounty",
        dda_mode=dda.mode,
        dda_override=dda.dda_override,
        adjusted_difficulty=dda.difficulty_modifier,
        second_concept=dda.second_concept,
        mastery_score=dda.mastery_score,
        loot=LootOut(
            key=dda.loot.key,
            label=dda.loot.label,
            rarity=dda.loot.rarity,
            color=dda.loot.color,
        ),
    )


# ─── Endpoints ────────────────────────────────────────────────────────────────

@router.post(
    "/generate",
    response_model=BountyOut,
    status_code=status.HTTP_201_CREATED,
    summary="Genera una misión Bounty al vuelo con DDA + IA",
)
async def generate_bounty(
    payload: BountyGenerateRequest,
    db: AsyncSession = Depends(get_db),
) -> BountyOut:
    """
    1. Analiza el perfil del jugador (ConceptMastery + UserProgress) con el DDA.
    2. Ajusta concepto y dificultad óptimamente.
    3. Llama al LLM para generar el contenido del reto.
    4. Persiste como Challenge tipo 'bounty' y retorna al frontend.
    """
    # ── 1. DDA: perfil del jugador ────────────────────────────────────────────
    dda = await analyze_player_profile(
        db=db,
        user_id=payload.user_id,
        requested_concept=payload.target_concept,
        requested_difficulty=payload.difficulty_modifier,
    )

    # ── 2. Generar contenido con el LLM ──────────────────────────────────────
    generated = await generate_dynamic_bounty(
        user_level=payload.user_level,
        target_concept=dda.adjusted_concept,
        difficulty_modifier=dda.difficulty_modifier,
        mode_hint=dda.mode if dda.mode != "standard" else None,
        second_concept=dda.second_concept,
    )

    # ── 3. Calcular recompensas dinámicas ─────────────────────────────────────
    tier = _tier_from_modifier(dda.difficulty_modifier)
    raw_xp = _base_xp(tier, dda.difficulty_modifier)
    final_xp = round(raw_xp * dda.xp_multiplier)

    # ── 4. Persistir en la base de datos ─────────────────────────────────────
    challenge = Challenge(
        title=generated["title"][:200],
        description=generated["lore_description"],
        difficulty_tier=tier,
        base_xp_reward=final_xp,
        initial_code=generated["initial_code"],
        expected_output=generated["expected_output"].strip(),
        test_inputs_json="[]",
        challenge_type="bounty",
        concepts_taught_json=_concepts_json(dda.adjusted_concept, dda.second_concept),
    )
    db.add(challenge)
    await db.flush()

    return _build_out(challenge, dda)


@router.get(
    "/{challenge_id}",
    response_model=BountyOut,
    summary="Recupera un Bounty existente",
)
async def get_bounty(
    challenge_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> BountyOut:
    challenge = await db.get(Challenge, challenge_id)
    if challenge is None or challenge.challenge_type != "bounty":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bounty no encontrado.",
        )

    # Para un bounty ya existente construimos un DDAResult neutral
    from app.services.dda_service import LOOT_TABLE, _loot_for_modifier  # local import ok
    modifier = 5.0  # default for display purposes
    loot = _loot_for_modifier(float(challenge.difficulty_tier.value) * 3)

    from dataclasses import fields
    neutral_dda = DDAResult(
        adjusted_concept="",
        second_concept=None,
        difficulty_modifier=modifier,
        mode="standard",
        xp_multiplier=loot.xp_multiplier,
        loot=loot,
        dda_override=False,
        mastery_score=0.0,
        failed_attempts=0,
    )

    return _build_out(challenge, neutral_dda)
