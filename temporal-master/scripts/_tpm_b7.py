"""
_tpm_b7.py — TPM Mastery · BLOQUE 7 (L91–L105)
===============================================
Fase: negociacion_influencia
Niveles: 91 a 105 (15 desafíos Python)
Boss: L105 — Influence Commander
"""
from __future__ import annotations

_BASE = dict(
    codex_id="tpm_mastery", sector_id=21, challenge_type="python",
    phase="negociacion_influencia", is_free=False, strict_match=False,
    is_phase_boss=False, is_project=False,
)
_BASE_BOSS = {k: v for k, v in _BASE.items() if k not in ("is_phase_boss", "is_project")}

# ─────────────────────────────────────────────────────────────────────────────
L91 = dict(
    **_BASE, level_order=91, title="BATNA Calculator", difficulty="easy",
    description=(
        "El BATNA (Best Alternative To a Negotiated Agreement) define tu poder de negociación. "
        "Implementa `batna_calculator(your_options, counterpart_options)` donde cada opción es "
        "`{'name': str, 'value': int}`.\n\n"
        "Imprime:\n"
        "`=== BATNA ANALYSIS ===`\n"
        "`Your BATNA: <name> (value: $N)`\n"
        "`Counterpart BATNA: <name> (value: $N)`\n"
        "`Power Balance: YOUR ADVANTAGE` si tu BATNA > su BATNA, "
        "`THEIR ADVANTAGE` si menor, `BALANCED` si igual.\n"
        "`Negotiation Leverage: HIGH/MEDIUM/LOW` según diferencia: "
        "HIGH si |diff| > 30% del mayor, MEDIUM si > 10%, LOW si ≤ 10%."
    ),
    hint="BATNA = opción de mayor valor. Calcula diferencia porcentual sobre el valor mayor.",
    initial_code=(
        "def batna_calculator(your_options, counterpart_options):\n"
        "    pass\n\n"
        "batna_calculator(\n"
        "    your_options=[\n"
        "        {'name': 'Vendor A contract', 'value': 80},\n"
        "        {'name': 'Build in-house',    'value': 60},\n"
        "        {'name': 'Delay project',     'value': 40},\n"
        "    ],\n"
        "    counterpart_options=[\n"
        "        {'name': 'Keep current client', 'value': 70},\n"
        "        {'name': 'Find new client',     'value': 50},\n"
        "    ]\n"
        ")\n"
    ),
    expected_output=(
        "=== BATNA ANALYSIS ===\n"
        "Your BATNA: Vendor A contract (value: $80)\n"
        "Counterpart BATNA: Keep current client (value: $70)\n"
        "Power Balance: YOUR ADVANTAGE\n"
        "Negotiation Leverage: LOW"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L92 = dict(
    **_BASE, level_order=92, title="ZOPA Finder", difficulty="easy",
    description=(
        "La ZOPA (Zone of Possible Agreement) es el rango donde ambas partes pueden llegar a acuerdo. "
        "Implementa `zopa_finder(your_min, your_max, their_min, their_max)` donde min es el mínimo "
        "aceptable y max es el objetivo ideal.\n\n"
        "Imprime:\n"
        "`=== ZOPA ANALYSIS ===`\n"
        "`Your range: $min – $max`\n"
        "`Their range: $min – $max`\n"
        "Si hay solapamiento (max(your_min,their_min) <= min(your_max,their_max)):\n"
        "`ZOPA EXISTS: $overlap_low – $overlap_high`\n"
        "`ZOPA width: $N`\n"
        "`Recommended anchor: $N` (midpoint de la ZOPA)\n"
        "Si no hay solapamiento:\n"
        "`NO ZOPA: Gap of $N`\n"
        "`Strategy: Bridge the gap by $N or walk away`"
    ),
    hint="ZOPA_low = max(your_min, their_min), ZOPA_high = min(your_max, their_max).",
    initial_code=(
        "def zopa_finder(your_min, your_max, their_min, their_max):\n"
        "    pass\n\n"
        "zopa_finder(your_min=100, your_max=150, their_min=90, their_max=130)\n"
    ),
    expected_output=(
        "=== ZOPA ANALYSIS ===\n"
        "Your range: $100 – $150\n"
        "Their range: $90 – $130\n"
        "ZOPA EXISTS: $100 – $130\n"
        "ZOPA width: $30\n"
        "Recommended anchor: $115"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L93 = dict(
    **_BASE, level_order=93, title="Scope Negotiation Analyzer", difficulty="medium",
    description=(
        "En negociaciones de alcance, cada ítem tiene costo y valor. "
        "Implementa `scope_negotiation(budget, items)` donde cada item es "
        "`{'name': str, 'cost': int, 'value': int, 'priority': str}` "
        "(priority: MUST/SHOULD/NICE).\n\n"
        "Greedy por ratio value/cost. MUST items se incluyen siempre (aunque excedan budget).\n\n"
        "Imprime:\n"
        "`=== SCOPE NEGOTIATION ===`\n"
        "`Budget: $N`\n"
        "`─────────────────────────`\n"
        "`INCLUDED (N items, $cost, value: N):`\n"
        "` ✓ <name> [$cost] [PRIORITY]`\n"
        "`EXCLUDED (N items):`\n"
        "` ✗ <name> [$cost] [PRIORITY]`\n"
        "`─────────────────────────`\n"
        "`Total Value Delivered: N`\n"
        "`Budget Utilization: N%`"
    ),
    hint="Primero incluye todos los MUST. Luego ordena el resto por value/cost desc y agrega mientras quepa.",
    initial_code=(
        "def scope_negotiation(budget, items):\n"
        "    pass\n\n"
        "scope_negotiation(budget=200, items=[\n"
        "    {'name': 'Auth system',      'cost': 80, 'value': 90,  'priority': 'MUST'},\n"
        "    {'name': 'Dashboard',        'cost': 60, 'value': 75,  'priority': 'SHOULD'},\n"
        "    {'name': 'Notifications',    'cost': 40, 'value': 60,  'priority': 'SHOULD'},\n"
        "    {'name': 'Dark mode',        'cost': 20, 'value': 15,  'priority': 'NICE'},\n"
        "    {'name': 'Export to PDF',    'cost': 50, 'value': 40,  'priority': 'NICE'},\n"
        "])\n"
    ),
    expected_output=(
        "=== SCOPE NEGOTIATION ===\n"
        "Budget: $200\n"
        "─────────────────────────\n"
        "INCLUDED (3 items, $180, value: 225):\n"
        " ✓ Auth system [$80] [MUST]\n"
        " ✓ Notifications [$40] [SHOULD]\n"
        " ✓ Dashboard [$60] [SHOULD]\n"
        "EXCLUDED (2 items):\n"
        " ✗ Dark mode [$20] [NICE]\n"
        " ✗ Export to PDF [$50] [NICE]\n"
        "─────────────────────────\n"
        "Total Value Delivered: 225\n"
        "Budget Utilization: 90%"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L94 = dict(
    **_BASE, level_order=94, title="Influence Map Builder", difficulty="medium",
    description=(
        "Un mapa de influencia categoriza stakeholders por poder e interés para diseñar estrategias. "
        "Implementa `influence_map(stakeholders)` donde cada uno es "
        "`{'name': str, 'power': int, 'interest': int, 'current_stance': str}` "
        "(stance: CHAMPION/SUPPORTER/NEUTRAL/SKEPTIC/BLOCKER).\n\n"
        "Cuadrantes (power 1-10, interest 1-10):\n"
        "- power≥6 & interest≥6 → MANAGE CLOSELY\n"
        "- power≥6 & interest<6 → KEEP SATISFIED\n"
        "- power<6 & interest≥6 → KEEP INFORMED\n"
        "- power<6 & interest<6 → MONITOR\n\n"
        "Imprime:\n"
        "`=== INFLUENCE MAP ===`\n"
        "Por cuadrante (orden: MANAGE CLOSELY→KEEP SATISFIED→KEEP INFORMED→MONITOR):\n"
        "`[QUADRANT]`\n"
        "`  <name> | P:<N> I:<N> | <stance> → <strategy>`\n\n"
        "Strategy por stance:\n"
        "CHAMPION→Leverage as advocate, SUPPORTER→Engage regularly,\n"
        "NEUTRAL→Educate and involve, SKEPTIC→Address concerns proactively,\n"
        "BLOCKER→Escalate or neutralize"
    ),
    hint="Agrupa por cuadrante en el orden dado. Dentro de cada cuadrante, ordena por power desc.",
    initial_code=(
        "def influence_map(stakeholders):\n"
        "    pass\n\n"
        "influence_map([\n"
        "    {'name': 'CTO',          'power': 9, 'interest': 8, 'current_stance': 'CHAMPION'},\n"
        "    {'name': 'CFO',          'power': 8, 'interest': 4, 'current_stance': 'NEUTRAL'},\n"
        "    {'name': 'Dev Lead',     'power': 5, 'interest': 9, 'current_stance': 'SUPPORTER'},\n"
        "    {'name': 'Legal',        'power': 7, 'interest': 3, 'current_stance': 'SKEPTIC'},\n"
        "    {'name': 'QA Manager',   'power': 4, 'interest': 7, 'current_stance': 'NEUTRAL'},\n"
        "    {'name': 'Ops Analyst',  'power': 3, 'interest': 3, 'current_stance': 'NEUTRAL'},\n"
        "])\n"
    ),
    expected_output=(
        "=== INFLUENCE MAP ===\n"
        "[MANAGE CLOSELY]\n"
        "  CTO | P:9 I:8 | CHAMPION → Leverage as advocate\n"
        "[KEEP SATISFIED]\n"
        "  CFO | P:8 I:4 | NEUTRAL → Educate and involve\n"
        "  Legal | P:7 I:3 | SKEPTIC → Address concerns proactively\n"
        "[KEEP INFORMED]\n"
        "  Dev Lead | P:5 I:9 | SUPPORTER → Engage regularly\n"
        "  QA Manager | P:4 I:7 | NEUTRAL → Educate and involve\n"
        "[MONITOR]\n"
        "  Ops Analyst | P:3 I:3 | NEUTRAL → Educate and involve"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L95 = dict(
    **_BASE, level_order=95, title="Win-Win Scenario Modeler", difficulty="medium",
    description=(
        "En negociaciones exitosas ambas partes ganan. "
        "Implementa `win_win_modeler(party_a, party_b, scenarios)` donde cada parte es "
        "`{'name': str, 'priorities': list[str]}` y cada escenario es "
        "`{'name': str, 'a_score': int, 'b_score': int}` (scores 1-10).\n\n"
        "Imprime:\n"
        "`=== WIN-WIN SCENARIO ANALYSIS ===`\n"
        "`Party A: <name> | Party B: <name>`\n"
        "`─────────────────────────────────`\n"
        "Por escenario (orden original):\n"
        "`<scenario_name>`\n"
        "`  <party_a>: N/10  <party_b>: N/10  Joint: N`\n"
        "`  Outcome: WIN-WIN/WIN-LOSE/LOSE-WIN/LOSE-LOSE`\n"
        "(WIN si score≥6, LOSE si <6)\n\n"
        "Al final:\n"
        "`─────────────────────────────────`\n"
        "`RECOMMENDED: <scenario con mayor joint score>`\n"
        "`Joint Value: N`"
    ),
    hint="Joint score = a_score + b_score. WIN si ≥6 para esa parte.",
    initial_code=(
        "def win_win_modeler(party_a, party_b, scenarios):\n"
        "    pass\n\n"
        "win_win_modeler(\n"
        "    party_a={'name': 'Engineering', 'priorities': ['quality', 'timeline']},\n"
        "    party_b={'name': 'Product',     'priorities': ['features', 'speed']},\n"
        "    scenarios=[\n"
        "        {'name': 'Full Scope Q3',   'a_score': 4,  'b_score': 9},\n"
        "        {'name': 'MVP Q2',          'a_score': 8,  'b_score': 7},\n"
        "        {'name': 'Phased Delivery', 'a_score': 7,  'b_score': 8},\n"
        "        {'name': 'Delayed Q4',      'a_score': 9,  'b_score': 3},\n"
        "    ]\n"
        ")\n"
    ),
    expected_output=(
        "=== WIN-WIN SCENARIO ANALYSIS ===\n"
        "Party A: Engineering | Party B: Product\n"
        "─────────────────────────────────\n"
        "Full Scope Q3\n"
        "  Engineering: 4/10  Product: 9/10  Joint: 13\n"
        "  Outcome: LOSE-WIN\n"
        "MVP Q2\n"
        "  Engineering: 8/10  Product: 7/10  Joint: 15\n"
        "  Outcome: WIN-WIN\n"
        "Phased Delivery\n"
        "  Engineering: 7/10  Product: 8/10  Joint: 15\n"
        "  Outcome: WIN-WIN\n"
        "Delayed Q4\n"
        "  Engineering: 9/10  Product: 3/10  Joint: 12\n"
        "  Outcome: WIN-LOSE\n"
        "─────────────────────────────────\n"
        "RECOMMENDED: MVP Q2\n"
        "Joint Value: 15"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L96 = dict(
    **_BASE, level_order=96, title="Resource Allocation Negotiator", difficulty="medium",
    description=(
        "Cuando múltiples equipos compiten por recursos, el TPM negocia la asignación óptima. "
        "Implementa `resource_negotiator(total_resources, requests)` donde cada request es "
        "`{'team': str, 'requested': int, 'minimum': int, 'priority': int}` (priority 1=alta).\n\n"
        "Algoritmo: asigna minimum a todos primero. Distribuye el remanente proporcionalmente "
        "según inverse priority (1/priority) normalizada.\n\n"
        "Imprime:\n"
        "`=== RESOURCE ALLOCATION NEGOTIATION ===`\n"
        "`Total Resources: N | Teams: N`\n"
        "`─────────────────────────────────────`\n"
        "Por equipo (orden por priority asc):\n"
        "`<team>`\n"
        "`  Requested: N | Minimum: N | Allocated: N`\n"
        "`  Satisfaction: N%` (allocated/requested*100, max 100%)\n"
        "`─────────────────────────────────────`\n"
        "`Total Allocated: N / N`\n"
        "`Average Satisfaction: N%`"
    ),
    hint="Remainder = total - sum(minimums). Distribuye remainder * (1/priority_i / sum(1/priority_j)). Trunca a int.",
    initial_code=(
        "def resource_negotiator(total_resources, requests):\n"
        "    pass\n\n"
        "resource_negotiator(total_resources=100, requests=[\n"
        "    {'team': 'Platform',  'requested': 40, 'minimum': 20, 'priority': 1},\n"
        "    {'team': 'Mobile',    'requested': 35, 'minimum': 15, 'priority': 2},\n"
        "    {'team': 'Data',      'requested': 30, 'minimum': 10, 'priority': 3},\n"
        "    {'team': 'QA',        'requested': 20, 'minimum': 8,  'priority': 4},\n"
        "])\n"
    ),
    expected_output=(
        "=== RESOURCE ALLOCATION NEGOTIATION ===\n"
        "Total Resources: 100 | Teams: 4\n"
        "─────────────────────────────────────\n"
        "Platform\n"
        "  Requested: 40 | Minimum: 20 | Allocated: 40\n"
        "  Satisfaction: 100%\n"
        "Mobile\n"
        "  Requested: 35 | Minimum: 15 | Allocated: 35\n"
        "  Satisfaction: 100%\n"
        "Data\n"
        "  Requested: 30 | Minimum: 10 | Allocated: 17\n"
        "  Satisfaction: 57%\n"
        "QA\n"
        "  Requested: 20 | Minimum: 8 | Allocated: 8\n"
        "  Satisfaction: 40%\n"
        "─────────────────────────────────────\n"
        "Total Allocated: 100 / 100\n"
        "Average Satisfaction: 74%"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L97 = dict(
    **_BASE, level_order=97, title="Concession Planner", difficulty="medium",
    description=(
        "Las concesiones bien planificadas crean movimiento sin perder valor. "
        "Implementa `concession_planner(opening_position, target, walkaway, rounds)` "
        "donde opening > target > walkaway (todos ints, negociación de precio).\n\n"
        "Patrón de concesiones decrecientes (patrón estándar de negociación): "
        "reparte (opening - target) en `rounds` concesiones donde cada una es "
        "proporcional al peso del round: round_i_weight = (rounds - i + 1) / sum(1..rounds).\n\n"
        "Imprime:\n"
        "`=== CONCESSION PLAN ===`\n"
        "`Opening: $N | Target: $N | Walkaway: $N`\n"
        "`─────────────────────────`\n"
        "Por ronda (1..rounds):\n"
        "`Round N: Offer $N (concede $N)`\n"
        "Al final:\n"
        "`─────────────────────────`\n"
        "`Total Conceded: $N`\n"
        "`Reserve (above walkaway): $N`\n"
        "`Strategy: Decreasing concessions signal diminishing flexibility`"
    ),
    hint="Concesión ronda i = round((opening-target) * weight_i). Acumula para calcular oferta.",
    initial_code=(
        "def concession_planner(opening_position, target, walkaway, rounds):\n"
        "    pass\n\n"
        "concession_planner(opening_position=200, target=160, walkaway=140, rounds=4)\n"
    ),
    expected_output=(
        "=== CONCESSION PLAN ===\n"
        "Opening: $200 | Target: $160 | Walkaway: $140\n"
        "─────────────────────────\n"
        "Round 1: Offer $184 (concede $16)\n"
        "Round 2: Offer $172 (concede $12)\n"
        "Round 3: Offer $164 (concede $8)\n"
        "Round 4: Offer $160 (concede $4)\n"
        "─────────────────────────\n"
        "Total Conceded: $40\n"
        "Reserve (above walkaway): $20\n"
        "Strategy: Decreasing concessions signal diminishing flexibility"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L98 = dict(
    **_BASE, level_order=98, title="Stakeholder Alignment Scorer", difficulty="medium",
    description=(
        "Mide qué tan alineados están los stakeholders en las dimensiones clave. "
        "Implementa `alignment_scorer(initiative, stakeholders)` donde cada stakeholder es "
        "`{'name': str, 'role': str, 'scores': dict}` y scores tiene claves fijas: "
        "goals, timeline, budget, approach, success_metrics (cada una 1-10).\n\n"
        "Imprime:\n"
        "`=== STAKEHOLDER ALIGNMENT: <initiative> ===`\n"
        "Por stakeholder:\n"
        "`<name> (<role>): N/10`  (promedio de sus 5 dimensiones)\n\n"
        "Luego tabla de dimensiones (promedio entre todos los stakeholders):\n"
        "`─────────────────────────────`\n"
        "`Dimension Scores:`\n"
        "`  goals            : N.N ██████████`  (barra de 10 bloques █)\n"
        "Mismas 5 dimensiones en orden: goals, timeline, budget, approach, success_metrics.\n\n"
        "`─────────────────────────────`\n"
        "`Overall Alignment: N.N/10`\n"
        "`Status: ALIGNED (≥7.5) / AT RISK (≥5) / MISALIGNED (<5)`"
    ),
    hint="Barra: int(score) bloques de █, resto ░ hasta 10 total.",
    initial_code=(
        "def alignment_scorer(initiative, stakeholders):\n"
        "    pass\n\n"
        "alignment_scorer('Platform Rewrite', [\n"
        "    {'name': 'CTO',      'role': 'Sponsor',  'scores': {'goals':9,'timeline':7,'budget':6,'approach':8,'success_metrics':9}},\n"
        "    {'name': 'Eng Lead', 'role': 'Owner',    'scores': {'goals':8,'timeline':6,'budget':7,'approach':9,'success_metrics':8}},\n"
        "    {'name': 'CFO',      'role': 'Approver', 'scores': {'goals':7,'timeline':8,'budget':5,'approach':6,'success_metrics':7}},\n"
        "])\n"
    ),
    expected_output=(
        "=== STAKEHOLDER ALIGNMENT: Platform Rewrite ===\n"
        "CTO (Sponsor): 7.8/10\n"
        "Eng Lead (Owner): 7.6/10\n"
        "CFO (Approver): 6.6/10\n"
        "─────────────────────────────\n"
        "Dimension Scores:\n"
        "  goals            : 8.0 ████████░░\n"
        "  timeline         : 7.0 ███████░░░\n"
        "  budget           : 6.0 ██████░░░░\n"
        "  approach         : 7.7 ███████░░░\n"
        "  success_metrics  : 8.0 ████████░░\n"
        "─────────────────────────────\n"
        "Overall Alignment: 7.3/10\n"
        "Status: AT RISK"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L99 = dict(
    **_BASE, level_order=99, title="Timeline Negotiation Simulator", difficulty="medium",
    description=(
        "Negocia fechas de entrega considerando restricciones de ambas partes. "
        "Implementa `timeline_negotiator(feature, team_estimate, exec_demand, today)` "
        "donde todas las fechas son strings 'YYYY-MM-DD'.\n\n"
        "Calcula:\n"
        "- team_days = (team_estimate - today).days\n"
        "- exec_days = (exec_demand - today).days\n"
        "- gap_days = team_days - exec_days\n"
        "- compromise_date = today + timedelta(days = int((team_days + exec_days) / 2))\n\n"
        "Imprime:\n"
        "`=== TIMELINE NEGOTIATION: <feature> ===`\n"
        "`Team Estimate: <date> (N days)`\n"
        "`Exec Demand:   <date> (N days)`\n"
        "`Gap: N days`\n"
        "`─────────────────────────`\n"
        "Si gap_days <= 0: `STATUS: ALIGNED - No negotiation needed`\n"
        "Si gap > 0:\n"
        "`STATUS: GAP EXISTS - Negotiation required`\n"
        "`Compromise Date: <date> (N days)`\n"
        "`Acceleration Options:`\n"
        "`  • Reduce scope by N% to hit exec demand`  (N% = gap/team_days*100, int)\n"
        "`  • Add N engineers to compress timeline`    (N = ceil(gap/10))\n"
        "`  • Split delivery: core by <exec_demand>, full by <compromise_date>`"
    ),
    hint="Usa datetime.date para parsear y calcular. Importa math.ceil.",
    initial_code=(
        "from datetime import date, timedelta\n"
        "import math\n\n"
        "def timeline_negotiator(feature, team_estimate, exec_demand, today):\n"
        "    pass\n\n"
        "timeline_negotiator(\n"
        "    feature='Payment Gateway v2',\n"
        "    team_estimate='2024-06-30',\n"
        "    exec_demand='2024-05-15',\n"
        "    today='2024-04-01'\n"
        ")\n"
    ),
    expected_output=(
        "=== TIMELINE NEGOTIATION: Payment Gateway v2 ===\n"
        "Team Estimate: 2024-06-30 (90 days)\n"
        "Exec Demand:   2024-05-15 (44 days)\n"
        "Gap: 46 days\n"
        "─────────────────────────\n"
        "STATUS: GAP EXISTS - Negotiation required\n"
        "Compromise Date: 2024-06-07 (67 days)\n"
        "Acceleration Options:\n"
        "  • Reduce scope by 51% to hit exec demand\n"
        "  • Add 5 engineers to compress timeline\n"
        "  • Split delivery: core by 2024-05-15, full by 2024-06-07"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L100 = dict(
    **_BASE, level_order=100, title="Priority Conflict Resolver", difficulty="medium",
    description=(
        "Cuando múltiples equipos tienen prioridades conflictivas, el TPM debe resolver. "
        "Implementa `priority_conflict_resolver(conflicts)` donde cada conflict es "
        "`{'item': str, 'teams': list[{'team': str, 'priority_rank': int, 'rationale': str}]}`.\n\n"
        "Para cada conflicto, el ganador es el equipo con menor priority_rank (más alta prioridad). "
        "En empate, gana el primero en la lista.\n\n"
        "Imprime:\n"
        "`=== PRIORITY CONFLICT RESOLUTION ===`\n"
        "Por conflicto:\n"
        "`[<item>]`\n"
        "Por equipo (orden original):\n"
        "`  <team> (Rank #N): <rationale>`\n"
        "`  → DECISION: <winner_team> wins (Rank #N)`\n"
        "`  → Action: Proceed with <item> as <winner_team>'s priority`\n\n"
        "Al final:\n"
        "`─────────────────────────`\n"
        "`Resolved: N conflicts`"
    ),
    hint="Menor rank = mayor prioridad. Itera en orden original para empates.",
    initial_code=(
        "def priority_conflict_resolver(conflicts):\n"
        "    pass\n\n"
        "priority_conflict_resolver([\n"
        "    {'item': 'Auth refactor', 'teams': [\n"
        "        {'team': 'Security', 'priority_rank': 1, 'rationale': 'Critical compliance risk'},\n"
        "        {'team': 'Platform', 'priority_rank': 3, 'rationale': 'Needed for v2 launch'},\n"
        "    ]},\n"
        "    {'item': 'DB migration', 'teams': [\n"
        "        {'team': 'Data',     'priority_rank': 2, 'rationale': 'Blocking analytics'},\n"
        "        {'team': 'Backend',  'priority_rank': 2, 'rationale': 'Performance bottleneck'},\n"
        "    ]},\n"
        "])\n"
    ),
    expected_output=(
        "=== PRIORITY CONFLICT RESOLUTION ===\n"
        "[Auth refactor]\n"
        "  Security (Rank #1): Critical compliance risk\n"
        "  Platform (Rank #3): Needed for v2 launch\n"
        "  → DECISION: Security wins (Rank #1)\n"
        "  → Action: Proceed with Auth refactor as Security's priority\n"
        "[DB migration]\n"
        "  Data (Rank #2): Blocking analytics\n"
        "  Backend (Rank #2): Performance bottleneck\n"
        "  → DECISION: Data wins (Rank #2)\n"
        "  → Action: Proceed with DB migration as Data's priority\n"
        "─────────────────────────\n"
        "Resolved: 2 conflicts"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L101 = dict(
    **_BASE, level_order=101, title="Persuasion Strength Analyzer", difficulty="medium",
    description=(
        "Un argumento persuasivo combina lógica, emoción y credibilidad (Aristóteles: Logos, Pathos, Ethos). "
        "Implementa `persuasion_analyzer(proposal, arguments)` donde cada argument es "
        "`{'text': str, 'logos': int, 'pathos': int, 'ethos': int}` (cada dimensión 1-10).\n\n"
        "Fuerza total = (logos*0.4 + pathos*0.3 + ethos*0.3).\n\n"
        "Imprime:\n"
        "`=== PERSUASION ANALYSIS: <proposal> ===`\n"
        "Por argumento (orden original):\n"
        "`\"<text>\"`\n"
        "`  Logos: N/10 | Pathos: N/10 | Ethos: N/10 | Score: N.N`\n"
        "`  Strength: COMPELLING (≥8) / SOLID (≥6) / WEAK (<6)`\n\n"
        "Al final:\n"
        "`─────────────────────────`\n"
        "`Strongest argument: \"<text>\" (N.N)`\n"
        "`Overall persuasiveness: N.N/10`\n"
        "`Recommendation: <Lead with Logos/Pathos/Ethos>` (la dimensión de mayor promedio)"
    ),
    hint="Overall = promedio de scores de todos los argumentos. Dimensión recomendada = la que tiene mayor promedio entre todos los argumentos.",
    initial_code=(
        "def persuasion_analyzer(proposal, arguments):\n"
        "    pass\n\n"
        "persuasion_analyzer('Adopt microservices architecture', [\n"
        "    {'text': 'Reduces deployment risk by 60%',      'logos': 9, 'pathos': 5, 'ethos': 8},\n"
        "    {'text': 'Teams will move 3x faster',           'logos': 7, 'pathos': 9, 'ethos': 6},\n"
        "    {'text': 'Industry standard at Google/Netflix', 'logos': 6, 'pathos': 6, 'ethos': 9},\n"
        "])\n"
    ),
    expected_output=(
        "=== PERSUASION ANALYSIS: Adopt microservices architecture ===\n"
        "\"Reduces deployment risk by 60%\"\n"
        "  Logos: 9/10 | Pathos: 5/10 | Ethos: 8/10 | Score: 7.5\n"
        "  Strength: SOLID\n"
        "\"Teams will move 3x faster\"\n"
        "  Logos: 7/10 | Pathos: 9/10 | Ethos: 6/10 | Score: 7.5\n"
        "  Strength: SOLID\n"
        "\"Industry standard at Google/Netflix\"\n"
        "  Logos: 6/10 | Pathos: 6/10 | Ethos: 9/10 | Score: 6.9\n"
        "  Strength: SOLID\n"
        "─────────────────────────\n"
        "Strongest argument: \"Reduces deployment risk by 60%\" (7.5)\n"
        "Overall persuasiveness: 7.3/10\n"
        "Recommendation: Lead with Ethos"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L102 = dict(
    **_BASE, level_order=102, title="Resistance Mapper", difficulty="medium",
    description=(
        "Mapear la resistencia permite anticipar objeciones. "
        "Implementa `resistance_mapper(initiative, resistors)` donde cada resistor es "
        "`{'name': str, 'type': str, 'intensity': int, 'root_cause': str}` "
        "(type: RATIONAL/EMOTIONAL/POLITICAL, intensity 1-10).\n\n"
        "Imprime:\n"
        "`=== RESISTANCE MAP: <initiative> ===`\n"
        "Agrupa por type (orden: RATIONAL→EMOTIONAL→POLITICAL):\n"
        "`[<TYPE> RESISTANCE]`\n"
        "`  <name> (intensity: N/10)`\n"
        "`  Root cause: <root_cause>`\n"
        "`  Counter-strategy: <strategy>`\n\n"
        "Estrategias por tipo:\n"
        "RATIONAL → Provide data and evidence\n"
        "EMOTIONAL → Acknowledge feelings, build trust\n"
        "POLITICAL → Find common ground, offer trade-offs\n\n"
        "Al final:\n"
        "`─────────────────────────────`\n"
        "`Highest resistance: <name> (N/10)`\n"
        "`Critical threshold: N resistors at HIGH intensity (≥7)`\n"
        "`Overall risk: HIGH (≥3 critical) / MEDIUM (≥1) / LOW (0)`"
    ),
    hint="Ordena dentro de cada grupo por intensity desc.",
    initial_code=(
        "def resistance_mapper(initiative, resistors):\n"
        "    pass\n\n"
        "resistance_mapper('Cloud Migration', [\n"
        "    {'name': 'IT Director',   'type': 'POLITICAL',  'intensity': 8, 'root_cause': 'Loss of control'},\n"
        "    {'name': 'Dev Team',      'type': 'EMOTIONAL',  'intensity': 6, 'root_cause': 'Fear of job loss'},\n"
        "    {'name': 'Finance',       'type': 'RATIONAL',   'intensity': 9, 'root_cause': 'Cost uncertainty'},\n"
        "    {'name': 'Legal',         'type': 'RATIONAL',   'intensity': 7, 'root_cause': 'Compliance gaps'},\n"
        "    {'name': 'Operations',    'type': 'EMOTIONAL',  'intensity': 5, 'root_cause': 'Process disruption'},\n"
        "])\n"
    ),
    expected_output=(
        "=== RESISTANCE MAP: Cloud Migration ===\n"
        "[RATIONAL RESISTANCE]\n"
        "  Finance (intensity: 9/10)\n"
        "  Root cause: Cost uncertainty\n"
        "  Counter-strategy: Provide data and evidence\n"
        "  Legal (intensity: 7/10)\n"
        "  Root cause: Compliance gaps\n"
        "  Counter-strategy: Provide data and evidence\n"
        "[EMOTIONAL RESISTANCE]\n"
        "  Dev Team (intensity: 6/10)\n"
        "  Root cause: Fear of job loss\n"
        "  Counter-strategy: Acknowledge feelings, build trust\n"
        "  Operations (intensity: 5/10)\n"
        "  Root cause: Process disruption\n"
        "  Counter-strategy: Acknowledge feelings, build trust\n"
        "[POLITICAL RESISTANCE]\n"
        "  IT Director (intensity: 8/10)\n"
        "  Root cause: Loss of control\n"
        "  Counter-strategy: Find common ground, offer trade-offs\n"
        "─────────────────────────────\n"
        "Highest resistance: Finance (9/10)\n"
        "Critical threshold: 3 resistors at HIGH intensity (≥7)\n"
        "Overall risk: HIGH"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L103 = dict(
    **_BASE, level_order=103, title="Coalition Strength Calculator", difficulty="medium",
    description=(
        "Una coalición fuerte garantiza que las iniciativas obtengan aprobación. "
        "Implementa `coalition_calculator(initiative, coalition_members)` donde cada miembro es "
        "`{'name': str, 'influence_score': int, 'commitment': str}` "
        "(commitment: CHAMPION/SUPPORTER/OBSERVER, influence 1-10).\n\n"
        "Peso de commitment: CHAMPION=1.0, SUPPORTER=0.6, OBSERVER=0.2.\n\n"
        "Weighted influence = influence_score × commitment_weight.\n\n"
        "Imprime:\n"
        "`=== COALITION ANALYSIS: <initiative> ===`\n"
        "Por miembro (orden original):\n"
        "`  <name> | Influence: N | <commitment> | Weighted: N.N`\n\n"
        "Al final:\n"
        "`─────────────────────────────`\n"
        "`Coalition Strength: N.N / 10.0`\n"
        "(strength = sum(weighted) / count)\n"
        "`CHAMPIONs: N | SUPPORTERs: N | OBSERVERs: N`\n"
        "`Status: STRONG (≥7) / ADEQUATE (≥5) / WEAK (<5)`\n"
        "`Recommendation: <mensaje>`\n\n"
        "Mensajes:\n"
        "STRONG → Ready to proceed, leverage champions\n"
        "ADEQUATE → Convert observers to supporters before proceeding\n"
        "WEAK → Build coalition before advancing initiative"
    ),
    hint="strength = sum(weighted_influences) / len(members). Redondea a 1 decimal.",
    initial_code=(
        "def coalition_calculator(initiative, coalition_members):\n"
        "    pass\n\n"
        "coalition_calculator('API Gateway Migration', [\n"
        "    {'name': 'CTO',       'influence_score': 10, 'commitment': 'CHAMPION'},\n"
        "    {'name': 'VP Eng',    'influence_score': 8,  'commitment': 'SUPPORTER'},\n"
        "    {'name': 'Arch Lead', 'influence_score': 7,  'commitment': 'CHAMPION'},\n"
        "    {'name': 'Dev Lead',  'influence_score': 6,  'commitment': 'OBSERVER'},\n"
        "    {'name': 'QA Lead',   'influence_score': 5,  'commitment': 'SUPPORTER'},\n"
        "])\n"
    ),
    expected_output=(
        "=== COALITION ANALYSIS: API Gateway Migration ===\n"
        "  CTO | Influence: 10 | CHAMPION | Weighted: 10.0\n"
        "  VP Eng | Influence: 8 | SUPPORTER | Weighted: 4.8\n"
        "  Arch Lead | Influence: 7 | CHAMPION | Weighted: 7.0\n"
        "  Dev Lead | Influence: 6 | OBSERVER | Weighted: 1.2\n"
        "  QA Lead | Influence: 5 | SUPPORTER | Weighted: 3.0\n"
        "─────────────────────────────\n"
        "Coalition Strength: 5.2 / 10.0\n"
        "CHAMPIONs: 2 | SUPPORTERs: 2 | OBSERVERs: 1\n"
        "Status: ADEQUATE\n"
        "Recommendation: Convert observers to supporters before proceeding"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L104 = dict(
    **_BASE, level_order=104, title="Negotiation Outcome Tracker", difficulty="medium",
    description=(
        "Registra y analiza el historial de negociaciones para mejorar estrategias futuras. "
        "Implementa `negotiation_tracker(negotiations)` donde cada negociación es "
        "`{'topic': str, 'our_position': int, 'their_position': int, "
        "'outcome': int, 'rounds': int, 'result': str}` (result: WON/LOST/COMPROMISE).\n\n"
        "Imprime:\n"
        "`=== NEGOTIATION OUTCOME TRACKER ===`\n"
        "Por negociación (orden original):\n"
        "`<topic>`\n"
        "`  Our: N | Their: N | Outcome: N | Rounds: N | <result>`\n"
        "`  Value captured: N%`  (outcome/our_position*100 si WON, outcome/their_position*100 si LOST, \n"
        "    promedio de ambos si COMPROMISE)\n\n"
        "Al final:\n"
        "`─────────────────────────────`\n"
        "`Results: N won / N lost / N compromise`\n"
        "`Win rate: N%`\n"
        "`Avg rounds to close: N.N`\n"
        "`Avg value captured: N%`"
    ),
    hint="Win rate = won/total*100. Value captured COMPROMISE = (outcome/our_position + outcome/their_position)/2*100.",
    initial_code=(
        "def negotiation_tracker(negotiations):\n"
        "    pass\n\n"
        "negotiation_tracker([\n"
        "    {'topic': 'Q3 headcount',   'our_position': 10, 'their_position': 6,  'outcome': 8,  'rounds': 3, 'result': 'COMPROMISE'},\n"
        "    {'topic': 'Release date',   'our_position': 90, 'their_position': 60, 'outcome': 90, 'rounds': 2, 'result': 'WON'},\n"
        "    {'topic': 'Budget cut',     'our_position': 500,'their_position': 300,'outcome': 300,'rounds': 5, 'result': 'LOST'},\n"
        "    {'topic': 'Vendor contract','our_position': 120,'their_position': 100,'outcome': 110,'rounds': 4, 'result': 'COMPROMISE'},\n"
        "])\n"
    ),
    expected_output=(
        "=== NEGOTIATION OUTCOME TRACKER ===\n"
        "Q3 headcount\n"
        "  Our: 10 | Their: 6 | Outcome: 8 | Rounds: 3 | COMPROMISE\n"
        "  Value captured: 87%\n"
        "Release date\n"
        "  Our: 90 | Their: 60 | Outcome: 90 | Rounds: 2 | WON\n"
        "  Value captured: 100%\n"
        "Budget cut\n"
        "  Our: 500 | Their: 300 | Outcome: 300 | Rounds: 5 | LOST\n"
        "  Value captured: 100%\n"
        "Vendor contract\n"
        "  Our: 120 | Their: 100 | Outcome: 110 | Rounds: 4 | COMPROMISE\n"
        "  Value captured: 97%\n"
        "─────────────────────────────\n"
        "Results: 1 won / 1 lost / 2 compromise\n"
        "Win rate: 25%\n"
        "Avg rounds to close: 3.5\n"
        "Avg value captured: 96%"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L105 = dict(
    **_BASE_BOSS, level_order=105, title="Influence Commander", difficulty="hard",
    is_phase_boss=True, is_project=True,
    description=(
        "BOSS L105: Eres el Influence Commander. "
        "Implementa la clase `InfluenceCommander` con:\n\n"
        "`__init__(self, tpm_name, initiative)` — almacena nombre e iniciativa.\n\n"
        "`assess_power(stakeholders)` — stakeholders: lista `{'name', 'power', 'interest', 'stance'}`. "
        "Identifica el top champion (mayor power con stance CHAMPION) y el top blocker "
        "(mayor power con stance BLOCKER). Imprime:\n"
        "`Power Assessment: N stakeholders`\n"
        "`  Top Champion: <name> (power: N)`\n"
        "`  Top Blocker: <name> (power: N)` o `  Top Blocker: None` si no hay.\n\n"
        "`build_coalition(members)` — members: lista `{'name', 'commitment', 'influence'}`. "
        "Calcula strength como en L103. Imprime:\n"
        "`Coalition: N members | Strength: N.N/10`\n\n"
        "`negotiate(topic, our_pos, their_pos)` — calcula midpoint. Imprime:\n"
        "`Negotiating: <topic>`\n"
        "`  Our: N | Their: N | Proposed: N`\n\n"
        "`command_report()` — imprime:\n"
        "`=== INFLUENCE COMMAND REPORT ===`\n"
        "`TPM: <tpm_name> | Initiative: <initiative>`\n"
        "`Stakeholders assessed, coalition built, negotiations tracked.`\n"
        "`Status: COMMANDING`"
    ),
    hint="Reutiliza la lógica de L103 para coalition strength. midpoint = (our_pos + their_pos) // 2.",
    initial_code=(
        "class InfluenceCommander:\n"
        "    def __init__(self, tpm_name, initiative):\n"
        "        pass\n"
        "    def assess_power(self, stakeholders):\n"
        "        pass\n"
        "    def build_coalition(self, members):\n"
        "        pass\n"
        "    def negotiate(self, topic, our_pos, their_pos):\n"
        "        pass\n"
        "    def command_report(self):\n"
        "        pass\n\n"
        "ic = InfluenceCommander('Maria Reyes', 'Data Platform v2')\n"
        "ic.assess_power([\n"
        "    {'name': 'CTO',      'power': 10, 'interest': 9, 'stance': 'CHAMPION'},\n"
        "    {'name': 'CFO',      'power': 9,  'interest': 5, 'stance': 'BLOCKER'},\n"
        "    {'name': 'VP Eng',   'power': 8,  'interest': 8, 'stance': 'SUPPORTER'},\n"
        "    {'name': 'Legal',    'power': 7,  'interest': 4, 'stance': 'NEUTRAL'},\n"
        "])\n"
        "ic.build_coalition([\n"
        "    {'name': 'CTO',    'commitment': 'CHAMPION',  'influence': 10},\n"
        "    {'name': 'VP Eng', 'commitment': 'SUPPORTER', 'influence': 8},\n"
        "    {'name': 'Dev Lead','commitment': 'CHAMPION', 'influence': 7},\n"
        "])\n"
        "ic.negotiate('Engineering headcount', 15, 10)\n"
        "ic.command_report()\n"
    ),
    expected_output=(
        "Power Assessment: 4 stakeholders\n"
        "  Top Champion: CTO (power: 10)\n"
        "  Top Blocker: CFO (power: 9)\n"
        "Coalition: 3 members | Strength: 7.3/10\n"
        "Negotiating: Engineering headcount\n"
        "  Our: 15 | Their: 10 | Proposed: 12\n"
        "=== INFLUENCE COMMAND REPORT ===\n"
        "TPM: Maria Reyes | Initiative: Data Platform v2\n"
        "Stakeholders assessed, coalition built, negotiations tracked.\n"
        "Status: COMMANDING"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
BLOQUE7 = [L91, L92, L93, L94, L95, L96, L97, L98, L99, L100, L101, L102, L103, L104, L105]
