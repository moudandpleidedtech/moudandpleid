"""
seed_sector_09.py — Sector 08: El Paradigma de Objetos (POO)
=============================================================
Niveles 71–80  |  10 misiones  |  Sector ID = 8

Temática técnica: Clases, objetos, __init__, métodos de instancia,
                  atributos, herencia básica, polimorfismo e isinstance.

Lore DAKI: "Creación de Avatares" (71–75) y "Gestión de Flota de Drones" (76–80).

Nivel 80 (Boss): Clase Drone completa con recibir_dano() y atacar().

NOTA de sandbox:
  • super().__init__() está bloqueado por el AST guard (Layer 2b bloquea
    accesos a atributos que empiezan con '_').
  • Los niveles de herencia redeclaran atributos del padre directamente
    en __init__ — patrón válido para OOP introductorio.
  • __build_class__, super y object están en el whitelist desde Prompt 31.

Uso standalone:
    python -m scripts.seed_sector_09
    python -m scripts.seed_sector_09 --dry-run
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.models.challenge import Challenge, DifficultyTier


# ─────────────────────────────────────────────────────────────────────────────
# Textos de teoría reutilizables
# ─────────────────────────────────────────────────────────────────────────────

THEORY_OOP_INTRO = """\
## Clases y Objetos

Una **clase** es un molde que define atributos (datos) y métodos (acciones).
Un **objeto** es una instancia concreta de esa clase.

```python
class Sensor:
    tipo = "temperatura"          # atributo de clase

    def activar(self):            # método de instancia
        print("Sensor activado")

s = Sensor()
s.activar()   # → "Sensor activado"
```

`self` es la referencia al objeto actual dentro de sus propios métodos.
"""

THEORY_INIT = """\
## El Constructor __init__

`__init__` se ejecuta automáticamente al crear una instancia.
Recibe los parámetros de inicialización y los guarda como atributos.

```python
class Drone:
    def __init__(self, nombre, hp):
        self.nombre = nombre
        self.hp     = hp

d = Drone("Alpha", 100)
print(d.nombre)   # → Alpha
print(d.hp)       # → 100
```
"""

THEORY_METHODS = """\
## Métodos de instancia

Los métodos acceden y modifican los atributos del objeto a través de `self`.

```python
class Drone:
    def __init__(self, nombre, hp):
        self.nombre = nombre
        self.hp     = hp

    def estado(self):
        print(f"{self.nombre}: {self.hp} HP")

d = Drone("Beta", 85)
d.estado()   # → Beta: 85 HP
```
"""

THEORY_MUTATION = """\
## Métodos que modifican el estado

Los métodos pueden cambiar los atributos del objeto:

```python
class Drone:
    def __init__(self, hp):
        self.hp = hp

    def recibir_dano(self, dano):
        self.hp = max(0, self.hp - dano)

d = Drone(100)
d.recibir_dano(35)
print(d.hp)   # → 65
```

`max(0, ...)` evita que `hp` sea negativo.
"""

THEORY_STR = """\
## El método __str__

`__str__` define cómo se representa el objeto como texto cuando se usa `print()` o `str()`.

```python
class Drone:
    def __init__(self, nombre, hp):
        self.nombre = nombre
        self.hp     = hp

    def __str__(self):
        return f"Drone[{self.nombre}] HP={self.hp}"

d = Drone("Gamma", 75)
print(d)   # → Drone[Gamma] HP=75
```
"""

THEORY_LIST_INSTANCES = """\
## Listas de objetos

Puedes almacenar múltiples instancias en una lista e iterar sobre ellas:

```python
flota = [Drone("Alpha", 100), Drone("Beta", 85), Drone("Gamma", 60)]

for drone in flota:
    print(f"{drone.nombre}: {drone.hp} HP")
```

Cada elemento de la lista es un objeto independiente con sus propios atributos.
"""

THEORY_INHERITANCE = """\
## Herencia básica

Una clase hija hereda los métodos de la clase padre. Para reutilizar
la inicialización del padre en el sandbox (donde `super().__init__()`
no está disponible), redeclaramos los atributos directamente:

```python
class DroneBase:
    def __init__(self, nombre, hp):
        self.nombre = nombre
        self.hp     = hp

    def descripcion(self):
        print("Drone Base")

class DroneCombate(DroneBase):
    def __init__(self, nombre, hp, ataque):
        self.nombre = nombre   # ← redeclaramos atributos padre
        self.hp     = hp
        self.ataque = ataque

    def atacar(self, objetivo):
        objetivo.hp = max(0, objetivo.hp - self.ataque)
        print(f"{self.nombre} ataca con {self.ataque} de daño")
```
"""

THEORY_POLYMORPHISM = """\
## Polimorfismo: sobreescribir métodos

Una clase hija puede **sobreescribir** un método heredado del padre
para cambiar su comportamiento:

```python
class DroneBase:
    def descripcion(self):
        print("Drone Base")

class DroneEspia(DroneBase):
    def __init__(self, sigilo):
        self.sigilo = sigilo

    def descripcion(self):          # sobreescribe al padre
        print(f"Drone Espía (sigilo: {self.sigilo})")
```

Aunque sean del mismo tipo, cada objeto ejecuta su propia versión del método.
"""

THEORY_ISINSTANCE = """\
## isinstance() con herencia

`isinstance(obj, Clase)` devuelve `True` si el objeto es una instancia
de `Clase` **o de cualquiera de sus clases hijas**:

```python
class DroneBase: pass
class DroneCombate(DroneBase): pass

d = DroneCombate()
print(isinstance(d, DroneCombate))   # → True
print(isinstance(d, DroneBase))      # → True  (hereda de DroneBase)
print(isinstance(d, str))            # → False
```
"""


# ─────────────────────────────────────────────────────────────────────────────
# Catálogo de misiones
# ─────────────────────────────────────────────────────────────────────────────

SECTOR_09: list[dict] = [
    # ── Nivel 71 ─────────────────────────────────────────────────────────────
    {
        "sector_id": 9,
        "level_order": 81,
        "title":       "El Primer Sensor",
        "description": (
            "Crea una clase `Sensor` con un atributo de clase `tipo = \"temperatura\"` "
            "y un método `activar(self)` que imprima exactamente:\n\n"
            "```\nSensor temperatura activado\n```\n\n"
            "Luego instancia el objeto y llama al método."
        ),
        "difficulty_tier":       DifficultyTier.BEGINNER,
        "difficulty":            "easy",
        "base_xp_reward":        120,
        "is_project":            False,
        "telemetry_goal_time":   180,
        "challenge_type":        "code",
        "phase":                 "teoria",
        "concepts_taught_json":  ["class", "atributo_clase", "metodo", "self", "instancia"],
        "initial_code": (
            "class Sensor:\n"
            "    tipo = \"temperatura\"\n"
            "\n"
            "    def activar(self):\n"
            "        # Imprime el mensaje de activación\n"
            "        pass\n"
            "\n"
            "s = Sensor()\n"
            "s.activar()\n"
        ),
        "expected_output":       "Sensor temperatura activado",
        "test_inputs_json":      [],
        "strict_match":          True,
        "lore_briefing": (
            "DAKI — Protocolo Avatares v1.0\n\n"
            "Para crear entidades autónomas necesitamos un molde base.\n"
            "Tu primera misión: diseña la clase `Sensor` y actívala."
        ),
        "pedagogical_objective": "Introducir el concepto de clase, atributo de clase y método de instancia.",
        "syntax_hint":           "Usa `f\"Sensor {self.tipo} activado\"` o concatenación.",
        "theory_content":        THEORY_OOP_INTRO,
        "hints_json": [
            "Una clase define el molde; un objeto es la instancia concreta.",
            "El método `activar` debe usar `self.tipo` para leer el atributo.",
            "Crea el objeto con `s = Sensor()` y llama `s.activar()`.",
        ],
        "grid_map_json": None,
    },

    # ── Nivel 72 ─────────────────────────────────────────────────────────────
    {
        "sector_id": 9,
        "level_order": 82,
        "title":       "Avatar con __init__",
        "description": (
            "Crea una clase `Avatar` con un constructor `__init__(self, nombre, hp)` "
            "que guarde ambos parámetros como atributos.\n\n"
            "Luego crea un avatar llamado `\"Alpha\"` con 100 HP e imprime:\n\n"
            "```\nAlpha\n100\n```"
        ),
        "difficulty_tier":       DifficultyTier.BEGINNER,
        "difficulty":            "easy",
        "base_xp_reward":        130,
        "is_project":            False,
        "telemetry_goal_time":   200,
        "challenge_type":        "code",
        "phase":                 "teoria",
        "concepts_taught_json":  ["__init__", "self", "atributo_instancia", "constructor"],
        "initial_code": (
            "class Avatar:\n"
            "    def __init__(self, nombre, hp):\n"
            "        # Guarda nombre y hp como atributos\n"
            "        pass\n"
            "\n"
            "a = Avatar(\"Alpha\", 100)\n"
            "print(a.nombre)\n"
            "print(a.hp)\n"
        ),
        "expected_output":       "Alpha\n100",
        "test_inputs_json":      [],
        "strict_match":          True,
        "lore_briefing": (
            "DAKI — Módulo de Identidad\n\n"
            "Cada avatar necesita un nombre y puntos de vida.\n"
            "Usa `__init__` para inicializar esos datos al nacer."
        ),
        "pedagogical_objective": "Aprender a definir y usar __init__ para inicializar atributos de instancia.",
        "syntax_hint":           "Dentro de `__init__`: `self.nombre = nombre` y `self.hp = hp`.",
        "theory_content":        THEORY_INIT,
        "hints_json": [
            "`__init__` se ejecuta automáticamente al crear un objeto.",
            "Asigna cada parámetro a un atributo: `self.nombre = nombre`.",
            "Accede al atributo desde fuera con `a.nombre`.",
        ],
        "grid_map_json": None,
    },

    # ── Nivel 73 ─────────────────────────────────────────────────────────────
    {
        "sector_id": 9,
        "level_order": 83,
        "title":       "Estado del Avatar",
        "description": (
            "Añade a la clase `Avatar` un método `estado(self)` que imprima:\n\n"
            "```\nNexo-7: 85 HP\n```\n\n"
            "Crea `Avatar(\"Nexo-7\", 85)` y llama al método."
        ),
        "difficulty_tier":       DifficultyTier.BEGINNER,
        "difficulty":            "easy",
        "base_xp_reward":        140,
        "is_project":            False,
        "telemetry_goal_time":   210,
        "challenge_type":        "code",
        "phase":                 "practica",
        "concepts_taught_json":  ["metodo_instancia", "f-string", "self"],
        "initial_code": (
            "class Avatar:\n"
            "    def __init__(self, nombre, hp):\n"
            "        self.nombre = nombre\n"
            "        self.hp     = hp\n"
            "\n"
            "    def estado(self):\n"
            "        # Imprime \"nombre: hp HP\"\n"
            "        pass\n"
            "\n"
            "a = Avatar(\"Nexo-7\", 85)\n"
            "a.estado()\n"
        ),
        "expected_output":       "Nexo-7: 85 HP",
        "test_inputs_json":      [],
        "strict_match":          True,
        "lore_briefing": (
            "DAKI — Monitor de Salud\n\n"
            "El sistema necesita conocer el estado vital de cada avatar.\n"
            "Implementa el método `estado()` para reportarlo."
        ),
        "pedagogical_objective": "Practicar métodos de instancia que leen y formatean atributos propios.",
        "syntax_hint":           "Usa `f\"{self.nombre}: {self.hp} HP\"`.",
        "theory_content":        THEORY_METHODS,
        "hints_json": [
            "Los métodos acceden a los atributos del objeto con `self.atributo`.",
            "Usa un f-string: `f\"{self.nombre}: {self.hp} HP\"`.",
            "Recuerda que `estado(self)` lleva `self` como primer parámetro.",
        ],
        "grid_map_json": None,
    },

    # ── Nivel 74 ─────────────────────────────────────────────────────────────
    {
        "sector_id": 9,
        "level_order": 84,
        "title":       "Recibir Daño",
        "description": (
            "Añade el método `recibir_dano(self, dano)` a la clase `Avatar`.\n"
            "El HP nunca debe bajar de 0.\n\n"
            "Con `Avatar(\"Nexo-7\", 100)` y `recibir_dano(35)`, imprime:\n\n"
            "```\n65\n```"
        ),
        "difficulty_tier":       DifficultyTier.BEGINNER,
        "difficulty":            "easy",
        "base_xp_reward":        150,
        "is_project":            False,
        "telemetry_goal_time":   220,
        "challenge_type":        "code",
        "phase":                 "practica",
        "concepts_taught_json":  ["metodo_mutador", "max", "self"],
        "initial_code": (
            "class Avatar:\n"
            "    def __init__(self, nombre, hp):\n"
            "        self.nombre = nombre\n"
            "        self.hp     = hp\n"
            "\n"
            "    def recibir_dano(self, dano):\n"
            "        # Reduce hp pero nunca por debajo de 0\n"
            "        pass\n"
            "\n"
            "a = Avatar(\"Nexo-7\", 100)\n"
            "a.recibir_dano(35)\n"
            "print(a.hp)\n"
        ),
        "expected_output":       "65",
        "test_inputs_json":      [],
        "strict_match":          True,
        "lore_briefing": (
            "DAKI — Sistema de Combate v1\n\n"
            "Los avatares deben poder recibir daño sin morir de forma inválida.\n"
            "Implementa `recibir_dano` con protección de HP mínimo."
        ),
        "pedagogical_objective": "Aprender a modificar atributos de instancia dentro de métodos usando max().",
        "syntax_hint":           "`self.hp = max(0, self.hp - dano)`",
        "theory_content":        THEORY_MUTATION,
        "hints_json": [
            "Modifica `self.hp` directamente dentro del método.",
            "Usa `max(0, self.hp - dano)` para evitar valores negativos.",
            "El nuevo HP se asigna a `self.hp`, no a una variable local.",
        ],
        "grid_map_json": None,
    },

    # ── Nivel 75 ─────────────────────────────────────────────────────────────
    {
        "sector_id": 9,
        "level_order": 85,
        "title":       "Representación __str__",
        "description": (
            "Añade el método `__str__(self)` a la clase `Drone` para que `print(d)` muestre:\n\n"
            "```\nDrone[Gamma] HP=75\n```\n\n"
            "Crea `Drone(\"Gamma\", 75)` e imprímelo directamente."
        ),
        "difficulty_tier":       DifficultyTier.BEGINNER,
        "difficulty":            "easy",
        "base_xp_reward":        160,
        "is_project":            False,
        "telemetry_goal_time":   230,
        "challenge_type":        "code",
        "phase":                 "practica",
        "concepts_taught_json":  ["__str__", "representacion_objeto", "f-string"],
        "initial_code": (
            "class Drone:\n"
            "    def __init__(self, nombre, hp):\n"
            "        self.nombre = nombre\n"
            "        self.hp     = hp\n"
            "\n"
            "    def __str__(self):\n"
            "        # Devuelve el string de representación\n"
            "        pass\n"
            "\n"
            "d = Drone(\"Gamma\", 75)\n"
            "print(d)\n"
        ),
        "expected_output":       "Drone[Gamma] HP=75",
        "test_inputs_json":      [],
        "strict_match":          True,
        "lore_briefing": (
            "DAKI — Interfaz de Identificación\n\n"
            "El sistema necesita visualizar cada drone en el panel de control.\n"
            "Define `__str__` para que `print(drone)` muestre su identidad."
        ),
        "pedagogical_objective": "Aprender a implementar __str__ para representación textual de objetos.",
        "syntax_hint":           "`return f\"Drone[{self.nombre}] HP={self.hp}\"`",
        "theory_content":        THEORY_STR,
        "hints_json": [
            "`__str__` debe RETORNAR un string, no imprimirlo.",
            "Usa un f-string: `f\"Drone[{self.nombre}] HP={self.hp}\"`.",
            "`print(d)` llama automáticamente a `d.__str__()`.",
        ],
        "grid_map_json": None,
    },

    # ── Nivel 76 ─────────────────────────────────────────────────────────────
    {
        "sector_id": 9,
        "level_order": 86,
        "title":       "Flota de Drones",
        "description": (
            "Crea una lista con tres drones y llama `estado()` en cada uno.\n\n"
            "Salida esperada:\n"
            "```\nAlpha: 100 HP\nBeta: 85 HP\nGamma: 60 HP\n```"
        ),
        "difficulty_tier":       DifficultyTier.BEGINNER,
        "difficulty":            "medium",
        "base_xp_reward":        170,
        "is_project":            False,
        "telemetry_goal_time":   250,
        "challenge_type":        "code",
        "phase":                 "practica",
        "concepts_taught_json":  ["lista_objetos", "iteracion", "metodo_instancia"],
        "initial_code": (
            "class Drone:\n"
            "    def __init__(self, nombre, hp):\n"
            "        self.nombre = nombre\n"
            "        self.hp     = hp\n"
            "\n"
            "    def estado(self):\n"
            "        print(f\"{self.nombre}: {self.hp} HP\")\n"
            "\n"
            "flota = [\n"
            "    Drone(\"Alpha\", 100),\n"
            "    Drone(\"Beta\",  85),\n"
            "    Drone(\"Gamma\", 60),\n"
            "]\n"
            "\n"
            "# Itera sobre la flota y llama estado() en cada drone\n"
            "for drone in flota:\n"
            "    pass\n"
        ),
        "expected_output":       "Alpha: 100 HP\nBeta: 85 HP\nGamma: 60 HP",
        "test_inputs_json":      [],
        "strict_match":          True,
        "lore_briefing": (
            "DAKI — Centro de Mando\n\n"
            "La flota completa debe reportar su estado al sistema central.\n"
            "Itera sobre la lista y activa el reporte de cada drone."
        ),
        "pedagogical_objective": "Practicar listas de objetos e iteración para llamar métodos sobre múltiples instancias.",
        "syntax_hint":           "Dentro del `for`, llama `drone.estado()`.",
        "theory_content":        THEORY_LIST_INSTANCES,
        "hints_json": [
            "Cada elemento de `flota` es un objeto `Drone` independiente.",
            "Dentro del `for drone in flota:`, escribe `drone.estado()`.",
            "La variable `drone` cambia en cada iteración al siguiente objeto.",
        ],
        "grid_map_json": None,
    },

    # ── Nivel 77 ─────────────────────────────────────────────────────────────
    {
        "sector_id": 9,
        "level_order": 87,
        "title":       "Herencia: Drone de Combate",
        "description": (
            "Crea `DroneBase` con `__init__(nombre, hp)` y `DroneCombate(DroneBase)` "
            "que añada el atributo `ataque` y el método `atacar(objetivo)`.\n\n"
            "`atacar` reduce el HP del objetivo y muestra:\n"
            "```\nRex ataca con 30 de daño\nTarget: 50 HP\n```\n\n"
            "Úsalo con `rex.atacar(target)` donde `rex = DroneCombate(\"Rex\", 100, 30)` "
            "y `target = DroneBase(\"Target\", 80, 0)` — pero `DroneBase.__init__` "
            "acepta un tercer parámetro ignorado para simplificar."
        ),
        "difficulty_tier":       DifficultyTier.INTERMEDIATE,
        "difficulty":            "medium",
        "base_xp_reward":        200,
        "is_project":            False,
        "telemetry_goal_time":   300,
        "challenge_type":        "code",
        "phase":                 "practica",
        "concepts_taught_json":  ["herencia", "clase_hija", "override_init", "metodo_atacar"],
        "initial_code": (
            "class DroneBase:\n"
            "    def __init__(self, nombre, hp, extra=None):\n"
            "        self.nombre = nombre\n"
            "        self.hp     = hp\n"
            "\n"
            "class DroneCombate(DroneBase):\n"
            "    def __init__(self, nombre, hp, ataque):\n"
            "        # Redeclara atributos del padre y añade self.ataque\n"
            "        self.nombre = nombre\n"
            "        self.hp     = hp\n"
            "        self.ataque = ataque\n"
            "\n"
            "    def atacar(self, objetivo):\n"
            "        # Reduce objetivo.hp y muestra el mensaje\n"
            "        pass\n"
            "\n"
            "rex    = DroneCombate(\"Rex\", 100, 30)\n"
            "target = DroneBase(\"Target\", 80)\n"
            "rex.atacar(target)\n"
            "print(f\"Target: {target.hp} HP\")\n"
        ),
        "expected_output":       "Rex ataca con 30 de daño\nTarget: 50 HP",
        "test_inputs_json":      [],
        "strict_match":          True,
        "lore_briefing": (
            "DAKI — Protocolo de Combate\n\n"
            "Los drones de combate heredan características base y añaden capacidad de ataque.\n"
            "Implementa la herencia y el método `atacar`."
        ),
        "pedagogical_objective": "Introducir herencia de clases y métodos que interactúan con otros objetos.",
        "syntax_hint":           "En `atacar`: `objetivo.hp = max(0, objetivo.hp - self.ataque)` y luego `print(...)`.",
        "theory_content":        THEORY_INHERITANCE,
        "hints_json": [
            "La clase hija hereda todos los métodos del padre.",
            "En el sandbox, redeclara `self.nombre` y `self.hp` en el `__init__` hijo.",
            "El método `atacar` recibe otro objeto como parámetro y modifica su `hp`.",
            "Usa `max(0, objetivo.hp - self.ataque)` para evitar HP negativo.",
        ],
        "grid_map_json": None,
    },

    # ── Nivel 78 ─────────────────────────────────────────────────────────────
    {
        "sector_id": 9,
        "level_order": 88,
        "title":       "Polimorfismo: Override de Método",
        "description": (
            "Crea `DroneBase` con `descripcion(self)` que imprime `\"Drone Base\"`.\n"
            "Crea `DroneEspia(DroneBase)` con `__init__(self, sigilo)` y sobreescribe "
            "`descripcion` para que imprima `\"Drone Espía (sigilo: 95)\"`.\n\n"
            "Salida esperada:\n"
            "```\nDrone Base\nDrone Espía (sigilo: 95)\n```"
        ),
        "difficulty_tier":       DifficultyTier.INTERMEDIATE,
        "difficulty":            "medium",
        "base_xp_reward":        210,
        "is_project":            False,
        "telemetry_goal_time":   280,
        "challenge_type":        "code",
        "phase":                 "practica",
        "concepts_taught_json":  ["polimorfismo", "override_metodo", "herencia"],
        "initial_code": (
            "class DroneBase:\n"
            "    def descripcion(self):\n"
            "        print(\"Drone Base\")\n"
            "\n"
            "class DroneEspia(DroneBase):\n"
            "    def __init__(self, sigilo):\n"
            "        self.sigilo = sigilo\n"
            "\n"
            "    def descripcion(self):\n"
            "        # Sobreescribe el método padre\n"
            "        pass\n"
            "\n"
            "base  = DroneBase()\n"
            "espia = DroneEspia(95)\n"
            "base.descripcion()\n"
            "espia.descripcion()\n"
        ),
        "expected_output":       "Drone Base\nDrone Espía (sigilo: 95)",
        "test_inputs_json":      [],
        "strict_match":          True,
        "lore_briefing": (
            "DAKI — Diversificación de Flota\n\n"
            "Distintos tipos de drones se comportan diferente ante el mismo comando.\n"
            "Implementa polimorfismo sobreescribiendo el método `descripcion`."
        ),
        "pedagogical_objective": "Demostrar polimorfismo: mismo nombre de método, comportamiento diferente según la clase.",
        "syntax_hint":           '`print(f"Drone Espía (sigilo: {self.sigilo})")`',
        "theory_content":        THEORY_POLYMORPHISM,
        "hints_json": [
            "Sobreescribir un método significa definirlo de nuevo en la clase hija.",
            "Python llama a la versión del método que corresponde a la clase real del objeto.",
            "Usa `self.sigilo` dentro de `DroneEspia.descripcion` para acceder al atributo.",
        ],
        "grid_map_json": None,
    },

    # ── Nivel 79 ─────────────────────────────────────────────────────────────
    {
        "sector_id": 9,
        "level_order": 89,
        "title":       "isinstance() en la Jerarquía",
        "description": (
            "Verifica la jerarquía de clases con `isinstance()`.\n\n"
            "Con `DroneBase` y `DroneCombate(DroneBase)`, crea un objeto `dc = DroneCombate()`.\n\n"
            "Imprime:\n"
            "```\nTrue\nTrue\nFalse\n```\n\n"
            "Donde:\n"
            "- Línea 1: `isinstance(dc, DroneCombate)`\n"
            "- Línea 2: `isinstance(dc, DroneBase)` (hereda)\n"
            "- Línea 3: `isinstance(dc, str)`"
        ),
        "difficulty_tier":       DifficultyTier.INTERMEDIATE,
        "difficulty":            "medium",
        "base_xp_reward":        190,
        "is_project":            False,
        "telemetry_goal_time":   260,
        "challenge_type":        "code",
        "phase":                 "practica",
        "concepts_taught_json":  ["isinstance", "jerarquia_clases", "herencia"],
        "initial_code": (
            "class DroneBase:\n"
            "    pass\n"
            "\n"
            "class DroneCombate(DroneBase):\n"
            "    pass\n"
            "\n"
            "dc = DroneCombate()\n"
            "\n"
            "# Imprime los tres isinstance\n"
            "print(isinstance(dc, DroneCombate))\n"
            "print(isinstance(dc, DroneBase))\n"
            "print(isinstance(dc, str))\n"
        ),
        "expected_output":       "True\nTrue\nFalse",
        "test_inputs_json":      [],
        "strict_match":          True,
        "lore_briefing": (
            "DAKI — Sistema de Identificación Táctica\n\n"
            "El sistema necesita verificar el tipo de cada entidad antes de asignarle órdenes.\n"
            "Usa `isinstance()` para clasificar correctamente en la jerarquía."
        ),
        "pedagogical_objective": "Entender que isinstance() respeta la jerarquía de herencia.",
        "syntax_hint":           "`isinstance(objeto, Clase)` devuelve `True` si el objeto es de esa clase o hija.",
        "theory_content":        THEORY_ISINSTANCE,
        "hints_json": [
            "`isinstance(dc, DroneBase)` es `True` porque `DroneCombate` hereda de `DroneBase`.",
            "`isinstance(dc, str)` es `False` porque `dc` no es un string.",
            "No necesitas modificar el código — solo completar las llamadas `isinstance`.",
        ],
        "grid_map_json": None,
    },

    # ── Nivel 80 (BOSS) ───────────────────────────────────────────────────────
    {
        "sector_id": 9,
        "level_order": 90,
        "title":       "CONTRATO-80: Batalla de Drones",
        "description": (
            "**BOSS del Sector 08 — Proyecto completo**\n\n"
            "Implementa la clase `Drone` con:\n"
            "- `__init__(self, nombre, hp, ataque)`\n"
            "- `recibir_dano(self, dano)` — HP mínimo 0\n"
            "- `atacar(self, objetivo)` — reduce HP del objetivo, imprime:\n"
            "  `\"[nombre] ataca a [objetivo.nombre] — daño: [ataque]\"`\n"
            "- `estado(self)` — imprime `\"[nombre]: [hp] HP [ACTIVO|DESTRUIDO]\"`\n"
            "  (DESTRUIDO si hp == 0)\n\n"
            "Luego ejecuta:\n"
            "```python\n"
            "alpha = Drone(\"Alpha\", 100, 25)\n"
            "beta  = Drone(\"Beta\",  80,  15)\n"
            "alpha.atacar(beta)\n"
            "alpha.atacar(beta)\n"
            "alpha.atacar(beta)\n"
            "alpha.atacar(beta)\n"
            "alpha.estado()\n"
            "beta.estado()\n"
            "```\n\n"
            "Salida esperada:\n"
            "```\nAlpha ataca a Beta — daño: 25\nAlpha ataca a Beta — daño: 25\n"
            "Alpha ataca a Beta — daño: 25\nAlpha ataca a Beta — daño: 25\n"
            "Alpha: 100 HP [ACTIVO]\nBeta: 0 HP [DESTRUIDO]\n```"
        ),
        "difficulty_tier":       DifficultyTier.ADVANCED,
        "difficulty":            "hard",
        "base_xp_reward":        500,
        "is_project":            True,
        "telemetry_goal_time":   600,
        "challenge_type":        "project",
        "phase":                 "proyecto",
        "concepts_taught_json":  ["clase_completa", "metodos_multiples", "estado_objeto", "OOP_integrado"],
        "initial_code": (
            "class Drone:\n"
            "    def __init__(self, nombre, hp, ataque):\n"
            "        self.nombre = nombre\n"
            "        self.hp     = hp\n"
            "        self.ataque = ataque\n"
            "\n"
            "    def recibir_dano(self, dano):\n"
            "        pass\n"
            "\n"
            "    def atacar(self, objetivo):\n"
            "        pass\n"
            "\n"
            "    def estado(self):\n"
            "        pass\n"
            "\n"
            "alpha = Drone(\"Alpha\", 100, 25)\n"
            "beta  = Drone(\"Beta\",   80,  15)\n"
            "alpha.atacar(beta)\n"
            "alpha.atacar(beta)\n"
            "alpha.atacar(beta)\n"
            "alpha.atacar(beta)\n"
            "alpha.estado()\n"
            "beta.estado()\n"
        ),
        "expected_output": (
            "Alpha ataca a Beta — daño: 25\n"
            "Alpha ataca a Beta — daño: 25\n"
            "Alpha ataca a Beta — daño: 25\n"
            "Alpha ataca a Beta — daño: 25\n"
            "Alpha: 100 HP [ACTIVO]\n"
            "Beta: 0 HP [DESTRUIDO]"
        ),
        "test_inputs_json": [],
        "strict_match":     True,
        "lore_briefing": (
            "DAKI — CONTRATO-80: Eliminación de Unidades Hostiles\n\n"
            "La simulación de combate requiere una clase `Drone` completamente funcional.\n"
            "Alpha debe destruir a Beta en 4 ataques. Implementa todos los métodos\n"
            "y demuestra que dominas el Paradigma de Objetos."
        ),
        "pedagogical_objective": "Integrar __init__, métodos mutadores, interacción entre objetos y formato condicional de estado.",
        "syntax_hint":           'En `estado`: `etiqueta = "ACTIVO" if self.hp > 0 else "DESTRUIDO"`.',
        "theory_content": (
            "## Boss Sector 08: Clase Drone completa\n\n"
            "Integra todos los conceptos del sector:\n\n"
            "| Método | Responsabilidad |\n"
            "|---|---|\n"
            "| `__init__` | Inicializa nombre, hp, ataque |\n"
            "| `recibir_dano` | Reduce hp con `max(0, ...)` |\n"
            "| `atacar` | Llama `recibir_dano` del objetivo e imprime log |\n"
            "| `estado` | Muestra HP y etiqueta ACTIVO/DESTRUIDO |\n\n"
            "**Flujo de `atacar`:**\n"
            "```python\n"
            "def atacar(self, objetivo):\n"
            "    objetivo.recibir_dano(self.ataque)\n"
            "    print(f\"{self.nombre} ataca a {objetivo.nombre} — daño: {self.ataque}\")\n"
            "```"
        ),
        "hints_json": [
            "Implementa `recibir_dano` primero: `self.hp = max(0, self.hp - dano)`.",
            "En `atacar`, llama `objetivo.recibir_dano(self.ataque)` y luego imprime el log.",
            "En `estado`, calcula la etiqueta: `\"ACTIVO\" if self.hp > 0 else \"DESTRUIDO\"`.",
            "Formato exacto: `f\"{self.nombre}: {self.hp} HP [{etiqueta}]\"`.",
        ],
        "grid_map_json": None,
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# Seed standalone
# ─────────────────────────────────────────────────────────────────────────────

async def seed(dry_run: bool = False) -> None:
    print("\n" + "═" * 60)
    print("  ⚡ Seed Sector 08 — El Paradigma de Objetos (POO)")
    print("═" * 60)
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
                    delete(Challenge).where(Challenge.sector_id == 9)
                )
            for data in SECTOR_09:
                level_order = data.get("level_order")
                title = data.get("title", "?")
                if dry_run:
                    print(f"  [DRY] ➕  L{level_order:02d}  {title}")
                else:
                    session.add(Challenge(**data))
                    print(f"  ➕  L{level_order:02d}  {title}")
            if not dry_run:
                await session.commit()
                print(f"\n  💾  Commit OK — {len(SECTOR_09)} misiones insertadas.")
        except Exception as exc:
            if not dry_run:
                await session.rollback()
            print(f"  ❌  ERROR: {exc}")
            await engine.dispose()
            sys.exit(1)

    await engine.dispose()
    print("═" * 60 + "\n")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Seed Sector 08 — POO")
    p.add_argument("--dry-run", action="store_true")
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(seed(dry_run=args.dry_run))
