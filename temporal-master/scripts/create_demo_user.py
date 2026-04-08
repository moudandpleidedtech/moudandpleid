"""
scripts/create_demo_user.py — Usuario de demostración DAKI EdTech

Crea (o resetea) una cuenta de demo con progreso pre-cargado, lista para
presentar a clientes técnicos. El usuario llega al Nexo en un estado
intermedio realista: ha completado el bloque de fundamentos y está
explorando lógica de control — exactamente el punto donde DAKI se vuelve
más visible e impresionante.

PERFIL DEL USUARIO DEMO
──────────────────────
  Callsign  : DEMO_OPERATOR
  Email     : demo@dakiedtech.com       ← agregar a ALPHA_WHITELIST si está activa
  Password  : DemoDaki2025!
  Nivel     : 28 (en el tramo final del Sector 2 — Flujo de Control)
  XP        : 4.850
  Racha     : 7 días
  Liga      : Plata
  Suscripción: ACTIVE (acceso completo)

PROGRESO PRE-CARGADO (27 challenges completados)
─────────────────────────────────────────────────
  Sector 0  Tutorial         — 1 completado
  Sector 1  Fundamentos      — 10 completados (L1-L10, incluyendo boss)
  Sector 2  Flujo de Control — 10 completados (L11-L20, incluyendo boss)
  Sector 3  Ciclos For       — 6 completados  (L21-L26, en curso)

  El demo está parado en L27 "Suma de Pares" — un nivel de ciclos
  intermedio, bueno para mostrar el IDE en acción.

USO
───
  # Crear (dry-run por defecto — solo muestra qué haría):
  python -m scripts.create_demo_user

  # Crear en la BD:
  python -m scripts.create_demo_user --no-dry-run

  # Resetear un demo existente (si ya existe, lo borra y recrea):
  python -m scripts.create_demo_user --no-dry-run --reset

  # Email personalizado (para una empresa específica):
  python -m scripts.create_demo_user --no-dry-run --email demo@cliente.com --callsign DEV_LEAD

DESPUÉS DE EJECUTAR
───────────────────
  1. Agregar el email a ALPHA_WHITELIST en Render (si está activa)
  2. Ir a dakiedtech.com/login
  3. Ingresar con las credenciales del script
  4. El usuario ya tiene progreso — no hay onboarding ni pantalla de carga lenta
"""

import argparse
import asyncio
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import delete, select

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

DEMO_LEVEL    = 28
DEMO_XP       = 4_850
DEMO_STREAK   = 7
DEMO_LEAGUE   = "Plata"

# Rangos de level_order completados
# El demo llega hasta L26 completado — L27 está abierto para mostrar en vivo
COMPLETED_LEVEL_ORDERS = list(range(0, 27))   # L0 a L26 inclusive (27 niveles)


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

        # ── Cargar challenges para armar el progreso ───────────────────────────
        ch_result = await session.execute(
            select(Challenge)
            .where(Challenge.level_order.in_(COMPLETED_LEVEL_ORDERS))
            .order_by(Challenge.level_order)
        )
        challenges = ch_result.scalars().all()

        found_orders = {c.level_order for c in challenges}
        missing = [lo for lo in COMPLETED_LEVEL_ORDERS if lo not in found_orders]
        if missing:
            print(f"⚠  {len(missing)} levels no encontrados en BD: {missing[:5]}{'...' if len(missing) > 5 else ''}")
            print("   El progreso se creará solo para los levels existentes.")
            challenges = [c for c in challenges if c.level_order not in missing]

        # ── Preview ───────────────────────────────────────────────────────────
        _print_preview(email, callsign, challenges, dry_run)

        if dry_run:
            print("\n[DRY RUN] Sin cambios. Pasá --no-dry-run para aplicar.\n")
            return

        # ── Crear usuario ──────────────────────────────────────────────────────
        now = datetime.now(timezone.utc)
        user = User(
            email=email,
            callsign=callsign,
            password_hash=hash_password(password),
            current_level=DEMO_LEVEL,
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

        # ── Crear progreso y métricas ──────────────────────────────────────────
        for i, challenge in enumerate(challenges):
            is_boss = (challenge.challenge_type == "boss") if challenge.challenge_type else False

            # Variación realista: los primeros niveles más rápido, los últimos con más intentos
            attempts = max(1, 1 + (i % 3))         # 1, 2, 3, 1, 2, 3...
            hints    = max(0, (i % 4) - 1)          # 0, 0, 1, 2, 0, 0, 1, 2...
            time_ms  = (90 + i * 15) * 1_000        # 90s a ~495s, crece con el nivel

            completed_at = now - timedelta(days=(len(challenges) - i) * 0.8)

            session.add(UserProgress(
                user_id=user.id,
                challenge_id=challenge.id,
                completed=True,
                boss_completed=is_boss,
                attempts=attempts,
                hints_used=hints,
                completed_at=completed_at,
                codex_id=challenge.codex_id if hasattr(challenge, "codex_id") else "python_core",
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

        _print_success(user, len(challenges), email, password)


def _print_preview(email: str, callsign: str, challenges: list, dry_run: bool) -> None:
    tag = "[DRY RUN] " if dry_run else ""
    print()
    print(f"╔══════════════════════════════════════════════════════╗")
    print(f"║       DAKI EDTECH — USUARIO DE DEMOSTRACIÓN          ║")
    print(f"╠══════════════════════════════════════════════════════╣")
    print(f"║  {tag}Callsign  : {callsign:<40}║"[:57] + "║")
    print(f"║  {tag}Email     : {email:<40}║"[:57] + "║")
    print(f"║  {tag}Password  : {DEMO_PASSWORD:<40}║"[:57] + "║")
    print(f"║  {tag}Nivel     : {DEMO_LEVEL:<40}║"[:57] + "║")
    print(f"║  {tag}XP        : {DEMO_XP:<40}║"[:57] + "║")
    print(f"║  {tag}Racha     : {DEMO_STREAK} días{'':<35}║"[:57] + "║")
    print(f"║  {tag}Liga      : {DEMO_LEAGUE:<40}║"[:57] + "║")
    print(f"║  {tag}Progreso  : {len(challenges)} challenges completados{'':<20}║"[:57] + "║")
    print(f"╚══════════════════════════════════════════════════════╝")

    sector_map = {0: "Tutorial", 1: "Fundamentos", 2: "Flujo", 3: "Ciclos For"}
    by_sector: dict[int, list] = {}
    for c in challenges:
        s = c.sector_id if c.sector_id is not None else (c.level_order // 10 if c.level_order else 0)
        by_sector.setdefault(s, []).append(c)

    print("\n  Progreso por sector:")
    for s in sorted(by_sector):
        chs = by_sector[s]
        label = sector_map.get(s, f"Sector {s}")
        titles = ", ".join(c.title[:20] for c in chs[:3])
        dots = "..." if len(chs) > 3 else ""
        print(f"    S{s:02d} {label:<18} — {len(chs):2d} completados  ({titles}{dots})")
    print()


def _print_success(user: User, n_challenges: int, email: str, password: str) -> None:
    print(f"\n{'='*56}")
    print(f"  ✅  DEMO USER CREADO EXITOSAMENTE")
    print(f"{'='*56}")
    print(f"  Callsign : {user.callsign}")
    print(f"  Email    : {email}")
    print(f"  Password : {password}")
    print(f"  Nivel    : {user.current_level}  |  XP: {user.total_xp:,}  |  Liga: {user.league_tier}")
    print(f"  Progress : {n_challenges} challenges completados (L0–L{COMPLETED_LEVEL_ORDERS[-1]})")
    print(f"\n  PRÓXIMOS PASOS:")
    print(f"  1. Agregar a ALPHA_WHITELIST en Render: {email}")
    print(f"  2. Ir a dakiedtech.com/login")
    print(f"  3. Ingresar con las credenciales de arriba")
    print(f"  4. El usuario aterriza directo en /hub con progreso visible")
    print(f"{'='*56}\n")


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Crea un usuario de demo con progreso pre-cargado para presentaciones.",
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
