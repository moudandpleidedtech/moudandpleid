"""
_tpm_b10.py — TPM Mastery · BLOQUE 10 (L136–L150)
==================================================
Fase: tpm_ai_estrategia
Niveles: 136 a 150 (15 desafíos Python)
Boss: L150 — El Director Estratégico (FINAL BOSS)
"""
from __future__ import annotations

_BASE = dict(
    codex_id="tpm_mastery", sector_id=21, challenge_type="python",
    phase="tpm_ai_estrategia", is_free=False, strict_match=False,
    is_phase_boss=False, is_project=False,
)
_BASE_BOSS = {k: v for k, v in _BASE.items() if k not in ("is_phase_boss", "is_project")}

# ─────────────────────────────────────────────────────────────────────────────
L136 = dict(
    **_BASE, level_order=136, title="ML Project Lifecycle Planner", difficulty="medium",
    description=(
        "Los proyectos de ML tienen fases únicas que el TPM debe gestionar. "
        "Implementa `ml_lifecycle_planner(project_name, phases)` donde cada phase es "
        "`{'name': str, 'weeks': int, 'owner': str, 'dependencies': list[str], 'status': str}` "
        "(status: DONE/IN_PROGRESS/PENDING).\n\n"
        "Fases estándar ML en orden: Data Collection → Data Preparation → "
        "Model Training → Model Evaluation → Deployment → Monitoring.\n\n"
        "Imprime:\n"
        "`=== ML PROJECT LIFECYCLE: <project_name> ===`\n"
        "Por fase (orden original):\n"
        "`  [<STATUS>] <name> (<weeks>w) — Owner: <owner>`\n"
        "`    Deps: <dep1>, <dep2>` o `    Deps: none`\n\n"
        "Al final:\n"
        "`─────────────────────────────────`\n"
        "`Total Duration: Nw`\n"
        "`Progress: N/N phases complete`\n"
        "`Current Phase: <primer IN_PROGRESS>` o `No active phase`\n"
        "`Critical Path: <fases con deps no vacías, separadas por → >`"
    ),
    hint="Total = sum(weeks). Critical path = fases con dependencias, en orden original, unidas por ' → '.",
    initial_code=(
        "def ml_lifecycle_planner(project_name, phases):\n"
        "    pass\n\n"
        "ml_lifecycle_planner('Churn Prediction Model', [\n"
        "    {'name':'Data Collection',   'weeks':3, 'owner':'Data Eng',   'dependencies':[],                    'status':'DONE'},\n"
        "    {'name':'Data Preparation',  'weeks':2, 'owner':'Data Sci',   'dependencies':['Data Collection'],   'status':'DONE'},\n"
        "    {'name':'Model Training',    'weeks':4, 'owner':'ML Eng',     'dependencies':['Data Preparation'],  'status':'IN_PROGRESS'},\n"
        "    {'name':'Model Evaluation',  'weeks':2, 'owner':'ML Eng',     'dependencies':['Model Training'],    'status':'PENDING'},\n"
        "    {'name':'Deployment',        'weeks':2, 'owner':'Platform',   'dependencies':['Model Evaluation'],  'status':'PENDING'},\n"
        "    {'name':'Monitoring',        'weeks':1, 'owner':'SRE',        'dependencies':['Deployment'],        'status':'PENDING'},\n"
        "])\n"
    ),
    expected_output=(
        "=== ML PROJECT LIFECYCLE: Churn Prediction Model ===\n"
        "  [DONE] Data Collection (3w) — Owner: Data Eng\n"
        "    Deps: none\n"
        "  [DONE] Data Preparation (2w) — Owner: Data Sci\n"
        "    Deps: Data Collection\n"
        "  [IN_PROGRESS] Model Training (4w) — Owner: ML Eng\n"
        "    Deps: Data Preparation\n"
        "  [PENDING] Model Evaluation (2w) — Owner: ML Eng\n"
        "    Deps: Model Training\n"
        "  [PENDING] Deployment (2w) — Owner: Platform\n"
        "    Deps: Model Evaluation\n"
        "  [PENDING] Monitoring (1w) — Owner: SRE\n"
        "    Deps: Deployment\n"
        "─────────────────────────────────\n"
        "Total Duration: 14w\n"
        "Progress: 2/6 phases complete\n"
        "Current Phase: Model Training\n"
        "Critical Path: Data Preparation → Model Training → Model Evaluation → Deployment → Monitoring"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L137 = dict(
    **_BASE, level_order=137, title="AI Risk Assessor", difficulty="medium",
    description=(
        "Los proyectos de IA tienen riesgos únicos: sesgo, privacidad, explicabilidad. "
        "Implementa `ai_risk_assessor(project_name, risks)` donde cada risk es "
        "`{'category': str, 'description': str, 'likelihood': int, 'impact': int, 'mitigation': str}` "
        "(likelihood e impact 1-5).\n\n"
        "Risk score = likelihood × impact.\n\n"
        "Nivel: CRITICAL (≥20) / HIGH (≥12) / MEDIUM (≥6) / LOW (<6).\n\n"
        "Imprime:\n"
        "`=== AI RISK ASSESSMENT: <project_name> ===`\n"
        "Por risk (orden por risk_score desc):\n"
        "`[<LEVEL>] <category>`\n"
        "`  Risk: <description>`\n"
        "`  Score: N (L:<likelihood> × I:<impact>)`\n"
        "`  Mitigation: <mitigation>`\n\n"
        "Al final:\n"
        "`─────────────────────────────────`\n"
        "`CRITICAL risks: N | HIGH risks: N`\n"
        "`Overall AI Risk: UNACCEPTABLE (CRITICAL>0) / ELEVATED (HIGH>0) / MANAGEABLE`\n"
        "`Recommendation:`\n"
        "UNACCEPTABLE → Block deployment until CRITICAL risks mitigated\n"
        "ELEVATED → Implement mitigations before launch\n"
        "MANAGEABLE → Proceed with standard monitoring"
    ),
    hint="Sort by score desc. Nivel usa >= en orden CRITICAL→HIGH→MEDIUM→LOW.",
    initial_code=(
        "def ai_risk_assessor(project_name, risks):\n"
        "    pass\n\n"
        "ai_risk_assessor('Customer Scoring Model', [\n"
        "    {'category':'Bias',        'description':'Model discriminates by zip code',     'likelihood':4,'impact':5,'mitigation':'Fairness audit + demographic testing'},\n"
        "    {'category':'Privacy',     'description':'PII in training data',                'likelihood':3,'impact':4,'mitigation':'Data anonymization pipeline'},\n"
        "    {'category':'Accuracy',    'description':'Model accuracy drops in production',  'likelihood':3,'impact':3,'mitigation':'Shadow mode testing for 2 weeks'},\n"
        "    {'category':'Explainability','description':'Cannot explain decisions to users', 'likelihood':5,'impact':3,'mitigation':'Add SHAP values to output'},\n"
        "])\n"
    ),
    expected_output=(
        "=== AI RISK ASSESSMENT: Customer Scoring Model ===\n"
        "[CRITICAL] Bias\n"
        "  Risk: Model discriminates by zip code\n"
        "  Score: 20 (L:4 × I:5)\n"
        "  Mitigation: Fairness audit + demographic testing\n"
        "[HIGH] Privacy\n"
        "  Risk: PII in training data\n"
        "  Score: 12 (L:3 × I:4)\n"
        "  Mitigation: Data anonymization pipeline\n"
        "[HIGH] Explainability\n"
        "  Risk: Cannot explain decisions to users\n"
        "  Score: 15 (L:5 × I:3)\n"
        "  Mitigation: Add SHAP values to output\n"
        "[MEDIUM] Accuracy\n"
        "  Risk: Model accuracy drops in production\n"
        "  Score: 9 (L:3 × I:3)\n"
        "  Mitigation: Shadow mode testing for 2 weeks\n"
        "─────────────────────────────────\n"
        "CRITICAL risks: 1 | HIGH risks: 2\n"
        "Overall AI Risk: UNACCEPTABLE\n"
        "Recommendation: Block deployment until CRITICAL risks mitigated"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L138 = dict(
    **_BASE, level_order=138, title="Token Cost Governor", difficulty="medium",
    description=(
        "Gestionar costos de LLM es crítico en producción. "
        "Implementa `token_cost_governor(budget_usd, models)` donde cada model es "
        "`{'name': str, 'requests_per_day': int, 'avg_input_tokens': int, "
        "'avg_output_tokens': int, 'input_cost_per_1k': float, 'output_cost_per_1k': float}`.\n\n"
        "Daily cost per model = "
        "requests × (input_tokens/1000 × input_cost + output_tokens/1000 × output_cost).\n\n"
        "Imprime:\n"
        "`=== TOKEN COST GOVERNOR ===`\n"
        "`Daily Budget: $N`\n"
        "`─────────────────────────────────`\n"
        "Por model (orden por daily_cost desc):\n"
        "`  <name>`\n"
        "`    Requests/day: N | Tokens: Nin/Nout`\n"
        "`    Daily Cost: $N.2f`\n"
        "`    Monthly Est: $N.0f`\n\n"
        "Al final:\n"
        "`─────────────────────────────────`\n"
        "`Total Daily Cost: $N.2f`\n"
        "`Total Monthly Est: $N.0f`\n"
        "`Budget Status: WITHIN BUDGET / OVER BUDGET`\n"
        "`Most Expensive: <name>`"
    ),
    hint="daily_cost = requests * (avg_input/1000 * input_cost + avg_output/1000 * output_cost). Monthly = daily*30.",
    initial_code=(
        "def token_cost_governor(budget_usd, models):\n"
        "    pass\n\n"
        "token_cost_governor(budget_usd=50, models=[\n"
        "    {'name':'GPT-4o',        'requests_per_day':500,  'avg_input_tokens':800,  'avg_output_tokens':200, 'input_cost_per_1k':0.005,  'output_cost_per_1k':0.015},\n"
        "    {'name':'Claude Haiku',  'requests_per_day':2000, 'avg_input_tokens':500,  'avg_output_tokens':150, 'input_cost_per_1k':0.00025,'output_cost_per_1k':0.00125},\n"
        "    {'name':'Embedding Ada', 'requests_per_day':5000, 'avg_input_tokens':300,  'avg_output_tokens':0,   'input_cost_per_1k':0.0001, 'output_cost_per_1k':0.0},\n"
        "])\n"
    ),
    expected_output=(
        "=== TOKEN COST GOVERNOR ===\n"
        "Daily Budget: $50\n"
        "─────────────────────────────────\n"
        "  GPT-4o\n"
        "    Requests/day: 500 | Tokens: 800in/200out\n"
        "    Daily Cost: $3.50\n"
        "    Monthly Est: $105\n"
        "  Claude Haiku\n"
        "    Requests/day: 2000 | Tokens: 500in/150out\n"
        "    Daily Cost: $0.63\n"
        "    Monthly Est: $19\n"
        "  Embedding Ada\n"
        "    Requests/day: 5000 | Tokens: 300in/0out\n"
        "    Daily Cost: $0.15\n"
        "    Monthly Est: $5\n"
        "─────────────────────────────────\n"
        "Total Daily Cost: $4.27\n"
        "Total Monthly Est: $128\n"
        "Budget Status: WITHIN BUDGET\n"
        "Most Expensive: GPT-4o"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L139 = dict(
    **_BASE, level_order=139, title="Model Evaluation Framework", difficulty="medium",
    description=(
        "Evalúa modelos de ML en múltiples dimensiones para decidir cuál productizar. "
        "Implementa `model_evaluator(task, models)` donde cada model es "
        "`{'name': str, 'accuracy': float, 'latency_ms': int, 'cost_per_1k': float, "
        "'explainability': int, 'fairness_score': float}` "
        "(explainability 1-10, fairness 0.0-1.0).\n\n"
        "Composite score = accuracy*0.3 + (1 - latency_ms/1000)*0.2 + "
        "(1 - cost_per_1k)*0.2 + explainability/10*0.15 + fairness_score*0.15\n"
        "Redondea a 3 decimales.\n\n"
        "Imprime:\n"
        "`=== MODEL EVALUATION: <task> ===`\n"
        "Por model (orden por composite score desc):\n"
        "`  <rank>. <name>`\n"
        "`     Accuracy: N% | Latency: Nms | Cost: $N.3f/1k`\n"
        "`     Explainability: N/10 | Fairness: N.2f`\n"
        "`     Composite Score: N.3f`\n\n"
        "Al final:\n"
        "`─────────────────────────────────`\n"
        "`RECOMMENDED: <name> (score: N.3f)`"
    ),
    hint="composite = a*0.3 + (1-lat/1000)*0.2 + (1-cost)*0.2 + expl/10*0.15 + fair*0.15. round(x,3).",
    initial_code=(
        "def model_evaluator(task, models):\n"
        "    pass\n\n"
        "model_evaluator('Sentiment Classification', [\n"
        "    {'name':'BERT-large',  'accuracy':0.94, 'latency_ms':120, 'cost_per_1k':0.02, 'explainability':5, 'fairness_score':0.88},\n"
        "    {'name':'DistilBERT',  'accuracy':0.91, 'latency_ms':45,  'cost_per_1k':0.008,'explainability':6, 'fairness_score':0.85},\n"
        "    {'name':'GPT-4o-mini', 'accuracy':0.93, 'latency_ms':800, 'cost_per_1k':0.015,'explainability':4, 'fairness_score':0.90},\n"
        "])\n"
    ),
    expected_output=(
        "=== MODEL EVALUATION: Sentiment Classification ===\n"
        "  1. DistilBERT\n"
        "     Accuracy: 91% | Latency: 45ms | Cost: $0.008/1k\n"
        "     Explainability: 6/10 | Fairness: 0.85\n"
        "     Composite Score: 0.773\n"
        "  2. BERT-large\n"
        "     Accuracy: 94% | Latency: 120ms | Cost: $0.020/1k\n"
        "     Explainability: 5/10 | Fairness: 0.88\n"
        "     Composite Score: 0.750\n"
        "  3. GPT-4o-mini\n"
        "     Accuracy: 93% | Latency: 800ms | Cost: $0.015/1k\n"
        "     Explainability: 4/10 | Fairness: 0.90\n"
        "     Composite Score: 0.580\n"
        "─────────────────────────────────\n"
        "RECOMMENDED: DistilBERT (score: 0.773)"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L140 = dict(
    **_BASE, level_order=140, title="Platform Adoption Metrics", difficulty="medium",
    description=(
        "Mide la adopción de una plataforma de IA interna por equipos. "
        "Implementa `platform_adoption(platform_name, teams)` donde cada team es "
        "`{'name': str, 'invited': int, 'activated': int, 'weekly_active': int, 'api_calls_week': int}`.\n\n"
        "Métricas:\n"
        "- activation_rate = activated/invited*100\n"
        "- retention_rate = weekly_active/activated*100 (si activated>0 else 0)\n"
        "- avg_api_calls = api_calls_week/weekly_active (si weekly_active>0 else 0)\n\n"
        "Imprime:\n"
        "`=== PLATFORM ADOPTION: <platform_name> ===`\n"
        "Por team (orden por activation_rate desc):\n"
        "`  <name>`\n"
        "`    Activation: N% | Retention: N% | Avg API calls: N`\n"
        "`    Health: CHAMPION (act≥80% AND ret≥70%) / GROWING (act≥50%) / STRUGGLING (<50%)`\n\n"
        "Al final:\n"
        "`─────────────────────────────────`\n"
        "`Total Invited: N | Total Activated: N (N%)`\n"
        "`Total Weekly Active: N`\n"
        "`Platform Health: HEALTHY (≥2 CHAMPION) / GROWING / AT RISK`"
    ),
    hint="Todos los rates son int(). avg_api_calls también int(). HEALTHY si len(champions)>=2.",
    initial_code=(
        "def platform_adoption(platform_name, teams):\n"
        "    pass\n\n"
        "platform_adoption('DAKI AI Platform', [\n"
        "    {'name': 'Engineering',  'invited': 80,  'activated': 72, 'weekly_active': 55, 'api_calls_week': 2200},\n"
        "    {'name': 'Data Science', 'invited': 20,  'activated': 19, 'weekly_active': 16, 'api_calls_week': 4800},\n"
        "    {'name': 'Product',      'invited': 30,  'activated': 18, 'weekly_active': 10, 'api_calls_week': 300},\n"
        "    {'name': 'Support',      'invited': 50,  'activated': 15, 'weekly_active': 5,  'api_calls_week': 100},\n"
        "])\n"
    ),
    expected_output=(
        "=== PLATFORM ADOPTION: DAKI AI Platform ===\n"
        "  Data Science\n"
        "    Activation: 95% | Retention: 84% | Avg API calls: 300\n"
        "    Health: CHAMPION\n"
        "  Engineering\n"
        "    Activation: 90% | Retention: 76% | Avg API calls: 40\n"
        "    Health: CHAMPION\n"
        "  Product\n"
        "    Activation: 60% | Retention: 55% | Avg API calls: 30\n"
        "    Health: GROWING\n"
        "  Support\n"
        "    Activation: 30% | Retention: 33% | Avg API calls: 20\n"
        "    Health: STRUGGLING\n"
        "─────────────────────────────────\n"
        "Total Invited: 180 | Total Activated: 124 (68%)\n"
        "Total Weekly Active: 86\n"
        "Platform Health: HEALTHY"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L141 = dict(
    **_BASE, level_order=141, title="Developer Experience Scorer", difficulty="medium",
    description=(
        "El Developer Experience (DevEx) determina la velocidad y satisfacción del equipo. "
        "Implementa `devex_scorer(team_name, surveys)` donde cada survey es "
        "`{'engineer': str, 'flow_state': int, 'feedback_loops': int, 'cognitive_load': int}` "
        "(escala 1-10, donde 10 es mejor excepto cognitive_load donde 10=peor).\n\n"
        "DevEx score por ingeniero = (flow_state + feedback_loops + (10 - cognitive_load)) / 3\n"
        "Redondea a 1 decimal.\n\n"
        "Imprime:\n"
        "`=== DEVELOPER EXPERIENCE: <team_name> ===`\n"
        "Por engineer (orden por devex_score desc):\n"
        "`  <engineer>: N.N/10`\n"
        "`    Flow: N | Feedback: N | Cognitive Load: N (inverted: N)`\n\n"
        "Al final:\n"
        "`─────────────────────────────`\n"
        "`Team DevEx: N.N/10`\n"
        "`Top performer: <name>`\n"
        "`Biggest drag: <name>` (menor score)\n"
        "`Status: EXCELLENT (≥8) / GOOD (≥6.5) / NEEDS IMPROVEMENT (<6.5)`\n"
        "`Focus area: <Flow State/Feedback Loops/Cognitive Load>` (el de menor promedio del equipo; "
        "para cognitive_load compara el promedio invertido)"
    ),
    hint="team_devex = round(sum(scores)/len(surveys), 1). Focus area = la dimensión (como promedio del equipo) con menor valor.",
    initial_code=(
        "def devex_scorer(team_name, surveys):\n"
        "    pass\n\n"
        "devex_scorer('Platform Team', [\n"
        "    {'engineer': 'Alice',   'flow_state': 8, 'feedback_loops': 7, 'cognitive_load': 4},\n"
        "    {'engineer': 'Bob',     'flow_state': 6, 'feedback_loops': 5, 'cognitive_load': 8},\n"
        "    {'engineer': 'Carlos',  'flow_state': 7, 'feedback_loops': 8, 'cognitive_load': 5},\n"
        "    {'engineer': 'Diana',   'flow_state': 5, 'feedback_loops': 6, 'cognitive_load': 7},\n"
        "])\n"
    ),
    expected_output=(
        "=== DEVELOPER EXPERIENCE: Platform Team ===\n"
        "  Alice: 7.7/10\n"
        "    Flow: 8 | Feedback: 7 | Cognitive Load: 4 (inverted: 6)\n"
        "  Carlos: 7.3/10\n"
        "    Flow: 7 | Feedback: 8 | Cognitive Load: 5 (inverted: 5)\n"
        "  Diana: 6.0/10\n"
        "    Flow: 5 | Feedback: 6 | Cognitive Load: 7 (inverted: 3)\n"
        "  Bob: 5.7/10\n"
        "    Flow: 6 | Feedback: 5 | Cognitive Load: 8 (inverted: 2)\n"
        "─────────────────────────────\n"
        "Team DevEx: 6.7/10\n"
        "Top performer: Alice\n"
        "Biggest drag: Bob\n"
        "Status: GOOD\n"
        "Focus area: Cognitive Load"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L142 = dict(
    **_BASE, level_order=142, title="AI Feature Prioritizer", difficulty="medium",
    description=(
        "Prioriza features de IA balanceando impacto de negocio, factibilidad técnica y riesgos. "
        "Implementa `ai_feature_prioritizer(features)` donde cada feature es "
        "`{'name': str, 'business_impact': int, 'technical_feasibility': int, "
        "'data_readiness': int, 'regulatory_risk': int}` (cada uno 1-10; "
        "regulatory_risk: 10=más riesgoso).\n\n"
        "AI Priority Score = (business_impact*0.35 + technical_feasibility*0.25 + "
        "data_readiness*0.25 + (10-regulatory_risk)*0.15)\n"
        "Redondea a 2 decimales.\n\n"
        "Imprime:\n"
        "`=== AI FEATURE PRIORITIZATION ===`\n"
        "Por feature (orden por score desc):\n"
        "`N. <name>`\n"
        "`   Business: N | Feasibility: N | Data: N | Reg Risk: N`\n"
        "`   AI Priority Score: N.2f`\n"
        "`   Recommendation: FAST TRACK (≥7.5) / PROCEED (≥6.0) / REVIEW (<6.0)`\n\n"
        "Al final:\n"
        "`─────────────────────────`\n"
        "`FAST TRACK: N features`\n"
        "`PROCEED: N features`\n"
        "`REVIEW: N features`"
    ),
    hint="score = bi*0.35 + tf*0.25 + dr*0.25 + (10-rr)*0.15. round(x, 2).",
    initial_code=(
        "def ai_feature_prioritizer(features):\n"
        "    pass\n\n"
        "ai_feature_prioritizer([\n"
        "    {'name':'Smart search',      'business_impact':9,'technical_feasibility':8,'data_readiness':9,'regulatory_risk':2},\n"
        "    {'name':'AI credit scoring', 'business_impact':9,'technical_feasibility':7,'data_readiness':8,'regulatory_risk':9},\n"
        "    {'name':'Churn prediction',  'business_impact':8,'technical_feasibility':9,'data_readiness':7,'regulatory_risk':3},\n"
        "    {'name':'Face recognition',  'business_impact':6,'technical_feasibility':8,'data_readiness':6,'regulatory_risk':10},\n"
        "])\n"
    ),
    expected_output=(
        "=== AI FEATURE PRIORITIZATION ===\n"
        "1. Smart search\n"
        "   Business: 9 | Feasibility: 8 | Data: 9 | Reg Risk: 2\n"
        "   AI Priority Score: 8.45\n"
        "   Recommendation: FAST TRACK\n"
        "2. Churn prediction\n"
        "   Business: 8 | Feasibility: 9 | Data: 7 | Reg Risk: 3\n"
        "   AI Priority Score: 7.85\n"
        "   Recommendation: FAST TRACK\n"
        "3. AI credit scoring\n"
        "   Business: 9 | Feasibility: 7 | Data: 8 | Reg Risk: 9\n"
        "   AI Priority Score: 7.0\n"
        "   Recommendation: PROCEED\n"
        "4. Face recognition\n"
        "   Business: 6 | Feasibility: 8 | Data: 6 | Reg Risk: 10\n"
        "   AI Priority Score: 5.6\n"
        "   Recommendation: REVIEW\n"
        "─────────────────────────\n"
        "FAST TRACK: 2 features\n"
        "PROCEED: 1 features\n"
        "REVIEW: 1 features"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L143 = dict(
    **_BASE, level_order=143, title="Data Quality Checker", difficulty="medium",
    description=(
        "La calidad de datos determina la calidad del modelo. "
        "Implementa `data_quality_checker(dataset_name, checks)` donde cada check es "
        "`{'dimension': str, 'records_checked': int, 'issues_found': int, 'threshold_pct': float}`.\n\n"
        "Quality score por dimensión = (1 - issues/records)*100. Redondea a 1 decimal.\n"
        "Pasa si quality_score >= (100 - threshold_pct).\n\n"
        "Imprime:\n"
        "`=== DATA QUALITY REPORT: <dataset_name> ===`\n"
        "Por dimensión (orden original):\n"
        "`  <dimension>`\n"
        "`    Records: N | Issues: N | Quality: N.1f% | Threshold: N.1f%`\n"
        "`    Status: PASS / FAIL`\n\n"
        "Al final:\n"
        "`─────────────────────────────────`\n"
        "`Dimensions Passed: N / N`\n"
        "`Overall Quality Score: N.1f%`  (promedio de quality scores)\n"
        "`ML Readiness: READY (all pass) / NOT READY`\n"
        "`Failed dimensions: <lista separada por ', '>` o `None`"
    ),
    hint="quality_score = round((1 - issues/records)*100, 1). Pass si quality_score >= 100 - threshold_pct.",
    initial_code=(
        "def data_quality_checker(dataset_name, checks):\n"
        "    pass\n\n"
        "data_quality_checker('Customer Dataset v2', [\n"
        "    {'dimension':'Completeness', 'records_checked':10000,'issues_found':150, 'threshold_pct':2.0},\n"
        "    {'dimension':'Accuracy',     'records_checked':10000,'issues_found':800, 'threshold_pct':5.0},\n"
        "    {'dimension':'Consistency',  'records_checked':10000,'issues_found':50,  'threshold_pct':1.0},\n"
        "    {'dimension':'Timeliness',   'records_checked':10000,'issues_found':600, 'threshold_pct':3.0},\n"
        "])\n"
    ),
    expected_output=(
        "=== DATA QUALITY REPORT: Customer Dataset v2 ===\n"
        "  Completeness\n"
        "    Records: 10000 | Issues: 150 | Quality: 98.5% | Threshold: 2.0%\n"
        "    Status: PASS\n"
        "  Accuracy\n"
        "    Records: 10000 | Issues: 800 | Quality: 92.0% | Threshold: 5.0%\n"
        "    Status: PASS\n"
        "  Consistency\n"
        "    Records: 10000 | Issues: 50 | Quality: 99.5% | Threshold: 1.0%\n"
        "    Status: PASS\n"
        "  Timeliness\n"
        "    Records: 10000 | Issues: 600 | Quality: 94.0% | Threshold: 3.0%\n"
        "    Status: FAIL\n"
        "─────────────────────────────────\n"
        "Dimensions Passed: 3 / 4\n"
        "Overall Quality Score: 96.0%\n"
        "ML Readiness: NOT READY\n"
        "Failed dimensions: Timeliness"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L144 = dict(
    **_BASE, level_order=144, title="MLOps Pipeline Analyzer", difficulty="medium",
    description=(
        "Un pipeline de MLOps bien diseñado automatiza el ciclo de vida del modelo. "
        "Implementa `mlops_analyzer(pipeline_name, stages)` donde cada stage es "
        "`{'name': str, 'automated': bool, 'avg_duration_min': int, 'failure_rate_pct': float, 'sla_min': int}`.\n\n"
        "Imprime:\n"
        "`=== MLOPS PIPELINE: <pipeline_name> ===`\n"
        "Por stage (orden original):\n"
        "`  [AUTO/MANUAL] <name>`\n"
        "`    Duration: Nmin | SLA: Nmin | Failure: N.1f%`\n"
        "`    SLA Status: COMPLIANT / BREACH`  (breach si avg_duration > sla)\n\n"
        "Al final:\n"
        "`─────────────────────────────────`\n"
        "`Automation Rate: N%`  (automated/total*100 int)\n"
        "`Total Pipeline Duration: Nmin`\n"
        "`SLA Breaches: N stages`\n"
        "`Avg Failure Rate: N.1f%`\n"
        "`Pipeline Maturity: ELITE (auto≥80% and breaches=0) / ADVANCED (auto≥60%) / BASIC`"
    ),
    hint="Automation rate = int(auto_count/total*100). avg_failure = round(sum(rates)/len, 1).",
    initial_code=(
        "def mlops_analyzer(pipeline_name, stages):\n"
        "    pass\n\n"
        "mlops_analyzer('Production ML Pipeline', [\n"
        "    {'name':'Data Ingestion',   'automated':True,  'avg_duration_min':15, 'failure_rate_pct':0.5, 'sla_min':20},\n"
        "    {'name':'Feature Eng',      'automated':True,  'avg_duration_min':45, 'failure_rate_pct':1.2, 'sla_min':60},\n"
        "    {'name':'Model Training',   'automated':True,  'avg_duration_min':120,'failure_rate_pct':3.5, 'sla_min':90},\n"
        "    {'name':'Model Validation', 'automated':False, 'avg_duration_min':60, 'failure_rate_pct':0.0, 'sla_min':120},\n"
        "    {'name':'Deployment',       'automated':True,  'avg_duration_min':10, 'failure_rate_pct':0.8, 'sla_min':15},\n"
        "])\n"
    ),
    expected_output=(
        "=== MLOPS PIPELINE: Production ML Pipeline ===\n"
        "  [AUTO] Data Ingestion\n"
        "    Duration: 15min | SLA: 20min | Failure: 0.5%\n"
        "    SLA Status: COMPLIANT\n"
        "  [AUTO] Feature Eng\n"
        "    Duration: 45min | SLA: 60min | Failure: 1.2%\n"
        "    SLA Status: COMPLIANT\n"
        "  [AUTO] Model Training\n"
        "    Duration: 120min | SLA: 90min | Failure: 3.5%\n"
        "    SLA Status: BREACH\n"
        "  [MANUAL] Model Validation\n"
        "    Duration: 60min | SLA: 120min | Failure: 0.0%\n"
        "    SLA Status: COMPLIANT\n"
        "  [AUTO] Deployment\n"
        "    Duration: 10min | SLA: 15min | Failure: 0.8%\n"
        "    SLA Status: COMPLIANT\n"
        "─────────────────────────────────\n"
        "Automation Rate: 80%\n"
        "Total Pipeline Duration: 250min\n"
        "SLA Breaches: 1 stages\n"
        "Avg Failure Rate: 1.2%\n"
        "Pipeline Maturity: ADVANCED"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L145 = dict(
    **_BASE, level_order=145, title="AI Governance Checklist", difficulty="medium",
    description=(
        "La gobernanza de IA requiere verificar múltiples dimensiones antes del despliegue. "
        "Implementa `ai_governance_check(model_name, checklist)` donde cada item es "
        "`{'pillar': str, 'check': str, 'status': str, 'required': bool}` "
        "(status: PASS/FAIL/N_A, required: True/False).\n\n"
        "Imprime:\n"
        "`=== AI GOVERNANCE CHECKLIST: <model_name> ===`\n"
        "Agrupa por pillar (orden de primera aparición):\n"
        "`[<pillar>]`\n"
        "Por item dentro del grupo (orden original):\n"
        "`  [PASS/FAIL/N/A] <check>`\n"
        "(N_A status → mostrar como N/A)\n"
        "(si required=True y status=FAIL → añade ` ← REQUIRED`)\n\n"
        "Al final:\n"
        "`─────────────────────────────────`\n"
        "`Passed: N | Failed: N | N/A: N`\n"
        "`Required failures: N`\n"
        "`Governance Score: N%`  (passed/total_non_na*100 int, donde total_non_na excluye N_A)\n"
        "`CLEARANCE: APPROVED (required_failures=0 and score≥75%) / CONDITIONAL (score≥60%) / BLOCKED`"
    ),
    hint="total_non_na = len([i for i in checklist if i['status'] != 'N_A']). Score = passed/total_non_na*100.",
    initial_code=(
        "def ai_governance_check(model_name, checklist):\n"
        "    pass\n\n"
        "ai_governance_check('Credit Risk Model v3', [\n"
        "    {'pillar':'Fairness',        'check':'Demographic parity tested',    'status':'PASS', 'required':True},\n"
        "    {'pillar':'Fairness',        'check':'Protected attributes excluded', 'status':'PASS', 'required':True},\n"
        "    {'pillar':'Transparency',    'check':'Model card published',          'status':'FAIL', 'required':True},\n"
        "    {'pillar':'Transparency',    'check':'SHAP explanations available',   'status':'PASS', 'required':False},\n"
        "    {'pillar':'Privacy',         'check':'PII removed from training',     'status':'PASS', 'required':True},\n"
        "    {'pillar':'Privacy',         'check':'GDPR compliance reviewed',      'status':'FAIL', 'required':True},\n"
        "    {'pillar':'Reliability',     'check':'Stress testing complete',       'status':'PASS', 'required':False},\n"
        "    {'pillar':'Reliability',     'check':'Fallback logic defined',        'status':'N_A',  'required':False},\n"
        "])\n"
    ),
    expected_output=(
        "=== AI GOVERNANCE CHECKLIST: Credit Risk Model v3 ===\n"
        "[Fairness]\n"
        "  [PASS] Demographic parity tested\n"
        "  [PASS] Protected attributes excluded\n"
        "[Transparency]\n"
        "  [FAIL] Model card published ← REQUIRED\n"
        "  [PASS] SHAP explanations available\n"
        "[Privacy]\n"
        "  [PASS] PII removed from training\n"
        "  [FAIL] GDPR compliance reviewed ← REQUIRED\n"
        "[Reliability]\n"
        "  [PASS] Stress testing complete\n"
        "  [N/A] Fallback logic defined\n"
        "─────────────────────────────────\n"
        "Passed: 5 | Failed: 2 | N/A: 1\n"
        "Required failures: 2\n"
        "Governance Score: 71%\n"
        "CLEARANCE: CONDITIONAL"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L146 = dict(
    **_BASE, level_order=146, title="Annual Planning Synthesizer", difficulty="hard",
    description=(
        "El plan anual consolida OKRs, iniciativas, headcount e inversión. "
        "Implementa `annual_planner(year, teams)` donde cada team es "
        "`{'name': str, 'okrs': list[str], 'headcount': int, 'budget_k': int, 'initiatives': list[str]}`.\n\n"
        "Imprime:\n"
        "`=== ANNUAL PLAN: <year> ===`\n"
        "Por team (orden original):\n"
        "`[<name>] HC:<headcount> | Budget: $<budget_k>K`\n"
        "`  OKRs:`\n"
        "Por OKR (con índice 1..N):\n"
        "`    <N>. <okr>`\n"
        "`  Initiatives:`\n"
        "Por initiative (con índice 1..N):\n"
        "`    <N>. <initiative>`\n\n"
        "Al final:\n"
        "`─────────────────────────────────`\n"
        "`Total Headcount: N`\n"
        "`Total Budget: $NK`\n"
        "`Total OKRs: N`\n"
        "`Total Initiatives: N`\n"
        "`Planning Status: COMPLETE`"
    ),
    hint="Total budget = sum(budget_k). Usa enumerate(list, 1) para los índices.",
    initial_code=(
        "def annual_planner(year, teams):\n"
        "    pass\n\n"
        "annual_planner(2025, [\n"
        "    {'name': 'Platform',\n"
        "     'headcount': 12, 'budget_k': 800,\n"
        "     'okrs': ['99.9% uptime', 'Deploy daily'],\n"
        "     'initiatives': ['K8s migration', 'Observability v2']},\n"
        "    {'name': 'Data',\n"
        "     'headcount': 8, 'budget_k': 500,\n"
        "     'okrs': ['Real-time pipeline', 'Data quality ≥95%'],\n"
        "     'initiatives': ['Lakehouse migration', 'ML feature store']},\n"
        "])\n"
    ),
    expected_output=(
        "=== ANNUAL PLAN: 2025 ===\n"
        "[Platform] HC:12 | Budget: $800K\n"
        "  OKRs:\n"
        "    1. 99.9% uptime\n"
        "    2. Deploy daily\n"
        "  Initiatives:\n"
        "    1. K8s migration\n"
        "    2. Observability v2\n"
        "[Data] HC:8 | Budget: $500K\n"
        "  OKRs:\n"
        "    1. Real-time pipeline\n"
        "    2. Data quality ≥95%\n"
        "  Initiatives:\n"
        "    1. Lakehouse migration\n"
        "    2. ML feature store\n"
        "─────────────────────────────────\n"
        "Total Headcount: 20\n"
        "Total Budget: $1300K\n"
        "Total OKRs: 4\n"
        "Total Initiatives: 4\n"
        "Planning Status: COMPLETE"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L147 = dict(
    **_BASE, level_order=147, title="Strategic Roadmap Validator", difficulty="hard",
    description=(
        "Valida que un roadmap estratégico sea coherente, realista y alineado. "
        "Implementa `roadmap_validator(roadmap_name, quarters, capacity_per_quarter)` "
        "donde cada quarter es "
        "`{'name': str, 'items': list[{'name': str, 'effort': int, 'type': str}]}` "
        "(type: FEATURE/TECH_DEBT/INFRA).\n\n"
        "Imprime:\n"
        "`=== ROADMAP VALIDATION: <roadmap_name> ===`\n"
        "Por quarter (orden original):\n"
        "`[<name>] Capacity: N`\n"
        "Por item (orden original):\n"
        "`  • <name> (<type>, effort: N)`\n"
        "`Total effort: N / N`\n"
        "`Status: FEASIBLE / OVERLOADED (total > capacity) / UNDERUTILIZED (total < capacity*0.7)`\n\n"
        "Al final:\n"
        "`─────────────────────────────────`\n"
        "`Quarters FEASIBLE: N`\n"
        "`Quarters OVERLOADED: N`\n"
        "`FEATURE effort: N% | TECH_DEBT effort: N% | INFRA effort: N%`\n"
        "(porcentajes sobre el total de todos los items)\n"
        "`Balance: HEALTHY (FEATURE 40-60%, TECH_DEBT 20-35%, INFRA 10-25%) / IMBALANCED`\n"
        "`Roadmap Status: APPROVED (0 overloaded) / NEEDS REVISION`"
    ),
    hint="type_pct = int(type_total/grand_total*100). Balance: verifica rangos para los 3 tipos.",
    initial_code=(
        "def roadmap_validator(roadmap_name, quarters, capacity_per_quarter):\n"
        "    pass\n\n"
        "roadmap_validator('2025 Platform Roadmap', [\n"
        "    {'name':'Q1', 'items':[\n"
        "        {'name':'Auth v2',        'effort':8,  'type':'FEATURE'},\n"
        "        {'name':'DB cleanup',     'effort':5,  'type':'TECH_DEBT'},\n"
        "        {'name':'K8s upgrade',    'effort':4,  'type':'INFRA'},\n"
        "    ]},\n"
        "    {'name':'Q2', 'items':[\n"
        "        {'name':'Dashboard v3',   'effort':10, 'type':'FEATURE'},\n"
        "        {'name':'CI/CD upgrade',  'effort':4,  'type':'INFRA'},\n"
        "        {'name':'Cache refactor', 'effort':6,  'type':'TECH_DEBT'},\n"
        "    ]},\n"
        "    {'name':'Q3', 'items':[\n"
        "        {'name':'Mobile app',     'effort':12, 'type':'FEATURE'},\n"
        "        {'name':'Observability',  'effort':5,  'type':'INFRA'},\n"
        "    ]},\n"
        "], capacity_per_quarter=20)\n"
    ),
    expected_output=(
        "=== ROADMAP VALIDATION: 2025 Platform Roadmap ===\n"
        "[Q1] Capacity: 20\n"
        "  • Auth v2 (FEATURE, effort: 8)\n"
        "  • DB cleanup (TECH_DEBT, effort: 5)\n"
        "  • K8s upgrade (INFRA, effort: 4)\n"
        "Total effort: 17 / 20\n"
        "Status: FEASIBLE\n"
        "[Q2] Capacity: 20\n"
        "  • Dashboard v3 (FEATURE, effort: 10)\n"
        "  • CI/CD upgrade (INFRA, effort: 4)\n"
        "  • Cache refactor (TECH_DEBT, effort: 6)\n"
        "Total effort: 20 / 20\n"
        "Status: FEASIBLE\n"
        "[Q3] Capacity: 20\n"
        "  • Mobile app (FEATURE, effort: 12)\n"
        "  • Observability (INFRA, effort: 5)\n"
        "Total effort: 17 / 20\n"
        "Status: FEASIBLE\n"
        "─────────────────────────────────\n"
        "Quarters FEASIBLE: 3\n"
        "Quarters OVERLOADED: 0\n"
        "FEATURE effort: 56% | TECH_DEBT effort: 20% | INFRA effort: 24%\n"
        "Balance: IMBALANCED\n"
        "Roadmap Status: APPROVED"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L148 = dict(
    **_BASE, level_order=148, title="TPM Maturity Self-Assessment", difficulty="hard",
    description=(
        "Un TPM maduro puede evaluarse en múltiples dominios. "
        "Implementa `tpm_maturity(tpm_name, domains)` donde cada domain es "
        "`{'domain': str, 'score': int, 'evidence': str}` (score 1-5).\n\n"
        "Nivel por score: 5=MASTERY, 4=PROFICIENT, 3=DEVELOPING, 2=AWARENESS, 1=NOVICE\n\n"
        "Imprime:\n"
        "`=== TPM MATURITY ASSESSMENT: <tpm_name> ===`\n"
        "Por domain (orden original):\n"
        "`  <domain>`\n"
        "`    Score: N/5 (<nivel>)`\n"
        "`    Evidence: <evidence>`\n\n"
        "Al final:\n"
        "`─────────────────────────────────`\n"
        "`Overall Maturity: N.N/5.0`\n"
        "`Level: <nivel>` (nivel del score promedio, trunca a int)\n"
        "`Strengths (score≥4):`\n"
        "Por domain (orden score desc):\n"
        "`  ★ <domain> (N/5)`\n"
        "`Growth Areas (score≤2):`\n"
        "Por domain (orden score asc):\n"
        "`  △ <domain> (N/5)`\n"
        "`Career Recommendation:`\n"
        "avg≥4.5 → Ready for Director-level TPM\n"
        "avg≥3.5 → Ready for Senior TPM\n"
        "avg≥2.5 → Developing TPM\n"
        "avg<2.5 → Focus on fundamentals"
    ),
    hint="overall = round(sum(scores)/len, 1). Level usa int(overall) para el lookup.",
    initial_code=(
        "def tpm_maturity(tpm_name, domains):\n"
        "    pass\n\n"
        "tpm_maturity('Roberto Salinas', [\n"
        "    {'domain':'Technical Credibility',  'score':4, 'evidence':'Led 3 platform migrations'},\n"
        "    {'domain':'Executive Communication','score':4, 'evidence':'QBR presenter for 2 years'},\n"
        "    {'domain':'People Leadership',      'score':3, 'evidence':'Managed 2 interns'},\n"
        "    {'domain':'Business Acumen',        'score':3, 'evidence':'Drove 2 cost reduction projects'},\n"
        "    {'domain':'Negotiation',            'score':2, 'evidence':'Limited formal negotiation exp'},\n"
        "    {'domain':'Change Management',      'score':3, 'evidence':'Led 1 org redesign'},\n"
        "    {'domain':'Decision Frameworks',    'score':5, 'evidence':'Certified in RICE, OKR, ADKAR'},\n"
        "])\n"
    ),
    expected_output=(
        "=== TPM MATURITY ASSESSMENT: Roberto Salinas ===\n"
        "  Technical Credibility\n"
        "    Score: 4/5 (PROFICIENT)\n"
        "    Evidence: Led 3 platform migrations\n"
        "  Executive Communication\n"
        "    Score: 4/5 (PROFICIENT)\n"
        "    Evidence: QBR presenter for 2 years\n"
        "  People Leadership\n"
        "    Score: 3/5 (DEVELOPING)\n"
        "    Evidence: Managed 2 interns\n"
        "  Business Acumen\n"
        "    Score: 3/5 (DEVELOPING)\n"
        "    Evidence: Drove 2 cost reduction projects\n"
        "  Negotiation\n"
        "    Score: 2/5 (AWARENESS)\n"
        "    Evidence: Limited formal negotiation exp\n"
        "  Change Management\n"
        "    Score: 3/5 (DEVELOPING)\n"
        "    Evidence: Led 1 org redesign\n"
        "  Decision Frameworks\n"
        "    Score: 5/5 (MASTERY)\n"
        "    Evidence: Certified in RICE, OKR, ADKAR\n"
        "─────────────────────────────────\n"
        "Overall Maturity: 3.4/5.0\n"
        "Level: DEVELOPING\n"
        "Strengths (score≥4):\n"
        "  ★ Decision Frameworks (5/5)\n"
        "  ★ Technical Credibility (4/5)\n"
        "  ★ Executive Communication (4/5)\n"
        "Growth Areas (score≤2):\n"
        "  △ Negotiation (2/5)\n"
        "Career Recommendation: Developing TPM"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L149 = dict(
    **_BASE, level_order=149, title="AI Cost ROI Calculator", difficulty="hard",
    description=(
        "Calcula el ROI real de una inversión en IA considerando todos los costos. "
        "Implementa `ai_roi_calculator(project_name, investment, benefits, costs)` donde:\n"
        "- investment: `{'engineering_months': int, 'monthly_rate': int, 'infra_setup': int}`\n"
        "- benefits: lista `{'name': str, 'monthly_value': int, 'start_month': int}`\n"
        "- costs: lista `{'name': str, 'monthly_cost': int}`\n"
        "Horizonte de análisis: 12 meses.\n\n"
        "Engineering cost = engineering_months * monthly_rate.\n"
        "Total investment = engineering_cost + infra_setup.\n"
        "Monthly net benefit = sum(monthly_value si month >= start_month) - sum(monthly_cost).\n"
        "Cumulative P&L por mes. ROI = (total_benefits_12 - total_costs_12) / total_investment * 100.\n\n"
        "Imprime:\n"
        "`=== AI ROI ANALYSIS: <project_name> ===`\n"
        "`Initial Investment: $N`\n"
        "`─────────────────────────────────────`\n"
        "Por mes 1..12:\n"
        "`  Month N: Net $N | Cumulative $N`\n\n"
        "Al final:\n"
        "`─────────────────────────────────────`\n"
        "`Total Benefits (12mo): $N`\n"
        "`Total Running Costs (12mo): $N`\n"
        "`ROI: N%`  (int)\n"
        "`Break-even: Month N` (primer mes donde cumulative >= 0) o `Not reached`\n"
        "`Verdict: STRONG ROI (≥100%) / POSITIVE ROI (≥0%) / NEGATIVE ROI`"
    ),
    hint="Cumulative inicia en -total_investment. Cada mes suma net_benefit. Break-even = primer mes cum>=0.",
    initial_code=(
        "def ai_roi_calculator(project_name, investment, benefits, costs):\n"
        "    pass\n\n"
        "ai_roi_calculator(\n"
        "    project_name='Customer Service AI',\n"
        "    investment={'engineering_months': 4, 'monthly_rate': 15000, 'infra_setup': 20000},\n"
        "    benefits=[\n"
        "        {'name': 'Support cost reduction', 'monthly_value': 18000, 'start_month': 3},\n"
        "        {'name': 'CSAT improvement',       'monthly_value': 5000,  'start_month': 5},\n"
        "    ],\n"
        "    costs=[\n"
        "        {'name': 'API costs',    'monthly_cost': 2000},\n"
        "        {'name': 'Maintenance',  'monthly_cost': 1500},\n"
        "    ]\n"
        ")\n"
    ),
    expected_output=(
        "=== AI ROI ANALYSIS: Customer Service AI ===\n"
        "Initial Investment: $80000\n"
        "─────────────────────────────────────\n"
        "  Month 1: Net $-3500 | Cumulative $-83500\n"
        "  Month 2: Net $-3500 | Cumulative $-87000\n"
        "  Month 3: Net $14500 | Cumulative $-72500\n"
        "  Month 4: Net $14500 | Cumulative $-58000\n"
        "  Month 5: Net $19500 | Cumulative $-38500\n"
        "  Month 6: Net $19500 | Cumulative $-19000\n"
        "  Month 7: Net $19500 | Cumulative $500\n"
        "  Month 8: Net $19500 | Cumulative $20000\n"
        "  Month 9: Net $19500 | Cumulative $39500\n"
        "  Month 10: Net $19500 | Cumulative $59000\n"
        "  Month 11: Net $19500 | Cumulative $78500\n"
        "  Month 12: Net $19500 | Cumulative $98000\n"
        "─────────────────────────────────────\n"
        "Total Benefits (12mo): $211000\n"
        "Total Running Costs (12mo): $42000\n"
        "ROI: 211%\n"
        "Break-even: Month 7\n"
        "Verdict: STRONG ROI"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
L150 = dict(
    **_BASE_BOSS, level_order=150, title="El Director Estratégico", difficulty="legendary",
    is_phase_boss=True, is_project=True,
    description=(
        "BOSS FINAL L150: Eres El Director Estratégico — el TPM completo. "
        "Has completado las 10 fases del programa. Demuestra todo lo aprendido.\n\n"
        "Implementa la clase `DirectorEstrategico` con:\n\n"
        "`__init__(self, name, company)` — almacena nombre y empresa.\n\n"
        "`plan(year, initiatives)` — initiatives: lista de strings. Imprime:\n"
        "`PLAN <year>: N initiatives`\n"
        "Por initiative (con índice):\n"
        "`  N. <initiative>`\n\n"
        "`assess_risk(risk_name, likelihood, impact)` — likelihood e impact 1-5. "
        "score = likelihood*impact. Imprime:\n"
        "`RISK [<nivel>]: <risk_name> (score: N)`\n"
        "(CRITICAL≥20, HIGH≥12, MEDIUM≥6, LOW<6)\n\n"
        "`negotiate(topic, our, their)` — Imprime:\n"
        "`NEGOTIATION: <topic> → Proposed: N`  (midpoint = (our+their)//2)\n\n"
        "`lead_change(change, readiness)` — readiness float 0-10. Imprime:\n"
        "`CHANGE: <change> | Readiness: N.N → <READY/AT RISK/NOT READY>`\n\n"
        "`decide(option_a, score_a, option_b, score_b)` — Imprime:\n"
        "`DECISION: <opción con mayor score> (score: N.N) over <opción perdedora>`\n\n"
        "`executive_report()` — Imprime:\n"
        "`╔══════════════════════════════════╗`\n"
        "`║    DIRECTOR ESTRATÉGICO REPORT   ║`\n"
        "`╠══════════════════════════════════╣`\n"
        "`║ TPM: <name>                      ║`\n"
        "`║ Company: <company>               ║`\n"
        "`║ Status: ALL SYSTEMS OPERATIONAL  ║`\n"
        "`║ Level: LEGENDARY TPM             ║`\n"
        "`╚══════════════════════════════════╝`"
    ),
    hint="Este es el boss final. Combina todas las fases. readiness: READY≥7, AT RISK≥5, NOT READY<5.",
    initial_code=(
        "class DirectorEstrategico:\n"
        "    def __init__(self, name, company):\n"
        "        pass\n"
        "    def plan(self, year, initiatives):\n"
        "        pass\n"
        "    def assess_risk(self, risk_name, likelihood, impact):\n"
        "        pass\n"
        "    def negotiate(self, topic, our, their):\n"
        "        pass\n"
        "    def lead_change(self, change, readiness):\n"
        "        pass\n"
        "    def decide(self, option_a, score_a, option_b, score_b):\n"
        "        pass\n"
        "    def executive_report(self):\n"
        "        pass\n\n"
        "de = DirectorEstrategico('Sofia Mendoza', 'DAKI Corp')\n"
        "de.plan(2025, ['AI Platform launch', 'Global expansion', 'DevEx transformation'])\n"
        "de.assess_risk('Data breach', likelihood=4, impact=5)\n"
        "de.negotiate('Engineering budget', our=500000, their=350000)\n"
        "de.lead_change('Remote-first policy', readiness=7.5)\n"
        "de.decide('Build internal tool', 8.2, 'Buy SaaS solution', 7.8)\n"
        "de.executive_report()\n"
    ),
    expected_output=(
        "PLAN 2025: 3 initiatives\n"
        "  1. AI Platform launch\n"
        "  2. Global expansion\n"
        "  3. DevEx transformation\n"
        "RISK [CRITICAL]: Data breach (score: 20)\n"
        "NEGOTIATION: Engineering budget → Proposed: $425000\n"
        "CHANGE: Remote-first policy | Readiness: 7.5 → READY\n"
        "DECISION: Build internal tool (score: 8.2) over Buy SaaS solution\n"
        "╔══════════════════════════════════╗\n"
        "║    DIRECTOR ESTRATÉGICO REPORT   ║\n"
        "╠══════════════════════════════════╣\n"
        "║ TPM: Sofia Mendoza               ║\n"
        "║ Company: DAKI Corp               ║\n"
        "║ Status: ALL SYSTEMS OPERATIONAL  ║\n"
        "║ Level: LEGENDARY TPM             ║\n"
        "╚══════════════════════════════════╝"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
BLOQUE10 = [L136, L137, L138, L139, L140, L141, L142, L143, L144, L145,
            L146, L147, L148, L149, L150]
