"""Bloque 1 — Arquitectura & Estrategia Shift-Left (L01–L20) — Python"""
from __future__ import annotations
import json

BLOQUE1 = [
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-001: CLASIFICADOR DE SEVERIDADES ]",
"description": (
    "Implementa `classify_bug(desc: str) -> str` que retorne `CRITICAL`, `HIGH`, `MEDIUM` o `LOW` "
    "según palabras clave en la descripción del bug."
),
"difficulty_tier": 1, "difficulty": "easy",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 1, "base_xp_reward": 100,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 180, "challenge_type": "python",
"phase": "fundamentos", "strict_match": False, "is_free": True,
"concepts_taught_json": json.dumps(["clasificación_bugs", "severidad", "triage"]),
"initial_code": (
    "def classify_bug(desc: str) -> str:\n"
    "    # TODO: retorna CRITICAL, HIGH, MEDIUM o LOW según palabras clave\n"
    "    # CRITICAL: crash, data loss, security, authentication\n"
    "    # HIGH:     broken, failure, error, wrong\n"
    "    # MEDIUM:   slow, delay, missing, incorrect\n"
    "    # LOW:      cualquier otro caso\n"
    "    pass\n"
    "\n"
    "\n"
    "bugs = [\n"
    "    'Login crash — data loss detected',\n"
    "    'Wrong total in checkout — calculation error',\n"
    "    'Dashboard slow — 3 second delay',\n"
    "    'Footer logo slightly misaligned',\n"
    "]\n"
    "for desc in bugs:\n"
    "    print(f'{classify_bug(desc)}: {desc}')\n"
),
"expected_output": (
    "CRITICAL: Login crash \u2014 data loss detected\n"
    "HIGH: Wrong total in checkout \u2014 calculation error\n"
    "MEDIUM: Dashboard slow \u2014 3 second delay\n"
    "LOW: Footer logo slightly misaligned"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Operador, el triage eficiente separa al QA junior del Architect. "
    "Clasifica la amenaza antes de perseguirla."
),
"theory_content": (
    "## Severidad de Bugs\n\n"
    "La severidad clasifica el **impacto técnico** del defecto:\n\n"
    "| Severidad | Criterio |\n"
    "|-----------|----------|\n"
    "| CRITICAL  | Data loss, crashes, vulnerabilidades de seguridad |\n"
    "| HIGH      | Funcionalidad rota, errores de cálculo |\n"
    "| MEDIUM    | Degradación de rendimiento, funcionalidad incompleta |\n"
    "| LOW       | Cosméticos, typos, mejoras menores |\n\n"
    "**Tip:** La severidad es técnica. La prioridad la dicta el negocio (eso viene en el nivel 2)."
),
"pedagogical_objective": "Implementar clasificación de bugs por severidad usando reglas de palabras clave.",
"syntax_hint": "Usa `any(w in desc.lower() for w in ['crash', 'data loss', ...])` para detectar categorías.",
"hints_json": json.dumps([
    "Convierte desc a minúsculas antes de comparar: `desc_lower = desc.lower()`",
    "Evalúa CRITICAL primero, luego HIGH, MEDIUM, y LOW como fallback.",
    "Para CRITICAL: 'crash', 'data loss', 'security', 'authentication'. Para HIGH: 'broken', 'failure', 'error', 'wrong'.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-002: PRIORIDAD VS SEVERIDAD ]",
"description": (
    "Implementa `get_priority(severity: str, business_impact: int) -> str` que retorne `HIGH`, `MEDIUM` o `LOW`. "
    "La prioridad combina severidad técnica con impacto de negocio (1-10)."
),
"difficulty_tier": 1, "difficulty": "easy",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 2, "base_xp_reward": 110,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 180, "challenge_type": "python",
"phase": "fundamentos", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["prioridad", "severidad", "contexto_negocio"]),
"initial_code": (
    "def get_priority(severity: str, business_impact: int) -> str:\n"
    "    # TODO: retorna HIGH / MEDIUM / LOW\n"
    "    # Reglas:\n"
    "    # - CRITICAL o HIGH + impact >= 7 → HIGH\n"
    "    # - CRITICAL o HIGH + impact < 7  → MEDIUM\n"
    "    # - MEDIUM (cualquier impacto)    → MEDIUM\n"
    "    # - LOW + impact >= 7             → MEDIUM\n"
    "    # - LOW + impact < 7              → LOW\n"
    "    pass\n"
    "\n"
    "\n"
    "cases = [\n"
    "    ('CRITICAL', 9),\n"
    "    ('CRITICAL', 2),\n"
    "    ('HIGH',     8),\n"
    "    ('HIGH',     3),\n"
    "    ('LOW',      9),\n"
    "]\n"
    "for sev, impact in cases:\n"
    "    priority = get_priority(sev, impact)\n"
    "    print(f'SEV={sev:<8} IMPACT={impact} -> PRIORITY={priority}')\n"
),
"expected_output": (
    "SEV=CRITICAL IMPACT=9 -> PRIORITY=HIGH\n"
    "SEV=CRITICAL IMPACT=2 -> PRIORITY=MEDIUM\n"
    "SEV=HIGH     IMPACT=8 -> PRIORITY=HIGH\n"
    "SEV=HIGH     IMPACT=3 -> PRIORITY=MEDIUM\n"
    "SEV=LOW      IMPACT=9 -> PRIORITY=MEDIUM"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "No todo bug crítico se arregla primero. "
    "La prioridad la dicta el negocio, no la técnica."
),
"theory_content": (
    "## Prioridad != Severidad\n\n"
    "| Severidad | Impacto Negocio | Prioridad |\n"
    "|-----------|-----------------|----------|\n"
    "| CRITICAL  | Alto (>=7)      | HIGH     |\n"
    "| CRITICAL  | Bajo (<7)       | MEDIUM   |\n"
    "| HIGH      | Alto (>=7)      | HIGH     |\n"
    "| HIGH      | Bajo (<7)       | MEDIUM   |\n"
    "| LOW       | Alto (>=7)      | MEDIUM   |\n"
    "| LOW       | Bajo (<7)       | LOW      |\n\n"
    "**Ejemplo real:** Un crash en el panel de admin (CRITICAL + impact=2) es MEDIUM prioridad "
    "porque solo lo usa 1 persona interna. Un typo en el CTA principal (LOW + impact=9) es MEDIUM "
    "porque lo ven millones de usuarios."
),
"pedagogical_objective": "Distinguir severidad técnica de prioridad de negocio y combinarlas correctamente.",
"syntax_hint": "Evalúa primero `severity in ('CRITICAL', 'HIGH')` y luego el threshold de `business_impact`.",
"hints_json": json.dumps([
    "Primero maneja CRITICAL y HIGH juntos: si impact >= 7 → HIGH, si no → MEDIUM.",
    "Para MEDIUM severity: retorna MEDIUM directamente sin importar el impact.",
    "Para LOW: si impact >= 7 → MEDIUM (impacto visible), si no → LOW.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-003: MATRIZ DE RIESGO ]",
"description": (
    "Implementa `risk_score(probability: float, impact: float) -> float` que retorne "
    "`probability * impact` redondeado a 1 decimal. "
    "Luego ordena la lista de features de mayor a menor riesgo."
),
"difficulty_tier": 1, "difficulty": "easy",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 3, "base_xp_reward": 120,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 180, "challenge_type": "python",
"phase": "fundamentos", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["risk_matrix", "probabilidad", "impacto"]),
"initial_code": (
    "def risk_score(probability: float, impact: float) -> float:\n"
    "    # TODO: retorna probability * impact redondeado a 1 decimal\n"
    "    pass\n"
    "\n"
    "\n"
    "features = [\n"
    "    ('Checkout',      4.0, 5.0),\n"
    "    ('Login',         2.0, 5.0),\n"
    "    ('Search',        3.0, 3.0),\n"
    "    ('Analytics',     2.0, 4.0),\n"
    "    ('Notifications', 1.0, 2.0),\n"
    "]\n"
    "ranked = sorted(features, key=lambda f: risk_score(f[1], f[2]), reverse=True)\n"
    "for name, prob, imp in ranked:\n"
    "    print(f'{name:<15} risk={risk_score(prob, imp):.1f}')\n"
),
"expected_output": (
    "Checkout        risk=20.0\n"
    "Login           risk=10.0\n"
    "Search          risk=9.0\n"
    "Analytics       risk=8.0\n"
    "Notifications   risk=2.0"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "El QA Architect prioriza por riesgo, no por intuición. "
    "La matriz es tu brújula en el caos del backlog."
),
"theory_content": (
    "## Risk-Based Testing\n\n"
    "```python\nrisk = probability * impact\n```\n\n"
    "- **Probability**: 1–5 (qué tan probable es que este feature falle)\n"
    "- **Impact**: 1–5 (qué tan grave sería el fallo para el negocio)\n"
    "- **Score máximo**: 25 (alta probabilidad + alto impacto)\n\n"
    "**Beneficio**: concentra el esfuerzo de testing donde más duele si falla."
),
"pedagogical_objective": "Calcular y ordenar features por riesgo usando la matriz probabilidad × impacto.",
"syntax_hint": "`return round(probability * impact, 1)`",
"hints_json": json.dumps([
    "risk_score: `return round(probability * impact, 1)`",
    "Para ordenar descendente: `sorted(..., key=lambda f: risk_score(f[1], f[2]), reverse=True)`",
    "Checkout: 4.0*5.0=20.0, Login: 2.0*5.0=10.0, Search: 3.0*3.0=9.0, Analytics: 2.0*4.0=8.0",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-004: TEST PLAN GENERATOR ]",
"description": (
    "Implementa `generate_test_plan(feature: str, scope: list[str]) -> dict` que retorne "
    "un diccionario con las secciones: `scope`, `approach`, `pass_criteria`, `deliverables`."
),
"difficulty_tier": 1, "difficulty": "easy",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 4, "base_xp_reward": 130,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 180, "challenge_type": "python",
"phase": "fundamentos", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["test_plan", "documentacion", "scope"]),
"initial_code": (
    "def generate_test_plan(feature: str, scope: list) -> dict:\n"
    "    # TODO: retorna dict con estas claves y valores exactos:\n"
    "    # 'scope'        → items de scope separados por ', '\n"
    "    # 'approach'     → 'functional testing, boundary value analysis, error guessing'\n"
    "    # 'pass_criteria'→ 'all critical tests PASS, no HIGH severity bugs open'\n"
    "    # 'deliverables' → 'test cases, test report, defect log'\n"
    "    pass\n"
    "\n"
    "\n"
    "plan = generate_test_plan(\n"
    "    'User Authentication',\n"
    "    ['login', 'logout', 'password_reset']\n"
    ")\n"
    "for section, content in plan.items():\n"
    "    print(f'{section}: {content}')\n"
),
"expected_output": (
    "scope: login, logout, password_reset\n"
    "approach: functional testing, boundary value analysis, error guessing\n"
    "pass_criteria: all critical tests PASS, no HIGH severity bugs open\n"
    "deliverables: test cases, test report, defect log"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Un test plan no es burocracia — es la arquitectura de tu defensa. "
    "Sin él, cada tester prueba a su manera."
),
"theory_content": (
    "## Estructura de un Test Plan\n\n"
    "Las secciones mínimas según IEEE 829:\n\n"
    "1. **Scope**: qué está dentro y fuera del testing\n"
    "2. **Approach**: técnicas de testing a usar\n"
    "3. **Pass/Fail Criteria**: cuándo se considera que el testing pasó\n"
    "4. **Deliverables**: qué documentos se producen\n\n"
    "El plan no necesita ser un documento de 50 páginas — "
    "una página bien estructurada es suficiente para un sprint."
),
"pedagogical_objective": "Estructurar las secciones mínimas de un test plan como función generadora.",
"syntax_hint": "Usa `', '.join(scope)` para concatenar la lista de scope en un string.",
"hints_json": json.dumps([
    "Retorna un dict literal con 4 claves: 'scope', 'approach', 'pass_criteria', 'deliverables'.",
    "scope: `', '.join(scope)` — une los items con coma y espacio.",
    "Las otras 3 secciones son strings fijos — úsalos exactamente como están en los comentarios.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-005: SHIFT-LEFT CALCULATOR ]",
"description": (
    "Implementa `bug_cost(phase: str, base_cost: float) -> float` con factores: "
    "requirements=1x, development=10x, qa=100x, production=1000x. "
    "Imprime el costo de un bug de $100 base en cada fase."
),
"difficulty_tier": 1, "difficulty": "easy",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 5, "base_xp_reward": 140,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 180, "challenge_type": "python",
"phase": "fundamentos", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["shift_left", "costo_defecto", "fases"]),
"initial_code": (
    "PHASE_MULTIPLIERS = {\n"
    "    # TODO: asigna los multiplicadores correctos\n"
    "    # requirements: 1x, development: 10x, qa: 100x, production: 1000x\n"
    "}\n"
    "\n"
    "\n"
    "def bug_cost(phase: str, base_cost: float) -> float:\n"
    "    # TODO: retorna base_cost * PHASE_MULTIPLIERS[phase]\n"
    "    pass\n"
    "\n"
    "\n"
    "base = 100.0\n"
    "phases = ['requirements', 'development', 'qa', 'production']\n"
    "for phase in phases:\n"
    "    cost = bug_cost(phase, base)\n"
    "    print(f'{phase:<15}: ${cost:,.0f}')\n"
),
"expected_output": (
    "requirements   : $100\n"
    "development    : $1,000\n"
    "qa             : $10,000\n"
    "production     : $100,000"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Cuanto más tarde encuentras un bug, más caro es matarlo. "
    "Shift-Left no es filosofía — es matemática."
),
"theory_content": (
    "## Costo del Defecto por Fase\n\n"
    "La regla del 10x establece que el costo de arreglar un bug se multiplica "
    "por 10 en cada fase subsecuente:\n\n"
    "```\n"
    "Requisitos:   $100       (1x)\n"
    "Desarrollo:   $1,000    (10x)\n"
    "QA:           $10,000  (100x)\n"
    "Producción:   $100,000 (1000x)\n"
    "```\n\n"
    "**Implicación**: encontrar un bug en requisitos ahorra $99,900 vs encontrarlo en producción."
),
"pedagogical_objective": "Calcular el costo de un defecto según la fase de detección usando la regla del 10x.",
"syntax_hint": "`{cost:,.0f}` formatea con separador de miles sin decimales.",
"hints_json": json.dumps([
    "PHASE_MULTIPLIERS = {'requirements': 1, 'development': 10, 'qa': 100, 'production': 1000}",
    "bug_cost: `return base_cost * PHASE_MULTIPLIERS[phase]`",
    "El formato `${cost:,.0f}` produce '$1,000' — la coma es el separador de miles.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-006: BOUNDARY DETECTOR ]",
"description": (
    "Implementa `boundary_values(min_val: int, max_val: int) -> list` que retorne "
    "`[min-1, min, nominal, max, max+1]` donde `nominal = (min + max) // 2`."
),
"difficulty_tier": 1, "difficulty": "easy",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 6, "base_xp_reward": 150,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 180, "challenge_type": "python",
"phase": "fundamentos", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["BVA", "boundary_values", "edge_cases"]),
"initial_code": (
    "def boundary_values(min_val: int, max_val: int) -> list:\n"
    "    # TODO: retorna [min-1, min, nominal, max, max+1]\n"
    "    # nominal = (min_val + max_val) // 2\n"
    "    pass\n"
    "\n"
    "\n"
    "for lo, hi in [(18, 65), (0, 100), (1, 10)]:\n"
    "    vals = boundary_values(lo, hi)\n"
    "    print(f'[{lo},{hi}] -> {vals}')\n"
),
"expected_output": (
    "[18,65] -> [17, 18, 41, 65, 66]\n"
    "[0,100] -> [-1, 0, 50, 100, 101]\n"
    "[1,10] -> [0, 1, 5, 10, 11]"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Los bugs habitan en las fronteras. "
    "Tu trabajo como Architect es vigilar cada una."
),
"theory_content": (
    "## Boundary Value Analysis (BVA)\n\n"
    "Los 5 valores canónicos para un rango [min, max]:\n\n"
    "| Valor     | Descripción |\n"
    "|-----------|-------------|\n"
    "| min - 1   | Justo debajo del límite inferior (inválido) |\n"
    "| min       | Exactamente en el límite inferior |\n"
    "| nominal   | Valor típico en el centro del rango |\n"
    "| max       | Exactamente en el límite superior |\n"
    "| max + 1   | Justo encima del límite superior (inválido) |\n\n"
    "**Por qué funciona**: la mayoría de los bugs de rango ocurren en los extremos, "
    "no en el centro. BVA maximiza la detección con mínimos test cases."
),
"pedagogical_objective": "Generar los 5 valores de frontera canónicos para cualquier rango dado.",
"syntax_hint": "`return [min_val-1, min_val, (min_val+max_val)//2, max_val, max_val+1]`",
"hints_json": json.dumps([
    "nominal = (min_val + max_val) // 2 — división entera.",
    "[18,65]: nominal=(18+65)//2=83//2=41. [0,100]: nominal=50. [1,10]: nominal=5.",
    "Retorna una lista de 5 elementos: [min-1, min, nominal, max, max+1].",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-007: EQUIVALENCE PARTITIONER ]",
"description": (
    "Implementa `partition_age(age: int) -> str` que clasifique edades en: "
    "`INVALID_NEGATIVE` (<0), `MINOR` (0-17), `ADULT` (18-64), `SENIOR` (65-120), `INVALID_TOO_HIGH` (>120)."
),
"difficulty_tier": 1, "difficulty": "easy",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 7, "base_xp_reward": 150,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 180, "challenge_type": "python",
"phase": "fundamentos", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["equivalence_partitioning", "clases", "dominio"]),
"initial_code": (
    "def partition_age(age: int) -> str:\n"
    "    # TODO: clasifica la edad en su clase de equivalencia\n"
    "    # < 0         → INVALID_NEGATIVE\n"
    "    # 0 a 17      → MINOR\n"
    "    # 18 a 64     → ADULT\n"
    "    # 65 a 120    → SENIOR\n"
    "    # > 120       → INVALID_TOO_HIGH\n"
    "    pass\n"
    "\n"
    "\n"
    "test_values = [-1, 0, 17, 18, 40, 64, 65, 120, 121]\n"
    "for age in test_values:\n"
    "    print(f'age={age:>4} -> {partition_age(age)}')\n"
),
"expected_output": (
    "age=  -1 -> INVALID_NEGATIVE\n"
    "age=   0 -> MINOR\n"
    "age=  17 -> MINOR\n"
    "age=  18 -> ADULT\n"
    "age=  40 -> ADULT\n"
    "age=  64 -> ADULT\n"
    "age=  65 -> SENIOR\n"
    "age= 120 -> SENIOR\n"
    "age= 121 -> INVALID_TOO_HIGH"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "No puedes probar todo. Pero puedes probar inteligentemente "
    "dividiendo el universo de inputs en clases de equivalencia."
),
"theory_content": (
    "## Equivalence Partitioning\n\n"
    "Cada clase de equivalencia agrupa valores que el sistema trata **de la misma manera**. "
    "Con probar 1 valor por clase, cubres toda la clase:\n\n"
    "| Clase             | Representante | Cobertura |\n"
    "|-------------------|---------------|-----------|\n"
    "| INVALID_NEGATIVE  | -1            | Todos <0  |\n"
    "| MINOR             | 10            | 0-17      |\n"
    "| ADULT             | 30            | 18-64     |\n"
    "| SENIOR            | 70            | 65-120    |\n"
    "| INVALID_TOO_HIGH  | 150           | >120      |\n\n"
    "**Combinado con BVA**: probar el representante + las fronteras = cobertura óptima."
),
"pedagogical_objective": "Clasificar valores en clases de equivalencia usando rangos con condiciones encadenadas.",
"syntax_hint": "Usa `if/elif` en orden: primero inválidos, luego rangos válidos.",
"hints_json": json.dumps([
    "Evalúa primero los casos inválidos: `if age < 0` y `elif age > 120`.",
    "Los rangos: MINOR → 0-17, ADULT → 18-64, SENIOR → 65-120.",
    "Usa elif encadenados: `elif age <= 17: return 'MINOR'`, `elif age <= 64: return 'ADULT'`, etc.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-008: DECISION TABLE BUILDER ]",
"description": (
    "Implementa `apply_discount(premium: bool, loyalty: bool, large_order: bool) -> int` "
    "que retorne el % de descuento según tabla de decisión de 3 condiciones."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 8, "base_xp_reward": 180,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "python",
"phase": "fundamentos", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["decision_table", "combinatoria", "condiciones"]),
"initial_code": (
    "from itertools import product\n"
    "\n"
    "\n"
    "def apply_discount(premium: bool, loyalty: bool, large_order: bool) -> int:\n"
    "    # TODO: retorna el % de descuento\n"
    "    # T T T → 30   T T F → 20   T F T → 15   T F F → 10\n"
    "    # F T T → 15   F T F → 10   F F T →  5   F F F →  0\n"
    "    pass\n"
    "\n"
    "\n"
    "print('PREMIUM | LOYALTY | LARGE | DISCOUNT')\n"
    "print('-' * 38)\n"
    "for p, l, o in product([True, False], repeat=3):\n"
    "    disc = apply_discount(p, l, o)\n"
    "    print(f'   {str(p)[0]}    |    {str(l)[0]}    |   {str(o)[0]}   |   {disc:>3}%')\n"
),
"expected_output": (
    "PREMIUM | LOYALTY | LARGE | DISCOUNT\n"
    "--------------------------------------\n"
    "   T    |    T    |   T   |    30%\n"
    "   T    |    T    |   F   |    20%\n"
    "   T    |    F    |   T   |    15%\n"
    "   T    |    F    |   F   |    10%\n"
    "   F    |    T    |   T   |    15%\n"
    "   F    |    T    |   F   |    10%\n"
    "   F    |    F    |   T   |     5%\n"
    "   F    |    F    |   F   |     0%"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Cuando hay múltiples condiciones combinadas, la tabla de decisión "
    "elimina la ambigüedad y garantiza cobertura completa."
),
"theory_content": (
    "## Decision Tables\n\n"
    "Una tabla de decisión mapea combinaciones de condiciones a acciones. "
    "Para N condiciones booleanas hay 2^N combinaciones posibles.\n\n"
    "Con 3 condiciones: 2^3 = **8 reglas**. Cada regla debe estar cubierta.\n\n"
    "```python\nfrom itertools import product\nfor p, l, o in product([True, False], repeat=3):\n    # 8 combinaciones garantizadas\n```\n\n"
    "**Ventaja**: detecta missing cases — combinaciones que el código no maneja."
),
"pedagogical_objective": "Implementar una tabla de decisión de 3 condiciones booleanas con 8 reglas exhaustivas.",
"syntax_hint": "Usa `if premium and loyalty and large_order: return 30` como primera condición.",
"hints_json": json.dumps([
    "Empieza con la condición más específica (los 3 True) y termina con la más general (ninguno).",
    "Puedes usar: `count = sum([premium, loyalty, large_order])` para contar condiciones activas.",
    "T+T+T=30, T+T=20, cualquier par=15, cualquier uno=10 o 5, ninguno=0. Considera qué par da 15 vs qué uno da 10.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-009: STATE TRANSITION MAPPER ]",
"description": (
    "Implementa `can_transition(current: str, target: str) -> bool` y "
    "`transition(sm_state: list, target: str) -> str` para una máquina de estados de pedidos. "
    "Estados: PENDING → PAID → SHIPPED → DELIVERED. PENDING/PAID pueden cancelarse."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 9, "base_xp_reward": 190,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "python",
"phase": "fundamentos", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["state_machine", "transiciones", "estados"]),
"initial_code": (
    "VALID_TRANSITIONS = {\n"
    "    # TODO: define las transiciones válidas\n"
    "    # 'PENDING':   ['PAID', 'CANCELLED'],\n"
    "    # 'PAID':      ['SHIPPED', 'CANCELLED'],\n"
    "    # 'SHIPPED':   ['DELIVERED'],\n"
    "    # 'DELIVERED': [],\n"
    "    # 'CANCELLED': [],\n"
    "}\n"
    "\n"
    "\n"
    "def transition(state: list, target: str) -> str:\n"
    "    # TODO: si target está en VALID_TRANSITIONS[state[0]], cambia state[0] y retorna 'OK'\n"
    "    # si no, retorna 'INVALID'\n"
    "    pass\n"
    "\n"
    "\n"
    "state = ['PENDING']\n"
    "steps = ['PAID', 'SHIPPED', 'PAID', 'DELIVERED', 'CANCELLED']\n"
    "for target in steps:\n"
    "    result = transition(state, target)\n"
    "    print(f'{result}: -> {target}')\n"
),
"expected_output": (
    "OK: -> PAID\n"
    "OK: -> SHIPPED\n"
    "INVALID: -> PAID\n"
    "OK: -> DELIVERED\n"
    "INVALID: -> CANCELLED"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Un sistema sin modelo de estados es un sistema sin control. "
    "Mapea antes de probar — el diagrama de estados es tu mapa."
),
"theory_content": (
    "## State Transition Testing\n\n"
    "Los estados válidos y sus transiciones definen el **espacio de prueba**:\n\n"
    "```\n"
    "PENDING → PAID → SHIPPED → DELIVERED\n"
    "    \\          \\\n"
    "     CANCELLED  CANCELLED\n"
    "```\n\n"
    "**Test cases clave:**\n"
    "- Happy path: PENDING → PAID → SHIPPED → DELIVERED\n"
    "- Cancelación temprana: PENDING → CANCELLED\n"
    "- Transición inválida: intentar SHIPPED → PAID\n\n"
    "El state transition testing garantiza cobertura de todos los caminos posibles."
),
"pedagogical_objective": "Modelar transiciones de estado válidas e inválidas con un diccionario de reglas.",
"syntax_hint": "Usa `state[0]` (una lista de 1 elemento) para poder mutar el estado dentro de la función.",
"hints_json": json.dumps([
    "VALID_TRANSITIONS = {'PENDING': ['PAID', 'CANCELLED'], 'PAID': ['SHIPPED', 'CANCELLED'], ...}",
    "En transition: `if target in VALID_TRANSITIONS.get(state[0], []):` → cambia state[0] = target, return 'OK'",
    "Los estados terminales (DELIVERED, CANCELLED) tienen lista vacía: no pueden transicionar a ningún lado.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-010: TEST CASE PRIORITIZER ]",
"description": (
    "Implementa `prioritize(test_cases: list) -> list` que ordene los test cases "
    "por `score = risk * frequency * visibility` de mayor a menor."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 10, "base_xp_reward": 200,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "python",
"phase": "fundamentos", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["priorizacion", "regression", "scoring"]),
"initial_code": (
    "def prioritize(test_cases: list) -> list:\n"
    "    # TODO: retorna test_cases ordenados por risk * frequency * visibility (desc)\n"
    "    pass\n"
    "\n"
    "\n"
    "suite = [\n"
    "    {'name': 'checkout_flow',  'risk': 5, 'frequency': 5, 'visibility': 5},\n"
    "    {'name': 'login',          'risk': 4, 'frequency': 5, 'visibility': 4},\n"
    "    {'name': 'search',         'risk': 3, 'frequency': 4, 'visibility': 3},\n"
    "    {'name': 'profile_update', 'risk': 2, 'frequency': 2, 'visibility': 2},\n"
    "    {'name': 'footer_links',   'risk': 1, 'frequency': 1, 'visibility': 1},\n"
    "]\n"
    "ranked = prioritize(suite)\n"
    "for tc in ranked:\n"
    "    score = tc['risk'] * tc['frequency'] * tc['visibility']\n"
    "    print(f'{score:>4} | {tc[\"name\"]}')\n"
),
"expected_output": (
    " 125 | checkout_flow\n"
    "  80 | login\n"
    "  36 | search\n"
    "   8 | profile_update\n"
    "   1 | footer_links"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Con 10,000 tests y 2 horas de sprint, no puedes ejecutarlos todos. "
    "El prioritizer decide cuáles importan."
),
"theory_content": (
    "## Test Prioritization\n\n"
    "```python\nscore = risk * frequency * visibility\n```\n\n"
    "- **Risk**: probabilidad × impacto de fallo\n"
    "- **Frequency**: con qué frecuencia se usa la feature\n"
    "- **Visibility**: qué tan visible es el bug para el usuario\n\n"
    "**Resultado**: ejecutar los top-N tests siempre maximiza la detección de bugs. "
    "Ideal para suites de regresión en CI con tiempo limitado."
),
"pedagogical_objective": "Ordenar test cases por score multivariable usando sorted() con key lambda.",
"syntax_hint": "`return sorted(test_cases, key=lambda tc: tc['risk'] * tc['frequency'] * tc['visibility'], reverse=True)`",
"hints_json": json.dumps([
    "sorted() con reverse=True ordena de mayor a menor.",
    "key=lambda tc: tc['risk'] * tc['frequency'] * tc['visibility'] — multiplica los 3 campos.",
    "checkout: 5*5*5=125, login: 4*5*4=80, search: 3*4*3=36, profile: 2*2*2=8, footer: 1*1*1=1.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-011: DEFECT DENSITY ANALYZER ]",
"description": (
    "Implementa `defect_density(bugs: int, kloc: float) -> float` que retorne "
    "`round(bugs / kloc, 2)`. Analiza los módulos y encuentra el de mayor densidad."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 11, "base_xp_reward": 210,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "python",
"phase": "fundamentos", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["defect_density", "metricas", "KLOC"]),
"initial_code": (
    "def defect_density(bugs: int, kloc: float) -> float:\n"
    "    # TODO: retorna round(bugs / kloc, 2)\n"
    "    pass\n"
    "\n"
    "\n"
    "modules = [\n"
    "    ('auth',      15, 2.1),\n"
    "    ('checkout',  42, 3.8),\n"
    "    ('search',     6, 4.2),\n"
    "    ('dashboard',  3, 1.0),\n"
    "    ('api',       28, 2.5),\n"
    "]\n"
    "analyzed = [(name, defect_density(bugs, kloc)) for name, bugs, kloc in modules]\n"
    "sorted_m = sorted(analyzed, key=lambda x: x[1], reverse=True)\n"
    "print('Module          | DD (bugs/KLOC)')\n"
    "print('-' * 33)\n"
    "for name, dd in sorted_m:\n"
    "    print(f'{name:<16}| {dd:.2f}')\n"
    "worst = sorted_m[0][0]\n"
    "print(f'\\nHighest risk: {worst}')\n"
),
"expected_output": (
    "Module          | DD (bugs/KLOC)\n"
    "---------------------------------\n"
    "api             | 11.20\n"
    "checkout        | 11.05\n"
    "auth            | 7.14\n"
    "dashboard       | 3.00\n"
    "search          | 1.43\n"
    "\n"
    "Highest risk: api"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "El módulo con mayor densidad de defectos necesita más cobertura — o un refactor. "
    "Los números no mienten."
),
"theory_content": (
    "## Defect Density\n\n"
    "```\nDD = bugs_found / (lines_of_code / 1000)\n```\n\n"
    "**Interpretación:**\n"
    "- DD < 2: bajo riesgo\n"
    "- DD 2–10: riesgo moderado, monitorear\n"
    "- DD > 10: alto riesgo, requiere atención urgente\n\n"
    "**Uso práctico**: identifica los módulos que necesitan más test cases, "
    "code review más estricto o refactoring."
),
"pedagogical_objective": "Calcular defect density por módulo e identificar el de mayor riesgo.",
"syntax_hint": "`round(bugs / kloc, 2)` — la densidad se expresa en bugs por cada 1000 líneas.",
"hints_json": json.dumps([
    "defect_density: `return round(bugs / kloc, 2)`",
    "api: 28/2.5=11.20, checkout: 42/3.8=11.05, auth: 15/2.1=7.14, dashboard: 3/1.0=3.00, search: 6/4.2=1.43",
    "sorted_m[0][0] da el nombre del módulo con la densidad más alta.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-012: COVERAGE GAP FINDER ]",
"description": (
    "Implementa `coverage_gap(implemented: list, tested: list) -> dict` que retorne "
    "`{'coverage': float, 'untested': list}`. "
    "`coverage = round(len(tested) / len(implemented) * 100, 1)`."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 12, "base_xp_reward": 220,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "python",
"phase": "fundamentos", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["cobertura", "gap_analysis", "features"]),
"initial_code": (
    "def coverage_gap(implemented: list, tested: list) -> dict:\n"
    "    # TODO: retorna {'coverage': float, 'untested': list}\n"
    "    # coverage = round(len(tested) / len(implemented) * 100, 1)\n"
    "    # untested = features implementadas pero no testeadas\n"
    "    pass\n"
    "\n"
    "\n"
    "features = [\n"
    "    'login', 'checkout', 'search', 'profile',\n"
    "    'notifications', 'reports', 'admin', 'payments'\n"
    "]\n"
    "tested = ['login', 'checkout', 'payments', 'admin']\n"
    "\n"
    "result = coverage_gap(features, tested)\n"
    "print(f'Coverage: {result[\"coverage\"]}%')\n"
    "print(f'Untested: {\", \".join(sorted(result[\"untested\"]))}')\n"
),
"expected_output": (
    "Coverage: 50.0%\n"
    "Untested: notifications, profile, reports, search"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "La cobertura del 80% suena bien hasta que descubres que el 20% sin cubrir "
    "es el checkout. El gap analysis es tu linterna."
),
"theory_content": (
    "## Coverage Gap Analysis\n\n"
    "```python\ncoverage = len(tested) / len(implemented) * 100\ngap = set(implemented) - set(tested)\n```\n\n"
    "**Lo que no mide la cobertura de líneas:**\n"
    "- Features que existen pero no tienen ni un test\n"
    "- Integración entre features\n\n"
    "El gap analysis a nivel de features es el primer paso para una auditoría de calidad."
),
"pedagogical_objective": "Calcular el gap de cobertura entre features implementadas y testeadas.",
"syntax_hint": "`untested = [f for f in implemented if f not in tested]`",
"hints_json": json.dumps([
    "coverage = round(len(tested) / len(implemented) * 100, 1) → 4/8*100 = 50.0",
    "untested = [f for f in implemented if f not in tested] — features presentes en implemented pero no en tested.",
    "sorted(result['untested']) asegura el orden alfabético para el output.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-013: REGRESSION SUITE OPTIMIZER ]",
"description": (
    "Implementa `select_tests(changed_files: list, test_map: dict) -> list` "
    "que retorne la lista de tests únicos afectados por los archivos cambiados."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 13, "base_xp_reward": 230,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "python",
"phase": "fundamentos", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["regression", "impact_analysis", "optimizacion"]),
"initial_code": (
    "def select_tests(changed_files: list, test_map: dict) -> list:\n"
    "    # TODO: retorna lista de tests únicos afectados por changed_files\n"
    "    # test_map: {archivo: [test1, test2, ...]}\n"
    "    # si un test aparece en múltiples archivos, solo inclúyelo una vez\n"
    "    pass\n"
    "\n"
    "\n"
    "test_map = {\n"
    "    'auth.py':     ['test_login', 'test_logout', 'test_password_reset'],\n"
    "    'checkout.py': ['test_cart', 'test_payment', 'test_order_confirm'],\n"
    "    'models.py':   ['test_login', 'test_cart', 'test_user_profile'],\n"
    "    'utils.py':    ['test_format_currency', 'test_date_parser'],\n"
    "}\n"
    "changed = ['auth.py', 'models.py']\n"
    "affected = sorted(select_tests(changed, test_map))\n"
    "print(f'Changed: {\", \".join(changed)}')\n"
    "print(f'Affected tests ({len(affected)}):')\n"
    "for t in affected:\n"
    "    print(f'  - {t}')\n"
),
"expected_output": (
    "Changed: auth.py, models.py\n"
    "Affected tests (5):\n"
    "  - test_cart\n"
    "  - test_login\n"
    "  - test_logout\n"
    "  - test_password_reset\n"
    "  - test_user_profile"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Ejecutar 10,000 tests por cada PR no escala. "
    "Impact analysis te dice cuáles importan — el resto esperan."
),
"theory_content": (
    "## Impact Analysis para Regression\n\n"
    "```\narchivo modificado → tests que lo cubren → ejecutar solo esos\n```\n\n"
    "**Beneficio**: si cambias `auth.py`, no necesitas correr los tests de `checkout.py`. "
    "Reduce el tiempo de CI de 45 min a 8 min.\n\n"
    "**Implementación**: un diccionario `file → [tests]` es el mapa de impacto. "
    "Construirlo es una inversión que paga dividendos en cada PR."
),
"pedagogical_objective": "Implementar impact analysis para seleccionar solo los tests afectados por cambios.",
"syntax_hint": "Usa un `set()` para evitar duplicados, luego convierte a list.",
"hints_json": json.dumps([
    "Itera changed_files, para cada uno obtén test_map.get(f, []) y agrega al set de afectados.",
    "affected = set(); for f in changed_files: affected.update(test_map.get(f, []))",
    "auth.py → [test_login, test_logout, test_password_reset] + models.py → [test_login, test_cart, test_user_profile] = 5 únicos.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-014: EXPLORATORY TESTING CHARTER ]",
"description": (
    "Implementa `create_charter(target: str, risks: list, duration_min: int) -> str` "
    "que retorne un charter de testing exploratorio formateado."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 14, "base_xp_reward": 240,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "python",
"phase": "fundamentos", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["exploratory_testing", "charter", "SBTM"]),
"initial_code": (
    "def create_charter(target: str, risks: list, duration_min: int) -> str:\n"
    "    # TODO: retorna charter con este formato exacto:\n"
    "    # TARGET: {target}\n"
    "    # RISKS: {risks unidos por ', '}\n"
    "    # DURATION: {duration_min} minutos\n"
    "    # NOTES: Sesion de exploracion libre dentro del scope definido.\n"
    "    pass\n"
    "\n"
    "\n"
    "charter = create_charter(\n"
    "    target='User Registration Flow',\n"
    "    risks=['email validation bypass', 'duplicate accounts', 'weak password accepted'],\n"
    "    duration_min=90\n"
    ")\n"
    "print(charter)\n"
),
"expected_output": (
    "TARGET: User Registration Flow\n"
    "RISKS: email validation bypass, duplicate accounts, weak password accepted\n"
    "DURATION: 90 minutos\n"
    "NOTES: Sesion de exploracion libre dentro del scope definido."
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "El testing exploratorio no es 'clickear random' — "
    "es una misión con objetivo, tiempo límite y riesgos identificados."
),
"theory_content": (
    "## Session-Based Test Management (SBTM)\n\n"
    "El charter define la sesión de exploración:\n\n"
    "```\nTARGET: qué explorar\nRISKS: qué puede salir mal\nDURATION: tiempo límite\nNOTES: contexto adicional\n```\n\n"
    "**Beneficio**: el exploratory testing con charter es **medible y reproducible**. "
    "Sin charter, es QA ad-hoc sin estructura."
),
"pedagogical_objective": "Generar un charter de testing exploratorio estructurado según SBTM.",
"syntax_hint": "Usa f-string multilínea con `\\n` entre secciones, y `', '.join(risks)` para la lista.",
"hints_json": json.dumps([
    "Construye el string con 4 líneas unidas por '\\n'.",
    "RISKS line: `f'RISKS: {\", \".join(risks)}'`",
    "El string final debe tener exactamente: TARGET, RISKS, DURATION, NOTES — sin línea extra al final.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-015: BUG REPORT VALIDATOR ]",
"description": (
    "Implementa `validate_bug_report(report: dict) -> list` que retorne lista de issues. "
    "Valida: campos requeridos (title, steps, expected, actual, severity), "
    "title <= 80 chars, severity en CRITICAL/HIGH/MEDIUM/LOW."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 15, "base_xp_reward": 250,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "python",
"phase": "fundamentos", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["bug_report", "calidad", "validacion"]),
"initial_code": (
    "REQUIRED_FIELDS = ['title', 'steps', 'expected', 'actual', 'severity']\n"
    "VALID_SEVERITIES = {'CRITICAL', 'HIGH', 'MEDIUM', 'LOW'}\n"
    "\n"
    "\n"
    "def validate_bug_report(report: dict) -> list:\n"
    "    # TODO: retorna lista de strings con los problemas encontrados\n"
    "    # - 'missing: {campo}' para campos ausentes o vacíos\n"
    "    # - 'title exceeds 80 chars' si title > 80 caracteres\n"
    "    # - 'invalid severity {valor}' si severity no está en VALID_SEVERITIES\n"
    "    pass\n"
    "\n"
    "\n"
    "reports = [\n"
    "    {'title': 'Login fails', 'steps': '1. Enter credentials', 'expected': 'Login',\n"
    "     'actual': 'Error 500', 'severity': 'HIGH'},\n"
    "    {'title': 'A' * 90, 'steps': '1. Do something', 'expected': 'Works',\n"
    "     'actual': '', 'severity': 'EXTREME'},\n"
    "    {'title': 'Search broken', 'actual': 'No results', 'severity': 'MEDIUM'},\n"
    "]\n"
    "for i, r in enumerate(reports, 1):\n"
    "    issues = validate_bug_report(r)\n"
    "    if issues:\n"
    "        print(f'Report {i}: INVALID - {\"; \".join(issues)}')\n"
    "    else:\n"
    "        print(f'Report {i}: VALID')\n"
),
"expected_output": (
    "Report 1: VALID\n"
    "Report 2: INVALID - title exceeds 80 chars; invalid severity EXTREME\n"
    "Report 3: INVALID - missing: steps; missing: expected"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Un bug report incompleto es ruido. "
    "El QA Architect establece el estándar de calidad del reporte."
),
"theory_content": (
    "## Bug Report Quality\n\n"
    "Campos obligatorios según estándar:\n"
    "1. **Title**: < 80 chars, descriptivo y específico\n"
    "2. **Steps to reproduce**: pasos numerados\n"
    "3. **Expected result**: comportamiento esperado\n"
    "4. **Actual result**: comportamiento observado\n"
    "5. **Severity**: CRITICAL/HIGH/MEDIUM/LOW\n\n"
    "Un buen bug report permite reproducir el defecto sin preguntas adicionales."
),
"pedagogical_objective": "Validar la calidad de un bug report verificando campos obligatorios y valores válidos.",
"syntax_hint": "Construye `issues = []` y usa `issues.append(...)` para cada problema encontrado.",
"hints_json": json.dumps([
    "Para campos faltantes: `for field in REQUIRED_FIELDS: if not report.get(field): issues.append(f'missing: {field}')`",
    "Para title length: `if len(report.get('title','')) > 80: issues.append('title exceeds 80 chars')`",
    "Report 2 tiene 'actual': '' (vacío) pero la validación de severity es independiente. Report 3 no tiene 'steps' ni 'expected'.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-016: TEST ESTIMATION ENGINE ]",
"description": (
    "Implementa `estimate_hours(test_cases: int, avg_minutes: float, complexity: float) -> float` "
    "que retorne `round((test_cases * avg_minutes * complexity) / 60, 1)`."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 16, "base_xp_reward": 280,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "python",
"phase": "fundamentos", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["estimacion", "planning", "metricas"]),
"initial_code": (
    "def estimate_hours(test_cases: int, avg_minutes: float, complexity: float) -> float:\n"
    "    # TODO: retorna round((test_cases * avg_minutes * complexity) / 60, 1)\n"
    "    pass\n"
    "\n"
    "\n"
    "scenarios = [\n"
    "    ('Smoke suite',      20,  5.0, 1.0),\n"
    "    ('Regression suite', 150, 8.0, 1.2),\n"
    "    ('API test suite',    80, 4.0, 1.5),\n"
    "    ('E2E full suite',   200,12.0, 1.8),\n"
    "]\n"
    "total = 0.0\n"
    "for name, cases, avg, comp in scenarios:\n"
    "    h = estimate_hours(cases, avg, comp)\n"
    "    total += h\n"
    "    print(f'{name:<22}: {h:>6.1f}h')\n"
    "print(f'{\\'TOTAL\\':<22}: {total:>6.1f}h')\n"
),
"expected_output": (
    "Smoke suite           :    1.7h\n"
    "Regression suite      :   24.0h\n"
    "API test suite        :    8.0h\n"
    "E2E full suite        :   72.0h\n"
    "TOTAL                 :  105.7h"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Cuando el PM pregunta '¿cuánto tarda QA?', "
    "tu respuesta debe ser un número respaldado por datos, no 'depende'."
),
"theory_content": (
    "## Test Estimation\n\n"
    "```python\nhours = (test_cases * avg_minutes * complexity) / 60\n```\n\n"
    "**Factores de complejidad comunes:**\n"
    "- 1.0: funcional simple\n"
    "- 1.2: integración o datos complejos\n"
    "- 1.5: API con múltiples endpoints\n"
    "- 1.8+: E2E multi-sistema\n\n"
    "**Tip**: calibra el `avg_minutes` midiendo 5-10 test cases reales. "
    "La primera estimación siempre se ajusta — lo importante es tener una."
),
"pedagogical_objective": "Implementar un motor de estimación de tiempo de testing con factor de complejidad.",
"syntax_hint": "`return round((test_cases * avg_minutes * complexity) / 60, 1)`",
"hints_json": json.dumps([
    "Smoke: (20*5.0*1.0)/60=100/60=1.666...→1.7. Regression: (150*8.0*1.2)/60=1440/60=24.0.",
    "API: (80*4.0*1.5)/60=480/60=8.0. E2E: (200*12.0*1.8)/60=4320/60=72.0.",
    "Total: 1.7+24.0+8.0+72.0=105.7h — súmalo acumulativamente en el loop.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-017: QUALITY GATE ENFORCER ]",
"description": (
    "Implementa `quality_gate(bugs_open: int, coverage: float, max_bugs: int = 0, min_coverage: float = 80.0) -> str` "
    "que retorne `'GO'` o `'NO-GO: {razones}'`."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 17, "base_xp_reward": 300,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "python",
"phase": "fundamentos", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["quality_gate", "release", "bloqueo"]),
"initial_code": (
    "def quality_gate(bugs_open: int, coverage: float,\n"
    "                 max_bugs: int = 0, min_coverage: float = 80.0) -> str:\n"
    "    # TODO: retorna 'GO' si pasa ambas condiciones\n"
    "    # Si falla, retorna 'NO-GO: {razones unidas por '; '}'\n"
    "    # Razón bugs:     '{bugs_open} open bugs exceed threshold'\n"
    "    # Razón coverage: 'coverage {coverage}% below minimum {min_coverage}%'\n"
    "    pass\n"
    "\n"
    "\n"
    "releases = [\n"
    "    ('v1.2.0', 0, 85.5),\n"
    "    ('v1.2.1', 2, 82.0),\n"
    "    ('v1.3.0', 0, 72.0),\n"
    "    ('v1.3.1', 3, 68.0),\n"
    "]\n"
    "for version, bugs, cov in releases:\n"
    "    decision = quality_gate(bugs, cov)\n"
    "    print(f'{version}: {decision}')\n"
),
"expected_output": (
    "v1.2.0: GO\n"
    "v1.2.1: NO-GO: 2 open bugs exceed threshold\n"
    "v1.3.0: NO-GO: coverage 72.0% below minimum 80.0%\n"
    "v1.3.1: NO-GO: 3 open bugs exceed threshold; coverage 68.0% below minimum 80.0%"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "El quality gate es la última línea de defensa antes de producción. "
    "Si no pasa, no sale. Sin excepciones."
),
"theory_content": (
    "## Quality Gates\n\n"
    "```python\ndef can_release(bugs, coverage, threshold=0, min_cov=80):\n    return bugs <= threshold and coverage >= min_cov\n```\n\n"
    "**En la práctica:**\n"
    "- El gate se ejecuta automáticamente en el pipeline de CI/CD\n"
    "- Si falla, el deploy se bloquea\n"
    "- Los reportes muestran exactamente por qué falló\n\n"
    "**Umbrales comunes**: 0 bugs CRITICAL abiertos, 80% de cobertura mínima."
),
"pedagogical_objective": "Implementar un quality gate que retorne GO/NO-GO con razones específicas.",
"syntax_hint": "Construye una lista de razones y únela con '; '. Si la lista está vacía, retorna 'GO'.",
"hints_json": json.dumps([
    "reasons = []; if bugs_open > max_bugs: reasons.append(f'{bugs_open} open bugs exceed threshold')",
    "if coverage < min_coverage: reasons.append(f'coverage {coverage}% below minimum {min_coverage}%')",
    "return 'GO' if not reasons else f'NO-GO: {\"; \".join(reasons)}'",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-018: ROOT CAUSE ANALYZER ]",
"description": (
    "Implementa `five_whys(symptom: str, whys: list) -> str` que retorne "
    "el análisis formateado con SYMPTOM, WHY 1…WHY N-1, y ROOT CAUSE al final."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 18, "base_xp_reward": 320,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "python",
"phase": "fundamentos", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["root_cause", "5_whys", "analisis"]),
"initial_code": (
    "def five_whys(symptom: str, whys: list) -> str:\n"
    "    # TODO: retorna análisis formateado\n"
    "    # Línea 1:   'SYMPTOM: {symptom}'\n"
    "    # Líneas 2…N:'WHY {i}: {whys[i-1]}' para i=1..len(whys)-1\n"
    "    # Última:    'ROOT CAUSE: {whys[-1]}'\n"
    "    pass\n"
    "\n"
    "\n"
    "analysis = five_whys(\n"
    "    symptom='Payment service down in production',\n"
    "    whys=[\n"
    "        'Database connection pool exhausted',\n"
    "        'Long-running queries blocking connections',\n"
    "        'Missing index on orders.created_at',\n"
    "        'Index removed during migration last Tuesday',\n"
    "        'Migration not reviewed for performance impact',\n"
    "    ]\n"
    ")\n"
    "print(analysis)\n"
),
"expected_output": (
    "SYMPTOM: Payment service down in production\n"
    "WHY 1: Database connection pool exhausted\n"
    "WHY 2: Long-running queries blocking connections\n"
    "WHY 3: Missing index on orders.created_at\n"
    "WHY 4: Index removed during migration last Tuesday\n"
    "ROOT CAUSE: Migration not reviewed for performance impact"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "El QA junior arregla el síntoma. El QA Architect mata la causa raíz. "
    "Los 5 Porqués es la herramienta."
),
"theory_content": (
    "## 5 Whys Method\n\n"
    "Por cada 'por qué' descubres una causa más profunda:\n\n"
    "```\n¿Por qué? → timeout\n¿Por qué? → query lenta\n¿Por qué? → sin índice\n¿Por qué? → removido en migración\n¿Por qué? → sin review de performance ← ROOT CAUSE\n```\n\n"
    "**Regla**: el último 'por qué' es la causa raíz — la que, si se arregla, "
    "previene que el síntoma ocurra de nuevo."
),
"pedagogical_objective": "Formatear un análisis de causa raíz usando el método de los 5 Porqués.",
"syntax_hint": "Usa enumerate para numerar los whys: `for i, why in enumerate(whys[:-1], 1): lines.append(f'WHY {i}: {why}')`",
"hints_json": json.dumps([
    "Empieza con lines = ['SYMPTOM: ' + symptom]",
    "Para los intermedios: `for i, why in enumerate(whys[:-1], 1): lines.append(f'WHY {i}: {why}')`",
    "El último: `lines.append('ROOT CAUSE: ' + whys[-1])`. Retorna '\\n'.join(lines).",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-019: TEST STRATEGY DOCUMENT ]",
"description": (
    "Implementa `build_strategy(project: str, phases: list, tools: list, environments: list) -> str` "
    "que retorne un documento de estrategia formateado con 5 secciones."
),
"difficulty_tier": 3, "difficulty": "hard",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 19, "base_xp_reward": 350,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 300, "challenge_type": "python",
"phase": "fundamentos", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["strategy", "documentacion", "vision"]),
"initial_code": (
    "def build_strategy(project: str, phases: list, tools: list, environments: list) -> str:\n"
    "    # TODO: retorna estrategia con este formato exacto:\n"
    "    # TEST STRATEGY: {project}\n"
    "    # ==================================\n"
    "    # PHASES:\n"
    "    #   - {phase1}\n"
    "    #   - {phase2} ...\n"
    "    # TOOLS: {tools unidos por ', '}\n"
    "    # ENVIRONMENTS: {envs unidos por ', '}\n"
    "    # APPROACH: Shift-left testing with automation at every layer.\n"
    "    pass\n"
    "\n"
    "\n"
    "strategy = build_strategy(\n"
    "    project='DAKI Platform v2.0',\n"
    "    phases=['unit', 'integration', 'e2e', 'performance'],\n"
    "    tools=['pytest', 'playwright', 'k6'],\n"
    "    environments=['dev', 'staging', 'prod'],\n"
    ")\n"
    "print(strategy)\n"
),
"expected_output": (
    "TEST STRATEGY: DAKI Platform v2.0\n"
    "==================================\n"
    "PHASES:\n"
    "  - unit\n"
    "  - integration\n"
    "  - e2e\n"
    "  - performance\n"
    "TOOLS: pytest, playwright, k6\n"
    "ENVIRONMENTS: dev, staging, prod\n"
    "APPROACH: Shift-left testing with automation at every layer."
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "La estrategia define el CÓMO global. "
    "Sin ella, cada QA prueba a su manera — y eso es caos organizado."
),
"theory_content": (
    "## Test Strategy vs Test Plan\n\n"
    "| Documento      | Alcance      | Nivel |\n"
    "|----------------|--------------|-------|\n"
    "| Test Strategy  | Todo el proyecto | QA Architect |\n"
    "| Test Plan      | Feature/Sprint  | QA Lead |\n"
    "| Test Case      | Escenario específico | QA Engineer |\n\n"
    "La estrategia responde: **¿Cómo vamos a garantizar calidad en este proyecto?** "
    "El plan responde: **¿Qué vamos a testear este sprint?**"
),
"pedagogical_objective": "Generar un documento de estrategia de testing estructurado con múltiples secciones.",
"syntax_hint": "Construye una lista de líneas y únelas con '\\n'. Para phases usa list comprehension.",
"hints_json": json.dumps([
    "lines = ['TEST STRATEGY: ' + project, '='*34, 'PHASES:']",
    "Para phases: `lines.extend([f'  - {p}' for p in phases])`",
    "Luego: TOOLS (join), ENVIRONMENTS (join), APPROACH fijo. '\\n'.join(lines).",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-020: CONTRATO — AUDITORIA DE CALIDAD ]",
"description": (
    "Proyecto integrador: implementa `run_audit(system_name: str, modules: list) -> None` "
    "que analice cada módulo (defect_density + coverage_status), calcule totales "
    "y emita veredicto GO/NO-GO."
),
"difficulty_tier": 3, "difficulty": "hard",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 20, "base_xp_reward": 500,
"is_project": True, "is_phase_boss": True,
"telemetry_goal_time": 420, "challenge_type": "python",
"phase": "fundamentos", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["auditoria", "integracion", "go_no_go"]),
"initial_code": (
    "def run_audit(system_name: str, modules: list) -> None:\n"
    "    # TODO: imprime el reporte completo de auditoría\n"
    "    # Para cada módulo: defect_density = round(bugs/kloc, 2)\n"
    "    #                   coverage_status = 'OK' si coverage >= 80, else 'FAIL'\n"
    "    # Calcula: total_bugs = suma de bugs\n"
    "    #          avg_coverage = round(media de coverage, 1)\n"
    "    # Veredicto: GO si total_bugs <= 5 AND avg_coverage >= 80.0\n"
    "    #            NO-GO si alguna condición falla\n"
    "    pass\n"
    "\n"
    "\n"
    "modules = [\n"
    "    {'name': 'auth',     'bugs': 1, 'kloc': 2.0, 'coverage': 92},\n"
    "    {'name': 'checkout', 'bugs': 2, 'kloc': 3.5, 'coverage': 85},\n"
    "    {'name': 'search',   'bugs': 0, 'kloc': 4.0, 'coverage': 78},\n"
    "    {'name': 'api',      'bugs': 1, 'kloc': 2.8, 'coverage': 88},\n"
    "]\n"
    "run_audit('DAKI Platform v2.0', modules)\n"
),
"expected_output": (
    "==========================================\n"
    "AUDITORIA DE CALIDAD: DAKI Platform v2.0\n"
    "==========================================\n"
    "Module      | Bugs | DD    | Cov  | Status\n"
    "-------------------------------------------\n"
    "auth        |    1 | 0.50  |  92% | OK\n"
    "checkout    |    2 | 0.57  |  85% | OK\n"
    "search      |    0 | 0.00  |  78% | FAIL\n"
    "api         |    1 | 0.36  |  88% | OK\n"
    "-------------------------------------------\n"
    "TOTAL BUGS: 4  AVG COVERAGE: 85.8%\n"
    "VEREDICTO: GO\n"
    "=========================================="
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Has completado el primer bloque. Este contrato demuestra "
    "que puedes auditar un sistema real y emitir un veredicto basado en datos."
),
"theory_content": (
    "## Proyecto: Auditoría de Calidad\n\n"
    "Este proyecto integra los conceptos del Bloque 1:\n\n"
    "- **Defect Density**: bugs / KLOC\n"
    "- **Coverage Status**: threshold de 80%\n"
    "- **Quality Gate**: total_bugs <= 5 AND avg_coverage >= 80\n\n"
    "**Output esperado**: un reporte tabular completo + veredicto GO/NO-GO.\n\n"
    "En el mundo real, este reporte se entrega al CTO/PO antes de un release."
),
"pedagogical_objective": "Integrar defect density, coverage analysis y quality gate en un reporte de auditoría completo.",
"syntax_hint": "Calcula avg_coverage = round(sum(m['coverage'] for m in modules) / len(modules), 1).",
"hints_json": json.dumps([
    "DD: round(m['bugs']/m['kloc'], 2). checkout: round(2/3.5, 2)=0.57. api: round(1/2.8, 2)=0.36.",
    "avg_coverage = round((92+85+78+88)/4, 1) = round(343/4, 1) = round(85.75, 1) = 85.8",
    "Veredicto: total_bugs=4 <= 5 Y avg=85.8 >= 80 → GO. La línea final es '=' * 42.",
]),
"grid_map_json": None,
},
]
