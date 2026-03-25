"""
scripts/create_founder.py — Protocolo God Mode (D022)

Promueve a un usuario existente al rol FOUNDER y activa su suscripción.

Uso:
    python -m scripts.create_founder --email adrian@daki.dev
    python -m scripts.create_founder --email adrian@daki.dev --dry-run

Efectos:
    - user.role               = 'FOUNDER'
    - user.is_licensed        = True
    - user.subscription_status = 'ACTIVE'

El FOUNDER bypassa todas las compuertas de catálogo (Niebla de Guerra).
Ver: app/core/access.py → check_catalog_gate(), check_incursion_access()
"""

import argparse
import asyncio
import sys
from pathlib import Path

# Asegurar que el root del proyecto está en sys.path cuando se ejecuta como módulo
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select

from app.core.database import AsyncSessionLocal, init_db
from app.models.user import User


async def promote_to_founder(email: str, dry_run: bool = False) -> None:
    await init_db()

    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()

        if user is None:
            print(f"✗  Operador no encontrado: {email}")
            sys.exit(1)

        print(f"╔══════════════════════════════════════════════════╗")
        print(f"║         PROTOCOLO GOD MODE — ACTIVACIÓN          ║")
        print(f"╠══════════════════════════════════════════════════╣")
        print(f"║  Callsign : {user.callsign:<38}║")
        print(f"║  Email    : {user.email:<38}║")
        print(f"║  Rol actual: {user.role:<37}║")
        print(f"║  Sub status: {user.subscription_status:<37}║")
        print(f"╚══════════════════════════════════════════════════╝")

        if user.role == "FOUNDER":
            print("ℹ  Este Operador ya tiene rol FOUNDER. Sin cambios.")
            return

        if dry_run:
            print("\n[DRY RUN] Cambios que se aplicarían:")
            print(f"  role               : {user.role!r} → 'FOUNDER'")
            print(f"  is_licensed        : {user.is_licensed} → True")
            print(f"  subscription_status: {user.subscription_status!r} → 'ACTIVE'")
            print("\n[DRY RUN] Sin cambios en la BD. Pasa --no-dry-run para aplicar.")
            return

        user.role                = "FOUNDER"
        user.is_licensed         = True
        user.subscription_status = "ACTIVE"
        await session.commit()
        await session.refresh(user)

        print(f"\n✅  FOUNDER activado para {user.callsign} ({user.email})")
        print(f"   role               = {user.role!r}")
        print(f"   is_licensed        = {user.is_licensed}")
        print(f"   subscription_status= {user.subscription_status!r}")
        print("\n   El Operador debe volver a iniciar sesión para recibir el JWT actualizado.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Promueve un usuario al rol FOUNDER (God Mode — D022).",
    )
    parser.add_argument("--email", required=True, help="Email del Operador a promover.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Simula la operación sin modificar la BD (default: True).",
    )
    parser.add_argument(
        "--no-dry-run",
        dest="dry_run",
        action="store_false",
        help="Aplica los cambios en la BD.",
    )
    args = parser.parse_args()

    asyncio.run(promote_to_founder(email=args.email, dry_run=args.dry_run))


if __name__ == "__main__":
    main()
