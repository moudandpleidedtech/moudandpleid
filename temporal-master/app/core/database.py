from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

# SSL requerido para Supabase y cualquier BD en producción (DB_SSL=true)
_connect_args: dict = {}
if settings.DB_SSL:
    import ssl as _ssl
    _ssl_ctx = _ssl.create_default_context()
    _connect_args = {"ssl": _ssl_ctx}

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
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


async def init_db() -> None:
    # Import all models so Base.metadata includes their tables
    import app.models.user  # noqa: F401
    import app.models.challenge  # noqa: F401
    import app.models.user_progress  # noqa: F401
    import app.models.concept_mastery  # noqa: F401
    import app.models.duel  # noqa: F401
    import app.models.bitacora_read  # noqa: F401  — add_daki_bitacora_tracking
    import app.models.user_metrics   # noqa: F401  — user telemetry
    import app.models.daki_interception  # noqa: F401  — Protocolo Memoria Muscular
    import app.models.user_core_memory   # noqa: F401  — Módulo de Memoria Evolutiva

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # Agrega columnas nuevas en tablas ya existentes (idempotente)
        await conn.execute(text(
            "ALTER TABLE challenges "
            "ADD COLUMN IF NOT EXISTS test_inputs_json TEXT NOT NULL DEFAULT '[]'"
        ))
        # Columnas de currículo (Prompt 12)
        for stmt in [
            "ALTER TABLE challenges ADD COLUMN IF NOT EXISTS level_order INTEGER",
            "ALTER TABLE challenges ADD COLUMN IF NOT EXISTS phase VARCHAR(20)",
            "ALTER TABLE challenges ADD COLUMN IF NOT EXISTS concepts_taught_json TEXT NOT NULL DEFAULT '[]'",
            "ALTER TABLE challenges ADD COLUMN IF NOT EXISTS grid_map_json TEXT",
            "ALTER TABLE challenges ADD COLUMN IF NOT EXISTS challenge_type VARCHAR(20) NOT NULL DEFAULT 'python'",
        ]:
            await conn.execute(text(stmt))
        # Columnas de telemetría (Prompt 13)
        for stmt in [
            "ALTER TABLE user_progress ADD COLUMN IF NOT EXISTS hints_used INTEGER NOT NULL DEFAULT 0",
            "ALTER TABLE user_progress ADD COLUMN IF NOT EXISTS syntax_errors_total INTEGER NOT NULL DEFAULT 0",
        ]:
            await conn.execute(text(stmt))
        # Contenido teórico (Prompt 18)
        await conn.execute(text(
            "ALTER TABLE challenges ADD COLUMN IF NOT EXISTS theory_content TEXT"
        ))
        # Liga competitiva (Prompt 19)
        await conn.execute(text(
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS league_tier VARCHAR(30) NOT NULL DEFAULT 'Bronce'"
        ))
        # Sistema PvP Elo (Prompt 20)
        await conn.execute(text(
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS elo_rating INTEGER NOT NULL DEFAULT 1200"
        ))
        # Briefing de misión (Prompt B)
        for stmt in [
            "ALTER TABLE challenges ADD COLUMN IF NOT EXISTS lore_briefing TEXT",
            "ALTER TABLE challenges ADD COLUMN IF NOT EXISTS pedagogical_objective TEXT",
            "ALTER TABLE challenges ADD COLUMN IF NOT EXISTS syntax_hint TEXT",
        ]:
            await conn.execute(text(stmt))
        # Telemetría de usuario — user_metrics (Backlog Item 1)
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

        # Medallas de usuario (Gamificación Boss)
        await conn.execute(text(
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS badges_json TEXT NOT NULL DEFAULT '[]'"
        ))

        # Pistas progresivas por misión
        await conn.execute(text(
            "ALTER TABLE challenges ADD COLUMN IF NOT EXISTS hints_json TEXT NOT NULL DEFAULT '[]'"
        ))

        # DAKI State Machine
        await conn.execute(text(
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS daki_level INTEGER NOT NULL DEFAULT 1"
        ))

        # Telemetría extendida — El Ojo de DAKI
        for stmt in [
            "ALTER TABLE user_metrics ADD COLUMN IF NOT EXISTS hints_used INTEGER NOT NULL DEFAULT 0",
            "ALTER TABLE user_metrics ADD COLUMN IF NOT EXISTS syntax_errors_log TEXT NOT NULL DEFAULT '[]'",
        ]:
            await conn.execute(text(stmt))

        # Arquitectura GG — 100 niveles
        for stmt in [
            "ALTER TABLE challenges ADD COLUMN IF NOT EXISTS sector_id INTEGER",
            "ALTER TABLE challenges ADD COLUMN IF NOT EXISTS difficulty VARCHAR(10)",
            "ALTER TABLE challenges ADD COLUMN IF NOT EXISTS is_project BOOLEAN NOT NULL DEFAULT FALSE",
            "ALTER TABLE challenges ADD COLUMN IF NOT EXISTS telemetry_goal_time INTEGER",
        ]:
            await conn.execute(text(stmt))
        # Índice para búsquedas por sector
        await conn.execute(text(
            "CREATE INDEX IF NOT EXISTS ix_challenges_sector_id ON challenges (sector_id)"
        ))

        # Protocolo Memoria Muscular — tabla de intercepciones DAKI
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
            "CREATE INDEX IF NOT EXISTS ix_daki_interceptions_user_id "
            "ON daki_interceptions (user_id)"
        ))

        # Bitácora DAKI — add_daki_bitacora_tracking
        # La tabla user_bitacora_read se crea vía create_all (modelo registrado arriba).
        # Este índice compuesto acelera la query GET /bitacora/unread?user_id=...
        await conn.execute(text(
            "CREATE INDEX IF NOT EXISTS ix_ubr_user_archivo "
            "ON user_bitacora_read (user_id, archivo_id)"
        ))

        # Freemium gate (Prompt 52)
        await conn.execute(text(
            "ALTER TABLE challenges ADD COLUMN IF NOT EXISTS is_free BOOLEAN NOT NULL DEFAULT FALSE"
        ))

        # Sistema de Rangos (Prompt 54)
        for stmt in [
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS points INTEGER NOT NULL DEFAULT 0",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS current_rank VARCHAR(60) NOT NULL DEFAULT 'Trainee'",
        ]:
            await conn.execute(text(stmt))

        # Memoria Evolutiva (Prompt 56) — user_core_memory se crea vía create_all.
        # El índice en user_id acelera get_recent_events().
        await conn.execute(text(
            "CREATE INDEX IF NOT EXISTS ix_user_core_memory_user_id "
            "ON user_core_memory (user_id)"
        ))
