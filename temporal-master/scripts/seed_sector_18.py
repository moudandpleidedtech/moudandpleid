"""
seed_sector_18.py — Sector 18: Manejo de Errores Avanzado (niveles 155–159)
============================================================================
Niveles 155–159  |  5 misiones  |  Sector ID = 17

El nivel 175 (Boss) es el CONTRATO-175 en seed_contratos.py.

Temática técnica: errores avanzados más allá de try/except básico.
Excepciones con mensajes, jerarquía de excepciones, raise explícito,
clases de excepción custom, context managers con __enter__/__exit__.

Nota: Sector 9 cubrió try/except/finally básico. Este sector cubre
el lado del LANZAMIENTO de excepciones y excepciones como contratos.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.models.challenge import Challenge, DifficultyTier  # noqa: F401

SECTOR_18 = [
    # ── L155 — raise explícito ────────────────────────────────────────────────
    {
        "title": "Lanzar Excepciones",
        "description": (
            "Implementá `dividir(a, b)` que lanza `ValueError` si b es 0\n"
            "con el mensaje `'No se puede dividir por cero'`.\n"
            "Si no, retorna a / b.\n\n"
            "Luego capturá la excepción al llamar `dividir(10, 0)`.\n\n"
            "Salida esperada:\n"
            "```\n5.0\nError: No se puede dividir por cero\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 18,
        "level_order": 165,
        "base_xp_reward": 300,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 180,
        "challenge_type": "python",
        "phase": "errores",
        "concepts_taught_json": json.dumps(["raise", "ValueError", "try_except", "exception"]),
        "initial_code": (
            "def dividir(a, b):\n"
            "    if b == 0:\n"
            "        raise ValueError('No se puede dividir por cero')\n"
            "    return a / b\n"
            "\n"
            "print(dividir(10, 2))\n"
            "\n"
            "try:\n"
            "    print(dividir(10, 0))\n"
            "except ValueError as e:\n"
            "    print(f'Error: {e}')\n"
        ),
        "expected_output": "5.0\nError: No se puede dividir por cero",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "Las funciones de DAKI usan `raise` para señalar condiciones inválidas. "
            "Es la diferencia entre 'retornar None en silencio' y 'anunciar el error claramente'."
        ),
        "pedagogical_objective": "Usar raise para lanzar ValueError con mensaje descriptivo desde dentro de una función.",
        "syntax_hint": "raise ValueError('mensaje'); except ValueError as e: print(e)",
        "theory_content": None,
        "hints_json": json.dumps([
            "raise ValueError('mensaje') lanza la excepción inmediatamente.",
            "except ValueError as e: captura la excepción y e contiene el mensaje.",
            "print(f'Error: {e}') imprime el mensaje de la excepción.",
        ]),
        "strict_match": True,
    },
    # ── L156 — Excepción custom ────────────────────────────────────────────────
    {
        "title": "Excepción Personalizada",
        "description": (
            "Creá la excepción custom `ErrorDeAcceso(Exception)` que acepta\n"
            "`usuario` y `razon` en su constructor. Su `__str__` retorna:\n"
            "`'Acceso denegado a USUARIO: RAZON'`\n\n"
            "Implementá `verificar_nivel(usuario, nivel)` que lanza `ErrorDeAcceso`\n"
            "si nivel < 5 con razon='nivel insuficiente'.\n\n"
            "Salida esperada:\n"
            "```\nAcceso denegado a BETA: nivel insuficiente\nOK: NEXO tiene nivel 7\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 18,
        "level_order": 166,
        "base_xp_reward": 325,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 240,
        "challenge_type": "python",
        "phase": "errores",
        "concepts_taught_json": json.dumps(["custom_exception", "Exception", "__str__", "raise"]),
        "initial_code": (
            "class ErrorDeAcceso(Exception):\n"
            "    def __init__(self, usuario, razon):\n"
            "        self.usuario = usuario\n"
            "        self.razon = razon\n"
            "\n"
            "    def __str__(self):\n"
            "        return f'Acceso denegado a {self.usuario}: {self.razon}'\n"
            "\n"
            "def verificar_nivel(usuario, nivel):\n"
            "    if nivel < 5:\n"
            "        raise ErrorDeAcceso(usuario, 'nivel insuficiente')\n"
            "    return f'OK: {usuario} tiene nivel {nivel}'\n"
            "\n"
            "try:\n"
            "    verificar_nivel('BETA', 3)\n"
            "except ErrorDeAcceso as e:\n"
            "    print(e)\n"
            "\n"
            "print(verificar_nivel('NEXO', 7))\n"
        ),
        "expected_output": "Acceso denegado a BETA: nivel insuficiente\nOK: NEXO tiene nivel 7",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "Las excepciones custom de DAKI son más informativas que las genéricas. "
            "ErrorDeAcceso incluye quién intentó acceder y por qué fue rechazado — "
            "información crucial para el log de seguridad."
        ),
        "pedagogical_objective": "Crear clase de excepción custom heredando de Exception con atributos propios.",
        "syntax_hint": "class ErrorDeAcceso(Exception): def __init__(self, usuario, razon): ...",
        "theory_content": None,
        "hints_json": json.dumps([
            "Las excepciones custom heredan de Exception (o de una subclase más específica).",
            "__str__ define cómo se muestra cuando se imprime o convierte a string.",
            "except ErrorDeAcceso as e: captura solo esta excepción; e.usuario y e.razon están disponibles.",
        ]),
        "strict_match": True,
    },
    # ── L157 — Encadenamiento de excepciones ──────────────────────────────────
    {
        "title": "Cadena de Errores",
        "description": (
            "Implementá `procesar_dato(valor)` que:\n"
            "1. Intenta convertir `valor` a int con int()\n"
            "2. Si falla, lanza `ValueError` con mensaje `'Dato invalido: VALOR'`\n"
            "   usando `raise ... from None` (suprime el contexto original)\n\n"
            "Salida esperada:\n"
            "```\n42\nDato invalido: abc\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 18,
        "level_order": 167,
        "base_xp_reward": 325,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 200,
        "challenge_type": "python",
        "phase": "errores",
        "concepts_taught_json": json.dumps(["exception_chaining", "raise_from", "ValueError"]),
        "initial_code": (
            "def procesar_dato(valor):\n"
            "    try:\n"
            "        return int(valor)\n"
            "    except ValueError:\n"
            "        raise ValueError(f'Dato invalido: {valor}') from None\n"
            "\n"
            "try:\n"
            "    print(procesar_dato('42'))\n"
            "    print(procesar_dato('abc'))\n"
            "except ValueError as e:\n"
            "    print(e)\n"
        ),
        "expected_output": "42\nDato invalido: abc",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "Cuando una capa de DAKI falla, relanza la excepción con un mensaje más claro "
            "para la capa superior. `raise ... from None` limpia el traceback innecesario."
        ),
        "pedagogical_objective": "Usar raise Exception from None para relanzar con mensaje más descriptivo.",
        "syntax_hint": "except ValueError: raise ValueError(f'msg {valor}') from None",
        "theory_content": None,
        "hints_json": json.dumps([
            "raise ValueError('mensaje') from None relanza una excepción nueva sin el contexto original.",
            "Esto limpia el traceback — en lugar de ver la excepción original de int(), ves solo la tuya.",
            "procesar_dato('42') retorna 42 normalmente; procesar_dato('abc') lanza el ValueError.",
        ]),
        "strict_match": True,
    },
    # ── L158 — finally garantizado ────────────────────────────────────────────
    {
        "title": "Limpieza Garantizada",
        "description": (
            "Implementá `conectar_y_procesar(datos)` que:\n"
            "1. 'Abre conexión' (imprime `'CONEXION: abierta'`)\n"
            "2. Procesa los datos (suma los enteros de la lista)\n"
            "3. Si la lista está vacía, lanza `ValueError('datos vacios')`\n"
            "4. En `finally`, siempre imprimí `'CONEXION: cerrada'`\n\n"
            "Salida esperada:\n"
            "```\nCONEXION: abierta\nResultado: 15\nCONEXION: cerrada\nCONEXION: abierta\nError: datos vacios\nCONEXION: cerrada\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 18,
        "level_order": 168,
        "base_xp_reward": 325,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 220,
        "challenge_type": "python",
        "phase": "errores",
        "concepts_taught_json": json.dumps(["finally", "try_except", "cleanup", "raise"]),
        "initial_code": (
            "def conectar_y_procesar(datos):\n"
            "    print('CONEXION: abierta')\n"
            "    try:\n"
            "        if not datos:\n"
            "            raise ValueError('datos vacios')\n"
            "        print(f'Resultado: {sum(datos)}')\n"
            "    except ValueError as e:\n"
            "        print(f'Error: {e}')\n"
            "    finally:\n"
            "        print('CONEXION: cerrada')\n"
            "\n"
            "conectar_y_procesar([1,2,3,4,5])\n"
            "conectar_y_procesar([])\n"
        ),
        "expected_output": "CONEXION: abierta\nResultado: 15\nCONEXION: cerrada\nCONEXION: abierta\nError: datos vacios\nCONEXION: cerrada",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "Las conexiones del Nexo deben cerrarse siempre — incluso si la misión falla. "
            "finally garantiza limpieza sin importar qué pase en try o except."
        ),
        "pedagogical_objective": "Usar finally para código de limpieza que se ejecuta siempre, con o sin excepción.",
        "syntax_hint": "try: ... except ValueError as e: ... finally: print('CONEXION: cerrada')",
        "theory_content": None,
        "hints_json": json.dumps([
            "finally se ejecuta SIEMPRE — si hay excepción O si todo sale bien.",
            "Es el lugar correcto para limpiar recursos (cerrar conexiones, archivos, etc.).",
            "Primero imprimí 'CONEXION: abierta', después el try/except/finally.",
        ]),
        "strict_match": True,
    },
    # ── L159 — Context Manager ─────────────────────────────────────────────────
    {
        "title": "Gestor de Contexto",
        "description": (
            "Implementá la clase `ConexionSimulada` como context manager:\n"
            "- `__enter__`: imprime `'>> Conexion establecida'`, retorna `self`\n"
            "- `__exit__(exc_type, exc_val, exc_tb)`: imprime\n"
            "  `'>> Conexion cerrada'` (retorna False para no suprimir errores)\n\n"
            "Usala con `with ConexionSimulada() as conn`:\n"
            "  imprime `'Procesando datos...'`\n\n"
            "Salida esperada:\n"
            "```\n>> Conexion establecida\nProcesando datos...\n>> Conexion cerrada\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "hard",
        "sector_id": 18,
        "level_order": 169,
        "base_xp_reward": 400,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 280,
        "challenge_type": "python",
        "phase": "errores",
        "concepts_taught_json": json.dumps(["context_manager", "__enter__", "__exit__", "with"]),
        "initial_code": (
            "class ConexionSimulada:\n"
            "    def __enter__(self):\n"
            "        print('>> Conexion establecida')\n"
            "        return self\n"
            "\n"
            "    def __exit__(self, exc_type, exc_val, exc_tb):\n"
            "        print('>> Conexion cerrada')\n"
            "        return False\n"
            "\n"
            "with ConexionSimulada() as conn:\n"
            "    print('Procesando datos...')\n"
        ),
        "expected_output": ">> Conexion establecida\nProcesando datos...\n>> Conexion cerrada",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El protocolo `with` de Python garantiza que `__exit__` se llame siempre — "
            "incluso si hay una excepción dentro del bloque. "
            "Es la forma idiomática de gestionar recursos en Python."
        ),
        "pedagogical_objective": "Implementar el protocolo context manager con __enter__ y __exit__ para uso con `with`.",
        "syntax_hint": "def __enter__(self): return self; def __exit__(self, *args): return False",
        "theory_content": None,
        "hints_json": json.dumps([
            "__enter__ se ejecuta al entrar al bloque with; lo que retorna se asigna a la variable 'as'.",
            "__exit__ se ejecuta SIEMPRE al salir del bloque with, incluso con excepciones.",
            "Retornar False en __exit__ significa 'no suprimir las excepciones'.",
        ]),
        "strict_match": True,
    },
]
