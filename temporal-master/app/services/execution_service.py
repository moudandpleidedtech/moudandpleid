import asyncio
import logging
import os
import re
import sys
import tempfile
import time

import httpx

PISTON_API_URL = "https://emkc.org/api/v2/piston/execute"
PISTON_TIMEOUT_S = 5.0
LOCAL_TIMEOUT_S  = 5.0

_log = logging.getLogger(__name__)

# Entorno mínimo para subprocess — sin DATABASE_URL, SECRET_KEY ni otras vars del servidor.
# sys.executable hereda el PATH del sistema; aquí lo declaramos explícito para seguridad.
_SAFE_ENV: dict[str, str] = {
    "PATH": "/usr/local/bin:/usr/bin:/bin",
    "HOME": "/tmp",
    "TMPDIR": "/tmp",
    "LANG": "en_US.UTF-8",
    "LC_ALL": "en_US.UTF-8",
    "PYTHONUTF8": "1",
    "PYTHONIOENCODING": "utf-8",
    "PYTHONDONTWRITEBYTECODE": "1",
}

# Error types DAKI knows how to identify
_KNOWN_ERRORS = (
    "SyntaxError", "IndentationError", "NameError", "TypeError",
    "ValueError", "AttributeError", "IndexError", "KeyError",
    "ZeroDivisionError", "RecursionError", "RuntimeError",
)


def _parse_python_error(stderr: str) -> dict | None:
    """
    Parse a Python traceback/error from stderr into a structured dict.

    Returns:
        {error_type: str, line: int | None, detail: str} or None if not parseable.
    """
    if not stderr or not stderr.strip():
        return None

    # Extract all "File ..., line N" occurrences — last one is most relevant
    line_matches = re.findall(r'File ".*?", line (\d+)', stderr)
    line_num: int | None = int(line_matches[-1]) if line_matches else None

    # Find the error type and detail (last matching error line in stderr)
    pattern = r'^(' + '|'.join(_KNOWN_ERRORS) + r'):\s*(.*)$'
    error_match = re.search(pattern, stderr, re.MULTILINE)

    if not error_match and line_num is None:
        return None

    return {
        "error_type": error_match.group(1) if error_match else "Error",
        "line": line_num,
        "detail": error_match.group(2).strip() if error_match else stderr.strip().splitlines()[-1],
    }


async def execute_node_code(source_code: str, test_inputs: list[str]) -> dict:
    """
    Ejecuta TypeScript/Node.js via Piston API.
    No tiene fallback local (Node.js no está garantizado en el servidor).
    """
    stdin = "\n".join(test_inputs) + ("\n" if test_inputs else "")
    try:
        result = await _execute_via_piston(
            source_code, stdin, language="typescript", version="5.0.4"
        )
    except Exception as exc:
        _log.warning("Piston TypeScript unavailable: %s", exc)
        result = {
            "stdout": "",
            "stderr": "TypeScript sandbox temporalmente no disponible. Intenta de nuevo.",
            "execution_time_ms": 0.0,
            "success": False,
        }
    result["error_info"] = None
    result.setdefault("sandbox_unavailable", False)
    return result


async def execute_python_code(source_code: str, test_inputs: list[str]) -> dict:
    """
    Ejecuta código Python con test_inputs como stdin.

    Flujo:
      1. Intenta Piston API (sandbox remoto aislado).
      2. Si Piston no está disponible, usa subprocess local con entorno limpio
         (_SAFE_ENV) que excluye DATABASE_URL, SECRET_KEY y demás vars del servidor.

    Returns:
        {stdout, stderr, execution_time_ms, success, error_info, sandbox_unavailable}
        sandbox_unavailable=True solo si ambos backends fallan (no contar attempt).
    """
    stdin = "\n".join(test_inputs) + ("\n" if test_inputs else "")

    # ── Intento 1: Piston ────────────────────────────────────────────────────
    try:
        result = await _execute_via_piston(source_code, stdin)
        result["sandbox_unavailable"] = False
        result["error_info"] = _parse_python_error(result.get("stderr", ""))
        return result
    except Exception as exc:
        _log.info("Piston unavailable (%s) — usando ejecutor local", type(exc).__name__)

    # ── Intento 2: subprocess local con env limpio ───────────────────────────
    try:
        result = await _execute_via_subprocess(source_code, stdin)
        result["sandbox_unavailable"] = False
        result["error_info"] = _parse_python_error(result.get("stderr", ""))
        return result
    except Exception as exc:
        _log.error("Ejecutor local también falló: %s", exc)

    return {
        "stdout": "",
        "stderr": "El entorno de ejecución no está disponible. Intentá de nuevo.",
        "execution_time_ms": 0.0,
        "success": False,
        "sandbox_unavailable": True,
        "error_info": None,
    }


async def _execute_via_piston(source_code: str, stdin: str, language: str = "python", version: str = "3.10.0") -> dict:
    payload = {
        "language": language,
        "version": version,
        "files": [{"content": source_code}],
        "stdin": stdin,
        "run_timeout": int(LOCAL_TIMEOUT_S * 1000),
    }

    start = time.perf_counter()
    async with httpx.AsyncClient(timeout=PISTON_TIMEOUT_S) as client:
        response = await client.post(PISTON_API_URL, json=payload)
        response.raise_for_status()
    elapsed_ms = (time.perf_counter() - start) * 1000

    # Respuesta inesperada de Piston → tratar como fallo para activar el fallback
    body = response.json()
    if "run" not in body:
        raise ValueError(f"Piston response missing 'run' key: {list(body.keys())}")

    run = body["run"]
    return {
        "stdout": run.get("stdout", ""),
        "stderr": run.get("stderr", ""),
        "execution_time_ms": round(elapsed_ms, 2),
        "success": run.get("code", 1) == 0,
    }


async def _execute_via_subprocess(source_code: str, stdin: str) -> dict:
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False, encoding="utf-8"
    ) as f:
        f.write(source_code)
        tmp_path = f.name

    try:
        start = time.perf_counter()
        proc = await asyncio.create_subprocess_exec(
            sys.executable,
            tmp_path,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=_SAFE_ENV,  # entorno limpio: sin DATABASE_URL, SECRET_KEY, etc.
            cwd=tempfile.gettempdir(),
        )
        try:
            stdout_bytes, stderr_bytes = await asyncio.wait_for(
                proc.communicate(input=stdin.encode()),
                timeout=LOCAL_TIMEOUT_S,
            )
            elapsed_ms = (time.perf_counter() - start) * 1000
            return {
                "stdout": stdout_bytes.decode(errors="replace"),
                "stderr": stderr_bytes.decode(errors="replace"),
                "execution_time_ms": round(elapsed_ms, 2),
                "success": proc.returncode == 0,
            }
        except asyncio.TimeoutError:
            proc.kill()
            await proc.wait()
            elapsed_ms = (time.perf_counter() - start) * 1000
            return {
                "stdout": "",
                "stderr": f"Execution timed out after {LOCAL_TIMEOUT_S}s",
                "execution_time_ms": round(elapsed_ms, 2),
                "success": False,
            }
    finally:
        os.unlink(tmp_path)
