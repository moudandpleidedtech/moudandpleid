"""
intercept.py — Endpoints del Protocolo de Memoria Muscular

GET  /api/v1/intercept/check?user_id=X&challenge_id=Y
     Verifica si DAKI debe interceptar el avance del Operador.
     Responde con intercept=false (libre paso) o intercept=true + la Micro-Misión.

POST /api/v1/intercept/{interception_id}/submit
     El Operador envía su solución a la Micro-Misión.
     Si es correcta → marca la intercepción como "passed" y libera el avance.
     Si es incorrecta → devuelve feedback de DAKI + estado "pending".

POST /api/v1/intercept/{interception_id}/skip
     El Operador ignora la Micro-Misión (solo DAKI nivel 1 lo permite sin penalidad).
     Marca la intercepción como "expired" para no bloquear el flujo.

────────────────────────────────────────────────────────────────────────────────
Integración en el flujo de validación de progreso:

  El frontend llama a GET /intercept/check ANTES de cargar el editor.

  Flujo normal:
    GET /challenge/:id       → datos del nivel
    GET /intercept/check     → {"intercept": false}  → editor listo
    POST /evaluate           → evalúa el código

  Flujo interceptado:
    GET /challenge/:id       → datos del nivel
    GET /intercept/check     → {"intercept": true, "mision": {...}}
    [Muestra el MisionFlashModal]
    POST /intercept/:id/submit → {"passed": true}  → editor del nivel original
    POST /evaluate             → evalúa el nivel original
"""

import json
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.challenge import Challenge
from app.services.evaluation_service import (
    EvaluacionResult,
    _ast_guard,
    _execute_isolated,
    _normalizar_strict,
    normalizar_salida,
    _EXEC_TIMEOUT_S,
)
from app.services.memoria_muscular import (
    InterceptResult,
    MisionFlash,
    completar_intercepcion,
    generar_mision_flash,
    registrar_intento_flash,
    verificar_intercepcion,
)
from app.models.daki_interception import DakiInterception
from app.services.daki_intel import get_daki_message

import asyncio
import concurrent.futures

router = APIRouter(prefix="/intercept", tags=["intercept"])


# ─── Schemas de respuesta ─────────────────────────────────────────────────────

class MisionFlashOut(BaseModel):
    concept_name: str
    title: str
    description: str
    lore_briefing: str
    initial_code: str
    hints: list[str]
    difficulty: str
    estimated_lines: int
    # expected_output NO se expone al frontend (evita trampas)


class InterceptCheckResponse(BaseModel):
    intercept: bool
    interception_id: uuid.UUID | None = None
    mision: MisionFlashOut | None = None
    daki_message: str = ""
    # Stats del concepto débil (útil para el UI)
    concept_name: str | None = None
    mastery_score: float | None = None
    sector_ensenado: int | None = None


class FlashSubmitRequest(BaseModel):
    user_id: uuid.UUID
    code: str
    daki_level: int = 1


class FlashSubmitResponse(BaseModel):
    passed: bool
    output_got: str = ""
    output_expected: str = ""   # revelado solo si falló, para feedback inmediato
    stdout: str = ""
    daki_message: str = ""
    attempts: int = 0
    status: str = ""            # "success" | "failed" | "error" | "timeout"


# ─── Thread pool compartido (reutiliza el del evaluation_service) ─────────────
_THREAD_POOL = concurrent.futures.ThreadPoolExecutor(
    max_workers=2, thread_name_prefix="gg-flash"
)


# ─────────────────────────────────────────────────────────────────────────────
# GET /intercept/check
# ─────────────────────────────────────────────────────────────────────────────

@router.get(
    "/check",
    response_model=InterceptCheckResponse,
    summary="Verifica si DAKI intercepta el avance del Operador",
    description=(
        "Consultar ANTES de cargar el editor de un nivel. "
        "Si intercept=true, el frontend debe mostrar el MisionFlashModal "
        "en vez de dejar que el Operador acceda al nivel directamente."
    ),
)
async def check_interception(
    user_id: uuid.UUID = Query(..., description="UUID del Operador"),
    challenge_id: uuid.UUID = Query(..., description="UUID del nivel que intenta acceder"),
    db: AsyncSession = Depends(get_db),
) -> InterceptCheckResponse:
    # Carga el challenge
    challenge = await db.get(Challenge, challenge_id)
    if challenge is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nivel no encontrado.",
        )

    result: InterceptResult = await verificar_intercepcion(db, user_id, challenge)

    if not result.intercept:
        return InterceptCheckResponse(intercept=False)

    # Construye la respuesta con la misión (sin exponer expected_output)
    mision_out = MisionFlashOut(
        concept_name=result.mision.concept_name,
        title=result.mision.title,
        description=result.mision.description,
        lore_briefing=result.mision.lore_briefing,
        initial_code=result.mision.initial_code,
        hints=result.mision.hints,
        difficulty=result.mision.difficulty,
        estimated_lines=result.mision.estimated_lines,
    )

    return InterceptCheckResponse(
        intercept=True,
        interception_id=result.interception_id,
        mision=mision_out,
        daki_message=result.daki_message,
        concept_name=result.concepto.nombre if result.concepto else None,
        mastery_score=result.concepto.mastery_score if result.concepto else None,
        sector_ensenado=result.concepto.sector_ensenado if result.concepto else None,
    )


# ─────────────────────────────────────────────────────────────────────────────
# POST /intercept/{interception_id}/submit
# ─────────────────────────────────────────────────────────────────────────────

@router.post(
    "/{interception_id}/submit",
    response_model=FlashSubmitResponse,
    summary="Envía la solución de la Micro-Misión",
)
async def submit_flash_mission(
    interception_id: uuid.UUID,
    payload: FlashSubmitRequest,
    db: AsyncSession = Depends(get_db),
) -> FlashSubmitResponse:
    # Carga la intercepción
    result = await db.execute(
        select(DakiInterception).where(
            DakiInterception.id == interception_id,
            DakiInterception.user_id == payload.user_id,
        )
    )
    interception = result.scalar_one_or_none()
    if interception is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Intercepción no encontrada.",
        )
    if interception.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"La intercepción ya tiene estado '{interception.status}'.",
        )

    # Registra el intento
    await registrar_intento_flash(db, interception_id, payload.user_id)

    # ── Evalúa el código contra el expected_output de la misión ───────────────
    mision_data = json.loads(interception.mision_flash_json)
    expected_output: str = mision_data.get("expected_output", "")
    test_inputs: list[str] = []

    # Layer 2 — AST Guard
    sec = _ast_guard(payload.code)
    if sec:
        daki_msg = get_daki_message("SecurityError", payload.daki_level)
        return FlashSubmitResponse(
            passed=False,
            output_expected=expected_output,
            daki_message=daki_msg,
            attempts=interception.flash_attempts,
            status="error",
        )

    # Layers 3–5 — sandbox
    loop = asyncio.get_running_loop()
    sandbox_result: dict = await loop.run_in_executor(
        _THREAD_POOL,
        _execute_isolated,
        payload.code,
        test_inputs,
        _EXEC_TIMEOUT_S,
    )

    # Timeout
    if sandbox_result.get("_timeout"):
        daki_msg = get_daki_message("timeout", payload.daki_level)
        return FlashSubmitResponse(
            passed=False,
            daki_message=daki_msg,
            attempts=interception.flash_attempts,
            status="timeout",
        )

    # Error de ejecución
    if sandbox_result.get("error_type"):
        event = sandbox_result["error_type"]
        daki_msg = get_daki_message(event, payload.daki_level)
        return FlashSubmitResponse(
            passed=False,
            output_got=sandbox_result["stdout"],
            daki_message=daki_msg,
            attempts=interception.flash_attempts,
            status="error",
        )

    # Comparación de salida (siempre tolerante en flash missions)
    got = normalizar_salida(sandbox_result["stdout"])
    expected = normalizar_salida(expected_output)
    passed = got == expected

    if passed:
        await completar_intercepcion(db, interception_id, payload.user_id)
        daki_msg = get_daki_message("success", payload.daki_level)
        return FlashSubmitResponse(
            passed=True,
            output_got=got,
            stdout=sandbox_result["stdout"],
            daki_message=daki_msg,
            attempts=interception.flash_attempts,
            status="success",
        )
    else:
        daki_msg = get_daki_message("failed", payload.daki_level)
        return FlashSubmitResponse(
            passed=False,
            output_got=got,
            output_expected=expected,   # se revela al fallar para dar feedback
            stdout=sandbox_result["stdout"],
            daki_message=daki_msg,
            attempts=interception.flash_attempts,
            status="failed",
        )


# ─────────────────────────────────────────────────────────────────────────────
# POST /intercept/{interception_id}/skip
# ─────────────────────────────────────────────────────────────────────────────

@router.post(
    "/{interception_id}/skip",
    status_code=status.HTTP_200_OK,
    summary="Omite la Micro-Misión (desbloquea el avance sin resolver)",
    description=(
        "Permite al Operador saltar la intercepción. "
        "La intercepción queda marcada como 'expired' y no se repite en las "
        "próximas horas (cooldown). No hay penalty de XP — la pedagogía "
        "es voluntaria, no punitiva."
    ),
)
async def skip_flash_mission(
    interception_id: uuid.UUID,
    user_id: uuid.UUID = Query(...),
    db: AsyncSession = Depends(get_db),
) -> dict:
    result = await db.execute(
        select(DakiInterception).where(
            DakiInterception.id == interception_id,
            DakiInterception.user_id == user_id,
            DakiInterception.status == "pending",
        )
    )
    interception = result.scalar_one_or_none()
    if interception is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Intercepción pendiente no encontrada.",
        )

    interception.status = "expired"
    return {
        "skipped": True,
        "message": (
            "DAKI registró tu decisión, Operador. "
            "El nexo se abre... por ahora. Pero los sistemas no olvidan."
        ),
    }
