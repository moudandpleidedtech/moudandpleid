"""
Endpoint del sistema de Jefes — The Infinite Looper (Jefe Final de Python Core).

POST /api/v1/boss/execute
  — Valida el código contra el desafío del Jefe Final.
  — Requiere haber completado >= BOSS_UNLOCK_THRESHOLD misiones Python Core.
  — Si es correcto, otorga 5 000 XP y la medalla SYSTEM_KILLER.

GET /api/v1/boss/status/{user_id}
  — Devuelve si el boss está desbloqueado y cuántas misiones faltan.

GET /api/v1/boss/config
  — Devuelve la configuración del desafío.

El jefe no necesita un Challenge en la DB: su lógica vive aquí.
"""

import json
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.challenge import Challenge
from app.models.user import User
from app.models.user_progress import UserProgress
from app.services import activity_service
from app.services.execution_service import execute_python_code
from app.services.gamification_service import GamificationEngine

router = APIRouter()

# ─── Configuración del jefe ───────────────────────────────────────────────────

BOSS_XP_REWARD = 5_000

# Número de misiones Python Core completadas para desbloquear el boss
BOSS_UNLOCK_THRESHOLD = 140   # AVANZADO_DONE — OOP completamente dominado

# ─── Desafío: ControladorNexo ─────────────────────────────────────────────────
#
# El ∞ LOOPER ha evolucionado: ya no es un simple `while True`.
# Ahora corrompe el Nexo con tres vectores simultáneos:
#   1. Un acumulador infinito de divisibles (sin cota)
#   2. Una trampa de Collatz que diverge cuando n → ∞
#   3. Una clase sin estado que colapsa la memoria de instancia
#
# El operador debe implementar ControladorNexo — el sistema de defensa del Nexo —
# combinando OOP, bucle for (cota finita), bucle while (convergencia) y f-string.
#
# Input:  "20"
# Output: "NEXO-ALPHA: suma=78, pasos=7"
#
# Verificación:
#   suma_divisibles(20) → 0+3+5+6+9+10+12+15+18 = 78
#   pasos_collatz(20)   → 20→10→5→16→8→4→2→1     = 7 pasos

BOSS_TEST_INPUTS: list[str] = ["20"]
BOSS_EXPECTED_OUTPUT = "NEXO-ALPHA: suma=78, pasos=7"

BOSS_INITIAL_CODE = """\
class ControladorNexo:
    def __init__(self, nombre):
        # Guarda el nombre como atributo de instancia
        # Inicializa self.operaciones en 0
        pass

    def suma_divisibles(self, n):
        # Retorna la suma de todos los múltiplos de 3 o 5
        # estrictamente menores que n (usar for acotado).
        pass

    def pasos_collatz(self, n):
        # Retorna cuántos pasos tarda la secuencia de Collatz
        # en llegar a 1 desde n (usar while).
        # Si n es par  → n //= 2
        # Si n es impar → n = 3*n + 1
        pass

    def analizar(self, n):
        s = self.suma_divisibles(n)
        p = self.pasos_collatz(n)
        self.operaciones += 1
        print(f"{self.nombre}: suma={s}, pasos={p}")


ctrl = ControladorNexo("NEXO-ALPHA")
ctrl.analizar(int(input()))
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
    badge_earned: str | None = None


class BossStatusResponse(BaseModel):
    unlocked: bool
    completed_count: int
    threshold: int
    remaining: int


# ─── Helper ───────────────────────────────────────────────────────────────────


async def _count_completed(user_id: uuid.UUID, db: AsyncSession) -> int:
    """Cuenta misiones Python Core completadas por el usuario."""
    result = await db.execute(
        select(func.count())
        .select_from(UserProgress)
        .join(Challenge, Challenge.id == UserProgress.challenge_id)
        .where(
            UserProgress.user_id == user_id,
            UserProgress.completed == True,  # noqa: E712
        )
    )
    return result.scalar_one() or 0


# ─── Endpoints ────────────────────────────────────────────────────────────────


@router.get(
    "/boss/status/{user_id}",
    response_model=BossStatusResponse,
    summary="Verifica si el boss está desbloqueado para el usuario",
)
async def boss_status(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> BossStatusResponse:
    count = await _count_completed(user_id, db)
    return BossStatusResponse(
        unlocked=count >= BOSS_UNLOCK_THRESHOLD,
        completed_count=count,
        threshold=BOSS_UNLOCK_THRESHOLD,
        remaining=max(0, BOSS_UNLOCK_THRESHOLD - count),
    )


@router.post(
    "/boss/execute",
    response_model=BossExecuteResponse,
    status_code=status.HTTP_200_OK,
    summary="Valida el código contra el Jefe Final ∞ LOOPER",
    description=(
        "Requiere completar al menos BOSS_UNLOCK_THRESHOLD misiones Python Core. "
        "Si el output coincide con el esperado, otorga 5 000 XP y la medalla SYSTEM_KILLER."
    ),
)
async def boss_execute(
    payload: BossExecuteRequest,
    db: AsyncSession = Depends(get_db),
) -> BossExecuteResponse:
    # ── Guardia de prerequisito ───────────────────────────────────────────────
    count = await _count_completed(payload.user_id, db)
    if count < BOSS_UNLOCK_THRESHOLD:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                f"El Jefe Final está sellado. "
                f"Completa {BOSS_UNLOCK_THRESHOLD - count} misiones más para desbloquearlo."
            ),
        )

    # ── Ejecución ─────────────────────────────────────────────────────────────
    result = await execute_python_code(payload.source_code, BOSS_TEST_INPUTS)

    success = (
        result["success"]
        and result["stdout"].strip() == BOSS_EXPECTED_OUTPUT
    )

    xp_earned = 0
    badge_earned: str | None = None
    user = await db.get(User, payload.user_id)
    new_total_xp = user.total_xp if user else 0
    new_level = user.current_level if user else 1

    if success and user:
        xp_earned = BOSS_XP_REWARD
        user.total_xp += xp_earned
        user.current_level = GamificationEngine.calculate_level_from_xp(user.total_xp)
        new_total_xp = user.total_xp
        new_level = user.current_level

        try:
            badges: list[str] = json.loads(user.badges_json or "[]")
        except (ValueError, TypeError):
            badges = []
        if "SYSTEM_KILLER" not in badges:
            badges.append("SYSTEM_KILLER")
            user.badges_json = json.dumps(badges)
            badge_earned = "SYSTEM_KILLER"

        await db.flush()
        await activity_service.emit_boss_defeated(user.callsign)

    return BossExecuteResponse(
        success=success,
        xp_earned=xp_earned,
        new_total_xp=new_total_xp,
        new_level=new_level,
        stdout=result["stdout"],
        stderr=result["stderr"],
        execution_time_ms=result["execution_time_ms"],
        badge_earned=badge_earned,
    )


@router.get(
    "/boss/config",
    summary="Retorna la configuración del desafío del Jefe Final",
)
async def boss_config() -> dict:
    return {
        "boss_id":        "infinite_looper",
        "title":          "∞ LOOPER — Jefe Final Python Core",
        "initial_code":   BOSS_INITIAL_CODE,
        "test_input":     BOSS_TEST_INPUTS[0],
        "xp_reward":      BOSS_XP_REWARD,
        "unlock_at":      BOSS_UNLOCK_THRESHOLD,
    }
