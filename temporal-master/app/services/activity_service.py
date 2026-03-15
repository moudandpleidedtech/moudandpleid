"""
Servicio de Actividad Global en Tiempo Real (Prompt 21).

Mantiene un buffer en memoria de los últimos 60 eventos y notifica
a todos los suscriptores SSE conectados en cuanto se emite uno nuevo.
"""

import asyncio
import time
import uuid
from collections import deque
from typing import Any

# ─── Buffer y suscriptores ────────────────────────────────────────────────────

_recent_events: deque[dict[str, Any]] = deque(maxlen=60)
_subscribers: list[asyncio.Queue] = []


def _make_event(
    event_type: str,
    message: str,
    actor: str | None = None,
    target: str | None = None,
    value: int | None = None,
) -> dict[str, Any]:
    return {
        "id": str(uuid.uuid4()),
        "type": event_type,
        "message": message,
        "actor": actor,
        "target": target,
        "value": value,
        "ts": int(time.time() * 1000),  # ms epoch
    }


async def _broadcast(event: dict[str, Any]) -> None:
    _recent_events.append(event)
    dead: list[asyncio.Queue] = []
    for q in _subscribers:
        try:
            q.put_nowait(event)
        except asyncio.QueueFull:
            dead.append(q)
    for q in dead:
        _subscribers.remove(q)


def add_subscriber(q: asyncio.Queue) -> None:
    _subscribers.append(q)


def remove_subscriber(q: asyncio.Queue) -> None:
    try:
        _subscribers.remove(q)
    except ValueError:
        pass


def get_recent(limit: int = 20) -> list[dict[str, Any]]:
    """Últimos N eventos en orden cronológico (más reciente al final)."""
    events = list(_recent_events)
    return events[-limit:]


# ─── Funciones de emisión ─────────────────────────────────────────────────────

async def emit_challenge_complete(username: str, challenge_title: str) -> None:
    ev = _make_event(
        event_type="challenge_complete",
        message=f"[{username}] completó el reto «{challenge_title}».",
        actor=username,
        value=None,
    )
    await _broadcast(ev)


async def emit_level_up(username: str, new_level: int) -> None:
    ev = _make_event(
        event_type="level_up",
        message=f"[{username}] subió al Nivel {new_level}.",
        actor=username,
        value=new_level,
    )
    await _broadcast(ev)


async def emit_boss_defeated(username: str) -> None:
    ev = _make_event(
        event_type="boss_defeated",
        message=f"[{username}] ha derrotado al Jefe THE INFINITE LOOPER.",
        actor=username,
    )
    await _broadcast(ev)


async def emit_duel_result(
    winner: str, loser: str, elo_delta: int
) -> None:
    ev = _make_event(
        event_type="duel_result",
        message=f"[{winner}] le ha arrebatado {elo_delta} puntos de Elo a [{loser}] en la Arena.",
        actor=winner,
        target=loser,
        value=elo_delta,
    )
    await _broadcast(ev)


async def emit_league_rank_up(username: str, new_tier: str) -> None:
    ev = _make_event(
        event_type="league_rank_up",
        message=f"[{username}] acaba de alcanzar el rango {new_tier}.",
        actor=username,
        value=None,
    )
    await _broadcast(ev)
