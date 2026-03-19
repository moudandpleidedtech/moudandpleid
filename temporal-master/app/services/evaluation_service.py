"""
evaluation_service.py — Motor de Evaluación con Sandbox de Seguridad (v2)

Arquitectura de defensa en capas:

  Layer 1 — Límite de tamaño
              Rechaza payloads > 10 KB antes de parsear nada.

  Layer 2 — AST Guard  (compile-time)
              Analiza el árbol sintáctico antes de exec().
              Bloquea: import/from-import, acceso a atributos con
              prefijo '_' (previene  ().__class__.__subclasses__()),
              y nombres explícitamente prohibidos (exec, eval, open,
              globals, locals, getattr, …).

  Layer 3 — Builtins Whitelist  (runtime)
              El exec() recibe un globals con __builtins__ reducido
              a las funciones educativas permitidas.  Todo lo demás
              (os, sys, socket, open, __import__, …) es invisible.

  Layer 4 — Process Isolation  (runtime)
              El código corre en un proceso hijo separado
              (multiprocessing.Process, daemon=True).
              Al cumplir el timeout, el proceso recibe SIGTERM → SIGKILL.
              No quedan hilos zombie consumiendo CPU del servidor.

  Layer 5 — Resource Limits  (runtime, Linux/POSIX)
              Dentro del proceso hijo, antes del exec():
              - RLIMIT_CPU  = 3 s  (el kernel mata el proceso si se excede)
              - RLIMIT_AS   = 128 MB  (evita malloc bombs)
              - RLIMIT_NPROC = 0  (impide fork bombs desde el sandbox)

Timeout: _EXEC_TIMEOUT_S = 3.0 s
"""

import ast
import asyncio
import builtins
import concurrent.futures
import io
import json
import multiprocessing as mp

# Contexto 'spawn' en vez del default 'fork' para el proceso hijo del sandbox.
# Con 'fork' el hijo hereda toda la memoria de FastAPI (> 128 MB) y choca
# inmediatamente con RLIMIT_AS = 128 MB antes de ejecutar una sola línea.
# Con 'spawn' el hijo arranca limpio e importa solo lo que necesita (~10 MB).
_MP_CTX = mp.get_context("spawn")
import re
import time
import uuid
from contextlib import redirect_stdout
from dataclasses import dataclass
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.challenge import Challenge

# ─── Constantes ───────────────────────────────────────────────────────────────

_EXEC_TIMEOUT_S  = 3.0        # segundos hasta SIGTERM del proceso hijo
_MAX_OUTPUT_CHARS = 8_000     # recorta salidas enormes
_MAX_CODE_BYTES   = 10_000    # rechaza payloads muy largos (> 10 KB)

# Excepciones que el sandbox puede reportar con nombre legible
_CATCHABLE = (
    SyntaxError, IndentationError, NameError, TypeError, ValueError,
    AttributeError, IndexError, KeyError, ZeroDivisionError,
    RecursionError, RuntimeError, StopIteration, OverflowError,
)

# Thread pool para correr la función de espera de procesos sin bloquear el loop
_THREAD_POOL = concurrent.futures.ThreadPoolExecutor(
    max_workers=4,
    thread_name_prefix="gg-sandbox",
)


# ─── Resultado estructurado ───────────────────────────────────────────────────

@dataclass
class EvaluacionResult:
    status: str                    # "success" | "failed" | "error" | "timeout"
    output_got: str = ""
    output_expected: str = ""
    output_matched: bool = False
    execution_time_ms: float = 0.0
    error: Optional[str] = None
    error_detail: Optional[str] = None
    error_line: Optional[int] = None

    @property
    def as_dict(self) -> dict:
        return {
            "status": self.status,
            "output_matched": self.output_matched,
            "stdout": self.output_got,
            "stderr": self.error_detail or "",
            "execution_time_ms": self.execution_time_ms,
            "error_info": {
                "error_type": self.error,
                "line": self.error_line,
                "detail": self.error_detail or "",
            } if self.error else None,
        }


# ─── Normalización ────────────────────────────────────────────────────────────

def normalizar_salida(texto: str) -> str:
    """
    Normalización TOLERANTE (modo estándar, strict_match=False).

    Aplica tres transformaciones en orden:
      1. Limpia saltos de línea inconsistentes (CRLF → LF).
      2. Colapsa cualquier secuencia de whitespace a un espacio simple,
         incluyendo espacios, tabuladores y saltos de línea internos.
         Esto evita fallar al usuario por espacios extra, indentación
         accidental o diferencias de CRLF/LF en cada línea.
      3. Strip global (elimina whitespace al inicio y al final).

    Ejemplo:
        "  75\\n  50  " → "75 50"
        "Hola,   Mundo" → "Hola, Mundo"
        "SISTEMA  ACTIVO\\n" → "SISTEMA ACTIVO"

    Nota: como ambos lados (usuario y expected) pasan por esta función,
    la comparación es justa.  La "lógica" debe ser correcta; el "formato"
    es perdonado.
    """
    return re.sub(r'\s+', ' ', texto).strip()


def _normalizar_strict(texto: str) -> str:
    """
    Normalización ESTRICTA (strict_match=True).

    Solo hace lo mínimo necesario para la interoperabilidad entre sistemas:
      • CRLF / CR  →  LF   (normaliza saltos de línea del SO)
      • Strip global        (elimina líneas vacías finales/iniciales)

    Todo lo demás se preserva tal cual: espacios internos, indentación,
    líneas vacías entre secciones, caracteres especiales.

    Usar en niveles que explícitamente enseñan formato de strings,
    f-strings con espaciado preciso o proyectos integradores multi-línea.
    """
    return texto.replace("\r\n", "\n").replace("\r", "\n").strip()


# ─────────────────────────────────────────────────────────────────────────────
# LAYER 2 — AST Guard
# ─────────────────────────────────────────────────────────────────────────────

# Nombres explícitamente bloqueados (acceso directo en código del usuario)
_BLOCKED_NAMES: frozenset[str] = frozenset({
    # Ejecución dinámica de código
    "exec", "eval", "compile",
    # Acceso al sistema de archivos
    "open",
    # Mecanismo de importación
    "__import__",
    # Introspección del namespace
    "globals", "locals", "vars", "dir",
    # Acceso a atributos en tiempo de ejecución (bypass del AST guard)
    "getattr", "setattr", "delattr", "hasattr",
    # Otros peligrosos
    "breakpoint", "memoryview",
    # Strings dunder que podrían usarse como claves de dict
    "__builtins__", "__class__", "__bases__", "__subclasses__",
    "__import__", "__spec__", "__loader__", "__file__",
})


class _SecurityError(Exception):
    """El código viola las políticas de seguridad del Nexo."""


class _ASTGuard(ast.NodeVisitor):
    """
    Visita el AST y lanza _SecurityError ante el primer patrón peligroso.

    Vectores que bloquea:
      • import / from … import  (Layer 2a)
      • Acceso a dunders/privados via atributo, ej. obj.__class__  (Layer 2b)
      • Nombres prohibidos en cualquier contexto  (Layer 2c)
    """

    # Layer 2a — imports
    def visit_Import(self, node: ast.Import) -> None:
        mod = node.names[0].name
        raise _SecurityError(
            f"import '{mod}' no está permitido en el entorno de entrenamiento."
        )

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        raise _SecurityError(
            "'from … import' no está permitido en el entorno de entrenamiento."
        )

    # Layer 2b — acceso a atributos con prefijo '_'
    # Bloquea ().__class__, [].__doc__, obj.__subclasses__(), etc.
    def visit_Attribute(self, node: ast.Attribute) -> None:
        if node.attr.startswith("_"):
            raise _SecurityError(
                f"Acceso al atributo '{node.attr}' está restringido por política de seguridad."
            )
        self.generic_visit(node)

    # Layer 2c — nombres prohibidos
    def visit_Name(self, node: ast.Name) -> None:
        if node.id in _BLOCKED_NAMES:
            raise _SecurityError(
                f"El identificador '{node.id}' está bloqueado por el Nexo."
            )
        self.generic_visit(node)


def _ast_guard(source_code: str) -> Optional[dict]:
    """
    Analiza el AST del código del usuario.

    Returns:
        None   si el código pasa la validación.
        dict   con error_type="SecurityError" si hay una violación.

    Los SyntaxError se ignoran aquí: el exec() los reportará con
    más detalle (línea, columna).
    """
    try:
        tree = ast.parse(source_code)
    except SyntaxError:
        return None   # el sandbox reportará el SyntaxError con detalle

    try:
        _ASTGuard().visit(tree)
        return None
    except _SecurityError as exc:
        return {
            "stdout":       "",
            "error_type":   "SecurityError",
            "error_detail": str(exc),
            "error_line":   None,
        }


# ─────────────────────────────────────────────────────────────────────────────
# LAYER 3 — Builtins Whitelist + exec()
# ─────────────────────────────────────────────────────────────────────────────

def _build_safe_globals(input_iter) -> dict:
    """
    Devuelve el dict globals para exec() con __builtins__ reducido a
    funciones educativas explícitamente permitidas.

    Cualquier nombre que no aparezca aquí lanza NameError dentro del
    código del usuario, que el sandbox captura limpiamente.
    """
    return {
        "__builtins__": {
            # I/O
            "print":      builtins.print,
            "input":      lambda _prompt="": next(input_iter, ""),
            # Tipos básicos
            "int": int,   "float": float, "str": str,
            "bool": bool, "list": list,   "dict": dict,
            "set": set,   "tuple": tuple,
            # Numéricas
            "abs": abs,   "max": max,     "min": min,
            "sum": sum,   "round": round, "pow": pow,
            "divmod": divmod,
            # Iteración / funcional
            "range": range,   "len": len,       "sorted": sorted,
            "reversed": reversed, "enumerate": enumerate,
            "zip": zip,   "map": map,       "filter": filter,
            # Conversión / representación
            "chr": chr,   "ord": ord,       "hex": hex,
            "bin": bin,   "oct": oct,       "repr": repr,
            "format": format,
            # Introspección mínima
            "isinstance": isinstance,
            "hasattr":    hasattr,
            # OOP — __name__ es necesario para que Python calcule __qualname__
            # de clases anidadas; sin él, cualquier `class Foo:` lanza NameError.
            "__name__":        "__main__",
            "__build_class__": builtins.__build_class__,
            "super":           super,
            "object":          object,
            # Excepciones estándar
            "Exception":           Exception,
            "BaseException":       BaseException,
            "ValueError":          ValueError,
            "TypeError":           TypeError,
            "ZeroDivisionError":   ZeroDivisionError,
            "IndexError":          IndexError,
            "KeyError":            KeyError,
            "AttributeError":      AttributeError,
            "NameError":           NameError,
            "RuntimeError":        RuntimeError,
            "StopIteration":       StopIteration,
            "NotImplementedError": NotImplementedError,
            "AssertionError":      AssertionError,
            "OverflowError":       OverflowError,
            "RecursionError":      RecursionError,
            # Literales especiales
            "True": True, "False": False,   "None": None,
        }
    }


def _run_in_sandbox(source_code: str, test_inputs: list[str]) -> dict:
    """
    Ejecuta source_code con exec() en el namespace restringido.
    Captura stdout.  Nunca eleva excepciones — las codifica en el dict.

    Pensado para correr DENTRO del proceso hijo (ya aislado).
    """
    stdout_buf = io.StringIO()
    safe_globals = _build_safe_globals(iter(test_inputs))

    try:
        compiled = compile(source_code, "<challenge>", "exec")
        with redirect_stdout(stdout_buf):
            exec(compiled, safe_globals)  # noqa: S102
        return {
            "stdout":       stdout_buf.getvalue()[:_MAX_OUTPUT_CHARS],
            "error_type":   None,
            "error_detail": None,
            "error_line":   None,
        }

    except SyntaxError as exc:
        return {
            "stdout":       stdout_buf.getvalue(),
            "error_type":   "SyntaxError",
            "error_detail": exc.msg,
            "error_line":   exc.lineno,
        }
    except IndentationError as exc:
        return {
            "stdout":       stdout_buf.getvalue(),
            "error_type":   "IndentationError",
            "error_detail": exc.msg,
            "error_line":   exc.lineno,
        }
    except _CATCHABLE as exc:
        return {
            "stdout":       stdout_buf.getvalue(),
            "error_type":   type(exc).__name__,
            "error_detail": str(exc),
            "error_line":   None,
        }
    except MemoryError:
        # El bucle generó demasiado output y llenó el StringIO.
        # Equivalente a agotar el recurso de memoria — se trata como timeout.
        return {"_timeout": True}
    except Exception as exc:  # noqa: BLE001
        stdout_safe = ""
        try:
            stdout_safe = stdout_buf.getvalue()
        except MemoryError:
            pass
        return {
            "stdout":       stdout_safe,
            "error_type":   "RuntimeError",
            "error_detail": str(exc),
            "error_line":   None,
        }


# ─────────────────────────────────────────────────────────────────────────────
# LAYERS 4 + 5 — Process Isolation + Resource Limits
# ─────────────────────────────────────────────────────────────────────────────

def _worker(
    source_code: str,
    test_inputs: list[str],
    result_q: "mp.SimpleQueue[dict]",
) -> None:
    """
    Corre dentro del proceso hijo.

    1. Desconecta el event loop heredado del padre (evita conflictos asyncio).
    2. Aplica límites de recursos POSIX (Layer 5).
    3. Ejecuta el sandbox y pone el resultado en result_q.
    """
    # Desconecta asyncio del padre para evitar interferencia
    try:
        asyncio.set_event_loop(None)
    except Exception:
        pass

    # Layer 5 — Resource Limits (solo Linux/POSIX)
    try:
        import resource  # noqa: PLC0415
        resource.setrlimit(resource.RLIMIT_CPU,   (3, 3))                        # 3 s CPU → SIGKILL por el SO
        resource.setrlimit(resource.RLIMIT_AS,    (128 << 20, 128 << 20))        # 128 MB de memoria virtual
        resource.setrlimit(resource.RLIMIT_NPROC, (0, 0))                        # 0 subprocesos (no fork bombs)
    except Exception:
        pass  # Windows u otras plataformas sin soporte POSIX

    result = _run_in_sandbox(source_code, test_inputs)
    result_q.put(result)


def _execute_isolated(
    source_code: str,
    test_inputs: list[str],
    timeout_s: float,
) -> dict:
    """
    Función bloqueante (corre en un hilo del _THREAD_POOL):

    1. Lanza un proceso hijo (daemon=True) para correr el sandbox.
    2. Espera hasta timeout_s segundos de reloj de pared.
    3. Si el proceso sigue vivo al expirar el timeout → SIGTERM → SIGKILL.
    4. Si el proceso fue matado por la señal del SO (RLIMIT_CPU, OOM) antes
       de que expire el timeout del padre → también se trata como timeout.
    5. Si terminó normalmente → lee y devuelve el resultado de la cola.
    """
    # mp.Queue (en vez de SimpleQueue) para tener empty() + get() no bloqueante
    result_q: "mp.Queue[dict]" = _MP_CTX.Queue(maxsize=1)

    p = _MP_CTX.Process(
        target=_worker,
        args=(source_code, test_inputs, result_q),
        daemon=True,
    )

    try:
        p.start()
    except Exception as exc:
        return {
            "stdout": "", "error_type": "RuntimeError",
            "error_detail": f"No se pudo lanzar el proceso sandbox: {exc}",
            "error_line": None,
        }

    p.join(timeout_s)

    # ── Timeout de reloj de pared: el proceso todavía corre ───────────────────
    if p.is_alive():
        p.terminate()          # SIGTERM
        p.join(0.5)
        if p.is_alive():
            p.kill()           # SIGKILL — último recurso
            p.join()
        return {"_timeout": True}

    # ── Proceso terminó (ya sea normal o por señal del SO) ────────────────────
    if not result_q.empty():
        try:
            return result_q.get_nowait()
        except Exception:
            pass

    # Cola vacía: el proceso murió sin producir resultado.
    # exit_code < 0  →  matado por señal (RLIMIT_CPU=SIGKILL, OOM kill del kernel)
    # exit_code > 0  →  excepción no capturada en el hijo (ej. MemoryError al
    #                    iterar el StringIO dentro de _run_in_sandbox)
    # Ambos casos = recurso agotado → tratamos igual que timeout.
    exit_code = p.exitcode
    if exit_code is not None and exit_code != 0:
        return {"_timeout": True}

    return {
        "stdout": "",
        "error_type": "RuntimeError",
        "error_detail": (
            "El proceso de evaluación terminó inesperadamente "
            f"(exit code {exit_code})."
        ),
        "error_line": None,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Función principal (async)
# ─────────────────────────────────────────────────────────────────────────────

async def evaluar_incursion(
    codigo_usuario: str,
    challenge_id: uuid.UUID,
    db: AsyncSession,
) -> EvaluacionResult:
    """
    Evalúa el código del usuario contra el expected_output del nivel.

    Pipeline:
      1. Límite de tamaño (L1)
      2. AST Guard (L2)
      3. Carga el challenge de la BD
      4. Ejecución aislada en proceso hijo (L3-L5) con timeout de 3 s
      5. Normalización y comparación de salida
    """

    # ── Layer 1: Límite de tamaño ─────────────────────────────────────────────
    if len(codigo_usuario.encode()) > _MAX_CODE_BYTES:
        return EvaluacionResult(
            status="error",
            error="SecurityError",
            error_detail=(
                f"El código supera el límite de {_MAX_CODE_BYTES // 1000} KB permitido."
            ),
        )

    # ── Layer 2: AST Guard ────────────────────────────────────────────────────
    sec = _ast_guard(codigo_usuario)
    if sec:
        return EvaluacionResult(
            status="error",
            error=sec["error_type"],
            error_detail=sec["error_detail"],
        )

    # ── Carga el challenge ────────────────────────────────────────────────────
    result = await db.execute(select(Challenge).where(Challenge.id == challenge_id))
    challenge = result.scalar_one_or_none()
    if challenge is None:
        return EvaluacionResult(
            status="error",
            error="NotFound",
            error_detail=f"Challenge {challenge_id} no encontrado.",
        )

    test_inputs: list[str]  = json.loads(challenge.test_inputs_json or "[]")
    expected_output: str    = challenge.expected_output or ""

    # Selecciona el normalizador según el flag del nivel
    # strict_match=True  → _normalizar_strict  (solo CRLF→LF + strip global)
    # strict_match=False → normalizar_salida   (colapsa whitespace redundante)
    _norm = _normalizar_strict if challenge.strict_match else normalizar_salida

    # ── Layers 3-5: ejecución en proceso hijo ─────────────────────────────────
    t0 = time.perf_counter()

    loop = asyncio.get_running_loop()
    sandbox_result: dict = await loop.run_in_executor(
        _THREAD_POOL,
        _execute_isolated,
        codigo_usuario,
        test_inputs,
        _EXEC_TIMEOUT_S,
    )

    elapsed_ms = round((time.perf_counter() - t0) * 1000, 2)

    # ── Timeout ───────────────────────────────────────────────────────────────
    if sandbox_result.get("_timeout"):
        return EvaluacionResult(
            status="timeout",
            output_expected=_norm(expected_output),
            execution_time_ms=elapsed_ms,
            error="TimeoutError",
            error_detail=(
                f"El proceso consumió más de {_EXEC_TIMEOUT_S:.0f} s. "
                "Posible bucle infinito detectado."
            ),
        )

    # ── Error de ejecución ────────────────────────────────────────────────────
    if sandbox_result["error_type"]:
        return EvaluacionResult(
            status="error",
            output_got=sandbox_result["stdout"],
            output_expected=_norm(expected_output),
            execution_time_ms=elapsed_ms,
            error=sandbox_result["error_type"],
            error_detail=sandbox_result["error_detail"],
            error_line=sandbox_result["error_line"],
        )

    # ── Comparación de salida ─────────────────────────────────────────────────
    got      = _norm(sandbox_result["stdout"])
    expected = _norm(expected_output)
    matched  = got == expected

    return EvaluacionResult(
        status="success" if matched else "failed",
        output_got=got,
        output_expected=expected,
        output_matched=matched,
        execution_time_ms=elapsed_ms,
    )
