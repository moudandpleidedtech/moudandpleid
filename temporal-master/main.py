from contextlib import asynccontextmanager
import os

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from sqlalchemy import func, select, text

from app.api.v1.router import router
from app.core.config import settings
from app.core.database import AsyncSessionLocal, init_db
from app.core.rate_limit import limiter

# ── Sentry (error tracking) ───────────────────────────────────────────────────
# Activar: agregar SENTRY_DSN en las env vars de Render.
# Obtener DSN: sentry.io → nuevo proyecto → Python → DSN.
_SENTRY_DSN = os.getenv("SENTRY_DSN", "")
if _SENTRY_DSN:
    try:
        import sentry_sdk
        sentry_sdk.init(
            dsn=_SENTRY_DSN,
            traces_sample_rate=0.2,   # 20% de requests trackeadas (bajo impacto)
            profiles_sample_rate=0.1,
            environment="production" if not settings.DEBUG else "development",
        )
        print("✅  [sentry] Error tracking activo.")
    except ImportError:
        print("⚠️  [sentry] sentry-sdk no instalado — pip install sentry-sdk")


async def _auto_seed() -> None:
    """Si la tabla challenges está vacía, carga todos los sectores automáticamente."""
    from app.models.challenge import Challenge  # noqa: F401 — registrar modelo
    async with AsyncSessionLocal() as session:
        count = await session.scalar(select(func.count()).select_from(Challenge))
    if count and count > 0:
        return  # Ya hay datos — nada que hacer

    print("🌱  [auto-seed] Base de datos vacía — iniciando inyección de contenido...")
    try:
        from scripts.seed_master import seed as seed_all
        await seed_all()
        from scripts.seed_tactical_keys import seed as seed_keys
        await seed_keys()
        print("✅  [auto-seed] Contenido cargado correctamente.")
    except Exception as exc:  # pragma: no cover
        print(f"⚠️  [auto-seed] Error durante la inyección: {exc}")


async def _seed_predict_challenges() -> None:
    """
    Siembra los 10 Predict Challenges (L180-L189, sector 21).
    Idempotente: usa UUIDs estables (uuid5) — INSERT ON CONFLICT DO NOTHING.
    El operador lee código y predice el output sin ejecutarlo.
    """
    import uuid
    import json as _json
    from app.models.challenge import Challenge, DifficultyTier

    _NS = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")

    PREDICT_CHALLENGES = [
        dict(
            level_order=180, difficulty_tier=DifficultyTier.INTERMEDIATE,
            difficulty="medium", base_xp_reward=120,
            title="PREDICCIÓN 01: Precedencia de Operadores",
            description="Leé el código. Antes de ejecutarlo, predecí el output exacto. "
                        "Escribí el número que verías en la consola.",
            initial_code="result = 2 + 3 * 4 - 1\nprint(result)",
            expected_output="13",
            concepts_taught=["operator_precedence", "arithmetic"],
            lore_briefing="El sistema evalúa expresiones. Predecí el resultado antes de que DAKI lo ejecute.",
            pedagogical_objective="Internalizar la precedencia de operadores aritméticos en Python.",
        ),
        dict(
            level_order=181, difficulty_tier=DifficultyTier.INTERMEDIATE,
            difficulty="medium", base_xp_reward=120,
            title="PREDICCIÓN 02: Indexing de Strings",
            description="Leé el código. Predecí las dos líneas de output que aparecerán en la consola.",
            initial_code='word = "Python"\nprint(word[0] + word[-1])\nprint(len(word))',
            expected_output="Pn\n6",
            concepts_taught=["string_indexing", "len", "string"],
            lore_briefing="Las cadenas son secuencias indexables. DAKI verifica si conocés los índices negativos.",
            pedagogical_objective="Dominar indexing positivo y negativo en strings.",
        ),
        dict(
            level_order=182, difficulty_tier=DifficultyTier.INTERMEDIATE,
            difficulty="medium", base_xp_reward=130,
            title="PREDICCIÓN 03: Booleanos como Enteros",
            description="Python trata True como 1 y False como 0. Predecí las 3 líneas de output.",
            initial_code="x = True\ny = False\nprint(x + x)\nprint(x * 5)\nprint(y + 10)",
            expected_output="2\n5\n10",
            concepts_taught=["boolean", "type", "arithmetic"],
            lore_briefing="Los booleanos son subclase de int. Un concepto que muchos operadores desconocen.",
            pedagogical_objective="Entender que True==1 y False==0 en Python.",
        ),
        dict(
            level_order=183, difficulty_tier=DifficultyTier.INTERMEDIATE,
            difficulty="medium", base_xp_reward=130,
            title="PREDICCIÓN 04: Slicing de Listas",
            description="Predecí el output exacto — incluyendo los corchetes y comas.",
            initial_code="nums = [10, 20, 30, 40, 50]\nprint(nums[-2:])\nprint(nums[::-1])",
            expected_output="[40, 50]\n[50, 40, 30, 20, 10]",
            concepts_taught=["list", "slice", "negative_index"],
            lore_briefing="El slicing con paso negativo es una trampa clásica. Demostrá que la conocés.",
            pedagogical_objective="Dominar slicing con índices negativos y paso inverso.",
        ),
        dict(
            level_order=184, difficulty_tier=DifficultyTier.INTERMEDIATE,
            difficulty="medium", base_xp_reward=140,
            title="PREDICCIÓN 05: Cadena de Métodos de String",
            description="Los métodos de string se encadenan de izquierda a derecha. Predecí el output.",
            initial_code='texto = "  hola mundo  "\nprint(texto.strip().upper().replace("O", "0"))',
            expected_output="H0LA MUND0",
            concepts_taught=["string", "method_chaining", "strip", "upper", "replace"],
            lore_briefing="El chaining de métodos es idiomático en Python. Cada método retorna el resultado anterior.",
            pedagogical_objective="Razonar sobre transformaciones encadenadas en strings.",
        ),
        dict(
            level_order=185, difficulty_tier=DifficultyTier.INTERMEDIATE,
            difficulty="hard", base_xp_reward=160,
            title="PREDICCIÓN 06: List Comprehension con Filtro",
            description="Predecí qué números pasan el filtro y cuál es su suma.",
            initial_code="nums = [x for x in range(1, 6) if x % 2 == 0]\nprint(nums)\nprint(sum(nums))",
            expected_output="[2, 4]\n6",
            concepts_taught=["list_comprehension", "filter", "range", "sum"],
            lore_briefing="Las comprensiones con condición filtran elementos. DAKI evalúa si podés razonarlas sin ejecutarlas.",
            pedagogical_objective="Predecir el resultado de list comprehensions con condiciones.",
        ),
        dict(
            level_order=186, difficulty_tier=DifficultyTier.INTERMEDIATE,
            difficulty="hard", base_xp_reward=160,
            title="PREDICCIÓN 07: Mutación de Diccionario",
            description="El dict se modifica antes de imprimirse. Predecí el output exacto.",
            initial_code='d = {"a": 1, "b": 2, "c": 3}\nd["a"] += 10\nd.pop("b")\nprint(sorted(d.items()))',
            expected_output="[('a', 11), ('c', 3)]",
            concepts_taught=["dict", "mutation", "pop", "sorted", "items"],
            lore_briefing="Las operaciones de mutación cambian el estado. Rastreá los cambios mentalmente.",
            pedagogical_objective="Razonar sobre el estado de un dict después de múltiples mutaciones.",
        ),
        dict(
            level_order=187, difficulty_tier=DifficultyTier.INTERMEDIATE,
            difficulty="hard", base_xp_reward=170,
            title="PREDICCIÓN 08: Scope de Variables",
            description="Una función crea su propio scope. ¿La variable global cambia?",
            initial_code="x = 5\ndef modify():\n    x = 10\n    return x\nprint(modify())\nprint(x)",
            expected_output="10\n5",
            concepts_taught=["scope", "local_variable", "global_variable", "function"],
            lore_briefing="Variables locales y globales coexisten. La asignación dentro de una función crea una variable local.",
            pedagogical_objective="Distinguir scope local vs global en funciones Python.",
        ),
        dict(
            level_order=188, difficulty_tier=DifficultyTier.ADVANCED,
            difficulty="hard", base_xp_reward=200,
            title="PREDICCIÓN 09: El Argumento Mutable (Python Gotcha)",
            description="Este es uno de los bugs más famosos de Python. Predecí las 3 líneas.",
            initial_code="def append_to(val, lst=[]):\n    lst.append(val)\n    return lst\n\nprint(append_to(1))\nprint(append_to(2))\nprint(append_to(3, []))",
            expected_output="[1]\n[1, 2]\n[3]",
            concepts_taught=["mutable_default", "function", "parameter", "list"],
            lore_briefing="Los argumentos por defecto mutables se comparten entre llamadas. Un gotcha que atrapa a seniors.",
            pedagogical_objective="Entender por qué los argumentos mutables por defecto son peligrosos.",
        ),
        dict(
            level_order=189, difficulty_tier=DifficultyTier.ADVANCED,
            difficulty="expert", base_xp_reward=350,
            title="PREDICCIÓN 10 — BOSS: Map, Filter y Lambda",
            description="PROTOCOLO FINAL DE LECTURA. Predecí las 3 líneas del output. Sin errores.",
            initial_code="nums = [1, 2, 3, 4, 5]\ndoubled = list(map(lambda x: x * 2, nums))\nresult = list(filter(lambda x: x > 6, doubled))\nprint(doubled)\nprint(result)\nprint(len(result))",
            expected_output="[2, 4, 6, 8, 10]\n[8, 10]\n2",
            concepts_taught=["map", "filter", "lambda", "list", "higher_order_function"],
            lore_briefing="El operador que puede leer código como prosa y predecir su salida exacta es un Lector de Sistemas. Nivel: Élite.",
            pedagogical_objective="Razonar sobre map y filter con lambdas sin ejecutar el código.",
            is_phase_boss=True,
        ),
    ]

    async with AsyncSessionLocal() as session:
        for ch in PREDICT_CHALLENGES:
            stable_id = uuid.uuid5(_NS, f"daki.predict.{ch['level_order']}")
            existing = await session.get(Challenge, stable_id)
            if existing:
                continue
            is_boss = ch.pop("is_phase_boss", False)
            concepts = ch.pop("concepts_taught")
            session.add(Challenge(
                id=stable_id,
                challenge_type="predict",
                sector_id=21,
                is_phase_boss=is_boss,
                is_project=False,
                strict_match=True,
                is_free=False,
                is_ironman=False,
                test_inputs_json="[]",
                concepts_taught_json=_json.dumps(concepts),
                hints_json="[]",
                phase="PREDICT",
                telemetry_goal_time=None,
                **ch,
            ))
        await session.commit()
    print("✅  [seed-predict] Predict Challenges L180-L189 verificados.")


async def _seed_incursions() -> None:
    """
    Sincroniza el catálogo de Incursiones (D021 — Mapa de Niebla).
    Idempotente: UPSERT por slug — nunca sobreescribe el campo `status`.
    Se ejecuta en cada startup para propagar cambios de contenido.
    """
    from app.models.incursion import Incursion  # noqa: F401 — registrar modelo
    try:
        from scripts.seed_incursions import seed as seed_inc
        await seed_inc()
    except Exception as exc:  # pragma: no cover
        print(f"⚠️  [seed-incursions] Error: {exc}")


async def _ensure_dev_user() -> None:
    """
    Crea (o actualiza) el usuario de desarrollo NEXO con acceso total.
    Idempotente: si ya existe, actualiza sus flags sin cambiar el UUID.

    Credenciales locales:
      Email    → admin@daki.dev
      Callsign → NEXO
      Password → DAKIadmin2025
    """
    from app.core.security import hash_password
    from app.models.user import User

    DEV_EMAIL    = "admin@daki.dev"
    DEV_CALLSIGN = "NEXO"
    DEV_PASSWORD = "DAKIadmin2025"

    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.email == DEV_EMAIL))
        user = result.scalar_one_or_none()

        if user is None:
            user = User(
                email=DEV_EMAIL,
                callsign=DEV_CALLSIGN,
                password_hash=hash_password(DEV_PASSWORD),
                current_level=99,
                total_xp=99_000,
                is_licensed=True,
                is_admin=True,
                role="FOUNDER",
                subscription_status="ACTIVE",
                league_tier="Diamante",
                current_rank="Comandante Supremo",
            )
            session.add(user)
            print("🛡️  [dev-user] Usuario NEXO creado — admin@daki.dev / DAKIadmin2025 [FOUNDER]")
        else:
            # Garantiza flags correctos aunque el usuario ya existiera
            user.is_licensed         = True
            user.is_admin            = True
            user.current_level       = 99
            user.role                = "FOUNDER"
            user.subscription_status = "ACTIVE"
            print("🛡️  [dev-user] Usuario NEXO verificado y actualizado [FOUNDER].")

        await session.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Fail fast si SECRET_KEY no fue cambiada del valor por defecto
    if settings.SECRET_KEY in ("change-me-in-production", ""):
        raise RuntimeError(
            "SECRET_KEY no configurada. Define la variable de entorno SECRET_KEY antes de iniciar."
        )
    await init_db()
    await _auto_seed()
    await _seed_predict_challenges()
    await _seed_incursions()
    # Usuario de desarrollo solo en modo DEBUG — nunca en producción
    if settings.DEBUG:
        await _ensure_dev_user()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    # Documentación interactiva y schema solo en modo DEBUG.
    # En producción ocultamos toda la superficie de la API a actores no deseados.
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    openapi_url="/openapi.json" if settings.DEBUG else None,
    lifespan=lifespan,
)

# ── Rate Limiter (Prompt 61) ───────────────────────────────────────────────────
# Registra el limitador en app.state para que slowapi lo encuentre
# en los decoradores @limiter.limit() de hint.py y daki.py.
app.state.limiter = limiter


async def _daki_rate_limit_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    """429 con voz de DAKI en lugar del mensaje genérico de slowapi."""
    return JSONResponse(
        status_code=429,
        content={
            "detail": "Operador, la red neuronal necesita enfriarse. Mantenga la posición."
        },
    )


app.add_exception_handler(RateLimitExceeded, _daki_rate_limit_handler)

# ── CORS estricto (Prompt 61) ─────────────────────────────────────────────────
# allow_origins lee settings.ALLOWED_ORIGINS (config.py):
#   dev  → http://localhost:3000
#   prod → https://dakiedtech.com, https://www.dakiedtech.com
# Cualquier origen no listado recibe 403 en la verificación del preflight OPTIONS.
app.add_middleware(
    CORSMiddleware,
    # cors_origins = ALLOWED_ORIGINS + FRONTEND_URL (si está definido en env)
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

app.include_router(router)


@app.get("/health", tags=["health"])
async def health_check():
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )
