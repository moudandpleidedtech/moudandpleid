import asyncio
import os
import sys
import tempfile
import time

import httpx

PISTON_API_URL = "https://emkc.org/api/v2/piston/execute"
PISTON_TIMEOUT_S = 10.0
LOCAL_TIMEOUT_S = 3.0


async def execute_python_code(source_code: str, test_inputs: list[str]) -> dict:
    """
    Execute Python source code with test_inputs joined as stdin.

    Returns:
        {'stdout': str, 'stderr': str, 'execution_time_ms': float, 'success': bool}

    Tries Piston API (remote sandbox) first; falls back to local subprocess.
    """
    # Unir inputs con newlines y añadir newline final para que el último input()
    # no quede esperando EOF en runtimes que requieren \n como terminador.
    stdin = "\n".join(test_inputs) + ("\n" if test_inputs else "")
    try:
        return await _execute_via_piston(source_code, stdin)
    except Exception:
        return await _execute_via_subprocess(source_code, stdin)


async def _execute_via_piston(source_code: str, stdin: str) -> dict:
    payload = {
        "language": "python",
        "version": "3.10.0",
        "files": [{"content": source_code}],
        "stdin": stdin,
        "run_timeout": int(LOCAL_TIMEOUT_S * 1000),
    }

    start = time.perf_counter()
    async with httpx.AsyncClient(timeout=PISTON_TIMEOUT_S) as client:
        response = await client.post(PISTON_API_URL, json=payload)
        response.raise_for_status()
    elapsed_ms = (time.perf_counter() - start) * 1000

    run = response.json()["run"]
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
