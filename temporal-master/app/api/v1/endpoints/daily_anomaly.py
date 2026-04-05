"""
daily_anomaly.py — Anomalía Diaria (Directiva F3)

Endpoint determinista: GET /daily-anomaly
Usa la fecha del servidor para generar una misión especial del día reproducible.
Sin tabla en la DB — todo se computa desde el banco estático de anomalías.
"""

import hashlib
from datetime import date

from fastapi import APIRouter

router = APIRouter()

# ── Banco de anomalías (15 entradas) ─────────────────────────────────────────

ANOMALIES = [
    {
        "id": "a01",
        "title": "ANOMALÍA ALFA-7",
        "description": "Escribe una función que reciba un número y retorne True si es par, False si es impar.",
        "concept": "boolean",
        "glyph": "⚡",
        "difficulty": "BÁSICO",
        "xp_bonus": 50,
    },
    {
        "id": "a02",
        "title": "SEÑAL PERDIDA",
        "description": "Dado un string, retorna cuántas vocales contiene (a, e, i, o, u).",
        "concept": "string",
        "glyph": "◈",
        "difficulty": "BÁSICO",
        "xp_bonus": 60,
    },
    {
        "id": "a03",
        "title": "BUCLE FANTASMA",
        "description": "Imprime los números del 1 al 20, pero reemplaza múltiplos de 3 con 'NEXO'.",
        "concept": "for_loop",
        "glyph": "◉",
        "difficulty": "INTERMEDIO",
        "xp_bonus": 75,
    },
    {
        "id": "a04",
        "title": "PROTOCOLO FIBONACCI",
        "description": "Genera los primeros N números de Fibonacci y retórnalos en una lista.",
        "concept": "list",
        "glyph": "▲",
        "difficulty": "INTERMEDIO",
        "xp_bonus": 80,
    },
    {
        "id": "a05",
        "title": "INVERSIÓN DE DATOS",
        "description": "Recibe una lista y retorna la misma lista al revés, sin usar .reverse() ni slicing.",
        "concept": "list",
        "glyph": "◀",
        "difficulty": "INTERMEDIO",
        "xp_bonus": 85,
    },
    {
        "id": "a06",
        "title": "CIFRADO CÉSAR",
        "description": "Desplaza cada letra de un string N posiciones en el alfabeto (solo minúsculas).",
        "concept": "string",
        "glyph": "🔑",
        "difficulty": "AVANZADO",
        "xp_bonus": 100,
    },
    {
        "id": "a07",
        "title": "CONTADOR SILENCIOSO",
        "description": "Dado un string, retorna un diccionario con la frecuencia de cada carácter.",
        "concept": "dict",
        "glyph": "◆",
        "difficulty": "INTERMEDIO",
        "xp_bonus": 70,
    },
    {
        "id": "a08",
        "title": "NÚMERO PRIMO",
        "description": "Escribe una función que determine si un número es primo.",
        "concept": "boolean",
        "glyph": "★",
        "difficulty": "INTERMEDIO",
        "xp_bonus": 75,
    },
    {
        "id": "a09",
        "title": "SUMA RECURSIVA",
        "description": "Calcula la suma de todos los números en una lista usando recursión.",
        "concept": "function",
        "glyph": "↺",
        "difficulty": "AVANZADO",
        "xp_bonus": 110,
    },
    {
        "id": "a10",
        "title": "PALÍNDROMO",
        "description": "Determina si un string es un palíndromo (se lee igual al derecho y al revés).",
        "concept": "string",
        "glyph": "⇔",
        "difficulty": "BÁSICO",
        "xp_bonus": 55,
    },
    {
        "id": "a11",
        "title": "FILTRO TÁCTICO",
        "description": "Filtra una lista de números y retorna solo los que son múltiplos de 7.",
        "concept": "list",
        "glyph": "▼",
        "difficulty": "BÁSICO",
        "xp_bonus": 50,
    },
    {
        "id": "a12",
        "title": "DECODIFICADOR",
        "description": "Convierte una lista de enteros ASCII en el string que representan.",
        "concept": "string",
        "glyph": "⌘",
        "difficulty": "INTERMEDIO",
        "xp_bonus": 80,
    },
    {
        "id": "a13",
        "title": "INTERSECCIÓN",
        "description": "Retorna los elementos comunes entre dos listas sin usar sets.",
        "concept": "list",
        "glyph": "∩",
        "difficulty": "INTERMEDIO",
        "xp_bonus": 70,
    },
    {
        "id": "a14",
        "title": "CONTADOR DE PALABRAS",
        "description": "Dado un texto, retorna cuántas veces aparece cada palabra (case-insensitive).",
        "concept": "dict",
        "glyph": "≡",
        "difficulty": "AVANZADO",
        "xp_bonus": 95,
    },
    {
        "id": "a15",
        "title": "SECUENCIA COLATZ",
        "description": "Implementa la secuencia de Collatz: si n es par divide por 2, si no multiplica por 3 y suma 1. Para cuando llegues a 1.",
        "concept": "while_loop",
        "glyph": "∞",
        "difficulty": "AVANZADO",
        "xp_bonus": 120,
    },
]

_DIFFICULTY_COLOR = {
    "BÁSICO":     "#00FF41",
    "INTERMEDIO": "#FFD700",
    "AVANZADO":   "#FF4444",
}


def _get_today_anomaly() -> dict:
    """
    Selecciona la anomalía del día de forma determinista usando un hash de la fecha.
    La misma fecha siempre produce la misma anomalía — sin estado en DB.
    """
    today_str = date.today().isoformat()                     # "2026-04-05"
    idx = int(hashlib.sha256(today_str.encode()).hexdigest(), 16) % len(ANOMALIES)
    anomaly = ANOMALIES[idx].copy()
    anomaly["date"] = today_str
    anomaly["difficulty_color"] = _DIFFICULTY_COLOR.get(anomaly["difficulty"], "#00FF41")
    return anomaly


@router.get(
    "/daily-anomaly",
    summary="Anomalía del día — misión especial determinista",
)
async def get_daily_anomaly() -> dict:
    """
    Retorna la anomalía diaria actual.
    Determinista por fecha — sin parámetros de entrada.
    """
    return _get_today_anomaly()
