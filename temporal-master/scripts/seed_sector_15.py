"""
seed_sector_15.py — Sector 15: Módulos Stdlib (niveles 131–140)
===============================================================
Niveles 131–140  |  10 misiones  |  Sector ID = 14

Temática técnica: biblioteca estándar de Python.
math, random, datetime, collections, string, os.path.

Nivel 140 (Boss): análisis de datos con múltiples módulos stdlib.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.models.challenge import Challenge, DifficultyTier  # noqa: F401

SECTOR_15 = [
    # ── L131 — math básico ────────────────────────────────────────────────────
    {
        "title": "El Módulo math",
        "description": (
            "Usá el módulo `math` para resolver tres cálculos:\n\n"
            "1. Raíz cuadrada de 144\n"
            "2. Redondear hacia arriba 7.1\n"
            "3. Imprimir pi con 4 decimales\n\n"
            "Salida esperada:\n"
            "```\n12.0\n8\n3.1416\n```"
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "easy",
        "sector_id": 15,
        "level_order": 141,
        "base_xp_reward": 200,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 120,
        "challenge_type": "python",
        "phase": "stdlib",
        "concepts_taught_json": json.dumps(["math", "sqrt", "ceil", "pi", "import"]),
        "initial_code": (
            "import math\n"
            "\n"
            "print(math.sqrt(144))\n"
            "print(math.ceil(7.1))\n"
            "print(round(math.pi, 4))\n"
        ),
        "expected_output": "12.0\n8\n3.1416",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El módulo math de Python da acceso a funciones matemáticas de alta precisión. "
            "DAKI los usa para cálculos balísticos, trayectorias y análisis de señales."
        ),
        "pedagogical_objective": "Importar math y usar sqrt(), ceil() y la constante pi.",
        "syntax_hint": "import math; math.sqrt(144); math.ceil(7.1); round(math.pi, 4)",
        "theory_content": None,
        "hints_json": json.dumps([
            "math.sqrt(n) retorna la raíz cuadrada como float.",
            "math.ceil(x) redondea hacia ARRIBA al entero más cercano.",
            "math.pi es la constante pi. Usá round(math.pi, 4) para 4 decimales.",
        ]),
        "strict_match": True,
    },
    # ── L132 — math geometría ─────────────────────────────────────────────────
    {
        "title": "Geometría Táctica",
        "description": (
            "Usando `math`, calculá e imprimí:\n\n"
            "1. La hipotenusa de un triángulo con catetos 3 y 4\n"
            "2. El área de un círculo de radio 5 (redondeado a 2 decimales)\n\n"
            "Salida esperada:\n"
            "```\n5.0\n78.54\n```"
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "easy",
        "sector_id": 15,
        "level_order": 142,
        "base_xp_reward": 210,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 150,
        "challenge_type": "python",
        "phase": "stdlib",
        "concepts_taught_json": json.dumps(["math", "hypot", "pi", "round"]),
        "initial_code": (
            "import math\n"
            "\n"
            "# Hipotenusa de triángulo 3-4-?\n"
            "print(math.hypot(3, 4))\n"
            "\n"
            "# Área del círculo: pi * r^2\n"
            "radio = 5\n"
            "print(round(math.pi * radio**2, 2))\n"
        ),
        "expected_output": "5.0\n78.54",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El sistema de navegación de DAKI calcula distancias euclidianas y áreas de cobertura "
            "para determinar el radio de influencia de cada sensor desplegado."
        ),
        "pedagogical_objective": "Usar math.hypot() para distancias euclidianas y math.pi para áreas circulares.",
        "syntax_hint": "math.hypot(a, b) = sqrt(a²+b²); area = math.pi * r**2",
        "theory_content": None,
        "hints_json": json.dumps([
            "math.hypot(3, 4) calcula sqrt(3²+4²) = sqrt(25) = 5.0.",
            "Área del círculo: math.pi * radio**2. Redondeá con round(..., 2).",
        ]),
        "strict_match": True,
    },
    # ── L133 — random básico ──────────────────────────────────────────────────
    {
        "title": "Generador Aleatorio",
        "description": (
            "Usá `random` con semilla 42 para garantizar reproducibilidad:\n\n"
            "1. Generá un entero aleatorio entre 1 y 10\n"
            "2. Elegí un elemento aleatorio de `['ALFA', 'BETA', 'GAMMA', 'DELTA']`\n"
            "3. Generá un float entre 0 y 1 redondeado a 2 decimales\n\n"
            "Con semilla 42, la salida esperada es:\n"
            "```\n1\nGAMMA\n0.65\n```"
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "easy",
        "sector_id": 15,
        "level_order": 143,
        "base_xp_reward": 200,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 150,
        "challenge_type": "python",
        "phase": "stdlib",
        "concepts_taught_json": json.dumps(["random", "seed", "randint", "choice", "random_float"]),
        "initial_code": (
            "import random\n"
            "\n"
            "random.seed(42)\n"
            "print(random.randint(1, 10))\n"
            "print(random.choice(['ALFA', 'BETA', 'GAMMA', 'DELTA']))\n"
            "print(round(random.random(), 2))\n"
        ),
        "expected_output": "1\nGAMMA\n0.65",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El sistema de asignación de misiones de DAKI usa números aleatorios para seleccionar "
            "operadores disponibles. La semilla garantiza que las pruebas sean reproducibles."
        ),
        "pedagogical_objective": "Usar random.seed() para reproducibilidad, randint() para enteros, choice() para elementos.",
        "syntax_hint": "random.seed(42); random.randint(1,10); random.choice(lista); random.random()",
        "theory_content": None,
        "hints_json": json.dumps([
            "random.seed(42) fija la secuencia aleatoria — misma semilla = mismos resultados.",
            "randint(a, b) retorna entero entre a y b (inclusive ambos extremos).",
            "random.random() retorna float entre 0.0 y 1.0.",
        ]),
        "strict_match": True,
    },
    # ── L134 — random avanzado ────────────────────────────────────────────────
    {
        "title": "Muestreo y Mezcla",
        "description": (
            "Con `random.seed(7)` y la lista `[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]`:\n\n"
            "1. Tomá una muestra de 4 elementos (random.sample)\n"
            "2. Imprimí la muestra ordenada ascendentemente\n"
            "3. Mezclá la lista original (random.shuffle) e imprimí los primeros 5\n\n"
            "Salida esperada:\n"
            "```\n[1, 3, 5, 10]\n[2, 9, 6, 4, 7]\n```"
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "easy",
        "sector_id": 15,
        "level_order": 144,
        "base_xp_reward": 210,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 150,
        "challenge_type": "python",
        "phase": "stdlib",
        "concepts_taught_json": json.dumps(["random", "sample", "shuffle", "sort"]),
        "initial_code": (
            "import random\n"
            "\n"
            "random.seed(7)\n"
            "datos = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]\n"
            "\n"
            "muestra = sorted(random.sample(datos, 4))\n"
            "print(muestra)\n"
            "\n"
            "random.shuffle(datos)\n"
            "print(datos[:5])\n"
        ),
        "expected_output": "[1, 3, 5, 10]\n[2, 9, 6, 4, 7]",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "DAKI selecciona equipos de operadores al azar para misiones de alto riesgo. "
            "El muestreo garantiza imparcialidad; la mezcla asegura rotación equitativa."
        ),
        "pedagogical_objective": "Distinguir sample() (sin reemplazo, no modifica) de shuffle() (modifica in-place).",
        "syntax_hint": "random.sample(lista, k) retorna nueva lista; random.shuffle(lista) modifica in-place",
        "theory_content": None,
        "hints_json": json.dumps([
            "random.sample(lista, k) retorna k elementos sin repetición (no modifica la original).",
            "random.shuffle(lista) mezcla la lista in-place (modifica la original).",
            "sorted() ordena la muestra antes de imprimirla.",
        ]),
        "strict_match": True,
    },
    # ── L135 — datetime básico ────────────────────────────────────────────────
    {
        "title": "Fechas y Diferencias",
        "description": (
            "Usando `datetime`:\n\n"
            "1. Creá la fecha `2026-04-10`\n"
            "2. Sumale 30 días con `timedelta`\n"
            "3. Calculá cuántos días faltan desde `2026-01-01` hasta `2026-04-10`\n\n"
            "Salida esperada:\n"
            "```\n2026-05-10\n99\n```"
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "easy",
        "sector_id": 15,
        "level_order": 145,
        "base_xp_reward": 215,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 150,
        "challenge_type": "python",
        "phase": "stdlib",
        "concepts_taught_json": json.dumps(["datetime", "date", "timedelta"]),
        "initial_code": (
            "from datetime import date, timedelta\n"
            "\n"
            "hoy = date(2026, 4, 10)\n"
            "futuro = hoy + timedelta(days=30)\n"
            "print(futuro)\n"
            "\n"
            "inicio = date(2026, 1, 1)\n"
            "dias = (hoy - inicio).days\n"
            "print(dias)\n"
        ),
        "expected_output": "2026-05-10\n99",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El sistema de misiones del Nexo programa operaciones con anticipación. "
            "DAKI calcula fechas de vencimiento y períodos de alerta usando el módulo datetime."
        ),
        "pedagogical_objective": "Usar date() para crear fechas, timedelta() para sumar días, y restar fechas para obtener diferencias.",
        "syntax_hint": "date(año, mes, día); fecha + timedelta(days=n); (fecha2 - fecha1).days",
        "theory_content": None,
        "hints_json": json.dumps([
            "from datetime import date, timedelta importa las clases que necesitás.",
            "timedelta(days=30) crea un intervalo de 30 días que podés sumar a una fecha.",
            "(hoy - inicio) retorna un timedelta; accedé a .days para el número entero.",
        ]),
        "strict_match": True,
    },
    # ── L136 — datetime strftime ──────────────────────────────────────────────
    {
        "title": "Formato de Fechas",
        "description": (
            "Dada la fecha `date(2026, 4, 10)`, imprimila en tres formatos:\n\n"
            "1. `'Viernes 10 de Abril de 2026'` (usando strftime)\n"
            "2. `'10/04/2026'`\n"
            "3. `'2026-04-10'` (ISO)\n\n"
            "Salida esperada:\n"
            "```\nViernes 10 de Abril de 2026\n10/04/2026\n2026-04-10\n```"
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "easy",
        "sector_id": 15,
        "level_order": 146,
        "base_xp_reward": 215,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 150,
        "challenge_type": "python",
        "phase": "stdlib",
        "concepts_taught_json": json.dumps(["datetime", "strftime", "date_format"]),
        "initial_code": (
            "from datetime import date\n"
            "\n"
            "DIAS = ['Lunes','Martes','Miercoles','Jueves','Viernes','Sabado','Domingo']\n"
            "MESES = ['','Enero','Febrero','Marzo','Abril','Mayo','Junio',\n"
            "         'Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']\n"
            "\n"
            "fecha = date(2026, 4, 10)\n"
            "\n"
            "dia_nombre = DIAS[fecha.weekday()]\n"
            "mes_nombre = MESES[fecha.month]\n"
            "print(f'{dia_nombre} {fecha.day} de {mes_nombre} de {fecha.year}')\n"
            "print(fecha.strftime('%d/%m/%Y'))\n"
            "print(fecha.isoformat())\n"
        ),
        "expected_output": "Viernes 10 de Abril de 2026\n10/04/2026\n2026-04-10",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "Los reportes de DAKI deben presentar fechas en múltiples formatos según el destinatario: "
            "legible para humanos, numérico para formularios, ISO para sistemas."
        ),
        "pedagogical_objective": "Usar strftime() para formatear fechas y combinar con listas para nombres en español.",
        "syntax_hint": "fecha.strftime('%d/%m/%Y'); fecha.isoformat(); fecha.weekday() → 0=Lunes",
        "theory_content": None,
        "hints_json": json.dumps([
            "strftime('%d/%m/%Y') da '10/04/2026'. %d=día, %m=mes, %Y=año 4 dígitos.",
            "fecha.weekday() retorna 0 para Lunes ... 4 para Viernes, 6 para Domingo.",
            "isoformat() da el formato YYYY-MM-DD estándar.",
        ]),
        "strict_match": True,
    },
    # ── L137 — collections.Counter ────────────────────────────────────────────
    {
        "title": "Contador de Elementos",
        "description": (
            "Usá `collections.Counter` para analizar la lista de misiones:\n"
            "```python\nmisiones = ['ALFA','BETA','ALFA','GAMMA','BETA','ALFA','DELTA','BETA']\n```\n\n"
            "Imprimí:\n"
            "1. Las 2 misiones más frecuentes (formato: `MISION: N`)\n"
            "2. La cantidad total de misiones únicas\n\n"
            "Salida esperada:\n"
            "```\nALFA: 3\nBETA: 3\nUnicas: 4\n```"
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "easy",
        "sector_id": 15,
        "level_order": 147,
        "base_xp_reward": 220,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 150,
        "challenge_type": "python",
        "phase": "stdlib",
        "concepts_taught_json": json.dumps(["collections", "Counter", "most_common"]),
        "initial_code": (
            "from collections import Counter\n"
            "\n"
            "misiones = ['ALFA','BETA','ALFA','GAMMA','BETA','ALFA','DELTA','BETA']\n"
            "c = Counter(misiones)\n"
            "\n"
            "for mision, count in c.most_common(2):\n"
            "    print(f'{mision}: {count}')\n"
            "\n"
            "print(f'Unicas: {len(c)}')\n"
        ),
        "expected_output": "ALFA: 3\nBETA: 3\nUnicas: 4",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "DAKI registra cada tipo de misión ejecutada. Counter proporciona estadísticas "
            "instantáneas sin escribir loops manuales de conteo."
        ),
        "pedagogical_objective": "Usar Counter() para frecuencias y most_common(n) para los n elementos más frecuentes.",
        "syntax_hint": "Counter(lista).most_common(2) retorna lista de tuplas (elemento, count)",
        "theory_content": None,
        "hints_json": json.dumps([
            "Counter(lista) crea un dict-like con frecuencias de cada elemento.",
            "most_common(n) retorna los n elementos más frecuentes como lista de tuplas.",
            "len(Counter) da el número de elementos únicos.",
        ]),
        "strict_match": True,
    },
    # ── L138 — string module ──────────────────────────────────────────────────
    {
        "title": "Validador de Contraseña Avanzado",
        "description": (
            "Usando el módulo `string`, verificá si una contraseña cumple:\n"
            "- Tiene al menos una letra minúscula\n"
            "- Tiene al menos una letra mayúscula\n"
            "- Tiene al menos un dígito\n"
            "- Tiene al menos un símbolo de `string.punctuation`\n\n"
            "Imprimí True o False para cada criterio.\n\n"
            "Contraseña: `'D@ki2026!'`\n\n"
            "Salida esperada:\n"
            "```\nTrue\nTrue\nTrue\nTrue\n```"
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "easy",
        "sector_id": 15,
        "level_order": 148,
        "base_xp_reward": 215,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 150,
        "challenge_type": "python",
        "phase": "stdlib",
        "concepts_taught_json": json.dumps(["string_module", "ascii_lowercase", "digits", "any"]),
        "initial_code": (
            "import string\n"
            "\n"
            "pwd = 'D@ki2026!'\n"
            "\n"
            "print(any(c in string.ascii_lowercase for c in pwd))\n"
            "print(any(c in string.ascii_uppercase for c in pwd))\n"
            "print(any(c in string.digits for c in pwd))\n"
            "print(any(c in string.punctuation for c in pwd))\n"
        ),
        "expected_output": "True\nTrue\nTrue\nTrue",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El módulo string de Python contiene conjuntos de caracteres predefinidos. "
            "DAKI los usa para validar sin escribir 'abcdefg...' a mano."
        ),
        "pedagogical_objective": "Usar string.ascii_lowercase, ascii_uppercase, digits y punctuation con any().",
        "syntax_hint": "string.ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'; string.digits = '0123456789'",
        "theory_content": None,
        "hints_json": json.dumps([
            "import string da acceso a string.ascii_lowercase, string.ascii_uppercase, string.digits, string.punctuation.",
            "any(c in string.digits for c in pwd) verifica si hay al menos un dígito.",
        ]),
        "strict_match": True,
    },
    # ── L139 — os.path ────────────────────────────────────────────────────────
    {
        "title": "Rutas del Sistema",
        "description": (
            "Usando `os.path`, analizá la ruta `/nexo/datos/operadores/informe.csv`:\n\n"
            "1. Nombre del archivo (sin directorio)\n"
            "2. Directorio contenedor\n"
            "3. Nombre sin extensión\n"
            "4. Extensión\n"
            "5. Ruta unida: directorio + 'backup' + nombre\n\n"
            "Salida esperada:\n"
            "```\ninforme.csv\n/nexo/datos/operadores\ninforme\n.csv\n/nexo/datos/operadores/backup/informe.csv\n```"
        ),
        "difficulty_tier": DifficultyTier.BEGINNER,
        "difficulty": "easy",
        "sector_id": 15,
        "level_order": 149,
        "base_xp_reward": 220,
        "is_project": False,
        "is_phase_boss": False,
        "telemetry_goal_time": 150,
        "challenge_type": "python",
        "phase": "stdlib",
        "concepts_taught_json": json.dumps(["os.path", "basename", "dirname", "splitext", "join"]),
        "initial_code": (
            "import os.path\n"
            "\n"
            "ruta = '/nexo/datos/operadores/informe.csv'\n"
            "\n"
            "print(os.path.basename(ruta))\n"
            "print(os.path.dirname(ruta))\n"
            "nombre, ext = os.path.splitext(os.path.basename(ruta))\n"
            "print(nombre)\n"
            "print(ext)\n"
            "print(os.path.join(os.path.dirname(ruta), 'backup', os.path.basename(ruta)))\n"
        ),
        "expected_output": "informe.csv\n/nexo/datos/operadores\ninforme\n.csv\n/nexo/datos/operadores/backup/informe.csv",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "DAKI administra miles de archivos de datos. os.path garantiza que las rutas "
            "funcionen en cualquier sistema operativo sin importar las diferencias de separadores."
        ),
        "pedagogical_objective": "Usar basename, dirname, splitext y join de os.path para manipular rutas portables.",
        "syntax_hint": "os.path.basename, dirname, splitext, join — todas operan con strings de rutas",
        "theory_content": None,
        "hints_json": json.dumps([
            "basename('/a/b/c.txt') → 'c.txt'; dirname('/a/b/c.txt') → '/a/b'.",
            "splitext('informe.csv') → ('informe', '.csv') — retorna tupla (nombre, extensión).",
            "os.path.join(dir, 'backup', archivo) construye la ruta uniendo componentes.",
        ]),
        "strict_match": True,
    },
    # ── L140 — BOSS: Inspector de Datos ───────────────────────────────────────
    {
        "title": "MODULO-01: El Inspector de Datos",
        "description": (
            "BOSS DEL SECTOR — Análisis multi-módulo.\n\n"
            "Dado el texto de registros:\n"
            "```\n'nexo alfa nexo beta gamma nexo alfa beta nexo gamma'\n```\n\n"
            "1. Usá Counter para contar frecuencias\n"
            "2. Imprimí el total de palabras y palabras únicas\n"
            "3. Calculá la media de frecuencias (redondeada a 1 decimal)\n"
            "4. Imprimí las palabras con frecuencia mayor a la media, ordenadas\n\n"
            "Salida esperada:\n"
            "```\nTotal: 10 | Unicas: 4\nMedia: 2.5\nSobre la media: ['nexo']\n```"
        ),
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "difficulty": "hard",
        "sector_id": 15,
        "level_order": 150,
        "base_xp_reward": 600,
        "is_project": False,
        "is_phase_boss": True,
        "telemetry_goal_time": 360,
        "challenge_type": "python",
        "phase": "stdlib",
        "concepts_taught_json": json.dumps(["Counter", "collections", "round", "sorted", "filter"]),
        "initial_code": (
            "from collections import Counter\n"
            "\n"
            "texto = 'nexo alfa nexo beta gamma nexo alfa beta nexo gamma'\n"
            "palabras = texto.split()\n"
            "c = Counter(palabras)\n"
            "\n"
            "total = len(palabras)\n"
            "unicas = len(c)\n"
            "print(f'Total: {total} | Unicas: {unicas}')\n"
            "\n"
            "media = round(total / unicas, 1)\n"
            "print(f'Media: {media}')\n"
            "\n"
            "sobre = sorted(p for p, freq in c.items() if freq > media)\n"
            "print(f'Sobre la media: {sobre}')\n"
        ),
        "expected_output": "Total: 10 | Unicas: 4\nMedia: 2.5\nSobre la media: ['nexo']",
        "test_inputs_json": json.dumps([]),
        "lore_briefing": (
            "El sistema de inteligencia del Nexo procesa transmisiones interceptadas. "
            "DAKI debe identificar las palabras clave con frecuencia anormalmente alta — "
            "los términos sobre la media son indicadores de comunicaciones críticas."
        ),
        "pedagogical_objective": "Integrar Counter con estadística básica (media) y filtrado por condición.",
        "syntax_hint": "media = total / len(c); [p for p, freq in c.items() if freq > media]",
        "theory_content": None,
        "hints_json": json.dumps([
            "La media de frecuencias es total_palabras / palabras_unicas.",
            "Filtrá c.items() con if freq > media para obtener palabras sobre la media.",
            "sorted() para ordenar el resultado — aquí solo hay uno pero el código debe ser general.",
        ]),
        "strict_match": True,
    },
]
