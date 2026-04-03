"""
_tpm_b5.py — TPM Mastery · BLOQUE 5 (L61–L75)
===============================================
Fase: ejecucion_entrega
Niveles: 61 a 75 (15 desafíos Python)
Boss: L75 — Execution Dashboard
"""
from __future__ import annotations

_BASE = dict(
    codex_id="tpm_mastery", sector_id=21, challenge_type="python",
    phase="ejecucion_entrega", is_free=False, strict_match=False,
    is_phase_boss=False, is_project=False,
)
_BASE_BOSS = {k: v for k, v in _BASE.items() if k not in ("is_phase_boss", "is_project")}

L61 = dict(
    **_BASE, level_order=61, title="Velocity Tracker", difficulty="easy",
    description=(
        "Implementa `velocity_tracker(sprints)` que analiza la velocidad del equipo.\n\n"
        "Cada sprint: `{'number': int, 'committed': int, 'completed': int}`.\n\n"
        "Para cada sprint calcula `pct = completed/committed*100` (int).\n"
        "Label: pct==100 → PERFECT, pct>=90 → ON TARGET, pct<90 → BELOW TARGET.\n\n"
        "Imprime: `Sprint N: committed=X  completed=X  (X%)  [LABEL]`\n\n"
        "Al final:\n"
        "`Avg velocity: X pts  Trend: [IMPROVING|DECLINING|STABLE]`\n\n"
        "Trend: compara completed del último sprint vs el primero."
    ),
    hint="avg = round(sum(completed)/len, 1). Trend: last > first → IMPROVING.",
    initial_code=(
        "def velocity_tracker(sprints):\n"
        "    pass\n\n"
        "velocity_tracker([\n"
        "    {'number': 1, 'committed': 40, 'completed': 32},\n"
        "    {'number': 2, 'committed': 40, 'completed': 38},\n"
        "    {'number': 3, 'committed': 45, 'completed': 45},\n"
        "    {'number': 4, 'committed': 50, 'completed': 44},\n"
        "])\n"
    ),
    expected_output=(
        "Sprint 1: committed=40  completed=32  (80%)  [BELOW TARGET]\n"
        "Sprint 2: committed=40  completed=38  (95%)  [ON TARGET]\n"
        "Sprint 3: committed=45  completed=45  (100%)  [PERFECT]\n"
        "Sprint 4: committed=50  completed=44  (88%)  [BELOW TARGET]\n"
        "Avg velocity: 39.8 pts  Trend: IMPROVING"
    ),
)

L62 = dict(
    **_BASE, level_order=62, title="Burndown Calculator", difficulty="medium",
    description=(
        "Implementa `burndown_report(total_points, sprint_days, daily_completions)` "
        "que calcula el burndown del sprint.\n\n"
        "Ideal = total/sprint_days puntos por día (burn lineal).\n"
        "Para cada día: `ideal_remaining = total - ideal*day` y "
        "`actual_remaining = total - sum(completions[:day])`.\n\n"
        "Imprime por día:\n"
        "`Day N:  ideal=X  actual=X  [AHEAD|ON TRACK|BEHIND]`\n\n"
        "AHEAD si actual < ideal, BEHIND si actual > ideal, ON TRACK si igual.\n\n"
        "Al final: `Final: COMPLETED — 0 pts remaining` o "
        "`Final: X pts remaining`."
    ),
    hint="ideal_remaining = total - (ideal_per_day * day). actual_remaining acumulativo.",
    initial_code=(
        "def burndown_report(total_points, sprint_days, daily_completions):\n"
        "    pass\n\n"
        "burndown_report(\n"
        "    total_points=80, sprint_days=10,\n"
        "    daily_completions=[9, 8, 7, 10, 8, 6, 9, 7, 8, 8]\n"
        ")\n"
    ),
    expected_output=(
        "Day 1:  ideal=72  actual=71  AHEAD\n"
        "Day 2:  ideal=64  actual=63  AHEAD\n"
        "Day 3:  ideal=56  actual=56  ON TRACK\n"
        "Day 4:  ideal=48  actual=46  AHEAD\n"
        "Day 5:  ideal=40  actual=38  AHEAD\n"
        "Day 6:  ideal=32  actual=32  ON TRACK\n"
        "Day 7:  ideal=24  actual=23  AHEAD\n"
        "Day 8:  ideal=16  actual=16  ON TRACK\n"
        "Day 9:  ideal=8   actual=8   ON TRACK\n"
        "Day 10: ideal=0   actual=0   ON TRACK\n"
        "Final: COMPLETED — 0 pts remaining"
    ),
)

L63 = dict(
    **_BASE, level_order=63, title="Earned Value Manager", difficulty="hard",
    description=(
        "EVM (Earned Value Management) es el estándar de medición de proyectos. "
        "Implementa `evm_report(project)` con los campos: "
        "`name`, `total_budget`, `planned_value`, `earned_value`, `actual_cost`.\n\n"
        "Calcula:\n"
        "- CPI = EV/AC (round 2 dec)\n"
        "- SPI = EV/PV (round 2 dec)\n"
        "- CV  = EV - AC\n"
        "- SV  = EV - PV\n"
        "- EAC = int(total_budget * AC / EV) (Estimate at Completion)\n\n"
        "Labels: CPI<1 → OVER BUDGET; SPI<1 → BEHIND SCHEDULE; ambos >=1 → ON TRACK.\n\n"
        "Formato exacto según expected_output."
    ),
    hint="EAC = total_budget / CPI = total_budget * AC / EV. Usa int() para truncar.",
    initial_code=(
        "def evm_report(project):\n"
        "    pass\n\n"
        "evm_report({\n"
        "    'name': 'Platform Migration',\n"
        "    'total_budget': 500000,\n"
        "    'planned_value': 200000,\n"
        "    'earned_value':  180000,\n"
        "    'actual_cost':   210000,\n"
        "})\n"
    ),
    expected_output=(
        "EVM Report: Platform Migration\n"
        "────────────────────────────────\n"
        "PV  (Planned Value):  $200,000\n"
        "EV  (Earned Value):   $180,000\n"
        "AC  (Actual Cost):    $210,000\n"
        "────────────────────────────────\n"
        "CPI (Cost Perf):      0.86  [OVER BUDGET]\n"
        "SPI (Schedule Perf):  0.90  [BEHIND SCHEDULE]\n"
        "CV  (Cost Variance):  $-30,000\n"
        "SV  (Schedule Var):   $-20,000\n"
        "EAC (Est at Completion): $583,333\n"
        "────────────────────────────────\n"
        "Status: AT RISK — both cost and schedule negative"
    ),
)

L64 = dict(
    **_BASE, level_order=64, title="Schedule Compression Planner", difficulty="hard",
    description=(
        "Implementa `schedule_compression(tasks, current_weeks, target_weeks)` "
        "que calcula el plan de compresión más económico.\n\n"
        "Cada tarea: `{'name': str, 'max_crash_weeks': int, 'cost_per_week': int}`.\n\n"
        "Ordena por cost_per_week ascendente. Greedy: aplica el crash más barato primero, "
        "hasta la semana máxima disponible, hasta alcanzar el target.\n\n"
        "Imprime el header, cada acción con costo acumulado, "
        "y el resultado final con costo total."
    ),
    hint="Acumula semanas_saved y cost mientras iteras. Cada tarea puede usar 1..max_crash_weeks semanas.",
    initial_code=(
        "def schedule_compression(tasks, current_weeks, target_weeks):\n"
        "    pass\n\n"
        "tasks = [\n"
        "    {'name': 'Backend',  'max_crash_weeks': 2, 'cost_per_week': 7500},\n"
        "    {'name': 'Frontend', 'max_crash_weeks': 1, 'cost_per_week': 8000},\n"
        "    {'name': 'Testing',  'max_crash_weeks': 1, 'cost_per_week': 5000},\n"
        "]\n"
        "schedule_compression(tasks, current_weeks=14, target_weeks=11)\n"
    ),
    expected_output=(
        "Schedule Compression Plan\n"
        "Current: 14wk  Target: 11wk  Reduction needed: 3 weeks\n"
        "\n"
        "Compression actions:\n"
        "  Crash Testing  : -1wk  $5,000/wk  cumulative: 1wk saved  $5,000\n"
        "  Crash Backend  : -1wk  $7,500/wk  cumulative: 2wk saved  $12,500\n"
        "  Crash Backend  : -1wk  $7,500/wk  cumulative: 3wk saved  $20,000\n"
        "\n"
        "Result: 11 weeks achievable\n"
        "Total crash cost: $20,000"
    ),
)

L65 = dict(
    **_BASE, level_order=65, title="Release Gate Checker", difficulty="medium",
    description=(
        "Implementa `release_gate_check(version, gates)` que evalúa si un release puede pasar.\n\n"
        "Cada gate: `{'name': str, 'status': str, 'required': bool}`.\n\n"
        "Imprime:\n"
        "`Release Gate Check: <version>`\n"
        "`  [PASS|FAIL] <name>  (<required|optional>)[ ← BLOCKING]`\n\n"
        "Marca con `← BLOCKING` los gates que son required y tienen status='fail'.\n\n"
        "Al final:\n"
        "`GO/NO-GO: [GO|NO-GO]`\n"
        "`Blocking gates: <lista>` (solo si NO-GO)"
    ),
    hint="NO-GO si algún required gate tiene status='fail'.",
    initial_code=(
        "def release_gate_check(version, gates):\n"
        "    pass\n\n"
        "release_gate_check('v2.5.0', [\n"
        "    {'name': 'Unit tests',    'status': 'pass', 'required': True},\n"
        "    {'name': 'Integration',   'status': 'pass', 'required': True},\n"
        "    {'name': 'Performance',   'status': 'fail', 'required': True},\n"
        "    {'name': 'Security scan', 'status': 'pass', 'required': True},\n"
        "    {'name': 'Docs updated',  'status': 'fail', 'required': False},\n"
        "])\n"
    ),
    expected_output=(
        "Release Gate Check: v2.5.0\n"
        "  [PASS] Unit tests    (required)\n"
        "  [PASS] Integration   (required)\n"
        "  [FAIL] Performance   (required) ← BLOCKING\n"
        "  [PASS] Security scan (required)\n"
        "  [FAIL] Docs updated  (optional)\n"
        "GO/NO-GO: NO-GO\n"
        "Blocking gates: Performance"
    ),
)

L66 = dict(
    **_BASE, level_order=66, title="Story Point Distribution", difficulty="easy",
    description=(
        "Implementa `point_distribution(stories)` que analiza la distribución de tamaños.\n\n"
        "Cada story: `{'id': str, 'points': int}`.\n\n"
        "Buckets:\n"
        "- XS: 1-2 pts\n"
        "- S:  3-4 pts\n"
        "- M:  5-7 pts\n"
        "- L:  8-12 pts\n"
        "- XL: 13+ pts\n\n"
        "Imprime por bucket:\n"
        "`<bucket padded 10>: N stories  N pts  (X%)`\n\n"
        "% = pts del bucket / total pts * 100 (1 dec).\n\n"
        "Al final: `Complexity risk: [HIGH|MEDIUM|LOW]`\n"
        "HIGH si XL% >= 40%, MEDIUM si >= 20%, LOW si < 20%."
    ),
    hint="Itera stories y clasifica por puntos. Acumula por bucket.",
    initial_code=(
        "def point_distribution(stories):\n"
        "    pass\n\n"
        "stories = [\n"
        "    {'id': 'US-01', 'points': 1},  {'id': 'US-02', 'points': 3},\n"
        "    {'id': 'US-03', 'points': 5},  {'id': 'US-04', 'points': 8},\n"
        "    {'id': 'US-05', 'points': 13}, {'id': 'US-06', 'points': 5},\n"
        "    {'id': 'US-07', 'points': 3},  {'id': 'US-08', 'points': 8},\n"
        "    {'id': 'US-09', 'points': 1},  {'id': 'US-10', 'points': 21},\n"
        "]\n"
        "point_distribution(stories)\n"
    ),
    expected_output=(
        "XS (1-2 pts):   2 stories   2 pts  (2.9%)\n"
        "S  (3-4 pts):   2 stories   6 pts  (8.8%)\n"
        "M  (5-7 pts):   2 stories  10 pts  (14.7%)\n"
        "L  (8-12 pts):  2 stories  16 pts  (23.5%)\n"
        "XL (13+ pts):   2 stories  34 pts  (50.0%)\n"
        "Complexity risk: HIGH (50.0% of points in XL stories)"
    ),
)

L67 = dict(
    **_BASE, level_order=67, title="Sprint Retrospective Analyzer", difficulty="medium",
    description=(
        "Implementa `retro_summary(retro)` que genera el acta de retrospectiva.\n\n"
        "retro: `{'went_well': list[str], 'improve': list[str], "
        "'action_items': list[dict]}`.\n\n"
        "action_item: `{'action': str, 'owner': str, 'sprint': str}`.\n\n"
        "Formato:\n"
        "```\n"
        "Sprint Retrospective Summary\n"
        "──────────────────────────────\n"
        "WENT WELL (N items):\n"
        "  + <item>\n"
        "IMPROVE (N items):\n"
        "  △ <item>\n"
        "ACTION ITEMS:\n"
        "  [ ] <action>  — Owner: <owner>  Sprint: <sprint>\n"
        "──────────────────────────────\n"
        "Signal: N wins / N improvements / N actions\n"
        "```"
    ),
    hint="Itera cada lista con su prefijo. Línea vacía entre secciones.",
    initial_code=(
        "def retro_summary(retro):\n"
        "    pass\n\n"
        "retro_summary({\n"
        "    'went_well': ['Auth shipped on time', 'Team collaboration improved'],\n"
        "    'improve':   ['Too many interruptions', 'Story estimates off'],\n"
        "    'action_items': [\n"
        "        {'action': 'Block 2h focus time daily',       'owner': 'Team', 'sprint': 'next'},\n"
        "        {'action': 'Re-estimate story sizes together', 'owner': 'Ana',  'sprint': 'next'},\n"
        "    ],\n"
        "})\n"
    ),
    expected_output=(
        "Sprint Retrospective Summary\n"
        "──────────────────────────────\n"
        "WENT WELL (2 items):\n"
        "  + Auth shipped on time\n"
        "  + Team collaboration improved\n"
        "IMPROVE (2 items):\n"
        "  △ Too many interruptions\n"
        "  △ Story estimates off\n"
        "ACTION ITEMS:\n"
        "  [ ] Block 2h focus time daily  — Owner: Team  Sprint: next\n"
        "  [ ] Re-estimate story sizes together  — Owner: Ana  Sprint: next\n"
        "──────────────────────────────\n"
        "Signal: 2 wins / 2 improvements / 2 actions"
    ),
)

L68 = dict(
    **_BASE, level_order=68, title="Priority Dependency Queue", difficulty="hard",
    description=(
        "Implementa `priority_dep_queue(tasks)` que ordena tareas respetando dependencias "
        "y usando prioridad (menor número = mayor prioridad) como criterio de desempate.\n\n"
        "Cada tarea: `{'id': str, 'name': str, 'deps': list[str], 'priority': int}`.\n\n"
        "Usa Kahn's algorithm. Cuando múltiples tareas tienen in-degree=0, "
        "selecciona la de menor número de prioridad.\n\n"
        "Imprime:\n"
        "`Dependency Queue (priority-sorted):`\n"
        "`N. <id>: <name padded 18> (p=N, deps: <deps|none>)`"
    ),
    hint="Usa una lista ordenada por priority en lugar de una simple queue.",
    initial_code=(
        "def priority_dep_queue(tasks):\n"
        "    pass\n\n"
        "tasks = [\n"
        "    {'id': 'T1', 'name': 'infra-setup',   'deps': [],           'priority': 1},\n"
        "    {'id': 'T2', 'name': 'auth-service',  'deps': ['T1'],       'priority': 1},\n"
        "    {'id': 'T3', 'name': 'user-api',      'deps': ['T1'],       'priority': 2},\n"
        "    {'id': 'T4', 'name': 'payment-api',   'deps': ['T2','T3'],  'priority': 1},\n"
        "    {'id': 'T5', 'name': 'frontend',      'deps': ['T3'],       'priority': 2},\n"
        "    {'id': 'T6', 'name': 'e2e-tests',     'deps': ['T4','T5'],  'priority': 1},\n"
        "]\n"
        "priority_dep_queue(tasks)\n"
    ),
    expected_output=(
        "Dependency Queue (priority-sorted):\n"
        "1. T1: infra-setup          (p=1, deps: none)\n"
        "2. T2: auth-service         (p=1, deps: T1)\n"
        "3. T3: user-api             (p=2, deps: T1)\n"
        "4. T4: payment-api          (p=1, deps: T2, T3)\n"
        "5. T5: frontend             (p=2, deps: T3)\n"
        "6. T6: e2e-tests            (p=1, deps: T4, T5)"
    ),
)

L69 = dict(
    **_BASE, level_order=69, title="Test Coverage Gate", difficulty="medium",
    description=(
        "Implementa `coverage_gate(modules)` que verifica umbrales de cobertura.\n\n"
        "Cada módulo: `{'name': str, 'coverage': float, 'threshold': float}`.\n\n"
        "Imprime por módulo:\n"
        "`  <name padded 12>: X%  threshold=X%  [PASS|FAIL]`\n\n"
        "Al final:\n"
        "`Passed: N/M  Overall: X%`\n"
        "`Gate: [PASS|FAIL] — <mensaje>`\n\n"
        "Overall = promedio de coverages (1 dec).\n"
        "Gate PASS si todos pasan. Si falla: `Gate: FAIL — N modules below threshold`."
    ),
    hint="Promedio de coverage, no de resultados PASS/FAIL.",
    initial_code=(
        "def coverage_gate(modules):\n"
        "    pass\n\n"
        "coverage_gate([\n"
        "    {'name': 'auth',     'coverage': 92.0, 'threshold': 80.0},\n"
        "    {'name': 'payments', 'coverage': 71.5, 'threshold': 80.0},\n"
        "    {'name': 'users',    'coverage': 85.0, 'threshold': 80.0},\n"
        "    {'name': 'reports',  'coverage': 45.0, 'threshold': 60.0},\n"
        "])\n"
    ),
    expected_output=(
        "  auth:     92.0%  threshold=80.0%  [PASS]\n"
        "  payments: 71.5%  threshold=80.0%  [FAIL]\n"
        "  users:    85.0%  threshold=80.0%  [PASS]\n"
        "  reports:  45.0%  threshold=60.0%  [FAIL]\n"
        "Passed: 2/4  Overall: 73.4%\n"
        "Gate: FAIL — 2 modules below threshold"
    ),
)

L70 = dict(
    **_BASE, level_order=70, title="Feature Flag Manager", difficulty="medium",
    description=(
        "Implementa `flag_status(flags)` que reporta el estado de los feature flags.\n\n"
        "Cada flag: `{'name': str, 'enabled': bool, 'rollout_pct': int, 'segments': list[str]}`.\n\n"
        "Imprime por flag:\n"
        "`  <name padded 14> [ON|OFF]  rollout=X%   segments: <s1, s2|none>`\n\n"
        "Al final:\n"
        "`Active: N/M  |  Full rollout: N  |  Partial: N  |  Disabled: N`\n\n"
        "Full rollout = enabled y rollout_pct==100.\n"
        "Partial = enabled y rollout_pct < 100.\n"
        "Disabled = not enabled."
    ),
    hint="segments: ', '.join(segments) si hay, 'none' si lista vacía.",
    initial_code=(
        "def flag_status(flags):\n"
        "    pass\n\n"
        "flag_status([\n"
        "    {'name': 'new-checkout', 'enabled': True,  'rollout_pct': 25,  'segments': ['premium']},\n"
        "    {'name': 'ai-suggest',   'enabled': True,  'rollout_pct': 10,  'segments': ['all']},\n"
        "    {'name': 'dark-mode',    'enabled': False, 'rollout_pct': 0,   'segments': []},\n"
        "    {'name': 'bulk-export',  'enabled': True,  'rollout_pct': 100, 'segments': ['all']},\n"
        "])\n"
    ),
    expected_output=(
        "  new-checkout   [ON]   rollout=25%   segments: premium\n"
        "  ai-suggest     [ON]   rollout=10%   segments: all\n"
        "  dark-mode      [OFF]  rollout=0%    segments: none\n"
        "  bulk-export    [ON]   rollout=100%  segments: all\n"
        "Active: 3/4  |  Full rollout: 1  |  Partial: 2  |  Disabled: 1"
    ),
)

L71 = dict(
    **_BASE, level_order=71, title="Rollout Plan Builder", difficulty="hard",
    description=(
        "Implementa `rollout_plan(feature, stages)` que construye el plan de despliegue gradual.\n\n"
        "Cada stage: `{'name': str, 'users_pct': int, 'duration_days': int, 'success_metric': str}`.\n\n"
        "Imprime:\n"
        "`Rollout Plan: <feature>`\n"
        "Por stage (con numeración):\n"
        "`Stage N: <name padded 20> <users_pct>% of users  <duration_days> days  → <success_metric>`\n\n"
        "Al final:\n"
        "`Total duration: N days`\n"
        "`Rollback triggers: Any stage failure halts rollout`"
    ),
    hint="Acumula total_duration sumando duration_days de todos los stages.",
    initial_code=(
        "def rollout_plan(feature, stages):\n"
        "    pass\n\n"
        "rollout_plan('AI Recommendations', [\n"
        "    {'name': 'Internal alpha',  'users_pct': 5,   'duration_days': 7,  'success_metric': 'No critical bugs'},\n"
        "    {'name': 'Beta users',      'users_pct': 20,  'duration_days': 14, 'success_metric': 'Error rate < 1%'},\n"
        "    {'name': 'General rollout', 'users_pct': 100, 'duration_days': 7,  'success_metric': 'All metrics green'},\n"
        "])\n"
    ),
    expected_output=(
        "Rollout Plan: AI Recommendations\n"
        "Stage 1: Internal alpha         5% of users  7 days  → No critical bugs\n"
        "Stage 2: Beta users             20% of users  14 days  → Error rate < 1%\n"
        "Stage 3: General rollout        100% of users  7 days  → All metrics green\n"
        "Total duration: 28 days\n"
        "Rollback triggers: Any stage failure halts rollout"
    ),
)

L72 = dict(
    **_BASE, level_order=72, title="Post-Release Monitor", difficulty="medium",
    description=(
        "Implementa `post_release_monitor(version, metrics)` que detecta anomalías "
        "después de un release.\n\n"
        "Cada métrica: `{'name': str, 'baseline': float, 'current': float, "
        "'threshold': float|None, 'higher_is_better': bool}`.\n\n"
        "delta_pct = (current - baseline) / baseline * 100 (1 dec).\n\n"
        "Estado:\n"
        "- Si threshold y higher_is_better=False y current > threshold → BREACH\n"
        "- Si higher_is_better=False y delta_pct > 20 → ELEVATED\n"
        "- Si higher_is_better=True  y delta_pct < -20 → DEGRADED\n"
        "- Sino → OK\n\n"
        "Imprime: `  <name padded 14>: baseline=X  current=X  delta=X%  [STATE]`\n\n"
        "Al final: `Alerts: N anomalies detected` o `Alerts: none`"
    ),
    hint="Evalúa BREACH primero, luego ELEVATED/DEGRADED, luego OK.",
    initial_code=(
        "def post_release_monitor(version, metrics):\n"
        "    print(f'Post-Release: {version}')\n"
        "    pass\n\n"
        "post_release_monitor('v2.5.0', [\n"
        "    {'name': 'error_rate',   'baseline': 0.5,  'current': 0.8,  'threshold': 1.0,  'higher_is_better': False},\n"
        "    {'name': 'p95_latency',  'baseline': 280,  'current': 340,  'threshold': 500,  'higher_is_better': False},\n"
        "    {'name': 'throughput',   'baseline': 850,  'current': 820,  'threshold': 600,  'higher_is_better': True},\n"
        "    {'name': 'active_users', 'baseline': 5200, 'current': 5800, 'threshold': None, 'higher_is_better': True},\n"
        "])\n"
    ),
    expected_output=(
        "Post-Release: v2.5.0\n"
        "  error_rate:    baseline=0.5   current=0.8   delta=+60.0%  ELEVATED\n"
        "  p95_latency:   baseline=280   current=340   delta=+21.4%  ELEVATED\n"
        "  throughput:    baseline=850   current=820   delta=-3.5%   OK\n"
        "  active_users:  baseline=5200  current=5800  delta=+11.5%  OK\n"
        "Alerts: 2 anomalies detected"
    ),
)

L73 = dict(
    **_BASE, level_order=73, title="Sprint Forecast Calculator", difficulty="medium",
    description=(
        "Implementa `sprint_forecast(velocities, backlog_points, sprint_weeks)` "
        "que proyecta cuándo se terminará el backlog.\n\n"
        "Usa el promedio de velocidades para la estimación base, "
        "y el mínimo para la estimación conservadora (P90).\n\n"
        "Imprime:\n"
        "`Sprint Forecast`\n"
        "`Velocity (last N): <lista separada por coma>`\n"
        "`Avg velocity: X pts/sprint`\n"
        "`Backlog: N pts`\n"
        "`Sprints needed: N  (N weeks at Nwk sprints)`\n"
        "`90th percentile estimate: N sprints (using min velocity: N pts)`"
    ),
    hint="ceil(backlog/avg) para sprints base, ceil(backlog/min_vel) para p90.",
    initial_code=(
        "import math\n\n"
        "def sprint_forecast(velocities, backlog_points, sprint_weeks):\n"
        "    pass\n\n"
        "sprint_forecast(\n"
        "    velocities=[42, 38, 45, 40, 43],\n"
        "    backlog_points=200,\n"
        "    sprint_weeks=2\n"
        ")\n"
    ),
    expected_output=(
        "Sprint Forecast\n"
        "Velocity (last 5): 42, 38, 45, 40, 43\n"
        "Avg velocity: 41.6 pts/sprint\n"
        "Backlog: 200 pts\n"
        "Sprints needed: 5  (10 weeks at 2wk sprints)\n"
        "90th percentile estimate: 6 sprints (using min velocity: 38 pts)"
    ),
)

L74 = dict(
    **_BASE, level_order=74, title="Blocker Escalation Tracker", difficulty="medium",
    description=(
        "Implementa `blocker_escalation(blockers)` que clasifica y prioriza blockers.\n\n"
        "Cada blocker: `{'id': str, 'description': str, 'days_open': int, 'owner': str}`.\n\n"
        "Clasificación por días:\n"
        "- URGENT (>=10 días): Escalate to VP\n"
        "- HIGH   (5-9 días):  Escalate to Manager\n"
        "- MEDIUM (2-4 días):  Follow up\n"
        "- LOW    (<2 días):   Monitor\n\n"
        "Ordena por days_open descendente. Imprime:\n"
        "`  [LEVEL] <id>: <description>`\n"
        "`          N days  Owner: <owner>  → <acción>`\n\n"
        "Al final: `Urgent: N  High: N  Medium: N  Low: N`"
    ),
    hint="Ordena con sorted(blockers, key=lambda b: b['days_open'], reverse=True).",
    initial_code=(
        "def blocker_escalation(blockers):\n"
        "    pass\n\n"
        "blocker_escalation([\n"
        "    {'id': 'BLK-01', 'description': 'Legal approval pending',          'days_open': 8,  'owner': 'Legal Team'},\n"
        "    {'id': 'BLK-02', 'description': 'Infra ticket unassigned',         'days_open': 3,  'owner': 'DevOps'},\n"
        "    {'id': 'BLK-03', 'description': 'Design assets not delivered',     'days_open': 1,  'owner': 'Designer'},\n"
        "    {'id': 'BLK-04', 'description': 'API credentials from vendor MIA', 'days_open': 12, 'owner': 'Vendor'},\n"
        "])\n"
    ),
    expected_output=(
        "  [URGENT] BLK-04: API credentials from vendor MIA\n"
        "           12 days  Owner: Vendor  → Escalate to VP\n"
        "  [HIGH]   BLK-01: Legal approval pending\n"
        "           8 days  Owner: Legal Team  → Escalate to Manager\n"
        "  [MEDIUM] BLK-02: Infra ticket unassigned\n"
        "           3 days  Owner: DevOps  → Follow up\n"
        "  [LOW]    BLK-03: Design assets not delivered\n"
        "           1 days  Owner: Designer  → Monitor\n"
        "Urgent: 1  High: 1  Medium: 1  Low: 1"
    ),
)

L75 = dict(
    **_BASE_BOSS, level_order=75,
    title="CONTRATO-TPM-75: Execution Dashboard",
    difficulty="legendary", is_phase_boss=True, is_project=True,
    description=(
        "Implementa `ExecutionDashboard` que consolida todas las métricas de ejecución.\n\n"
        "Métodos:\n"
        "- `add_sprint(number, committed, completed)`\n"
        "- `add_gate(name, status, required)` — status: 'pass'|'fail'\n"
        "- `add_blocker(description, days_open)`\n"
        "- `generate_dashboard(program_name)` — imprime el dashboard\n\n"
        "Secciones del dashboard:\n"
        "1. Header con program_name\n"
        "2. SPRINT VELOCITY: últimos 3 sprints + avg + trend (IMPROVING/DECLINING/STABLE)\n"
        "3. RELEASE GATES: PASS/FAIL + GO/NO-GO verdict\n"
        "4. BLOCKERS: clasificados por urgencia (>=5d=HIGH, else MEDIUM)\n"
        "5. OVERALL STATUS: RED si NO-GO o blocker HIGH; YELLOW si algún gate fail opcional; GREEN si todo OK"
    ),
    hint="Calcula avg velocity como round(sum/len,1). Trend: last > first → IMPROVING.",
    initial_code=(
        "class ExecutionDashboard:\n"
        "    def __init__(self):\n"
        "        self.sprints  = []\n"
        "        self.gates    = []\n"
        "        self.blockers = []\n\n"
        "    def add_sprint(self, number, committed, completed):\n"
        "        pass\n\n"
        "    def add_gate(self, name, status, required):\n"
        "        pass\n\n"
        "    def add_blocker(self, description, days_open):\n"
        "        pass\n\n"
        "    def generate_dashboard(self, program_name):\n"
        "        pass\n\n\n"
        "dash = ExecutionDashboard()\n"
        "dash.add_sprint(1, 40, 38)\n"
        "dash.add_sprint(2, 45, 45)\n"
        "dash.add_sprint(3, 50, 44)\n"
        "dash.add_gate('Unit tests', 'pass', True)\n"
        "dash.add_gate('E2E tests',  'fail', True)\n"
        "dash.add_gate('Perf test',  'pass', False)\n"
        "dash.add_blocker('Auth vendor delay',    6)\n"
        "dash.add_blocker('Missing QA resource',  3)\n"
        "dash.generate_dashboard('DAKI Platform v3.0')\n"
    ),
    expected_output=(
        "╔═══════════════════════════════════════╗\n"
        "║  EXECUTION: DAKI Platform v3.0       ║\n"
        "╚═══════════════════════════════════════╝\n"
        "\n"
        "SPRINT VELOCITY:\n"
        "  Sprint 1: 38/40 pts (95%)\n"
        "  Sprint 2: 45/45 pts (100%)\n"
        "  Sprint 3: 44/50 pts (88%)\n"
        "  Avg: 42.3 pts  Trend: IMPROVING\n"
        "\n"
        "RELEASE GATES:\n"
        "  [PASS] Unit tests  (required)\n"
        "  [FAIL] E2E tests   (required) ← BLOCKING\n"
        "  [PASS] Perf test   (optional)\n"
        "  Verdict: NO-GO\n"
        "\n"
        "BLOCKERS (2):\n"
        "  [HIGH]   Auth vendor delay    6 days\n"
        "  [MEDIUM] Missing QA resource  3 days\n"
        "\n"
        "OVERALL STATUS: RED"
    ),
)

BLOQUE5 = [L61,L62,L63,L64,L65,L66,L67,L68,L69,L70,L71,L72,L73,L74,L75]
