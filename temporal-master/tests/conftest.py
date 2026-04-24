"""
tests/conftest.py — Configuración global de la suite de tests.

Niveles de test disponibles:
  - e2e      → golpean la API de producción real. Siempre corren.
               Comando: pytest tests/e2e/ -v
  - integration → usan ASGI transport + DB real. Requieren DATABASE_URL real.
               Comando: DATABASE_URL=<neon_url> pytest tests/ -m integration -v
               Con Docker: docker-compose up -d db && pytest tests/ -m integration -v

El marker 'integration' se saltea automáticamente si DATABASE_URL apunta
a un host local/Docker (sin DB real disponible).
"""

import os
import pytest

# ─── Detección de DB disponible ───────────────────────────────────────────────

def _db_is_local() -> bool:
    """True cuando DATABASE_URL apunta a un host local (Docker Compose, localhost)."""
    url = os.getenv("DATABASE_URL", "")
    return not url or "@db:" in url or "@localhost" in url or "127.0.0.1" in url


_SKIP_REASON = (
    "Tests de integración requieren una DB real accesible. "
    "Opciones:\n"
    "  • Docker:  docker-compose up -d db && pytest tests/ -m integration\n"
    "  • Neon:    DATABASE_URL=<url_neon> pytest tests/ -m integration"
)

# ─── Marker reutilizable ──────────────────────────────────────────────────────

needs_db = pytest.mark.skipif(_db_is_local(), reason=_SKIP_REASON)
