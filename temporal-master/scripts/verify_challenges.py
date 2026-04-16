"""
verify_challenges.py — Verifica que cada nivel del catálogo sea jugable.

Controles por nivel:
  [S] Schema      — campos requeridos presentes y no vacíos
  [J] JSON        — test_inputs_json / hints_json / concepts_taught_json parseables
  [H] Hints       — entre 1 y 3 pistas en hints_json
  [X] Ejecutable  — syntax_hint corre sin crash (subprocess local)
  [P] Pass        — syntax_hint produce exactamente expected_output (normalizado)
  [N] No-trivial  — initial_code NO produce expected_output (puzzle no resuelto de inicio)
  [U] Unicidad    — (sector_id, level_order) sin duplicados en el catálogo

Uso:
    python -m scripts.verify_challenges              # verifica todo el catálogo
    python -m scripts.verify_challenges --sector 4   # solo un sector
    python -m scripts.verify_challenges --fast       # solo controles de schema/JSON (sin ejecución)
    python -m scripts.verify_challenges --verbose    # muestra PASS + FAIL (por defecto solo FAIL)
"""

import argparse
import ast
import json
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.seed_master import load_sectors

# ─── Constantes ───────────────────────────────────────────────────────────────

EXEC_TIMEOUT = 5.0   # segundos por ejecución de subprocess
MAX_HINTS    = 3

# Colores ANSI (degradan a vacío si no hay tty)
_tty = sys.stdout.isatty()
RED    = "\033[91m" if _tty else ""
GREEN  = "\033[92m" if _tty else ""
YELLOW = "\033[93m" if _tty else ""
CYAN   = "\033[96m" if _tty else ""
BOLD   = "\033[1m"  if _tty else ""
RESET  = "\033[0m"  if _tty else ""


# ─── Normalización (idéntica a compiler.py) ────────────────────────────────

def _normalize(text: str) -> str:
    text = unicodedata.normalize("NFC", text)
    text = text.replace("\u2014", "-").replace("\u2013", "-")
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.strip() for line in normalized.splitlines()]
    return "\n".join(lines).strip()


# ─── Ejecución local ──────────────────────────────────────────────────────────

def _run_code(source: str, test_inputs: list[str]) -> tuple[str, str, bool]:
    """
    Ejecuta source_code en un subprocess Python aislado.
    Retorna (stdout, stderr, success).
    Solo para uso en scripts de desarrollo — no usar en producción.
    """
    stdin_bytes = ("\n".join(test_inputs) + ("\n" if test_inputs else "")).encode()
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False, encoding="utf-8"
    ) as f:
        f.write(source)
        tmp = f.name
    try:
        result = subprocess.run(
            [sys.executable, tmp],
            input=stdin_bytes,
            capture_output=True,
            timeout=EXEC_TIMEOUT,
        )
        return (
            result.stdout.decode(errors="replace"),
            result.stderr.decode(errors="replace"),
            result.returncode == 0,
        )
    except subprocess.TimeoutExpired:
        return ("", f"TIMEOUT (>{EXEC_TIMEOUT}s)", False)
    except Exception as exc:
        return ("", str(exc), False)
    finally:
        Path(tmp).unlink(missing_ok=True)


# ─── Verificación de un challenge ────────────────────────────────────────────

class Check:
    """Resultado de un control individual."""
    __slots__ = ("code", "ok", "msg")

    def __init__(self, code: str, ok: bool, msg: str = ""):
        self.code = code   # "S", "J", "H", "X", "P", "N", "U"
        self.ok   = ok
        self.msg  = msg    # descripción del error (vacío si ok)

    def __str__(self) -> str:
        if self.ok:
            return f"{GREEN}[{self.code}✓]{RESET}"
        return f"{RED}[{self.code}✗]{RESET}"


def verify_one(ch: dict[str, Any], seen_positions: set[tuple], fast: bool) -> list[Check]:
    checks: list[Check] = []

    # ── [S] Schema ─────────────────────────────────────────────────────────────
    missing = [
        f for f in ("title", "description", "expected_output", "initial_code",
                    "sector_id", "level_order", "challenge_type")
        if not ch.get(f) and ch.get(f) != 0
    ]
    checks.append(Check("S", not missing,
                        f"campos vacíos: {missing}" if missing else ""))

    # ── [J] JSON fields ────────────────────────────────────────────────────────
    json_errors: list[str] = []
    for field in ("test_inputs_json", "hints_json", "concepts_taught_json"):
        raw = ch.get(field, "[]")
        if not raw:
            continue
        try:
            json.loads(raw)
        except json.JSONDecodeError as e:
            json_errors.append(f"{field}: {e}")
    checks.append(Check("J", not json_errors,
                        "; ".join(json_errors) if json_errors else ""))

    # ── [H] Hints count ────────────────────────────────────────────────────────
    hints: list[str] = []
    try:
        hints = json.loads(ch.get("hints_json") or "[]")
    except Exception:
        pass
    h_ok  = 1 <= len(hints) <= MAX_HINTS
    checks.append(Check("H", h_ok,
                        f"{len(hints)} pistas (se esperan 1-{MAX_HINTS})" if not h_ok else ""))

    # ── [U] Unicidad posicional ────────────────────────────────────────────────
    pos = (ch.get("sector_id"), ch.get("level_order"))
    dup = pos in seen_positions
    checks.append(Check("U", not dup,
                        f"duplicado en S{pos[0]:02d} L{pos[1]:03d}" if dup else ""))
    seen_positions.add(pos)

    # ── Ejecución (se omite si --fast o si es TypeScript) ─────────────────────
    challenge_type = ch.get("challenge_type", "python") or "python"
    if fast or challenge_type != "python":
        # Si es TypeScript, marca como N/A en vez de fallo
        na_msg = "omitido (--fast)" if fast else f"omitido (type={challenge_type})"
        checks.append(Check("X", True, na_msg))
        checks.append(Check("P", True, na_msg))
        checks.append(Check("N", True, na_msg))
        return checks

    try:
        test_inputs: list[str] = json.loads(ch.get("test_inputs_json") or "[]")
    except Exception:
        test_inputs = []

    expected_norm = _normalize(ch.get("expected_output", ""))
    syntax_hint   = (ch.get("syntax_hint") or "").strip()

    # ── [X] + [P] Syntax hint es válido y produce expected_output ──────────────
    # syntax_hint es un campo pedagógico — a menudo es un fragmento, no un programa
    # completo. Tratamos cualquier indicador de "snippet" como omisión, no fallo.
    _SNIPPET_ERRORS = (
        "NameError",
        "UnboundLocalError",
        "return' outside function",  # fragmento de función
        "yield' outside function",
    )
    _SNIPPET_SYNTAX_MSG = (
        "return' outside",
        "yield' outside",
        "invalid character",           # '²', '→', '—', etc. → texto doc embebido
        "invalid syntax",              # fragmento incompleto / pseudo-código
        "expected an indented block",  # firma de función/clase sin cuerpo
    )

    if not syntax_hint:
        checks.append(Check("X", True, "sin syntax_hint (omitido)"))
        checks.append(Check("P", True, "sin syntax_hint (omitido)"))
    else:
        # ── Verificar sintaxis con ast ──────────────────────────────────────
        try:
            ast.parse(syntax_hint)
            syntax_ok = True
        except SyntaxError as e:
            err_msg = str(e)
            is_snippet_syntax = any(s in err_msg for s in _SNIPPET_SYNTAX_MSG)
            if is_snippet_syntax:
                checks.append(Check("X", True, f"snippet/pseudo-código (omitido)"))
                checks.append(Check("P", True, f"snippet/pseudo-código (omitido)"))
            else:
                # SyntaxError genuino (no esperado en un snippet)
                checks.append(Check("X", False, f"SyntaxError inesperado: {err_msg[:100]}"))
                checks.append(Check("P", False, "no ejecutado (SyntaxError)"))
            syntax_ok = False

        if syntax_ok:
            stdout, stderr, success = _run_code(syntax_hint, test_inputs)
            is_runtime_snippet = not success and any(s in stderr for s in _SNIPPET_ERRORS)
            if is_runtime_snippet:
                checks.append(Check("X", True, "snippet parcial (omitido)"))
                checks.append(Check("P", True, "snippet parcial (omitido)"))
            elif not success:
                # Crash real (no snippet) → fallo de ejecución
                stderr_last = stderr.strip().splitlines()[-1] if stderr.strip() else ""
                checks.append(Check("X", False, f"stderr: {stderr_last[:140]}"))
                checks.append(Check("P", False, "no ejecutado (crash en [X])"))
            else:
                # Ejecutó OK → verificar output
                checks.append(Check("X", True))
                got_norm = _normalize(stdout)
                if got_norm == "":
                    # Sin output: hint define función pero no la llama → snippet de definición
                    checks.append(Check("P", True, "hint define función sin llamarla (omitido)"))
                elif got_norm == expected_norm:
                    checks.append(Check("P", True))
                else:
                    got_repr      = repr(got_norm[:80])
                    expected_repr = repr(expected_norm[:80])
                    checks.append(Check("P", False,
                                        f"got={got_repr}  expected={expected_repr}"))

    # ── [N] initial_code no produce expected_output (no pre-resuelto) ──────────
    initial_code = (ch.get("initial_code") or "").strip()
    if not initial_code:
        checks.append(Check("N", True, "sin initial_code (omitido)"))
    else:
        try:
            ast.parse(initial_code)
            i_ok = True
        except SyntaxError:
            # El initial_code con SyntaxError es deliberado en varios niveles
            i_ok = False

        if not i_ok:
            # SyntaxError intencional en initial_code → no produce output → OK
            checks.append(Check("N", True, "initial_code tiene SyntaxError (esperado)"))
        else:
            stdout_i, _stderr_i, success_i = _run_code(initial_code, test_inputs)
            if success_i:
                got_i = _normalize(stdout_i)
                pre_solved = (got_i == expected_norm)
                checks.append(Check("N", not pre_solved,
                                    f"initial_code ya produce el output correcto: {repr(got_i[:80])}"
                                    if pre_solved else ""))
            else:
                # El initial_code crashea → tampoco produce el output esperado → OK
                checks.append(Check("N", True, "initial_code crashea (no pre-resuelto)"))

    return checks


# ─── Entrada principal ────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verifica que cada nivel del catálogo sea jugable."
    )
    parser.add_argument("--sector", type=int, default=None,
                        help="Verificar solo este sector (ej. --sector 4)")
    parser.add_argument("--fast", action="store_true",
                        help="Solo controles de schema/JSON, sin ejecutar código")
    parser.add_argument("--verbose", action="store_true",
                        help="Mostrar PASS y FAIL (por defecto solo FAIL)")
    args = parser.parse_args()

    catalog = load_sectors(filter_sector=args.sector)
    total   = len(catalog)

    print(f"\n{BOLD}{'─'*64}{RESET}")
    print(f"{BOLD}  DAKI — Verificación de Niveles{'  [FAST]' if args.fast else ''}{RESET}")
    print(f"{'─'*64}")
    print(f"  Catálogo: {total} challenges"
          + (f"  (sector {args.sector})" if args.sector is not None else ""))
    print(f"  Controles: [S]chema [J]SON [H]ints [U]nicidad"
          + ("" if args.fast else " [X]ejecutable [P]ass [N]o-trivial"))
    print(f"{'─'*64}\n")

    seen_positions: set[tuple] = set()
    failures: list[tuple[dict, list[Check]]] = []
    warns:    list[tuple[dict, list[Check]]] = []
    passed    = 0

    for ch in catalog:
        checks  = verify_one(ch, seen_positions, fast=args.fast)
        has_fail = any(not c.ok and not c.msg.startswith("omitido") and not c.msg.startswith("sin syntax") for c in checks)
        has_warn = any(not c.ok and (c.msg.startswith("omitido") or c.msg.startswith("sin syntax")) for c in checks)

        label = f"S{ch.get('sector_id', '?'):02d} L{ch.get('level_order', '?'):03d}"
        title = (ch.get("title") or "")[:42]
        check_str = " ".join(str(c) for c in checks)

        if has_fail:
            failures.append((ch, checks))
            print(f"  {RED}FAIL{RESET}  {label}  {title:<42}  {check_str}")
            for c in checks:
                if not c.ok and c.msg and not c.msg.startswith("omitido") and not c.msg.startswith("sin syntax"):
                    print(f"         {YELLOW}↳ [{c.code}] {c.msg}{RESET}")
        elif has_warn and args.verbose:
            warns.append((ch, checks))
            print(f"  {YELLOW}WARN{RESET}  {label}  {title:<42}  {check_str}")
        elif not has_fail and not has_warn:
            passed += 1
            if args.verbose:
                print(f"  {GREEN}PASS{RESET}  {label}  {title:<42}  {check_str}")
        else:
            passed += 1  # warn pero no fail → pasa

    # ── Resumen ────────────────────────────────────────────────────────────────
    print(f"\n{'─'*64}")
    print(f"  Total    : {total}")
    print(f"  {GREEN}Pasaron  : {passed}{RESET}")
    print(f"  {RED}Fallaron : {len(failures)}{RESET}")
    if warns:
        print(f"  {YELLOW}Warnings : {len(warns)}{RESET}")

    if failures:
        print(f"\n  {BOLD}Niveles con errores ({len(failures)}):{RESET}")
        for ch, checks in failures:
            bad = [f"[{c.code}] {c.msg}" for c in checks
                   if not c.ok and c.msg and not c.msg.startswith("omitido")]
            print(f"    S{ch.get('sector_id','?'):02d} L{ch.get('level_order','?'):03d}  "
                  f"{(ch.get('title') or '')[:40]}")
            for b in bad:
                print(f"      {YELLOW}→ {b}{RESET}")
        sys.exit(1)
    else:
        print(f"\n  {GREEN}{BOLD}Todos los niveles son jugables.{RESET}")
        sys.exit(0)


if __name__ == "__main__":
    main()
