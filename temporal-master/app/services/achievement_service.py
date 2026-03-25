"""
achievement_service.py — Sistema de Logros DAKI

25 logros ocultos que se desbloquean en eventos clave del aprendizaje.
Cada logro se registra una sola vez por usuario (idempotente).

Triggers:
  "level_complete"      — llamado desde /execute cuando output_matched=True
  "contract_validated"  — llamado desde /contracts/review cuando aprobado
  "login"               — llamado al hacer login (para rachas)

Context keys (según trigger):
  level_complete:
    hints_used       int   pistas usadas en el nivel actual
    attempts         int   intentos en este nivel
    execution_time_ms float tiempo de ejecución del último intento
    user_level       int   nivel actual del usuario DESPUÉS de la subida
    user_streak      int   racha de días actual
    total_completed  int   total de niveles completados por el usuario
    already_completed bool  si el nivel ya estaba completo antes de este intento
    level_order      int   order del nivel (1-100)

  contract_validated:
    level_order      int   50 | 60 | 70
    total_contracts  int   total de contratos validados por el usuario

  login:
    user_streak      int   racha actual (ya actualizada)
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.achievement import UserAchievement
from app.models.user_progress import UserProgress

# ─── Catálogo de Logros ───────────────────────────────────────────────────────

ACHIEVEMENTS: dict[str, dict] = {
    # ── Primera vez ──────────────────────────────────────────────────────────
    "primer_pulso": {
        "name": "Primer Pulso",
        "description": "Ejecutaste tu primer código en el Nexo.",
        "icon": "⚡",
        "xp_bonus": 50,
        "rarity": "common",
    },
    # ── Autonomía ────────────────────────────────────────────────────────────
    "autonomo": {
        "name": "Operador Autónomo",
        "description": "Completaste un nivel sin usar ninguna pista de DAKI.",
        "icon": "🎯",
        "xp_bonus": 100,
        "rarity": "uncommon",
    },
    "cinco_sin_pistas": {
        "name": "Mente Independiente",
        "description": "5 niveles completados sin pistas.",
        "icon": "🧠",
        "xp_bonus": 200,
        "rarity": "uncommon",
    },
    "diez_sin_pistas": {
        "name": "Modo Silencio",
        "description": "10 niveles completados sin pistas de DAKI.",
        "icon": "🔇",
        "xp_bonus": 400,
        "rarity": "rare",
    },
    # ── Velocidad ────────────────────────────────────────────────────────────
    "velocista": {
        "name": "Protocolo Rápido",
        "description": "Resolviste un nivel en menos de 90 segundos.",
        "icon": "⚡",
        "xp_bonus": 150,
        "rarity": "uncommon",
    },
    "relampago": {
        "name": "Relámpago del Nexo",
        "description": "Resolviste un nivel en menos de 30 segundos.",
        "icon": "🌩️",
        "xp_bonus": 300,
        "rarity": "rare",
    },
    # ── Persistencia ─────────────────────────────────────────────────────────
    "obstinado": {
        "name": "Sin Rendición",
        "description": "Resolviste un nivel después de 10 o más intentos fallidos.",
        "icon": "💪",
        "xp_bonus": 250,
        "rarity": "uncommon",
    },
    "perfeccionista": {
        "name": "Primer Intento",
        "description": "Resolviste un nivel a la primera.",
        "icon": "🏆",
        "xp_bonus": 200,
        "rarity": "rare",
    },
    # ── Hitos de nivel ───────────────────────────────────────────────────────
    "nivel_10": {
        "name": "Agente Confirmado",
        "description": "Alcanzaste el Nivel 10.",
        "icon": "🔟",
        "xp_bonus": 500,
        "rarity": "uncommon",
    },
    "nivel_25": {
        "name": "Operador de Campo",
        "description": "Alcanzaste el Nivel 25.",
        "icon": "🎖️",
        "xp_bonus": 1000,
        "rarity": "rare",
    },
    "nivel_50": {
        "name": "Comandante del Nexo",
        "description": "Alcanzaste el Nivel 50. Eres élite.",
        "icon": "⭐",
        "xp_bonus": 2500,
        "rarity": "epic",
    },
    "nivel_75": {
        "name": "Arquitecto del Código",
        "description": "Alcanzaste el Nivel 75.",
        "icon": "🏗️",
        "xp_bonus": 5000,
        "rarity": "epic",
    },
    # ── Progreso global ───────────────────────────────────────────────────────
    "diez_completados": {
        "name": "Cadencia de Fuego",
        "description": "10 niveles completados.",
        "icon": "🔥",
        "xp_bonus": 300,
        "rarity": "common",
    },
    "cincuenta_completados": {
        "name": "Veterano del Nexo",
        "description": "50 niveles completados.",
        "icon": "🎗️",
        "xp_bonus": 1500,
        "rarity": "rare",
    },
    # ── Rachas ───────────────────────────────────────────────────────────────
    "racha_3": {
        "name": "Compromiso Iniciado",
        "description": "3 días consecutivos activo en el Nexo.",
        "icon": "📅",
        "xp_bonus": 150,
        "rarity": "common",
    },
    "racha_7": {
        "name": "Semana de Combate",
        "description": "7 días consecutivos activo en el Nexo.",
        "icon": "🗓️",
        "xp_bonus": 500,
        "rarity": "uncommon",
    },
    "racha_30": {
        "name": "Protocolo Permanente",
        "description": "30 días consecutivos. Eres parte del Nexo.",
        "icon": "🌙",
        "xp_bonus": 3000,
        "rarity": "legendary",
    },
    # ── Contratos ────────────────────────────────────────────────────────────
    "primer_contrato": {
        "name": "Primer Despliegue",
        "description": "Tu primer contrato validado por DAKI.",
        "icon": "📋",
        "xp_bonus": 500,
        "rarity": "uncommon",
    },
    "comandante": {
        "name": "Comandante Certificado",
        "description": "Los 3 contratos de certificación completados.",
        "icon": "🎓",
        "xp_bonus": 2000,
        "rarity": "epic",
    },
    # ── Secretos ─────────────────────────────────────────────────────────────
    "codigo_limpio": {
        "name": "Código Limpio",
        "description": "Resolviste 3 niveles seguidos sin errores de sintaxis.",
        "icon": "✨",
        "xp_bonus": 300,
        "rarity": "rare",
    },
    "madrugador": {
        "name": "Turno de Medianoche",
        "description": "Completaste un nivel entre las 00:00 y las 05:00.",
        "icon": "🌑",
        "xp_bonus": 100,
        "rarity": "uncommon",
    },
    "explorador": {
        "name": "Explorador del Nexo",
        "description": "Completaste niveles de 3 sectores diferentes.",
        "icon": "🗺️",
        "xp_bonus": 400,
        "rarity": "uncommon",
    },
}

# ─── Insights por concepto ────────────────────────────────────────────────────
# Una frase que conecta el concepto recién aprendido con el mundo real.

CONCEPT_INSIGHTS: dict[str, str] = {
    "variables":          "En el mundo real, cada variable es una casilla en la RAM de tu computadora — así funciona cada app que usás.",
    "tipos de datos":     "Los tipos de datos evitan que los sistemas bancarios confundan un monto con un nombre.",
    "operadores":         "Los operadores aritméticos que usaste son la base de los motores de pricing de Amazon.",
    "condicionales":      "Cada if/else que escribiste es la misma lógica que usa Spotify para decidir qué canción reproducir.",
    "bucles":             "Los bucles son el corazón de todo: desde el feed infinito de Instagram hasta los algoritmos de minería de Bitcoin.",
    "funciones":          "Las funciones que creaste son exactamente cómo Netflix organiza millones de líneas de código en piezas manejables.",
    "listas":             "Las listas que usaste son la estructura detrás de los resultados de Google — ordenadas, indexadas, buscables.",
    "diccionarios":       "Los diccionarios son la base de JSON, el formato que mueve el 90% de las APIs del mundo.",
    "strings":            "La manipulación de strings que practicaste es la base del procesamiento de lenguaje natural en ChatGPT.",
    "input/output":       "El I/O que codificaste es la misma interfaz que conecta tu teclado con el sistema operativo.",
    "clases":             "Las clases que aprendiste son los bloques con los que se construyen frameworks como Django y Flask.",
    "herencia":           "La herencia de clases permite que el código de iOS y Android compartan lógica base sin repetirse.",
    "excepciones":        "El manejo de excepciones que implementaste es lo que evita que una app de pagos colapse con un error de red.",
    "archivos":           "Las operaciones con archivos son la base de los sistemas de logging que monitorean millones de servidores.",
    "recursión":          "La recursión que aplicaste es la base de los algoritmos de búsqueda en árboles que usa Git internamente.",
    "comprensión de listas": "Las list comprehensions reducen el código que procesa datasets de millones de registros en una sola línea.",
    "generadores":        "Los generadores que usaste son cómo Python maneja streams de datos gigantes sin consumir toda la memoria.",
    "decoradores":        "Los decoradores son exactamente cómo FastAPI y Flask registran rutas de API con una sola línea.",
    "módulos":            "Los módulos que importaste son el sistema que permite que proyectos con cientos de archivos se mantengan organizados.",
    "sets":               "Los sets son la estructura detrás de los sistemas de deduplicación de logs en plataformas como Cloudflare.",
    "tuplas":             "Las tuplas inmutables son clave en bases de datos: garantizan que ciertos datos no puedan corromperse.",
    "while":              "Los bucles while controlan los sistemas de retry de conexión en cada cliente HTTP del mundo.",
    "range":              "range() es la base de las paginaciones de API que sirven millones de resultados por segundo.",
    "format":             "El formateo de strings que practicaste es cómo se construyen los mensajes de error y logs en producción.",
    "casting":            "El casting de tipos evita los bugs más costosos en fintech — donde confundir int y float puede costar miles de dólares.",
}

_DEFAULT_INSIGHT = "En el mundo real, cada línea de código que escribiste hoy es parte del lenguaje que construyó la economía digital."


def get_insight_for_concepts(concepts: list[str]) -> str:
    """Retorna el insight más relevante para los conceptos enseñados en el nivel."""
    for concept in concepts:
        for key, insight in CONCEPT_INSIGHTS.items():
            if key.lower() in concept.lower() or concept.lower() in key.lower():
                return insight
    return _DEFAULT_INSIGHT


# ─── Check & Grant ────────────────────────────────────────────────────────────

async def check_and_grant(
    db: AsyncSession,
    user_id: uuid.UUID,
    trigger: str,
    context: dict,
) -> list[dict]:
    """
    Evalúa qué logros nuevos merece el usuario y los registra.
    Retorna solo los logros RECIÉN desbloqueados (no los ya existentes).
    Idempotente: si el logro ya existe, no hace nada.
    """
    # 1. Logros ya desbloqueados
    existing_result = await db.execute(
        select(UserAchievement.achievement_id).where(UserAchievement.user_id == user_id)
    )
    already_unlocked: set[str] = {row[0] for row in existing_result.all()}

    candidates: list[str] = []

    if trigger == "level_complete":
        already_completed: bool = context.get("already_completed", False)
        hints_used:        int  = context.get("hints_used", 0)
        attempts:          int  = context.get("attempts", 1)
        exec_ms:           float = context.get("execution_time_ms", 9999.0)
        user_level:        int  = context.get("user_level", 1)
        user_streak:       int  = context.get("user_streak", 0)
        total_completed:   int  = context.get("total_completed", 0)
        level_order:       int  = context.get("level_order", 0)

        # Solo otorgar logros en primera compleción para la mayoría
        if not already_completed:
            candidates.append("primer_pulso")

            if hints_used == 0:
                candidates.append("autonomo")

            if attempts == 1:
                candidates.append("perfeccionista")

            if attempts >= 10:
                candidates.append("obstinado")

            if exec_ms < 30_000:
                candidates.append("relampago")
            elif exec_ms < 90_000:
                candidates.append("velocista")

            # Total completados milestones
            if total_completed >= 10:
                candidates.append("diez_completados")
            if total_completed >= 50:
                candidates.append("cincuenta_completados")

            # Hora del día (medianoche)
            now_hour = datetime.now(timezone.utc).hour
            if now_hour < 5:
                candidates.append("madrugador")

            # Sin pistas acumuladas (necesita query adicional)
            if hints_used == 0:
                no_hint_count = await _count_no_hint_completions(db, user_id)
                if no_hint_count >= 10:
                    candidates.append("diez_sin_pistas")
                elif no_hint_count >= 5:
                    candidates.append("cinco_sin_pistas")

            # Sectores distintos completados
            distinct_sectors = await _count_distinct_sectors(db, user_id)
            if distinct_sectors >= 3:
                candidates.append("explorador")

        # Hitos de nivel (pueden otorgarse en rein tento también)
        if user_level >= 10:
            candidates.append("nivel_10")
        if user_level >= 25:
            candidates.append("nivel_25")
        if user_level >= 50:
            candidates.append("nivel_50")
        if user_level >= 75:
            candidates.append("nivel_75")

        # Rachas
        if user_streak >= 3:
            candidates.append("racha_3")
        if user_streak >= 7:
            candidates.append("racha_7")
        if user_streak >= 30:
            candidates.append("racha_30")

    elif trigger == "contract_validated":
        total_contracts: int = context.get("total_contracts", 0)
        candidates.append("primer_contrato")
        if total_contracts >= 3:
            candidates.append("comandante")

    elif trigger == "login":
        user_streak = context.get("user_streak", 0)
        if user_streak >= 3:
            candidates.append("racha_3")
        if user_streak >= 7:
            candidates.append("racha_7")
        if user_streak >= 30:
            candidates.append("racha_30")

    # 2. Filtrar los que ya están desbloqueados y los que no existen en el catálogo
    new_ids = [aid for aid in candidates if aid not in already_unlocked and aid in ACHIEVEMENTS]

    if not new_ids:
        return []

    # 3. Insertar en BD
    now = datetime.now(timezone.utc)
    for achievement_id in new_ids:
        db.add(UserAchievement(
            user_id=user_id,
            achievement_id=achievement_id,
            unlocked_at=now,
        ))
    await db.flush()

    # 4. Retornar datos enriquecidos para el frontend
    return [
        {**ACHIEVEMENTS[aid], "id": aid, "unlocked_at": now.isoformat()}
        for aid in new_ids
    ]


# ─── Helpers de consulta ──────────────────────────────────────────────────────

async def _count_no_hint_completions(db: AsyncSession, user_id: uuid.UUID) -> int:
    """Cuenta niveles completados sin ninguna pista usada."""
    result = await db.execute(
        select(func.count()).select_from(UserProgress).where(
            UserProgress.user_id == user_id,
            UserProgress.completed.is_(True),
            UserProgress.hints_used == 0,
        )
    )
    return result.scalar_one() or 0


async def _count_distinct_sectors(db: AsyncSession, user_id: uuid.UUID) -> int:
    """Cuenta sectores distintos donde el usuario completó al menos un nivel."""
    from app.models.challenge import Challenge  # local import to avoid circular
    result = await db.execute(
        select(func.count(Challenge.sector_id.distinct()))
        .join(UserProgress, UserProgress.challenge_id == Challenge.id)
        .where(
            UserProgress.user_id == user_id,
            UserProgress.completed.is_(True),
            Challenge.sector_id.isnot(None),
        )
    )
    return result.scalar_one() or 0


async def get_user_achievements(
    db: AsyncSession,
    user_id: uuid.UUID,
) -> list[dict]:
    """Retorna todos los logros desbloqueados por el usuario, enriquecidos con metadata."""
    result = await db.execute(
        select(UserAchievement)
        .where(UserAchievement.user_id == user_id)
        .order_by(UserAchievement.unlocked_at.desc())
    )
    records = result.scalars().all()
    return [
        {
            **ACHIEVEMENTS.get(r.achievement_id, {"name": r.achievement_id, "icon": "🏅", "description": "", "xp_bonus": 0, "rarity": "common"}),
            "id": r.achievement_id,
            "unlocked_at": r.unlocked_at.isoformat(),
        }
        for r in records
    ]
