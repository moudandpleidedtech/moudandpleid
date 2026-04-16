"""
Seed — SECTOR 05: Arquitectura de Datos (10 niveles, IDs 31–40).

Uso (desde la raíz del proyecto):
    python -m scripts.seed_sector_05

Comportamiento:
    1. Elimina solo los challenges con sector_id = 4 (idempotente).
    2. Inserta los 10 niveles del Sector 04 con curva easy → medium → hard.
    3. El Nivel 40 es un Mini-Boss Proyecto Integrador (is_project = True).

Temática técnica: listas, diccionarios, def, parámetros, return.
Narrativa: gestión de inventario de fragmentos de memoria, módulos de ataque
           personalizados, mapeo de rutas de red.
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

THEORY_N31 = """\
## PROTOCOLO: Listas — El Inventario de Datos

Una **lista** es una colección ordenada de valores. Se define con corchetes `[]`.

```python
fragmentos = ["Alpha", "Beta", "Gamma"]
```

- Los elementos se acceden por **índice** (posición), empezando desde `0`
- El último elemento tiene índice `len(lista) - 1`
- Los índices negativos cuentan desde el final: `-1` es el último

```python
print(fragmentos[0])   # Alpha  (primero)
print(fragmentos[2])   # Gamma  (tercero)
print(fragmentos[-1])  # Gamma  (último)
```

---

## REGLA DE ORO

Las listas pueden contener cualquier tipo de dato: strings, enteros, floats, e incluso
otras listas. El índice siempre empieza en **cero**.
"""

THEORY_N32 = """\
## PROTOCOLO: append() y len() — Cargar el Inventario

Para añadir elementos a una lista en tiempo de ejecución usa `.append()`:

```python
inventario = []
inventario.append("Nodo-A")
inventario.append("Nodo-B")
# inventario es ahora ["Nodo-A", "Nodo-B"]
```

Para conocer cuántos elementos tiene una lista usa `len()`:

```python
print(len(inventario))   # 2
```

---

## OTROS MÉTODOS ÚTILES

| Método              | Efecto                            |
|---------------------|-----------------------------------|
| `lista.append(x)`   | Agrega `x` al final               |
| `lista.remove(x)`   | Elimina la primera aparición de x |
| `lista.pop()`       | Elimina y retorna el último       |
| `lista[i] = x`      | Reemplaza el elemento en índice i |
"""

THEORY_N33 = """\
## PROTOCOLO: Iterar Listas con for

Un bucle `for` puede recorrer directamente los elementos de una lista:

```python
fragmentos = ["Alpha", "Beta", "Gamma"]
for f in fragmentos:
    print(f)
# Alpha
# Beta
# Gamma
```

Si necesitas el índice además del valor, usa `enumerate()`:

```python
for i, f in enumerate(fragmentos):
    print(i, f)
# 0 Alpha
# 1 Beta
# 2 Gamma
```

---

## APLICACIÓN: Buscar en una lista

```python
objetivo = "Beta"
for f in fragmentos:
    if f == objetivo:
        print("Fragmento encontrado")
```
"""

THEORY_N34 = """\
## PROTOCOLO: Diccionarios — El Mapa de Red

Un **diccionario** almacena pares **clave → valor**. Se define con llaves `{}`.

```python
nodo = {
    "nombre": "NEXO-7",
    "energia": 100,
    "estado": "activo",
}
```

- Se accede al valor usando la **clave** entre corchetes
- Las claves son únicas dentro del mismo diccionario

```python
print(nodo["nombre"])   # NEXO-7
print(nodo["energia"])  # 100
```

---

## AGREGAR Y MODIFICAR

```python
nodo["sector"] = 4        # agrega una nueva clave
nodo["energia"] = 75      # modifica un valor existente
```

Para verificar si una clave existe: `"nombre" in nodo`
"""

THEORY_N35 = """\
## PROTOCOLO: Iterar Diccionarios

Para recorrer todos los pares clave-valor usa `.items()`:

```python
rutas = {"Norte": 42, "Sur": 15}
for clave, valor in rutas.items():
    print(clave, valor)
# Norte 42
# Sur 15
```

Otras formas de iterar:

| Método          | Itera sobre           |
|-----------------|-----------------------|
| `.keys()`       | Solo las claves       |
| `.values()`     | Solo los valores      |
| `.items()`      | Tuplas (clave, valor) |

---

## EJEMPLO TÁCTICO

```python
for nombre, distancia in rutas.items():
    print(f"{nombre}: {distancia} km")
```
"""

THEORY_N36 = """\
## PROTOCOLO: def — Crear un Módulo

Una **función** es un bloque de código reutilizable que se define con `def`.

```python
def activar_modulo():
    print("MODULO ACTIVADO")

activar_modulo()   # llamada — ejecuta el bloque
```

- `def` seguido del nombre y paréntesis `()`
- El bloque de la función debe estar **indentado**
- La función no hace nada hasta que es **llamada**

---

## REGLA DE ORO

Define la función **antes** de llamarla. Python lee el archivo de arriba
hacia abajo, así que si llamas la función antes de definirla, obtendrás
un `NameError`.
"""

THEORY_N37 = """\
## PROTOCOLO: Parámetros — Módulos Configurables

Los **parámetros** permiten pasar datos a la función cuando se la llama.

```python
def saludar(nombre, nivel):
    print(f"Operador {nombre}, nivel {nivel}")

saludar("Rex", 7)   # nombre="Rex", nivel=7
```

- Los parámetros se declaran entre los paréntesis de `def`
- Los **argumentos** son los valores que se pasan al llamar la función
- El orden de los argumentos importa (a menos que uses nombres)

---

## PARÁMETROS CON VALOR POR DEFECTO

```python
def saludar(nombre, nivel=1):
    print(f"Operador {nombre}, nivel {nivel}")

saludar("Rex")       # nivel toma el valor 1
saludar("Rex", 5)    # nivel toma el valor 5
```
"""

THEORY_N38 = """\
## PROTOCOLO: return — El Módulo que Responde

`return` hace que la función **devuelva** un valor al código que la llamó.

```python
def calcular_daño(ataque, defensa):
    return ataque - defensa

resultado = calcular_daño(100, 35)
print(resultado)   # 65
```

- Sin `return`, la función devuelve `None` implícitamente
- `return` **termina** la ejecución de la función inmediatamente
- El valor retornado puede asignarse a una variable o usarse directamente

---

## DIFERENCIA CLAVE

```python
# Con return → el valor sale de la función
def doble(x):
    return x * 2

# Sin return → imprime dentro, no devuelve nada útil
def doble_mal(x):
    print(x * 2)
```
"""

THEORY_N39 = """\
## PROTOCOLO: Funciones + Listas

Las funciones pueden recibir listas como parámetros y procesarlas.

```python
def suma_lista(lista):
    total = 0
    for x in lista:
        total += x
    return total

numeros = [10, 20, 30]
print(suma_lista(numeros))   # 60
```

También pueden construir y retornar listas nuevas:

```python
def duplicar(lista):
    resultado = []
    for x in lista:
        resultado.append(x * 2)
    return resultado

print(duplicar([1, 2, 3]))   # [2, 4, 6]
```

---

## PRINCIPIO DE RESPONSABILIDAD ÚNICA

Cada función debe hacer **una sola cosa** y hacerla bien.
Una función que suma es solo para sumar. No para imprimir.
"""


# ─── Niveles del Sector 04 ────────────────────────────────────────────────────

SECTOR_05 = [
    # ── NIVEL 31 — Listas: acceso por índice ─────────────────────────────────
    {
        "title": "Fragmentos de Memoria",
        "description": (
            "El almacén del Nexo registra fragmentos de memoria como una lista ordenada. "
            "Para recuperar datos, debes acceder por su posición exacta.\n\n"
            "Dada la lista `fragmentos = [\"Alpha\", \"Beta\", \"Gamma\", \"Delta\"]`, "
            "imprime el **primer** elemento y luego el **último**, cada uno en su línea.\n\n"
            "Salida esperada:\n"
            "```\nAlpha\nDelta\n```"
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "easy",
        "sector_id": 5,
        "level_order": 41,
        "base_xp_reward": 100,
        "is_project": False,
        "telemetry_goal_time": 90,
        "challenge_type": "python",
        "phase": "estructuras",
        "concepts_taught_json": json.dumps(["listas", "índices", "índice negativo"]),
        "initial_code": (
            "# MISIÓN: Imprime el primer y el último fragmento\n"
            "\n"
            'fragmentos = ["Alpha", "Beta", "Gamma", "Delta"]\n'
            "\n"
            "# Imprime el primer elemento (índice 0)\n"
            "print(fragmentos[___])\n"
            "\n"
            "# Imprime el último elemento (índice -1 o el numérico)\n"
            "print(fragmentos[___])\n"
        ),
        "expected_output": "Alpha\nDelta",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El almacén del Sector 04 tiene los fragmentos de memoria catalogados en orden. "
            "DAKI necesita recuperar el primero — el de mayor antigüedad — y el último, "
            "el más reciente, para inicializar el protocolo de sincronización temporal."
        ),
        "pedagogical_objective": (
            "Introducir listas y acceso por índice. "
            "Diferenciar índice 0 (primero) e índice -1 (último)."
        ),
        "syntax_hint": "print(fragmentos[0])\nprint(fragmentos[-1])",
        "theory_content": THEORY_N31,
        "hints_json": json.dumps([
            "Las listas usan índices que empiezan en 0. El primer elemento es fragmentos[0].",
            "Para el último elemento puedes usar el índice -1: fragmentos[-1].",
            "Solución: print(fragmentos[0]) y print(fragmentos[-1]).",
        ]),
    },
    # ── NIVEL 32 — append y len ───────────────────────────────────────────────
    {
        "title": "Cargando el Inventario",
        "description": (
            "El inventario de nodos del firewall empieza vacío. Debes cargarlo con "
            "tres nodos y verificar que el sistema los registró.\n\n"
            "Agrega `\"Nodo-A\"`, `\"Nodo-B\"` y `\"Nodo-C\"` a la lista `inventario`. "
            "Luego imprime el total de nodos registrados y el primer nodo.\n\n"
            "Salida esperada:\n"
            "```\n3\nNodo-A\n```"
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "easy",
        "sector_id": 5,
        "level_order": 42,
        "base_xp_reward": 100,
        "is_project": False,
        "telemetry_goal_time": 100,
        "challenge_type": "python",
        "phase": "estructuras",
        "concepts_taught_json": json.dumps(["listas", "append()", "len()"]),
        "initial_code": (
            "# MISIÓN: Agrega los tres nodos al inventario\n"
            "\n"
            "inventario = []\n"
            "\n"
            "# Agrega Nodo-A, Nodo-B y Nodo-C con .append()\n"
            "\n"
            "\n"
            "\n"
            "# Imprime cuántos nodos hay y el primero\n"
            "print(len(inventario))\n"
            "print(inventario[0])\n"
        ),
        "expected_output": "3\nNodo-A",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El firewall del Nexo perdió su registro de nodos en el último ataque. "
            "DAKI necesita que recargues manualmente los tres nodos de defensa primaria. "
            "El sistema confirma la carga imprimiendo el total registrado y el nodo principal."
        ),
        "pedagogical_objective": (
            "Usar .append() para agregar elementos a una lista vacía. "
            "Usar len() para obtener el tamaño. Combinar con acceso por índice."
        ),
        "syntax_hint": (
            "inventario.append(\"Nodo-A\")\n"
            "inventario.append(\"Nodo-B\")\n"
            "inventario.append(\"Nodo-C\")"
        ),
        "theory_content": THEORY_N32,
        "hints_json": json.dumps([
            "Para agregar un elemento al final de una lista usa: lista.append(elemento).",
            "Necesitas tres líneas de append(), una por cada nodo. El orden importa.",
            "Después de los tres .append(), print(len(inventario)) da 3 y print(inventario[0]) da Nodo-A.",
        ]),
    },
    # ── NIVEL 33 — Iterar lista ───────────────────────────────────────────────
    {
        "title": "Exploración Secuencial",
        "description": (
            "El escáner de fragmentos debe inspeccionar cada nodo del inventario "
            "en orden, uno por línea.\n\n"
            "Recorre la lista `sectores` con un `for` e imprime cada elemento.\n\n"
            "Salida esperada:\n"
            "```\nNexo-Norte\nNexo-Sur\nNexo-Este\nNexo-Oeste\n```"
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "easy",
        "sector_id": 5,
        "level_order": 43,
        "base_xp_reward": 125,
        "is_project": False,
        "telemetry_goal_time": 90,
        "challenge_type": "python",
        "phase": "estructuras",
        "concepts_taught_json": json.dumps(["for sobre lista", "iteración"]),
        "initial_code": (
            "# MISIÓN: Imprime cada sector del inventario\n"
            "\n"
            'sectores = ["Nexo-Norte", "Nexo-Sur", "Nexo-Este", "Nexo-Oeste"]\n'
            "\n"
            "for sector in sectores:\n"
            "    # Imprime el sector actual\n"
        ),
        "expected_output": "Nexo-Norte\nNexo-Sur\nNexo-Este\nNexo-Oeste",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "DAKI ha recibido el mapa de sectores activos del Nexo. "
            "El protocolo de exploración requiere verificar cada sector en orden, "
            "registrando su señal antes de pasar al siguiente. "
            "Un sector sin verificar puede convertirse en punto de entrada para el enemigo."
        ),
        "pedagogical_objective": (
            "Iterar directamente sobre los elementos de una lista con for. "
            "Sin necesidad de range() ni índices."
        ),
        "syntax_hint": "for sector in sectores:\n    print(sector)",
        "theory_content": THEORY_N33,
        "hints_json": json.dumps([
            "Un for puede recorrer una lista directamente: for x in lista — sin range().",
            "En cada iteración, la variable sector toma el valor del elemento actual.",
            "Dentro del for, solo necesitas print(sector).",
        ]),
    },
    # ── NIVEL 34 — Diccionario: creación y acceso ─────────────────────────────
    {
        "title": "Mapa de Nodo",
        "description": (
            "Cada nodo del Nexo tiene un registro con su nombre, sector y nivel de energía. "
            "Accede a los datos del nodo para el reporte de estado.\n\n"
            "Dado el diccionario `nodo`, imprime el valor de `\"nombre\"` "
            "y luego el de `\"energia\"`, cada uno en su línea.\n\n"
            "Salida esperada:\n"
            "```\nGamma-9\n85\n```"
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "easy",
        "sector_id": 5,
        "level_order": 44,
        "base_xp_reward": 125,
        "is_project": False,
        "telemetry_goal_time": 100,
        "challenge_type": "python",
        "phase": "estructuras",
        "concepts_taught_json": json.dumps(["diccionarios", "acceso por clave"]),
        "initial_code": (
            "# MISIÓN: Imprime el nombre y la energía del nodo\n"
            "\n"
            "nodo = {\n"
            '    "nombre":  "Gamma-9",\n'
            '    "sector":  4,\n'
            '    "energia": 85,\n'
            '    "estado":  "activo",\n'
            "}\n"
            "\n"
            '# Imprime el valor de la clave "nombre"\n'
            "print(nodo[___])\n"
            "\n"
            '# Imprime el valor de la clave "energia"\n'
            "print(nodo[___])\n"
        ),
        "expected_output": "Gamma-9\n85",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El nodo Gamma-9 envió una señal de estado al Nexo. "
            "DAKI necesita extraer dos campos específicos de su registro: "
            "el identificador del nodo y su nivel de energía actual, "
            "para incluirlos en el reporte táctico del sector."
        ),
        "pedagogical_objective": (
            "Introducir diccionarios. Acceder a valores con dict['clave']. "
            "Entender que las claves son strings con comillas."
        ),
        "syntax_hint": 'print(nodo["nombre"])\nprint(nodo["energia"])',
        "theory_content": THEORY_N34,
        "hints_json": json.dumps([
            "En un diccionario, accedes a un valor con: diccionario['clave'].",
            'Para la clave "nombre" escribe nodo["nombre"]. Las comillas son parte de la clave.',
            'Solución: print(nodo["nombre"]) y print(nodo["energia"]).',
        ]),
    },
    # ── NIVEL 35 — Diccionario: iterar .items() ───────────────────────────────
    {
        "title": "Rutas de Red",
        "description": (
            "El mapa de rutas del Nexo almacena el nombre de cada ruta y su distancia. "
            "Necesitas generar un reporte que muestre todas las rutas disponibles.\n\n"
            "Recorre el diccionario `rutas` con `.items()` e imprime cada par "
            "en el formato `ruta: distancia`.\n\n"
            "Salida esperada:\n"
            "```\nAlfa: 12\nBeta: 7\nGamma: 25\n```"
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "medium",
        "sector_id": 5,
        "level_order": 45,
        "base_xp_reward": 150,
        "is_project": False,
        "telemetry_goal_time": 150,
        "challenge_type": "python",
        "phase": "estructuras",
        "concepts_taught_json": json.dumps(["diccionarios", ".items()", "for sobre dict"]),
        "initial_code": (
            "# MISIÓN: Imprime cada ruta y su distancia en formato 'ruta: distancia'\n"
            "\n"
            "rutas = {\n"
            '    "Alfa":  12,\n'
            '    "Beta":  7,\n'
            '    "Gamma": 25,\n'
            "}\n"
            "\n"
            "for ruta, distancia in rutas.items():\n"
            "    # Imprime: 'ruta: distancia'\n"
        ),
        "expected_output": "Alfa: 12\nBeta: 7\nGamma: 25",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El módulo de navegación del Nexo tiene tres rutas activas hacia nodos remotos. "
            "Antes de lanzar el protocolo de reconocimiento, DAKI necesita el listado "
            "completo de rutas con sus distancias para calcular el tiempo de respuesta "
            "óptimo. Un solo error en el reporte puede causar un desvío de trayectoria."
        ),
        "pedagogical_objective": (
            "Iterar diccionarios con .items(). Desempaquetar clave y valor "
            "en dos variables del for. Formatear la salida con f-strings."
        ),
        "syntax_hint": "for ruta, distancia in rutas.items():\n    print(f\"{ruta}: {distancia}\")",
        "theory_content": THEORY_N35,
        "hints_json": json.dumps([
            ".items() devuelve cada par (clave, valor) del diccionario. Úsalos en el for.",
            "Desempaqueta con: for ruta, distancia in rutas.items() — dos variables en el for.",
            'Dentro del for usa: print(f"{ruta}: {distancia}") para el formato exacto.',
        ]),
    },
    # ── NIVEL 36 — def sin parámetros ─────────────────────────────────────────
    {
        "title": "Primer Módulo",
        "description": (
            "Para construir el sistema de ataque del Nexo, primero debes aprender a "
            "encapsular código en módulos reutilizables.\n\n"
            "Define una función `activar_modulo()` que imprima exactamente `MODULO ACTIVADO`. "
            "Luego llámala **dos veces**.\n\n"
            "Salida esperada:\n"
            "```\nMODULO ACTIVADO\nMODULO ACTIVADO\n```"
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "medium",
        "sector_id": 5,
        "level_order": 46,
        "base_xp_reward": 150,
        "is_project": False,
        "telemetry_goal_time": 120,
        "challenge_type": "python",
        "phase": "estructuras",
        "concepts_taught_json": json.dumps(["def", "función sin parámetros", "llamada"]),
        "initial_code": (
            "# MISIÓN: Define activar_modulo() y llámala dos veces\n"
            "\n"
            "def activar_modulo():\n"
            "    # Imprime 'MODULO ACTIVADO'\n"
            "    pass\n"
            "\n"
            "# Llama a la función dos veces\n"
        ),
        "expected_output": "MODULO ACTIVADO\nMODULO ACTIVADO",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El Nexo opera mediante módulos de software que pueden activarse en cualquier momento. "
            "DAKI te enseña el primer paso de la arquitectura modular: "
            "encapsular una acción en una función reutilizable. "
            "El mismo módulo puede activarse múltiples veces sin reescribir el código."
        ),
        "pedagogical_objective": (
            "Definir una función sin parámetros con def. "
            "Entender que la función debe ser llamada para ejecutarse. "
            "Ver la reutilización: llamar la misma función múltiples veces."
        ),
        "syntax_hint": (
            "def activar_modulo():\n"
            "    print('MODULO ACTIVADO')\n"
            "\n"
            "activar_modulo()\n"
            "activar_modulo()"
        ),
        "theory_content": THEORY_N36,
        "hints_json": json.dumps([
            "Reemplaza el pass con print('MODULO ACTIVADO'). El pass es solo un marcador vacío.",
            "Para llamar la función escribe su nombre seguido de (): activar_modulo()",
            "La función se llama dos veces: dos líneas con activar_modulo() después de la definición.",
        ]),
    },
    # ── NIVEL 37 — def con parámetros ─────────────────────────────────────────
    {
        "title": "Módulo de Identificación",
        "description": (
            "Los módulos del Nexo deben configurarse con datos del operador antes de activarse.\n\n"
            "Define `identificar(nombre, sector)` que imprima:\n"
            "`Operador: {nombre} | Sector: {sector}`\n\n"
            "Llámala con `\"Kira\"` y `4`.\n\n"
            "Salida esperada:\n"
            "```\nOperador: Kira | Sector: 4\n```"
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "medium",
        "sector_id": 5,
        "level_order": 47,
        "base_xp_reward": 175,
        "is_project": False,
        "telemetry_goal_time": 150,
        "challenge_type": "python",
        "phase": "estructuras",
        "concepts_taught_json": json.dumps(["def", "parámetros", "f-strings en funciones"]),
        "initial_code": (
            "# MISIÓN: Define identificar(nombre, sector) e imprímelo con el formato exacto\n"
            "\n"
            "def identificar(nombre, sector):\n"
            "    # Imprime: 'Operador: {nombre} | Sector: {sector}'\n"
            "    pass\n"
            "\n"
            'identificar("Kira", 4)\n'
        ),
        "expected_output": "Operador: Kira | Sector: 4",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "Cada módulo del sistema de combate del Nexo necesita ser identificado "
            "con el nombre del operador y el sector de despliegue antes de entrar en acción. "
            "DAKI diseñó este módulo de identificación para estandarizar el proceso "
            "de registro en todos los puntos de acceso."
        ),
        "pedagogical_objective": (
            "Definir funciones con parámetros. Usar los parámetros dentro de la función "
            "como variables locales. Pasar argumentos en la llamada."
        ),
        "syntax_hint": (
            "def identificar(nombre, sector):\n"
            '    print(f"Operador: {nombre} | Sector: {sector}")'
        ),
        "theory_content": THEORY_N37,
        "hints_json": json.dumps([
            "Los parámetros (nombre, sector) actúan como variables dentro de la función.",
            'Usa un f-string para el formato exacto: f"Operador: {nombre} | Sector: {sector}"',
            "Reemplaza el pass con el print del f-string. La llamada ya está hecha.",
        ]),
    },
    # ── NIVEL 38 — def con return ─────────────────────────────────────────────
    {
        "title": "Módulo de Daño",
        "description": (
            "El sistema de combate necesita calcular el daño neto de un ataque. "
            "La función debe devolver el resultado para que otros módulos lo usen.\n\n"
            "Define `calcular_dano(ataque, defensa)` que **retorne** `ataque - defensa`. "
            "Luego imprime el resultado de llamarla con `120` y `45`.\n\n"
            "Salida esperada:\n"
            "```\n75\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 5,
        "level_order": 48,
        "base_xp_reward": 200,
        "is_project": False,
        "telemetry_goal_time": 180,
        "challenge_type": "python",
        "phase": "estructuras",
        "concepts_taught_json": json.dumps(["def", "return", "valor de retorno"]),
        "initial_code": (
            "# MISIÓN: Define calcular_dano que retorne ataque - defensa\n"
            "\n"
            "def calcular_dano(ataque, defensa):\n"
            "    # Retorna la diferencia\n"
            "    pass\n"
            "\n"
            "resultado = calcular_dano(120, 45)\n"
            "print(resultado)\n"
        ),
        "expected_output": "75",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El módulo de combate del Nexo calcula el daño neto de cada ataque "
            "restando la defensa del enemigo al poder de ataque del operador. "
            "Este cálculo no se imprime directamente — se devuelve para que "
            "el sistema de puntuación lo registre y otros módulos lo aprovechen."
        ),
        "pedagogical_objective": (
            "Entender la diferencia entre print() dentro de una función y return. "
            "El valor retornado puede capturarse en una variable. "
            "return termina la ejecución de la función."
        ),
        "syntax_hint": (
            "def calcular_dano(ataque, defensa):\n"
            "    return ataque - defensa"
        ),
        "theory_content": THEORY_N38,
        "hints_json": json.dumps([
            "Reemplaza el pass con: return ataque - defensa",
            "return envía el resultado fuera de la función. La variable resultado lo captura.",
            "El print va FUERA de la función — la función solo calcula y retorna.",
        ]),
    },
    # ── NIVEL 39 — Función que procesa lista ──────────────────────────────────
    {
        "title": "Analizador de Fragmentos",
        "description": (
            "El analizador del Nexo necesita calcular la energía total de un conjunto "
            "de fragmentos para priorizar cuáles activar primero.\n\n"
            "Completa `suma_fragmentos(lista)` para que sume todos los elementos "
            "y **retorne** el total. Luego imprímelo.\n\n"
            "Salida esperada:\n"
            "```\n110\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 5,
        "level_order": 49,
        "base_xp_reward": 250,
        "is_project": False,
        "telemetry_goal_time": 200,
        "challenge_type": "python",
        "phase": "estructuras",
        "concepts_taught_json": json.dumps(["def", "return", "lista como parámetro", "acumulador"]),
        "initial_code": (
            "# MISIÓN: Completa suma_fragmentos para que sume y retorne el total\n"
            "\n"
            "def suma_fragmentos(lista):\n"
            "    total = 0\n"
            "    for fragmento in lista:\n"
            "        # Acumula el valor de cada fragmento\n"
            "        pass\n"
            "    return total\n"
            "\n"
            "energia = [15, 30, 25, 40]\n"
            "print(suma_fragmentos(energia))\n"
        ),
        "expected_output": "110",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El banco de fragmentos del Sector 04 almacena nodos de energía de diferentes "
            "potencias. Para saber si hay suficiente energía total para lanzar el protocolo "
            "de ataque, DAKI necesita un analizador que sume todos los valores del inventario "
            "y reporte el total disponible."
        ),
        "pedagogical_objective": (
            "Función que recibe una lista y la procesa con un acumulador. "
            "Combinar: parámetro lista, for dentro de función, acumulador, return."
        ),
        "syntax_hint": (
            "def suma_fragmentos(lista):\n"
            "    total = 0\n"
            "    for fragmento in lista:\n"
            "        total += fragmento\n"
            "    return total"
        ),
        "theory_content": THEORY_N39,
        "hints_json": json.dumps([
            "El pass es el marcador vacío. Reemplázalo con: total += fragmento",
            "total += fragmento suma el valor de cada elemento al acumulador.",
            "El return total ya está — solo falta la línea que acumula dentro del for.",
        ]),
    },
    # ── NIVEL 40 — MINI-BOSS: función que filtra pares ────────────────────────
    {
        "title": "NEXUS-04: El Filtro de Paridad",
        "description": (
            "**MINI-BOSS — SECTOR 04**\n\n"
            "El sistema de clasificación del Nexo necesita separar los fragmentos de energía "
            "estables (pares) de los inestables (impares). Solo los pares pueden "
            "integrarse al núcleo sin causar interferencias.\n\n"
            "**Tu misión:** Implementa `filtrar_pares(lista)` que reciba una lista de enteros "
            "y **retorne una nueva lista** con solo los números pares.\n\n"
            "**Entrada:** `n` (cantidad de fragmentos). Luego `n` números, uno por línea.\n\n"
            "**Salida:** Los números pares, uno por línea, en el orden en que aparecen.\n\n"
            "Entradas: `6`, `3`, `8`, `15`, `4`, `7`, `12`.\n\n"
            "Salida esperada:\n"
            "```\n8\n4\n12\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "hard",
        "sector_id": 5,
        "level_order": 50,
        "base_xp_reward": 700,
        "is_project": True,
        "telemetry_goal_time": 420,
        "challenge_type": "python",
        "phase": "proyecto",
        "concepts_taught_json": json.dumps([
            "def", "return", "listas", "append()", "for", "if", "módulo %",
            "función que construye y retorna lista", "integración"
        ]),
        "initial_code": (
            "# ╔══════════════════════════════════════════════╗\n"
            "# ║  NEXUS-04: EL FILTRO DE PARIDAD — MINI-BOSS ║\n"
            "# ╚══════════════════════════════════════════════╝\n"
            "#\n"
            "# Implementa filtrar_pares(lista):\n"
            "#   - Recorre la lista\n"
            "#   - Guarda los números pares en una nueva lista\n"
            "#   - Retorna esa lista\n"
            "\n"
            "def filtrar_pares(lista):\n"
            "    pares = []\n"
            "    for numero in lista:\n"
            "        # Si numero es par, agrégalo a 'pares'\n"
            "        pass\n"
            "    return pares\n"
            "\n"
            "\n"
            "# ── No modificar lo de abajo ──\n"
            "n = int(input())\n"
            "fragmentos = []\n"
            "for _ in range(n):\n"
            "    fragmentos.append(int(input()))\n"
            "\n"
            "resultado = filtrar_pares(fragmentos)\n"
            "for p in resultado:\n"
            "    print(p)\n"
        ),
        "expected_output": "8\n4\n12",
        "test_inputs_json": json.dumps(["6", "3", "8", "15", "4", "7", "12"]),
        "lore_briefing": (
            "Operador, el núcleo del Nexo solo puede procesar fragmentos de energía estable. "
            "La inestabilidad se manifiesta como un número impar de oscilaciones cuánticas. "
            "Tu misión es crear el filtro de clasificación definitivo: "
            "un módulo que separe los fragmentos estables (pares) de los caóticos (impares). "
            "Este módulo se convertirá en el clasificador permanente del Sector 04. "
            "DAKI confía en tu dominio de listas y funciones para proteger el núcleo."
        ),
        "pedagogical_objective": (
            "Proyecto integrador del Sector 04. Implementar una función que: "
            "recibe una lista, construye una lista de resultados con append(), "
            "filtra con if + módulo %, y retorna la lista filtrada. "
            "Combina todo el Sector 04: def, parámetros, return, listas, for, if."
        ),
        "syntax_hint": (
            "def filtrar_pares(lista):\n"
            "    pares = []\n"
            "    for numero in lista:\n"
            "        if numero % 2 == 0:\n"
            "            pares.append(numero)\n"
            "    return pares"
        ),
        "theory_content": None,
        "hints_json": json.dumps([
            "Un número es par si numero % 2 == 0. El operador % da el resto de la división.",
            "Dentro del for, usa: if numero % 2 == 0: pares.append(numero)",
            (
                "Reemplaza el pass con la condición y el append. "
                "La lista pares ya está creada arriba y el return ya está abajo — "
                "solo falta el if dentro del for."
            ),
        ]),
    },
]


# ─── Lógica de población ──────────────────────────────────────────────────────

async def seed() -> None:
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with SessionLocal() as session:
        deleted = await session.execute(
            delete(Challenge).where(Challenge.sector_id == 5)
        )
        deleted_count = deleted.rowcount
        await session.flush()
        print(f"🧹  Sector 04 anterior eliminado — {deleted_count} challenge(s) removidos.")

        print(f"\n🌱  Insertando {len(SECTOR_05)} niveles del Sector 04...\n")
        for data in SECTOR_05:
            challenge = Challenge(**data)
            session.add(challenge)
            project_flag = " ★ MINI-BOSS" if data["is_project"] else ""
            print(
                f"    [{data['level_order']:02d}/40] {data['title']:<38} "
                f"({data['difficulty'].upper()}, {data['base_xp_reward']} XP, "
                f"~{data['telemetry_goal_time']}s){project_flag}"
            )

        await session.commit()

    await engine.dispose()
    print(f"\n✅  Sector 04 cargado — {len(SECTOR_05)} niveles listos.")
    print("    Boss: NEXUS-04 El Filtro de Paridad desbloqueado.\n")


if __name__ == "__main__":
    asyncio.run(seed())
