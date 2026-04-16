"""
seed_sector_12.py — Sector 12: Refuerzo Táctico (niveles 101–110)
==================================================================
Niveles 101–110  |  10 misiones  |  Sector ID = 11

Temática técnica: práctica mixta de conceptos S1-S10.
Algoritmos clásicos, manipulación de strings, listas, dicts y OOP básico.

Lore DAKI: "El Operador consolida lo aprendido y demuestra versatilidad táctica."

Nivel 110 (Boss): Analizador de Texto — estadísticas completas de un corpus.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.models.challenge import Challenge, DifficultyTier  # noqa: F401

SECTOR_12 = [
    # ── L101 — Caesar Cipher ─────────────────────────────────────────────────
    {
        "title": "Cifrado César",
        "description": (
            "El cifrado César desplaza cada letra del alfabeto N posiciones.\n\n"
            "Implementá la función `cifrar(texto, desplazamiento)` que recibe un\n"
            "string en mayúsculas y un entero, y retorna el texto cifrado.\n"
            "Solo cifrá letras A-Z; los espacios y números quedan igual.\n\n"
            "Ejemplos:\n"
            "```\ncifrar('HOLA', 3)   → 'KROD'\n"
            "cifrar('NEXO', 13)  → 'ARKB'\n```"
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "easy",
        "sector_id": 12,
        "level_order": 111,
        "base_xp_reward": 175,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 180,
        "challenge_type": "python",
        "phase": "refuerzo",
        "concepts_taught_json": json.dumps(["string", "modulo", "ord", "chr", "loop"]),
        "initial_code": (
            "def cifrar(texto, desplazamiento):\n"
            "    pass  # TU CÓDIGO AQUÍ\n"
            "\n"
            "print(cifrar('HOLA', 3))\n"
            "print(cifrar('NEXO', 13))\n"
        ),
        "expected_output": "KROD\nARKB",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "DAKI interceptó transmisiones cifradas del enemigo. "
            "El protocolo usa un cifrado César clásico. "
            "Implementá el módulo de cifrado para que el sistema pueda encriptar mensajes de campo."
        ),
        "pedagogical_objective": "Aplicar ord(), chr() y módulo aritmético para rotar caracteres en un alfabeto.",
        "syntax_hint": "nuevo = (ord(char) - 65 + desplazamiento) % 26 + 65",
        "theory_content": None,
        "hints_json": json.dumps([
            "ord('A')=65, ord('Z')=90. Restá 65, sumá el desplazamiento, hacé módulo 26, sumá 65 de nuevo.",
            "El truco del módulo 26 hace que Z+1 vuelva a A: (25+1)%26=0 → 'A'.",
            "Solución: nuevo = (ord(char) - 65 + desplazamiento) % 26 + 65",
        ]),
        "strict_match": True,
    },
    # ── L102 — Contar Vocales ────────────────────────────────────────────────
    {
        "title": "Escáner de Vocales",
        "description": (
            "Escribí la función `contar_vocales(texto)` que retorna un dict\n"
            "con la frecuencia de cada vocal (a, e, i, o, u) en el texto.\n"
            "Ignorá mayúsculas/minúsculas. Solo incluí vocales presentes.\n\n"
            "Ejemplo:\n"
            "```\ncontar_vocales('Hola Mundo') → {'o': 2, 'a': 1, 'u': 1}\n```"
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "easy",
        "sector_id": 12,
        "level_order": 112,
        "base_xp_reward": 175,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 150,
        "challenge_type": "python",
        "phase": "refuerzo",
        "concepts_taught_json": json.dumps(["dict", "string", "loop", "lower"]),
        "initial_code": (
            "def contar_vocales(texto):\n"
            "    pass  # TU CÓDIGO AQUÍ\n"
            "\n"
            "print(contar_vocales('Hola Mundo'))\n"
        ),
        "expected_output": "{'o': 2, 'a': 1, 'u': 1}",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El analizador fonético de DAKI necesita identificar patrones de vocales "
            "en transmisiones de voz codificadas. Cada vocal tiene una frecuencia de onda distinta."
        ),
        "pedagogical_objective": "Construir un dict de frecuencias usando dict.get() con valor por defecto.",
        "syntax_hint": "resultado[char] = resultado.get(char, 0) + 1",
        "theory_content": None,
        "hints_json": json.dumps([
            "Convertí el texto a minúsculas antes de iterar con .lower().",
            "dict.get(key, 0) retorna 0 si la clave no existe — perfecto para contadores.",
            "Solución: resultado[char] = resultado.get(char, 0) + 1",
        ]),
        "strict_match": True,
    },
    # ── L103 — Invertir Palabras ─────────────────────────────────────────────
    {
        "title": "Inversión de Transmisión",
        "description": (
            "Escribí la función `invertir_palabras(frase)` que invierte el orden\n"
            "de las palabras en una frase, pero mantiene cada palabra igual.\n\n"
            "Ejemplo:\n"
            "```\ninvertir_palabras('DAKI protege el Nexo') → 'Nexo el protege DAKI'\n```"
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "easy",
        "sector_id": 12,
        "level_order": 113,
        "base_xp_reward": 175,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 120,
        "challenge_type": "python",
        "phase": "refuerzo",
        "concepts_taught_json": json.dumps(["string", "split", "join", "slice"]),
        "initial_code": (
            "def invertir_palabras(frase):\n"
            "    pass  # TU CÓDIGO AQUÍ\n"
            "\n"
            "print(invertir_palabras('DAKI protege el Nexo'))\n"
        ),
        "expected_output": "Nexo el protege DAKI",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "Las transmisiones enemigas llegaron invertidas por un fallo del transmisor. "
            "DAKI necesita reordenar las palabras para reconstruir el mensaje original."
        ),
        "pedagogical_objective": "Combinar split(), slicing inverso [::-1] y join() para manipular palabras.",
        "syntax_hint": "' '.join(frase.split()[::-1])",
        "theory_content": None,
        "hints_json": json.dumps([
            "split() sin argumentos divide por espacios y elimina espacios extra.",
            "[::-1] invierte cualquier lista o string.",
            "Solución: return ' '.join(frase.split()[::-1])",
        ]),
        "strict_match": True,
    },
    # ── L104 — Segundo Máximo ────────────────────────────────────────────────
    {
        "title": "Segundo en Comando",
        "description": (
            "Escribí la función `segundo_maximo(numeros)` que retorna el\n"
            "segundo valor más grande de la lista.\n"
            "Si todos los elementos son iguales, retorná None.\n\n"
            "Ejemplos:\n"
            "```\nsegundo_maximo([3, 1, 4, 1, 5, 9, 2, 6]) → 6\n"
            "segundo_maximo([7, 7, 7])                    → None\n```"
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "easy",
        "sector_id": 12,
        "level_order": 114,
        "base_xp_reward": 180,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 150,
        "challenge_type": "python",
        "phase": "refuerzo",
        "concepts_taught_json": json.dumps(["list", "sorted", "set", "slice"]),
        "initial_code": (
            "def segundo_maximo(numeros):\n"
            "    pass  # TU CÓDIGO AQUÍ\n"
            "\n"
            "print(segundo_maximo([3, 1, 4, 1, 5, 9, 2, 6]))\n"
            "print(segundo_maximo([7, 7, 7]))\n"
        ),
        "expected_output": "6\nNone",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El sistema de rankings tácticos de DAKI necesita identificar al operador "
            "en segunda posición — el que tomaría el comando si el líder cae."
        ),
        "pedagogical_objective": "Usar set() para eliminar duplicados y sorted() con reverse=True para ordenar descendente.",
        "syntax_hint": "sorted(set(numeros), reverse=True)[1]",
        "theory_content": None,
        "hints_json": json.dumps([
            "set() elimina duplicados. Si todos son iguales, set() tiene 1 elemento.",
            "sorted(set(numeros), reverse=True) ordena de mayor a menor sin repetidos.",
            "Solución: unicos = sorted(set(numeros), reverse=True); return unicos[1] if len(unicos)>=2 else None",
        ]),
        "strict_match": True,
    },
    # ── L105 — Número Primo ──────────────────────────────────────────────────
    {
        "title": "Detector de Primos",
        "description": (
            "Escribí la función `es_primo(n)` que retorna True si n es primo,\n"
            "False en caso contrario. Un número primo es divisible solo por 1 y por sí mismo.\n\n"
            "Luego imprimí todos los primos entre 1 y 30 en una línea separada.\n\n"
            "Salida esperada:\n"
            "```\n2 3 5 7 11 13 17 19 23 29\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 12,
        "level_order": 115,
        "base_xp_reward": 200,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 200,
        "challenge_type": "python",
        "phase": "refuerzo",
        "concepts_taught_json": json.dumps(["function", "loop", "modulo", "boolean"]),
        "initial_code": (
            "def es_primo(n):\n"
            "    pass  # TU CÓDIGO AQUÍ\n"
            "\n"
            "primos = [str(n) for n in range(1, 31) if es_primo(n)]\n"
            "print(' '.join(primos))\n"
        ),
        "expected_output": "2 3 5 7 11 13 17 19 23 29",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "Los códigos de acceso del Nexo se generan a partir de números primos. "
            "DAKI necesita un detector confiable para validar cada código antes de activarlo."
        ),
        "pedagogical_objective": "Implementar la prueba de primalidad eficiente con raíz cuadrada como límite.",
        "syntax_hint": "for i in range(2, int(n**0.5) + 1): if n % i == 0: return False",
        "theory_content": None,
        "hints_json": json.dumps([
            "Solo necesitás probar divisores hasta sqrt(n). Si n=36, sqrt=6; si no encontrás divisor hasta 6, es primo.",
            "n**0.5 = sqrt(n). Usá int(n**0.5)+1 como límite del range.",
            "Solución: for i in range(2, int(n**0.5)+1): if n%i==0: return False; return True",
        ]),
        "strict_match": True,
    },
    # ── L106 — Suma de Dígitos ───────────────────────────────────────────────
    {
        "title": "Suma de Dígitos",
        "description": (
            "Escribí la función `suma_digitos(n)` que suma todos los dígitos de\n"
            "un número entero positivo de forma recursiva.\n\n"
            "Ejemplos:\n"
            "```\nsuma_digitos(1234) → 10\n"
            "suma_digitos(9999) → 36\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 12,
        "level_order": 116,
        "base_xp_reward": 200,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 180,
        "challenge_type": "python",
        "phase": "refuerzo",
        "concepts_taught_json": json.dumps(["recursion", "modulo", "floor_division"]),
        "initial_code": (
            "def suma_digitos(n):\n"
            "    pass  # TU CÓDIGO AQUÍ\n"
            "\n"
            "print(suma_digitos(1234))\n"
            "print(suma_digitos(9999))\n"
        ),
        "expected_output": "10\n36",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El sistema de checksum de DAKI valida integridad sumando los dígitos de cada paquete. "
            "Un número de 4 dígitos con suma > 30 indica datos corruptos."
        ),
        "pedagogical_objective": "Aplicar recursión con caso base (n<10) y caso recursivo usando módulo y división entera.",
        "syntax_hint": "return n % 10 + suma_digitos(n // 10)",
        "theory_content": None,
        "hints_json": json.dumps([
            "n % 10 extrae el último dígito. n // 10 elimina el último dígito.",
            "Caso base: si n<10 (un solo dígito), retorná n directamente.",
            "Solución: return n % 10 + suma_digitos(n // 10)",
        ]),
        "strict_match": True,
    },
    # ── L107 — Frecuencia de Palabras ────────────────────────────────────────
    {
        "title": "Frecuencia de Palabras",
        "description": (
            "Escribí la función `frecuencia(texto)` que retorna un dict con la\n"
            "frecuencia de cada palabra en el texto (ignorando mayúsculas).\n"
            "Las palabras están separadas por espacios.\n\n"
            "Luego imprimí las 3 palabras más frecuentes ordenadas de mayor a menor.\n\n"
            "Texto: `'nexo nexo daki daki daki operador nexo'`\n\n"
            "Salida esperada:\n"
            "```\ndaki: 3\nnexo: 3\noperador: 1\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 12,
        "level_order": 117,
        "base_xp_reward": 210,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 200,
        "challenge_type": "python",
        "phase": "refuerzo",
        "concepts_taught_json": json.dumps(["dict", "sorted", "lambda", "string"]),
        "initial_code": (
            "def frecuencia(texto):\n"
            "    pass  # TU CÓDIGO AQUÍ\n"
            "\n"
            "texto = 'nexo nexo daki daki daki operador nexo'\n"
            "freq = frecuencia(texto)\n"
            "top3 = sorted(freq.items(), key=lambda x: (-x[1], x[0]))[:3]\n"
            "for palabra, count in top3:\n"
            "    print(f'{palabra}: {count}')\n"
        ),
        "expected_output": "daki: 3\nnexo: 3\noperador: 1",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "DAKI analiza comunicaciones para detectar palabras clave repetidas. "
            "Las palabras más frecuentes revelan el tema central de cada transmisión."
        ),
        "pedagogical_objective": "Combinar dict de frecuencias con sorted() y lambda para ordenar por múltiples criterios.",
        "syntax_hint": "sorted(freq.items(), key=lambda x: (-x[1], x[0]))",
        "theory_content": None,
        "hints_json": json.dumps([
            "Usá -x[1] como primera clave para ordenar frecuencia descendente, x[0] para alfabético en empates.",
            "sorted(dict.items()) retorna lista de tuplas (clave, valor) ordenables.",
            "Solución: sorted(freq.items(), key=lambda x: (-x[1], x[0]))[:3]",
        ]),
        "strict_match": True,
    },
    # ── L108 — Clase Cuenta Bancaria ─────────────────────────────────────────
    {
        "title": "Cuenta Táctica",
        "description": (
            "Implementá la clase `CuentaTactica` con:\n"
            "- `__init__(self, titular, saldo_inicial)`: inicializa la cuenta\n"
            "- `depositar(monto)`: suma al saldo (solo si monto > 0)\n"
            "- `retirar(monto)`: resta del saldo si hay fondos suficientes;\n"
            "  imprimí `'FONDOS INSUFICIENTES'` si no alcanza\n"
            "- `saldo()`: retorna el saldo actual\n\n"
            "Salida esperada para el código dado:\n"
            "```\n1500\nFONDOS INSUFICIENTES\n1200\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 12,
        "level_order": 118,
        "base_xp_reward": 220,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 240,
        "challenge_type": "python",
        "phase": "refuerzo",
        "concepts_taught_json": json.dumps(["class", "__init__", "methods", "self"]),
        "initial_code": (
            "class CuentaTactica:\n"
            "    def __init__(self, titular, saldo_inicial):\n"
            "        pass  # TU CÓDIGO AQUÍ\n"
            "\n"
            "    def depositar(self, monto):\n"
            "        pass\n"
            "\n"
            "    def retirar(self, monto):\n"
            "        pass\n"
            "\n"
            "    def saldo(self):\n"
            "        pass\n"
            "\n"
            "cuenta = CuentaTactica('Operador-7', 1000)\n"
            "cuenta.depositar(500)\n"
            "print(cuenta.saldo())\n"
            "cuenta.retirar(2000)\n"
            "cuenta.retirar(300)\n"
            "print(cuenta.saldo())\n"
        ),
        "expected_output": "1500\nFONDOS INSUFICIENTES\n1200",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "Los operadores del Nexo manejan créditos tácticos para comprar mejoras y equipamiento. "
            "El sistema de cuentas debe ser robusto — ningún operador puede quedar en números negativos."
        ),
        "pedagogical_objective": "Diseñar una clase con estado interno, validaciones en métodos y encapsulamiento básico.",
        "syntax_hint": "if monto > self._saldo: print('FONDOS INSUFICIENTES') else: self._saldo -= monto",
        "theory_content": None,
        "hints_json": json.dumps([
            "El saldo inicial se guarda en __init__ como self._saldo = saldo_inicial.",
            "En retirar(), primero verificá si monto > self._saldo antes de restar.",
            "El método saldo() simplemente retorna self._saldo.",
        ]),
        "strict_match": True,
    },
    # ── L109 — Búsqueda Binaria ──────────────────────────────────────────────
    {
        "title": "Protocolo Búsqueda Binaria",
        "description": (
            "Implementá `busqueda_binaria(lista, objetivo)` que busca `objetivo`\n"
            "en una lista ORDENADA y retorna su índice, o -1 si no existe.\n"
            "No usés el método index() — implementá el algoritmo manualmente.\n\n"
            "Ejemplos:\n"
            "```\nbusqueda_binaria([1,3,5,7,9,11,13], 7)  → 3\n"
            "busqueda_binaria([1,3,5,7,9,11,13], 6)  → -1\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 12,
        "level_order": 119,
        "base_xp_reward": 225,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 240,
        "challenge_type": "python",
        "phase": "refuerzo",
        "concepts_taught_json": json.dumps(["algorithm", "while", "binary_search", "list"]),
        "initial_code": (
            "def busqueda_binaria(lista, objetivo):\n"
            "    pass  # TU CÓDIGO AQUÍ\n"
            "\n"
            "print(busqueda_binaria([1,3,5,7,9,11,13], 7))\n"
            "print(busqueda_binaria([1,3,5,7,9,11,13], 6))\n"
        ),
        "expected_output": "3\n-1",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El sistema de detección de DAKI necesita encontrar amenazas en listas ordenadas "
            "de registros de actividad. La búsqueda binaria es O(log n) — "
            "esencial cuando hay millones de registros."
        ),
        "pedagogical_objective": "Implementar búsqueda binaria con dos punteros izq/der y el invariante izq <= der.",
        "syntax_hint": "medio = (izq + der) // 2; si lista[medio] < objetivo: izq = medio + 1",
        "theory_content": None,
        "hints_json": json.dumps([
            "Mantenés dos índices: izq y der. El medio es (izq+der)//2.",
            "Si lista[medio] < objetivo, el objetivo está a la derecha: izq = medio + 1.",
            "Si lista[medio] > objetivo, está a la izquierda: der = medio - 1.",
        ]),
        "strict_match": True,
    },
    # ── L110 — BOSS: Analizador de Texto ────────────────────────────────────
    {
        "title": "NEXO-11: El Analizador de Transmisiones",
        "description": (
            "BOSS DEL SECTOR — Análisis completo de texto.\n\n"
            "Dado el texto: `'el nexo protege el sistema el operador activa el nexo'`\n\n"
            "Imprimí (en ese orden):\n"
            "1. Total de palabras\n"
            "2. Total de palabras únicas\n"
            "3. La palabra más frecuente (si hay empate, la primera alfabéticamente)\n"
            "4. La longitud promedio de las palabras (redondeada a 1 decimal)\n\n"
            "Salida esperada:\n"
            "```\nPalabras: 10\nUnicas: 6\nMas frecuente: el\nLongitud media: 3.5\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "hard",
        "sector_id": 12,
        "level_order": 120,
        "base_xp_reward": 500,
        "is_project": False,
        "is_phase_boss": True,
        "telemetry_goal_time": 300,
        "challenge_type": "python",
        "phase": "refuerzo",
        "concepts_taught_json": json.dumps(["dict", "sorted", "lambda", "string", "round", "set"]),
        "initial_code": (
            "texto = 'el nexo protege el sistema el operador activa el nexo'\n"
            "palabras = texto.split()\n"
            "\n"
            "# 1. Total de palabras\n"
            "# TU CÓDIGO AQUÍ\n"
            "\n"
            "# 2. Total de palabras únicas\n"
            "# TU CÓDIGO AQUÍ\n"
            "\n"
            "# 3. Palabra más frecuente (empate: la primera alfabéticamente)\n"
            "# TU CÓDIGO AQUÍ\n"
            "\n"
            "# 4. Longitud promedio redondeada a 1 decimal\n"
            "# TU CÓDIGO AQUÍ\n"
        ),
        "expected_output": "Palabras: 10\nUnicas: 6\nMas frecuente: el\nLongitud media: 3.5",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "DAKI recibió la transmisión más larga del ciclo operativo. "
            "El sistema de análisis semántico necesita estadísticas completas "
            "para determinar el perfil de amenaza del emisor. El Operador debe demostrar "
            "dominio total sobre manipulación de texto y frecuencias."
        ),
        "pedagogical_objective": "Integrar dict de frecuencias, sorted con lambda multi-criterio, set() y expresiones generadoras.",
        "syntax_hint": "sorted(freq.items(), key=lambda x: (-x[1], x[0]))[0][0]",
        "theory_content": None,
        "hints_json": json.dumps([
            "Calculá freq igual que antes. Para el más frecuente, ordená por (-frecuencia, nombre) y tomá el [0][0].",
            "Longitud promedio: sum(len(p) for p in palabras) / len(palabras).",
            "Usá f-strings para el formato exacto: f'Palabras: {len(palabras)}'.",
        ]),
        "strict_match": True,
    },
]
