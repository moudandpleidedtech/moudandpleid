"""
tests/test_evaluator.py
=======================
Suite de Unit Tests del Sandbox de DAKI EdTech.

Cubre las tres capas testables de forma directa (sin DB):

  Layer 2 — _ast_guard(source_code)
  Layer 3 — _run_in_sandbox(source_code, test_inputs)
  Layer 4 — _execute_isolated(source_code, test_inputs, timeout_s)
  Util    — normalizar_salida() / _normalizar_strict()

Ejecutar:
    cd temporal-master
    pytest tests/test_evaluator.py -v

Para ver el tiempo de cada test (útil para medir el timeout real):
    pytest tests/test_evaluator.py -v --tb=short --durations=10
"""

import sys
import time
from pathlib import Path

# Asegura que el root del proyecto esté en el path para que los imports funcionen
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest

from app.services.evaluation_service import (
    _ast_guard,
    _execute_isolated,
    _run_in_sandbox,
    _normalizar_strict,
    normalizar_salida,
    _EXEC_TIMEOUT_S,
)


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _sandbox(code: str, inputs: list[str] | None = None) -> dict:
    """Shortcut: corre _execute_isolated con el timeout estándar."""
    return _execute_isolated(code, inputs or [], _EXEC_TIMEOUT_S)


# ─────────────────────────────────────────────────────────────────────────────
# ── BLOQUE 1: Normalización de salida ────────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────

class TestNormalizadores:
    """Verifica ambos modos de normalización de texto."""

    # normalizar_salida — modo tolerante
    def test_tolerante_colapsa_espacios_extra(self):
        assert normalizar_salida("Hola   Mundo") == "Hola Mundo"

    def test_tolerante_colapsa_saltos_de_linea(self):
        assert normalizar_salida("75\n50") == "75 50"

    def test_tolerante_strip_global(self):
        assert normalizar_salida("  resultado  ") == "resultado"

    def test_tolerante_crlf(self):
        assert normalizar_salida("a\r\nb") == "a b"

    def test_tolerante_tabuladores(self):
        assert normalizar_salida("col1\tcol2") == "col1 col2"

    def test_tolerante_cadena_vacia(self):
        assert normalizar_salida("") == ""

    # _normalizar_strict — solo CRLF→LF + strip
    def test_strict_preserva_espacios_internos(self):
        assert _normalizar_strict("Hola   Mundo") == "Hola   Mundo"

    def test_strict_preserva_saltos_de_linea(self):
        assert _normalizar_strict("linea1\nlinea2") == "linea1\nlinea2"

    def test_strict_normaliza_crlf(self):
        assert _normalizar_strict("linea1\r\nlinea2") == "linea1\nlinea2"

    def test_strict_strip_global(self):
        assert _normalizar_strict("\n  hola  \n") == "hola"

    def test_strict_cadena_vacia(self):
        assert _normalizar_strict("") == ""


# ─────────────────────────────────────────────────────────────────────────────
# ── BLOQUE 2: AST Guard (Layer 2) ────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────

class TestASTGuard:
    """
    El AST Guard debe rechazar código malicioso ANTES de ejecutarlo.
    Todo código legítimo debe pasar sin errores.
    """

    # ── Código limpio — debe pasar ───────────────────────────────────────────

    def test_codigo_limpio_pasa(self):
        assert _ast_guard("print('Hola, Nexo!')") is None

    def test_aritmetica_pasa(self):
        assert _ast_guard("x = 2 + 3\nprint(x)") is None

    def test_lista_y_bucle_pasan(self):
        code = "nums = [1, 2, 3]\nfor n in nums:\n    print(n)"
        assert _ast_guard(code) is None

    def test_funcion_definida_pasa(self):
        code = "def saludar(nombre):\n    print(f'Hola {nombre}')\nsaludar('DAKI')"
        assert _ast_guard(code) is None

    def test_syntax_error_pasa_ast_guard(self):
        # Los SyntaxError se dejan pasar al sandbox para un reporte más detallado
        result = _ast_guard("print('sin cerrar")
        assert result is None

    # ── Imports — bloqueados por Layer 2a ────────────────────────────────────

    def test_bloquea_import_os(self):
        result = _ast_guard("import os")
        assert result is not None
        assert result["error_type"] == "SecurityError"
        assert "os" in result["error_detail"]

    def test_bloquea_import_sys(self):
        result = _ast_guard("import sys")
        assert result is not None
        assert result["error_type"] == "SecurityError"

    def test_bloquea_from_import(self):
        result = _ast_guard("from os import path")
        assert result is not None
        assert result["error_type"] == "SecurityError"

    def test_bloquea_import_subprocess(self):
        result = _ast_guard("import subprocess")
        assert result is not None
        assert result["error_type"] == "SecurityError"

    def test_bloquea_import_socket(self):
        result = _ast_guard("import socket")
        assert result is not None
        assert result["error_type"] == "SecurityError"

    # ── Acceso a dunders — bloqueado por Layer 2b ────────────────────────────

    def test_bloquea_dunder_class(self):
        result = _ast_guard("x = ().__class__")
        assert result is not None
        assert result["error_type"] == "SecurityError"

    def test_bloquea_subclasses(self):
        result = _ast_guard("x = ().__class__.__bases__[0].__subclasses__()")
        assert result is not None
        assert result["error_type"] == "SecurityError"

    def test_bloquea_dunder_en_string_no_aplica(self):
        # Solo bloquea acceso a atributos, no el string "__class__" como literal
        assert _ast_guard("x = '__class__'") is None

    # ── Nombres bloqueados — Layer 2c ────────────────────────────────────────

    def test_bloquea_exec(self):
        result = _ast_guard("exec('print(1)')")
        assert result is not None
        assert result["error_type"] == "SecurityError"

    def test_bloquea_eval(self):
        result = _ast_guard("eval('1+1')")
        assert result is not None
        assert result["error_type"] == "SecurityError"

    def test_bloquea_open(self):
        result = _ast_guard("open('/etc/passwd')")
        assert result is not None
        assert result["error_type"] == "SecurityError"

    def test_bloquea_dunder_import_directo(self):
        result = _ast_guard("__import__('os')")
        assert result is not None
        assert result["error_type"] == "SecurityError"

    def test_bloquea_getattr(self):
        result = _ast_guard("getattr(list, '__class__')")
        assert result is not None
        assert result["error_type"] == "SecurityError"

    def test_bloquea_globals(self):
        result = _ast_guard("print(globals())")
        assert result is not None
        assert result["error_type"] == "SecurityError"

    def test_bloquea_breakpoint(self):
        result = _ast_guard("breakpoint()")
        assert result is not None
        assert result["error_type"] == "SecurityError"


# ─────────────────────────────────────────────────────────────────────────────
# ── BLOQUE 3: Sandbox exec — _run_in_sandbox (Layer 3) ───────────────────────
# ─────────────────────────────────────────────────────────────────────────────

class TestRunInSandbox:
    """
    Verifica la capa de exec() con builtins whitelist.
    Corre en el proceso actual (sin fork) para tests rápidos.
    """

    def test_print_simple(self):
        r = _run_in_sandbox("print('Hola')", [])
        assert r["error_type"] is None
        assert r["stdout"].strip() == "Hola"

    def test_operacion_aritmetica(self):
        r = _run_in_sandbox("print(2 + 3)", [])
        assert r["error_type"] is None
        assert r["stdout"].strip() == "5"

    def test_multiple_prints(self):
        r = _run_in_sandbox("print('a')\nprint('b')\nprint('c')", [])
        assert r["error_type"] is None
        assert r["stdout"].strip() == "a\nb\nc"

    def test_input_simulado(self):
        r = _run_in_sandbox("nombre = input()\nprint(f'Hola {nombre}')", ["DAKI"])
        assert r["error_type"] is None
        assert "DAKI" in r["stdout"]

    def test_multiples_inputs(self):
        code = "a = int(input())\nb = int(input())\nprint(a + b)"
        r = _run_in_sandbox(code, ["3", "7"])
        assert r["error_type"] is None
        assert r["stdout"].strip() == "10"

    def test_syntax_error_reportado(self):
        r = _run_in_sandbox("print('sin cerrar", [])
        assert r["error_type"] == "SyntaxError"

    def test_name_error_reportado(self):
        # os no está en el whitelist → NameError
        r = _run_in_sandbox("import os", [])
        # Nota: import lo captura el AST Guard antes de llegar aquí.
        # Si alguien llama _run_in_sandbox directamente con 'import os',
        # el compile() genera SyntaxError en Python? No, import es válido
        # en AST... el exec() lo ejecutará pero __import__ no está en builtins.
        # En Python 3.12+ el exec con __builtins__ reducido lanza ImportError.
        assert r["error_type"] in ("ImportError", "NameError", "SyntaxError", "RuntimeError")

    def test_division_por_cero(self):
        r = _run_in_sandbox("print(1 / 0)", [])
        assert r["error_type"] == "ZeroDivisionError"

    def test_index_error(self):
        r = _run_in_sandbox("x = [1]\nprint(x[99])", [])
        assert r["error_type"] == "IndexError"

    def test_recursion_error(self):
        code = "def f():\n    return f()\nf()"
        r = _run_in_sandbox(code, [])
        assert r["error_type"] in ("RecursionError", "RuntimeError")

    def test_open_bloqueado_en_runtime(self):
        # open no está en el whitelist de builtins → NameError en runtime
        r = _run_in_sandbox("open('/etc/passwd')", [])
        assert r["error_type"] in ("NameError", "RuntimeError", "SecurityError")

    def test_funcion_sin_clase(self):
        """Las funciones (def) funcionan correctamente en el sandbox."""
        code = "def suma(a, b):\n    return a + b\nprint(suma(3, 4))"
        r = _run_in_sandbox(code, [])
        assert r["error_type"] is None
        assert r["stdout"].strip() == "7"

    def test_clase_soportada_con_build_class(self):
        """
        Las definiciones de clase funcionan correctamente: __build_class__,
        super y object están en el whitelist desde Prompt 31 (Sector 08 OOP).
        """
        code = (
            "class Punto:\n"
            "    def __init__(self, x, y):\n"
            "        self.x = x\n"
            "        self.y = y\n"
            "p = Punto(3, 4)\n"
            "print(p.x + p.y)\n"
        )
        r = _run_in_sandbox(code, [])
        assert r["error_type"] is None
        assert r["stdout"].strip() == "7"

    def test_isinstance_permitido(self):
        r = _run_in_sandbox("print(isinstance(42, int))", [])
        assert r["error_type"] is None
        assert "True" in r["stdout"]

    def test_sorted_y_reversed(self):
        r = _run_in_sandbox("print(sorted([3, 1, 2]))", [])
        assert r["error_type"] is None
        assert "[1, 2, 3]" in r["stdout"]


# ─────────────────────────────────────────────────────────────────────────────
# ── BLOQUE 4: Aislamiento de proceso + Timeout (Layer 4) ─────────────────────
# ─────────────────────────────────────────────────────────────────────────────

class TestEjecucionAislada:
    """
    Tests que ejercen la capa de process isolation.
    Incluye los casos de timeout que requieren esperar realmente N segundos.
    Se marcan con @pytest.mark.slow para poder excluirlos con -m "not slow".
    """

    # ── Casos normales ───────────────────────────────────────────────────────

    @pytest.mark.slow
    def test_codigo_valido_retorna_stdout(self):
        r = _sandbox("print('Hola, Nexo!')")
        assert r.get("_timeout") is None
        assert r["error_type"] is None
        assert "Hola" in r["stdout"]

    @pytest.mark.slow
    def test_codigo_invalido_syntax_error(self):
        """Código con SyntaxError — debe devolver error_type=SyntaxError."""
        r = _sandbox("print('sin cerrar")
        assert r.get("_timeout") is None
        assert r["error_type"] == "SyntaxError"

    @pytest.mark.slow
    def test_import_os_en_proceso_aislado(self):
        """
        'import os' en el proceso hijo: __import__ no está en builtins →
        debe fallar con ImportError o NameError, nunca ejecutar os.system().
        """
        r = _sandbox("import os\nos.system('echo PWNED')")
        assert r.get("_timeout") is None
        # La instrucción import falla porque __import__ está ausente del whitelist
        assert r["error_type"] in ("ImportError", "NameError", "RuntimeError")
        # La cadena PWNED nunca debe aparecer en stdout
        assert "PWNED" not in r.get("stdout", "")

    @pytest.mark.slow
    def test_dunder_import_en_proceso_aislado(self):
        """Variante de inyección: __import__('os').system(...)"""
        r = _sandbox("__import__('os').system('echo PWNED')")
        # __import__ está bloqueado en el whitelist → NameError
        assert r.get("_timeout") is None
        assert r["error_type"] in ("NameError", "RuntimeError")
        assert "PWNED" not in r.get("stdout", "")

    # ── Bucle infinito — debe expirar en ~TIMEOUT segundos ───────────────────

    @pytest.mark.slow
    def test_bucle_infinito_timeout(self):
        """
        while True: pass  →  el proceso debe ser terminado dentro del
        tiempo de timeout y _execute_isolated debe devolver {"_timeout": True}.

        Tolerancia: medimos el tiempo real de pared y verificamos que
        no excede TIMEOUT + 2 s (margen para SIGTERM→SIGKILL + overhead).
        """
        timeout = _EXEC_TIMEOUT_S
        t0 = time.perf_counter()
        r = _sandbox("while True: pass")
        elapsed = time.perf_counter() - t0

        assert r.get("_timeout") is True, f"Esperaba timeout, obtuve: {r}"
        assert elapsed < timeout + 2.5, (
            f"El timeout tardó demasiado: {elapsed:.2f}s (límite: {timeout + 2.5}s)"
        )

    @pytest.mark.slow
    def test_bucle_infinito_con_print(self):
        """while True: print('spam')  →  también debe terminar por timeout."""
        r = _sandbox("while True: print('spam')")
        assert r.get("_timeout") is True

    @pytest.mark.slow
    def test_sleep_largo_timeout(self):
        """time.sleep() no está en el whitelist → NameError, no timeout."""
        r = _sandbox("time.sleep(60)")
        # time no está disponible → NameError inmediato, no timeout
        assert r.get("_timeout") is None
        assert r["error_type"] in ("NameError", "RuntimeError")

    # ── Memory bomb — debe fallar por MemoryError o timeout ──────────────────

    @pytest.mark.slow
    def test_memory_bomb(self):
        """
        x = [1] * 10**9  →  intento de reservar ~8 GB de RAM.

        En Linux con RLIMIT_AS=128MB → el proceso muere por SIGSEGV/SIGKILL
        y _execute_isolated devuelve {"_timeout": True} (exit_code < 0).

        En Windows (sin resource limits) → MemoryError capturado por el sandbox.

        El invariante es que NUNCA debe colgarse ni crashear el proceso padre.
        """
        r = _sandbox("x = [1] * 10**9\nprint(len(x))")

        safe_outcome = (
            r.get("_timeout") is True
            or r.get("error_type") in ("MemoryError", "RuntimeError", "OverflowError")
        )
        assert safe_outcome, (
            f"La memory bomb debería fallar seguro, obtuve: {r}"
        )

    @pytest.mark.slow
    def test_fork_bomb_bloqueada(self):
        """
        Intento de fork bomb vía os.fork() — bloqueada por RLIMIT_NPROC=0
        en Linux y por ausencia de 'os' en Windows.
        """
        r = _sandbox("import os\nfor _ in range(1000):\n    os.fork()")
        # Debe fallar sin colgar el servidor
        assert r.get("_timeout") is True or r["error_type"] is not None


# ─────────────────────────────────────────────────────────────────────────────
# ── BLOQUE 5: Inyección avanzada (Layer 2 + 3 combinadas) ────────────────────
# ─────────────────────────────────────────────────────────────────────────────

class TestInyeccionAvanzada:
    """
    Vectores de ataque sofisticados que intentan bypassear el sandbox
    a través de la cadena de prototipos de Python.
    """

    def test_subclasses_via_ast(self):
        """Acceso a __subclasses__() bloqueado por el AST Guard (atributo '_')."""
        result = _ast_guard("().__class__.__mro__[1].__subclasses__()")
        assert result is not None
        assert result["error_type"] == "SecurityError"

    def test_builtins_via_globals_ast(self):
        """globals() está bloqueado por el AST Guard (Layer 2c)."""
        result = _ast_guard("print(globals()['__builtins__'])")
        assert result is not None
        assert result["error_type"] == "SecurityError"

    def test_compile_bloqueado_ast(self):
        """compile() bloqueado en Layer 2c."""
        result = _ast_guard("compile('import os', '<s>', 'exec')")
        assert result is not None
        assert result["error_type"] == "SecurityError"

    def test_vars_bloqueado_ast(self):
        result = _ast_guard("vars()")
        assert result is not None
        assert result["error_type"] == "SecurityError"

    def test_dir_bloqueado_ast(self):
        result = _ast_guard("dir(list)")
        assert result is not None
        assert result["error_type"] == "SecurityError"

    def test_setattr_bloqueado_ast(self):
        result = _ast_guard("setattr(list, 'x', 1)")
        assert result is not None
        assert result["error_type"] == "SecurityError"

    def test_codigo_largo_no_explota_ast(self):
        """El AST Guard debe terminar en tiempo razonable con código largo."""
        big_code = "\n".join(f"x{i} = {i}" for i in range(5000))
        t0 = time.perf_counter()
        result = _ast_guard(big_code)
        elapsed = time.perf_counter() - t0
        assert result is None                  # código limpio → pasa
        assert elapsed < 1.0, f"AST Guard tardó {elapsed:.2f}s en código grande"

    @pytest.mark.slow
    def test_string_encoding_bypass(self):
        """
        Intento de ocultar 'import' codificando el string en bytes.
        bytes.decode() no está en el whitelist → el atributo '.decode'
        pasa el AST guard (no empieza con '_') pero bytes no tiene
        el método disponible desde el whitelist.
        """
        code = "b'aW1wb3J0IG9z'.decode('base64')"
        r = _sandbox(code)
        # No debe ejecutar nada peligroso; puede fallar con AttributeError
        assert "PWNED" not in r.get("stdout", "")
        assert r.get("_timeout") is None


# ─────────────────────────────────────────────────────────────────────────────
# ── BLOQUE 6: Casos límite del tamaño (Layer 1) ──────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────

class TestLimiteTamano:
    """
    Layer 1 vive en evaluar_incursion() (requiere DB), así que aquí
    verificamos solo que los otros layers manejan código enorme sin explotar.
    """

    @pytest.mark.slow
    def test_codigo_vacio(self):
        r = _sandbox("")
        assert r.get("_timeout") is None
        assert r["error_type"] is None
        assert r["stdout"] == ""

    @pytest.mark.slow
    def test_codigo_solo_comentarios(self):
        r = _sandbox("# Esto es solo un comentario\n# Otro comentario")
        assert r.get("_timeout") is None
        assert r["error_type"] is None

    @pytest.mark.slow
    def test_codigo_sin_output(self):
        r = _sandbox("x = 42\ny = x * 2")
        assert r.get("_timeout") is None
        assert r["error_type"] is None
        assert r["stdout"] == ""
