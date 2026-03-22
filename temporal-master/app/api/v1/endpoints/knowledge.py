"""
GET /api/v1/knowledge           — Lista todos los conceptos tácticos
GET /api/v1/knowledge/{concept_id} — Recupera un concepto por ID
GET /api/v1/knowledge/search?term={term} — Busca por término Python

El frontend usa estos endpoints para poblar los tooltips interactivos
en la terminal cuando DAKI menciona términos con backticks.
"""

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel

from app.services import knowledge_base

router = APIRouter()


class ConceptOut(BaseModel):
    concept_id: str
    tactical_name: str
    python_term: str
    keywords: list[str]
    definition: str
    syntax: str
    example: str
    tactics: str


@router.get(
    "/knowledge",
    response_model=list[ConceptOut],
    summary="Lista todos los conceptos de la Base de Conocimiento Táctica",
    tags=["knowledge"],
)
def list_concepts() -> list[ConceptOut]:
    return [ConceptOut(**c) for c in knowledge_base.list_concepts()]


@router.get(
    "/knowledge/search",
    response_model=ConceptOut | None,
    summary="Busca un concepto por término Python (ej: 'for', 'range()', 'dict')",
    tags=["knowledge"],
)
def search_concept(term: str = Query(..., description="Término Python a buscar")) -> ConceptOut | None:
    concept_id = knowledge_base.find_by_keyword(term)
    if concept_id is None:
        return None
    data = knowledge_base.get_concept(concept_id)
    if data is None:
        return None
    return ConceptOut(concept_id=concept_id, **data)


@router.get(
    "/knowledge/{concept_id}",
    response_model=ConceptOut,
    summary="Recupera un concepto táctico por su ID",
    tags=["knowledge"],
)
def get_concept(concept_id: str) -> ConceptOut:
    data = knowledge_base.get_concept(concept_id)
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Concepto '{concept_id}' no encontrado en la Base de Conocimiento.",
        )
    return ConceptOut(concept_id=concept_id, **data)
