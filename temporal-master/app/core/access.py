"""
access.py — Compuertas de Acceso al Nexo (D018 — Árbol de Habilidades)

Dos tipos de compuerta operan en capas:

  ┌─────────────────────────────────────────────────────────────────┐
  │  COMPUERTA FINANCIERA                                           │
  │  ¿Tiene suscripción activa o trial vigente?                     │
  │  → No  → 402 + URL de Stripe                                    │
  │  → Sí  → continúa                                              │
  ├─────────────────────────────────────────────────────────────────┤
  │  COMPUERTA TÁCTICA (Skill Tree)                                 │
  │  ¿Completó todos los prerrequisitos de esta Incursión?          │
  │  → No  → 403 + lista de incursiones faltantes (DAKI-flavored)  │
  │  → Sí  → acceso concedido                                      │
  └─────────────────────────────────────────────────────────────────┘

Funciones públicas:
  check_incursion_access(db, challenge_id, user_id)
    → Compuerta unificada D018: financiera + táctica. Usar en endpoints
      que sirven Incursiones de Códice (Sales, TPM, y futuros).

  check_freemium_access(db, challenge_id, user_id)   [LEGACY]
    → Mantiene compatibilidad con evaluate.py y otros endpoints que
      aún usan el sistema freemium original (Python Core).

  require_paid(user_id, db)
    → Dependencia FastAPI para rutas que siempre requieren suscripción
      activa independientemente del nivel (admin, certificados).
"""

import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.challenge import Challenge
from app.models.challenge_prerequisite import ChallengePrerequisite
from app.models.user import User
from app.models.user_progress import UserProgress

# ─── Respuestas de error canónicas ───────────────────────────────────────────

_PAYWALL = {
    "code": "LICENSE_REQUIRED",
    "message": (
        "Tu enlace neuronal no ha sido financiado. "
        "Adquiere una Licencia de Fundador para acceder al Nexo completo."
    ),
    "action_url": "https://pay.dakiedtech.com",
}

_TRIAL_EXPIRED = {
    "code": "TRIAL_EXPIRED",
    "message": (
        "Tu período de prueba ha expirado, Operador. "
        "El Nexo requiere una licencia activa para continuar el entrenamiento."
    ),
    "action_url": "https://pay.dakiedtech.com",
}

_PREREQUISITES_NOT_MET_TEMPLATE = {
    "code": "PREREQUISITES_NOT_MET",
    "daki_message": (
        "Sector bloqueado. El Nexo detecta entrenamiento previo incompleto. "
        "Neutraliza las incursiones faltantes antes de solicitar acceso a este sector."
    ),
    # 'missing_prerequisites' se inyecta dinámicamente por check_incursion_access
}

_ERR_INCURSION_ENCRYPTED = {
    "code": "INCURSION_ENCRYPTED",
    "message": (
        "Esta Incursión está en estado ENCRIPTADO. "
        "Acceso denegado — Desbloqueo en Fase Beta."
    ),
}


# ─── Helpers internos ────────────────────────────────────────────────────────

def _is_founder(user: User) -> bool:
    """True si el usuario tiene rol FOUNDER (God Mode — bypassa compuertas de catálogo)."""
    return getattr(user, "role", "USER") == "FOUNDER"


def _has_subscription_access(user: User) -> bool:
    """
    True si el usuario tiene acceso financiero al contenido de pago.

    Orden de evaluación:
      1. subscription_status == 'ACTIVE'  → acceso pleno, sin expiración.
      2. subscription_status == 'TRIAL'   → acceso si trial_end_date no expiró.
      3. is_licensed == True              → flag legacy (backward compat).
      4. Todo lo demás                    → sin acceso.
    """
    if user.subscription_status == "ACTIVE":
        return True

    if user.subscription_status == "TRIAL":
        if user.trial_end_date is None:
            return True  # Trial sin fecha de fin = activo indefinidamente
        return user.trial_end_date > datetime.now(timezone.utc)

    # Compatibilidad con el flag booleano previo al sistema de suscripción
    return bool(user.is_licensed)


def _is_trial_expired(user: User) -> bool:
    """True solo cuando el usuario tiene TRIAL pero la fecha de expiración pasó."""
    return (
        user.subscription_status == "TRIAL"
        and user.trial_end_date is not None
        and user.trial_end_date <= datetime.now(timezone.utc)
    )


async def _load_user(db: AsyncSession, user_id: uuid.UUID) -> User:
    """Carga el usuario o levanta 404."""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Operador no encontrado en el registro del Nexo.",
        )
    return user


async def _check_single_prerequisite(
    db: AsyncSession,
    prereq: Challenge,
    user_id: uuid.UUID,
) -> bool:
    """
    Verifica si el usuario satisface UN prerrequisito dado.

    Regla de evaluación:
      - Si prereq.is_phase_boss = True  → necesita UserProgress.boss_completed = True
        (no basta con haber llegado al boss — hay que haberlo ganado)
      - Si prereq.is_phase_boss = False → necesita UserProgress.completed = True
    """
    result = await db.execute(
        select(UserProgress).where(
            UserProgress.user_id == user_id,
            UserProgress.challenge_id == prereq.id,
        )
    )
    progress = result.scalar_one_or_none()

    if progress is None:
        return False

    if prereq.is_phase_boss:
        return progress.boss_completed

    return progress.completed


async def _get_missing_prerequisites(
    db: AsyncSession,
    challenge: Challenge,
    user_id: uuid.UUID,
) -> list[dict]:
    """
    Evalúa TODOS los prerrequisitos de una Incursión y devuelve los que faltan.

    Dos fuentes de prerrequisitos (se chequean ambas y se acumulan):
      1. challenge.prerequisite_challenge_id — FK simple (cadena lineal).
      2. challenge_prerequisites table — N:M para casos multi-prerrequisito.

    Returns:
        Lista vacía si todos los prerrequisitos están satisfechos.
        Lista de dicts con {challenge_id, title, is_phase_boss, required_status}
        para los prerrequisitos faltantes.
    """
    missing: list[dict] = []

    # ── Fuente 1: FK simple ───────────────────────────────────────────────────
    if challenge.prerequisite_challenge_id is not None:
        prereq = await db.get(Challenge, challenge.prerequisite_challenge_id)
        if prereq is not None:
            satisfied = await _check_single_prerequisite(db, prereq, user_id)
            if not satisfied:
                missing.append({
                    "challenge_id": str(prereq.id),
                    "title": prereq.title,
                    "codex_id": prereq.codex_id,
                    "is_phase_boss": prereq.is_phase_boss,
                    "required_status": "boss_completed" if prereq.is_phase_boss else "completed",
                })

    # ── Fuente 2: tabla de correlatividades múltiples ─────────────────────────
    multi_result = await db.execute(
        select(ChallengePrerequisite).where(
            ChallengePrerequisite.challenge_id == challenge.id
        )
    )
    multi_prereqs = list(multi_result.scalars().all())

    for cp in multi_prereqs:
        # Evitar duplicar si ya está en missing (podría estar en ambas fuentes)
        if any(m["challenge_id"] == str(cp.required_challenge_id) for m in missing):
            continue

        prereq = await db.get(Challenge, cp.required_challenge_id)
        if prereq is None:
            continue  # FK huérfana — ignorar silenciosamente

        satisfied = await _check_single_prerequisite(db, prereq, user_id)
        if not satisfied:
            missing.append({
                "challenge_id": str(prereq.id),
                "title": prereq.title,
                "codex_id": prereq.codex_id,
                "is_phase_boss": prereq.is_phase_boss,
                "required_status": "boss_completed" if prereq.is_phase_boss else "completed",
            })

    return missing


# ─── check_catalog_gate — Compuerta de Catálogo D022 (Niebla de Guerra) ──────

async def check_catalog_gate(
    db: AsyncSession,
    system_prompt_id: str,
    user: Optional[User],
) -> None:
    """
    Compuerta de catálogo D022: bloquea el acceso a Incursiones ENCRYPTED.

    Orden de evaluación:
      1. Busca la Incursión por system_prompt_id.
      2. Si no existe o está ACTIVE → acceso libre (pasa sin error).
      3. Si el usuario tiene role == 'FOUNDER' → bypass total (God Mode).
      4. Si está ENCRYPTED y el usuario no es FOUNDER → 403.

    Usar en context_router.resolve_stance() como primera compuerta
    de catálogo, ANTES de las compuertas financiera y táctica.
    """
    from app.models.incursion import Incursion  # importación local para evitar circulares

    result = await db.execute(
        select(Incursion).where(Incursion.system_prompt_id == system_prompt_id)
    )
    incursion = result.scalar_one_or_none()

    # Sin registro de incursión o incursión activa → pasa
    if incursion is None or incursion.status == "ACTIVE":
        return

    # God Mode — FOUNDER bypassa la compuerta de catálogo
    if user is not None and _is_founder(user):
        return

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail={**_ERR_INCURSION_ENCRYPTED, "slug": incursion.slug},
    )


# ─── check_incursion_access — Compuerta D018 (unificada) ─────────────────────

async def check_incursion_access(
    db: AsyncSession,
    challenge_id: uuid.UUID,
    user_id: Optional[uuid.UUID],
) -> Optional[User]:
    """
    Compuerta unificada D018: Financiera + Táctica (Skill Tree).

    Orden de evaluación:
      1. Carga el challenge. → 404 si no existe.
      2. Si is_free=True    → acceso libre, devuelve None sin más checks.
      3. Si user_id=None    → 402 (invitado intenta contenido de pago).
      4. Carga el usuario   → 404 si no existe.
      5. COMPUERTA FINANCIERA:
           subscription_status='ACTIVE'        → pasa
           subscription_status='TRIAL' vigente → pasa
           is_licensed=True (legacy)           → pasa
           trial expirado                      → 402 con mensaje de trial expirado
           sin acceso                          → 402 con paywall
      6. COMPUERTA TÁCTICA:
           Evalúa prerequisite_challenge_id + tabla challenge_prerequisites.
           Si algún prerrequisito falta → 403 con lista de faltantes.
      7. Todo correcto → devuelve el objeto User.

    Úsala en endpoints que sirven Incursiones de Códice (Sales, TPM, etc.)
    reemplazando la llamada a check_freemium_access + resolve_level_status.
    """
    # ── 1. Cargar challenge ───────────────────────────────────────────────────
    challenge: Optional[Challenge] = await db.get(Challenge, challenge_id)
    if challenge is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incursión no encontrada en el registro del Nexo.",
        )

    # ── 2. Niveles gratuitos — sin checks ────────────────────────────────────
    if challenge.is_free:
        return None

    # ── 3. Invitado intentando contenido de pago ─────────────────────────────
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=_PAYWALL,
        )

    # ── 4. Cargar usuario ─────────────────────────────────────────────────────
    user = await _load_user(db, user_id)

    # ── 4b. God Mode — FOUNDER bypassa compuertas financiera y táctica ────────
    if _is_founder(user):
        return user

    # ── 5. Compuerta Financiera ───────────────────────────────────────────────
    if not _has_subscription_access(user):
        # Distinguir trial expirado de "nunca tuvo acceso" para mejor UX
        detail = _TRIAL_EXPIRED if _is_trial_expired(user) else _PAYWALL
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=detail,
        )

    # ── 6. Compuerta Táctica — Árbol de Habilidades ───────────────────────────
    missing = await _get_missing_prerequisites(db, challenge, user_id)
    if missing:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                **_PREREQUISITES_NOT_MET_TEMPLATE,
                "missing_prerequisites": missing,
            },
        )

    # ── 7. Acceso concedido ───────────────────────────────────────────────────
    return user


# ─── require_paid — compuerta total (sin freemium) ───────────────────────────

async def require_paid(
    user_id: Optional[uuid.UUID] = Query(None, description="UUID del operador autenticado"),
    db: AsyncSession = Depends(get_db),
) -> Optional[User]:
    """
    Dependencia FastAPI de suscripción total — no distingue niveles gratuitos.
    Usa el nuevo _has_subscription_access (compatible con subscription_status + is_licensed).

    - user_id ausente → devuelve None (modo invitado, sin bloqueo).
    - sin acceso      → 402 Payment Required.
    - con acceso      → devuelve el objeto User.
    """
    if user_id is None:
        return None

    user = await _load_user(db, user_id)

    if not _has_subscription_access(user):
        detail = _TRIAL_EXPIRED if _is_trial_expired(user) else _PAYWALL
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=detail,
        )

    return user


# ─── check_freemium_access — LEGACY (mantiene compatibilidad) ────────────────

async def check_freemium_access(
    db: AsyncSession,
    challenge_id: uuid.UUID,
    user_id: Optional[uuid.UUID],
) -> Optional[User]:
    """
    Compuerta freemium original. Mantiene compatibilidad con evaluate.py
    y otros endpoints del Python Core que aún no usan el Skill Tree D018.

    Para nuevos endpoints de Códice, usar check_incursion_access en su lugar.

    Reglas (sin cambios respecto a la versión pre-D018):
      1. is_free=True  → acceso libre.
      2. is_free=False → requiere suscripción activa (ahora via _has_subscription_access).
    """
    challenge: Optional[Challenge] = await db.get(Challenge, challenge_id)
    if challenge is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Misión no encontrada.",
        )

    if challenge.is_free:
        return None

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=_PAYWALL,
        )

    user = await _load_user(db, user_id)

    if not _has_subscription_access(user):
        detail = _TRIAL_EXPIRED if _is_trial_expired(user) else _PAYWALL
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=detail,
        )

    return user
