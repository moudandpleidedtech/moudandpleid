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
    get_concept_intel,
    get_escalation_directive,
    get_offline_response,
    get_stage_addendum,
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
    concepts_taught: list[str] | None = None,
    pedagogical_objective: str | None = None,
    syntax_hint: str | None = None,
    db_hints: list[str] | None = None,
    stage_addendum: str = "",
    concept_intel: str = "",
    weak_concepts: list[str] | None = None,
    error_type: str = "",
) -> str:
    """
    Construye el mensaje del usuario que recibe el modelo.

    v3 — Inyección de Intel de Misión:
    - Conceptos evaluados, objetivo pedagógico, patrón estructural y pistas pre-cargadas.
    - Etapa DAKI (comportamiento calibrado al nivel del Operador).
    - Intel táctica por concepto (errores frecuentes pre-catalogados).
    """
    escalation = get_escalation_directive(fail_count)
    history_block = f"\n{operator_history}\n" if operator_history else ""

    # ── Etapa DAKI y comportamiento calibrado ────────────────────────────────
    stage_block = f"\n{stage_addendum}\n" if stage_addendum else ""

    # ── Intel táctica por concepto ───────────────────────────────────────────
    intel_block = f"\n{concept_intel}\n" if concept_intel else ""

    # ── Intel de la misión: conceptos, objetivo, scaffold, pistas DB ─────────
    mission_intel_parts: list[str] = []
    if error_type:
        mission_intel_parts.append(f"Tipo de error (DAKI Memory): {error_type}")
    if concepts_taught:
        mission_intel_parts.append(f"Conceptos evaluados: {', '.join(concepts_taught)}")
    if pedagogical_objective:
        mission_intel_parts.append(f"Objetivo pedagógico: {pedagogical_objective}")
    if syntax_hint:
        mission_intel_parts.append(
            f"Patrón estructural esperado (NO dar directamente — úsalo para calibrar el scaffold):\n"
            f"```python\n{syntax_hint}\n```"
        )
    if db_hints and len(db_hints) >= fail_count:
        # Pistas pre-escritas por nivel — guía a DAKI sobre la intención pedagógica
        hint_idx = min(fail_count - 1, len(db_hints) - 1)
        mission_intel_parts.append(
            f"Pista pre-cargada para NIVEL-{min(fail_count, 3)} (orienta tu respuesta, "
            f"NO la copies literalmente — reescríbela en voz DAKI táctica):\n"
            f"  \"{db_hints[hint_idx]}\""
        )

    # ── DAKI Memory: conceptos con refuerzo pendiente ─────────────────────────
    if weak_concepts:
        top_weak = weak_concepts[:3]
        mission_intel_parts.append(
            f"MEMORIA DAKI — Conceptos con baja maestría en este Operador "
            f"(reforzar sutilmente si aparecen en el código): {', '.join(top_weak)}"
        )

    mission_intel_block = ""
    if mission_intel_parts:
        mission_intel_block = (
            "--- INTEL DE MISIÓN (pre-cargada en el Nexo) ---\n"
            + "\n".join(mission_intel_parts)
            + "\n--- FIN INTEL DE MISIÓN ---\n\n"
        )

    # ── Análisis de patrones problemáticos de plataforma ─────────────────────
    platform_notes = _detect_platform_issues(source_code)
    platform_block = ""
    if platform_notes:
        platform_block = "\n--- ANÁLISIS DE PLATAFORMA ---\n" + "\n".join(platform_notes) + "\n"

    # ── Formateo del error / stacktrace ──────────────────────────────────────
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
        f"{stage_block}"
        f"{history_block}\n"
        f"{mission_intel_block}"
        f"{intel_block}\n"
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

    Economía de tokens:
    - Éxito: respuesta estática — cero llamadas al LLM. El valor real ya llegó
      (el Operador sabe que pasó). El LLM no añade información accionable.
    - Fallo: cache semántico por (challenge_title, error_output[:200]).
      El mismo error en la misma misión produce la misma reacción — sin duplicar tokens.
    """
    # ── Éxito: respuesta estática, $0 en tokens ───────────────────────────────
    if is_success:
        return "Protocolo validado. Acceso concedido al siguiente sector."

    # ── Fallo: check cache antes de llamar al LLM ─────────────────────────────
    error_fingerprint = error_output.strip()[:200] if error_output.strip() else "output_mismatch"
    cache_key = await semantic_cache_service.generate_cache_key(
        mission_level=0,
        user_code=f"exec_feedback|{challenge_title}",
        compiler_error=error_fingerprint,
    )
    cached = await semantic_cache_service.get_cached_response(cache_key)
    if cached is not None:
        return cached

    if not settings.ANTHROPIC_API_KEY:
        return "// [DAKI] Anomalía detectada. El stacktrace contiene la coordenada del fallo."

    client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

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
        ) or "// [DAKI] Anomalía. Revisa el stacktrace."

        # Guardar en caché — el mismo error no vuelve a costar tokens
        await semantic_cache_service.save_to_cache(cache_key, text)
        return text

    except Exception:
        return "// [DAKI] Anomalía detectada. Revisa el stacktrace."


# ─── Punto de entrada público ─────────────────────────────────────────────────

def get_db_fallback_hint(db_hints: list[str] | None, fail_count: int) -> str | None:
    """
    Retorna la pista pre-escrita de la DB según el nivel de falla.
    Índice 0 → fail_count=1, índice 1 → fail_count=2, índice 2+ → fail_count>=3.
    Retorna None si no hay pistas disponibles.
    """
    if not db_hints:
        return None
    idx = min(max(fail_count - 1, 0), len(db_hints) - 1)
    hint = db_hints[idx] if idx < len(db_hints) else None
    return hint if hint else None


async def get_hint(
    challenge_title: str,
    challenge_description: str,
    source_code: str,
    error_output: str,
    fail_count: int = 1,
    operator_history: str = "",
    concepts_taught: list[str] | None = None,
    pedagogical_objective: str | None = None,
    syntax_hint: str | None = None,
    db_hints: list[str] | None = None,
    operator_level: int = 1,
    weak_concepts: list[str] | None = None,
    error_type: str = "",
) -> str:
    """
    Genera una pista táctica calibrada al nivel de falla y al nivel del Operador.

    Args:
        challenge_title:       Nombre de la misión activa.
        challenge_description: Descripción del desafío.
        source_code:           Código actual del Operador (truncado a 2000 chars).
        error_output:          Stacktrace o error real obtenido (truncado a 800 chars).
        fail_count:            Intentos fallidos (1=sutil | 2=conceptual | ≥3=reframe).
        operator_history:      Sección OPERATOR_HISTORY desde memory_service.
        concepts_taught:       Conceptos evaluados en esta misión.
        pedagogical_objective: Objetivo de aprendizaje del nivel.
        syntax_hint:           Patrón estructural de la solución esperada.
        db_hints:              Pistas pre-escritas de la DB (3 niveles).
        operator_level:        Nivel actual del Operador (calibra etapa DAKI).

    Returns:
        Pista táctica como string calibrada al nivel de falla.
    """
    if not settings.ANTHROPIC_API_KEY:
        # Fallback: usa pista pre-escrita de la DB si existe
        db_hint = get_db_fallback_hint(db_hints, fail_count)
        return db_hint or get_offline_response(fail_count)

    client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
    max_tokens = _MAX_TOKENS.get(min(fail_count, 3), 420)

    # Construir contexto enriquecido
    stage_addendum = get_stage_addendum(operator_level)
    concept_intel = get_concept_intel(concepts_taught or [])

    user_msg = _build_user_message(
        challenge_title=challenge_title,
        challenge_description=challenge_description,
        source_code=source_code,
        error_output=error_output,
        fail_count=fail_count,
        operator_history=operator_history,
        concepts_taught=concepts_taught,
        pedagogical_objective=pedagogical_objective,
        syntax_hint=syntax_hint,
        db_hints=db_hints,
        stage_addendum=stage_addendum,
        concept_intel=concept_intel,
        weak_concepts=weak_concepts,
        error_type=error_type,
    )

    try:
        return await _run_with_tools(
            client=client,
            messages=[{"role": "user", "content": user_msg}],
            max_tokens=max_tokens,
            fallback_fail_count=fail_count,
        )
    except Exception:
        # Fallback a pista pre-escrita de la DB antes del fallback genérico
        db_hint = get_db_fallback_hint(db_hints, fail_count)
        return db_hint or get_offline_response(fail_count)


# ─────────────────────────────────────────────────────────────────────────────
# AIMentorService — Orquestador de la Trinidad de Ahorro de Tokens
#
# Flujo:
#   Cache hit  → respuesta $0, sin llamada al LLM
#   Cache miss → PromptBuilder comprime → LLMRouter elige modelo → LLM → Cache save
# ─────────────────────────────────────────────────────────────────────────────

import time as _time
from typing import Any, Final

from app.services.llm_router      import llm_router_service
from app.services.semantic_cache  import semantic_cache_service
from app.services.prompt_builder  import prompt_builder_service

_NEXO_SATURADO = (
    "// [DAKI] Nexo saturado. El canal de IA está temporalmente fuera de línea. "
    "Reintenta en unos segundos, Operador."
)

_MENTOR_MAX_TOKENS = 420


async def _call_llm(
    model_id:   str,
    messages:   list[dict[str, Any]],
    fail_count: int = 1,
) -> tuple[str, int]:
    """
    Llama al LLM real usando el cliente Anthropic existente.
    Extrae el system message de la lista y lo pasa al parámetro `system`.

    Returns:
        (response_text, estimated_tokens_used)
    """
    from app.core.config import settings  # import diferido — evita circular

    # Separar system del resto
    system_content = next(
        (m["content"] for m in messages if m.get("role") == "system"), ""
    )
    user_messages = [m for m in messages if m.get("role") != "system"]

    if not settings.ANTHROPIC_API_KEY:
        return get_offline_response(fail_count), 0

    client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

    response = await client.messages.create(
        model=model_id,
        max_tokens=_MENTOR_MAX_TOKENS,
        system=system_content,
        messages=user_messages,
    )

    text_block = next(
        (b for b in response.content if getattr(b, "type", None) == "text"), None
    )
    text            = text_block.text.strip() if text_block else get_offline_response(fail_count)
    tokens_used_est = getattr(response.usage, "input_tokens", 0) + getattr(response.usage, "output_tokens", 0)
    return text, tokens_used_est


_ESCALATION_THRESHOLD: Final[int] = 3   # intentos fallidos antes de forzar PREMIUM

_PROACTIVE_RULES = (
    "El Operador no ha enviado un mensaje. Reacciona al evento de telemetría recibido. "
    "Sé breve: máximo 2 líneas. Nombra el problema específico que sugiere el evento. "
    "No preguntes — señala y orienta. Tono DAKI operacional."
)

_PROACTIVE_EVENTS: dict[str, str] = {
    "idle_15_min":          "El Operador lleva 15 minutos sin avanzar en el código.",
    "idle_30_min":          "El Operador lleva 30 minutos inactivo. Posible bloqueo cognitivo.",
    "infinite_loop_warning":"El entorno detectó un bucle que no termina en el código activo.",
    "repeated_same_error":  "El Operador repitió el mismo error 3 veces consecutivas.",
    "copy_paste_detected":  "Se detectó un patrón de copy-paste sin modificaciones en el código.",
    "no_tests_run":         "El Operador lleva 20 minutos sin ejecutar ninguna prueba.",
}


class AIMentorService:
    """
    Orquestador principal de la Trinidad de Ahorro de Tokens.

    Flujo estricto (process_operator_request):
      A. Cache lookup        → hit: retorno $0
      B. Auto-escalada       → failed_attempts >= 3 fuerza PREMIUM_MODEL
      C. PromptBuilder       → compresión de historial y reglas
      D. LLMRouter           → selección de modelo (si no fue forzado)
      E. LLM call            → llamada real
      F. Cache save          → persiste para futuros hits
      G. Return              → respuesta + métricas

    Método adicional (generate_proactive_hint):
      Telemetría de trinchera — DAKI habla sin que el Operador lo pida.
    """

    async def process_operator_request(
        self,
        user_id:         str,
        mission_level:   int,
        mission_rules:   str,
        user_code:       str,
        prompt:          str,
        chat_history:    list[Any],
        error_msg:       str = "",
        failed_attempts: int = 0,
    ) -> dict[str, Any]:
        """
        Punto de entrada unificado para todas las interacciones con el mentor IA.

        Args:
            failed_attempts: Intentos fallidos acumulados en la misión actual.
                             Si >= ESCALATION_THRESHOLD (3), se fuerza PREMIUM_MODEL.

        Returns dict con:
            response          str   — texto de la respuesta
            source            str   — "cache" | "llm"
            model_used        str   — modelo seleccionado (vacío en cache hit)
            cost              int   — 0 (cache) | 1 (llm llamado)
            tokens_estimated  int   — tokens usados (0 en cache hit)
            latency_ms        float — tiempo total de procesamiento
            escalated         bool  — True si se forzó PREMIUM por frustración
        """
        t_start = _time.monotonic()

        try:
            # ── A. Cache lookup ───────────────────────────────────────────────
            cache_key = await semantic_cache_service.generate_cache_key(
                mission_level=mission_level,
                user_code=user_code,
                compiler_error=error_msg,
            )
            cached = await semantic_cache_service.get_cached_response(cache_key)

            if cached is not None:
                return {
                    "response":         cached,
                    "source":           "cache",
                    "model_used":       "",
                    "cost":             0,
                    "tokens_estimated": 0,
                    "latency_ms":       round((_time.monotonic() - t_start) * 1000, 2),
                    "escalated":        False,
                }

            # ── B. Auto-escalada por frustración ──────────────────────────────
            escalated = failed_attempts >= _ESCALATION_THRESHOLD
            if escalated:
                from app.services.llm_router import PREMIUM_MODEL
                model_id = PREMIUM_MODEL
                logger.info(
                    "Auto-escalada activada → PREMIUM_MODEL | user=%s | intentos=%d",
                    user_id, failed_attempts,
                )
            else:
                model_id = None  # se resuelve en paso D

            # ── C. Comprimir historial y reglas ───────────────────────────────
            messages = prompt_builder_service.build_tactical_prompt(
                current_mission_rules=mission_rules,
                chat_history=chat_history,
                new_user_message=prompt,
            )

            # ── D. Seleccionar modelo (solo si no fue forzado en B) ───────────
            if model_id is None:
                model_id = await llm_router_service.route_prompt(
                    prompt_text=prompt,
                    mission_level=mission_level,
                )

            # ── E. Llamada al LLM ─────────────────────────────────────────────
            ai_response, tokens_used = await _call_llm(
                model_id=model_id,
                messages=messages,
            )

            # ── F. Guardar en caché ───────────────────────────────────────────
            await semantic_cache_service.save_to_cache(cache_key, ai_response)

            # ── G. Registrar frecuencia de error (anticipación) ───────────────
            if error_msg:
                error_type = error_msg.split(":")[0].strip()[:60]
                semantic_cache_service.check_error_frequency(mission_level, error_type)

            return {
                "response":         ai_response,
                "source":           "llm",
                "model_used":       model_id,
                "cost":             1,
                "tokens_estimated": tokens_used,
                "latency_ms":       round((_time.monotonic() - t_start) * 1000, 2),
                "escalated":        escalated,
            }

        except Exception as exc:
            import logging as _logging
            _logging.getLogger(__name__).error(
                "AIMentorService.process_operator_request falló: %s", exc, exc_info=True
            )
            return {
                "response":         _NEXO_SATURADO,
                "source":           "error",
                "model_used":       "",
                "cost":             0,
                "tokens_estimated": 0,
                "latency_ms":       round((_time.monotonic() - t_start) * 1000, 2),
                "escalated":        False,
            }

    async def generate_proactive_hint(
        self,
        user_id:       str,
        telemetry_event: str,
        current_code:  str,
    ) -> str:
        """
        Telemetría de Trinchera: DAKI interviene sin que el Operador envíe un mensaje.

        El frontend dispara eventos como "idle_15_min" o "infinite_loop_warning".
        DAKI construye un prompt corto usando FAST_MODEL y responde directamente
        al canal de telemetría — no al chat principal.

        Args:
            user_id:          ID del Operador (para logging).
            telemetry_event:  Clave del evento (ver _PROACTIVE_EVENTS).
            current_code:     Snapshot del código actual en el IDE.

        Returns:
            Mensaje proactivo de DAKI (1-2 líneas).
        """
        try:
            from app.services.llm_router import FAST_MODEL

            # Resolver descripción del evento
            event_description = _PROACTIVE_EVENTS.get(
                telemetry_event,
                f"Evento de telemetría recibido: {telemetry_event}",
            )

            # Construir prompt comprimido — sin historial, sin reglas de misión
            proactive_prompt = (
                f"EVENTO: {event_description}\n\n"
                f"Código actual del Operador:\n"
                f"```python\n{current_code[:800]}\n```"
            )

            messages = prompt_builder_service.build_tactical_prompt(
                current_mission_rules=_PROACTIVE_RULES,
                chat_history=[],          # sin historial — intervención puntual
                new_user_message=proactive_prompt,
            )

            logger.info(
                "Telemetría proactiva → evento=%s | user=%s",
                telemetry_event, user_id,
            )

            response_text, _ = await _call_llm(
                model_id=FAST_MODEL,      # siempre FAST — es una intervención, no análisis profundo
                messages=messages,
            )
            return response_text

        except Exception as exc:
            logger.error(
                "generate_proactive_hint falló: event=%s user=%s error=%s",
                telemetry_event, user_id, exc, exc_info=True,
            )
            return "// [DAKI] Canal de telemetría momentáneamente fuera de línea."


# Singleton
ai_mentor_service = AIMentorService()
