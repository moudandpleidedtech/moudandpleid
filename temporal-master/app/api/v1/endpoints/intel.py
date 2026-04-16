"""
app/api/v1/endpoints/intel.py — Inteligencia Operacional DAKI

GET /intel/mastery-radar  — Maestría promedio por categoría conceptual (spider chart data)
GET /intel/error-vault    — Archivo de fallas: errores más frecuentes del Operador
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_operator
from app.models.user import User

import random

from app.core.database import get_db
from app.models.challenge import Challenge
from app.models.concept_mastery import ConceptMastery
from app.models.user_metrics import UserMetric
from app.models.user_progress import UserProgress

router = APIRouter(prefix="/intel", tags=["intel"])

# ── Mapa de clasificación de conceptos ────────────────────────────────────────

_CONCEPT_CATEGORIES: list[tuple[list[str], str]] = [
    (["print", "variable", "string", "integer", "float", "boolean", "bool",
      "tipo", "casting", "type", "format", "fstring", "concatenat"],
     "Variables & Tipos"),
    (["if", "else", "elif", "condition", "comparison", "operador lógico",
      "boolean logic", "and", "or", "not", "condicional"],
     "Control de Flujo"),
    (["for", "while", "loop", "range", "break", "continue", "iterate",
      "iteration", "bucle", "repetición"],
     "Bucles"),
    (["function", "def", "parameter", "return", "scope", "recursion",
      "lambda", "función", "argumento"],
     "Funciones"),
    (["list", "dict", "tuple", "set", "array", "index", "slice",
      "comprehension", "estructura", "collection"],
     "Estructuras"),
    (["class", "object", "oop", "inherit", "method", "encapsulat",
      "polymorphism", "abstraction", "instance", "clase"],
     "OOP"),
    (["input", "file", "api", "request", "json", "module", "import",
      "exception", "error handling", "try", "except", "i/o"],
     "APIs & I/O"),
]

_ORDERED_CATEGORIES = [
    "Variables & Tipos", "Control de Flujo", "Bucles",
    "Funciones", "Estructuras", "OOP", "APIs & I/O",
]


def _classify(concept: str) -> str:
    lower = concept.lower()
    for keywords, category in _CONCEPT_CATEGORIES:
        if any(kw in lower for kw in keywords):
            return category
    return "Otros"


# ── Endpoints ──────────────────────────────────────────────────────────────────

@router.get("/mastery-radar")
async def mastery_radar(
    user_id: uuid.UUID = Query(..., description="UUID del Operador"),
    operator: User = Depends(get_current_operator),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    if user_id != operator.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso denegado.")
    """
    Retorna la maestría promedio por categoría para renderizar el radar chart.
    Score 0-100 por categoría. Categorías sin datos retornan 0.
    """
    result = await db.execute(
        select(ConceptMastery).where(ConceptMastery.user_id == user_id)
    )
    records = result.scalars().all()

    buckets: dict[str, list[float]] = {c: [] for c in _ORDERED_CATEGORIES}
    buckets["Otros"] = []

    for r in records:
        cat = _classify(r.concept_name)
        if cat not in buckets:
            cat = "Otros"
        buckets[cat].append(r.mastery_score)

    axes = []
    for cat in _ORDERED_CATEGORIES:
        scores = buckets[cat]
        avg = round(sum(scores) / len(scores), 1) if scores else 0.0
        axes.append({
            "category": cat,
            "score": avg,
            "count": len(scores),
            "needs_reinforcement": any(s < 40 for s in scores),
        })

    total_mastered = sum(1 for r in records if r.mastery_score >= 70)

    return {
        "axes": axes,
        "total_concepts": len(records),
        "total_mastered": total_mastered,
        "total_reinforcement_needed": sum(1 for r in records if r.needs_reinforcement),
    }


@router.get("/weekly-review")
async def weekly_review(
    user_id: uuid.UUID = Query(..., description="UUID del Operador"),
    operator: User = Depends(get_current_operator),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    if user_id != operator.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso denegado.")
    """
    Retorna conceptos que necesitan refuerzo semanal:
    - updated_at < 7 días atrás (no practicado recientemente)
    - mastery_score < 70 (maestría incompleta)
    Máximo 8 conceptos, ordenados por score ascendente (más débil primero).
    """
    cutoff = datetime.now(timezone.utc) - timedelta(days=7)

    result = await db.execute(
        select(ConceptMastery).where(
            ConceptMastery.user_id == user_id,
            ConceptMastery.mastery_score < 70,
            ConceptMastery.updated_at < cutoff,
        )
    )
    records = result.scalars().all()
    records_sorted = sorted(records, key=lambda r: r.mastery_score)[:8]

    concepts = [
        {
            "concept": r.concept_name,
            "score": round(r.mastery_score, 1),
            "last_seen": r.updated_at.isoformat() if r.updated_at else None,
            "needs_reinforcement": r.needs_reinforcement,
        }
        for r in records_sorted
    ]

    return {
        "concepts": concepts,
        "total": len(concepts),
        "cutoff_days": 7,
    }


@router.get("/error-vault")
async def error_vault(
    user_id: uuid.UUID = Query(..., description="UUID del Operador"),
    operator: User = Depends(get_current_operator),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    if user_id != operator.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso denegado.")
    """
    Agrega errores de syntax_errors_log de todas las misiones del Operador.
    Retorna top 5 errores con frecuencia y estadísticas globales.
    """
    result = await db.execute(
        select(UserMetric).where(UserMetric.user_id == user_id)
    )
    metrics = result.scalars().all()

    error_counts: dict[str, int] = {}
    total_attempts = 0
    total_hints    = 0
    missions_failed = 0

    for m in metrics:
        total_attempts += m.attempts
        total_hints    += m.hints_used
        if m.status == "fail":
            missions_failed += 1
        try:
            errors = json.loads(m.syntax_errors_log or "[]")
            if isinstance(errors, list):
                for err in errors:
                    key = str(err).strip()
                    if key:
                        error_counts[key] = error_counts.get(key, 0) + 1
        except Exception:
            pass

    top = sorted(error_counts.items(), key=lambda x: x[1], reverse=True)[:5]

    return {
        "top_errors": [{"type": t, "count": c} for t, c in top],
        "total_errors_logged": sum(error_counts.values()),
        "total_attempts": total_attempts,
        "total_hints": total_hints,
        "missions_with_data": len(metrics),
        "missions_failed": missions_failed,
    }


@router.get("/pattern-callout")
async def pattern_callout(
    user_id: uuid.UUID = Query(...),
    challenge_id: uuid.UUID = Query(...),
    operator: User = Depends(get_current_operator),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    if user_id != operator.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso denegado.")
    """
    Busca si el operador ya trabajó algún concepto del challenge actual
    en challenges previos completados. Devuelve el primer match para que
    DAKI muestre el callout de patrón en la consola.
    """
    # Obtener conceptos del challenge actual
    current = await db.get(Challenge, challenge_id)
    if not current or not current.concepts_taught_json:
        return {}
    try:
        current_concepts = set(json.loads(current.concepts_taught_json))
    except Exception:
        return {}
    if not current_concepts:
        return {}

    # Challenges completados por el operador (excluyendo el actual)
    result = await db.execute(
        select(UserProgress, Challenge)
        .join(Challenge, Challenge.id == UserProgress.challenge_id)
        .where(
            UserProgress.user_id == user_id,
            UserProgress.completed.is_(True),
            UserProgress.challenge_id != challenge_id,
            Challenge.level_order.isnot(None),
        )
        .order_by(Challenge.level_order)
    )
    rows = result.all()

    for progress, ch in rows:
        try:
            ch_concepts = set(json.loads(ch.concepts_taught_json or "[]"))
        except Exception:
            continue
        overlap = current_concepts & ch_concepts
        if overlap:
            concept = next(iter(overlap))
            return {
                "previous_title": ch.title,
                "previous_level": ch.level_order,
                "concept": concept,
            }
    return {}


@router.get("/retrieval-challenge")
async def retrieval_challenge(
    user_id: uuid.UUID = Query(...),
    concept: str = Query(...),
    operator: User = Depends(get_current_operator),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    if user_id != operator.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso denegado.")
    """
    Devuelve un challenge completado por el operador que trabaje el concepto dado.
    Usado por la Revisión Semanal para activar el protocolo de recuperación.
    """
    result = await db.execute(
        select(UserProgress, Challenge)
        .join(Challenge, Challenge.id == UserProgress.challenge_id)
        .where(
            UserProgress.user_id == user_id,
            UserProgress.completed.is_(True),
            Challenge.concepts_taught_json.contains(concept),
            Challenge.challenge_type == "python",
        )
        .order_by(Challenge.level_order)
    )
    rows = result.all()
    if not rows:
        return {}
    # Elegir uno al azar entre los primeros 5 para variar
    progress, ch = random.choice(rows[:5])
    return {
        "challenge_id": str(ch.id),
        "title": ch.title,
        "level_order": ch.level_order,
        "slug": getattr(ch, "slug", None) or str(ch.id),
    }
