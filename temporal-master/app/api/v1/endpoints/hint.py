import json as _json
import uuid

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.rate_limit import limiter
from app.models.challenge import Challenge
from app.models.user_progress import UserProgress
from app.services import ai_mentor
from app.services.mastery_service import get_reinforcement_concepts
from app.services.memory_service import (
    format_operator_history,
    get_recent_events,
    record_event,
)

router = APIRouter()


class HintRequest(BaseModel):
    user_id: uuid.UUID
    challenge_id: uuid.UUID
    source_code: str
    error_output: str = ""
    error_type: str = ""       # tipo limpio extraído en el frontend (e.g. "NameError")
    fail_count: int = 1        # número de intentos fallidos → calibra el nivel de pista DAKI
    operator_level: int = 1    # nivel actual del Operador → calibra etapa DAKI


class HintResponse(BaseModel):
    hint: str
    questions: list[str] = []   # Modo Socrático: preguntas guía para fail_count == 1


@router.post(
    "/hint",
    response_model=HintResponse,
    status_code=status.HTTP_200_OK,
    summary="Solicita una pista de ENIGMA para el desafío actual",
    description=(
        "Llama al mentor IA (ENIGMA) para obtener una pista de máximo 2 líneas "
        "cuando el usuario lleva 3 o más intentos fallidos en un desafío Python."
    ),
)
@limiter.limit("10/minute")
async def request_hint(
    request: Request,
    payload: HintRequest,
    db: AsyncSession = Depends(get_db),
) -> HintResponse:
    challenge = await db.get(Challenge, payload.challenge_id)
    if challenge is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Desafío no encontrado.",
        )

    # Registra la pista en la telemetría del progreso del usuario
    prog_result = await db.execute(
        select(UserProgress).where(
            UserProgress.user_id == payload.user_id,
            UserProgress.challenge_id == payload.challenge_id,
        )
    )
    progress = prog_result.scalar_one_or_none()
    if progress is None:
        progress = UserProgress(
            user_id=payload.user_id,
            challenge_id=payload.challenge_id,
            hints_used=0,
        )
        db.add(progress)
    progress.hints_used = (progress.hints_used or 0) + 1

    # ── Memoria Evolutiva: registrar error_frecuente y recuperar historial ─────
    resolved_error_type = payload.error_type or (payload.error_output[:120] if payload.error_output else "")
    if payload.fail_count >= 2:
        await record_event(
            db=db,
            user_id=payload.user_id,
            event_type="error_frecuente",
            context_data={
                "challenge_title": challenge.title,
                "fail_count": payload.fail_count,
                "error_type": resolved_error_type,
            },
            challenge_id=payload.challenge_id,
        )

    recent_events = await get_recent_events(db, payload.user_id, limit=5)
    operator_history = format_operator_history(recent_events)

    # ── Extraer intel de la misión desde la DB ────────────────────────────────
    concepts_taught: list[str] = []
    try:
        raw = challenge.concepts_taught_json
        if raw:
            parsed = _json.loads(raw)
            if isinstance(parsed, list):
                concepts_taught = [str(c) for c in parsed]
    except Exception:
        pass

    db_hints: list[str] = []
    try:
        raw = challenge.hints_json
        if raw:
            parsed = _json.loads(raw)
            if isinstance(parsed, list):
                db_hints = [str(h) for h in parsed]
    except Exception:
        pass

    # ── DAKI Memory: conceptos con baja maestría → refuerzo contextual ───────
    weak_concepts: list[str] = await get_reinforcement_concepts(db, payload.user_id)

    hint = await ai_mentor.get_hint(
        challenge_title=challenge.title,
        challenge_description=challenge.description,
        source_code=payload.source_code,
        error_output=payload.error_output,
        error_type=resolved_error_type,
        fail_count=max(1, payload.fail_count),
        operator_history=operator_history,
        concepts_taught=concepts_taught,
        pedagogical_objective=challenge.pedagogical_objective or None,
        syntax_hint=challenge.syntax_hint or None,
        db_hints=db_hints,
        operator_level=max(1, payload.operator_level),
        weak_concepts=weak_concepts or None,
    )

    # ── Modo Socrático: solo en el primer intento (fail_count == 1) ───────────
    # Genera 2 preguntas guía para que el Operador razone antes de ver la pista.
    questions: list[str] = []
    if payload.fail_count <= 1:
        import anthropic as _anthropic
        from app.core.config import settings as _settings
        from app.services.daki_persona import DAKI_SYSTEM_PROMPT as _SYS
        _socratic_directive = (
            "[DIRECTIVA: MODO SOCRÁTICO]\n"
            "Genera EXACTAMENTE 2 preguntas breves (una por línea) que guíen al Operador "
            "a descubrir el error por sí mismo, sin revelar la solución. "
            "Las preguntas deben referirse al código y al error específico. "
            "Solo las preguntas, sin numeración, sin preámbulo.\n\n"
            f"Misión: {challenge.title}\n"
            f"Error del Operador: {resolved_error_type or 'sin error de tipo'}\n"
            f"Código:\n```python\n{payload.source_code[:600]}\n```"
        )
        try:
            _client = _anthropic.AsyncAnthropic(api_key=_settings.ANTHROPIC_API_KEY)
            _resp = await _client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=100,
                system=_SYS,
                messages=[{"role": "user", "content": _socratic_directive}],
            )
            _text = next(
                (b.text.strip() for b in _resp.content if getattr(b, "type", None) == "text"), ""
            )
            questions = [q.strip() for q in _text.splitlines() if q.strip()][:2]
        except Exception:
            pass  # Socrático no es crítico — fallback a pista directa

    await db.commit()
    return HintResponse(hint=hint, questions=questions)
