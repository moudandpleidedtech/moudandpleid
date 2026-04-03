"""
seed_tpm_mastery.py — TPM Mastery: El Líder Técnico Completo (150 Niveles)
===========================================================================
Disciplina: De coordinador a Director Estratégico TPM

Fases:
    B1  (L001–L015): programa_fundamentos      — OKRs, WBS, RACI, CPM, Risk, Roadmap
    B2  (L016–L030): credibilidad_tecnica       — SLA/SLO, DORA, Incident, CI/CD, Tech Debt
    B3  (L031–L045): finanzas_negocio           — ROI, Break-even, P&L, TCO, Burn Rate
    B4  (L046–L060): comunicacion_ejecutiva     — SCR, Escalation, OKR Updates, QBR
    B5  (L061–L075): ejecucion_entrega          — EVM, Burndown, Release Gates, Sprint
    B6  (L076–L090): liderazgo_personas         — 1-on-1, SBI, Hiring, Onboarding, GROW
    B7  (L091–L105): negociacion_influencia     — BATNA, ZOPA, Influence Map, Coalition
    B8  (L106–L120): gestion_cambio             — ADKAR, Kotter, Adoption Curve, CHCM
    B9  (L121–L135): decision_frameworks        — RICE, MoSCoW, Kano, ICE, Weighted Matrix
    B10 (L136–L150): tpm_ai_estrategia          — ML Lifecycle, AI Risk, Token Cost, ROI

Evaluación:
    - challenge_type="python" → ejecutado vía Piston Python 3.10
    - expected_output comparado con stdout normalizado (strip por línea, NFC, CRLF→LF)
    - strict_match=False en todos los niveles

Uso:  python -m scripts.seed_tpm_mastery
"""
from __future__ import annotations
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# ── Importar bloques ──────────────────────────────────────────────────────────
from scripts._tpm_b1  import BLOQUE1   # L001–L015  programa_fundamentos
from scripts._tpm_b2  import BLOQUE2   # L016–L030  credibilidad_tecnica
from scripts._tpm_b3  import BLOQUE3   # L031–L045  finanzas_negocio
from scripts._tpm_b4  import BLOQUE4   # L046–L060  comunicacion_ejecutiva
from scripts._tpm_b5  import BLOQUE5   # L061–L075  ejecucion_entrega
from scripts._tpm_b6  import BLOQUE6   # L076–L090  liderazgo_personas
from scripts._tpm_b7  import BLOQUE7   # L091–L105  negociacion_influencia
from scripts._tpm_b8  import BLOQUE8   # L106–L120  gestion_cambio
from scripts._tpm_b9  import BLOQUE9   # L121–L135  decision_frameworks
from scripts._tpm_b10 import BLOQUE10  # L136–L150  tpm_ai_estrategia

# ── Catálogo completo ─────────────────────────────────────────────────────────
TPM_MASTERY = (
    BLOQUE1 + BLOQUE2 + BLOQUE3 + BLOQUE4 + BLOQUE5
    + BLOQUE6 + BLOQUE7 + BLOQUE8 + BLOQUE9 + BLOQUE10
)  # 150 niveles


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
            delete(Challenge).where(Challenge.codex_id == "tpm_mastery")
        )
        print(f"  TPM Mastery anterior eliminado — {deleted.rowcount} challenge(s) removidos.")
        print(f"\n  Insertando {len(TPM_MASTERY)} niveles de TPM Mastery...\n")

        phase_label = ""
        phase_descriptions = {
            "programa_fundamentos":   "Fundamentos del Programa  (L001–L015)",
            "credibilidad_tecnica":   "Credibilidad Técnica       (L016–L030)",
            "finanzas_negocio":       "Finanzas y Negocio         (L031–L045)",
            "comunicacion_ejecutiva": "Comunicación Ejecutiva     (L046–L060)",
            "ejecucion_entrega":      "Ejecución y Entrega        (L061–L075)",
            "liderazgo_personas":     "Liderazgo y Personas       (L076–L090)",
            "negociacion_influencia": "Negociación e Influencia   (L091–L105)",
            "gestion_cambio":         "Gestión del Cambio         (L106–L120)",
            "decision_frameworks":    "Frameworks de Decisión     (L121–L135)",
            "tpm_ai_estrategia":      "TPM + IA y Estrategia      (L136–L150)",
        }

        for data in TPM_MASTERY:
            if data["phase"] != phase_label:
                phase_label = data["phase"]
                desc = phase_descriptions.get(phase_label, phase_label)
                print(f"\n  ── FASE: {desc} ──")

            boss_tag = " [BOSS]"    if data.get("is_phase_boss") else ""
            free_tag = " [FREE]"    if data.get("is_free")       else ""
            proj_tag = " [PROJECT]" if data.get("is_project")    else ""
            # Mapea 'hint' → 'syntax_hint' (campo real del modelo Challenge)
            row = {k: v for k, v in data.items() if k != "hint"}
            if data.get("hint"):
                row["syntax_hint"] = data["hint"]
            session.add(Challenge(**row))
            print(
                f"    [{data['level_order']:03d}] {data['title']:<55} "
                f"({data['difficulty'].upper()}{boss_tag}{free_tag}{proj_tag})"
            )

        await session.commit()

    await engine.dispose()

    total    = len(TPM_MASTERY)
    boss_n   = sum(1 for d in TPM_MASTERY if d.get("is_phase_boss"))
    free_n   = sum(1 for d in TPM_MASTERY if d.get("is_free"))
    phases   = len(set(d["phase"] for d in TPM_MASTERY))

    print(f"\n  ══════════════════════════════════════════════════════════")
    print(f"  TPM Mastery — {total} niveles cargados exitosamente.")
    print(f"    codex_id    = 'tpm_mastery'")
    print(f"    sector_id   = 21")
    print(f"    Fases       = {phases}   Boss gates = {boss_n}   Free tiers = {free_n}")
    print(f"    Rango       = L001 – L150")
    print(f"  ══════════════════════════════════════════════════════════\n")


if __name__ == "__main__":
    import asyncio
    asyncio.run(seed())
