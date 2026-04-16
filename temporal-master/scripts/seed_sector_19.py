"""
seed_sector_19.py — Sector 19: Proyecto Modular (niveles 160–165)
=================================================================
Niveles 160–165  |  6 misiones  |  Sector ID = 18

Temática técnica: estructuras de proyectos Python.
if __name__, json, sys.argv (simulado), módulos, dataclasses básicas.

Nivel 165 (Boss): proyecto integrador final del sector.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.models.challenge import Challenge, DifficultyTier  # noqa: F401

SECTOR_19 = [
    # ── L160 — if __name__ == '__main__' ──────────────────────────────────────
    {
        "title": "El Guardián del Main",
        "description": (
            "Definí la función `calcular_imc(peso, altura)` que retorna el IMC\n"
            "(peso / altura²), redondeado a 1 decimal.\n\n"
            "Luego usá el patrón `if __name__ == '__main__'` para ejecutar:\n"
            "```python\nprint(calcular_imc(70, 1.75))\nprint(calcular_imc(90, 1.80))\n```\n\n"
            "Salida esperada:\n"
            "```\n22.9\n27.8\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 19,
        "level_order": 170,
        "base_xp_reward": 300,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 180,
        "challenge_type": "python",
        "phase": "proyecto",
        "concepts_taught_json": json.dumps(["__name__", "main_guard", "function", "module"]),
        "initial_code": (
            "def calcular_imc(peso, altura):\n"
            "    return round(peso / altura**2, 1)\n"
            "\n"
            "if __name__ == '__main__':\n"
            "    print(calcular_imc(70, 1.75))\n"
            "    print(calcular_imc(90, 1.80))\n"
        ),
        "expected_output": "22.9\n27.8",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El patrón `if __name__ == '__main__'` es el estándar para scripts Python. "
            "Separa el código 'ejecutable como script' del código 'importable como módulo'. "
            "DAKI usa este patrón en todos sus módulos de análisis."
        ),
        "pedagogical_objective": "Entender el guardián __main__ para separar código ejecutable de código importable.",
        "syntax_hint": "if __name__ == '__main__': — el código dentro solo corre cuando ejecutás el script directamente",
        "theory_content": None,
        "hints_json": json.dumps([
            "__name__ vale '__main__' cuando ejecutás el script directamente.",
            "Si otro módulo importa este archivo, __name__ vale el nombre del módulo — el bloque no se ejecuta.",
            "Poné siempre la lógica principal dentro de if __name__ == '__main__'.",
        ]),
        "strict_match": True,
    },
    # ── L161 — json.dumps / json.loads ────────────────────────────────────────
    {
        "title": "JSON: El Lenguaje de los Datos",
        "description": (
            "Trabajá con el módulo `json`:\n\n"
            "1. Convertí el dict a JSON string (con indent=2)\n"
            "2. Volvé a parsearlo y accedé al campo `'mision'`\n\n"
            "Dict: `{'operador': 'NEXO', 'nivel': 7, 'mision': 'ALFA-01'}`\n\n"
            "Salida esperada:\n"
            "```\n{\n  \"operador\": \"NEXO\",\n  \"nivel\": 7,\n  \"mision\": \"ALFA-01\"\n}\nALFA-01\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 19,
        "level_order": 171,
        "base_xp_reward": 300,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 180,
        "challenge_type": "python",
        "phase": "proyecto",
        "concepts_taught_json": json.dumps(["json", "dumps", "loads", "serialization"]),
        "initial_code": (
            "import json\n"
            "\n"
            "datos = {'operador': 'NEXO', 'nivel': 7, 'mision': 'ALFA-01'}\n"
            "\n"
            "json_str = json.dumps(datos, indent=2)\n"
            "print(json_str)\n"
            "\n"
            "recuperado = json.loads(json_str)\n"
            "print(recuperado['mision'])\n"
        ),
        "expected_output": '{\n  "operador": "NEXO",\n  "nivel": 7,\n  "mision": "ALFA-01"\n}\nALFA-01',
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "JSON es el formato universal de intercambio de datos del Nexo. "
            "json.dumps() serializa Python → JSON string; json.loads() deserializa JSON string → Python."
        ),
        "pedagogical_objective": "Usar json.dumps() con indent para serialización legible y json.loads() para deserialización.",
        "syntax_hint": "json.dumps(dict, indent=2); json.loads(json_string)['clave']",
        "theory_content": None,
        "hints_json": json.dumps([
            "json.dumps(datos, indent=2) convierte el dict a string JSON con indentación de 2 espacios.",
            "json.loads(json_str) convierte el string JSON de vuelta a dict Python.",
            "El resultado de json.dumps usa comillas dobles — es el estándar JSON.",
        ]),
        "strict_match": True,
    },
    # ── L162 — Argumentos de CLI (simulado) ───────────────────────────────────
    {
        "title": "Argumentos de Línea de Comandos",
        "description": (
            "Simulá el procesamiento de argumentos de línea de comandos.\n\n"
            "Dado `args = ['nexo_tool.py', '--modo', 'ataque', '--nivel', '7']`,\n"
            "parseá los argumentos en un dict ignorando el nombre del script.\n\n"
            "Imprimí el dict resultante y luego el valor de `'--modo'`.\n\n"
            "Salida esperada:\n"
            "```\n{'--modo': 'ataque', '--nivel': '7'}\nataque\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 19,
        "level_order": 172,
        "base_xp_reward": 310,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 200,
        "challenge_type": "python",
        "phase": "proyecto",
        "concepts_taught_json": json.dumps(["sys_argv", "cli_args", "dict", "loop"]),
        "initial_code": (
            "args = ['nexo_tool.py', '--modo', 'ataque', '--nivel', '7']\n"
            "\n"
            "# Ignoramos el primer arg (nombre del script)\n"
            "params = {}\n"
            "pares = args[1:]\n"
            "for i in range(0, len(pares), 2):\n"
            "    params[pares[i]] = pares[i+1]\n"
            "\n"
            "print(params)\n"
            "print(params['--modo'])\n"
        ),
        "expected_output": "{'--modo': 'ataque', '--nivel': '7'}\nataque",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "Las herramientas de DAKI se ejecutan desde terminal con argumentos. "
            "sys.argv contiene el nombre del script + todos los argumentos. "
            "Parsearlos manualmente enseña el patrón antes de usar argparse."
        ),
        "pedagogical_objective": "Parsear argumentos CLI como pares flag/valor iterando de a 2 con range(0, n, 2).",
        "syntax_hint": "for i in range(0, len(pares), 2): params[pares[i]] = pares[i+1]",
        "theory_content": None,
        "hints_json": json.dumps([
            "args[1:] omite el nombre del script (primer elemento).",
            "range(0, len(pares), 2) itera de 2 en 2: [0, 2, 4, ...] para tomar flag + valor.",
            "pares[i] es el flag ('--modo'), pares[i+1] es el valor ('ataque').",
        ]),
        "strict_match": True,
    },
    # ── L163 — Módulo con constantes ─────────────────────────────────────────
    {
        "title": "Estructura de Módulo",
        "description": (
            "Simulá la estructura de un módulo Python con constantes y funciones.\n\n"
            "Define las constantes `VERSION = '1.0.0'` y `NOMBRE = 'NEXO-CORE'`.\n"
            "Implementá `info_modulo()` que retorna el string formateado:\n"
            "`'NEXO-CORE v1.0.0'`\n\n"
            "Implementá `calcular_xp(base, multiplicador)` → base * multiplicador\n\n"
            "Salida esperada:\n"
            "```\nNEXO-CORE v1.0.0\n750\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 19,
        "level_order": 173,
        "base_xp_reward": 310,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 150,
        "challenge_type": "python",
        "phase": "proyecto",
        "concepts_taught_json": json.dumps(["constants", "module_structure", "function"]),
        "initial_code": (
            "VERSION = '1.0.0'\n"
            "NOMBRE = 'NEXO-CORE'\n"
            "\n"
            "def info_modulo():\n"
            "    return f'{NOMBRE} v{VERSION}'\n"
            "\n"
            "def calcular_xp(base, multiplicador):\n"
            "    return base * multiplicador\n"
            "\n"
            "if __name__ == '__main__':\n"
            "    print(info_modulo())\n"
            "    print(calcular_xp(150, 5))\n"
        ),
        "expected_output": "NEXO-CORE v1.0.0\n750",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "Los módulos de DAKI siguen una estructura estándar: constantes en MAYÚSCULAS al tope, "
            "funciones con nombres descriptivos, y el bloque __main__ al final."
        ),
        "pedagogical_objective": "Establecer la convención de constantes en MAYÚSCULAS y estructura estándar de módulo.",
        "syntax_hint": "VERSION = '1.0.0'; constantes en MAYÚSCULAS son convención Python",
        "theory_content": None,
        "hints_json": json.dumps([
            "Las constantes en Python se definen en MAYÚSCULAS por convención (PEP 8).",
            "info_modulo() usa las constantes del módulo directamente — son accesibles en todo el scope.",
            "Poné el código de ejecución dentro de if __name__ == '__main__'.",
        ]),
        "strict_match": True,
    },
    # ── L164 — json con archivos ──────────────────────────────────────────────
    {
        "title": "Persistencia JSON",
        "description": (
            "Guardá un dict como JSON en `/tmp/config.json` y volvelo a leer.\n\n"
            "Dict: `{'version': '2.0', 'debug': False, 'max_ops': 100}`\n\n"
            "Escribí con `json.dump(datos, f)` y leé con `json.load(f)`.\n"
            "Imprimí el dict recuperado y luego el valor de `'max_ops'`.\n\n"
            "Salida esperada:\n"
            "```\n{'version': '2.0', 'debug': False, 'max_ops': 100}\n100\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 19,
        "level_order": 174,
        "base_xp_reward": 310,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 200,
        "challenge_type": "python",
        "phase": "proyecto",
        "concepts_taught_json": json.dumps(["json", "dump", "load", "file_io", "persistence"]),
        "initial_code": (
            "import json\n"
            "\n"
            "datos = {'version': '2.0', 'debug': False, 'max_ops': 100}\n"
            "\n"
            "with open('/tmp/config.json', 'w') as f:\n"
            "    json.dump(datos, f)\n"
            "\n"
            "with open('/tmp/config.json', 'r') as f:\n"
            "    config = json.load(f)\n"
            "\n"
            "print(config)\n"
            "print(config['max_ops'])\n"
        ),
        "expected_output": "{'version': '2.0', 'debug': False, 'max_ops': 100}\n100",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "La configuración de DAKI persiste entre sesiones en archivos JSON. "
            "json.dump() escribe directo a un archivo; json.load() lo lee — "
            "más eficiente que dumps/loads para archivos."
        ),
        "pedagogical_objective": "Distinguir json.dumps/loads (string) de json.dump/load (archivo).",
        "syntax_hint": "json.dump(datos, f) escribe al archivo; json.load(f) lee del archivo",
        "theory_content": None,
        "hints_json": json.dumps([
            "json.dump(datos, f) — escribe al archivo abierto f.",
            "json.load(f) — lee del archivo abierto f y retorna el objeto Python.",
            "La diferencia: dump/load trabajan con archivos; dumps/loads trabajan con strings.",
        ]),
        "strict_match": True,
    },
    # ── L165 — BOSS: Proyecto Integrador ──────────────────────────────────────
    {
        "title": "NEXO-FINAL: Gestor de Misiones",
        "description": (
            "BOSS DEL SECTOR — Proyecto modular completo.\n\n"
            "Implementá un gestor de misiones:\n"
            "1. Clase `GestorMisiones` con `__init__` (lista vacía), `agregar(mision_dict)`,\n"
            "   `serializar()` → json.dumps con indent=2, `reporte()` → imprime stats\n"
            "2. Agregá 3 misiones: `{'id':'M1','xp':300,'tipo':'RECON'}`,\n"
            "   `{'id':'M2','xp':500,'tipo':'ATAQUE'}`, `{'id':'M3','xp':300,'tipo':'RECON'}`\n"
            "3. Reporte imprime: total, xp_total, tipos únicos ordenados\n\n"
            "Salida esperada:\n"
            "```\nTotal: 3 misiones\nXP total: 1100\nTipos: ATAQUE, RECON\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "hard",
        "sector_id": 19,
        "level_order": 175,
        "base_xp_reward": 700,
        "is_project": False,
        "is_phase_boss": True,
        "telemetry_goal_time": 480,
        "challenge_type": "python",
        "phase": "proyecto",
        "concepts_taught_json": json.dumps(["class", "json", "set", "sorted", "sum"]),
        "initial_code": (
            "import json\n"
            "\n"
            "class GestorMisiones:\n"
            "    def __init__(self):\n"
            "        self.misiones = []\n"
            "\n"
            "    def agregar(self, mision):\n"
            "        self.misiones.append(mision)\n"
            "\n"
            "    def serializar(self):\n"
            "        return json.dumps(self.misiones, indent=2)\n"
            "\n"
            "    def reporte(self):\n"
            "        total = len(self.misiones)\n"
            "        xp_total = sum(m['xp'] for m in self.misiones)\n"
            "        tipos = ', '.join(sorted(set(m['tipo'] for m in self.misiones)))\n"
            "        print(f'Total: {total} misiones')\n"
            "        print(f'XP total: {xp_total}')\n"
            "        print(f'Tipos: {tipos}')\n"
            "\n"
            "gestor = GestorMisiones()\n"
            "gestor.agregar({'id':'M1','xp':300,'tipo':'RECON'})\n"
            "gestor.agregar({'id':'M2','xp':500,'tipo':'ATAQUE'})\n"
            "gestor.agregar({'id':'M3','xp':300,'tipo':'RECON'})\n"
            "gestor.reporte()\n"
        ),
        "expected_output": "Total: 3 misiones\nXP total: 1100\nTipos: ATAQUE, RECON",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "DAKI necesita un gestor de misiones que combine OOP, JSON y análisis de datos. "
            "Este proyecto integra todo lo aprendido en el sector — "
            "clases, json, set para únicos, sorted para orden, sum para totales."
        ),
        "pedagogical_objective": "Integrar class, json.dumps, set() para únicos, sum() con generator y sorted() en un proyecto cohesivo.",
        "syntax_hint": "set(m['tipo'] for m in self.misiones) da tipos únicos; sorted() los ordena",
        "theory_content": None,
        "hints_json": json.dumps([
            "sum(m['xp'] for m in self.misiones) suma los XP de todas las misiones.",
            "set(m['tipo'] for m in self.misiones) obtiene tipos sin duplicados.",
            "sorted(set(...)) ordena los tipos; join() los une con coma y espacio.",
        ]),
        "strict_match": True,
    },
]
