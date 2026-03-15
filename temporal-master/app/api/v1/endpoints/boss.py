"""
Endpoint del sistema de Jefes (Prompt 16).

POST /api/v1/boss/execute
  — Valida el código contra el desafío del jefe TheInfiniteLooper.
  — Si es correcto, otorga XP al usuario y retorna el resultado.

El jefe no necesita un Challenge en la DB: su lógica vive aquí.
"""

import uuid

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.user import User
from app.services import activity_service
from app.services.execution_service import execute_python_code
from app.services.gamification_service import GamificationEngine

router = APIRouter()

# ─── Configuración del jefe ───────────────────────────────────────────────────

BOSS_XP_REWARD = 1_500

# Desafío: factorial_iterativo(7) → 5040
# El jugador debe usar un bucle for acotado (no while True).
BOSS_TEST_INPUTS: list[str] = ["7"]
BOSS_EXPECTED_OUTPUT = "5040"

BOSS_INITIAL_CODE = """\
def factorial_iterativo(n):
    # El ∞ LOOPER ejecuta: while True: contador += 1
    # Tu mision: detenerlo con un bucle FOR acotado.
    # Retorna n! (n factorial) usando for, no recursion.
    # Ejemplo: factorial_iterativo(5) → 120
    pass

n = int(input())
print(factorial_iterativo(n))
"""

# ─── Schemas ──────────────────────────────────────────────────────────────────


class BossExecuteRequest(BaseModel):
    user_id: uuid.UUID
    source_code: str


class BossExecuteResponse(BaseModel):
    success: bool
    xp_earned: int
    new_total_xp: int
    new_level: int
    stdout: str
    stderr: str
    execution_time_ms: float


# ─── Endpoint ─────────────────────────────────────────────────────────────────


@router.post(
    "/boss/execute",
    response_model=BossExecuteResponse,
    status_code=status.HTTP_200_OK,
    summary="Valida el código contra TheInfiniteLooper",
    description=(
        "Ejecuta el código del jugador contra el reto del jefe ∞ LOOPER. "
        "Si la salida coincide con el valor esperado, otorga 1 500 XP al usuario. "
        "No requiere un Challenge registrado en la base de datos."
    ),
)
async def boss_execute(
    payload: BossExecuteRequest,
    db: AsyncSession = Depends(get_db),
) -> BossExecuteResponse:
    result = await execute_python_code(payload.source_code, BOSS_TEST_INPUTS)

    success = (
        result["success"]
        and result["stdout"].strip() == BOSS_EXPECTED_OUTPUT
    )

    xp_earned = 0
    user = await db.get(User, payload.user_id)
    new_total_xp = user.total_xp if user else 0
    new_level = user.current_level if user else 1

    if success and user:
        xp_earned = BOSS_XP_REWARD
        user.total_xp += xp_earned
        user.current_level = GamificationEngine.calculate_level_from_xp(user.total_xp)
        new_total_xp = user.total_xp
        new_level = user.current_level
        await db.flush()
        await activity_service.emit_boss_defeated(user.username)

    return BossExecuteResponse(
        success=success,
        xp_earned=xp_earned,
        new_total_xp=new_total_xp,
        new_level=new_level,
        stdout=result["stdout"],
        stderr=result["stderr"],
        execution_time_ms=result["execution_time_ms"],
    )


@router.get(
    "/boss/config",
    summary="Retorna la configuración del desafío del jefe",
)
async def boss_config() -> dict:
    return {
        "boss_id": "infinite_looper",
        "title": "∞ LOOPER — Módulo Bucles",
        "initial_code": BOSS_INITIAL_CODE,
        "test_input": BOSS_TEST_INPUTS[0],
        "xp_reward": BOSS_XP_REWARD,
    }
