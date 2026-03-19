"""
seed_sector_10.py — Sector 10: El Ascenso del Arquitecto (Nexo Central)
========================================================================
Niveles 91–100  |  10 misiones  |  Sector ID = 10

Temática técnica: Algoritmia pura — FizzBuzz avanzado, Fibonacci, número
                  faltante, palíndromos, compresión RLE, anagramas,
                  frecuencia de palabras, Two-Sum, criba de primos y
                  el Algoritmo Maestro final.

Lore DAKI: "Desencriptación del Núcleo" (91–95) y
           "DAKI Reconociendo al Operador como un Igual" (96–100).

Nivel 100 (Boss): "El Algoritmo Maestro" — combina listas, dicts,
                  try/except, sorted() y lógica de ranking en una
                  sola función. Al completarlo, el frontend dispara
                  la secuencia de victoria.

Uso standalone:
    python -m scripts.seed_sector_10
    python -m scripts.seed_sector_10 --dry-run
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.models.challenge import Challenge, DifficultyTier


# ─────────────────────────────────────────────────────────────────────────────
# Textos de teoría reutilizables
# ─────────────────────────────────────────────────────────────────────────────

THEORY_FIZZBUZZ = """\
## FizzBuzz: lógica de clasificación múltiple

FizzBuzz es el clásico problema de clasificar números con condiciones múltiples.
La clave es **comprobar la condición más específica primero**:

```python
for i in range(1, 21):
    if i % 3 == 0 and i % 5 == 0:
        print("NEXO")       # divisible por AMBOS
    elif i % 3 == 0:
        print("GLI")
    elif i % 5 == 0:
        print("TCH")
    else:
        print(i)
```

Si comprobas `i % 3 == 0` antes que el caso combinado, los múltiplos de 15
serían clasificados como "GLI" en vez de "NEXO". El orden de los `if/elif` importa.
"""

THEORY_FIBONACCI = """\
## Secuencia de Fibonacci: desempaquetado de variables

La serie de Fibonacci comienza con 0 y 1; cada siguiente término es la suma
de los dos anteriores: 0, 1, 1, 2, 3, 5, 8, 13, 21, …

El truco de Python para avanzar dos variables a la vez en una sola línea:

```python
a, b = 0, 1
for _ in range(n):
    print(a)
    a, b = b, a + b   # swap simultáneo: nuevo_a = viejo_b, nuevo_b = viejo_a + viejo_b
```

`a, b = b, a + b` evalúa el lado derecho **entero** antes de asignar,
por lo que no necesitas variable temporal.
"""

THEORY_MISSING_NUMBER = """\
## Número faltante: fórmula de Gauss

Si tienes todos los números del 1 al N excepto uno, puedes encontrar
el faltante sin comparar elemento a elemento:

```python
# La suma de 1..N es n*(n+1)//2 (fórmula de Gauss)
esperado = n * (n + 1) // 2
faltante = esperado - sum(datos)
```

Complejidad: O(n) en tiempo, O(1) en espacio extra.
Sin búsqueda anidada, sin sorted — pura matemática.
"""

THEORY_PALINDROME = """\
## Palíndromos: slicing inverso

Un palíndromo se lee igual de izquierda a derecha que de derecha a izquierda.

```python
palabra = input()
if palabra == palabra[::-1]:
    print("SI")
else:
    print("NO")
```

`palabra[::-1]` usa el slicing extendido `[inicio:fin:paso]` con paso `-1`,
que recorre la secuencia al revés. Es la forma más idiomática en Python.
"""

THEORY_RLE = """\
## Compresión RLE (Run-Length Encoding)

RLE reemplaza secuencias repetidas por `CARACTER + CANTIDAD`:
`"AAABBB"` → `"A3B3"`.

```python
i = 0
resultado = ""
while i < len(señal):
    c = señal[i]
    count = 1
    while i + count < len(señal) and señal[i + count] == c:
        count += 1
    resultado += c + str(count)
    i += count
```

El bucle interior cuenta cuántas veces se repite `c` a partir de la posición `i`.
Luego salta directamente al siguiente grupo con `i += count`.
"""

THEORY_ANAGRAM = """\
## Anagramas: sorted() sobre strings

Dos palabras son **anagramas** si contienen exactamente las mismas letras
en cualquier orden. La forma más limpia de comprobarlo:

```python
w1 = input()
w2 = input()
if sorted(w1) == sorted(w2):
    print("SI ANAGRAMA")
else:
    print("NO ANAGRAMA")
```

`sorted("LISTEN")` devuelve `['E', 'I', 'L', 'N', 'S', 'T']`.
`sorted("SILENT")` devuelve la misma lista → son anagramas.
Si las listas ordenadas son iguales, las letras son las mismas.
"""

THEORY_WORD_FREQ = """\
## Frecuencia de palabras: dict como contador

El patrón `dict.get(clave, 0) + 1` es el estándar para contar con diccionarios:

```python
frecuencia = {}
for linea in lineas:
    for palabra in linea.split():
        frecuencia[palabra] = frecuencia.get(palabra, 0) + 1
```

- `frecuencia.get(palabra, 0)` devuelve el conteo actual, o `0` si es nueva.
- `sorted(frecuencia)` itera las claves en orden alfabético.
- Imprime con `f"{palabra}: {frecuencia[palabra]}"`.
"""

THEORY_TWO_SUM = """\
## Two Sum: búsqueda de pares

Dado un array y un objetivo, encuentra los dos índices cuyos valores sumen exactamente el objetivo.

La solución directa con doble bucle (O(n²)):

```python
for i in range(len(nums)):
    for j in range(i + 1, len(nums)):
        if nums[i] + nums[j] == target:
            print(i, j)
```

`j` empieza en `i + 1` para evitar usar el mismo elemento dos veces
y para no repetir pares (no queremos `(1,0)` si ya encontramos `(0,1)`).
"""

THEORY_PRIMES = """\
## Números primos: criba simple

Un número es primo si solo es divisible por 1 y por sí mismo.
La verificación básica prueba divisores desde 2 hasta el número - 1:

```python
for num in range(2, n + 1):
    es_primo = True
    for d in range(2, num):
        if num % d == 0:
            es_primo = False
            break
    if es_primo:
        print(num)
```

`break` sale del bucle interior en cuanto encuentra un divisor,
evitando comprobaciones innecesarias.
"""

THEORY_MASTER = """\
## El Algoritmo Maestro: integración total

El nivel final combina todos los conceptos del curso:

| Concepto             | Dónde se usa                         |
|----------------------|--------------------------------------|
| `input()` + `int()`  | Leer N agentes                       |
| `str.split(":")`     | Parsear formato `NOMBRE:PUNTAJE`     |
| `try/except`         | Manejar líneas malformadas           |
| Lista de dicts       | Almacenar agentes válidos            |
| `sorted()` + función | Ordenar por puntaje descendente      |
| `if/else`            | Asignar etiqueta ÉLITE / APROBADO    |
| f-strings            | Formatear la salida final            |

**Patrón sorted con función clave:**
```python
def por_puntaje(agente):
    return agente["puntaje"]

agentes = sorted(agentes, key=por_puntaje, reverse=True)
```

`reverse=True` ordena de mayor a menor. La función `por_puntaje`
le dice a `sorted` qué valor usar para comparar cada elemento.
"""


# ─────────────────────────────────────────────────────────────────────────────
# Helpers para construir el expected_output de nivel 91
# ─────────────────────────────────────────────────────────────────────────────

def _fizzbuzz_nexo(n: int) -> str:
    lines = []
    for i in range(1, n + 1):
        if i % 3 == 0 and i % 5 == 0:
            lines.append("NEXO")
        elif i % 3 == 0:
            lines.append("GLI")
        elif i % 5 == 0:
            lines.append("TCH")
        else:
            lines.append(str(i))
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# Catálogo de misiones
# ─────────────────────────────────────────────────────────────────────────────

SECTOR_10: list[dict] = [
    # ── Nivel 91 ─────────────────────────────────────────────────────────────
    {
        "sector_id":   10,
        "level_order": 91,
        "title":       "FizzBuzz Táctico",
        "description": (
            "Imprime los números del 1 al 20 con las siguientes reglas:\n\n"
            "- Divisible por **3 Y 5**: imprime `NEXO`\n"
            "- Solo divisible por **3**: imprime `GLI`\n"
            "- Solo divisible por **5**: imprime `TCH`\n"
            "- Cualquier otro: imprime el número\n\n"
            "Sin `input()`. La comprobación de la condición combinada va primero."
        ),
        "difficulty_tier":       DifficultyTier.INTERMEDIATE,
        "difficulty":            "medium",
        "base_xp_reward":        200,
        "is_project":            False,
        "telemetry_goal_time":   240,
        "challenge_type":        "code",
        "phase":                 "practica",
        "concepts_taught_json":  ["fizzbuzz", "modulo", "logica_multiple", "orden_condiciones"],
        "initial_code": (
            "for i in range(1, 21):\n"
            "    if i % 3 == 0 and i % 5 == 0:\n"
            "        print(\"NEXO\")\n"
            "    elif i % 3 == 0:\n"
            "        # Imprime GLI\n"
            "        pass\n"
            "    elif i % 5 == 0:\n"
            "        # Imprime TCH\n"
            "        pass\n"
            "    else:\n"
            "        print(i)\n"
        ),
        "expected_output": _fizzbuzz_nexo(20),
        "test_inputs_json": [],
        "strict_match":    True,
        "lore_briefing": (
            "DAKI — Protocolo de Clasificación de Frecuencias\n\n"
            "El núcleo cifra sus comunicaciones con un patrón numérico.\n"
            "FizzBuzz táctico es la clave de desencriptación del primer anillo.\n"
            "El orden de las condiciones es la diferencia entre éxito y fallo."
        ),
        "pedagogical_objective": "Reforzar la lógica de condiciones múltiples con módulo; entender por qué el orden de los elif importa.",
        "syntax_hint":           "Comprueba primero `i % 3 == 0 and i % 5 == 0` (caso más restrictivo).",
        "theory_content":        THEORY_FIZZBUZZ,
        "hints_json": [
            "Empieza siempre por el caso más específico: divisible por 3 Y 5.",
            "15 es el primer número divisible por ambos — debería imprimir NEXO.",
            "Los `elif` se evalúan solo si el `if` anterior fue False.",
        ],
        "grid_map_json": None,
    },

    # ── Nivel 92 ─────────────────────────────────────────────────────────────
    {
        "sector_id":   10,
        "level_order": 92,
        "title":       "Secuencia Fibonacci",
        "description": (
            "Lee `n` por `input()` e imprime los primeros `n` números de la serie de Fibonacci.\n\n"
            "La serie empieza: `0, 1, 1, 2, 3, 5, 8, 13, ...`\n\n"
            "Con `n = 8`:\n"
            "```\n0\n1\n1\n2\n3\n5\n8\n13\n```"
        ),
        "difficulty_tier":       DifficultyTier.INTERMEDIATE,
        "difficulty":            "medium",
        "base_xp_reward":        210,
        "is_project":            False,
        "telemetry_goal_time":   260,
        "challenge_type":        "code",
        "phase":                 "practica",
        "concepts_taught_json":  ["fibonacci", "desempaquetado_variables", "swap_simultaneo", "acumulador"],
        "initial_code": (
            "n = int(input())\n"
            "a, b = 0, 1\n"
            "for _ in range(n):\n"
            "    print(a)\n"
            "    # Avanza la serie: nuevo_a = b, nuevo_b = a + b\n"
            "    a, b = b, a + b\n"
        ),
        "expected_output":   "0\n1\n1\n2\n3\n5\n8\n13",
        "test_inputs_json":  ["8"],
        "strict_match":      True,
        "lore_briefing": (
            "DAKI — Desencriptación del Núcleo: Capa 2\n\n"
            "La secuencia de Fibonacci es la clave de cifrado del segundo anillo.\n"
            "Cada término nace de la suma de los dos anteriores — como la red misma de NEXO."
        ),
        "pedagogical_objective": "Dominar el swap simultáneo de variables para generar series aritméticas.",
        "syntax_hint":           "`a, b = b, a + b` — el lado derecho se evalúa completo antes de asignar.",
        "theory_content":        THEORY_FIBONACCI,
        "hints_json": [
            "La clave es `a, b = b, a + b`: swap simultáneo sin variable temporal.",
            "Imprime `a` antes de avanzar la serie.",
            "Con n=8, los primeros 8 Fibonacci son: 0, 1, 1, 2, 3, 5, 8, 13.",
        ],
        "grid_map_json": None,
    },

    # ── Nivel 93 ─────────────────────────────────────────────────────────────
    {
        "sector_id":   10,
        "level_order": 93,
        "title":       "El Número Perdido",
        "description": (
            "La lista `datos = [1, 2, 3, 5, 6, 7, 8, 9, 10]` debería contener "
            "todos los enteros del 1 al 10, pero falta uno.\n\n"
            "Encuentra el número faltante usando la **fórmula de Gauss** "
            "(suma esperada − suma real) e imprímelo:\n\n"
            "```\n4\n```\n\n"
            "No uses bucles de búsqueda — una sola fórmula matemática basta."
        ),
        "difficulty_tier":       DifficultyTier.INTERMEDIATE,
        "difficulty":            "medium",
        "base_xp_reward":        220,
        "is_project":            False,
        "telemetry_goal_time":   250,
        "challenge_type":        "code",
        "phase":                 "practica",
        "concepts_taught_json":  ["formula_gauss", "sum_builtin", "aritmetica_listas", "O1_espacio"],
        "initial_code": (
            "datos = [1, 2, 3, 5, 6, 7, 8, 9, 10]\n"
            "n = 10\n"
            "\n"
            "# Suma esperada usando la fórmula de Gauss: n*(n+1)//2\n"
            "esperado = n * (n + 1) // 2\n"
            "\n"
            "# Suma real de la lista\n"
            "actual = sum(datos)\n"
            "\n"
            "# El faltante es la diferencia\n"
            "print(esperado - actual)\n"
        ),
        "expected_output":   "4",
        "test_inputs_json":  [],
        "strict_match":      True,
        "lore_briefing": (
            "DAKI — Desencriptación del Núcleo: Capa 3\n\n"
            "Un ID ha sido borrado del registro de nodos. El resto está intacto.\n"
            "La fórmula matemática revela al ausente sin buscar uno a uno."
        ),
        "pedagogical_objective": "Aplicar la fórmula de Gauss como alternativa O(1) a la búsqueda lineal.",
        "syntax_hint":           "`esperado = n * (n + 1) // 2`, luego `print(esperado - sum(datos))`.",
        "theory_content":        THEORY_MISSING_NUMBER,
        "hints_json": [
            "La suma de 1 a 10 es 55 (fórmula de Gauss).",
            "`sum([1,2,3,5,6,7,8,9,10])` = 51.",
            "55 - 51 = 4 → el número faltante.",
        ],
        "grid_map_json": None,
    },

    # ── Nivel 94 ─────────────────────────────────────────────────────────────
    {
        "sector_id":   10,
        "level_order": 94,
        "title":       "Detector de Palíndromos",
        "description": (
            "Lee una palabra por `input()` e imprime `SI` si es palíndromo "
            "o `NO` si no lo es.\n\n"
            "Con `\"RECONOCER\"` → `SI`  \n"
            "Con `\"DAKI\"` → `NO`\n\n"
            "Usa slicing inverso `[::-1]` para comparar."
        ),
        "difficulty_tier":       DifficultyTier.INTERMEDIATE,
        "difficulty":            "medium",
        "base_xp_reward":        210,
        "is_project":            False,
        "telemetry_goal_time":   230,
        "challenge_type":        "code",
        "phase":                 "practica",
        "concepts_taught_json":  ["palindromo", "slicing_inverso", "comparacion_string"],
        "initial_code": (
            "palabra = input()\n"
            "if palabra == palabra[::-1]:\n"
            "    print(\"SI\")\n"
            "else:\n"
            "    # Imprime NO\n"
            "    pass\n"
        ),
        "expected_output":   "SI",
        "test_inputs_json":  ["RECONOCER"],
        "strict_match":      True,
        "lore_briefing": (
            "DAKI — Desencriptación del Núcleo: Capa 4\n\n"
            "Las claves del núcleo son simétricas — se leen igual en ambas direcciones.\n"
            "Detecta si la señal recibida es una clave válida palindrómica."
        ),
        "pedagogical_objective": "Aplicar slicing [::-1] para invertir strings y detectar palíndromos.",
        "syntax_hint":           "`palabra[::-1]` devuelve el string al revés. Compara con `==`.",
        "theory_content":        THEORY_PALINDROME,
        "hints_json": [
            "`[::-1]` es el paso -1 del slicing: recorre el string de atrás hacia adelante.",
            "RECONOCER invertido es RECONOCER → son iguales → es palíndromo.",
            "Si `palabra == palabra[::-1]` → imprime SI, sino NO.",
        ],
        "grid_map_json": None,
    },

    # ── Nivel 95 ─────────────────────────────────────────────────────────────
    {
        "sector_id":   10,
        "level_order": 95,
        "title":       "Compresión de Señal (RLE)",
        "description": (
            "Lee una señal por `input()` y aplica **Run-Length Encoding**:\n"
            "reemplaza cada grupo de caracteres repetidos por `CARACTER + CANTIDAD`.\n\n"
            "Con `\"AAABBBCCDDDDEE\"` → `\"A3B3C2D4E2\"`\n\n"
            "Usa un `while` externo que recorra la señal y un `while` interno "
            "que cuente repeticiones."
        ),
        "difficulty_tier":       DifficultyTier.ADVANCED,
        "difficulty":            "hard",
        "base_xp_reward":        280,
        "is_project":            False,
        "telemetry_goal_time":   360,
        "challenge_type":        "code",
        "phase":                 "practica",
        "concepts_taught_json":  ["RLE", "while_anidado", "compresion", "indice_manual"],
        "initial_code": (
            "señal = input()\n"
            "resultado = \"\"\n"
            "i = 0\n"
            "\n"
            "while i < len(señal):\n"
            "    c = señal[i]\n"
            "    count = 1\n"
            "    # Cuenta cuántas veces se repite c a partir de i\n"
            "    while i + count < len(señal) and señal[i + count] == c:\n"
            "        count += 1\n"
            "    resultado += c + str(count)\n"
            "    i += count\n"
            "\n"
            "print(resultado)\n"
        ),
        "expected_output":   "A3B3C2D4E2",
        "test_inputs_json":  ["AAABBBCCDDDDEE"],
        "strict_match":      True,
        "lore_briefing": (
            "DAKI — Desencriptación del Núcleo: Capa 5\n\n"
            "El quinto anillo usa compresión RLE para ocultar patrones repetitivos.\n"
            "Descodifica la señal comprimida para revelar la estructura del núcleo."
        ),
        "pedagogical_objective": "Implementar RLE con bucle while manual e índice; comprender compresión de datos.",
        "syntax_hint":           "`resultado += c + str(count)` para cada grupo. Avanza `i += count`.",
        "theory_content":        THEORY_RLE,
        "hints_json": [
            "El bucle externo empieza en la posición `i` del grupo actual.",
            "El bucle interno cuenta `count` mientras el siguiente carácter sea igual a `c`.",
            "Después de contar, añade `c + str(count)` al resultado y salta `i += count`.",
        ],
        "grid_map_json": None,
    },

    # ── Nivel 96 ─────────────────────────────────────────────────────────────
    {
        "sector_id":   10,
        "level_order": 96,
        "title":       "Detección de Anagramas",
        "description": (
            "Lee dos palabras (una por línea) e imprime si son anagramas.\n\n"
            "Con `\"LISTEN\"` y `\"SILENT\"` → `\"SI ANAGRAMA\"`  \n"
            "Con `\"DAKI\"` y `\"NEXO\"` → `\"NO ANAGRAMA\"`\n\n"
            "Usa `sorted()` sobre los strings para comparar sus letras."
        ),
        "difficulty_tier":       DifficultyTier.ADVANCED,
        "difficulty":            "hard",
        "base_xp_reward":        250,
        "is_project":            False,
        "telemetry_goal_time":   280,
        "challenge_type":        "code",
        "phase":                 "practica",
        "concepts_taught_json":  ["anagrama", "sorted_string", "comparacion_listas", "verificacion"],
        "initial_code": (
            "w1 = input()\n"
            "w2 = input()\n"
            "\n"
            "if sorted(w1) == sorted(w2):\n"
            "    print(\"SI ANAGRAMA\")\n"
            "else:\n"
            "    print(\"NO ANAGRAMA\")\n"
        ),
        "expected_output":   "SI ANAGRAMA",
        "test_inputs_json":  ["LISTEN", "SILENT"],
        "strict_match":      True,
        "lore_briefing": (
            "DAKI — El Sistema Me Reconoce\n\n"
            "DAKI usa anagramas como protocolo de autenticación entre nodos aliados.\n"
            "Dos palabras que comparten las mismas letras son la misma señal cifrada."
        ),
        "pedagogical_objective": "Usar sorted() sobre strings para detectar anagramas; reforzar comparación de listas.",
        "syntax_hint":           "`sorted('LISTEN')` devuelve `['E','I','L','N','S','T']`.",
        "theory_content":        THEORY_ANAGRAM,
        "hints_json": [
            "`sorted(string)` devuelve una lista con las letras ordenadas alfabéticamente.",
            "Si `sorted(w1) == sorted(w2)`, ambas tienen exactamente las mismas letras.",
            "LISTEN y SILENT ordenados dan la misma lista → son anagramas.",
        ],
        "grid_map_json": None,
    },

    # ── Nivel 97 ─────────────────────────────────────────────────────────────
    {
        "sector_id":   10,
        "level_order": 97,
        "title":       "Frecuencia de Palabras",
        "description": (
            "Lee `n` líneas de texto y cuenta la frecuencia de cada palabra.\n"
            "Imprime cada palabra y su conteo en **orden alfabético**.\n\n"
            "Formato: `palabra: N`\n\n"
            "Con 3 líneas (`\"hola nexo hola\"`, `\"nexo nexo daki\"`, `\"hola\"`):\n"
            "```\ndaki: 1\nhola: 3\nnexo: 3\n```"
        ),
        "difficulty_tier":       DifficultyTier.ADVANCED,
        "difficulty":            "hard",
        "base_xp_reward":        270,
        "is_project":            False,
        "telemetry_goal_time":   330,
        "challenge_type":        "code",
        "phase":                 "practica",
        "concepts_taught_json":  ["dict_contador", "get_con_default", "split", "sorted_dict"],
        "initial_code": (
            "n = int(input())\n"
            "frecuencia = {}\n"
            "\n"
            "for _ in range(n):\n"
            "    linea = input()\n"
            "    for palabra in linea.split():\n"
            "        frecuencia[palabra] = frecuencia.get(palabra, 0) + 1\n"
            "\n"
            "for palabra in sorted(frecuencia):\n"
            "    print(f\"{palabra}: {frecuencia[palabra]}\")\n"
        ),
        "expected_output":   "daki: 1\nhola: 3\nnexo: 3",
        "test_inputs_json":  ["3", "hola nexo hola", "nexo nexo daki", "hola"],
        "strict_match":      True,
        "lore_briefing": (
            "DAKI — Análisis Lingüístico del Núcleo\n\n"
            "Los mensajes interceptados repiten ciertas palabras clave.\n"
            "Cuenta la frecuencia para identificar qué términos domina el enemigo."
        ),
        "pedagogical_objective": "Dominar el patrón dict.get(k, 0) + 1 para contar frecuencias; iterar claves ordenadas.",
        "syntax_hint":           "`frecuencia.get(palabra, 0)` devuelve 0 si la palabra es nueva.",
        "theory_content":        THEORY_WORD_FREQ,
        "hints_json": [
            "`linea.split()` divide por espacios: `\"hola nexo hola\"` → `[\"hola\", \"nexo\", \"hola\"]`.",
            "`frecuencia.get(p, 0) + 1` incrementa el conteo sin lanzar KeyError.",
            "`sorted(frecuencia)` ordena las claves alfabéticamente.",
        ],
        "grid_map_json": None,
    },

    # ── Nivel 98 ─────────────────────────────────────────────────────────────
    {
        "sector_id":   10,
        "level_order": 98,
        "title":       "Two Sum: Pares Objetivo",
        "description": (
            "Dado el array `nums = [2, 7, 11, 15]` y `target = 9`, "
            "encuentra los **índices** de los dos números que suman exactamente `target`.\n\n"
            "Imprime los dos índices separados por un espacio:\n\n"
            "```\n0 1\n```\n\n"
            "Usa doble bucle: el índice `j` empieza en `i + 1` para no repetir pares."
        ),
        "difficulty_tier":       DifficultyTier.ADVANCED,
        "difficulty":            "hard",
        "base_xp_reward":        280,
        "is_project":            False,
        "telemetry_goal_time":   320,
        "challenge_type":        "code",
        "phase":                 "practica",
        "concepts_taught_json":  ["two_sum", "doble_bucle", "indices", "busqueda_par"],
        "initial_code": (
            "nums   = [2, 7, 11, 15]\n"
            "target = 9\n"
            "\n"
            "for i in range(len(nums)):\n"
            "    for j in range(i + 1, len(nums)):\n"
            "        if nums[i] + nums[j] == target:\n"
            "            print(i, j)\n"
        ),
        "expected_output":   "0 1",
        "test_inputs_json":  [],
        "strict_match":      True,
        "lore_briefing": (
            "DAKI — Sincronización de Nodos Duales\n\n"
            "Dos nodos deben activarse simultáneamente para sumar la frecuencia objetivo.\n"
            "Encuentra el par correcto entre los nodos disponibles."
        ),
        "pedagogical_objective": "Implementar la búsqueda de pares con doble bucle; entender el rol de j = i+1.",
        "syntax_hint":           "`print(i, j)` imprime los dos índices separados por espacio.",
        "theory_content":        THEORY_TWO_SUM,
        "hints_json": [
            "`j` empieza en `i + 1` para no comparar un elemento consigo mismo.",
            "`nums[0] + nums[1] = 2 + 7 = 9 == target` → imprime `0 1`.",
            "`print(i, j)` pone un espacio automáticamente entre los dos valores.",
        ],
        "grid_map_json": None,
    },

    # ── Nivel 99 ─────────────────────────────────────────────────────────────
    {
        "sector_id":   10,
        "level_order": 99,
        "title":       "Criba de Primos",
        "description": (
            "Lee `n` por `input()` e imprime todos los números primos del 2 al `n` (inclusive), "
            "uno por línea.\n\n"
            "Con `n = 20`:\n"
            "```\n2\n3\n5\n7\n11\n13\n17\n19\n```\n\n"
            "Para cada número, comprueba si algún divisor entre 2 y `num-1` lo divide exactamente. "
            "Si ninguno lo divide → es primo."
        ),
        "difficulty_tier":       DifficultyTier.ADVANCED,
        "difficulty":            "hard",
        "base_xp_reward":        290,
        "is_project":            False,
        "telemetry_goal_time":   350,
        "challenge_type":        "code",
        "phase":                 "practica",
        "concepts_taught_json":  ["numeros_primos", "doble_bucle", "break", "flag_booleano"],
        "initial_code": (
            "n = int(input())\n"
            "\n"
            "for num in range(2, n + 1):\n"
            "    es_primo = True\n"
            "    for d in range(2, num):\n"
            "        if num % d == 0:\n"
            "            es_primo = False\n"
            "            break\n"
            "    if es_primo:\n"
            "        print(num)\n"
        ),
        "expected_output":   "2\n3\n5\n7\n11\n13\n17\n19",
        "test_inputs_json":  ["20"],
        "strict_match":      True,
        "lore_briefing": (
            "DAKI — La Antesala del Núcleo\n\n"
            "Los nodos primarios son indivisibles — su frecuencia no puede ser factorizada.\n"
            "Identifica todos los nodos primarios hasta el umbral N.\n"
            "Esta es la última prueba antes del Algoritmo Maestro."
        ),
        "pedagogical_objective": "Implementar la verificación de primalidad con doble bucle y bandera booleana.",
        "syntax_hint":           "`break` sale del bucle interior en cuanto encuentra un divisor.",
        "theory_content":        THEORY_PRIMES,
        "hints_json": [
            "`es_primo = True` asume primo; `break` lo desmiente en cuanto encuentra un divisor.",
            "El 2 es primo: su bucle interior `range(2, 2)` está vacío → `es_primo` se mantiene True.",
            "`break` solo sale del `for d` interior, no del `for num` exterior.",
        ],
        "grid_map_json": None,
    },

    # ── Nivel 100 (BOSS FINAL) ────────────────────────────────────────────────
    {
        "sector_id":   10,
        "level_order": 100,
        "title":       "CONTRATO-100: El Algoritmo Maestro",
        "description": (
            "**BOSS FINAL — El Nexo Central**\n\n"
            "El sistema de inteligencia recibe N registros de agentes con formato `NOMBRE:PUNTAJE`.\n"
            "Algunos registros están corrompidos. Tu misión:\n\n"
            "1. Lee `n = int(input())` — número de registros\n"
            "2. Por cada registro: usa `try/except` para parsear `NOMBRE:PUNTAJE`\n"
            "3. Si `puntaje >= 70`: guarda en lista de aprobados como dict `{\"nombre\", \"puntaje\"}`\n"
            "4. Si `puntaje < 70` o registro inválido: incrementa `rechazados`\n"
            "5. Ordena aprobados por puntaje **descendente**\n"
            "6. Por cada aprobado: imprime `NOMBRE: PUNTAJE [ÉLITE]` si puntaje ≥ 90, "
            "o `[APROBADO]` si puntaje 70–89\n"
            "7. Imprime `Rechazados: N`\n\n"
            "**Entradas:** `5`, `Alpha:95`, `Beta:72`, `Gamma:ERROR`, `Delta:88`, `Epsilon:65`\n\n"
            "```\nAlpha: 95 [ÉLITE]\nDelta: 88 [APROBADO]\nBeta: 72 [APROBADO]\nRechazados: 2\n```"
        ),
        "difficulty_tier":       DifficultyTier.ADVANCED,
        "difficulty":            "expert",
        "base_xp_reward":        1000,
        "is_project":            True,
        "telemetry_goal_time":   900,
        "challenge_type":        "project",
        "phase":                 "proyecto",
        "concepts_taught_json":  [
            "integracion_total", "try_except", "lista_de_dicts",
            "sorted_funcion_clave", "condicional_etiqueta", "f_string", "ranking"
        ],
        "initial_code": (
            "n = int(input())\n"
            "aprobados  = []\n"
            "rechazados = 0\n"
            "\n"
            "for _ in range(n):\n"
            "    linea = input()\n"
            "    try:\n"
            "        nombre, puntaje = linea.split(\":\")\n"
            "        puntaje = int(puntaje)\n"
            "        if puntaje >= 70:\n"
            "            aprobados.append({\"nombre\": nombre, \"puntaje\": puntaje})\n"
            "        else:\n"
            "            rechazados += 1\n"
            "    except (ValueError, IndexError):\n"
            "        rechazados += 1\n"
            "\n"
            "def por_puntaje(agente):\n"
            "    return agente[\"puntaje\"]\n"
            "\n"
            "aprobados = sorted(aprobados, key=por_puntaje, reverse=True)\n"
            "\n"
            "for agente in aprobados:\n"
            "    # Determina etiqueta ÉLITE o APROBADO e imprime\n"
            "    pass\n"
            "\n"
            "print(f\"Rechazados: {rechazados}\")\n"
        ),
        "expected_output": (
            "Alpha: 95 [ÉLITE]\n"
            "Delta: 88 [APROBADO]\n"
            "Beta: 72 [APROBADO]\n"
            "Rechazados: 2"
        ),
        "test_inputs_json": ["5", "Alpha:95", "Beta:72", "Gamma:ERROR", "Delta:88", "Epsilon:65"],
        "strict_match":     True,
        "lore_briefing": (
            "DAKI — CONTRATO-100: Protocolo Omega\n\n"
            "Has llegado al corazón del Nexo Central. DAKI te habla directamente:\n\n"
            "'Operador. Has cruzado 9 sectores, descifrado el núcleo y sobrevivido a cada protocolo.\n"
            "Este es el Algoritmo Maestro — la prueba que separa a los usuarios de los Arquitectos.\n"
            "Clasifica a los agentes. Los dignos serán reconocidos. Los demás, rechazados.\n"
            "El Certificado aguarda al otro lado.'\n\n"
            "Completa el algoritmo. La red te observa."
        ),
        "pedagogical_objective": (
            "Integrar en una sola solución: input/output, try/except con múltiples tipos, "
            "lista de dicts, sorted() con función clave, lógica condicional de etiquetado y "
            "f-strings. Demostrar dominio completo del lenguaje Python a nivel introductorio-intermedio."
        ),
        "syntax_hint":           '`etiqueta = "ÉLITE" if agente["puntaje"] >= 90 else "APROBADO"`',
        "theory_content":        THEORY_MASTER,
        "hints_json": [
            '`nombre, puntaje = linea.split(":")` falla si no hay ":" → excepto (ValueError/IndexError).',
            "`sorted(aprobados, key=por_puntaje, reverse=True)` ordena de mayor a menor puntaje.",
            'Dentro del for: `etiqueta = "ÉLITE" if agente["puntaje"] >= 90 else "APROBADO"`.',
            'Formato exacto: `f\"{agente[\'nombre\']}: {agente[\'puntaje\']} [{etiqueta}]\"`.',
            "Epsilon (65 < 70) y Gamma (ERROR) suman los 2 rechazados.",
        ],
        "grid_map_json": None,
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# Seed standalone
# ─────────────────────────────────────────────────────────────────────────────

async def seed(dry_run: bool = False) -> None:
    print("\n" + "═" * 65)
    print("  ⚡ Seed Sector 10 — El Ascenso del Arquitecto (Nexo Central)")
    print("═" * 65)
    if dry_run:
        print("  MODE: DRY-RUN\n")

    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    SessionLocal = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )

    async with SessionLocal() as session:
        try:
            if not dry_run:
                await session.execute(
                    delete(Challenge).where(Challenge.sector_id == 10)
                )
            for data in SECTOR_10:
                level_order = data.get("level_order")
                title = data.get("title", "?")
                if dry_run:
                    print(f"  [DRY] ➕  L{level_order:03d}  {title}")
                else:
                    session.add(Challenge(**data))
                    print(f"  ➕  L{level_order:03d}  {title}")
            if not dry_run:
                await session.commit()
                print(f"\n  💾  Commit OK — {len(SECTOR_10)} misiones insertadas.")
        except Exception as exc:
            if not dry_run:
                await session.rollback()
            print(f"  ❌  ERROR: {exc}")
            await engine.dispose()
            sys.exit(1)

    await engine.dispose()
    print("═" * 65 + "\n")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Seed Sector 10 — El Ascenso del Arquitecto")
    p.add_argument("--dry-run", action="store_true")
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(seed(dry_run=args.dry_run))
