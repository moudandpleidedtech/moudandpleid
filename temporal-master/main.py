from contextlib import asynccontextmanager

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


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await _auto_seed()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    # Documentación interactiva solo en modo DEBUG; ocultarla en producción
    # evita exponer la superficie de la API a actores no deseados.
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
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
