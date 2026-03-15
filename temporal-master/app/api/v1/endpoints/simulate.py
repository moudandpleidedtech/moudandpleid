from fastapi import APIRouter, status
from pydantic import BaseModel, field_validator

from app.services.drone_simulator import simulate_drone

router = APIRouter()


class SimulateRequest(BaseModel):
    code: str
    matrix: list[list[int]]
    start: dict[str, int] | None = None

    @field_validator("matrix")
    @classmethod
    def validate_matrix(cls, v: list[list[int]]) -> list[list[int]]:
        if not v or not v[0]:
            raise ValueError("La matriz no puede estar vacía.")
        if len(v) > 20 or len(v[0]) > 20:
            raise ValueError("La matriz no puede superar 20×20.")
        cols = len(v[0])
        if any(len(row) != cols for row in v):
            raise ValueError("Todas las filas deben tener el mismo número de columnas.")
        return v

    @field_validator("code")
    @classmethod
    def validate_code(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("El código no puede estar vacío.")
        if len(v) > 5_000:
            raise ValueError("El código no puede superar 5 000 caracteres.")
        return v


class PathStepOut(BaseModel):
    x: int
    y: int
    crashed: bool
    collected: bool


class EnemyEvent(BaseModel):
    x: int
    y: int
    enemy_type: int   # 4 = Syntax Swarm · 5 = Logic Brute
    event: str        # "enemy_destroyed"
    attack_type: str  # "aoe_for" | "precision_if"


class SimulateResponse(BaseModel):
    path: list[PathStepOut]
    success: bool
    crashed: bool
    steps: int
    execution_time_ms: float
    error: str | None = None
    enemy_events: list[EnemyEvent] = []


@router.post(
    "/simulate",
    response_model=SimulateResponse,
    status_code=status.HTTP_200_OK,
    summary="Simula el movimiento del dron Byte en una matriz 2D",
    description=(
        "Ejecuta el código del usuario en un entorno restringido. "
        "Solo están disponibles: mover_arriba(), mover_abajo(), "
        "mover_izquierda(), mover_derecha() y recolectar(). "
        "Devuelve el historial completo de coordenadas con flags de colisión."
    ),
)
async def simulate_endpoint(payload: SimulateRequest) -> SimulateResponse:
    result = await simulate_drone(
        code=payload.code,
        matrix=payload.matrix,
        start=payload.start,
    )
    return SimulateResponse(**result)
