"""
seed_sector_21.py — Sector 21: Entrevistas Técnicas (niveles 174, 176–179)
===========================================================================
Niveles 174, 176–179  |  5 misiones  |  Sector ID = 20

El nivel 175 (Boss Contrato) está en seed_contratos.py.

Temática: algoritmos clásicos de entrevistas técnicas.
Problemas estilo LeetCode/HackerRank adaptados al universo DAKI.
Énfasis en eficiencia (O(n) sobre O(n²)) y claridad de implementación.

Cubre:
- Two Sum con diccionario (O(n))
- Palíndromo sin librerías
- Anagramas con sorted()
- Máximo subarreglo (Kadane)
- BOSS: Agrupar anagramas con defaultdict
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.models.challenge import Challenge, DifficultyTier  # noqa: F401

SECTOR_21 = [
    # ── L174 — Two Sum O(n) ───────────────────────────────────────────────────
    {
        "title": "Dos Suma Eficiente",
        "description": (
            "Implementá `dos_suma(numeros, objetivo)` que encuentra los **índices** de\n"
            "dos números que suman `objetivo`. Debe ser O(n) usando un diccionario.\n\n"
            "Retorna una lista `[i, j]` donde `numeros[i] + numeros[j] == objetivo`.\n\n"
            "Salida esperada:\n"
            "```\n[0, 1]\n[1, 2]\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 21,
        "level_order": 184,
        "base_xp_reward": 400,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 300,
        "challenge_type": "python",
        "phase": "entrevistas",
        "concepts_taught_json": json.dumps(["two_sum", "dict", "enumerate", "O(n)"]),
        "initial_code": (
            "def dos_suma(numeros, objetivo):\n"
            "    vistos = {}\n"
            "    for i, num in enumerate(numeros):\n"
            "        complemento = objetivo - num\n"
            "        if complemento in vistos:\n"
            "            return [vistos[complemento], i]\n"
            "        vistos[num] = i\n"
            "    return []\n"
            "\n"
            "print(dos_suma([2, 7, 11, 15], 9))\n"
            "print(dos_suma([3, 2, 4], 6))\n"
        ),
        "expected_output": "[0, 1]\n[1, 2]",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El protocolo de emparejamiento de DAKI busca pares de señales que se combinan "
            "para alcanzar una frecuencia objetivo. La solución O(n²) es demasiado lenta "
            "para transmisiones en tiempo real. Usá el complemento para eficiencia O(n)."
        ),
        "pedagogical_objective": "Implementar Two Sum en O(n) usando un diccionario como tabla hash para el complemento.",
        "syntax_hint": "complemento = objetivo - num; if complemento in vistos: return [vistos[complemento], i]",
        "theory_content": None,
        "hints_json": json.dumps([
            "Para cada número, el complemento es objetivo - num.",
            "Si el complemento ya lo viste antes (está en vistos), encontraste la pareja.",
            "El diccionario guarda {numero: indice} para recuperar el índice del complemento.",
        ]),
        "strict_match": True,
    },
    # ── L176 — Palíndromo ─────────────────────────────────────────────────────
    {
        "title": "Detector de Palíndromos",
        "description": (
            "Implementá `es_palindromo(texto)` que retorna `True` si el texto es\n"
            "palíndromo (ignorando espacios y mayúsculas), `False` si no.\n\n"
            "Salida esperada:\n"
            "```\nTrue\nFalse\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 21,
        "level_order": 186,
        "base_xp_reward": 400,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 240,
        "challenge_type": "python",
        "phase": "entrevistas",
        "concepts_taught_json": json.dumps(["palindrome", "string_slicing", "lower", "replace"]),
        "initial_code": (
            "def es_palindromo(texto):\n"
            "    limpio = texto.lower().replace(' ', '')\n"
            "    return limpio == limpio[::-1]\n"
            "\n"
            "print(es_palindromo('anita lava la tina'))\n"
            "print(es_palindromo('python'))\n"
        ),
        "expected_output": "True\nFalse",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "Los mensajes cifrados del Nexo a veces usan palíndromos como firma de autenticidad. "
            "El detector debe ignorar espacios y case para verificar la simetría del mensaje."
        ),
        "pedagogical_objective": "Implementar detector de palíndromo usando slicing inverso [::-1] con normalización.",
        "syntax_hint": "limpio = texto.lower().replace(' ', ''); return limpio == limpio[::-1]",
        "theory_content": None,
        "hints_json": json.dumps([
            "Primero normalizá el texto: lower() para ignorar mayúsculas, replace(' ', '') para quitar espacios.",
            "Un palíndromo es igual a su reverso: texto == texto[::-1].",
            "[::-1] es el slicing que invierte un string en Python.",
        ]),
        "strict_match": True,
    },
    # ── L177 — Anagramas ──────────────────────────────────────────────────────
    {
        "title": "Detector de Anagramas",
        "description": (
            "Implementá `son_anagramas(palabra1, palabra2)` que retorna `True`\n"
            "si las dos palabras son anagramas (mismas letras, distinto orden).\n\n"
            "Salida esperada:\n"
            "```\nTrue\nFalse\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 21,
        "level_order": 187,
        "base_xp_reward": 400,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 240,
        "challenge_type": "python",
        "phase": "entrevistas",
        "concepts_taught_json": json.dumps(["anagram", "sorted", "string", "comparison"]),
        "initial_code": (
            "def son_anagramas(palabra1, palabra2):\n"
            "    return sorted(palabra1.lower()) == sorted(palabra2.lower())\n"
            "\n"
            "print(son_anagramas('listen', 'silent'))\n"
            "print(son_anagramas('hello', 'world'))\n"
        ),
        "expected_output": "True\nFalse",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "Los operadores de DAKI reciben mensajes codificados como anagramas. "
            "Dos palabras son anagramas si contienen exactamente las mismas letras. "
            "sorted() ordena las letras para comparar en igualdad."
        ),
        "pedagogical_objective": "Detectar anagramas usando sorted() para comparar frecuencia de letras.",
        "syntax_hint": "sorted('listen') == sorted('silent') → compará listas de letras ordenadas.",
        "theory_content": None,
        "hints_json": json.dumps([
            "Dos palabras son anagramas si tienen las mismas letras en cualquier orden.",
            "sorted('listen') retorna ['e', 'i', 'l', 'n', 's', 't'] — igual que sorted('silent').",
            "Normalizá con .lower() para ignorar mayúsculas antes de sorted().",
        ]),
        "strict_match": True,
    },
    # ── L178 — Máximo subarreglo (Kadane) ─────────────────────────────────────
    {
        "title": "Máximo Subarreglo",
        "description": (
            "Implementá `max_subarray(numeros)` usando el **algoritmo de Kadane** (O(n))\n"
            "para encontrar la suma máxima de un subarreglo contiguo.\n\n"
            "Salida esperada:\n"
            "```\n6\n15\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "hard",
        "sector_id": 21,
        "level_order": 188,
        "base_xp_reward": 475,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 360,
        "challenge_type": "python",
        "phase": "entrevistas",
        "concepts_taught_json": json.dumps(["kadane", "dynamic_programming", "max_subarray", "O(n)"]),
        "initial_code": (
            "def max_subarray(numeros):\n"
            "    max_actual = numeros[0]\n"
            "    max_global = numeros[0]\n"
            "\n"
            "    for num in numeros[1:]:\n"
            "        max_actual = max(num, max_actual + num)\n"
            "        max_global = max(max_global, max_actual)\n"
            "\n"
            "    return max_global\n"
            "\n"
            "print(max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]))\n"
            "print(max_subarray([1, 2, 3, 4, 5]))\n"
        ),
        "expected_output": "6\n15",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El analizador de señales de DAKI busca la secuencia de valores consecutivos "
            "con mayor energía total. El algoritmo de Kadane resuelve esto en O(n) "
            "usando programación dinámica: en cada paso decidís si continuar la secuencia "
            "o empezar una nueva desde el elemento actual."
        ),
        "pedagogical_objective": "Implementar el algoritmo de Kadane para máximo subarreglo contiguo en O(n).",
        "syntax_hint": "max_actual = max(num, max_actual + num) — ¿es mejor empezar de nuevo o continuar?",
        "theory_content": None,
        "hints_json": json.dumps([
            "En cada posición, decidís: ¿sumo este elemento a la secuencia actual o empiezo nueva?",
            "max_actual = max(num, max_actual + num) — si max_actual + num < num, conviene empezar de nuevo.",
            "max_global guarda el mejor resultado histórico visto hasta ahora.",
        ]),
        "strict_match": True,
    },
    # ── L179 — BOSS: Agrupar anagramas ────────────────────────────────────────
    {
        "title": "NEXO-FINAL: Agrupador de Anagramas",
        "description": (
            "**MISIÓN BOSS** — Implementá `agrupar_anagramas(palabras)` que agrupa\n"
            "una lista de palabras por sus anagramas usando `defaultdict`.\n\n"
            "Retorna una lista de grupos. Imprimí cada grupo ordenado.\n\n"
            "Salida esperada:\n"
            "```\n['ate', 'eat', 'tea']\n['bat']\n['nat', 'tan']\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "hard",
        "sector_id": 21,
        "level_order": 189,
        "base_xp_reward": 600,
        "is_project": False,
        "is_phase_boss": True,
        "telemetry_goal_time": 420,
        "challenge_type": "python",
        "phase": "entrevistas",
        "concepts_taught_json": json.dumps(["defaultdict", "groupby", "anagram", "tuple", "sorted"]),
        "initial_code": (
            "from collections import defaultdict\n"
            "\n"
            "def agrupar_anagramas(palabras):\n"
            "    grupos = defaultdict(list)\n"
            "    for palabra in palabras:\n"
            "        clave = tuple(sorted(palabra))\n"
            "        grupos[clave].append(palabra)\n"
            "    return list(grupos.values())\n"
            "\n"
            "resultado = agrupar_anagramas(['eat', 'tea', 'tan', 'ate', 'nat', 'bat'])\n"
            "for grupo in sorted(resultado, key=lambda g: g[0]):\n"
            "    print(sorted(grupo))\n"
        ),
        "expected_output": "['ate', 'eat', 'tea']\n['bat']\n['nat', 'tan']",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "La misión final del Sector 21: el clasificador de frecuencias del Nexo "
            "debe agrupar transmisiones que comparten la misma 'huella espectral' (sus anagramas). "
            "defaultdict(list) permite acumular grupos sin verificar si la clave existe. "
            "tuple(sorted(palabra)) crea la huella única de cada transmisión."
        ),
        "pedagogical_objective": "Usar defaultdict + tuple(sorted()) como clave para agrupar elementos por equivalencia de anagrama.",
        "syntax_hint": "clave = tuple(sorted(palabra)); grupos[clave].append(palabra)",
        "theory_content": None,
        "hints_json": json.dumps([
            "La clave de cada grupo es la firma de sus letras: tuple(sorted('eat')) == tuple(sorted('tea')).",
            "defaultdict(list) crea automáticamente una lista vacía para claves nuevas.",
            "Para ordenar la salida: sorted(resultado, key=lambda g: g[0]) ordena los grupos por su primer elemento.",
        ]),
        "strict_match": True,
    },
]
