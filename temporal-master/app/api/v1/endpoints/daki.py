"""
POST /api/v1/daki/stagnation — Intervención Proactiva de DAKI (Prompt 56)

El frontend detecta 2 minutos de inactividad y llama este endpoint para:
1. Registrar el evento tiempo_estancado en UserCoreMemory.
2. Generar un mensaje de intervención proactiva de DAKI.
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

_STAGNATION_DIRECTIVE = """\
[DIRECTIVA ESPECIAL: INTERVENCIÓN POR ESTANCAMIENTO]
El Operador lleva 2+ minutos sin ejecutar código. Ha entrado en modo parálisis.
Activa el Protocolo Anti-Abandono: una sola frase de máximo 2 líneas que lo
saque del loop mental. No hagas pregunta. Da una instrucción concreta y ejecutable.
No menciones el tiempo transcurrido. Tono: urgente pero controlado.\
"""


class StagnationRequest(BaseModel):
    user_id: uuid.UUID
    challenge_id: uuid.UUID
    idle_minutes: float = 2.0    # minutos de inactividad detectados por el frontend


class StagnationResponse(BaseModel):
    daki_message: str            # frase de intervención proactiva


@router.post(
    "/daki/stagnation",
    response_model=StagnationResponse,
    status_code=status.HTTP_200_OK,
    summary="Intervención proactiva de DAKI por estancamiento del Operador",
    tags=["daki"],
)
async def operator_stagnation(
    payload: StagnationRequest,
    db: AsyncSession = Depends(get_db),
) -> StagnationResponse:
    challenge = await db.get(Challenge, payload.challenge_id)
    if challenge is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Desafío no encontrado.",
        )

    # Registrar evento de estancamiento
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

    # Recuperar historial para contexto
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

    if settings.ANTHROPIC_API_KEY:
        client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
        resp = await client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=120,
            system=DAKI_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_msg}],
        )
        daki_msg = resp.content[0].text.strip()
    else:
        daki_msg = (
            "// [DAKI] Red Central sin señal. "
            "Operador: ejecuta cualquier cosa ahora. El movimiento rompe el bloqueo."
        )

    await db.commit()
    return StagnationResponse(daki_message=daki_msg)
