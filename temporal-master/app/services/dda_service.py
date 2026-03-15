"""
Algoritmo de Dificultad Adaptativa — DDA (Prompt 23).

Lee ConceptMastery y UserProgress del jugador para calcular el perfil
de dificultad óptimo antes de generar un Bounty.

Reglas de decisión
──────────────────
MASTERY_PUSH   mastery_score > 80
               → mezcla con un concepto relacionado, difficulty sube a 8.0
               → mayor multiplicador XP + loot épico

STEALTH_REVIEW mastery_score < 40  AND  failed_attempts_on_concept >= 3
               → difficulty baja a 3.0
               → lore de "escudos bajos", loot básico

STANDARD       cualquier otro caso
               → usa la difficulty solicitada por el jugador
"""

import json
import uuid
from dataclasses import dataclass
from typing import Literal

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.challenge import Challenge
from app.models.concept_mastery import ConceptMastery
from app.models.user_progress import UserProgress

# ─── Umbrales ─────────────────────────────────────────────────────────────────

MASTERY_PUSH_THRESHOLD = 80.0
FRUSTRATION_THRESHOLD  = 40.0
FRUSTRATION_MIN_FAILS  = 3       # fallos mínimos para activar repaso encubierto

# ─── Conceptos relacionados para la mezcla en MASTERY_PUSH ────────────────────

_CONCEPT_BLEND: dict[str, str] = {
    "funciones":         "decoradores",
    "recursión":         "generadores",
    "listas":            "diccionarios",
    "diccionarios":      "clases",
    "clases":            "herencia",
    "decoradores":       "funciones de orden superior",
    "generadores":       "comprensiones",
    "comprensiones":     "expresiones lambda",
    "manejo de errores": "context managers",
    "strings":           "expresiones regulares",
    "bucles":            "generadores",
    "lambda":            "map y filter",
}

_DEFAULT_BLEND = "programación funcional"

# ─── Tabla de loot por dificultad ─────────────────────────────────────────────

@dataclass
class LootTier:
    key: str
    label: str
    rarity: str
    color: str
    xp_multiplier: float


LOOT_TABLE: list[LootTier] = [
    LootTier("common",    "Datos Básicos",       "COMÚN",       "#888888", 1.0),
    LootTier("uncommon",  "Fragmento de Código", "POCO COMÚN",  "#00FF41", 1.5),
    LootTier("rare",      "Chip de Combate",     "RARO",        "#7DF9FF", 2.0),
    LootTier("epic",      "Núcleo Enigma",       "ÉPICO",       "#FFD700", 3.0),
]


def _loot_for_modifier(modifier: float) -> LootTier:
    if modifier <= 3.0:
        return LOOT_TABLE[0]   # common
    if modifier <= 6.0:
        return LOOT_TABLE[1]   # uncommon
    if modifier <= 8.0:
        return LOOT_TABLE[2]   # rare
    return LOOT_TABLE[3]       # epic


# ─── DDA result ───────────────────────────────────────────────────────────────

@dataclass
class DDAResult:
    adjusted_concept: str
    second_concept: str | None
    difficulty_modifier: float
    mode: Literal["standard", "mastery_push", "stealth_review"]
    xp_multiplier: float
    loot: LootTier
    dda_override: bool          # True si el DDA cambió algo respecto a lo pedido
    # Raw data for prompt context
    mastery_score: float
    failed_attempts: int


# ─── Core logic ───────────────────────────────────────────────────────────────

async def analyze_player_profile(
    db: AsyncSession,
    user_id: uuid.UUID,
    requested_concept: str,
    requested_difficulty: float,
) -> DDAResult:
    """
    Analiza el perfil del jugador y devuelve un DDAResult con la dificultad
    y concepto ajustados óptimamente.
    """
    concept_norm = requested_concept.strip().lower()

    # 1. Leer maestría para el concepto solicitado
    mastery_result = await db.execute(
        select(ConceptMastery).where(
            ConceptMastery.user_id == user_id,
            ConceptMastery.concept_name == concept_norm,
        )
    )
    mastery_record = mastery_result.scalar_one_or_none()
    mastery_score: float = mastery_record.mastery_score if mastery_record else 0.0

    # 2. Contar intentos fallidos en desafíos que enseñan este concepto
    failed_result = await db.execute(
        select(func.coalesce(func.sum(UserProgress.attempts), 0))
        .join(Challenge, Challenge.id == UserProgress.challenge_id)
        .where(
            UserProgress.user_id == user_id,
            UserProgress.completed.is_(False),
            Challenge.concepts_taught_json.contains(concept_norm),
        )
    )
    failed_attempts: int = int(failed_result.scalar() or 0)

    # 3. Aplicar reglas DDA
    if mastery_score > MASTERY_PUSH_THRESHOLD:
        second = _CONCEPT_BLEND.get(concept_norm, _DEFAULT_BLEND)
        modifier = 8.0
        loot = _loot_for_modifier(modifier)
        return DDAResult(
            adjusted_concept=requested_concept,
            second_concept=second,
            difficulty_modifier=modifier,
            mode="mastery_push",
            xp_multiplier=loot.xp_multiplier,
            loot=loot,
            dda_override=(modifier != requested_difficulty or second is not None),
            mastery_score=mastery_score,
            failed_attempts=failed_attempts,
        )

    if mastery_score < FRUSTRATION_THRESHOLD and failed_attempts >= FRUSTRATION_MIN_FAILS:
        modifier = 3.0
        loot = _loot_for_modifier(modifier)
        return DDAResult(
            adjusted_concept=requested_concept,
            second_concept=None,
            difficulty_modifier=modifier,
            mode="stealth_review",
            xp_multiplier=loot.xp_multiplier,
            loot=loot,
            dda_override=(modifier != requested_difficulty),
            mastery_score=mastery_score,
            failed_attempts=failed_attempts,
        )

    # Standard: respeta la dificultad pedida por el jugador
    modifier = requested_difficulty
    loot = _loot_for_modifier(modifier)
    return DDAResult(
        adjusted_concept=requested_concept,
        second_concept=None,
        difficulty_modifier=modifier,
        mode="standard",
        xp_multiplier=loot.xp_multiplier,
        loot=loot,
        dda_override=False,
        mastery_score=mastery_score,
        failed_attempts=failed_attempts,
    )
