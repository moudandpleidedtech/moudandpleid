"""
DAKI — Instructora IA táctica para DAKI EdTech.

Usa la API de Claude (Anthropic) para generar pistas concisas cuando el usuario
falla repetidamente en un desafío. La pista tiene máximo 2 líneas, estilo cyberpunk
cálido, y NUNCA revela la solución completa.
"""

import anthropic

from app.core.config import settings

_SYSTEM_PROMPT = """\
Eres DAKI, la instructora táctica de DAKI EdTech. Tienes un tono cálido pero directo,
como una mentora que quiere que el operador aprenda, no que dependa de ti.
Tu función exclusiva: dar UNA pista de máximo 2 líneas sobre el error de Python del usuario.

Reglas absolutas:
- Máximo 2 líneas. Sin introducción. Sin despedida.
- NUNCA escribas el código corregido ni la solución completa.
- Usa vocabulario técnico-cyberpunk: "fragmento", "protocolo", "secuencia", "módulo", "núcleo".
- Si el error es de sintaxis, señala la línea o el símbolo en cuestión.
- Si la lógica está mal, da una pista conceptual sin revelar el algoritmo.
- Tono: cálido, directo, empoderador. El operador debe sentir que puede lograrlo.
"""

_FALLBACK = (
    "// DAKI fuera de línea — clave API no configurada.\n"
    "// Revisa el stderr o el valor que estás retornando."
)


async def get_hint(
    challenge_title: str,
    challenge_description: str,
    source_code: str,
    error_output: str,
) -> str:
    """
    Llama a Claude y devuelve una pista de máximo 2 líneas en estilo DAKI EdTech.
    Si la clave no está configurada, devuelve un mensaje de fallback.
    """
    if not settings.ANTHROPIC_API_KEY:
        return _FALLBACK

    client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

    user_msg = (
        f"Desafío: {challenge_title}\n"
        f"Descripción: {challenge_description}\n\n"
        f"Código del usuario:\n```python\n{source_code[:2000]}\n```\n\n"
        f"Salida / Error obtenido:\n{error_output[:500]}\n\n"
        "Dame la pista (máximo 2 líneas)."
    )

    message = await client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=120,
        system=_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_msg}],
    )

    return message.content[0].text.strip()
