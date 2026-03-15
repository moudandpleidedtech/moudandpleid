"""
Motor de simulación del dron Byte para la Fase 0 (Pre-Python).

El usuario escribe comandos simplificados:
    mover_arriba(), mover_abajo(), mover_izquierda(), mover_derecha(), recolectar()

El motor ejecuta el código en un entorno restringido, registra cada posición
en path_history y detiene la ejecución ante colisiones o al alcanzar la meta.
"""

import asyncio
import concurrent.futures
import re
import time
from typing import TypedDict

MAX_STEPS = 200
EXEC_TIMEOUT_S = 3.0

# ─── Tipos de celda ────────────────────────────────────────────────────────────
# 0 = suelo · 1 = muro · 2 = núcleo (meta) · 3 = inicio
# 4 = Syntax Swarm (enemigo básico) · 5 = Logic Brute (enemigo blindado)

# Patrones prohibidos — primera capa de defensa antes de exec()
_FORBIDDEN = re.compile(
    r"(__|\bimport\b|\bopen\b|\beval\b|\bexec\b|\bcompile\b"
    r"|\bglobals\b|\blocals\b|\bvars\b|\bdir\b|\bgetattr\b"
    r"|\bsetattr\b|\bdelattr\b|\bhasattr\b|\bsubprocess\b|\bos\b)"
)


class PathStep(TypedDict):
    x: int
    y: int
    crashed: bool
    collected: bool


# ─── Excepciones internas de control de flujo ─────────────────────────────────

class _DroneHalted(Exception):
    """Terminación normal: colisión, meta alcanzada o dron ya detenido."""


class _StepLimitExceeded(Exception):
    """El código superó el límite de pasos permitidos."""


# ─── Simulador ────────────────────────────────────────────────────────────────

class _Drone:
    """Estado del dron y sus funciones de movimiento."""

    def __init__(self, matrix: list[list[int]], start_x: int, start_y: int) -> None:
        self.matrix = matrix
        self.rows = len(matrix)
        self.cols = len(matrix[0]) if matrix else 0
        self.x = start_x
        self.y = start_y
        self.path: list[PathStep] = [
            PathStep(x=start_x, y=start_y, crashed=False, collected=False)
        ]
        self.crashed = False
        self.completed = False
        self._steps = 0

    def _tick(self) -> None:
        self._steps += 1
        if self._steps > MAX_STEPS:
            raise _StepLimitExceeded(
                f"Límite de {MAX_STEPS} pasos alcanzado — posible bucle infinito."
            )

    def _move(self, dx: int, dy: int) -> None:
        self._tick()
        if self.crashed or self.completed:
            raise _DroneHalted("El dron ya está detenido.")

        nx, ny = self.x + dx, self.y + dy

        # Fuera del mapa
        if not (0 <= nx < self.cols and 0 <= ny < self.rows):
            self.crashed = True
            self.path.append(PathStep(x=nx, y=ny, crashed=True, collected=False))
            raise _DroneHalted(f"Fuera de los límites del mapa en ({nx}, {ny}).")

        cell = self.matrix[ny][nx]

        # Muro
        if cell == 1:
            self.crashed = True
            self.path.append(PathStep(x=nx, y=ny, crashed=True, collected=False))
            raise _DroneHalted(f"Colisión con muro en ({nx}, {ny}).")

        self.x, self.y = nx, ny

        # Núcleo de datos (meta)
        if cell == 2:
            self.completed = True
            self.path.append(PathStep(x=nx, y=ny, crashed=False, collected=True))
            raise _DroneHalted("Núcleo de datos alcanzado.")

        self.path.append(PathStep(x=nx, y=ny, crashed=False, collected=False))

    # ── API pública del dron ──────────────────────────────────────────────────

    def mover_arriba(self) -> None:    self._move(0, -1)
    def mover_abajo(self) -> None:     self._move(0, 1)
    def mover_izquierda(self) -> None: self._move(-1, 0)
    def mover_derecha(self) -> None:   self._move(1, 0)

    def recolectar(self) -> None:
        self._tick()
        if self.crashed or self.completed:
            raise _DroneHalted("El dron no puede recolectar en este estado.")
        cell = self.matrix[self.y][self.x]
        if cell == 2:
            self.completed = True
            self.path.append(PathStep(x=self.x, y=self.y, crashed=False, collected=True))
            raise _DroneHalted("Núcleo de datos recolectado con recolectar().")


# ─── Builtins seguros para el entorno del dron ────────────────────────────────

_SAFE_BUILTINS = {
    "range": range, "len": len, "enumerate": enumerate,
    "int": int, "str": str, "bool": bool,
    "abs": abs, "min": min, "max": max, "print": print,
    "True": True, "False": False, "None": None,
}


# ─── Lógica de combate (post-simulación) ─────────────────────────────────────

def _detect_attacks(code: str) -> tuple[bool, bool]:
    """Retorna (tiene_for, tiene_if_else) analizando el código del jugador."""
    # Ignora comentarios para evitar falsos positivos
    lines = [line.split("#")[0] for line in code.split("\n")]
    clean = "\n".join(lines)
    has_for = bool(re.search(r"\bfor\b", clean))
    has_if_else = bool(re.search(r"\bif\b", clean)) and bool(re.search(r"\belse\b", clean))
    return has_for, has_if_else


def _combat_zone(path: list[PathStep]) -> set[tuple[int, int]]:
    """
    Zona de combate = celdas del propio camino + celdas adyacentes (Manhattan 1).
    Un bucle for hace AoE sobre esta zona completa.
    """
    zone: set[tuple[int, int]] = set()
    for step in path:
        zone.add((step["x"], step["y"]))
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            zone.add((step["x"] + dx, step["y"] + dy))
    return zone


def _resolve_enemy_events(
    path: list[PathStep],
    matrix: list[list[int]],
    has_for: bool,
    has_if_else: bool,
) -> list[dict]:
    """
    Resuelve eventos de combate:
      · Syntax Swarm (4) — destruido si el dron tiene bucle for (AoE)
      · Logic Brute  (5) — destruido solo si el dron tiene if/else (Ataque de Precisión)
    Solo se procesan celdas dentro de la zona de combate.
    """
    if not (has_for or has_if_else):
        return []

    zone = _combat_zone(path)
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0
    events: list[dict] = []

    for (cx, cy) in zone:
        if not (0 <= cy < rows and 0 <= cx < cols):
            continue
        cell = matrix[cy][cx]
        if cell == 4 and has_for:
            events.append({
                "x": cx, "y": cy, "enemy_type": 4,
                "event": "enemy_destroyed", "attack_type": "aoe_for",
            })
        elif cell == 5 and has_if_else:
            events.append({
                "x": cx, "y": cy, "enemy_type": 5,
                "event": "enemy_destroyed", "attack_type": "precision_if",
            })

    return events


# ─── Ejecución en hilo aislado ────────────────────────────────────────────────

def _run_sync(
    code: str,
    matrix: list[list[int]],
    start_x: int,
    start_y: int,
) -> tuple[list[PathStep], bool, bool, str | None]:
    """Ejecuta el código del usuario en un entorno completamente restringido."""
    drone = _Drone(matrix, start_x, start_y)
    error: str | None = None

    restricted_globals: dict = {
        "__builtins__": _SAFE_BUILTINS,
        "mover_arriba":    drone.mover_arriba,
        "mover_abajo":     drone.mover_abajo,
        "mover_izquierda": drone.mover_izquierda,
        "mover_derecha":   drone.mover_derecha,
        "recolectar":      drone.recolectar,
    }

    try:
        exec(compile(code, "<drone_code>", "exec"), restricted_globals)  # noqa: S102
    except _DroneHalted:
        pass  # terminación esperada
    except _StepLimitExceeded as e:
        error = str(e)
    except SyntaxError as e:
        error = f"Error de sintaxis en línea {e.lineno}: {e.msg}"
    except Exception as e:
        error = f"Error de ejecución: {type(e).__name__}: {e}"

    return drone.path, drone.crashed, drone.completed, error


# ─── Punto de entrada asíncrono ───────────────────────────────────────────────

async def simulate_drone(
    code: str,
    matrix: list[list[int]],
    start: dict[str, int] | None = None,
) -> dict:
    """
    Ejecuta el código del dron de forma asíncrona con timeout estricto.

    Returns:
        {
            'path': list[PathStep],
            'success': bool,
            'crashed': bool,
            'steps': int,
            'execution_time_ms': float,
            'error': str | None,
            'enemy_events': list[dict],
        }
    """
    # Validación de seguridad previa al exec()
    if _FORBIDDEN.search(code):
        return {
            "path": [],
            "success": False,
            "crashed": False,
            "steps": 0,
            "execution_time_ms": 0.0,
            "error": "El código contiene instrucciones no permitidas en el entorno del dron.",
            "enemy_events": [],
        }

    # Detectar posición de inicio (celda tipo 3, o default 0,0)
    start_x, start_y = 0, 0
    if start:
        start_x, start_y = start.get("x", 0), start.get("y", 0)
    else:
        for y, row in enumerate(matrix):
            for x, cell in enumerate(row):
                if cell == 3:
                    start_x, start_y = x, y
                    break

    loop = asyncio.get_event_loop()
    t0 = time.perf_counter()

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        try:
            path, crashed, completed, error = await asyncio.wait_for(
                loop.run_in_executor(pool, _run_sync, code, matrix, start_x, start_y),
                timeout=EXEC_TIMEOUT_S,
            )
        except asyncio.TimeoutError:
            elapsed = round((time.perf_counter() - t0) * 1000, 2)
            return {
                "path": [PathStep(x=start_x, y=start_y, crashed=False, collected=False)],
                "success": False,
                "crashed": False,
                "steps": 0,
                "execution_time_ms": elapsed,
                "error": f"Tiempo de ejecución excedido ({EXEC_TIMEOUT_S}s).",
                "enemy_events": [],
            }

    elapsed = round((time.perf_counter() - t0) * 1000, 2)

    # Resolución de combate post-simulación
    has_for, has_if_else = _detect_attacks(code)
    enemy_events = _resolve_enemy_events(path, matrix, has_for, has_if_else)

    return {
        "path": path,
        "success": completed and not crashed,
        "crashed": crashed,
        "steps": len(path) - 1,
        "execution_time_ms": elapsed,
        "error": error,
        "enemy_events": enemy_events,
    }
