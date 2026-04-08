"""
scripts/create_demo_user.py — Usuario de demostración DAKI EdTech

Crea (o resetea) una cuenta de demo con TODAS las misiones completadas.
El usuario aparece como el mejor estudiante posible: cada challenge de
Python Core resuelto, stats de élite, listo para impresionar a un CTO.

PERFIL DEL USUARIO DEMO
──────────────────────
  Callsign  : DEMO_OPERATOR
  Email     : demo@dakiedtech.com       ← agregar a ALPHA_WHITELIST si está activa
  Password  : DemoDaki2025!
  XP        : 45.000
  Racha     : 30 días
  Liga      : Diamante
  Suscripción: ACTIVE (acceso completo)

  Nivel actual: se calcula automáticamente como el total de challenges
  en BD + 1 (siempre estará en el siguiente nivel disponible).

PROGRESO PRE-CARGADO
────────────────────
  Completa TODOS los challenges de Python Core (codex_id IS NULL o
  'python_core') en el mismo orden que los retorna el endpoint /challenges.
  Eso garantiza que la cadena de unlock quede 100% verde.

USO
───
  # Dry-run (solo muestra qué haría):
  python -m scripts.create_demo_user

  # Crear en la BD:
  python -m scripts.create_demo_user --no-dry-run

  # Resetear un demo existente:
  python -m scripts.create_demo_user --no-dry-run --reset

  # Email personalizado:
  python -m scripts.create_demo_user --no-dry-run --email demo@cliente.com --callsign DEV_LEAD

DESPUÉS DE EJECUTAR
───────────────────
  1. Agregar el email a ALPHA_WHITELIST en Render (si está activa)
  2. Ir a dakiedtech.com/login
  3. Ingresar con las credenciales — aterriza directo en /hub con todo completado
"""

import argparse
import asyncio
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import delete, nulls_last, or_, select

from app.core.database import AsyncSessionLocal, init_db
from app.core.security import hash_password
from app.models.challenge import Challenge
from app.models.user import User
from app.models.user_metrics import UserMetric
from app.models.user_progress import UserProgress

# ─── Configuración del usuario demo ───────────────────────────────────────────

DEMO_EMAIL    = "demo@dakiedtech.com"
DEMO_CALLSIGN = "DEMO_OPERATOR"
DEMO_PASSWORD = "DemoDaki2025!"

DEMO_XP      = 45_000
DEMO_STREAK  = 30
DEMO_LEAGUE  = "Diamante"


# ─── Core ─────────────────────────────────────────────────────────────────────

async def run(
    email: str,
    callsign: str,
    password: str,
    reset: bool,
    dry_run: bool,
) -> None:
    await init_db()

    async with AsyncSessionLocal() as session:

        # ── Verificar si ya existe ─────────────────────────────────────────────
        result = await session.execute(select(User).where(User.email == email))
        existing = result.scalar_one_or_none()

        if existing and not reset:
            print(f"\n⚠  Ya existe un usuario con email {email!r}.")
            print(f"   Callsign: {existing.callsign} | Nivel: {existing.current_level}")
            print(f"   Pasá --reset para borrarlo y recrearlo desde cero.\n")
            return

        # ── Reset: limpiar usuario existente ──────────────────────────────────
        if existing and reset:
            if dry_run:
                print(f"[DRY RUN] Se eliminaría el usuario {existing.callsign!r} y todo su progreso.")
            else:
                # Cascade elimina progress y metrics por FK ondelete=CASCADE
                await session.execute(delete(User).where(User.email == email))
                await session.commit()
                print(f"♻  Usuario anterior eliminado: {existing.callsign!r}")
            existing = None

        # ── Cargar challenges — EXACTAMENTE igual que el endpoint /challenges ──
        # codex_id IS NULL (legacy Python) o 'python_core' explícito
        python_only = or_(Challenge.codex_id.is_(None), Challenge.codex_id == "python_core")
        ch_result = await session.execute(
            select(Challenge)
            .where(python_only)
            .order_by(nulls_last(Challenge.level_order), Challenge.base_xp_reward)
        )
        challenges = ch_result.scalars().all()

        if not challenges:
            print("⚠  No se encontraron challenges de Python Core en la BD.")
            print("   Verificá que la base de datos tenga datos cargados.")
            return

        # El nivel demo es el siguiente al último challenge (siempre un paso adelante)
        demo_level = len(challenges) + 1

        # ── Preview ───────────────────────────────────────────────────────────
        _print_preview(email, callsign, challenges, demo_level, dry_run)

        if dry_run:
            print("\n[DRY RUN] Sin cambios. Pasá --no-dry-run para aplicar.\n")
            return

        # ── Crear usuario ──────────────────────────────────────────────────────
        now = datetime.now(timezone.utc)
        user = User(
            email=email,
            callsign=callsign,
            password_hash=hash_password(password),
            current_level=demo_level,
            total_xp=DEMO_XP,
            streak_days=DEMO_STREAK,
            league_tier=DEMO_LEAGUE,
            is_licensed=True,
            subscription_status="ACTIVE",
            last_login=now,
            mission_state={},
        )
        session.add(user)
        await session.flush()  # obtener user.id

        # ── Crear progreso y métricas para TODOS los challenges ────────────────
        n = len(challenges)
        for i, challenge in enumerate(challenges):
            is_boss = challenge.challenge_type == "boss" if challenge.challenge_type else False

            # Stats que parecen de un estudiante élite:
            # - Siempre resuelve en el primer o segundo intento
            # - Usa pocas pistas (solo en los niveles más difíciles)
            # - Cada vez más rápido (mejora visible)
            attempts = 1 if i % 5 != 3 else 2          # 80% primer intento
            hints    = 0 if i < n * 0.7 else (1 if not is_boss else 0)  # pistas solo al final
            time_ms  = max(45_000, (180 - i) * 800)    # rápido y mejora con el tiempo

            # Distribuye los completed_at en los últimos 35 días (1 por día aprox)
            days_ago = (n - i) * (35.0 / n)
            completed_at = now - timedelta(days=days_ago)

            codex = challenge.codex_id or "python_core"

            session.add(UserProgress(
                user_id=user.id,
                challenge_id=challenge.id,
                completed=True,
                boss_completed=is_boss,
                attempts=attempts,
                hints_used=hints,
                completed_at=completed_at,
                codex_id=codex,
            ))

            session.add(UserMetric(
                user_id=user.id,
                challenge_id=challenge.id,
                attempts=attempts,
                hints_used=hints,
                time_spent_ms=time_ms,
                status="success",
                syntax_errors_log="[]",
                last_attempt_at=completed_at,
            ))

        await session.commit()
        await session.refresh(user)

        _print_success(user, n, email, password)


def _print_preview(
    email: str,
    callsign: str,
    challenges: list,
    demo_level: int,
    dry_run: bool,
) -> None:
    tag = "[DRY RUN] " if dry_run else ""
    n   = len(challenges)
    w   = 54

    print()
    print(f"╔{'═' * w}╗")
    print(f"║{'  DAKI EDTECH — USUARIO DE DEMOSTRACIÓN':^{w}}║")
    print(f"╠{'═' * w}╣")
    rows = [
        ("Callsign",  callsign),
        ("Email",     email),
        ("Password",  DEMO_PASSWORD),
        ("Nivel",     str(demo_level)),
        ("XP",        f"{DEMO_XP:,}"),
        ("Racha",     f"{DEMO_STREAK} días"),
        ("Liga",      DEMO_LEAGUE),
        ("Progreso",  f"{n} challenges (TODOS completados)"),
    ]
    for label, value in rows:
        line = f"  {tag}{label:<10}: {value}"
        print(f"║{line:<{w}}║")
    print(f"╚{'═' * w}╝")

    # Resumen por sector
    by_sector: dict[int, list] = {}
    for c in challenges:
        s = c.sector_id if c.sector_id is not None else (
            c.level_order // 10 if c.level_order is not None else 99
        )
        by_sector.setdefault(s, []).append(c)

    sector_names = {
        0: "Tutorial",
        1: "Fundamentos",
        2: "Flujo de Control",
        3: "Ciclos For",
        4: "Funciones",
        5: "Listas",
        6: "Dicts & Sets",
        7: "POO",
        8: "Excepciones",
        9: "Archivos & Módulos",
        99: "Sin sector",
    }

    print("\n  Progreso por sector:")
    for s in sorted(by_sector):
        chs   = by_sector[s]
        label = sector_names.get(s, f"Sector {s}")
        print(f"    S{s:02d} {label:<20} — {len(chs):3d} completados  ✓")
    print()


def _print_success(user: User, n_challenges: int, email: str, password: str) -> None:
    w = 56
    print(f"\n{'=' * w}")
    print(f"  ✅  DEMO USER CREADO EXITOSAMENTE")
    print(f"{'=' * w}")
    print(f"  Callsign : {user.callsign}")
    print(f"  Email    : {email}")
    print(f"  Password : {password}")
    print(f"  Nivel    : {user.current_level}  |  XP: {user.total_xp:,}  |  Liga: {user.league_tier}")
    print(f"  Racha    : {user.streak_days} días")
    print(f"  Progreso : {n_challenges} challenges completados (TODOS)")
    print(f"\n  PRÓXIMOS PASOS:")
    print(f"  1. Agregar a ALPHA_WHITELIST en Render: {email}")
    print(f"  2. Ir a dakiedtech.com/login")
    print(f"  3. Ingresar con las credenciales de arriba")
    print(f"  4. El usuario aterriza en /hub con todas las misiones completadas")
    print(f"{'=' * w}\n")


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Crea un usuario de demo con TODAS las misiones completadas.",
    )
    parser.add_argument(
        "--email", default=DEMO_EMAIL,
        help=f"Email del usuario demo (default: {DEMO_EMAIL})",
    )
    parser.add_argument(
        "--callsign", default=DEMO_CALLSIGN,
        help=f"Callsign del usuario demo (default: {DEMO_CALLSIGN})",
    )
    parser.add_argument(
        "--password", default=DEMO_PASSWORD,
        help=f"Contraseña del usuario demo (default: {DEMO_PASSWORD})",
    )
    parser.add_argument(
        "--reset", action="store_true", default=False,
        help="Si el usuario ya existe, lo elimina y lo recrea.",
    )
    parser.add_argument(
        "--dry-run", action="store_true", default=True,
        help="Muestra qué se haría sin tocar la BD (default: True).",
    )
    parser.add_argument(
        "--no-dry-run", dest="dry_run", action="store_false",
        help="Aplica los cambios en la BD.",
    )
    args = parser.parse_args()

    asyncio.run(run(
        email=args.email,
        callsign=args.callsign,
        password=args.password,
        reset=args.reset,
        dry_run=args.dry_run,
    ))


if __name__ == "__main__":
    main()
