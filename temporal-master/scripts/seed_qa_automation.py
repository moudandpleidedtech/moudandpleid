"""
seed_qa_automation.py — QA Automation: Operaciones Especiales (40 Niveles)
===========================================================================
Disciplina: De Python Core a QA Automation Engineer

Fases:
    ALPHA   (L01–L08): Pytest Assault        — Python  · pytest, fixtures, mocks, cobertura
    BRAVO   (L09–L16): TypeScript Operative  — TS      · generics, async, env, tipos utilitarios
    CHARLIE (L17–L27): Playwright Siege      — TS      · locators, POM, fixtures, intercepción, matrix
    DELTA   (L28–L35): API Hunter            — TS      · HTTP, Supertest, JWT, Zod, perf, GraphQL, Pact
    ECHO    (L36–L40): DevOps Commander      — TS      · GitHub Actions, Allure, config multi-env, Docker, CI

Evaluación:
    - challenge_type="python"     → ejecutado vía Piston Python 3.10
    - challenge_type="typescript" → ejecutado vía Piston TypeScript 5.0.4
    - expected_output comparado con stdout normalizado (strip por línea, NFC, CRLF→LF)

Uso:  python -m scripts.seed_qa_automation
"""
from __future__ import annotations
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# ── Importar fases intermedias ────────────────────────────────────────────────
from scripts._qa_fase1   import FASE1          # L01–L08  (Python)
from scripts._qa_fase2   import FASE2          # L09–L16  (TypeScript)
from scripts._qa_fase3   import FASE3          # L17–L27  (TypeScript)
from scripts._qa_fase4y5 import FASE4, FASE5   # L28–L35, L36–L40 (TypeScript)

# ── Catálogo completo ─────────────────────────────────────────────────────────
QA_AUTOMATION = FASE1 + FASE2 + FASE3 + FASE4 + FASE5   # 40 niveles


# ── Seed standalone ───────────────────────────────────────────────────────────

async def seed() -> None:
    import asyncio
    from sqlalchemy import delete
    from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
    from app.core.config import settings
    from app.models.challenge import Challenge

    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    Session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with Session() as session:
        deleted = await session.execute(
            delete(Challenge).where(Challenge.codex_id == "qa_automation_ops")
        )
        print(f"  QA Automation anterior eliminado — {deleted.rowcount} challenge(s) removidos.")
        print(f"\n  Insertando {len(QA_AUTOMATION)} niveles de QA Automation Ops...\n")

        phase_label = ""
        for data in QA_AUTOMATION:
            # Separador visual de fase
            if data["phase"] != phase_label:
                phase_label = data["phase"]
                descriptions = {
                    "ALPHA":   "Pytest Assault      (L01–L08, Python)",
                    "BRAVO":   "TypeScript Operative(L09–L16, TS)",
                    "CHARLIE": "Playwright Siege    (L17–L27, TS)",
                    "DELTA":   "API Hunter          (L28–L35, TS)",
                    "ECHO":    "DevOps Commander    (L36–L40, TS)",
                }
                print(f"\n  ── FASE {phase_label}: {descriptions.get(phase_label, '')} ──")

            boss_tag  = " [BOSS]"  if data.get("is_phase_boss") else ""
            free_tag  = " [FREE]"  if data.get("is_free")       else ""
            session.add(Challenge(**data))
            print(
                f"    [{data['level_order']:02d}] {data['title']:<58} "
                f"({data['challenge_type'].upper()}, {data['difficulty'].upper()}{boss_tag}{free_tag})"
            )

        await session.commit()

    await engine.dispose()

    total     = len(QA_AUTOMATION)
    python_n  = sum(1 for d in QA_AUTOMATION if d["challenge_type"] == "python")
    ts_n      = sum(1 for d in QA_AUTOMATION if d["challenge_type"] == "typescript")
    boss_n    = sum(1 for d in QA_AUTOMATION if d.get("is_phase_boss"))
    free_n    = sum(1 for d in QA_AUTOMATION if d.get("is_free"))

    print(f"\n  ══════════════════════════════════════════════════")
    print(f"  QA Automation Ops — {total} niveles cargados.")
    print(f"    codex_id  = 'qa_automation_ops'")
    print(f"    Python    = {python_n}   TypeScript = {ts_n}")
    print(f"    Boss gates= {boss_n}   Free tiers = {free_n}")
    print(f"  ══════════════════════════════════════════════════\n")


if __name__ == "__main__":
    import asyncio
    asyncio.run(seed())
