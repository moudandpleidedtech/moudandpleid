"""
context_router.py — Enrutador de Contexto Dinámico (D020 — AI Stance Switcher)

Implementa el patrón Factory para seleccionar la "postura" de IA correcta
(System Prompt + modelo + límite de tokens) según el contexto de la Incursión activa.

Flujo de uso en el endpoint:
  1. El endpoint recibe incursion_id (alias o codex_id canónico) + challenge_id (UUID opcional).
  2. resolve_stance() hace el gate de seguridad y retorna un ContextStance listo.
  3. El endpoint llama al modelo con stance.system_prompt, stance.max_tokens, stance.model.

Aliases canónicos de incursion_id:
  "python"   → codex_id = None ("python_core", challenges sin codex_id en BD)
  "sales"    → codex_id = "sales_mastery_v1"
  "tpm"      → codex_id = "tpm_mastery_v1"
  "cybersec" → codex_id = "cybersecurity_v1"  (futuro — prompt placeholder activo)

Gate de acceso (ejecutado ANTES de cualquier llamada al modelo):
  ┌─────────────────────────────────────────────────────────────────┐
  │  Si challenge_id fue provisto (UUID):                           │
  │    → check_incursion_access(db, challenge_id, user_id)          │
  │      (compuerta financiera + táctica completa)                  │
  ├─────────────────────────────────────────────────────────────────┤
  │  Si solo incursion_id (alias sin challenge_id):                 │
  │    → "python": acceso libre (tier gratuito)                     │
  │    → cualquier otro: requiere user autenticado + suscripción    │
  └─────────────────────────────────────────────────────────────────┘

Funciones públicas:
  resolve_stance(db, incursion_id, user, challenge_id, **tpm_kwargs)
    → ContextStance — listo para inyectar en la llamada al modelo.
    → Lanza HTTPException 401/402/403/404 si el acceso es denegado.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.access import _has_subscription_access, _is_trial_expired, check_catalog_gate, check_incursion_access
from app.models.user import User
from app.services.daki_persona import DAKI_SYSTEM_PROMPT
from app.services.sales_codex_persona import SALES_CODEX_SYSTEM_PROMPT
from app.services.tpm_codex_persona import get_tpm_character_prompt

# ─── Constantes ──────────────────────────────────────────────────────────────

# Aliases de entrada → codex_id canónico en la BD (None = python_core legacy)
_ALIAS_TO_CODEX: dict[str, str | None] = {
    "python":        None,
    "python_core":   None,
    "sales":         "sales_mastery_v1",
    "sales_mastery": "sales_mastery_v1",
    "tpm":           "tpm_mastery_v1",
    "tpm_mastery":   "tpm_mastery_v1",
    "cybersec":      "cybersecurity_v1",
    "cybersecurity": "cybersecurity_v1",
}

# Codexes que requieren suscripción activa (compuerta financiera)
_PAID_CODEXES: frozenset[str | None] = frozenset({
    "sales_mastery_v1",
    "tpm_mastery_v1",
    "cybersecurity_v1",
})

# ─── System Prompt — Red Team Instructor (cybersec, placeholder) ─────────────

_CYBERSEC_INSTRUCTOR_PROMPT = """\
# INSTRUCTOR RED TEAM — PROTOCOLO ARES · DAKI EdTech

## IDENTIDAD OPERACIONAL

Eres DAKI en modo Red Team: instructor de seguridad ofensiva de élite dentro de
un laboratorio de entrenamiento certificado (CTF / pentest autorizado).
Tu rol: forjar operadores que piensan como atacantes para construir defensas reales.

## VOZ Y TONO

- Precisión técnica quirúrgica. Sin relleno, sin eufemismos.
- Vocabulario operacional: vectores, superficie de ataque, kill-chain, C2, persistence, pivoting.
- Tono: instructor de CERT / red team lead. Exigente, no hostil.
- No ofreces código de exploit copiable. Guías al Operador a comprender la mecánica del ataque.

## PROTOCOLO DE ENSEÑANZA

Para cada técnica o vulnerabilidad:
  1. CONTEXTO TÁCTICO   — ¿En qué fase del kill-chain opera? ¿Qué condiciones la habilitan?
  2. MECÁNICA INTERNA   — ¿Por qué funciona? ¿Qué asume del objetivo?
  3. CONTRAMEDIDA BLUE  — ¿Cómo la detectaría un SOC? ¿Qué log generaría?

El Operador aprende atacando en laboratorio; la defensa emerge del entendimiento del ataque.

## LÍMITES ABSOLUTOS

- No generar payloads funcionales, shellcode ni exploits listos para usar fuera del lab.
- Si el Operador menciona un objetivo que no sea su propio laboratorio o entorno CTF
  sancionado: detener la sesión e instruirle a obtener autorización escrita.
- Toda técnica se enseña en el contexto "¿cómo lo detectarías?" — siempre doble cara.
"""

# ─── Stance — postura de IA resuelta ─────────────────────────────────────────

@dataclass
class ContextStance:
    """
    Postura de IA completamente resuelta y lista para ser usada en un API call.

    Todos los campos son inmutables una vez construidos.
    El caller solo necesita usar system_prompt + max_tokens + model.
    """
    persona_key:   str             # alias normalizado: "python"|"sales"|"tpm"|"cybersec"
    codex_id:      str | None      # codex canónico en BD (None = python_core)
    system_prompt: str             # prompt listo para inyectar como `system=`
    max_tokens:    int             # límite de tokens apropiado para el contexto
    model:         str             # modelo Claude a usar
    persona_label: str             # nombre legible para logs/debug
    access_verified: bool = field(default=False, repr=False)


# ─── Constructores de posturas (privados) ────────────────────────────────────

def _python_stance(user: Optional[User]) -> ContextStance:
    """
    Mentor técnico de Python Core.
    Reutiliza DAKI_SYSTEM_PROMPT (núcleo cognitivo canónico de daki_persona.py).
    Si el usuario tiene callsign conocido, se inyecta en el prompt.
    """
    if user is not None:
        callsign_line = (
            f"\n\n[CONTEXTO DE OPERADOR]\n"
            f"Estás hablando con {user.callsign}, Nivel {user.current_level}. "
            f"Personaliza ocasionalmente con su callsign. No en cada mensaje."
        )
        prompt = DAKI_SYSTEM_PROMPT + callsign_line
    else:
        prompt = DAKI_SYSTEM_PROMPT

    return ContextStance(
        persona_key="python",
        codex_id=None,
        system_prompt=prompt,
        max_tokens=300,
        model="claude-haiku-4-5-20251001",
        persona_label="DAKI — Mentora Python Core",
        access_verified=True,
    )


def _sales_stance(user: Optional[User]) -> ContextStance:
    """Instructora de Technical Sales Mastery."""
    return ContextStance(
        persona_key="sales",
        codex_id="sales_mastery_v1",
        system_prompt=SALES_CODEX_SYSTEM_PROMPT,
        max_tokens=500,
        model="claude-haiku-4-5-20251001",
        persona_label="DAKI — Instructora Technical Sales",
        access_verified=True,
    )


def _tpm_stance(
    user: Optional[User],
    character: str = "mentor_tecnico",
    crisis_context: str = "",
    level_id: int = 1,
    current_act: int = 1,
) -> ContextStance:
    """
    Personaje TPM dinámico — delega en get_tpm_character_prompt() de tpm_codex_persona.
    El caller puede especificar el personaje activo y el acto de la crisis.
    """
    system_prompt = get_tpm_character_prompt(
        character=character,
        level_id=level_id,
        crisis_context=crisis_context,
        current_act=current_act,
    )
    label_map = {
        "mentor_tecnico":    "Marcos — Mentor Técnico Senior",
        "dev_frustrado":     "Sofía — Dev Frustrada",
        "ceo_hallway":       "Rodrigo — CEO Hallway",
        "cliente_exigente":  "Andrés — Cliente Exigente",
    }
    return ContextStance(
        persona_key="tpm",
        codex_id="tpm_mastery_v1",
        system_prompt=system_prompt,
        max_tokens=600,
        model="claude-haiku-4-5-20251001",
        persona_label=f"TPM — {label_map.get(character, character)}",
        access_verified=True,
    )


def _cybersec_stance(user: Optional[User]) -> ContextStance:
    """Instructor Red Team — Protocolo ARES."""
    return ContextStance(
        persona_key="cybersec",
        codex_id="cybersecurity_v1",
        system_prompt=_CYBERSEC_INSTRUCTOR_PROMPT,
        max_tokens=450,
        model="claude-haiku-4-5-20251001",
        persona_label="DAKI — Instructor Red Team (ARES)",
        access_verified=True,
    )


# ─── Fábrica de builders ──────────────────────────────────────────────────────

# Mapea persona_key → función constructora.
# Los builders de TPM necesan kwargs extra — se manejan por separado en resolve_stance.
_STANCE_FACTORY: dict[str, object] = {
    "python":   _python_stance,
    "sales":    _sales_stance,
    "cybersec": _cybersec_stance,
}

# ─── Respuestas de error canónicas ───────────────────────────────────────────

_ERR_UNKNOWN_CONTEXT = {
    "code": "UNKNOWN_INCURSION_CONTEXT",
    "message": "Contexto de incursión no reconocido. Valores válidos: python, sales, tpm, cybersec.",
}

_ERR_AUTH_REQUIRED = {
    "code": "AUTH_REQUIRED",
    "message": (
        "Este Códice requiere autenticación, Operador. "
        "Identifícate en el Nexo antes de solicitar acceso a contenido de élite."
    ),
}

_ERR_SUBSCRIPTION_REQUIRED = {
    "code": "LICENSE_REQUIRED",
    "message": (
        "Tu enlace neuronal no ha sido financiado. "
        "Adquiere una Licencia de Fundador para acceder a los Códices de Élite."
    ),
    "action_url": "https://pay.dakiedtech.com",
}

_ERR_TRIAL_EXPIRED = {
    "code": "TRIAL_EXPIRED",
    "message": (
        "Tu período de prueba ha expirado, Operador. "
        "El Nexo requiere una licencia activa para los Códices de Élite."
    ),
    "action_url": "https://pay.dakiedtech.com",
}

# ─── Gate de acceso (sin challenge_id) ───────────────────────────────────────

def _check_subscription_gate(codex_id: str | None, user: Optional[User]) -> None:
    """
    Compuerta financiera ligera para cuando no se provee challenge_id.

    Reglas:
      - codex_id = None ("python_core"): acceso libre, no lanza.
      - codex_id en _PAID_CODEXES: requiere user autenticado + suscripción activa.
    """
    if codex_id not in _PAID_CODEXES:
        return  # python_core o desconocido → dejar pasar

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=_ERR_AUTH_REQUIRED,
        )

    if not _has_subscription_access(user):
        detail = _ERR_TRIAL_EXPIRED if _is_trial_expired(user) else _ERR_SUBSCRIPTION_REQUIRED
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=detail,
        )


# ─── resolve_stance — entrada pública principal ───────────────────────────────

async def resolve_stance(
    db: AsyncSession,
    incursion_id: str,
    user: Optional[User],
    challenge_id: Optional[uuid.UUID] = None,
    # Parámetros específicos del Códice TPM
    tpm_character: str = "mentor_tecnico",
    tpm_crisis_context: str = "",
    tpm_level_id: int = 1,
    tpm_current_act: int = 1,
) -> ContextStance:
    """
    Resuelve el alias de incursion_id, verifica acceso y retorna un ContextStance listo.

    Args:
        db:                 Sesión async de SQLAlchemy.
        incursion_id:       Alias de contexto ("python"|"sales"|"tpm"|"cybersec")
                            o codex_id canónico ("sales_mastery_v1", etc.).
        user:               Usuario autenticado (None si es invitado).
        challenge_id:       UUID del challenge específico (opcional).
                            Si se provee, ejecuta check_incursion_access completo.
                            Si no, solo verifica suscripción para codexes de pago.
        tpm_character:      Personaje activo del Códice TPM (solo relevante si incursion_id=="tpm").
        tpm_crisis_context: Descripción de la crisis activa para el personaje TPM.
        tpm_level_id:       Número de nivel activo en el Desafío 00 (1-30).
        tpm_current_act:    Acto del personaje (para transiciones como Sofía en L14).

    Returns:
        ContextStance con system_prompt, max_tokens y model listos.

    Raises:
        HTTPException 400 — incursion_id no reconocido.
        HTTPException 401 — usuario no autenticado y codex requiere auth.
        HTTPException 402 — sin suscripción o trial expirado.
        HTTPException 403 — prerrequisitos no satisfechos (solo cuando challenge_id provisto).
        HTTPException 404 — challenge_id no existe en la BD.
    """
    # ── 1. Normalizar alias → codex_id ───────────────────────────────────────
    key = incursion_id.strip().lower()
    if key not in _ALIAS_TO_CODEX:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=_ERR_UNKNOWN_CONTEXT,
        )
    codex_id = _ALIAS_TO_CODEX[key]
    # Normalizar key al alias corto canónico
    persona_key = next(
        k for k, v in _ALIAS_TO_CODEX.items()
        if v == codex_id and len(k) <= 8  # prefer short alias
    )

    # ── 1b. Compuerta de catálogo (D022 — Niebla de Guerra) ──────────────────
    # Bloquea acceso a Incursiones ENCRYPTED para no-FOUNDER, ANTES de gastar tokens.
    # python_core (key=="python") no tiene entrada de catálogo → pasa sin error.
    if persona_key != "python":
        await check_catalog_gate(db, persona_key, user)

    # ── 2. Gate de acceso ─────────────────────────────────────────────────────
    if challenge_id is not None:
        # Compuerta completa: financiera + táctica (check_incursion_access lanza en caso de fallo)
        user_id = user.id if user is not None else None
        await check_incursion_access(db, challenge_id, user_id)
    else:
        # Sin challenge_id: solo compuerta financiera ligera
        _check_subscription_gate(codex_id, user)

    # ── 3. Construir postura ──────────────────────────────────────────────────
    if persona_key == "tpm":
        return _tpm_stance(
            user=user,
            character=tpm_character,
            crisis_context=tpm_crisis_context,
            level_id=tpm_level_id,
            current_act=tpm_current_act,
        )

    builder = _STANCE_FACTORY.get(persona_key)
    if builder is None:
        # No debería ocurrir dado el check de _ALIAS_TO_CODEX, pero defensive
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=_ERR_UNKNOWN_CONTEXT,
        )
    return builder(user)  # type: ignore[call-arg]
