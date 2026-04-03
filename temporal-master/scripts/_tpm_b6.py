"""
_tpm_b6.py — TPM Mastery · BLOQUE 6 (L76–L90)
===============================================
Fase: liderazgo_personas
Niveles: 76 a 90 (15 desafíos Python)
Boss: L90 — People Leadership Dashboard
"""
from __future__ import annotations

_BASE = dict(
    codex_id="tpm_mastery", sector_id=21, challenge_type="python",
    phase="liderazgo_personas", is_free=False, strict_match=False,
    is_phase_boss=False, is_project=False,
)
_BASE_BOSS = {k: v for k, v in _BASE.items() if k not in ("is_phase_boss", "is_project")}

L76 = dict(
    **_BASE, level_order=76, title="1-on-1 Agenda Builder", difficulty="easy",
    description=(
        "Las 1-on-1s estructuradas son la herramienta de liderazgo más poderosa. "
        "Implementa `one_on_one_agenda(report_name, topics)` donde cada topic tiene "
        "`{'category': str, 'item': str, 'time_min': int}`.\n\n"
        "Categorías: CAREER, FEEDBACK, BLOCKERS, WINS, FOCUS.\n\n"
        "Imprime el agenda agrupado por categoría en este orden: "
        "BLOCKERS → WINS → FEEDBACK → FOCUS → CAREER.\n\n"
        "Formato:\n"
        "`1-on-1: <report_name>  Total: Nmin`\n"
        "`─────────────────────────────`\n"
        "`[CATEGORY] (Nmin)`\n"
        "`  • <item>`\n"
        "Al final: `─────────────────────────────`"
    ),
    hint="Filtra topics por categoría en el orden fijo. Suma time_min por categoría.",
    initial_code=(
        "def one_on_one_agenda(report_name, topics):\n"
        "    pass\n\n"
        "one_on_one_agenda('Ana Torres', [\n"
        "    {'category': 'WINS',     'item': 'Auth module shipped early',          'time_min': 5},\n"
        "    {'category': 'BLOCKERS', 'item': 'Waiting on DB access from IT',       'time_min': 10},\n"
        "    {'category': 'FEEDBACK', 'item': 'Review PR turnaround speed',         'time_min': 10},\n"
        "    {'category': 'CAREER',   'item': 'Discuss Staff Engineer path',        'time_min': 15},\n"
        "    {'category': 'FOCUS',    'item': 'Q2 priorities alignment',            'time_min': 10},\n"
        "])\n"
    ),
    expected_output=(
        "1-on-1: Ana Torres  Total: 50min\n"
        "─────────────────────────────\n"
        "[BLOCKERS] (10min)\n"
        "  • Waiting on DB access from IT\n"
        "[WINS] (5min)\n"
        "  • Auth module shipped early\n"
        "[FEEDBACK] (10min)\n"
        "  • Review PR turnaround speed\n"
        "[FOCUS] (10min)\n"
        "  • Q2 priorities alignment\n"
        "[CAREER] (15min)\n"
        "  • Discuss Staff Engineer path\n"
        "─────────────────────────────"
    ),
)

L77 = dict(
    **_BASE, level_order=77, title="SBI Feedback Formatter", difficulty="medium",
    description=(
        "El modelo SBI (Situation-Behavior-Impact) es el estándar para dar feedback efectivo. "
        "Implementa `format_sbi(feedback_items)` que valida y formatea cada feedback.\n\n"
        "Cada item: `{'recipient': str, 'situation': str, 'behavior': str, "
        "'impact': str, 'type': str}` (type: 'positive'|'constructive').\n\n"
        "Valida que situation, behavior e impact sean no vacíos. "
        "Si alguno está vacío: marca `[INCOMPLETE]`.\n\n"
        "Formato por item:\n"
        "`[POSITIVE|CONSTRUCTIVE] → <recipient>`\n"
        "`  Situation: <situation>`\n"
        "`  Behavior:  <behavior>`\n"
        "`  Impact:    <impact>`\n\n"
        "Al final: `Feedback ready: N  Incomplete: N`"
    ),
    hint="Chequea if not situation or not behavior or not impact para marcar INCOMPLETE.",
    initial_code=(
        "def format_sbi(feedback_items):\n"
        "    pass\n\n"
        "format_sbi([\n"
        "    {'recipient': 'Bruno', 'type': 'positive',\n"
        "     'situation': 'During the auth incident on Monday',\n"
        "     'behavior':  'you stayed calm and led the war room effectively',\n"
        "     'impact':    'the team resolved it 40% faster than our last P1'},\n"
        "    {'recipient': 'Diego', 'type': 'constructive',\n"
        "     'situation': 'In last week sprint review',\n"
        "     'behavior':  'you interrupted the PM three times',\n"
        "     'impact':    'it made the PM feel unheard and slowed the discussion'},\n"
        "    {'recipient': 'Cata', 'type': 'constructive',\n"
        "     'situation': '',\n"
        "     'behavior':  'misses deadlines',\n"
        "     'impact':    ''},\n"
        "])\n"
    ),
    expected_output=(
        "[POSITIVE] → Bruno\n"
        "  Situation: During the auth incident on Monday\n"
        "  Behavior:  you stayed calm and led the war room effectively\n"
        "  Impact:    the team resolved it 40% faster than our last P1\n"
        "[CONSTRUCTIVE] → Diego\n"
        "  Situation: In last week sprint review\n"
        "  Behavior:  you interrupted the PM three times\n"
        "  Impact:    it made the PM feel unheard and slowed the discussion\n"
        "[INCOMPLETE] → Cata\n"
        "  Situation: (missing)\n"
        "  Behavior:  misses deadlines\n"
        "  Impact:    (missing)\n"
        "Feedback ready: 2  Incomplete: 1"
    ),
)

L78 = dict(
    **_BASE, level_order=78, title="Hiring Scorecard", difficulty="medium",
    description=(
        "Implementa `hiring_scorecard(candidates, competencies)` que puntúa candidatos.\n\n"
        "Cada candidato: `{'name': str, 'scores': dict}` (competencia → score 1-5).\n"
        "Cada competencia: `{'name': str, 'weight': float}` (pesos suman 1.0).\n\n"
        "Weighted score = sum(score * weight) (2 dec).\n\n"
        "Imprime ordenado por score desc:\n"
        "`N. <name>: score=X.XX  [STRONG HIRE|HIRE|NO HIRE]`\n"
        "`   <competencia>=N  ...`\n\n"
        "STRONG HIRE si score >= 4.0, HIRE si >= 3.0, NO HIRE si < 3.0.\n\n"
        "Al final: `Recommendation: <nombre del primero>`"
    ),
    hint="Itera competencias en orden dado para la línea de scores.",
    initial_code=(
        "def hiring_scorecard(candidates, competencies):\n"
        "    pass\n\n"
        "competencies = [\n"
        "    {'name': 'technical',    'weight': 0.35},\n"
        "    {'name': 'communication','weight': 0.25},\n"
        "    {'name': 'ownership',    'weight': 0.20},\n"
        "    {'name': 'collaboration','weight': 0.20},\n"
        "]\n"
        "candidates = [\n"
        "    {'name': 'Laura M.', 'scores': {'technical': 5, 'communication': 4, 'ownership': 5, 'collaboration': 4}},\n"
        "    {'name': 'Pedro R.', 'scores': {'technical': 4, 'communication': 5, 'ownership': 3, 'collaboration': 5}},\n"
        "    {'name': 'Sofia K.', 'scores': {'technical': 3, 'communication': 3, 'ownership': 2, 'collaboration': 3}},\n"
        "]\n"
        "hiring_scorecard(candidates, competencies)\n"
    ),
    expected_output=(
        "1. Laura M.: score=4.60  [STRONG HIRE]\n"
        "   technical=5  communication=4  ownership=5  collaboration=4\n"
        "2. Pedro R.: score=4.25  [STRONG HIRE]\n"
        "   technical=4  communication=5  ownership=3  collaboration=5\n"
        "3. Sofia K.: score=2.85  [NO HIRE]\n"
        "   technical=3  communication=3  ownership=2  collaboration=3\n"
        "Recommendation: Laura M."
    ),
)

L79 = dict(
    **_BASE, level_order=79, title="Performance Review Builder", difficulty="hard",
    description=(
        "Implementa `performance_review(employee)` que genera una reseña de desempeño.\n\n"
        "employee: `{'name': str, 'role': str, 'period': str, "
        "'dimensions': list[dict], 'okr_completion_pct': float, 'highlights': list[str], "
        "'growth_areas': list[str]}`.\n\n"
        "Cada dimensión: `{'name': str, 'score': int, 'evidence': str}` (score 1-5).\n\n"
        "Overall score = promedio de dimensiones (2 dec).\n"
        "Rating: >= 4.5 → Exceptional, >= 3.5 → Strong, >= 2.5 → Meeting Expectations, "
        "< 2.5 → Needs Improvement.\n\n"
        "Imprime: header, dimensiones con score y evidencia, OKR completion, "
        "highlights, growth areas y rating final."
    ),
    hint="Promedio = sum(scores)/len(dimensions). Rating por comparación >= en orden descendente.",
    initial_code=(
        "def performance_review(employee):\n"
        "    pass\n\n"
        "performance_review({\n"
        "    'name': 'Ana Torres', 'role': 'Senior Engineer', 'period': 'H1 2024',\n"
        "    'dimensions': [\n"
        "        {'name': 'Technical Impact',  'score': 5, 'evidence': 'Led auth refactor, 40% perf gain'},\n"
        "        {'name': 'Collaboration',     'score': 4, 'evidence': 'Mentored 2 juniors effectively'},\n"
        "        {'name': 'Delivery',          'score': 4, 'evidence': 'Shipped 100% of committed stories'},\n"
        "        {'name': 'Communication',     'score': 3, 'evidence': 'Docs improved but still gaps'},\n"
        "    ],\n"
        "    'okr_completion_pct': 92,\n"
        "    'highlights': ['Auth module early delivery', 'Zero P1 incidents in owned services'],\n"
        "    'growth_areas': ['Technical writing', 'Cross-team visibility'],\n"
        "})\n"
    ),
    expected_output=(
        "PERFORMANCE REVIEW: Ana Torres  |  Senior Engineer  |  H1 2024\n"
        "══════════════════════════════════════════════════\n"
        "DIMENSIONS:\n"
        "  Technical Impact  [5/5] Led auth refactor, 40% perf gain\n"
        "  Collaboration     [4/5] Mentored 2 juniors effectively\n"
        "  Delivery          [4/5] Shipped 100% of committed stories\n"
        "  Communication     [3/5] Docs improved but still gaps\n"
        "\n"
        "OKR Completion: 92%\n"
        "\n"
        "HIGHLIGHTS:\n"
        "  ★ Auth module early delivery\n"
        "  ★ Zero P1 incidents in owned services\n"
        "\n"
        "GROWTH AREAS:\n"
        "  → Technical writing\n"
        "  → Cross-team visibility\n"
        "\n"
        "Overall Score: 4.00  |  Rating: Strong"
    ),
)

L80 = dict(
    **_BASE, level_order=80, title="Team Health Pulse", difficulty="medium",
    description=(
        "Implementa `team_health_pulse(survey_results)` que analiza el pulso del equipo.\n\n"
        "Cada resultado: `{'name': str, 'scores': dict}` donde scores tiene "
        "las dimensiones: motivation, clarity, collaboration, workload, growth.\n"
        "Cada score es 1-5.\n\n"
        "Para cada dimensión calcula el promedio del equipo (1 dec).\n"
        "Label: >= 4.0 → Healthy, >= 3.0 → Neutral, < 3.0 → At Risk.\n\n"
        "Imprime por dimensión (ordenadas):\n"
        "`  <dimension padded 14>: X.X/5  [label]  <barra █/░ de 5>`\n\n"
        "Al final:\n"
        "`Team average: X.X/5`\n"
        "`At Risk: <dimensiones separadas por coma, o 'none'>`"
    ),
    hint="Barra = '█' * round(avg) + '░' * (5 - round(avg)).",
    initial_code=(
        "def team_health_pulse(survey_results):\n"
        "    pass\n\n"
        "survey_results = [\n"
        "    {'name': 'Ana',   'scores': {'motivation': 5, 'clarity': 4, 'collaboration': 5, 'workload': 3, 'growth': 4}},\n"
        "    {'name': 'Bruno', 'scores': {'motivation': 4, 'clarity': 3, 'collaboration': 4, 'workload': 2, 'growth': 3}},\n"
        "    {'name': 'Cata',  'scores': {'motivation': 3, 'clarity': 4, 'collaboration': 4, 'workload': 2, 'growth': 4}},\n"
        "    {'name': 'Diego', 'scores': {'motivation': 4, 'clarity': 3, 'collaboration': 5, 'workload': 3, 'growth': 3}},\n"
        "]\n"
        "team_health_pulse(survey_results)\n"
    ),
    expected_output=(
        "  clarity      : 3.5/5  [Neutral]  ████░\n"
        "  collaboration: 4.5/5  [Healthy]  █████\n"
        "  growth       : 3.5/5  [Neutral]  ████░\n"
        "  motivation   : 4.0/5  [Healthy]  ████░\n"
        "  workload     : 2.5/5  [At Risk]  ███░░\n"
        "Team average: 3.6/5\n"
        "At Risk: workload"
    ),
)

L81 = dict(
    **_BASE, level_order=81, title="Career Ladder Mapper", difficulty="hard",
    description=(
        "Implementa `career_ladder_map(engineer)` que mapea las habilidades de un "
        "ingeniero a un nivel de carrera y detecta brechas.\n\n"
        "engineer: `{'name': str, 'skills': dict}` donde skills es skill→score (1-5).\n\n"
        "Niveles y requisitos mínimos (todos los skills deben cumplir):\n"
        "- Staff (L6):  technical>=5, leadership>=4, scope>=4, communication>=4\n"
        "- Senior (L5): technical>=4, leadership>=3, scope>=3, communication>=3\n"
        "- Mid (L4):    technical>=3, leadership>=2, scope>=2, communication>=2\n"
        "- Junior (L3): cualquier score\n\n"
        "El nivel actual es el más alto que cumple todos los requisitos.\n\n"
        "Imprime scores, nivel actual, y gaps para el siguiente nivel."
    ),
    hint="Evalúa de Staff hacia abajo. El primer nivel que cumple todos es el actual.",
    initial_code=(
        "def career_ladder_map(engineer):\n"
        "    pass\n\n"
        "LEVELS = [\n"
        "    ('Staff (L6)',  {'technical': 5, 'leadership': 4, 'scope': 4, 'communication': 4}),\n"
        "    ('Senior (L5)', {'technical': 4, 'leadership': 3, 'scope': 3, 'communication': 3}),\n"
        "    ('Mid (L4)',    {'technical': 3, 'leadership': 2, 'scope': 2, 'communication': 2}),\n"
        "    ('Junior (L3)', {}),\n"
        "]\n"
        "career_ladder_map({\n"
        "    'name': 'Bruno Rivas',\n"
        "    'skills': {'technical': 4, 'leadership': 3, 'scope': 3, 'communication': 2},\n"
        "})\n"
    ),
    expected_output=(
        "Career Map: Bruno Rivas\n"
        "  technical=4  leadership=3  scope=3  communication=2\n"
        "\n"
        "Current level: Senior (L5)\n"
        "\n"
        "Gaps to Staff (L6):\n"
        "  technical:    4 → need 5  (gap: 1)\n"
        "  communication: 2 → need 4  (gap: 2)"
    ),
)

L82 = dict(
    **_BASE, level_order=82, title="Onboarding Plan Generator", difficulty="medium",
    description=(
        "Implementa `onboarding_plan(role, start_week, milestones)` que genera "
        "el plan de incorporación.\n\n"
        "Cada milestone: `{'week': int, 'title': str, 'deliverable': str, 'support': str}`.\n\n"
        "Imprime:\n"
        "`Onboarding Plan: <role>  Start: Week <start_week>`\n"
        "`════════════════════════════════`\n"
        "Por milestone:\n"
        "`Week N: <title>`\n"
        "`  Deliverable: <deliverable>`\n"
        "`  Support:     <support>`\n"
        "`════════════════════════════════`\n"
        "`Total milestones: N  |  Duration: N weeks`\n\n"
        "Duración = semana del último milestone - start_week + 1."
    ),
    hint="Itera milestones en orden. Duración = last_week - start_week + 1.",
    initial_code=(
        "def onboarding_plan(role, start_week, milestones):\n"
        "    pass\n\n"
        "onboarding_plan('Senior TPM', start_week=1, milestones=[\n"
        "    {'week': 1, 'title': 'Company & Team Context',\n"
        "     'deliverable': 'Read all strategy docs',       'support': 'Manager 1-on-1 daily'},\n"
        "    {'week': 2, 'title': 'Shadow Active Programs',\n"
        "     'deliverable': 'Status report draft',          'support': 'Buddy TPM'},\n"
        "    {'week': 4, 'title': 'Own First Workstream',\n"
        "     'deliverable': 'Run weekly sync independently', 'support': 'Manager check-in'},\n"
        "    {'week': 8, 'title': 'Full Program Ownership',\n"
        "     'deliverable': 'Program kickoff doc approved',  'support': 'Peer review'},\n"
        "])\n"
    ),
    expected_output=(
        "Onboarding Plan: Senior TPM  Start: Week 1\n"
        "════════════════════════════════\n"
        "Week 1: Company & Team Context\n"
        "  Deliverable: Read all strategy docs\n"
        "  Support:     Manager 1-on-1 daily\n"
        "Week 2: Shadow Active Programs\n"
        "  Deliverable: Status report draft\n"
        "  Support:     Buddy TPM\n"
        "Week 4: Own First Workstream\n"
        "  Deliverable: Run weekly sync independently\n"
        "  Support:     Manager check-in\n"
        "Week 8: Full Program Ownership\n"
        "  Deliverable: Program kickoff doc approved\n"
        "  Support:     Peer review\n"
        "════════════════════════════════\n"
        "Total milestones: 4  |  Duration: 8 weeks"
    ),
)

L83 = dict(
    **_BASE, level_order=83, title="Team Skills Matrix", difficulty="hard",
    description=(
        "Implementa `skills_matrix(team, required_skills)` que identifica cobertura y brechas.\n\n"
        "team: lista de `{'name': str, 'skills': list[str]}`.\n"
        "required_skills: lista de strings.\n\n"
        "Para cada skill requerido muestra quién lo tiene y el nivel de cobertura.\n\n"
        "Imprime:\n"
        "`SKILLS MATRIX`\n"
        "`<skill padded 20>: coverage=N/M  owners: <name1, name2|NONE>`\n"
        "`  [COVERED|AT RISK|CRITICAL]`\n\n"
        "COVERED si coverage >= 2, AT RISK si coverage == 1, CRITICAL si coverage == 0.\n\n"
        "Al final:\n"
        "`Critical gaps: <skills separadas por coma|none>`\n"
        "`Bus factor risks: <skills con coverage==1 separadas por coma|none>`"
    ),
    hint="Itera required_skills. Para cada una, filtra team members que la tienen.",
    initial_code=(
        "def skills_matrix(team, required_skills):\n"
        "    pass\n\n"
        "team = [\n"
        "    {'name': 'Ana',   'skills': ['Python', 'Playwright', 'API testing', 'CI/CD']},\n"
        "    {'name': 'Bruno', 'skills': ['Python', 'TypeScript', 'API testing']},\n"
        "    {'name': 'Cata',  'skills': ['TypeScript', 'Playwright', 'Performance']},\n"
        "    {'name': 'Diego', 'skills': ['Python', 'CI/CD', 'Docker']},\n"
        "]\n"
        "skills_matrix(team, ['Python', 'TypeScript', 'Playwright', 'Performance', 'Security', 'CI/CD'])\n"
    ),
    expected_output=(
        "SKILLS MATRIX\n"
        "Python              : coverage=3/4  owners: Ana, Bruno, Diego\n"
        "  [COVERED]\n"
        "TypeScript          : coverage=2/4  owners: Bruno, Cata\n"
        "  [COVERED]\n"
        "Playwright          : coverage=2/4  owners: Ana, Cata\n"
        "  [COVERED]\n"
        "Performance         : coverage=1/4  owners: Cata\n"
        "  [AT RISK]\n"
        "Security            : coverage=0/4  owners: NONE\n"
        "  [CRITICAL]\n"
        "CI/CD               : coverage=2/4  owners: Ana, Diego\n"
        "  [COVERED]\n"
        "Critical gaps: Security\n"
        "Bus factor risks: Performance"
    ),
)

L84 = dict(
    **_BASE, level_order=84, title="Recognition Tracker", difficulty="easy",
    description=(
        "Implementa `recognition_report(recognitions)` que genera el reporte mensual de reconocimientos.\n\n"
        "Cada reconocimiento: `{'recipient': str, 'nominator': str, "
        "'category': str, 'description': str}`.\n\n"
        "Categorías: INNOVATION, DELIVERY, COLLABORATION, LEADERSHIP, QUALITY.\n\n"
        "Imprime agrupado por categoría:\n"
        "`[<CATEGORY>]`\n"
        "`  🏆 <recipient> (nominated by <nominator>)`\n"
        "`     <description>`\n\n"
        "Al final:\n"
        "`Total recognitions: N  |  Most recognized: <nombre con más reconocimientos>`"
    ),
    hint="Agrupa en dict de categoría→lista. Para 'most recognized' usa un Counter.",
    initial_code=(
        "def recognition_report(recognitions):\n"
        "    pass\n\n"
        "recognition_report([\n"
        "    {'recipient': 'Ana',   'nominator': 'Bruno', 'category': 'DELIVERY',      'description': 'Shipped auth 2 days early'},\n"
        "    {'recipient': 'Bruno', 'nominator': 'Ana',   'category': 'COLLABORATION', 'description': 'Helped 3 teammates unblock'},\n"
        "    {'recipient': 'Ana',   'nominator': 'Diego', 'category': 'QUALITY',       'description': 'Zero regressions in Q1'},\n"
        "    {'recipient': 'Cata',  'nominator': 'Ana',   'category': 'INNOVATION',    'description': 'Proposed automated visual testing'},\n"
        "])\n"
    ),
    expected_output=(
        "[COLLABORATION]\n"
        "  🏆 Bruno (nominated by Ana)\n"
        "     Helped 3 teammates unblock\n"
        "[DELIVERY]\n"
        "  🏆 Ana (nominated by Bruno)\n"
        "     Shipped auth 2 days early\n"
        "[INNOVATION]\n"
        "  🏆 Cata (nominated by Ana)\n"
        "     Proposed automated visual testing\n"
        "[QUALITY]\n"
        "  🏆 Ana (nominated by Diego)\n"
        "     Zero regressions in Q1\n"
        "Total recognitions: 4  |  Most recognized: Ana"
    ),
)

L85 = dict(
    **_BASE, level_order=85, title="Coaching Session Planner", difficulty="medium",
    description=(
        "Implementa `coaching_plan(coachee)` que genera un plan de coaching estructurado "
        "usando el modelo GROW (Goal-Reality-Options-Way Forward).\n\n"
        "coachee: `{'name': str, 'goal': str, 'current_reality': str, "
        "'obstacles': list[str], 'options': list[str], 'commitment': str, 'by_date': str}`.\n\n"
        "Formato:\n"
        "`COACHING SESSION — <name>`\n"
        "`GOAL:`\n"
        "`  <goal>`\n"
        "`REALITY:`\n"
        "`  <current_reality>`\n"
        "`OBSTACLES:`\n"
        "`  • <obstacle>`\n"
        "`OPTIONS:`\n"
        "`  N. <option>`\n"
        "`WAY FORWARD:`\n"
        "`  Commitment: <commitment>`\n"
        "`  By: <by_date>`"
    ),
    hint="Obstáculos con '•', opciones numeradas. Secciones separadas por línea vacía.",
    initial_code=(
        "def coaching_plan(coachee):\n"
        "    pass\n\n"
        "coaching_plan({\n"
        "    'name': 'Diego Mora',\n"
        "    'goal': 'Lead a full QA strategy for the mobile app independently',\n"
        "    'current_reality': 'Can execute test plans but needs guidance on strategy',\n"
        "    'obstacles': ['Limited exposure to mobile testing tools', 'Low confidence presenting to stakeholders'],\n"
        "    'options': ['Shadow Ana on next mobile sprint', 'Take Appium course this month', 'Present at next team demo'],\n"
        "    'commitment': 'Complete Appium course and shadow Ana for 2 sprints',\n"
        "    'by_date': '2024-05-15',\n"
        "})\n"
    ),
    expected_output=(
        "COACHING SESSION — Diego Mora\n"
        "\n"
        "GOAL:\n"
        "  Lead a full QA strategy for the mobile app independently\n"
        "\n"
        "REALITY:\n"
        "  Can execute test plans but needs guidance on strategy\n"
        "\n"
        "OBSTACLES:\n"
        "  • Limited exposure to mobile testing tools\n"
        "  • Low confidence presenting to stakeholders\n"
        "\n"
        "OPTIONS:\n"
        "  1. Shadow Ana on next mobile sprint\n"
        "  2. Take Appium course this month\n"
        "  3. Present at next team demo\n"
        "\n"
        "WAY FORWARD:\n"
        "  Commitment: Complete Appium course and shadow Ana for 2 sprints\n"
        "  By: 2024-05-15"
    ),
)

L86 = dict(
    **_BASE, level_order=86, title="Conflict Resolution Analyzer", difficulty="hard",
    description=(
        "Implementa `analyze_conflict(conflict)` que clasifica un conflicto y sugiere resolución.\n\n"
        "conflict: `{'parties': list[str], 'description': str, "
        "'type': str, 'intensity': int, 'shared_goal': str}`.\n\n"
        "Types: 'task' (sobre trabajo), 'process' (sobre cómo trabajar), 'relationship' (interpersonal).\n"
        "Intensity: 1-5.\n\n"
        "Estrategia de resolución:\n"
        "- task + intensity<=3 → Facilitate structured discussion\n"
        "- task + intensity>3  → Mediated problem solving\n"
        "- process + any       → Process redesign workshop\n"
        "- relationship + intensity<=3 → 1-on-1 coaching sessions\n"
        "- relationship + intensity>3  → HR involvement recommended\n\n"
        "Imprime el análisis completo con partes, tipo, intensidad, estrategia y próximo paso."
    ),
    hint="Evalúa type primero, luego intensity dentro de cada type.",
    initial_code=(
        "def analyze_conflict(conflict):\n"
        "    pass\n\n"
        "analyze_conflict({\n"
        "    'parties': ['Ana Torres', 'Bruno Rivas'],\n"
        "    'description': 'Disagreement on API design ownership and review process',\n"
        "    'type': 'process',\n"
        "    'intensity': 3,\n"
        "    'shared_goal': 'Ship reliable APIs on time',\n"
        "})\n"
    ),
    expected_output=(
        "CONFLICT ANALYSIS\n"
        "Parties: Ana Torres, Bruno Rivas\n"
        "Type: process  |  Intensity: 3/5\n"
        "Description: Disagreement on API design ownership and review process\n"
        "\n"
        "Shared goal: Ship reliable APIs on time\n"
        "\n"
        "Strategy: Process redesign workshop\n"
        "Next step: Schedule 90-min session to co-design the API review workflow\n"
        "Resolution odds: HIGH (shared goal identified, intensity manageable)"
    ),
)

L87 = dict(
    **_BASE, level_order=87, title="Team Capacity Monitor", difficulty="medium",
    description=(
        "Implementa `capacity_monitor(team_members)` que detecta riesgos de sobrecarga.\n\n"
        "Cada miembro: `{'name': str, 'allocated_pct': int, 'pto_days': int, 'sprint_days': int}`.\n\n"
        "Effective capacity = 100% - (pto_days/sprint_days * 100) en %.\n"
        "Utilization = allocated_pct / effective_capacity * 100 (1 dec).\n\n"
        "Riesgo: utilization > 110% → OVERLOADED, 90-110% → OPTIMAL, < 90% → UNDERUTILIZED.\n\n"
        "Imprime por miembro:\n"
        "`  <name padded 12>: alloc=X%  eff_capacity=X%  utilization=X%  [RIESGO]`\n\n"
        "Al final:\n"
        "`Team risk: N overloaded  N optimal  N underutilized`"
    ),
    hint="eff_capacity = 100 - (pto_days/sprint_days*100). utilization = allocated/eff*100.",
    initial_code=(
        "def capacity_monitor(team_members):\n"
        "    pass\n\n"
        "capacity_monitor([\n"
        "    {'name': 'Ana',   'allocated_pct': 100, 'pto_days': 0, 'sprint_days': 10},\n"
        "    {'name': 'Bruno', 'allocated_pct': 90,  'pto_days': 2, 'sprint_days': 10},\n"
        "    {'name': 'Cata',  'allocated_pct': 80,  'pto_days': 0, 'sprint_days': 10},\n"
        "    {'name': 'Diego', 'allocated_pct': 110, 'pto_days': 1, 'sprint_days': 10},\n"
        "])\n"
    ),
    expected_output=(
        "  Ana:         alloc=100%  eff_capacity=100%  utilization=100.0%  OPTIMAL\n"
        "  Bruno:       alloc=90%   eff_capacity=80%   utilization=112.5%  OVERLOADED\n"
        "  Cata:        alloc=80%   eff_capacity=100%  utilization=80.0%   UNDERUTILIZED\n"
        "  Diego:       alloc=110%  eff_capacity=90%   utilization=122.2%  OVERLOADED\n"
        "Team risk: 2 overloaded  1 optimal  1 underutilized"
    ),
)

L88 = dict(
    **_BASE, level_order=88, title="Skip-Level Interview Planner", difficulty="medium",
    description=(
        "Implementa `skip_level_plan(reports)` que genera guías de entrevista skip-level.\n\n"
        "Cada report: `{'name': str, 'role': str, 'tenure_months': int, 'recent_concern': str}`.\n\n"
        "Genera 3 preguntas por persona adaptadas a:\n"
        "- tenure < 6 meses: enfoque en onboarding y clarity\n"
        "- tenure 6-18 meses: enfoque en growth y blockers\n"
        "- tenure > 18 meses: enfoque en retention y leadership\n\n"
        "Incluye la concern como contexto si está presente.\n\n"
        "Formato:\n"
        "`Skip-Level Guide: <name> (<role>)`\n"
        "`  Focus: <onboarding|growth|retention>`\n"
        "`  Context: <concern|none>`\n"
        "`  Q1: <pregunta>`\n"
        "`  Q2: <pregunta>`\n"
        "`  Q3: <pregunta>`\n"
    ),
    hint="Define listas de preguntas por tenure bracket. Selecciona las 3 primeras.",
    initial_code=(
        "QUESTIONS = {\n"
        "    'onboarding': [\n"
        "        'What has been clearest/most confusing about your first weeks?',\n"
        "        'Do you have what you need to be effective?',\n"
        "        'What would have made onboarding better?',\n"
        "    ],\n"
        "    'growth': [\n"
        "        'What are you most proud of in the last quarter?',\n"
        "        'What is slowing you down or blocking your growth?',\n"
        "        'Is there a skill or area you want to develop more?',\n"
        "    ],\n"
        "    'retention': [\n"
        "        'What keeps you energized and engaged here?',\n"
        "        'Is there anything that would make you consider leaving?',\n"
        "        'Where do you see yourself in 2 years?',\n"
        "    ],\n"
        "}\n\n"
        "def skip_level_plan(reports):\n"
        "    pass\n\n"
        "skip_level_plan([\n"
        "    {'name': 'Luca',  'role': 'QA Engineer',    'tenure_months': 3,  'recent_concern': 'Unclear about team priorities'},\n"
        "    {'name': 'Sofia', 'role': 'Backend Engineer','tenure_months': 12, 'recent_concern': ''},\n"
        "])\n"
    ),
    expected_output=(
        "Skip-Level Guide: Luca (QA Engineer)\n"
        "  Focus: onboarding\n"
        "  Context: Unclear about team priorities\n"
        "  Q1: What has been clearest/most confusing about your first weeks?\n"
        "  Q2: Do you have what you need to be effective?\n"
        "  Q3: What would have made onboarding better?\n"
        "Skip-Level Guide: Sofia (Backend Engineer)\n"
        "  Focus: growth\n"
        "  Context: none\n"
        "  Q1: What are you most proud of in the last quarter?\n"
        "  Q2: What is slowing you down or blocking your growth?\n"
        "  Q3: Is there a skill or area you want to develop more?"
    ),
)

L89 = dict(
    **_BASE, level_order=89, title="Manager Effectiveness Scorer", difficulty="hard",
    description=(
        "Implementa `manager_score(feedback_data)` que evalúa la efectividad de un manager "
        "a partir de feedback 360.\n\n"
        "feedback_data: `{'manager': str, 'self_scores': dict, "
        "'report_scores': list[dict], 'peer_scores': list[dict]}`.\n\n"
        "Cada scores dict tiene: communication, technical, delegation, "
        "development, delivery (1-5).\n\n"
        "Calcula promedio por fuente (self, reports, peers) y por dimensión.\n"
        "Identifica gaps: dimensiones donde self > avg_reports + 1 (blind spots).\n\n"
        "Imprime: scores por fuente, promedios por dimensión, blind spots, "
        "y recomendación de desarrollo."
    ),
    hint="avg_reports = promedio de todos los report_scores para cada dimensión.",
    initial_code=(
        "def manager_score(feedback_data):\n"
        "    pass\n\n"
        "feedback_data = {\n"
        "    'manager': 'Maria Chen',\n"
        "    'self_scores':   {'communication': 5, 'technical': 4, 'delegation': 4, 'development': 5, 'delivery': 5},\n"
        "    'report_scores': [\n"
        "        {'communication': 3, 'technical': 4, 'delegation': 2, 'development': 3, 'delivery': 4},\n"
        "        {'communication': 4, 'technical': 4, 'delegation': 3, 'development': 4, 'delivery': 5},\n"
        "    ],\n"
        "    'peer_scores': [\n"
        "        {'communication': 4, 'technical': 4, 'delegation': 3, 'development': 4, 'delivery': 5},\n"
        "    ],\n"
        "}\n"
        "manager_score(feedback_data)\n"
    ),
    expected_output=(
        "360 Feedback: Maria Chen\n"
        "──────────────────────────────────\n"
        "             Self  Reports  Peers\n"
        "communication  5.0    3.5    4.0\n"
        "technical      4.0    4.0    4.0\n"
        "delegation     4.0    2.5    3.0\n"
        "development    5.0    3.5    4.0\n"
        "delivery       5.0    4.5    5.0\n"
        "──────────────────────────────────\n"
        "Blind spots (self scores > reports avg + 1):\n"
        "  delegation: self=4.0 vs reports=2.5\n"
        "  communication: self=5.0 vs reports=3.5\n"
        "  development: self=5.0 vs reports=3.5\n"
        "Development focus: delegation, communication"
    ),
)

L90 = dict(
    **_BASE_BOSS, level_order=90,
    title="CONTRATO-TPM-90: People Leadership Dashboard",
    difficulty="legendary", is_phase_boss=True, is_project=True,
    description=(
        "Implementa `PeopleLeadershipDashboard` que integra todas las dimensiones de liderazgo.\n\n"
        "Métodos:\n"
        "- `add_member(name, performance_score, health_score, capacity_pct)`\n"
        "  performance_score y health_score: 1-5. capacity_pct: porcentaje de carga.\n"
        "- `add_open_role(title, priority)` — roles abiertos a contratar\n"
        "- `generate_report()` — imprime el dashboard\n\n"
        "El dashboard muestra:\n"
        "1. Cada miembro con semáforo: RED si perf<3 o health<3 o capacity>110, YELLOW si cualquier valor borderline (perf==3 o health==3 o capacity>95), GREEN si todo OK\n"
        "2. Team averages\n"
        "3. Open roles\n"
        "4. Overall team status y recomendaciones principales"
    ),
    hint="Borderline: perf==3 o health==3 o 95<capacity<=110. Acumula contadores para el summary.",
    initial_code=(
        "class PeopleLeadershipDashboard:\n"
        "    def __init__(self):\n"
        "        self.members    = []\n"
        "        self.open_roles = []\n\n"
        "    def add_member(self, name, performance_score, health_score, capacity_pct):\n"
        "        pass\n\n"
        "    def add_open_role(self, title, priority):\n"
        "        pass\n\n"
        "    def generate_report(self):\n"
        "        pass\n\n\n"
        "pld = PeopleLeadershipDashboard()\n"
        "pld.add_member('Ana',   performance_score=5, health_score=4, capacity_pct=100)\n"
        "pld.add_member('Bruno', performance_score=4, health_score=3, capacity_pct=112)\n"
        "pld.add_member('Cata',  performance_score=3, health_score=4, capacity_pct=85)\n"
        "pld.add_member('Diego', performance_score=4, health_score=5, capacity_pct=90)\n"
        "pld.add_open_role('Senior QA Engineer', priority='HIGH')\n"
        "pld.add_open_role('DevOps Engineer',    priority='MEDIUM')\n"
        "pld.generate_report()\n"
    ),
    expected_output=(
        "╔══════════════════════════════════════╗\n"
        "║  PEOPLE LEADERSHIP DASHBOARD        ║\n"
        "╚══════════════════════════════════════╝\n"
        "\n"
        "TEAM STATUS:\n"
        "  Ana    perf=5  health=4  capacity=100%  [GREEN]\n"
        "  Bruno  perf=4  health=3  capacity=112%  [RED]\n"
        "  Cata   perf=3  health=4  capacity=85%   [YELLOW]\n"
        "  Diego  perf=4  health=5  capacity=90%   [GREEN]\n"
        "\n"
        "AVERAGES:\n"
        "  Performance: 4.0/5  |  Health: 4.0/5  |  Capacity: 96.8%\n"
        "\n"
        "OPEN ROLES:\n"
        "  [HIGH]   Senior QA Engineer\n"
        "  [MEDIUM] DevOps Engineer\n"
        "\n"
        "OVERALL: YELLOW\n"
        "Actions needed:\n"
        "  • Bruno: overloaded + health borderline — reduce allocation\n"
        "  • Cata: performance borderline — schedule coaching session"
    ),
)

BLOQUE6 = [L76,L77,L78,L79,L80,L81,L82,L83,L84,L85,L86,L87,L88,L89,L90]
