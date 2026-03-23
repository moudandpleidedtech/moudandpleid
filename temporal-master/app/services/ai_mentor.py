"""
ai_mentor.py — Motor de Pistas Tácticas de DAKI (Prompt 62 — Refactorización)

Cambios v2 (Prompt 62):
    - _build_user_message: inyección estructurada del stacktrace (tipo, línea, detalle, stdout)
    - _build_user_message: detección automática de input() con argumentos → nota de plataforma
    - _MAX_TOKENS ampliado para NIVEL-3 (acomoda bloque ```python``` de variables ficticias)
    - Escalation directives actualizadas (anti-spoon-feeding + variables ficticias en N3)

Escalación:
    fail_count=1  → NIVEL-1: Pista sutil (2 líneas, referencia al error real)
    fail_count=2  → NIVEL-2: Pista conceptual fuerte (3 líneas)
    fail_count≥3  → NIVEL-3: Reframing con estructura ficticia (4 líneas + bloque código)

Function Calling (Prompt 58):
    Cuando DAKI detecta una pregunta conceptual genérica, puede llamar
    `lookup_tactical_concept` para recuperar la definición táctica de la
    Base de Conocimiento local en lugar de inventarla.
"""

import json
import re

import anthropic

from app.core.config import settings
from app.services import knowledge_base
from app.services.daki_persona import (
    DAKI_SYSTEM_PROMPT,
    get_escalation_directive,
    get_offline_response,
)

# ─── Tokens por nivel ────────────────────────────────────────────────────────

_MAX_TOKENS: dict[int, int] = {
    1: 180,   # NIVEL-1: respuesta sutil, 2 líneas
    2: 260,   # NIVEL-2: pista conceptual, 3 líneas
    3: 420,   # NIVEL-3: 4 líneas + bloque ```python``` con variables ficticias
}

# ─── Patrón: input() con argumentos ──────────────────────────────────────────

# Detecta input("...") / input('...') / input(número) — argumento no vacío
_INPUT_WITH_ARG_RE = re.compile(r'input\s*\(\s*[^\s)]')

# Detecta print() que parecen ser prompts de entrada (texto con ":" o "?")
_PRINT_PROMPT_RE = re.compile(
    r'print\s*\(\s*["\'].*?(?::|¿|\?|ingrese|enter|introduce|escribe|número|numero)[^"\']*["\']',
    re.IGNORECASE,
)


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

    return get_offline_response(fallback_fail_count)


# ─── Detección de patrones problemáticos ─────────────────────────────────────

def _detect_platform_issues(source_code: str) -> list[str]:
    """
    Analiza el código del Operador en busca de patrones que causan fallos
    específicos del entorno de simulación (no errores de Python en sí).

    Retorna una lista de notas de plataforma para inyectar en el prompt.
    """
    notes: list[str] = []

    if _INPUT_WITH_ARG_RE.search(source_code):
        notes.append(
            "⚠ NOTA DE PLATAFORMA: El código contiene `input()` con argumento(s). "
            "En el entorno de simulación de DAKI, `input()` es interceptado automáticamente "
            "y cualquier argumento genera stdout extra que rompe la comparación de salida. "
            "Esto NO es un error de sintaxis Python — es un error de comprensión del entorno. "
            "DAKI debe indicar que `input()` debe usarse sin argumentos en este entorno."
        )

    if _PRINT_PROMPT_RE.search(source_code):
        notes.append(
            "⚠ NOTA DE PLATAFORMA: El código contiene `print()` que parece ser un prompt de entrada "
            "(ej. 'Ingrese:', 'Enter:''). Este print genera stdout extra que no coincide con la salida "
            "esperada. DAKI debe explicar que los prompts de entrada no deben imprimirse explícitamente."
        )

    return notes


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

    Mejoras v2 (Prompt 62):
    - Inyección estructurada del stacktrace con etiquetas claras.
    - Detección de input() con argumentos → nota de plataforma.
    - Separación entre tipo de error, línea y detalle.
    """
    escalation = get_escalation_directive(fail_count)
    history_block = f"\n{operator_history}\n" if operator_history else ""

    # ── Análisis de patrones problemáticos de plataforma ─────────────────────
    platform_notes = _detect_platform_issues(source_code)
    platform_block = ""
    if platform_notes:
        platform_block = "\n--- ANÁLISIS DE PLATAFORMA ---\n" + "\n".join(platform_notes) + "\n"

    # ── Formateo del error / stacktrace ──────────────────────────────────────
    # El error_output puede contener:
    # - Un stacktrace completo de Python (SyntaxError, TypeError, etc.)
    # - Una diferencia de salida (expected vs got)
    # - Vacío si fue correcto pero salida incorrecta
    if error_output.strip():
        error_block = (
            "--- STACKTRACE / ERROR REAL (leer obligatoriamente) ---\n"
            f"{error_output[:800]}\n"
            "--- FIN STACKTRACE ---\n"
        )
    else:
        error_block = (
            "--- RESULTADO ---\n"
            "No hay error de ejecución. La secuencia compila, pero la salida no coincide "
            "con el protocolo esperado (output mismatch — no es SyntaxError).\n"
        )

    return (
        f"{escalation}\n"
        f"{history_block}\n"
        f"--- CONTEXTO DE INCURSIÓN ---\n"
        f"Nombre: {challenge_title}\n"
        f"Descripción: {challenge_description}\n\n"
        f"--- CÓDIGO DEL OPERADOR ---\n"
        f"```python\n{source_code[:2000]}\n```\n\n"
        f"{error_block}\n"
        f"{platform_block}"
        "Activa el protocolo correspondiente. Referencia el error real del stacktrace. "
        "No inventes un error diferente al reportado."
    )


# ─── Reacción inmediata a ejecución de código ────────────────────────────────

_EXEC_MAX_TOKENS = 120  # 1-2 líneas tácticas — reacción, no andamiaje completo

_DIRECTIVE_EXEC_FAIL = """\
[DIRECTIVA: REACCIÓN INMEDIATA A EJECUCIÓN — FALLO | INTENTO #{attempt}]
El Operador acaba de ejecutar código que falló.
1. Lee el stacktrace real. Identifica tipo de error y línea exacta.
2. Responde con MÁXIMO 2 líneas: nombra el error real y señala la zona afectada.
3. NO des la solución. NO expliques el concepto — eso es para el sistema de pistas.
4. Tono DAKI operacional: directo, sin rodeos.\
"""

_DIRECTIVE_EXEC_SUCCESS = """\
[DIRECTIVA: REACCIÓN INMEDIATA A EJECUCIÓN — ÉXITO]
El Operador completó la misión correctamente.
Responde con UNA línea de reconocimiento táctico.
Sin elogios vacíos. Sin "¡Excelente!" ni "¡Perfecto!". Tono DAKI eficiente.\
"""


async def get_execute_feedback(
    challenge_title: str,
    challenge_description: str,
    source_code: str,
    error_output: str,
    attempt_number: int,
    is_success: bool,
) -> str:
    """
    Genera la reacción inmediata de DAKI a cada ejecución de código.

    Diferencia con get_hint():
    - No es andamiaje escalado — es observación táctica de 1-2 líneas.
    - Se activa automáticamente en CADA ejecución (éxito o fallo).
    - Para éxitos: reconocimiento breve sin spoon-feeding.
    - Para fallos: señala el error específico del stacktrace real.
    """
    if not settings.ANTHROPIC_API_KEY:
        if is_success:
            return "Protocolo validado. Acceso concedido al siguiente sector."
        return "// [DAKI] Anomalía detectada. El stacktrace contiene la coordenada del fallo."

    client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

    if is_success:
        directive = _DIRECTIVE_EXEC_SUCCESS
        error_block = ""
    else:
        directive = _DIRECTIVE_EXEC_FAIL.replace("{attempt}", str(attempt_number))
        if error_output.strip():
            error_block = (
                "--- STACKTRACE / ERROR REAL ---\n"
                f"{error_output[:600]}\n"
                "--- FIN ---\n"
            )
        else:
            error_block = (
                "--- RESULTADO ---\n"
                "Sin excepción Python. La salida no coincide con el protocolo esperado (output mismatch).\n"
            )

    user_msg = (
        f"{directive}\n\n"
        f"Misión: {challenge_title}\n"
        f"Descripción: {challenge_description[:300]}\n\n"
        f"Código ejecutado:\n```python\n{source_code[:1200]}\n```\n\n"
        f"{error_block}"
    )

    try:
        response = await client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=_EXEC_MAX_TOKENS,
            system=DAKI_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_msg}],
        )
        text = next(
            (b.text.strip() for b in response.content if getattr(b, "type", None) == "text"),
            None,
        )
        return text or ("Protocolo validado." if is_success else "// [DAKI] Anomalía. Revisa el stacktrace.")
    except Exception:
        if is_success:
            return "Protocolo validado. Acceso concedido."
        return "// [DAKI] Anomalía detectada. Revisa el stacktrace."


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
        error_output:          Stacktrace o error real obtenido (truncado a 800 chars).
        fail_count:            Número de intentos fallidos.
                               1 → sutil | 2 → conceptual | ≥3 → reframe + estructura ficticia.
        operator_history:      Sección OPERATOR_HISTORY formateada desde memory_service.

    Returns:
        Pista táctica como string calibrada al nivel de falla.
    """
    if not settings.ANTHROPIC_API_KEY:
        return get_offline_response(fail_count)

    client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
    max_tokens = _MAX_TOKENS.get(min(fail_count, 3), 420)

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
