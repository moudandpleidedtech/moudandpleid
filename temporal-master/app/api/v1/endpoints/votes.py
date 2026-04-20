from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

router = APIRouter(prefix="/votes", tags=["votes"])

# Offset base para simular tráfico preexistente
_BASE = {"negocios": 347, "tecnologia": 289}
_VALID = set(_BASE.keys())


@router.get("")
async def get_votes(db: AsyncSession = Depends(get_db)):
    rows = await db.execute(text("SELECT category, count FROM ebook_votes"))
    counts = {row.category: row.count for row in rows}
    return {
        "negocios":   counts.get("negocios",   0) + _BASE["negocios"],
        "tecnologia": counts.get("tecnologia", 0) + _BASE["tecnologia"],
    }


@router.post("/{category}")
async def cast_vote(category: str, db: AsyncSession = Depends(get_db)):
    if category not in _VALID:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Categoría inválida")

    await db.execute(
        text("""
            INSERT INTO ebook_votes (category, count)
            VALUES (:cat, 1)
            ON CONFLICT (category) DO UPDATE SET count = ebook_votes.count + 1
        """),
        {"cat": category},
    )
    await db.commit()

    rows = await db.execute(text("SELECT category, count FROM ebook_votes"))
    counts = {row.category: row.count for row in rows}
    return {
        "negocios":   counts.get("negocios",   0) + _BASE["negocios"],
        "tecnologia": counts.get("tecnologia", 0) + _BASE["tecnologia"],
    }
