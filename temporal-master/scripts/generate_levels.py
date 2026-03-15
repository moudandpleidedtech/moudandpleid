"""
Generador de Currículo — 20 Niveles del Juego
==============================================

Genera levels.json con los 20 niveles y los inserta en PostgreSQL.

Uso (desde la raíz del proyecto):
    python -m scripts.generate_levels

Fases:
    Niveles  1-5  → Fase 0      : Dron Byte / lógica de movimiento (matrices 5×5)
    Niveles  6-10 → Python Básico: variables, tipos, operaciones matemáticas
    Niveles 11-15 → Control de Flujo: if/elif/else
    Niveles 16-20 → Bucles       : for, while, listas
"""

import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import delete, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.models.challenge import Challenge, DifficultyTier
from app.models.user import User          # noqa: F401 — resuelve FK de UserProgress
from app.models.user_progress import UserProgress  # noqa: F401

# ─── Definición del currículo completo ───────────────────────────────────────

LEVELS = [

    # ══════════════════════════════════════════════════════════════════════════
    # FASE 0 — Niveles 1-5: Lógica pura con el Dron Byte (matrices 5×5)
    # ══════════════════════════════════════════════════════════════════════════

    {
        "level_id": 1,
        "phase": "fase0",
        "title": "Nivel 1 — Protocolo Alpha",
        "lore_description": (
            "El Dron Byte acaba de despertar en el Sector Alpha.\n\n"
            "El camino al Núcleo de Datos está despejado — solo necesitas "
            "guiarlo en línea recta hasta el objetivo.\n\n"
            "Usa mover_derecha() y mover_abajo() para alcanzar el núcleo y "
            "luego recolectar() para completar la misión."
        ),
        "grid_map": [
            [3, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 2],
        ],
        "initial_code": (
            "# Comandos del Dron Byte:\n"
            "#   mover_arriba()     mover_abajo()\n"
            "#   mover_izquierda()  mover_derecha()\n"
            "#   recolectar()\n"
            "\n"
            "# Guia al dron desde (0,0) hasta el nucleo en (4,4)\n"
        ),
        "expected_output": "MISION_COMPLETADA",
        "test_inputs": [],
        "difficulty_tier": DifficultyTier.BEGINNER,
        "base_xp_reward": 50,
        "concepts_taught": ["secuencias", "logica_espacial", "movimiento_lineal"],
    },
    {
        "level_id": 2,
        "phase": "fase0",
        "title": "Nivel 2 — Corredor Beta",
        "lore_description": (
            "Una pared de interferencia bloquea el acceso directo al Núcleo.\n\n"
            "El Dron debe rodear el obstáculo. Analiza el mapa: hay una "
            "barrera vertical en la columna 2 que te impide avanzar en línea recta.\n\n"
            "Encuentra el camino alternativo por debajo de la barrera."
        ),
        "grid_map": [
            [3, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 2],
        ],
        "initial_code": (
            "# Hay una barrera vertical — debes rodearla por debajo\n"
            "# Pista: baja primero, luego cruza la barrera\n"
            "\n"
        ),
        "expected_output": "MISION_COMPLETADA",
        "test_inputs": [],
        "difficulty_tier": DifficultyTier.BEGINNER,
        "base_xp_reward": 80,
        "concepts_taught": ["secuencias", "esquivar_obstaculos", "planificacion_rutas"],
    },
    {
        "level_id": 3,
        "phase": "fase0",
        "title": "Nivel 3 — Zona Restringida",
        "lore_description": (
            "El Sector Gamma está sembrado de zonas de alta radiación.\n\n"
            "Los muros representan campos de radiación que destruirán al Dron "
            "si los toca. Debes encontrar el único camino seguro entre los "
            "obstáculos dispersos.\n\n"
            "Planifica cada movimiento antes de ejecutar."
        ),
        "grid_map": [
            [3, 0, 0, 1, 0],
            [0, 1, 0, 1, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 1, 2],
        ],
        "initial_code": (
            "# Zona minada — cada movimiento cuenta\n"
            "# Celdas con 1 = campo de radiacion = COLISION\n"
            "\n"
        ),
        "expected_output": "MISION_COMPLETADA",
        "test_inputs": [],
        "difficulty_tier": DifficultyTier.BEGINNER,
        "base_xp_reward": 120,
        "concepts_taught": ["secuencias", "planificacion_rutas", "lectura_de_mapas"],
    },
    {
        "level_id": 4,
        "phase": "fase0",
        "title": "Nivel 4 — Laberinto Sigma",
        "lore_description": (
            "El sistema de seguridad del Sector Delta ha activado un laberinto "
            "de paredes electrificadas.\n\n"
            "Solo existe un camino: debes rodear las barreras horizontales que "
            "bloquean el paso. Observa que las paredes forman dos filas casi "
            "completas — cada una con un único hueco.\n\n"
            "Zigzaguea con precisión."
        ),
        "grid_map": [
            [3, 0, 0, 0, 0],
            [1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1],
            [0, 0, 0, 0, 2],
        ],
        "initial_code": (
            "# Barreras horizontales con un hueco cada una\n"
            "# Fila 1: hueco en columna 4  |  Fila 3: hueco en columna 0\n"
            "\n"
        ),
        "expected_output": "MISION_COMPLETADA",
        "test_inputs": [],
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "base_xp_reward": 180,
        "concepts_taught": ["secuencias", "laberintos", "pensamiento_logico"],
    },
    {
        "level_id": 5,
        "phase": "fase0",
        "title": "Nivel 5 — Núcleo Omega",
        "lore_description": (
            "ALERTA: Protocolo de seguridad máxima activado.\n\n"
            "Este es el nivel de acceso al núcleo central del sistema ENIGMA. "
            "El laberinto es denso y no hay margen de error — una sola colisión "
            "reinicia toda la secuencia.\n\n"
            "Solo los arquitectos más precisos llegan hasta aquí. "
            "Este es tu último obstáculo antes de acceder al lenguaje real del sistema."
        ),
        "grid_map": [
            [3, 1, 0, 0, 0],
            [0, 1, 0, 1, 0],
            [0, 0, 0, 1, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 2],
        ],
        "initial_code": (
            "# Laberinto de maxima seguridad\n"
            "# Analiza el mapa cuidadosamente antes de ejecutar\n"
            "\n"
        ),
        "expected_output": "MISION_COMPLETADA",
        "test_inputs": [],
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "base_xp_reward": 250,
        "concepts_taught": ["secuencias", "laberintos_complejos", "precision"],
    },

    # ══════════════════════════════════════════════════════════════════════════
    # PYTHON BÁSICO — Niveles 6-10: Variables, tipos, operaciones
    # ══════════════════════════════════════════════════════════════════════════

    {
        "level_id": 6,
        "phase": "basico",
        "title": "Nivel 6 — Variables: Potencia del Reactor",
        "lore_description": (
            "El reactor del sistema requiere calibración.\n\n"
            "Recibirás dos enteros: la potencia base y el multiplicador de "
            "eficiencia. Tu código debe calcular la potencia total y mostrarla.\n\n"
            "Ejemplo: potencia=120, multiplicador=3 → salida: 360"
        ),
        "grid_map": None,
        "initial_code": (
            "# Lee dos enteros y muestra su producto\n"
            "potencia = int(input())\n"
            "multiplicador = int(input())\n"
            "# Tu código aquí:\n"
        ),
        "expected_output": "360",
        "test_inputs": ["120", "3"],
        "difficulty_tier": DifficultyTier.BEGINNER,
        "base_xp_reward": 100,
        "concepts_taught": ["variables", "int", "input", "operaciones_aritmeticas"],
    },
    {
        "level_id": 7,
        "phase": "basico",
        "title": "Nivel 7 — Strings: Código de Acceso",
        "lore_description": (
            "El sistema de autenticación requiere concatenar fragmentos de código.\n\n"
            "Recibirás dos strings: un prefijo y un sufijo. Únelos con un guión "
            "en medio y muestra el resultado.\n\n"
            "Ejemplo: prefijo='SECTOR', sufijo='7G' → salida: SECTOR-7G"
        ),
        "grid_map": None,
        "initial_code": (
            "prefijo = input()\n"
            "sufijo = input()\n"
            "# Concatena con '-' en el medio y muestra el resultado\n"
        ),
        "expected_output": "SECTOR-7G",
        "test_inputs": ["SECTOR", "7G"],
        "difficulty_tier": DifficultyTier.BEGINNER,
        "base_xp_reward": 100,
        "concepts_taught": ["variables", "strings", "concatenacion"],
    },
    {
        "level_id": 8,
        "phase": "basico",
        "title": "Nivel 8 — Matemáticas: XP Faltante",
        "lore_description": (
            "El motor de progresión necesita calcular cuánto XP le falta a un "
            "agente para subir de nivel.\n\n"
            "Fórmula: XP_siguiente_nivel = (nivel_actual + 1)² × 100\n"
            "Calcula la diferencia entre ese valor y el XP actual del agente.\n\n"
            "Ejemplo: xp=350, nivel=2 → siguiente nivel necesita 900 → falta 550"
        ),
        "grid_map": None,
        "initial_code": (
            "xp_actual = int(input())\n"
            "nivel_actual = int(input())\n"
            "# Calcula: xp_necesario = (nivel_actual + 1) ** 2 * 100\n"
            "# Muestra la diferencia\n"
        ),
        "expected_output": "550",
        "test_inputs": ["350", "2"],
        "difficulty_tier": DifficultyTier.BEGINNER,
        "base_xp_reward": 150,
        "concepts_taught": ["variables", "int", "potencias", "operaciones_aritmeticas"],
    },
    {
        "level_id": 9,
        "phase": "basico",
        "title": "Nivel 9 — Float: Temperatura del Reactor",
        "lore_description": (
            "Los sensores del reactor reportan temperaturas en Celsius. "
            "El sistema interno trabaja en Kelvin.\n\n"
            "Convierte la lectura: Kelvin = Celsius + 273.15\n"
            "Muestra el resultado redondeado a 2 decimales.\n\n"
            "Ejemplo: 36.6 → 309.75"
        ),
        "grid_map": None,
        "initial_code": (
            "celsius = float(input())\n"
            "# Convierte a Kelvin y muestra con 2 decimales\n"
        ),
        "expected_output": "309.75",
        "test_inputs": ["36.6"],
        "difficulty_tier": DifficultyTier.BEGINNER,
        "base_xp_reward": 150,
        "concepts_taught": ["variables", "float", "round", "conversion_tipos"],
    },
    {
        "level_id": 10,
        "phase": "basico",
        "title": "Nivel 10 — f-strings: ID de Agente",
        "lore_description": (
            "El sistema de identificación genera badges para cada agente.\n\n"
            "Recibirás el nombre (string) y el nivel (int). Genera el badge "
            "con este formato exacto: AGENTE {NOMBRE_EN_MAYUSCULAS} | NVL {nivel con 2 dígitos}\n\n"
            "Ejemplo: nombre='neo', nivel=7 → AGENTE NEO | NVL 07"
        ),
        "grid_map": None,
        "initial_code": (
            "nombre = input()\n"
            "nivel = int(input())\n"
            "# Genera el badge: AGENTE {NOMBRE} | NVL {nivel:02d}\n"
            "# Pista: usa .upper() y f-strings con formato {:02d}\n"
        ),
        "expected_output": "AGENTE NEO | NVL 07",
        "test_inputs": ["neo", "7"],
        "difficulty_tier": DifficultyTier.BEGINNER,
        "base_xp_reward": 200,
        "concepts_taught": ["f_strings", "string_methods", "formato_numeros"],
    },

    # ══════════════════════════════════════════════════════════════════════════
    # CONTROL DE FLUJO — Niveles 11-15: if/elif/else
    # ══════════════════════════════════════════════════════════════════════════

    {
        "level_id": 11,
        "phase": "control",
        "title": "Nivel 11 — if/else: Escudo de Radiación",
        "lore_description": (
            "Los sensores de radiación del Sector Gamma están activos.\n\n"
            "Si el nivel de radiación supera 50, el escudo debe activarse "
            "automáticamente. De lo contrario, el sistema permanece en modo seguro.\n\n"
            "Entrada: un entero (nivel de radiación)\n"
            "Salida: 'ESCUDO ACTIVADO' si radiacion > 50, 'NIVEL SEGURO' si no."
        ),
        "grid_map": None,
        "initial_code": (
            "radiacion = int(input())\n"
            "# Si radiacion > 50: muestra 'ESCUDO ACTIVADO'\n"
            "# Si no: muestra 'NIVEL SEGURO'\n"
        ),
        "expected_output": "ESCUDO ACTIVADO",
        "test_inputs": ["75"],
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "base_xp_reward": 250,
        "concepts_taught": ["if_else", "condicionales", "operadores_comparacion"],
    },
    {
        "level_id": 12,
        "phase": "control",
        "title": "Nivel 12 — elif: Clasificación de Energía",
        "lore_description": (
            "El monitor de energía del sistema clasifica el estado del reactor "
            "en tres categorías.\n\n"
            "energía >= 80 → 'OPTIMO'\n"
            "energía >= 40 → 'ESTABLE'\n"
            "energía < 40  → 'CRITICO'\n\n"
            "Entrada: un entero (nivel de energía 0-100)\n"
            "Ejemplo: energia=55 → ESTABLE"
        ),
        "grid_map": None,
        "initial_code": (
            "energia = int(input())\n"
            "# Clasifica el nivel de energia en OPTIMO / ESTABLE / CRITICO\n"
        ),
        "expected_output": "ESTABLE",
        "test_inputs": ["55"],
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "base_xp_reward": 300,
        "concepts_taught": ["if_elif_else", "condicionales_multiples", "rangos"],
    },
    {
        "level_id": 13,
        "phase": "control",
        "title": "Nivel 13 — and: Control de Acceso",
        "lore_description": (
            "El sistema de seguridad verifica dos condiciones simultáneamente: "
            "nivel de autorización Y clave de acceso.\n\n"
            "Solo se concede acceso si nivel >= 5 AND clave == 'ENIGMA'.\n\n"
            "Entrada: nivel (int) y clave (str)\n"
            "Ejemplo: nivel=7, clave='ENIGMA' → ACCESO CONCEDIDO"
        ),
        "grid_map": None,
        "initial_code": (
            "nivel = int(input())\n"
            "clave = input()\n"
            "# Verifica ambas condiciones con 'and'\n"
            "# 'ACCESO CONCEDIDO' o 'ACCESO DENEGADO'\n"
        ),
        "expected_output": "ACCESO CONCEDIDO",
        "test_inputs": ["7", "ENIGMA"],
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "base_xp_reward": 350,
        "concepts_taught": ["operador_and", "condiciones_multiples", "autenticacion"],
    },
    {
        "level_id": 14,
        "phase": "control",
        "title": "Nivel 14 — Métodos string: Análisis de Mensajes",
        "lore_description": (
            "El interceptor de comunicaciones clasifica los mensajes entrantes "
            "según su contenido.\n\n"
            "Si empieza con 'ALERTA' → 'CRITICO'\n"
            "Si tiene más de 10 caracteres → 'LARGO'\n"
            "En otro caso → 'NORMAL'\n\n"
            "Ejemplo: 'ALERTA-SISTEMA' → CRITICO"
        ),
        "grid_map": None,
        "initial_code": (
            "mensaje = input()\n"
            "# Usa startswith() y len() para clasificar\n"
        ),
        "expected_output": "CRITICO",
        "test_inputs": ["ALERTA-SISTEMA"],
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "base_xp_reward": 400,
        "concepts_taught": ["string_methods", "startswith", "len", "if_elif"],
    },
    {
        "level_id": 15,
        "phase": "control",
        "title": "Nivel 15 — Condiciones compuestas: Reactor Seguro",
        "lore_description": (
            "El reactor central opera de forma segura solo cuando AMBOS "
            "parámetros están dentro del rango permitido.\n\n"
            "temperatura < 100 AND presion < 200 → 'REACTOR OK'\n"
            "Si alguno excede el límite → 'REACTOR PELIGRO'\n\n"
            "Ejemplo: temp=85, presion=150 → REACTOR OK"
        ),
        "grid_map": None,
        "initial_code": (
            "temp = int(input())\n"
            "presion = int(input())\n"
            "# Verifica los dos limites simultaneamente\n"
        ),
        "expected_output": "REACTOR OK",
        "test_inputs": ["85", "150"],
        "difficulty_tier": DifficultyTier.INTERMEDIATE,
        "base_xp_reward": 450,
        "concepts_taught": ["condiciones_compuestas", "operador_and", "umbrales"],
    },

    # ══════════════════════════════════════════════════════════════════════════
    # BUCLES — Niveles 16-20: for, while, listas
    # ══════════════════════════════════════════════════════════════════════════

    {
        "level_id": 16,
        "phase": "bucles",
        "title": "Nivel 16 — for: Suma de Registros",
        "lore_description": (
            "Los sensores del sistema reportan N lecturas de energía.\n\n"
            "La primera línea contiene N (cantidad de lecturas). "
            "Las siguientes N líneas contienen un entero cada una.\n"
            "Calcula y muestra la suma total.\n\n"
            "Ejemplo: N=4, valores=10,20,30,40 → 100"
        ),
        "grid_map": None,
        "initial_code": (
            "n = int(input())\n"
            "total = 0\n"
            "# Usa un bucle for range(n) para acumular\n"
            "print(total)\n"
        ),
        "expected_output": "100",
        "test_inputs": ["4", "10", "20", "30", "40"],
        "difficulty_tier": DifficultyTier.ADVANCED,
        "base_xp_reward": 500,
        "concepts_taught": ["for_range", "acumuladores", "input_multiple"],
    },
    {
        "level_id": 17,
        "phase": "bucles",
        "title": "Nivel 17 — for + lista: Pico de Amenaza",
        "lore_description": (
            "El sistema de detección registra N niveles de amenaza y necesita "
            "identificar el pico máximo para activar la respuesta adecuada.\n\n"
            "Lee N enteros y muestra el mayor.\n\n"
            "Ejemplo: N=5, valores=34,78,12,99,56 → 99"
        ),
        "grid_map": None,
        "initial_code": (
            "n = int(input())\n"
            "lecturas = []\n"
            "# Llena la lista con n valores\n"
            "# Muestra el valor maximo\n"
        ),
        "expected_output": "99",
        "test_inputs": ["5", "34", "78", "12", "99", "56"],
        "difficulty_tier": DifficultyTier.ADVANCED,
        "base_xp_reward": 550,
        "concepts_taught": ["for_range", "listas", "append", "max"],
    },
    {
        "level_id": 18,
        "phase": "bucles",
        "title": "Nivel 18 — while: Intentos de Acceso",
        "lore_description": (
            "El sistema registra cuántos intentos tarda en recibir la clave "
            "correcta 'SISTEMA'.\n\n"
            "Usa un bucle while que siga leyendo claves hasta obtener 'SISTEMA'. "
            "Cuenta y muestra el número de intentos totales (incluido el exitoso).\n\n"
            "Ejemplo: intentos=['PRUEBA','FALLO','SISTEMA'] → 3"
        ),
        "grid_map": None,
        "initial_code": (
            "intentos = 0\n"
            "clave = ''\n"
            "# Bucle while: lee hasta que clave == 'SISTEMA'\n"
            "# Cuenta cada intento\n"
            "print(intentos)\n"
        ),
        "expected_output": "3",
        "test_inputs": ["PRUEBA", "FALLO", "SISTEMA"],
        "difficulty_tier": DifficultyTier.ADVANCED,
        "base_xp_reward": 600,
        "concepts_taught": ["while", "break", "contadores", "condicion_salida"],
    },
    {
        "level_id": 19,
        "phase": "bucles",
        "title": "Nivel 19 — for + string: Cifrado de Mensajes",
        "lore_description": (
            "El sistema de comunicaciones transforma los mensajes convirtiendo "
            "todas las letras a mayúsculas pero dejando los demás caracteres intactos.\n\n"
            "Recorre cada carácter del mensaje: si es letra → mayúscula, si no → igual.\n\n"
            "Ejemplo: 'r3actor-7' → R3ACTOR-7"
        ),
        "grid_map": None,
        "initial_code": (
            "texto = input()\n"
            "resultado = ''\n"
            "# Recorre cada caracter\n"
            "# Si es letra: convierte a mayuscula\n"
            "# Si no: mantener igual\n"
            "print(resultado)\n"
        ),
        "expected_output": "R3ACTOR-7",
        "test_inputs": ["r3actor-7"],
        "difficulty_tier": DifficultyTier.ADVANCED,
        "base_xp_reward": 650,
        "concepts_taught": ["for_string", "isalpha", "upper", "concatenacion"],
    },
    {
        "level_id": 20,
        "phase": "bucles",
        "title": "Nivel 20 — Protocolo Final: Promedio del Sistema",
        "lore_description": (
            "El protocolo final del sistema requiere calcular el promedio de N "
            "lecturas de temperatura del núcleo.\n\n"
            "Lee N valores float y calcula su promedio redondeado a 2 decimales.\n\n"
            "Ejemplo: N=4, valores=10.5,20.0,15.5,14.0 → 15.0\n\n"
            "Al completar este nivel, habrás demostrado dominio de los fundamentos. "
            "El sistema ENIGMA te reconocerá como Arquitecto Certificado."
        ),
        "grid_map": None,
        "initial_code": (
            "n = int(input())\n"
            "suma = 0.0\n"
            "# Lee n floats y acumula\n"
            "# Muestra round(suma / n, 2)\n"
        ),
        "expected_output": "15.0",
        "test_inputs": ["4", "10.5", "20.0", "15.5", "14.0"],
        "difficulty_tier": DifficultyTier.ADVANCED,
        "base_xp_reward": 800,
        "concepts_taught": ["for_range", "float", "promedio", "round", "acumuladores"],
    },
]


# ─── Serialización JSON (grid_map y test_inputs como JSON strings) ────────────

def build_json_record(level: dict) -> dict:
    """Convierte un nivel a registro DB-friendly (tipos Python nativos)."""
    return {
        "level_id": level["level_id"],
        "phase": level["phase"],
        "title": level["title"],
        "lore_description": level["lore_description"],
        "grid_map": level["grid_map"],          # lista o None
        "initial_code": level["initial_code"],
        "expected_output": level["expected_output"],
        "test_inputs": level["test_inputs"],    # lista de strings
        "difficulty_tier": level["difficulty_tier"].name,
        "base_xp_reward": level["base_xp_reward"],
        "concepts_taught": level["concepts_taught"],
    }


# ─── Inserción en base de datos ───────────────────────────────────────────────

async def insert_levels(levels_data: list[dict]) -> None:
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with SessionLocal() as session:
        print("Aplicando migraciones de columnas...")
        for stmt in [
            "ALTER TABLE challenges ADD COLUMN IF NOT EXISTS level_order INTEGER",
            "ALTER TABLE challenges ADD COLUMN IF NOT EXISTS phase VARCHAR(20)",
            "ALTER TABLE challenges ADD COLUMN IF NOT EXISTS concepts_taught_json TEXT NOT NULL DEFAULT '[]'",
            "ALTER TABLE challenges ADD COLUMN IF NOT EXISTS grid_map_json TEXT",
            "ALTER TABLE challenges ADD COLUMN IF NOT EXISTS challenge_type VARCHAR(20) NOT NULL DEFAULT 'python'",
        ]:
            await session.execute(text(stmt))
        await session.flush()
        print("    Columnas listas.")

        print("\nLimpiando tablas...")
        await session.execute(delete(UserProgress))
        await session.execute(delete(Challenge))
        await session.flush()
        print("    user_progress → limpia")
        print("    challenges    → limpia")

        print(f"\nInsertando {len(levels_data)} niveles...")
        for level in levels_data:
            is_drone = level["grid_map"] is not None

            challenge = Challenge(
                title=level["title"],
                description=level["lore_description"],
                difficulty_tier=level["difficulty_tier"],
                base_xp_reward=level["base_xp_reward"],
                initial_code=level["initial_code"],
                expected_output=level["expected_output"],
                test_inputs_json=json.dumps(level["test_inputs"]),
                # Campos de currículo
                level_order=level["level_id"],
                phase=level["phase"],
                concepts_taught_json=json.dumps(level["concepts_taught"]),
                grid_map_json=json.dumps(level["grid_map"]) if level["grid_map"] else None,
                challenge_type="drone" if is_drone else "python",
            )
            session.add(challenge)

            phase_label = level["phase"].upper().ljust(8)
            ctype = "dron  " if is_drone else "python"
            print(f"    [{level['level_id']:02d}] {phase_label} | {ctype} | {level['title']}")

        await session.commit()

    await engine.dispose()
    print(f"\nListo — {len(levels_data)} niveles insertados correctamente.")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    # 1) Generar levels.json
    output_path = Path(__file__).resolve().parent.parent / "levels.json"
    records = [build_json_record(lv) for lv in LEVELS]

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    print(f"levels.json generado en: {output_path}")
    print(f"Total niveles: {len(records)}\n")

    # 2) Insertar en DB
    asyncio.run(insert_levels(LEVELS))


if __name__ == "__main__":
    main()
