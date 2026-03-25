"""
daki_session_service.py — Gestión de Sesiones con Inteligencia DAKI
────────────────────────────────────────────────────────────────────
6 características del sistema tutora 24/7:

  Feature 1 — Memoria persistente:  DakiSessionLog almacena contexto inter-sesión
  Feature 2 — Voz de apertura:      open_session() genera bienvenida personalizada
  Feature 3 — Pre-anuncio Boss:     check_boss_warning() alerta 2 niveles antes
  Feature 4 — Revisión no solicit.: wire de no_tests_run ya en _PROACTIVE_EVENTS
  Feature 5 — Tono por contexto:    get_tone_for_context() en daki_persona.py
  Feature 6 — Briefing de cierre:   close_session() genera resumen 3 líneas
"""

from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Final

import anthropic
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.concept_mastery import ConceptMastery
from app.models.session_log import DakiSessionLog
from app.services.daki_persona import get_tone_for_context

logger = logging.getLogger(__name__)

# ── Constantes ────────────────────────────────────────────────────────────────

_BOSS_LEVELS: Final[tuple[int, ...]] = (10, 25, 50)
_BOSS_WARN_DISTANCE: Final[int] = 2   # avisar cuando falten N niveles

_OPENING_SYSTEM: Final[str] = (
    "Eres DAKI, mentora táctica de élite del Nexo. El Operador acaba de iniciar sesión. "
    "Genera un briefing de apertura de EXACTAMENTE 3 líneas en español, sin prefijos ni etiquetas:\n"
    "  Línea 1 — Estado del Operador: menciona la racha, nivel o un dato táctico relevante.\n"
    "  Línea 2 — Frente abierto: el concepto con menor maestría o patrón de error detectado. "
    "Si no hay datos, señala qué área suele ser el cuello de botella en este nivel.\n"
    "  Línea 3 — Directiva concreta: la siguiente acción específica que debe ejecutar hoy.\n"
    "Sin saludos, sin elogios, sin 'bienvenido de vuelta'. "
    "Tono: comandante que ya conoce al Operador. Cada línea separada por salto de línea."
)

_CLOSING_SYSTEM: Final[str] = (
    "Eres DAKI, mentora táctica de élite del Nexo. El Operador cierra su sesión. "
    "Genera un briefing de cierre de exactamente 3 líneas en español:\n"
    "  Línea 1: Lo que el Operador consolidó hoy (usa los datos reales).\n"
    "  Línea 2: El frente abierto más urgente (concepto débil o error recurrente).\n"
    "  Línea 3: La siguiente misión táctica para la próxima sesión.\n"
    "Sin elogios. Sin 'hasta pronto'. Tono DAKI operacional."
)


# ── Utilidad privada — LLM de sesión ──────────────────────────────────────────

async def _call_session_llm(system: str, user_msg: str, max_tokens: int = 200) -> str:
    """
    Llama a Haiku para generar mensajes de sesión (apertura/cierre).
    Haiku es suficiente — son mensajes cortos con contexto ligero.
    Retorna string vacío ante cualquier fallo (fallback en el llamador).
    """
    if not settings.ANTHROPIC_API_KEY:
        return ""
    try:
        client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
        response = await client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=max_tokens,
            system=system,
            messages=[{"role": "user", "content": user_msg}],
        )
        text = next(
            (b.text.strip() for b in response.content if getattr(b, "type", None) == "text"),
            None,
        )
        return text or ""
    except Exception as exc:
        logger.error("_call_session_llm falló: %s", exc, exc_info=True)
        return ""


# ── Feature 2: Voz de apertura de sesión ──────────────────────────────────────

async def open_session(
    db:             AsyncSession,
    user_id:        uuid.UUID,
    operator_level: int,
    streak_days:    int,
    callsign:       str,
    hour:           int,
) -> dict:
    """
    Abre una nueva sesión DAKI.

    Flujo:
      1. Recupera el concepto más débil del Operador (ConceptMastery con needs_reinforcement)
      2. Calcula el tono contextual (Feature 5 — hora, racha, errores)
      3. Genera mensaje de bienvenida personalizado vía FAST_MODEL
      4. Persiste el registro en daki_session_logs
      5. Retorna session_id + opening_message + weak_concept

    Args:
        hour: Hora local del Operador (0–23) para calibrar tono día/noche.
    """
    # 1. Conceptos con refuerzo pendiente (el más débil + total)
    weak_result = await db.execute(
        select(ConceptMastery)
        .where(
            ConceptMastery.user_id == user_id,
            ConceptMastery.needs_reinforcement == True,  # noqa: E712
        )
        .order_by(ConceptMastery.mastery_score.asc())
        .limit(5)
    )
    weak_records  = weak_result.scalars().all()
    weak_concept  = weak_records[0].concept_name if weak_records else None
    reinforce_count = len(weak_records)

    # 2. Tono contextual (Feature 5)
    from app.services.semantic_cache import semantic_cache_service
    stats         = semantic_cache_service.get_stats()
    error_tracked = stats.get("total_error_types_tracked", 0)
    tone_directive = get_tone_for_context(
        hour=hour,
        streak_days=streak_days,
        error_count=error_tracked,
    )

    # 3. Prompt para el LLM
    context_parts = [
        f"Operador: {callsign}",
        f"Nivel actual: {operator_level}",
        f"Racha activa: {streak_days} días",
    ]
    if weak_concept:
        weak_names = ", ".join(r.concept_name for r in weak_records)
        context_parts.append(f"Conceptos con refuerzo pendiente ({reinforce_count}): {weak_names}")
    context_parts.append(tone_directive)

    opening_message = await _call_session_llm(
        system=_OPENING_SYSTEM,
        user_msg="\n".join(context_parts),
        max_tokens=160,
    )

    # Fallback sin LLM
    if not opening_message:
        if streak_days >= 3:
            opening_message = (
                f"Racha activa: {streak_days} días, {callsign}. "
                "El Nexo te espera. Misiones pendientes en cola."
            )
        elif weak_concept:
            opening_message = (
                f"Operador {callsign}. Frente abierto detectado: [{weak_concept}]. "
                "Ese concepto necesita refuerzo antes de avanzar."
            )
        else:
            opening_message = (
                f"Operador {callsign}. Nivel {operator_level}. "
                "Nexo conectado. Ejecuta la primera misión."
            )

    # 4. Persistir
    session = DakiSessionLog(
        user_id=user_id,
        opened_at=datetime.now(timezone.utc),
        operator_level=operator_level,
        streak_days=streak_days,
        weak_concept=weak_concept,
        opening_message=opening_message,
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)

    logger.info("Sesión abierta → user=%s | nivel=%d | session=%s", user_id, operator_level, session.id)

    return {
        "session_id":      str(session.id),
        "opening_message": opening_message,
        "weak_concept":    weak_concept,
    }


# ── Feature 6: Briefing de cierre de sesión ───────────────────────────────────

async def close_session(
    db:                   AsyncSession,
    session_id:           uuid.UUID,
    challenges_completed: int,
    challenges_attempted: int,
    hints_requested:      int,
    dominant_error_type:  str | None = None,
) -> dict:
    """
    Cierra la sesión y genera un briefing de 3 líneas.

    Flujo:
      1. Carga el registro de sesión por session_id
      2. Construye contexto con métricas de la sesión
      3. Llama al LLM para generar el briefing personalizado
      4. Actualiza el registro con métricas + briefing + closed_at
      5. Retorna el briefing

    Retorna {"briefing": ""} si la sesión no existe (tolerante a IDs stale).
    """
    session = await db.get(DakiSessionLog, session_id)
    if session is None:
        logger.warning("close_session: sesión %s no encontrada", session_id)
        return {"briefing": ""}

    # Contexto para el LLM
    context_parts = [
        f"Misiones completadas: {challenges_completed}/{challenges_attempted}",
        f"Pistas solicitadas: {hints_requested}",
        f"Nivel del Operador: {session.operator_level}",
        f"Racha: {session.streak_days} días",
    ]
    if session.weak_concept:
        context_parts.append(f"Concepto con refuerzo pendiente: {session.weak_concept}")
    if dominant_error_type:
        context_parts.append(f"Error más frecuente en sesión: {dominant_error_type}")

    closing_briefing = await _call_session_llm(
        system=_CLOSING_SYSTEM,
        user_msg="\n".join(context_parts),
        max_tokens=200,
    )

    # Fallback sin LLM
    if not closing_briefing:
        lines = [
            f"Sesión: {challenges_completed} misiones completadas de {challenges_attempted}.",
            f"Frente abierto: {session.weak_concept or 'Sin datos — continúa ejecutando misiones'}.",
            "Siguiente operación: primera misión sin pistas. Mide tu avance real.",
        ]
        closing_briefing = "\n".join(lines)

    # Actualizar registro
    session.closed_at            = datetime.now(timezone.utc)
    session.challenges_completed = challenges_completed
    session.challenges_attempted = challenges_attempted
    session.hints_requested      = hints_requested
    session.dominant_error_type  = dominant_error_type
    session.closing_briefing     = closing_briefing
    await db.commit()

    logger.info("Sesión cerrada → session=%s | completadas=%d/%d", session_id, challenges_completed, challenges_attempted)

    return {"briefing": closing_briefing}


# ── Feature 3: Pre-anuncio de Boss Battle ─────────────────────────────────────

def check_boss_warning(operator_level: int) -> dict:
    """
    Verifica si el Operador está próximo a un Boss Battle.

    Bosses en niveles: 10, 25, 50.
    Alerta cuando faltan <= _BOSS_WARN_DISTANCE niveles.

    Returns:
        {
            "warning":     bool,
            "boss_level":  int | None,
            "levels_away": int | None,
            "message":     str | None,
        }
    """
    for boss in _BOSS_LEVELS:
        distance = boss - operator_level
        if 0 < distance <= _BOSS_WARN_DISTANCE:
            return {
                "warning":     True,
                "boss_level":  boss,
                "levels_away": distance,
                "message": (
                    f"[ALERTA TÁCTICA] Boss Battle en Nivel {boss} detectado. "
                    f"Faltan {distance} misión(es). "
                    "Refuerza los conceptos débiles antes de enfrentarlo, Operador. "
                    "Los Boss Battles no tienen pistas — solo tú y el código."
                ),
            }

    return {"warning": False, "boss_level": None, "levels_away": None, "message": None}
