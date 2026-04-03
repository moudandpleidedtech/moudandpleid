"""
_tpm_b3.py — TPM Mastery · BLOQUE 3 (L31–L45)
===============================================
Fase: finanzas_negocio
Niveles: 31 a 45 (15 desafíos Python)
Boss: L45 — Business Case Generator
"""
from __future__ import annotations

_BASE = dict(
    codex_id       = "tpm_mastery",
    sector_id      = 21,
    challenge_type = "python",
    phase          = "finanzas_negocio",
    is_free        = False,
    strict_match   = False,
    is_phase_boss  = False,
    is_project     = False,
)
_BASE_BOSS = {k: v for k, v in _BASE.items() if k not in ("is_phase_boss", "is_project")}

# ─────────────────────────────────────────────────────────────────────────────
# L31 — ROI Calculator
# ─────────────────────────────────────────────────────────────────────────────
L31 = dict(
    **_BASE,
    level_order   = 31,
    title         = "ROI Calculator",
    difficulty    = "easy",
    description   = (
        "El ROI es el primer número que el CFO mira. "
        "Implementa `roi_report(projects)` que calcula el retorno sobre inversión.\n\n"
        "Cada proyecto: `{'name': str, 'investment': float, 'annual_benefit': float, 'years': int}`.\n\n"
        "Fórmulas:\n"
        "- `total_benefit = annual_benefit * years`\n"
        "- `net_benefit   = total_benefit - investment`\n"
        "- `roi_pct       = net_benefit / investment * 100` (1 dec)\n"
        "- `payback_years = investment / annual_benefit` (1 dec)\n\n"
        "Imprime por proyecto:\n"
        "`<name>: invest=$X  benefit=$X  ROI=X%  payback=Xy`\n"
        "`  → [APPROVE|REVIEW|REJECT]`\n\n"
        "APPROVE si roi_pct >= 50, REJECT si roi_pct < 0, REVIEW en otro caso.\n\n"
        "Al final: `Approved: N  Review: N  Rejected: N`"
    ),
    hint          = "Redondea roi_pct a 1 decimal. payback_years también a 1 decimal.",
    initial_code  = (
        "def roi_report(projects):\n"
        "    pass\n\n"
        "projects = [\n"
        "    {'name': 'Platform rewrite',   'investment': 200000, 'annual_benefit': 80000,  'years': 3},\n"
        "    {'name': 'Auth modernization', 'investment': 50000,  'annual_benefit': 45000,  'years': 2},\n"
        "    {'name': 'Legacy migration',   'investment': 300000, 'annual_benefit': 120000, 'years': 3},\n"
        "    {'name': 'Chatbot feature',    'investment': 80000,  'annual_benefit': 15000,  'years': 2},\n"
        "]\n"
        "roi_report(projects)\n"
    ),
    expected_output = (
        "Platform rewrite: invest=$200000  benefit=$240000  ROI=20.0%  payback=2.5y\n"
        "  → REVIEW\n"
        "Auth modernization: invest=$50000  benefit=$90000  ROI=80.0%  payback=1.1y\n"
        "  → APPROVE\n"
        "Legacy migration: invest=$300000  benefit=$360000  ROI=20.0%  payback=2.5y\n"
        "  → REVIEW\n"
        "Chatbot feature: invest=$80000  benefit=$30000  ROI=-62.5%  payback=5.3y\n"
        "  → REJECT\n"
        "Approved: 1  Review: 2  Rejected: 1"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L32 — Break-Even Analyzer
# ─────────────────────────────────────────────────────────────────────────────
L32 = dict(
    **_BASE,
    level_order   = 32,
    title         = "Break-Even Analyzer",
    difficulty    = "medium",
    description   = (
        "El punto de equilibrio es la conversación que el TPM tiene con el CFO antes de aprobar headcount. "
        "Implementa `break_even_analysis(products)` que calcula el punto de equilibrio.\n\n"
        "Cada producto: `{'name': str, 'fixed_cost': float, 'variable_cost_per_unit': float, "
        "'price_per_unit': float}`.\n\n"
        "Fórmulas:\n"
        "- `contribution_margin = price_per_unit - variable_cost_per_unit`\n"
        "- `break_even_units    = ceil(fixed_cost / contribution_margin)`\n"
        "- `break_even_revenue  = break_even_units * price_per_unit`\n\n"
        "Imprime por producto:\n"
        "`<name>:`\n"
        "`  Price=$X  VarCost=$X  Margin=$X (X%)`\n"
        "`  Break-even: N units = $X revenue`\n\n"
        "El margen % = contribution_margin / price_per_unit * 100 (1 dec)."
    ),
    hint          = "Importa math.ceil. Contribution margin = precio - costo variable.",
    initial_code  = (
        "import math\n\n"
        "def break_even_analysis(products):\n"
        "    pass\n\n"
        "products = [\n"
        "    {'name': 'DAKI Pro Plan',      'fixed_cost': 50000,  'variable_cost_per_unit': 8.0,  'price_per_unit': 29.0},\n"
        "    {'name': 'DAKI Enterprise',    'fixed_cost': 120000, 'variable_cost_per_unit': 25.0, 'price_per_unit': 199.0},\n"
        "    {'name': 'DAKI Certification', 'fixed_cost': 30000,  'variable_cost_per_unit': 12.0, 'price_per_unit': 49.0},\n"
        "]\n"
        "break_even_analysis(products)\n"
    ),
    expected_output = (
        "DAKI Pro Plan:\n"
        "  Price=$29.0  VarCost=$8.0  Margin=$21.0 (72.4%)\n"
        "  Break-even: 2381 units = $69049.0 revenue\n"
        "DAKI Enterprise:\n"
        "  Price=$199.0  VarCost=$25.0  Margin=$174.0 (87.4%)\n"
        "  Break-even: 690 units = $137310.0 revenue\n"
        "DAKI Certification:\n"
        "  Price=$49.0  VarCost=$12.0  Margin=$37.0 (75.5%)\n"
        "  Break-even: 811 units = $39739.0 revenue"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L33 — Unit Economics Calculator
# ─────────────────────────────────────────────────────────────────────────────
L33 = dict(
    **_BASE,
    level_order   = 33,
    title         = "Unit Economics Calculator",
    difficulty    = "medium",
    description   = (
        "LTV/CAC es el ratio que determina si un negocio es viable. "
        "Implementa `unit_economics(cohorts)` que calcula las métricas clave por cohorte.\n\n"
        "Cada cohorte: `{'name': str, 'cac': float, 'monthly_revenue': float, "
        "'churn_rate_pct': float, 'gross_margin_pct': float}`.\n\n"
        "Fórmulas:\n"
        "- `ltv = (monthly_revenue * gross_margin_pct/100) / (churn_rate_pct/100)`\n"
        "- `ltv_cac_ratio = ltv / cac` (2 dec)\n"
        "- `payback_months = cac / (monthly_revenue * gross_margin_pct/100)` (1 dec)\n\n"
        "Imprime por cohorte:\n"
        "`<name>: LTV=$X  CAC=$X  LTV/CAC=X  payback=Xmo`\n"
        "`  → [EXCELLENT|GOOD|POOR]`\n\n"
        "EXCELLENT si ltv_cac_ratio >= 3, GOOD si >= 1, POOR si < 1."
    ),
    hint          = "LTV = (MRR × GM%) / churn%. Guarda 2 decimales en LTV/CAC.",
    initial_code  = (
        "def unit_economics(cohorts):\n"
        "    pass\n\n"
        "cohorts = [\n"
        "    {'name': 'Enterprise Q1', 'cac': 1200, 'monthly_revenue': 200, 'churn_rate_pct': 2.0,  'gross_margin_pct': 75},\n"
        "    {'name': 'SMB Q1',        'cac': 350,  'monthly_revenue': 45,  'churn_rate_pct': 5.0,  'gross_margin_pct': 70},\n"
        "    {'name': 'Freemium Q2',   'cac': 80,   'monthly_revenue': 12,  'churn_rate_pct': 15.0, 'gross_margin_pct': 80},\n"
        "]\n"
        "unit_economics(cohorts)\n"
    ),
    expected_output = (
        "Enterprise Q1: LTV=$7500.0  CAC=$1200  LTV/CAC=6.25  payback=8.0mo\n"
        "  → EXCELLENT\n"
        "SMB Q1: LTV=$630.0  CAC=$350  LTV/CAC=1.8  payback=11.1mo\n"
        "  → GOOD\n"
        "Freemium Q2: LTV=$64.0  CAC=$80  LTV/CAC=0.8  payback=8.3mo\n"
        "  → POOR"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L34 — P&L Simplifier
# ─────────────────────────────────────────────────────────────────────────────
L34 = dict(
    **_BASE,
    level_order   = 34,
    title         = "P&L Simplifier",
    difficulty    = "medium",
    description   = (
        "Un TPM que entiende el P&L puede hablar el idioma de los ejecutivos. "
        "Implementa `pl_report(quarters)` que construye un estado de resultados simplificado.\n\n"
        "Cada quarter: `{'name': str, 'revenue': float, 'cogs': float, "
        "'opex': float, 'tax_rate_pct': float}`.\n\n"
        "Cálculos:\n"
        "- `gross_profit = revenue - cogs`\n"
        "- `gross_margin_pct = gross_profit / revenue * 100` (1 dec)\n"
        "- `ebitda = gross_profit - opex`\n"
        "- `tax = max(0, ebitda * tax_rate_pct / 100)`\n"
        "- `net_income = ebitda - tax`\n\n"
        "Imprime por quarter:\n"
        "`<name>: Rev=$X  GP=$X (X%)  EBITDA=$X  Net=$X  [PROFIT|LOSS]`\n\n"
        "PROFIT si net_income > 0, LOSS si <= 0.\n\n"
        "Al final: `Full year: Rev=$X  Net=$X  Avg GM=X%`"
    ),
    hint          = "El tax solo aplica si ebitda > 0. max(0, ...) lo resuelve.",
    initial_code  = (
        "def pl_report(quarters):\n"
        "    pass\n\n"
        "quarters = [\n"
        "    {'name': 'Q1 2024', 'revenue': 480000, 'cogs': 192000, 'opex': 310000, 'tax_rate_pct': 25},\n"
        "    {'name': 'Q2 2024', 'revenue': 560000, 'cogs': 210000, 'opex': 290000, 'tax_rate_pct': 25},\n"
        "    {'name': 'Q3 2024', 'revenue': 640000, 'cogs': 224000, 'opex': 270000, 'tax_rate_pct': 25},\n"
        "    {'name': 'Q4 2024', 'revenue': 720000, 'cogs': 230000, 'opex': 260000, 'tax_rate_pct': 25},\n"
        "]\n"
        "pl_report(quarters)\n"
    ),
    expected_output = (
        "Q1 2024: Rev=$480000  GP=$288000 (60.0%)  EBITDA=$-22000  Net=$-22000  LOSS\n"
        "Q2 2024: Rev=$560000  GP=$350000 (62.5%)  EBITDA=$60000   Net=$45000   PROFIT\n"
        "Q3 2024: Rev=$640000  GP=$416000 (65.0%)  EBITDA=$146000  Net=$109500  PROFIT\n"
        "Q4 2024: Rev=$720000  GP=$490000 (68.1%)  EBITDA=$230000  Net=$172500  PROFIT\n"
        "Full year: Rev=$2400000  Net=$305000  Avg GM=63.9%"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L35 — Make vs Buy Evaluator
# ─────────────────────────────────────────────────────────────────────────────
L35 = dict(
    **_BASE,
    level_order   = 35,
    title         = "Make vs Buy Evaluator",
    difficulty    = "hard",
    description   = (
        "La decisión Make vs Buy es una de las más estratégicas que enfrenta un TPM. "
        "Implementa `make_vs_buy(decision)` que evalúa ambas alternativas.\n\n"
        "decision: `{'feature': str, 'make': dict, 'buy': dict}`.\n\n"
        "make: `{'dev_months': int, 'monthly_eng_cost': float, "
        "'monthly_maintenance': float, 'control_score': int}`\n"
        "buy: `{'setup_cost': float, 'monthly_license': float, "
        "'integration_months': int, 'control_score': int}`\n\n"
        "Calcula para un horizonte de 36 meses:\n"
        "- make_total = dev_months × monthly_eng_cost + (36 - dev_months) × monthly_maintenance\n"
        "- buy_total  = setup_cost + integration_months × monthly_eng_cost_equivalent "
        "+ 36 × monthly_license\n"
        "  (usa monthly_eng_cost del make como monthly_eng_cost_equivalent para la integración)\n\n"
        "Imprime ambas opciones con su costo total a 36 meses y control score.\n"
        "Decisión: la de menor costo total, con nota si control_score difiere > 2 puntos.\n\n"
        "Formato exacto:\n"
        "`Feature: <feature>`\n"
        "`  MAKE: $X (36mo)  control=N/5`\n"
        "`  BUY:  $X (36mo)  control=N/5`\n"
        "`  Decision: [MAKE|BUY] — saves $X`\n"
        "`  Note: <nota si aplica>`"
    ),
    hint          = "Calcula make_total y buy_total, luego compara. La nota solo aparece si control difiere > 2.",
    initial_code  = (
        "def make_vs_buy(decision):\n"
        "    pass\n\n"
        "make_vs_buy({\n"
        "    'feature': 'SSO Authentication',\n"
        "    'make': {\n"
        "        'dev_months': 4,\n"
        "        'monthly_eng_cost': 15000,\n"
        "        'monthly_maintenance': 2000,\n"
        "        'control_score': 5,\n"
        "    },\n"
        "    'buy': {\n"
        "        'setup_cost': 8000,\n"
        "        'monthly_license': 1200,\n"
        "        'integration_months': 1,\n"
        "        'control_score': 2,\n"
        "    },\n"
        "})\n"
    ),
    expected_output = (
        "Feature: SSO Authentication\n"
        "  MAKE: $124000 (36mo)  control=5/5\n"
        "  BUY:  $66200 (36mo)  control=2/5\n"
        "  Decision: BUY — saves $57800\n"
        "  Note: BUY scores 3 pts lower on control — verify vendor lock-in risk"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L36 — Budget Variance Tracker
# ─────────────────────────────────────────────────────────────────────────────
L36 = dict(
    **_BASE,
    level_order   = 36,
    title         = "Budget Variance Tracker",
    difficulty    = "medium",
    description   = (
        "El control presupuestario es la responsabilidad financiera del TPM. "
        "Implementa `budget_variance(line_items)` que analiza desviaciones.\n\n"
        "Cada ítem: `{'category': str, 'budgeted': float, 'actual': float}`.\n\n"
        "Para cada ítem:\n"
        "- `variance = actual - budgeted`\n"
        "- `variance_pct = variance / budgeted * 100` (1 dec)\n\n"
        "Imprime:\n"
        "`<category padded 20>  budget=$X  actual=$X  variance=+X|-X (X%|-X%)  [OK|OVER|UNDER]`\n\n"
        "OVER si variance > 0, UNDER si variance < 0, OK si == 0.\n\n"
        "Al final:\n"
        "`Total budget: $X  Total actual: $X  Overall variance: $+X|-X (X%)`\n"
        "`Status: [ON BUDGET|OVER BUDGET|UNDER BUDGET]`\n\n"
        "Status global usa el total."
    ),
    hint          = "Acumula totales mientras iteras. El signo del variance puede ser + o -.",
    initial_code  = (
        "def budget_variance(line_items):\n"
        "    pass\n\n"
        "line_items = [\n"
        "    {'category': 'Engineering',  'budgeted': 180000, 'actual': 195000},\n"
        "    {'category': 'Cloud Infra',  'budgeted':  48000, 'actual':  41500},\n"
        "    {'category': 'Tooling',      'budgeted':  12000, 'actual':  12000},\n"
        "    {'category': 'QA & Testing', 'budgeted':  30000, 'actual':  37500},\n"
        "    {'category': 'Design',       'budgeted':  24000, 'actual':  21000},\n"
        "]\n"
        "budget_variance(line_items)\n"
    ),
    expected_output = (
        "Engineering            budget=$180000  actual=$195000  variance=+$15000 (+8.3%)  OVER\n"
        "Cloud Infra            budget=$48000   actual=$41500   variance=-$6500 (-13.5%)  UNDER\n"
        "Tooling                budget=$12000   actual=$12000   variance=$0 (0.0%)        OK\n"
        "QA & Testing           budget=$30000   actual=$37500   variance=+$7500 (+25.0%)  OVER\n"
        "Design                 budget=$24000   actual=$21000   variance=-$3000 (-12.5%)  UNDER\n"
        "Total budget: $294000  Total actual: $307000  Overall variance: +$13000 (+4.4%)\n"
        "Status: OVER BUDGET"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L37 — Headcount ROI Model
# ─────────────────────────────────────────────────────────────────────────────
L37 = dict(
    **_BASE,
    level_order   = 37,
    title         = "Headcount ROI Model",
    difficulty    = "hard",
    description   = (
        "Contratar es una inversión, no un gasto. "
        "Implementa `headcount_roi(hires)` que evalúa el retorno de nuevas contrataciones.\n\n"
        "Cada hire: `{'role': str, 'annual_cost': float, "
        "'productivity_month': int, 'annual_value_generated': float}`.\n\n"
        "`productivity_month` = mes en que el hire alcanza productividad plena.\n\n"
        "Cálculos (horizonte 12 meses):\n"
        "- `ramp_cost    = annual_cost / 12 * productivity_month * 0.5` (costo de los meses de ramp a 50%)\n"
        "- `full_months  = 12 - productivity_month`\n"
        "- `value_full   = annual_value_generated / 12 * full_months`\n"
        "- `net_value    = value_full - annual_cost` (valor neto en 12 meses)\n"
        "- `roi_12m_pct  = net_value / annual_cost * 100` (1 dec)\n\n"
        "Imprime por hire:\n"
        "`<role>: cost=$X/yr  value=$X/yr  ramp=Mo N  ROI(12mo)=X%  [HIRE|DEFER]`\n\n"
        "HIRE si roi_12m_pct >= -20 (se acepta hasta un -20% el primer año)."
    ),
    hint          = "ramp_cost es solo informativo, no afecta el ROI. net_value = value generado - costo total.",
    initial_code  = (
        "def headcount_roi(hires):\n"
        "    pass\n\n"
        "hires = [\n"
        "    {'role': 'Senior Engineer',  'annual_cost': 180000, 'productivity_month': 2, 'annual_value_generated': 250000},\n"
        "    {'role': 'QA Engineer',      'annual_cost': 110000, 'productivity_month': 1, 'annual_value_generated': 130000},\n"
        "    {'role': 'Data Scientist',   'annual_cost': 160000, 'productivity_month': 4, 'annual_value_generated': 140000},\n"
        "    {'role': 'DevOps Engineer',  'annual_cost': 140000, 'productivity_month': 2, 'annual_value_generated': 200000},\n"
        "]\n"
        "headcount_roi(hires)\n"
    ),
    expected_output = (
        "Senior Engineer:  cost=$180000/yr  value=$250000/yr  ramp=Mo 2  ROI(12mo)=22.2%   HIRE\n"
        "QA Engineer:      cost=$110000/yr  value=$130000/yr  ramp=Mo 1  ROI(12mo)=8.3%    HIRE\n"
        "Data Scientist:   cost=$160000/yr  value=$140000/yr  ramp=Mo 4  ROI(12mo)=-29.2%  DEFER\n"
        "DevOps Engineer:  cost=$140000/yr  value=$200000/yr  ramp=Mo 2  ROI(12mo)=19.0%   HIRE"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L38 — TCO (Total Cost of Ownership) Comparator
# ─────────────────────────────────────────────────────────────────────────────
L38 = dict(
    **_BASE,
    level_order   = 38,
    title         = "TCO Comparator",
    difficulty    = "medium",
    description   = (
        "El TCO revela el costo real de una solución más allá del precio de lista. "
        "Implementa `tco_compare(solutions, years)` que calcula el costo total de propiedad.\n\n"
        "Cada solución: `{'name': str, 'initial_cost': float, 'annual_license': float, "
        "'annual_maintenance': float, 'training_cost': float, 'migration_cost': float}`.\n\n"
        "`tco = initial_cost + training_cost + migration_cost + "
        "(annual_license + annual_maintenance) * years`\n\n"
        "Imprime ordenado por TCO ascendente:\n"
        "`N. <name>: TCO=$X (Nyr)`\n"
        "`   Initial=$X  Recurring=$X/yr  Setup=$X`\n\n"
        "Setup = training + migration.\n"
        "Recurring = annual_license + annual_maintenance.\n\n"
        "Al final: `Best value: <nombre>  |  Savings vs worst: $X`"
    ),
    hint          = "Ordena por tco. Savings = tco_worst - tco_best.",
    initial_code  = (
        "def tco_compare(solutions, years):\n"
        "    pass\n\n"
        "solutions = [\n"
        "    {'name': 'AWS Managed',    'initial_cost': 0,      'annual_license': 60000, 'annual_maintenance': 8000,  'training_cost': 5000,  'migration_cost': 15000},\n"
        "    {'name': 'Self-Hosted',    'initial_cost': 80000,  'annual_license': 0,     'annual_maintenance': 25000, 'training_cost': 12000, 'migration_cost': 20000},\n"
        "    {'name': 'SaaS Vendor',    'initial_cost': 5000,   'annual_license': 72000, 'annual_maintenance': 0,     'training_cost': 3000,  'migration_cost': 8000},\n"
        "]\n"
        "tco_compare(solutions, years=3)\n"
    ),
    expected_output = (
        "1. AWS Managed: TCO=$224000 (3yr)\n"
        "   Initial=$0  Recurring=$68000/yr  Setup=$20000\n"
        "2. Self-Hosted: TCO=$187000 (3yr)\n"
        "   Initial=$80000  Recurring=$25000/yr  Setup=$32000\n"
        "3. SaaS Vendor: TCO=$232000 (3yr)\n"
        "   Initial=$5000  Recurring=$72000/yr  Setup=$11000\n"
        "Best value: Self-Hosted  |  Savings vs worst: $45000"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L39 — Revenue Impact Estimator
# ─────────────────────────────────────────────────────────────────────────────
L39 = dict(
    **_BASE,
    level_order   = 39,
    title         = "Revenue Impact Estimator",
    difficulty    = "hard",
    description   = (
        "Implementa `revenue_impact(scenarios)` que modela el impacto en ingresos "
        "de iniciativas tecnológicas bajo 3 escenarios.\n\n"
        "Cada iniciativa: `{'name': str, 'base_revenue': float, "
        "'scenarios': {'pessimistic': float, 'base': float, 'optimistic': float}}`.\n\n"
        "Los valores de escenario son multiplicadores (e.g. 1.05 = +5% de revenue).\n\n"
        "Calcula para cada escenario: `impact = base_revenue * multiplier - base_revenue`.\n\n"
        "Imprime por iniciativa:\n"
        "`<name> (base=$X):`\n"
        "`  Pessimistic: $+X|-X  |  Base: $+X|-X  |  Optimistic: $+X|-X`\n\n"
        "Al final: `Portfolio Base Case: $+X total impact across N initiatives`\n"
        "(suma de impactos en el escenario 'base')"
    ),
    hint          = "impact = base_revenue * (multiplier - 1). Usa f'$+{x:,.0f}' o f'$-{abs(x):,.0f}'.",
    initial_code  = (
        "def revenue_impact(scenarios):\n"
        "    pass\n\n"
        "initiatives = [\n"
        "    {'name': 'Mobile App Launch', 'base_revenue': 1200000,\n"
        "     'scenarios': {'pessimistic': 1.03, 'base': 1.08, 'optimistic': 1.18}},\n"
        "    {'name': 'API Marketplace',   'base_revenue': 800000,\n"
        "     'scenarios': {'pessimistic': 1.05, 'base': 1.12, 'optimistic': 1.25}},\n"
        "    {'name': 'AI Personalization','base_revenue': 600000,\n"
        "     'scenarios': {'pessimistic': 0.98, 'base': 1.06, 'optimistic': 1.20}},\n"
        "]\n"
        "revenue_impact(initiatives)\n"
    ),
    expected_output = (
        "Mobile App Launch (base=$1,200,000):\n"
        "  Pessimistic: $+36,000  |  Base: $+96,000  |  Optimistic: $+216,000\n"
        "API Marketplace (base=$800,000):\n"
        "  Pessimistic: $+40,000  |  Base: $+96,000  |  Optimistic: $+200,000\n"
        "AI Personalization (base=$600,000):\n"
        "  Pessimistic: $-12,000  |  Base: $+36,000  |  Optimistic: $+120,000\n"
        "Portfolio Base Case: $+228,000 total impact across 3 initiatives"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L40 — Cost per Feature Analyzer
# ─────────────────────────────────────────────────────────────────────────────
L40 = dict(
    **_BASE,
    level_order   = 40,
    title         = "Cost per Feature Analyzer",
    difficulty    = "medium",
    description   = (
        "Saber cuánto cuesta cada feature permite priorizar con datos. "
        "Implementa `cost_per_feature(team, sprints)` que distribuye el costo del equipo "
        "entre las features entregadas.\n\n"
        "team: lista de `{'name': str, 'weekly_cost': float}`.\n"
        "sprints: lista de `{'number': int, 'weeks': int, 'features': list[str]}`.\n\n"
        "Para cada sprint:\n"
        "- `sprint_cost = sum(weekly_cost) * weeks`\n"
        "- `cost_per_feature = sprint_cost / len(features)` (si hay features)\n\n"
        "Imprime por sprint:\n"
        "`Sprint N (N weeks): total=$X  N features  avg=$X/feature`\n"
        "Luego cada feature: `  - <feature>: $X`\n\n"
        "Al final: `Total delivered: N features  Total cost: $X  Overall avg: $X/feature`"
    ),
    hint          = "Redondea los costos a enteros para mayor claridad.",
    initial_code  = (
        "def cost_per_feature(team, sprints):\n"
        "    pass\n\n"
        "team = [\n"
        "    {'name': 'Ana',   'weekly_cost': 3500},\n"
        "    {'name': 'Bruno', 'weekly_cost': 3200},\n"
        "    {'name': 'Cata',  'weekly_cost': 2800},\n"
        "]\n"
        "sprints = [\n"
        "    {'number': 1, 'weeks': 2, 'features': ['Login flow', 'Registration', 'Email verify']},\n"
        "    {'number': 2, 'weeks': 2, 'features': ['Dashboard', 'Profile settings']},\n"
        "    {'number': 3, 'weeks': 3, 'features': ['Analytics', 'Export CSV', 'Notifications', 'Search']},\n"
        "]\n"
        "cost_per_feature(team, sprints)\n"
    ),
    expected_output = (
        "Sprint 1 (2 weeks): total=$19000  3 features  avg=$6333/feature\n"
        "  - Login flow: $6333\n"
        "  - Registration: $6333\n"
        "  - Email verify: $6333\n"
        "Sprint 2 (2 weeks): total=$19000  2 features  avg=$9500/feature\n"
        "  - Dashboard: $9500\n"
        "  - Profile settings: $9500\n"
        "Sprint 3 (3 weeks): total=$28500  4 features  avg=$7125/feature\n"
        "  - Analytics: $7125\n"
        "  - Export CSV: $7125\n"
        "  - Notifications: $7125\n"
        "  - Search: $7125\n"
        "Total delivered: 9 features  Total cost: $66500  Overall avg: $7389/feature"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L41 — Opportunity Cost Calculator
# ─────────────────────────────────────────────────────────────────────────────
L41 = dict(
    **_BASE,
    level_order   = 41,
    title         = "Opportunity Cost Calculator",
    difficulty    = "hard",
    description   = (
        "El costo de oportunidad es lo que cuesta NO hacer algo. "
        "Implementa `opportunity_cost(options, team_capacity_weeks)` que evalúa qué proyectos "
        "no caben dado un límite de capacidad.\n\n"
        "Cada opción: `{'name': str, 'weeks_required': int, 'annual_value': float, 'priority': int}`.\n\n"
        "Selecciona proyectos en orden de prioridad (menor número = mayor prioridad) "
        "hasta agotar la capacidad.\n\n"
        "Imprime:\n"
        "`SELECTED (capacity used: N/N weeks):`\n"
        "Luego los seleccionados: `  [SELECTED] <name>: Nwk  value=$X`\n\n"
        "`NOT FUNDED (opportunity cost):`\n"
        "Luego los no seleccionados: `  [DEFERRED] <name>: Nwk  value=$X`\n\n"
        "Al final:\n"
        "`Selected value: $X  |  Opportunity cost: $X`"
    ),
    hint          = "Ordena por priority, itera acumulando semanas hasta pasar la capacidad.",
    initial_code  = (
        "def opportunity_cost(options, team_capacity_weeks):\n"
        "    pass\n\n"
        "options = [\n"
        "    {'name': 'Auth revamp',       'weeks_required': 6,  'annual_value': 200000, 'priority': 1},\n"
        "    {'name': 'Mobile app',        'weeks_required': 16, 'annual_value': 450000, 'priority': 2},\n"
        "    {'name': 'Analytics v2',      'weeks_required': 8,  'annual_value': 180000, 'priority': 3},\n"
        "    {'name': 'API marketplace',   'weeks_required': 12, 'annual_value': 320000, 'priority': 4},\n"
        "    {'name': 'AI features',       'weeks_required': 10, 'annual_value': 280000, 'priority': 5},\n"
        "]\n"
        "opportunity_cost(options, team_capacity_weeks=26)\n"
    ),
    expected_output = (
        "SELECTED (capacity used: 22/26 weeks):\n"
        "  [SELECTED] Auth revamp: 6wk  value=$200,000\n"
        "  [SELECTED] Mobile app: 16wk  value=$450,000\n"
        "NOT FUNDED (opportunity cost):\n"
        "  [DEFERRED] Analytics v2: 8wk  value=$180,000\n"
        "  [DEFERRED] API marketplace: 12wk  value=$320,000\n"
        "  [DEFERRED] AI features: 10wk  value=$280,000\n"
        "Selected value: $650,000  |  Opportunity cost: $780,000"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L42 — Vendor Evaluation Scorecard
# ─────────────────────────────────────────────────────────────────────────────
L42 = dict(
    **_BASE,
    level_order   = 42,
    title         = "Vendor Evaluation Scorecard",
    difficulty    = "medium",
    description   = (
        "Elegir un vendor es una decisión financiera y de riesgo. "
        "Implementa `vendor_scorecard(vendors, criteria_weights)` que puntúa vendors.\n\n"
        "Cada vendor: `{'name': str, 'scores': dict}` (dict de criterio → score 1-5).\n"
        "criteria_weights: dict de criterio → peso (suman 1.0).\n\n"
        "Calcula `weighted_score = sum(score * weight)` (2 dec).\n\n"
        "Imprime ordenado por score desc:\n"
        "`N. <name>: score=X.XX  [RECOMMENDED|VIABLE|NOT RECOMMENDED]`\n"
        "Luego los scores por criterio: `   <criterion>=N (weight=X%)`\n\n"
        "RECOMMENDED si score >= 3.5, NOT RECOMMENDED si score < 2.5, VIABLE en otro caso.\n\n"
        "Al final: `Recommendation: <nombre del primero>`"
    ),
    hint          = "El peso en porcentaje = weight * 100 como entero.",
    initial_code  = (
        "def vendor_scorecard(vendors, criteria_weights):\n"
        "    pass\n\n"
        "criteria_weights = {\n"
        "    'price':       0.30,\n"
        "    'reliability': 0.25,\n"
        "    'support':     0.20,\n"
        "    'integration': 0.15,\n"
        "    'roadmap':     0.10,\n"
        "}\n"
        "vendors = [\n"
        "    {'name': 'VendorA', 'scores': {'price': 4, 'reliability': 5, 'support': 4, 'integration': 3, 'roadmap': 4}},\n"
        "    {'name': 'VendorB', 'scores': {'price': 5, 'reliability': 3, 'support': 3, 'integration': 4, 'roadmap': 3}},\n"
        "    {'name': 'VendorC', 'scores': {'price': 2, 'reliability': 4, 'support': 5, 'integration': 5, 'roadmap': 5}},\n"
        "]\n"
        "vendor_scorecard(vendors, criteria_weights)\n"
    ),
    expected_output = (
        "1. VendorA: score=4.10  RECOMMENDED\n"
        "   price=4 (weight=30%)  reliability=5 (weight=25%)  support=4 (weight=20%)  integration=3 (weight=15%)  roadmap=4 (weight=10%)\n"
        "2. VendorB: score=3.80  RECOMMENDED\n"
        "   price=5 (weight=30%)  reliability=3 (weight=25%)  support=3 (weight=20%)  integration=4 (weight=15%)  roadmap=3 (weight=10%)\n"
        "3. VendorC: score=3.70  RECOMMENDED\n"
        "   price=2 (weight=30%)  reliability=4 (weight=25%)  support=5 (weight=20%)  integration=5 (weight=15%)  roadmap=5 (weight=10%)\n"
        "Recommendation: VendorA"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L43 — Burn Rate Monitor
# ─────────────────────────────────────────────────────────────────────────────
L43 = dict(
    **_BASE,
    level_order   = 43,
    title         = "Burn Rate Monitor",
    difficulty    = "medium",
    description   = (
        "Implementa `burn_rate_monitor(budget, monthly_burns)` que monitorea "
        "el consumo del presupuesto mes a mes.\n\n"
        "`monthly_burns`: lista de floats (gasto por mes).\n\n"
        "Para cada mes imprime:\n"
        "`Month N: burned=$X  cumulative=$X  remaining=$X  runway=Nmo  [GREEN|YELLOW|RED]`\n\n"
        "Runway = remaining / avg_burn_so_far (en meses, 1 dec).\n"
        "Si runway < 2 → RED, si < 4 → YELLOW, si >= 4 → GREEN.\n\n"
        "Al final:\n"
        "`Avg monthly burn: $X  |  Projected end: month N`\n\n"
        "Projected end = month en que el acumulado supera el budget "
        "(usando el promedio de burns como tasa proyectada)."
    ),
    hint          = "avg_burn = cumulative / month_number. runway = remaining / avg_burn.",
    initial_code  = (
        "def burn_rate_monitor(budget, monthly_burns):\n"
        "    pass\n\n"
        "burn_rate_monitor(\n"
        "    budget=500000,\n"
        "    monthly_burns=[38000, 42000, 45000, 51000, 48000, 55000],\n"
        ")\n"
    ),
    expected_output = (
        "Month 1: burned=$38000   cumulative=$38000   remaining=$462000  runway=12.2mo  GREEN\n"
        "Month 2: burned=$42000   cumulative=$80000   remaining=$420000  runway=10.5mo  GREEN\n"
        "Month 3: burned=$45000   cumulative=$125000  remaining=$375000  runway=9.0mo   GREEN\n"
        "Month 4: burned=$51000   cumulative=$176000  remaining=$324000  runway=7.3mo   GREEN\n"
        "Month 5: burned=$48000   cumulative=$224000  remaining=$276000  runway=6.2mo   GREEN\n"
        "Month 6: burned=$55000   cumulative=$279000  remaining=$221000  runway=4.8mo   GREEN\n"
        "Avg monthly burn: $46500  |  Projected end: month 17"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L44 — Feature Value vs Cost Matrix
# ─────────────────────────────────────────────────────────────────────────────
L44 = dict(
    **_BASE,
    level_order   = 44,
    title         = "Feature Value vs Cost Matrix",
    difficulty    = "hard",
    description   = (
        "Implementa `value_cost_matrix(features)` que clasifica features "
        "en 4 cuadrantes según valor de negocio y costo de implementación.\n\n"
        "Cada feature: `{'name': str, 'business_value': int, 'dev_cost': int}` (1-10).\n\n"
        "Cuadrantes (umbral = 5):\n"
        "- value > 5 y cost <= 5 → `Quick Win`\n"
        "- value > 5 y cost > 5  → `Strategic Bet`\n"
        "- value <= 5 y cost <= 5 → `Fill-In`\n"
        "- value <= 5 y cost > 5  → `Money Pit`\n\n"
        "Imprime agrupado por cuadrante (en el orden: Quick Win, Strategic Bet, Fill-In, Money Pit):\n"
        "`[<quadrant>]`\n"
        "`  <name>  value=N  cost=N`\n\n"
        "Al final: `Quick Win: N  Strategic Bet: N  Fill-In: N  Money Pit: N`\n"
        "`Prioritize: <lista de Quick Wins separada por coma>`"
    ),
    hint          = "Agrupa en un dict de cuadrante → lista antes de imprimir.",
    initial_code  = (
        "def value_cost_matrix(features):\n"
        "    pass\n\n"
        "features = [\n"
        "    {'name': 'Dark mode',          'business_value': 4, 'dev_cost': 2},\n"
        "    {'name': 'SSO login',          'business_value': 9, 'dev_cost': 3},\n"
        "    {'name': 'AI recommendations', 'business_value': 8, 'dev_cost': 9},\n"
        "    {'name': 'Export to Excel',    'business_value': 7, 'dev_cost': 2},\n"
        "    {'name': 'Blockchain audit',   'business_value': 3, 'dev_cost': 8},\n"
        "    {'name': 'Email digest',       'business_value': 6, 'dev_cost': 1},\n"
        "    {'name': 'Advanced analytics', 'business_value': 8, 'dev_cost': 7},\n"
        "]\n"
        "value_cost_matrix(features)\n"
    ),
    expected_output = (
        "[Quick Win]\n"
        "  SSO login  value=9  cost=3\n"
        "  Export to Excel  value=7  cost=2\n"
        "  Email digest  value=6  cost=1\n"
        "[Strategic Bet]\n"
        "  AI recommendations  value=8  cost=9\n"
        "  Advanced analytics  value=8  cost=7\n"
        "[Fill-In]\n"
        "  Dark mode  value=4  cost=2\n"
        "[Money Pit]\n"
        "  Blockchain audit  value=3  cost=8\n"
        "Quick Win: 3  Strategic Bet: 2  Fill-In: 1  Money Pit: 1\n"
        "Prioritize: SSO login, Export to Excel, Email digest"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L45 — BOSS: Business Case Generator
# ─────────────────────────────────────────────────────────────────────────────
L45 = dict(
    **_BASE_BOSS,
    level_order   = 45,
    title         = "CONTRATO-TPM-45: Business Case Generator",
    difficulty    = "legendary",
    is_phase_boss = True,
    is_project    = True,
    description   = (
        "El business case es el documento que convierte ideas técnicas en aprobaciones ejecutivas. "
        "Implementa la clase `BusinessCase` que genera un business case completo.\n\n"
        "Métodos:\n"
        "- `__init__(title, owner, quarter)`\n"
        "- `set_investment(amount, breakdown)` — breakdown es dict de categoría→monto\n"
        "- `set_benefits(annual_revenue_uplift, annual_cost_savings, one_time_savings)`\n"
        "- `set_risks(risks)` — lista de `{'desc': str, 'probability': str, 'mitigation': str}`\n"
        "- `generate()` — imprime el business case completo\n\n"
        "generate() debe calcular:\n"
        "- ROI a 3 años: (total_benefits_3yr - investment) / investment * 100 (1 dec)\n"
        "- Payback: investment / (annual_revenue_uplift + annual_cost_savings) (1 dec) en años\n"
        "- NPV simplificado a 3 años con discount_rate=10%: "
        "sum(annual_benefit / (1.1)**yr for yr in 1..3) - investment (0 dec)\n\n"
        "El reporte incluye: header, Executive Summary, Investment, Benefits, "
        "Financial Summary (ROI, Payback, NPV), Risks, y Recommendation."
    ),
    hint          = "NPV: sum(benefit/(1.1**yr) for yr in range(1,4)) - investment. round() a entero.",
    initial_code  = (
        "class BusinessCase:\n"
        "    def __init__(self, title, owner, quarter):\n"
        "        self.title    = title\n"
        "        self.owner    = quarter\n"
        "        self.quarter  = quarter\n"
        "        self.owner    = owner\n"
        "        self.investment    = 0\n"
        "        self.breakdown     = {}\n"
        "        self.annual_rev    = 0\n"
        "        self.annual_cost   = 0\n"
        "        self.one_time      = 0\n"
        "        self.risks         = []\n\n"
        "    def set_investment(self, amount, breakdown):\n"
        "        pass\n\n"
        "    def set_benefits(self, annual_revenue_uplift, annual_cost_savings, one_time_savings):\n"
        "        pass\n\n"
        "    def set_risks(self, risks):\n"
        "        pass\n\n"
        "    def generate(self):\n"
        "        pass\n\n\n"
        "bc = BusinessCase(\n"
        "    title   = 'Platform Modernization Initiative',\n"
        "    owner   = 'Maria Chen, TPM',\n"
        "    quarter = 'Q3 2024',\n"
        ")\n"
        "bc.set_investment(\n"
        "    amount=280000,\n"
        "    breakdown={'Engineering': 200000, 'Infrastructure': 50000, 'Training': 30000},\n"
        ")\n"
        "bc.set_benefits(\n"
        "    annual_revenue_uplift=150000,\n"
        "    annual_cost_savings=80000,\n"
        "    one_time_savings=40000,\n"
        ")\n"
        "bc.set_risks([\n"
        "    {'desc': 'Migration complexity underestimated', 'probability': 'Medium', 'mitigation': 'Phased rollout'},\n"
        "    {'desc': 'Team ramp-up slower than planned',    'probability': 'Low',    'mitigation': 'External consultant'},\n"
        "])\n"
        "bc.generate()\n"
    ),
    expected_output = (
        "╔══════════════════════════════════════════════════════╗\n"
        "║  BUSINESS CASE: Platform Modernization Initiative   ║\n"
        "║  Owner: Maria Chen, TPM  |  Quarter: Q3 2024        ║\n"
        "╚══════════════════════════════════════════════════════╝\n"
        "\n"
        "EXECUTIVE SUMMARY:\n"
        "  Platform modernization to reduce costs and unlock revenue growth.\n"
        "  Total investment: $280,000  |  3-year horizon\n"
        "\n"
        "INVESTMENT BREAKDOWN:\n"
        "  Engineering:    $200,000\n"
        "  Infrastructure: $50,000\n"
        "  Training:       $30,000\n"
        "\n"
        "BENEFITS (annual):\n"
        "  Revenue uplift:  $150,000/yr\n"
        "  Cost savings:    $80,000/yr\n"
        "  One-time savings: $40,000\n"
        "\n"
        "FINANCIAL SUMMARY:\n"
        "  ROI (3yr):  138.6%\n"
        "  Payback:    1.2 years\n"
        "  NPV (3yr):  $307,395\n"
        "\n"
        "RISKS:\n"
        "  [Medium] Migration complexity underestimated\n"
        "           Mitigation: Phased rollout\n"
        "  [Low]    Team ramp-up slower than planned\n"
        "           Mitigation: External consultant\n"
        "\n"
        "RECOMMENDATION: APPROVE\n"
        "  Strong ROI of 138.6% and payback under 18 months."
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
BLOQUE3 = [L31, L32, L33, L34, L35, L36, L37, L38, L39, L40, L41, L42, L43, L44, L45]
