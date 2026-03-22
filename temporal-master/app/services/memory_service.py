"""
memory_service.py — Módulo de Memoria Evolutiva de DAKI (Prompt 56)

Persiste eventos clave del Operador y formatea un historial comprimido
para inyección en el contexto del LLM como sección OPERATOR_HISTORY.

Eventos registrados:
    error_frecuente  — fail_count >= 2 en la misma incursión
    exito_rapido     — resuelto en el primer intento
    tiempo_estancado — inactividad >= 2 minutos detectada por el frontend
    subida_rango     — ascenso de rango en gamification_service
"""

import json
import uuid

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_core_memory import UserCoreMemory


# ─── Escritura ────────────────────────────────────────────────────────────────

async def record_event(
    db: AsyncSession,
    user_id: uuid.UUID,
    event_type: str,
    context_data: dict,
    challenge_id: uuid.UUID | None = None,
) -> None:
    """Persiste un evento de memoria para el Operador. Hace flush pero no commit."""
    record = UserCoreMemory(
        user_id=user_id,
        challenge_id=challenge_id,
        event_type=event_type,
        context_data=json.dumps(context_data, ensure_ascii=False),
    )
    db.add(record)
    await db.flush()


# ─── Lectura ──────────────────────────────────────────────────────────────────

async def get_recent_events(
    db: AsyncSession,
    user_id: uuid.UUID,
    limit: int = 5,
) -> list[UserCoreMemory]:
    """Devuelve los últimos N eventos del Operador ordenados más-reciente-primero."""
    result = await db.execute(
        select(UserCoreMemory)
        .where(UserCoreMemory.user_id == user_id)
        .order_by(desc(UserCoreMemory.created_at))
        .limit(limit)
    )
    return list(result.scalars().all())


# ─── Formateo para LLM ────────────────────────────────────────────────────────

def format_operator_history(events: list[UserCoreMemory]) -> str:
    """
    Convierte la lista de eventos en la sección OPERATOR_HISTORY que se
    inyecta en el mensaje de usuario enviado al LLM.

    Retorna string vacío si no hay eventos (sin sección innecesaria).
    """
    if not events:
        return ""

    lines = ["[OPERATOR_HISTORY — Perfil de Comportamiento Reciente]"]
    for ev in reversed(events):   # orden cronológico (más antiguo primero)
        ctx: dict = {}
        try:
            ctx = json.loads(ev.context_data)
        except Exception:
            pass

        ts = ev.created_at.strftime("%H:%M") if ev.created_at else "?"

        if ev.event_type == "error_frecuente":
            lines.append(
                f"  [{ts}] ERROR_RECURRENTE — Misión: {ctx.get('challenge_title', '?')} "
                f"— Tipo: {ctx.get('error_type', '?')} — Fallas: {ctx.get('fail_count', '?')}"
            )
        elif ev.event_type == "exito_rapido":
            lines.append(
                f"  [{ts}] EXITO_RAPIDO — Misión: {ctx.get('challenge_title', '?')} "
                f"— Resuelto en primer intento"
            )
        elif ev.event_type == "tiempo_estancado":
            lines.append(
                f"  [{ts}] ESTANCAMIENTO — Misión: {ctx.get('challenge_title', '?')} "
                f"— {ctx.get('idle_minutes', 2)} min inactivo"
            )
        elif ev.event_type == "subida_rango":
            lines.append(
                f"  [{ts}] ASCENSO_RANGO — {ctx.get('old_rank', '?')} → {ctx.get('new_rank', '?')}"
            )
        else:
            lines.append(f"  [{ts}] {ev.event_type.upper()} — {ctx}")

    lines.append(
        "Usa este historial para calibrar el tono y el nivel de intervención. "
        "Un Operador con múltiples ERROR_RECURRENTE necesita reframing; "
        "uno con EXITO_RAPIDO puede tolerar pistas más concisas."
    )
    return "\n".join(lines)
