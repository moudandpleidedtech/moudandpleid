"""
seed_sector_14.py — Sector 14: Integración Total (niveles 121–129)
==================================================================
Niveles 121–129  |  9 misiones  |  Sector ID = 13

El nivel 130 (Boss) es el CONTRATO-130 en seed_contratos.py.

Temática técnica: desafíos de integración que combinan múltiples conceptos.
Clases + dicts, procesamiento de texto complejo, algoritmos + OOP.

Lore DAKI: "El Operador demuestra que puede combinar todo lo aprendido
            bajo presión. El nivel 130 (Contrato) es la prueba final."
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.models.challenge import Challenge, DifficultyTier  # noqa: F401

SECTOR_14 = [
    # ── L121 — Clase Pila (Stack) ─────────────────────────────────────────────
    {
        "title": "Pila Táctica",
        "description": (
            "Implementá la clase `Pila` (stack LIFO) con:\n"
            "- `push(item)`: agrega al tope\n"
            "- `pop()`: remueve y retorna el tope; retorna None si vacía\n"
            "- `peek()`: retorna el tope sin remover; None si vacía\n"
            "- `esta_vacia()`: retorna True/False\n"
            "- `tamanio()`: retorna cantidad de elementos\n\n"
            "Salida esperada del código dado:\n"
            "```\n3\nC\nC\n2\nFalse\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 14,
        "level_order": 131,
        "base_xp_reward": 230,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 240,
        "challenge_type": "python",
        "phase": "integracion",
        "concepts_taught_json": json.dumps(["class", "list", "stack", "__init__"]),
        "initial_code": (
            "class Pila:\n"
            "    def __init__(self):\n"
            "        pass  # TU CÓDIGO AQUÍ\n"
            "\n"
            "    def push(self, item):\n"
            "        pass\n"
            "\n"
            "    def pop(self):\n"
            "        pass\n"
            "\n"
            "    def peek(self):\n"
            "        pass\n"
            "\n"
            "    def esta_vacia(self):\n"
            "        pass\n"
            "\n"
            "    def tamanio(self):\n"
            "        pass\n"
            "\n"
            "p = Pila()\n"
            "p.push('A'); p.push('B'); p.push('C')\n"
            "print(p.tamanio())\n"
            "print(p.pop())\n"
            "print(p.peek())\n"
            "print(p.tamanio())\n"
            "print(p.esta_vacia())\n"
        ),
        "expected_output": "3\nC\nB\n2\nFalse",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "DAKI usa una pila para gestionar el historial de comandos tácticos. "
            "El último comando enviado puede ser revertido en cualquier momento (LIFO). "
            "El Operador debe implementar esta estructura fundamental."
        ),
        "pedagogical_objective": "Implementar la estructura de datos Pila usando una lista interna con append/pop.",
        "syntax_hint": "self._datos.pop() if self._datos else None",
        "theory_content": None,
        "hints_json": json.dumps([
            "Una lista Python ya es una pila: append() agrega al final (tope), pop() remueve del final.",
            "Para peek(), accedé al último elemento con self._datos[-1].",
            "Verificá lista vacía antes de pop/peek para evitar IndexError.",
        ]),
        "strict_match": True,
    },
    # ── L122 — Validar Paréntesis ─────────────────────────────────────────────
    {
        "title": "Validador de Expresiones",
        "description": (
            "Implementá `parentesis_validos(s)` que verifica si los paréntesis,\n"
            "corchetes y llaves están correctamente anidados y cerrados.\n\n"
            "Ejemplos:\n"
            "```\nparentesis_validos('()[]{}')    → True\n"
            "parentesis_validos('([)]')      → False\n"
            "parentesis_validos('{[()]}')    → True\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 14,
        "level_order": 132,
        "base_xp_reward": 230,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 220,
        "challenge_type": "python",
        "phase": "integracion",
        "concepts_taught_json": json.dumps(["stack", "dict", "list", "string"]),
        "initial_code": (
            "def parentesis_validos(s):\n"
            "    pass  # TU CÓDIGO AQUÍ\n"
            "\n"
            "print(parentesis_validos('()[]{}'))\n"
            "print(parentesis_validos('([)]'))\n"
            "print(parentesis_validos('{[()]}'))\n"
        ),
        "expected_output": "True\nFalse\nTrue",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El compilador de DAKI necesita validar expresiones del sistema antes de ejecutarlas. "
            "Un paréntesis mal cerrado puede corromper una secuencia de comandos completa."
        ),
        "pedagogical_objective": "Aplicar el patrón stack para matching de pares usando un dict de correspondencias.",
        "syntax_hint": "if not pila or pila[-1] != pares[char]: return False",
        "theory_content": None,
        "hints_json": json.dumps([
            "Abridor → push a la pila. Cerrador → verificar que el tope sea el abridor correspondiente.",
            "Dict pares: {')':'(', ']':'[', '}':'{'} mapea cerradores a sus abridores esperados.",
            "Al final, la pila debe estar vacía para que la expresión sea válida.",
        ]),
        "strict_match": True,
    },
    # ── L123 — Matriz Transpuesta ─────────────────────────────────────────────
    {
        "title": "Transposición de Matriz",
        "description": (
            "Implementá `transponer(matriz)` que retorna la transpuesta\n"
            "de una matriz (lista de listas). Filas se convierten en columnas.\n\n"
            "Ejemplo:\n"
            "```\ntransponer([[1,2,3],[4,5,6]]) → [[1,4],[2,5],[3,6]]\n```\n\n"
            "Imprimí cada fila de la transpuesta en una línea."
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 14,
        "level_order": 133,
        "base_xp_reward": 225,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 200,
        "challenge_type": "python",
        "phase": "integracion",
        "concepts_taught_json": json.dumps(["list", "zip", "list_comprehension", "nested_list"]),
        "initial_code": (
            "def transponer(matriz):\n"
            "    pass  # TU CÓDIGO AQUÍ\n"
            "\n"
            "resultado = transponer([[1,2,3],[4,5,6]])\n"
            "for fila in resultado:\n"
            "    print(fila)\n"
        ),
        "expected_output": "[1, 4]\n[2, 5]\n[3, 6]",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El módulo de análisis espacial de DAKI trabaja con matrices de coordenadas. "
            "La transposición convierte filas en columnas — "
            "esencial para cambiar perspectivas en el análisis táctico 2D."
        ),
        "pedagogical_objective": "Usar zip(*matriz) con desempaquetado de argumentos para transponer matrices en una línea.",
        "syntax_hint": "[list(fila) for fila in zip(*matriz)]",
        "theory_content": None,
        "hints_json": json.dumps([
            "zip(*matriz) desempaqueta la matriz y agrupa los elementos por posición de columna.",
            "Si matriz=[[1,2],[3,4]], zip(*matriz) produce (1,3) y (2,4).",
            "Cada resultado de zip es una tupla — convertila con list().",
        ]),
        "strict_match": True,
    },
    # ── L124 — Generador de Contraseña ───────────────────────────────────────
    {
        "title": "Fortaleza de Contraseña",
        "description": (
            "Implementá `evaluar_contrasena(pwd)` que retorna un string\n"
            "indicando la fortaleza: 'DEBIL', 'MEDIA' o 'FUERTE'.\n\n"
            "Criterios:\n"
            "- Longitud >= 8 (1 punto)\n"
            "- Tiene mayúscula (1 punto)\n"
            "- Tiene dígito (1 punto)\n"
            "- Tiene símbolo (@#$%) (1 punto)\n\n"
            "0-1 puntos → 'DEBIL', 2-3 puntos → 'MEDIA', 4 puntos → 'FUERTE'\n\n"
            "Salida esperada:\n"
            "```\nDEBIL\nMEDIA\nFUERTE\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 14,
        "level_order": 134,
        "base_xp_reward": 225,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 200,
        "challenge_type": "python",
        "phase": "integracion",
        "concepts_taught_json": json.dumps(["string", "any", "boolean", "function"]),
        "initial_code": (
            "def evaluar_contrasena(pwd):\n"
            "    pass  # TU CÓDIGO AQUÍ\n"
            "\n"
            "print(evaluar_contrasena('abc'))\n"
            "print(evaluar_contrasena('Nexo2025'))\n"
            "print(evaluar_contrasena('D@ki#2025!'))\n"
        ),
        "expected_output": "DEBIL\nMEDIA\nFUERTE",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El sistema de seguridad del Nexo requiere que todas las contraseñas sean evaluadas "
            "antes de ser aceptadas. Las contraseñas débiles son el vector de ataque más común."
        ),
        "pedagogical_objective": "Usar any() con generator expressions para verificar condiciones sobre caracteres.",
        "syntax_hint": "any(c.isupper() for c in pwd)",
        "theory_content": None,
        "hints_json": json.dumps([
            "any() retorna True si al menos un elemento del iterable es True.",
            "any(c.isdigit() for c in pwd) verifica si hay al menos un dígito.",
            "Acumulá puntos con += 1 para cada criterio cumplido.",
        ]),
        "strict_match": True,
    },
    # ── L125 — Serializar / Deserializar ─────────────────────────────────────
    {
        "title": "Codificador de Mensajes",
        "description": (
            "Implementá dos funciones:\n"
            "- `serializar(datos)`: convierte dict → string 'clave=valor' separados por ';'\n"
            "- `deserializar(texto)` → dict\n\n"
            "Ejemplo:\n"
            "```python\ndatos = {'operador':'NEXO', 'nivel':'7', 'mision':'ALFA'}\nserializar(datos) → 'mision=ALFA;nivel=7;operador=NEXO'\n"
            "deserializar('mision=ALFA;nivel=7;operador=NEXO') → {'mision':'ALFA', 'nivel':'7', 'operador':'NEXO'}\n```\n\n"
            "Las claves van ordenadas alfabéticamente al serializar.\n\n"
            "Salida esperada:\n"
            "```\nmision=ALFA;nivel=7;operador=NEXO\n{'mision': 'ALFA', 'nivel': '7', 'operador': 'NEXO'}\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 14,
        "level_order": 135,
        "base_xp_reward": 230,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 210,
        "challenge_type": "python",
        "phase": "integracion",
        "concepts_taught_json": json.dumps(["dict", "string", "split", "join", "sorted"]),
        "initial_code": (
            "def serializar(datos):\n"
            "    pass  # TU CÓDIGO AQUÍ\n"
            "\n"
            "def deserializar(texto):\n"
            "    pass  # TU CÓDIGO AQUÍ\n"
            "\n"
            "datos = {'operador':'NEXO', 'nivel':'7', 'mision':'ALFA'}\n"
            "serializado = serializar(datos)\n"
            "print(serializado)\n"
            "print(deserializar(serializado))\n"
        ),
        "expected_output": "mision=ALFA;nivel=7;operador=NEXO\n{'mision': 'ALFA', 'nivel': '7', 'operador': 'NEXO'}",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "Los mensajes tácticos de DAKI se transmiten como strings simples para minimizar el ancho de banda. "
            "El Operador implementa el protocolo de serialización bidireccional."
        ),
        "pedagogical_objective": "Implementar serialización/deserialización manual combinando join, split y sorted.",
        "syntax_hint": "';'.join(f'{k}={v}' for k, v in sorted(datos.items()))",
        "theory_content": None,
        "hints_json": json.dumps([
            "sorted(datos.items()) retorna pares (clave, valor) ordenados por clave.",
            "join() une los pares 'k=v' con ';' como separador.",
            "Para deserializar: split(';') por pares, luego split('=') por clave/valor.",
        ]),
        "strict_match": True,
    },
    # ── L126 — Mergesort ─────────────────────────────────────────────────────
    {
        "title": "Ordenamiento por Fusión",
        "description": (
            "Implementá `mergesort(lista)` que ordena una lista de enteros\n"
            "usando el algoritmo Merge Sort (divide y conquista).\n\n"
            "Ejemplos:\n"
            "```\nmergesort([5,2,8,1,9,3]) → [1, 2, 3, 5, 8, 9]\n"
            "mergesort([])             → []\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "hard",
        "sector_id": 14,
        "level_order": 136,
        "base_xp_reward": 250,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 300,
        "challenge_type": "python",
        "phase": "integracion",
        "concepts_taught_json": json.dumps(["recursion", "algorithm", "list", "divide_conquer"]),
        "initial_code": (
            "def mergesort(lista):\n"
            "    pass  # TU CÓDIGO AQUÍ\n"
            "\n"
            "def _merge(izq, der):\n"
            "    pass  # TU CÓDIGO AQUÍ\n"
            "\n"
            "print(mergesort([5,2,8,1,9,3]))\n"
            "print(mergesort([]))\n"
        ),
        "expected_output": "[1, 2, 3, 5, 8, 9]\n[]",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El sistema de clasificación del Nexo necesita ordenar millones de registros. "
            "Merge Sort garantiza O(n log n) en todos los casos — "
            "el estándar de oro para ordenamiento estable."
        ),
        "pedagogical_objective": "Implementar Merge Sort recursivo: dividir a la mitad, ordenar cada mitad, fusionar.",
        "syntax_hint": "medio = len(lista) // 2; izq = mergesort(lista[:medio]); der = mergesort(lista[medio:])",
        "theory_content": None,
        "hints_json": json.dumps([
            "Caso base: lista con 0 o 1 elementos ya está ordenada — retornala.",
            "Dividí por la mitad con lista[:medio] y lista[medio:], ordená cada parte recursivamente.",
            "_merge() fusiona dos listas ordenadas en una, comparando elemento por elemento.",
        ]),
        "strict_match": True,
    },
    # ── L127 — Clase con __str__ ──────────────────────────────────────────────
    {
        "title": "Operador con Identidad",
        "description": (
            "Implementá la clase `Operador` con:\n"
            "- `__init__(self, callsign, nivel, xp)`: inicializa\n"
            "- `subir_nivel()`: incrementa nivel en 1 y retorna el nuevo nivel\n"
            "- `__str__()`: retorna '[CALLSIGN] Nivel N — XP total'\n\n"
            "Salida esperada:\n"
            "```\n[NEXO] Nivel 7 — 2500 XP\n8\n[NEXO] Nivel 8 — 2500 XP\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 14,
        "level_order": 137,
        "base_xp_reward": 235,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 200,
        "challenge_type": "python",
        "phase": "integracion",
        "concepts_taught_json": json.dumps(["class", "__str__", "__init__", "methods"]),
        "initial_code": (
            "class Operador:\n"
            "    def __init__(self, callsign, nivel, xp):\n"
            "        pass  # TU CÓDIGO AQUÍ\n"
            "\n"
            "    def subir_nivel(self):\n"
            "        pass\n"
            "\n"
            "    def __str__(self):\n"
            "        pass\n"
            "\n"
            "op = Operador('NEXO', 7, 2500)\n"
            "print(op)\n"
            "print(op.subir_nivel())\n"
            "print(op)\n"
        ),
        "expected_output": "[NEXO] Nivel 7 — 2500 XP\n8\n[NEXO] Nivel 8 — 2500 XP",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "Cada operador del Nexo tiene una identidad única. El método __str__ define "
            "cómo se presenta el operador al sistema — nombre, nivel y experiencia acumulada."
        ),
        "pedagogical_objective": "Implementar __str__ para representación legible de objetos usando f-strings.",
        "syntax_hint": "def __str__(self): return f'[{self.callsign}] Nivel {self.nivel} — {self.xp} XP'",
        "theory_content": None,
        "hints_json": json.dumps([
            "__str__ se llama automáticamente cuando usás print(objeto) o str(objeto).",
            "El formato exacto importa: '[CALLSIGN] Nivel N — XP total'.",
            "subir_nivel() debe incrementar self.nivel y retornarlo.",
        ]),
        "strict_match": True,
    },
    # ── L128 — Generador de Fibonacci ─────────────────────────────────────────
    {
        "title": "Secuencia Fibonacci",
        "description": (
            "Implementá la función `fibonacci(n)` que retorna una lista\n"
            "con los primeros n números de la secuencia de Fibonacci.\n"
            "F(0)=0, F(1)=1, F(n)=F(n-1)+F(n-2).\n\n"
            "Ejemplos:\n"
            "```\nfibonacci(8)  → [0, 1, 1, 2, 3, 5, 8, 13]\n"
            "fibonacci(1)  → [0]\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 14,
        "level_order": 138,
        "base_xp_reward": 230,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 180,
        "challenge_type": "python",
        "phase": "integracion",
        "concepts_taught_json": json.dumps(["loop", "list", "algorithm"]),
        "initial_code": (
            "def fibonacci(n):\n"
            "    pass  # TU CÓDIGO AQUÍ\n"
            "\n"
            "print(fibonacci(8))\n"
            "print(fibonacci(1))\n"
        ),
        "expected_output": "[0, 1, 1, 2, 3, 5, 8, 13]\n[0]",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "Los patrones de crecimiento de amenazas en el Nexo siguen la secuencia de Fibonacci. "
            "DAKI predice la expansión de cada brote modelando su propagación."
        ),
        "pedagogical_objective": "Construir la secuencia iterativamente usando seq[-1] y seq[-2] para acceder a los últimos elementos.",
        "syntax_hint": "seq.append(seq[-1] + seq[-2])",
        "theory_content": None,
        "hints_json": json.dumps([
            "Empezá con [0, 1] y en cada iteración sumá los últimos dos: seq[-1] + seq[-2].",
            "Manejá los casos especiales: n=1 retorna [0], n=2 retorna [0, 1].",
            "El loop corre n-2 veces (ya tenés los primeros 2 elementos).",
        ]),
        "strict_match": True,
    },
    # ── L129 — Máximo de Columnas ─────────────────────────────────────────────
    {
        "title": "Análisis Columnar",
        "description": (
            "Dada una matriz (lista de listas de enteros), retorná una lista\n"
            "con el valor máximo de cada columna.\n\n"
            "Implementá `max_por_columna(matriz)` → lista.\n\n"
            "Ejemplo:\n"
            "```python\nmatriz = [\n    [3, 1, 4],\n    [1, 5, 9],\n    [2, 6, 5]\n]\n"
            "max_por_columna(matriz) → [3, 6, 9]\n```\n\n"
            "Imprimí el resultado."
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 14,
        "level_order": 139,
        "base_xp_reward": 240,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 210,
        "challenge_type": "python",
        "phase": "integracion",
        "concepts_taught_json": json.dumps(["list", "zip", "max", "nested_list"]),
        "initial_code": (
            "def max_por_columna(matriz):\n"
            "    pass  # TU CÓDIGO AQUÍ\n"
            "\n"
            "matriz = [\n"
            "    [3, 1, 4],\n"
            "    [1, 5, 9],\n"
            "    [2, 6, 5]\n"
            "]\n"
            "print(max_por_columna(matriz))\n"
        ),
        "expected_output": "[3, 6, 9]",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El sistema de monitoreo del Nexo registra métricas en matriz: "
            "cada fila es un sensor, cada columna es un instante de tiempo. "
            "El máximo por columna indica el pico de actividad en cada momento."
        ),
        "pedagogical_objective": "Usar zip(*matriz) para iterar columnas y max() para encontrar el valor pico.",
        "syntax_hint": "[max(col) for col in zip(*matriz)]",
        "theory_content": None,
        "hints_json": json.dumps([
            "zip(*matriz) agrupa elementos por posición de columna — cada zip produce una columna.",
            "max(col) encuentra el mayor de cada columna.",
            "Combiná con list comprehension: [max(col) for col in zip(*matriz)].",
        ]),
        "strict_match": True,
    },
]
