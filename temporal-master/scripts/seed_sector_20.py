"""
seed_sector_20.py — Sector 20: Modo Debug (niveles 166–173)
============================================================
Niveles 166–173  |  8 misiones  |  Sector ID = 19

challenge_type = "debug": código con bugs intencionales que el operador debe corregir.
Cada misión presenta código roto; el operador corrige y ejecuta hasta lograr el output esperado.

Tipos de bugs cubiertos:
- NameError (variable mal nombrada)
- TypeError (concatenar str + int)
- Off-by-one (range incorrecto)
- Missing return
- KeyError (clave inexistente)
- Acumulador roto (reset dentro del loop)
- Condición invertida
- BOSS: IndexError + error de lógica combinados
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.models.challenge import Challenge, DifficultyTier  # noqa: F401

SECTOR_20 = [
    # ── L166 — NameError ──────────────────────────────────────────────────────
    {
        "title": "Variable Perdida",
        "description": (
            "El siguiente código tiene un **bug**: usa el nombre de variable incorrecto.\n"
            "Encontrá y corregí el error para que imprima el promedio.\n\n"
            "Salida esperada:\n"
            "```\n20.0\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "easy",
        "sector_id": 20,
        "level_order": 176,
        "base_xp_reward": 275,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 180,
        "challenge_type": "debug",
        "phase": "debug",
        "concepts_taught_json": json.dumps(["NameError", "variables", "debug"]),
        "initial_code": (
            "def calcular_promedio(numeros):\n"
            "    total = sum(numeros)\n"
            "    promedio = total / len(numeros)\n"
            "    return resultado\n"
            "\n"
            "print(calcular_promedio([10, 20, 30]))\n"
        ),
        "expected_output": "20.0",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El sistema de análisis de DAKI tiene un error de naming. "
            "Un operador anterior usó el nombre de variable incorrecto en el return. "
            "Encontrá la inconsistencia y corregila."
        ),
        "pedagogical_objective": "Identificar y corregir NameError causado por nombre de variable incorrecto.",
        "syntax_hint": "El return usa un nombre distinto al que definiste para almacenar el promedio.",
        "theory_content": None,
        "hints_json": json.dumps([
            "NameError: name 'resultado' is not defined — ¿eso te dice algo?",
            "La función calcula el promedio y lo guarda en 'promedio', pero el return dice otra cosa.",
            "Cambiá 'resultado' por 'promedio' en el return.",
        ]),
        "strict_match": True,
    },
    # ── L167 — TypeError ──────────────────────────────────────────────────────
    {
        "title": "Tipos en Conflicto",
        "description": (
            "El siguiente código lanza `TypeError` al intentar concatenar tipos incompatibles.\n"
            "Corregí el error sin cambiar la lógica de la función.\n\n"
            "Salida esperada:\n"
            "```\nOperador NEXO nivel 7\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "easy",
        "sector_id": 20,
        "level_order": 177,
        "base_xp_reward": 275,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 180,
        "challenge_type": "debug",
        "phase": "debug",
        "concepts_taught_json": json.dumps(["TypeError", "str_conversion", "debug"]),
        "initial_code": (
            "def describir_nivel(nombre, nivel):\n"
            "    return 'Operador ' + nombre + ' nivel ' + nivel\n"
            "\n"
            "print(describir_nivel('NEXO', 7))\n"
        ),
        "expected_output": "Operador NEXO nivel 7",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El generador de reportes de DAKI falla al combinar texto con números. "
            "Python no permite sumar str con int directamente. Corregí la conversión."
        ),
        "pedagogical_objective": "Identificar TypeError por concatenación str + int y corregir con str() o f-string.",
        "syntax_hint": "No se puede sumar str + int. Usá str(nivel) o reescribí con f-string.",
        "theory_content": None,
        "hints_json": json.dumps([
            "TypeError: can only concatenate str (not 'int') to str.",
            "Convertí 'nivel' a string con str(nivel) antes de concatenar.",
            "O simplificá todo: return f'Operador {nombre} nivel {nivel}'",
        ]),
        "strict_match": True,
    },
    # ── L168 — Off-by-one ─────────────────────────────────────────────────────
    {
        "title": "Límite Incorrecto",
        "description": (
            "El código genera una lista de niveles pero **le falta el último elemento**.\n"
            "Corregí el range para incluir el número final.\n\n"
            "Salida esperada:\n"
            "```\n[1, 2, 3, 4, 5]\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "easy",
        "sector_id": 20,
        "level_order": 178,
        "base_xp_reward": 275,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 200,
        "challenge_type": "debug",
        "phase": "debug",
        "concepts_taught_json": json.dumps(["off_by_one", "range", "debug"]),
        "initial_code": (
            "def listar_niveles(inicio, fin):\n"
            "    niveles = []\n"
            "    for i in range(inicio, fin):\n"
            "        niveles.append(i)\n"
            "    return niveles\n"
            "\n"
            "print(listar_niveles(1, 5))\n"
        ),
        "expected_output": "[1, 2, 3, 4, 5]",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El mapeador de sectores de DAKI siempre pierde el último nodo. "
            "Es el error más clásico en programación: off-by-one. "
            "range(1, 5) va de 1 a 4. Corregí el límite."
        ),
        "pedagogical_objective": "Identificar y corregir error off-by-one en range() usando fin+1.",
        "syntax_hint": "range(inicio, fin) excluye 'fin'. Necesitás range(inicio, fin + 1).",
        "theory_content": None,
        "hints_json": json.dumps([
            "range(1, 5) genera [1, 2, 3, 4] — el 5 no está incluido.",
            "range en Python es exclusivo en el límite superior.",
            "Cambiá range(inicio, fin) por range(inicio, fin + 1).",
        ]),
        "strict_match": True,
    },
    # ── L169 — Missing return ─────────────────────────────────────────────────
    {
        "title": "Sin Retorno",
        "description": (
            "La función calcula correctamente pero **no retorna nada**.\n"
            "Agregá el `return` que falta.\n\n"
            "Salida esperada:\n"
            "```\n42\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "easy",
        "sector_id": 20,
        "level_order": 179,
        "base_xp_reward": 275,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 150,
        "challenge_type": "debug",
        "phase": "debug",
        "concepts_taught_json": json.dumps(["return", "None", "debug"]),
        "initial_code": (
            "def duplicar(numero):\n"
            "    resultado = numero * 2\n"
            "\n"
            "print(duplicar(21))\n"
        ),
        "expected_output": "42",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El multiplicador de DAKI calcula el doble pero lo descarta en el vacío. "
            "Una función sin return devuelve None. Buscá la línea que falta."
        ),
        "pedagogical_objective": "Identificar que una función sin return devuelve None e insertar el return correcto.",
        "syntax_hint": "La función calcula 'resultado' pero nunca lo retorna. Agregá return resultado.",
        "theory_content": None,
        "hints_json": json.dumps([
            "print(duplicar(21)) imprime 'None' porque la función no retorna nada.",
            "Todo el cálculo está correcto, solo falta la última línea.",
            "Agregá 'return resultado' antes de que la función termine.",
        ]),
        "strict_match": True,
    },
    # ── L170 — KeyError ───────────────────────────────────────────────────────
    {
        "title": "Clave Inexistente",
        "description": (
            "El código intenta acceder a una clave que **no existe** en el diccionario.\n"
            "Corregí el nombre de clave para obtener el valor correcto.\n\n"
            "Salida esperada:\n"
            "```\nNEXO\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "easy",
        "sector_id": 20,
        "level_order": 180,
        "base_xp_reward": 275,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 150,
        "challenge_type": "debug",
        "phase": "debug",
        "concepts_taught_json": json.dumps(["KeyError", "dict", "debug"]),
        "initial_code": (
            "datos = {'nombre': 'NEXO', 'nivel': 7, 'sector': 19}\n"
            "print(datos['name'])\n"
        ),
        "expected_output": "NEXO",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "La base de datos de operadores de DAKI usa claves en español, "
            "pero alguien mezcló idiomas. El sistema lanza KeyError. Corregí la clave."
        ),
        "pedagogical_objective": "Identificar KeyError por nombre de clave incorrecto en un diccionario.",
        "syntax_hint": "Mirá las claves disponibles en el diccionario y compará con la que se usa.",
        "theory_content": None,
        "hints_json": json.dumps([
            "KeyError: 'name' — la clave 'name' no existe en el diccionario.",
            "Las claves disponibles son: 'nombre', 'nivel', 'sector'.",
            "Cambiá datos['name'] por datos['nombre'].",
        ]),
        "strict_match": True,
    },
    # ── L171 — Acumulador roto ────────────────────────────────────────────────
    {
        "title": "Acumulador Reseteado",
        "description": (
            "La función debería sumar todos los números de la lista, pero **siempre retorna el último**.\n"
            "Encontrá por qué el acumulador se reinicia y corregilo.\n\n"
            "Salida esperada:\n"
            "```\n15\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 20,
        "level_order": 181,
        "base_xp_reward": 325,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 220,
        "challenge_type": "debug",
        "phase": "debug",
        "concepts_taught_json": json.dumps(["accumulator", "loop", "scope", "debug"]),
        "initial_code": (
            "def sumar_lista(numeros):\n"
            "    for numero in numeros:\n"
            "        total = 0\n"
            "        total += numero\n"
            "    return total\n"
            "\n"
            "print(sumar_lista([1, 2, 3, 4, 5]))\n"
        ),
        "expected_output": "15",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El sumador de XP de DAKI tiene un problema sutil: "
            "reinicia el contador en cada iteración del loop. "
            "El acumulador debe inicializarse UNA sola vez, antes del loop."
        ),
        "pedagogical_objective": "Identificar que un acumulador inicializado dentro del loop se resetea en cada iteración.",
        "syntax_hint": "total = 0 está dentro del loop — se reinicia en cada vuelta. Movelo antes del for.",
        "theory_content": None,
        "hints_json": json.dumps([
            "El código imprime 5 (solo el último número) porque total se resetea en cada iteración.",
            "total = 0 debe estar ANTES del for, no dentro.",
            "Mové 'total = 0' una línea hacia arriba, fuera del loop.",
        ]),
        "strict_match": True,
    },
    # ── L172 — Condición invertida ────────────────────────────────────────────
    {
        "title": "Lógica Invertida",
        "description": (
            "La función `es_mayor_de_edad` **retorna lo opuesto de lo correcto**.\n"
            "Corregí la condición para que funcione como se espera.\n\n"
            "Salida esperada:\n"
            "```\nTrue\nFalse\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 20,
        "level_order": 182,
        "base_xp_reward": 325,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 200,
        "challenge_type": "debug",
        "phase": "debug",
        "concepts_taught_json": json.dumps(["logic_error", "boolean", "conditions", "debug"]),
        "initial_code": (
            "def es_mayor_de_edad(edad):\n"
            "    if edad < 18:\n"
            "        return True\n"
            "    return False\n"
            "\n"
            "print(es_mayor_de_edad(20))\n"
            "print(es_mayor_de_edad(15))\n"
        ),
        "expected_output": "True\nFalse",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El verificador de acceso de DAKI tiene la lógica al revés: "
            "bloquea a los adultos y deja pasar a los menores. "
            "Es el bug más peligroso: el código corre sin errores pero hace lo incorrecto."
        ),
        "pedagogical_objective": "Identificar error de lógica (condición invertida) que no lanza excepción pero produce resultado incorrecto.",
        "syntax_hint": "edad < 18 retorna True para menores. Pero la función se llama 'es_mayor_de_edad'...",
        "theory_content": None,
        "hints_json": json.dumps([
            "El código no lanza ningún error, simplemente produce el resultado incorrecto.",
            "es_mayor_de_edad(20) debería ser True — una persona de 20 años ES mayor de edad.",
            "Cambiá 'edad < 18' por 'edad >= 18'.",
        ]),
        "strict_match": True,
    },
    # ── L173 — BOSS: IndexError + lógica ──────────────────────────────────────
    {
        "title": "NEXO-DEBUG: Análisis de Equipo",
        "description": (
            "**MISIÓN BOSS** — El analizador de equipo tiene **dos bugs combinados**:\n"
            "1. Un `IndexError` por límite de range incorrecto\n"
            "2. El resultado imprime los datos de otro operador\n\n"
            "Corregí ambos errores.\n\n"
            "Salida esperada:\n"
            "```\nMejor operador: BETA con 2300 XP\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "hard",
        "sector_id": 20,
        "level_order": 183,
        "base_xp_reward": 500,
        "is_project": False,
        "is_phase_boss": True,
        "telemetry_goal_time": 360,
        "challenge_type": "debug",
        "phase": "debug",
        "concepts_taught_json": json.dumps(["IndexError", "logic_error", "loop", "dict", "debug"]),
        "initial_code": (
            "def analizar_equipo(operadores):\n"
            "    mejor = operadores[0]\n"
            "    for i in range(1, len(operadores) + 1):\n"
            "        if operadores[i]['xp'] > mejor['xp']:\n"
            "            mejor = operadores[i]\n"
            "    return f\"Mejor operador: {mejor['nombre']} con {mejor['xp']} XP\"\n"
            "\n"
            "equipo = [\n"
            "    {'nombre': 'ALPHA', 'xp': 1500},\n"
            "    {'nombre': 'BETA', 'xp': 2300},\n"
            "    {'nombre': 'GAMMA', 'xp': 1800},\n"
            "]\n"
            "print(analizar_equipo(equipo))\n"
        ),
        "expected_output": "Mejor operador: BETA con 2300 XP",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El clasificador de élite de DAKI está en modo crítico. "
            "Dos bugs combinados: uno revienta el índice, otro confunde al ganador. "
            "Encontrá y corregí ambos para que la misión quede registrada correctamente."
        ),
        "pedagogical_objective": "Identificar y corregir IndexError por range incorrecto más error de lógica en comparación de diccionarios.",
        "syntax_hint": "range(1, len(operadores) + 1) va un paso más allá del último índice válido.",
        "theory_content": None,
        "hints_json": json.dumps([
            "Bug 1: range(1, len(operadores) + 1) — el último valor es len(operadores), que no existe como índice.",
            "Los índices válidos van de 0 a len(operadores)-1. Usá range(1, len(operadores)).",
            "Bug 2: una vez corregido el IndexError, verificá que el output sea el operador con más XP.",
        ]),
        "strict_match": True,
    },
]
