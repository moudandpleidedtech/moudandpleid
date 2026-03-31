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
    await init_db()
    await _auto_seed()
    await _seed_incursions()
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
