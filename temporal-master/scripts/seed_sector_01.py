"""
Seed — SECTOR 01: Fundamentos de Python (10 niveles).

Uso (desde la raíz del proyecto):
    python -m scripts.seed_sector_01

Comportamiento:
    1. Elimina solo los challenges con sector_id = 1 (idempotente).
    2. Inserta los 10 niveles del Sector 01 con curva easy → medium → hard.
    3. El Nivel 10 es un Proyecto Integrador (is_project = True).
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

THEORY_N1 = """\
## PROTOCOLO: print() — Tu Primera Transmisión

`print()` es la función que muestra información en pantalla. Es la forma en que
tu programa "habla" con el mundo exterior.

```python
print("Hola, Mundo")
```

- El texto debe ir entre **comillas simples** `'...'` o **dobles** `"..."`
- `print()` agrega un salto de línea automático al final

---

## REGLA DE ORO

Cada instrucción va en su propia línea. Python ejecuta línea por línea,
de arriba hacia abajo.

```python
print("Primera línea")
print("Segunda línea")
```
"""

THEORY_N2 = """\
## PROTOCOLO: Variables — Cajas de Datos

Una **variable** es un nombre que guarda un valor en memoria.

```python
nombre = "Operador"
edad   = 25
```

- El `=` **asigna** el valor (no es igualdad matemática)
- El nombre va a la **izquierda**, el valor a la **derecha**
- Las cadenas de texto van entre comillas

---

## TIPOS BÁSICOS

| Tipo     | Ejemplo          | Descripción              |
|----------|------------------|--------------------------|
| `str`    | `"DAKI"`         | Texto (string)           |
| `int`    | `100`            | Número entero            |
| `float`  | `3.14`           | Número decimal           |
| `bool`   | `True` / `False` | Verdadero o Falso        |

```python
nombre = "Nexo"
print(nombre)    # → Nexo
```
"""

THEORY_N5 = """\
## PROTOCOLO: input() — Recibir Datos del Exterior

`input()` **pausa** el programa y espera que el usuario escriba algo.
Siempre devuelve texto (`str`).

```python
nombre = input()
print("Bienvenido, " + nombre)
```

---

## CONCATENACIÓN DE STRINGS

El operador `+` une cadenas de texto:

```python
saludo = "Hola, " + "Mundo"   # → "Hola, Mundo"
```

⚠️  Solo puedes unir strings con strings. Para combinar números:

```python
nivel = 7
print("Nivel: " + str(nivel))   # convierte int → str primero
```
"""

THEORY_N6 = """\
## PROTOCOLO: Operaciones Aritméticas

Python puede operar como calculadora:

| Operador | Descripción       | Ejemplo        | Resultado |
|----------|-------------------|----------------|-----------|
| `+`      | Suma              | `30 + 70`      | `100`     |
| `-`      | Resta             | `100 - 25`     | `75`      |
| `*`      | Multiplicación    | `5 * 20`       | `100`     |
| `/`      | División real     | `10 / 3`       | `3.333…`  |
| `//`     | División entera   | `10 // 3`      | `3`       |
| `%`      | Módulo (resto)    | `10 % 3`       | `1`       |

---

## CONVERTIR input() A NÚMERO

`input()` siempre devuelve texto. Para operar con él:

```python
a = int(input())   # convierte "30" → 30
b = int(input())
print(a + b)       # → 100
```
"""

THEORY_N8 = """\
## PROTOCOLO: f-strings — Texto Dinámico

Los **f-strings** permiten insertar variables dentro de un texto
sin concatenar manualmente:

```python
nombre = "DAKI"
nivel  = 7
print(f"Operador {nombre} — Nivel {nivel}")
# → Operador DAKI — Nivel 7
```

- Pon una `f` antes de la comilla: `f"..."`
- Las variables van entre `{}` dentro del string

---

## COMPARACIÓN CON CONCATENACIÓN

```python
# ❌ Tedioso
print("Operador " + nombre + " — Nivel " + str(nivel))

# ✅ Limpio con f-string
print(f"Operador {nombre} — Nivel {nivel}")
```
"""

THEORY_N9 = """\
## PROTOCOLO: if / else — Tomar Decisiones

El bloque `if` ejecuta código **solo si la condición es verdadera**.
`else` cubre el caso contrario.

```python
energia = int(input())

if energia > 50:
    print("SISTEMAS ACTIVOS")
else:
    print("RESERVA CRÍTICA")
```

- La condición no lleva paréntesis (aunque puedes ponerlos)
- El bloque indentado con **4 espacios** pertenece al `if`/`else`
- `>`, `<`, `>=`, `<=`, `==`, `!=` son los operadores de comparación

---

## OPERADORES DE COMPARACIÓN

| Operador | Significado      |
|----------|------------------|
| `==`     | igual a          |
| `!=`     | distinto de      |
| `>`      | mayor que        |
| `<`      | menor que        |
| `>=`     | mayor o igual    |
| `<=`     | menor o igual    |
"""

# ─── Definición de los 10 niveles ────────────────────────────────────────────

SECTOR_01 = [
    # ── NIVEL 1 ──────────────────────────────────────────────────────────────
    {
        "title": "Hola, Mundo Real",
        "description": (
            "El sistema está en silencio. Tu primera misión es hacerte notar.\n\n"
            "Usa `print()` para mostrar exactamente el mensaje: `Hola, Mundo`"
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "easy",
        "sector_id": 1,
        "level_order": 1,
        "base_xp_reward": 50,
        "is_project": False,
        "telemetry_goal_time": 60,
        "challenge_type": "python",
        "phase": "fundamentos",
        "concepts_taught_json": json.dumps(["print", "strings"]),
        "initial_code": (
            "# MISIÓN: Imprime exactamente el siguiente mensaje\n"
            "# Hola, Mundo\n"
            "\n"
        ),
        "expected_output": "Hola, Mundo",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "Operador, el sistema está en silencio total. Ningún pulso activo. "
            "DAKI necesita una señal para confirmar que el enlace funciona. "
            "Transmite tu primera señal al Nexo."
        ),
        "pedagogical_objective": "Aprender a usar print() para mostrar texto en pantalla.",
        "syntax_hint": 'print("Hola, Mundo")',
        "theory_content": THEORY_N1,
        "hints_json": json.dumps([
            "Operador, necesitas una función que envíe texto a la pantalla. Se llama print().",
            "Escribe print() y dentro del paréntesis pon el mensaje entre comillas dobles.",
            'La solución exacta es: print("Hola, Mundo") — con la coma y el espacio incluidos.',
        ]),
    },
    # ── NIVEL 2 ──────────────────────────────────────────────────────────────
    {
        "title": "Identidad Digital",
        "description": (
            "DAKI necesita una etiqueta para rastrearte en el Nexo.\n\n"
            "Crea una variable llamada `nombre` con el valor `\"Operador\"` "
            "e imprímela."
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "easy",
        "sector_id": 1,
        "level_order": 2,
        "base_xp_reward": 75,
        "is_project": False,
        "telemetry_goal_time": 90,
        "challenge_type": "python",
        "phase": "fundamentos",
        "concepts_taught_json": json.dumps(["variables", "strings", "print"]),
        "initial_code": (
            "# MISIÓN: Crea la variable 'nombre' con el valor 'Operador' e imprímela\n"
            "\n"
            "nombre = \n"
            "print(nombre)\n"
        ),
        "expected_output": "Operador",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "Sin identificación, el Nexo te trata como un agente anónimo. "
            "Registra tu etiqueta en el sistema para que DAKI pueda autenticarte "
            "en los protocolos avanzados."
        ),
        "pedagogical_objective": "Declarar y usar variables de tipo string. Imprimir su valor.",
        "syntax_hint": 'nombre = "Operador"\nprint(nombre)',
        "theory_content": THEORY_N2,
        "hints_json": json.dumps([
            "Una variable guarda un valor. Usa el símbolo = para asignar: nombre = ...",
            "El valor es un texto, así que debe ir entre comillas: nombre = \"Operador\"",
            'Completa: nombre = "Operador" y en la siguiente línea print(nombre).',
        ]),
    },
    # ── NIVEL 3 ──────────────────────────────────────────────────────────────
    {
        "title": "Carga de Energía",
        "description": (
            "El firewall consume recursos. DAKI necesita conocer nuestra reserva.\n\n"
            "Crea una variable `energia` con el valor entero `100` e imprímela."
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "easy",
        "sector_id": 1,
        "level_order": 3,
        "base_xp_reward": 75,
        "is_project": False,
        "telemetry_goal_time": 90,
        "challenge_type": "python",
        "phase": "fundamentos",
        "concepts_taught_json": json.dumps(["variables", "int", "print"]),
        "initial_code": (
            "# MISIÓN: Crea la variable 'energia' con valor 100 e imprímela\n"
            "\n"
            "energia = \n"
            "print(energia)\n"
        ),
        "expected_output": "100",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "Los sensores del Nexo reportan niveles de energía críticos. "
            "Antes de lanzar cualquier protocolo, el sistema necesita verificar "
            "que la reserva de poder está al máximo."
        ),
        "pedagogical_objective": "Diferenciar variables de tipo int vs str. Los enteros no usan comillas.",
        "syntax_hint": "energia = 100\nprint(energia)",
        "theory_content": None,
        "hints_json": json.dumps([
            "Los números enteros no necesitan comillas — son simplemente el número: energia = 100",
            "A diferencia de los strings, los int se escriben sin comillas: 100, no \"100\".",
            "Completa: energia = 100 y en la siguiente línea print(energia).",
        ]),
    },
    # ── NIVEL 4 ──────────────────────────────────────────────────────────────
    {
        "title": "Dos Fuerzas",
        "description": (
            "El sistema de combate necesita registrar dos parámetros del operador.\n\n"
            "Crea dos variables: `ataque = 75` y `defensa = 50`. "
            "Imprime `ataque` en la primera línea y `defensa` en la segunda."
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "easy",
        "sector_id": 1,
        "level_order": 4,
        "base_xp_reward": 100,
        "is_project": False,
        "telemetry_goal_time": 120,
        "challenge_type": "python",
        "phase": "fundamentos",
        "concepts_taught_json": json.dumps(["variables", "int", "múltiples variables"]),
        "initial_code": (
            "# MISIÓN: Define ataque=75 y defensa=50, imprime cada una en su línea\n"
            "\n"
            "ataque  = \n"
            "defensa = \n"
            "\n"
            "print(ataque)\n"
            "print(defensa)\n"
        ),
        "expected_output": "75\n50",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El módulo táctico del Nexo requiere dos parámetros para calcular "
            "la probabilidad de éxito en una incursión: fuerza de ataque y escudo defensivo. "
            "Carga ambos vectores en el sistema."
        ),
        "pedagogical_objective": "Gestionar múltiples variables. Entender que cada print() agrega una línea nueva.",
        "syntax_hint": "ataque = 75\ndefensa = 50\nprint(ataque)\nprint(defensa)",
        "theory_content": None,
        "hints_json": json.dumps([
            "Puedes tener tantas variables como necesites. Cada una en su propia línea.",
            "Para imprimir dos valores en líneas separadas, usa dos print() distintos.",
            "Define: ataque = 75 y defensa = 50. Luego print(ataque) y print(defensa).",
        ]),
    },
    # ── NIVEL 5 ──────────────────────────────────────────────────────────────
    {
        "title": "El Nombre en el Sistema",
        "description": (
            "El Nexo recibe operadores desde el exterior. Necesitas leer su identificador.\n\n"
            "Lee un nombre con `input()` y muestra: `Bienvenido, ` seguido del nombre.\n"
            "Ejemplo: si el nombre es `Operador`, imprime `Bienvenido, Operador`."
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "easy",
        "sector_id": 1,
        "level_order": 5,
        "base_xp_reward": 125,
        "is_project": False,
        "telemetry_goal_time": 150,
        "challenge_type": "python",
        "phase": "fundamentos",
        "concepts_taught_json": json.dumps(["input", "concatenación", "strings"]),
        "initial_code": (
            "# MISIÓN: Lee un nombre e imprime 'Bienvenido, ' + el nombre\n"
            "\n"
            "nombre = input()\n"
            "# TU CÓDIGO AQUÍ\n"
        ),
        "expected_output": "Bienvenido, Operador",
        "test_inputs_json": json.dumps(["Operador"]),
        "lore_briefing": (
            "Los nuevos agentes se conectan al Nexo sin identificación. "
            "DAKI necesita un protocolo de bienvenida que lea el nombre del operador "
            "y lo registre en el sistema de acceso."
        ),
        "pedagogical_objective": "Usar input() para capturar datos. Concatenar strings con el operador +.",
        "syntax_hint": 'nombre = input()\nprint("Bienvenido, " + nombre)',
        "theory_content": THEORY_N5,
        "hints_json": json.dumps([
            "input() lee lo que el usuario escribe y lo guarda como texto. Asígnalo a una variable.",
            'Para unir dos textos usa el operador +: "Bienvenido, " + nombre',
            'El código completo es: nombre = input() y print("Bienvenido, " + nombre).',
        ]),
    },
    # ── NIVEL 6 ──────────────────────────────────────────────────────────────
    {
        "title": "Suma de Poder",
        "description": (
            "Dos reactores de energía envían su carga al Nexo. DAKI necesita el total.\n\n"
            "Lee dos números enteros (uno por línea) y muestra su suma.\n"
            "Ejemplo: `30` y `70` → `100`."
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "medium",
        "sector_id": 1,
        "level_order": 6,
        "base_xp_reward": 150,
        "is_project": False,
        "telemetry_goal_time": 180,
        "challenge_type": "python",
        "phase": "fundamentos",
        "concepts_taught_json": json.dumps(["int()", "aritmética", "input"]),
        "initial_code": (
            "# MISIÓN: Lee dos números e imprime su suma\n"
            "\n"
            "a = int(input())\n"
            "b = int(input())\n"
            "\n"
            "# Imprime la suma de a y b\n"
        ),
        "expected_output": "100",
        "test_inputs_json": json.dumps(["30", "70"]),
        "lore_briefing": (
            "Los dos reactores principales del Nexo reportan su nivel de carga por separado. "
            "Para calcular si tenemos energía suficiente para el siguiente protocolo, "
            "necesitamos sumar ambas reservas."
        ),
        "pedagogical_objective": "Convertir strings a int con int(). Realizar operaciones aritméticas básicas.",
        "syntax_hint": "a = int(input())\nb = int(input())\nprint(a + b)",
        "theory_content": THEORY_N6,
        "hints_json": json.dumps([
            "input() siempre devuelve texto. Para operar con números debes convertirlo: int(input())",
            "Una vez que tienes a y b como enteros, puedes sumarlos directamente: a + b",
            "La solución es: a = int(input()), b = int(input()), print(a + b).",
        ]),
    },
    # ── NIVEL 7 ──────────────────────────────────────────────────────────────
    {
        "title": "División Táctica",
        "description": (
            "El sistema necesita distribuir recursos en unidades iguales.\n\n"
            "Lee dos enteros: `total` y `divisor`. Imprime:\n"
            "- Línea 1: el resultado de la **división entera** (`//`)\n"
            "- Línea 2: el **resto** (`%`)\n\n"
            "Ejemplo: `100` y `3` → `33` y `1`."
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "medium",
        "sector_id": 1,
        "level_order": 7,
        "base_xp_reward": 175,
        "is_project": False,
        "telemetry_goal_time": 200,
        "challenge_type": "python",
        "phase": "fundamentos",
        "concepts_taught_json": json.dumps(["//", "%", "división entera", "módulo"]),
        "initial_code": (
            "# MISIÓN: Lee total y divisor. Imprime división entera y luego el resto.\n"
            "\n"
            "total   = int(input())\n"
            "divisor = int(input())\n"
            "\n"
            "# Imprime total // divisor\n"
            "# Imprime total % divisor\n"
        ),
        "expected_output": "33\n1",
        "test_inputs_json": json.dumps(["100", "3"]),
        "lore_briefing": (
            "El Nexo necesita repartir 100 unidades de energía entre 3 nodos de defensa. "
            "Cada nodo recibe la misma cantidad. Las unidades restantes quedan en reserva. "
            "Calcula la distribución exacta."
        ),
        "pedagogical_objective": "Entender la diferencia entre / (real), // (entera) y % (módulo).",
        "syntax_hint": "print(total // divisor)\nprint(total % divisor)",
        "theory_content": None,
        "hints_json": json.dumps([
            "En Python, // es la división que ignora los decimales: 100 // 3 = 33.",
            "El operador % devuelve lo que sobra: 100 % 3 = 1 (porque 33 × 3 = 99).",
            "Usa print(total // divisor) en la primera línea y print(total % divisor) en la segunda.",
        ]),
    },
    # ── NIVEL 8 ──────────────────────────────────────────────────────────────
    {
        "title": "Protocolo de Identificación",
        "description": (
            "DAKI genera credenciales formateadas para cada operador.\n\n"
            "Lee un `nombre` y un `nivel` (entero). Imprime exactamente:\n"
            "`Operador {nombre} - Nivel {nivel}`\n\n"
            "Ejemplo: `DAKI` y `7` → `Operador DAKI - Nivel 7`."
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "medium",
        "sector_id": 1,
        "level_order": 8,
        "base_xp_reward": 200,
        "is_project": False,
        "telemetry_goal_time": 200,
        "challenge_type": "python",
        "phase": "fundamentos",
        "concepts_taught_json": json.dumps(["f-strings", "formato", "variables mixtas"]),
        "initial_code": (
            "# MISIÓN: Imprime 'Operador {nombre} - Nivel {nivel}' usando f-string\n"
            "\n"
            "nombre = input()\n"
            "nivel  = int(input())\n"
            "\n"
            '# print(f"Operador ...)\n'
        ),
        "expected_output": "Operador DAKI - Nivel 7",
        "test_inputs_json": json.dumps(["DAKI", "7"]),
        "lore_briefing": (
            "El sistema de autenticación del Nexo emite credenciales con formato estándar. "
            "Cada vez que un operador se conecta, DAKI genera su placa de identificación "
            "con nombre y nivel de acceso."
        ),
        "pedagogical_objective": "Usar f-strings para formatear texto dinámico con variables de distintos tipos.",
        "syntax_hint": 'print(f"Operador {nombre} - Nivel {nivel}")',
        "theory_content": THEORY_N8,
        "hints_json": json.dumps([
            "Los f-strings te permiten insertar variables dentro de un texto usando {}. Empieza con f\"...\"",
            'Pon la f antes de la comilla y usa {} para cada variable: f"Texto {variable}"',
            'La solución: print(f"Operador {nombre} - Nivel {nivel}") — usa guión simple (-).',
        ]),
    },
    # ── NIVEL 9 ──────────────────────────────────────────────────────────────
    {
        "title": "La Primera Decisión",
        "description": (
            "El Nexo evalúa el estado del sistema antes de cada operación.\n\n"
            "Lee un número entero `energia`. Si es mayor a `50`, imprime "
            "`SISTEMAS ACTIVOS`. De lo contrario, imprime `RESERVA CRÍTICA`."
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "medium",
        "sector_id": 1,
        "level_order": 9,
        "base_xp_reward": 250,
        "is_project": False,
        "telemetry_goal_time": 240,
        "challenge_type": "python",
        "phase": "fundamentos",
        "concepts_taught_json": json.dumps(["if", "else", "comparación", "condicionales"]),
        "initial_code": (
            "# MISIÓN: Lee energia. Si > 50 imprime 'SISTEMAS ACTIVOS', si no 'RESERVA CRÍTICA'\n"
            "\n"
            "energia = int(input())\n"
            "\n"
            "if energia > 50:\n"
            "    # Tu código aquí\n"
            "else:\n"
            "    # Tu código aquí\n"
        ),
        "expected_output": "SISTEMAS ACTIVOS",
        "test_inputs_json": json.dumps(["75"]),
        "lore_briefing": (
            "Antes de activar cualquier protocolo del Nexo, DAKI verifica el nivel de energía. "
            "Si los recursos son suficientes, los sistemas se activan. "
            "Si no, se entra en modo de reserva crítica para preservar el núcleo."
        ),
        "pedagogical_objective": "Introducir if/else. Entender la indentación y los operadores de comparación.",
        "syntax_hint": "if energia > 50:\n    print('SISTEMAS ACTIVOS')\nelse:\n    print('RESERVA CRÍTICA')",
        "theory_content": THEORY_N9,
        "hints_json": json.dumps([
            "if comprueba una condición. Si es verdadera, ejecuta el bloque indentado debajo.",
            "El bloque después del if debe tener 4 espacios de indentación. Lo mismo para el else.",
            "Dentro del if: print('SISTEMAS ACTIVOS'). Dentro del else: print('RESERVA CRÍTICA').",
        ]),
    },
    # ── NIVEL 10 — PROYECTO INTEGRADOR ───────────────────────────────────────
    {
        "title": "NEXUS-01: Perfil del Operador",
        "description": (
            "**PROYECTO INTEGRADOR — SECTOR 01**\n\n"
            "Es el momento de demostrar todo lo aprendido. Construye un programa "
            "completo que genere el perfil de un operador.\n\n"
            "**Entrada:** nombre (str) y nivel (int), uno por línea.\n\n"
            "**Salida esperada:**\n"
            "```\n"
            "=== PERFIL DEL OPERADOR ===\n"
            "Nombre: {nombre}\n"
            "Nivel: {nivel}\n"
            "Estado: ACTIVO\n"
            "```\n\n"
            "Ejemplo: `Operador` y `5` → el perfil con esos datos."
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "hard",
        "sector_id": 1,
        "level_order": 10,
        "base_xp_reward": 500,
        "is_project": True,
        "telemetry_goal_time": 300,
        "challenge_type": "python",
        "phase": "proyecto",
        "concepts_taught_json": json.dumps([
            "variables", "input", "int()", "f-strings", "print", "integración"
        ]),
        "initial_code": (
            "# ╔══════════════════════════════════════════════╗\n"
            "# ║  NEXUS-01: PROYECTO INTEGRADOR — SECTOR 01  ║\n"
            "# ╚══════════════════════════════════════════════╝\n"
            "#\n"
            "# Construye el perfil del operador con todo lo aprendido.\n"
            "# Entrada: nombre (str) y nivel (int), uno por línea.\n"
            "\n"
            "nombre = input()\n"
            "nivel  = int(input())\n"
            "\n"
            "# Imprime el perfil completo (4 líneas exactas)\n"
        ),
        "expected_output": (
            "=== PERFIL DEL OPERADOR ===\n"
            "Nombre: Operador\n"
            "Nivel: 5\n"
            "Estado: ACTIVO"
        ),
        "test_inputs_json": json.dumps(["Operador", "5"]),
        "lore_briefing": (
            "Operador, has completado el entrenamiento básico del Nexo. "
            "La prueba final es construir tu propia placa de identidad digital. "
            "DAKI necesita verificar que puedes integrar variables, entrada de datos "
            "y formato en un solo programa funcional. El sistema te observa."
        ),
        "pedagogical_objective": (
            "Proyecto integrador del Sector 01. Combina: variables, input(), int(), "
            "f-strings y múltiples print() para construir una salida estructurada."
        ),
        "syntax_hint": (
            'print("=== PERFIL DEL OPERADOR ===")\n'
            'print(f"Nombre: {nombre}")\n'
            'print(f"Nivel: {nivel}")\n'
            'print("Estado: ACTIVO")'
        ),
        "theory_content": None,
        "hints_json": json.dumps([
            "Necesitas 4 print() en total. El primero y el último son textos fijos sin variables.",
            "Para las líneas 2 y 3 usa f-strings: f\"Nombre: {nombre}\" y f\"Nivel: {nivel}\"",
            (
                "Solución: print(\"=== PERFIL DEL OPERADOR ===\"), "
                "print(f\"Nombre: {nombre}\"), print(f\"Nivel: {nivel}\"), print(\"Estado: ACTIVO\")"
            ),
        ]),
    },
]


# ─── Lógica de población ──────────────────────────────────────────────────────

async def seed() -> None:
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with SessionLocal() as session:
        # Elimina solo el sector 01 previo (idempotente)
        deleted = await session.execute(
            delete(Challenge).where(Challenge.sector_id == 1)
        )
        deleted_count = deleted.rowcount
        await session.flush()
        print(f"🧹  Sector 01 anterior eliminado — {deleted_count} challenge(s) removidos.")

        print(f"\n🌱  Insertando {len(SECTOR_01)} niveles del Sector 01...\n")
        for data in SECTOR_01:
            challenge = Challenge(**data)
            session.add(challenge)
            project_flag = " ★ PROYECTO" if data["is_project"] else ""
            print(
                f"    [{data['level_order']:02d}/10] {data['title']:<35} "
                f"({data['difficulty'].upper()}, {data['base_xp_reward']} XP, "
                f"~{data['telemetry_goal_time']}s){project_flag}"
            )

        await session.commit()

    await engine.dispose()
    print(f"\n✅  Sector 01 cargado — {len(SECTOR_01)} niveles listos.")
    print("    Tip: ejecuta seed_database.py si necesitas restaurar las misiones originales.\n")


if __name__ == "__main__":
    asyncio.run(seed())
