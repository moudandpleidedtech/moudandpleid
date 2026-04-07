"""
app/api/v1/endpoints/campaign.py — Mapa de Campaña (Nexo DAKI)

GET /api/v1/campaign/map?user_id=<uuid>

Devuelve el progreso del operador por nodo del mapa.
La estructura visual de zonas/nodos está en el frontend (CampaignMap.tsx).
Este endpoint solo calcula: completed / unlocked / boss_completed por nodo.
"""

from __future__ import annotations

import uuid
from typing import Any, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.challenge import Challenge
from app.models.user_progress import UserProgress

router = APIRouter(prefix="/campaign", tags=["campaign"])


# ── Definición canónica de nodos del mapa ──────────────────────────────────────
# Cada nodo tiene: id, codex_id (zona), rango level_order min-max
# La estructura visual está en CampaignMap.tsx — estos IDs deben coincidir.

_NODES: list[dict[str, Any]] = [
    # ── PYTHON CORE ──────────────────────────────────────────────────────────
    {"id": "s00_s03", "codex_id": "python_core",       "lo_min": 0,   "lo_max": 30},
    {"id": "s04_s07", "codex_id": "python_core",       "lo_min": 31,  "lo_max": 66},
    # ── AVANZADO ─────────────────────────────────────────────────────────────
    {"id": "s08_s10", "codex_id": "python_avanzado",   "lo_min": 67,  "lo_max": 96},
    {"id": "s11_s13", "codex_id": "python_avanzado",   "lo_min": 97,  "lo_max": 126},
    # ── ÉLITE ─────────────────────────────────────────────────────────────────
    {"id": "s14_s15", "codex_id": "python_elite",      "lo_min": 127, "lo_max": 142},
    {"id": "s16_s18", "codex_id": "python_elite",      "lo_min": 143, "lo_max": 161},
    # ── PROTOCOLOS DE ÉLITE ───────────────────────────────────────────────────
    {"id": "s19_debug",    "codex_id": "protocolos_elite", "lo_min": 162, "lo_max": 169},
    {"id": "s20_interview","codex_id": "protocolos_elite", "lo_min": 170, "lo_max": 179},
    {"id": "s21_predict",  "codex_id": "protocolos_elite", "lo_min": 180, "lo_max": 189},
]


@router.get("/map")
async def get_campaign_map(
    user_id: Optional[uuid.UUID] = Query(None),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """
    Retorna el progreso del operador por nodo del mapa de campaña.
    Sin user_id: solo el primer nodo está desbloqueado.

    Response:
      { zones: { <codex_id>: { <node_id>: { completed, unlocked, boss_completed } } } }
    """
    # Nodo → challenges (level_order range)
    ch_result = await db.execute(
        select(Challenge.id, Challenge.level_order, Challenge.is_phase_boss)
        .where(Challenge.level_order.isnot(None))
        .order_by(Challenge.level_order)
    )
    challenges = ch_result.all()  # (id, level_order, is_phase_boss)

    # ── Progreso del usuario ──────────────────────────────────────────────────
    completed_ids: set[uuid.UUID] = set()
    if user_id:
        prog_result = await db.execute(
            select(UserProgress.challenge_id)
            .where(UserProgress.user_id == user_id, UserProgress.completed.is_(True))
        )
        completed_ids = {row[0] for row in prog_result.all()}

    # ── Calcular estado por nodo ──────────────────────────────────────────────
    # Un nodo está "completed" si el challenge con el mayor level_order en su rango está completado.
    # Un nodo está "boss_completed" si algún is_phase_boss en su rango está completado.
    # Un nodo está "unlocked" si el nodo anterior está completed o boss_completed.

    node_state: dict[str, dict[str, bool]] = {}

    for node in _NODES:
        lo_min, lo_max = node["lo_min"], node["lo_max"]
        in_range = [c for c in challenges if lo_min <= (c[1] or 0) <= lo_max]

        boss_done = any(c[2] and c[0] in completed_ids for c in in_range)
        last_done = bool(in_range and in_range[-1][0] in completed_ids)
        node_state[node["id"]] = {
            "completed":      last_done,
            "boss_completed": boss_done,
        }

    # Determinar unlocked en secuencia
    prev_done = True  # primer nodo siempre desbloqueado
    for node in _NODES:
        node_state[node["id"]]["unlocked"] = prev_done
        ns = node_state[node["id"]]
        prev_done = ns["completed"] or ns["boss_completed"]

    # ── Agrupar por codex_id ──────────────────────────────────────────────────
    zones: dict[str, dict[str, dict[str, bool]]] = {}
    for node in _NODES:
        cid = node["codex_id"]
        if cid not in zones:
            zones[cid] = {}
        zones[cid][node["id"]] = node_state[node["id"]]

    # Total de challenges completados
    total_completed = len(completed_ids)

    return {
        "zones": zones,
        "total_completed": total_completed,
    }
