"""
Feed de Actividad Global en Tiempo Real (Prompt 21).

GET /api/v1/activity/stream  — Server-Sent Events (SSE)
GET /api/v1/activity/recent  — Últimos N eventos (polling fallback)
"""

import asyncio
import json

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from app.services import activity_service

router = APIRouter(prefix="/activity", tags=["activity"])

HEARTBEAT_INTERVAL = 20  # segundos entre pings keep-alive


@router.get(
    "/stream",
    summary="Feed de actividad global vía Server-Sent Events",
    response_class=StreamingResponse,
)
async def activity_stream(request: Request) -> StreamingResponse:
    """
    Abre una conexión SSE.
    - Envía inmediatamente los últimos 15 eventos.
    - A partir de entonces reenvía cada nuevo evento en tiempo real.
    - Emite un comentario `: ping` cada 20 s para mantener la conexión.
    """

    async def generator():
        q: asyncio.Queue = asyncio.Queue(maxsize=100)
        activity_service.add_subscriber(q)
        try:
            # Eventos históricos iniciales
            for ev in activity_service.get_recent(15):
                yield f"data: {json.dumps(ev)}\n\n"

            # Streaming en vivo
            while True:
                if await request.is_disconnected():
                    break
                try:
                    event = await asyncio.wait_for(q.get(), timeout=HEARTBEAT_INTERVAL)
                    yield f"data: {json.dumps(event)}\n\n"
                except asyncio.TimeoutError:
                    yield ": ping\n\n"
        finally:
            activity_service.remove_subscriber(q)

    return StreamingResponse(
        generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@router.get(
    "/recent",
    summary="Últimos eventos de actividad (polling fallback)",
)
async def get_recent_activity(limit: int = 20) -> list[dict]:
    return activity_service.get_recent(min(limit, 50))
