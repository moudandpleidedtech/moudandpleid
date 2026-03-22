"""
ai_mentor.py — Motor de Pistas Tácticas de DAKI

Llama al modelo LLM (Claude Haiku) con el Núcleo Cognitivo de DAKI y genera
pistas calibradas según el nivel de falla del Operador.

Escalación:
    fail_count=1  → NIVEL-1: Pista sutil (2 líneas)
    fail_count=2  → NIVEL-2: Pista conceptual fuerte (3 líneas)
    fail_count≥3  → NIVEL-3: Reframing total del problema (4 líneas)

El system prompt completo vive en daki_persona.py.
"""

import anthropic

from app.core.config import settings
from app.services.daki_persona import (
    DAKI_SYSTEM_PROMPT,
    get_escalation_directive,
    get_offline_response,
)

# Tokens máximos por nivel — progresivamente más generosos
_MAX_TOKENS: dict[int, int] = {1: 110, 2: 160, 3: 220}


def _build_user_message(
    challenge_title: str,
    challenge_description: str,
    source_code: str,
    error_output: str,
    fail_count: int,
    operator_history: str = "",
) -> str:
    """
    Construye el mensaje del usuario que recibe el modelo.
    Inyecta la directiva de escalación y el historial del Operador (si existe).
    """
    escalation = get_escalation_directive(fail_count)

    history_block = f"\n{operator_history}\n" if operator_history else ""

    return (
        f"{escalation}\n"
        f"{history_block}\n"
        f"--- CONTEXTO DE INCURSIÓN ---\n"
        f"Nombre: {challenge_title}\n"
        f"Descripción: {challenge_description}\n\n"
        f"Código del Operador:\n```python\n{source_code[:2000]}\n```\n\n"
        f"Salida / Error obtenido:\n{error_output[:600] or '(sin error — salida incorrecta)'}\n\n"
        "Activa el protocolo correspondiente y entrega la pista táctica."
    )


async def get_hint(
    challenge_title: str,
    challenge_description: str,
    source_code: str,
    error_output: str,
    fail_count: int = 1,
    operator_history: str = "",
) -> str:
    """
    Genera una pista táctica calibrada al nivel de falla del Operador.

    Args:
        challenge_title:       Nombre de la misión activa.
        challenge_description: Descripción del desafío.
        source_code:           Código actual del Operador (truncado a 2000 chars).
        error_output:          Salida o error obtenido (truncado a 600 chars).
        fail_count:            Número de intentos fallidos en esta incursión.
                               1 → sutil | 2 → conceptual | ≥3 → reframe.
        operator_history:      Sección OPERATOR_HISTORY formateada desde memory_service.

    Returns:
        Pista táctica como string (máx 2–4 líneas según nivel).
    """
    if not settings.ANTHROPIC_API_KEY:
        return get_offline_response(fail_count)

    client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

    max_tokens = _MAX_TOKENS.get(min(fail_count, 3), 220)

    user_msg = _build_user_message(
        challenge_title=challenge_title,
        challenge_description=challenge_description,
        source_code=source_code,
        error_output=error_output,
        fail_count=fail_count,
        operator_history=operator_history,
    )

    message = await client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=max_tokens,
        system=DAKI_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_msg}],
    )

    return message.content[0].text.strip()
