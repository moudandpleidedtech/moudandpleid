"""
seed_beta_codes.py — Inserta los códigos de acceso Beta iniciales.

Uso (desde la raíz del proyecto):
    python -m scripts.seed_beta_codes

Los códigos se insertan solo si no existen (idempotente).
"""

import asyncio

from sqlalchemy import select

from app.core.database import AsyncSessionLocal, engine, Base
from app.models.beta_code import BetaCode

INITIAL_CODES = [
    {"code": "GLITCH-GOLD-INIT",  "max_uses": 10},
    {"code": "NEXO-ALPHA-01",     "max_uses": 20},
    {"code": "DAKI-FOUNDER-001",  "max_uses": 5},
    {"code": "SISTEMA-BREACH",    "max_uses": 15},
    {"code": "OPERATOR-ZERO",     "max_uses": 50},
]


async def main() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        for entry in INITIAL_CODES:
            exists = await db.execute(
                select(BetaCode).where(BetaCode.code == entry["code"])
            )
            if exists.scalar_one_or_none() is None:
                db.add(BetaCode(code=entry["code"], max_uses=entry["max_uses"]))
                print(f"  [+] {entry['code']}")
            else:
                print(f"  [=] {entry['code']} (ya existe)")

        await db.commit()
    print("\n✓ Seed de códigos Beta completado.")


if __name__ == "__main__":
    asyncio.run(main())
