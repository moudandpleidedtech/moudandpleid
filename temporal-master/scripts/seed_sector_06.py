"""
Seed — SECTOR 06: Bóvedas de Memoria (9 niveles, IDs 51–59).

Uso (desde la raíz del proyecto):
    python -m scripts.seed_sector_06

Comportamiento:
    1. Elimina solo los challenges con sector_id=6 y level_order < 60 (preserva CONTRATO-60).
    2. Inserta los 9 niveles del Sector 06 con curva easy → medium → hard.
    3. El nivel 60 (Boss) vive en seed_contratos.py — no se toca aquí.

Temática técnica: tuplas (creación, acceso, desempaquetado), sets (conjuntos,
                  .add(), operaciones de conjunto), diccionarios anidados,
                  listas de diccionarios (búsqueda, filtrado, agregación).
Narrativa: optimización de almacenamiento, mapeo de la base de datos del Nexo.
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

THEORY_N51 = """\
## PROTOCOLO: Tuplas — Registros Inmutables

Una **tupla** es una colección ordenada e **inmutable** de valores.
Se define con paréntesis `()`:

```python
coordenada = (10, 25)
registro   = ("NEXO-7", 42, "ACTIVO")
```

Se accede por índice igual que una lista:

```python
print(coordenada[0])    # 10
print(coordenada[1])    # 25
print(registro[-1])     # "ACTIVO"
```

---

## INMUTABILIDAD

A diferencia de las listas, las tuplas **no se pueden modificar** después de crearse:

```python
coords = (5, 3)
coords[0] = 10   # ← TypeError: 'tuple' object does not support item assignment
```

---

## ¿CUÁNDO USAR TUPLAS?

- Datos que **no deben cambiar**: coordenadas, RGB, credenciales
- **Retornar múltiples valores** desde una función
- Como **claves de diccionario** (las listas no pueden serlo)
"""

THEORY_N52 = """\
## PROTOCOLO: Desempaquetado de Tuplas

El **desempaquetado** asigna los elementos de una tupla a variables individuales en una sola línea:

```python
registro = ("NEXO-7", 42, "ACTIVO")

# Sin desempaquetado (tedioso):
nombre = registro[0]
nivel  = registro[1]
estado = registro[2]

# Con desempaquetado (elegante):
nombre, nivel, estado = registro
```

El número de variables debe coincidir con el número de elementos de la tupla.

---

## DESEMPAQUETADO EN for

Muy útil al iterar listas de tuplas:

```python
puntos = [(1, 2), (3, 4), (5, 6)]
for x, y in puntos:
    print(f"({x}, {y})")
```

---

## RETORNO MÚLTIPLE

Las funciones pueden "retornar" múltiples valores empaquetados en una tupla:

```python
def minmax(lista):
    return min(lista), max(lista)

minimo, maximo = minmax([3, 1, 4, 1, 5])
```
"""

THEORY_N53 = """\
## PROTOCOLO: Sets — Conjuntos Sin Duplicados

Un **set** es una colección **desordenada** de elementos **únicos**.
Se define con llaves `{}` o con `set()`:

```python
accesos = {"Alpha", "Beta", "Gamma"}
vacío   = set()   # ← set(), no {} (eso crea un dict vacío)
```

---

## OPERACIONES BÁSICAS

```python
accesos = {"Alpha", "Beta"}
accesos.add("Gamma")       # agrega un elemento
accesos.add("Alpha")       # ← ignorado, ya existe
accesos.remove("Beta")     # elimina (KeyError si no existe)
accesos.discard("Beta")    # elimina si existe, sin error si no

print("Alpha" in accesos)  # True — verificación O(1)
print(len(accesos))        # 2
```

---

## IMPORTANTE: Los Sets son Desordenados

El orden de iteración es **impredecible**. Para salida determinista usa `sorted()`:

```python
for elemento in sorted(accesos):
    print(elemento)
```
"""

THEORY_N54 = """\
## PROTOCOLO: Operaciones de Conjuntos

Los sets soportan las operaciones matemáticas de la teoría de conjuntos:

| Operación       | Sintaxis Python          | Descripción                          |
|-----------------|--------------------------|--------------------------------------|
| Unión           | `a | b` o `a.union(b)`   | Todos los elementos de a y b         |
| Intersección    | `a & b` o `a.intersection(b)` | Solo los que están en ambos     |
| Diferencia      | `a - b` o `a.difference(b)` | Los de a que NO están en b        |
| Dif. simétrica  | `a ^ b`                  | Los que están en uno pero no en ambos|

---

## EJEMPLO

```python
sector_a = {"N1", "N2", "N3"}
sector_b = {"N2", "N3", "N4"}

print(sector_a | sector_b)   # {'N1', 'N2', 'N3', 'N4'}
print(sector_a & sector_b)   # {'N2', 'N3'}
print(sector_a - sector_b)   # {'N1'}
```

---

## CASO DE USO: Deduplicación

```python
ids_duplicados = ["A1", "B2", "A1", "C3", "B2"]
ids_unicos = set(ids_duplicados)   # {'A1', 'B2', 'C3'}
```
"""

THEORY_N55 = """\
## PROTOCOLO: Diccionarios Anidados

Un diccionario puede contener otro diccionario como valor.
Se accede encadenando corchetes:

```python
nexo = {
    "sector_1": {"nombre": "Alpha", "energia": 85},
    "sector_2": {"nombre": "Beta",  "energia": 60},
}

print(nexo["sector_1"]["nombre"])   # "Alpha"
print(nexo["sector_2"]["energia"])  # 60
```

Cada `[]` baja un nivel en la estructura:
1. `nexo["sector_1"]` → `{"nombre": "Alpha", "energia": 85}`
2. `...["nombre"]`    → `"Alpha"`

---

## MODIFICAR VALORES ANIDADOS

```python
nexo["sector_1"]["energia"] = 90   # actualiza el valor
nexo["sector_3"] = {"nombre": "Gamma", "energia": 70}  # agrega nuevo sector
```
"""

THEORY_N56 = """\
## PROTOCOLO: Iterar Estructuras Anidadas

Para recorrer un diccionario de diccionarios usa `.items()` y accede al
sub-diccionario dentro del bucle:

```python
mapa = {
    "Alpha": {"energia": 85, "estado": "activo"},
    "Beta":  {"energia": 60, "estado": "inactivo"},
}

for nombre, datos in mapa.items():
    print(f"{nombre}: {datos['energia']}%")
# Alpha: 85%
# Beta: 60%
```

---

## FILTRADO DURANTE LA ITERACIÓN

```python
for nombre, datos in mapa.items():
    if datos["estado"] == "activo":
        print(f"{nombre} está operativo")
# Alpha está operativo
```

---

## NOTA: Orden de los Dicts

En Python 3.7+, los diccionarios mantienen el **orden de inserción**.
La salida será siempre en el orden en que se definieron las claves.
"""

THEORY_N57 = """\
## PROTOCOLO: Listas de Diccionarios — La Base de Datos del Nexo

Una **lista de diccionarios** es la forma más común de representar registros
tabulares en Python (equivalente a filas de una tabla):

```python
agentes = [
    {"id": "A01", "nombre": "Rex",   "nivel": 5},
    {"id": "A02", "nombre": "Kira",  "nivel": 8},
    {"id": "A03", "nombre": "Ghost", "nivel": 3},
]
```

---

## BÚSQUEDA POR CLAVE

Para encontrar un registro específico, recorre la lista con `for` y filtra con `if`:

```python
for agente in agentes:
    if agente["id"] == "A02":
        print(agente["nombre"])   # "Kira"
        print(agente["nivel"])    # 8
        break   # opcional: detiene la búsqueda al encontrar el primero
```

---

## ACCESO A CAMPOS

Dentro del bucle, `agente` es un dict normal:
- `agente["id"]`     → valor de la clave "id"
- `agente["nombre"]` → valor de la clave "nombre"
"""

THEORY_N58 = """\
## PROTOCOLO: Filtrado de Registros

Para obtener un subconjunto de registros que cumplen una condición,
recorre la lista y usa `if`:

```python
agentes = [
    {"nombre": "Rex",   "nivel": 5},
    {"nombre": "Kira",  "nivel": 8},
    {"nombre": "Ghost", "nivel": 3},
]

for agente in agentes:
    if agente["nivel"] >= 5:
        print(agente["nombre"])
# Rex
# Kira
```

---

## CONSTRUIR UNA LISTA FILTRADA

Para guardar los resultados (no solo imprimirlos):

```python
elite = []
for agente in agentes:
    if agente["nivel"] >= 5:
        elite.append(agente)
# elite contiene los dicts de Rex y Kira
```

---

## MÚLTIPLES CONDICIONES

```python
for agente in agentes:
    if agente["nivel"] >= 5 and agente["estado"] == "activo":
        print(agente["nombre"])
```
"""

THEORY_N59 = """\
## PROTOCOLO: Agregación sobre Registros

Para calcular el **máximo, mínimo o suma** de un campo en una lista de dicts,
usa el patrón de acumulador con un bucle:

```python
sensores = [
    {"id": "S1", "lectura": 45},
    {"id": "S2", "lectura": 78},
    {"id": "S3", "lectura": 91},
]

# Encontrar el sensor con mayor lectura
max_lectura = 0
max_id = ""
for s in sensores:
    if s["lectura"] > max_lectura:
        max_lectura = s["lectura"]
        max_id = s["id"]

print(max_id)       # "S3"
print(max_lectura)  # 91
```

---

## SUMA Y PROMEDIO

```python
total = 0
for s in sensores:
    total += s["lectura"]
promedio = total / len(sensores)
print(promedio)   # 71.33...
```
"""


# ─── Niveles del Sector 06 ────────────────────────────────────────────────────

SECTOR_06 = [
    # ── NIVEL 51 — Tuplas: creación e indexación ──────────────────────────────
    {
        "title": "Coordenadas del Nodo",
        "description": (
            "El sistema de navegación del Nexo almacena las coordenadas de cada "
            "nodo como tuplas inmutables de dos valores: columna y fila.\n\n"
            "Dada la coordenada `pos = (10, 25)`, imprime la columna (primer elemento) "
            "y la fila (segundo elemento), cada uno en su propia línea.\n\n"
            "Salida esperada:\n"
            "```\n10\n25\n```"
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "easy",
        "sector_id": 6,
        "level_order": 51,
        "base_xp_reward": 100,
        "is_project": False,
        "telemetry_goal_time": 90,
        "challenge_type": "python",
        "phase": "boveda",
        "concepts_taught_json": json.dumps(["tuplas", "indexación", "inmutabilidad"]),
        "initial_code": (
            "# MISIÓN: Accede a los elementos de la coordenada\n"
            "\n"
            "pos = (10, 25)\n"
            "\n"
            "# Imprime la columna (índice 0)\n"
            "print(pos[___])\n"
            "\n"
            "# Imprime la fila (índice 1)\n"
            "print(pos[___])\n"
        ),
        "expected_output": "10\n25",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El sistema de mapeo del Nexo registra la posición de cada nodo "
            "como una pareja de coordenadas que no puede ser alterada "
            "una vez que el nodo se ancla al grid. "
            "DAKI usa tuplas para garantizar que estas coordenadas son inmutables: "
            "ningún proceso puede moverlas accidentalmente."
        ),
        "pedagogical_objective": (
            "Introducir tuplas como colecciones inmutables. "
            "Acceso por índice igual que en listas. "
            "Diferenciar de listas: no se pueden modificar."
        ),
        "syntax_hint": "print(pos[0])\nprint(pos[1])",
        "theory_content": THEORY_N51,
        "hints_json": json.dumps([
            "Las tuplas se indexan igual que las listas: pos[0] es el primer elemento.",
            "pos[0] es 10 (columna) y pos[1] es 25 (fila).",
            "Solución: print(pos[0]) y print(pos[1]).",
        ]),
        "strict_match": True,
    },
    # ── NIVEL 52 — Desempaquetado de tuplas ───────────────────────────────────
    {
        "title": "Registro de Nodo",
        "description": (
            "La bóveda de datos del Sector 06 almacena cada nodo como una tupla "
            "de tres campos: nombre, nivel y estado.\n\n"
            "Dada la tupla `registro = (\"NEXO-7\", 42, \"ACTIVO\")`, "
            "**desempaqueta** los tres valores en variables separadas e imprime:\n\n"
            "```\nNodo: NEXO-7 | Nivel: 42 | Estado: ACTIVO\n```"
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "easy",
        "sector_id": 6,
        "level_order": 52,
        "base_xp_reward": 100,
        "is_project": False,
        "telemetry_goal_time": 100,
        "challenge_type": "python",
        "phase": "boveda",
        "concepts_taught_json": json.dumps(["tuplas", "desempaquetado", "f-strings"]),
        "initial_code": (
            "# MISIÓN: Desempaqueta la tupla en tres variables\n"
            "\n"
            'registro = ("NEXO-7", 42, "ACTIVO")\n'
            "\n"
            "# Desempaqueta: nombre, nivel, estado = registro\n"
            "___, ___, ___ = registro\n"
            "\n"
            "print(f\"Nodo: {nombre} | Nivel: {nivel} | Estado: {estado}\")\n"
        ),
        "expected_output": "Nodo: NEXO-7 | Nivel: 42 | Estado: ACTIVO",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "La bóveda del Nexo transmite los registros de nodo en formato compacto: "
            "tres campos en una sola tupla. Para procesar cada campo individualmente, "
            "DAKI usa el desempaquetado — una forma elegante de asignar los tres "
            "valores a tres variables en una sola línea de código."
        ),
        "pedagogical_objective": (
            "Introducir el desempaquetado de tuplas (tuple unpacking). "
            "Ver que el número de variables debe coincidir con los elementos. "
            "Combinar con f-strings para mostrar los valores."
        ),
        "syntax_hint": (
            "nombre, nivel, estado = registro\n"
            'print(f"Nodo: {nombre} | Nivel: {nivel} | Estado: {estado}")'
        ),
        "theory_content": THEORY_N52,
        "hints_json": json.dumps([
            "El desempaquetado asigna cada elemento a una variable: a, b, c = (1, 2, 3) — tres variables para tres elementos.",
            "Las variables deben llamarse nombre, nivel y estado para que el f-string del print funcione.",
            "Solución: nombre, nivel, estado = registro (una sola línea).",
        ]),
        "strict_match": True,
    },
    # ── NIVEL 53 — Sets: creación y .add() ────────────────────────────────────
    {
        "title": "Control de Acceso Único",
        "description": (
            "El sistema de control de acceso del Nexo registra los IDs de los "
            "operadores que entraron al sector. No puede haber duplicados: "
            "si un operador ya está registrado, el sistema lo ignora.\n\n"
            "Parte del set `accesos = {\"Alpha\", \"Beta\"}`. "
            "Agrega `\"Gamma\"` y luego vuelve a agregar `\"Alpha\"` (intento duplicado). "
            "Imprime los accesos registrados en **orden alfabético**, uno por línea.\n\n"
            "Salida esperada:\n"
            "```\nAlpha\nBeta\nGamma\n```"
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "easy",
        "sector_id": 6,
        "level_order": 53,
        "base_xp_reward": 125,
        "is_project": False,
        "telemetry_goal_time": 120,
        "challenge_type": "python",
        "phase": "boveda",
        "concepts_taught_json": json.dumps(["sets", ".add()", "deduplicación", "sorted()"]),
        "initial_code": (
            "# MISIÓN: Registra accesos sin duplicados\n"
            "\n"
            'accesos = {"Alpha", "Beta"}\n'
            "\n"
            "# Agrega Gamma\n"
            'accesos.___(___)\n'
            "\n"
            "# Intenta agregar Alpha de nuevo (el set lo ignora)\n"
            'accesos.___(___)\n'
            "\n"
            "# Imprime en orden alfabético\n"
            "for a in sorted(accesos):\n"
            "    print(a)\n"
        ),
        "expected_output": "Alpha\nBeta\nGamma",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El portal de entrada del Sector 06 registra cada operador que cruza el umbral. "
            "Si el mismo operador intenta registrarse dos veces — por un bug o un ataque "
            "de repetición — el sistema descarta silenciosamente el duplicado. "
            "DAKI diseñó el registro con un set precisamente por esta propiedad: "
            "unicidad garantizada sin código adicional."
        ),
        "pedagogical_objective": (
            "Introducir sets. Usar .add() para agregar elementos. "
            "Observar que los duplicados se ignoran automáticamente. "
            "Usar sorted() para obtener salida determinista (sets son desordenados)."
        ),
        "syntax_hint": (
            'accesos.add("Gamma")\n'
            'accesos.add("Alpha")   # ignorado — ya existe'
        ),
        "theory_content": THEORY_N53,
        "hints_json": json.dumps([
            "Para agregar un elemento a un set usa .add(): accesos.add('Gamma')",
            'Los sets ignoran los duplicados automáticamente. accesos.add("Alpha") no hace nada si ya existe.',
            "sorted() devuelve los elementos en orden alfabético para que la salida sea determinista.",
        ]),
        "strict_match": True,
    },
    # ── NIVEL 54 — Operaciones de conjuntos ───────────────────────────────────
    {
        "title": "Nodos en Conflicto",
        "description": (
            "Dos sectores del Nexo están reclamando la misma zona de memoria. "
            "Para resolver el conflicto, necesitas identificar exactamente "
            "qué nodos están siendo reclamados por **ambos** sectores.\n\n"
            "Dados los sets:\n"
            "```\nsector_a = {\"N1\", \"N2\", \"N3\", \"N5\"}\n"
            "sector_b = {\"N2\", \"N3\", \"N4\", \"N6\"}\n```\n\n"
            "Calcula la **intersección** (nodos en ambos) e imprime los nodos "
            "en **orden alfabético**, uno por línea.\n\n"
            "Salida esperada:\n"
            "```\nN2\nN3\n```"
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "medium",
        "sector_id": 6,
        "level_order": 54,
        "base_xp_reward": 150,
        "is_project": False,
        "telemetry_goal_time": 150,
        "challenge_type": "python",
        "phase": "boveda",
        "concepts_taught_json": json.dumps([
            "sets", "intersección (&)", "operaciones de conjuntos", "sorted()"
        ]),
        "initial_code": (
            "# MISIÓN: Encuentra los nodos reclamados por ambos sectores\n"
            "\n"
            'sector_a = {"N1", "N2", "N3", "N5"}\n'
            'sector_b = {"N2", "N3", "N4", "N6"}\n'
            "\n"
            "# Intersección: nodos que están en sector_a Y en sector_b\n"
            "comunes = sector_a ___ sector_b\n"
            "\n"
            "# Imprime en orden alfabético\n"
            "for nodo in sorted(comunes):\n"
            "    print(nodo)\n"
        ),
        "expected_output": "N2\nN3",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El árbitro de conflictos del Nexo necesita identificar los nodos disputados: "
            "aquellos que dos sectores han marcado como propios simultáneamente. "
            "Estos nodos deben ser intervenidos por DAKI antes de que el conflicto "
            "derive en corrupción de datos. La intersección de conjuntos permite "
            "encontrarlos en una sola operación."
        ),
        "pedagogical_objective": (
            "Usar el operador & para la intersección de sets. "
            "Aplicar sorted() para salida determinista. "
            "Introducir las operaciones matemáticas de conjuntos."
        ),
        "syntax_hint": (
            "comunes = sector_a & sector_b\n"
            "for nodo in sorted(comunes):\n"
            "    print(nodo)"
        ),
        "theory_content": THEORY_N54,
        "hints_json": json.dumps([
            "El operador & calcula la intersección: los elementos que están en AMBOS sets.",
            "sector_a & sector_b devuelve un nuevo set con solo los elementos compartidos.",
            "Envuelve el resultado en sorted() para imprimirlos en orden: for nodo in sorted(comunes):",
        ]),
        "strict_match": True,
    },
    # ── NIVEL 55 — Diccionario anidado: acceso ─────────────────────────────────
    {
        "title": "Base de Datos del Nexo",
        "description": (
            "La base de datos del Sector 06 almacena la información de cada "
            "sub-sector como un diccionario anidado dentro de un diccionario principal.\n\n"
            "Dado el mapa:\n"
            "```python\n"
            'nexo = {\n    "sector_1": {"nombre": "Alpha", "energia": 85},\n'
            '    "sector_2": {"nombre": "Beta",  "energia": 60},\n}\n'
            "```\n\n"
            "Imprime el **nombre** del sector_1 y la **energía** del sector_2.\n\n"
            "Salida esperada:\n"
            "```\nAlpha\n60\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 6,
        "level_order": 55,
        "base_xp_reward": 150,
        "is_project": False,
        "telemetry_goal_time": 120,
        "challenge_type": "python",
        "phase": "boveda",
        "concepts_taught_json": json.dumps([
            "diccionarios", "diccionarios anidados", "acceso multinivel"
        ]),
        "initial_code": (
            "# MISIÓN: Accede a los campos del diccionario anidado\n"
            "\n"
            "nexo = {\n"
            '    "sector_1": {"nombre": "Alpha", "energia": 85},\n'
            '    "sector_2": {"nombre": "Beta",  "energia": 60},\n'
            "}\n"
            "\n"
            '# Imprime el nombre del sector_1\n'
            'print(nexo[___][___])\n'
            "\n"
            '# Imprime la energía del sector_2\n'
            'print(nexo[___][___])\n'
        ),
        "expected_output": "Alpha\n60",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "La base de datos del Nexo usa una estructura de dos niveles: "
            "el primer nivel identifica el sector, el segundo contiene los datos del sector. "
            "DAKI necesita que domines el acceso a este tipo de estructura "
            "para poder consultar cualquier campo de cualquier sector "
            "sin necesidad de aplanar la base de datos."
        ),
        "pedagogical_objective": (
            "Acceder a diccionarios anidados encadenando corchetes []. "
            "Entender que cada [] baja un nivel en la jerarquía. "
            "dict[clave_externa][clave_interna]."
        ),
        "syntax_hint": 'print(nexo["sector_1"]["nombre"])\nprint(nexo["sector_2"]["energia"])',
        "theory_content": THEORY_N55,
        "hints_json": json.dumps([
            "Para acceder a un diccionario anidado encadenas dos []: nexo['sector_1'] te da el dict interno.",
            'Luego adds otro [] para la clave interna: nexo["sector_1"]["nombre"] da "Alpha".',
            'Solución: print(nexo["sector_1"]["nombre"]) y print(nexo["sector_2"]["energia"])',
        ]),
        "strict_match": True,
    },
    # ── NIVEL 56 — Diccionario anidado: iteración ──────────────────────────────
    {
        "title": "Mapa de Sectores",
        "description": (
            "El sistema de monitoreo del Nexo necesita un reporte del estado "
            "energético de todos los sectores activos.\n\n"
            "Dado el mapa:\n"
            "```python\n"
            "mapa = {\n"
            '    "Alpha": {"energia": 85, "estado": "activo"},\n'
            '    "Beta":  {"energia": 60, "estado": "inactivo"},\n'
            '    "Gamma": {"energia": 92, "estado": "activo"},\n'
            "}\n```\n\n"
            "Recorre el mapa e imprime cada sector con su nivel de energía "
            "en el formato `nombre: energia%`.\n\n"
            "Salida esperada:\n"
            "```\nAlpha: 85%\nBeta: 60%\nGamma: 92%\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 6,
        "level_order": 56,
        "base_xp_reward": 175,
        "is_project": False,
        "telemetry_goal_time": 150,
        "challenge_type": "python",
        "phase": "boveda",
        "concepts_taught_json": json.dumps([
            "diccionarios anidados", ".items()", "iteración anidada", "f-strings"
        ]),
        "initial_code": (
            "# MISIÓN: Genera el reporte energético de todos los sectores\n"
            "\n"
            "mapa = {\n"
            '    "Alpha": {"energia": 85, "estado": "activo"},\n'
            '    "Beta":  {"energia": 60, "estado": "inactivo"},\n'
            '    "Gamma": {"energia": 92, "estado": "activo"},\n'
            "}\n"
            "\n"
            "for nombre, datos in mapa.items():\n"
            "    # Imprime: 'nombre: energia%'\n"
            "    print(___)\n"
        ),
        "expected_output": "Alpha: 85%\nBeta: 60%\nGamma: 92%",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El sistema de monitoreo energético del Nexo necesita un reporte completo "
            "que muestre el nivel de carga de cada sector registrado en la bóveda. "
            "El reporte se genera automáticamente en cada ciclo de mantenimiento. "
            "DAKI necesita que el módulo iterador produzca exactamente "
            "el formato que espera el sistema de alertas."
        ),
        "pedagogical_objective": (
            "Iterar un diccionario de diccionarios con .items(). "
            "Acceder a los sub-campos del dict interno (datos) dentro del for. "
            "Formatear la salida con f-strings."
        ),
        "syntax_hint": (
            "for nombre, datos in mapa.items():\n"
            "    print(f\"{nombre}: {datos['energia']}%\")"
        ),
        "theory_content": THEORY_N56,
        "hints_json": json.dumps([
            ".items() desempaqueta cada par en (nombre, datos). 'datos' es el dict interno.",
            "Dentro del for, accede a la energía con: datos['energia']",
            "Usa un f-string: print(f\"{nombre}: {datos['energia']}%\")",
        ]),
        "strict_match": True,
    },
    # ── NIVEL 57 — Lista de dicts: búsqueda ────────────────────────────────────
    {
        "title": "Búsqueda en la Bóveda",
        "description": (
            "La bóveda de agentes del Nexo almacena los registros como una "
            "lista de diccionarios. El sistema de identificación necesita "
            "localizar un agente específico por su ID.\n\n"
            "Dado el registro de agentes, encuentra el agente con "
            "`id == \"A02\"` e imprime su **nombre** y **nivel**.\n\n"
            "Salida esperada:\n"
            "```\nKira\n8\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 6,
        "level_order": 57,
        "base_xp_reward": 200,
        "is_project": False,
        "telemetry_goal_time": 180,
        "challenge_type": "python",
        "phase": "boveda",
        "concepts_taught_json": json.dumps([
            "lista de diccionarios", "búsqueda por clave", "for + if"
        ]),
        "initial_code": (
            "# MISIÓN: Encuentra al agente con id='A02'\n"
            "\n"
            "agentes = [\n"
            '    {"id": "A01", "nombre": "Rex",   "nivel": 5},\n'
            '    {"id": "A02", "nombre": "Kira",  "nivel": 8},\n'
            '    {"id": "A03", "nombre": "Ghost", "nivel": 3},\n'
            "]\n"
            "\n"
            "for agente in agentes:\n"
            '    if agente[___] == ___:\n'
            "        print(agente[___])\n"
            "        print(agente[___])\n"
        ),
        "expected_output": "Kira\n8",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El sistema de identificación del Nexo recibe una solicitud urgente: "
            "localizar al agente con identificador A02 en la bóveda de personal. "
            "El registro contiene cientos de entradas. El módulo de búsqueda de DAKI "
            "recorre la lista y extrae solo los datos del agente solicitado "
            "para el reporte de despliegue táctico."
        ),
        "pedagogical_objective": (
            "Buscar un registro específico en una lista de dicts. "
            "Patrón: for + if para localizar por valor de clave. "
            "Acceder a múltiples campos del registro encontrado."
        ),
        "syntax_hint": (
            "for agente in agentes:\n"
            '    if agente["id"] == "A02":\n'
            '        print(agente["nombre"])\n'
            '        print(agente["nivel"])'
        ),
        "theory_content": THEORY_N57,
        "hints_json": json.dumps([
            'Dentro del for, accede al id con agente["id"]. Compara con "A02".',
            'Cuando la condición es True, imprime agente["nombre"] y agente["nivel"].',
            'Solución: if agente["id"] == "A02": print(agente["nombre"]) + print(agente["nivel"])',
        ]),
        "strict_match": True,
    },
    # ── NIVEL 58 — Lista de dicts: filtrado ────────────────────────────────────
    {
        "title": "Élite del Nexo",
        "description": (
            "El comando del Nexo necesita convocar solo a los agentes de alto nivel "
            "para una misión de infiltración. Solo los agentes con "
            "`nivel >= 5` califican para la Élite.\n\n"
            "Filtra la lista e imprime el **nombre** de cada agente élite, "
            "en el orden en que aparecen en el registro.\n\n"
            "Salida esperada:\n"
            "```\nRex\nKira\nVex\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "hard",
        "sector_id": 6,
        "level_order": 58,
        "base_xp_reward": 250,
        "is_project": False,
        "telemetry_goal_time": 200,
        "challenge_type": "python",
        "phase": "boveda",
        "concepts_taught_json": json.dumps([
            "lista de diccionarios", "filtrado por condición", "for + if"
        ]),
        "initial_code": (
            "# MISIÓN: Imprime solo los agentes con nivel >= 5\n"
            "\n"
            "agentes = [\n"
            '    {"nombre": "Rex",   "nivel": 5},\n'
            '    {"nombre": "Kira",  "nivel": 8},\n'
            '    {"nombre": "Ghost", "nivel": 3},\n'
            '    {"nombre": "Vex",   "nivel": 7},\n'
            "]\n"
            "\n"
            "for agente in agentes:\n"
            "    if agente[___] >= ___:\n"
            "        print(agente[___])\n"
        ),
        "expected_output": "Rex\nKira\nVex",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "La misión de infiltración del Nexo es extremadamente peligrosa. "
            "Solo los agentes con nivel de combate 5 o superior han completado "
            "el entrenamiento necesario para sobrevivir el sector enemigo. "
            "DAKI ejecuta el filtro de selección y notifica a los elegidos. "
            "Ghost se queda en la base — su nivel no es suficiente esta vez."
        ),
        "pedagogical_objective": (
            "Filtrar una lista de dicts con una condición numérica. "
            "Patrón: for + if sobre campo de dict. "
            "Distinguir búsqueda (un solo resultado) de filtrado (múltiples resultados)."
        ),
        "syntax_hint": (
            "for agente in agentes:\n"
            '    if agente["nivel"] >= 5:\n'
            '        print(agente["nombre"])'
        ),
        "theory_content": THEORY_N58,
        "hints_json": json.dumps([
            'Dentro del for, accede al nivel con agente["nivel"] y compara con >= 5.',
            'Si la condición se cumple, imprime agente["nombre"].',
            'Solución: if agente["nivel"] >= 5: print(agente["nombre"])',
        ]),
        "strict_match": True,
    },
    # ── NIVEL 59 — Lista de dicts: agregación (máximo) ─────────────────────────
    {
        "title": "Sensor Crítico",
        "description": (
            "El sistema de detección del Nexo tiene cuatro sensores activos. "
            "Un pico de lectura inusualmente alto indica una amenaza inminente. "
            "El protocolo de alerta necesita identificar qué sensor reportó "
            "la lectura **más alta** y cuál fue su valor.\n\n"
            "Imprime el **ID** del sensor con mayor lectura y luego la **lectura** misma.\n\n"
            "Salida esperada:\n"
            "```\nS4\n91\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "hard",
        "sector_id": 6,
        "level_order": 59,
        "base_xp_reward": 300,
        "is_project": False,
        "telemetry_goal_time": 240,
        "challenge_type": "python",
        "phase": "boveda",
        "concepts_taught_json": json.dumps([
            "lista de diccionarios", "agregación", "máximo con acumulador",
            "for sobre lista de dicts"
        ]),
        "initial_code": (
            "# MISIÓN: Encuentra el sensor con la lectura más alta\n"
            "\n"
            "sensores = [\n"
            '    {"id": "S1", "lectura": 45},\n'
            '    {"id": "S2", "lectura": 78},\n'
            '    {"id": "S3", "lectura": 23},\n'
            '    {"id": "S4", "lectura": 91},\n'
            "]\n"
            "\n"
            "max_lectura = 0\n"
            'max_id = ""\n'
            "\n"
            "for s in sensores:\n"
            "    if s[___] > max_lectura:\n"
            "        max_lectura = s[___]\n"
            "        max_id = s[___]\n"
            "\n"
            "print(max_id)\n"
            "print(max_lectura)\n"
        ),
        "expected_output": "S4\n91",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "La red de sensores del Nexo está en alerta máxima. "
            "Uno de los cuatro puntos de medición registró una lectura anómala "
            "que sugiere una brecha en el perímetro de seguridad. "
            "El sistema de respuesta táctica de DAKI necesita el ID del sensor "
            "comprometido y el valor exacto de la lectura para priorizar la intervención."
        ),
        "pedagogical_objective": (
            "Encontrar el máximo en una lista de dicts usando acumulador. "
            "Mantener tanto el valor máximo como el registro completo que lo contiene. "
            "Patrón clásico de búsqueda de máximo/mínimo sobre registros."
        ),
        "syntax_hint": (
            "for s in sensores:\n"
            '    if s["lectura"] > max_lectura:\n'
            '        max_lectura = s["lectura"]\n'
            '        max_id = s["id"]'
        ),
        "theory_content": THEORY_N59,
        "hints_json": json.dumps([
            'Accede a la lectura de cada sensor con s["lectura"] dentro del for.',
            'Si la lectura actual supera max_lectura, actualiza AMBAS variables: max_lectura y max_id.',
            's["id"] contiene el identificador del sensor. Guárdalo en max_id cuando encuentres un nuevo máximo.',
        ]),
        "strict_match": True,
    },
]


# ─── Lógica de población ──────────────────────────────────────────────────────

async def seed() -> None:
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with SessionLocal() as session:
        # Idempotente: elimina solo niveles 51–59 (preserva el CONTRATO-60)
        deleted = await session.execute(
            delete(Challenge).where(
                Challenge.sector_id == 6,
                Challenge.level_order < 60,
            )
        )
        deleted_count = deleted.rowcount
        await session.flush()
        print(f"🧹  Sector 06 (51-59) anterior eliminado — {deleted_count} challenge(s) removidos.")

        print(f"\n🌱  Insertando {len(SECTOR_06)} niveles del Sector 06...\n")
        for data in SECTOR_06:
            challenge = Challenge(**data)
            session.add(challenge)
            print(
                f"    [{data['level_order']:02d}/59] {data['title']:<38} "
                f"({data['difficulty'].upper()}, {data['base_xp_reward']} XP, "
                f"~{data['telemetry_goal_time']}s)"
            )

        await session.commit()

    await engine.dispose()
    print(f"\n✅  Sector 06 cargado — {len(SECTOR_06)} niveles listos.")
    print("    Boss CONTRATO-60 preservado (gestionar con seed_contratos.py)\n")


if __name__ == "__main__":
    asyncio.run(seed())
