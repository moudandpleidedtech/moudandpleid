import asyncio
import os
import re
import sys
import tempfile
import time

import httpx

PISTON_API_URL = "https://emkc.org/api/v2/piston/execute"
PISTON_TIMEOUT_S = 6.0   # reducido de 10s — activa fallback más rápido
LOCAL_TIMEOUT_S  = 4.0   # subido de 3s — más margen para código legítimo

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

    Usado para desafíos con challenge_type='typescript'.
    Piston compila y ejecuta TypeScript con ts-node; el output de
    console.log() se captura en stdout para comparar con expected_output.

    Returns:
        {'stdout': str, 'stderr': str, 'execution_time_ms': float, 'success': bool,
         'error_info': None}
    """
    stdin = "\n".join(test_inputs) + ("\n" if test_inputs else "")
    try:
        result = await _execute_via_piston(
            source_code, stdin, language="typescript", version="5.0.4"
        )
    except Exception as exc:
        # Fallback explícito: Piston no disponible o respuesta inválida
        import logging
        logging.getLogger(__name__).warning("Piston TypeScript unavailable: %s", exc)
        result = {
            "stdout": "",
            "stderr": "TypeScript sandbox temporalmente no disponible. Intenta de nuevo.",
            "execution_time_ms": 0.0,
            "success": False,
        }
    # TypeScript error_info parsing omitido — stderr ya contiene el mensaje completo
    result["error_info"] = None
    return result


async def execute_python_code(source_code: str, test_inputs: list[str]) -> dict:
    """
    Execute Python source code with test_inputs joined as stdin.

    Returns:
        {'stdout': str, 'stderr': str, 'execution_time_ms': float, 'success': bool}

    Usa Piston API (sandbox remoto aislado) como único backend.
    El fallback local fue eliminado por razones de seguridad: un subprocess
    local hereda todas las variables de entorno del servidor (DATABASE_URL,
    SECRET_KEY, STRIPE_SECRET_KEY, etc.) y no tiene restricciones de filesystem
    ni de red, lo que permite exfiltración de credenciales.
    """
    stdin = "\n".join(test_inputs) + ("\n" if test_inputs else "")
    try:
        result = await _execute_via_piston(source_code, stdin)
    except Exception as exc:
        import logging
        logging.getLogger(__name__).warning("Piston unavailable (%s) — sandbox no disponible", type(exc).__name__)
        result = {
            "stdout": "",
            "stderr": "El sandbox de ejecución no está disponible temporalmente. Intentá de nuevo en unos segundos.",
            "execution_time_ms": 0.0,
            "success": False,
        }

    result["error_info"] = _parse_python_error(result.get("stderr", ""))
    return result


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
