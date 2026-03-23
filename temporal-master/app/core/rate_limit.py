"""
rate_limit.py — Singleton del limitador de tasa para endpoints LLM (Prompt 61).

Clave: IP del cliente (get_remote_address).
En producción detrás de un proxy reverso (nginx/Caddy), configurar
FORWARDED_ALLOW_IPS en uvicorn para que get_remote_address lea
X-Forwarded-For en lugar de la IP del proxy.

Registrado en main.py como app.state.limiter.
Importado por hint.py y daki.py para el decorador @limiter.limit().
"""

from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
