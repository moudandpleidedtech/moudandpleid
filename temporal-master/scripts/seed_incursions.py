"""
seed_incursions.py — Datos iniciales del Catálogo de Incursiones (D021)

Inserta 4 Incursiones en la BD:
  1 ACTIVE    — "Operación Vanguardia: Fundamentos de Élite"  (Python Core)
  3 ENCRYPTED — TPM Mastery, Ciberseguridad Red Team, Technical Sales Mastery

Lógica: UPSERT por slug — idempotente.
  Si la fila ya existe → actualiza titulo, descripcion, color_acento, icono, ruta.
  El campo `status` NUNCA se sobreescribe si ya existe en la BD,
  para preservar activaciones manuales hechas en producción.

Uso standalone:
  python -m scripts.seed_incursions

Uso programático (desde main.py):
  from scripts.seed_incursions import seed
  await seed()
"""

from __future__ import annotations

import asyncio

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert as pg_insert

from app.core.database import AsyncSessionLocal, init_db
from app.models.incursion import Incursion  # noqa: F401 — registra el modelo en Base


# ─── Datos canónicos ──────────────────────────────────────────────────────────

INCURSIONS: list[dict] = [
    {
        "slug":             "python-core",
        "titulo":           "Operación Vanguardia: Fundamentos de Élite",
        "descripcion": (
            "El protocolo de iniciación del Nexo. "
            "Domina Python desde los fundamentos hasta la arquitectura de sistemas. "
            "100 misiones. 4 sectores. 1 Boss Final. "
            "La base de todo lo que viene después."
        ),
        "status":           "ACTIVE",
        "system_prompt_id": "python",
        "ruta":             "/misiones",
        "color_acento":     "#00FF41",
        "icono":            "⬡",
        "orden":            1,
    },
    {
        "slug":             "tpm-mastery",
        "titulo":           "Technical Project Manager (TPM)",
        "descripcion": (
            "Aprende a gestionar equipos de ingeniería desde las trincheras. "
            "Crisis de oficina, decisiones bajo presión, stakeholders imposibles. "
            "El Desafío 00 te convertirá en el gerente que ningún equipo quiere perder. "
            "[EN CONSTRUCCIÓN — disponible pronto]"
        ),
        "status":           "ENCRYPTED",
        "system_prompt_id": "tpm",
        "ruta":             "/codex/tpm",
        "color_acento":     "#FF6B35",
        "icono":            "◎",
        "orden":            2,
    },
    {
        "slug":             "red-team",
        "titulo":           "Ciberseguridad: Red Team",
        "descripcion": (
            "Protocolo ARES — clasificado. "
            "Aprende a pensar como atacante para construir como defensor. "
            "CTF, análisis de vulnerabilidades, kill-chain ofensivo. "
            "Solo para operadores con clearance."
        ),
        "status":           "ENCRYPTED",
        "system_prompt_id": "cybersec",
        "ruta":             "/codex/red-team",
        "color_acento":     "#FF2D78",
        "icono":            "⬟",
        "orden":            3,
    },
    {
        "slug":             "sales-mastery",
        "titulo":           "Technical Sales Mastery",
        "descripcion": (
            "Convierte tu expertise técnico en ventaja comercial. "
            "Aprende a hablar con CTOs, CEOs y clientes sin perder credibilidad. "
            "20 niveles. 2 Boss Battles. 20 Haikus de Cierre. "
            "Para el ingeniero que quiere cruzar al otro lado de la mesa."
        ),
        "status":           "ENCRYPTED",
        "system_prompt_id": "sales",
        "ruta":             "/codex/sales",
        "color_acento":     "#FFC700",
        "icono":            "◈",
        "orden":            4,
    },
    {
        "slug":             "qa-senior-architect",
        "titulo":           "QA Senior Architect",
        "descripcion": (
            "Protocolo CENTINELA — Formación de élite en Quality Assurance. "
            "Aprende a diseñar escudos para ecosistemas donde el fallo no es opción: "
            "fintech, healthcare, infraestructura cloud. "
            "Análisis de causa raíz, test cases letales, automatización con pytest. "
            "Para el ingeniero que quiere ser la última línea de defensa."
        ),
        "status":           "ENCRYPTED",
        "system_prompt_id": "qa",
        "ruta":             "/codex/qa-senior-architect",
        "color_acento":     "#00D4FF",
        "icono":            "🛡",
        "orden":            5,
    },
    {
        "slug":             "qa-automation-ops",
        "titulo":           "QA Automation: Operaciones Especiales",
        "descripcion": (
            "Protocolo SPECTRE — La transición definitiva de QA Manual a Automation Engineer. "
            "TypeScript, Playwright, API Testing y CI/CD con GitHub Actions. "
            "5 Fases Operativas. 100 misiones. 5 Pruebas de Fuego. "
            "Para el QA consolidado que quiere programar la defensa, no solo describirla."
        ),
        "status":           "ENCRYPTED",
        "system_prompt_id": "qa-automation",
        "ruta":             "/codex/qa-automation-ops",
        "color_acento":     "#7B61FF",
        "icono":            "⚙",
        "orden":            6,
    },
]


# ─── Función principal ────────────────────────────────────────────────────────

async def seed() -> None:
    """
    UPSERT idempotente de las Incursiones canónicas.

    Todos los campos —incluyendo `status`— se sincronizan con INCURSIONS en cada
    ejecución. Esto permite abrir o cerrar Incursiones editando este archivo y
    volviendo a desplegar sin intervención manual en la BD.
    """
    async with AsyncSessionLocal() as session:
        for data in INCURSIONS:
            result = await session.execute(
                select(Incursion).where(Incursion.slug == data["slug"])
            )
            existing = result.scalar_one_or_none()

            if existing is None:
                # INSERT — primera vez
                session.add(Incursion(**data))
                print(f"  ➕ [seed_incursions] INSERT: {data['slug']} [{data['status']}]")
            else:
                # UPDATE — sincroniza todos los campos incluyendo status
                await session.execute(
                    update(Incursion)
                    .where(Incursion.slug == data["slug"])
                    .values(
                        titulo           = data["titulo"],
                        descripcion      = data["descripcion"],
                        system_prompt_id = data["system_prompt_id"],
                        ruta             = data["ruta"],
                        color_acento     = data["color_acento"],
                        icono            = data["icono"],
                        orden            = data["orden"],
                        status           = data["status"],
                    )
                )
                print(f"  ♻️  [seed_incursions] UPDATE: {data['slug']} → status={data['status']}")

        await session.commit()

    print("✅  [seed_incursions] Catálogo de Incursiones sincronizado.")


# ─── Entrada directa ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    async def _main() -> None:
        await init_db()
        await seed()

    asyncio.run(_main())
