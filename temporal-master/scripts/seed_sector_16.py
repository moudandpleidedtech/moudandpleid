"""
seed_sector_16.py — Sector 16: File I/O (niveles 141–146)
==========================================================
Niveles 141–146  |  6 misiones  |  Sector ID = 15

Temática técnica: lectura y escritura de archivos en Python.
open(), with, r/w/a, readlines(), CSV (csv.writer, csv.reader, csv.DictReader).

Nivel 146 (Boss): procesamiento CSV con Counter.

NOTA SANDBOX: Los challenges de File I/O se diseñan usando StringIO o
simulando el contenido como string (la ejecución real en sandbox escribe en /tmp).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.models.challenge import Challenge, DifficultyTier  # noqa: F401

SECTOR_16 = [
    # ── L141 — open write + read ──────────────────────────────────────────────
    {
        "title": "Escribir y Leer",
        "description": (
            "Escribí un archivo y volvelo a leer.\n\n"
            "1. Escribí las líneas `'NEXO'`, `'DAKI'`, `'ALFA'` en `/tmp/nexo.txt`\n"
            "   (una por línea, usando el modo `'w'` y `with`)\n"
            "2. Leé el archivo completo e imprimí su contenido (sin newline extra)\n\n"
            "Salida esperada:\n"
            "```\nNEXO\nDAKI\nALFA\n```"
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "easy",
        "sector_id": 16,
        "level_order": 151,
        "base_xp_reward": 250,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 180,
        "challenge_type": "python",
        "phase": "fileio",
        "concepts_taught_json": json.dumps(["file_io", "open", "write", "read", "with"]),
        "initial_code": (
            "# Escribir\n"
            "with open('/tmp/nexo.txt', 'w') as f:\n"
            "    f.write('NEXO\\n')\n"
            "    f.write('DAKI\\n')\n"
            "    f.write('ALFA\\n')\n"
            "\n"
            "# Leer\n"
            "with open('/tmp/nexo.txt', 'r') as f:\n"
            "    contenido = f.read()\n"
            "print(contenido, end='')\n"
        ),
        "expected_output": "NEXO\nDAKI\nALFA",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "DAKI persiste los registros de operaciones en disco. La escritura atómica "
            "con `with` garantiza que el archivo se cierre correctamente incluso ante errores."
        ),
        "pedagogical_objective": "Usar `with open()` en modo 'w' para escribir y 'r' para leer — la forma idiomática de File I/O.",
        "syntax_hint": "with open('archivo', 'w') as f: f.write('texto\\n')",
        "theory_content": None,
        "hints_json": json.dumps([
            "El modo 'w' crea el archivo (o lo sobreescribe). 'r' lo abre solo lectura.",
            "f.write() necesita el \\n explícito — no lo agrega automáticamente.",
            "print(contenido, end='') evita la doble línea en blanco al final.",
        ]),
        "strict_match": True,
    },
    # ── L142 — writelines + readlines ─────────────────────────────────────────
    {
        "title": "Línea por Línea",
        "description": (
            "1. Escribí usando `writelines()` las líneas del log:\n"
            "   `['ERROR: timeout\\n', 'INFO: conectado\\n', 'ERROR: memoria\\n']`\n"
            "   en `/tmp/log.txt`\n"
            "2. Leé línea por línea con `for line in f` e imprimí\n"
            "   solo las que empiezan con `'ERROR'` (sin el newline)\n\n"
            "Salida esperada:\n"
            "```\nERROR: timeout\nERROR: memoria\n```"
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "easy",
        "sector_id": 16,
        "level_order": 152,
        "base_xp_reward": 255,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 180,
        "challenge_type": "python",
        "phase": "fileio",
        "concepts_taught_json": json.dumps(["file_io", "writelines", "readlines", "strip", "for_loop"]),
        "initial_code": (
            "lineas = ['ERROR: timeout\\n', 'INFO: conectado\\n', 'ERROR: memoria\\n']\n"
            "\n"
            "with open('/tmp/log.txt', 'w') as f:\n"
            "    f.writelines(lineas)\n"
            "\n"
            "with open('/tmp/log.txt', 'r') as f:\n"
            "    for line in f:\n"
            "        if line.startswith('ERROR'):\n"
            "            print(line.strip())\n"
        ),
        "expected_output": "ERROR: timeout\nERROR: memoria",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El analizador de logs de DAKI filtra millones de líneas buscando errores críticos. "
            "Leer línea por línea es eficiente en memoria — no carga el archivo completo."
        ),
        "pedagogical_objective": "Usar writelines() para escribir listas y for line in f para iterar eficientemente.",
        "syntax_hint": "f.writelines(lista_de_lineas); for line in f: if line.startswith('X'): print(line.strip())",
        "theory_content": None,
        "hints_json": json.dumps([
            "writelines() escribe la lista sin agregar separadores — las líneas deben incluir \\n.",
            "for line in f itera el archivo línea por línea sin cargar todo en memoria.",
            "line.strip() elimina el \\n al final.",
        ]),
        "strict_match": True,
    },
    # ── L143 — modo append ────────────────────────────────────────────────────
    {
        "title": "Modo Acumulativo",
        "description": (
            "Implementá un sistema de log que acumule entradas:\n\n"
            "1. Escribí `'SESION 1\\n'` en `/tmp/historial.txt` (modo 'w')\n"
            "2. Agregá `'SESION 2\\n'` y `'SESION 3\\n'` (modo 'a')\n"
            "3. Leé e imprimí el archivo completo\n\n"
            "Salida esperada:\n"
            "```\nSESION 1\nSESION 2\nSESION 3\n```"
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "easy",
        "sector_id": 16,
        "level_order": 153,
        "base_xp_reward": 255,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 150,
        "challenge_type": "python",
        "phase": "fileio",
        "concepts_taught_json": json.dumps(["file_io", "append_mode", "open"]),
        "initial_code": (
            "with open('/tmp/historial.txt', 'w') as f:\n"
            "    f.write('SESION 1\\n')\n"
            "\n"
            "with open('/tmp/historial.txt', 'a') as f:\n"
            "    f.write('SESION 2\\n')\n"
            "    f.write('SESION 3\\n')\n"
            "\n"
            "with open('/tmp/historial.txt', 'r') as f:\n"
            "    print(f.read(), end='')\n"
        ),
        "expected_output": "SESION 1\nSESION 2\nSESION 3",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El historial de misiones de DAKI se acumula sin sobreescribir registros anteriores. "
            "El modo 'a' (append) agrega al final del archivo existente."
        ),
        "pedagogical_objective": "Distinguir modo 'w' (sobreescribir/crear) de modo 'a' (agregar al final).",
        "syntax_hint": "open('archivo', 'a') agrega al final; open('archivo', 'w') sobreescribe",
        "theory_content": None,
        "hints_json": json.dumps([
            "El modo 'w' crea el archivo nuevo o lo vacía si ya existe.",
            "El modo 'a' agrega al final del archivo sin borrar lo existente.",
        ]),
        "strict_match": True,
    },
    # ── L144 — readlines + comprehension ──────────────────────────────────────
    {
        "title": "Filtro de Registros",
        "description": (
            "1. Escribí en `/tmp/datos.txt` los números del 1 al 10 (uno por línea)\n"
            "2. Leelos con `readlines()` y usá list comprehension para\n"
            "   obtener los pares como enteros\n"
            "3. Imprimí la lista de pares\n\n"
            "Salida esperada:\n"
            "```\n[2, 4, 6, 8, 10]\n```"
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "easy",
        "sector_id": 16,
        "level_order": 154,
        "base_xp_reward": 260,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 180,
        "challenge_type": "python",
        "phase": "fileio",
        "concepts_taught_json": json.dumps(["file_io", "readlines", "list_comprehension", "strip"]),
        "initial_code": (
            "with open('/tmp/datos.txt', 'w') as f:\n"
            "    for i in range(1, 11):\n"
            "        f.write(f'{i}\\n')\n"
            "\n"
            "with open('/tmp/datos.txt', 'r') as f:\n"
            "    lineas = f.readlines()\n"
            "\n"
            "pares = [int(l.strip()) for l in lineas if int(l.strip()) % 2 == 0]\n"
            "print(pares)\n"
        ),
        "expected_output": "[2, 4, 6, 8, 10]",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El procesador de DAKI filtra registros de sensores para quedarse solo con los "
            "datos pares — los que corresponden a mediciones en ciclos regulares."
        ),
        "pedagogical_objective": "Usar readlines() para cargar todas las líneas, luego filtrar con list comprehension.",
        "syntax_hint": "[int(l.strip()) for l in readlines() if int(l.strip()) % 2 == 0]",
        "theory_content": None,
        "hints_json": json.dumps([
            "readlines() retorna una lista de strings, cada uno con \\n al final.",
            "Usá .strip() para eliminar el \\n antes de convertir con int().",
            "Filtrá los pares con if int(l.strip()) % 2 == 0 en la comprehension.",
        ]),
        "strict_match": True,
    },
    # ── L145 — CSV básico ─────────────────────────────────────────────────────
    {
        "title": "Registro CSV",
        "description": (
            "1. Escribí un CSV en `/tmp/operadores.csv` con estos datos:\n"
            "   `[['callsign','nivel','xp'],['NEXO','7','2500'],['ALFA','3','800']]`\n"
            "2. Leelo con `csv.reader` e imprimí cada fila como lista\n\n"
            "Salida esperada:\n"
            "```\n['callsign', 'nivel', 'xp']\n['NEXO', '7', '2500']\n['ALFA', '3', '800']\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "medium",
        "sector_id": 16,
        "level_order": 155,
        "base_xp_reward": 280,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 200,
        "challenge_type": "python",
        "phase": "fileio",
        "concepts_taught_json": json.dumps(["csv", "csv.writer", "csv.reader", "file_io"]),
        "initial_code": (
            "import csv\n"
            "\n"
            "datos = [['callsign','nivel','xp'],['NEXO','7','2500'],['ALFA','3','800']]\n"
            "\n"
            "with open('/tmp/operadores.csv', 'w', newline='') as f:\n"
            "    escritor = csv.writer(f)\n"
            "    escritor.writerows(datos)\n"
            "\n"
            "with open('/tmp/operadores.csv', 'r') as f:\n"
            "    lector = csv.reader(f)\n"
            "    for fila in lector:\n"
            "        print(fila)\n"
        ),
        "expected_output": "['callsign', 'nivel', 'xp']\n['NEXO', '7', '2500']\n['ALFA', '3', '800']",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "Los datos de operadores del Nexo se intercambian en formato CSV con otros sistemas. "
            "csv.writer y csv.reader manejan automáticamente las comillas y comas dentro de campos."
        ),
        "pedagogical_objective": "Usar csv.writer con writerows() para escribir, csv.reader para iterar filas.",
        "syntax_hint": "csv.writer(f).writerows(lista_de_listas); csv.reader(f) itera filas",
        "theory_content": None,
        "hints_json": json.dumps([
            "csv.writer(f) crea un escritor; .writerows(listas) escribe múltiples filas a la vez.",
            "newline='' en open() es necesario en Windows para evitar líneas en blanco extra.",
            "csv.reader(f) itera el archivo retornando cada fila como lista de strings.",
        ]),
        "strict_match": True,
    },
    # ── L146 — BOSS: CSV DictReader ────────────────────────────────────────────
    {
        "title": "ARCHIVO-01: Procesador CSV",
        "description": (
            "BOSS DEL SECTOR — Procesamiento CSV con DictReader.\n\n"
            "1. Escribí el CSV `/tmp/misiones.csv` con:\n"
            "   ```\ncallsign,tipo,resultado\nNEXO,ALFA,exito\nALFA,BETA,falla\nDAKI,ALFA,exito\nNEXO,BETA,exito\nALFA,ALFA,falla\n```\n"
            "2. Leelo con `csv.DictReader`\n"
            "3. Usá Counter para contar éxitos por callsign\n"
            "4. Imprimí callsign: N_exitos ordenado por callsign\n\n"
            "Salida esperada:\n"
            "```\nALFA: 0\nDAKI: 1\nNEXO: 2\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "hard",
        "sector_id": 16,
        "level_order": 156,
        "base_xp_reward": 650,
        "is_project": False,
        "is_phase_boss": True,
        "telemetry_goal_time": 420,
        "challenge_type": "python",
        "phase": "fileio",
        "concepts_taught_json": json.dumps(["csv", "DictReader", "Counter", "file_io", "filter"]),
        "initial_code": (
            "import csv\n"
            "from collections import Counter\n"
            "\n"
            "contenido = \"\"\"callsign,tipo,resultado\n"
            "NEXO,ALFA,exito\n"
            "ALFA,BETA,falla\n"
            "DAKI,ALFA,exito\n"
            "NEXO,BETA,exito\n"
            "ALFA,ALFA,falla\"\"\"\n"
            "\n"
            "with open('/tmp/misiones.csv', 'w', newline='') as f:\n"
            "    f.write(contenido)\n"
            "\n"
            "exitos = Counter()\n"
            "with open('/tmp/misiones.csv', 'r') as f:\n"
            "    for fila in csv.DictReader(f):\n"
            "        if fila['resultado'] == 'exito':\n"
            "            exitos[fila['callsign']] += 1\n"
            "\n"
            "todos = sorted(set(exitos.keys()) | {'ALFA', 'DAKI', 'NEXO'})\n"
            "for cs in todos:\n"
            "    print(f'{cs}: {exitos.get(cs, 0)}')\n"
        ),
        "expected_output": "ALFA: 0\nDAKI: 1\nNEXO: 2",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El sistema de evaluación del Nexo analiza el historial completo de misiones en CSV. "
            "DAKI necesita identificar a los operadores con mayor tasa de éxito "
            "para las asignaciones de élite."
        ),
        "pedagogical_objective": "Integrar csv.DictReader (filas como dicts) con Counter para análisis filtrado.",
        "syntax_hint": "for fila in csv.DictReader(f): fila['campo'] accede por nombre de columna",
        "theory_content": None,
        "hints_json": json.dumps([
            "csv.DictReader usa la primera fila como cabecera. Cada fila es un dict {columna: valor}.",
            "Counter() sin argumento inicializa vacío; exitos[key] += 1 funciona incluso si la clave no existe.",
            "Para mostrar los 0s (ALFA no tuvo éxitos), usá exitos.get(cs, 0).",
        ]),
        "strict_match": True,
    },
]
