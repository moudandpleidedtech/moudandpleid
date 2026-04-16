"""
seed_sector_17.py — Sector 17: OOP Avanzado (niveles 147–154)
=============================================================
Niveles 147–154  |  8 misiones  |  Sector ID = 16

Temática técnica: OOP avanzado más allá de lo visto en Sector 8.
__str__, __repr__, __eq__, @classmethod, @staticmethod,
herencia avanzada, super(), polimorfismo real.

Nivel 154 (Boss): jerarquía de clases completa.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.models.challenge import Challenge, DifficultyTier  # noqa: F401

SECTOR_17 = [
    # ── L147 — __str__ y __repr__ ─────────────────────────────────────────────
    {
        "title": "Identidad del Objeto",
        "description": (
            "Implementá la clase `Mision` con:\n"
            "- `__init__(self, codigo, tipo, xp)`\n"
            "- `__str__`: `'[CODIGO] TIPO — XP xp'`\n"
            "- `__repr__`: `'Mision(codigo=CODIGO, tipo=TIPO, xp=XP)'`\n\n"
            "Salida esperada:\n"
            "```\n[ALFA-01] RECON — 300 xp\nMision(codigo=ALFA-01, tipo=RECON, xp=300)\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 17,
        "level_order": 157,
        "base_xp_reward": 275,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 200,
        "challenge_type": "python",
        "phase": "oop_avanzado",
        "concepts_taught_json": json.dumps(["class", "__str__", "__repr__", "dunder"]),
        "initial_code": (
            "class Mision:\n"
            "    def __init__(self, codigo, tipo, xp):\n"
            "        self.codigo = codigo\n"
            "        self.tipo = tipo\n"
            "        self.xp = xp\n"
            "\n"
            "    def __str__(self):\n"
            "        return f'[{self.codigo}] {self.tipo} — {self.xp} xp'\n"
            "\n"
            "    def __repr__(self):\n"
            "        return f'Mision(codigo={self.codigo}, tipo={self.tipo}, xp={self.xp})'\n"
            "\n"
            "m = Mision('ALFA-01', 'RECON', 300)\n"
            "print(str(m))\n"
            "print(repr(m))\n"
        ),
        "expected_output": "[ALFA-01] RECON — 300 xp\nMision(codigo=ALFA-01, tipo=RECON, xp=300)",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "DAKI necesita dos formas de representar una misión: una legible para el operador "
            "(__str__) y una técnica para depuración y logs del sistema (__repr__)."
        ),
        "pedagogical_objective": "Distinguir __str__ (para humanos) de __repr__ (para debugging/reproducibilidad).",
        "syntax_hint": "__str__ = legible; __repr__ = técnico con todos los parámetros",
        "theory_content": None,
        "hints_json": json.dumps([
            "__str__ se llama con str(obj) o print(obj).",
            "__repr__ se llama con repr(obj) o en la consola interactiva.",
            "La convención de __repr__: el resultado debería poder usarse para recrear el objeto.",
        ]),
        "strict_match": True,
    },
    # ── L148 — __eq__ ────────────────────────────────────────────────────────
    {
        "title": "Igualdad de Objetos",
        "description": (
            "Implementá la clase `Coordenada` con:\n"
            "- `__init__(self, x, y)`\n"
            "- `__eq__(self, otro)`: True si x e y son iguales\n"
            "- `__str__`: `'(X, Y)'`\n\n"
            "Salida esperada:\n"
            "```\n(3, 4)\nTrue\nFalse\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 17,
        "level_order": 158,
        "base_xp_reward": 275,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 180,
        "challenge_type": "python",
        "phase": "oop_avanzado",
        "concepts_taught_json": json.dumps(["class", "__eq__", "dunder", "__str__"]),
        "initial_code": (
            "class Coordenada:\n"
            "    def __init__(self, x, y):\n"
            "        self.x = x\n"
            "        self.y = y\n"
            "\n"
            "    def __eq__(self, otro):\n"
            "        return self.x == otro.x and self.y == otro.y\n"
            "\n"
            "    def __str__(self):\n"
            "        return f'({self.x}, {self.y})'\n"
            "\n"
            "c1 = Coordenada(3, 4)\n"
            "c2 = Coordenada(3, 4)\n"
            "c3 = Coordenada(1, 2)\n"
            "print(c1)\n"
            "print(c1 == c2)\n"
            "print(c1 == c3)\n"
        ),
        "expected_output": "(3, 4)\nTrue\nFalse",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El sistema de navegación del Nexo compara coordenadas para detectar superposición de sensores. "
            "Sin __eq__, Python compara identidad (si son el mismo objeto), no igualdad de valores."
        ),
        "pedagogical_objective": "Implementar __eq__ para comparación de valores entre objetos del mismo tipo.",
        "syntax_hint": "def __eq__(self, otro): return self.x == otro.x and self.y == otro.y",
        "theory_content": None,
        "hints_json": json.dumps([
            "Sin __eq__, c1 == c2 sería False aunque tengan los mismos valores (compara identidad).",
            "__eq__ recibe otro como el objeto a comparar — verificá self.x == otro.x y self.y == otro.y.",
        ]),
        "strict_match": True,
    },
    # ── L149 — @classmethod ───────────────────────────────────────────────────
    {
        "title": "Constructor Alternativo",
        "description": (
            "Implementá la clase `Operador` con:\n"
            "- `__init__(self, callsign, nivel)`\n"
            "- `@classmethod desde_string(cls, texto)`: parsea `'CALLSIGN:NIVEL'`\n"
            "- `__str__`: `'Operador(CALLSIGN, nivel=N)'`\n\n"
            "Salida esperada:\n"
            "```\nOperador(NEXO, nivel=7)\nOperador(ALFA, nivel=3)\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 17,
        "level_order": 159,
        "base_xp_reward": 280,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 200,
        "challenge_type": "python",
        "phase": "oop_avanzado",
        "concepts_taught_json": json.dumps(["classmethod", "cls", "alternative_constructor"]),
        "initial_code": (
            "class Operador:\n"
            "    def __init__(self, callsign, nivel):\n"
            "        self.callsign = callsign\n"
            "        self.nivel = nivel\n"
            "\n"
            "    @classmethod\n"
            "    def desde_string(cls, texto):\n"
            "        partes = texto.split(':')\n"
            "        return cls(partes[0], int(partes[1]))\n"
            "\n"
            "    def __str__(self):\n"
            "        return f'Operador({self.callsign}, nivel={self.nivel})'\n"
            "\n"
            "op1 = Operador('NEXO', 7)\n"
            "op2 = Operador.desde_string('ALFA:3')\n"
            "print(op1)\n"
            "print(op2)\n"
        ),
        "expected_output": "Operador(NEXO, nivel=7)\nOperador(ALFA, nivel=3)",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "Los datos de operadores llegan en diferentes formatos. "
            "@classmethod permite crear constructores alternativos que parsean "
            "distintos formatos de entrada sin duplicar la lógica de __init__."
        ),
        "pedagogical_objective": "Usar @classmethod con cls para crear constructores alternativos que parsean datos.",
        "syntax_hint": "@classmethod def desde_string(cls, texto): return cls(partes[0], int(partes[1]))",
        "theory_content": None,
        "hints_json": json.dumps([
            "@classmethod recibe cls (la clase misma) en lugar de self.",
            "cls(args) crea una instancia de la clase — es el equivalente de llamar Operador(args).",
            "Esto permite crear la clase desde diferentes formatos de entrada.",
        ]),
        "strict_match": True,
    },
    # ── L150 — Herencia básica ────────────────────────────────────────────────
    {
        "title": "Jerarquía de Unidades",
        "description": (
            "Implementá:\n"
            "- `Unidad(nombre, hp)`: clase base con método `estado()` → `'NOMBRE: HP hp'`\n"
            "- `Soldado(nombre, hp, arma)`: hereda de Unidad; override de `estado()` "
            "  → `'NOMBRE(ARMA): HP hp'`\n\n"
            "Salida esperada:\n"
            "```\nBase: 100 hp\nRECON(Rifle): 80 hp\nTrue\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 17,
        "level_order": 160,
        "base_xp_reward": 285,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 220,
        "challenge_type": "python",
        "phase": "oop_avanzado",
        "concepts_taught_json": json.dumps(["inheritance", "override", "isinstance", "polymorphism"]),
        "initial_code": (
            "class Unidad:\n"
            "    def __init__(self, nombre, hp):\n"
            "        self.nombre = nombre\n"
            "        self.hp = hp\n"
            "\n"
            "    def estado(self):\n"
            "        return f'{self.nombre}: {self.hp} hp'\n"
            "\n"
            "class Soldado(Unidad):\n"
            "    def __init__(self, nombre, hp, arma):\n"
            "        self.nombre = nombre\n"
            "        self.hp = hp\n"
            "        self.arma = arma\n"
            "\n"
            "    def estado(self):\n"
            "        return f'{self.nombre}({self.arma}): {self.hp} hp'\n"
            "\n"
            "base = Unidad('Base', 100)\n"
            "recon = Soldado('RECON', 80, 'Rifle')\n"
            "print(base.estado())\n"
            "print(recon.estado())\n"
            "print(isinstance(recon, Unidad))\n"
        ),
        "expected_output": "Base: 100 hp\nRECON(Rifle): 80 hp\nTrue",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "Las unidades del Nexo comparten atributos básicos pero se especializan. "
            "La herencia permite reusar la base y extender sin repetir código."
        ),
        "pedagogical_objective": "Implementar herencia con override de método y verificar con isinstance().",
        "syntax_hint": "class Soldado(Unidad): def estado(self): return ... (override)",
        "theory_content": None,
        "hints_json": json.dumps([
            "class Soldado(Unidad) hace que Soldado herede todos los atributos y métodos de Unidad.",
            "Redefinir estado() en Soldado sobreescribe (override) el método del padre.",
            "isinstance(recon, Unidad) retorna True porque Soldado hereda de Unidad.",
        ]),
        "strict_match": True,
    },
    # ── L151 — super() ────────────────────────────────────────────────────────
    {
        "title": "Llamada al Padre",
        "description": (
            "Reimplementá `Soldado` usando `super().__init__()` para reusar\n"
            "el constructor de `Unidad` y extenderlo.\n\n"
            "- `Unidad(nombre, hp)` → `estado()` → `'NOMBRE: HP hp'`\n"
            "- `Soldado(nombre, hp, arma)` usa `super().__init__(nombre, hp)`\n"
            "  y agrega `self.arma`; `estado()` usa `super().estado()` + ` | ARMA`\n\n"
            "Salida esperada:\n"
            "```\nBase: 100 hp\nRECON: 80 hp | Rifle\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 17,
        "level_order": 161,
        "base_xp_reward": 290,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 220,
        "challenge_type": "python",
        "phase": "oop_avanzado",
        "concepts_taught_json": json.dumps(["super", "inheritance", "method_override"]),
        "initial_code": (
            "class Unidad:\n"
            "    def __init__(self, nombre, hp):\n"
            "        self.nombre = nombre\n"
            "        self.hp = hp\n"
            "\n"
            "    def estado(self):\n"
            "        return f'{self.nombre}: {self.hp} hp'\n"
            "\n"
            "class Soldado(Unidad):\n"
            "    def __init__(self, nombre, hp, arma):\n"
            "        super().__init__(nombre, hp)\n"
            "        self.arma = arma\n"
            "\n"
            "    def estado(self):\n"
            "        return super().estado() + f' | {self.arma}'\n"
            "\n"
            "base = Unidad('Base', 100)\n"
            "recon = Soldado('RECON', 80, 'Rifle')\n"
            "print(base.estado())\n"
            "print(recon.estado())\n"
        ),
        "expected_output": "Base: 100 hp\nRECON: 80 hp | Rifle",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "super() es la forma correcta de llamar al constructor del padre. "
            "Evita repetir código y garantiza compatibilidad con herencia múltiple."
        ),
        "pedagogical_objective": "Usar super().__init__() para inicializar atributos del padre sin repetir código.",
        "syntax_hint": "super().__init__(nombre, hp); super().estado() llama al método del padre",
        "theory_content": None,
        "hints_json": json.dumps([
            "super().__init__(nombre, hp) delega la inicialización al constructor de Unidad.",
            "super().estado() llama al método estado() de la clase padre.",
            "Después de super().__init__(), solo necesitás inicializar los atributos nuevos.",
        ]),
        "strict_match": True,
    },
    # ── L152 — @staticmethod ──────────────────────────────────────────────────
    {
        "title": "Método Estático",
        "description": (
            "Implementá la clase `Calculadora` con:\n"
            "- `@staticmethod sumar(a, b)` → a + b\n"
            "- `@staticmethod es_par(n)` → True/False\n"
            "- `@staticmethod max_de_tres(a, b, c)` → el mayor de los tres\n\n"
            "Los métodos estáticos no reciben self ni cls.\n\n"
            "Salida esperada:\n"
            "```\n15\nFalse\n9\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 17,
        "level_order": 162,
        "base_xp_reward": 280,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 180,
        "challenge_type": "python",
        "phase": "oop_avanzado",
        "concepts_taught_json": json.dumps(["staticmethod", "class", "utility_methods"]),
        "initial_code": (
            "class Calculadora:\n"
            "    @staticmethod\n"
            "    def sumar(a, b):\n"
            "        return a + b\n"
            "\n"
            "    @staticmethod\n"
            "    def es_par(n):\n"
            "        return n % 2 == 0\n"
            "\n"
            "    @staticmethod\n"
            "    def max_de_tres(a, b, c):\n"
            "        return max(a, b, c)\n"
            "\n"
            "print(Calculadora.sumar(7, 8))\n"
            "print(Calculadora.es_par(7))\n"
            "print(Calculadora.max_de_tres(5, 9, 3))\n"
        ),
        "expected_output": "15\nFalse\n9",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "Las calculadoras tácticas de DAKI no necesitan estado — son funciones puras "
            "agrupadas en una clase por organización. @staticmethod las agrupa sin overhead de instancia."
        ),
        "pedagogical_objective": "Usar @staticmethod para métodos que no acceden al estado del objeto ni de la clase.",
        "syntax_hint": "@staticmethod def metodo(args): — sin self ni cls",
        "theory_content": None,
        "hints_json": json.dumps([
            "@staticmethod no recibe self (instancia) ni cls (clase) — es una función regular agrupada en la clase.",
            "Se llama con Calculadora.metodo() sin crear instancia.",
            "Usá @staticmethod cuando la lógica no depende de atributos del objeto.",
        ]),
        "strict_match": True,
    },
    # ── L153 — Polimorfismo ───────────────────────────────────────────────────
    {
        "title": "Protocolo Polimórfico",
        "description": (
            "Implementá tres clases que implementan el método `activar()`:\n"
            "- `Sensor`: `activar()` → `'Sensor: escaneando'`\n"
            "- `Turret`: `activar()` → `'Turret: disparando'`\n"
            "- `Shield`: `activar()` → `'Shield: protegiendo'`\n\n"
            "Luego itero sobre una lista de instancias y llamo `activar()` en cada una.\n\n"
            "Salida esperada:\n"
            "```\nSensor: escaneando\nTurret: disparando\nShield: protegiendo\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 17,
        "level_order": 163,
        "base_xp_reward": 280,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 200,
        "challenge_type": "python",
        "phase": "oop_avanzado",
        "concepts_taught_json": json.dumps(["polymorphism", "duck_typing", "class", "interface"]),
        "initial_code": (
            "class Sensor:\n"
            "    def activar(self):\n"
            "        return 'Sensor: escaneando'\n"
            "\n"
            "class Turret:\n"
            "    def activar(self):\n"
            "        return 'Turret: disparando'\n"
            "\n"
            "class Shield:\n"
            "    def activar(self):\n"
            "        return 'Shield: protegiendo'\n"
            "\n"
            "dispositivos = [Sensor(), Turret(), Shield()]\n"
            "for d in dispositivos:\n"
            "    print(d.activar())\n"
        ),
        "expected_output": "Sensor: escaneando\nTurret: disparando\nShield: protegiendo",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El sistema de control del Nexo activa distintos dispositivos con la misma interfaz. "
            "El polimorfismo permite tratar objetos distintos de forma uniforme — "
            "el corazón del diseño orientado a objetos."
        ),
        "pedagogical_objective": "Demostrar polimorfismo: distintos objetos con el mismo método responden diferente.",
        "syntax_hint": "for d in dispositivos: d.activar() — cada objeto llama su propia versión",
        "theory_content": None,
        "hints_json": json.dumps([
            "En Python, el polimorfismo es 'duck typing': si tiene el método activar(), funciona.",
            "No necesitás una clase base común — basta con que cada clase implemente activar().",
            "El loop for d in dispositivos llama el activar() correcto para cada tipo.",
        ]),
        "strict_match": True,
    },
    # ── L154 — BOSS: Jerarquía Completa ─────────────────────────────────────
    {
        "title": "OOP-01: La Red de Nodos",
        "description": (
            "BOSS DEL SECTOR — Jerarquía OOP completa.\n\n"
            "Implementá:\n"
            "- `Nodo(id, capacidad)`: base con `info()` → `'Nodo#ID [capacidad]'`\n"
            "- `NodoActivo(id, capacidad, tipo)`: hereda con super(); "
            "`info()` → `'[TIPO] Nodo#ID [capacidad]'`; "
            "`@classmethod crear(cls, config)` parsea `'ID:CAP:TIPO'`\n\n"
            "Con la lista `['1:100:RECON', '2:200:ATAQUE', '3:150:DEFENSA']`\n"
            "creá nodos y ordenálos por capacidad desc. Imprimí su info.\n\n"
            "Salida esperada:\n"
            "```\n[ATAQUE] Nodo#2 [200]\n[DEFENSA] Nodo#3 [150]\n[RECON] Nodo#1 [100]\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "hard",
        "sector_id": 17,
        "level_order": 164,
        "base_xp_reward": 700,
        "is_project": False,
        "is_phase_boss": True,
        "telemetry_goal_time": 480,
        "challenge_type": "python",
        "phase": "oop_avanzado",
        "concepts_taught_json": json.dumps(["inheritance", "super", "classmethod", "__str__", "sorted", "lambda"]),
        "initial_code": (
            "class Nodo:\n"
            "    def __init__(self, id, capacidad):\n"
            "        self.id = id\n"
            "        self.capacidad = capacidad\n"
            "\n"
            "    def info(self):\n"
            "        return f'Nodo#{self.id} [{self.capacidad}]'\n"
            "\n"
            "class NodoActivo(Nodo):\n"
            "    def __init__(self, id, capacidad, tipo):\n"
            "        super().__init__(id, capacidad)\n"
            "        self.tipo = tipo\n"
            "\n"
            "    def info(self):\n"
            "        return f'[{self.tipo}] Nodo#{self.id} [{self.capacidad}]'\n"
            "\n"
            "    @classmethod\n"
            "    def crear(cls, config):\n"
            "        partes = config.split(':')\n"
            "        return cls(partes[0], int(partes[1]), partes[2])\n"
            "\n"
            "configs = ['1:100:RECON', '2:200:ATAQUE', '3:150:DEFENSA']\n"
            "nodos = [NodoActivo.crear(c) for c in configs]\n"
            "nodos.sort(key=lambda n: n.capacidad, reverse=True)\n"
            "for n in nodos:\n"
            "    print(n.info())\n"
        ),
        "expected_output": "[ATAQUE] Nodo#2 [200]\n[DEFENSA] Nodo#3 [150]\n[RECON] Nodo#1 [100]",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El Nexo organiza su infraestructura como una red de nodos con distintas capacidades. "
            "DAKI despliega los nodos de mayor capacidad primero — la jerarquía OOP "
            "permite crear, clasificar y gestionar la red eficientemente."
        ),
        "pedagogical_objective": "Integrar herencia, super(), @classmethod constructor alternativo y sorted con lambda.",
        "syntax_hint": "@classmethod def crear(cls, config): partes = config.split(':'); return cls(...)",
        "theory_content": None,
        "hints_json": json.dumps([
            "NodoActivo.crear() parsea 'ID:CAP:TIPO' y crea la instancia con cls(id, cap, tipo).",
            "nodos.sort(key=lambda n: n.capacidad, reverse=True) ordena por capacidad descendente.",
            "super().__init__(id, capacidad) inicializa los atributos heredados de Nodo.",
        ]),
        "strict_match": True,
    },
]
