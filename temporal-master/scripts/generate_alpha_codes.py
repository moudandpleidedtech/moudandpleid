"""
generate_alpha_codes.py — Fabricante de Munición (Operación Vanguardia)
────────────────────────────────────────────────────────────────────────
Genera N Alpha Codes únicos de un solo uso e inserta en la tabla alpha_codes.

Uso (desde temporal-master/):
    python -m scripts.generate_alpha_codes
    python -m scripts.generate_alpha_codes --count 50
    python -m scripts.generate_alpha_codes --count 100 --prefix VANG

Estrategia de unicidad (sin IntegrityError mid-transaction):
    1. Genera todos los códigos en memoria usando secrets.choice().
    2. Deduplica el batch en memoria (set).
    3. Consulta la DB con SELECT ... WHERE code IN (...) para filtrar preexistentes.
    4. Inserta solo los nuevos en una transacción atómica única.
    → Resultado: 0 riesgo de transacción abortada, 0 duplicados en la Bóveda.

Seguridad del token:
    - secrets.choice()  → CSPRNG, no predecible, no enumerable.
    - Alfabeto depurado → excluye O/0/I/1 (anti-confusión visual al distribuir).
    - Formato           → PREFIX-XXXX-XXXX (ej. VANG-3K7P-X9QR).
"""

from __future__ import annotations

import argparse
import asyncio
import secrets
import string
import sys
from typing import Final

sys.path.insert(0, ".")  # permite importar `app.*` desde temporal-master/

# ── Constantes ────────────────────────────────────────────────────────────────

# Alfabeto sin ambigüedad visual: sin O (≈0), sin I (≈1)
_SAFE_ALPHABET: Final[str] = "".join(
    c for c in (string.ascii_uppercase + string.digits)
    if c not in ("O", "0", "I", "1")
)

_SEGMENT_LEN: Final[int] = 4     # longitud de cada segmento: XXXX
_DEFAULT_COUNT: Final[int] = 50


# ── Generación de tokens ──────────────────────────────────────────────────────

def _segment() -> str:
    return "".join(secrets.choice(_SAFE_ALPHABET) for _ in range(_SEGMENT_LEN))


def _make_code(prefix: str) -> str:
    return f"{prefix}-{_segment()}-{_segment()}"


def _generate_batch(count: int, prefix: str) -> list[str]:
    """
    Genera `count` códigos únicos en memoria.
    Si hay colisión interna (probabilidad ~1/10^12), regenera hasta cubrir el total.
    """
    codes: set[str] = set()
    while len(codes) < count:
        codes.add(_make_code(prefix))
    return list(codes)


# ── Lógica principal ──────────────────────────────────────────────────────────

async def _run(count: int, prefix: str) -> None:
    from sqlalchemy import select

    from app.core.database import AsyncSessionLocal, init_db
    from app.models.alpha_code import AlphaCode

    # ── 1. Asegurar que las tablas existen ────────────────────────────────────
    print("▶  Conectando con la Bóveda Alpha (init_db)...")
    try:
        await init_db()
    except Exception as exc:
        print(f"\n✗  Error al inicializar la DB: {exc}")
        sys.exit(1)
    print("   Conexión establecida.\n")

    # ── 2. Generar batch en memoria ───────────────────────────────────────────
    print(f"▶  Fabricando {count} municiones [{prefix}-XXXX-XXXX]...")
    candidate_codes = _generate_batch(count, prefix)

    # ── 3. Filtrar preexistentes en la DB (una sola query) ───────────────────
    async with AsyncSessionLocal() as session:
        existing_result = await session.execute(
            select(AlphaCode.code).where(AlphaCode.code.in_(candidate_codes))
        )
        existing_codes: set[str] = {row[0] for row in existing_result.fetchall()}

    if existing_codes:
        print(f"   [INFO] {len(existing_codes)} código(s) ya existen en la Bóveda — se omitirán.")

    new_codes = [c for c in candidate_codes if c not in existing_codes]

    if not new_codes:
        print("\n⚠   Todos los códigos generados ya existen en la DB. No hay nada que insertar.")
        sys.exit(0)

    # ── 4. Insertar en transacción atómica ────────────────────────────────────
    print(f"▶  Almacenando {len(new_codes)} código(s) en la Bóveda Alpha...")
    try:
        async with AsyncSessionLocal() as session:
            async with session.begin():
                session.add_all([
                    AlphaCode(code=code, is_used=False)
                    for code in new_codes
                ])
    except Exception as exc:
        print(f"\n✗  Error durante la inserción: {exc}")
        print("   Ningún código fue guardado (transacción revertida).")
        sys.exit(1)

    # ── 5. Imprimir lista de códigos generados ────────────────────────────────
    print()
    print("─" * 46)
    print(f"  {'#':>3}   {'CÓDIGO':<18}   {'ESTADO'}")
    print("─" * 46)
    for i, code in enumerate(new_codes, 1):
        print(f"  {i:>3}.  {code:<18}   [ DISPONIBLE ]")
    print("─" * 46)

    # ── 6. Mensaje de éxito ───────────────────────────────────────────────────
    print(f"\n✅  {len(new_codes)} municiones generadas y almacenadas en la Bóveda Alpha.")
    if existing_codes:
        print(f"⚠   {len(existing_codes)} código(s) omitidos por duplicado.")


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fabricante de Munición — Genera Alpha Codes para la Operación Vanguardia",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Ejemplos:\n"
            "  python -m scripts.generate_alpha_codes\n"
            "  python -m scripts.generate_alpha_codes --count 50\n"
            "  python -m scripts.generate_alpha_codes --count 100 --prefix VANG\n"
        ),
    )
    parser.add_argument(
        "--count",
        type=int,
        default=_DEFAULT_COUNT,
        help=f"Cantidad de códigos a generar (default: {_DEFAULT_COUNT})",
    )
    parser.add_argument(
        "--prefix",
        type=str,
        default="VANG",
        help="Prefijo del token (default: VANG)",
    )
    args = parser.parse_args()

    if args.count < 1 or args.count > 10_000:
        print("✗  --count debe estar entre 1 y 10.000.")
        sys.exit(1)

    asyncio.run(_run(args.count, args.prefix.upper().strip()))


if __name__ == "__main__":
    main()
