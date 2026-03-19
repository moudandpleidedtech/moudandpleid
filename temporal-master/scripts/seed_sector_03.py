"""
Seed — SECTOR 03: El Bucle Infinito (10 niveles, IDs 21–30).

Uso (desde la raíz del proyecto):
    python -m scripts.seed_sector_03

Comportamiento:
    1. Elimina solo los challenges con sector_id = 3 (idempotente).
    2. Inserta los 10 niveles del Sector 03 con curva easy → medium → hard.
    3. El Nivel 30 es un Mini-Boss Proyecto Integrador (is_project = True).

Temática técnica: for, while, range(), break, continue.
Narrativa: descifrar señales repetitivas, optimizar el firewall, escapar de trampas temporales.
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

THEORY_N21 = """\
## PROTOCOLO: for — El Ciclo de Exploración

Un bucle `for` repite un bloque de código para cada elemento de una secuencia.

```python
for i in range(3):
    print(i)
# Imprime: 0  1  2
```

- `range(n)` genera los números `0, 1, 2, ..., n-1`
- La variable del bucle (`i`) toma cada valor de la secuencia
- El bloque indentado se ejecuta **una vez por cada valor**

---

## REGLA DE ORO

La indentación define qué código está **dentro** del bucle.
Todo lo que tenga 4 espacios extra después del `for:` forma parte del ciclo.

```python
for i in range(3):
    print("dentro")   # ← se repite 3 veces
print("fuera")        # ← se ejecuta 1 vez, al terminar
```
"""

THEORY_N22 = """\
## PROTOCOLO: range() — El Generador de Secuencias

`range()` puede recibir 1, 2 o 3 argumentos:

```python
range(5)        # 0, 1, 2, 3, 4
range(2, 6)     # 2, 3, 4, 5
range(1, 10, 2) # 1, 3, 5, 7, 9  (paso de 2)
```

| Forma              | Genera                     |
|--------------------|----------------------------|
| `range(n)`         | 0 hasta n-1                |
| `range(a, b)`      | a hasta b-1                |
| `range(a, b, paso)`| a hasta b-1, saltando paso |

---

## EJEMPLO TÁCTICO

```python
for potencia in range(10, 51, 10):
    print(potencia)
# Imprime: 10  20  30  40  50
```
"""

THEORY_N23 = """\
## PROTOCOLO: Acumuladores — Suma en Bucle

Un **acumulador** es una variable que se actualiza en cada iteración del bucle.

```python
total = 0
for i in range(1, 6):
    total = total + i
print(total)   # 15  (1+2+3+4+5)
```

El patrón es siempre el mismo:
1. Inicializa la variable **antes** del bucle
2. Actualiza la variable **dentro** del bucle
3. Usa el resultado **después** del bucle

---

## ATAJO: +=

```python
total = 0
for i in range(1, 6):
    total += i   # equivale a total = total + i
print(total)
```
"""

THEORY_N24 = """\
## PROTOCOLO: while — El Guardián de la Condición

A diferencia de `for`, el bucle `while` repite mientras una condición sea verdadera.

```python
contador = 0
while contador < 3:
    print(contador)
    contador += 1
# Imprime: 0  1  2
```

⚠️ **Peligro: Bucle Infinito**

Si la condición **nunca se vuelve falsa**, el programa nunca termina:

```python
while True:
    print("esto no para")   # ← BUCLE INFINITO
```

Siempre asegúrate de que algo dentro del bucle modifique la condición.
"""

THEORY_N25 = """\
## PROTOCOLO: break — Salida de Emergencia

`break` interrumpe el bucle inmediatamente, sin importar la condición.

```python
for i in range(10):
    if i == 4:
        break
    print(i)
# Imprime: 0  1  2  3
```

Es útil para salir de un bucle cuando se cumple una condición específica,
sin tener que recorrer todos los elementos restantes.

---

## TÁCTICA COMBINADA: while + break

```python
while True:
    señal = input()
    if señal == "STOP":
        break
    print("Señal recibida:", señal)
```
"""

THEORY_N26 = """\
## PROTOCOLO: continue — Saltar Iteraciones

`continue` omite el resto del bloque actual y pasa a la **siguiente iteración**.

```python
for i in range(5):
    if i == 2:
        continue
    print(i)
# Imprime: 0  1  3  4   (salta el 2)
```

La diferencia con `break`:
- `break` **termina** el bucle por completo
- `continue` **salta** solo la iteración actual y continúa con la siguiente

---

## APLICACIÓN: Filtrar elementos

```python
for numero in range(1, 11):
    if numero % 2 == 0:
        continue
    print(numero)   # Solo imprime impares: 1 3 5 7 9
```
"""

THEORY_N27 = """\
## PROTOCOLO: Bucles Anidados — Ciclos dentro de Ciclos

Un bucle puede contener otro bucle en su interior.

```python
for fila in range(3):
    for col in range(3):
        print(fila, col)
```

Por cada iteración del bucle externo, el bucle interno completa **todas** sus iteraciones.

---

## EJEMPLO: Tabla de multiplicar

```python
for i in range(1, 4):
    for j in range(1, 4):
        print(i * j, end=" ")
    print()
# 1 2 3
# 2 4 6
# 3 6 9
```

`end=" "` evita el salto de línea automático de print().
"""

THEORY_N28 = """\
## PROTOCOLO: for sobre Strings — Iterar Caracteres

Un `for` puede recorrer los caracteres de un string uno a uno.

```python
palabra = "NEXO"
for letra in palabra:
    print(letra)
# Imprime: N  E  X  O
```

---

## PROTOCOLO: len() y range() combinados

Para acceder por índice:

```python
palabra = "DAKI"
for i in range(len(palabra)):
    print(i, palabra[i])
# 0 D
# 1 A
# 2 K
# 3 I
```

Útil cuando necesitas el índice y el valor al mismo tiempo.
"""

THEORY_N29 = """\
## PROTOCOLO: while con Contador — Control Preciso

Cuando conoces la condición de parada pero no el número exacto de iteraciones,
`while` con un contador es más flexible que `for`.

```python
n = int(input())
i = 1
total = 0
while i <= n:
    total += i
    i += 1
print(total)
```

---

## COMPARATIVA: for vs while

| Situación                          | Mejor usar |
|------------------------------------|------------|
| Número fijo de repeticiones        | `for`      |
| Condición dinámica de parada       | `while`    |
| Recorrer una colección             | `for`      |
| Esperar una entrada específica     | `while`    |
"""


# ─── Niveles del Sector 03 ────────────────────────────────────────────────────

SECTOR_03 = [
    # ── NIVEL 21 — for básico con range ──────────────────────────────────────
    {
        "title": "La Primera Onda",
        "description": (
            "El firewall emite una señal de 5 pulsos numerados para calibrar el canal.\n\n"
            "Usa un bucle `for` con `range()` para imprimir los números del `0` al `4`, "
            "uno por línea."
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "easy",
        "sector_id": 3,
        "level_order": 21,
        "base_xp_reward": 100,
        "is_project": False,
        "telemetry_goal_time": 60,
        "challenge_type": "python",
        "phase": "ciclos",
        "concepts_taught_json": json.dumps(["for", "range()"]),
        "initial_code": (
            "# MISIÓN: Imprime los números del 0 al 4, uno por línea\n"
            "\n"
            "for i in range(5):\n"
            "    # Tu código aquí\n"
        ),
        "expected_output": "0\n1\n2\n3\n4",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El canal de transmisión al Nexo está sin calibrar. "
            "DAKI necesita que emitas exactamente 5 pulsos de prueba en secuencia, "
            "comenzando desde cero. Sin esta calibración, ningún dato llega al núcleo."
        ),
        "pedagogical_objective": (
            "Introducir el bucle for con range(). Entender que range(5) genera 0, 1, 2, 3, 4."
        ),
        "syntax_hint": "for i in range(5):\n    print(i)",
        "theory_content": THEORY_N21,
        "hints_json": json.dumps([
            "range(5) genera los números 0, 1, 2, 3, 4. El bucle los recorre uno a uno.",
            "Dentro del bucle usa print(i) para imprimir el valor actual de i en cada iteración.",
            "La solución es: for i in range(5): con print(i) indentado debajo.",
        ]),
    },
    # ── NIVEL 22 — range con inicio y fin ────────────────────────────────────
    {
        "title": "Pulsos de Frecuencia",
        "description": (
            "La antena del sector necesita emitir frecuencias entre `1` y `5` inclusive "
            "para sincronizar los nodos.\n\n"
            "Usa `range()` con dos argumentos para imprimir los números del `1` al `5`, "
            "uno por línea."
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "easy",
        "sector_id": 3,
        "level_order": 22,
        "base_xp_reward": 100,
        "is_project": False,
        "telemetry_goal_time": 75,
        "challenge_type": "python",
        "phase": "ciclos",
        "concepts_taught_json": json.dumps(["for", "range(inicio, fin)"]),
        "initial_code": (
            "# MISIÓN: Imprime del 1 al 5, uno por línea\n"
            "\n"
            "for frecuencia in range(1, 6):\n"
            "    # Tu código aquí\n"
        ),
        "expected_output": "1\n2\n3\n4\n5",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "Los nodos del Nexo operan en frecuencias del 1 al 5. "
            "Para activarlos en secuencia, DAKI necesita un pulso en cada frecuencia exacta. "
            "El range(0) no es suficiente — los nodos comienzan desde el uno."
        ),
        "pedagogical_objective": (
            "Usar range(inicio, fin). Entender que el inicio es inclusivo y el fin es exclusivo."
        ),
        "syntax_hint": "for frecuencia in range(1, 6):\n    print(frecuencia)",
        "theory_content": THEORY_N22,
        "hints_json": json.dumps([
            "range(1, 6) genera 1, 2, 3, 4, 5. El segundo número es el límite exclusivo.",
            "Para incluir el 5, el range debe terminar en 6: range(1, 6).",
            "Solución: for frecuencia in range(1, 6): con print(frecuencia) dentro.",
        ]),
    },
    # ── NIVEL 23 — acumulador suma ────────────────────────────────────────────
    {
        "title": "Reactor de Energía",
        "description": (
            "Los 5 reactores del sector emiten cargas de `1`, `2`, `3`, `4` y `5` unidades. "
            "DAKI necesita la energía total acumulada.\n\n"
            "Lee un número `n` y suma todos los enteros del `1` al `n` (inclusive). "
            "Imprime el resultado.\n\n"
            "Ejemplo: `n = 5` → `15`."
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "easy",
        "sector_id": 3,
        "level_order": 23,
        "base_xp_reward": 125,
        "is_project": False,
        "telemetry_goal_time": 120,
        "challenge_type": "python",
        "phase": "ciclos",
        "concepts_taught_json": json.dumps(["for", "acumulador", "+="]),
        "initial_code": (
            "# MISIÓN: Lee n e imprime la suma de 1 a n\n"
            "\n"
            "n = int(input())\n"
            "total = 0\n"
            "\n"
            "for i in range(1, n + 1):\n"
            "    # Acumula el valor de i en total\n"
            "\n"
            "print(total)\n"
        ),
        "expected_output": "15",
        "test_inputs_json": json.dumps(["5"]),
        "lore_briefing": (
            "Los reactores del Sector 03 no transmiten energía de golpe — "
            "la acumulan de forma incremental. Cada reactor añade su carga al sistema "
            "hasta que el ciclo completo de recarga termina. "
            "DAKI necesita saber cuánta energía total hay disponible."
        ),
        "pedagogical_objective": (
            "Patrón acumulador: inicializar antes del bucle, actualizar dentro, "
            "usar después. Uso de +=."
        ),
        "syntax_hint": "total = 0\nfor i in range(1, n + 1):\n    total += i\nprint(total)",
        "theory_content": THEORY_N23,
        "hints_json": json.dumps([
            "Necesitas una variable que empiece en 0 y vaya sumando cada i del bucle.",
            "Dentro del bucle escribe: total += i  (equivale a total = total + i).",
            "Después del bucle (sin indentación) escribe print(total) para mostrar la suma.",
        ]),
    },
    # ── NIVEL 24 — while básico ───────────────────────────────────────────────
    {
        "title": "El Guardián del Portal",
        "description": (
            "El portal de acceso permanece cerrado hasta que la energía supere `50` unidades. "
            "Empieza con `energia = 10` y suma `15` por cada ciclo de carga.\n\n"
            "Usa un `while` para imprimir el valor de `energia` al inicio de cada ciclo "
            "mientras sea `<= 50`. "
            "Cuando supere 50, imprime `PORTAL ABIERTO`.\n\n"
            "Salida esperada:\n"
            "```\n10\n25\n40\n55\nPORTAL ABIERTO\n```"
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "easy",
        "sector_id": 3,
        "level_order": 24,
        "base_xp_reward": 150,
        "is_project": False,
        "telemetry_goal_time": 150,
        "challenge_type": "python",
        "phase": "ciclos",
        "concepts_taught_json": json.dumps(["while", "condición", "+="]),
        "initial_code": (
            "# MISIÓN: Carga energía hasta superar 50, luego abre el portal\n"
            "\n"
            "energia = 10\n"
            "\n"
            "while energia <= 50:\n"
            "    print(energia)\n"
            "    # Suma 15 a energia\n"
            "\n"
            "print('PORTAL ABIERTO')\n"
        ),
        "expected_output": "10\n25\n40\n55\nPORTAL ABIERTO",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El portal al núcleo del Nexo tiene un protocolo de seguridad: "
            "solo se abre cuando la energía supera el umbral crítico de 50 unidades. "
            "Cada ciclo del reactor añade 15 unidades. DAKI monitorea el proceso en tiempo real."
        ),
        "pedagogical_objective": (
            "Introducir while con condición numérica. La variable de control debe "
            "modificarse dentro del bucle para que la condición eventualmente sea falsa."
        ),
        "syntax_hint": (
            "while energia <= 50:\n"
            "    print(energia)\n"
            "    energia += 15\n"
            "print('PORTAL ABIERTO')"
        ),
        "theory_content": THEORY_N24,
        "hints_json": json.dumps([
            "El while repite mientras la condición sea verdadera. Necesitas que energia cambie.",
            "Dentro del while, después de imprimir energia, agrégale 15: energia += 15",
            "El print('PORTAL ABIERTO') va FUERA del while (sin indentación), al final.",
        ]),
    },
    # ── NIVEL 25 — break ──────────────────────────────────────────────────────
    {
        "title": "Señal de Corte",
        "description": (
            "El sistema de escucha recibe señales numéricas. "
            "Cuando detecta un `0`, debe interrumpir la transmisión.\n\n"
            "Lee números del `1` al `10` con un `for`. "
            "Si el número es `7`, imprime `SEÑAL CORTADA` y detén el bucle con `break`. "
            "De lo contrario, imprime el número.\n\n"
            "Salida esperada:\n"
            "```\n1\n2\n3\n4\n5\n6\nSEÑAL CORTADA\n```"
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "medium",
        "sector_id": 3,
        "level_order": 25,
        "base_xp_reward": 150,
        "is_project": False,
        "telemetry_goal_time": 150,
        "challenge_type": "python",
        "phase": "ciclos",
        "concepts_taught_json": json.dumps(["for", "break", "if dentro de bucle"]),
        "initial_code": (
            "# MISIÓN: Recorre del 1 al 10. Si el número es 7, para el bucle\n"
            "\n"
            "for i in range(1, 11):\n"
            "    if i == 7:\n"
            "        # Imprime SEÑAL CORTADA y detén el bucle\n"
            "        pass\n"
            "    else:\n"
            "        print(i)\n"
        ),
        "expected_output": "1\n2\n3\n4\n5\n6\nSEÑAL CORTADA",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "Los sensores del Nexo captan transmisiones de agentes externos. "
            "La señal 7 es el código de interrupción de emergencia. "
            "Cuando DAKI la detecta, el protocolo de escucha debe cortarse de inmediato "
            "para evitar la infiltración de datos corruptos en el núcleo."
        ),
        "pedagogical_objective": (
            "Usar break para interrumpir un bucle for. Combinar if/else dentro de un for."
        ),
        "syntax_hint": (
            "for i in range(1, 11):\n"
            "    if i == 7:\n"
            "        print('SEÑAL CORTADA')\n"
            "        break\n"
            "    else:\n"
            "        print(i)"
        ),
        "theory_content": THEORY_N25,
        "hints_json": json.dumps([
            "break termina el bucle por completo cuando se ejecuta. Ponlo dentro del if i == 7.",
            "El bloque if i == 7: debe tener dos líneas: print('SEÑAL CORTADA') y luego break.",
            "El else: maneja todos los demás números: simplemente print(i).",
        ]),
    },
    # ── NIVEL 26 — continue ───────────────────────────────────────────────────
    {
        "title": "Filtro de Interferencias",
        "description": (
            "El canal de transmisión tiene interferencias en los canales pares. "
            "Solo deben pasar las señales impares.\n\n"
            "Recorre los números del `1` al `10`. "
            "Si el número es par, **sáltalo** con `continue`. "
            "Si es impar, imprímelo.\n\n"
            "Salida esperada:\n"
            "```\n1\n3\n5\n7\n9\n```"
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "medium",
        "sector_id": 3,
        "level_order": 26,
        "base_xp_reward": 150,
        "is_project": False,
        "telemetry_goal_time": 150,
        "challenge_type": "python",
        "phase": "ciclos",
        "concepts_taught_json": json.dumps(["for", "continue", "módulo %"]),
        "initial_code": (
            "# MISIÓN: Imprime solo los números impares del 1 al 10\n"
            "\n"
            "for i in range(1, 11):\n"
            "    if i % 2 == 0:\n"
            "        # Salta los números pares\n"
            "        pass\n"
            "    print(i)\n"
        ),
        "expected_output": "1\n3\n5\n7\n9",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "Las señales pares del sector están corrompidas por parásitos electromagnéticos. "
            "El filtro de DAKI debe desechar toda señal cuya frecuencia sea divisible por 2. "
            "Solo las señales impares tienen integridad suficiente para llegar al Nexo."
        ),
        "pedagogical_objective": (
            "Usar continue para saltar iteraciones. Entender % (módulo) para "
            "detectar números pares/impares."
        ),
        "syntax_hint": (
            "for i in range(1, 11):\n"
            "    if i % 2 == 0:\n"
            "        continue\n"
            "    print(i)"
        ),
        "theory_content": THEORY_N26,
        "hints_json": json.dumps([
            "El operador % da el resto de la división. Si i % 2 == 0, el número es par.",
            "continue salta al inicio del siguiente ciclo sin ejecutar el resto del bloque.",
            "Reemplaza el pass con continue. El print(i) sigue ahí — continue lo salta para pares.",
        ]),
    },
    # ── NIVEL 27 — range con paso ─────────────────────────────────────────────
    {
        "title": "Cronómetro Táctico",
        "description": (
            "El sistema de conteo regresivo del Nexo opera en pasos de `10`. "
            "Genera la cuenta desde `50` hasta `10` inclusive, bajando de `10` en `10`.\n\n"
            "Usa `range()` con tres argumentos (inicio, fin, paso).\n\n"
            "Salida esperada:\n"
            "```\n50\n40\n30\n20\n10\n```"
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "medium",
        "sector_id": 3,
        "level_order": 27,
        "base_xp_reward": 175,
        "is_project": False,
        "telemetry_goal_time": 150,
        "challenge_type": "python",
        "phase": "ciclos",
        "concepts_taught_json": json.dumps(["for", "range(inicio, fin, paso)", "paso negativo"]),
        "initial_code": (
            "# MISIÓN: Imprime 50, 40, 30, 20, 10 usando range con paso negativo\n"
            "\n"
            "for tiempo in range(50, 9, -10):\n"
            "    # Imprime tiempo\n"
        ),
        "expected_output": "50\n40\n30\n20\n10",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El Cronómetro Táctico del Nexo inicia la secuencia de evacuación "
            "en cuenta regresiva. El reloj no descuenta de uno en uno — "
            "salta de 10 en 10 para maximizar la velocidad de respuesta. "
            "DAKI calibra el cronómetro para que termine exactamente en 10."
        ),
        "pedagogical_objective": (
            "Usar range con tres argumentos incluyendo paso negativo. "
            "Entender que con paso negativo el inicio > fin."
        ),
        "syntax_hint": "for tiempo in range(50, 9, -10):\n    print(tiempo)",
        "theory_content": None,
        "hints_json": json.dumps([
            "range(inicio, fin, paso) con paso negativo va en cuenta regresiva.",
            "Para incluir el 10 en la salida, el límite inferior debe ser 9 (exclusivo): range(50, 9, -10).",
            "Solución: for tiempo in range(50, 9, -10): con print(tiempo) dentro.",
        ]),
    },
    # ── NIVEL 28 — while con input ────────────────────────────────────────────
    {
        "title": "Protocolo de Reconocimiento",
        "description": (
            "El sistema de autenticación lee contraseñas hasta recibir la correcta.\n\n"
            "Lee contraseñas con `input()` en un `while True`. "
            "Si la contraseña es `NEXO-7`, imprime `ACCESO CONCEDIDO` y detén el bucle. "
            "Si no, imprime `CLAVE INCORRECTA`.\n\n"
            "Entradas de prueba: `hola`, `12345`, `NEXO-7`.\n\n"
            "Salida esperada:\n"
            "```\nCLAVE INCORRECTA\nCLAVE INCORRECTA\nACCESO CONCEDIDO\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 3,
        "level_order": 28,
        "base_xp_reward": 200,
        "is_project": False,
        "telemetry_goal_time": 200,
        "challenge_type": "python",
        "phase": "ciclos",
        "concepts_taught_json": json.dumps(["while True", "break", "input", "autenticación"]),
        "initial_code": (
            "# MISIÓN: Lee contraseñas hasta recibir 'NEXO-7'\n"
            "\n"
            "while True:\n"
            "    clave = input()\n"
            "    if clave == 'NEXO-7':\n"
            "        # Acceso concedido y salir del bucle\n"
            "        pass\n"
            "    else:\n"
            "        # Clave incorrecta\n"
            "        pass\n"
        ),
        "expected_output": "CLAVE INCORRECTA\nCLAVE INCORRECTA\nACCESO CONCEDIDO",
        "test_inputs_json": json.dumps(["hola", "12345", "NEXO-7"]),
        "lore_briefing": (
            "La sala de mando del Nexo tiene un sistema de acceso por contraseña. "
            "Un agente infiltrado intenta entrar con claves falsas. "
            "El protocolo debe rechazar cada intento inválido y registrar el acceso "
            "en cuanto se introduzca la clave maestra correcta: NEXO-7."
        ),
        "pedagogical_objective": (
            "Patrón while True + break. Combinar input() con lógica condicional "
            "dentro de un bucle indefinido."
        ),
        "syntax_hint": (
            "while True:\n"
            "    clave = input()\n"
            "    if clave == 'NEXO-7':\n"
            "        print('ACCESO CONCEDIDO')\n"
            "        break\n"
            "    else:\n"
            "        print('CLAVE INCORRECTA')"
        ),
        "theory_content": THEORY_N28,
        "hints_json": json.dumps([
            "while True crea un bucle infinito. Solo break puede salir de él.",
            "Dentro del if clave == 'NEXO-7': escribe primero el print y luego el break.",
            "El else: maneja las claves incorrectas: solo un print('CLAVE INCORRECTA').",
        ]),
    },
    # ── NIVEL 29 — for + acumulador con input ─────────────────────────────────
    {
        "title": "Escáner de Frecuencias",
        "description": (
            "El escáner recibe `n` frecuencias y necesita reportar cuántas están "
            "en la zona de peligro (mayores que `50`).\n\n"
            "Lee `n` y luego `n` números. Cuenta cuántos son mayores que `50` e imprímelo.\n\n"
            "Entradas: `4`, `30`, `60`, `45`, `80`.\n\n"
            "Salida esperada: `2`"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 3,
        "level_order": 29,
        "base_xp_reward": 250,
        "is_project": False,
        "telemetry_goal_time": 240,
        "challenge_type": "python",
        "phase": "ciclos",
        "concepts_taught_json": json.dumps(["for", "acumulador contador", "input en bucle", "if"]),
        "initial_code": (
            "# MISIÓN: Lee n frecuencias y cuenta cuántas superan 50\n"
            "\n"
            "n = int(input())\n"
            "peligro = 0\n"
            "\n"
            "for _ in range(n):\n"
            "    freq = int(input())\n"
            "    # Incrementa peligro si freq > 50\n"
            "\n"
            "print(peligro)\n"
        ),
        "expected_output": "2",
        "test_inputs_json": json.dumps(["4", "30", "60", "45", "80"]),
        "lore_briefing": (
            "El escáner de frecuencias del Nexo detecta transmisiones hostiles. "
            "Las frecuencias por encima de 50 kHz pertenecen a agentes enemigos. "
            "DAKI necesita saber cuántas señales de peligro hay en el scan actual "
            "para calcular el nivel de amenaza del sector."
        ),
        "pedagogical_objective": (
            "Patrón acumulador-contador: contar elementos que cumplen una condición "
            "en un bucle con input() dinámico."
        ),
        "syntax_hint": (
            "for _ in range(n):\n"
            "    freq = int(input())\n"
            "    if freq > 50:\n"
            "        peligro += 1\n"
            "print(peligro)"
        ),
        "theory_content": THEORY_N29,
        "hints_json": json.dumps([
            "Usa _ como variable del for cuando no necesitas el índice — solo iteras n veces.",
            "Dentro del bucle, lee cada frecuencia con int(input()) y compárala con 50.",
            "Si freq > 50, incrementa el contador: peligro += 1. Al final, print(peligro).",
        ]),
    },
    # ── NIVEL 30 — MINI-BOSS ──────────────────────────────────────────────────
    {
        "title": "NEXUS-03: El Bucle Parásito",
        "description": (
            "**MINI-BOSS — SECTOR 03**\n\n"
            "Un parásito digital se ha instalado en el núcleo y genera ciclos infinitos "
            "que consumen toda la energía del sistema. Para erradicarlo, debes "
            "implementar un escáner con control total de flujo.\n\n"
            "**Entrada:** `n` (número de señales a escanear).\n"
            "Luego `n` números enteros.\n\n"
            "**Protocolo de erradicación:**\n"
            "1. Suma todos los números.\n"
            "2. Cuenta cuántos son **negativos** (parásitos).\n"
            "3. Si hay parásitos, imprime `PARASITO DETECTADO: X` "
            "(X = cantidad de parásitos).\n"
            "4. Si no hay, imprime `SISTEMA LIMPIO`.\n"
            "5. Siempre imprime `SUMA TOTAL: Y` (Y = suma de todos).\n\n"
            "Entradas: `5`, `10`, `-3`, `7`, `-1`, `4`.\n\n"
            "Salida esperada:\n"
            "```\nPARASITO DETECTADO: 2\nSUMA TOTAL: 17\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "hard",
        "sector_id": 3,
        "level_order": 30,
        "base_xp_reward": 600,
        "is_project": True,
        "telemetry_goal_time": 360,
        "challenge_type": "python",
        "phase": "proyecto",
        "concepts_taught_json": json.dumps([
            "for", "while", "acumulador", "contador", "if/else", "break", "continue",
            "integración de ciclos"
        ]),
        "initial_code": (
            "# ╔═══════════════════════════════════════════════╗\n"
            "# ║  NEXUS-03: EL BUCLE PARÁSITO — MINI-BOSS     ║\n"
            "# ╚═══════════════════════════════════════════════╝\n"
            "#\n"
            "# Escanea n señales, detecta parásitos (negativos)\n"
            "# y reporta la suma total.\n"
            "\n"
            "n = int(input())\n"
            "suma = 0\n"
            "parasitos = 0\n"
            "\n"
            "for _ in range(n):\n"
            "    señal = int(input())\n"
            "    # Acumula la suma y cuenta los negativos\n"
            "\n"
            "# Imprime el resultado según el protocolo\n"
        ),
        "expected_output": "PARASITO DETECTADO: 2\nSUMA TOTAL: 17",
        "test_inputs_json": json.dumps(["5", "10", "-3", "7", "-1", "4"]),
        "lore_briefing": (
            "Operador, el Bucle Parásito es la amenaza más sofisticada del Sector 03. "
            "Se camufla entre señales legítimas como valores negativos, drenando energía "
            "en cada ciclo de proceso. DAKI ha localizado su firma: cualquier número "
            "menor que cero es un nodo parásito. "
            "Tu misión es erradicarlos contándolos, calcular el daño total (suma) "
            "y emitir el reporte de purificación. El Nexo depende de tu precisión."
        ),
        "pedagogical_objective": (
            "Proyecto integrador del Sector 03. Combina: for, acumulador de suma, "
            "contador con condición, if/else para el reporte final. "
            "Valida el dominio completo de ciclos y control de flujo."
        ),
        "syntax_hint": (
            "for _ in range(n):\n"
            "    señal = int(input())\n"
            "    suma += señal\n"
            "    if señal < 0:\n"
            "        parasitos += 1\n"
            "if parasitos > 0:\n"
            "    print(f'PARASITO DETECTADO: {parasitos}')\n"
            "else:\n"
            "    print('SISTEMA LIMPIO')\n"
            "print(f'SUMA TOTAL: {suma}')"
        ),
        "theory_content": None,
        "hints_json": json.dumps([
            "Necesitas dos acumuladores: uno suma todas las señales, otro cuenta las negativas.",
            "Dentro del for: suma += señal siempre. Y si señal < 0: parasitos += 1.",
            (
                "El if/else va FUERA del bucle (sin indentación). "
                "Luego print(f'SUMA TOTAL: {suma}') también fuera."
            ),
        ]),
    },
]


# ─── Lógica de población ──────────────────────────────────────────────────────

async def seed() -> None:
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with SessionLocal() as session:
        # Elimina solo el sector 03 previo (idempotente)
        deleted = await session.execute(
            delete(Challenge).where(Challenge.sector_id == 3)
        )
        deleted_count = deleted.rowcount
        await session.flush()
        print(f"🧹  Sector 03 anterior eliminado — {deleted_count} challenge(s) removidos.")

        print(f"\n🌱  Insertando {len(SECTOR_03)} niveles del Sector 03...\n")
        for data in SECTOR_03:
            challenge = Challenge(**data)
            session.add(challenge)
            project_flag = " ★ MINI-BOSS" if data["is_project"] else ""
            print(
                f"    [{data['level_order']:02d}/30] {data['title']:<38} "
                f"({data['difficulty'].upper()}, {data['base_xp_reward']} XP, "
                f"~{data['telemetry_goal_time']}s){project_flag}"
            )

        await session.commit()

    await engine.dispose()
    print(f"\n✅  Sector 03 cargado — {len(SECTOR_03)} niveles listos.")
    print("    Boss: NEXUS-03 El Bucle Parásito desbloqueado.\n")


if __name__ == "__main__":
    asyncio.run(seed())
