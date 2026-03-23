"""
seed_tactical_keys.py — Inyección del lote inicial de Llaves de Override Táctico.

Uso (desde la raíz del proyecto):
    python -m scripts.seed_tactical_keys

Comportamiento:
    - Inserta 5 llaves con max_uses=10, current_uses=0, is_active=True.
    - Usa ON CONFLICT DO NOTHING sobre code_string (UNIQUE) → idempotente.
      Puede ejecutarse múltiples veces sin errores ni duplicados.
    - Normaliza los codes a UPPER antes de insertar (igual que el endpoint).
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import settings
from app.models.tactical_key import TacticalAccessKey  # noqa: F401 — registra la tabla

# ─── Lote inicial ─────────────────────────────────────────────────────────────

TACTICAL_KEYS = [
    {"code_string": "GLITCH-GOLD-INIT", "max_uses": 10, "current_uses": 0, "is_active": True},
    {"code_string": "QA-VANGUARD-10",   "max_uses": 10, "current_uses": 0, "is_active": True},
    {"code_string": "NETZACH-ALPHA",     "max_uses": 10, "current_uses": 0, "is_active": True},
    {"code_string": "DAKI-CORE-00",      "max_uses": 10, "current_uses": 0, "is_active": True},
    {"code_string": "OVERRIDE-NEXUS",    "max_uses": 10, "current_uses": 0, "is_active": True},
]

# ─── Engine ───────────────────────────────────────────────────────────────────

_engine = create_async_engine(settings.DATABASE_URL, echo=False)
_Session = async_sessionmaker(_engine, expire_on_commit=False)

# ─── Runner ───────────────────────────────────────────────────────────────────

async def seed() -> None:
    async with _Session() as session:
        stmt = (
            pg_insert(TacticalAccessKey)
            .values(TACTICAL_KEYS)
            .on_conflict_do_nothing(index_elements=["code_string"])
        )
        await session.execute(stmt)
        await session.commit()

    print("✓ Llaves tácticas inyectadas:")
    for k in TACTICAL_KEYS:
        print(f"  [{k['code_string']}]  max_uses={k['max_uses']}  activa={k['is_active']}")
    print("  Llaves ya existentes: omitidas (ON CONFLICT DO NOTHING).")

    await _engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed())
