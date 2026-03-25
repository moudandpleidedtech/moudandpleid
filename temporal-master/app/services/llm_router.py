"""
llm_router.py — LLMRouterService
─────────────────────────────────
Enruta cada prompt al modelo óptimo según nivel de misión y complejidad
del texto. Minimiza costos sin sacrificar calidad en momentos críticos.

Lógica actual: mockeada (retorna identificadores de modelo).
Lista para inyectar SDK calls (Anthropic / OpenAI) sin cambiar la interfaz.
"""

from __future__ import annotations

import logging
from enum import Enum
from typing import Final

from pydantic import BaseModel, Field, field_validator

logger = logging.getLogger(__name__)

# ── Constantes de modelo ──────────────────────────────────────────────────────

FAST_MODEL:    Final[str] = "claude-haiku-4-5-20251001"   # bajo costo, alta velocidad
PREMIUM_MODEL: Final[str] = "claude-sonnet-4-6"           # máxima calidad, Boss Battles

BOSS_BATTLE_THRESHOLD: Final[int] = 10
LONG_PROMPT_THRESHOLD: Final[int] = 150


# ── Esquemas ──────────────────────────────────────────────────────────────────

class RoutingTier(str, Enum):
    FAST    = "FAST"
    PREMIUM = "PREMIUM"


class RoutingDecision(BaseModel):
    model_id:      str          = Field(..., description="Identificador del modelo seleccionado")
    tier:          RoutingTier  = Field(..., description="Tier de enrutamiento aplicado")
    reason:        str          = Field(..., description="Motivo de la decisión")
    mission_level: int          = Field(..., ge=1)
    prompt_length: int          = Field(..., ge=0)

    model_config = {"frozen": True}


class RouterInput(BaseModel):
    prompt_text:   str = Field(..., min_length=1)
    mission_level: int = Field(..., ge=1, le=999)

    @field_validator("prompt_text")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        return v.strip()


# ── Servicio ──────────────────────────────────────────────────────────────────

class LLMRouterService:
    """
    Decide qué modelo LLM usar para cada prompt.

    Reglas de enrutamiento:
    - FAST    → misión <= 10  Y  prompt < 150 chars
    - PREMIUM → misión > 10  O  prompt >= 150 chars  (Boss Battle territory)
    """

    async def route_prompt(
        self,
        prompt_text:   str,
        mission_level: int,
    ) -> str:
        """
        Retorna el identificador del modelo apropiado.

        Args:
            prompt_text:   Texto completo del prompt a enrutar.
            mission_level: Nivel actual de la misión (1–999).

        Returns:
            Model ID string (FAST_MODEL o PREMIUM_MODEL).

        Raises:
            ValueError: Si los parámetros de entrada son inválidos.
        """
        try:
            payload = RouterInput(
                prompt_text=prompt_text,
                mission_level=mission_level,
            )
            decision = self._decide(payload)
            logger.debug(
                "LLMRouter → %s | nivel=%d | chars=%d | motivo=%s",
                decision.model_id,
                decision.mission_level,
                decision.prompt_length,
                decision.reason,
            )
            return decision.model_id

        except Exception as exc:
            logger.error("LLMRouterService.route_prompt falló: %s", exc, exc_info=True)
            # Fallback seguro: PREMIUM garantiza calidad ante cualquier fallo de lógica
            return PREMIUM_MODEL

    def _decide(self, payload: RouterInput) -> RoutingDecision:
        """Lógica de enrutamiento pura, sin efectos secundarios."""
        length       = len(payload.prompt_text)
        is_boss      = payload.mission_level > BOSS_BATTLE_THRESHOLD
        is_long      = length >= LONG_PROMPT_THRESHOLD

        if is_boss or is_long:
            reason = (
                "Boss Battle (nivel > 10)" if is_boss and not is_long
                else "Prompt complejo (≥ 150 chars)" if is_long and not is_boss
                else "Boss Battle + prompt complejo"
            )
            return RoutingDecision(
                model_id      = PREMIUM_MODEL,
                tier          = RoutingTier.PREMIUM,
                reason        = reason,
                mission_level = payload.mission_level,
                prompt_length = length,
            )

        return RoutingDecision(
            model_id      = FAST_MODEL,
            tier          = RoutingTier.FAST,
            reason        = "Misión temprana + prompt corto",
            mission_level = payload.mission_level,
            prompt_length = length,
        )


# ── Singleton listo para inyección de dependencias ────────────────────────────

llm_router_service = LLMRouterService()
