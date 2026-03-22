"""
app/api/v1/endpoints/daki.py — Endpoints de Intervención Proactiva de DAKI

POST /api/v1/daki/stagnation  — Registra tiempo_estancado + genera mensaje (Prompt 56)
POST /api/v1/daki/intervene   — Intervención táctica con contexto del código (Prompt 57)

Ambos son llamados por el frontend cuando el Operador lleva 2+ minutos
sin actividad semántica (sin cambios de código ni envíos de solución).
"""

import uuid

import anthropic
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.models.challenge import Challenge
from app.services.daki_persona import DAKI_SYSTEM_PROMPT
from app.services.memory_service import (
    format_operator_history,
    get_recent_events,
    record_event,
)

router = APIRouter()

# ─── Directivas ──────────────────────────────────────────────────────────────

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


# ─── Helpers ─────────────────────────────────────────────────────────────────

async def _call_haiku(user_msg: str, max_tokens: int = 120) -> str:
    """Llama a Haiku con el DAKI_SYSTEM_PROMPT. Retorna texto o fallback offline."""
    if not settings.ANTHROPIC_API_KEY:
        return (
            "// [DAKI] Red Central sin señal. "
            "Operador: ejecuta cualquier cosa ahora. El movimiento rompe el bloqueo."
        )
    client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
    resp = await client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=max_tokens,
        system=DAKI_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_msg}],
    )
    return resp.content[0].text.strip()


# ─── Endpoints ───────────────────────────────────────────────────────────────

@router.post(
    "/daki/stagnation",
    response_model=StagnationResponse,
    status_code=status.HTTP_200_OK,
    summary="Intervención proactiva por estancamiento — registra evento de memoria",
)
async def operator_stagnation(
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
async def operator_intervene(
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
