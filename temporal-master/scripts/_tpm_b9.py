"""
_tpm_b9.py — TPM Mastery · BLOQUE 9 (L121–L135)
================================================
Fase: decision_frameworks
Niveles: 121 a 135 (15 desafíos Python)
Boss: L135 — Decision Command Center
"""
from __future__ import annotations

_BASE = dict(
    codex_id="tpm_mastery", sector_id=21, challenge_type="python",
    phase="decision_frameworks", is_free=False, strict_match=False,
    is_phase_boss=False, is_project=False,
)
_BASE_BOSS = {k: v for k, v in _BASE.items() if k not in ("is_phase_boss", "is_project")}

# ─────────────────────────────────────────────────────────────────────────────
L121 = dict(
    **_BASE, level_order=121, title="RICE Prioritizer", difficulty="easy",
    description=(
        "RICE (Reach × Impact × Confidence / Effort) es el framework de priorización más "
        "usado en product management. "
        "Implementa `rice_prioritizer(features)` donde cada feature es "
        "`{'name': str, 'reach': int, 'impact': int, 'confidence': int, 'effort': float}` "
        "(confidence es %, effort en person-months).\n\n"
        "RICE score = (reach × impact × confidence/100) / effort. Redondea a 1 decimal.\n\n"
        "Imprime:\n"
        "`=== RICE PRIORITIZATION ===`\n"
        "Por feature (orden por RICE score desc):\n"
        "`N. <name>`\n"
        "`   R:<reach> × I:<impact> × C:<confidence>% ÷ E:<effort> = <score>`\n\n"
        "Al final:\n"
        "`─────────────────────────`\n"
        "`Top Priority: <name> (score: <score>)`"
    ),
    hint="RICE = reach*impact*(confidence/100)/effort. sorted desc por score.",
    initial_code=(
        "def rice_prioritizer(features):\n"
        "    pass\n\n"
        "rice_prioritizer([\n"
        "    {'name': 'Search autocomplete', 'reach': 5000, 'impact': 3, 'confidence': 80, 'effort': 2.0},\n"
        "    {'name': 'Dark mode',           'reach': 8000, 'impact': 1, 'confidence': 90, 'effort': 1.0},\n"
        "    {'name': 'Bulk export',         'reach': 500,  'impact': 3, 'confidence': 70, 'effort': 3.0},\n"
        "    {'name': 'SSO integration',     'reach': 200,  'impact': 3, 'confidence': 95, 'effort': 5.0},\n"
        "])\n"
    ),
    expected_output=(
        "=== RICE PRIORITIZATION ===\n"
        "1. Search autocomplete\n"
        "   R:5000 × I:3 × C:80% ÷ E:2.0 = 6000.0\n"
        "2. Dark mode\n"
        "   R:8000 × I:1 × C:90% ÷ E:1.0 = 7200.0\n"
        "3. Bulk export\n"
        "   R:500 × I:3 × C:70% ÷ E:3.0 = 350.0\n"
        "4. SSO integration\n"
        "   R:200 × I:3 × C:95% ÷ E:5.0 = 114.0\n"
        "─────────────────────────\n"
        "Top Priority: Dark mode (score: 7200.0)"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L122 = dict(
    **_BASE, level_order=122, title="MoSCoW Prioritizer", difficulty="easy",
    description=(
        "MoSCoW clasifica requerimientos en Must/Should/Could/Won't. "
        "Implementa `moscow_prioritizer(project, requirements)` donde cada req es "
        "`{'name': str, 'category': str, 'effort': int, 'value': int}` "
        "(category: MUST/SHOULD/COULD/WONT).\n\n"
        "Imprime:\n"
        "`=== MoSCoW PRIORITIZATION: <project> ===`\n"
        "Por categoría (orden: MUST→SHOULD→COULD→WONT):\n"
        "`[<category>]`\n"
        "Por req dentro del grupo (orden por value desc):\n"
        "`  • <name> (effort: N, value: N)`\n\n"
        "Al final:\n"
        "`─────────────────────────────`\n"
        "`Summary: N MUST | N SHOULD | N COULD | N WONT`\n"
        "`MUST effort total: N`\n"
        "`SHOULD effort total: N`\n"
        "`Recommendation: Focus sprint on MUST items first`"
    ),
    hint="Filtra por categoría, ordena por value desc dentro de cada grupo.",
    initial_code=(
        "def moscow_prioritizer(project, requirements):\n"
        "    pass\n\n"
        "moscow_prioritizer('MVP Launch', [\n"
        "    {'name': 'User login',         'category': 'MUST',   'effort': 5, 'value': 10},\n"
        "    {'name': 'Password reset',     'category': 'MUST',   'effort': 3, 'value': 8},\n"
        "    {'name': 'Email notifications','category': 'SHOULD', 'effort': 4, 'value': 7},\n"
        "    {'name': 'Social login',       'category': 'COULD',  'effort': 6, 'value': 5},\n"
        "    {'name': 'Analytics dashboard','category': 'SHOULD', 'effort': 8, 'value': 6},\n"
        "    {'name': 'Dark mode',          'category': 'WONT',   'effort': 3, 'value': 3},\n"
        "])\n"
    ),
    expected_output=(
        "=== MoSCoW PRIORITIZATION: MVP Launch ===\n"
        "[MUST]\n"
        "  • User login (effort: 5, value: 10)\n"
        "  • Password reset (effort: 3, value: 8)\n"
        "[SHOULD]\n"
        "  • Email notifications (effort: 4, value: 7)\n"
        "  • Analytics dashboard (effort: 8, value: 6)\n"
        "[COULD]\n"
        "  • Social login (effort: 6, value: 5)\n"
        "[WONT]\n"
        "  • Dark mode (effort: 3, value: 3)\n"
        "─────────────────────────────\n"
        "Summary: 2 MUST | 2 SHOULD | 1 COULD | 1 WONT\n"
        "MUST effort total: 8\n"
        "SHOULD effort total: 12\n"
        "Recommendation: Focus sprint on MUST items first"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L123 = dict(
    **_BASE, level_order=123, title="Kano Model Analyzer", difficulty="medium",
    description=(
        "El modelo Kano clasifica features por cómo afectan la satisfacción del usuario. "
        "Implementa `kano_analyzer(features)` donde cada feature es "
        "`{'name': str, 'functional': int, 'dysfunctional': int}` (ratings 1-5; "
        "functional=satisfacción si presente, dysfunctional=satisfacción si ausente).\n\n"
        "Clasificación (tabla Kano estándar):\n"
        "- Must-Be: functional<=3 AND dysfunctional>=4\n"
        "- Performance: functional>=4 AND dysfunctional<=2\n"
        "- Attractive: functional>=4 AND dysfunctional>=3\n"
        "- Indifferent: functional<=3 AND dysfunctional<=2\n"
        "- Reverse: functional<=2 AND dysfunctional<=2 (override si cumple)\n\n"
        "Aplica en orden: Must-Be primero, luego Performance, Attractive, Indifferent.\n\n"
        "Imprime:\n"
        "`=== KANO MODEL ANALYSIS ===`\n"
        "Agrupa por categoría (Must-Be→Performance→Attractive→Indifferent):\n"
        "`[<Category>]`\n"
        "`  <name> (F:<functional>, D:<dysfunctional>)`\n\n"
        "Al final:\n"
        "`─────────────────────────────`\n"
        "`Invest in: <Performance features>` (names separados por ', ') o None\n"
        "`Hygiene (fix first): <Must-Be features>` o None"
    ),
    hint="Aplica reglas en orden. Si no cumple ninguna, clasifica como Indifferent.",
    initial_code=(
        "def kano_analyzer(features):\n"
        "    pass\n\n"
        "kano_analyzer([\n"
        "    {'name': 'Fast load time',    'functional': 5, 'dysfunctional': 1},\n"
        "    {'name': 'App crashes',       'functional': 2, 'dysfunctional': 5},\n"
        "    {'name': 'AI recommendations','functional': 5, 'dysfunctional': 3},\n"
        "    {'name': 'Custom themes',     'functional': 3, 'dysfunctional': 2},\n"
        "    {'name': 'Offline mode',      'functional': 4, 'dysfunctional': 2},\n"
        "])\n"
    ),
    expected_output=(
        "=== KANO MODEL ANALYSIS ===\n"
        "[Must-Be]\n"
        "  App crashes (F:2, D:5)\n"
        "[Performance]\n"
        "  Fast load time (F:5, D:1)\n"
        "  Offline mode (F:4, D:2)\n"
        "[Attractive]\n"
        "  AI recommendations (F:5, D:3)\n"
        "[Indifferent]\n"
        "  Custom themes (F:3, D:2)\n"
        "─────────────────────────────\n"
        "Invest in: Fast load time, Offline mode\n"
        "Hygiene (fix first): App crashes"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L124 = dict(
    **_BASE, level_order=124, title="Eisenhower Matrix", difficulty="easy",
    description=(
        "La Matriz de Eisenhower organiza tareas por urgencia e importancia. "
        "Implementa `eisenhower_matrix(tasks)` donde cada task es "
        "`{'name': str, 'urgent': bool, 'important': bool, 'owner': str}`.\n\n"
        "Cuadrantes:\n"
        "- Q1 DO NOW: urgent=True AND important=True\n"
        "- Q2 SCHEDULE: urgent=False AND important=True\n"
        "- Q3 DELEGATE: urgent=True AND important=False\n"
        "- Q4 ELIMINATE: urgent=False AND important=False\n\n"
        "Imprime:\n"
        "`=== EISENHOWER MATRIX ===`\n"
        "Por cuadrante (Q1→Q2→Q3→Q4):\n"
        "`[Q<N> - <label>]`\n"
        "Por task (orden original):\n"
        "`  • <name> → <owner>`\n\n"
        "Al final:\n"
        "`─────────────────────────────`\n"
        "`Q1: N tasks | Q2: N tasks | Q3: N tasks | Q4: N tasks`\n"
        "`Focus: Q1 items require immediate attention`"
    ),
    hint="Clasifica cada task en su cuadrante. Si un cuadrante está vacío, imprime el header igualmente.",
    initial_code=(
        "def eisenhower_matrix(tasks):\n"
        "    pass\n\n"
        "eisenhower_matrix([\n"
        "    {'name': 'Fix prod outage',      'urgent': True,  'important': True,  'owner': 'Eng Lead'},\n"
        "    {'name': 'Q3 roadmap planning',  'urgent': False, 'important': True,  'owner': 'TPM'},\n"
        "    {'name': 'Reply to slack ping',  'urgent': True,  'important': False, 'owner': 'Self'},\n"
        "    {'name': 'Architecture review',  'urgent': False, 'important': True,  'owner': 'Architect'},\n"
        "    {'name': 'Weekly status email',  'urgent': True,  'important': False, 'owner': 'PMO'},\n"
        "    {'name': 'Old report cleanup',   'urgent': False, 'important': False, 'owner': 'Analyst'},\n"
        "    {'name': 'Critical bug fix',     'urgent': True,  'important': True,  'owner': 'Backend'},\n"
        "])\n"
    ),
    expected_output=(
        "=== EISENHOWER MATRIX ===\n"
        "[Q1 - DO NOW]\n"
        "  • Fix prod outage → Eng Lead\n"
        "  • Critical bug fix → Backend\n"
        "[Q2 - SCHEDULE]\n"
        "  • Q3 roadmap planning → TPM\n"
        "  • Architecture review → Architect\n"
        "[Q3 - DELEGATE]\n"
        "  • Reply to slack ping → Self\n"
        "  • Weekly status email → PMO\n"
        "[Q4 - ELIMINATE]\n"
        "  • Old report cleanup → Analyst\n"
        "─────────────────────────────\n"
        "Q1: 2 tasks | Q2: 2 tasks | Q3: 2 tasks | Q4: 1 tasks\n"
        "Focus: Q1 items require immediate attention"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L125 = dict(
    **_BASE, level_order=125, title="Weighted Decision Matrix", difficulty="medium",
    description=(
        "La matriz de decisión ponderada ayuda a elegir entre alternativas con criterios múltiples. "
        "Implementa `weighted_matrix(decision, criteria, options)` donde:\n"
        "- criteria: lista `{'name': str, 'weight': float}`\n"
        "- options: lista `{'name': str, 'scores': dict}` (dict maps criterion name → score 1-10)\n\n"
        "Weighted score = sum(score_i × weight_i). Redondea a 2 decimales.\n\n"
        "Imprime:\n"
        "`=== WEIGHTED DECISION MATRIX: <decision> ===`\n\n"
        "Header de tabla:\n"
        "`Option           ` + por cada criterion `| <name[:8]>(<weight>) ` + `| TOTAL`\n\n"
        "Por opción (orden por weighted score desc):\n"
        "`<name[:16]>      ` + por cada criterion `| <score[:8]>          ` + `| <total>`\n\n"
        "Al final:\n"
        "`─────────────────────────`\n"
        "`RECOMMENDATION: <nombre de la opción con mayor score>`"
    ),
    hint="Usa ljust para alinear columnas. RECOMMENDATION = opción con mayor weighted score.",
    initial_code=(
        "def weighted_matrix(decision, criteria, options):\n"
        "    pass\n\n"
        "weighted_matrix(\n"
        "    decision='Select Cloud Provider',\n"
        "    criteria=[\n"
        "        {'name': 'Cost',       'weight': 0.3},\n"
        "        {'name': 'Reliability','weight': 0.4},\n"
        "        {'name': 'Support',    'weight': 0.3},\n"
        "    ],\n"
        "    options=[\n"
        "        {'name': 'AWS',        'scores': {'Cost': 6, 'Reliability': 9, 'Support': 8}},\n"
        "        {'name': 'GCP',        'scores': {'Cost': 8, 'Reliability': 8, 'Support': 7}},\n"
        "        {'name': 'Azure',      'scores': {'Cost': 7, 'Reliability': 8, 'Support': 9}},\n"
        "    ]\n"
        ")\n"
    ),
    expected_output=(
        "=== WEIGHTED DECISION MATRIX: Select Cloud Provider ===\n"
        "Option           | Cost(0.3)  | Reliabi(0.4) | Support(0.3) | TOTAL\n"
        "AWS              | 6          | 9            | 8            | 7.8\n"
        "Azure            | 7          | 8            | 9            | 7.9\n"
        "GCP              | 8          | 8            | 7            | 7.7\n"
        "─────────────────────────\n"
        "RECOMMENDATION: Azure"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L126 = dict(
    **_BASE, level_order=126, title="ICE Scorer", difficulty="easy",
    description=(
        "ICE (Impact, Confidence, Ease) es un framework rápido de priorización. "
        "Implementa `ice_scorer(items)` donde cada item es "
        "`{'name': str, 'impact': int, 'confidence': int, 'ease': int}` (cada uno 1-10).\n\n"
        "ICE score = (impact + confidence + ease) / 3. Redondea a 1 decimal.\n\n"
        "Imprime:\n"
        "`=== ICE SCORING ===`\n"
        "Por item (orden por ICE score desc):\n"
        "`N. <name>`\n"
        "`   Impact: N | Confidence: N | Ease: N → ICE: N.N`\n\n"
        "Al final:\n"
        "`─────────────────────────`\n"
        "`Top item: <name> (ICE: N.N)`\n"
        "`Average ICE: N.N`"
    ),
    hint="ICE = round((impact+confidence+ease)/3, 1). sort desc.",
    initial_code=(
        "def ice_scorer(items):\n"
        "    pass\n\n"
        "ice_scorer([\n"
        "    {'name': 'A/B test checkout flow', 'impact': 8, 'confidence': 9, 'ease': 7},\n"
        "    {'name': 'Redesign onboarding',    'impact': 9, 'confidence': 6, 'ease': 4},\n"
        "    {'name': 'Add push notifications', 'impact': 7, 'confidence': 8, 'ease': 9},\n"
        "    {'name': 'Referral program',       'impact': 9, 'confidence': 5, 'ease': 3},\n"
        "])\n"
    ),
    expected_output=(
        "=== ICE SCORING ===\n"
        "1. A/B test checkout flow\n"
        "   Impact: 8 | Confidence: 9 | Ease: 7 → ICE: 8.0\n"
        "2. Add push notifications\n"
        "   Impact: 7 | Confidence: 8 | Ease: 9 → ICE: 8.0\n"
        "3. Redesign onboarding\n"
        "   Impact: 9 | Confidence: 6 | Ease: 4 → ICE: 6.3\n"
        "4. Referral program\n"
        "   Impact: 9 | Confidence: 5 | Ease: 3 → ICE: 5.7\n"
        "─────────────────────────\n"
        "Top item: A/B test checkout flow (ICE: 8.0)\n"
        "Average ICE: 7.0"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L127 = dict(
    **_BASE, level_order=127, title="Feature Prioritization Engine", difficulty="medium",
    description=(
        "Combina múltiples señales para priorización de features. "
        "Implementa `prioritization_engine(features)` donde cada feature es "
        "`{'name': str, 'user_requests': int, 'revenue_impact': int, "
        "'strategic_fit': int, 'dev_effort': int}` "
        "(revenue_impact y strategic_fit 1-10; dev_effort en semanas).\n\n"
        "Score = (user_requests * 0.3 + revenue_impact * 0.4 + strategic_fit * 0.3) / dev_effort\n"
        "Redondea a 2 decimales.\n\n"
        "Imprime:\n"
        "`=== FEATURE PRIORITIZATION ENGINE ===`\n"
        "Por feature (orden por score desc):\n"
        "`<rank>. <name>`\n"
        "`   Signals: requests=N, revenue=N, strategic=N, effort=Nw`\n"
        "`   Priority Score: N.N`\n"
        "`   Tier: TIER 1 (≥2.0) / TIER 2 (≥1.0) / TIER 3 (<1.0)`\n\n"
        "Al final:\n"
        "`─────────────────────────────`\n"
        "`TIER 1: N features`\n"
        "`TIER 2: N features`\n"
        "`TIER 3: N features`"
    ),
    hint="score = (req*0.3 + rev*0.4 + strat*0.3) / effort. round 2 decimales.",
    initial_code=(
        "def prioritization_engine(features):\n"
        "    pass\n\n"
        "prioritization_engine([\n"
        "    {'name': 'Real-time sync',   'user_requests': 8, 'revenue_impact': 9, 'strategic_fit': 8, 'dev_effort': 4},\n"
        "    {'name': 'Bulk import',      'user_requests': 6, 'revenue_impact': 5, 'strategic_fit': 4, 'dev_effort': 2},\n"
        "    {'name': 'Mobile app',       'user_requests': 9, 'revenue_impact': 8, 'strategic_fit': 9, 'dev_effort': 10},\n"
        "    {'name': 'API v2',           'user_requests': 5, 'revenue_impact': 7, 'strategic_fit': 8, 'dev_effort': 3},\n"
        "    {'name': 'Custom reports',   'user_requests': 7, 'revenue_impact': 6, 'strategic_fit': 5, 'dev_effort': 5},\n"
        "])\n"
    ),
    expected_output=(
        "=== FEATURE PRIORITIZATION ENGINE ===\n"
        "1. Real-time sync\n"
        "   Signals: requests=8, revenue=9, strategic=8, effort=4w\n"
        "   Priority Score: 2.1\n"
        "   Tier: TIER 1\n"
        "2. API v2\n"
        "   Signals: requests=5, revenue=7, strategic=8, effort=3w\n"
        "   Priority Score: 2.17\n"
        "   Tier: TIER 1\n"
        "3. Bulk import\n"
        "   Signals: requests=6, revenue=5, strategic=4, effort=2w\n"
        "   Priority Score: 2.5\n"
        "   Tier: TIER 1\n"
        "4. Custom reports\n"
        "   Signals: requests=7, revenue=6, strategic=5, effort=5w\n"
        "   Priority Score: 1.23\n"
        "   Tier: TIER 2\n"
        "5. Mobile app\n"
        "   Signals: requests=9, revenue=8, strategic=9, effort=10w\n"
        "   Priority Score: 0.86\n"
        "   Tier: TIER 3\n"
        "─────────────────────────────\n"
        "TIER 1: 3 features\n"
        "TIER 2: 1 features\n"
        "TIER 3: 1 features"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L128 = dict(
    **_BASE, level_order=128, title="Constraint-Based Prioritizer", difficulty="medium",
    description=(
        "Las restricciones de capacidad limitan qué puede ejecutarse. "
        "Implementa `constraint_prioritizer(capacity, items)` donde capacity es "
        "`{'eng': int, 'design': int, 'qa': int}` (personas disponibles) y cada item es "
        "`{'name': str, 'value': int, 'eng': int, 'design': int, 'qa': int}`.\n\n"
        "Greedy: ordena por value desc; incluye item si NO excede ningún recurso restante.\n\n"
        "Imprime:\n"
        "`=== CONSTRAINT-BASED PRIORITIZATION ===`\n"
        "`Capacity: Eng=N | Design=N | QA=N`\n"
        "`─────────────────────────────────────`\n"
        "`SELECTED (N items, total value: N):`\n"
        "` ✓ <name> (value: N | Eng:N Design:N QA:N)`\n"
        "`DEFERRED (N items):`\n"
        "` ✗ <name> (value: N | Eng:N Design:N QA:N)`\n"
        "`─────────────────────────────────────`\n"
        "`Resource Utilization:`\n"
        "`  Eng:    N / N (N%)`\n"
        "`  Design: N / N (N%)`\n"
        "`  QA:     N / N (N%)`"
    ),
    hint="Track eng_used, design_used, qa_used. Item fits si (used+req) <= capacity en cada dimensión.",
    initial_code=(
        "def constraint_prioritizer(capacity, items):\n"
        "    pass\n\n"
        "constraint_prioritizer(\n"
        "    capacity={'eng': 10, 'design': 4, 'qa': 6},\n"
        "    items=[\n"
        "        {'name': 'Feature A', 'value': 90, 'eng': 4, 'design': 2, 'qa': 2},\n"
        "        {'name': 'Feature B', 'value': 80, 'eng': 3, 'design': 1, 'qa': 2},\n"
        "        {'name': 'Feature C', 'value': 70, 'eng': 5, 'design': 2, 'qa': 3},\n"
        "        {'name': 'Feature D', 'value': 60, 'eng': 2, 'design': 1, 'qa': 1},\n"
        "        {'name': 'Feature E', 'value': 50, 'eng': 3, 'design': 0, 'qa': 2},\n"
        "    ]\n"
        ")\n"
    ),
    expected_output=(
        "=== CONSTRAINT-BASED PRIORITIZATION ===\n"
        "Capacity: Eng=10 | Design=4 | QA=6\n"
        "─────────────────────────────────────\n"
        "SELECTED (4 items, total value: 300):\n"
        " ✓ Feature A (value: 90 | Eng:4 Design:2 QA:2)\n"
        " ✓ Feature B (value: 80 | Eng:3 Design:1 QA:2)\n"
        " ✓ Feature D (value: 60 | Eng:2 Design:1 QA:1)\n"
        " ✓ Feature E (value: 50 | Eng:3 Design:0 QA:2)\n"
        "DEFERRED (1 items):\n"
        " ✗ Feature C (value: 70 | Eng:5 Design:2 QA:3)\n"
        "─────────────────────────────────────\n"
        "Resource Utilization:\n"
        "  Eng:    12 / 10 (120%)\n"
        "  Design: 4 / 4 (100%)\n"
        "  QA:     7 / 6 (116%)"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L129 = dict(
    **_BASE, level_order=129, title="Technical vs Business Tradeoff", difficulty="medium",
    description=(
        "Los TPM constantemente navegan tradeoffs entre deuda técnica y valor de negocio. "
        "Implementa `tech_business_tradeoff(initiatives)` donde cada initiative es "
        "`{'name': str, 'tech_debt_reduction': int, 'business_value': int, 'risk_if_deferred': str}` "
        "(scores 1-10, risk: HIGH/MEDIUM/LOW).\n\n"
        "Balance score = (tech_debt_reduction * 0.5 + business_value * 0.5).\n"
        "Redondea a 1 decimal.\n\n"
        "Cuadrante (tech_debt_reduction, business_value):\n"
        "≥7 & ≥7 → STRATEGIC WIN\n"
        "≥7 & <7 → TECH PRIORITY\n"
        "<7 & ≥7 → BUSINESS PRIORITY\n"
        "<7 & <7 → LOW PRIORITY\n\n"
        "Imprime:\n"
        "`=== TECH vs BUSINESS TRADEOFF ===`\n"
        "Por initiative (orden por balance score desc):\n"
        "`<name>`\n"
        "`  Tech Debt: N | Business: N | Balance: N.N | Risk: <risk>`\n"
        "`  Quadrant: <quadrant>`\n\n"
        "Al final:\n"
        "`─────────────────────────`\n"
        "`STRATEGIC WINs: N`\n"
        "`Recommendation: Start with STRATEGIC WINs, then address HIGH-risk deferrals`"
    ),
    hint="Balance = round((td + bv) / 2, 1). No redondear antes de la comparación.",
    initial_code=(
        "def tech_business_tradeoff(initiatives):\n"
        "    pass\n\n"
        "tech_business_tradeoff([\n"
        "    {'name': 'DB refactor',      'tech_debt_reduction': 9, 'business_value': 4, 'risk_if_deferred': 'HIGH'},\n"
        "    {'name': 'New dashboard',    'tech_debt_reduction': 2, 'business_value': 9, 'risk_if_deferred': 'LOW'},\n"
        "    {'name': 'Auth overhaul',    'tech_debt_reduction': 8, 'business_value': 8, 'risk_if_deferred': 'HIGH'},\n"
        "    {'name': 'Report builder',   'tech_debt_reduction': 3, 'business_value': 7, 'risk_if_deferred': 'MEDIUM'},\n"
        "    {'name': 'CI/CD upgrade',    'tech_debt_reduction': 7, 'business_value': 7, 'risk_if_deferred': 'MEDIUM'},\n"
        "])\n"
    ),
    expected_output=(
        "=== TECH vs BUSINESS TRADEOFF ===\n"
        "Auth overhaul\n"
        "  Tech Debt: 8 | Business: 8 | Balance: 8.0 | Risk: HIGH\n"
        "  Quadrant: STRATEGIC WIN\n"
        "CI/CD upgrade\n"
        "  Tech Debt: 7 | Business: 7 | Balance: 7.0 | Risk: MEDIUM\n"
        "  Quadrant: STRATEGIC WIN\n"
        "DB refactor\n"
        "  Tech Debt: 9 | Business: 4 | Balance: 6.5 | Risk: HIGH\n"
        "  Quadrant: TECH PRIORITY\n"
        "New dashboard\n"
        "  Tech Debt: 2 | Business: 9 | Balance: 5.5 | Risk: LOW\n"
        "  Quadrant: BUSINESS PRIORITY\n"
        "Report builder\n"
        "  Tech Debt: 3 | Business: 7 | Balance: 5.0 | Risk: MEDIUM\n"
        "  Quadrant: BUSINESS PRIORITY\n"
        "─────────────────────────\n"
        "STRATEGIC WINs: 2\n"
        "Recommendation: Start with STRATEGIC WINs, then address HIGH-risk deferrals"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L130 = dict(
    **_BASE, level_order=130, title="Decision Tree Builder", difficulty="medium",
    description=(
        "Un árbol de decisión guía elecciones complejas con múltiples ramas. "
        "Implementa `decision_tree(decision, nodes)` donde cada node es "
        "`{'id': str, 'question': str, 'yes_next': str, 'no_next': str, 'is_leaf': bool, 'outcome': str}`.\n\n"
        "El nodo raíz tiene id='root'. Recorre el árbol siguiendo yes_next con "
        "las condiciones dadas en `answers` (dict id→bool).\n\n"
        "Firma: `decision_tree(decision, nodes, answers)`\n\n"
        "Imprime:\n"
        "`=== DECISION TREE: <decision> ===`\n"
        "Por cada nodo visitado (en orden de visita):\n"
        "`? <question>`\n"
        "`→ YES` o `→ NO` (según el answer para ese nodo)\n\n"
        "Al llegar a un leaf (is_leaf=True):\n"
        "`✓ DECISION: <outcome>`"
    ),
    hint="Usa dict para indexar nodos por id. Empieza en 'root'. Si answer es True sigue yes_next, si False sigue no_next.",
    initial_code=(
        "def decision_tree(decision, nodes, answers):\n"
        "    pass\n\n"
        "decision_tree(\n"
        "    decision='Build vs Buy',\n"
        "    nodes=[\n"
        "        {'id':'root',    'question':'Is it a core competency?',          'yes_next':'n2',   'no_next':'n3',   'is_leaf':False, 'outcome':''},\n"
        "        {'id':'n2',      'question':'Do we have internal expertise?',     'yes_next':'leaf1','no_next':'leaf2','is_leaf':False, 'outcome':''},\n"
        "        {'id':'n3',      'question':'Is it available off-the-shelf?',     'yes_next':'leaf3','no_next':'leaf4','is_leaf':False, 'outcome':''},\n"
        "        {'id':'leaf1',   'question':'',                                   'yes_next':'',     'no_next':'',     'is_leaf':True,  'outcome':'BUILD internally'},\n"
        "        {'id':'leaf2',   'question':'',                                   'yes_next':'',     'no_next':'',     'is_leaf':True,  'outcome':'HIRE and BUILD'},\n"
        "        {'id':'leaf3',   'question':'',                                   'yes_next':'',     'no_next':'',     'is_leaf':True,  'outcome':'BUY off-the-shelf'},\n"
        "        {'id':'leaf4',   'question':'',                                   'yes_next':'',     'no_next':'',     'is_leaf':True,  'outcome':'PARTNER or custom build'},\n"
        "    ],\n"
        "    answers={'root': True, 'n2': False}\n"
        ")\n"
    ),
    expected_output=(
        "=== DECISION TREE: Build vs Buy ===\n"
        "? Is it a core competency?\n"
        "→ YES\n"
        "? Do we have internal expertise?\n"
        "→ NO\n"
        "✓ DECISION: HIRE and BUILD"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L131 = dict(
    **_BASE, level_order=131, title="Consensus Scorer", difficulty="medium",
    description=(
        "Mide el nivel de consenso del equipo en una decisión. "
        "Implementa `consensus_scorer(decision, votes)` donde cada vote es "
        "`{'person': str, 'score': int, 'concern': str}` (score 1-5: "
        "1=Block, 2=Object, 3=Neutral, 4=Support, 5=Strongly Support).\n\n"
        "Imprime:\n"
        "`=== CONSENSUS SCORING: <decision> ===`\n"
        "Por voto (orden original):\n"
        "`  <person>: N/5 (<label>)`\n"
        "(labels: 1=BLOCK, 2=OBJECT, 3=NEUTRAL, 4=SUPPORT, 5=STRONG SUPPORT)\n"
        "`    Concern: <concern>` (solo si concern no está vacío)\n\n"
        "Al final:\n"
        "`─────────────────────────────`\n"
        "`Average Score: N.N/5.0`\n"
        "`BLOCKs: N | OBJECTIONs: N`\n"
        "`Consensus Level: CONSENSUS (avg≥4.0 and no BLOCKs) / ROUGH CONSENSUS (avg≥3.5 and no BLOCKs) / NEEDS WORK`\n"
        "`Recommendation:`\n"
        "CONSENSUS → Proceed with decision\n"
        "ROUGH CONSENSUS → Address objections, then proceed\n"
        "NEEDS WORK → Resolve blocks before proceeding"
    ),
    hint="avg = round(sum(scores)/len(votes), 1). Cuenta blocks (score==1) y objections (score==2).",
    initial_code=(
        "def consensus_scorer(decision, votes):\n"
        "    pass\n\n"
        "consensus_scorer('Migrate to Kubernetes', [\n"
        "    {'person': 'CTO',      'score': 5, 'concern': ''},\n"
        "    {'person': 'Eng Lead', 'score': 4, 'concern': ''},\n"
        "    {'person': 'DevOps',   'score': 5, 'concern': ''},\n"
        "    {'person': 'QA Lead',  'score': 3, 'concern': 'Testing complexity'},\n"
        "    {'person': 'Finance',  'score': 2, 'concern': 'Cost increase'},\n"
        "])\n"
    ),
    expected_output=(
        "=== CONSENSUS SCORING: Migrate to Kubernetes ===\n"
        "  CTO: 5/5 (STRONG SUPPORT)\n"
        "  Eng Lead: 4/5 (SUPPORT)\n"
        "  DevOps: 5/5 (STRONG SUPPORT)\n"
        "  QA Lead: 3/5 (NEUTRAL)\n"
        "    Concern: Testing complexity\n"
        "  Finance: 2/5 (OBJECT)\n"
        "    Concern: Cost increase\n"
        "─────────────────────────────\n"
        "Average Score: 3.8/5.0\n"
        "BLOCKs: 0 | OBJECTIONs: 1\n"
        "Consensus Level: ROUGH CONSENSUS\n"
        "Recommendation: Address objections, then proceed"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L132 = dict(
    **_BASE, level_order=132, title="Reversibility Assessor", difficulty="medium",
    description=(
        "Jeff Bezos distingue decisiones Tipo 1 (irreversibles) y Tipo 2 (reversibles). "
        "Implementa `reversibility_assessor(decisions)` donde cada decision es "
        "`{'name': str, 'reversibility': str, 'impact': str, 'speed_needed': str}` "
        "(reversibility: HIGH/LOW, impact: HIGH/LOW, speed_needed: FAST/SLOW).\n\n"
        "Clasificación:\n"
        "- Type 1 (One-way door): reversibility=LOW\n"
        "- Type 2 (Two-way door): reversibility=HIGH\n\n"
        "Approach:\n"
        "Type 1 + HIGH impact → Require executive approval, full analysis\n"
        "Type 1 + LOW impact → Require team lead approval\n"
        "Type 2 + FAST speed → Delegate to individual, bias for action\n"
        "Type 2 + SLOW speed → Team decision, lightweight process\n\n"
        "Imprime:\n"
        "`=== REVERSIBILITY ASSESSMENT ===`\n"
        "Por decisión (orden original):\n"
        "`<name>`\n"
        "`  Type: <Type 1/2> | Impact: <impact> | Speed: <speed_needed>`\n"
        "`  Approach: <approach>`\n\n"
        "Al final:\n"
        "`─────────────────────────────`\n"
        "`Type 1 decisions: N (slow down, analyze)`\n"
        "`Type 2 decisions: N (speed up, experiment)`"
    ),
    hint="Type 1 = LOW reversibility. Type 2 = HIGH reversibility.",
    initial_code=(
        "def reversibility_assessor(decisions):\n"
        "    pass\n\n"
        "reversibility_assessor([\n"
        "    {'name': 'Migrate production DB',   'reversibility': 'LOW',  'impact': 'HIGH', 'speed_needed': 'SLOW'},\n"
        "    {'name': 'Change button color',     'reversibility': 'HIGH', 'impact': 'LOW',  'speed_needed': 'FAST'},\n"
        "    {'name': 'Sunset legacy API',       'reversibility': 'LOW',  'impact': 'LOW',  'speed_needed': 'SLOW'},\n"
        "    {'name': 'Test new pricing page',   'reversibility': 'HIGH', 'impact': 'HIGH', 'speed_needed': 'SLOW'},\n"
        "])\n"
    ),
    expected_output=(
        "=== REVERSIBILITY ASSESSMENT ===\n"
        "Migrate production DB\n"
        "  Type: Type 1 | Impact: HIGH | Speed: SLOW\n"
        "  Approach: Require executive approval, full analysis\n"
        "Change button color\n"
        "  Type: Type 2 | Impact: LOW | Speed: FAST\n"
        "  Approach: Delegate to individual, bias for action\n"
        "Sunset legacy API\n"
        "  Type: Type 1 | Impact: LOW | Speed: SLOW\n"
        "  Approach: Require team lead approval\n"
        "Test new pricing page\n"
        "  Type: Type 2 | Impact: HIGH | Speed: SLOW\n"
        "  Approach: Team decision, lightweight process\n"
        "─────────────────────────────\n"
        "Type 1 decisions: 2 (slow down, analyze)\n"
        "Type 2 decisions: 2 (speed up, experiment)"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L133 = dict(
    **_BASE, level_order=133, title="Data-Driven Validator", difficulty="medium",
    description=(
        "Valida si una hipótesis tiene suficiente soporte en datos. "
        "Implementa `data_validator(hypothesis, evidence)` donde cada evidence item es "
        "`{'source': str, 'metric': str, 'value': float, 'supports': bool, 'confidence': str}` "
        "(confidence: HIGH/MEDIUM/LOW).\n\n"
        "Pesos de confidence: HIGH=3, MEDIUM=2, LOW=1.\n"
        "Evidence score = sum(weight si supports else -weight).\n\n"
        "Imprime:\n"
        "`=== DATA VALIDATION: <hypothesis> ===`\n"
        "Por evidence (orden original):\n"
        "`  [SUPPORTS/REFUTES] <source>`\n"
        "`    Metric: <metric> = <value> (confidence: <confidence>)`\n\n"
        "Al final:\n"
        "`─────────────────────────────`\n"
        "`Supporting evidence: N items`\n"
        "`Refuting evidence: N items`\n"
        "`Evidence Score: +N / -N`\n"
        "`Validation: VALIDATED (score≥3) / INCONCLUSIVE (-2<score<3) / REFUTED (score≤-3)`\n"
        "`Recommendation:`\n"
        "VALIDATED → Proceed with confidence\n"
        "INCONCLUSIVE → Gather more data before deciding\n"
        "REFUTED → Reject hypothesis, explore alternatives"
    ),
    hint="evidence_score = sum(weight if supports else -weight for each item).",
    initial_code=(
        "def data_validator(hypothesis, evidence):\n"
        "    pass\n\n"
        "data_validator('Improving onboarding reduces churn by 20%', [\n"
        "    {'source': 'A/B test Q1',     'metric': 'Churn rate',    'value': 18.0, 'supports': True,  'confidence': 'HIGH'},\n"
        "    {'source': 'User survey',     'metric': 'NPS score',     'value': 42.0, 'supports': True,  'confidence': 'MEDIUM'},\n"
        "    {'source': 'Cohort analysis', 'metric': 'D7 retention',  'value': 65.0, 'supports': True,  'confidence': 'HIGH'},\n"
        "    {'source': 'Support tickets', 'metric': 'Onboard issues', 'value': 12.0,'supports': False, 'confidence': 'LOW'},\n"
        "])\n"
    ),
    expected_output=(
        "=== DATA VALIDATION: Improving onboarding reduces churn by 20% ===\n"
        "  [SUPPORTS] A/B test Q1\n"
        "    Metric: Churn rate = 18.0 (confidence: HIGH)\n"
        "  [SUPPORTS] User survey\n"
        "    Metric: NPS score = 42.0 (confidence: MEDIUM)\n"
        "  [SUPPORTS] Cohort analysis\n"
        "    Metric: D7 retention = 65.0 (confidence: HIGH)\n"
        "  [REFUTES] Support tickets\n"
        "    Metric: Onboard issues = 12.0 (confidence: LOW)\n"
        "─────────────────────────────\n"
        "Supporting evidence: 3 items\n"
        "Refuting evidence: 1 items\n"
        "Evidence Score: +8 / -1\n"
        "Validation: VALIDATED\n"
        "Recommendation: Proceed with confidence"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L134 = dict(
    **_BASE, level_order=134, title="Strategic Alignment Scorer", difficulty="medium",
    description=(
        "Evalúa qué tan alineados están los proyectos con los objetivos estratégicos. "
        "Implementa `strategic_alignment(company_goals, projects)` donde:\n"
        "- company_goals: lista de strings\n"
        "- projects: lista `{'name': str, 'goal_alignment': dict, 'investment': int}`\n"
        "  (goal_alignment maps goal → score 0-10)\n\n"
        "Alignment score de proyecto = promedio de sus goal_alignment scores (round 1 decimal).\n\n"
        "Imprime:\n"
        "`=== STRATEGIC ALIGNMENT REPORT ===`\n"
        "Por proyecto (orden por alignment_score desc):\n"
        "`<name>`\n"
        "`  Investment: $N | Alignment: N.N/10`\n"
        "Por goal (orden original de company_goals):\n"
        "`    <goal>: N/10`\n"
        "`  Status: ALIGNED (≥7) / PARTIAL (≥5) / MISALIGNED (<5)`\n\n"
        "Al final:\n"
        "`─────────────────────────────────`\n"
        "`Portfolio Alignment: N.N/10`  (promedio de todos los alignment scores)\n"
        "`Investment in ALIGNED projects: $N`\n"
        "`Investment in MISALIGNED projects: $N`\n"
        "`Recommendation: Reallocate MISALIGNED budget to ALIGNED initiatives`"
    ),
    hint="Portfolio alignment = round(sum(scores)/len(projects), 1).",
    initial_code=(
        "def strategic_alignment(company_goals, projects):\n"
        "    pass\n\n"
        "strategic_alignment(\n"
        "    company_goals=['Revenue Growth', 'Customer Retention', 'Operational Efficiency'],\n"
        "    projects=[\n"
        "        {'name': 'CRM Upgrade',     'investment': 300,\n"
        "         'goal_alignment': {'Revenue Growth': 8, 'Customer Retention': 9, 'Operational Efficiency': 7}},\n"
        "        {'name': 'Legacy Cleanup',  'investment': 150,\n"
        "         'goal_alignment': {'Revenue Growth': 2, 'Customer Retention': 3, 'Operational Efficiency': 8}},\n"
        "        {'name': 'AI Features',     'investment': 400,\n"
        "         'goal_alignment': {'Revenue Growth': 9, 'Customer Retention': 7, 'Operational Efficiency': 6}},\n"
        "    ]\n"
        ")\n"
    ),
    expected_output=(
        "=== STRATEGIC ALIGNMENT REPORT ===\n"
        "AI Features\n"
        "  Investment: $400 | Alignment: 7.3/10\n"
        "    Revenue Growth: 9/10\n"
        "    Customer Retention: 7/10\n"
        "    Operational Efficiency: 6/10\n"
        "  Status: ALIGNED\n"
        "CRM Upgrade\n"
        "  Investment: $300 | Alignment: 8.0/10\n"
        "    Revenue Growth: 8/10\n"
        "    Customer Retention: 9/10\n"
        "    Operational Efficiency: 7/10\n"
        "  Status: ALIGNED\n"
        "Legacy Cleanup\n"
        "  Investment: $150 | Alignment: 4.3/10\n"
        "    Revenue Growth: 2/10\n"
        "    Customer Retention: 3/10\n"
        "    Operational Efficiency: 8/10\n"
        "  Status: MISALIGNED\n"
        "─────────────────────────────────\n"
        "Portfolio Alignment: 6.5/10\n"
        "Investment in ALIGNED projects: $700\n"
        "Investment in MISALIGNED projects: $150\n"
        "Recommendation: Reallocate MISALIGNED budget to ALIGNED initiatives"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L135 = dict(
    **_BASE_BOSS, level_order=135, title="Decision Command Center", difficulty="hard",
    is_phase_boss=True, is_project=True,
    description=(
        "BOSS L135: Eres el Decision Command Center. "
        "Implementa la clase `DecisionCommandCenter` con:\n\n"
        "`__init__(self, tpm_name)` — almacena nombre.\n\n"
        "`prioritize(items)` — items: lista `{'name': str, 'impact': int, 'effort': int}`. "
        "Score = impact/effort (round 1 decimal). Imprime:\n"
        "`Prioritized N items:`\n"
        "Por item (orden score desc):\n"
        "`  N. <name> (score: N.N)`\n\n"
        "`assess_reversibility(name, reversibility, impact)` — "
        "(reversibility: HIGH/LOW, impact: HIGH/LOW). Imprime:\n"
        "`<name>: Type <1/2> → <Slow down/Bias for action>`\n\n"
        "`validate_decision(name, evidence_score)` — Imprime:\n"
        "`<name>: <VALIDATED/INCONCLUSIVE/REFUTED> (score: N)`\n\n"
        "`command_report()` — Imprime:\n"
        "`=== DECISION COMMAND CENTER ===`\n"
        "`TPM: <tpm_name>`\n"
        "`Framework: Data-driven, reversibility-aware, impact-scored`\n"
        "`Status: DECIDING`"
    ),
    hint="Type 1 = LOW reversibility → Slow down. Type 2 = HIGH → Bias for action. Validated: score≥3, Refuted: score≤-3.",
    initial_code=(
        "class DecisionCommandCenter:\n"
        "    def __init__(self, tpm_name):\n"
        "        pass\n"
        "    def prioritize(self, items):\n"
        "        pass\n"
        "    def assess_reversibility(self, name, reversibility, impact):\n"
        "        pass\n"
        "    def validate_decision(self, name, evidence_score):\n"
        "        pass\n"
        "    def command_report(self):\n"
        "        pass\n\n"
        "dcc = DecisionCommandCenter('Laura Gomez')\n"
        "dcc.prioritize([\n"
        "    {'name': 'Feature A', 'impact': 9, 'effort': 2},\n"
        "    {'name': 'Feature B', 'impact': 7, 'effort': 5},\n"
        "    {'name': 'Feature C', 'impact': 8, 'effort': 3},\n"
        "])\n"
        "dcc.assess_reversibility('DB Migration', 'LOW', 'HIGH')\n"
        "dcc.validate_decision('New pricing model', 5)\n"
        "dcc.command_report()\n"
    ),
    expected_output=(
        "Prioritized 3 items:\n"
        "  1. Feature A (score: 4.5)\n"
        "  2. Feature C (score: 2.7)\n"
        "  3. Feature B (score: 1.4)\n"
        "DB Migration: Type 1 → Slow down\n"
        "New pricing model: VALIDATED (score: 5)\n"
        "=== DECISION COMMAND CENTER ===\n"
        "TPM: Laura Gomez\n"
        "Framework: Data-driven, reversibility-aware, impact-scored\n"
        "Status: DECIDING"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
BLOQUE9 = [L121, L122, L123, L124, L125, L126, L127, L128, L129, L130,
           L131, L132, L133, L134, L135]
