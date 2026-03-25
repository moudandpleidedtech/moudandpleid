"""
semantic_cache.py — SemanticCacheService
─────────────────────────────────────────
Escudo Térmico: intercepta llamadas redundantes a la IA hasheando
la combinación (nivel + código + error). Costo $0 en cache hit.

Almacenamiento actual: dict en memoria.
Interfaz diseñada para swap transparente a Redis sin cambiar contratos.
"""

from __future__ import annotations

import hashlib
import logging
import time
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Final, Optional

logger = logging.getLogger(__name__)

# ── Constantes ────────────────────────────────────────────────────────────────

DEFAULT_TTL_SECONDS: Final[int] = 3600          # 1 hora
MAX_CACHE_ENTRIES:   Final[int] = 10_000        # límite de memoria segura
HASH_ALGORITHM:      Final[str] = "sha256"


# ── Estructuras internas ──────────────────────────────────────────────────────

@dataclass
class CacheEntry:
    response:   str
    created_at: float = field(default_factory=time.monotonic)
    hits:       int   = 0

    def is_expired(self, ttl: int = DEFAULT_TTL_SECONDS) -> bool:
        return (time.monotonic() - self.created_at) > ttl


# ── Servicio ──────────────────────────────────────────────────────────────────

class SemanticCacheService:
    """
    Caché semántico para respuestas de IA.

    - Clave: SHA-256(mission_level + normalizado(user_code) + normalizado(compiler_error))
    - Almacenamiento: dict en memoria (swap a Redis: implementar _get/_set con aioredis)
    - Estadísticas: hits, misses, frecuencia de errores por nivel
    """

    def __init__(self, ttl_seconds: int = DEFAULT_TTL_SECONDS) -> None:
        self._ttl             = ttl_seconds
        self._cache:          dict[str, CacheEntry]            = {}
        self._error_freq:     dict[tuple[int, str], int]       = defaultdict(int)
        self._stats:          dict[str, int]                   = {"hits": 0, "misses": 0, "evictions": 0}

    # ── Clave ─────────────────────────────────────────────────────────────────

    async def generate_cache_key(
        self,
        mission_level:  int,
        user_code:      str,
        compiler_error: str = "",
    ) -> str:
        """
        Genera un hash SHA-256 determinístico a partir de los inputs normalizados.

        Normalización:
        - Código: strip + lowercase + colapsar espacios múltiples
        - Error:  strip + lowercase (sin normalizar indentación — es semántica)
        """
        try:
            normalized_code  = " ".join(user_code.strip().lower().split())
            normalized_error = compiler_error.strip().lower()
            raw = f"{mission_level}|{normalized_code}|{normalized_error}"
            return hashlib.new(HASH_ALGORITHM, raw.encode("utf-8")).hexdigest()
        except Exception as exc:
            logger.error("generate_cache_key falló: %s", exc, exc_info=True)
            raise ValueError(f"No se pudo generar la clave de caché: {exc}") from exc

    # ── Lectura ───────────────────────────────────────────────────────────────

    async def get_cached_response(self, cache_key: str) -> Optional[str]:
        """
        Retorna la respuesta cacheada si existe y no expiró.
        Retorna None en cache miss o entrada expirada.
        """
        try:
            entry = self._cache.get(cache_key)

            if entry is None:
                self._stats["misses"] += 1
                return None

            if entry.is_expired(self._ttl):
                del self._cache[cache_key]
                self._stats["evictions"] += 1
                self._stats["misses"]    += 1
                logger.debug("Cache EXPIRED → key=%s…", cache_key[:12])
                return None

            entry.hits           += 1
            self._stats["hits"]  += 1
            logger.debug(
                "Cache HIT → key=%s… | hits_acumulados=%d",
                cache_key[:12],
                entry.hits,
            )
            return entry.response

        except Exception as exc:
            logger.error("get_cached_response falló: %s", exc, exc_info=True)
            return None   # fallo silencioso: el sistema cae al LLM real

    # ── Escritura ─────────────────────────────────────────────────────────────

    async def save_to_cache(self, cache_key: str, ai_response: str) -> None:
        """
        Persiste la respuesta de la IA en caché.
        Aplica evicción FIFO si se supera MAX_CACHE_ENTRIES.
        """
        try:
            if not cache_key or not ai_response:
                logger.warning("save_to_cache ignorado: key o response vacíos")
                return

            if len(self._cache) >= MAX_CACHE_ENTRIES:
                oldest_key = next(iter(self._cache))
                del self._cache[oldest_key]
                self._stats["evictions"] += 1
                logger.debug("Cache EVICT (FIFO) → key=%s…", oldest_key[:12])

            self._cache[cache_key] = CacheEntry(response=ai_response)
            logger.debug("Cache SAVE → key=%s… | total_entries=%d", cache_key[:12], len(self._cache))

        except Exception as exc:
            logger.error("save_to_cache falló: %s", exc, exc_info=True)
            # No propagar: fallar al guardar no debe romper el flujo principal

    # ── Frecuencia de errores ─────────────────────────────────────────────────

    def check_error_frequency(self, mission_level: int, error_type: str) -> int:
        """
        Registra y retorna cuántas veces ocurre un tipo de error en un nivel.

        Propósito táctico: detectar errores recurrentes para generar
        alertas preventivas a futuros Operadores antes de que los cometan.

        Args:
            mission_level: Nivel de la misión donde ocurrió el error.
            error_type:    Tipo normalizado (ej. "TypeError", "IndentationError").

        Returns:
            Frecuencia acumulada del error en ese nivel.
        """
        try:
            key                       = (mission_level, error_type.strip().lower())
            self._error_freq[key]    += 1
            count                     = self._error_freq[key]
            logger.debug(
                "ErrorFreq → nivel=%d | tipo=%s | count=%d",
                mission_level, error_type, count,
            )
            return count
        except Exception as exc:
            logger.error("check_error_frequency falló: %s", exc, exc_info=True)
            return 0

    # ── Utilidades ────────────────────────────────────────────────────────────

    def get_stats(self) -> dict[str, int]:
        """Retorna métricas de rendimiento del caché."""
        return {
            **self._stats,
            "total_entries": len(self._cache),
            "total_error_types_tracked": len(self._error_freq),
        }

    def invalidate(self, cache_key: str) -> bool:
        """Elimina una entrada específica. Retorna True si existía."""
        existed = self._cache.pop(cache_key, None) is not None
        if existed:
            logger.info("Cache INVALIDATED → key=%s…", cache_key[:12])
        return existed

    def flush(self) -> None:
        """Vacía el caché completo. Usar con precaución."""
        count = len(self._cache)
        self._cache.clear()
        self._stats["evictions"] += count
        logger.warning("Cache FLUSHED → %d entradas eliminadas", count)


# ── Singleton ─────────────────────────────────────────────────────────────────

semantic_cache_service = SemanticCacheService()
