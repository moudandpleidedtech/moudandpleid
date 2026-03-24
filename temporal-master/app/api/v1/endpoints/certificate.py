"""
GET /api/v1/certificate/download

Genera y devuelve en streaming el certificado PDF oficial DAKI EdTech
para el Operador que completó el Nivel 100.

Seguridad:
    Requiere ?user_id=<uuid> con un registro UserProgress.completed == True
    para el challenge con level_order == 100.  Devuelve 403 si no cumple.

Respuesta:
    StreamingResponse — application/pdf
    Content-Disposition: attachment; filename="GG_Certificado_Nivel100.pdf"
    No se escribe nada al disco del servidor.
"""

import io
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.challenge import Challenge
from app.models.user import User
from app.models.user_progress import UserProgress
from app.services.certificate_service import build_certificate_pdf

router = APIRouter(prefix="/certificate", tags=["certificate"])


# ─── Guard ────────────────────────────────────────────────────────────────────

async def _verify_level100_completion(
    user_id: uuid.UUID,
    db: AsyncSession,
) -> User:
    """
    Verifica que el usuario exista y haya completado (status completed) el
    challenge con level_order == 100.

    Raises:
        404  si el usuario no existe
        403  si no ha completado el nivel 100
    """
    # Carga el usuario
    user_result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = user_result.scalar_one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado.",
        )

    # Busca el challenge de level_order 100
    ch_result = await db.execute(
        select(Challenge).where(Challenge.level_order == 100).limit(1)
    )
    challenge = ch_result.scalar_one_or_none()
    if challenge is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El nivel 100 aún no ha sido configurado en el sistema.",
        )

    # Verifica que el usuario lo haya completado
    prog_result = await db.execute(
        select(UserProgress).where(
            UserProgress.user_id    == user_id,
            UserProgress.challenge_id == challenge.id,
            UserProgress.completed  == True,  # noqa: E712
        )
    )
    if prog_result.scalar_one_or_none() is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code":    "LEVEL_100_NOT_COMPLETED",
                "message": (
                    "Acceso denegado. Debes completar el Nivel 100 para "
                    "recibir las credenciales oficiales."
                ),
            },
        )

    return user


# ─── Endpoint ─────────────────────────────────────────────────────────────────

@router.get(
    "/download",
    summary="Descarga el certificado PDF del Operador de Nivel 100",
    description=(
        "Genera el certificado oficial DAKI EdTech en formato PDF y lo devuelve "
        "como descarga directa.  Requiere que el Operador haya completado el Nivel 100. "
        "El archivo se genera en memoria — nada se escribe en el disco del servidor."
    ),
    response_class=StreamingResponse,
    responses={
        200: {
            "content": {"application/pdf": {}},
            "description": "PDF del certificado — listo para descargar.",
        },
        403: {"description": "Nivel 100 no completado."},
        404: {"description": "Usuario o nivel no encontrado."},
    },
)
async def download_certificate(
    user_id: uuid.UUID = Query(..., description="UUID del Operador autenticado"),
    db: AsyncSession = Depends(get_db),
) -> StreamingResponse:
    # ── 1. Guard: verifica elegibilidad ──────────────────────────────────────
    user = await _verify_level100_completion(user_id, db)

    # ── 2. Genera el PDF en memoria ───────────────────────────────────────────
    pdf_bytes, cert_id = build_certificate_pdf(
        callsign=user.callsign,
        rank=user.current_rank or "Netzach Operative",
    )

    # ── 3. Devuelve como streaming sin tocar el disco ─────────────────────────
    filename = f"GG_Certificado_Nivel100_{cert_id}.pdf"

    return StreamingResponse(
        content=io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition":       f'attachment; filename="{filename}"',
            "Content-Length":            str(len(pdf_bytes)),
            "X-GG-Certificate-ID":       cert_id,
            "X-GG-Operator":             user.callsign,
            "Cache-Control":             "no-store",
        },
    )
