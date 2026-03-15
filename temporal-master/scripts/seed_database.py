"""
Script de población de datos — inserta 5 retos iniciales en la base de datos.

Uso (desde la raíz del proyecto):
    python -m scripts.seed_database

Comportamiento:
    1. Elimina filas existentes en user_progress y challenges (orden FK-seguro).
    2. Inserta 5 misiones con curva de aprendizaje INICIANTE → AVANZADO,
       incluyendo contenido teórico en Markdown (theory_content).
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
from app.models.user import User  # noqa: F401
from app.models.user_progress import UserProgress  # noqa: F401

# ─── Teoría en Markdown por misión ───────────────────────────────────────────
# Las páginas se separan con \n---\n

THEORY_M1 = """\
## PROTOCOLO: Funciones en Python

Una **función** es un bloque de código reutilizable. Se define con `def`:

```python
def nombre(parametro):
    return resultado
```

- `def` — declara la función
- `return` — envía el valor al llamador
- Si no hay `return`, la función devuelve `None`

---

## APLICACIÓN: f-strings

Para construir strings dinámicos usa **f-strings** (Python 3.6+):

```python
nombre = "Ada"
mensaje = f"Hola, {nombre}"
print(mensaje)  # → Hola, Ada
```

Todo lo que escribas dentro de `{}` se evalúa como código Python en el momento de la ejecución.

---

## EJEMPLO COMPLETO

```python
def saludar(nombre):
    return f"Hola, {nombre}"

resultado = saludar("Mundo")
print(resultado)  # → Hola, Mundo
```

**Flujo:**
- `saludar("Mundo")` invoca la función con `nombre = "Mundo"`
- La función retorna el string construido
- `print()` lo muestra en consola
"""

THEORY_M2 = """\
## PROTOCOLO: Tipos de Datos Básicos

Python tiene tipos fundamentales que debes conocer:

| Tipo | Ejemplo | Descripción |
|------|---------|-------------|
| `int` | `42` | Número entero |
| `float` | `3.14` | Número decimal |
| `str` | `"Hola"` | Cadena de texto |
| `bool` | `True` | Verdadero o Falso |

La función `type(x)` te dice el tipo de cualquier variable.

---

## APLICACIÓN: input() y conversión de tipos

`input()` **siempre** devuelve un `str`. Para operar matemáticamente, convierte:

```python
texto = input()      # "17" (string)
numero = int(texto)  # 17  (entero)
```

Operadores aritméticos básicos:
- `+` suma  · `-` resta  · `*` multiplicación  · `//` división entera  · `%` módulo

---

## EJEMPLO COMPLETO

```python
def sumar(a, b):
    return a + b

a = int(input())
b = int(input())
print(sumar(a, b))
```

**Nota:** `int(input())` es un patrón muy común en Python para leer números.
"""

THEORY_M3 = """\
## PROTOCOLO: Strings como Secuencias

En Python, un **string es una secuencia de caracteres**. Puedes acceder a cada uno por su índice:

```python
texto = "Python"
print(texto[0])   # → "P"
print(texto[-1])  # → "n"  (último elemento)
```

Los índices negativos cuentan desde el final.

---

## APLICACIÓN: Slicing (rebanado)

El **slicing** extrae partes de un string:

```python
texto = "Python"
print(texto[0:3])   # → "Pyt"
print(texto[2:])    # → "thon"
print(texto[::-1])  # → "nohtyP"  (invertido)
```

La sintaxis es `[inicio:fin:paso]`. Con `paso = -1` recorres el string al revés.

---

## EJEMPLO COMPLETO

```python
def invertir(cadena):
    return cadena[::-1]

texto = input()
print(invertir(texto))
```

**Equivalencia:** `cadena[::-1]` es idéntico a:
```python
resultado = ""
for c in cadena:
    resultado = c + resultado
```
El slicing es más idiomático (pythónico) y más eficiente.
"""

THEORY_M4 = """\
## PROTOCOLO: Bucles for

El bucle `for` itera sobre cualquier **secuencia** (string, lista, rango):

```python
for elemento in secuencia:
    # cuerpo del bucle
```

Ejemplos:
```python
for letra in "Python":
    print(letra)        # imprime P, y, t, h, o, n

for i in range(5):
    print(i)            # imprime 0, 1, 2, 3, 4
```

---

## APLICACIÓN: El operador `in`

`in` comprueba si un valor está dentro de una colección:

```python
"a" in "arquitecto"   # True
"z" in "Python"       # False
```

Para contar vocales puedes combinar `for` + `in`:

```python
vocales = "aeiouAEIOU"
contador = 0
for letra in texto:
    if letra in vocales:
        contador += 1
```

---

## EJEMPLO COMPLETO

```python
def contar_vocales(texto):
    vocales = "aeiouAEIOU"
    return sum(1 for c in texto if c in vocales)

texto = input()
print(contar_vocales(texto))
```

`sum(1 for c in texto if c in vocales)` usa una **generator expression** — un `for` comprimido en una línea.
"""

THEORY_M5 = """\
## PROTOCOLO: Recursión vs Iteración

La **recursión** llama a la misma función desde sí misma:

```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)  # ⚠ lento para n grande
```

Para `n = 40` esto hace ~330 millones de llamadas. La complejidad es O(2^n).

---

## APLICACIÓN: Solución Iterativa

Con un bucle `while` y dos variables mantenemos O(n) tiempo y O(1) espacio:

```python
def fibonacci(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
```

- `a, b = b, a + b` actualiza ambas variables **simultáneamente** (asignación paralela)
- `_` es la convención para una variable que no usamos

---

## COMPARACIÓN DE RENDIMIENTO

```python
# Recursivo: fibonacci(40) → ~3 segundos
# Iterativo: fibonacci(40) → < 0.001 segundos
```

**Regla:** Cuando una función recursiva recalcula los mismos valores repetidamente, conviértela en iterativa (o usa **memoización** con `@functools.lru_cache`).
"""

# ─── Definición de retos ──────────────────────────────────────────────────────

CHALLENGES = [
    # ── Tier 1 / BÁSICO ───────────────────────────────────────────────────────
    {
        "title": "Misión 1: El Eco del Sistema",
        "description": (
            "El sistema necesita que implementes una función de saludo personalizado.\n\n"
            "Completa `saludar(nombre)` para que retorne el string `'Hola, {nombre}'`.\n"
            "El nombre llega por stdin — no lo modifiques."
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "base_xp_reward": 100,
        "initial_code": (
            "def saludar(nombre):\n"
            "    # Tu código aquí\n"
            "    pass\n"
            "\n"
            "nombre = input()\n"
            "print(saludar(nombre))\n"
        ),
        "expected_output": "Hola, Arquitecto",
        "test_inputs_json": json.dumps(["Arquitecto"]),
        "level_order": 1,
        "phase": "basico",
        "concepts_taught_json": json.dumps(["def", "return", "f-strings"]),
        "challenge_type": "python",
        "theory_content": THEORY_M1,
    },
    {
        "title": "Misión 2: La Calculadora Binaria",
        "description": (
            "Los registros llegan en dos líneas separadas. Debes sumarlos.\n\n"
            "Implementa `sumar(a, b)` que retorne la suma de dos enteros.\n"
            "Los valores se leen desde stdin (un número por línea)."
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "base_xp_reward": 150,
        "initial_code": (
            "def sumar(a, b):\n"
            "    # Tu código aquí\n"
            "    pass\n"
            "\n"
            "a = int(input())\n"
            "b = int(input())\n"
            "print(sumar(a, b))\n"
        ),
        "expected_output": "42",
        "test_inputs_json": json.dumps(["17", "25"]),
        "level_order": 2,
        "phase": "basico",
        "concepts_taught_json": json.dumps(["int", "input", "aritmetica"]),
        "challenge_type": "python",
        "theory_content": THEORY_M2,
    },
    # ── Tier 2 / CONTROL ──────────────────────────────────────────────────────
    {
        "title": "Misión 3: El Inversor de Cadenas",
        "description": (
            "Un mensaje cifrado llega al sistema. Para descifrarlo necesitas invertirlo.\n\n"
            "Implementa `invertir(cadena)` que retorne el string al revés.\n"
            "Ejemplo: `'Arquitecto'` → `'otcetiqrA'`."
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "base_xp_reward": 300,
        "initial_code": (
            "def invertir(cadena):\n"
            "    # Tu código aquí\n"
            "    pass\n"
            "\n"
            "cadena = input()\n"
            "print(invertir(cadena))\n"
        ),
        "expected_output": "otcetiqrA",
        "test_inputs_json": json.dumps(["Arquitecto"]),
        "level_order": 3,
        "phase": "control",
        "concepts_taught_json": json.dumps(["strings", "slicing", "indices"]),
        "challenge_type": "python",
        "theory_content": THEORY_M3,
    },
    {
        "title": "Misión 4: El Contador de Vocales",
        "description": (
            "El sistema de análisis léxico necesita contar las vocales de un mensaje.\n\n"
            "Implementa `contar_vocales(texto)` que retorne la cantidad de vocales "
            "(a, e, i, o, u — mayúsculas y minúsculas).\n"
            "Ejemplo: `'Arquitecto'` tiene 5 vocales (A, u, i, e, o)."
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "base_xp_reward": 500,
        "initial_code": (
            "def contar_vocales(texto):\n"
            "    # Tu código aquí\n"
            "    pass\n"
            "\n"
            "texto = input()\n"
            "print(contar_vocales(texto))\n"
        ),
        "expected_output": "5",
        "test_inputs_json": json.dumps(["Arquitecto"]),
        "level_order": 4,
        "phase": "bucles",
        "concepts_taught_json": json.dumps(["for", "in", "contador"]),
        "challenge_type": "python",
        "theory_content": THEORY_M4,
    },
    # ── Tier 3 / AVANZADO ─────────────────────────────────────────────────────
    {
        "title": "Misión 5: La Secuencia de Fibonacci",
        "description": (
            "El núcleo del sistema requiere el N-ésimo número de Fibonacci "
            "para inicializar su protocolo de seguridad.\n\n"
            "Implementa `fibonacci(n)` que retorne el n-ésimo número (base 1).\n"
            "Ejemplo: `fibonacci(10)` → `55`.\n"
            "Restricción: no uses recursión simple — el input puede ser grande."
        ),
        "difficulty_tier": DifficultyTier.ADVANCED,
        "base_xp_reward": 800,
        "initial_code": (
            "def fibonacci(n):\n"
            "    # Tu código aquí\n"
            "    pass\n"
            "\n"
            "n = int(input())\n"
            "print(fibonacci(n))\n"
        ),
        "expected_output": "55",
        "test_inputs_json": json.dumps(["10"]),
        "level_order": 5,
        "phase": "bucles",
        "concepts_taught_json": json.dumps(["while", "iteracion", "optimizacion"]),
        "challenge_type": "python",
        "theory_content": THEORY_M5,
    },
]


# ─── Lógica de población ──────────────────────────────────────────────────────

async def seed() -> None:
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with SessionLocal() as session:
        print("🧹  Limpiando tablas...")
        await session.execute(delete(UserProgress))
        await session.execute(delete(Challenge))
        await session.flush()
        print("    user_progress → limpia")
        print("    challenges    → limpia")

        print("\n🌱  Insertando misiones...")
        for i, data in enumerate(CHALLENGES, start=1):
            challenge = Challenge(**data)
            session.add(challenge)
            tier_label = data["difficulty_tier"].name
            has_theory = "✓ teoría" if data.get("theory_content") else "— sin teoría"
            print(f"    [{i}/{len(CHALLENGES)}] {data['title']}  ({tier_label}, {data['base_xp_reward']} XP, {has_theory})")

        await session.commit()

    await engine.dispose()
    print(f"\n✅  Listo — {len(CHALLENGES)} misiones insertadas correctamente.")


if __name__ == "__main__":
    asyncio.run(seed())
