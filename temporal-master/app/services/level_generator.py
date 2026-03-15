"""
Generador de Niveles Infinitos con LLM (Prompts 22–23).

Usa Claude Opus 4.6 para generar misiones tipo 'Bounty' al vuelo.
El modelo devuelve un JSON estricto con: title, lore_description,
initial_code y expected_output.

Acepta un mode_hint opcional del DDA para moldear el lore generado:
  - 'mastery_push'   → enemigos con escudo, tiempo limitado
  - 'stealth_review' → escudos bajos, misión de calibración
"""

import json
import logging

import anthropic

from app.core.config import settings

logger = logging.getLogger(__name__)

# Modelo y parámetros
_MODEL = "claude-opus-4-6"
_MAX_TOKENS = 1024


_FALLBACK_CHALLENGE = {
    "title": "PROTOCOLO DESCONOCIDO",
    "lore_description": (
        "// ENIGMA fuera de línea — clave API no configurada.\n"
        "// Implementa una función que sume dos números enteros."
    ),
    "initial_code": (
        "def suma(a, b):\n"
        "    # BUG: retorna None en lugar de la suma\n"
        "    pass\n\n"
        "print(suma(3, 7))"
    ),
    "expected_output": "10",
}


_MODE_HINTS: dict[str, str] = {
    "mastery_push": (
        "El jugador domina el concepto principal; los enemigos tienen ESCUDOS CUÁNTICOS. "
        "La misión mezcla dos conceptos. El lore debe mencionar protocolos de élite, "
        "tiempo limitado y recompensas épicas."
    ),
    "stealth_review": (
        "El jugador tiene dificultades con este concepto; los escudos enemigos están BAJOS. "
        "El lore debe ser algo como 'Los escudos están bajos, aprovecha para calibrar tus "
        "datos'. La misión es una revisión encubierta: mantén el código simple pero formativo."
    ),
}


async def generate_dynamic_bounty(
    user_level: int,
    target_concept: str,
    difficulty_modifier: float,
    mode_hint: str | None = None,
    second_concept: str | None = None,
) -> dict:
    """
    Genera un reto de Python al vuelo usando Claude Opus 4.6.

    Args:
        user_level: Nivel actual del jugador (1–50).
        target_concept: Concepto de Python principal.
        difficulty_modifier: Dificultad de 1.0 a 10.0.
        mode_hint: 'mastery_push' | 'stealth_review' | None
        second_concept: Concepto secundario a mezclar (solo en mastery_push).

    Returns:
        Dict con title, lore_description, initial_code, expected_output.
    """
    if not settings.ANTHROPIC_API_KEY:
        logger.warning("ANTHROPIC_API_KEY no configurada; usando bounty de fallback.")
        return _FALLBACK_CHALLENGE

    client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

    # Construir descripción del concepto (puede ser una mezcla)
    concept_desc = (
        f"{target_concept} combinado con {second_concept}"
        if second_concept
        else target_concept
    )

    # Prompt base (Prompt 22)
    user_prompt = (
        f"Genera un reto de Python sobre {concept_desc}. "
        f"La dificultad debe ser {difficulty_modifier:.1f} sobre 10. "
        "Devuelve un JSON con: title, lore_description (estilo Cyberpunk), "
        "initial_code (con un bug o incompleto) y expected_output. "
        "No incluyas markdown, solo el JSON raw."
    )

    # Añadir contexto del modo DDA si aplica
    mode_context = _MODE_HINTS.get(mode_hint or "", "")

    system_prompt = (
        "Eres un generador de misiones para un videojuego cyberpunk de programación. "
        "Devuelves EXCLUSIVAMENTE un objeto JSON válido, sin texto adicional, "
        "sin bloques de código markdown, sin explicaciones. "
        f"El jugador está en el nivel {user_level}; ajusta la complejidad al nivel indicado. "
        + (f"\nCONTEXTO DE MISIÓN: {mode_context}" if mode_context else "")
    )

    try:
        response = await client.messages.create(
            model=_MODEL,
            max_tokens=_MAX_TOKENS,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )

        raw = next(
            (block.text for block in response.content if block.type == "text"), ""
        ).strip()

        return json.loads(raw)

    except (json.JSONDecodeError, KeyError, IndexError) as exc:
        logger.error("Error parseando JSON del LLM: %s", exc)
        return _FALLBACK_CHALLENGE
    except anthropic.BadRequestError as exc:
        # Errores conocidos: sin créditos, modelo inválido, etc.
        body = exc.body if hasattr(exc, "body") else {}
        msg = (body or {}).get("error", {}).get("message", str(exc))
        logger.error("BadRequest Anthropic: %s", msg)
        raise RuntimeError(msg) from exc
    except anthropic.APIError as exc:
        logger.error("Error de la API de Anthropic: %s", exc)
        return _FALLBACK_CHALLENGE
