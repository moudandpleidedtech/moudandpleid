"""
_tpm_b2.py — TPM Mastery · BLOQUE 2 (L16–L30)
===============================================
Fase: credibilidad_tecnica
Niveles: 16 a 30 (15 desafíos Python)
Boss: L30 — System Reliability Scorecard
"""
from __future__ import annotations

_BASE = dict(
    codex_id       = "tpm_mastery",
    sector_id      = 21,
    challenge_type = "python",
    phase          = "credibilidad_tecnica",
    is_free        = False,
    strict_match   = False,
    is_phase_boss  = False,
    is_project     = False,
)
_BASE_BOSS = {k: v for k, v in _BASE.items() if k not in ("is_phase_boss", "is_project")}

# ─────────────────────────────────────────────────────────────────────────────
# L16 — SLA vs SLO Calculator
# ─────────────────────────────────────────────────────────────────────────────
L16 = dict(
    **_BASE,
    level_order   = 16,
    title         = "SLA vs SLO Calculator",
    difficulty    = "medium",
    description   = (
        "Un TPM técnico distingue entre SLA (contrato con cliente) y SLO (objetivo interno). "
        "Implementa `sla_slo_report(services)` que evalúa ambos para cada servicio.\n\n"
        "Cada servicio:\n"
        "`{'name': str, 'uptime_pct': float, 'slo_target': float, 'sla_target': float}`\n\n"
        "Para cada servicio imprime:\n"
        "`<name>: uptime=X%  SLO=[MET|MISSED]  SLA=[MET|BREACHED]`\n\n"
        "SLO MET si uptime_pct >= slo_target.\n"
        "SLA MET si uptime_pct >= sla_target.\n\n"
        "Al final: `SLO: N/M met  |  SLA: N/M met`"
    ),
    hint          = "SLO es el objetivo interno (más estricto). SLA es el compromiso externo.",
    initial_code  = (
        "def sla_slo_report(services):\n"
        "    pass\n\n"
        "services = [\n"
        "    {'name': 'API Gateway',    'uptime_pct': 99.97, 'slo_target': 99.95, 'sla_target': 99.9},\n"
        "    {'name': 'Auth Service',   'uptime_pct': 99.85, 'slo_target': 99.95, 'sla_target': 99.9},\n"
        "    {'name': 'Data Pipeline',  'uptime_pct': 99.91, 'slo_target': 99.95, 'sla_target': 99.9},\n"
        "    {'name': 'Notif Service',  'uptime_pct': 99.80, 'slo_target': 99.9,  'sla_target': 99.5},\n"
        "]\n"
        "sla_slo_report(services)\n"
    ),
    expected_output = (
        "API Gateway:   uptime=99.97%  SLO=MET      SLA=MET\n"
        "Auth Service:  uptime=99.85%  SLO=MISSED   SLA=BREACHED\n"
        "Data Pipeline: uptime=99.91%  SLO=MISSED   SLA=MET\n"
        "Notif Service: uptime=99.80%  SLO=MISSED   SLA=MET\n"
        "SLO: 1/4 met  |  SLA: 3/4 met"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L17 — Error Budget Calculator
# ─────────────────────────────────────────────────────────────────────────────
L17 = dict(
    **_BASE,
    level_order   = 17,
    title         = "Error Budget Calculator",
    difficulty    = "medium",
    description   = (
        "El error budget es el tiempo de downtime permitido según el SLO. "
        "Implementa `error_budget_report(services, period_days)` que calcula el budget.\n\n"
        "Cada servicio: `{'name': str, 'slo_pct': float, 'actual_uptime_pct': float}`.\n\n"
        "Para cada servicio:\n"
        "- `budget_minutes = (1 - slo_pct/100) * period_days * 24 * 60` (2 dec)\n"
        "- `used_minutes   = (1 - actual_uptime_pct/100) * period_days * 24 * 60` (2 dec)\n"
        "- `remaining_pct  = max(0, (budget_minutes - used_minutes) / budget_minutes * 100)` (1 dec)\n\n"
        "Imprime:\n"
        "`<name>: budget=Xmin  used=Xmin  remaining=X%  [HEALTHY|BURNING|EXHAUSTED]`\n\n"
        "HEALTHY si remaining >= 50%, BURNING si > 0%, EXHAUSTED si 0%."
    ),
    hint          = "period_days * 24 * 60 = total minutos del período. Redondea a 2 o 1 decimal según campo.",
    initial_code  = (
        "def error_budget_report(services, period_days):\n"
        "    pass\n\n"
        "services = [\n"
        "    {'name': 'Payment API',  'slo_pct': 99.9,  'actual_uptime_pct': 99.95},\n"
        "    {'name': 'Search API',   'slo_pct': 99.9,  'actual_uptime_pct': 99.82},\n"
        "    {'name': 'Webhook Svc',  'slo_pct': 99.5,  'actual_uptime_pct': 99.5},\n"
        "]\n"
        "error_budget_report(services, period_days=30)\n"
    ),
    expected_output = (
        "Payment API:  budget=43.20min  used=7.20min   remaining=83.3%  HEALTHY\n"
        "Search API:   budget=43.20min  used=115.20min  remaining=0.0%  EXHAUSTED\n"
        "Webhook Svc:  budget=216.00min  used=216.00min  remaining=0.0%  EXHAUSTED"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L18 — API Capacity Planner
# ─────────────────────────────────────────────────────────────────────────────
L18 = dict(
    **_BASE,
    level_order   = 18,
    title         = "API Capacity Planner",
    difficulty    = "medium",
    description   = (
        "Implementa `capacity_plan(endpoints, growth_rate, months)` que proyecta el tráfico "
        "de endpoints API para planificar infraestructura.\n\n"
        "Cada endpoint: `{'path': str, 'current_rps': float, 'max_capacity_rps': float}`.\n\n"
        "La proyección mensual aplica `current_rps * (1 + growth_rate) ** month`.\n\n"
        "Para cada endpoint imprime la tabla de proyección:\n"
        "`<path>  current=Xrps  capacity=Xrps`\n"
        "Luego por mes: `  Month N: Xrps  [OK|WARNING|CRITICAL]`\n\n"
        "WARNING si projected > capacity * 0.8.\n"
        "CRITICAL si projected > capacity.\n"
        "Incluye el primer mes que alcanza WARNING y el primero que alcanza CRITICAL "
        "(o `Never` si no ocurre dentro del período)."
    ),
    hint          = "Usa round(x, 1) para los rps. Evalúa WARNING antes que CRITICAL.",
    initial_code  = (
        "def capacity_plan(endpoints, growth_rate, months):\n"
        "    pass\n\n"
        "endpoints = [\n"
        "    {'path': '/api/search',   'current_rps': 850.0,  'max_capacity_rps': 1000.0},\n"
        "    {'path': '/api/checkout', 'current_rps': 200.0,  'max_capacity_rps': 500.0},\n"
        "]\n"
        "capacity_plan(endpoints, growth_rate=0.05, months=4)\n"
    ),
    expected_output = (
        "/api/search  current=850.0rps  capacity=1000.0rps\n"
        "  Month 1: 892.5rps  WARNING\n"
        "  Month 2: 937.1rps  WARNING\n"
        "  Month 3: 984.0rps  WARNING\n"
        "  Month 4: 1033.2rps  CRITICAL\n"
        "  First WARNING: Month 1  |  First CRITICAL: Month 4\n"
        "/api/checkout  current=200.0rps  capacity=500.0rps\n"
        "  Month 1: 210.0rps  OK\n"
        "  Month 2: 220.5rps  OK\n"
        "  Month 3: 231.5rps  OK\n"
        "  Month 4: 243.1rps  OK\n"
        "  First WARNING: Never  |  First CRITICAL: Never"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L19 — DORA Metrics Calculator
# ─────────────────────────────────────────────────────────────────────────────
L19 = dict(
    **_BASE,
    level_order   = 19,
    title         = "DORA Metrics Calculator",
    difficulty    = "hard",
    description   = (
        "Las métricas DORA son el lenguaje de ingeniería de elite. "
        "Implementa `dora_report(deployments, incidents)` que calcula las 4 métricas.\n\n"
        "deployments: lista de `{'date': str, 'lead_time_hours': float}`.\n"
        "incidents: lista de `{'date': str, 'severity': str, 'ttr_hours': float}` "
        "(solo severity='p1' cuenta para MTTR).\n\n"
        "Métricas:\n"
        "1. **Deployment Frequency**: deploys / días del período (format: X.X deploys/day)\n"
        "2. **Lead Time for Changes**: promedio de lead_time_hours (1 dec) en horas\n"
        "3. **Change Failure Rate**: incidents / deployments * 100 (1 dec) %\n"
        "4. **MTTR**: promedio de ttr_hours de incidentes p1 (1 dec) en horas\n\n"
        "El período va desde el deploy más antiguo al más reciente (inclusive).\n\n"
        "Clasifica cada métrica como Elite/High/Medium/Low según DORA 2023 benchmarks:\n"
        "- Deploy Freq: Elite≥1/day, High≥1/week(0.14), Medium≥1/month(0.03), Low<\n"
        "- Lead Time: Elite<1h, High<1day(24h), Medium<1week(168h), Low>=\n"
        "- CFR: Elite<5%, High<10%, Medium<15%, Low>=\n"
        "- MTTR: Elite<1h, High<24h, Medium<168h, Low>="
    ),
    hint          = "Días del período = (max_date - min_date).days + 1. Usa date.fromisoformat().",
    initial_code  = (
        "from datetime import date\n\n"
        "def dora_report(deployments, incidents):\n"
        "    pass\n\n"
        "deployments = [\n"
        "    {'date': '2024-01-02', 'lead_time_hours': 3.5},\n"
        "    {'date': '2024-01-05', 'lead_time_hours': 5.0},\n"
        "    {'date': '2024-01-09', 'lead_time_hours': 2.0},\n"
        "    {'date': '2024-01-12', 'lead_time_hours': 8.0},\n"
        "    {'date': '2024-01-16', 'lead_time_hours': 4.5},\n"
        "    {'date': '2024-01-19', 'lead_time_hours': 1.5},\n"
        "]\n"
        "incidents = [\n"
        "    {'date': '2024-01-07', 'severity': 'p1', 'ttr_hours': 2.5},\n"
        "    {'date': '2024-01-14', 'severity': 'p2', 'ttr_hours': 0.5},\n"
        "    {'date': '2024-01-18', 'severity': 'p1', 'ttr_hours': 1.0},\n"
        "]\n"
        "dora_report(deployments, incidents)\n"
    ),
    expected_output = (
        "DORA Metrics Report\n"
        "Deployment Frequency : 0.3 deploys/day  [Medium]\n"
        "Lead Time for Changes: 4.1h              [Elite]\n"
        "Change Failure Rate  : 50.0%             [Low]\n"
        "MTTR                 : 1.8h              [High]"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L20 — Incident Severity Classifier
# ─────────────────────────────────────────────────────────────────────────────
L20 = dict(
    **_BASE,
    level_order   = 20,
    title         = "Incident Severity Classifier",
    difficulty    = "medium",
    description   = (
        "Un TPM responde a incidentes con claridad y velocidad. "
        "Implementa `classify_incidents(incidents)` que asigna severidad P1-P4.\n\n"
        "Cada incidente: `{'id': str, 'users_affected': int, 'revenue_impact': bool, "
        "'data_loss': bool, 'service_down': bool}`.\n\n"
        "Reglas (evalúa en orden, la primera que aplique gana):\n"
        "- P1: data_loss=True O (service_down=True Y revenue_impact=True)\n"
        "- P2: service_down=True O (revenue_impact=True Y users_affected >= 1000)\n"
        "- P3: users_affected >= 100\n"
        "- P4: resto\n\n"
        "Imprime: `[P<N>] <id>: <razón>`\n\n"
        "Razones: 'data loss detected', 'service down + revenue impact', "
        "'service disruption', 'revenue + high user impact', "
        "'significant user impact', 'minor impact'.\n\n"
        "Al final: `P1: N  P2: N  P3: N  P4: N`"
    ),
    hint          = "Evalúa P1 primero. Si no aplica, evalúa P2. El orden importa.",
    initial_code  = (
        "def classify_incidents(incidents):\n"
        "    pass\n\n"
        "incidents = [\n"
        "    {'id': 'INC-01', 'users_affected': 5000, 'revenue_impact': True,  'data_loss': False, 'service_down': True},\n"
        "    {'id': 'INC-02', 'users_affected': 200,  'revenue_impact': False, 'data_loss': True,  'service_down': False},\n"
        "    {'id': 'INC-03', 'users_affected': 1500, 'revenue_impact': True,  'data_loss': False, 'service_down': False},\n"
        "    {'id': 'INC-04', 'users_affected': 300,  'revenue_impact': False, 'data_loss': False, 'service_down': False},\n"
        "    {'id': 'INC-05', 'users_affected': 10,   'revenue_impact': False, 'data_loss': False, 'service_down': False},\n"
        "]\n"
        "classify_incidents(incidents)\n"
    ),
    expected_output = (
        "[P1] INC-01: service down + revenue impact\n"
        "[P1] INC-02: data loss detected\n"
        "[P2] INC-03: revenue + high user impact\n"
        "[P3] INC-04: significant user impact\n"
        "[P4] INC-05: minor impact\n"
        "P1: 2  P2: 1  P3: 1  P4: 1"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L21 — Scalability Math
# ─────────────────────────────────────────────────────────────────────────────
L21 = dict(
    **_BASE,
    level_order   = 21,
    title         = "Scalability Math",
    difficulty    = "hard",
    description   = (
        "Un TPM debe entender cuántos servidores necesita el equipo y cuándo. "
        "Implementa `scale_calculator(config)` que modela el crecimiento y la infraestructura.\n\n"
        "config: `{'users_today': int, 'growth_pct_month': float, 'rps_per_user': float, "
        "'server_capacity_rps': int, 'months': int}`.\n\n"
        "Para cada mes, calcula:\n"
        "- `users = users_today * (1 + growth_pct_month/100) ** month`\n"
        "- `total_rps = users * rps_per_user`\n"
        "- `servers_needed = ceil(total_rps / server_capacity_rps)`\n\n"
        "Imprime por mes:\n"
        "`Month N: users=X  rps=X  servers=N`\n\n"
        "Al final: `Servers today: N  Servers month-N: N  Growth: Nx`\n"
        "(Growth = servidores finales / servidores iniciales, 1 decimal)"
    ),
    hint          = "Importa math.ceil. Los usuarios del mes 0 son users_today.",
    initial_code  = (
        "import math\n\n"
        "def scale_calculator(config):\n"
        "    pass\n\n"
        "scale_calculator({\n"
        "    'users_today':          10000,\n"
        "    'growth_pct_month':     15,\n"
        "    'rps_per_user':         0.05,\n"
        "    'server_capacity_rps':  100,\n"
        "    'months':               4,\n"
        "})\n"
    ),
    expected_output = (
        "Month 1: users=11500  rps=575.0  servers=6\n"
        "Month 2: users=13225  rps=661.2  servers=7\n"
        "Month 3: users=15209  rps=760.4  servers=8\n"
        "Month 4: users=17490  rps=874.5  servers=9\n"
        "Servers today: 5  Servers month-4: 9  Growth: 1.8x"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L22 — CI/CD Pipeline Analyzer
# ─────────────────────────────────────────────────────────────────────────────
L22 = dict(
    **_BASE,
    level_order   = 22,
    title         = "CI/CD Pipeline Analyzer",
    difficulty    = "medium",
    description   = (
        "Un TPM que entiende los pipelines puede hablar con credibilidad con el equipo de DevOps. "
        "Implementa `analyze_pipeline(runs)` que analiza corridas de CI/CD.\n\n"
        "Cada run: `{'id': str, 'stages': list[dict]}`.\n"
        "Cada stage: `{'name': str, 'duration_s': int, 'status': str}`.\n\n"
        "Para cada run imprime:\n"
        "`Run <id>: total=Xs  status=[PASS|FAIL]`\n"
        "Luego la etapa más lenta: `  Bottleneck: <name> (Xs)`\n\n"
        "Un run es FAIL si alguna etapa tiene status='failed'.\n\n"
        "Al final imprime:\n"
        "`Avg pipeline time: Xs  |  Pass rate: X%  |  Top bottleneck: <name>`\n\n"
        "Top bottleneck global = etapa con mayor duration_s entre todos los runs."
    ),
    hint          = "Acumula las duraciones y busca el máximo global en una segunda pasada.",
    initial_code  = (
        "def analyze_pipeline(runs):\n"
        "    pass\n\n"
        "runs = [\n"
        "    {'id': 'run-01', 'stages': [\n"
        "        {'name': 'build',      'duration_s': 45,  'status': 'passed'},\n"
        "        {'name': 'unit-test',  'duration_s': 120, 'status': 'passed'},\n"
        "        {'name': 'e2e',        'duration_s': 310, 'status': 'passed'},\n"
        "        {'name': 'deploy-stg', 'duration_s': 60,  'status': 'passed'},\n"
        "    ]},\n"
        "    {'id': 'run-02', 'stages': [\n"
        "        {'name': 'build',      'duration_s': 42,  'status': 'passed'},\n"
        "        {'name': 'unit-test',  'duration_s': 115, 'status': 'failed'},\n"
        "        {'name': 'e2e',        'duration_s': 0,   'status': 'skipped'},\n"
        "        {'name': 'deploy-stg', 'duration_s': 0,   'status': 'skipped'},\n"
        "    ]},\n"
        "    {'id': 'run-03', 'stages': [\n"
        "        {'name': 'build',      'duration_s': 48,  'status': 'passed'},\n"
        "        {'name': 'unit-test',  'duration_s': 118, 'status': 'passed'},\n"
        "        {'name': 'e2e',        'duration_s': 298, 'status': 'passed'},\n"
        "        {'name': 'deploy-stg', 'duration_s': 55,  'status': 'passed'},\n"
        "    ]},\n"
        "]\n"
        "analyze_pipeline(runs)\n"
    ),
    expected_output = (
        "Run run-01: total=535s  status=PASS\n"
        "  Bottleneck: e2e (310s)\n"
        "Run run-02: total=157s  status=FAIL\n"
        "  Bottleneck: unit-test (115s)\n"
        "Run run-03: total=519s  status=PASS\n"
        "  Bottleneck: e2e (298s)\n"
        "Avg pipeline time: 404s  |  Pass rate: 67%  |  Top bottleneck: e2e"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L23 — Technical Debt Tracker
# ─────────────────────────────────────────────────────────────────────────────
L23 = dict(
    **_BASE,
    level_order   = 23,
    title         = "Technical Debt Tracker",
    difficulty    = "medium",
    description   = (
        "La deuda técnica es riesgo de programa disfrazado de código. "
        "Implementa `debt_report(items)` que cuantifica y prioriza la deuda técnica.\n\n"
        "Cada item: `{'id': str, 'desc': str, 'effort_days': int, "
        "'interest_days_per_sprint': float, 'sprints_active': int}`.\n\n"
        "Calcula:\n"
        "- `total_interest = interest_days_per_sprint * sprints_active`\n"
        "- `debt_ratio = total_interest / effort_days` (2 dec) — cuántas veces el costo ya supera el fix\n\n"
        "Ordena por debt_ratio descendente.\n\n"
        "Imprime por item:\n"
        "`[PAYOFF NOW|PAY SOON|MONITOR] <id>: <desc>`\n"
        "`  effort=Nd  interest_accrued=Nd  ratio=X`\n\n"
        "PAYOFF NOW si ratio >= 2, PAY SOON si ratio >= 1, MONITOR si < 1.\n\n"
        "Al final: `Total accrued interest: Nd  Payoff now: N items`"
    ),
    hint          = "Calcula interest total, luego el ratio. Redondea interest a int para la impresión.",
    initial_code  = (
        "def debt_report(items):\n"
        "    pass\n\n"
        "items = [\n"
        "    {'id': 'TD-01', 'desc': 'Monolithic auth module',    'effort_days': 5,  'interest_days_per_sprint': 0.5, 'sprints_active': 12},\n"
        "    {'id': 'TD-02', 'desc': 'Missing DB indexes',        'effort_days': 2,  'interest_days_per_sprint': 0.8, 'sprints_active': 6},\n"
        "    {'id': 'TD-03', 'desc': 'No integration test suite', 'effort_days': 10, 'interest_days_per_sprint': 0.3, 'sprints_active': 8},\n"
        "    {'id': 'TD-04', 'desc': 'Hardcoded config values',   'effort_days': 1,  'interest_days_per_sprint': 0.1, 'sprints_active': 20},\n"
        "]\n"
        "debt_report(items)\n"
    ),
    expected_output = (
        "[PAYOFF NOW] TD-02: Missing DB indexes\n"
        "  effort=2d  interest_accrued=5d  ratio=2.4\n"
        "[PAYOFF NOW] TD-01: Monolithic auth module\n"
        "  effort=5d  interest_accrued=6d  ratio=1.2\n"
        "[MONITOR]    TD-04: Hardcoded config values\n"
        "  effort=1d  interest_accrued=2d  ratio=2.0\n"
        "[MONITOR]    TD-03: No integration test suite\n"
        "  effort=10d  interest_accrued=2d  ratio=0.24\n"
        "Total accrued interest: 15d  Payoff now: 2 items"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L24 — Database Scalability Advisor
# ─────────────────────────────────────────────────────────────────────────────
L24 = dict(
    **_BASE,
    level_order   = 24,
    title         = "Database Scalability Advisor",
    difficulty    = "hard",
    description   = (
        "Implementa `db_advisor(tables)` que analiza tablas de base de datos y "
        "recomienda acciones de escalabilidad.\n\n"
        "Cada tabla: `{'name': str, 'rows_millions': float, 'avg_query_ms': float, "
        "'indexes': int, 'has_partition': bool}`.\n\n"
        "Reglas de diagnóstico (aplica TODAS las que aplican, en este orden):\n"
        "1. rows > 100M y no partition → `RECOMMEND: add table partitioning`\n"
        "2. avg_query_ms > 500 → `RECOMMEND: query optimization needed`\n"
        "3. indexes == 0 → `RECOMMEND: add indexes`\n"
        "4. avg_query_ms < 10 y indexes > 3 → `NOTE: may have too many indexes`\n\n"
        "Imprime por tabla:\n"
        "`<name> (rows=XM, query=Xms, idx=N[, partitioned]):`\n"
        "Luego cada recomendación con `  → <rec>`.\n"
        "Si no hay recomendaciones: `  → OK: no action needed`\n\n"
        "Al final: `Tables analyzed: N  Requiring action: N`"
    ),
    hint          = "Evalúa todas las reglas independientemente, no uses elif.",
    initial_code  = (
        "def db_advisor(tables):\n"
        "    pass\n\n"
        "tables = [\n"
        "    {'name': 'events',       'rows_millions': 250.0, 'avg_query_ms': 820.0, 'indexes': 2, 'has_partition': False},\n"
        "    {'name': 'users',        'rows_millions': 5.0,   'avg_query_ms': 8.0,   'indexes': 5, 'has_partition': False},\n"
        "    {'name': 'transactions', 'rows_millions': 120.0, 'avg_query_ms': 45.0,  'indexes': 0, 'has_partition': True},\n"
        "    {'name': 'sessions',     'rows_millions': 30.0,  'avg_query_ms': 12.0,  'indexes': 1, 'has_partition': False},\n"
        "]\n"
        "db_advisor(tables)\n"
    ),
    expected_output = (
        "events (rows=250.0M, query=820.0ms, idx=2):\n"
        "  → RECOMMEND: add table partitioning\n"
        "  → RECOMMEND: query optimization needed\n"
        "users (rows=5.0M, query=8.0ms, idx=5):\n"
        "  → NOTE: may have too many indexes\n"
        "transactions (rows=120.0M, query=45.0ms, idx=0, partitioned):\n"
        "  → RECOMMEND: add indexes\n"
        "sessions (rows=30.0M, query=12.0ms, idx=1):\n"
        "  → OK: no action needed\n"
        "Tables analyzed: 4  Requiring action: 3"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L25 — System Tradeoff Evaluator
# ─────────────────────────────────────────────────────────────────────────────
L25 = dict(
    **_BASE,
    level_order   = 25,
    title         = "System Tradeoff Evaluator",
    difficulty    = "hard",
    description   = (
        "Un TPM entiende y comunica tradeoffs arquitectónicos. "
        "Implementa `evaluate_tradeoffs(options)` que puntúa alternativas técnicas.\n\n"
        "Cada opción: `{'name': str, 'scores': dict}`.\n"
        "Los scores son de 1-5 en dimensiones: `scalability`, `cost`, `complexity`, "
        "`time_to_market`, `reliability`.\n\n"
        "Los pesos del negocio: `scalability=0.3, cost=0.2, complexity=0.15, "
        "time_to_market=0.25, reliability=0.1`.\n\n"
        "Calcula `weighted_score = sum(score * weight)` para cada opción (2 dec).\n\n"
        "Imprime cada opción con sus scores y weighted_score, ordenadas de mayor a menor:\n"
        "`N. <name>  weighted=X.XX`\n"
        "`   scalability=N  cost=N  complexity=N  ttm=N  reliability=N`\n\n"
        "Al final: `Recommendation: <nombre de la opción ganadora>`"
    ),
    hint          = "WEIGHTS = {'scalability':0.3,'cost':0.2,'complexity':0.15,'time_to_market':0.25,'reliability':0.1}",
    initial_code  = (
        "def evaluate_tradeoffs(options):\n"
        "    pass\n\n"
        "WEIGHTS = {\n"
        "    'scalability': 0.3, 'cost': 0.2, 'complexity': 0.15,\n"
        "    'time_to_market': 0.25, 'reliability': 0.1,\n"
        "}\n\n"
        "options = [\n"
        "    {'name': 'Microservices', 'scores': {'scalability':5,'cost':2,'complexity':2,'time_to_market':2,'reliability':4}},\n"
        "    {'name': 'Monolith',      'scores': {'scalability':2,'cost':5,'complexity':5,'time_to_market':5,'reliability':3}},\n"
        "    {'name': 'Modular Mono',  'scores': {'scalability':3,'cost':4,'complexity':4,'time_to_market':4,'reliability':4}},\n"
        "]\n"
        "evaluate_tradeoffs(options)\n"
    ),
    expected_output = (
        "1. Modular Mono  weighted=3.65\n"
        "   scalability=3  cost=4  complexity=4  ttm=4  reliability=4\n"
        "2. Monolith  weighted=3.55\n"
        "   scalability=2  cost=5  complexity=5  ttm=5  reliability=3\n"
        "3. Microservices  weighted=3.00\n"
        "   scalability=5  cost=2  complexity=2  ttm=2  reliability=4\n"
        "Recommendation: Modular Mono"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L26 — Observability Coverage Checker
# ─────────────────────────────────────────────────────────────────────────────
L26 = dict(
    **_BASE,
    level_order   = 26,
    title         = "Observability Coverage Checker",
    difficulty    = "medium",
    description   = (
        "Implementa `observability_check(services)` que evalúa la cobertura de observabilidad "
        "de cada servicio en los tres pilares: logs, metrics, traces.\n\n"
        "Cada servicio: `{'name': str, 'has_logs': bool, 'has_metrics': bool, "
        "'has_traces': bool, 'alert_count': int}`.\n\n"
        "Score de observabilidad = (pillars_covered / 3 * 100) como entero.\n\n"
        "Imprime por servicio:\n"
        "`<name>: logs=[Y|N]  metrics=[Y|N]  traces=[Y|N]  alerts=N  score=N%  [FULL|PARTIAL|BLIND]`\n\n"
        "FULL si score=100, BLIND si score=0, PARTIAL en otro caso.\n\n"
        "Al final:\n"
        "`Coverage: X% avg  |  Full: N  Partial: N  Blind: N`\n"
        "(avg = promedio de scores, entero)"
    ),
    hint          = "Cuenta cuántos de los 3 booleans son True para el score.",
    initial_code  = (
        "def observability_check(services):\n"
        "    pass\n\n"
        "services = [\n"
        "    {'name': 'payment-api',  'has_logs': True,  'has_metrics': True,  'has_traces': True,  'alert_count': 12},\n"
        "    {'name': 'user-service', 'has_logs': True,  'has_metrics': True,  'has_traces': False, 'alert_count': 5},\n"
        "    {'name': 'legacy-crm',   'has_logs': True,  'has_metrics': False, 'has_traces': False, 'alert_count': 0},\n"
        "    {'name': 'batch-jobs',   'has_logs': False, 'has_metrics': False, 'has_traces': False, 'alert_count': 0},\n"
        "]\n"
        "observability_check(services)\n"
    ),
    expected_output = (
        "payment-api:  logs=Y  metrics=Y  traces=Y  alerts=12  score=100%  FULL\n"
        "user-service: logs=Y  metrics=Y  traces=N  alerts=5   score=66%   PARTIAL\n"
        "legacy-crm:   logs=Y  metrics=N  traces=N  alerts=0   score=33%   PARTIAL\n"
        "batch-jobs:   logs=N  metrics=N  traces=N  alerts=0   score=0%    BLIND\n"
        "Coverage: 50% avg  |  Full: 1  Partial: 2  Blind: 1"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L27 — Release Risk Scorer
# ─────────────────────────────────────────────────────────────────────────────
L27 = dict(
    **_BASE,
    level_order   = 27,
    title         = "Release Risk Scorer",
    difficulty    = "hard",
    description   = (
        "Antes de aprobar un release, el TPM evalúa el riesgo. "
        "Implementa `release_risk_score(release)` que computa un score compuesto.\n\n"
        "release: `{'name': str, 'changes': int, 'test_coverage_pct': float, "
        "'open_bugs': int, 'last_incident_days': int, 'has_rollback_plan': bool}`.\n\n"
        "Factores de riesgo (cada uno suma puntos al score, mayor = más riesgo):\n"
        "- changes > 50: +30; changes > 20: +15; else +0\n"
        "- test_coverage_pct < 60: +25; < 80: +10; else +0\n"
        "- open_bugs > 5: +20; > 0: +10; else +0\n"
        "- last_incident_days < 3: +20; < 7: +10; else +0\n"
        "- has_rollback_plan=False: +15\n\n"
        "Score total máximo = 110. Clasifica:\n"
        "- score <= 20 → LOW RISK → GO\n"
        "- score <= 50 → MEDIUM RISK → GO WITH CAUTION\n"
        "- score > 50  → HIGH RISK → NO-GO\n\n"
        "Imprime cada factor contribuyente, el score total y la decisión."
    ),
    hint          = "Evalúa cada factor independientemente con if/elif. Acumula los puntos.",
    initial_code  = (
        "def release_risk_score(release):\n"
        "    pass\n\n"
        "release = {\n"
        "    'name':               'v2.4.0',\n"
        "    'changes':            67,\n"
        "    'test_coverage_pct':  74.5,\n"
        "    'open_bugs':          3,\n"
        "    'last_incident_days': 2,\n"
        "    'has_rollback_plan':  True,\n"
        "}\n"
        "release_risk_score(release)\n"
    ),
    expected_output = (
        "Release Risk: v2.4.0\n"
        "  changes=67          → +30 pts (high change volume)\n"
        "  coverage=74.5%      → +10 pts (coverage below 80%)\n"
        "  open_bugs=3         → +10 pts (open bugs present)\n"
        "  last_incident=2d    → +20 pts (recent incident)\n"
        "  rollback_plan=True  → +0 pts\n"
        "Total score: 70  →  HIGH RISK — NO-GO"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L28 — API Contract Validator
# ─────────────────────────────────────────────────────────────────────────────
L28 = dict(
    **_BASE,
    level_order   = 28,
    title         = "API Contract Validator",
    difficulty    = "hard",
    description   = (
        "Un TPM técnico detecta breaking changes antes de que lleguen a producción. "
        "Implementa `validate_api_contract(v1, v2)` que compara dos versiones de un contrato API.\n\n"
        "Cada versión: `{'endpoints': list[dict]}`.\n"
        "Cada endpoint: `{'method': str, 'path': str, 'required_params': list[str], "
        "'response_fields': list[str]}`.\n\n"
        "Un endpoint se identifica por `method + path`.\n\n"
        "Detecta:\n"
        "- **BREAKING**: endpoint removido, required_param agregado, response_field removido\n"
        "- **SAFE**: endpoint agregado, required_param removido, response_field agregado\n\n"
        "Imprime por cambio:\n"
        "`[BREAKING|SAFE] <método>: <descripción>`\n\n"
        "Al final: `Breaking changes: N  |  Safe changes: N`\n"
        "`Verdict: [COMPATIBLE|BREAKING CHANGE]`"
    ),
    hint          = "Usa dicts keyed por 'METHOD PATH' para comparar versiones. Itera sobre todas las claves.",
    initial_code  = (
        "def validate_api_contract(v1, v2):\n"
        "    pass\n\n"
        "v1 = {'endpoints': [\n"
        "    {'method': 'GET',  'path': '/users',    'required_params': ['page'],         'response_fields': ['id','name','email']},\n"
        "    {'method': 'POST', 'path': '/users',    'required_params': ['name','email'], 'response_fields': ['id','created_at']},\n"
        "    {'method': 'GET',  'path': '/reports',  'required_params': [],               'response_fields': ['data','total']},\n"
        "]}\n"
        "v2 = {'endpoints': [\n"
        "    {'method': 'GET',  'path': '/users',    'required_params': ['page','limit'], 'response_fields': ['id','name','email','role']},\n"
        "    {'method': 'POST', 'path': '/users',    'required_params': ['name','email'], 'response_fields': ['id','created_at']},\n"
        "    {'method': 'GET',  'path': '/analytics','required_params': [],               'response_fields': ['views','sessions']},\n"
        "]}\n"
        "validate_api_contract(v1, v2)\n"
    ),
    expected_output = (
        "[BREAKING] GET /users: required param added — limit\n"
        "[SAFE]     GET /users: response field added — role\n"
        "[BREAKING] GET /reports: endpoint removed\n"
        "[SAFE]     GET /analytics: endpoint added\n"
        "Breaking changes: 2  |  Safe changes: 2\n"
        "Verdict: BREAKING CHANGE"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L29 — Infrastructure Cost Estimator
# ─────────────────────────────────────────────────────────────────────────────
L29 = dict(
    **_BASE,
    level_order   = 29,
    title         = "Infrastructure Cost Estimator",
    difficulty    = "medium",
    description   = (
        "Un TPM necesita estimar costos de infraestructura para propuestas de arquitectura. "
        "Implementa `infra_cost_estimate(components, months)` que calcula el costo total.\n\n"
        "Cada componente: `{'name': str, 'type': str, 'units': int, 'cost_per_unit_month': float}`.\n\n"
        "Para cada componente:\n"
        "`monthly_cost = units * cost_per_unit_month`\n"
        "`total_cost   = monthly_cost * months`\n\n"
        "Imprime por componente:\n"
        "`  <name> (<type>): $X.XX/mo × N = $X.XX`\n\n"
        "Agrupa por type con subtotales:\n"
        "`<TYPE>:`\n"
        "Luego los componentes de ese tipo.\n"
        "`  Subtotal: $X.XX`\n\n"
        "Al final:\n"
        "`Monthly total: $X.XX  |  Project total (N mo): $X.XX`"
    ),
    hint          = "Agrupa los componentes por type antes de iterar. Puedes usar un dict de listas.",
    initial_code  = (
        "def infra_cost_estimate(components, months):\n"
        "    pass\n\n"
        "components = [\n"
        "    {'name': 'App servers',  'type': 'Compute', 'units': 4,  'cost_per_unit_month': 150.0},\n"
        "    {'name': 'Worker nodes', 'type': 'Compute', 'units': 2,  'cost_per_unit_month': 120.0},\n"
        "    {'name': 'Primary DB',   'type': 'Database','units': 1,  'cost_per_unit_month': 480.0},\n"
        "    {'name': 'Read replica', 'type': 'Database','units': 2,  'cost_per_unit_month': 240.0},\n"
        "    {'name': 'CDN',          'type': 'Network', 'units': 1,  'cost_per_unit_month': 80.0},\n"
        "]\n"
        "infra_cost_estimate(components, months=6)\n"
    ),
    expected_output = (
        "Compute:\n"
        "  App servers (Compute): $600.00/mo × 6 = $3600.00\n"
        "  Worker nodes (Compute): $240.00/mo × 6 = $1440.00\n"
        "  Subtotal: $5040.00\n"
        "Database:\n"
        "  Primary DB (Database): $480.00/mo × 6 = $2880.00\n"
        "  Read replica (Database): $480.00/mo × 6 = $2880.00\n"
        "  Subtotal: $5760.00\n"
        "Network:\n"
        "  CDN (Network): $80.00/mo × 6 = $480.00\n"
        "  Subtotal: $480.00\n"
        "Monthly total: $1880.00  |  Project total (6 mo): $11280.00"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L30 — BOSS: System Reliability Scorecard
# ─────────────────────────────────────────────────────────────────────────────
L30 = dict(
    **_BASE_BOSS,
    level_order   = 30,
    title         = "CONTRATO-TPM-30: System Reliability Scorecard",
    difficulty    = "legendary",
    is_phase_boss = True,
    is_project    = True,
    description   = (
        "Evaluación de credibilidad técnica completa. Implementa `ReliabilityScorecard` "
        "que consolida métricas técnicas en un reporte ejecutivo.\n\n"
        "Métodos:\n"
        "- `add_service(name, uptime_pct, p95_ms, deploy_freq_per_week, error_rate_pct)`\n"
        "- `generate_scorecard()` — imprime el reporte completo\n\n"
        "Para cada servicio calcula un score (0-100):\n"
        "- Uptime: >= 99.9% → 25pts, >= 99.5% → 15pts, else 0\n"
        "- P95: <= 200ms → 25pts, <= 500ms → 15pts, else 0\n"
        "- Deploy freq: >= 5/week → 25pts, >= 1/week → 15pts, else 0\n"
        "- Error rate: <= 0.1% → 25pts, <= 1% → 15pts, else 0\n\n"
        "Grade: 90-100=A, 75-89=B, 60-74=C, <60=D\n\n"
        "El scorecard imprime cada servicio con sus 4 factores, score y grade.\n"
        "Al final: promedio del sistema, grade global y recomendación "
        "(SCALE CONFIDENTLY / PROCEED WITH CAUTION / NEEDS IMMEDIATE ATTENTION)."
    ),
    hint          = "Acumula los 4 factores de puntos. Grade global = mismo criterio sobre el promedio.",
    initial_code  = (
        "class ReliabilityScorecard:\n"
        "    def __init__(self):\n"
        "        self.services = []\n\n"
        "    def add_service(self, name, uptime_pct, p95_ms, deploy_freq_per_week, error_rate_pct):\n"
        "        pass\n\n"
        "    def generate_scorecard(self):\n"
        "        pass\n\n\n"
        "sc = ReliabilityScorecard()\n"
        "sc.add_service('API Gateway',    uptime_pct=99.95, p95_ms=180,  deploy_freq_per_week=8,  error_rate_pct=0.05)\n"
        "sc.add_service('Auth Service',   uptime_pct=99.7,  p95_ms=420,  deploy_freq_per_week=2,  error_rate_pct=0.8)\n"
        "sc.add_service('Legacy Reports', uptime_pct=98.5,  p95_ms=1200, deploy_freq_per_week=0.5,error_rate_pct=2.5)\n"
        "sc.generate_scorecard()\n"
    ),
    expected_output = (
        "=== SYSTEM RELIABILITY SCORECARD ===\n"
        "\n"
        "API Gateway:\n"
        "  uptime=99.95%   → 25pts\n"
        "  p95=180ms       → 25pts\n"
        "  deploys=8/week  → 25pts\n"
        "  errors=0.05%    → 25pts\n"
        "  Score: 100/100  Grade: A\n"
        "\n"
        "Auth Service:\n"
        "  uptime=99.7%    → 15pts\n"
        "  p95=420ms       → 15pts\n"
        "  deploys=2/week  → 15pts\n"
        "  errors=0.8%     → 15pts\n"
        "  Score: 60/100  Grade: C\n"
        "\n"
        "Legacy Reports:\n"
        "  uptime=98.5%    → 0pts\n"
        "  p95=1200ms      → 0pts\n"
        "  deploys=0.5/week  → 0pts\n"
        "  errors=2.5%     → 0pts\n"
        "  Score: 0/100  Grade: D\n"
        "\n"
        "System Average: 53/100  Grade: D\n"
        "Recommendation: NEEDS IMMEDIATE ATTENTION"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
BLOQUE2 = [L16, L17, L18, L19, L20, L21, L22, L23, L24, L25, L26, L27, L28, L29, L30]
