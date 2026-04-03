"""Bloque 3 — CI/CD & Infraestructura (L41–L60) — Python"""
from __future__ import annotations
import json

BLOQUE3 = [
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-041: YAML PIPELINE PARSER ]",
"description": (
    "Implementa `parse_pipeline(yaml_str: str) -> dict` que extraiga: "
    "`stages` (lista), `jobs_per_stage` (dict stage→count), `total_jobs` (int). "
    "El YAML simulado usa un dict Python como entrada."
),
"difficulty_tier": 1, "difficulty": "easy",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 41, "base_xp_reward": 170,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 200, "challenge_type": "python",
"phase": "cicd_infra", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["YAML", "CI_CD", "parsing", "pipeline"]),
"initial_code": (
    "def parse_pipeline(config: dict) -> dict:\n"
    "    # TODO: extrae del dict de config:\n"
    "    # 'stages'        → lista de nombres de stage (keys del dict 'pipeline')\n"
    "    # 'jobs_per_stage'→ dict {stage_name: len(jobs_list)}\n"
    "    # 'total_jobs'    → suma total de jobs\n"
    "    pass\n"
    "\n"
    "\n"
    "config = {\n"
    "    'pipeline': {\n"
    "        'build':    ['compile', 'lint', 'type-check'],\n"
    "        'test':     ['unit-tests', 'integration-tests', 'e2e-tests', 'coverage'],\n"
    "        'security': ['sast', 'dependency-audit'],\n"
    "        'deploy':   ['deploy-staging', 'smoke-tests', 'deploy-prod'],\n"
    "    }\n"
    "}\n"
    "result = parse_pipeline(config)\n"
    "print(f'Stages: {\", \".join(result[\"stages\"])}')\n"
    "for stage, count in result['jobs_per_stage'].items():\n"
    "    print(f'  {stage}: {count} jobs')\n"
    "print(f'Total jobs: {result[\"total_jobs\"]}')\n"
),
"expected_output": (
    "Stages: build, test, security, deploy\n"
    "  build: 3 jobs\n"
    "  test: 4 jobs\n"
    "  security: 2 jobs\n"
    "  deploy: 3 jobs\n"
    "Total jobs: 12"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "El pipeline es el corazón del CI. "
    "Si no lo entiendes, no puedes optimizarlo — ni debuggearlo cuando falla a las 2am."
),
"theory_content": (
    "## CI/CD Pipeline Anatomy\n\n"
    "Un pipeline típico tiene stages ordenados:\n\n"
    "```\nbuild → test → security → deploy\n```\n\n"
    "Cada stage tiene jobs que pueden correr en paralelo. "
    "Si un stage falla, los siguientes se cancelan.\n\n"
    "**GitHub Actions, GitLab CI, Jenkins** — todos siguen esta estructura base."
),
"pedagogical_objective": "Parsear la estructura de un pipeline CI/CD extrayendo stages y conteo de jobs.",
"syntax_hint": "Itera `config['pipeline'].items()` para obtener stage y su lista de jobs.",
"hints_json": json.dumps([
    "stages = list(config['pipeline'].keys())",
    "jobs_per_stage = {stage: len(jobs) for stage, jobs in config['pipeline'].items()}",
    "total_jobs = sum(jobs_per_stage.values()): 3+4+2+3=12.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-042: GIT HOOK VALIDATOR ]",
"description": (
    "Implementa `PreCommitHook` con `add_check(name, fn)` y `run() -> dict`. "
    "Ejecuta todos los checks y retorna `{'passed': list, 'failed': list, 'blocked': bool}`."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 42, "base_xp_reward": 180,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "python",
"phase": "cicd_infra", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["git_hooks", "pre_commit", "linting", "calidad"]),
"initial_code": (
    "class PreCommitHook:\n"
    "    def __init__(self):\n"
    "        self._checks = []\n"
    "\n"
    "    def add_check(self, name: str, fn):\n"
    "        # TODO: agrega (name, fn) a self._checks\n"
    "        pass\n"
    "\n"
    "    def run(self) -> dict:\n"
    "        # TODO: ejecuta cada check (llama fn())\n"
    "        # Si fn() retorna True → agrega name a 'passed'\n"
    "        # Si fn() retorna False → agrega name a 'failed'\n"
    "        # 'blocked': True si hay algún check fallido\n"
    "        # Para cada check imprime: '[OK] {name}' o '[FAIL] {name}'\n"
    "        pass\n"
    "\n"
    "\n"
    "hook = PreCommitHook()\n"
    "hook.add_check('lint',           lambda: True)\n"
    "hook.add_check('type-check',     lambda: True)\n"
    "hook.add_check('unit-tests',     lambda: False)\n"
    "hook.add_check('secret-scanner', lambda: True)\n"
    "\n"
    "result = hook.run()\n"
    "print(f'Passed: {\", \".join(result[\"passed\"])}')\n"
    "print(f'Failed: {\", \".join(result[\"failed\"])}')\n"
    "print(f'Blocked: {result[\"blocked\"]}')\n"
),
"expected_output": (
    "[OK] lint\n"
    "[OK] type-check\n"
    "[FAIL] unit-tests\n"
    "[OK] secret-scanner\n"
    "Passed: lint, type-check, secret-scanner\n"
    "Failed: unit-tests\n"
    "Blocked: True"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "El pre-commit hook es tu primera línea de defensa — "
    "antes de que el código entre al repo y contamine la base."
),
"theory_content": (
    "## Pre-Commit Hooks\n\n"
    "Se ejecutan automáticamente antes de cada `git commit`:\n\n"
    "```bash\n# .git/hooks/pre-commit\nnpm run lint && npm run type-check && npm test\n```\n\n"
    "**Herramienta recomendada**: `pre-commit` (Python) permite configurar hooks como YAML:\n"
    "```yaml\nrepos:\n  - repo: pycqa/flake8\n    hooks:\n      - id: flake8\n```\n\n"
    "Si el hook falla, el commit se bloquea — evita que código roto llegue al repo."
),
"pedagogical_objective": "Implementar un sistema de pre-commit hooks con ejecución de múltiples checks.",
"syntax_hint": "Itera self._checks y llama a cada `fn()` para determinar si pasa o falla.",
"hints_json": json.dumps([
    "add_check: self._checks.append((name, fn))",
    "En run: passed=[], failed=[]. Para cada name, fn: result=fn(); si result: passed.append(name), print '[OK]'; si no: failed.append, print '[FAIL]'",
    "blocked = len(failed) > 0. Retorna el dict al final.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-043: DOCKER TEST ENVIRONMENT ]",
"description": (
    "Implementa `DockerfileGenerator.generate(base_image: str, packages: list, test_cmd: str) -> str` "
    "que produzca un Dockerfile para entorno de testing."
),
"difficulty_tier": 1, "difficulty": "easy",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 43, "base_xp_reward": 190,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 200, "challenge_type": "python",
"phase": "cicd_infra", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["Docker", "entorno", "reproducibilidad", "CI"]),
"initial_code": (
    "class DockerfileGenerator:\n"
    "    def generate(self, base_image: str, packages: list, test_cmd: str) -> str:\n"
    "        # TODO: retorna Dockerfile con este formato exacto:\n"
    "        # FROM {base_image}\n"
    "        # WORKDIR /app\n"
    "        # COPY requirements.txt .\n"
    "        # RUN pip install {packages[0]} {packages[1]} ...\n"
    "        # COPY . .\n"
    "        # CMD [\"{test_cmd}\"] (separado por espacios si hay más de una palabra)\n"
    "        pass\n"
    "\n"
    "\n"
    "gen = DockerfileGenerator()\n"
    "dockerfile = gen.generate(\n"
    "    base_image='python:3.11-slim',\n"
    "    packages=['pytest', 'pytest-cov', 'requests', 'playwright'],\n"
    "    test_cmd='pytest --cov=app tests/',\n"
    ")\n"
    "print(dockerfile)\n"
),
"expected_output": (
    "FROM python:3.11-slim\n"
    "WORKDIR /app\n"
    "COPY requirements.txt .\n"
    "RUN pip install pytest pytest-cov requests playwright\n"
    "COPY . .\n"
    'CMD ["pytest", "--cov=app", "tests/"]'
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Docker garantiza que tus tests corran igual en local, en CI y en la máquina del nuevo dev. "
    "Sin 'works on my machine' — siempre."
),
"theory_content": (
    "## Docker para Testing\n\n"
    "Un Dockerfile de testing mínimo:\n\n"
    "```dockerfile\nFROM python:3.11-slim\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install -r requirements.txt\nCOPY . .\nCMD [\"pytest\"]\n```\n\n"
    "**CMD con JSON array**: la forma preferida para evitar shell interpolation:\n"
    "`CMD [\"pytest\", \"--cov=app\"]` — cada argumento es un elemento del array."
),
"pedagogical_objective": "Generar un Dockerfile válido para entorno de testing con múltiples dependencias.",
"syntax_hint": "Para CMD: convierte `test_cmd.split()` a `', '.join(f'\"{part}\"' for part in parts)`.",
"hints_json": json.dumps([
    "RUN pip install: ' '.join(packages) — une los packages con espacio.",
    "CMD: parts = test_cmd.split(); f'CMD [{', '.join(f'\"{p}\"' for p in parts)}]'",
    "CMD line: ['pytest', '--cov=app', 'tests/'] → CMD [\"pytest\", \"--cov=app\", \"tests/\"]",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-044: GITHUB ACTIONS WORKFLOW ]",
"description": (
    "Implementa `WorkflowBuilder.build(name: str, triggers: list, jobs: dict) -> str` "
    "que genere la estructura de un workflow de GitHub Actions como texto formateado."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 44, "base_xp_reward": 200,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "python",
"phase": "cicd_infra", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["GitHub_Actions", "workflow", "CI", "automatizacion"]),
"initial_code": (
    "class WorkflowBuilder:\n"
    "    def build(self, name: str, triggers: list, jobs: dict) -> str:\n"
    "        # TODO: genera workflow formateado:\n"
    "        # name: {name}\n"
    "        # on: {triggers unidos por ', '}\n"
    "        # jobs:\n"
    "        #   {job_name}:\n"
    "        #     steps: {step_count} steps\n"
    "        # (para cada job en jobs)\n"
    "        pass\n"
    "\n"
    "\n"
    "builder = WorkflowBuilder()\n"
    "workflow = builder.build(\n"
    "    name='QA Pipeline',\n"
    "    triggers=['push', 'pull_request'],\n"
    "    jobs={\n"
    "        'lint':        ['checkout', 'setup-python', 'run-flake8'],\n"
    "        'unit-tests':  ['checkout', 'setup-python', 'install-deps', 'run-pytest', 'upload-coverage'],\n"
    "        'e2e-tests':   ['checkout', 'setup-python', 'install-playwright', 'run-e2e'],\n"
    "    }\n"
    ")\n"
    "print(workflow)\n"
),
"expected_output": (
    "name: QA Pipeline\n"
    "on: push, pull_request\n"
    "jobs:\n"
    "  lint:\n"
    "    steps: 3 steps\n"
    "  unit-tests:\n"
    "    steps: 5 steps\n"
    "  e2e-tests:\n"
    "    steps: 4 steps"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "GitHub Actions es el CI/CD más accesible del mercado. "
    "Domínalo y dominas el pipeline de calidad de casi cualquier empresa."
),
"theory_content": (
    "## GitHub Actions Structure\n\n"
    "```yaml\nname: CI Pipeline\non: [push, pull_request]\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v3\n      - run: pytest\n```\n\n"
    "**Triggers comunes**: `push` (cada push), `pull_request` (en PRs), `schedule` (cron), `workflow_dispatch` (manual)."
),
"pedagogical_objective": "Generar la estructura de un workflow de GitHub Actions con múltiples jobs.",
"syntax_hint": "Construye una lista de líneas e itera los jobs con `jobs.items()`.",
"hints_json": json.dumps([
    "lines = ['name: ' + name, 'on: ' + ', '.join(triggers), 'jobs:']",
    "Para cada job: lines.append(f'  {job_name}:'); lines.append(f'    steps: {len(steps)} steps')",
    "Retorna '\\n'.join(lines).",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-045: ENVIRONMENT VARIABLE MANAGER ]",
"description": (
    "Implementa `EnvManager` con `load(env_name: str, config: dict)`, "
    "`get(key: str) -> str` y `validate_required(keys: list) -> list`. "
    "Retorna lista de claves faltantes."
),
"difficulty_tier": 1, "difficulty": "easy",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 45, "base_xp_reward": 220,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 200, "challenge_type": "python",
"phase": "cicd_infra", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["env_vars", "secrets", "configuracion", "entornos"]),
"initial_code": (
    "class EnvManager:\n"
    "    def __init__(self):\n"
    "        self._env = {}\n"
    "        self._name = 'none'\n"
    "\n"
    "    def load(self, env_name: str, config: dict):\n"
    "        # TODO: guarda env_name en self._name y config en self._env\n"
    "        # imprime 'Loaded env: {env_name} ({len(config)} vars)'\n"
    "        pass\n"
    "\n"
    "    def get(self, key: str) -> str:\n"
    "        # TODO: retorna self._env.get(key, 'NOT_SET')\n"
    "        pass\n"
    "\n"
    "    def validate_required(self, keys: list) -> list:\n"
    "        # TODO: retorna lista de keys que no están en self._env o tienen valor vacío\n"
    "        pass\n"
    "\n"
    "\n"
    "env = EnvManager()\n"
    "env.load('staging', {\n"
    "    'DATABASE_URL': 'postgres://staging-db/app',\n"
    "    'API_KEY':      'sk-staging-abc123',\n"
    "    'DEBUG':        'false',\n"
    "})\n"
    "print(env.get('DATABASE_URL'))\n"
    "print(env.get('SECRET_KEY'))\n"
    "missing = env.validate_required(['DATABASE_URL', 'API_KEY', 'SECRET_KEY', 'JWT_SECRET'])\n"
    "print(f'Missing: {\", \".join(missing)}')\n"
),
"expected_output": (
    "Loaded env: staging (3 vars)\n"
    "postgres://staging-db/app\n"
    "NOT_SET\n"
    "Missing: SECRET_KEY, JWT_SECRET"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Los secrets hardcodeados son vulnerabilidades esperando ser explotadas. "
    "El EnvManager los centraliza y valida antes del despliegue."
),
"theory_content": (
    "## Environment Variables en CI/CD\n\n"
    "**Regla**: nunca hardcodees secrets en el código ni en los tests.\n\n"
    "```bash\n# GitHub Actions\nenv:\n  DATABASE_URL: ${{ secrets.DATABASE_URL }}\n  API_KEY: ${{ secrets.API_KEY }}\n```\n\n"
    "**En tests**: valida que todas las variables requeridas estén presentes "
    "al inicio de la suite — falla rápido si falta una."
),
"pedagogical_objective": "Implementar un gestor de variables de entorno con carga, lectura y validación.",
"syntax_hint": "`validate_required`: `return [k for k in keys if k not in self._env or not self._env[k]]`",
"hints_json": json.dumps([
    "load: self._name = env_name; self._env = config; print(f'Loaded env: {env_name} ({len(config)} vars)')",
    "get: return self._env.get(key, 'NOT_SET')",
    "validate_required: return [k for k in keys if k not in self._env]",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-046: TEST PARALLELIZATION CONFIG ]",
"description": (
    "Implementa `ParallelConfig.optimize(total_tests: int, avg_duration_s: float, target_minutes: float) -> dict` "
    "que calcule los workers necesarios para alcanzar el target de duración."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 46, "base_xp_reward": 230,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "python",
"phase": "cicd_infra", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["paralelismo", "pytest_xdist", "CI", "optimizacion"]),
"initial_code": (
    "import math\n"
    "\n"
    "\n"
    "class ParallelConfig:\n"
    "    def optimize(self, total_tests: int, avg_duration_s: float,\n"
    "                 target_minutes: float) -> dict:\n"
    "        # TODO: calcula la configuración óptima de paralelización\n"
    "        # total_duration_s = total_tests * avg_duration_s\n"
    "        # workers_needed = ceil(total_duration_s / (target_minutes * 60))\n"
    "        # actual_duration_min = round(total_duration_s / workers_needed / 60, 1)\n"
    "        # Retorna dict con: workers, total_duration_s, actual_duration_min\n"
    "        pass\n"
    "\n"
    "\n"
    "config = ParallelConfig()\n"
    "scenarios = [\n"
    "    (500, 5.4, 15),\n"
    "    (200, 8.0, 10),\n"
    "    (1000, 3.0, 5),\n"
    "]\n"
    "for tests, avg, target in scenarios:\n"
    "    result = config.optimize(tests, avg, target)\n"
    "    print(f'{tests} tests | workers={result[\"workers\"]} | '\n"
    "          f'actual={result[\"actual_duration_min\"]}min')\n"
),
"expected_output": (
    "500 tests | workers=3 | actual=15.0min\n"
    "200 tests | workers=3 | actual=8.9min\n"
    "1000 tests | workers=10 | actual=5.0min"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Un CI de 45 minutos mata la productividad. "
    "La paralelización lo baja a 8 — si sabes cuántos workers configurar."
),
"theory_content": (
    "## pytest-xdist Paralelización\n\n"
    "```bash\npytest -n auto  # detecta CPUs disponibles\npytest -n 4    # 4 workers fijos\n```\n\n"
    "**Fórmula**:\n"
    "```\nworkers = ceil(total_time / target_time)\nactual_time = total_time / workers\n```\n\n"
    "**Overhead**: paralelizar add ~10-20% de overhead por sincronización. "
    "No esperes reducción lineal perfecta."
),
"pedagogical_objective": "Calcular la configuración óptima de workers para paralelización de tests en CI.",
"syntax_hint": "`workers_needed = math.ceil(total_duration_s / (target_minutes * 60))`",
"hints_json": json.dumps([
    "Scenario 1: total=500*5.4=2700s. target=15*60=900s. workers=ceil(2700/900)=3. actual=2700/3/60=15.0min.",
    "Scenario 2: total=200*8=1600s. target=10*60=600s. workers=ceil(1600/600)=ceil(2.67)=3. actual=1600/3/60=8.89→8.9min.",
    "Scenario 3: total=1000*3=3000s. target=5*60=300s. workers=ceil(3000/300)=10. actual=3000/10/60=5.0min.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-047: ARTIFACT COLLECTOR ]",
"description": (
    "Implementa `ArtifactCollector` con `collect(test_run_id: str, artifacts: list)` "
    "y `summary() -> str`. Clasifica artefactos por tipo: `report`, `screenshot`, `log`."
),
"difficulty_tier": 1, "difficulty": "easy",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 47, "base_xp_reward": 240,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 200, "challenge_type": "python",
"phase": "cicd_infra", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["artifacts", "logs", "evidencia", "CI"]),
"initial_code": (
    "class ArtifactCollector:\n"
    "    def __init__(self):\n"
    "        self._collected = []\n"
    "\n"
    "    def collect(self, test_run_id: str, artifacts: list):\n"
    "        # TODO: para cada artifact en artifacts:\n"
    "        # - determina el tipo por extensión: .html/.xml → 'report', .png/.jpg → 'screenshot', .log → 'log'\n"
    "        # - agrega {'run': test_run_id, 'file': artifact, 'type': tipo} a self._collected\n"
    "        # - imprime 'Collected [{tipo}]: {artifact}'\n"
    "        pass\n"
    "\n"
    "    def summary(self) -> str:\n"
    "        # TODO: retorna resumen formateado:\n"
    "        # 'Total: {n} artifacts'\n"
    "        # '  reports: {count}'\n"
    "        # '  screenshots: {count}'\n"
    "        # '  logs: {count}'\n"
    "        pass\n"
    "\n"
    "\n"
    "collector = ArtifactCollector()\n"
    "collector.collect('run-001', [\n"
    "    'test-report.html',\n"
    "    'failure-screenshot.png',\n"
    "    'app.log',\n"
    "    'junit-results.xml',\n"
    "    'login-failure.png',\n"
    "])\n"
    "print(collector.summary())\n"
),
"expected_output": (
    "Collected [report]: test-report.html\n"
    "Collected [screenshot]: failure-screenshot.png\n"
    "Collected [log]: app.log\n"
    "Collected [report]: junit-results.xml\n"
    "Collected [screenshot]: login-failure.png\n"
    "Total: 5 artifacts\n"
    "  reports: 2\n"
    "  screenshots: 2\n"
    "  logs: 1"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Sin artifacts, un test fallido en CI es un misterio. "
    "Con artifacts — el screenshot, el log, el reporte — es un caso resuelto."
),
"theory_content": (
    "## CI Artifacts\n\n"
    "GitHub Actions:\n"
    "```yaml\n- uses: actions/upload-artifact@v3\n  with:\n    name: test-results\n    path: |\n      test-results/\n      screenshots/\n      *.log\n```\n\n"
    "**Best practice**: siempre recolectar artifacts `if: always()` — "
    "especialmente en tests fallidos, que son justo cuando más los necesitas."
),
"pedagogical_objective": "Implementar un colector de artefactos de CI que clasifique por tipo y genere resumen.",
"syntax_hint": "Determina el tipo con: `artifact.rsplit('.', 1)[-1]` y mapea extensión → tipo.",
"hints_json": json.dumps([
    "EXT_MAP = {'html': 'report', 'xml': 'report', 'png': 'screenshot', 'jpg': 'screenshot', 'log': 'log'}",
    "ext = artifact.rsplit('.', 1)[-1]; tipo = EXT_MAP.get(ext, 'other')",
    "En summary: counts = {t: sum(1 for a in self._collected if a['type']==t) for t in ['report','screenshot','log']}",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-048: MATRIX BUILD STRATEGY ]",
"description": (
    "Implementa `MatrixBuilder.generate(python_versions: list, os_list: list) -> list` "
    "y `estimate_duration(matrix: list, avg_minutes: float) -> str`."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 48, "base_xp_reward": 250,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "python",
"phase": "cicd_infra", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["matrix_build", "cross_platform", "versiones", "CI"]),
"initial_code": (
    "from itertools import product\n"
    "\n"
    "\n"
    "class MatrixBuilder:\n"
    "    def generate(self, python_versions: list, os_list: list) -> list:\n"
    "        # TODO: retorna lista de dicts {'python': v, 'os': o}\n"
    "        pass\n"
    "\n"
    "    def estimate_duration(self, matrix: list, avg_minutes: float) -> str:\n"
    "        # TODO: retorna 'Matrix: {n} combinations | parallel: {avg_minutes}min | sequential: {total}min'\n"
    "        # sequential = len(matrix) * avg_minutes\n"
    "        pass\n"
    "\n"
    "\n"
    "builder = MatrixBuilder()\n"
    "matrix = builder.generate(\n"
    "    python_versions=['3.10', '3.11', '3.12'],\n"
    "    os_list=['ubuntu-latest', 'windows-latest', 'macos-latest']\n"
    ")\n"
    "print(f'Generated {len(matrix)} combinations:')\n"
    "for combo in matrix:\n"
    "    print(f'  py{combo[\"python\"]} on {combo[\"os\"]}')\n"
    "print(builder.estimate_duration(matrix, avg_minutes=8.0))\n"
),
"expected_output": (
    "Generated 9 combinations:\n"
    "  py3.10 on ubuntu-latest\n"
    "  py3.10 on windows-latest\n"
    "  py3.10 on macos-latest\n"
    "  py3.11 on ubuntu-latest\n"
    "  py3.11 on windows-latest\n"
    "  py3.11 on macos-latest\n"
    "  py3.12 on ubuntu-latest\n"
    "  py3.12 on windows-latest\n"
    "  py3.12 on macos-latest\n"
    "Matrix: 9 combinations | parallel: 8.0min | sequential: 72.0min"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "La matrix build garantiza compatibilidad cross-platform sin duplicar workflows. "
    "9 combinaciones en paralelo = 8 minutos. En secuencia = 72."
),
"theory_content": (
    "## GitHub Actions Matrix Strategy\n\n"
    "```yaml\nstrategy:\n  matrix:\n    python: ['3.10', '3.11', '3.12']\n    os: [ubuntu-latest, windows-latest, macos-latest]\n```\n\n"
    "GitHub Actions ejecuta todas las combinaciones **en paralelo**. "
    "La duración total = max(duración de cualquier combinación), no la suma."
),
"pedagogical_objective": "Generar una matriz de builds cross-platform y estimar el impacto de la paralelización.",
"syntax_hint": "`[{'python': v, 'os': o} for v, o in product(python_versions, os_list)]`",
"hints_json": json.dumps([
    "generate: return [{'python': v, 'os': o} for v, o in product(python_versions, os_list)]",
    "sequential = len(matrix) * avg_minutes = 9 * 8.0 = 72.0",
    "estimate_duration: return f'Matrix: {len(matrix)} combinations | parallel: {avg_minutes}min | sequential: {sequential:.1f}min'",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-049: PIPELINE STAGE GATE ]",
"description": (
    "Implementa `StagePipeline` con `add_stage(name, fn)` y `run() -> dict`. "
    "Si un stage falla, los siguientes se marcan como `SKIPPED`."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 49, "base_xp_reward": 260,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "python",
"phase": "cicd_infra", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["stage_gate", "pipeline", "fail_fast", "CI"]),
"initial_code": (
    "class StagePipeline:\n"
    "    def __init__(self):\n"
    "        self._stages = []\n"
    "\n"
    "    def add_stage(self, name: str, fn):\n"
    "        # TODO: agrega (name, fn) a self._stages\n"
    "        pass\n"
    "\n"
    "    def run(self) -> dict:\n"
    "        # TODO: ejecuta stages en orden\n"
    "        # Imprime 'Running stage: {name}'\n"
    "        # Si fn() retorna True: imprime '  PASS: {name}', agrega a results['passed']\n"
    "        # Si fn() retorna False: imprime '  FAIL: {name}', agrega a results['failed']\n"
    "        #   → Los siguientes stages: imprime '  SKIP: {name}', agrega a results['skipped']\n"
    "        # Retorna {'passed': list, 'failed': list, 'skipped': list}\n"
    "        pass\n"
    "\n"
    "\n"
    "pipeline = StagePipeline()\n"
    "pipeline.add_stage('build',     lambda: True)\n"
    "pipeline.add_stage('unit-test', lambda: False)\n"
    "pipeline.add_stage('e2e-test',  lambda: True)\n"
    "pipeline.add_stage('deploy',    lambda: True)\n"
    "\n"
    "results = pipeline.run()\n"
    "print(f'Passed:  {\", \".join(results[\"passed\"])}')\n"
    "print(f'Failed:  {\", \".join(results[\"failed\"])}')\n"
    "print(f'Skipped: {\", \".join(results[\"skipped\"])}')\n"
),
"expected_output": (
    "Running stage: build\n"
    "  PASS: build\n"
    "Running stage: unit-test\n"
    "  FAIL: unit-test\n"
    "  SKIP: e2e-test\n"
    "  SKIP: deploy\n"
    "Passed:  build\n"
    "Failed:  unit-test\n"
    "Skipped: e2e-test, deploy"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Los stage gates ahorran recursos: si los unit tests fallan, "
    "no tiene sentido gastar tiempo y dinero en e2e y deploy."
),
"theory_content": (
    "## Fail-Fast Pipeline\n\n"
    "```\nbuild → unit-test (FAIL) → e2e-test (SKIP) → deploy (SKIP)\n```\n\n"
    "**Principio**: la información más rápida y barata primero. "
    "Unit tests (5 min) antes de E2E tests (30 min).\n\n"
    "Si el build falla, no gastes 30 min en e2e que van a fallar igual."
),
"pedagogical_objective": "Implementar un pipeline con gate de stages que cortocircuita en caso de fallo.",
"syntax_hint": "Usa un flag `blocked = False` que se activa cuando un stage falla.",
"hints_json": json.dumps([
    "blocked = False. Para cada stage: si blocked: print SKIP, agrega a skipped, continúa.",
    "Si no blocked: print 'Running stage: {name}'; result = fn(). Si True: PASS; si False: FAIL y blocked = True.",
    "Los stages posteriores al fallo: no ejecutan fn(), solo se marcan SKIP.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-050: FLAKY TEST QUARANTINE ]",
"description": (
    "Implementa `FlakyDetector.analyze(test_history: dict) -> dict` que detecte tests flaky. "
    "Un test es flaky si tiene resultados mixtos (PASS y FAIL en el historial). "
    "Retorna `{'flaky': list, 'stable_pass': list, 'stable_fail': list}`."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 50, "base_xp_reward": 270,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "python",
"phase": "cicd_infra", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["flaky_tests", "quarantine", "estabilidad", "historial"]),
"initial_code": (
    "class FlakyDetector:\n"
    "    def analyze(self, test_history: dict) -> dict:\n"
    "        # TODO: clasifica cada test según su historial de resultados\n"
    "        # test_history: {test_name: ['PASS', 'FAIL', 'PASS', ...]}\n"
    "        # flaky: tiene al menos 1 PASS y 1 FAIL\n"
    "        # stable_pass: todos PASS\n"
    "        # stable_fail: todos FAIL\n"
    "        pass\n"
    "\n"
    "\n"
    "detector = FlakyDetector()\n"
    "history = {\n"
    "    'test_login':       ['PASS', 'PASS', 'PASS', 'PASS'],\n"
    "    'test_checkout':    ['PASS', 'FAIL', 'PASS', 'FAIL'],\n"
    "    'test_search':      ['PASS', 'PASS', 'FAIL', 'PASS'],\n"
    "    'test_payment':     ['FAIL', 'FAIL', 'FAIL', 'FAIL'],\n"
    "    'test_profile':     ['PASS', 'PASS', 'PASS', 'PASS'],\n"
    "    'test_admin':       ['FAIL', 'PASS', 'FAIL', 'PASS'],\n"
    "}\n"
    "result = detector.analyze(history)\n"
    "print(f'Flaky ({len(result[\"flaky\"])}):')\n"
    "for t in result['flaky']:\n"
    "    print(f'  - {t}')\n"
    "print(f'Stable PASS: {\", \".join(result[\"stable_pass\"])}')\n"
    "print(f'Stable FAIL: {\", \".join(result[\"stable_fail\"])}')\n"
),
"expected_output": (
    "Flaky (3):\n"
    "  - test_checkout\n"
    "  - test_search\n"
    "  - test_admin\n"
    "Stable PASS: test_login, test_profile\n"
    "Stable FAIL: test_payment"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Un test flaky que bloquea el CI es peor que no tener el test. "
    "La quarantine lo contiene — el problema queda visible pero no bloquea el equipo."
),
"theory_content": (
    "## Flaky Test Management\n\n"
    "Un test flaky tiene resultados no deterministas — pasa a veces, falla otras "
    "sin cambios en el código.\n\n"
    "**Causas comunes**: timing issues, dependencias de red, datos compartidos entre tests, "
    "orden de ejecución.\n\n"
    "**Estrategia**: detectar → quarantine → investigar → arreglar → reintegrar."
),
"pedagogical_objective": "Detectar tests flaky analizando historial de resultados con clasificación tripartita.",
"syntax_hint": "`has_pass = 'PASS' in results; has_fail = 'FAIL' in results`",
"hints_json": json.dumps([
    "Para cada test_name, results in history: has_pass = 'PASS' in results; has_fail = 'FAIL' in results",
    "if has_pass and has_fail: flaky.append(). elif all(r=='PASS'): stable_pass.append(). else: stable_fail.append().",
    "test_checkout: PASS+FAIL → flaky. test_login: todos PASS → stable_pass. test_payment: todos FAIL → stable_fail.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-051: DOCKER COMPOSE TEST STACK ]",
"description": (
    "Implementa `ComposeStack.define_service(name, image, env, depends_on)` "
    "y `generate_compose() -> str` que genere la configuración del stack."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 51, "base_xp_reward": 290,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "python",
"phase": "cicd_infra", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["docker_compose", "stack", "integracion", "servicios"]),
"initial_code": (
    "class ComposeStack:\n"
    "    def __init__(self):\n"
    "        self._services = []\n"
    "\n"
    "    def define_service(self, name: str, image: str,\n"
    "                       env: dict = None, depends_on: list = None):\n"
    "        # TODO: agrega servicio a self._services\n"
    "        pass\n"
    "\n"
    "    def generate_compose(self) -> str:\n"
    "        # TODO: genera composición formateada:\n"
    "        # version: '3.8'\n"
    "        # services:\n"
    "        #   {name}:\n"
    "        #     image: {image}\n"
    "        #     environment: {n} vars   (solo si env no vacío)\n"
    "        #     depends_on: {deps}      (solo si depends_on no vacío)\n"
    "        pass\n"
    "\n"
    "\n"
    "stack = ComposeStack()\n"
    "stack.define_service('db',   'postgres:15', env={'POSTGRES_DB': 'testdb'})\n"
    "stack.define_service('redis','redis:7')\n"
    "stack.define_service('app',  'myapp:test',\n"
    "                     env={'DATABASE_URL': 'postgres://db/testdb', 'REDIS_URL': 'redis://redis'},\n"
    "                     depends_on=['db', 'redis'])\n"
    "print(stack.generate_compose())\n"
),
"expected_output": (
    "version: '3.8'\n"
    "services:\n"
    "  db:\n"
    "    image: postgres:15\n"
    "    environment: 1 vars\n"
    "  redis:\n"
    "    image: redis:7\n"
    "  app:\n"
    "    image: myapp:test\n"
    "    environment: 2 vars\n"
    "    depends_on: db, redis"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Los integration tests necesitan infraestructura real. "
    "Docker Compose la orquesta — app + DB + redis listos en 30 segundos."
),
"theory_content": (
    "## Docker Compose para Testing\n\n"
    "```yaml\nversion: '3.8'\nservices:\n  db:\n    image: postgres:15\n    environment:\n      POSTGRES_DB: testdb\n  app:\n    image: myapp:test\n    depends_on: [db]\n```\n\n"
    "**En CI**: `docker compose up -d && pytest && docker compose down`\n\n"
    "Garantiza que los tests de integración siempre tienen la misma infraestructura."
),
"pedagogical_objective": "Generar configuración de Docker Compose para un stack de testing con dependencias.",
"syntax_hint": "Solo añade la línea `environment` si `env` no es None/vacío, igual con `depends_on`.",
"hints_json": json.dumps([
    "define_service: self._services.append({'name':name,'image':image,'env':env,'depends_on':depends_on})",
    "En generate_compose: para cada servicio, agrega indented lines. Si env: f'    environment: {len(env)} vars'",
    "Si depends_on: f'    depends_on: {\", \".join(depends_on)}'",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-052: JENKINS PIPELINE CONVERTER ]",
"description": (
    "Implementa `PipelineConverter.jenkinsfile_to_gha(stages: list) -> str` "
    "que convierta una lista de stages de Jenkinsfile a formato GitHub Actions."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 52, "base_xp_reward": 300,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "python",
"phase": "cicd_infra", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["Jenkins", "migracion", "GitHub_Actions", "CI"]),
"initial_code": (
    "class PipelineConverter:\n"
    "    def jenkinsfile_to_gha(self, stages: list) -> str:\n"
    "        # TODO: convierte stages de Jenkins a GitHub Actions\n"
    "        # stages: lista de dicts {'name': str, 'steps': list[str], 'when': str|None}\n"
    "        # Formato de salida:\n"
    "        # jobs:\n"
    "        #   {name}:\n"
    "        #     runs-on: ubuntu-latest\n"
    "        #     if: {when}    (solo si when no es None)\n"
    "        #     steps:\n"
    "        #       - run: {step}   (para cada step)\n"
    "        pass\n"
    "\n"
    "\n"
    "converter = PipelineConverter()\n"
    "stages = [\n"
    "    {'name': 'build',    'steps': ['mvn compile', 'mvn package'],         'when': None},\n"
    "    {'name': 'test',     'steps': ['mvn test', 'mvn verify'],             'when': None},\n"
    "    {'name': 'deploy',   'steps': ['helm upgrade myapp ./chart'],         'when': 'main_branch'},\n"
    "]\n"
    "print(converter.jenkinsfile_to_gha(stages))\n"
),
"expected_output": (
    "jobs:\n"
    "  build:\n"
    "    runs-on: ubuntu-latest\n"
    "    steps:\n"
    "      - run: mvn compile\n"
    "      - run: mvn package\n"
    "  test:\n"
    "    runs-on: ubuntu-latest\n"
    "    steps:\n"
    "      - run: mvn test\n"
    "      - run: mvn verify\n"
    "  deploy:\n"
    "    runs-on: ubuntu-latest\n"
    "    if: main_branch\n"
    "    steps:\n"
    "      - run: helm upgrade myapp ./chart"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "La migración de Jenkins a GitHub Actions es inevitable en muchas empresas. "
    "El QA Architect que puede traducir pipelines entre plataformas es invaluable."
),
"theory_content": (
    "## Jenkins vs GitHub Actions\n\n"
    "| Jenkins (Jenkinsfile) | GitHub Actions |\n"
    "|-----------------------|----------------|\n"
    "| `stage('Build')` | `jobs: build:` |\n"
    "| `steps { sh 'cmd' }` | `steps: - run: cmd` |\n"
    "| `when { branch 'main' }` | `if: github.ref == 'refs/heads/main'` |\n\n"
    "La conversión no siempre es 1:1 — algunos features de Jenkins no tienen equivalente directo en GHA."
),
"pedagogical_objective": "Convertir la estructura de un Jenkinsfile a formato GitHub Actions usando mapeo de campos.",
"syntax_hint": "Construye líneas iterando stages y sus steps, añadiendo `if` solo cuando `when` no es None.",
"hints_json": json.dumps([
    "lines = ['jobs:']. Para cada stage: lines.extend([f'  {name}:', '    runs-on: ubuntu-latest'])",
    "Si stage['when']: lines.append(f'    if: {stage[\"when\"]}')",
    "lines.append('    steps:'). Para cada step: lines.append(f'      - run: {step}')",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-053: TEST COVERAGE REPORTER ]",
"description": (
    "Implementa `CoverageReporter.analyze(modules: list, threshold: float = 80.0) -> dict` "
    "que retorne `{'modules': list, 'overall': float, 'gate_passed': bool, 'below_threshold': list}`."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 53, "base_xp_reward": 310,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "python",
"phase": "cicd_infra", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["coverage", "threshold", "enforcement", "gate"]),
"initial_code": (
    "class CoverageReporter:\n"
    "    def analyze(self, modules: list, threshold: float = 80.0) -> dict:\n"
    "        # TODO: analiza cobertura por módulo\n"
    "        # modules: lista de dicts {'name': str, 'coverage': float}\n"
    "        # overall: round(media de coberturas, 1)\n"
    "        # gate_passed: True si overall >= threshold\n"
    "        # below_threshold: nombres de módulos con coverage < threshold\n"
    "        pass\n"
    "\n"
    "\n"
    "reporter = CoverageReporter()\n"
    "modules = [\n"
    "    {'name': 'auth',     'coverage': 94.2},\n"
    "    {'name': 'checkout', 'coverage': 87.5},\n"
    "    {'name': 'search',   'coverage': 71.3},\n"
    "    {'name': 'api',      'coverage': 88.9},\n"
    "    {'name': 'utils',    'coverage': 65.0},\n"
    "]\n"
    "result = reporter.analyze(modules)\n"
    "print(f'Overall coverage: {result[\"overall\"]}%')\n"
    "print(f'Gate passed: {result[\"gate_passed\"]}')\n"
    "print(f'Below threshold (80%):')\n"
    "for m in result['below_threshold']:\n"
    "    print(f'  - {m}')\n"
),
"expected_output": (
    "Overall coverage: 81.4%\n"
    "Gate passed: True\n"
    "Below threshold (80%):\n"
    "  - search\n"
    "  - utils"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "La cobertura sin enforcement es una métrica vanidosa. "
    "El gate la hace accionable — si no alcanza el 80%, el merge se bloquea."
),
"theory_content": (
    "## Coverage Gate en CI\n\n"
    "```bash\npytest --cov=app --cov-fail-under=80\n```\n\n"
    "Con `--cov-fail-under=80`, pytest retorna exit code 1 si la cobertura cae bajo 80%.\n\n"
    "**Combinado con GitHub Actions**: el job falla → el PR no puede mergearse.\n\n"
    "**Tip**: configura el threshold por módulo, no solo global — el global puede enmascarar módulos críticos no cubiertos."
),
"pedagogical_objective": "Analizar cobertura por módulo y determinar si se cumple el quality gate.",
"syntax_hint": "`overall = round(sum(m['coverage'] for m in modules) / len(modules), 1)`",
"hints_json": json.dumps([
    "overall = round(sum(m['coverage'] for m in modules) / len(modules), 1) = round((94.2+87.5+71.3+88.9+65.0)/5, 1) = round(407/5, 1) = round(81.38, 1) = 81.4",
    "gate_passed = overall >= threshold = 81.4 >= 80.0 = True",
    "below_threshold = [m['name'] for m in modules if m['coverage'] < threshold] → search (71.3) y utils (65.0)",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-054: NOTIFICATION BOT ]",
"description": (
    "Implementa `NotificationBot.send_results(channel: str, results: dict) -> str` "
    "que formatee y retorne el mensaje de notificación de resultados de tests."
),
"difficulty_tier": 1, "difficulty": "easy",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 54, "base_xp_reward": 320,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 200, "challenge_type": "python",
"phase": "cicd_infra", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["notificaciones", "Slack", "comunicacion", "CI"]),
"initial_code": (
    "class NotificationBot:\n"
    "    def send_results(self, channel: str, results: dict) -> str:\n"
    "        # TODO: formatea y retorna el mensaje\n"
    "        # results: {'passed': int, 'failed': int, 'duration_s': float, 'branch': str}\n"
    "        # pass_rate = round(passed / (passed + failed) * 100, 1)\n"
    "        # status_icon = 'PASS' si failed == 0, else 'FAIL'\n"
    "        # Formato:\n"
    "        # [{status_icon}] #{channel} — Branch: {branch}\n"
    "        # Tests: {passed}P / {failed}F | Pass rate: {pass_rate}% | {duration_s}s\n"
    "        pass\n"
    "\n"
    "\n"
    "bot = NotificationBot()\n"
    "test_cases = [\n"
    "    ('qa-alerts', {'passed': 142, 'failed': 0,  'duration_s': 187.3, 'branch': 'main'}),\n"
    "    ('qa-alerts', {'passed': 138, 'failed': 4,  'duration_s': 195.1, 'branch': 'feature/auth-refactor'}),\n"
    "]\n"
    "for channel, results in test_cases:\n"
    "    msg = bot.send_results(channel, results)\n"
    "    print(msg)\n"
),
"expected_output": (
    "[PASS] #qa-alerts \u2014 Branch: main\n"
    "Tests: 142P / 0F | Pass rate: 100.0% | 187.3s\n"
    "[FAIL] #qa-alerts \u2014 Branch: feature/auth-refactor\n"
    "Tests: 138P / 4F | Pass rate: 97.2% | 195.1s"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "El equipo necesita saber el estado del build sin abrir el CI. "
    "El bot lo comunica en el canal correcto en el momento correcto."
),
"theory_content": (
    "## CI Notifications\n\n"
    "Integración con Slack en GitHub Actions:\n"
    "```yaml\n- uses: slackapi/slack-github-action@v1\n  with:\n    channel-id: 'C1234567'\n    slack-message: 'Build: ${{ job.status }}'\n```\n\n"
    "**Best practice**: notifica solo cuando cambia el estado (pass→fail o fail→pass), "
    "no en cada build exitoso — el ruido desensibiliza al equipo."
),
"pedagogical_objective": "Generar mensajes de notificación de resultados de CI con métricas formateadas.",
"syntax_hint": "`pass_rate = round(passed / (passed + failed) * 100, 1)` — cuidado con división por cero.",
"hints_json": json.dumps([
    "status_icon = 'PASS' if results['failed'] == 0 else 'FAIL'",
    "pass_rate: caso 1: 142/(142+0)*100=100.0. caso 2: 138/142*100=97.183→97.2",
    "Retorna 2 líneas unidas con '\\n'. El caracter — es \\u2014 (emdash).",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-055: PERFORMANCE BASELINE CI ]",
"description": (
    "Implementa `PerformanceBaseline.compare(baseline: dict, current: dict) -> dict` "
    "que detecte regresiones. Un endpoint regresiona si su `p95` supera el baseline en más de 20%."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 55, "base_xp_reward": 330,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "python",
"phase": "cicd_infra", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["performance", "baseline", "regresion", "p95"]),
"initial_code": (
    "class PerformanceBaseline:\n"
    "    REGRESSION_THRESHOLD = 1.20  # 20% de degradación\n"
    "\n"
    "    def compare(self, baseline: dict, current: dict) -> dict:\n"
    "        # TODO: compara p95 de cada endpoint\n"
    "        # baseline y current: {endpoint: {'p95': float}}\n"
    "        # Para cada endpoint: delta = (current_p95 - baseline_p95) / baseline_p95\n"
    "        # Si current_p95 > baseline_p95 * THRESHOLD: 'REGRESSION'\n"
    "        # Si no: 'OK'\n"
    "        # Retorna {'results': list[dict], 'regressions': int}\n"
    "        # Cada resultado: {'endpoint': str, 'baseline': float, 'current': float, 'status': str}\n"
    "        pass\n"
    "\n"
    "\n"
    "checker = PerformanceBaseline()\n"
    "baseline = {\n"
    "    '/api/login':    {'p95': 180},\n"
    "    '/api/checkout': {'p95': 320},\n"
    "    '/api/search':   {'p95': 95},\n"
    "}\n"
    "current = {\n"
    "    '/api/login':    {'p95': 195},\n"
    "    '/api/checkout': {'p95': 410},\n"
    "    '/api/search':   {'p95': 92},\n"
    "}\n"
    "result = checker.compare(baseline, current)\n"
    "for r in result['results']:\n"
    "    print(f'{r[\"endpoint\"]:<18} baseline={r[\"baseline\"]}ms current={r[\"current\"]}ms [{r[\"status\"]}]')\n"
    "print(f'Regressions: {result[\"regressions\"]}')\n"
),
"expected_output": (
    "/api/login         baseline=180ms current=195ms [OK]\n"
    "/api/checkout      baseline=320ms current=410ms [REGRESSION]\n"
    "/api/search        baseline=95ms current=92ms [OK]\n"
    "Regressions: 1"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "La regresión de performance es silenciosa — no rompe tests funcionales. "
    "Sin baseline, no la detectas hasta que el usuario se queja en producción."
),
"theory_content": (
    "## Performance Baseline Testing\n\n"
    "Proceso:\n"
    "1. Establece baseline en main/release\n"
    "2. En cada PR, corre performance tests\n"
    "3. Compara p95 actual vs baseline\n"
    "4. Falla el CI si hay regresión > threshold\n\n"
    "**p95**: el percentil 95 — el 95% de las requests responde en <= ese tiempo."
),
"pedagogical_objective": "Detectar regresiones de performance comparando percentiles p95 contra un baseline.",
"syntax_hint": "`status = 'REGRESSION' if current_p95 > baseline_p95 * self.REGRESSION_THRESHOLD else 'OK'`",
"hints_json": json.dumps([
    "/api/login: 195 > 180*1.20=216? No (195<216) → OK.",
    "/api/checkout: 410 > 320*1.20=384? Yes (410>384) → REGRESSION.",
    "/api/search: 92 > 95*1.20=114? No → OK. regressions = sum(1 for r in results if r['status']=='REGRESSION') = 1.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-056: SCHEDULED TEST RUNNER ]",
"description": (
    "Implementa `TestScheduler` con `add_schedule(name, cron: str, suite: str)` "
    "y `list_schedules() -> list`. Valida el cron format básico (5 campos)."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 56, "base_xp_reward": 340,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "python",
"phase": "cicd_infra", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["scheduling", "nightly", "cron", "regression"]),
"initial_code": (
    "class TestScheduler:\n"
    "    def __init__(self):\n"
    "        self._schedules = []\n"
    "\n"
    "    def add_schedule(self, name: str, cron: str, suite: str) -> str:\n"
    "        # TODO: valida cron (debe tener exactamente 5 campos separados por espacio)\n"
    "        # Si válido: agrega y retorna 'Scheduled: {name} [{cron}] -> {suite}'\n"
    "        # Si inválido: retorna 'ERROR: invalid cron \"{cron}\"'\n"
    "        pass\n"
    "\n"
    "    def list_schedules(self) -> list:\n"
    "        # TODO: retorna self._schedules\n"
    "        pass\n"
    "\n"
    "\n"
    "scheduler = TestScheduler()\n"
    "print(scheduler.add_schedule('nightly-regression', '0 2 * * *', 'full-regression'))\n"
    "print(scheduler.add_schedule('weekly-e2e',         '0 6 * * 1', 'e2e-suite'))\n"
    "print(scheduler.add_schedule('bad-cron',           '0 2 *',     'smoke'))\n"
    "print(f'Active schedules: {len(scheduler.list_schedules())}')\n"
),
"expected_output": (
    "Scheduled: nightly-regression [0 2 * * *] -> full-regression\n"
    "Scheduled: weekly-e2e [0 6 * * 1] -> e2e-suite\n"
    'ERROR: invalid cron "0 2 *"\n'
    "Active schedules: 2"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "No todo test debe correr en cada push. "
    "Los schedules optimizan recursos — smoke en cada PR, regresión completa de noche."
),
"theory_content": (
    "## Cron Scheduling en CI\n\n"
    "Formato cron: `minuto hora día_mes mes día_semana`\n\n"
    "```\n0 2 * * *    # Cada día a las 2am\n0 6 * * 1    # Cada lunes a las 6am\n*/15 * * * * # Cada 15 minutos\n```\n\n"
    "GitHub Actions:\n"
    "```yaml\non:\n  schedule:\n    - cron: '0 2 * * *'\n```"
),
"pedagogical_objective": "Implementar un scheduler de tests con validación de formato cron.",
"syntax_hint": "`len(cron.split()) == 5` valida que el cron tenga exactamente 5 campos.",
"hints_json": json.dumps([
    "Validación: if len(cron.split()) != 5: return f'ERROR: invalid cron \"{cron}\"'",
    "Si válido: self._schedules.append({'name':name,'cron':cron,'suite':suite}); return f'Scheduled: {name} [{cron}] -> {suite}'",
    "'0 2 *' tiene 3 campos → ERROR. list_schedules: return self._schedules (2 entradas).",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-057: ROLLBACK DETECTOR ]",
"description": (
    "Implementa `RollbackDetector.evaluate(pre_deploy: dict, post_deploy: dict) -> str` "
    "que retorne `'STABLE'`, `'MONITOR'` o `'ROLLBACK'` según los cambios en métricas."
),
"difficulty_tier": 3, "difficulty": "hard",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 57, "base_xp_reward": 360,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 300, "challenge_type": "python",
"phase": "cicd_infra", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["rollback", "canary", "deployment", "metricas"]),
"initial_code": (
    "class RollbackDetector:\n"
    "    # Umbrales de decisión\n"
    "    ROLLBACK_ERROR_RATE  = 0.05   # > 5% error rate → ROLLBACK\n"
    "    MONITOR_ERROR_RATE   = 0.02   # > 2% → MONITOR\n"
    "    ROLLBACK_LATENCY_MUL = 2.0    # > 2x latencia baseline → ROLLBACK\n"
    "    MONITOR_LATENCY_MUL  = 1.5    # > 1.5x → MONITOR\n"
    "\n"
    "    def evaluate(self, pre: dict, post: dict) -> str:\n"
    "        # TODO: compara error_rate y p95_latency entre pre y post\n"
    "        # Si error_rate_post > ROLLBACK o p95_post > p95_pre * ROLLBACK_LATENCY → 'ROLLBACK'\n"
    "        # Si error_rate_post > MONITOR o p95_post > p95_pre * MONITOR_LATENCY   → 'MONITOR'\n"
    "        # Si no: 'STABLE'\n"
    "        # pre/post: {'error_rate': float, 'p95_latency': float}\n"
    "        pass\n"
    "\n"
    "\n"
    "detector = RollbackDetector()\n"
    "scenarios = [\n"
    "    ('Normal deploy',  {'error_rate': 0.01, 'p95_latency': 200}, {'error_rate': 0.01, 'p95_latency': 210}),\n"
    "    ('Slight issues',  {'error_rate': 0.01, 'p95_latency': 200}, {'error_rate': 0.03, 'p95_latency': 260}),\n"
    "    ('Bad deploy',     {'error_rate': 0.01, 'p95_latency': 200}, {'error_rate': 0.08, 'p95_latency': 450}),\n"
    "]\n"
    "for name, pre, post in scenarios:\n"
    "    decision = detector.evaluate(pre, post)\n"
    "    print(f'{name:<20}: {decision}')\n"
),
"expected_output": (
    "Normal deploy       : STABLE\n"
    "Slight issues       : MONITOR\n"
    "Bad deploy          : ROLLBACK"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "El canary deployment sin detector de rollback es un kamikaze. "
    "El detector es tu paracaídas — actúa en segundos, no en horas."
),
"theory_content": (
    "## Rollback Decision Logic\n\n"
    "```\nerror_rate > 5%  OR  latency > 2x baseline → ROLLBACK inmediato\nerror_rate > 2%  OR  latency > 1.5x          → MONITOR (vigilar)\nEn caso contrario                             → STABLE\n```\n\n"
    "**Prioridad**: evalúa ROLLBACK primero. Si cualquier condición de ROLLBACK se cumple, "
    "no necesitas evaluar MONITOR."
),
"pedagogical_objective": "Implementar un detector de rollback con umbrales múltiples y decisión por prioridad.",
"syntax_hint": "Evalúa ROLLBACK antes que MONITOR — la condición más severa primero.",
"hints_json": json.dumps([
    "Caso 1: error_rate=0.01 <= 0.05, p95=210 <= 200*2=400 → no rollback. p95=210 <= 200*1.5=300, error=0.01<=0.02 → STABLE.",
    "Caso 2: error_rate=0.03 > 0.02 → MONITOR (no llega a ROLLBACK 0.05).",
    "Caso 3: error_rate=0.08 > 0.05 → ROLLBACK (condición de rollback activa).",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-058: INFRASTRUCTURE AS TEST CODE ]",
"description": (
    "Implementa `TestInfra` con `define_resource(tipo, name, config)`, "
    "`validate() -> list` (detecta recursos sin config) "
    "y `export_manifest() -> str`."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 58, "base_xp_reward": 380,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "python",
"phase": "cicd_infra", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["IaC", "testing_infra", "versionado", "reproducibilidad"]),
"initial_code": (
    "class TestInfra:\n"
    "    def __init__(self):\n"
    "        self._resources = []\n"
    "\n"
    "    def define_resource(self, tipo: str, name: str, config: dict):\n"
    "        # TODO: agrega {'type': tipo, 'name': name, 'config': config} a self._resources\n"
    "        pass\n"
    "\n"
    "    def validate(self) -> list:\n"
    "        # TODO: retorna lista de nombres de recursos con config vacío o None\n"
    "        pass\n"
    "\n"
    "    def export_manifest(self) -> str:\n"
    "        # TODO: retorna manifest formateado:\n"
    "        # infra_manifest:\n"
    "        #   resources: {total}\n"
    "        #   {tipo}:\n"
    "        #     - {name} ({n} config params)\n"
    "        # (agrupa por tipo)\n"
    "        pass\n"
    "\n"
    "\n"
    "infra = TestInfra()\n"
    "infra.define_resource('database', 'test-postgres', {'host': 'localhost', 'port': 5432, 'db': 'testdb'})\n"
    "infra.define_resource('cache',    'test-redis',    {'host': 'localhost', 'port': 6379})\n"
    "infra.define_resource('service',  'test-app',      {'image': 'myapp:test', 'port': 8000})\n"
    "infra.define_resource('service',  'orphan-svc',    {})\n"
    "\n"
    "issues = infra.validate()\n"
    "print(f'Validation issues: {issues}')\n"
    "print(infra.export_manifest())\n"
),
"expected_output": (
    "Validation issues: ['orphan-svc']\n"
    "infra_manifest:\n"
    "  resources: 4\n"
    "  database:\n"
    "    - test-postgres (3 config params)\n"
    "  cache:\n"
    "    - test-redis (2 config params)\n"
    "  service:\n"
    "    - test-app (2 config params)\n"
    "    - orphan-svc (0 config params)"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Si tu entorno de testing no es código, no es reproducible. "
    "Y si no es reproducible, no es confiable — 'works on my machine' en testing es inaceptable."
),
"theory_content": (
    "## Infrastructure as Code para Testing\n\n"
    "Beneficios de versionar la infra de testing:\n\n"
    "1. **Reproducible**: cualquier dev puede recrear el entorno\n"
    "2. **Auditable**: git log muestra qué cambió y cuándo\n"
    "3. **Consistente**: dev, CI y staging usan la misma definición\n\n"
    "Herramientas: Terraform, Pulumi, CloudFormation (para infra cloud), "
    "Docker Compose (para infra local)."
),
"pedagogical_objective": "Modelar infraestructura de testing como código con validación y export de manifest.",
"syntax_hint": "Para agrupar por tipo: `from collections import defaultdict; by_type = defaultdict(list)`.",
"hints_json": json.dumps([
    "validate: return [r['name'] for r in self._resources if not r['config']]",
    "Para export_manifest: agrupa por tipo. lines = ['infra_manifest:', f'  resources: {len(self._resources)}']",
    "Para cada tipo único: lines.append(f'  {tipo}:'); para cada r de ese tipo: lines.append(f'    - {r[\"name\"]} ({len(r[\"config\"])} config params)')",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-059: MULTI-REPO TEST ORCHESTRATOR ]",
"description": (
    "Implementa `MultiRepoOrchestrator.run(repos: dict) -> dict` que ejecute tests "
    "para cada repo y agregue resultados. Si un repo falla, los repos que dependen de él "
    "se marcan como `BLOCKED`."
),
"difficulty_tier": 3, "difficulty": "hard",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 59, "base_xp_reward": 380,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 300, "challenge_type": "python",
"phase": "cicd_infra", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["multi_repo", "orquestacion", "microservicios", "dependencias"]),
"initial_code": (
    "class MultiRepoOrchestrator:\n"
    "    def run(self, repos: dict) -> dict:\n"
    "        # TODO: ejecuta tests de cada repo en orden\n"
    "        # repos: {repo_name: {'tests_pass': bool, 'depends_on': list}}\n"
    "        # Si depends_on tiene repos que fallaron: marca como BLOCKED\n"
    "        # Si tests_pass True: PASS. Si False: FAIL.\n"
    "        # Retorna {repo_name: status}\n"
    "        # Para cada repo imprime: '{repo}: {status}'\n"
    "        pass\n"
    "\n"
    "\n"
    "orchestrator = MultiRepoOrchestrator()\n"
    "repos = {\n"
    "    'shared-lib':  {'tests_pass': True,  'depends_on': []},\n"
    "    'auth-service':{'tests_pass': False, 'depends_on': ['shared-lib']},\n"
    "    'api-gateway': {'tests_pass': True,  'depends_on': ['auth-service']},\n"
    "    'frontend':    {'tests_pass': True,  'depends_on': ['api-gateway']},\n"
    "    'analytics':   {'tests_pass': True,  'depends_on': ['shared-lib']},\n"
    "}\n"
    "results = orchestrator.run(repos)\n"
    "failed_or_blocked = [r for r, s in results.items() if s != 'PASS']\n"
    "print(f'Issues: {\", \".join(failed_or_blocked)}')\n"
),
"expected_output": (
    "shared-lib: PASS\n"
    "auth-service: FAIL\n"
    "api-gateway: BLOCKED\n"
    "frontend: BLOCKED\n"
    "analytics: PASS\n"
    "Issues: auth-service, api-gateway, frontend"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Los microservicios se despliegan por separado pero fallan juntos. "
    "El orquestador los prueba en conjunto y propaga el fallo correctamente."
),
"theory_content": (
    "## Multi-Repo Testing\n\n"
    "En arquitecturas de microservicios, los repos tienen dependencias transitivas:\n\n"
    "```\nshared-lib ← auth-service (FAIL) ← api-gateway (BLOCKED) ← frontend (BLOCKED)\n```\n\n"
    "**Estrategia**: usa un grafo de dependencias y propagación de fallos. "
    "Un repo BLOCKED no ejecuta sus tests — no tiene sentido."
),
"pedagogical_objective": "Implementar orquestación multi-repo con propagación de bloqueos por dependencias.",
"syntax_hint": "Acumula un set de `failed_repos` y verifica si algún `depends_on` está en ese set.",
"hints_json": json.dumps([
    "failed_repos = set(). Para cada repo en orden: si cualquier dep en depends_on está en failed_repos → BLOCKED.",
    "Si no blocked y tests_pass → PASS; si no tests_pass → FAIL; agrega a failed_repos si FAIL.",
    "shared-lib: PASS. auth-service: FAIL (no deps bloqueados pero tests_pass=False). api-gateway: depends_on=[auth-service] que es FAIL → BLOCKED.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-060: CONTRATO — PIPELINE QA ENTERPRISE ]",
"description": (
    "Proyecto integrador: implementa `EnterprisePipeline` con stages dinámicos, "
    "gates de cobertura y performance, notificaciones y resumen final."
),
"difficulty_tier": 3, "difficulty": "hard",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 60, "base_xp_reward": 500,
"is_project": True, "is_phase_boss": True,
"telemetry_goal_time": 420, "challenge_type": "python",
"phase": "cicd_infra", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["pipeline", "enterprise", "gates", "integracion"]),
"initial_code": (
    "class EnterprisePipeline:\n"
    "    def __init__(self, project: str):\n"
    "        self.project = project\n"
    "        self._stages  = []\n"
    "        self._results = []\n"
    "\n"
    "    def add_stage(self, name: str, fn, gate: str = None):\n"
    "        # TODO: agrega {'name': name, 'fn': fn, 'gate': gate} a self._stages\n"
    "        pass\n"
    "\n"
    "    def run(self) -> None:\n"
    "        # TODO: ejecuta stages en orden con lógica fail-fast\n"
    "        # Para cada stage: ejecuta fn() que retorna (success: bool, message: str)\n"
    "        # Imprime: 'Stage [{gate}] {name}: PASS — {message}' o '...FAIL — {message}'\n"
    "        # Si falla: imprime 'BLOCKED: {restantes}' y para\n"
    "        # gate puede ser None, 'COVERAGE', 'PERFORMANCE', 'SECURITY'\n"
    "        pass\n"
    "\n"
    "    def report(self) -> None:\n"
    "        # TODO: imprime el resumen final\n"
    "        # === Pipeline: {project} ===\n"
    "        # Stages: {passed}/{total} passed\n"
    "        # Status: PIPELINE PASS o PIPELINE FAIL\n"
    "        pass\n"
    "\n"
    "\n"
    "p = EnterprisePipeline('DAKI Platform')\n"
    "p.add_stage('build',       lambda: (True,  'compiled OK'),            gate=None)\n"
    "p.add_stage('unit-tests',  lambda: (True,  '847 tests, 0 failures'),  gate='COVERAGE')\n"
    "p.add_stage('e2e-tests',   lambda: (False, '3 scenarios failed'),     gate=None)\n"
    "p.add_stage('deploy-stg',  lambda: (True,  'staging updated'),        gate=None)\n"
    "p.run()\n"
    "p.report()\n"
),
"expected_output": (
    "Stage [---] build: PASS \u2014 compiled OK\n"
    "Stage [COVERAGE] unit-tests: PASS \u2014 847 tests, 0 failures\n"
    "Stage [---] e2e-tests: FAIL \u2014 3 scenarios failed\n"
    "BLOCKED: deploy-stg\n"
    "=== Pipeline: DAKI Platform ===\n"
    "Stages: 2/4 passed\n"
    "Status: PIPELINE FAIL"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Has dominado la infraestructura de QA. "
    "Este contrato integra stages, gates, fail-fast y reporting en un pipeline enterprise."
),
"theory_content": (
    "## Pipeline Enterprise\n\n"
    "Un pipeline enterprise integra:\n\n"
    "- **Fail-fast**: si un stage falla, los siguientes se bloquean\n"
    "- **Gates**: etiquetas que indican el tipo de validación\n"
    "- **Reporting**: resumen ejecutivo para stakeholders\n\n"
    "Este es el patrón que usan equipos de ingeniería en empresas de nivel enterprise."
),
"pedagogical_objective": "Implementar un pipeline enterprise completo con gates, fail-fast y reporte ejecutivo.",
"syntax_hint": "El gate `None` se muestra como `'---'`. Usa `fn()` que retorna `(bool, str)`.",
"hints_json": json.dumps([
    "run: blocked=False, passed=0. Para cada stage: si blocked: print BLOCKED: {name}; agrega a _results como fail; continúa.",
    "Si no blocked: success, msg = stage['fn'](); gate_label = stage['gate'] or '---'; print Stage [{gate_label}] {name}: PASS/FAIL — {msg}.",
    "report: total=len(_results), passed=sum(1 for r in _results if r); print encabezado, stages count, PIPELINE PASS/FAIL.",
]),
"grid_map_json": None,
},
]
