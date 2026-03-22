"""
ai_mentor.py — Motor de Pistas Tácticas de DAKI (con Tool Use)

Llama al modelo LLM (Claude Haiku) con el Núcleo Cognitivo de DAKI y genera
pistas calibradas según el nivel de falla del Operador.

Escalación:
    fail_count=1  → NIVEL-1: Pista sutil (2 líneas)
    fail_count=2  → NIVEL-2: Pista conceptual fuerte (3 líneas)
    fail_count≥3  → NIVEL-3: Reframing total del problema (4 líneas)

Function Calling (Prompt 58):
    Cuando DAKI detecta una pregunta conceptual genérica, puede llamar
    `lookup_tactical_concept` para recuperar la definición táctica de la
    Base de Conocimiento local en lugar de inventarla.
"""

import json

import anthropic

from app.core.config import settings
from app.services import knowledge_base
from app.services.daki_persona import (
    DAKI_SYSTEM_PROMPT,
    get_escalation_directive,
    get_offline_response,
)

# ─── Tokens por nivel ────────────────────────────────────────────────────────

_MAX_TOKENS: dict[int, int] = {1: 160, 2: 220, 3: 300}
# Ampliados respecto a v1 para acomodar posibles tool_use blocks sin recortar la respuesta

# ─── Tool schema ─────────────────────────────────────────────────────────────

DAKI_TOOLS = [
    {
        "name": "lookup_tactical_concept",
        "description": (
            "Recupera la definición táctica de un concepto de Python de la Base de Conocimiento de DAKI. "
            "Úsala cuando el Operador pregunta qué es un concepto o cómo funciona algo. "
            "La respuesta incluye: nombre táctico, definición, sintaxis, ejemplo y táctica de uso."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "concept_id": {
                    "type": "string",
                    "description": (
                        "ID del concepto. Uno de: "
                        "variable, for_loop, while_loop, if_else, function, "
                        "list, dict, string, number, input_fn, print_fn, "
                        "range_fn, return_stmt, import_stmt, boolean"
                    ),
                }
            },
            "required": ["concept_id"],
        },
    }
]


# ─── Tool use loop ────────────────────────────────────────────────────────────

async def _run_with_tools(
    client: anthropic.AsyncAnthropic,
    messages: list[dict],
    max_tokens: int,
    fallback_fail_count: int = 1,
    max_tool_rounds: int = 2,
) -> str:
    """
    Ejecuta el LLM en un loop de tool use.

    Si el modelo llama `lookup_tactical_concept`, resuelve la llamada localmente
    con knowledge_base.get_concept() y reinyecta el resultado. Repite hasta
    max_tool_rounds o hasta que el modelo entregue texto final.

    Retorna el texto de la respuesta final.
    """
    for _ in range(max_tool_rounds + 1):
        response = await client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=max_tokens,
            system=DAKI_SYSTEM_PROMPT,
            tools=DAKI_TOOLS,
            messages=messages,
        )

        if response.stop_reason != "tool_use":
            # Respuesta de texto final
            text_block = next(
                (b for b in response.content if getattr(b, "type", None) == "text"),
                None,
            )
            return text_block.text.strip() if text_block else get_offline_response(fallback_fail_count)

        # Procesar tool calls
        messages = messages + [{"role": "assistant", "content": response.content}]

        tool_results = []
        for block in response.content:
            if getattr(block, "type", None) != "tool_use":
                continue
            concept_id: str = (block.input or {}).get("concept_id", "")
            concept_data = knowledge_base.get_concept(concept_id)
            if concept_data:
                result_text = json.dumps(concept_data, ensure_ascii=False)
            else:
                result_text = json.dumps(
                    {"error": f"Concepto '{concept_id}' no encontrado en la Base de Conocimiento."}
                )
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": result_text,
            })

        messages = messages + [{"role": "user", "content": tool_results}]

    # Agotamos los rounds sin texto — fallback
    return get_offline_response(fallback_fail_count)


# ─── Construcción del mensaje ─────────────────────────────────────────────────

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


# ─── Punto de entrada público ─────────────────────────────────────────────────

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
    max_tokens = _MAX_TOKENS.get(min(fail_count, 3), 300)

    user_msg = _build_user_message(
        challenge_title=challenge_title,
        challenge_description=challenge_description,
        source_code=source_code,
        error_output=error_output,
        fail_count=fail_count,
        operator_history=operator_history,
    )

    return await _run_with_tools(
        client=client,
        messages=[{"role": "user", "content": user_msg}],
        max_tokens=max_tokens,
        fallback_fail_count=fail_count,
    )
