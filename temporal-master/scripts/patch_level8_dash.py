"""
patch_level8_dash.py — Corrige el guión largo en el nivel 8 (Protocolo de Identificación).

Problema: expected_output, description, initial_code y hints_json usaban em-dash (—, U+2014)
o en-dash (–, U+2013) en lugar del guión simple (-). Esto hacía imposible completar el
nivel porque el usuario no puede teclear esos caracteres fácilmente.

Uso:
    python -m scripts.patch_level8_dash
"""

import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import settings
from app.models.challenge import Challenge

_engine = create_async_engine(settings.DATABASE_URL, echo=False)
_Session = async_sessionmaker(_engine, expire_on_commit=False)

EM_DASH = "\u2014"
EN_DASH = "\u2013"


def _fix(text: str) -> str:
    return text.replace(EM_DASH, "-").replace(EN_DASH, "-")


async def patch() -> None:
    async with _Session() as session:
        result = await session.execute(
            select(Challenge).where(Challenge.level_order == 8)
        )
        challenge = result.scalar_one_or_none()

        if challenge is None:
            print("✗ No se encontró el nivel 8. Verifica que la base de datos esté seeded.")
            return

        changed = []

        new_expected = _fix(challenge.expected_output or "")
        if new_expected != challenge.expected_output:
            challenge.expected_output = new_expected
            changed.append("expected_output")

        new_desc = _fix(challenge.description or "")
        if new_desc != challenge.description:
            challenge.description = new_desc
            changed.append("description")

        new_ic = _fix(challenge.initial_code or "")
        if new_ic != challenge.initial_code:
            challenge.initial_code = new_ic
            changed.append("initial_code")

        if challenge.hints_json:
            # hints_json stores JSON with ensure_ascii=True by default, so em-dash
            # appears as literal \u2014 (6 chars), not as the actual character.
            # We need to fix both the literal JSON-escape form AND the actual char form.
            new_hints_json = (
                challenge.hints_json
                .replace("\\u2014", "-").replace("\\u2013", "-")  # JSON-escaped form
                .replace(EM_DASH,    "-").replace(EN_DASH,    "-")  # actual char form
            )
            if new_hints_json != challenge.hints_json:
                challenge.hints_json = new_hints_json
                changed.append("hints_json")

        if challenge.syntax_hint:
            new_sh = _fix(challenge.syntax_hint)
            if new_sh != challenge.syntax_hint:
                challenge.syntax_hint = new_sh
                changed.append("syntax_hint")

        if changed:
            await session.commit()
            print(f"✓ Nivel 8 '{challenge.title}' actualizado.")
            print(f"  Campos modificados: {', '.join(changed)}")
            print(f"  expected_output ahora: {challenge.expected_output!r}")
        else:
            print(f"  Nivel 8 '{challenge.title}' ya estaba correcto, no se modificó.")

    await _engine.dispose()


if __name__ == "__main__":
    asyncio.run(patch())
