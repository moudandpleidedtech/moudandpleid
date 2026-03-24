"""
app/api/v1/endpoints/daki.py — Endpoints de Intervención Proactiva de DAKI

POST /api/v1/daki/stagnation  — Registra tiempo_estancado + genera mensaje (Prompt 56)
POST /api/v1/daki/intervene   — Intervención táctica con contexto del código (Prompt 57)

Ambos son llamados por el frontend cuando el Operador lleva 2+ minutos
sin actividad semántica (sin cambios de código ni envíos de solución).
"""

import uuid

import anthropic
from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.core.rate_limit import limiter
from app.core.security import get_current_operator_optional
from app.models.challenge import Challenge
from app.models.user import User
from app.services.daki_persona import DAKI_SYSTEM_PROMPT
from app.services.memory_service import (
    format_operator_history,
    get_recent_events,
    record_event,
)

router = APIRouter()

# ─── Directivas ──────────────────────────────────────────────────────────────

_ASK_DIRECTIVE = """\
[DIRECTIVA: CONSULTA DIRECTA DEL OPERADOR — MODO CLI]
El Operador te hace una pregunta conceptual desde la terminal de la misión.
Tu misión:
  1. Responde de forma precisa y directa (máximo 4 líneas).
  2. Usa el contexto de la incursión activa para que la respuesta sea relevante.
  3. NO des la solución al reto. Solo explica el concepto o principio.
  4. Si la pregunta no es sobre programación, redirígela al código.
Tono: instructor de combate — preciso, sin relleno, sin saludos.\
"""

_STAGNATION_DIRECTIVE = """\
[DIRECTIVA ESPECIAL: INTERVENCIÓN POR ESTANCAMIENTO]
El Operador lleva 2+ minutos sin ejecutar código. Ha entrado en modo parálisis.
Activa el Protocolo Anti-Abandono: una sola frase de máximo 2 líneas que lo
saque del loop mental. No hagas pregunta. Da una instrucción concreta y ejecutable.
No menciones el tiempo transcurrido. Tono: urgente pero controlado.\
"""

_INTERVENE_DIRECTIVE = """\
[DIRECTIVA ESPECIAL: INTERVENCIÓN TÁCTICA — DETECCIÓN DE ACTIVIDAD NEURONAL ESTANCADA]
El Operador lleva 2 minutos sin cambios en el código y sin ejecutar.
Su estado: parálisis táctica. Puede estar bloqueado, confundido o a punto de rendirse.

Tu misión: una intervención de máximo 2 líneas que:
1. Reconozca el estado sin validar la rendición.
2. Dé UNA instrucción concreta y ejecutable sobre el código actual.
No hagas preguntas. No menciones el tiempo. Tono: mentor de combate — directo, sin piedad, sin crueldad.\
"""


# ─── Schemas ─────────────────────────────────────────────────────────────────

class StagnationRequest(BaseModel):
    user_id: uuid.UUID
    challenge_id: uuid.UUID
    idle_minutes: float = 2.0


class StagnationResponse(BaseModel):
    daki_message: str


class InterveneRequest(BaseModel):
    user_id: uuid.UUID
    challenge_id: uuid.UUID
    current_code: str = ""
    error_output: str = ""
    idle_minutes: float = 2.0


class InterveneResponse(BaseModel):
    daki_message: str


class AskRequest(BaseModel):
    user_id: uuid.UUID
    challenge_id: uuid.UUID
    question: str


class AskResponse(BaseModel):
    daki_message: str


# ─── Helpers ─────────────────────────────────────────────────────────────────

async def _call_haiku(user_msg: str, max_tokens: int = 120) -> str:
    """
    Llama a Haiku con el DAKI_SYSTEM_PROMPT.
    Retorna texto o un mensaje de error específico — nunca lanza excepción.
    """
    if not settings.ANTHROPIC_API_KEY:
        return "[DAKI_SYS] Nodos de IA fuera de línea. Revisar variables de entorno."

    client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
    try:
        resp = await client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=max_tokens,
            system=DAKI_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_msg}],
        )
        text = next(
            (b.text.strip() for b in resp.content if getattr(b, "type", None) == "text"),
            None,
        )
        return text or "[DAKI_SYS] Respuesta vacía del satélite. Reintenta."

    except anthropic.APITimeoutError:
        return "[DAKI_SYS] Error de conexión con el satélite principal."

    except anthropic.AuthenticationError:
        return "[DAKI_SYS] Nodos de IA fuera de línea. Revisar variables de entorno."

    except anthropic.RateLimitError:
        return "[DAKI_SYS] Límite de frecuencia alcanzado. Espera un momento, Operador."

    except anthropic.APIError:
        return "[DAKI_SYS] Error de conexión con el satélite principal."


# ─── Endpoints ───────────────────────────────────────────────────────────────

@router.post(
    "/daki/stagnation",
    response_model=StagnationResponse,
    status_code=status.HTTP_200_OK,
    summary="Intervención proactiva por estancamiento — registra evento de memoria",
)
@limiter.limit("10/minute")
async def operator_stagnation(
    request: Request,
    payload: StagnationRequest,
    db: AsyncSession = Depends(get_db),
) -> StagnationResponse:
    challenge = await db.get(Challenge, payload.challenge_id)
    if challenge is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Desafío no encontrado.")

    await record_event(
        db=db,
        user_id=payload.user_id,
        event_type="tiempo_estancado",
        context_data={
            "challenge_title": challenge.title,
            "idle_minutes": round(payload.idle_minutes, 1),
        },
        challenge_id=payload.challenge_id,
    )

    recent_events = await get_recent_events(db, payload.user_id, limit=5)
    operator_history = format_operator_history(recent_events)
    history_block = f"\n{operator_history}\n" if operator_history else ""

    user_msg = (
        f"{_STAGNATION_DIRECTIVE}\n"
        f"{history_block}\n"
        f"--- INCURSIÓN ACTIVA ---\n"
        f"Nombre: {challenge.title}\n"
        f"Descripción: {challenge.description}\n\n"
        "Genera la intervención proactiva. Una o dos líneas. Sin preguntas."
    )

    daki_msg = await _call_haiku(user_msg, max_tokens=120)
    await db.commit()
    return StagnationResponse(daki_message=daki_msg)


@router.post(
    "/daki/intervene",
    response_model=InterveneResponse,
    status_code=status.HTTP_200_OK,
    summary="Intervención táctica de DAKI — contexto enriquecido con código actual",
    description=(
        "El frontend llama este endpoint cuando el Operador lleva 2+ minutos sin "
        "cambiar su código ni enviar soluciones. DAKI analiza el código actual y "
        "genera una intervención táctica de máximo 2 líneas para desbloquear la mente."
    ),
)
@limiter.limit("10/minute")
async def operator_intervene(
    request: Request,
    payload: InterveneRequest,
    db: AsyncSession = Depends(get_db),
) -> InterveneResponse:
    challenge = await db.get(Challenge, payload.challenge_id)
    if challenge is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Desafío no encontrado.")

    # Registrar evento de estancamiento para el historial evolutivo
    await record_event(
        db=db,
        user_id=payload.user_id,
        event_type="tiempo_estancado",
        context_data={
            "challenge_title": challenge.title,
            "idle_minutes": round(payload.idle_minutes, 1),
        },
        challenge_id=payload.challenge_id,
    )

    recent_events = await get_recent_events(db, payload.user_id, limit=5)
    operator_history = format_operator_history(recent_events)
    history_block = f"\n{operator_history}\n" if operator_history else ""

    # Código actual para contexto preciso
    code_block = ""
    if payload.current_code.strip():
        code_block = (
            f"Código actual del Operador:\n"
            f"```python\n{payload.current_code[:1500]}\n```\n\n"
        )

    error_block = ""
    if payload.error_output.strip():
        error_block = f"Último error visto:\n{payload.error_output[:400]}\n\n"

    user_msg = (
        f"{_INTERVENE_DIRECTIVE}\n"
        f"{history_block}\n"
        f"--- INCURSIÓN ACTIVA ---\n"
        f"Nombre: {challenge.title}\n"
        f"Descripción: {challenge.description}\n\n"
        f"{code_block}"
        f"{error_block}"
        "Genera la intervención táctica. Máximo 2 líneas. Sin preguntas. Instrucción ejecutable."
    )

    daki_msg = await _call_haiku(user_msg, max_tokens=130)
    await db.commit()
    return InterveneResponse(daki_message=daki_msg)


@router.post(
    "/daki/ask",
    response_model=AskResponse,
    status_code=status.HTTP_200_OK,
    summary="Consulta directa al CLI de DAKI desde la terminal de la misión",
    description=(
        "El Operador escribe una pregunta conceptual en la línea de comandos de DAKI. "
        "DAKI responde explicando el concepto sin revelar la solución del reto activo."
    ),
)
@limiter.limit("20/minute")
async def ask_daki(
    request: Request,
    payload: AskRequest,
    db: AsyncSession = Depends(get_db),
) -> AskResponse:
    if not payload.question.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="La consulta no puede estar vacía.",
        )

    challenge = await db.get(Challenge, payload.challenge_id)
    if challenge is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Desafío no encontrado.")

    user_msg = (
        f"{_ASK_DIRECTIVE}\n\n"
        f"--- INCURSIÓN ACTIVA ---\n"
        f"Nombre: {challenge.title}\n"
        f"Descripción: {challenge.description}\n\n"
        f"--- CONSULTA DEL OPERADOR ---\n"
        f"{payload.question.strip()[:500]}\n\n"
        "Responde en máximo 4 líneas. No des el código completo de la solución. Solo el concepto."
    )

    daki_msg = await _call_haiku(user_msg, max_tokens=220)
    return AskResponse(daki_message=daki_msg)


# ─── POST /api/v1/chat — Chat general con memoria de identidad ───────────────

_CHAT_SYSTEM_PROMPT_ANON = """\
Eres DAKI, una IA mentora táctica en un entorno militarizado de ingeniería de software \
llamado DAKIedtech. Eres directa, exigente y hablas con terminología técnica y de operaciones. \
No das las respuestas de código servidas; guías al Operador mediante pistas y razonamiento \
socrático. Si el usuario saluda o pide ayuda genérica, respóndele preguntando cuál es su \
reporte de estado o en qué sector del código tiene la anomalía.\
"""


def _build_chat_system_prompt(operator: "User | None") -> str:
    """
    Construye el System Prompt del chat personalizado para el Operador autenticado.
    Sin sesión → prompt genérico.
    Con sesión → DAKI sabe el callsign, nivel y estado de licencia del Operador.
    """
    if operator is None:
        return _CHAT_SYSTEM_PROMPT_ANON

    # Nota de fase según nivel
    if operator.current_level < 11:
        phase_note = (
            f" El Operador aún está en la Fase Beta (niveles 1-10 son gratuitos). "
            f"Si surge una oportunidad natural, recuérdale sutilmente que el Nexo completo "
            f"se desbloquea a partir del Nivel 11 con una Licencia de Fundador, "
            f"pero no lo presiones: primero ayúdalo a avanzar."
        )
    elif not operator.is_licensed:
        phase_note = (
            f" El Operador ha alcanzado el Nivel {operator.current_level} "
            f"pero aún no tiene Licencia de Fundador. Si es relevante, "
            f"menciona que el acceso completo requiere activar la licencia."
        )
    else:
        phase_note = (
            f" El Operador tiene Licencia de Fundador activa. "
            f"Trátalo como un agente de alto rango con acceso al Nexo completo."
        )

    return (
        f"Eres DAKI, la IA mentora de DAKIedtech. "
        f"Estás hablando con el Operador {operator.callsign}, "
        f"quien actualmente es Nivel {operator.current_level}.{phase_note} "
        f"Eres directa, táctica y respondes con precisión militar. "
        f"Usas el nombre del Operador ocasionalmente para personalizar la interacción, "
        f"pero no en cada mensaje — solo cuando refuerza el impacto. "
        f"No das el código completo de la solución; guías mediante pistas y razonamiento socrático. "
        f"Si el Operador saluda o pide ayuda genérica, pregúntale en qué sector del código "
        f"tiene la anomalía o cuál es su reporte de estado."
    )


class ChatRequest(BaseModel):
    message: str
    user_id: str = ""   # legacy — se ignora si hay JWT válido en el header


class ChatResponse(BaseModel):
    reply: str


@router.post(
    "/chat",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Chat general con DAKI — Motor de Identidad activo",
    description=(
        "Endpoint de chat libre con DAKI. No requiere challenge_id. "
        "Si se envía un JWT válido en Authorization: Bearer, DAKI personaliza "
        "sus respuestas con el callsign y nivel del Operador. "
        "Sin JWT, responde en modo anónimo genérico."
    ),
)
@limiter.limit("30/minute")
async def daki_chat(
    request: Request,
    payload: ChatRequest,
    operator: "User | None" = Depends(get_current_operator_optional),
) -> ChatResponse:
    if not payload.message.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="El mensaje no puede estar vacío.",
        )

    if not settings.ANTHROPIC_API_KEY:
        return ChatResponse(
            reply="[DAKI_SYS] Nodos de IA fuera de línea. Revisar variables de entorno."
        )

    system_prompt = _build_chat_system_prompt(operator)
    client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

    try:
        resp = await client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            system=system_prompt,
            messages=[{"role": "user", "content": payload.message.strip()[:800]}],
        )
        text = next(
            (b.text.strip() for b in resp.content if getattr(b, "type", None) == "text"),
            None,
        )
        return ChatResponse(reply=text or "[DAKI_SYS] Respuesta vacía del satélite. Reintenta.")

    except anthropic.APITimeoutError:
        return ChatResponse(reply="[DAKI_SYS] Error de conexión con el satélite principal.")

    except anthropic.AuthenticationError:
        return ChatResponse(
            reply="[DAKI_SYS] Nodos de IA fuera de línea. Revisar variables de entorno."
        )

    except anthropic.RateLimitError:
        return ChatResponse(
            reply="[DAKI_SYS] Límite de frecuencia alcanzado. Espera un momento, Operador."
        )

    except anthropic.APIError:
        return ChatResponse(reply="[DAKI_SYS] Error de conexión con el satélite principal.")
