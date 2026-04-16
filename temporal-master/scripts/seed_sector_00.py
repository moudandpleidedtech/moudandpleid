"""
Seed — SECTOR 00: Protocolo de Calibración Sináptica (1 nivel tutorial).

Uso (desde la raíz del proyecto):
    python -m scripts.seed_sector_00

Comportamiento:
    1. Elimina solo los challenges con sector_id = 0 (idempotente).
    2. Inserta el Protocolo 00 (challenge_type='tutorial').
       Este challenge debe completarse antes de que se desbloqueen
       las incursiones del Sector 01.
"""

import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.models.challenge import Challenge, DifficultyTier

# ─── Contenido del Sector 00 ──────────────────────────────────────────────────

SECTOR_00 = [
    {
        "title": "[ PROTOCOLO 00: CALIBRACIÓN SINÁPTICA ]",
        "description": (
            "Calibración sináptica obligatoria antes de infiltrarte en el Nexo.\n\n"
            "Completa las 4 fases guiadas por DAKI: diagnostica el sistema, corrige "
            "sintaxis rota, asigna memoria y aprende el retorno de señal.\n\n"
            "Cada fase incrementa el enlace neuronal un 25%."
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "easy",
        "base_xp_reward": 50,
        "initial_code": 'print("Iniciando enlace neuronal...")\n',
        "expected_output": "Enlace Listo",
        "test_inputs_json": json.dumps([]),
        "sector_id": 0,
        "level_order": 0,
        "phase": "tutorial",
        "concepts_taught_json": json.dumps(["print", "sintaxis", "variables", "return"]),
        "challenge_type": "tutorial",
        "is_project": False,
        "telemetry_goal_time": 300,
        "theory_content": None,
        "lore_briefing": None,
        "pedagogical_objective": (
            "Introducir los conceptos de print, SyntaxError, variables y return "
            "mediante un tutorial guiado de 4 fases interactivas."
        ),
        "syntax_hint": (
            'def finalizar_enlace():\n'
            '    return "Enlace Listo"\n\n'
            'print(finalizar_enlace())\n'
        ),
        "hints_json": json.dumps([
            "Fase 2: corrige el SyntaxError (faltan comillas o paréntesis).",
            "Fase 3: asigna un valor a la variable antes de hacer print.",
            "Fase 4: define la función con 'def' y usa 'return' para devolver el valor.",
        ]),
        "is_free": True,
    },
]


# ─── Lógica de población ──────────────────────────────────────────────────────

async def seed() -> None:
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with SessionLocal() as session:
        deleted = await session.execute(
            delete(Challenge).where(Challenge.sector_id == 0)
        )
        deleted_count = deleted.rowcount
        await session.flush()
        print(f"🧹  Sector 00 anterior eliminado — {deleted_count} challenge(s) removidos.")

        print(f"\n🌱  Insertando {len(SECTOR_00)} nivel(es) del Sector 00...\n")
        for data in SECTOR_00:
            challenge = Challenge(**data)
            session.add(challenge)
            print(
                f"    [00/00] {data['title']:<45} "
                f"(TUTORIAL, {data['base_xp_reward']} XP)"
            )

        await session.commit()

    await engine.dispose()
    print(f"\n✅  Sector 00 cargado — Protocolo de Calibración listo.\n")


if __name__ == "__main__":
    asyncio.run(seed())
