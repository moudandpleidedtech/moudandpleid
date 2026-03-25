"""
prompt_builder.py — PromptBuilderService
─────────────────────────────────────────
Dieta de Prompts: construye el contexto mínimo y suficiente para cada
llamada al LLM. Sin tokens innecesarios, sin temario global inyectado.

Trinity de Ahorro de Tokens:
  1. LLMRouterService     → modelo correcto
  2. SemanticCacheService → $0 en consultas repetidas
  3. PromptBuilderService → input tokens mínimos (este módulo)
"""

from __future__ import annotations

import logging
import re
from typing import Any, Final, Literal

from pydantic import BaseModel, Field, field_validator, model_validator

logger = logging.getLogger(__name__)

# ── Constantes ────────────────────────────────────────────────────────────────

MAX_HISTORY_PAIRS:    Final[int] = 3      # últimos 3 pares = 6 mensajes máximo
MAX_MISSION_RULES_LEN: Final[int] = 2000  # límite de seguridad para reglas
MAX_USER_MESSAGE_LEN:  Final[int] = 4000  # límite de seguridad para input

DAKI_SYSTEM_IDENTITY: Final[str] = (
    "Eres DAKI, Arquitecto de Inteligencia Táctica y mentor de élite del Nexo. "
    "Tu misión: guiar al Operador para que resuelva el desafío actual mediante "
    "preguntas socráticas y pistas quirúrgicas. NUNCA entregues la solución completa. "
    "Responde siempre en español. Sé directo, táctico y sin relleno."
)


# ── Schemas ───────────────────────────────────────────────────────────────────

class ChatMessage(BaseModel):
    """Mensaje validado listo para el SDK del LLM."""

    role:    Literal["user", "assistant", "system"]
    content: str = Field(..., min_length=1, max_length=8000)

    @field_validator("content")
    @classmethod
    def strip_content(cls, v: str) -> str:
        return v.strip()

    model_config = {"frozen": True}


class TacticalPrompt(BaseModel):
    """Resultado final del builder: lista de mensajes + métricas."""

    messages:          list[dict[str, str]]
    system_tokens_est: int = Field(description="Estimación de tokens del system message")
    history_msgs_used: int = Field(description="Mensajes de historial incluidos (post-trim)")
    total_msgs:        int = Field(description="Total de mensajes en el prompt")

    model_config = {"frozen": True}


# ── Servicio ──────────────────────────────────────────────────────────────────

class PromptBuilderService:
    """
    Constructor de prompts hiper-eficiente para el LLM de DAKI.

    Reglas de compresión:
    - System: identidad táctica fija + reglas dinámicas del nivel actual ÚNICAMENTE.
    - History: últimos MAX_HISTORY_PAIRS pares (user/assistant). El resto se descarta.
    - Mensajes system en el historial entrante son siempre ignorados (se reconstruyen).
    - Mensajes malformados son descartados con warning (nunca rompen el flujo).
    """

    def build_tactical_prompt(
        self,
        current_mission_rules: str,
        chat_history:          list[Any],
        new_user_message:      str,
    ) -> list[dict[str, str]]:
        """
        Construye el prompt mínimo y suficiente para una llamada al LLM.

        Args:
            current_mission_rules: Reglas específicas del nivel actual.
            chat_history:          Historial previo (list[dict] con keys role/content).
            new_user_message:      Mensaje nuevo del Operador.

        Returns:
            Lista de dicts `[{"role": ..., "content": ...}]` lista para el SDK.

        Raises:
            ValueError: Si `new_user_message` está vacío o `current_mission_rules` es inválido.
        """
        try:
            # 1. Validar inputs críticos
            new_user_message      = self._validate_user_message(new_user_message)
            current_mission_rules = self._validate_mission_rules(current_mission_rules)

            # 2. System message dinámico (identidad + reglas del nivel, nada más)
            system_msg = self._build_system_message(current_mission_rules)

            # 3. Sanitizar y recortar historial
            clean_history = self._sanitize_history(chat_history)
            trimmed       = self._trim_to_pairs(clean_history, MAX_HISTORY_PAIRS)

            # 4. Mensaje nuevo del Operador
            user_msg = ChatMessage(role="user", content=new_user_message)

            # 5. Ensamblar lista final
            messages: list[dict[str, str]] = (
                [system_msg.model_dump()]
                + [m.model_dump() for m in trimmed]
                + [user_msg.model_dump()]
            )

            result = TacticalPrompt(
                messages          = messages,
                system_tokens_est = self._estimate_tokens(system_msg.content),
                history_msgs_used = len(trimmed),
                total_msgs        = len(messages),
            )

            logger.debug(
                "PromptBuilder → total=%d msgs | history=%d/%d | sys_tokens~%d",
                result.total_msgs,
                result.history_msgs_used,
                len(clean_history),
                result.system_tokens_est,
            )
            return result.messages

        except ValueError:
            raise
        except Exception as exc:
            logger.error("build_tactical_prompt falló inesperadamente: %s", exc, exc_info=True)
            raise ValueError(f"Error al construir el prompt: {exc}") from exc

    # ── Construcción del system message ──────────────────────────────────────

    def _build_system_message(self, mission_rules: str) -> ChatMessage:
        """
        Combina identidad táctica fija con las reglas exclusivas del nivel actual.
        Nunca inyecta el temario global ni contexto de otros niveles.
        """
        content = (
            f"{DAKI_SYSTEM_IDENTITY}\n\n"
            f"## REGLAS DE LA MISIÓN ACTUAL\n"
            f"{mission_rules}"
        )
        return ChatMessage(role="system", content=content)

    # ── Sanitización del historial ────────────────────────────────────────────

    def _sanitize_history(self, raw_history: list[Any]) -> list[ChatMessage]:
        """
        Convierte y valida cada mensaje del historial entrante.

        - Filtra mensajes con role "system" (siempre se reconstruye).
        - Descarta entradas malformadas con warning.
        - Garantiza contenido no vacío.
        """
        if not isinstance(raw_history, list):
            logger.warning("chat_history no es una lista, se ignora: tipo=%s", type(raw_history).__name__)
            return []

        clean: list[ChatMessage] = []
        for i, item in enumerate(raw_history):
            try:
                if not isinstance(item, dict):
                    raise TypeError(f"Entrada {i} no es dict: {type(item).__name__}")

                role    = item.get("role", "")
                content = item.get("content", "")

                # Filtrar mensajes system del historial — siempre se reconstruyen
                if role == "system":
                    logger.debug("Historial: omitiendo system message en posición %d", i)
                    continue

                clean.append(ChatMessage(role=role, content=str(content)))  # type: ignore[arg-type]

            except Exception as exc:
                logger.warning("Historial: descartando mensaje malformado [%d]: %s", i, exc)
                continue

        return clean

    def _trim_to_pairs(
        self,
        history: list[ChatMessage],
        max_pairs: int,
    ) -> list[ChatMessage]:
        """
        Retiene los últimos `max_pairs` pares (user + assistant).
        Si el historial tiene N mensajes impares, se preserva la integridad
        descartando desde el inicio hasta completar pares enteros.

        Ejemplo con max_pairs=3:
          [u,a, u,a, u,a, u,a]  →  [u,a, u,a, u,a]  (últimos 6)
          [u,a, u,a, u]         →  [u,a, u]          (últimos 5, preserva par incompleto al final)
        """
        max_msgs = max_pairs * 2
        if len(history) <= max_msgs:
            return history

        trimmed   = history[-max_msgs:]
        discarded = len(history) - len(trimmed)
        logger.debug(
            "Historial recortado: %d → %d mensajes (%d descartados)",
            len(history), len(trimmed), discarded,
        )
        return trimmed

    # ── Validaciones ──────────────────────────────────────────────────────────

    @staticmethod
    def _validate_user_message(msg: str) -> str:
        if not isinstance(msg, str) or not msg.strip():
            raise ValueError("new_user_message no puede estar vacío")
        stripped = msg.strip()
        if len(stripped) > MAX_USER_MESSAGE_LEN:
            logger.warning(
                "user_message truncado: %d → %d chars",
                len(stripped), MAX_USER_MESSAGE_LEN,
            )
            stripped = stripped[:MAX_USER_MESSAGE_LEN]
        return stripped

    @staticmethod
    def _validate_mission_rules(rules: str) -> str:
        if not isinstance(rules, str) or not rules.strip():
            raise ValueError("current_mission_rules no puede estar vacío")
        rules = rules.strip()
        if len(rules) > MAX_MISSION_RULES_LEN:
            logger.warning(
                "mission_rules truncado: %d → %d chars",
                len(rules), MAX_MISSION_RULES_LEN,
            )
            rules = rules[:MAX_MISSION_RULES_LEN]
        return rules

    # ── Utilidades ────────────────────────────────────────────────────────────

    @staticmethod
    def _estimate_tokens(text: str) -> int:
        """
        Estimación rápida de tokens (~4 chars/token, heurística estándar OpenAI/Anthropic).
        No reemplaza tiktoken, pero evita importar dependencias extra para logging.
        """
        return max(1, len(re.sub(r"\s+", " ", text)) // 4)


# ── Singleton ─────────────────────────────────────────────────────────────────

prompt_builder_service = PromptBuilderService()
