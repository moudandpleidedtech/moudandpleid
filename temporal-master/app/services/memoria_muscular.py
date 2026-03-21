"""
memoria_muscular.py — Protocolo de Memoria Muscular (Spaced Repetition adaptativo)

Detecta degradación de conceptos fundamentales mediante tres señales:

  Señal A — ConceptMastery.needs_reinforcement
            La señal canónica: el motor de gamificación la actualiza cada vez
            que el usuario completa un nivel. Si el mastery_score bajó de 40
            por completar con demasiados intentos/pistas, needs_reinforcement=True.

  Señal B — Densidad de errores en UserMetric.syntax_errors_log
            Analiza los últimos N errores cometidos en challenges del sector
            actual. Mapea tipos de error (SyntaxError, IndentationError, etc.)
            a conceptos sospechosos usando la tabla de correlaciones.

  Señal C — Tiempo sin practicar el concepto
            Si ConceptMastery.updated_at es > DECAY_DAYS días atrás y el
            mastery_score está en la zona de peligro (< 60), el concepto
            se marca como candidato para repaso.

Las tres señales se combinan en un score de degradación por concepto.
El concepto con el score más alto (y que pertenece a un sector anterior al
actual) dispara la intercepción.

────────────────────────────────────────────────────────────────────────────────
Función principal pública:
  await verificar_intercepcion(db, user_id, challenge) → InterceptResult

────────────────────────────────────────────────────────────────────────────────
"""

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Optional
import random

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.challenge import Challenge
from app.models.concept_mastery import ConceptMastery
from app.models.daki_interception import DakiInterception
from app.models.user_metrics import UserMetric


# ─── Constantes de configuración ─────────────────────────────────────────────

# Un concepto con mastery_score por debajo de este umbral y
# que provino de un sector anterior al actual dispara la intercepción
_MASTERY_THRESHOLD_HARD = 40.0     # needs_reinforcement flag
_MASTERY_THRESHOLD_SOFT = 60.0     # zona de peligro (Señal C)

# Días sin práctica para activar la Señal C
_DECAY_DAYS = 7

# Errores en el log del sector actual para activar la Señal B
_ERROR_COUNT_THRESHOLD = 5

# No volver a interceptar el mismo concepto antes de este número de horas
# (evita que el sistema sea molesto)
_REINTERCEPT_COOLDOWN_HOURS = 6

# ─── Correlación error → concepto(s) sospechoso(s) ───────────────────────────
#
# Cuando el sandbox reporta un tipo de error en un challenge, este mapa
# sugiere qué conceptos previos podrían estar olvidados.
# Es heurístico: un SyntaxError puede venir de cualquier concepto, pero
# los más frecuentes en estudiantes son bucles y condicionales.

_ERROR_CONCEPT_CORRELATION: dict[str, list[str]] = {
    "SyntaxError":       ["for", "while", "if", "elif", "def", "class", "strings"],
    "IndentationError":  ["for", "while", "if", "def"],
    "NameError":         ["variables", "for", "def", "functions"],
    "TypeError":         ["type conversion", "arithmetic", "int", "str", "float"],
    "ValueError":        ["type conversion", "input", "int", "float"],
    "AttributeError":    ["strings", "list", "dict"],
    "IndexError":        ["list", "for", "range"],
    "KeyError":          ["dict"],
    "ZeroDivisionError": ["arithmetic", "operators"],
    "RecursionError":    ["def", "recursion"],
}


# ─────────────────────────────────────────────────────────────────────────────
# Estructuras de datos
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class ConceptoDebil:
    """Concepto identificado como degradado con su score de urgencia."""
    nombre: str                    # ej. "for", "if", "variables"
    sector_ensenado: int           # sector donde se enseñó por primera vez
    mastery_score: float           # 0.0 – 100.0 (más bajo = más urgente)
    score_degradacion: float       # puntuación compuesta [0..1] (más alto = intervenir)
    errores_recientes: int = 0     # errores del tipo correlacionado en el sector actual
    dias_sin_practicar: int = 0


@dataclass
class MisionFlash:
    """Micro-Misión de repaso generada al vuelo. No vive en la tabla challenges."""
    concept_name: str
    title: str
    description: str
    lore_briefing: str
    initial_code: str
    expected_output: str
    hints: list[str] = field(default_factory=list)
    difficulty: str = "easy"
    estimated_lines: int = 3       # líneas de código esperadas para resolver


@dataclass
class InterceptResult:
    """Resultado del chequeo de intercepción para un challenge + usuario."""
    intercept: bool
    interception_id: Optional[uuid.UUID] = None
    concepto: Optional[ConceptoDebil] = None
    mision: Optional[MisionFlash] = None
    daki_message: str = ""


# ─────────────────────────────────────────────────────────────────────────────
# Catálogo de Plantillas de Micro-Misiones
# ─────────────────────────────────────────────────────────────────────────────
#
# Cada concepto tiene al menos 2 plantillas distintas para variedad.
# Las misiones son deliberadamente cortas (3-5 líneas de solución)
# y temáticamente ambientadas en el universo DAKI EdTech.

_PLANTILLAS: dict[str, list[dict]] = {

    "for": [
        {
            "title": "Rastreo Perimetral [Repaso]",
            "description": (
                "Los sensores de DAKI detectaron 4 anomalías en el perímetro. "
                "Usa un bucle for para imprimirlas una por una."
            ),
            "lore": (
                "Registro de incursión anterior:\n"
                "«DAKI escaneó el perímetro. 4 señales calientes. "
                "El bucle no cerró. Las anomalías siguen activas.»"
            ),
            "initial_code": (
                'anomalias = ["Glitch-A", "Glitch-B", "Glitch-C", "Glitch-D"]\n'
                "# Imprime cada anomalía usando un bucle for\n"
            ),
            "expected_output": "Glitch-A\nGlitch-B\nGlitch-C\nGlitch-D",
            "hints": [
                "Usa `for item in lista:` para recorrer la lista.",
                "Dentro del bucle, `print(item)` imprime el elemento actual.",
                "La solución es:\nfor a in anomalias:\n    print(a)",
            ],
        },
        {
            "title": "Secuencia de Inicialización [Repaso]",
            "description": (
                "El núcleo de DAKI necesita inicializar sus módulos del 1 al 5. "
                "Usa range() para generar la secuencia."
            ),
            "lore": (
                "«Secuencia de arranque interrumpida. "
                "El contador no completó su ciclo. Reinicializa los 5 módulos.»"
            ),
            "initial_code": "# Imprime los números del 1 al 5 usando for y range()\n",
            "expected_output": "1\n2\n3\n4\n5",
            "hints": [
                "range(1, 6) genera los números del 1 al 5.",
                "Combínalo con un for: `for n in range(1, 6):`",
                "La solución es:\nfor n in range(1, 6):\n    print(n)",
            ],
        },
    ],

    "while": [
        {
            "title": "Bucle de Vigilancia [Repaso]",
            "description": (
                "El sistema de vigilancia debe contar mientras el nivel de amenaza "
                "sea menor a 3. Imprime cada nivel comenzando en 0."
            ),
            "lore": (
                "«Protocolo de alerta activo. "
                "El bucle while no ejecutó el conteo correcto. Recalibra.»"
            ),
            "initial_code": (
                "nivel = 0\n"
                "# Usa while para imprimir nivel mientras sea menor a 3\n"
                "# Incrementa nivel en cada iteración\n"
            ),
            "expected_output": "0\n1\n2",
            "hints": [
                "La condición del while es `nivel < 3`.",
                "Dentro del bucle: imprime nivel y luego haz `nivel += 1`.",
                "La solución es:\nwhile nivel < 3:\n    print(nivel)\n    nivel += 1",
            ],
        },
    ],

    "if": [
        {
            "title": "Verificación de Acceso [Repaso]",
            "description": (
                "El escáner de seguridad verifica el nivel de autorización. "
                "Si es mayor o igual a 5, concede acceso; si no, lo deniega."
            ),
            "lore": (
                "«Intento de acceso registrado. "
                "La lógica condicional falló. El Operador quedó fuera del nexo.»"
            ),
            "initial_code": (
                "nivel_autorizacion = 7\n"
                "# Si nivel_autorizacion >= 5 imprime ACCESO CONCEDIDO\n"
                "# Si no, imprime ACCESO DENEGADO\n"
            ),
            "expected_output": "ACCESO CONCEDIDO",
            "hints": [
                "Usa `if nivel_autorizacion >= 5:`",
                "La cláusula `else:` maneja el caso contrario.",
                "La solución es:\nif nivel_autorizacion >= 5:\n    print('ACCESO CONCEDIDO')\nelse:\n    print('ACCESO DENEGADO')",
            ],
        },
        {
            "title": "Clasificador de Señales [Repaso]",
            "description": (
                "DAKI necesita clasificar una señal. "
                "Si la intensidad es mayor a 50 es 'CRITICA', si es igual es 'LIMITE', si no es 'NORMAL'."
            ),
            "lore": "«Análisis de señal incompleto. La clasificación quedó en null.»",
            "initial_code": (
                "intensidad = 50\n"
                "# Clasifica: > 50 → CRITICA, == 50 → LIMITE, < 50 → NORMAL\n"
            ),
            "expected_output": "LIMITE",
            "hints": [
                "Necesitas if/elif/else para tres casos.",
                "`elif intensidad == 50:` maneja el caso exacto.",
                "La solución es:\nif intensidad > 50:\n    print('CRITICA')\nelif intensidad == 50:\n    print('LIMITE')\nelse:\n    print('NORMAL')",
            ],
        },
    ],

    "elif": [
        {
            "title": "Protocolo de Amenaza [Repaso]",
            "description": (
                "Clasifica el nivel de amenaza: "
                "1=BAJO, 2=MODERADO, 3=ALTO, otro=DESCONOCIDO."
            ),
            "lore": "«El clasificador de amenazas retornó un estado indefinido.»",
            "initial_code": (
                "amenaza = 2\n"
                "# Clasifica el nivel de amenaza usando if/elif/else\n"
            ),
            "expected_output": "MODERADO",
            "hints": [
                "Usa `if amenaza == 1:` para el primer caso.",
                "Añade `elif amenaza == 2:` y `elif amenaza == 3:`.",
                "La solución usa tres elif y un else final para DESCONOCIDO.",
            ],
        },
    ],

    "variables": [
        {
            "title": "Registro de Identidad [Repaso]",
            "description": (
                "Crea las variables `nombre` y `sector` con los valores indicados, "
                "luego imprímelas en líneas separadas."
            ),
            "lore": (
                "«Registro de identidad del Operador borrado. "
                "Las variables no fueron asignadas correctamente.»"
            ),
            "initial_code": (
                '# Asigna: nombre = "DAKI", sector = 4\n'
                "# Imprime nombre en una línea y sector en otra\n"
            ),
            "expected_output": "DAKI\n4",
            "hints": [
                'Usa `nombre = "DAKI"` para asignar el string.',
                "`sector = 4` asigna el entero.",
                "La solución es:\nnombre = 'DAKI'\nsector = 4\nprint(nombre)\nprint(sector)",
            ],
        },
    ],

    "def": [
        {
            "title": "Módulo de Saludo [Repaso]",
            "description": (
                "Define una función `saludar(nombre)` que imprima 'Hola, [nombre]!'. "
                "Luego llámala con el argumento 'Operador'."
            ),
            "lore": "«El módulo de saludo no está definido. El nexo no puede inicializar el protocolo.»",
            "initial_code": (
                "# Define la función saludar(nombre)\n"
                "# Llámala con 'Operador'\n"
            ),
            "expected_output": "Hola, Operador!",
            "hints": [
                "Usa `def saludar(nombre):` para definir la función.",
                "Dentro usa `print(f'Hola, {nombre}!')`.",
                "La solución es:\ndef saludar(nombre):\n    print(f'Hola, {nombre}!')\nsaludar('Operador')",
            ],
        },
    ],

    "strings": [
        {
            "title": "Concatenación de Datos [Repaso]",
            "description": (
                "Une las dos cadenas con un espacio entre ellas e imprímelas como una sola línea."
            ),
            "lore": "«Transmisión fragmentada. Los strings llegaron separados y el decoder falló.»",
            "initial_code": (
                'parte_a = "NEXO"\n'
                'parte_b = "ACTIVO"\n'
                "# Imprime parte_a y parte_b unidos con un espacio\n"
            ),
            "expected_output": "NEXO ACTIVO",
            "hints": [
                "Puedes usar el operador `+` para unir strings.",
                "`parte_a + ' ' + parte_b` da el resultado deseado.",
                "La solución es:\nprint(parte_a + ' ' + parte_b)",
            ],
        },
    ],

    "f-strings": [
        {
            "title": "Reporte de Estado [Repaso]",
            "description": (
                "Usa una f-string para imprimir el mensaje exacto: "
                "'Operador Nexus en sector 3'."
            ),
            "lore": "«El módulo de reporte devolvió None. La f-string no fue construida.»",
            "initial_code": (
                'operador = "Nexus"\n'
                "sector = 3\n"
                "# Imprime: Operador Nexus en sector 3 usando una f-string\n"
            ),
            "expected_output": "Operador Nexus en sector 3",
            "hints": [
                "Las f-strings comienzan con `f` antes de las comillas.",
                'Usa `{operador}` y `{sector}` dentro de la f-string.',
                "La solución es:\nprint(f'Operador {operador} en sector {sector}')",
            ],
        },
    ],

    "input": [
        {
            "title": "Captura de ID [Repaso]",
            "description": (
                "Lee el nombre del Operador con input() e imprímelo precedido de 'ID: '."
            ),
            "lore": "«El buffer de entrada quedó vacío. El sistema no capturó el ID del Operador.»",
            "initial_code": (
                "# Lee el nombre con input() y guárdalo en una variable\n"
                "# Imprime: ID: [nombre]\n"
            ),
            "expected_output": "ID: DAKI",
            "hints": [
                "Usa `nombre = input()` para leer la entrada.",
                'Luego `print("ID: " + nombre)` o una f-string.',
                "La solución es:\nnombre = input()\nprint('ID: ' + nombre)",
            ],
        },
    ],

    "arithmetic": [
        {
            "title": "Cálculo de Energía [Repaso]",
            "description": (
                "Calcula la energía total: potencia × tiempo. "
                "potencia = 12, tiempo = 5. Imprime el resultado."
            ),
            "lore": "«El módulo de energía retornó 0. La multiplicación no fue ejecutada.»",
            "initial_code": (
                "potencia = 12\n"
                "tiempo = 5\n"
                "# Calcula la energía (potencia * tiempo) e imprímela\n"
            ),
            "expected_output": "60",
            "hints": [
                "La multiplicación en Python usa `*`.",
                "`energia = potencia * tiempo` guarda el resultado.",
                "La solución es:\nenergia = potencia * tiempo\nprint(energia)",
            ],
        },
    ],

    "type conversion": [
        {
            "title": "Conversión de Señal [Repaso]",
            "description": (
                "Convierte el string '42' a entero, súmale 8 e imprime el resultado."
            ),
            "lore": "«Error de tipos. El decodificador recibió un string donde esperaba un int.»",
            "initial_code": (
                'dato = "42"\n'
                "# Convierte dato a int, súmale 8 e imprime el resultado\n"
            ),
            "expected_output": "50",
            "hints": [
                "Usa `int(dato)` para convertir el string a entero.",
                "`int(dato) + 8` da el resultado.",
                "La solución es:\nprint(int(dato) + 8)",
            ],
        },
    ],

    "list": [
        {
            "title": "Inventario del Nexo [Repaso]",
            "description": (
                "Crea una lista con 3 ítems: 'Core', 'Módulo', 'Cable'. "
                "Imprime el segundo elemento."
            ),
            "lore": "«El sistema de inventario accedió al índice incorrecto. Ítem no encontrado.»",
            "initial_code": (
                "# Crea la lista inventario con: 'Core', 'Módulo', 'Cable'\n"
                "# Imprime el segundo elemento\n"
            ),
            "expected_output": "Módulo",
            "hints": [
                "Los índices en Python comienzan en 0.",
                "El segundo elemento tiene índice 1: `inventario[1]`.",
                "La solución es:\ninventario = ['Core', 'Módulo', 'Cable']\nprint(inventario[1])",
            ],
        },
    ],

    "dict": [
        {
            "title": "Tabla de Registros [Repaso]",
            "description": (
                "Crea un diccionario con la clave 'operador' y valor 'DAKI'. "
                "Imprime el valor accedido por esa clave."
            ),
            "lore": "«La tabla de registros devolvió KeyError. La clave no fue encontrada.»",
            "initial_code": (
                "# Crea el diccionario registro con clave 'operador' y valor 'DAKI'\n"
                "# Imprime el valor de la clave 'operador'\n"
            ),
            "expected_output": "DAKI",
            "hints": [
                "Un diccionario se crea con `{clave: valor}`.",
                "Accede al valor con `registro['operador']`.",
                "La solución es:\nregistro = {'operador': 'DAKI'}\nprint(registro['operador'])",
            ],
        },
    ],
}

# Plantilla genérica para conceptos sin plantilla explícita
_PLANTILLA_GENERICA: dict = {
    "title": "Ejercicio Táctico de Repaso [Repaso]",
    "description": (
        "DAKI detectó degradación en tu dominio de este concepto. "
        "Completa el siguiente ejercicio para recalibrar tus sistemas."
    ),
    "lore": (
        "«Degradación detectada. Ejercicio de recalibración iniciado. "
        "El Operador debe demostrar dominio básico antes de continuar.»"
    ),
    "initial_code": "# Escribe tu código aquí\nprint('Nexo calibrado')\n",
    "expected_output": "Nexo calibrado",
    "hints": [
        "El código debe imprimir exactamente 'Nexo calibrado'.",
        "Usa print() con el string correcto.",
        "La solución es:\nprint('Nexo calibrado')",
    ],
}


# ─────────────────────────────────────────────────────────────────────────────
# Mensaje narrativo de DAKI
# ─────────────────────────────────────────────────────────────────────────────

_DAKI_INTERCEPT_MESSAGES = [
    (
        "Operador, tus últimos escaneos muestran degradación en tu manejo de [{concepto}]. "
        "Antes de abrir la siguiente puerta, calibremos tus sistemas con este ejercicio táctico."
    ),
    (
        "[{concepto}] — señal degradada detectada. "
        "El Nexo no permite el avance hasta que recalibremos este módulo contigo. "
        "Completa la Micro-Misión para continuar."
    ),
    (
        "DAKI detecta una anomalía en tu matriz cognitiva: [{concepto}] "
        "muestra interferencia. Una sesión corta de recalibración "
        "restaurará tu rendimiento óptimo. El nexo espera."
    ),
]


def _construir_mensaje_daki(concepto: str) -> str:
    """Elige un mensaje narrativo al azar e inserta el nombre del concepto."""
    template = random.choice(_DAKI_INTERCEPT_MESSAGES)
    return template.replace("{concepto}", concepto.upper())


# ─────────────────────────────────────────────────────────────────────────────
# Generación de Micro-Misión
# ─────────────────────────────────────────────────────────────────────────────

def generar_mision_flash(concepto_debil: ConceptoDebil) -> MisionFlash:
    """
    Ensambla una Micro-Misión de repaso para el concepto débil del Operador.

    El catálogo `_PLANTILLAS` contiene entre 1 y 3 ejercicios por concepto.
    Se elige uno al azar para dar variedad si la misión se repite.

    Args:
        concepto_debil: El concepto identificado como degradado.

    Returns:
        Un objeto MisionFlash listo para serializar y enviar al frontend.
    """
    plantillas = _PLANTILLAS.get(concepto_debil.nombre)
    if plantillas:
        plantilla = random.choice(plantillas)
    else:
        plantilla = _PLANTILLA_GENERICA

    return MisionFlash(
        concept_name=concepto_debil.nombre,
        title=plantilla["title"],
        description=plantilla["description"],
        lore_briefing=plantilla.get("lore", ""),
        initial_code=plantilla["initial_code"],
        expected_output=plantilla["expected_output"],
        hints=plantilla.get("hints", []),
        difficulty="easy",
        estimated_lines=plantilla.get("estimated_lines", 3),
    )


# ─────────────────────────────────────────────────────────────────────────────
# Análisis de degradación
# ─────────────────────────────────────────────────────────────────────────────

async def analizar_degradacion(
    db: AsyncSession,
    user_id: uuid.UUID,
    sector_actual: int,
) -> list[ConceptoDebil]:
    """
    Identifica los conceptos degradados del Operador que provienen de sectores
    ANTERIORES al sector_actual.

    Combina las tres señales:
      A) ConceptMastery.needs_reinforcement  → peso 0.5
      B) Densidad de errores en sector actual → peso 0.3
      C) Días sin practicar (decay)          → peso 0.2

    Returns:
        Lista ordenada de ConceptoDebil (más urgente primero).
        Lista vacía si no hay degradación detectable.
    """

    # ── Señal A: Conceptos marcados para refuerzo ─────────────────────────────
    mastery_result = await db.execute(
        select(ConceptMastery).where(
            ConceptMastery.user_id == user_id,
        )
    )
    all_mastery: list[ConceptMastery] = list(mastery_result.scalars().all())

    if not all_mastery:
        return []

    # ── Obtiene los challenges de sectores ANTERIORES para saber dónde se enseñó
    #    cada concepto (necesitamos sector_id < sector_actual)
    from app.models.challenge import Challenge as ChallengeModel  # local import
    challenges_result = await db.execute(
        select(ChallengeModel).where(
            ChallengeModel.sector_id < sector_actual,
            ChallengeModel.sector_id.isnot(None),
        )
    )
    prev_challenges: list[ChallengeModel] = list(challenges_result.scalars().all())

    # Mapea concepto → sector más temprano donde se enseñó
    concept_to_sector: dict[str, int] = {}
    for ch in prev_challenges:
        try:
            concepts = json.loads(ch.concepts_taught_json or "[]")
        except (json.JSONDecodeError, TypeError):
            concepts = []
        for c in concepts:
            c_lower = c.lower()
            if c_lower not in concept_to_sector:
                concept_to_sector[c_lower] = ch.sector_id
            else:
                # Toma el sector más temprano
                concept_to_sector[c_lower] = min(concept_to_sector[c_lower], ch.sector_id)

    # ── Señal B: Errores recientes en el sector actual ────────────────────────
    current_sector_challenges_result = await db.execute(
        select(ChallengeModel).where(
            ChallengeModel.sector_id == sector_actual,
        )
    )
    current_challenges = list(current_sector_challenges_result.scalars().all())
    current_ids = [ch.id for ch in current_challenges]

    # Cuenta errores por tipo en el sector actual
    error_frequency: dict[str, int] = {}   # concepto → nº de errores correlacionados
    if current_ids:
        metrics_result = await db.execute(
            select(UserMetric).where(
                UserMetric.user_id == user_id,
                UserMetric.challenge_id.in_(current_ids),
            )
        )
        for metric in metrics_result.scalars().all():
            try:
                errors: list[str] = json.loads(metric.syntax_errors_log or "[]")
            except (json.JSONDecodeError, TypeError):
                errors = []
            for error_type in errors:
                for related_concept in _ERROR_CONCEPT_CORRELATION.get(error_type, []):
                    error_frequency[related_concept] = (
                        error_frequency.get(related_concept, 0) + 1
                    )

    # ── Señal C: Decay por tiempo sin practicar ───────────────────────────────
    now = datetime.now(timezone.utc)
    decay_threshold = now - timedelta(days=_DECAY_DAYS)

    # ── Combina señales en score de degradación ───────────────────────────────
    conceptos_debiles: list[ConceptoDebil] = []

    for mastery in all_mastery:
        concept = mastery.concept_name.lower()

        # Solo nos interesan conceptos enseñados en sectores anteriores
        if concept not in concept_to_sector:
            continue

        # ── Señal A ───────────────────────────────────────────────────────────
        score_a = 0.0
        if mastery.needs_reinforcement:
            # Normaliza: cuanto más bajo el mastery_score, mayor urgencia
            score_a = 1.0 - (mastery.mastery_score / _MASTERY_THRESHOLD_HARD)
            score_a = max(0.0, min(1.0, score_a))
        elif mastery.mastery_score < _MASTERY_THRESHOLD_SOFT:
            score_a = 0.4 * (1.0 - mastery.mastery_score / _MASTERY_THRESHOLD_SOFT)

        # ── Señal B ───────────────────────────────────────────────────────────
        errores = error_frequency.get(concept, 0)
        score_b = min(1.0, errores / _ERROR_COUNT_THRESHOLD) if errores > 0 else 0.0

        # ── Señal C ───────────────────────────────────────────────────────────
        score_c = 0.0
        if mastery.mastery_score < _MASTERY_THRESHOLD_SOFT:
            updated = mastery.updated_at
            if updated.tzinfo is None:
                updated = updated.replace(tzinfo=timezone.utc)
            if updated < decay_threshold:
                days_stale = (now - updated).days
                score_c = min(1.0, days_stale / (3 * _DECAY_DAYS))

        # Score combinado
        score_total = 0.5 * score_a + 0.3 * score_b + 0.2 * score_c

        # Solo añade si hay señal real de degradación
        if score_total > 0.1 or (mastery.needs_reinforcement and concept in concept_to_sector):
            conceptos_debiles.append(ConceptoDebil(
                nombre=concept,
                sector_ensenado=concept_to_sector[concept],
                mastery_score=mastery.mastery_score,
                score_degradacion=score_total,
                errores_recientes=errores,
                dias_sin_practicar=max(0, (now - (
                    mastery.updated_at if mastery.updated_at.tzinfo
                    else mastery.updated_at.replace(tzinfo=timezone.utc)
                )).days),
            ))

    # Ordena por urgencia descendente
    conceptos_debiles.sort(key=lambda c: c.score_degradacion, reverse=True)
    return conceptos_debiles


# ─────────────────────────────────────────────────────────────────────────────
# Función principal: verificar_intercepcion
# ─────────────────────────────────────────────────────────────────────────────

async def verificar_intercepcion(
    db: AsyncSession,
    user_id: uuid.UUID,
    challenge: "Challenge",
) -> InterceptResult:
    """
    Punto de entrada principal del Protocolo de Memoria Muscular.

    Llamar ANTES de permitir que el usuario cargue un nivel.
    Típicamente invocado desde el endpoint GET /challenge/:id o desde
    el frontend antes de abrir el editor.

    Pipeline:
      1. Si el challenge no tiene sector → no interceptar (legacy/sin sector)
      2. Si el challenge es del Sector 1 → no interceptar (primer sector)
      3. Chequea si hay una intercepción activa no completada para este usuario
         → si existe y está vigente, retorna esa misión (idempotente)
      4. Analiza degradación con analizar_degradacion()
      5. Si hay conceptos débiles del sector anterior → crea DakiInterception
      6. Genera y retorna la MisionFlash

    Args:
        db:         Sesión de base de datos.
        user_id:    UUID del usuario actual.
        challenge:  El challenge que el usuario intenta acceder.

    Returns:
        InterceptResult con intercept=True si DAKI debe interceptar,
        intercept=False si el usuario puede continuar libremente.
    """
    # ── 1. Checks rápidos de salida ────────────────────────────────────────
    if challenge.sector_id is None or challenge.sector_id <= 1:
        return InterceptResult(intercept=False)

    # ── 2. ¿Hay una intercepción activa y vigente para este usuario? ───────
    now = datetime.now(timezone.utc)
    active_result = await db.execute(
        select(DakiInterception).where(
            DakiInterception.user_id == user_id,
            DakiInterception.status == "pending",
            DakiInterception.expires_at > now,
        ).order_by(DakiInterception.triggered_at.desc()).limit(1)
    )
    existing = active_result.scalar_one_or_none()

    if existing is not None:
        # Ya hay una intercepción activa — la devolvemos (idempotente)
        mision_data = json.loads(existing.mision_flash_json)
        mision = MisionFlash(**mision_data)
        concepto = ConceptoDebil(
            nombre=existing.concept_name,
            sector_ensenado=existing.triggered_on_sector - 1,
            mastery_score=0.0,
            score_degradacion=1.0,
        )
        return InterceptResult(
            intercept=True,
            interception_id=existing.id,
            concepto=concepto,
            mision=mision,
            daki_message=existing.daki_message,
        )

    # ── 3. ¿Estuvo interceptado recientemente por el mismo concepto? ────────
    cooldown_cutoff = now - timedelta(hours=_REINTERCEPT_COOLDOWN_HOURS)
    recent_result = await db.execute(
        select(DakiInterception).where(
            DakiInterception.user_id == user_id,
            DakiInterception.triggered_at > cooldown_cutoff,
        )
    )
    recent_concepts = {r.concept_name for r in recent_result.scalars().all()}

    # ── 4. Analiza degradación ────────────────────────────────────────────
    conceptos = await analizar_degradacion(db, user_id, challenge.sector_id)

    # Filtra conceptos en cooldown
    candidatos = [c for c in conceptos if c.nombre not in recent_concepts]

    if not candidatos:
        return InterceptResult(intercept=False)

    # ── 5. Toma el concepto más urgente ───────────────────────────────────
    concepto_elegido = candidatos[0]

    # ── 6. Genera la Micro-Misión ─────────────────────────────────────────
    mision = generar_mision_flash(concepto_elegido)
    daki_msg = _construir_mensaje_daki(concepto_elegido.nombre)

    # ── 7. Persiste la intercepción ───────────────────────────────────────
    interception = DakiInterception(
        user_id=user_id,
        concept_name=concepto_elegido.nombre,
        triggered_on_challenge_id=challenge.id,
        triggered_on_sector=challenge.sector_id,
        mision_flash_json=json.dumps({
            "concept_name":    mision.concept_name,
            "title":           mision.title,
            "description":     mision.description,
            "lore_briefing":   mision.lore_briefing,
            "initial_code":    mision.initial_code,
            "expected_output": mision.expected_output,
            "hints":           mision.hints,
            "difficulty":      mision.difficulty,
            "estimated_lines": mision.estimated_lines,
        }),
        daki_message=daki_msg,
        status="pending",
        expires_at=now + timedelta(hours=24),
    )
    db.add(interception)
    await db.flush()   # para obtener el id generado antes del commit

    return InterceptResult(
        intercept=True,
        interception_id=interception.id,
        concepto=concepto_elegido,
        mision=mision,
        daki_message=daki_msg,
    )


async def completar_intercepcion(
    db: AsyncSession,
    interception_id: uuid.UUID,
    user_id: uuid.UUID,
) -> bool:
    """
    Marca una intercepción como completada ("passed").

    Llamar cuando el Operador envía la Micro-Misión correctamente.
    Opcionalmente podría disparar un boost de mastery_score para el concepto.

    Returns:
        True si se encontró y actualizó, False si no existe o ya estaba completada.
    """
    result = await db.execute(
        select(DakiInterception).where(
            DakiInterception.id == interception_id,
            DakiInterception.user_id == user_id,
            DakiInterception.status == "pending",
        )
    )
    interception = result.scalar_one_or_none()
    if interception is None:
        return False

    interception.status = "passed"
    interception.completed_at = datetime.now(timezone.utc)

    # Boost de mastery_score: recompensar el repaso con +10 puntos
    from app.models.concept_mastery import ConceptMastery  # local import
    mastery_result = await db.execute(
        select(ConceptMastery).where(
            ConceptMastery.user_id == user_id,
            ConceptMastery.concept_name == interception.concept_name,
        )
    )
    mastery = mastery_result.scalar_one_or_none()
    if mastery is not None:
        mastery.mastery_score = min(100.0, (mastery.mastery_score or 0.0) + 10.0)
        mastery.needs_reinforcement = mastery.mastery_score < _MASTERY_THRESHOLD_HARD

    return True


async def registrar_intento_flash(
    db: AsyncSession,
    interception_id: uuid.UUID,
    user_id: uuid.UUID,
) -> None:
    """Incrementa el contador de intentos de la Micro-Misión."""
    result = await db.execute(
        select(DakiInterception).where(
            DakiInterception.id == interception_id,
            DakiInterception.user_id == user_id,
        )
    )
    interception = result.scalar_one_or_none()
    if interception is not None:
        interception.flash_attempts = (interception.flash_attempts or 0) + 1
