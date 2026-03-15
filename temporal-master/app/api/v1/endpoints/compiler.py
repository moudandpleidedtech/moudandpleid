import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.challenge import Challenge
from app.schemas.gamification import ChallengeAttemptResult
from app.services.execution_service import execute_python_code
from app.services.gamification_service import gamification_engine

router = APIRouter()


class CodeExecuteRequest(BaseModel):
    user_id: uuid.UUID
    challenge_id: uuid.UUID
    source_code: str
    test_inputs: list[str] = []
    hints_used: int = 0  # pistas solicitadas a ENIGMA antes de este intento


class CodeExecuteResponse(BaseModel):
    stdout: str
    stderr: str
    execution_time_ms: float
    output_matched: bool
    gamification: ChallengeAttemptResult


@router.post(
    "/execute",
    response_model=CodeExecuteResponse,
    status_code=status.HTTP_200_OK,
    summary="Execute user code for a challenge",
    description=(
        "Runs the submitted source code via Piston API (or local subprocess fallback), "
        "validates stdout against the challenge's expected_output, "
        "and automatically triggers gamification scoring."
    ),
)
async def execute_challenge_code(
    payload: CodeExecuteRequest,
    db: AsyncSession = Depends(get_db),
) -> CodeExecuteResponse:
    challenge = await db.get(Challenge, payload.challenge_id)
    if challenge is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Challenge {payload.challenge_id} not found",
        )

    exec_result = await execute_python_code(payload.source_code, payload.test_inputs)

    # Cuenta errores de sintaxis detectados en stderr de este intento
    syntax_errors_count = exec_result["stderr"].count("SyntaxError")

    output_matched = exec_result["stdout"].strip() == challenge.expected_output.strip()
    is_success = exec_result["success"] and output_matched

    try:
        gamification_result = await gamification_engine.process_challenge_completion(
            db=db,
            user_id=payload.user_id,
            challenge_id=payload.challenge_id,
            is_success=is_success,
            execution_time_ms=int(exec_result["execution_time_ms"]),
            syntax_errors_count=syntax_errors_count,
            hints_used_this_session=payload.hints_used,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    return CodeExecuteResponse(
        stdout=exec_result["stdout"],
        stderr=exec_result["stderr"],
        execution_time_ms=exec_result["execution_time_ms"],
        output_matched=output_matched,
        gamification=gamification_result,
    )
