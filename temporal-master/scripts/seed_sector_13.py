"""
seed_sector_13.py — Sector 13: Patrones de Datos (niveles 111–120)
===================================================================
Niveles 111–120  |  10 misiones  |  Sector ID = 12

Temática técnica: patrones algorítmicos clásicos aplicados con Python.
Anagramas, dos punteros, ventana deslizante, aplanamiento, agrupación.

Nivel 120 (Boss): Pipeline de transformación de datos.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.models.challenge import Challenge, DifficultyTier  # noqa: F401

SECTOR_13 = [
    # ── L111 — Detector de Anagramas ─────────────────────────────────────────
    {
        "title": "Detector de Anagramas",
        "description": (
            "Dos palabras son anagramas si usan exactamente las mismas letras.\n\n"
            "Implementá `son_anagramas(a, b)` que retorna True o False.\n"
            "Ignorá mayúsculas y espacios.\n\n"
            "Ejemplos:\n"
            "```\nson_anagramas('Roma', 'Amor')  → True\n"
            "son_anagramas('nexo', 'xeon')  → True\n"
            "son_anagramas('daki', 'raid')  → False\n```"
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "easy",
        "sector_id": 13,
        "level_order": 121,
        "base_xp_reward": 185,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 150,
        "challenge_type": "python",
        "phase": "patrones",
        "concepts_taught_json": json.dumps(["string", "sorted", "lower"]),
        "initial_code": (
            "def son_anagramas(a, b):\n"
            "    limpiar = lambda s: sorted(s.lower().replace(' ', ''))\n"
            "    return limpiar(a) == limpiar(b)\n"
            "\n"
            "print(son_anagramas('Roma', 'Amor'))\n"
            "print(son_anagramas('nexo', 'xeon'))\n"
            "print(son_anagramas('daki', 'raid'))\n"
        ),
        "expected_output": "True\nTrue\nFalse",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El sistema criptográfico de DAKI usa anagramas como protocolo de verificación. "
            "Dos agentes intercambian palabras: si son anagramas, la identidad está confirmada."
        ),
        "pedagogical_objective": "Detectar anagramas ordenando y comparando las letras de ambas palabras.",
        "syntax_hint": "sorted(s.lower()) == sorted(t.lower())",
        "theory_content": None,
        "hints_json": json.dumps([
            "sorted(string) retorna una lista de caracteres ordenados. Dos anagramas tienen la misma lista.",
            "Limpiá espacios con .replace(' ', '') antes de ordenar.",
            "Solución: sorted(a.lower().replace(' ','')) == sorted(b.lower().replace(' ',''))",
        ]),
        "strict_match": True,
    },
    # ── L112 — Two Sum ───────────────────────────────────────────────────────
    {
        "title": "Two Sum Táctico",
        "description": (
            "Dado una lista de enteros y un objetivo, encontrá los ÍNDICES de\n"
            "los dos números que suman el objetivo.\n\n"
            "Implementá `two_sum(nums, objetivo)` → retorna una tupla (i, j) con i < j.\n"
            "Garantizado que existe exactamente una solución.\n\n"
            "Ejemplos:\n"
            "```\ntwo_sum([2,7,11,15], 9)   → (0, 1)\n"
            "two_sum([3,2,4], 6)       → (1, 2)\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 13,
        "level_order": 122,
        "base_xp_reward": 210,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 200,
        "challenge_type": "python",
        "phase": "patrones",
        "concepts_taught_json": json.dumps(["dict", "algorithm", "enumerate"]),
        "initial_code": (
            "def two_sum(nums, objetivo):\n"
            "    vistos = {}\n"
            "    for i, num in enumerate(nums):\n"
            "        complemento = objetivo - num\n"
            "        if complemento in vistos:\n"
            "            return (vistos[complemento], i)\n"
            "        vistos[num] = i\n"
            "    return None\n"
            "\n"
            "print(two_sum([2,7,11,15], 9))\n"
            "print(two_sum([3,2,4], 6))\n"
        ),
        "expected_output": "(0, 1)\n(1, 2)",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El detector de combinaciones de DAKI analiza pares de señales que combinadas "
            "alcanzan una frecuencia objetivo. Solución O(n) con diccionario."
        ),
        "pedagogical_objective": "Aplicar el patrón hash-map para two-sum: guardar índices vistos y buscar complemento.",
        "syntax_hint": "complemento = objetivo - num; if complemento in vistos: return (vistos[complemento], i)",
        "theory_content": None,
        "hints_json": json.dumps([
            "Para cada número, calculá qué complemento necesitás para llegar al objetivo.",
            "Si el complemento ya está en el diccionario, encontraste el par.",
            "vistos[num] = i guarda el índice de cada número procesado.",
        ]),
        "strict_match": True,
    },
    # ── L113 — Aplanar Lista ─────────────────────────────────────────────────
    {
        "title": "Aplanador de Datos",
        "description": (
            "Implementá `aplanar(lista)` que convierte una lista con sublistas\n"
            "anidadas en una lista plana (un solo nivel).\n"
            "Solo un nivel de anidamiento garantizado.\n\n"
            "Ejemplo:\n"
            "```\naplanar([[1,2], [3,4], [5]]) → [1, 2, 3, 4, 5]\n```\n\n"
            "Imprimí el resultado."
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "easy",
        "sector_id": 13,
        "level_order": 123,
        "base_xp_reward": 185,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 150,
        "challenge_type": "python",
        "phase": "patrones",
        "concepts_taught_json": json.dumps(["list_comprehension", "nested_list"]),
        "initial_code": (
            "def aplanar(lista):\n"
            "    return [elem for sublista in lista for elem in sublista]\n"
            "\n"
            "print(aplanar([[1,2], [3,4], [5]]))\n"
        ),
        "expected_output": "[1, 2, 3, 4, 5]",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "Los datos de los sensores del Nexo llegan en paquetes agrupados. "
            "El procesador necesita una lista plana para analizar cada lectura individualmente."
        ),
        "pedagogical_objective": "Usar list comprehension doble para aplanar listas anidadas de un nivel.",
        "syntax_hint": "[elem for sublista in lista for elem in sublista]",
        "theory_content": None,
        "hints_json": json.dumps([
            "La comprehension doble: el primer for itera sublistas, el segundo itera elementos de cada sublista.",
            "[elem for sublista in lista for elem in sublista] es equivalente a un doble for anidado.",
        ]),
        "strict_match": True,
    },
    # ── L114 — Agrupar por Categoría ─────────────────────────────────────────
    {
        "title": "Clasificador de Registros",
        "description": (
            "Dado una lista de tuplas (nombre, categoria), agrupá por categoría\n"
            "en un dict donde cada clave es la categoría y el valor es una lista de nombres.\n\n"
            "Implementá `agrupar(registros)` → dict.\n\n"
            "Entrada:\n"
            "```python\nregistros = [('Ana','A'),('Bob','B'),('Carl','A'),('Dan','B'),('Eva','C')]\n```\n"
            "Salida esperada:\n"
            "```\nA: ['Ana', 'Carl']\nB: ['Bob', 'Dan']\nC: ['Eva']\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 13,
        "level_order": 124,
        "base_xp_reward": 210,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 180,
        "challenge_type": "python",
        "phase": "patrones",
        "concepts_taught_json": json.dumps(["dict", "list", "tuple", "setdefault"]),
        "initial_code": (
            "def agrupar(registros):\n"
            "    grupos = {}\n"
            "    for nombre, categoria in registros:\n"
            "        grupos.setdefault(categoria, []).append(nombre)\n"
            "    return grupos\n"
            "\n"
            "registros = [('Ana','A'),('Bob','B'),('Carl','A'),('Dan','B'),('Eva','C')]\n"
            "grupos = agrupar(registros)\n"
            "for cat in sorted(grupos):\n"
            "    print(f'{cat}: {grupos[cat]}')\n"
        ),
        "expected_output": "A: ['Ana', 'Carl']\nB: ['Bob', 'Dan']\nC: ['Eva']",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El sistema de asignación de DAKI clasifica operadores por rango y especialidad. "
            "Agrupar eficientemente determina qué escuadrones están disponibles para cada misión."
        ),
        "pedagogical_objective": "Usar dict.setdefault() para construir un dict de listas sin verificar si la clave existe.",
        "syntax_hint": "grupos.setdefault(categoria, []).append(nombre)",
        "theory_content": None,
        "hints_json": json.dumps([
            "dict.setdefault(key, default) retorna el valor si existe, o lo inicializa con default.",
            "grupos.setdefault(categoria, []) retorna la lista (nueva o existente) para esa categoría.",
            "Luego .append(nombre) agrega el nombre a esa lista.",
        ]),
        "strict_match": True,
    },
    # ── L115 — Promedio Móvil ────────────────────────────────────────────────
    {
        "title": "Media Móvil de Sensores",
        "description": (
            "Implementá `media_movil(datos, k)` que retorna una lista con el\n"
            "promedio de cada ventana de k elementos consecutivos.\n"
            "Redondeá cada promedio a 1 decimal.\n\n"
            "Ejemplo:\n"
            "```\nmedia_movil([1,2,3,4,5,6], 3) → [2.0, 3.0, 4.0, 5.0]\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 13,
        "level_order": 125,
        "base_xp_reward": 215,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 200,
        "challenge_type": "python",
        "phase": "patrones",
        "concepts_taught_json": json.dumps(["list", "slice", "round", "range"]),
        "initial_code": (
            "def media_movil(datos, k):\n"
            "    resultado = []\n"
            "    for i in range(len(datos) - k + 1):\n"
            "        ventana = datos[i:i+k]\n"
            "        resultado.append(round(sum(ventana) / k, 1))\n"
            "    return resultado\n"
            "\n"
            "print(media_movil([1,2,3,4,5,6], 3))\n"
        ),
        "expected_output": "[2.0, 3.0, 4.0, 5.0]",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "Los sensores del Nexo generan ruido. "
            "DAKI suaviza las lecturas calculando el promedio de cada ventana de k muestras. "
            "Es el patrón 'sliding window' — fundamental en análisis de series temporales."
        ),
        "pedagogical_objective": "Implementar sliding window con slicing datos[i:i+k] para calcular promedios locales.",
        "syntax_hint": "for i in range(len(datos) - k + 1): ventana = datos[i:i+k]",
        "theory_content": None,
        "hints_json": json.dumps([
            "El número de ventanas es len(datos) - k + 1.",
            "Cada ventana empieza en índice i y termina en i+k (exclusive): datos[i:i+k].",
            "Calculá sum(ventana)/k y redondeá con round(..., 1).",
        ]),
        "strict_match": True,
    },
    # ── L116 — Palíndromo Avanzado ────────────────────────────────────────────
    {
        "title": "Palíndromo Táctico",
        "description": (
            "Un palíndromo se lee igual al derecho y al revés.\n"
            "Implementá `es_palindromo(texto)` que ignora espacios, signos\n"
            "de puntuación y mayúsculas.\n\n"
            "Ejemplos:\n"
            "```\nes_palindromo('A man a plan a canal Panama') → True\n"
            "es_palindromo('NEXO')                        → False\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 13,
        "level_order": 126,
        "base_xp_reward": 215,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 180,
        "challenge_type": "python",
        "phase": "patrones",
        "concepts_taught_json": json.dumps(["string", "isalnum", "lower", "slice"]),
        "initial_code": (
            "def es_palindromo(texto):\n"
            "    limpio = ''.join(c.lower() for c in texto if c.isalnum())\n"
            "    return limpio == limpio[::-1]\n"
            "\n"
            "print(es_palindromo('A man a plan a canal Panama'))\n"
            "print(es_palindromo('NEXO'))\n"
        ),
        "expected_output": "True\nFalse",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "Las claves de acceso del Nexo son palíndromos — son válidas sin importar "
            "cómo se lean. DAKI necesita validar cada clave antes de autorizar el acceso."
        ),
        "pedagogical_objective": "Limpiar texto con isalnum() y comparar con su reverso [::-1].",
        "syntax_hint": "''.join(c.lower() for c in texto if c.isalnum())",
        "theory_content": None,
        "hints_json": json.dumps([
            "isalnum() retorna True solo para letras y números (filtra espacios y puntuación).",
            "Usá una generator expression para construir el string limpio en minúsculas.",
            "Compará el string limpio con su reverso: limpio == limpio[::-1].",
        ]),
        "strict_match": True,
    },
    # ── L117 — Números Romanos ────────────────────────────────────────────────
    {
        "title": "Decodificador Romano",
        "description": (
            "Implementá `romano_a_entero(s)` que convierte un número romano a entero.\n"
            "Valores: I=1, V=5, X=10, L=50, C=100, D=500, M=1000.\n"
            "Si un símbolo menor precede a uno mayor, se resta.\n\n"
            "Ejemplos:\n"
            "```\nromano_a_entero('III')   → 3\n"
            "romano_a_entero('IX')    → 9\n"
            "romano_a_entero('MCMXC') → 1990\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 13,
        "level_order": 127,
        "base_xp_reward": 220,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 210,
        "challenge_type": "python",
        "phase": "patrones",
        "concepts_taught_json": json.dumps(["dict", "string", "loop"]),
        "initial_code": (
            "def romano_a_entero(s):\n"
            "    valores = {'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000}\n"
            "    total = 0\n"
            "    for i in range(len(s)):\n"
            "        if i + 1 < len(s) and valores[s[i]] < valores[s[i+1]]:\n"
            "            total -= valores[s[i]]\n"
            "        else:\n"
            "            total += valores[s[i]]\n"
            "    return total\n"
            "\n"
            "print(romano_a_entero('III'))\n"
            "print(romano_a_entero('IX'))\n"
            "print(romano_a_entero('MCMXC'))\n"
        ),
        "expected_output": "3\n9\n1990",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "Los archivos históricos del Nexo usan numeración romana en los códigos de clasificación. "
            "DAKI necesita un decodificador para acceder a los registros pre-digitales."
        ),
        "pedagogical_objective": "Manejar la regla de sustracción romana comparando cada símbolo con el siguiente.",
        "syntax_hint": "if valores[s[i]] < valores[s[i+1]]: total -= valores[s[i]]",
        "theory_content": None,
        "hints_json": json.dumps([
            "Si el símbolo actual vale MENOS que el siguiente, se RESTA. Si no, se SUMA.",
            "IX: I(1) < X(10), entonces se resta: total = -1 + 10 = 9.",
            "Recorrés con range(len(s)) y mirás s[i] y s[i+1] para cada par.",
        ]),
        "strict_match": True,
    },
    # ── L118 — Máxima Suma Continua (Kadane) ─────────────────────────────────
    {
        "title": "Subarray de Mayor Ganancia",
        "description": (
            "Encontrá el subarray contiguo con la suma más alta.\n\n"
            "Implementá `max_subarray(nums)` → retorna la suma máxima.\n\n"
            "Ejemplos:\n"
            "```\nmax_subarray([-2,1,-3,4,-1,2,1,-5,4]) → 6  (subarray [4,-1,2,1])\n"
            "max_subarray([-1,-2,-3])               → -1\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "hard",
        "sector_id": 13,
        "level_order": 128,
        "base_xp_reward": 240,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 240,
        "challenge_type": "python",
        "phase": "patrones",
        "concepts_taught_json": json.dumps(["algorithm", "dynamic_programming", "max"]),
        "initial_code": (
            "def max_subarray(nums):\n"
            "    max_actual = nums[0]\n"
            "    max_global = nums[0]\n"
            "    for num in nums[1:]:\n"
            "        max_actual = max(num, max_actual + num)\n"
            "        max_global = max(max_global, max_actual)\n"
            "    return max_global\n"
            "\n"
            "print(max_subarray([-2,1,-3,4,-1,2,1,-5,4]))\n"
            "print(max_subarray([-1,-2,-3]))\n"
        ),
        "expected_output": "6\n-1",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El análisis de mercado táctico del Nexo busca el período de mayor ganancia "
            "en una serie de fluctuaciones. El Algoritmo de Kadane resuelve esto en O(n)."
        ),
        "pedagogical_objective": "Implementar el algoritmo de Kadane para la suma máxima de subarray en O(n).",
        "syntax_hint": "max_actual = max(num, max_actual + num)",
        "theory_content": None,
        "hints_json": json.dumps([
            "En cada paso decidís: ¿empiezo un nuevo subarray desde aquí, o extiendo el actual?",
            "max_actual = max(num, max_actual + num) captura esa decisión.",
            "max_global se actualiza si max_actual supera el máximo visto hasta ahora.",
        ]),
        "strict_match": True,
    },
    # ── L119 — Comprimir String (RLE) ─────────────────────────────────────────
    {
        "title": "Compresión RLE",
        "description": (
            "Run-Length Encoding comprime strings reemplazando secuencias\n"
            "de caracteres repetidos por el carácter + su cuenta.\n"
            "Si la compresión no reduce el tamaño, retorná el original.\n\n"
            "Implementá `comprimir(s)` → string comprimido.\n\n"
            "Ejemplos:\n"
            "```\ncomprimir('aabcccdddd') → 'a2bc3d4'\n"
            "comprimir('abc')         → 'abc'\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 13,
        "level_order": 129,
        "base_xp_reward": 220,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 210,
        "challenge_type": "python",
        "phase": "patrones",
        "concepts_taught_json": json.dumps(["string", "loop", "accumulator"]),
        "initial_code": (
            "def comprimir(s):\n"
            "    if not s:\n"
            "        return ''\n"
            "    resultado = ''\n"
            "    count = 1\n"
            "    for i in range(1, len(s)):\n"
            "        if s[i] == s[i-1]:\n"
            "            count += 1\n"
            "        else:\n"
            "            resultado += s[i-1] + (str(count) if count > 1 else '')\n"
            "            count = 1\n"
            "    resultado += s[-1] + (str(count) if count > 1 else '')\n"
            "    return resultado if len(resultado) < len(s) else s\n"
            "\n"
            "print(comprimir('aabcccdddd'))\n"
            "print(comprimir('abc'))\n"
        ),
        "expected_output": "a2bc3d4\nabc",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "Las transmisiones largas de DAKI contienen muchos caracteres repetidos. "
            "El protocolo RLE reduce el ancho de banda necesario para las comunicaciones de campo."
        ),
        "pedagogical_objective": "Implementar RLE iterando con índice, comparando s[i] con s[i-1] y acumulando resultados.",
        "syntax_hint": "resultado += s[i-1] + (str(count) if count > 1 else '')",
        "theory_content": None,
        "hints_json": json.dumps([
            "Llevá count del carácter actual. Cuando cambia el carácter, añadí prev_char + count al resultado.",
            "Si count==1, no añadís el número (solo la letra: 'b' no 'b1').",
            "Al terminar el loop, añadí el último carácter con su count.",
        ]),
        "strict_match": True,
    },
    # ── L120 — BOSS: Pipeline de Datos ────────────────────────────────────────
    {
        "title": "NEXO-12: Pipeline de Procesamiento",
        "description": (
            "BOSS DEL SECTOR — Pipeline completo de transformación de datos.\n\n"
            "Dado el texto de operadores:\n"
            "```\n'OMEGA:95 ALPHA:78 DELTA:95 BETA:62 GAMMA:78 SIGMA:45'\n```\n\n"
            "1. Parseá los pares nombre:puntaje en un dict\n"
            "2. Filtrá operadores con puntaje >= 70\n"
            "3. Agrupalos por puntaje en un dict {puntaje: [nombres ordenados]}\n"
            "4. Imprimí grupos ordenados de mayor a menor puntaje:\n\n"
            "```\n95: ALPHA, DELTA, OMEGA\n78: GAMMA, OMEGA\n```\n\n"
            "Salida esperada:\n"
            "```\n95: DELTA, OMEGA\n78: ALPHA, GAMMA\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "hard",
        "sector_id": 13,
        "level_order": 130,
        "base_xp_reward": 550,
        "is_project": False,
        "is_phase_boss": True,
        "telemetry_goal_time": 360,
        "challenge_type": "python",
        "phase": "patrones",
        "concepts_taught_json": json.dumps(["dict", "sorted", "filter", "string", "setdefault"]),
        "initial_code": (
            "texto = 'OMEGA:95 ALPHA:78 DELTA:95 BETA:62 GAMMA:78 SIGMA:45'\n"
            "\n"
            "# 1. Parsear\n"
            "operadores = {}\n"
            "for par in texto.split():\n"
            "    nombre, puntaje = par.split(':')\n"
            "    operadores[nombre] = int(puntaje)\n"
            "\n"
            "# 2. Filtrar >= 70\n"
            "elite = {k: v for k, v in operadores.items() if v >= 70}\n"
            "\n"
            "# 3. Agrupar por puntaje\n"
            "grupos = {}\n"
            "for nombre, puntaje in elite.items():\n"
            "    grupos.setdefault(puntaje, []).append(nombre)\n"
            "\n"
            "# 4. Imprimir de mayor a menor\n"
            "for puntaje in sorted(grupos, reverse=True):\n"
            "    nombres = ', '.join(sorted(grupos[puntaje]))\n"
            "    print(f'{puntaje}: {nombres}')\n"
        ),
        "expected_output": "95: DELTA, OMEGA\n78: ALPHA, GAMMA",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El sistema de selección del Nexo recibió los puntajes de todos los operadores disponibles. "
            "DAKI necesita filtrar la élite, agrupar por nivel de desempeño y presentar el ranking "
            "para que el comandante asigne las misiones de alto riesgo."
        ),
        "pedagogical_objective": "Integrar parsing de strings, dict comprehension con filtro, agrupación con setdefault y sorted multi-nivel.",
        "syntax_hint": "for par in texto.split(): nombre, puntaje = par.split(':')",
        "theory_content": None,
        "hints_json": json.dumps([
            "Paso 1: split() por espacio da pares; split(':') da nombre y puntaje.",
            "Paso 2: dict comprehension con if v >= 70 filtra los que no califican.",
            "Paso 3-4: setdefault() para agrupar; sorted(grupos, reverse=True) para ordenar de mayor a menor.",
        ]),
        "strict_match": True,
    },
]
