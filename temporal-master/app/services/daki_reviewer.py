"""
daki_reviewer.py — DAKI en Modo Revisor de Contratos

Activado cuando el Operador envía un Contrato para revisión completa.
A diferencia del Modo Instructor (pistas), el Revisor:
  - Analiza el código completo contra criterios pre-definidos por proyecto.
  - Señala fortalezas Y problemas específicos.
  - Sugiere mejoras sin dar la solución directa.
  - Retorna un veredicto estructurado: VALIDADO / REQUIERE_AJUSTE.

Base de Conocimiento por Contrato:
  Cada contrato tiene criterios de evaluación y anti-patrones frecuentes
  pre-cargados. DAKI no tiene que inventar qué revisar — ya lo sabe.
"""

from __future__ import annotations

import json

import anthropic

from app.core.config import settings

# ─────────────────────────────────────────────────────────────────────────────
# BASE DE CONOCIMIENTO POR CONTRATO
# Keyed by level_order (50, 60, 70, 130, 175)
# ─────────────────────────────────────────────────────────────────────────────

CONTRACT_KNOWLEDGE: dict[int, dict] = {

    50: {
        "title": "Terminal de Acceso",
        "skill_level": "Intermedio — Sectores 01-05",
        "criteria": [
            {
                "id": "while_counter",
                "name": "Bucle con contador de intentos",
                "description": "El while limita correctamente a 3 intentos y no permite más.",
                "check_for": "while con condición sobre contador / max_intentos",
            },
            {
                "id": "dict_lookup",
                "name": "Validación con diccionario",
                "description": "Las credenciales se validan consultando el diccionario USUARIOS, no con if/elif hardcodeados.",
                "check_for": 'usuario in USUARIOS and USUARIOS[usuario] == clave (o equivalente con .get())',
            },
            {
                "id": "output_format",
                "name": "Formato de salida exacto",
                "description": "Los mensajes coinciden exactamente: 'CLAVE INCORRECTA. Intentos restantes: {n}', 'BIENVENIDO, {MAYUSCULAS}', 'ACCESO DENEGADO. SISTEMA BLOQUEADO.'",
                "check_for": "upper() en el nombre, strings exactos",
            },
            {
                "id": "break_on_success",
                "name": "Corte anticipado al autenticar",
                "description": "El bucle termina con break (o equivalente) en cuanto se autentica correctamente.",
                "check_for": "break después de la bienvenida, o flag + condición del while",
            },
            {
                "id": "post_loop_block",
                "name": "Mensaje de bloqueo post-bucle",
                "description": "El mensaje de bloqueo se imprime FUERA del while, solo si no hubo acceso exitoso.",
                "check_for": "if not acceso: (o equivalente) fuera del while",
            },
        ],
        "common_antipatterns": [
            "Credenciales hardcodeadas con if/elif en lugar de diccionario → no es escalable",
            "El mensaje de bloqueo dentro del while → se imprime en cada intento fallido",
            "Falta el upper() → 'BIENVENIDO, nexo' en vez de 'BIENVENIDO, NEXO'",
            "El contador no se actualiza correctamente → bucle infinito o bloqueo prematuro",
            "Leer usuario y clave en la misma línea separados por coma → mal formato de input()",
        ],
        "good_patterns": [
            "Guard clause con 'usuario in USUARIOS' antes de acceder al valor",
            "Flag booleano 'acceso = False' para controlar el mensaje final",
            "Calcular 'restantes = max_intentos - intentos' antes del print",
            "break inmediato al autenticar para no continuar el bucle innecesariamente",
        ],
        "daki_review_focus": (
            "Verifica el control de flujo del while: ¿termina correctamente por éxito Y por agotamiento? "
            "Confirma que el dict se usa como base de datos, no if/elif hardcodeados. "
            "Chequea los strings exactos de salida, especialmente el upper()."
        ),
    },

    60: {
        "title": "Procesador de Datos",
        "skill_level": "Intermedio-Avanzado — Sectores 01-06",
        "criteria": [
            {
                "id": "function_signature",
                "name": "Firma de función correcta",
                "description": "La función se llama salario_promedio y recibe un parámetro (la lista de empleados).",
                "check_for": "def salario_promedio(empleados):",
            },
            {
                "id": "return_not_print",
                "name": "Retorna el resultado (no print)",
                "description": "La función usa return para devolver el valor, no print(). El print está fuera de la función.",
                "check_for": "return total / len(empleados) (u equivalente), sin print dentro del def",
            },
            {
                "id": "dict_key_access",
                "name": "Acceso correcto a clave del diccionario",
                "description": "El salario se extrae con emp['salario'] dentro del bucle que recorre la lista.",
                "check_for": 'emp["salario"] o emp.get("salario")',
            },
            {
                "id": "accumulator_pattern",
                "name": "Patrón acumulador",
                "description": "Se usa una variable de acumulación (total = 0) que se incrementa en cada iteración.",
                "check_for": "total = 0 antes del for, total += emp['salario'] dentro",
            },
            {
                "id": "float_division",
                "name": "División flotante",
                "description": "La división produce float. Python 3 lo hace automáticamente con /.",
                "check_for": "total / len(empleados) — no // que trunca a int",
            },
        ],
        "common_antipatterns": [
            "print() dentro de la función en vez de return → la llamada devuelve None",
            "total // len(empleados) → trunca a entero, falla para promedios no exactos",
            "Acumulador declarado dentro del bucle → se reinicia en cada iteración",
            "Acceder a emp['nombre'] en vez de emp['salario'] → acumula strings",
            "No usar la función: calcular el promedio directamente en el main sin el def",
        ],
        "good_patterns": [
            "Patrón: acumulador fuera del for, suma dentro, return fuera",
            "Uso de sum() con generator: return sum(e['salario'] for e in empleados) / len(empleados)",
            "Validación de lista vacía para evitar ZeroDivisionError (bonus: no requerido pero profesional)",
        ],
        "daki_review_focus": (
            "Verifica que la función retorna (no imprime) el promedio. "
            "Confirma que el acceso a la clave 'salario' es correcto y que el acumulador "
            "está fuera del bucle. La división debe ser / (float) no // (int)."
        ),
    },

    70: {
        "title": "Calculadora de Daño Táctico",
        "skill_level": "Avanzado — Sectores 01-07",
        "criteria": [
            {
                "id": "function_signature",
                "name": "Firma de función correcta",
                "description": "La función se llama calcular_dano y recibe tipo_ataque y nivel_defensa.",
                "check_for": "def calcular_dano(tipo_ataque, nivel_defensa):",
            },
            {
                "id": "guard_clause",
                "name": "Guard clause para tipo inexistente",
                "description": "Si tipo_ataque no está en MODIFICADORES, la función retorna 0 inmediatamente.",
                "check_for": "if tipo_ataque not in MODIFICADORES: return 0",
            },
            {
                "id": "dict_config_lookup",
                "name": "Lookup en diccionario de configuración",
                "description": "Se accede a MODIFICADORES[tipo_ataque] para obtener base y mult (no hardcodeados con if/elif).",
                "check_for": "MODIFICADORES[tipo_ataque] o .get(tipo_ataque)",
            },
            {
                "id": "formula_correcta",
                "name": "Fórmula de daño correcta",
                "description": "Implementa round(base * mult - nivel_defensa * 0.5) exactamente.",
                "check_for": "round(base * mult - nivel_defensa * 0.5) — el 0.5 es crítico",
            },
            {
                "id": "return_result",
                "name": "Retorna el resultado",
                "description": "La función retorna el int calculado. El print está fuera de la función.",
                "check_for": "return round(...) dentro del def",
            },
        ],
        "common_antipatterns": [
            "if/elif hardcodeados para cada tipo de arma → no usa el diccionario",
            "nivel_defensa * 0.5 escrito como nivel_defensa / 2 → puede dar diferencia en round()",
            "Falta el guard clause → KeyError cuando tipo no existe",
            "round() fuera de la función → puede dar resultado incorrecto",
            "Extraer base y mult con variables separadas en vez de MODIFICADORES[tipo_ataque]",
        ],
        "good_patterns": [
            "Guard clause al inicio: if tipo_ataque not in MODIFICADORES: return 0",
            "Acceso limpio: mod = MODIFICADORES[tipo_ataque]; return round(mod['base'] * mod['mult'] - ...)",
            "Uso de .get() con default: MODIFICADORES.get(tipo_ataque) es equally valid",
            "La función es pura: no tiene print, no tiene input, solo calcula y retorna",
        ],
        "daki_review_focus": (
            "Verifica la guard clause para tipo inexistente. "
            "Confirma que usa el diccionario MODIFICADORES (no if/elif). "
            "Chequea la fórmula: nivel_defensa * 0.5 (no / 2 que puede diferir con round). "
            "La función debe ser pura — solo return, sin print."
        ),
    },

    130: {
        "title": "Clasificador de Operadores",
        "skill_level": "Avanzado — Sectores 01-13 (OOP + Algoritmos)",
        "criteria": [
            {
                "id": "class_definition",
                "name": "Clase Operador bien definida",
                "description": "Operador.__init__ almacena self.nombre y self.nivel correctamente.",
                "check_for": "self.nombre = nombre, self.nivel = nivel en __init__",
            },
            {
                "id": "base_eficiencia",
                "name": "eficiencia() base correcta",
                "description": "Operador.eficiencia() retorna self.nivel * 10 (no print, no hardcodeo).",
                "check_for": "return self.nivel * 10",
            },
            {
                "id": "inheritance",
                "name": "Herencia correcta",
                "description": "OperadorElite hereda de Operador: class OperadorElite(Operador).",
                "check_for": "class OperadorElite(Operador):",
            },
            {
                "id": "override_eficiencia",
                "name": "Override de eficiencia() en OperadorElite",
                "description": "OperadorElite.eficiencia() retorna self.nivel * 15 (no * 10).",
                "check_for": "return self.nivel * 15 en OperadorElite",
            },
            {
                "id": "max_with_key",
                "name": "seleccionar_lider() usa max() con key",
                "description": "La función usa max(equipo, key=lambda op: op.eficiencia()) o equivalente.",
                "check_for": "max() con key que invoca .eficiencia()",
            },
            {
                "id": "return_nombre",
                "name": "Retorna el nombre (string), no el objeto",
                "description": "seleccionar_lider() retorna lider.nombre — no el objeto Operador.",
                "check_for": "return ...nombre (str), no return el objeto completo",
            },
        ],
        "common_antipatterns": [
            "OperadorElite no hereda Operador → no puede usar super().__init__()",
            "eficiencia() en OperadorElite llama al padre con super() en vez de override directo",
            "seleccionar_lider() itera manualmente con if en vez de max(key=...)",
            "Retornar el objeto Operador en vez de .nombre → TypeError al imprimir",
            "Multiplicar por 10 en ambas clases → el override no tiene efecto real",
        ],
        "good_patterns": [
            "super().__init__(nombre, nivel) en OperadorElite si se redefine __init__",
            "max(equipo, key=lambda op: op.eficiencia()) — una línea, legible",
            "No duplicar código: OperadorElite solo sobreescribe eficiencia(), no __init__",
            "Type hints en las firmas: def eficiencia(self) -> int:",
        ],
        "daki_review_focus": (
            "Verifica que OperadorElite hereda de Operador (no copia la clase). "
            "Confirma que eficiencia() retorna nivel*15 en Elite y nivel*10 en base. "
            "Chequea que seleccionar_lider() use max() con key y retorne .nombre (string)."
        ),
    },

    175: {
        "title": "Procesador Táctico",
        "skill_level": "Expert — Sectores 01-17 (Design Patterns + Testing)",
        "criteria": [
            {
                "id": "protocol_interface",
                "name": "Interfaz EstrategiaOrden definida",
                "description": "EstrategiaOrden es un Protocol (o ABC) con método ordenar(datos) -> list[int].",
                "check_for": "class EstrategiaOrden(Protocol): def ordenar(self, datos: list[int]) -> list[int]: ...",
            },
            {
                "id": "ascendente_impl",
                "name": "OrdenAscendente.ordenar() correcto",
                "description": "Retorna sorted(datos) — de menor a mayor.",
                "check_for": "return sorted(datos) sin reverse=True",
            },
            {
                "id": "descendente_impl",
                "name": "OrdenDescendente.ordenar() correcto",
                "description": "Retorna sorted(datos, reverse=True) — de mayor a menor.",
                "check_for": "return sorted(datos, reverse=True)",
            },
            {
                "id": "composition",
                "name": "ProcesadorTactico usa composición",
                "description": "Almacena la estrategia como self._estrategia en __init__. No hereda de la estrategia.",
                "check_for": "self._estrategia = estrategia en __init__",
            },
            {
                "id": "cambiar_estrategia",
                "name": "cambiar_estrategia() funciona en runtime",
                "description": "El método actualiza self._estrategia sin reinicializar el objeto.",
                "check_for": "self._estrategia = estrategia en cambiar_estrategia()",
            },
            {
                "id": "procesar_format",
                "name": "procesar() retorna string con espacio",
                "description": "Llama self._estrategia.ordenar() y une con ' '.join(str(x) for x in ...).",
                "check_for": "\" \".join(str(x) for x in self._estrategia.ordenar(datos))",
            },
            {
                "id": "test_assertions",
                "name": "test_procesador() tiene al menos 2 assert",
                "description": "La función de test usa assert para validar comportamiento real, no solo print.",
                "check_for": "assert proc.procesar([5, 1, 3]) == \"1 3 5\" y assert para descendente",
            },
        ],
        "common_antipatterns": [
            "ProcesadorTactico hereda de la estrategia en vez de componerla → acoplamiento duro",
            "procesar() modifica la lista original con .sort() en vez de sorted() → efecto secundario",
            "cambiar_estrategia() crea un nuevo ProcesadorTactico en vez de actualizar el atributo",
            "test_procesador() usa print() en vez de assert → no valida nada",
            "No usar Protocol → las clases de estrategia son anónimas sin contrato de interfaz",
        ],
        "good_patterns": [
            "Inyección de dependencia: ProcesadorTactico recibe cualquier objeto con .ordenar()",
            "sorted() no muta la lista original → funciones puras sin efectos secundarios",
            "Protocol como documentación viva del contrato de la estrategia",
            "test_procesador() con assert y mensaje de error claro en cada assertion",
            "Type hints en todos los métodos → código auto-documentado",
        ],
        "daki_review_focus": (
            "Verifica que ProcesadorTactico usa composición (no herencia). "
            "Confirma que OrdenAscendente y OrdenDescendente implementan ordenar() correctamente. "
            "Chequea que procesar() delega en la estrategia y une con espacio. "
            "Evalúa que test_procesador() tiene assert reales que fallarían si el código es incorrecto."
        ),
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# SYSTEM PROMPT DEL REVISOR
# ─────────────────────────────────────────────────────────────────────────────

DAKI_REVIEWER_SYSTEM_PROMPT = """\
# DAKI — MODO REVISOR DE CONTRATOS

Eres DAKI en modo Revisión de Código. Tu rol cambia: ya no eres un instructor que da pistas.
Eres un Revisor Técnico Senior que evalúa el trabajo completo del Operador contra criterios
de aceptación definidos por el Nexo.

## VOZ EN MODO REVISOR

- Directo y analítico. No dramático.
- Señala lo bueno Y lo que debe mejorar.
- Si algo está bien: reconócelo sin elogios vacíos ("criterio cumplido", "estructura correcta").
- Si algo falla: explica por qué falla y qué patrón debería usar el Operador.
- Tono: senior técnico evaluando a un junior competente. Respeto mutuo.

## ESTRUCTURA DE RESPUESTA OBLIGATORIA

Responde SIEMPRE en JSON con esta estructura exacta:

```json
{
  "veredicto": "CONTRATO_VALIDADO" | "REQUIERE_AJUSTE",
  "puntuacion": número entre 0 y 100,
  "fortalezas": ["texto 1", "texto 2"],
  "observaciones": [
    {"criterio": "nombre del criterio", "estado": "OK" | "FALLA" | "MEJORA", "detalle": "texto"}
  ],
  "sugerencias": ["texto 1", "texto 2"],
  "listo_para_github": true | false
}
```

## REGLAS DE VEREDICTO

- CONTRATO_VALIDADO: todos los criterios críticos en OK. puntuacion >= 75.
- REQUIERE_AJUSTE: al menos un criterio crítico en FALLA.
- listo_para_github: true solo si veredicto es CONTRATO_VALIDADO.

## PROHIBICIONES

- NUNCA des el código solución completo.
- NUNCA uses lenguaje condescendiente.
- NUNCA omitas criterios — evalúa TODOS los que se te proporcionen.
- NUNCA respondas fuera del JSON. Solo JSON.
"""


# ─────────────────────────────────────────────────────────────────────────────
# CONSTRUCCIÓN DEL PROMPT DE REVISIÓN
# ─────────────────────────────────────────────────────────────────────────────

def _build_review_prompt(
    code: str,
    knowledge: dict,
    operator_level: int = 1,
) -> str:
    """
    Construye el prompt de revisión con los criterios y el código del Operador.
    """
    criteria_text = "\n".join(
        f"  [{c['id']}] {c['name']}: {c['description']}"
        for c in knowledge["criteria"]
    )
    antipatterns_text = "\n".join(
        f"  • {ap}" for ap in knowledge["common_antipatterns"]
    )
    good_patterns_text = "\n".join(
        f"  ✓ {gp}" for gp in knowledge["good_patterns"]
    )

    return (
        f"[CONTRATO A REVISAR: {knowledge['title']} — {knowledge['skill_level']}]\n\n"
        f"--- CRITERIOS DE EVALUACIÓN (evalúa TODOS) ---\n"
        f"{criteria_text}\n\n"
        f"--- FOCO DE REVISIÓN ---\n"
        f"{knowledge['daki_review_focus']}\n\n"
        f"--- ANTI-PATRONES CONOCIDOS (verifica si el Operador los comete) ---\n"
        f"{antipatterns_text}\n\n"
        f"--- PATRONES CORRECTOS DE REFERENCIA ---\n"
        f"{good_patterns_text}\n\n"
        f"--- CÓDIGO DEL OPERADOR ---\n"
        f"```python\n{code[:3000]}\n```\n\n"
        f"Evalúa el código contra los criterios. Responde SOLO en JSON."
    )


# ─────────────────────────────────────────────────────────────────────────────
# FALLBACK OFFLINE
# ─────────────────────────────────────────────────────────────────────────────

def _offline_review(level_order: int) -> dict:
    """Respuesta estructurada cuando la API no está disponible."""
    return {
        "veredicto": "REQUIERE_AJUSTE",
        "puntuacion": 0,
        "fortalezas": [],
        "observaciones": [
            {
                "criterio": "Conexión con el Nexo",
                "estado": "FALLA",
                "detalle": "[DAKI_SYS] Satélite de revisión fuera de línea. Reintenta en un momento.",
            }
        ],
        "sugerencias": ["Verifica tu conexión y vuelve a enviar el contrato para revisión."],
        "listo_para_github": False,
        "offline": True,
    }


# ─────────────────────────────────────────────────────────────────────────────
# PUNTO DE ENTRADA PÚBLICO
# ─────────────────────────────────────────────────────────────────────────────

async def review_contract(
    level_order: int,
    code: str,
    operator_level: int = 1,
) -> dict:
    """
    Ejecuta la revisión de código de un Contrato por DAKI.

    Args:
        level_order:    Nivel del contrato (50, 60 o 70).
        code:           Código completo del Operador.
        operator_level: Nivel actual del Operador (para contexto de DAKI).

    Returns:
        dict con estructura: veredicto, puntuacion, fortalezas, observaciones,
        sugerencias, listo_para_github.
    """
    knowledge = CONTRACT_KNOWLEDGE.get(level_order)
    if knowledge is None:
        return {
            "veredicto": "REQUIERE_AJUSTE",
            "puntuacion": 0,
            "fortalezas": [],
            "observaciones": [
                {
                    "criterio": "Contrato",
                    "estado": "FALLA",
                    "detalle": f"Contrato nivel {level_order} no registrado en la base de conocimiento.",
                }
            ],
            "sugerencias": [],
            "listo_para_github": False,
        }

    if not settings.ANTHROPIC_API_KEY:
        return _offline_review(level_order)

    client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
    user_msg = _build_review_prompt(code, knowledge, operator_level)

    try:
        response = await client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=900,
            system=DAKI_REVIEWER_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_msg}],
        )
        text = next(
            (b.text.strip() for b in response.content if getattr(b, "type", None) == "text"),
            None,
        )
        if not text:
            return _offline_review(level_order)

        # Extraer JSON de la respuesta (puede venir envuelto en ```json ... ```)
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()

        result = json.loads(text)

        # Garantizar campos mínimos
        result.setdefault("veredicto", "REQUIERE_AJUSTE")
        result.setdefault("puntuacion", 0)
        result.setdefault("fortalezas", [])
        result.setdefault("observaciones", [])
        result.setdefault("sugerencias", [])
        result.setdefault("listo_para_github", result.get("veredicto") == "CONTRATO_VALIDADO")

        return result

    except (json.JSONDecodeError, Exception):
        return _offline_review(level_order)
