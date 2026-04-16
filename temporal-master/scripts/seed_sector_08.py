"""
Seed — SECTOR 08: Motores Lógicos (9 niveles, IDs 61–69).

Uso (desde la raíz del proyecto):
    python -m scripts.seed_sector_08

Comportamiento:
    1. Elimina solo los challenges con sector_id=7 y level_order < 70 (preserva CONTRATO-70).
    2. Inserta los 9 niveles del Sector 07 con curva easy → medium → hard.
    3. El nivel 70 (Boss) vive en seed_contratos.py — no se toca aquí.

Temática técnica: funciones matemáticas de la biblioteca estándar de Python:
    abs(), round(), pow(), min(), max(), sum(), divmod(), // y %.
    Operadores de división entera y módulo aplicados a problemas reales.
    Fórmulas de combate, distribución de recursos, simulación de física.

Narrativa: simulación de físicas de combate, cálculo de rutas de evasión.

NOTA TÉCNICA: El sandbox de GG evalúa código en un entorno aislado que no permite
    `import X`. En lugar de math/random/datetime, este sector enseña las funciones
    matemáticas equivalentes que Python expone como built-ins de forma nativa,
    sin necesidad de importación.
"""

import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.models.challenge import Challenge, DifficultyTier


# ─── Contenido teórico por nivel ─────────────────────────────────────────────

THEORY_N61 = """\
## PROTOCOLO: abs() — Valor Absoluto

`abs(x)` devuelve el valor absoluto de un número: elimina el signo negativo.

```python
print(abs(42))    # 42   (ya era positivo)
print(abs(-42))   # 42   (negativo → positivo)
print(abs(-3.7))  # 3.7
```

---

## CASO DE USO: Distancia

La distancia entre dos puntos siempre es positiva, sin importar el orden:

```python
punto_a = 87
punto_b = 52
distancia = abs(punto_a - punto_b)
print(distancia)   # 35  (mismo resultado que abs(52 - 87))
```

---

## DIFERENCIA vs DISTANCIA

```python
# Diferencia — puede ser negativa:
diferencia = punto_b - punto_a   # -35

# Distancia — siempre positiva:
distancia  = abs(punto_b - punto_a)   # 35
```
"""

THEORY_N62 = """\
## PROTOCOLO: round() — Redondeo de Precisión

`round(numero)` redondea al **entero más cercano**.
`round(numero, decimales)` redondea a N decimales.

```python
print(round(87.6543))     # 88    → al entero más cercano
print(round(87.6543, 2))  # 87.65 → 2 decimales
print(round(87.6543, 1))  # 87.7  → 1 decimal
print(round(87.5))        # 88    → el .5 redondea hacia arriba
```

---

## REGLA DE ORO

Python usa el **redondeo bancario** (round half to even):
`round(0.5)` → `0`, `round(1.5)` → `2` (redondea al par más cercano).

Para la mayoría de los casos prácticos en GG esto no importa.

---

## EVITAR SALIDA FLOTANTE INESPERADA

```python
# Sin round:
print(1 / 3)          # 0.3333333333333333

# Con round:
print(round(1/3, 4))  # 0.3333
```
"""

THEORY_N63 = """\
## PROTOCOLO: pow() y ** — Potenciación

Dos formas de calcular potencias en Python:

```python
# Operador **
print(2 ** 8)      # 256
print(3 ** 4)      # 81

# Función pow()
print(pow(2, 8))   # 256  ← equivalente al operador
print(pow(3, 4))   # 81
```

---

## RAÍCES CON EXPONENTES FRACCIONARIOS

La raíz cuadrada es equivalente a elevar a la potencia 0.5:

```python
print(pow(16, 0.5))   # 4.0   → raíz cuadrada de 16
print(pow(27, 1/3))   # 3.0   → raíz cúbica de 27
```

---

## pow() CON TRES ARGUMENTOS — MÓDULO

`pow(base, exp, mod)` calcula `(base ** exp) % mod` de forma eficiente:

```python
print(pow(2, 10, 1000))   # (2^10) % 1000 = 1024 % 1000 = 24
```

Útil en criptografía y sistemas de hash tácticos.
"""

THEORY_N64 = """\
## PROTOCOLO: min() y max() — Extremos de una Secuencia

`min()` y `max()` devuelven el elemento menor o mayor de una secuencia:

```python
lecturas = [45, 78, 23, 91, 56]

print(min(lecturas))   # 23  → valor más bajo
print(max(lecturas))   # 91  → valor más alto
```

También funcionan con argumentos directos (sin lista):

```python
print(min(5, 3, 8, 1))   # 1
print(max(5, 3, 8, 1))   # 8
```

---

## ENCONTRAR EL RANGO

```python
rango = max(lecturas) - min(lecturas)
print(rango)   # 91 - 23 = 68
```

---

## CON STRINGS

`min()` y `max()` también funcionan con strings (orden alfabético):

```python
codigos = ["ALFA", "BETA", "GAMMA", "DELTA"]
print(min(codigos))   # "ALFA"
print(max(codigos))   # "GAMMA"
```
"""

THEORY_N65 = """\
## PROTOCOLO: divmod() — División Completa en Una Operación

`divmod(a, b)` retorna una **tupla** `(cociente, resto)`:
Equivale a hacer `a // b` y `a % b` al mismo tiempo.

```python
cociente, resto = divmod(135, 60)
print(cociente)   # 2   → cuántas veces entra 60 en 135
print(resto)      # 15  → lo que sobra después de las divisiones
```

---

## CASO DE USO: Conversión de Unidades

```python
# Convertir 7384 segundos a horas, minutos y segundos
segundos_totales = 7384

horas,   resto_horas = divmod(segundos_totales, 3600)
minutos, segundos    = divmod(resto_horas,       60)

print(f"{horas}h {minutos}m {segundos}s")   # 2h 3m 4s
```

---

## ALTERNATIVA SIN divmod()

```python
cociente = a // b   # división entera
resto    = a % b    # módulo (resto)
```

`divmod()` es más eficiente porque calcula ambos a la vez.
"""

THEORY_N66 = """\
## PROTOCOLO: sum() — Suma de Iterables

`sum(iterable)` suma todos los elementos de una lista o cualquier secuencia:

```python
escudos = [80, 65, 90, 75, 60]
total = sum(escudos)
print(total)   # 370
```

También acepta un segundo argumento como valor inicial:

```python
print(sum([10, 20, 30], 100))   # 160  (100 + 10 + 20 + 30)
```

---

## PATRÓN: PROMEDIO

```python
valores = [80, 65, 90, 75, 60]
promedio = sum(valores) / len(valores)
print(round(promedio, 1))   # 74.0
```

---

## sum() vs ACUMULADOR MANUAL

```python
# Con sum():
total = sum(valores)

# Sin sum() (equivalente):
total = 0
for v in valores:
    total += v
```

`sum()` es más conciso y ligeramente más rápido. Úsalo siempre que puedas.
"""

THEORY_N67 = """\
## PROTOCOLO: // y % — Aritmética Entera

El operador `//` realiza **división entera** (descarta el decimal):

```python
print(100 // 7)   # 14  → cuántos grupos completos de 7 caben en 100
print(7   // 3)   # 2
print(17  // 5)   # 3
```

El operador `%` calcula el **módulo** (el resto de la división entera):

```python
print(100 % 7)    # 2   → lo que sobra después de repartir grupos de 7
print(7   % 3)    # 1
print(17  % 5)    # 2
```

---

## RELACIÓN ENTRE // Y %

Siempre se cumple: `a == (a // b) * b + (a % b)`

```python
a, b = 100, 7
print((a // b) * b + (a % b))   # 100  ✓
```

---

## USOS FRECUENTES

```python
# ¿Es par?
if n % 2 == 0: ...

# Distribución equitativa
unidades = 100
grupos = 7
por_grupo  = unidades // grupos   # 14
excedente  = unidades % grupos    # 2

# Wrap-around (índice circular)
i = (i + 1) % len(lista)
```
"""

THEORY_N68 = """\
## PROTOCOLO: Fórmulas de Combate

Las funciones matemáticas built-in se combinan para modelar sistemas de combate:

```python
# Daño neto (no puede ser negativo)
ataque       = 120
multiplicador = 1.5
defensa      = 40

dano = max(0, round(ataque * multiplicador - defensa * 0.5))
#       ^          ^   180.0              -   20.0
#     mínimo 0  redondea   └─────────────────────────────────┘
#                               = 160.0  →  round  →  160
print(dano)   # 160
```

---

## PATRÓN: CLAMP (ACOTAR VALORES)

`max(0, valor)` garantiza un mínimo de 0.
`min(100, valor)` garantiza un máximo de 100.
`max(0, min(100, valor))` acota entre 0 y 100:

```python
hp = max(0, min(100, hp_actual + curacion))
```

---

## COMPOSICIÓN DE FUNCIONES

Las funciones matemáticas se pueden anidar directamente:

```python
resultado = round(abs(pow(x, 0.5) - y), 2)
```
"""

THEORY_N69 = """\
## PROTOCOLO: Motor de Cálculo — Simulación Paso a Paso

Un motor de cálculo lee datos, aplica fórmulas iterativamente y acumula resultados:

```python
# Simulación de combate: N ataques contra un objetivo con defensa fija
n        = int(input())   # número de ataques
hp       = 100
defensa  = 5
dano_acumulado = 0

for _ in range(n):
    ataque   = int(input())
    dano_neto = max(0, ataque - defensa)   # la defensa absorbe parte del daño
    dano_acumulado += dano_neto

hp_final = max(0, hp - dano_acumulado)
print(dano_acumulado)
print(hp_final)
```

---

## PRINCIPIOS DEL MOTOR

1. **Inicializar** el estado antes del bucle (`hp`, acumuladores)
2. **Leer** los datos de entrada dentro del bucle
3. **Aplicar** la fórmula por cada entrada
4. **Acumular** el resultado con `+=`
5. **Calcular** el estado final fuera del bucle (después del `for`)
"""


# ─── Niveles del Sector 07 ────────────────────────────────────────────────────

SECTOR_08 = [
    # ── NIVEL 61 — abs() ─────────────────────────────────────────────────────
    {
        "title": "Distancia de Señal",
        "description": (
            "El sistema de triangulación del Nexo necesita calcular la distancia "
            "entre dos lecturas de sensor. La distancia siempre es positiva, "
            "sin importar cuál lectura sea mayor.\n\n"
            "Dadas `lectura_a = 87` y `lectura_b = 52`, "
            "calcula e imprime la distancia entre ambas lecturas.\n\n"
            "Salida esperada:\n"
            "```\n35\n```"
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "easy",
        "sector_id": 8,
        "level_order": 71,
        "base_xp_reward": 100,
        "is_project": False,
        "telemetry_goal_time": 90,
        "challenge_type": "python",
        "phase": "motores",
        "concepts_taught_json": json.dumps(["abs()", "distancia", "valor absoluto"]),
        "initial_code": (
            "# MISIÓN: Calcula la distancia entre las dos lecturas\n"
            "\n"
            "lectura_a = 87\n"
            "lectura_b = 52\n"
            "\n"
            "# abs() devuelve el valor absoluto (siempre positivo)\n"
            "distancia = ___(lectura_a - lectura_b)\n"
            "print(distancia)\n"
        ),
        "expected_output": "35",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "Los dos sensores de triangulación del Sector 07 reportaron lecturas "
            "en diferentes momentos del ciclo de exploración. "
            "Para calcular la distancia real entre los puntos de medición, "
            "DAKI necesita la diferencia absoluta — sin importar el orden de resta, "
            "la distancia siempre debe ser un número positivo."
        ),
        "pedagogical_objective": (
            "Introducir abs() como función para obtener el valor absoluto. "
            "Aplicar al cálculo de distancias donde el signo no importa."
        ),
        "syntax_hint": "distancia = abs(lectura_a - lectura_b)",
        "theory_content": THEORY_N61,
        "hints_json": json.dumps([
            "abs() recibe un número y devuelve su valor absoluto: abs(-35) = 35, abs(35) = 35.",
            "La distancia es la diferencia sin signo: abs(lectura_a - lectura_b) o abs(lectura_b - lectura_a), ambos dan 35.",
            "Solución: distancia = abs(lectura_a - lectura_b)",
        ]),
        "strict_match": True,
    },
    # ── NIVEL 62 — round() ────────────────────────────────────────────────────
    {
        "title": "Calibración de Puntería",
        "description": (
            "El sistema de puntería del Nexo calcula ángulos de tiro con alta precisión, "
            "pero el protocolo de reporte solo acepta valores enteros para el registro "
            "general y dos decimales para el registro técnico.\n\n"
            "Dada la lectura `precision = 87.6543`, imprime:\n"
            "1. El valor redondeado al **entero más cercano**\n"
            "2. El valor redondeado a **2 decimales**\n\n"
            "Salida esperada:\n"
            "```\n88\n87.65\n```"
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "easy",
        "sector_id": 8,
        "level_order": 72,
        "base_xp_reward": 100,
        "is_project": False,
        "telemetry_goal_time": 90,
        "challenge_type": "python",
        "phase": "motores",
        "concepts_taught_json": json.dumps(["round()", "redondeo", "decimales"]),
        "initial_code": (
            "# MISIÓN: Redondea la precisión a entero y a 2 decimales\n"
            "\n"
            "precision = 87.6543\n"
            "\n"
            "# Redondea al entero más cercano\n"
            "print(___(precision))\n"
            "\n"
            "# Redondea a 2 decimales\n"
            "print(___(precision, ___))\n"
        ),
        "expected_output": "88\n87.65",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El módulo de calibración del Nexo recibe ángulos de puntería "
            "con 4 decimales del sensor de física de combate. "
            "El reporte táctico necesita dos formatos: uno para el display general "
            "(entero redondeado) y otro para el log técnico detallado (2 decimales). "
            "DAKI llama al módulo de redondeo antes de transmitir los datos."
        ),
        "pedagogical_objective": (
            "Usar round() sin segundo argumento para redondear al entero más cercano. "
            "Usar round(x, n) con segundo argumento para controlar la cantidad de decimales."
        ),
        "syntax_hint": "print(round(precision))\nprint(round(precision, 2))",
        "theory_content": THEORY_N62,
        "hints_json": json.dumps([
            "round(precision) sin segundo argumento redondea al entero más cercano. 87.6543 → 88.",
            "round(precision, 2) redondea a 2 decimales. 87.6543 → 87.65.",
            "Solución: print(round(precision)) y print(round(precision, 2))",
        ]),
        "strict_match": True,
    },
    # ── NIVEL 63 — pow() y ** ─────────────────────────────────────────────────
    {
        "title": "Amplificador de Potencia",
        "description": (
            "El reactor del Nexo usa amplificación exponencial para calcular "
            "la energía de salida: la potencia base se eleva al número de "
            "ciclos de amplificación.\n\n"
            "Dada `base = 3` y `exponente = 4`, imprime el resultado de "
            "elevar la base al exponente usando la función `pow()`.\n\n"
            "Salida esperada:\n"
            "```\n81\n```"
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "easy",
        "sector_id": 8,
        "level_order": 73,
        "base_xp_reward": 125,
        "is_project": False,
        "telemetry_goal_time": 90,
        "challenge_type": "python",
        "phase": "motores",
        "concepts_taught_json": json.dumps(["pow()", "potenciación", "operador **"]),
        "initial_code": (
            "# MISIÓN: Calcula base elevada al exponente con pow()\n"
            "\n"
            "base = 3\n"
            "exponente = 4\n"
            "\n"
            "# pow(base, exponente) es equivalente a base ** exponente\n"
            "print(___(base, exponente))\n"
        ),
        "expected_output": "81",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El núcleo del reactor del Sector 07 usa amplificación exponencial. "
            "Con base 3 y 4 ciclos de amplificación, la energía de salida crece "
            "multiplicando la base por sí misma tantas veces como ciclos haya: "
            "3 × 3 × 3 × 3 = 81 unidades de energía táctica. "
            "DAKI necesita este cálculo para el protocolo de sobrecarga controlada."
        ),
        "pedagogical_objective": (
            "Introducir pow(base, exponente) para cálculos de potencia. "
            "Mencionar la equivalencia con el operador ** (base ** exponente)."
        ),
        "syntax_hint": "print(pow(base, exponente))  # equivalente a print(3 ** 4)",
        "theory_content": THEORY_N63,
        "hints_json": json.dumps([
            "pow(base, exponente) calcula base elevada al exponente. pow(3, 4) = 3×3×3×3 = 81.",
            "También puedes usar el operador **: print(base ** exponente) da el mismo resultado.",
            "Solución: print(pow(base, exponente))",
        ]),
        "strict_match": True,
    },
    # ── NIVEL 64 — min() y max() ──────────────────────────────────────────────
    {
        "title": "Análisis de Amenazas",
        "description": (
            "El sistema de detección del Nexo recibe múltiples lecturas de amenaza "
            "y necesita identificar la amenaza mínima y máxima para ajustar "
            "el nivel de respuesta defensiva.\n\n"
            "Dada la lista `lecturas = [45, 78, 23, 91, 56]`, "
            "imprime la lectura **mínima** y luego la **máxima**.\n\n"
            "Salida esperada:\n"
            "```\n23\n91\n```"
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "easy",
        "sector_id": 8,
        "level_order": 74,
        "base_xp_reward": 125,
        "is_project": False,
        "telemetry_goal_time": 100,
        "challenge_type": "python",
        "phase": "motores",
        "concepts_taught_json": json.dumps(["min()", "max()", "extremos", "análisis de datos"]),
        "initial_code": (
            "# MISIÓN: Encuentra la amenaza mínima y máxima\n"
            "\n"
            "lecturas = [45, 78, 23, 91, 56]\n"
            "\n"
            "# Imprime la lectura mínima\n"
            "print(___(lecturas))\n"
            "\n"
            "# Imprime la lectura máxima\n"
            "print(___(lecturas))\n"
        ),
        "expected_output": "23\n91",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El radar de amenazas del Sector 07 devuelve cinco lecturas de intensidad "
            "de señales enemigas. El protocolo de respuesta defensiva necesita conocer "
            "los extremos: la amenaza más débil define el umbral de alerta temprana, "
            "mientras que la amenaza más fuerte determina el nivel máximo de respuesta. "
            "DAKI extrae ambos valores en una sola pasada."
        ),
        "pedagogical_objective": (
            "Usar min() y max() sobre una lista para obtener el valor extremo. "
            "No requieren ordenar la lista — funcionan en O(n)."
        ),
        "syntax_hint": "print(min(lecturas))\nprint(max(lecturas))",
        "theory_content": THEORY_N64,
        "hints_json": json.dumps([
            "min(lista) devuelve el elemento más pequeño de la lista, sin necesidad de ordenarla.",
            "max(lista) devuelve el elemento más grande.",
            "Solución: print(min(lecturas)) y print(max(lecturas))",
        ]),
        "strict_match": True,
    },
    # ── NIVEL 65 — divmod() ───────────────────────────────────────────────────
    {
        "title": "Conversión de Tiempo Táctico",
        "description": (
            "El cronómetro táctico del Nexo registra el tiempo en segundos totales. "
            "Para el reporte de misión necesitas convertirlo a **minutos y segundos**.\n\n"
            "Dado `segundos = 135`, usa `divmod()` para obtener los minutos y "
            "el resto en segundos, e imprímelos por separado.\n\n"
            "Salida esperada:\n"
            "```\n2\n15\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 8,
        "level_order": 75,
        "base_xp_reward": 150,
        "is_project": False,
        "telemetry_goal_time": 120,
        "challenge_type": "python",
        "phase": "motores",
        "concepts_taught_json": json.dumps([
            "divmod()", "tuplas", "desempaquetado", "conversión de unidades"
        ]),
        "initial_code": (
            "# MISIÓN: Convierte segundos a minutos y segundos\n"
            "\n"
            "segundos = 135\n"
            "\n"
            "# divmod(a, b) retorna (cociente, resto) como tupla\n"
            "minutos, resto = ___(segundos, 60)\n"
            "\n"
            "print(minutos)\n"
            "print(resto)\n"
        ),
        "expected_output": "2\n15",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El sistema de reporte táctico del Nexo registra todas las operaciones "
            "en segundos totales para facilitar los cálculos internos. "
            "Sin embargo, el informe final para el comando central debe presentar "
            "el tiempo en formato legible: minutos y segundos. "
            "DAKI usa divmod para convertir en una sola operación eficiente."
        ),
        "pedagogical_objective": (
            "Usar divmod(a, b) para obtener cociente y resto en un solo paso. "
            "Practicar el desempaquetado de la tupla resultado. "
            "Caso real: conversión de unidades de tiempo."
        ),
        "syntax_hint": "minutos, resto = divmod(segundos, 60)",
        "theory_content": THEORY_N65,
        "hints_json": json.dumps([
            "divmod(135, 60) calcula cuántas veces cabe 60 en 135 y cuánto sobra: devuelve (2, 15).",
            "Desempaqueta la tupla con: minutos, resto = divmod(segundos, 60).",
            "Solución: minutos, resto = divmod(segundos, 60), luego print(minutos) y print(resto).",
        ]),
        "strict_match": True,
    },
    # ── NIVEL 66 — sum() y promedio ───────────────────────────────────────────
    {
        "title": "Telemetría del Escuadrón",
        "description": (
            "El módulo de telemetría del Nexo monitorea el nivel de escudo de "
            "cada agente del escuadrón. El comando necesita el total de energía "
            "defensiva disponible y el promedio por agente.\n\n"
            "Dada la lista `escudos = [80, 65, 90, 75, 60]`, imprime:\n"
            "1. La **suma total** de todos los escudos\n"
            "2. El **promedio** redondeado a 1 decimal\n\n"
            "Salida esperada:\n"
            "```\n370\n74.0\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 8,
        "level_order": 76,
        "base_xp_reward": 150,
        "is_project": False,
        "telemetry_goal_time": 130,
        "challenge_type": "python",
        "phase": "motores",
        "concepts_taught_json": json.dumps([
            "sum()", "promedio", "len()", "round()", "estadísticas básicas"
        ]),
        "initial_code": (
            "# MISIÓN: Calcula la suma total y el promedio de los escudos\n"
            "\n"
            "escudos = [80, 65, 90, 75, 60]\n"
            "\n"
            "# Suma todos los elementos de la lista\n"
            "total = ___(escudos)\n"
            "print(total)\n"
            "\n"
            "# Promedio = total / cantidad de elementos, redondeado a 1 decimal\n"
            "promedio = ___(total / ___(escudos), ___)\n"
            "print(promedio)\n"
        ),
        "expected_output": "370\n74.0",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El sistema de gestión de recursos defensivos del Nexo necesita dos métricas "
            "para el reporte táctico de cada ciclo: la capacidad total de escudo del "
            "escuadrón (para calcular cuánto daño puede absorber en conjunto) "
            "y el promedio por agente (para identificar si alguno está "
            "significativamente por debajo de la media y necesita reabastecimiento)."
        ),
        "pedagogical_objective": (
            "Usar sum() para sumar una lista sin bucle. "
            "Calcular el promedio combinando sum() y len(). "
            "Aplicar round() con 1 decimal al resultado float."
        ),
        "syntax_hint": (
            "total = sum(escudos)\n"
            "promedio = round(total / len(escudos), 1)"
        ),
        "theory_content": THEORY_N66,
        "hints_json": json.dumps([
            "sum(escudos) suma todos los elementos de la lista de forma directa.",
            "El promedio es total dividido entre la cantidad: total / len(escudos).",
            "Envuelve el resultado en round(..., 1) para 1 decimal: round(total / len(escudos), 1)",
        ]),
        "strict_match": True,
    },
    # ── NIVEL 67 — // y % ─────────────────────────────────────────────────────
    {
        "title": "Distribución de Munición",
        "description": (
            "El sistema logístico del Nexo necesita distribuir 100 unidades de munición "
            "entre 7 tanques de forma equitativa. Cada tanque debe recibir la misma "
            "cantidad (sin fracciones), y el excedente queda en el depósito central.\n\n"
            "Imprime cuántas unidades recibe cada tanque y cuántas quedan en el depósito.\n\n"
            "Salida esperada:\n"
            "```\n14\n2\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 8,
        "level_order": 77,
        "base_xp_reward": 150,
        "is_project": False,
        "telemetry_goal_time": 120,
        "challenge_type": "python",
        "phase": "motores",
        "concepts_taught_json": json.dumps([
            "división entera //", "módulo %", "distribución de recursos", "aritmética entera"
        ]),
        "initial_code": (
            "# MISIÓN: Distribuye munición de forma equitativa\n"
            "\n"
            "municion = 100\n"
            "tanques  = 7\n"
            "\n"
            "# Unidades por tanque (división entera, sin fracciones)\n"
            "por_tanque = municion ___ tanques\n"
            "print(por_tanque)\n"
            "\n"
            "# Unidades sobrantes (lo que queda después de repartir)\n"
            "sobrante = municion ___ tanques\n"
            "print(sobrante)\n"
        ),
        "expected_output": "14\n2",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El comandante del Sector 07 ordenó la redistribución de reservas de munición "
            "antes del siguiente turno de combate. No pueden darse fracciones de unidad "
            "— cada tanque recibe un número entero completo. "
            "El excedente que no puede dividirse equitativamente queda en el depósito "
            "central de DAKI para reserva estratégica."
        ),
        "pedagogical_objective": (
            "Usar // para división entera (cociente sin decimales). "
            "Usar % para el módulo (resto de la división). "
            "Ver la relación: municion == por_tanque * tanques + sobrante."
        ),
        "syntax_hint": (
            "por_tanque = municion // tanques   # 100 // 7 = 14\n"
            "sobrante   = municion % tanques    # 100 % 7  = 2"
        ),
        "theory_content": THEORY_N67,
        "hints_json": json.dumps([
            "El operador // hace división entera (descarta el decimal): 100 // 7 = 14.",
            "El operador % da el módulo (el resto): 100 % 7 = 2 (porque 14 × 7 = 98, y 100 - 98 = 2).",
            "Solución: por_tanque = municion // tanques y sobrante = municion % tanques",
        ]),
        "strict_match": True,
    },
    # ── NIVEL 68 — Fórmula de daño con input ─────────────────────────────────
    {
        "title": "Cálculo de Impacto",
        "description": (
            "El motor de combate del Nexo calcula el daño neto de un ataque "
            "usando la fórmula:\n\n"
            "```\ndano = max(0, round(ataque × multiplicador − defensa × 0.5))\n```\n\n"
            "Lee los tres parámetros de entrada (uno por línea) y aplica la fórmula.\n\n"
            "**Entradas:** `120`, `1.5`, `40`\n\n"
            "Salida esperada:\n"
            "```\n160\n```\n\n"
            "_(120 × 1.5 = 180.0 — 40 × 0.5 = 20.0 → 160.0 → round → 160)_"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "hard",
        "sector_id": 8,
        "level_order": 78,
        "base_xp_reward": 250,
        "is_project": False,
        "telemetry_goal_time": 200,
        "challenge_type": "python",
        "phase": "motores",
        "concepts_taught_json": json.dumps([
            "max()", "round()", "fórmula de combate", "input()", "float", "composición de funciones"
        ]),
        "initial_code": (
            "# MISIÓN: Implementa la fórmula de daño neto\n"
            "\n"
            "ataque        = int(input())\n"
            "multiplicador = float(input())\n"
            "defensa       = int(input())\n"
            "\n"
            "# Fórmula: max(0, round(ataque * multiplicador - defensa * 0.5))\n"
            "dano = ___(0, ___(ataque * ___ - defensa * 0.5))\n"
            "print(dano)\n"
        ),
        "expected_output": "160",
        "test_inputs_json": json.dumps(["120", "1.5", "40"]),
        "lore_briefing": (
            "El motor de física de combate del Nexo usa una fórmula de daño en dos pasos: "
            "primero multiplica el poder de ataque por el modificador del arma, "
            "luego resta la absorción de la defensa (50% del valor defensivo). "
            "round() ajusta al entero operativo y max(0, ...) garantiza que "
            "la defensa nunca invierte el daño convirtiéndolo en curación."
        ),
        "pedagogical_objective": (
            "Componer múltiples funciones matemáticas en una sola expresión. "
            "Usar max(0, x) como patrón de clamping mínimo. "
            "Combinar int() y float() para leer tipos diferentes con input()."
        ),
        "syntax_hint": (
            "dano = max(0, round(ataque * multiplicador - defensa * 0.5))"
        ),
        "theory_content": THEORY_N68,
        "hints_json": json.dumps([
            "La fórmula tiene dos capas: primero round() redondea el cálculo, luego max(0, ...) garantiza que no sea negativo.",
            "El multiplicador se lee como float(input()). ataque * multiplicador da 120 * 1.5 = 180.0.",
            "Completa los blancos: dano = max(0, round(ataque * multiplicador - defensa * 0.5))",
        ]),
        "strict_match": True,
    },
    # ── NIVEL 69 — Motor de combate con múltiples ataques ────────────────────
    {
        "title": "Motor de Física",
        "description": (
            "El simulador de combate del Nexo procesa una ráfaga de N ataques "
            "contra un objetivo con 100 HP y defensa fija de 5 puntos. "
            "Cada ataque reduce el HP por `max(0, ataque - defensa)`.\n\n"
            "Lee N ataques (uno por línea) y calcula el daño total acumulado "
            "y el HP final del objetivo.\n\n"
            "**Entradas:** `3`, `20`, `8`, `35`\n\n"
            "Salida esperada:\n"
            "```\n48\n52\n```\n\n"
            "_(20−5=15, 8−5=3, 35−5=30 → total=48, HP=100−48=52)_"
        ),
        "difficulty_tier": DifficultyTier.ADVANCED,
        "difficulty": "hard",
        "sector_id": 8,
        "level_order": 79,
        "base_xp_reward": 350,
        "is_project": False,
        "telemetry_goal_time": 300,
        "challenge_type": "python",
        "phase": "motores",
        "concepts_taught_json": json.dumps([
            "max()", "acumulador", "input()", "for + range", "simulación",
            "composición de funciones", "motor de cálculo"
        ]),
        "initial_code": (
            "# MISIÓN: Simula N ataques y calcula el daño total y HP final\n"
            "\n"
            "n       = int(input())\n"
            "hp      = 100\n"
            "defensa = 5\n"
            "dano_total = 0\n"
            "\n"
            "for _ in range(n):\n"
            "    ataque    = int(input())\n"
            "    # Daño neto: el ataque menos la defensa, mínimo 0\n"
            "    dano_neto  = ___(0, ataque - defensa)\n"
            "    dano_total += dano_neto\n"
            "\n"
            "# HP final: el HP inicial menos el daño total, mínimo 0\n"
            "hp_final = ___(0, hp - dano_total)\n"
            "print(dano_total)\n"
            "print(hp_final)\n"
        ),
        "expected_output": "48\n52",
        "test_inputs_json": json.dumps(["3", "20", "8", "35"]),
        "lore_briefing": (
            "El simulador táctico de DAKI necesita predecir el resultado de una ráfaga "
            "de ataques enemigos antes de que el enfrentamiento ocurra. "
            "Cada proyectil tiene un poder de ataque diferente, y la defensa del objetivo "
            "absorbe parte del daño de cada impacto. El motor calcula el HP "
            "restante después de toda la ráfaga para que el comando pueda "
            "decidir si el objetivo sobrevivirá o necesita refuerzos urgentes."
        ),
        "pedagogical_objective": (
            "Construir un motor de cálculo iterativo: leer N valores, "
            "aplicar fórmula por cada uno, acumular con +=. "
            "Usar max() tanto para el daño neto por golpe como para el HP final. "
            "Integra: for+range, input(), acumulador, max(), composición de funciones."
        ),
        "syntax_hint": (
            "for _ in range(n):\n"
            "    ataque    = int(input())\n"
            "    dano_neto  = max(0, ataque - defensa)\n"
            "    dano_total += dano_neto\n"
            "\n"
            "hp_final = max(0, hp - dano_total)"
        ),
        "theory_content": THEORY_N69,
        "hints_json": json.dumps([
            "Dentro del for, max(0, ataque - defensa) calcula el daño neto de cada golpe (nunca negativo).",
            "Acumula el daño neto con: dano_total += dano_neto",
            "Fuera del for, hp_final = max(0, hp - dano_total) asegura que el HP no baje de 0.",
        ]),
        "strict_match": True,
    },
]


# ─── Lógica de población ──────────────────────────────────────────────────────

async def seed() -> None:
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with SessionLocal() as session:
        # Idempotente: elimina solo niveles 61–69 (preserva el CONTRATO-70)
        deleted = await session.execute(
            delete(Challenge).where(
                Challenge.sector_id == 8,
                Challenge.level_order < 70,
            )
        )
        deleted_count = deleted.rowcount
        await session.flush()
        print(f"🧹  Sector 07 (61-69) anterior eliminado — {deleted_count} challenge(s) removidos.")

        print(f"\n🌱  Insertando {len(SECTOR_08)} niveles del Sector 07...\n")
        for data in SECTOR_08:
            challenge = Challenge(**data)
            session.add(challenge)
            print(
                f"    [{data['level_order']:02d}/69] {data['title']:<38} "
                f"({data['difficulty'].upper()}, {data['base_xp_reward']} XP, "
                f"~{data['telemetry_goal_time']}s)"
            )

        await session.commit()

    await engine.dispose()
    print(f"\n✅  Sector 07 cargado — {len(SECTOR_08)} niveles listos.")
    print("    Boss CONTRATO-70 preservado (gestionar con seed_contratos.py)\n")


if __name__ == "__main__":
    asyncio.run(seed())
