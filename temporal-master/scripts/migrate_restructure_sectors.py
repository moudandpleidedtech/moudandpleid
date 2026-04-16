"""
migrate_restructure_sectors.py — Reestructura pedagógica DAKI EdTech
======================================================================
Inserta Sector 04 (Funciones, L31–40) y Sector 22 (Recursión, L190–194).
Desplaza todos los sectores y niveles existentes ≥ S04 / L31.

Cambios en DB:
  • UPDATE challenges SET level_order = level_order + 10 WHERE level_order >= 31
  • UPDATE challenges SET sector_id  = sector_id  +  1 WHERE sector_id  >= 4
  • INSERT 10 challenges nuevos: sector_id=4, level_orders 31–40  (Funciones)
  • INSERT  5 challenges nuevos: sector_id=22, level_orders 190–194 (Recursión)

Cambios en disco (seed files):
  • Renombra seed_sector_04.py → seed_sector_05.py ... seed_sector_20.py → seed_sector_21.py
  • Actualiza sector_id y level_order dentro de cada archivo renombrado
  • Crea nuevo seed_sector_04.py (Funciones) [marker — el contenido canónico
    vive en este mismo script como NEW_FUNCTIONS_CHALLENGES]
  • Crea seed_sector_22.py (Recursión) [idem]

Uso:
    python -m scripts.migrate_restructure_sectors              # aplica todo
    python -m scripts.migrate_restructure_sectors --dry-run    # solo muestra el plan
    python -m scripts.migrate_restructure_sectors --db-only    # solo DB, no toca archivos
    python -m scripts.migrate_restructure_sectors --files-only # solo archivos, no DB

ADVERTENCIA: Hacer backup de la DB antes de ejecutar en producción.
La migración es idempotente en DB si se ejecuta dos veces en el mismo estado.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import re
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.models.challenge import Challenge, DifficultyTier

# ─────────────────────────────────────────────────────────────────────────────
# THEORY CONTENT — Sector 04: Funciones
# ─────────────────────────────────────────────────────────────────────────────

THEORY_F31 = """\
## PROTOCOLO: Funciones — El Módulo Reutilizable

Una **función** es un bloque de código con nombre que puedes ejecutar
cuantas veces necesites usando su nombre seguido de `()`.

```python
def activar_nexo():
    print("NEXO ACTIVADO")

activar_nexo()   # ejecuta el bloque
activar_nexo()   # lo ejecuta de nuevo
```

- `def` → declara la función
- `activar_nexo` → es el nombre (elige nombres descriptivos)
- `():` → paréntesis vacíos + dos puntos obligatorios
- El bloque indentado es el **cuerpo** de la función

---

## REGLA DE ORO

Define la función **antes** de llamarla.
Python lee de arriba hacia abajo: si llamás antes de definir, obtenés `NameError`.
"""

THEORY_F32 = """\
## PROTOCOLO: Parámetros — Funciones que Reciben Datos

Un **parámetro** es una variable especial que recibe un valor cuando la función es llamada.

```python
def saludar(nombre):
    print(f"Operador {nombre} conectado")

saludar("REX")    # nombre = "REX"
saludar("DAKI")   # nombre = "DAKI"
```

- El parámetro (`nombre`) vive **solo dentro** de la función
- El **argumento** es el valor que pasás al llamar: `"REX"`, `"DAKI"`
- Podés llamar la misma función con distintos argumentos → reutilización

---

## DIFERENCIA: parámetro vs argumento

| Concepto     | Dónde aparece | Ejemplo           |
|--------------|---------------|-------------------|
| Parámetro    | En `def`      | `def f(nombre):`  |
| Argumento    | En la llamada | `f("REX")`        |
"""

THEORY_F33 = """\
## PROTOCOLO: return — La Función que Responde

`return` hace que la función **devuelva** un valor al código que la llamó.

```python
def calcular_escudo(nivel):
    return nivel * 15

escudo = calcular_escudo(4)
print(escudo)   # 60
```

- Sin `return` la función devuelve `None` (nada útil)
- `return` **termina** la función inmediatamente
- El valor retornado puede guardarse en una variable o usarse directo

---

## print vs return — La Confusión Clásica

```python
def doble_malo(x):
    print(x * 2)       # imprime, NO devuelve nada

def doble_bueno(x):
    return x * 2       # devuelve el valor → lo podés usar

resultado = doble_bueno(5)   # resultado = 10
```

`print` muestra en consola. `return` devuelve un valor para ser usado.
"""

THEORY_F34 = """\
## PROTOCOLO: Múltiples Parámetros

Una función puede recibir más de un parámetro, separados por comas.

```python
def frecuencia(base, amplitud):
    return base + amplitud * 2

print(frecuencia(10, 5))   # 20
print(frecuencia(3, 4))    # 11
```

- Los argumentos se asignan **en orden**: primero → primero, segundo → segundo
- Podés pasar variables, literales o expresiones como argumentos

---

## EJEMPLO CON STRINGS

```python
def identificar(operador, sector):
    return f"{operador} asignado al Sector {sector}"

print(identificar("REX", 4))
# REX asignado al Sector 4
```
"""

THEORY_F35 = """\
## PROTOCOLO: Funciones que Retornan Booleanos

Las funciones pueden retornar `True` o `False` directamente.
Esto es muy útil para crear **verificadores** o **validadores**.

```python
def tiene_acceso(nivel):
    return nivel >= 5

print(tiene_acceso(7))   # True
print(tiene_acceso(3))   # False
```

- `return nivel >= 5` evalúa la comparación y retorna el resultado booleano
- Podés usar estas funciones directamente en `if`:
  ```python
  if tiene_acceso(nivel_usuario):
      print("Acceso concedido")
  ```

---

## REGLA DE ORO

No escribas `return True` / `return False` en lados opuestos de un `if`
cuando podés simplemente `return condicion`.
"""

THEORY_F36 = """\
## PROTOCOLO: Lógica Compleja en Funciones

Las funciones pueden contener `if/elif/else` para retornar distintos resultados.

```python
def clasificar(nivel, activo):
    if nivel >= 8 and activo:
        return "ÉLITE"
    elif nivel >= 4:
        return "OPERATIVO"
    else:
        return "RECLUTA"
```

- Cada rama del `if` puede tener su propio `return`
- Cuando Python ejecuta un `return`, la función termina ahí
- `and` / `or` permiten combinar condiciones en una sola línea

---

## FLUJO DE EJECUCIÓN

```
clasificar(9, True)  → nivel >= 8 AND activo → "ÉLITE"
clasificar(5, False) → nivel >= 4 (sin importar activo) → "OPERATIVO"
clasificar(2, True)  → ninguna condición → "RECLUTA"
```
"""

THEORY_F37 = """\
## PROTOCOLO: Valores por Defecto

Un parámetro puede tener un **valor por defecto** que se usa cuando no se pasa argumento.

```python
def estado(operador, sector=0):
    print(f"{operador} — Sector {sector}")

estado("REX", 4)   # REX — Sector 4
estado("DAKI")     # DAKI — Sector 0  (usa el default)
```

- El parámetro con default va **siempre al final** del paréntesis
- Si pasás el argumento, sobreescribe el default
- Útil para opciones que tienen un comportamiento "normal" y uno "especial"

---

## CASO REAL

```python
def activar(nombre, potencia=100, modo="normal"):
    print(f"{nombre}: {potencia}% — modo {modo}")

activar("REX")                  # REX: 100% — modo normal
activar("DAKI", 75, "sigilo")   # DAKI: 75% — modo sigilo
```
"""

THEORY_F38 = """\
## PROTOCOLO: Scope — El Alcance de las Variables

Las variables creadas **dentro** de una función solo existen mientras la función se ejecuta.
Esto se llama **scope local**.

```python
def calcular():
    resultado = 42    # variable LOCAL
    return resultado

calcular()
# print(resultado)  ← ERROR: resultado no existe fuera de la función
```

- Las variables locales no "contaminan" el espacio global
- Cada llamada a la función crea su propio scope aislado

---

## IMPLICANCIA TÁCTICA

```python
def suma(a, b):
    total = a + b    # 'total' es local
    return total     # devolvemos el valor antes de que desaparezca

resultado = suma(3, 4)  # capturamos el valor retornado
print(resultado)        # 7
```

Si no hacés `return`, el valor calculado se pierde cuando la función termina.
"""

THEORY_F39 = """\
## PROTOCOLO: Composición — Funciones que Llaman Funciones

Una función puede llamar a otra función. Esto se llama **composición**.

```python
def doble(x):
    return x * 2

def cuadruple(x):
    return doble(doble(x))   # llama a doble dos veces

print(cuadruple(3))   # 12
```

- `cuadruple` usa `doble` como un bloque de construcción
- La salida de una función puede ser el argumento de otra
- Este es el principio de **reutilización de código**

---

## PIPELINE TÁCTICO

```python
def limpiar(texto):
    return texto.strip().lower()

def formatear(texto):
    limpio = limpiar(texto)   # usa limpiar
    return f"[{limpio}]"

print(formatear("  REX  "))   # [rex]
```
"""

THEORY_F40 = """\
## NEXUS-04: Arquitectura de Funciones

Has llegado al Boss del Sector 04. Este desafío integra **todo** lo que aprendiste:

1. `def` y llamadas a funciones
2. Parámetros y `return`
3. Funciones con lógica (`if/elif/else`)
4. Parámetros con valores por defecto
5. Composición: una función llama a otra

---

## MISIÓN

Construí un sistema de 4 funciones que colaboran:

```
xp_requerido(nivel) → calcula el XP necesario para ese nivel
tiene_xp(xp_actual, nivel) → verifica si el operador tiene suficiente XP
rango(nivel) → retorna el nombre del rango según el nivel
reporte(nombre, nivel, xp_actual) → usa las 3 funciones anteriores
```

Este es el patrón fundamental de la ingeniería de software:
**funciones pequeñas y específicas que se combinan para resolver problemas complejos**.
"""

# ─────────────────────────────────────────────────────────────────────────────
# THEORY CONTENT — Sector 22: Recursión
# ─────────────────────────────────────────────────────────────────────────────

THEORY_R190 = """\
## PROTOCOLO: Recursión — La Función que se Llama a Sí Misma

Una función **recursiva** es aquella que se llama a sí misma dentro de su cuerpo.

```python
def cuenta_regresiva(n):
    if n == 0:          # CASO BASE — detiene la recursión
        print("¡FUEGO!")
        return
    print(n)
    cuenta_regresiva(n - 1)   # LLAMADA RECURSIVA — n se reduce

cuenta_regresiva(3)
# 3
# 2
# 1
# ¡FUEGO!
```

---

## ESTRUCTURA DE TODA FUNCIÓN RECURSIVA

1. **Caso base**: la condición que DETIENE la recursión (imprescindible)
2. **Llamada recursiva**: la función se llama con un argumento más pequeño

Sin caso base → recursión infinita → `RecursionError`.
"""

THEORY_R191 = """\
## PROTOCOLO: Recursión con return

Las funciones recursivas pueden **retornar valores** acumulados.

```python
def factorial(n):
    if n == 0:           # caso base
        return 1
    return n * factorial(n - 1)   # recursiva con return

print(factorial(5))   # 120
```

Traza mental:
```
factorial(5)
  = 5 * factorial(4)
  = 5 * (4 * factorial(3))
  = 5 * 4 * 3 * 2 * 1
  = 120
```

---

## REGLA DE ORO

Cada llamada recursiva debe acercarse al caso base.
Si n no decrece, la recursión nunca termina.
"""

THEORY_R192 = """\
## PROTOCOLO: Recursión con Doble Llamada

Algunas funciones hacen **dos llamadas recursivas** por cada nivel.

```python
def fibonacci(n):
    if n <= 1:               # caso base (n=0 → 0, n=1 → 1)
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

El árbol de llamadas crece exponencialmente:
```
fibonacci(4)
├── fibonacci(3)
│   ├── fibonacci(2) → fibonacci(1) + fibonacci(0)
│   └── fibonacci(1)
└── fibonacci(2)
    ├── fibonacci(1)
    └── fibonacci(0)
```

---

## NOTA PEDAGÓGICA

Esta implementación es O(2ⁿ) — exponencial. En producción se usa
memoización o iteración. Pero para aprender recursión es el ejemplo
más claro de ramificación.
"""

THEORY_R193 = """\
## PROTOCOLO: Recursión sobre Estructuras

La recursión también funciona con **listas**. Podés procesar el primer elemento
y llamarte con el resto.

```python
def suma_lista(lista):
    if len(lista) == 0:        # caso base: lista vacía
        return 0
    return lista[0] + suma_lista(lista[1:])   # cabeza + cola recursiva

print(suma_lista([1, 2, 3, 4]))   # 10
```

- `lista[0]` → el primer elemento (cabeza)
- `lista[1:]` → el resto de la lista (cola) — cada vez más pequeña

---

## ANALOGÍA

Pensá en una pila de cartas. En cada llamada tomás la carta de arriba y
procesás el resto de la pila. Cuando la pila está vacía, terminaste.
"""

THEORY_R194 = """\
## NEXUS-22: El Laberinto del Nexo

El Boss final del Sector 22. Integrás **todo** lo aprendido sobre recursión:

1. Caso base correcto
2. Llamada recursiva que reduce el problema
3. Recursión con retorno numérico
4. Recursión sobre strings
5. Recursión sobre listas (estructura anidada)

---

## MISIÓN

Implementá 3 funciones recursivas que no se tocan entre sí:

```
potencia(base, exp)    → base^exp sin usar **
es_palindromo(s)       → True/False comparando primer y último caracter
aplanar(lista)         → convierte lista anidada en lista plana
```

Cada función es un problema clásico de recursión que aparece en
entrevistas técnicas y fundamentos de ciencias de la computación.
"""

# ─────────────────────────────────────────────────────────────────────────────
# CHALLENGES — Sector 04: Funciones (L31–L40)
# ─────────────────────────────────────────────────────────────────────────────

NEW_FUNCTIONS_CHALLENGES: list[dict] = [
    # ── L31 — def sin parámetros ──────────────────────────────────────────────
    {
        "title": "Primera Transmisión",
        "description": (
            "Creá tu primera función. Define `transmitir()` que imprima "
            "`TRANSMISION INICIADA`. Llamala **dos veces** para verificar que "
            "funciona.\n\n"
            "Salida esperada:\n"
            "```\nTRANSMISION INICIADA\nTRANSMISION INICIADA\n```"
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "easy",
        "sector_id": 4,
        "level_order": 31,
        "base_xp_reward": 100,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 90,
        "challenge_type": "python",
        "phase": "funciones",
        "concepts_taught_json": json.dumps(["def", "llamada a función", "reutilización"]),
        "initial_code": (
            "# MISIÓN: Define la función y llámala dos veces\n"
            "\n"
            "def transmitir():\n"
            "    ___\n"
            "\n"
            "transmitir()\n"
            "transmitir()\n"
        ),
        "expected_output": "TRANSMISION INICIADA\nTRANSMISION INICIADA",
        "test_inputs_json": json.dumps([]),
        "strict_match": True,
        "lore_briefing": (
            "El Sector 04 requiere inicializar el protocolo de transmisión. "
            "DAKI detectó que el equipo repite la misma instrucción varias veces. "
            "Una función resuelve eso: escribís el código una sola vez y lo llamás "
            "cuantas veces necesitás."
        ),
        "pedagogical_objective": (
            "Introducir `def` y la mecánica de llamar una función. "
            "Demostrar la reutilización: definís una vez, ejecutás muchas."
        ),
        "syntax_hint": "def transmitir():\n    print('TRANSMISION INICIADA')",
        "theory_content": THEORY_F31,
        "hints_json": json.dumps([
            "Una función se define con `def nombre():` seguido de un bloque indentado.",
            "Dentro de la función escribí `print('TRANSMISION INICIADA')`.",
            "Para llamarla: `transmitir()` — el nombre seguido de paréntesis.",
        ]),
        "is_free": False,
        "is_ironman": False,
    },
    # ── L32 — def con 1 parámetro ─────────────────────────────────────────────
    {
        "title": "Canal Personalizado",
        "description": (
            "Define `identificar(operador)` que imprima `Operador: X` donde X "
            "es el argumento recibido. Llamala con `\"NEXO\"` y con `\"DAKI\"`.\n\n"
            "Salida esperada:\n"
            "```\nOperador: NEXO\nOperador: DAKI\n```"
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "easy",
        "sector_id": 4,
        "level_order": 32,
        "base_xp_reward": 110,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 100,
        "challenge_type": "python",
        "phase": "funciones",
        "concepts_taught_json": json.dumps(["parámetros", "argumentos", "f-string"]),
        "initial_code": (
            "# MISIÓN: Define la función con un parámetro\n"
            "\n"
            "def identificar(operador):\n"
            "    print(f\"Operador: ___\")\n"
            "\n"
            "identificar(\"NEXO\")\n"
            "identificar(\"DAKI\")\n"
        ),
        "expected_output": "Operador: NEXO\nOperador: DAKI",
        "test_inputs_json": json.dumps([]),
        "strict_match": True,
        "lore_briefing": (
            "El sistema de identificación del Nexo necesita saludar a cada operador "
            "por su nombre. La misma función, distintos datos — eso es exactamente para "
            "qué sirven los parámetros."
        ),
        "pedagogical_objective": (
            "Introducir parámetros. Diferenciar parámetro (en def) de argumento (en llamada). "
            "Usar el parámetro dentro de la función con f-string."
        ),
        "syntax_hint": "def identificar(operador):\n    print(f'Operador: {operador}')",
        "theory_content": THEORY_F32,
        "hints_json": json.dumps([
            "El parámetro `operador` es como una variable que recibe el valor al llamar la función.",
            "Usá f-string: `print(f'Operador: {operador}')` para insertar el valor.",
            "Llamás la función con el valor que querés: `identificar('NEXO')`.",
        ]),
        "is_free": False,
        "is_ironman": False,
    },
    # ── L33 — return vs print ─────────────────────────────────────────────────
    {
        "title": "Señal de Retorno",
        "description": (
            "Define `calcular_escudo(nivel)` que **retorne** `nivel * 15` "
            "(sin imprimir). Luego guardá el resultado en una variable e "
            "imprimilo.\n\n"
            "Llamala con `nivel = 4` y con `nivel = 7`.\n\n"
            "Salida esperada:\n"
            "```\n60\n105\n```"
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "easy",
        "sector_id": 4,
        "level_order": 33,
        "base_xp_reward": 120,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 110,
        "challenge_type": "python",
        "phase": "funciones",
        "concepts_taught_json": json.dumps(["return", "print vs return", "variables"]),
        "initial_code": (
            "# MISIÓN: La función debe retornar, no imprimir\n"
            "\n"
            "def calcular_escudo(nivel):\n"
            "    return ___\n"
            "\n"
            "escudo1 = calcular_escudo(4)\n"
            "print(escudo1)\n"
            "\n"
            "escudo2 = calcular_escudo(7)\n"
            "print(escudo2)\n"
        ),
        "expected_output": "60\n105",
        "test_inputs_json": json.dumps([]),
        "strict_match": True,
        "lore_briefing": (
            "El módulo de defensa del Nexo calcula el nivel de escudo pero no lo muestra "
            "directamente — lo retorna para que otros módulos lo usen. "
            "La diferencia entre `return` y `print` es fundamental: `print` muestra, "
            "`return` devuelve un valor que se puede usar más adelante."
        ),
        "pedagogical_objective": (
            "Establecer la distinción entre `print` y `return`. "
            "Mostrar que el valor retornado puede capturarse en una variable."
        ),
        "syntax_hint": "return nivel * 15",
        "theory_content": THEORY_F33,
        "hints_json": json.dumps([
            "La función debe usar `return`, no `print`.",
            "return nivel * 15 calcula y devuelve el resultado.",
            "Capturá el resultado: escudo1 = calcular_escudo(4) y luego print(escudo1).",
        ]),
        "is_free": False,
        "is_ironman": False,
    },
    # ── L34 — múltiples parámetros ────────────────────────────────────────────
    {
        "title": "Frecuencia Combinada",
        "description": (
            "Define `combinar_señal(base, amplitud)` que retorne `base + amplitud * 2`.\n\n"
            "Llamala con `(10, 5)` y con `(3, 4)` e imprimí los resultados.\n\n"
            "Salida esperada:\n"
            "```\n20\n11\n```"
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "easy",
        "sector_id": 4,
        "level_order": 34,
        "base_xp_reward": 120,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 120,
        "challenge_type": "python",
        "phase": "funciones",
        "concepts_taught_json": json.dumps(["múltiples parámetros", "return", "operadores"]),
        "initial_code": (
            "# MISIÓN: Función con dos parámetros\n"
            "\n"
            "def combinar_señal(base, amplitud):\n"
            "    return ___\n"
            "\n"
            "print(combinar_señal(10, 5))\n"
            "print(combinar_señal(3, 4))\n"
        ),
        "expected_output": "20\n11",
        "test_inputs_json": json.dumps([]),
        "strict_match": True,
        "lore_briefing": (
            "El amplificador de señales del Nexo combina una frecuencia base con su amplitud. "
            "Múltiples parámetros permiten que una función trabaje con varios datos a la vez."
        ),
        "pedagogical_objective": (
            "Consolidar el uso de múltiples parámetros y `return` con una expresión aritmética."
        ),
        "syntax_hint": "return base + amplitud * 2",
        "theory_content": THEORY_F34,
        "hints_json": json.dumps([
            "La función recibe dos parámetros: base y amplitud.",
            "La fórmula es base + amplitud * 2.",
            "Usá return para devolver el resultado.",
        ]),
        "is_free": False,
        "is_ironman": False,
    },
    # ── L35 — return booleano ─────────────────────────────────────────────────
    {
        "title": "Verificador de Acceso",
        "description": (
            "Define `tiene_acceso(nivel)` que retorne `True` si `nivel >= 5`, "
            "`False` si no.\n\n"
            "Imprimí el resultado para `nivel = 7` y `nivel = 3`.\n\n"
            "Salida esperada:\n"
            "```\nTrue\nFalse\n```"
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "medium",
        "sector_id": 4,
        "level_order": 35,
        "base_xp_reward": 150,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 130,
        "challenge_type": "python",
        "phase": "funciones",
        "concepts_taught_json": json.dumps(["return bool", "comparadores", ">=", "funciones predicado"]),
        "initial_code": (
            "# MISIÓN: La función retorna True o False\n"
            "\n"
            "def tiene_acceso(nivel):\n"
            "    return ___\n"
            "\n"
            "print(tiene_acceso(7))\n"
            "print(tiene_acceso(3))\n"
        ),
        "expected_output": "True\nFalse",
        "test_inputs_json": json.dumps([]),
        "strict_match": True,
        "lore_briefing": (
            "El sistema de control de acceso del Nexo verifica si un operador tiene el nivel "
            "mínimo requerido. En lugar de escribir `if nivel >= 5: return True` y "
            "`else: return False`, podés simplemente retornar la comparación directamente."
        ),
        "pedagogical_objective": (
            "Enseñar que `return nivel >= 5` retorna un booleano directamente. "
            "Evitar el antipatrón `if cond: return True else: return False`."
        ),
        "syntax_hint": "return nivel >= 5",
        "theory_content": THEORY_F35,
        "hints_json": json.dumps([
            "Una comparación como `nivel >= 5` ya ES True o False.",
            "Podés hacer directamente `return nivel >= 5` sin if/else.",
            "No necesitás escribir `if nivel >= 5: return True` — es redundante.",
        ]),
        "is_free": False,
        "is_ironman": False,
    },
    # ── L36 — if/elif/else + and/or ───────────────────────────────────────────
    {
        "title": "Clasificador de Amenaza",
        "description": (
            "Define `clasificar(nivel, activo)` que retorne:\n"
            "- `\"ELITE\"` si `nivel >= 8` **y** `activo` es `True`\n"
            "- `\"OPERATIVO\"` si `nivel >= 4`\n"
            "- `\"RECLUTA\"` en cualquier otro caso\n\n"
            "Salida esperada:\n"
            "```\nELITE\nOPERATIVO\nRECLUTA\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 4,
        "level_order": 36,
        "base_xp_reward": 175,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 180,
        "challenge_type": "python",
        "phase": "funciones",
        "concepts_taught_json": json.dumps(["if/elif/else", "and", "lógica en funciones", "return múltiple"]),
        "initial_code": (
            "# MISIÓN: Clasificador con lógica interna\n"
            "\n"
            "def clasificar(nivel, activo):\n"
            "    if nivel >= 8 and ___:\n"
            "        return \"ELITE\"\n"
            "    elif nivel >= ___:\n"
            "        return \"OPERATIVO\"\n"
            "    else:\n"
            "        return \"RECLUTA\"\n"
            "\n"
            "print(clasificar(9, True))\n"
            "print(clasificar(5, False))\n"
            "print(clasificar(2, True))\n"
        ),
        "expected_output": "ELITE\nOPERATIVO\nRECLUTA",
        "test_inputs_json": json.dumps([]),
        "strict_match": True,
        "lore_briefing": (
            "El sistema de clasificación táctica del Nexo evalúa a cada operador. "
            "Solo los que tienen nivel alto Y están activos alcanzan el rango ELITE. "
            "`and` requiere que **ambas** condiciones sean verdaderas."
        ),
        "pedagogical_objective": (
            "Usar if/elif/else dentro de funciones. "
            "Practicar `and` para condiciones compuestas. "
            "Reforzar que cada rama puede tener su propio `return`."
        ),
        "syntax_hint": "if nivel >= 8 and activo:\n    return 'ELITE'",
        "theory_content": THEORY_F36,
        "hints_json": json.dumps([
            "La primera condición requiere nivel >= 8 AND activo == True.",
            "`and activo` es equivalente a `and activo == True` — los booleanos ya son True/False.",
            "elif cubre nivel >= 4 (sin importar activo). else cubre todo lo demás.",
        ]),
        "is_free": False,
        "is_ironman": False,
    },
    # ── L37 — parámetro con valor por defecto ─────────────────────────────────
    {
        "title": "Protocolo por Defecto",
        "description": (
            "Define `activar(nombre, potencia=100)` que imprima "
            "`X activado al Y%`.\n\n"
            "Llamala con `(\"NEXO\", 75)` y solo con `(\"DAKI\")` "
            "(usando el valor por defecto).\n\n"
            "Salida esperada:\n"
            "```\nNEXO activado al 75%\nDAKI activado al 100%\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 4,
        "level_order": 37,
        "base_xp_reward": 175,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 150,
        "challenge_type": "python",
        "phase": "funciones",
        "concepts_taught_json": json.dumps(["default param", "parámetros opcionales", "f-string"]),
        "initial_code": (
            "# MISIÓN: Un parámetro tiene valor por defecto\n"
            "\n"
            "def activar(nombre, potencia=___):\n"
            "    print(f\"{nombre} activado al {potencia}%\")\n"
            "\n"
            "activar(\"NEXO\", 75)\n"
            "activar(\"DAKI\")\n"
        ),
        "expected_output": "NEXO activado al 75%\nDAKI activado al 100%",
        "test_inputs_json": json.dumps([]),
        "strict_match": True,
        "lore_briefing": (
            "La mayoría de los módulos del Nexo se activan al 100% de potencia por defecto. "
            "Solo en misiones especiales se ajusta la potencia. "
            "Los valores por defecto hacen que los argumentos sean opcionales."
        ),
        "pedagogical_objective": (
            "Introducir parámetros con valores por defecto. "
            "Mostrar que se puede omitir el argumento si el default es suficiente."
        ),
        "syntax_hint": "def activar(nombre, potencia=100):",
        "theory_content": THEORY_F37,
        "hints_json": json.dumps([
            "El valor por defecto se define en def: `def activar(nombre, potencia=100):`.",
            "Cuando llamás `activar('DAKI')`, potencia toma el valor 100 automáticamente.",
            "Cuando llamás `activar('NEXO', 75)`, potencia toma el valor 75.",
        ]),
        "is_free": False,
        "is_ironman": False,
    },
    # ── L38 — scope local ─────────────────────────────────────────────────────
    {
        "title": "Zona de Alcance",
        "description": (
            "Define `procesar(valor)` que cree una variable local `resultado = valor * 3 + 10` "
            "y la retorne.\n\n"
            "Imprimí el resultado para `valor = 5` y `valor = 8`.\n\n"
            "Salida esperada:\n"
            "```\n25\n34\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 4,
        "level_order": 38,
        "base_xp_reward": 175,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 150,
        "challenge_type": "python",
        "phase": "funciones",
        "concepts_taught_json": json.dumps(["scope local", "variables locales", "return"]),
        "initial_code": (
            "# MISIÓN: Usá una variable local dentro de la función\n"
            "\n"
            "def procesar(valor):\n"
            "    resultado = ___\n"
            "    return resultado\n"
            "\n"
            "print(procesar(5))\n"
            "print(procesar(8))\n"
        ),
        "expected_output": "25\n34",
        "test_inputs_json": json.dumps([]),
        "strict_match": True,
        "lore_briefing": (
            "El procesador de señales del Nexo trabaja en un espacio aislado: "
            "sus variables no interfieren con el exterior. "
            "Las variables definidas dentro de una función son **locales** — "
            "existen solo mientras la función se ejecuta."
        ),
        "pedagogical_objective": (
            "Introducir el concepto de scope local. "
            "Mostrar que las variables dentro de la función son propias de ella "
            "y que hay que retornar el valor para usarlo afuera."
        ),
        "syntax_hint": "resultado = valor * 3 + 10",
        "theory_content": THEORY_F38,
        "hints_json": json.dumps([
            "Creá la variable: `resultado = valor * 3 + 10`.",
            "Luego retornala: `return resultado`.",
            "5 * 3 + 10 = 25 ✓   8 * 3 + 10 = 34 ✓",
        ]),
        "is_free": False,
        "is_ironman": False,
    },
    # ── L39 — composición de funciones ────────────────────────────────────────
    {
        "title": "Cadena de Mando",
        "description": (
            "Define dos funciones:\n"
            "- `duplicar(x)` → retorna `x * 2`\n"
            "- `cuadruple(x)` → usa `duplicar` dos veces y retorna el resultado\n\n"
            "Imprimí `cuadruple(3)` y `cuadruple(5)`.\n\n"
            "Salida esperada:\n"
            "```\n12\n20\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 4,
        "level_order": 39,
        "base_xp_reward": 200,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 180,
        "challenge_type": "python",
        "phase": "funciones",
        "concepts_taught_json": json.dumps(["composición", "función que llama función", "reutilización"]),
        "initial_code": (
            "# MISIÓN: Una función usa a otra\n"
            "\n"
            "def duplicar(x):\n"
            "    return ___\n"
            "\n"
            "def cuadruple(x):\n"
            "    return duplicar(___)\n"
            "\n"
            "print(cuadruple(3))\n"
            "print(cuadruple(5))\n"
        ),
        "expected_output": "12\n20",
        "test_inputs_json": json.dumps([]),
        "strict_match": True,
        "lore_briefing": (
            "La jerarquía táctica del Nexo usa módulos anidados: un módulo de alto nivel "
            "coordina módulos más simples. Cuadruple llama a duplicar dos veces — "
            "eso es composición de funciones: bloques pequeños que forman soluciones grandes."
        ),
        "pedagogical_objective": (
            "Introducir la composición: una función puede llamar a otra. "
            "Reforzar que la salida de una función puede ser el argumento de otra."
        ),
        "syntax_hint": "def cuadruple(x):\n    return duplicar(duplicar(x))",
        "theory_content": THEORY_F39,
        "hints_json": json.dumps([
            "`duplicar(x)` retorna x * 2.",
            "`cuadruple` debe llamar a `duplicar` con el resultado de `duplicar(x)`.",
            "duplicar(duplicar(3)) = duplicar(6) = 12 ✓",
        ]),
        "is_free": False,
        "is_ironman": False,
    },
    # ── L40 — BOSS: 4 funciones colaborando ──────────────────────────────────
    {
        "title": "NEXUS-04: Arquitectura del Nexo",
        "description": (
            "**MISIÓN BOSS** — Construí 4 funciones que colaboran:\n\n"
            "1. `xp_requerido(nivel)` → retorna `nivel * 100`\n"
            "2. `tiene_xp(xp_actual, nivel)` → retorna `True` si `xp_actual >= xp_requerido(nivel)`\n"
            "3. `rango(nivel)` → retorna `\"NEXUS\"` si `nivel >= 8`, `\"COMANDO\"` si `nivel >= 5`, `\"BASE\"` si no\n"
            "4. `reporte(nombre, nivel, xp_actual)` → imprime el reporte usando las 3 funciones anteriores\n\n"
            "Llamá `reporte(\"REX\", 6, 550)` y `reporte(\"GHOST\", 3, 200)`.\n\n"
            "Salida esperada:\n"
            "```\nREX | Rango: COMANDO | XP: 550/600 | Acceso: False\n"
            "GHOST | Rango: BASE | XP: 200/300 | Acceso: False\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "hard",
        "sector_id": 4,
        "level_order": 40,
        "base_xp_reward": 450,
        "is_project": True,
        "is_phase_boss": True,
        "telemetry_goal_time": 480,
        "challenge_type": "python",
        "phase": "funciones",
        "concepts_taught_json": json.dumps([
            "composición de funciones", "if/elif/else", "return bool",
            "parámetros", "f-string", "integración"
        ]),
        "initial_code": (
            "# BOSS MISSION: 4 funciones colaborando\n"
            "\n"
            "def xp_requerido(nivel):\n"
            "    return ___\n"
            "\n"
            "def tiene_xp(xp_actual, nivel):\n"
            "    return xp_actual >= ___\n"
            "\n"
            "def rango(nivel):\n"
            "    if nivel >= 8:\n"
            "        return \"NEXUS\"\n"
            "    elif nivel >= ___:\n"
            "        return \"COMANDO\"\n"
            "    else:\n"
            "        return \"BASE\"\n"
            "\n"
            "def reporte(nombre, nivel, xp_actual):\n"
            "    r = rango(nivel)\n"
            "    xp_req = xp_requerido(nivel)\n"
            "    acceso = tiene_xp(xp_actual, nivel)\n"
            "    print(f\"___ | Rango: ___ | XP: ___/___ | Acceso: ___\")\n"
            "\n"
            "reporte(\"REX\", 6, 550)\n"
            "reporte(\"GHOST\", 3, 200)\n"
        ),
        "expected_output": (
            "REX | Rango: COMANDO | XP: 550/600 | Acceso: False\n"
            "GHOST | Rango: BASE | XP: 200/300 | Acceso: False"
        ),
        "test_inputs_json": json.dumps([]),
        "strict_match": True,
        "lore_briefing": (
            "El NEXUS-04 es el nodo central de coordinación táctica del Sector 04. "
            "Su arquitectura modular requiere 4 funciones interdependientes: "
            "cada una hace una sola cosa, pero juntas generan el reporte completo. "
            "Este es el patrón fundamental del software profesional."
        ),
        "pedagogical_objective": (
            "Integrar todos los conceptos de funciones: def, parámetros, return, "
            "valores booleanos, if/elif/else, composición y f-strings. "
            "Boss de fase que desbloquea el Sector 05."
        ),
        "syntax_hint": (
            "reporte usa: r=rango(nivel), xp_req=xp_requerido(nivel), "
            "acceso=tiene_xp(xp_actual, nivel). "
            "f-string: f'{nombre} | Rango: {r} | XP: {xp_actual}/{xp_req} | Acceso: {acceso}'"
        ),
        "theory_content": THEORY_F40,
        "hints_json": json.dumps([
            "xp_requerido(nivel) = nivel * 100. Para nivel=6: 600. Para nivel=3: 300.",
            "tiene_xp(xp_actual, nivel) llama a xp_requerido: return xp_actual >= xp_requerido(nivel).",
            "rango: nivel >= 8 → NEXUS, nivel >= 5 → COMANDO, else → BASE. Nivel 6 → COMANDO.",
        ]),
        "is_free": False,
        "is_ironman": False,
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# CHALLENGES — Sector 22: Recursión (L190–L194)
# ─────────────────────────────────────────────────────────────────────────────

NEW_RECURSION_CHALLENGES: list[dict] = [
    # ── L190 — cuenta_regresiva básica ────────────────────────────────────────
    {
        "title": "El Eco del Nexo",
        "description": (
            "Define `cuenta_regresiva(n)` que imprima los números desde `n` hasta `1`, "
            "y luego imprima `FUEGO`.\n\n"
            "La función debe ser **recursiva** (no usar `for` ni `while`).\n\n"
            "Llamala con `cuenta_regresiva(4)`.\n\n"
            "Salida esperada:\n"
            "```\n4\n3\n2\n1\nFUEGO\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 22,
        "level_order": 190,
        "base_xp_reward": 350,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 300,
        "challenge_type": "python",
        "phase": "recursion",
        "concepts_taught_json": json.dumps(["recursión", "caso base", "llamada recursiva", "self-call"]),
        "initial_code": (
            "# MISIÓN: Cuenta regresiva recursiva (sin for/while)\n"
            "\n"
            "def cuenta_regresiva(n):\n"
            "    if n == ___:         # caso base\n"
            "        print('FUEGO')\n"
            "        return\n"
            "    print(n)\n"
            "    cuenta_regresiva(___)  # llamada recursiva\n"
            "\n"
            "cuenta_regresiva(4)\n"
        ),
        "expected_output": "4\n3\n2\n1\nFUEGO",
        "test_inputs_json": json.dumps([]),
        "strict_match": True,
        "lore_briefing": (
            "El sistema de armamento del Nexo inicia una cuenta regresiva antes de disparar. "
            "El protocolo es recursivo: en cada tick imprime el número y se llama a sí mismo "
            "con el tick anterior. Cuando llega a cero, activa el disparo."
        ),
        "pedagogical_objective": (
            "Introducir recursión con el ejemplo más intuitivo: cuenta regresiva. "
            "Establecer el patrón fundamental: caso base + llamada recursiva con n-1."
        ),
        "syntax_hint": "if n == 0: print('FUEGO'); return\nprint(n)\ncuenta_regresiva(n - 1)",
        "theory_content": THEORY_R190,
        "hints_json": json.dumps([
            "El caso base es cuando n == 0: imprimís FUEGO y retornás.",
            "La llamada recursiva es cuenta_regresiva(n - 1): n se reduce en cada llamada.",
            "La función se llama a sí misma con un número más pequeño hasta llegar a 0.",
        ]),
        "is_free": False,
        "is_ironman": False,
    },
    # ── L191 — factorial recursivo ────────────────────────────────────────────
    {
        "title": "Factorial del Nexo",
        "description": (
            "Define `factorial(n)` que calcule **recursivamente** el factorial de `n`.\n\n"
            "Regla: `factorial(0) = 1` y `factorial(n) = n * factorial(n-1)`.\n\n"
            "Imprimí `factorial(5)` y `factorial(0)`.\n\n"
            "Salida esperada:\n"
            "```\n120\n1\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 22,
        "level_order": 191,
        "base_xp_reward": 375,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 300,
        "challenge_type": "python",
        "phase": "recursion",
        "concepts_taught_json": json.dumps(["factorial", "return recursivo", "caso base n=0", "acumulación"]),
        "initial_code": (
            "# MISIÓN: Factorial recursivo con return\n"
            "\n"
            "def factorial(n):\n"
            "    if n == 0:          # caso base\n"
            "        return ___\n"
            "    return n * factorial(___)\n"
            "\n"
            "print(factorial(5))\n"
            "print(factorial(0))\n"
        ),
        "expected_output": "120\n1",
        "test_inputs_json": json.dumps([]),
        "strict_match": True,
        "lore_briefing": (
            "El criptoprocesador del Nexo usa factorial para calcular combinaciones de "
            "claves de seguridad. 5! = 5×4×3×2×1 = 120. La recursión permite expresar "
            "esta definición matemática directamente en código."
        ),
        "pedagogical_objective": (
            "Introducir recursión con return. "
            "Mostrar que cada llamada acumula el resultado multiplicando n por el resultado de la subproblema."
        ),
        "syntax_hint": "if n == 0: return 1\nreturn n * factorial(n - 1)",
        "theory_content": THEORY_R191,
        "hints_json": json.dumps([
            "El caso base: factorial(0) = 1.",
            "El caso recursivo: return n * factorial(n - 1).",
            "factorial(5) = 5 * factorial(4) = 5 * 4 * 3 * 2 * 1 * 1 = 120.",
        ]),
        "is_free": False,
        "is_ironman": False,
    },
    # ── L192 — fibonacci ──────────────────────────────────────────────────────
    {
        "title": "Fibonacci Táctico",
        "description": (
            "Define `fibonacci(n)` recursivamente.\n\n"
            "Regla: `fibonacci(0) = 0`, `fibonacci(1) = 1`, "
            "`fibonacci(n) = fibonacci(n-1) + fibonacci(n-2)`.\n\n"
            "Imprimí `fibonacci(6)` y `fibonacci(8)`.\n\n"
            "Salida esperada:\n"
            "```\n8\n21\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 22,
        "level_order": 192,
        "base_xp_reward": 400,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 360,
        "challenge_type": "python",
        "phase": "recursion",
        "concepts_taught_json": json.dumps(["fibonacci", "doble llamada recursiva", "árbol de recursión"]),
        "initial_code": (
            "# MISIÓN: Fibonacci con doble llamada recursiva\n"
            "\n"
            "def fibonacci(n):\n"
            "    if n <= 1:          # caso base dual\n"
            "        return n\n"
            "    return fibonacci(___) + fibonacci(___)\n"
            "\n"
            "print(fibonacci(6))\n"
            "print(fibonacci(8))\n"
        ),
        "expected_output": "8\n21",
        "test_inputs_json": json.dumps([]),
        "strict_match": True,
        "lore_briefing": (
            "La secuencia Fibonacci aparece en los patrones de expansión del Nexo. "
            "Cada número es la suma de los dos anteriores: 0,1,1,2,3,5,8,13,21... "
            "La doble llamada recursiva traduce la definición matemática directamente a código."
        ),
        "pedagogical_objective": (
            "Introducir la recursión con dos llamadas recursivas. "
            "Mostrar el árbol de llamadas y por qué fibonacci es O(2^n)."
        ),
        "syntax_hint": "return fibonacci(n - 1) + fibonacci(n - 2)",
        "theory_content": THEORY_R192,
        "hints_json": json.dumps([
            "El caso base: si n <= 1, retorná n (fibonacci(0)=0, fibonacci(1)=1).",
            "El caso recursivo: return fibonacci(n-1) + fibonacci(n-2).",
            "fibonacci(6) = 8: 0,1,1,2,3,5,8 (índice 0 al 6).",
        ]),
        "is_free": False,
        "is_ironman": False,
    },
    # ── L193 — recursión sobre listas ─────────────────────────────────────────
    {
        "title": "Suma Profunda",
        "description": (
            "Define `suma_lista(lista)` que sume todos los elementos de forma **recursiva** "
            "(sin usar `sum()`, `for`, ni `while`).\n\n"
            "Imprimí `suma_lista([1, 2, 3, 4])` y `suma_lista([10, 20, 30])`.\n\n"
            "Salida esperada:\n"
            "```\n10\n60\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "hard",
        "sector_id": 22,
        "level_order": 193,
        "base_xp_reward": 425,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 360,
        "challenge_type": "python",
        "phase": "recursion",
        "concepts_taught_json": json.dumps(["recursión sobre listas", "lista[1:]", "cabeza-cola", "caso base lista vacía"]),
        "initial_code": (
            "# MISIÓN: Suma recursiva (sin sum/for/while)\n"
            "\n"
            "def suma_lista(lista):\n"
            "    if len(lista) == ___:   # caso base: lista vacía\n"
            "        return 0\n"
            "    return lista[0] + suma_lista(lista[___:])\n"
            "\n"
            "print(suma_lista([1, 2, 3, 4]))\n"
            "print(suma_lista([10, 20, 30]))\n"
        ),
        "expected_output": "10\n60",
        "test_inputs_json": json.dumps([]),
        "strict_match": True,
        "lore_briefing": (
            "El analizador de energía del Nexo suma lecturas de sensores de forma recursiva. "
            "El patrón cabeza-cola es fundamental: tomás el primer elemento, sumás el resto. "
            "lista[1:] crea una copia de la lista sin el primer elemento — cada llamada "
            "acorta la lista hasta que está vacía."
        ),
        "pedagogical_objective": (
            "Extender la recursión a estructuras de datos (listas). "
            "Enseñar el patrón cabeza-cola: lista[0] + f(lista[1:]). "
            "Establecer lista vacía como caso base."
        ),
        "syntax_hint": "if len(lista) == 0: return 0\nreturn lista[0] + suma_lista(lista[1:])",
        "theory_content": THEORY_R193,
        "hints_json": json.dumps([
            "El caso base es lista vacía (len == 0): retorná 0.",
            "La llamada recursiva usa lista[1:] que es la lista sin el primer elemento.",
            "suma_lista([1,2,3,4]) = 1 + suma_lista([2,3,4]) = 1 + 2 + 3 + 4 = 10.",
        ]),
        "is_free": False,
        "is_ironman": False,
    },
    # ── L194 — BOSS: 3 funciones recursivas ──────────────────────────────────
    {
        "title": "NEXUS-22: El Laberinto del Nexo",
        "description": (
            "**MISIÓN BOSS** — Implementá 3 funciones recursivas independientes:\n\n"
            "1. `potencia(base, exp)` → calcula `base^exp` sin usar `**`\n"
            "   - Caso base: `exp == 0` → retorna `1`\n"
            "   - Recursiva: `base * potencia(base, exp - 1)`\n\n"
            "2. `es_palindromo(s)` → `True` si el string es palíndromo\n"
            "   - Caso base: `len(s) <= 1` → retorna `True`\n"
            "   - Recursiva: primer char == último char **y** `es_palindromo(s[1:-1])`\n\n"
            "3. `aplanar(lista)` → convierte una lista anidada en lista plana\n"
            "   - Caso base: `lista` vacía → retorna `[]`\n"
            "   - Recursiva: si `lista[0]` es lista → aplanar(lista[0]) + aplanar(lista[1:]), si no → [lista[0]] + aplanar(lista[1:])\n\n"
            "Salida esperada:\n"
            "```\n8\nTrue\nFalse\n[1, 2, 3, 4, 5]\n```"
        ),
        "difficulty_tier": DifficultyTier.ADVANCED,
        "difficulty": "hard",
        "sector_id": 22,
        "level_order": 194,
        "base_xp_reward": 600,
        "is_project": True,
        "is_phase_boss": True,
        "telemetry_goal_time": 600,
        "challenge_type": "python",
        "phase": "recursion",
        "concepts_taught_json": json.dumps([
            "potencia recursiva", "palíndromo recursivo", "aplanar lista", "isinstance",
            "recursión múltiple", "integración"
        ]),
        "initial_code": (
            "# BOSS MISSION: 3 funciones recursivas\n"
            "\n"
            "def potencia(base, exp):\n"
            "    if exp == 0:\n"
            "        return ___\n"
            "    return base * potencia(base, ___)\n"
            "\n"
            "def es_palindromo(s):\n"
            "    if len(s) <= 1:\n"
            "        return True\n"
            "    return s[0] == s[-1] and es_palindromo(___)\n"
            "\n"
            "def aplanar(lista):\n"
            "    if len(lista) == 0:\n"
            "        return []\n"
            "    if isinstance(lista[0], list):\n"
            "        return aplanar(lista[0]) + aplanar(lista[1:])\n"
            "    return [lista[0]] + aplanar(___)\n"
            "\n"
            "print(potencia(2, 3))\n"
            "print(es_palindromo('radar'))\n"
            "print(es_palindromo('nexo'))\n"
            "print(aplanar([1, [2, 3], [4, [5]]]))\n"
        ),
        "expected_output": "8\nTrue\nFalse\n[1, 2, 3, 4, 5]",
        "test_inputs_json": json.dumps([]),
        "strict_match": True,
        "lore_briefing": (
            "El Laberinto del Nexo es el desafío final del Sector 22. "
            "Tres módulos de encriptación recursiva deben ser activados simultáneamente: "
            "el módulo de potenciación, el verificador de simetría y el aplanador de rutas. "
            "Solo quien domine la recursión completa puede atravesar el laberinto."
        ),
        "pedagogical_objective": (
            "Boss integrador del Sector 22. Cubre recursión numérica (potencia), "
            "recursión sobre strings (palíndromo) y recursión sobre estructuras anidadas (aplanar). "
            "Introduce isinstance() para detectar tipos en tiempo de ejecución."
        ),
        "syntax_hint": (
            "potencia: return 1 si exp==0, sino base * potencia(base, exp-1). "
            "es_palindromo: s[0] == s[-1] and es_palindromo(s[1:-1]). "
            "aplanar: [lista[0]] + aplanar(lista[1:]) para elementos no-lista."
        ),
        "theory_content": THEORY_R194,
        "hints_json": json.dumps([
            "potencia: caso base exp==0 → return 1. Recursiva: return base * potencia(base, exp-1).",
            "es_palindromo: s[1:-1] es el string sin el primer y último char.",
            "aplanar: si lista[0] es una lista, aplanala también. Sino, envuélvela en []: [lista[0]].",
        ]),
        "is_free": False,
        "is_ironman": False,
    },
]

ALL_NEW_CHALLENGES = NEW_FUNCTIONS_CHALLENGES + NEW_RECURSION_CHALLENGES

# ─────────────────────────────────────────────────────────────────────────────
# DB MIGRATION
# ─────────────────────────────────────────────────────────────────────────────

async def migrate_db(dry_run: bool = False) -> None:
    print("\n" + "=" * 60)
    print("  DB MIGRATION")
    print("=" * 60)

    if dry_run:
        print(f"  [DRY] DELETE challenges WHERE sector_id=21 AND level_order BETWEEN 180 AND 189")
        print(f"  [DRY] UPDATE level_order +10 WHERE level_order >= 31")
        print(f"  [DRY] UPDATE sector_id   +1  WHERE sector_id  >= 4")
        print(f"  [DRY] INSERT {len(NEW_FUNCTIONS_CHALLENGES)} challenges (Funciones, sector_id=4, L31-40)")
        print(f"  [DRY] INSERT {len(NEW_RECURSION_CHALLENGES)} challenges (Recursion, sector_id=22, L190-194)")
        for ch in ALL_NEW_CHALLENGES:
            print(f"         [S{ch['sector_id']:02d}|L{ch['level_order']:03d}] {ch['title']}")
        print("\n  [DRY RUN] - ningun cambio aplicado a la DB.")
        return

    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        async with session.begin():
            # 0. Eliminar challenges experimentales de S21 (PREDICCION 01-10, L180-189)
            #    Estos eran prototipos sin user_progress. Si no existen, rowcount=0.
            r = await session.execute(
                text("DELETE FROM challenges WHERE sector_id = 21 AND level_order BETWEEN 180 AND 189")
            )
            if r.rowcount > 0:
                print(f"  OK  DELETE {r.rowcount} challenges experimentales (S21 L180-189)")
            else:
                print(f"  --  No habia challenges experimentales en S21 L180-189")

            # 1. Shift level_orders
            r = await session.execute(
                text("UPDATE challenges SET level_order = level_order + 10 WHERE level_order >= 31")
            )
            print(f"  OK  level_order +10 para {r.rowcount} challenges")

            # 2. Shift sector_ids
            r = await session.execute(
                text("UPDATE challenges SET sector_id = sector_id + 1 WHERE sector_id >= 4")
            )
            print(f"  OK  sector_id  +1  para {r.rowcount} challenges")

            # 3. INSERT new challenges
            inserted = 0
            for data in ALL_NEW_CHALLENGES:
                ch = Challenge(
                    id=uuid.uuid4(),
                    title=data["title"],
                    description=data["description"],
                    difficulty_tier=data["difficulty_tier"],
                    base_xp_reward=data["base_xp_reward"],
                    initial_code=data["initial_code"],
                    expected_output=data["expected_output"],
                    test_inputs_json=data.get("test_inputs_json", "[]"),
                    level_order=data["level_order"],
                    phase=data.get("phase"),
                    concepts_taught_json=data.get("concepts_taught_json", "[]"),
                    challenge_type=data.get("challenge_type", "python"),
                    theory_content=data.get("theory_content"),
                    lore_briefing=data.get("lore_briefing"),
                    pedagogical_objective=data.get("pedagogical_objective"),
                    syntax_hint=data.get("syntax_hint"),
                    hints_json=data.get("hints_json", "[]"),
                    sector_id=data["sector_id"],
                    difficulty=data.get("difficulty"),
                    is_project=data.get("is_project", False),
                    is_phase_boss=data.get("is_phase_boss", False),
                    telemetry_goal_time=data.get("telemetry_goal_time"),
                    strict_match=data.get("strict_match", True),
                    is_free=data.get("is_free", False),
                    is_ironman=data.get("is_ironman", False),
                )
                session.add(ch)
                inserted += 1
                print(f"  +  [S{data['sector_id']:02d}|L{data['level_order']:03d}] {data['title']}")

            print(f"\n  OK  INSERT {inserted} challenges nuevos")

    await engine.dispose()
    print("\n  DB migration completada.")


# ─────────────────────────────────────────────────────────────────────────────
# SEED FILE MIGRATION
# ─────────────────────────────────────────────────────────────────────────────

def _update_seed_content(content: str, old_num: int, new_num: int) -> str:
    """
    Actualiza el contenido de un seed file:
    - Renombra la variable SECTOR_XX
    - Actualiza sector_id en dict literals
    - Desplaza level_orders >= 31 en +10
    - Actualiza referencias en comentarios/docstrings
    """
    # Variable: SECTOR_04 → SECTOR_05
    content = content.replace(f"SECTOR_{old_num:02d}", f"SECTOR_{new_num:02d}")

    # sector_id en dict: "sector_id": 4  (y variantes con espacio)
    content = re.sub(
        r'"sector_id":\s*' + str(old_num) + r'\b',
        f'"sector_id": {new_num}',
        content
    )
    # sector_id en código: Challenge.sector_id == 4
    content = re.sub(
        r'(sector_id\s*==\s*)' + str(old_num) + r'\b',
        r'\g<1>' + str(new_num),
        content
    )

    # level_order: shift +10 para todos los valores >= 31
    def shift_level(m: re.Match) -> str:
        val = int(m.group(1))
        if val >= 31:
            return f'"level_order": {val + 10}'
        return m.group(0)

    content = re.sub(r'"level_order":\s*(\d+)', shift_level, content)

    # Referencias en docstring/comentarios
    content = content.replace(f"seed_sector_{old_num:02d}", f"seed_sector_{new_num:02d}")

    # Docstring sector número (e.g., "SECTOR 04:" → "SECTOR 05:")
    content = re.sub(
        r'(SECTOR\s+0?)' + str(old_num) + r':',
        r'\g<1>' + str(new_num) + ':',
        content
    )
    content = re.sub(
        r'(Sector\s+)' + str(old_num) + r':',
        r'\g<1>' + str(new_num) + ':',
        content
    )

    return content


def migrate_seed_files(dry_run: bool = False) -> None:
    print("=" * 60)
    print("  SEED FILE MIGRATION")
    print("=" * 60)

    scripts_dir = Path(__file__).resolve().parent

    # Renombrar en orden DESCENDENTE para evitar sobreescrituras
    for old_num in range(20, 3, -1):  # 20, 19, ..., 4
        new_num = old_num + 1
        old_file = scripts_dir / f"seed_sector_{old_num:02d}.py"

        if not old_file.exists():
            print(f"  SKIP  seed_sector_{old_num:02d}.py no encontrado")
            continue

        new_file = scripts_dir / f"seed_sector_{new_num:02d}.py"
        content = old_file.read_text(encoding="utf-8")
        new_content = _update_seed_content(content, old_num, new_num)

        if dry_run:
            print(f"  [DRY] seed_sector_{old_num:02d}.py -> seed_sector_{new_num:02d}.py "
                  f"(sector_id {old_num} -> {new_num})")
        else:
            new_file.write_text(new_content, encoding="utf-8")
            old_file.unlink()
            print(f"  OK  seed_sector_{old_num:02d}.py -> seed_sector_{new_num:02d}.py")

    print()
    if not dry_run:
        print("  Seed files renombrados y actualizados.")
        print("  Creá seed_sector_04.py y seed_sector_22.py manualmente o")
        print("  ejecutá `python -m scripts.migrate_restructure_sectors --write-seeds`")
    else:
        print("  [DRY RUN] - ningun archivo modificado.")


# ─────────────────────────────────────────────────────────────────────────────
# WRITE NEW SEED FILES
# ─────────────────────────────────────────────────────────────────────────────

SEED_04_HEADER = '''\
"""
seed_sector_04.py — Sector 04: Funciones (10 niveles, IDs 31–40).

Uso (desde la raíz del proyecto):
    python -m scripts.seed_sector_04

Comportamiento:
    1. Elimina solo los challenges con sector_id = 4.
    2. Inserta los 10 niveles del Sector 04 — curva easy → medium → hard.
    3. El Nivel 40 es Boss de Fase (is_phase_boss = True).

Temática técnica: def, parámetros, return, scope local, composición.
Narrativa: módulos de transmisión táctica del Nexo.
"""
import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.migrate_restructure_sectors import NEW_FUNCTIONS_CHALLENGES as SECTOR_04

# SECTOR_04 se importa del script de migración — es la fuente canónica.
# Para re-seedear: python -m scripts.seed_master --sector 4
'''

SEED_22_HEADER = '''\
"""
seed_sector_22.py — Sector 22: Recursión (5 niveles, IDs 190–194).

Uso (desde la raíz del proyecto):
    python -m scripts.seed_sector_22

Comportamiento:
    1. Elimina solo los challenges con sector_id = 22.
    2. Inserta los 5 niveles del Sector 22 — medium → hard.
    3. El Nivel 194 es Boss de Fase (is_phase_boss = True).

Temática técnica: recursión, caso base, llamada recursiva, factorial,
                  fibonacci, recursión sobre listas.
Narrativa: El Laberinto del Nexo — el desafío final recursivo.
"""
import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.migrate_restructure_sectors import NEW_RECURSION_CHALLENGES as SECTOR_22

# SECTOR_22 se importa del script de migración — es la fuente canónica.
# Para re-seedear: python -m scripts.seed_master --sector 22
'''


def write_new_seed_files(dry_run: bool = False) -> None:
    scripts_dir = Path(__file__).resolve().parent
    files = {
        scripts_dir / "seed_sector_04.py": SEED_04_HEADER,
        scripts_dir / "seed_sector_22.py": SEED_22_HEADER,
    }
    for path, content in files.items():
        if dry_run:
            print(f"  [DRY] escribir {path.name}")
        else:
            path.write_text(content, encoding="utf-8")
            print(f"  OK  {path.name} creado")


# ─────────────────────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

async def main() -> None:
    parser = argparse.ArgumentParser(
        description="Reestructura sectores DAKI: inserta S04 Funciones y S22 Recursión."
    )
    parser.add_argument("--dry-run",    action="store_true", help="Solo muestra el plan, no aplica cambios")
    parser.add_argument("--db-only",    action="store_true", help="Solo migra la DB, no toca archivos")
    parser.add_argument("--files-only", action="store_true", help="Solo migra archivos, no toca la DB")
    parser.add_argument("--write-seeds", action="store_true", help="Solo escribe seed_sector_04.py y seed_sector_22.py")
    args = parser.parse_args()

    dry = args.dry_run

    print()
    print("=" * 60)
    print("  DAKI EdTech - Reestructura Pedagogica de Sectores")
    print("  +10 niveles (Funciones S04) + 5 (Recursion S22) = 190")
    print("=" * 60)
    if dry:
        print("  ** MODO DRY RUN - no se aplica ningun cambio **\n")

    if args.write_seeds:
        write_new_seed_files(dry_run=dry)
        return

    if not args.files_only:
        await migrate_db(dry_run=dry)

    if not args.db_only:
        migrate_seed_files(dry_run=dry)
        if not dry:
            write_new_seed_files(dry_run=dry)

    print()
    print("  Siguiente paso: actualizar seed_master.py para incluir")
    print("  ('scripts.seed_sector_04', 'SECTOR_04') y")
    print("  ('scripts.seed_sector_22', 'SECTOR_22') en la lista sources.")
    print()


if __name__ == "__main__":
    asyncio.run(main())
