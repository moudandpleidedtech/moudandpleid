"""
_tpm_b1.py — TPM Mastery · BLOQUE 1 (L01–L15)
===============================================
Fase: programa_fundamentos
Niveles: 01 a 15 (15 desafíos Python)
Boss: L15 — Program Kickoff Report Generator
"""
from __future__ import annotations

_BASE = dict(
    codex_id       = "tpm_mastery",
    sector_id      = 21,
    challenge_type = "python",
    phase          = "programa_fundamentos",
    is_free        = False,
    strict_match   = False,
    is_phase_boss  = False,
    is_project     = False,
)
_BASE_BOSS = {k: v for k, v in _BASE.items() if k not in ("is_phase_boss", "is_project")}
_BASE_FREE = {k: v for k, v in _BASE.items() if k != "is_free"}

# ─────────────────────────────────────────────────────────────────────────────
# L01 — OKR Validator  [FREE]
# ─────────────────────────────────────────────────────────────────────────────
L01 = dict(
    **_BASE_FREE,
    level_order   = 1,
    title         = "OKR Validator",
    difficulty    = "easy",
    is_free       = True,
    description   = (
        "Los OKRs (Objectives & Key Results) son el lenguaje estratégico del TPM. "
        "Implementa `validate_okrs(okrs)` que evalúa si los Key Results son medibles.\n\n"
        "Un KR es **medible** si contiene al menos un dígito numérico en su texto.\n\n"
        "Cada OKR es un dict `{'objective': str, 'key_results': list[str]}`.\n\n"
        "Para cada OKR imprime:\n"
        "`O<N>: <objective> — X/Y KRs measurable [OK|WEAK]`\n\n"
        "`OK` si todos los KRs son medibles. `WEAK` si alguno no lo es.\n\n"
        "Al final: `Valid OKRs: N/M`"
    ),
    hint          = "Usa `any(c.isdigit() for c in kr)` para verificar si un KR tiene número.",
    initial_code  = (
        "def validate_okrs(okrs):\n"
        "    pass\n\n"
        "okrs = [\n"
        "    {'objective': 'Improve platform reliability',\n"
        "     'key_results': ['Reduce p99 latency to 200ms', 'Achieve 99.9% uptime', 'Reduce error rate to 0.1%']},\n"
        "    {'objective': 'Grow user base',\n"
        "     'key_results': ['Reach 10000 active users', 'Increase retention by 15%', 'Launch referral program']},\n"
        "    {'objective': 'Accelerate delivery',\n"
        "     'key_results': ['Deploy every week', 'Reduce lead time to 3 days', 'Cut review cycle to 24h']},\n"
        "]\n"
        "validate_okrs(okrs)\n"
    ),
    expected_output = (
        "O1: Improve platform reliability — 3/3 KRs measurable [OK]\n"
        "O2: Grow user base — 2/3 KRs measurable [WEAK]\n"
        "O3: Accelerate delivery — 2/3 KRs measurable [WEAK]\n"
        "Valid OKRs: 1/3"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L02 — WBS Builder
# ─────────────────────────────────────────────────────────────────────────────
L02 = dict(
    **_BASE,
    level_order   = 2,
    title         = "WBS Builder",
    difficulty    = "easy",
    description   = (
        "El Work Breakdown Structure (WBS) descompone un proyecto en fases y tareas numeradas. "
        "Implementa `build_wbs(project, phases)` donde `phases` es una lista de "
        "`{'name': str, 'tasks': list[str]}`.\n\n"
        "Imprime el WBS con formato jerárquico:\n"
        "```\n"
        "WBS: <project>\n"
        "N. <phase>\n"
        "   N.M <task>\n"
        "```\n"
        "Al final: `Total: N phases, M tasks`"
    ),
    hint          = "Usa enumerate con start=1 para los índices. Las tareas llevan doble indentación.",
    initial_code  = (
        "def build_wbs(project, phases):\n"
        "    pass\n\n"
        "build_wbs(\n"
        "    project='DAKI Platform v2 Launch',\n"
        "    phases=[\n"
        "        {'name': 'Discovery',   'tasks': ['User research', 'Competitive analysis', 'Requirements doc']},\n"
        "        {'name': 'Design',      'tasks': ['Wireframes', 'UI components', 'Design review']},\n"
        "        {'name': 'Development', 'tasks': ['Backend API', 'Frontend', 'Integration tests']},\n"
        "        {'name': 'Launch',      'tasks': ['Staging deploy', 'UAT', 'Production deploy']},\n"
        "    ]\n"
        ")\n"
    ),
    expected_output = (
        "WBS: DAKI Platform v2 Launch\n"
        "1. Discovery\n"
        "   1.1 User research\n"
        "   1.2 Competitive analysis\n"
        "   1.3 Requirements doc\n"
        "2. Design\n"
        "   2.1 Wireframes\n"
        "   2.2 UI components\n"
        "   2.3 Design review\n"
        "3. Development\n"
        "   3.1 Backend API\n"
        "   3.2 Frontend\n"
        "   3.3 Integration tests\n"
        "4. Launch\n"
        "   4.1 Staging deploy\n"
        "   4.2 UAT\n"
        "   4.3 Production deploy\n"
        "Total: 4 phases, 12 tasks"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L03 — RACI Validator
# ─────────────────────────────────────────────────────────────────────────────
L03 = dict(
    **_BASE,
    level_order   = 3,
    title         = "RACI Validator",
    difficulty    = "easy",
    description   = (
        "Una matriz RACI asigna roles a actividades: R=Responsible, A=Accountable, "
        "C=Consulted, I=Informed. Cada actividad debe tener **exactamente un Accountable**.\n\n"
        "Implementa `validate_raci(activities, roles, assignments)` donde:\n"
        "- `activities`: lista de nombres de actividades\n"
        "- `roles`: lista de roles\n"
        "- `assignments`: dict `{activity: {role: letter}}`\n\n"
        "Imprime la matriz con el formato:\n"
        "`<activity padded 16> <role1>  <role2>  ...  [OK|NO-A]`\n\n"
        "`NO-A` si la actividad no tiene exactamente un 'A'.\n\n"
        "Al final: `RACI valid: N/M activities accountable`"
    ),
    hint          = "Cuenta cuántas veces aparece 'A' en los valores del dict de la actividad.",
    initial_code  = (
        "def validate_raci(activities, roles, assignments):\n"
        "    pass\n\n"
        "activities = ['Requirements', 'Design', 'Development', 'Testing', 'Deployment']\n"
        "roles = ['TPM', 'PM', 'Eng', 'QA']\n"
        "assignments = {\n"
        "    'Requirements': {'TPM': 'A', 'PM': 'R', 'Eng': 'C', 'QA': 'I'},\n"
        "    'Design':       {'TPM': 'I', 'PM': 'A', 'Eng': 'R', 'QA': 'C'},\n"
        "    'Development':  {'TPM': 'I', 'PM': 'C', 'Eng': 'A', 'QA': 'C'},\n"
        "    'Testing':      {'TPM': 'I', 'PM': 'C', 'Eng': 'C', 'QA': 'A'},\n"
        "    'Deployment':   {'TPM': 'A', 'PM': 'I', 'Eng': 'R', 'QA': 'C'},\n"
        "}\n"
        "validate_raci(activities, roles, assignments)\n"
    ),
    expected_output = (
        "Activity          TPM  PM   Eng  QA\n"
        "Requirements       A    R    C    I   [OK]\n"
        "Design             I    A    R    C   [OK]\n"
        "Development        I    C    A    C   [OK]\n"
        "Testing            I    C    C    A   [OK]\n"
        "Deployment         A    I    R    C   [OK]\n"
        "RACI valid: 5/5 activities accountable"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L04 — Dependency Sorter
# ─────────────────────────────────────────────────────────────────────────────
L04 = dict(
    **_BASE,
    level_order   = 4,
    title         = "Dependency Sorter",
    difficulty    = "medium",
    description   = (
        "Un TPM debe ordenar tareas respetando dependencias antes de asignarlas al equipo. "
        "Implementa `sort_by_dependencies(tasks)` usando el algoritmo de Kahn "
        "(ordenamiento topológico).\n\n"
        "Cada tarea: `{'id': str, 'name': str, 'deps': list[str]}`.\n\n"
        "Cuando múltiples tareas tienen sus dependencias satisfechas al mismo tiempo, "
        "procésalas en el orden en que aparecen en la lista original.\n\n"
        "Imprime:\n"
        "`Execution order:`\n"
        "`N. <id>: <name>`\n"
        "Al final: `No circular dependencies detected.`"
    ),
    hint          = "Calcula in-degree por tarea. Usa una cola con los nodos de in-degree=0.",
    initial_code  = (
        "from collections import deque\n\n"
        "def sort_by_dependencies(tasks):\n"
        "    pass\n\n"
        "tasks = [\n"
        "    {'id': 'T1', 'name': 'Setup environment', 'deps': []},\n"
        "    {'id': 'T2', 'name': 'Design DB schema',  'deps': ['T1']},\n"
        "    {'id': 'T3', 'name': 'Implement auth',    'deps': ['T1']},\n"
        "    {'id': 'T4', 'name': 'Build API',         'deps': ['T2', 'T3']},\n"
        "    {'id': 'T5', 'name': 'QA testing',        'deps': ['T4']},\n"
        "    {'id': 'T6', 'name': 'Deploy to prod',    'deps': ['T5']},\n"
        "]\n"
        "sort_by_dependencies(tasks)\n"
    ),
    expected_output = (
        "Execution order:\n"
        "1. T1: Setup environment\n"
        "2. T2: Design DB schema\n"
        "3. T3: Implement auth\n"
        "4. T4: Build API\n"
        "5. T5: QA testing\n"
        "6. T6: Deploy to prod\n"
        "No circular dependencies detected."
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L05 — Risk Scorer
# ─────────────────────────────────────────────────────────────────────────────
L05 = dict(
    **_BASE,
    level_order   = 5,
    title         = "Risk Scorer",
    difficulty    = "easy",
    description   = (
        "El registro de riesgos es el arma principal del TPM para proteger el programa. "
        "Implementa `score_risks(risks)` que calcula `score = probability × impact` "
        "y clasifica cada riesgo.\n\n"
        "Clasificación:\n"
        "- score >= 15 → CRITICAL\n"
        "- score >= 8  → HIGH\n"
        "- score >= 4  → MEDIUM\n"
        "- score < 4   → LOW\n\n"
        "Ordena por score descendente. Imprime:\n"
        "`[LEVEL] <id>  score=N  <desc>`\n\n"
        "Al final: `Summary: Critical=N  High=N  Medium=N  Low=N`"
    ),
    hint          = "Ordena con sorted(..., key=lambda r: r['prob']*r['impact'], reverse=True).",
    initial_code  = (
        "def score_risks(risks):\n"
        "    pass\n\n"
        "risks = [\n"
        "    {'id': 'R1', 'desc': 'Key engineer leaves',   'prob': 3, 'impact': 5},\n"
        "    {'id': 'R2', 'desc': 'Vendor API deprecated', 'prob': 2, 'impact': 4},\n"
        "    {'id': 'R3', 'desc': 'Scope expansion',       'prob': 4, 'impact': 3},\n"
        "    {'id': 'R4', 'desc': 'Integration delay',     'prob': 5, 'impact': 5},\n"
        "    {'id': 'R5', 'desc': 'Budget overrun',        'prob': 2, 'impact': 2},\n"
        "]\n"
        "score_risks(risks)\n"
    ),
    expected_output = (
        "Risk Register (sorted by score):\n"
        "[CRITICAL] R4  score=25  Integration delay\n"
        "[CRITICAL] R1  score=15  Key engineer leaves\n"
        "[HIGH]     R3  score=12  Scope expansion\n"
        "[HIGH]     R2  score=8   Vendor API deprecated\n"
        "[MEDIUM]   R5  score=4   Budget overrun\n"
        "Summary: Critical=2  High=2  Medium=1  Low=0"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L06 — Roadmap Prioritizer
# ─────────────────────────────────────────────────────────────────────────────
L06 = dict(
    **_BASE,
    level_order   = 6,
    title         = "Roadmap Prioritizer",
    difficulty    = "medium",
    description   = (
        "Un TPM ordena el backlog respetando dependencias y maximizando el valor. "
        "Implementa `prioritize_roadmap(features)` con un algoritmo greedy:\n\n"
        "En cada ronda, de las features disponibles (todas sus deps ya están colocadas), "
        "selecciona la de mayor score. Repite hasta colocar todas.\n\n"
        "Cada feature: `{'id': str, 'name': str, 'score': int, 'deps': list[str]}`.\n\n"
        "Imprime:\n"
        "`Prioritized Roadmap:`\n"
        "`N. <id>: <name>  [score=N]`"
    ),
    hint          = "Mantén un set de 'placed'. En cada paso filtra features no placed con deps ⊆ placed.",
    initial_code  = (
        "def prioritize_roadmap(features):\n"
        "    pass\n\n"
        "features = [\n"
        "    {'id': 'F1', 'name': 'User authentication', 'score': 95, 'deps': []},\n"
        "    {'id': 'F2', 'name': 'Dashboard v1',        'score': 80, 'deps': ['F1']},\n"
        "    {'id': 'F3', 'name': 'Analytics engine',    'score': 70, 'deps': ['F1']},\n"
        "    {'id': 'F4', 'name': 'Export to PDF',       'score': 45, 'deps': ['F2']},\n"
        "    {'id': 'F5', 'name': 'Mobile app',          'score': 60, 'deps': ['F2', 'F3']},\n"
        "]\n"
        "prioritize_roadmap(features)\n"
    ),
    expected_output = (
        "Prioritized Roadmap:\n"
        "1. F1: User authentication  [score=95]\n"
        "2. F2: Dashboard v1  [score=80]\n"
        "3. F3: Analytics engine  [score=70]\n"
        "4. F5: Mobile app  [score=60]\n"
        "5. F4: Export to PDF  [score=45]"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L07 — Milestone Health Checker
# ─────────────────────────────────────────────────────────────────────────────
L07 = dict(
    **_BASE,
    level_order   = 7,
    title         = "Milestone Health Checker",
    difficulty    = "medium",
    description   = (
        "Implementa `check_milestones(milestones, today)` que evalúa el estado de salud "
        "de los hitos de un programa.\n\n"
        "Cada milestone: `{'name': str, 'planned': str, 'actual': str|None, 'done': bool}`.\n"
        "`today` es un objeto `date`.\n\n"
        "Reglas de estado:\n"
        "- Done + delay == 0 → `[GREEN]  Completed on time`\n"
        "- Done + delay > 0  → `[YELLOW] Completed N days late`\n"
        "- Not done + today > planned → `[RED]    Overdue by N days`\n"
        "- Not done + today <= planned → `[GREEN]  On track (N days remaining)`\n\n"
        "Formato: `  <name padded 18> <estado>`\n\n"
        "Al final: `Overall: N RED, N YELLOW, N GREEN`"
    ),
    hint          = "Usa `(date.fromisoformat(s2) - date.fromisoformat(s1)).days` para calcular diferencias.",
    initial_code  = (
        "from datetime import date\n\n"
        "def check_milestones(milestones, today):\n"
        "    pass\n\n"
        "milestones = [\n"
        "    {'name': 'Kickoff',         'planned': '2024-01-15', 'actual': '2024-01-15', 'done': True},\n"
        "    {'name': 'Design Complete', 'planned': '2024-02-01', 'actual': '2024-02-08', 'done': True},\n"
        "    {'name': 'Alpha Release',   'planned': '2024-03-15', 'actual': None,         'done': False},\n"
        "    {'name': 'Beta Launch',     'planned': '2024-04-30', 'actual': None,         'done': False},\n"
        "]\n"
        "check_milestones(milestones, date(2024, 3, 20))\n"
    ),
    expected_output = (
        "Milestone Health Report:\n"
        "  Kickoff            [GREEN]  Completed on time\n"
        "  Design Complete    [YELLOW] Completed 7 days late\n"
        "  Alpha Release      [RED]    Overdue by 5 days\n"
        "  Beta Launch        [GREEN]  On track (41 days remaining)\n"
        "Overall: 1 RED, 1 YELLOW, 2 GREEN"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L08 — Critical Path Finder
# ─────────────────────────────────────────────────────────────────────────────
L08 = dict(
    **_BASE,
    level_order   = 8,
    title         = "Critical Path Finder",
    difficulty    = "hard",
    description   = (
        "El camino crítico determina la duración mínima del proyecto. "
        "Implementa `find_critical_path(tasks)` que calcula el camino más largo en un DAG.\n\n"
        "Cada tarea: `{'id': str, 'name': str, 'duration': int, 'deps': list[str]}`.\n\n"
        "Algoritmo:\n"
        "1. Ordena topológicamente las tareas.\n"
        "2. Para cada tarea, calcula `dist[id] = max(dist[dep] for dep in deps) + duration`.\n"
        "   Si no hay deps, `dist[id] = duration`.\n"
        "3. Reconstruye el camino desde la tarea con mayor dist hasta el origen.\n\n"
        "Imprime:\n"
        "`Critical Path: id1 → id2 → ...`\n"
        "`Duration: N days`\n"
        "`Tasks on path: name1, name2, ...`"
    ),
    hint          = "Guarda el predecesor de cada nodo durante el paso 2 para poder reconstruir el camino.",
    initial_code  = (
        "def find_critical_path(tasks):\n"
        "    pass\n\n"
        "tasks = [\n"
        "    {'id': 'A', 'name': 'Requirements', 'duration': 5,  'deps': []},\n"
        "    {'id': 'B', 'name': 'Design',        'duration': 8,  'deps': ['A']},\n"
        "    {'id': 'C', 'name': 'Backend dev',   'duration': 15, 'deps': ['B']},\n"
        "    {'id': 'D', 'name': 'Frontend dev',  'duration': 10, 'deps': ['B']},\n"
        "    {'id': 'E', 'name': 'Integration',   'duration': 5,  'deps': ['C', 'D']},\n"
        "    {'id': 'F', 'name': 'Testing',       'duration': 7,  'deps': ['E']},\n"
        "    {'id': 'G', 'name': 'Deployment',    'duration': 2,  'deps': ['F']},\n"
        "]\n"
        "find_critical_path(tasks)\n"
    ),
    expected_output = (
        "Critical Path: A → B → C → E → F → G\n"
        "Duration: 42 days\n"
        "Tasks on path: Requirements, Design, Backend dev, Integration, Testing, Deployment"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L09 — Stakeholder Quadrant Mapper
# ─────────────────────────────────────────────────────────────────────────────
L09 = dict(
    **_BASE,
    level_order   = 9,
    title         = "Stakeholder Quadrant Mapper",
    difficulty    = "easy",
    description   = (
        "La matriz poder/interés es la herramienta central del TPM para gestionar expectativas. "
        "Implementa `map_stakeholders(stakeholders)` que clasifica cada stakeholder en "
        "4 cuadrantes según `influence` (1-5) e `interest` (1-5).\n\n"
        "Cuadrantes (umbral: > 3 = alto, <= 3 = bajo):\n"
        "- influence > 3 y interest > 3 → `Manage Closely`\n"
        "- influence > 3 y interest <= 3 → `Keep Satisfied`\n"
        "- influence <= 3 y interest > 3 → `Keep Informed`\n"
        "- influence <= 3 y interest <= 3 → `Monitor`\n\n"
        "Imprime cada stakeholder:\n"
        "`[<quadrant padded 16>]  <name>  (influence=N, interest=N)`"
    ),
    hint          = "El umbral es estrictamente > 3, no >= 3.",
    initial_code  = (
        "def map_stakeholders(stakeholders):\n"
        "    pass\n\n"
        "stakeholders = [\n"
        "    {'name': 'CTO',           'influence': 5, 'interest': 5},\n"
        "    {'name': 'CFO',           'influence': 5, 'interest': 2},\n"
        "    {'name': 'Lead Engineer', 'influence': 3, 'interest': 5},\n"
        "    {'name': 'Support Team',  'influence': 2, 'interest': 4},\n"
        "    {'name': 'External User', 'influence': 1, 'interest': 2},\n"
        "]\n"
        "map_stakeholders(stakeholders)\n"
    ),
    expected_output = (
        "[Manage Closely]   CTO           (influence=5, interest=5)\n"
        "[Keep Satisfied]   CFO           (influence=5, interest=2)\n"
        "[Keep Informed]    Lead Engineer (influence=3, interest=5)\n"
        "[Keep Informed]    Support Team  (influence=2, interest=4)\n"
        "[Monitor]          External User (influence=1, interest=2)"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L10 — Sprint Capacity Planner
# ─────────────────────────────────────────────────────────────────────────────
L10 = dict(
    **_BASE,
    level_order   = 10,
    title         = "Sprint Capacity Planner",
    difficulty    = "medium",
    description   = (
        "Implementa `sprint_capacity_report(team, stories)` que evalúa si el trabajo "
        "planeado cabe en la capacidad del equipo.\n\n"
        "Cada miembro: `{'name': str, 'capacity': int}` (horas disponibles).\n"
        "Cada historia: `{'id': str, 'title': str, 'estimate': int}` (horas estimadas).\n\n"
        "Imprime:\n"
        "```\n"
        "Team Capacity: Nh\n"
        "  <name>: Nh\n"
        "Stories Planned: Nh\n"
        "  <id>: <title>  Nh\n"
        "Status: [OK — Xh remaining|OVERALLOCATED by Xh]\n"
        "```"
    ),
    hint          = "Suma todas las capacidades y todas las estimaciones, luego compara.",
    initial_code  = (
        "def sprint_capacity_report(team, stories):\n"
        "    pass\n\n"
        "team = [\n"
        "    {'name': 'Ana',   'capacity': 40},\n"
        "    {'name': 'Bruno', 'capacity': 35},\n"
        "    {'name': 'Cata',  'capacity': 30},\n"
        "]\n"
        "stories = [\n"
        "    {'id': 'US-01', 'title': 'Login page',         'estimate': 13},\n"
        "    {'id': 'US-02', 'title': 'User profile',        'estimate': 8},\n"
        "    {'id': 'US-03', 'title': 'Dashboard widget',    'estimate': 20},\n"
        "    {'id': 'US-04', 'title': 'API integration',     'estimate': 25},\n"
        "    {'id': 'US-05', 'title': 'Notification system', 'estimate': 40},\n"
        "]\n"
        "sprint_capacity_report(team, stories)\n"
    ),
    expected_output = (
        "Team Capacity: 105h\n"
        "  Ana: 40h\n"
        "  Bruno: 35h\n"
        "  Cata: 30h\n"
        "Stories Planned: 106h\n"
        "  US-01: Login page  13h\n"
        "  US-02: User profile  8h\n"
        "  US-03: Dashboard widget  20h\n"
        "  US-04: API integration  25h\n"
        "  US-05: Notification system  40h\n"
        "Status: OVERALLOCATED by 1h"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L11 — Meeting Cost Calculator
# ─────────────────────────────────────────────────────────────────────────────
L11 = dict(
    **_BASE,
    level_order   = 11,
    title         = "Meeting Cost Calculator",
    difficulty    = "medium",
    description   = (
        "Las reuniones tienen un costo real. Implementa `meeting_cost(meetings)` que "
        "calcula el costo monetario de cada reunión.\n\n"
        "Cada reunión: `{'title': str, 'duration_min': int, 'attendees': list[dict]}`.\n"
        "Cada attendee: `{'name': str, 'hourly_rate': float}`.\n\n"
        "Costo = suma de (hourly_rate × duration_min / 60) por asistente.\n\n"
        "Imprime por reunión:\n"
        "`<title> (<N> min, <M> attendees): $X.XX`\n\n"
        "Al final: `Total cost: $X.XX`"
    ),
    hint          = "duration_hours = duration_min / 60. Usa f'${cost:.2f}' para el formato.",
    initial_code  = (
        "def meeting_cost(meetings):\n"
        "    pass\n\n"
        "meetings = [\n"
        "    {'title': 'Sprint Planning', 'duration_min': 120, 'attendees': [\n"
        "        {'name': 'TPM',      'hourly_rate': 85},\n"
        "        {'name': 'PM',       'hourly_rate': 75},\n"
        "        {'name': 'Eng Lead', 'hourly_rate': 95},\n"
        "        {'name': 'Designer', 'hourly_rate': 65},\n"
        "        {'name': 'QA Lead',  'hourly_rate': 70},\n"
        "    ]},\n"
        "    {'title': 'Quick Sync', 'duration_min': 30, 'attendees': [\n"
        "        {'name': 'TPM', 'hourly_rate': 85},\n"
        "        {'name': 'Eng', 'hourly_rate': 80},\n"
        "    ]},\n"
        "]\n"
        "meeting_cost(meetings)\n"
    ),
    expected_output = (
        "Sprint Planning (120 min, 5 attendees): $780.00\n"
        "Quick Sync (30 min, 2 attendees): $82.50\n"
        "Total cost: $862.50"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L12 — Scope Change Detector
# ─────────────────────────────────────────────────────────────────────────────
L12 = dict(
    **_BASE,
    level_order   = 12,
    title         = "Scope Change Detector",
    difficulty    = "medium",
    description   = (
        "El scope creep es el enemigo silencioso del programa. "
        "Implementa `scope_change_report(baseline, current)` que compara dos listas de features.\n\n"
        "Clasifica cada item como:\n"
        "- UNCHANGED: en ambas listas\n"
        "- ADDED: solo en current\n"
        "- REMOVED: solo en baseline\n\n"
        "Imprime:\n"
        "```\n"
        "Scope Change Report:\n"
        "  UNCHANGED (N): item1, item2, ...\n"
        "  ADDED     (N): item1, item2, ...\n"
        "  REMOVED   (N): item1, item2, ...\n"
        "Scope creep: +N items added, -N items removed\n"
        "Baseline: N items  Current: N items  Delta: +N|-N|0\n"
        "```\n"
        "El Delta usa `+N` si creció, `-N` si decreció, `0` si igual."
    ),
    hint          = "Usa sets para calcular intersección, diferencia. Mantén el orden con list comprehension.",
    initial_code  = (
        "def scope_change_report(baseline, current):\n"
        "    pass\n\n"
        "baseline = ['Login', 'Register', 'Dashboard', 'Profile', 'Settings']\n"
        "current  = ['Login', 'Register', 'Dashboard', 'Analytics', 'Export', 'Notifications']\n"
        "scope_change_report(baseline, current)\n"
    ),
    expected_output = (
        "Scope Change Report:\n"
        "  UNCHANGED (3): Login, Register, Dashboard\n"
        "  ADDED     (3): Analytics, Export, Notifications\n"
        "  REMOVED   (2): Profile, Settings\n"
        "Scope creep: +3 items added, -2 items removed\n"
        "Baseline: 5 items  Current: 6 items  Delta: +1"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L13 — Program Status RAG
# ─────────────────────────────────────────────────────────────────────────────
L13 = dict(
    **_BASE,
    level_order   = 13,
    title         = "Program Status RAG Reporter",
    difficulty    = "medium",
    description   = (
        "El reporte RAG (Red/Amber/Green) es el artefacto de comunicación semanal del TPM. "
        "Implementa `program_rag_report(components)` que evalúa el estado por componente.\n\n"
        "Cada componente: `{'name': str, 'schedule': str, 'budget': str, 'quality': str}` "
        "(cada valor es 'RED', 'YELLOW' o 'GREEN').\n\n"
        "El estado del componente es el peor de sus 3 dimensiones "
        "(RED > YELLOW > GREEN).\n\n"
        "Imprime por componente:\n"
        "`  <name padded 16> S=<s>  B=<b>  Q=<q>  → <status>`\n\n"
        "El estado general del programa es el peor entre todos los componentes.\n"
        "Al final: `Overall: <STATUS>`"
    ),
    hint          = "Define un ranking: {'RED': 2, 'YELLOW': 1, 'GREEN': 0}. Usa max() con ese ranking.",
    initial_code  = (
        "def program_rag_report(components):\n"
        "    pass\n\n"
        "components = [\n"
        "    {'name': 'Backend API',    'schedule': 'GREEN',  'budget': 'GREEN',  'quality': 'GREEN'},\n"
        "    {'name': 'Frontend',       'schedule': 'YELLOW', 'budget': 'GREEN',  'quality': 'GREEN'},\n"
        "    {'name': 'Infra & DevOps', 'schedule': 'RED',    'budget': 'RED',    'quality': 'YELLOW'},\n"
        "    {'name': 'Mobile',         'schedule': 'GREEN',  'budget': 'YELLOW', 'quality': 'GREEN'},\n"
        "]\n"
        "program_rag_report(components)\n"
    ),
    expected_output = (
        "Program Status Report:\n"
        "  Backend API      S=GREEN  B=GREEN  Q=GREEN   → GREEN\n"
        "  Frontend         S=YELLOW B=GREEN  Q=GREEN   → YELLOW\n"
        "  Infra & DevOps   S=RED    B=RED    Q=YELLOW  → RED\n"
        "  Mobile           S=GREEN  B=YELLOW Q=GREEN   → YELLOW\n"
        "Overall: RED"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L14 — Assumptions Register
# ─────────────────────────────────────────────────────────────────────────────
L14 = dict(
    **_BASE,
    level_order   = 14,
    title         = "Assumptions Register",
    difficulty    = "hard",
    description   = (
        "Las suposiciones no validadas son riesgos ocultos. "
        "Implementa `assumptions_register(assumptions, today)` que gestiona el registro.\n\n"
        "Cada suposición: `{'id': str, 'description': str, 'risk': str, 'expires': str}`.\n"
        "`today` es un string ISO `'YYYY-MM-DD'`.\n\n"
        "Ordena por riesgo: high → medium → low. "
        "Dentro del mismo nivel, mantén el orden original.\n\n"
        "Marca como `[EXPIRED]` si `expires < today`.\n\n"
        "Formato por línea:\n"
        "`  [<risk padded 6>] <id>: <description>  expires=<date>[ [EXPIRED]]`\n\n"
        "Al final: `Expired assumptions: N`"
    ),
    hint          = "Define un orden de risk: {'high': 0, 'medium': 1, 'low': 2}. Usa sorted() con stable sort.",
    initial_code  = (
        "def assumptions_register(assumptions, today):\n"
        "    pass\n\n"
        "assumptions = [\n"
        "    {'id': 'A1', 'description': 'Vendor API remains backward compatible', 'risk': 'high',   'expires': '2024-06-01'},\n"
        "    {'id': 'A2', 'description': 'Team headcount stays at 8 engineers',    'risk': 'medium', 'expires': '2024-04-01'},\n"
        "    {'id': 'A3', 'description': 'No regulatory changes in Q2',            'risk': 'low',    'expires': '2024-06-30'},\n"
        "    {'id': 'A4', 'description': 'Cloud costs within approved budget',      'risk': 'medium', 'expires': '2024-03-01'},\n"
        "]\n"
        "assumptions_register(assumptions, '2024-03-20')\n"
    ),
    expected_output = (
        "Assumptions Register (as of 2024-03-20):\n"
        "  [high]   A1: Vendor API remains backward compatible  expires=2024-06-01\n"
        "  [medium] A2: Team headcount stays at 8 engineers    expires=2024-04-01\n"
        "  [medium] A4: Cloud costs within approved budget      expires=2024-03-01 [EXPIRED]\n"
        "  [low]    A3: No regulatory changes in Q2             expires=2024-06-30\n"
        "Expired assumptions: 1"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L15 — BOSS: Program Kickoff Report Generator
# ─────────────────────────────────────────────────────────────────────────────
L15 = dict(
    **_BASE_BOSS,
    level_order   = 15,
    title         = "CONTRATO-TPM-15: Program Kickoff Report Generator",
    difficulty    = "legendary",
    is_phase_boss = True,
    is_project    = True,
    description   = (
        "Prueba de fuego del TPM fundacional. Implementa la clase `ProgramKickoff` que "
        "genera el documento de lanzamiento oficial de un programa.\n\n"
        "Métodos requeridos:\n"
        "- `__init__(name, quarter)` — inicializa el programa\n"
        "- `add_okr(objective, key_results)` — agrega un OKR\n"
        "- `add_risk(id, desc, prob, impact)` — agrega un riesgo\n"
        "- `add_milestone(name, week)` — agrega un hito\n"
        "- `add_team_member(name, role, hours)` — agrega un miembro\n"
        "- `generate_report()` — imprime el reporte completo\n\n"
        "El reporte incluye: header, OKRs (con validación de KRs medibles), "
        "Top Risks (ordenados por score desc), Milestones, Team con capacidad total, "
        "y un STATUS final.\n\n"
        "STATUS: `NEEDS ATTENTION` si hay OKRs WEAK o riesgos CRITICAL; "
        "de lo contrario `READY`."
    ),
    hint          = (
        "Reutiliza la lógica de niveles anteriores: KR medible = tiene dígito. "
        "Risk score = prob × impact. CRITICAL si score >= 15."
    ),
    initial_code  = (
        "class ProgramKickoff:\n"
        "    def __init__(self, name, quarter):\n"
        "        self.name       = name\n"
        "        self.quarter    = quarter\n"
        "        self.okrs       = []\n"
        "        self.risks      = []\n"
        "        self.milestones = []\n"
        "        self.team       = []\n\n"
        "    def add_okr(self, objective, key_results):\n"
        "        pass\n\n"
        "    def add_risk(self, id, desc, prob, impact):\n"
        "        pass\n\n"
        "    def add_milestone(self, name, week):\n"
        "        pass\n\n"
        "    def add_team_member(self, name, role, hours):\n"
        "        pass\n\n"
        "    def generate_report(self):\n"
        "        pass\n\n\n"
        "pk = ProgramKickoff('DAKI EdTech Platform v3.0', 'Q2 2024')\n\n"
        "pk.add_okr('Scale to 50k active learners',\n"
        "           ['Reach 50000 MAU', 'Achieve 85% course completion rate', 'Launch mobile app'])\n"
        "pk.add_okr('Achieve platform excellence',\n"
        "           ['99.9% uptime SLA', 'Reduce p95 to 300ms', 'Zero critical incidents'])\n\n"
        "pk.add_risk('R1', 'DB scaling bottleneck',         prob=4, impact=5)\n"
        "pk.add_risk('R2', 'Key engineer departure',        prob=3, impact=4)\n"
        "pk.add_risk('R3', 'Scope creep from stakeholders', prob=5, impact=3)\n\n"
        "pk.add_milestone('Architecture review', week=2)\n"
        "pk.add_milestone('Alpha release',       week=6)\n"
        "pk.add_milestone('Beta launch',         week=10)\n"
        "pk.add_milestone('GA release',          week=14)\n\n"
        "pk.add_team_member('Ana Torres',  'Tech Lead',    40)\n"
        "pk.add_team_member('Bruno Rivas', 'Backend Eng',  40)\n"
        "pk.add_team_member('Carla Vega',  'Frontend Eng', 40)\n"
        "pk.add_team_member('Diego Mora',  'QA Engineer',  32)\n"
        "pk.add_team_member('Elena Park',  'Designer',     24)\n\n"
        "pk.generate_report()\n"
    ),
    expected_output = (
        "=== PROGRAM KICKOFF: DAKI EdTech Platform v3.0 | Q2 2024 ===\n"
        "\n"
        "OKRs:\n"
        "  O1: Scale to 50k active learners — 2/3 KRs measurable [WEAK]\n"
        "  O2: Achieve platform excellence — 2/3 KRs measurable [WEAK]\n"
        "  OKR health: 0/2 fully measurable\n"
        "\n"
        "Top Risks:\n"
        "  [CRITICAL] R1  score=20  DB scaling bottleneck\n"
        "  [CRITICAL] R3  score=15  Scope creep from stakeholders\n"
        "  [HIGH]     R2  score=12  Key engineer departure\n"
        "\n"
        "Milestones:\n"
        "  Week 2: Architecture review\n"
        "  Week 6: Alpha release\n"
        "  Week 10: Beta launch\n"
        "  Week 14: GA release\n"
        "\n"
        "Team (176h/sprint):\n"
        "  Ana Torres (Tech Lead): 40h\n"
        "  Bruno Rivas (Backend Eng): 40h\n"
        "  Carla Vega (Frontend Eng): 40h\n"
        "  Diego Mora (QA Engineer): 32h\n"
        "  Elena Park (Designer): 24h\n"
        "\n"
        "KICKOFF STATUS: NEEDS ATTENTION\n"
        "  - 0/2 OKRs fully measurable\n"
        "  - 2 critical risks identified"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
BLOQUE1 = [L01, L02, L03, L04, L05, L06, L07, L08, L09, L10, L11, L12, L13, L14, L15]
