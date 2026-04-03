"""
seed_qa_architect.py — QA Senior Architect: 100 Niveles (Sector 20)
====================================================================
Disciplina: QA de Ecosistemas Críticos

Fases:
    fundamentos       (L01–L20): Arquitectura de pruebas y estrategia
    automatizacion_e2e(L21–L40): E2E, Playwright, POM, patrones
    cicd_infra        (L41–L60): CI/CD, pipelines, Docker, coverage
    api_contratos     (L61–L80): HTTP, contratos, GraphQL, caos, seguridad
    perf_liderazgo    (L81–L100): Performance, OWASP, liderazgo QA

Evaluación:
    - challenge_type="python" → ejecutado vía Piston Python 3.10
    - expected_output comparado con stdout normalizado

Uso:  python -m scripts.seed_qa_architect
"""
from __future__ import annotations
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# ── Importar bloques ─────────────────────────────────────────────────────────
from scripts._qa_arch_b1 import BLOQUE1   # L01–L20  fundamentos
from scripts._qa_arch_b2 import BLOQUE2   # L21–L40  automatizacion_e2e
from scripts._qa_arch_b3 import BLOQUE3   # L41–L60  cicd_infra
from scripts._qa_arch_b4 import BLOQUE4   # L61–L80  api_contratos
from scripts._qa_arch_b5 import BLOQUE5   # L81–L100 perf_liderazgo

# ── Catálogo completo ─────────────────────────────────────────────────────────
QA_ARCHITECT = BLOQUE1 + BLOQUE2 + BLOQUE3 + BLOQUE4 + BLOQUE5   # 100 niveles


# ── Seed standalone ───────────────────────────────────────────────────────────

async def seed() -> None:
    import asyncio
    from sqlalchemy import delete
    from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
    from app.core.config import settings
    from app.models.challenge import Challenge

    engine  = create_async_engine(settings.DATABASE_URL, echo=False)
    Session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with Session() as session:
        deleted = await session.execute(
            delete(Challenge).where(Challenge.codex_id == "qa_senior_architect")
        )
        print(f"  QA Architect anterior eliminado — {deleted.rowcount} challenge(s) removidos.")
        print(f"\n  Insertando {len(QA_ARCHITECT)} niveles de QA Senior Architect...\n")

        phase_label = ""
        phase_descriptions = {
            "fundamentos":        "Arquitectura & Estrategia   (L01–L20, Python)",
            "automatizacion_e2e": "Automatización E2E          (L21–L40, Python)",
            "cicd_infra":         "CI/CD & Infraestructura     (L41–L60, Python)",
            "api_contratos":      "API & Contratos             (L61–L80, Python)",
            "perf_liderazgo":     "Performance & Liderazgo     (L81–L100, Python)",
        }

        for data in QA_ARCHITECT:
            if data["phase"] != phase_label:
                phase_label = data["phase"]
                print(f"\n  ── FASE {phase_label}: {phase_descriptions.get(phase_label, '')} ──")

            boss_tag = " [BOSS]"    if data.get("is_phase_boss") else ""
            proj_tag = " [PROJECT]" if data.get("is_project")    else ""
            free_tag = " [FREE]"    if data.get("is_free")        else ""
            session.add(Challenge(**data))
            print(
                f"    [{data['level_order']:03d}] {data['title']:<58} "
                f"({data['difficulty'].upper()}{boss_tag}{proj_tag}{free_tag})"
            )

        await session.commit()

    await engine.dispose()

    total   = len(QA_ARCHITECT)
    boss_n  = sum(1 for d in QA_ARCHITECT if d.get("is_phase_boss"))
    proj_n  = sum(1 for d in QA_ARCHITECT if d.get("is_project"))
    free_n  = sum(1 for d in QA_ARCHITECT if d.get("is_free"))

    print(f"\n  ══════════════════════════════════════════════════")
    print(f"  QA Senior Architect — {total} niveles cargados.")
    print(f"    codex_id  = 'qa_senior_architect'")
    print(f"    sector_id = 20   (todos Python)")
    print(f"    Boss gates= {boss_n}   Projects = {proj_n}   Free = {free_n}")
    print(f"  ══════════════════════════════════════════════════\n")


if __name__ == "__main__":
    import asyncio
    asyncio.run(seed())
