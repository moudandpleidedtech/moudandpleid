"""
app/core/database.py — Motor de Base de Datos y Migraciones Auto-gestionadas

Todas las migraciones son idempotentes (IF NOT EXISTS, DO $$ BEGIN ... END $$).
No se usa Alembic: el esquema se auto-actualiza en cada startup via init_db().

Organización:
  _migrate_v1_curriculum()    — columnas de contenido curricular (Prompts 12-13)
  _migrate_v2_gamification()  — liga, elo, badges, daki_level, user_metrics
  _migrate_v3_architecture()  — GG 100 niveles, sector_id, memoria muscular
  _migrate_v4_access()        — freemium, rangos, memoria evolutiva, tactical keys
  _migrate_v5_subscriptions() — Vanguardia alpha, Stripe, is_admin, payment_id
  _migrate_v6_skill_tree()    — D018 árbol habilidades, D022 god mode
  _migrate_v7_cleanup()       — renombres legacy, emails, D030 incursiones
  _migrate_v8_auth()          — Google OAuth index
  _migrate_v9_pedagogy()      — Ironman, edge cases, UPDATEs de datos iniciales
"""

from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

_connect_args: dict = {"ssl": True} if settings.DB_SSL else {}

# pool_size + max_overflow = conexiones físicas máximas al mismo tiempo.
# Con Neon Launch + pooler (PgBouncer): pool_size=15, max_overflow=15 → 30 físicas
# El pooler de Neon multiplexa N sesiones lógicas sobre estas físicas,
# por lo que 200+ usuarios simultáneos funcionan sin problema.
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=15,
    max_overflow=15,
    connect_args=_connect_args,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# ── Migraciones versionadas ────────────────────────────────────────────────────

async def _migrate_v1_curriculum(conn) -> None:
    """Prompts 12-13: columnas curriculares y telemetría básica."""
    await conn.execute(text(
        "ALTER TABLE challenges ADD COLUMN IF NOT EXISTS test_inputs_json TEXT NOT NULL DEFAULT '[]'"
    ))
    for stmt in [
        "ALTER TABLE challenges ADD COLUMN IF NOT EXISTS level_order INTEGER",
        "ALTER TABLE challenges ADD COLUMN IF NOT EXISTS phase VARCHAR(20)",
        "ALTER TABLE challenges ADD COLUMN IF NOT EXISTS concepts_taught_json TEXT NOT NULL DEFAULT '[]'",
        "ALTER TABLE challenges ADD COLUMN IF NOT EXISTS grid_map_json TEXT",
        "ALTER TABLE challenges ADD COLUMN IF NOT EXISTS challenge_type VARCHAR(20) NOT NULL DEFAULT 'python'",
    ]:
        await conn.execute(text(stmt))
    for stmt in [
        "ALTER TABLE user_progress ADD COLUMN IF NOT EXISTS hints_used INTEGER NOT NULL DEFAULT 0",
        "ALTER TABLE user_progress ADD COLUMN IF NOT EXISTS syntax_errors_total INTEGER NOT NULL DEFAULT 0",
    ]:
        await conn.execute(text(stmt))
    # Contenido teórico y briefing (Prompts 18, B)
    for stmt in [
        "ALTER TABLE challenges ADD COLUMN IF NOT EXISTS theory_content TEXT",
        "ALTER TABLE challenges ADD COLUMN IF NOT EXISTS lore_briefing TEXT",
        "ALTER TABLE challenges ADD COLUMN IF NOT EXISTS pedagogical_objective TEXT",
        "ALTER TABLE challenges ADD COLUMN IF NOT EXISTS syntax_hint TEXT",
        "ALTER TABLE challenges ADD COLUMN IF NOT EXISTS hints_json TEXT NOT NULL DEFAULT '[]'",
    ]:
        await conn.execute(text(stmt))


async def _migrate_v2_gamification(conn) -> None:
    """Liga, Elo, badges, DAKI state machine, telemetría extendida."""
    for stmt in [
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS league_tier VARCHAR(30) NOT NULL DEFAULT 'Bronce'",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS elo_rating INTEGER NOT NULL DEFAULT 1200",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS badges_json TEXT NOT NULL DEFAULT '[]'",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS daki_level INTEGER NOT NULL DEFAULT 1",
    ]:
        await conn.execute(text(stmt))
    # Tabla user_metrics con constraint UNIQUE
    await conn.execute(text("""
        CREATE TABLE IF NOT EXISTS user_metrics (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id UUID NOT NULL,
            challenge_id UUID NOT NULL,
            attempts INTEGER NOT NULL DEFAULT 1,
            time_spent_ms INTEGER NOT NULL DEFAULT 0,
            status VARCHAR(10) NOT NULL DEFAULT 'fail',
            first_attempt_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            last_attempt_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            CONSTRAINT uq_metrics_user_challenge UNIQUE (user_id, challenge_id)
        )
    """))
    await conn.execute(text(
        "CREATE INDEX IF NOT EXISTS ix_user_metrics_user_id ON user_metrics (user_id)"
    ))
    # Telemetría extendida
    for stmt in [
        "ALTER TABLE user_metrics ADD COLUMN IF NOT EXISTS hints_used INTEGER NOT NULL DEFAULT 0",
        "ALTER TABLE user_metrics ADD COLUMN IF NOT EXISTS syntax_errors_log TEXT NOT NULL DEFAULT '[]'",
    ]:
        await conn.execute(text(stmt))


async def _migrate_v3_architecture(conn) -> None:
    """Arquitectura GG 100 niveles y Protocolo Memoria Muscular."""
    for stmt in [
        "ALTER TABLE challenges ADD COLUMN IF NOT EXISTS sector_id INTEGER",
        "ALTER TABLE challenges ADD COLUMN IF NOT EXISTS difficulty VARCHAR(10)",
        "ALTER TABLE challenges ADD COLUMN IF NOT EXISTS is_project BOOLEAN NOT NULL DEFAULT FALSE",
        "ALTER TABLE challenges ADD COLUMN IF NOT EXISTS telemetry_goal_time INTEGER",
    ]:
        await conn.execute(text(stmt))
    await conn.execute(text(
        "CREATE INDEX IF NOT EXISTS ix_challenges_sector_id ON challenges (sector_id)"
    ))
    # Tabla daki_interceptions (Memoria Muscular)
    await conn.execute(text("""
        CREATE TABLE IF NOT EXISTS daki_interceptions (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            concept_name VARCHAR(100) NOT NULL,
            triggered_on_challenge_id UUID NOT NULL,
            triggered_on_sector INTEGER NOT NULL,
            mision_flash_json TEXT NOT NULL,
            daki_message TEXT NOT NULL,
            status VARCHAR(10) NOT NULL DEFAULT 'pending',
            flash_attempts INTEGER NOT NULL DEFAULT 0,
            triggered_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            completed_at TIMESTAMPTZ,
            expires_at TIMESTAMPTZ NOT NULL
        )
    """))
    await conn.execute(text(
        "CREATE INDEX IF NOT EXISTS ix_daki_interceptions_user_id ON daki_interceptions (user_id)"
    ))
    # Bitácora DAKI
    await conn.execute(text(
        "CREATE INDEX IF NOT EXISTS ix_ubr_user_archivo ON user_bitacora_read (user_id, archivo_id)"
    ))


async def _migrate_v4_access(conn) -> None:
    """Freemium gate, rangos, memoria evolutiva y llaves tácticas."""
    await conn.execute(text(
        "ALTER TABLE challenges ADD COLUMN IF NOT EXISTS is_free BOOLEAN NOT NULL DEFAULT FALSE"
    ))
    for stmt in [
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS points INTEGER NOT NULL DEFAULT 0",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS current_rank VARCHAR(60) NOT NULL DEFAULT 'Trainee'",
    ]:
        await conn.execute(text(stmt))
    await conn.execute(text(
        "CREATE INDEX IF NOT EXISTS ix_user_core_memory_user_id ON user_core_memory (user_id)"
    ))
    await conn.execute(text(
        "CREATE INDEX IF NOT EXISTS ix_tactical_keys_code ON tactical_access_keys (code_string)"
    ))
    await conn.execute(text(
        "UPDATE tactical_access_keys SET code_string = UPPER(code_string) "
        "WHERE code_string != UPPER(code_string)"
    ))
    # Freemium: primeros 10 niveles + sector 0 + tutoriales son gratuitos
    await conn.execute(text(
        "UPDATE challenges SET is_free = TRUE "
        "WHERE (level_order IS NOT NULL AND level_order <= 9) "
        "   OR sector_id = 0 "
        "   OR challenge_type = 'tutorial'"
    ))


async def _migrate_v5_subscriptions(conn) -> None:
    """Operación Vanguardia (suscripción alpha), Stripe, is_admin."""
    for stmt in [
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS subscription_status VARCHAR(20) NOT NULL DEFAULT 'INACTIVE'",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS trial_end_date TIMESTAMPTZ",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS stripe_customer_id VARCHAR(255)",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS is_admin BOOLEAN NOT NULL DEFAULT FALSE",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS payment_id VARCHAR(255)",
    ]:
        await conn.execute(text(stmt))
    for stmt in [
        "CREATE INDEX IF NOT EXISTS ix_users_subscription_status ON users (subscription_status)",
        "CREATE INDEX IF NOT EXISTS ix_alpha_codes_is_used ON alpha_codes (is_used)",
    ]:
        await conn.execute(text(stmt))


async def _migrate_v6_skill_tree(conn) -> None:
    """D018 Árbol de Habilidades y D022 God Mode (rol FOUNDER)."""
    for stmt in [
        "ALTER TABLE challenges ADD COLUMN IF NOT EXISTS codex_id VARCHAR(50)",
        "ALTER TABLE challenges ADD COLUMN IF NOT EXISTS prerequisite_challenge_id UUID REFERENCES challenges(id)",
        "ALTER TABLE challenges ADD COLUMN IF NOT EXISTS is_phase_boss BOOLEAN NOT NULL DEFAULT FALSE",
        "ALTER TABLE challenges ADD COLUMN IF NOT EXISTS strict_match BOOLEAN NOT NULL DEFAULT FALSE",
        "ALTER TABLE user_progress ADD COLUMN IF NOT EXISTS boss_completed BOOLEAN NOT NULL DEFAULT FALSE",
        "ALTER TABLE user_progress ADD COLUMN IF NOT EXISTS codex_id VARCHAR(50)",
        "ALTER TABLE user_progress ADD COLUMN IF NOT EXISTS score INTEGER",
    ]:
        await conn.execute(text(stmt))
    for stmt in [
        "CREATE INDEX IF NOT EXISTS ix_challenges_codex_id ON challenges (codex_id)",
        "CREATE INDEX IF NOT EXISTS ix_user_progress_codex ON user_progress (user_id, codex_id)",
    ]:
        await conn.execute(text(stmt))
    # D022 God Mode
    await conn.execute(text(
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(20) NOT NULL DEFAULT 'USER'"
    ))
    await conn.execute(text("CREATE INDEX IF NOT EXISTS ix_users_role ON users (role)"))


async def _migrate_v7_cleanup(conn) -> None:
    """Limpieza de esquema legacy, renombres de columnas, D030 incursiones."""
    for stmt in [
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS mission_state JSONB NOT NULL DEFAULT '{}'",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS last_login TIMESTAMPTZ",
    ]:
        await conn.execute(text(stmt))
    # Renombres de esquema v0 → v1 (idempotente)
    for old_col, new_col in [
        ("username",        "callsign"),
        ("hashed_password", "password_hash"),
        ("is_paid",         "is_licensed"),
    ]:
        await conn.execute(text(f"""
            DO $$ BEGIN
                IF EXISTS (
                    SELECT 1 FROM information_schema.columns
                    WHERE table_name='users' AND column_name='{old_col}'
                ) THEN
                    ALTER TABLE users RENAME COLUMN {old_col} TO {new_col};
                END IF;
            END $$;
        """))
    # Limpieza emails alpha
    await conn.execute(text(
        "UPDATE users SET email = REPLACE(email, '@quest.local', '') "
        "WHERE email LIKE '%@quest.local'"
    ))
    # D030: progresión entre incursiones
    for stmt in [
        "ALTER TABLE incursions ADD COLUMN IF NOT EXISTS prerequisite_incursion_slug VARCHAR(60)",
        "ALTER TABLE incursions ADD COLUMN IF NOT EXISTS total_levels INTEGER",
    ]:
        await conn.execute(text(stmt))


async def _migrate_v8_auth(conn) -> None:
    """Google OAuth — índice parcial en google_id."""
    await conn.execute(text(
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS google_id VARCHAR(255)"
    ))
    await conn.execute(text(
        "CREATE INDEX IF NOT EXISTS ix_users_google_id ON users (google_id) "
        "WHERE google_id IS NOT NULL"
    ))


async def _migrate_v10_pending_activations(conn) -> None:
    """Hotmart: tabla de activaciones pendientes para pagos previos al registro."""
    await conn.execute(text("""
        CREATE TABLE IF NOT EXISTS pending_activations (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            email VARCHAR(255) NOT NULL,
            transaction_id VARCHAR(255) NOT NULL,
            event VARCHAR(50) NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
    """))
    await conn.execute(text(
        "CREATE INDEX IF NOT EXISTS ix_pending_activations_email ON pending_activations (email)"
    ))


async def _migrate_v9_pedagogy(conn) -> None:
    """Protocolo Guerrero: Ironman, Edge Cases y marcado de datos iniciales."""
    for stmt in [
        "ALTER TABLE challenges ADD COLUMN IF NOT EXISTS is_ironman BOOLEAN NOT NULL DEFAULT FALSE",
        "ALTER TABLE challenges ADD COLUMN IF NOT EXISTS edge_cases_json TEXT",
    ]:
        await conn.execute(text(stmt))

    # Ironman: 2° challenge no-boss por sector (sectores 8-20), idempotente
    await conn.execute(text("""
        WITH picks AS (
            SELECT id,
                   ROW_NUMBER() OVER (
                       PARTITION BY sector_id ORDER BY level_order
                   ) AS rn
            FROM challenges
            WHERE sector_id BETWEEN 8 AND 20
              AND is_phase_boss = FALSE
              AND is_project    = FALSE
              AND challenge_type IN ('python', 'debug')
        )
        UPDATE challenges SET is_ironman = TRUE
        WHERE id IN (SELECT id FROM picks WHERE rn = 2)
    """))

    # Edge cases en boss challenges (solo si no tienen ya)
    boss_edge_cases: list[tuple[int, str]] = [
        (136, '[{"description": "¿Qué pasa si la lista de entrada está vacía? ¿Tu solución retorna [] o lanza un error?"}, {"description": "¿Funciona tu solución con valores negativos o cero? Probá el caso extremo."}, {"description": "¿Cuánta memoria usa tu solución con 1 millón de elementos? Considerá un generador."}]'),
        (142, '[{"description": "¿Tu función maneja el caso donde no se pasan argumentos opcionales?"}, {"description": "¿Qué pasa si se pasa None como entrada? ¿Lanza un error o lo maneja silenciosamente?"}, {"description": "¿Podés reescribir esto en una línea con comprensión de lista o expresión generadora?"}]'),
        (150, '[{"description": "¿Qué pasa si intentás instanciar la clase sin pasar argumentos al __init__?"}, {"description": "¿Tus métodos modifican el estado del objeto (mutables) o retornan nuevos valores (inmutables)?"}, {"description": "¿Cómo se vería este diseño si necesitás una subclase que hereda el comportamiento?"}]'),
        (155, '[{"description": "¿Tu solución maneja inputs de tipo incorrecto (string donde se espera int)?"}, {"description": "¿Qué pasa con una lista de 1 elemento? ¿Y con una lista ya ordenada?"}, {"description": "¿Cuál es la complejidad temporal de tu solución? O(n), O(n log n) o O(n²)?"}]'),
        (161, '[{"description": "¿Tu solución es Pythónica? ¿Hay algún built-in (map, filter, zip, enumerate) que simplifique el código?"}, {"description": "¿Qué pasa si el input tiene duplicados? ¿Tu solución los maneja correctamente?"}, {"description": "¿Cómo se comporta tu código con 10,000 elementos? ¿Hay un bottleneck?"}]'),
        (169, '[{"description": "¿Encontraste todos los bugs? Los bugs silenciosos (sin error pero con resultado incorrecto) son los más peligrosos."}, {"description": "¿Qué herramienta usarías en producción para detectar este bug automáticamente? (pytest, type hints, assertions)"}, {"description": "¿Cómo escribirías un test unitario que hubiera detectado este bug antes de llegar a producción?"}]'),
        (179, '[{"description": "¿Cuál es la complejidad temporal y espacial de tu solución? ¿El entrevistador te preguntaría si podés hacerlo mejor?"}, {"description": "¿Tu solución funciona con inputs vacíos, None, o con un solo elemento? Los entrevistadores siempre prueban edge cases."}, {"description": "¿Podés explicar tu solución en voz alta en 30 segundos? Si no podés explicarla, no la entendés lo suficientemente bien."}]'),
    ]
    for level_order, edge_json in boss_edge_cases:
        await conn.execute(
            text("UPDATE challenges SET edge_cases_json = :ej WHERE level_order = :lo AND edge_cases_json IS NULL"),
            {"ej": edge_json, "lo": level_order},
        )


# ── Punto de entrada principal ─────────────────────────────────────────────────

async def init_db() -> None:
    """
    Ejecuta create_all + todas las migraciones en orden.
    Completamente idempotente: seguro de llamar en cada startup.
    """
    # Registro de todos los modelos (necesario para Base.metadata.create_all)
    import app.models.user               # noqa: F401
    import app.models.challenge          # noqa: F401
    import app.models.user_progress      # noqa: F401
    import app.models.concept_mastery    # noqa: F401
    import app.models.duel               # noqa: F401
    import app.models.bitacora_read      # noqa: F401
    import app.models.user_metrics       # noqa: F401
    import app.models.daki_interception  # noqa: F401
    import app.models.user_core_memory   # noqa: F401
    import app.models.tactical_key       # noqa: F401
    import app.models.session_log        # noqa: F401
    import app.models.alpha_code         # noqa: F401
    import app.models.beta_code          # noqa: F401
    import app.models.incursion          # noqa: F401
    import app.models.challenge_prerequisite  # noqa: F401
    import app.models.intelligence_report    # noqa: F401
    import app.models.pending_activation     # noqa: F401

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await _migrate_v1_curriculum(conn)
        await _migrate_v2_gamification(conn)
        await _migrate_v3_architecture(conn)
        await _migrate_v4_access(conn)
        await _migrate_v5_subscriptions(conn)
        await _migrate_v6_skill_tree(conn)
        await _migrate_v7_cleanup(conn)
        await _migrate_v8_auth(conn)
        await _migrate_v9_pedagogy(conn)
        await _migrate_v10_pending_activations(conn)
