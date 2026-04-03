"""
_tpm_b8.py — TPM Mastery · BLOQUE 8 (L106–L120)
================================================
Fase: gestion_cambio
Niveles: 106 a 120 (15 desafíos Python)
Boss: L120 — Change Management Command Center
"""
from __future__ import annotations

_BASE = dict(
    codex_id="tpm_mastery", sector_id=21, challenge_type="python",
    phase="gestion_cambio", is_free=False, strict_match=False,
    is_phase_boss=False, is_project=False,
)
_BASE_BOSS = {k: v for k, v in _BASE.items() if k not in ("is_phase_boss", "is_project")}

# ─────────────────────────────────────────────────────────────────────────────
L106 = dict(
    **_BASE, level_order=106, title="ADKAR Assessment", difficulty="easy",
    description=(
        "El modelo ADKAR (Awareness, Desire, Knowledge, Ability, Reinforcement) "
        "mide la preparación individual al cambio. "
        "Implementa `adkar_assessment(person, scores)` donde scores es "
        "`{'awareness': int, 'desire': int, 'knowledge': int, 'ability': int, 'reinforcement': int}` "
        "(cada una 1-5).\n\n"
        "El primer elemento con score < 3 es el 'barrier point'.\n\n"
        "Imprime:\n"
        "`=== ADKAR ASSESSMENT: <person> ===`\n"
        "Por dimensión en orden ADKAR:\n"
        "`  <DIMENSION>: N/5 [████░] <OK/BARRIER>`\n"
        "(barra de 5 bloques: int(score) █ + resto ░)\n"
        "(OK si score≥3, BARRIER si <3)\n\n"
        "Al final:\n"
        "`─────────────────────────`\n"
        "`Overall: N.N/5.0`\n"
        "`Barrier Point: <dimension>` o `Barrier Point: None`\n"
        "`Status: READY (no barrier) / NEEDS SUPPORT (barrier exists)`"
    ),
    hint="El barrier point es la primera dimensión en orden ADKAR con score < 3. Barra: '█'*score + '░'*(5-score).",
    initial_code=(
        "def adkar_assessment(person, scores):\n"
        "    pass\n\n"
        "adkar_assessment('Carlos Mendez', {\n"
        "    'awareness': 4, 'desire': 2, 'knowledge': 3, 'ability': 2, 'reinforcement': 1\n"
        "})\n"
    ),
    expected_output=(
        "=== ADKAR ASSESSMENT: Carlos Mendez ===\n"
        "  AWARENESS:     4/5 [████░] OK\n"
        "  DESIRE:        2/5 [██░░░] BARRIER\n"
        "  KNOWLEDGE:     3/5 [███░░] OK\n"
        "  ABILITY:       2/5 [██░░░] BARRIER\n"
        "  REINFORCEMENT: 1/5 [█░░░░] BARRIER\n"
        "─────────────────────────\n"
        "Overall: 2.4/5.0\n"
        "Barrier Point: desire\n"
        "Status: NEEDS SUPPORT"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L107 = dict(
    **_BASE, level_order=107, title="Kotter Step Tracker", difficulty="easy",
    description=(
        "El modelo de 8 pasos de Kotter es el framework de cambio más usado. "
        "Implementa `kotter_tracker(initiative, steps)` donde cada step es "
        "`{'step': int, 'name': str, 'status': str, 'completion_pct': int}` "
        "(status: COMPLETE/IN_PROGRESS/NOT_STARTED).\n\n"
        "Los 8 pasos de Kotter son: 1-Create Urgency, 2-Form Coalition, 3-Create Vision, "
        "4-Communicate Vision, 5-Remove Obstacles, 6-Generate Wins, 7-Build on Change, 8-Anchor Change.\n\n"
        "Imprime:\n"
        "`=== KOTTER 8-STEP TRACKER: <initiative> ===`\n"
        "Por step (orden 1..8):\n"
        "`  Step N: <name>`\n"
        "`    Status: <status> | Progress: N%`\n\n"
        "Al final:\n"
        "`─────────────────────────────`\n"
        "`Completed: N/8 steps`\n"
        "`Overall Progress: N%`  (promedio de completion_pct)\n"
        "`Current Focus: Step N - <name>` (primer step IN_PROGRESS) o `None in progress`\n"
        "`Change Health: ON TRACK (≥50% progreso y ningún IN_PROGRESS con pct<20) / AT RISK`"
    ),
    hint="Overall = int(sum(pcts)/8). Change Health AT RISK si overall < 50% o hay algún IN_PROGRESS con pct < 20.",
    initial_code=(
        "def kotter_tracker(initiative, steps):\n"
        "    pass\n\n"
        "kotter_tracker('DevOps Transformation', [\n"
        "    {'step':1, 'name':'Create Urgency',     'status':'COMPLETE',     'completion_pct':100},\n"
        "    {'step':2, 'name':'Form Coalition',     'status':'COMPLETE',     'completion_pct':100},\n"
        "    {'step':3, 'name':'Create Vision',      'status':'COMPLETE',     'completion_pct':100},\n"
        "    {'step':4, 'name':'Communicate Vision', 'status':'IN_PROGRESS',  'completion_pct':60},\n"
        "    {'step':5, 'name':'Remove Obstacles',   'status':'IN_PROGRESS',  'completion_pct':30},\n"
        "    {'step':6, 'name':'Generate Wins',      'status':'NOT_STARTED',  'completion_pct':0},\n"
        "    {'step':7, 'name':'Build on Change',    'status':'NOT_STARTED',  'completion_pct':0},\n"
        "    {'step':8, 'name':'Anchor Change',      'status':'NOT_STARTED',  'completion_pct':0},\n"
        "])\n"
    ),
    expected_output=(
        "=== KOTTER 8-STEP TRACKER: DevOps Transformation ===\n"
        "  Step 1: Create Urgency\n"
        "    Status: COMPLETE | Progress: 100%\n"
        "  Step 2: Form Coalition\n"
        "    Status: COMPLETE | Progress: 100%\n"
        "  Step 3: Create Vision\n"
        "    Status: COMPLETE | Progress: 100%\n"
        "  Step 4: Communicate Vision\n"
        "    Status: IN_PROGRESS | Progress: 60%\n"
        "  Step 5: Remove Obstacles\n"
        "    Status: IN_PROGRESS | Progress: 30%\n"
        "  Step 6: Generate Wins\n"
        "    Status: NOT_STARTED | Progress: 0%\n"
        "  Step 7: Build on Change\n"
        "    Status: NOT_STARTED | Progress: 0%\n"
        "  Step 8: Anchor Change\n"
        "    Status: NOT_STARTED | Progress: 0%\n"
        "─────────────────────────────\n"
        "Completed: 3/8 steps\n"
        "Overall Progress: 48%\n"
        "Current Focus: Step 4 - Communicate Vision\n"
        "Change Health: AT RISK"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L108 = dict(
    **_BASE, level_order=108, title="Adoption Curve Simulator", difficulty="medium",
    description=(
        "La curva de adopción de Rogers clasifica usuarios por cuándo adoptan una innovación. "
        "Implementa `adoption_curve(total_users, adoption_data)` donde adoption_data es "
        "`{'innovators': int, 'early_adopters': int, 'early_majority': int, "
        "'late_majority': int, 'laggards': int}` (conteos actuales).\n\n"
        "Benchmarks Rogers (% del total):\n"
        "innovators=2.5%, early_adopters=13.5%, early_majority=34%, late_majority=34%, laggards=16%.\n\n"
        "Imprime:\n"
        "`=== ADOPTION CURVE: N total users ===`\n"
        "Por segmento en orden:\n"
        "`  <Segment>: N users (N%) | Target: N% | Gap: +N% / -N% / ON TARGET`\n"
        "(Gap ON TARGET si |actual%-target%| < 1)\n\n"
        "Al final:\n"
        "`─────────────────────────────────`\n"
        "`Total Adopted: N (N%)`\n"
        "`Critical Mass: REACHED (early_majority ≥ target) / NOT REACHED`\n"
        "`Chasm Status: CROSSED (early_adopters + early_majority >= 16.5% of total) / AT CHASM`"
    ),
    hint="actual_pct = count/total*100. Calcula como float round(x,1). Chasm = (early_adopters+early_majority)/total*100 >= 16.5.",
    initial_code=(
        "def adoption_curve(total_users, adoption_data):\n"
        "    pass\n\n"
        "adoption_curve(1000, {\n"
        "    'innovators': 20,\n"
        "    'early_adopters': 110,\n"
        "    'early_majority': 280,\n"
        "    'late_majority': 150,\n"
        "    'laggards': 40,\n"
        "})\n"
    ),
    expected_output=(
        "=== ADOPTION CURVE: 1000 total users ===\n"
        "  Innovators: 20 users (2.0%) | Target: 2.5% | Gap: -0.5%\n"
        "  Early Adopters: 110 users (11.0%) | Target: 13.5% | Gap: -2.5%\n"
        "  Early Majority: 280 users (28.0%) | Target: 34.0% | Gap: -6.0%\n"
        "  Late Majority: 150 users (15.0%) | Target: 34.0% | Gap: -19.0%\n"
        "  Laggards: 40 users (4.0%) | Target: 16.0% | Gap: -12.0%\n"
        "─────────────────────────────────\n"
        "Total Adopted: 600 (60.0%)\n"
        "Critical Mass: NOT REACHED\n"
        "Chasm Status: CROSSED"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L109 = dict(
    **_BASE, level_order=109, title="Resistance Heatmap", difficulty="medium",
    description=(
        "Un mapa de calor de resistencia por departamento ayuda a focalizar esfuerzos. "
        "Implementa `resistance_heatmap(change_name, departments)` donde cada dept es "
        "`{'name': str, 'size': int, 'resistance_score': float}` (score 1.0-10.0).\n\n"
        "Imprime:\n"
        "`=== RESISTANCE HEATMAP: <change_name> ===`\n"
        "Por departamento (orden por resistance_score desc):\n"
        "`  <name> (<size> people) | Score: N.N | <nivel> | <barra>`\n\n"
        "Nivel: CRITICAL (≥8) / HIGH (≥6) / MEDIUM (≥4) / LOW (<4)\n"
        "Barra visual (10 chars): int(score) bloques de '▓' + resto '░'\n\n"
        "Al final:\n"
        "`─────────────────────────────────`\n"
        "`Weighted Resistance: N.N`  (sum(size*score)/sum(size))\n"
        "`Highest Risk Dept: <name>`\n"
        "`People at CRITICAL resistance: N`\n"
        "`Strategy: INTENSIVE ENGAGEMENT (weighted≥7) / TARGETED SUPPORT (≥5) / MONITOR (<5)`"
    ),
    hint="Weighted = sum(dept.size * dept.score) / sum(dept.size). Redondea a 1 decimal.",
    initial_code=(
        "def resistance_heatmap(change_name, departments):\n"
        "    pass\n\n"
        "resistance_heatmap('ERP Implementation', [\n"
        "    {'name': 'Finance',     'size': 50,  'resistance_score': 8.5},\n"
        "    {'name': 'Operations',  'size': 120, 'resistance_score': 6.2},\n"
        "    {'name': 'Engineering', 'size': 80,  'resistance_score': 3.8},\n"
        "    {'name': 'HR',          'size': 30,  'resistance_score': 7.1},\n"
        "    {'name': 'Sales',       'size': 90,  'resistance_score': 5.5},\n"
        "])\n"
    ),
    expected_output=(
        "=== RESISTANCE HEATMAP: ERP Implementation ===\n"
        "  Finance (50 people) | Score: 8.5 | CRITICAL | ▓▓▓▓▓▓▓▓░░\n"
        "  HR (30 people) | Score: 7.1 | HIGH | ▓▓▓▓▓▓▓░░░\n"
        "  Operations (120 people) | Score: 6.2 | HIGH | ▓▓▓▓▓▓░░░░\n"
        "  Sales (90 people) | Score: 5.5 | MEDIUM | ▓▓▓▓▓░░░░░\n"
        "  Engineering (80 people) | Score: 3.8 | LOW | ▓▓▓░░░░░░░\n"
        "─────────────────────────────────\n"
        "Weighted Resistance: 5.9\n"
        "Highest Risk Dept: Finance\n"
        "People at CRITICAL resistance: 50\n"
        "Strategy: TARGETED SUPPORT"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L110 = dict(
    **_BASE, level_order=110, title="Change Readiness Scorer", difficulty="medium",
    description=(
        "Mide qué tan lista está la organización para el cambio en 5 dimensiones. "
        "Implementa `change_readiness(organization, dimensions)` donde cada dimensión es "
        "`{'name': str, 'score': int, 'weight': float}` (score 1-10).\n\n"
        "Weighted score = sum(score * weight) / sum(weight).\n\n"
        "Imprime:\n"
        "`=== CHANGE READINESS: <organization> ===`\n"
        "Por dimensión (orden original):\n"
        "`  <name>: N/10 (weight: N.N) → <status>`\n"
        "Status: READY (≥7) / AT RISK (≥5) / NOT READY (<5)\n\n"
        "Al final:\n"
        "`─────────────────────────────`\n"
        "`Readiness Score: N.N/10`\n"
        "`Weakest Area: <name>`\n"
        "`Strongest Area: <name>`\n"
        "`Overall Status: READY / AT RISK / NOT READY`\n"
        "`Priority Actions:`\n"
        "Lista de dimensiones NOT READY (score<5), orden score asc:\n"
        "`  • Strengthen <name> (currently N/10)`"
    ),
    hint="Redondea weighted score a 1 decimal. Weakest = menor score. Strongest = mayor score.",
    initial_code=(
        "def change_readiness(organization, dimensions):\n"
        "    pass\n\n"
        "change_readiness('DAKI Corp', [\n"
        "    {'name': 'Leadership Alignment', 'score': 8, 'weight': 0.3},\n"
        "    {'name': 'Culture & Mindset',    'score': 5, 'weight': 0.25},\n"
        "    {'name': 'Process Maturity',     'score': 4, 'weight': 0.2},\n"
        "    {'name': 'Technology Readiness', 'score': 7, 'weight': 0.15},\n"
        "    {'name': 'Skills & Capacity',    'score': 3, 'weight': 0.1},\n"
        "])\n"
    ),
    expected_output=(
        "=== CHANGE READINESS: DAKI Corp ===\n"
        "  Leadership Alignment: 8/10 (weight: 0.3) → READY\n"
        "  Culture & Mindset: 5/10 (weight: 0.25) → AT RISK\n"
        "  Process Maturity: 4/10 (weight: 0.2) → NOT READY\n"
        "  Technology Readiness: 7/10 (weight: 0.15) → READY\n"
        "  Skills & Capacity: 3/10 (weight: 0.1) → NOT READY\n"
        "─────────────────────────────\n"
        "Readiness Score: 5.8/10\n"
        "Weakest Area: Skills & Capacity\n"
        "Strongest Area: Leadership Alignment\n"
        "Overall Status: AT RISK\n"
        "Priority Actions:\n"
        "  • Strengthen Skills & Capacity (currently 3/10)\n"
        "  • Strengthen Process Maturity (currently 4/10)"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L111 = dict(
    **_BASE, level_order=111, title="Communication Plan Builder", difficulty="medium",
    description=(
        "Un plan de comunicación de cambio debe cubrir audiencias, mensajes y canales. "
        "Implementa `communication_plan(change_name, audiences)` donde cada audience es "
        "`{'name': str, 'size': int, 'concern': str, 'channel': str, 'frequency': str}`.\n\n"
        "Imprime:\n"
        "`=== COMMUNICATION PLAN: <change_name> ===`\n"
        "`Total Reach: N people across N audiences`\n"
        "`─────────────────────────────────────`\n"
        "Por audience (orden original):\n"
        "`[<name>] — N people`\n"
        "`  Channel:   <channel>`\n"
        "`  Frequency: <frequency>`\n"
        "`  Key Message: Address concern about <concern>`\n"
        "`  Call to Action: Provide feedback via <channel>`\n\n"
        "Al final:\n"
        "`─────────────────────────────────────`\n"
        "`Channel Distribution:`\n"
        "Conteo de audiences por canal, orden desc por count:\n"
        "`  <channel>: N audience(s)`"
    ),
    hint="Total reach = sum(sizes). Channel distribution: Counter de channel values.",
    initial_code=(
        "def communication_plan(change_name, audiences):\n"
        "    pass\n\n"
        "communication_plan('Agile Transformation', [\n"
        "    {'name': 'Executive Team',  'size': 10,  'concern': 'ROI',            'channel': 'Email',   'frequency': 'Monthly'},\n"
        "    {'name': 'Engineering',     'size': 80,  'concern': 'workflow changes','channel': 'Slack',   'frequency': 'Weekly'},\n"
        "    {'name': 'Product Mgmt',    'size': 20,  'concern': 'process adoption','channel': 'Slack',   'frequency': 'Weekly'},\n"
        "    {'name': 'QA Team',         'size': 15,  'concern': 'role clarity',    'channel': 'Meeting', 'frequency': 'Bi-weekly'},\n"
        "])\n"
    ),
    expected_output=(
        "=== COMMUNICATION PLAN: Agile Transformation ===\n"
        "Total Reach: 125 people across 4 audiences\n"
        "─────────────────────────────────────\n"
        "[Executive Team] — 10 people\n"
        "  Channel:   Email\n"
        "  Frequency: Monthly\n"
        "  Key Message: Address concern about ROI\n"
        "  Call to Action: Provide feedback via Email\n"
        "[Engineering] — 80 people\n"
        "  Channel:   Slack\n"
        "  Frequency: Weekly\n"
        "  Key Message: Address concern about workflow changes\n"
        "  Call to Action: Provide feedback via Slack\n"
        "[Product Mgmt] — 20 people\n"
        "  Channel:   Slack\n"
        "  Frequency: Weekly\n"
        "  Key Message: Address concern about process adoption\n"
        "  Call to Action: Provide feedback via Slack\n"
        "[QA Team] — 15 people\n"
        "  Channel:   Meeting\n"
        "  Frequency: Bi-weekly\n"
        "  Key Message: Address concern about role clarity\n"
        "  Call to Action: Provide feedback via Meeting\n"
        "─────────────────────────────────────\n"
        "Channel Distribution:\n"
        "  Slack: 2 audience(s)\n"
        "  Email: 1 audience(s)\n"
        "  Meeting: 1 audience(s)"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L112 = dict(
    **_BASE, level_order=112, title="Training Plan Estimator", difficulty="medium",
    description=(
        "Planifica el entrenamiento necesario para el cambio. "
        "Implementa `training_estimator(change_name, groups)` donde cada group es "
        "`{'name': str, 'headcount': int, 'training_hours': float, 'delivery': str}` "
        "(delivery: IN_PERSON/ONLINE/HYBRID).\n\n"
        "Cost: IN_PERSON=$150/hr/person, ONLINE=$30/hr/person, HYBRID=$80/hr/person.\n\n"
        "Imprime:\n"
        "`=== TRAINING PLAN: <change_name> ===`\n"
        "Por grupo (orden original):\n"
        "`  <name>`\n"
        "`    Headcount: N | Hours: N.N | Mode: <delivery>`\n"
        "`    Cost: $N`\n\n"
        "Al final:\n"
        "`─────────────────────────────────`\n"
        "`Total Participants: N`\n"
        "`Total Training Hours: N.N`\n"
        "`Total Investment: $N`\n"
        "`Avg Cost per Person: $N`\n"
        "`Recommended Mode: <modo más usado>` (si hay empate, orden IN_PERSON>ONLINE>HYBRID)"
    ),
    hint="cost_per_group = headcount * hours * rate. Avg = total_cost / total_participants (int).",
    initial_code=(
        "def training_estimator(change_name, groups):\n"
        "    pass\n\n"
        "training_estimator('CRM Migration', [\n"
        "    {'name': 'Sales Team',   'headcount': 50, 'training_hours': 8.0,  'delivery': 'IN_PERSON'},\n"
        "    {'name': 'Support',      'headcount': 30, 'training_hours': 6.0,  'delivery': 'ONLINE'},\n"
        "    {'name': 'Management',   'headcount': 10, 'training_hours': 4.0,  'delivery': 'IN_PERSON'},\n"
        "    {'name': 'Engineering',  'headcount': 20, 'training_hours': 12.0, 'delivery': 'ONLINE'},\n"
        "])\n"
    ),
    expected_output=(
        "=== TRAINING PLAN: CRM Migration ===\n"
        "  Sales Team\n"
        "    Headcount: 50 | Hours: 8.0 | Mode: IN_PERSON\n"
        "    Cost: $60000\n"
        "  Support\n"
        "    Headcount: 30 | Hours: 6.0 | Mode: ONLINE\n"
        "    Cost: $5400\n"
        "  Management\n"
        "    Headcount: 10 | Hours: 4.0 | Mode: IN_PERSON\n"
        "    Cost: $6000\n"
        "  Engineering\n"
        "    Headcount: 20 | Hours: 12.0 | Mode: ONLINE\n"
        "    Cost: $7200\n"
        "─────────────────────────────────\n"
        "Total Participants: 110\n"
        "Total Training Hours: 30.0\n"
        "Total Investment: $78600\n"
        "Avg Cost per Person: $714\n"
        "Recommended Mode: IN_PERSON"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L113 = dict(
    **_BASE, level_order=113, title="Change Impact Analyzer", difficulty="medium",
    description=(
        "Analiza el impacto del cambio en procesos y personas. "
        "Implementa `change_impact(change_name, impacts)` donde cada impact es "
        "`{'area': str, 'impact_level': str, 'people_affected': int, 'process_change': str}` "
        "(impact_level: HIGH/MEDIUM/LOW).\n\n"
        "Imprime:\n"
        "`=== CHANGE IMPACT ANALYSIS: <change_name> ===`\n"
        "Agrupa por impact_level (orden: HIGH→MEDIUM→LOW):\n"
        "`[<LEVEL> IMPACT]`\n"
        "Por area dentro del grupo (orden original):\n"
        "`  <area> (N people)`\n"
        "`  Process: <process_change>`\n\n"
        "Al final:\n"
        "`─────────────────────────────────`\n"
        "`Total People Impacted: N`\n"
        "`HIGH Impact Areas: N`\n"
        "`Change Complexity: SEVERE (HIGH≥3) / MODERATE (HIGH≥1) / MANAGEABLE (HIGH=0)`\n"
        "`Recommended Approach:`\n"
        "SEVERE → Phased rollout with intensive change management\n"
        "MODERATE → Targeted support for high-impact areas\n"
        "MANAGEABLE → Standard communication and training"
    ),
    hint="Total people = sum(people_affected). Agrupa filtrando por impact_level.",
    initial_code=(
        "def change_impact(change_name, impacts):\n"
        "    pass\n\n"
        "change_impact('SAP Implementation', [\n"
        "    {'area': 'Finance',     'impact_level': 'HIGH',   'people_affected': 50,  'process_change': 'Complete workflow redesign'},\n"
        "    {'area': 'HR',          'impact_level': 'HIGH',   'people_affected': 25,  'process_change': 'New payroll system'},\n"
        "    {'area': 'Procurement', 'impact_level': 'HIGH',   'people_affected': 20,  'process_change': 'New approval flows'},\n"
        "    {'area': 'Operations',  'impact_level': 'MEDIUM', 'people_affected': 100, 'process_change': 'Updated reporting'},\n"
        "    {'area': 'IT',          'impact_level': 'MEDIUM', 'people_affected': 30,  'process_change': 'Infrastructure changes'},\n"
        "    {'area': 'Sales',       'impact_level': 'LOW',    'people_affected': 80,  'process_change': 'Minor UI changes'},\n"
        "])\n"
    ),
    expected_output=(
        "=== CHANGE IMPACT ANALYSIS: SAP Implementation ===\n"
        "[HIGH IMPACT]\n"
        "  Finance (50 people)\n"
        "  Process: Complete workflow redesign\n"
        "  HR (25 people)\n"
        "  Process: New payroll system\n"
        "  Procurement (20 people)\n"
        "  Process: New approval flows\n"
        "[MEDIUM IMPACT]\n"
        "  Operations (100 people)\n"
        "  Process: Updated reporting\n"
        "  IT (30 people)\n"
        "  Process: Infrastructure changes\n"
        "[LOW IMPACT]\n"
        "  Sales (80 people)\n"
        "  Process: Minor UI changes\n"
        "─────────────────────────────────\n"
        "Total People Impacted: 305\n"
        "HIGH Impact Areas: 3\n"
        "Change Complexity: SEVERE\n"
        "Recommended Approach: Phased rollout with intensive change management"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L114 = dict(
    **_BASE, level_order=114, title="Stakeholder Sentiment Tracker", difficulty="medium",
    description=(
        "Rastrea cómo evoluciona el sentimiento de stakeholders hacia el cambio a lo largo del tiempo. "
        "Implementa `sentiment_tracker(change_name, snapshots)` donde cada snapshot es "
        "`{'week': int, 'positive': int, 'neutral': int, 'negative': int}`.\n\n"
        "Imprime:\n"
        "`=== SENTIMENT TRACKER: <change_name> ===`\n"
        "Por snapshot (orden por week asc):\n"
        "`  Week N: +N% neutral:N% -N% | Net: +N / -N`\n"
        "(los porcentajes son round a 0 decimales del total de esa semana; "
        "Net = positive-negative)\n\n"
        "Al final:\n"
        "`─────────────────────────────`\n"
        "`Trend: IMPROVING / DECLINING / STABLE`\n"
        "(IMPROVING si Net última semana > Net primera semana, "
        "DECLINING si menor, STABLE si igual)\n"
        "`Latest snapshot:`\n"
        "`  Positive: N% | Neutral: N% | Negative: N%`\n"
        "`Sentiment Status: POSITIVE (positive%≥60) / MIXED (≥40) / NEGATIVE (<40)`"
    ),
    hint="total_week = positive+neutral+negative. pct = round(count/total*100). Latest = snapshot de mayor week.",
    initial_code=(
        "def sentiment_tracker(change_name, snapshots):\n"
        "    pass\n\n"
        "sentiment_tracker('Remote Work Policy', [\n"
        "    {'week': 1, 'positive': 30, 'neutral': 40, 'negative': 30},\n"
        "    {'week': 2, 'positive': 35, 'neutral': 38, 'negative': 27},\n"
        "    {'week': 3, 'positive': 45, 'neutral': 35, 'negative': 20},\n"
        "    {'week': 4, 'positive': 55, 'neutral': 30, 'negative': 15},\n"
        "])\n"
    ),
    expected_output=(
        "=== SENTIMENT TRACKER: Remote Work Policy ===\n"
        "  Week 1: +30% neutral:40% -30% | Net: +0\n"
        "  Week 2: +35% neutral:38% -27% | Net: +8\n"
        "  Week 3: +45% neutral:35% -20% | Net: +25\n"
        "  Week 4: +55% neutral:30% -15% | Net: +40\n"
        "─────────────────────────────\n"
        "Trend: IMPROVING\n"
        "Latest snapshot:\n"
        "  Positive: 55% | Neutral: 30% | Negative: 15%\n"
        "Sentiment Status: MIXED"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L115 = dict(
    **_BASE, level_order=115, title="Go-Live Readiness Checker", difficulty="medium",
    description=(
        "Antes de lanzar un cambio organizacional, verifica criterios clave. "
        "Implementa `go_live_checker(change_name, criteria)` donde cada criterion es "
        "`{'category': str, 'check': str, 'status': str, 'blocker': bool}` "
        "(status: PASS/FAIL/IN_PROGRESS).\n\n"
        "Imprime:\n"
        "`=== GO-LIVE READINESS: <change_name> ===`\n"
        "Por criterio (orden original):\n"
        "`  [PASS/FAIL/IN_PROGRESS] <category>: <check>`\n"
        "(si blocker=True y status≠PASS, añade ` ⚠ BLOCKER`)\n\n"
        "Al final:\n"
        "`─────────────────────────────────`\n"
        "`Results: N passed / N failed / N in progress`\n"
        "`Blockers outstanding: N`\n"
        "`Readiness Score: N%`  (passed/total*100 int)\n"
        "`DECISION: GO (0 blockers outstanding and readiness≥80%) / NO-GO`"
    ),
    hint="Blockers outstanding = count where blocker=True and status != PASS.",
    initial_code=(
        "def go_live_checker(change_name, criteria):\n"
        "    pass\n\n"
        "go_live_checker('HR System Launch', [\n"
        "    {'category': 'Training',    'check': 'All users trained',           'status': 'PASS',        'blocker': True},\n"
        "    {'category': 'Data',        'check': 'Data migration validated',     'status': 'PASS',        'blocker': True},\n"
        "    {'category': 'Testing',     'check': 'UAT sign-off received',        'status': 'PASS',        'blocker': True},\n"
        "    {'category': 'Support',     'check': 'Help desk trained',            'status': 'IN_PROGRESS', 'blocker': False},\n"
        "    {'category': 'Comms',       'check': 'Launch email sent',            'status': 'FAIL',        'blocker': False},\n"
        "    {'category': 'Rollback',    'check': 'Rollback plan documented',     'status': 'PASS',        'blocker': True},\n"
        "])\n"
    ),
    expected_output=(
        "=== GO-LIVE READINESS: HR System Launch ===\n"
        "  [PASS] Training: All users trained\n"
        "  [PASS] Data: Data migration validated\n"
        "  [PASS] Testing: UAT sign-off received\n"
        "  [IN_PROGRESS] Support: Help desk trained\n"
        "  [FAIL] Comms: Launch email sent\n"
        "  [PASS] Rollback: Rollback plan documented\n"
        "─────────────────────────────────\n"
        "Results: 4 passed / 1 failed / 1 in progress\n"
        "Blockers outstanding: 0\n"
        "Readiness Score: 66%\n"
        "DECISION: NO-GO"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L116 = dict(
    **_BASE, level_order=116, title="Rollout Progress Monitor", difficulty="medium",
    description=(
        "Monitorea el progreso de un rollout por oleadas. "
        "Implementa `rollout_monitor(change_name, waves)` donde cada wave es "
        "`{'wave': int, 'name': str, 'target': int, 'adopted': int, 'issues': int}`.\n\n"
        "Imprime:\n"
        "`=== ROLLOUT PROGRESS: <change_name> ===`\n"
        "Por ola (orden wave asc):\n"
        "`  Wave N - <name>`\n"
        "`    Target: N | Adopted: N | Rate: N% | Issues: N`\n"
        "`    Status: COMPLETE (≥90%) / ON TRACK (≥70%) / STRUGGLING (<70%)`\n\n"
        "Al final:\n"
        "`─────────────────────────────────`\n"
        "`Overall Adoption: N / N (N%)`\n"
        "`Total Issues: N`\n"
        "`Waves Complete: N / N`\n"
        "`Program Status: ON SCHEDULE (all waves COMPLETE or ON TRACK) / DELAYED`"
    ),
    hint="Rate = int(adopted/target*100). Overall = sum(adopted)/sum(target)*100 (int).",
    initial_code=(
        "def rollout_monitor(change_name, waves):\n"
        "    pass\n\n"
        "rollout_monitor('Cloud Migration', [\n"
        "    {'wave': 1, 'name': 'Pilot Group',    'target': 20,  'adopted': 19, 'issues': 2},\n"
        "    {'wave': 2, 'name': 'Early Adopters', 'target': 50,  'adopted': 47, 'issues': 5},\n"
        "    {'wave': 3, 'name': 'Main Rollout',   'target': 200, 'adopted': 130,'issues': 18},\n"
        "    {'wave': 4, 'name': 'Stragglers',     'target': 80,  'adopted': 10, 'issues': 3},\n"
        "])\n"
    ),
    expected_output=(
        "=== ROLLOUT PROGRESS: Cloud Migration ===\n"
        "  Wave 1 - Pilot Group\n"
        "    Target: 20 | Adopted: 19 | Rate: 95% | Issues: 2\n"
        "    Status: COMPLETE\n"
        "  Wave 2 - Early Adopters\n"
        "    Target: 50 | Adopted: 47 | Rate: 94% | Issues: 5\n"
        "    Status: COMPLETE\n"
        "  Wave 3 - Main Rollout\n"
        "    Target: 200 | Adopted: 130 | Rate: 65% | Issues: 18\n"
        "    Status: STRUGGLING\n"
        "  Wave 4 - Stragglers\n"
        "    Target: 80 | Adopted: 10 | Rate: 12% | Issues: 3\n"
        "    Status: STRUGGLING\n"
        "─────────────────────────────────\n"
        "Overall Adoption: 206 / 350 (58%)\n"
        "Total Issues: 28\n"
        "Waves Complete: 2 / 4\n"
        "Program Status: DELAYED"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L117 = dict(
    **_BASE, level_order=117, title="Change Benefit Realization", difficulty="medium",
    description=(
        "Los beneficios del cambio deben medirse vs las promesas originales. "
        "Implementa `benefit_realization(change_name, benefits)` donde cada benefit es "
        "`{'name': str, 'promised': float, 'realized': float, 'unit': str}`.\n\n"
        "Imprime:\n"
        "`=== BENEFIT REALIZATION: <change_name> ===`\n"
        "Por beneficio (orden original):\n"
        "`  <name>`\n"
        "`    Promised: N.N <unit> | Realized: N.N <unit>`\n"
        "`    Achievement: N% | <status>`\n"
        "Status: EXCEEDED (≥110%) / ON TARGET (≥90%) / BELOW TARGET (≥60%) / FAILING (<60%)\n\n"
        "Al final:\n"
        "`─────────────────────────────────`\n"
        "`Benefits Exceeded:    N`\n"
        "`Benefits On Target:   N`\n"
        "`Benefits Below Target: N`\n"
        "`Benefits Failing:     N`\n"
        "`Overall Realization: N%`  (sum(realized)/sum(promised)*100 int)\n"
        "`Change ROI Status: DELIVERING (≥80%) / UNDERPERFORMING (<80%)`"
    ),
    hint="achievement = int(realized/promised*100). Overall = int(sum(realized)/sum(promised)*100).",
    initial_code=(
        "def benefit_realization(change_name, benefits):\n"
        "    pass\n\n"
        "benefit_realization('Process Automation', [\n"
        "    {'name': 'Time saved',       'promised': 100.0, 'realized': 115.0, 'unit': 'hrs/month'},\n"
        "    {'name': 'Error reduction',  'promised': 50.0,  'realized': 48.0,  'unit': '%'},\n"
        "    {'name': 'Cost savings',     'promised': 200.0, 'realized': 120.0, 'unit': 'K USD'},\n"
        "    {'name': 'User adoption',    'promised': 90.0,  'realized': 45.0,  'unit': '%'},\n"
        "])\n"
    ),
    expected_output=(
        "=== BENEFIT REALIZATION: Process Automation ===\n"
        "  Time saved\n"
        "    Promised: 100.0 hrs/month | Realized: 115.0 hrs/month\n"
        "    Achievement: 115% | EXCEEDED\n"
        "  Error reduction\n"
        "    Promised: 50.0 % | Realized: 48.0 %\n"
        "    Achievement: 96% | ON TARGET\n"
        "  Cost savings\n"
        "    Promised: 200.0 K USD | Realized: 120.0 K USD\n"
        "    Achievement: 60% | BELOW TARGET\n"
        "  User adoption\n"
        "    Promised: 90.0 % | Realized: 45.0 %\n"
        "    Achievement: 50% | FAILING\n"
        "─────────────────────────────────\n"
        "Benefits Exceeded:    1\n"
        "Benefits On Target:   1\n"
        "Benefits Below Target: 1\n"
        "Benefits Failing:     1\n"
        "Overall Realization: 75%\n"
        "Change ROI Status: UNDERPERFORMING"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L118 = dict(
    **_BASE, level_order=118, title="Lessons Learned Compiler", difficulty="easy",
    description=(
        "Las lecciones aprendidas son el activo más valioso de la gestión del cambio. "
        "Implementa `lessons_compiler(project_name, lessons)` donde cada lesson es "
        "`{'category': str, 'what_happened': str, 'impact': str, 'lesson': str, 'type': str}` "
        "(type: SUCCESS/FAILURE/OBSERVATION).\n\n"
        "Imprime:\n"
        "`=== LESSONS LEARNED: <project_name> ===`\n"
        "Agrupa por type (orden: SUCCESS→FAILURE→OBSERVATION):\n"
        "`[<TYPE>S]` (pluraliza: SUCCESS→SUCCESSES, FAILURE→FAILURES, OBSERVATION→OBSERVATIONS)\n"
        "Por lesson dentro del grupo (orden original):\n"
        "`  Category: <category>`\n"
        "`  What: <what_happened>`\n"
        "`  Impact: <impact>`\n"
        "`  Lesson: <lesson>`\n"
        "`  ---`\n\n"
        "Al final:\n"
        "`─────────────────────────────────`\n"
        "`Total: N lessons (N successes, N failures, N observations)`\n"
        "`Top Category: <categoría que aparece más veces>`"
    ),
    hint="Top category = Counter(categories).most_common(1)[0][0].",
    initial_code=(
        "def lessons_compiler(project_name, lessons):\n"
        "    pass\n\n"
        "lessons_compiler('ERP Phase 1', [\n"
        "    {'category':'Training',    'what_happened':'Early training sessions oversubscribed',\n"
        "     'impact':'High engagement','lesson':'Schedule training 3 months ahead','type':'SUCCESS'},\n"
        "    {'category':'Comms',       'what_happened':'Late communication caused rumors',\n"
        "     'impact':'Low morale','lesson':'Communicate early and often','type':'FAILURE'},\n"
        "    {'category':'Training',    'what_happened':'Online modules underutilized',\n"
        "     'impact':'Knowledge gaps','lesson':'Mandate completion before go-live','type':'FAILURE'},\n"
        "    {'category':'Leadership',  'what_happened':'Exec sponsorship was visible',\n"
        "     'impact':'Faster adoption','lesson':'Visible leadership drives change','type':'SUCCESS'},\n"
        "    {'category':'Comms',       'what_happened':'FAQ page reduced support tickets',\n"
        "     'impact':'Neutral','lesson':'Self-service resources are valuable','type':'OBSERVATION'},\n"
        "])\n"
    ),
    expected_output=(
        "=== LESSONS LEARNED: ERP Phase 1 ===\n"
        "[SUCCESSES]\n"
        "  Category: Training\n"
        "  What: Early training sessions oversubscribed\n"
        "  Impact: High engagement\n"
        "  Lesson: Schedule training 3 months ahead\n"
        "  ---\n"
        "  Category: Leadership\n"
        "  What: Exec sponsorship was visible\n"
        "  Impact: Faster adoption\n"
        "  Lesson: Visible leadership drives change\n"
        "  ---\n"
        "[FAILURES]\n"
        "  Category: Comms\n"
        "  What: Late communication caused rumors\n"
        "  Impact: Low morale\n"
        "  Lesson: Communicate early and often\n"
        "  ---\n"
        "  Category: Training\n"
        "  What: Online modules underutilized\n"
        "  Impact: Knowledge gaps\n"
        "  Lesson: Mandate completion before go-live\n"
        "  ---\n"
        "[OBSERVATIONS]\n"
        "  Category: Comms\n"
        "  What: FAQ page reduced support tickets\n"
        "  Impact: Neutral\n"
        "  Lesson: Self-service resources are valuable\n"
        "  ---\n"
        "─────────────────────────────────\n"
        "Total: 5 lessons (2 successes, 2 failures, 1 observations)\n"
        "Top Category: Training"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L119 = dict(
    **_BASE, level_order=119, title="Change Fatigue Index", difficulty="medium",
    description=(
        "La fatiga del cambio ocurre cuando hay demasiados cambios simultáneos. "
        "Implementa `change_fatigue_index(team_name, active_changes)` donde cada change es "
        "`{'name': str, 'duration_months': int, 'intensity': str, 'affected_pct': float}` "
        "(intensity: HIGH/MEDIUM/LOW).\n\n"
        "Weights de intensidad: HIGH=3, MEDIUM=2, LOW=1.\n"
        "Impact score por cambio = intensity_weight * affected_pct * duration_months.\n"
        "Fatigue Index = sum(impact_scores) / 100 (redondea a 1 decimal).\n\n"
        "Imprime:\n"
        "`=== CHANGE FATIGUE INDEX: <team_name> ===`\n"
        "Por cambio (orden por impact_score desc):\n"
        "`  <name> | <intensity> | N months | N% affected | Impact: N.N`\n\n"
        "Al final:\n"
        "`─────────────────────────────────`\n"
        "`Active Changes: N`\n"
        "`Fatigue Index: N.N`\n"
        "`Risk Level: CRITICAL (≥10) / HIGH (≥5) / MODERATE (≥2) / LOW (<2)`\n"
        "`Recommendation:`\n"
        "CRITICAL → Freeze non-critical changes immediately\n"
        "HIGH → Sequence changes, avoid overlaps\n"
        "MODERATE → Monitor closely, increase support\n"
        "LOW → Healthy change capacity"
    ),
    hint="impact = intensity_weight * affected_pct * duration_months. Fatigue = round(sum(impacts)/100, 1).",
    initial_code=(
        "def change_fatigue_index(team_name, active_changes):\n"
        "    pass\n\n"
        "change_fatigue_index('Engineering Org', [\n"
        "    {'name': 'Cloud Migration',  'duration_months': 6, 'intensity': 'HIGH',   'affected_pct': 80.0},\n"
        "    {'name': 'Agile Adoption',   'duration_months': 4, 'intensity': 'HIGH',   'affected_pct': 100.0},\n"
        "    {'name': 'New HR System',    'duration_months': 3, 'intensity': 'MEDIUM', 'affected_pct': 60.0},\n"
        "    {'name': 'Office Relocation','duration_months': 2, 'intensity': 'LOW',    'affected_pct': 100.0},\n"
        "])\n"
    ),
    expected_output=(
        "=== CHANGE FATIGUE INDEX: Engineering Org ===\n"
        "  Agile Adoption | HIGH | 4 months | 100.0% affected | Impact: 1200.0\n"
        "  Cloud Migration | HIGH | 6 months | 80.0% affected | Impact: 1440.0\n"
        "  New HR System | MEDIUM | 3 months | 60.0% affected | Impact: 360.0\n"
        "  Office Relocation | LOW | 2 months | 100.0% affected | Impact: 200.0\n"
        "─────────────────────────────────\n"
        "Active Changes: 4\n"
        "Fatigue Index: 32.0\n"
        "Risk Level: CRITICAL\n"
        "Recommendation: Freeze non-critical changes immediately"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L120 = dict(
    **_BASE_BOSS, level_order=120, title="Change Management Command Center", difficulty="hard",
    is_phase_boss=True, is_project=True,
    description=(
        "BOSS L120: Eres el Change Management Command Center. "
        "Implementa la clase `ChangeCommandCenter` con:\n\n"
        "`__init__(self, tpm_name, change_name)` — almacena nombre TPM y del cambio.\n\n"
        "`assess_readiness(score)` — score float. Imprime:\n"
        "`Readiness: N.N/10 → <READY/AT RISK/NOT READY>`\n\n"
        "`track_adoption(waves)` — waves: lista `{'name': str, 'rate': int}`. "
        "Calcula avg rate. Imprime:\n"
        "`Adoption across N waves: avg N%`\n"
        "`Status: ON TRACK (avg≥70%) / DELAYED`\n\n"
        "`log_lesson(category, lesson_type, text)` — almacena en lista interna. Imprime:\n"
        "`Lesson logged: [<lesson_type>] <category>`\n\n"
        "`command_report()` — imprime:\n"
        "`=== CHANGE COMMAND CENTER ===`\n"
        "`TPM: <tpm_name> | Change: <change_name>`\n"
        "`Lessons captured: N`\n"
        "`Status: CHANGE AGENT ACTIVE`"
    ),
    hint="track_adoption avg = int(sum(rates)/len(waves)). Readiness: READY≥7, AT RISK≥5, NOT READY<5.",
    initial_code=(
        "class ChangeCommandCenter:\n"
        "    def __init__(self, tpm_name, change_name):\n"
        "        pass\n"
        "    def assess_readiness(self, score):\n"
        "        pass\n"
        "    def track_adoption(self, waves):\n"
        "        pass\n"
        "    def log_lesson(self, category, lesson_type, text):\n"
        "        pass\n"
        "    def command_report(self):\n"
        "        pass\n\n"
        "ccc = ChangeCommandCenter('Ana Reyes', 'Digital Transformation')\n"
        "ccc.assess_readiness(6.5)\n"
        "ccc.track_adoption([\n"
        "    {'name': 'Wave 1', 'rate': 92},\n"
        "    {'name': 'Wave 2', 'rate': 78},\n"
        "    {'name': 'Wave 3', 'rate': 65},\n"
        "])\n"
        "ccc.log_lesson('Training', 'SUCCESS', 'Early sessions drove engagement')\n"
        "ccc.log_lesson('Comms', 'FAILURE', 'Late updates caused confusion')\n"
        "ccc.command_report()\n"
    ),
    expected_output=(
        "Readiness: 6.5/10 → AT RISK\n"
        "Adoption across 3 waves: avg 78%\n"
        "Status: ON TRACK\n"
        "Lesson logged: [SUCCESS] Training\n"
        "Lesson logged: [FAILURE] Comms\n"
        "=== CHANGE COMMAND CENTER ===\n"
        "TPM: Ana Reyes | Change: Digital Transformation\n"
        "Lessons captured: 2\n"
        "Status: CHANGE AGENT ACTIVE"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
BLOQUE8 = [L106, L107, L108, L109, L110, L111, L112, L113, L114, L115,
           L116, L117, L118, L119, L120]
