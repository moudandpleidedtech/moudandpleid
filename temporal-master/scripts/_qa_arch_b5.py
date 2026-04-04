"""
_qa_arch_b5.py — QA Senior Architect · BLOQUE 5 (L81–L100)
===========================================================
Fase: perf_liderazgo — Performance Engineering & QA Leadership
Niveles: 81 a 100 (20 desafíos Python)
Boss final: L100 — El Arquitecto Centinela
"""
from __future__ import annotations

_BASE = dict(
    codex_id        = "qa_senior_architect",
    sector_id       = 20,
    challenge_type  = "python",
    phase           = "perf_liderazgo",
    difficulty_tier = 3,
    base_xp_reward  = 300,
    is_free         = False,
    strict_match    = False,
    is_phase_boss   = False,
    is_project      = False,
)

# ─────────────────────────────────────────────────────────────────────────────
# L81 — Load Test Planner
# ─────────────────────────────────────────────────────────────────────────────
L81 = dict(
    **_BASE,
    level_order   = 81,
    title         = "Load Test Planner",
    difficulty    = "hard",
    base_xp_reward = 310,
    description   = (
        "Implementa `plan_load_test(endpoints, users, ramp_seconds)` que, dado un "
        "listado de endpoints con sus pesos relativos, distribuye los usuarios virtuales "
        "proporcionalmente y calcula el tiempo de ramp-up por endpoint.\n\n"
        "Cada endpoint es un dict `{'path': str, 'weight': int}`. "
        "Los usuarios se distribuyen según `weight / total_weight * users` (floor). "
        "El sobrante va al endpoint de mayor peso. "
        "El ramp_step = `ramp_seconds / users` (redondeado a 2 decimales).\n\n"
        "Imprime por endpoint: `path  users=N  ramp_step=Xs`."
    ),
    syntax_hint   ="Usa floor division y asigna el sobrante al endpoint con mayor weight.",
    initial_code  = (
        "def plan_load_test(endpoints, users, ramp_seconds):\n"
        "    # distribuye usuarios y calcula ramp_step por endpoint\n"
        "    pass\n\n"
        "endpoints = [\n"
        "    {'path': '/api/login',    'weight': 3},\n"
        "    {'path': '/api/search',   'weight': 5},\n"
        "    {'path': '/api/checkout', 'weight': 2},\n"
        "]\n"
        "plan_load_test(endpoints, users=100, ramp_seconds=30)\n"
    ),
    expected_output = (
        "/api/login     users=30  ramp_step=0.3s\n"
        "/api/search    users=50  ramp_step=0.3s\n"
        "/api/checkout  users=20  ramp_step=0.3s"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L82 — Response Time Percentiles
# ─────────────────────────────────────────────────────────────────────────────
L82 = dict(
    **_BASE,
    level_order   = 82,
    title         = "Response Time Percentiles",
    difficulty    = "hard",
    base_xp_reward = 320,
    description   = (
        "Implementa `percentile_report(samples)` que calcula P50, P90, P95 y P99 "
        "de una lista de tiempos de respuesta (ms) y los imprime.\n\n"
        "Usa la fórmula: índice = ceil(p/100 * n) - 1 (lista ordenada, base 0). "
        "Imprime: `P50=Xms  P90=Xms  P95=Xms  P99=Xms`.\n\n"
        "Luego evalúa SLA: si P95 > 500ms imprime `SLA BREACH: P95` y si P99 > 1000ms "
        "imprime `SLA BREACH: P99`. Si no hay breach imprime `SLA OK`."
    ),
    syntax_hint   ="Importa math.ceil. Ordena la lista antes de indexar.",
    initial_code  = (
        "import math\n\n"
        "def percentile_report(samples):\n"
        "    pass\n\n"
        "times = [120, 95, 340, 210, 88, 455, 670, 820, 150, 310,\n"
        "         190, 430, 560, 730, 980, 1100, 75, 260, 390, 480]\n"
        "percentile_report(times)\n"
    ),
    expected_output = (
        "P50=350ms  P90=826ms  P95=981ms  P99=1100ms\n"
        "SLA BREACH: P95\n"
        "SLA BREACH: P99"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L83 — Throughput Calculator
# ─────────────────────────────────────────────────────────────────────────────
L83 = dict(
    **_BASE,
    level_order   = 83,
    title         = "Throughput Calculator",
    difficulty    = "medium",
    difficulty_tier = 2,
    base_xp_reward = 250,
    description   = (
        "Implementa `throughput_report(windows)` donde `windows` es una lista de "
        "dicts `{'start': int, 'end': int, 'requests': int}` (tiempos en segundos).\n\n"
        "Para cada ventana calcula: `rps = requests / (end - start)` (2 decimales). "
        "Imprime: `Window N: Xrps (X req / Xs)`.\n\n"
        "Al final imprime: `Peak: Xrps` y `Average: Xrps` (media de todos los rps, 2 dec)."
    ),
    syntax_hint   ="Guarda todos los rps para calcular peak y average al final.",
    initial_code  = (
        "def throughput_report(windows):\n"
        "    pass\n\n"
        "windows = [\n"
        "    {'start': 0,  'end': 10, 'requests': 320},\n"
        "    {'start': 10, 'end': 20, 'requests': 580},\n"
        "    {'start': 20, 'end': 30, 'requests': 470},\n"
        "    {'start': 30, 'end': 40, 'requests': 610},\n"
        "]\n"
        "throughput_report(windows)\n"
    ),
    expected_output = (
        "Window 1: 32.00rps (320 req / 10s)\n"
        "Window 2: 58.00rps (580 req / 10s)\n"
        "Window 3: 47.00rps (470 req / 10s)\n"
        "Window 4: 61.00rps (610 req / 10s)\n"
        "Peak: 61.00rps\n"
        "Average: 49.50rps"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L84 — Resource Monitor
# ─────────────────────────────────────────────────────────────────────────────
L84 = dict(
    **_BASE,
    level_order   = 84,
    title         = "Resource Monitor",
    difficulty    = "medium",
    difficulty_tier = 2,
    base_xp_reward = 260,
    description   = (
        "Implementa `monitor_resources(snapshots)` que analiza snapshots del sistema "
        "durante una prueba de carga.\n\n"
        "Cada snapshot: `{'t': int, 'cpu': float, 'mem': float, 'errors': int}`.\n\n"
        "Imprime cada snapshot: `t=Xs  cpu=X%  mem=X%  errors=N`.\n"
        "Luego imprime el snapshot de mayor cpu con prefijo `Peak CPU:` "
        "y el de mayor mem con prefijo `Peak MEM:`.\n"
        "Finalmente: `Total errors: N`."
    ),
    syntax_hint   ="Usa max() con key= para encontrar los picos.",
    initial_code  = (
        "def monitor_resources(snapshots):\n"
        "    pass\n\n"
        "snaps = [\n"
        "    {'t': 0,  'cpu': 22.0, 'mem': 45.0, 'errors': 0},\n"
        "    {'t': 10, 'cpu': 68.5, 'mem': 62.0, 'errors': 3},\n"
        "    {'t': 20, 'cpu': 91.2, 'mem': 78.5, 'errors': 7},\n"
        "    {'t': 30, 'cpu': 55.0, 'mem': 88.3, 'errors': 2},\n"
        "]\n"
        "monitor_resources(snaps)\n"
    ),
    expected_output = (
        "t=0s   cpu=22.0%  mem=45.0%  errors=0\n"
        "t=10s  cpu=68.5%  mem=62.0%  errors=3\n"
        "t=20s  cpu=91.2%  mem=78.5%  errors=7\n"
        "t=30s  cpu=55.0%  mem=88.3%  errors=2\n"
        "Peak CPU: t=20s cpu=91.2%\n"
        "Peak MEM: t=30s mem=88.3%\n"
        "Total errors: 12"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L85 — Stress Test Escalator
# ─────────────────────────────────────────────────────────────────────────────
L85 = dict(
    **_BASE,
    level_order   = 85,
    title         = "Stress Test Escalator",
    difficulty    = "hard",
    base_xp_reward = 340,
    description   = (
        "Implementa `stress_escalate(stages)` que simula un test de estrés escalonado.\n\n"
        "Cada stage: `{'users': int, 'error_rate': float, 'avg_ms': float}`.\n\n"
        "Recorre los stages en orden. Para cada uno imprime:\n"
        "`Stage N: users=X  errors=X%  avg=Xms  → [OK|DEGRADED|BROKEN]`\n\n"
        "Reglas de estado:\n"
        "- `BROKEN`   si error_rate > 10 o avg_ms > 2000\n"
        "- `DEGRADED` si error_rate > 2  o avg_ms > 800\n"
        "- `OK`       en otro caso\n\n"
        "Si un stage es BROKEN, imprime `System broke at stage N` y detén la escalada."
    ),
    syntax_hint   ="Evalúa BROKEN antes que DEGRADED. Break al detectar BROKEN.",
    initial_code  = (
        "def stress_escalate(stages):\n"
        "    pass\n\n"
        "stages = [\n"
        "    {'users': 50,  'error_rate': 0.5, 'avg_ms': 210.0},\n"
        "    {'users': 100, 'error_rate': 1.8, 'avg_ms': 480.0},\n"
        "    {'users': 200, 'error_rate': 4.2, 'avg_ms': 950.0},\n"
        "    {'users': 400, 'error_rate': 15.0,'avg_ms': 2400.0},\n"
        "    {'users': 800, 'error_rate': 45.0,'avg_ms': 6000.0},\n"
        "]\n"
        "stress_escalate(stages)\n"
    ),
    expected_output = (
        "Stage 1: users=50   errors=0.5%  avg=210.0ms  → OK\n"
        "Stage 2: users=100  errors=1.8%  avg=480.0ms  → OK\n"
        "Stage 3: users=200  errors=4.2%  avg=950.0ms  → DEGRADED\n"
        "Stage 4: users=400  errors=15.0%  avg=2400.0ms  → BROKEN\n"
        "System broke at stage 4"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L86 — Spike Test Simulator
# ─────────────────────────────────────────────────────────────────────────────
L86 = dict(
    **_BASE,
    level_order   = 86,
    title         = "Spike Test Simulator",
    difficulty    = "hard",
    base_xp_reward = 360,
    description   = (
        "Implementa `spike_test(baseline_rps, spike_rps, spike_duration, recovery_sla_s)` "
        "que simula un spike test en 4 fases:\n\n"
        "1. **Baseline** — imprime `[BASELINE] Xrps — stable`\n"
        "2. **Spike**    — imprime `[SPIKE] Xrps — X concurrent users estimated`\n"
        "   (concurrent = spike_rps * 2, entero)\n"
        "3. **Recovery** — imprime `[RECOVERY] duration=Xs SLA=Xs → [PASS|FAIL]`\n"
        "   PASS si spike_duration <= recovery_sla_s, FAIL en otro caso\n"
        "4. **Result**   — imprime `Spike ratio: Xx` (spike_rps/baseline_rps, 1 decimal)\n"
        "   Luego `Verdict: [RESILIENT|FRAGILE]`: RESILIENT si ratio < 5, FRAGILE si ratio >= 5"
    ),
    syntax_hint   ="Calcula concurrent = spike_rps * 2. ratio = spike_rps / baseline_rps.",
    initial_code  = (
        "def spike_test(baseline_rps, spike_rps, spike_duration, recovery_sla_s):\n"
        "    pass\n\n"
        "spike_test(baseline_rps=100, spike_rps=800,\n"
        "           spike_duration=45, recovery_sla_s=30)\n"
    ),
    expected_output = (
        "[BASELINE] 100rps — stable\n"
        "[SPIKE] 800rps — 1600 concurrent users estimated\n"
        "[RECOVERY] duration=45s SLA=30s → FAIL\n"
        "Spike ratio: 8.0x\n"
        "Verdict: FRAGILE"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L87 — Endurance Test Monitor
# ─────────────────────────────────────────────────────────────────────────────
L87 = dict(
    **_BASE,
    level_order   = 87,
    title         = "Endurance Test Monitor",
    difficulty    = "hard",
    base_xp_reward = 370,
    description   = (
        "Implementa `endurance_monitor(hourly_stats)` que analiza un test de resistencia "
        "de varias horas.\n\n"
        "Cada stat: `{'hour': int, 'avg_ms': float, 'mem_mb': float, 'errors': int}`.\n\n"
        "Imprime cada hora: `Hour X: avg=Xms  mem=XMB  errors=N`.\n\n"
        "Detecta degradación progresiva:\n"
        "- **Memory leak**: si mem_mb crece más de 50MB entre hora 1 y última hora → imprime "
        "`WARNING: possible memory leak (+XMB)`\n"
        "- **Latency drift**: si avg_ms de la última hora > avg_ms de hora 1 * 1.3 → imprime "
        "`WARNING: latency drift (+X%)`\n"
        "- Si no hay warnings → imprime `Endurance: STABLE`"
    ),
    syntax_hint   ="Compara first vs last para detectar drift. El % es int((last/first - 1)*100).",
    initial_code  = (
        "def endurance_monitor(hourly_stats):\n"
        "    pass\n\n"
        "stats = [\n"
        "    {'hour': 1, 'avg_ms': 210.0, 'mem_mb': 512.0, 'errors': 0},\n"
        "    {'hour': 2, 'avg_ms': 218.0, 'mem_mb': 538.0, 'errors': 1},\n"
        "    {'hour': 3, 'avg_ms': 235.0, 'mem_mb': 567.0, 'errors': 0},\n"
        "    {'hour': 4, 'avg_ms': 290.0, 'mem_mb': 601.0, 'errors': 3},\n"
        "    {'hour': 5, 'avg_ms': 340.0, 'mem_mb': 648.0, 'errors': 2},\n"
        "]\n"
        "endurance_monitor(stats)\n"
    ),
    expected_output = (
        "Hour 1: avg=210.0ms  mem=512.0MB  errors=0\n"
        "Hour 2: avg=218.0ms  mem=538.0MB  errors=1\n"
        "Hour 3: avg=235.0ms  mem=567.0MB  errors=0\n"
        "Hour 4: avg=290.0ms  mem=601.0MB  errors=3\n"
        "Hour 5: avg=340.0ms  mem=648.0MB  errors=2\n"
        "WARNING: possible memory leak (+136.0MB)\n"
        "WARNING: latency drift (+61%)"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L88 — SLA Compliance Checker
# ─────────────────────────────────────────────────────────────────────────────
L88 = dict(
    **_BASE,
    level_order   = 88,
    title         = "SLA Compliance Checker",
    difficulty    = "medium",
    difficulty_tier = 2,
    base_xp_reward = 280,
    description   = (
        "Implementa `sla_report(services)` que verifica SLAs para múltiples servicios.\n\n"
        "Cada servicio: `{'name': str, 'uptime_pct': float, 'p95_ms': float, "
        "'error_rate': float, 'sla': dict}`.\n\n"
        "El SLA define: `{'uptime': float, 'p95_ms': float, 'error_rate': float}`.\n\n"
        "Para cada servicio imprime:\n"
        "`<name>: uptime=[OK|BREACH] p95=[OK|BREACH] errors=[OK|BREACH] → [COMPLIANT|NON-COMPLIANT]`\n\n"
        "BREACH si el valor medido supera el límite SLA (uptime: menor es breach; "
        "p95_ms y error_rate: mayor es breach).\n"
        "COMPLIANT solo si los 3 checks son OK.\n\n"
        "Al final: `Compliant: N/M services`."
    ),
    syntax_hint   ="uptime breach si medido < sla.uptime. Los otros: medido > sla.",
    initial_code  = (
        "def sla_report(services):\n"
        "    pass\n\n"
        "services = [\n"
        "    {'name': 'auth-service',    'uptime_pct': 99.95, 'p95_ms': 280.0,  'error_rate': 0.1,\n"
        "     'sla': {'uptime': 99.9,    'p95_ms': 500.0, 'error_rate': 1.0}},\n"
        "    {'name': 'payment-service', 'uptime_pct': 99.7,  'p95_ms': 620.0,  'error_rate': 0.8,\n"
        "     'sla': {'uptime': 99.9,    'p95_ms': 500.0, 'error_rate': 1.0}},\n"
        "    {'name': 'search-service',  'uptime_pct': 98.5,  'p95_ms': 180.0,  'error_rate': 2.5,\n"
        "     'sla': {'uptime': 99.0,    'p95_ms': 300.0, 'error_rate': 2.0}},\n"
        "]\n"
        "sla_report(services)\n"
    ),
    expected_output = (
        "auth-service: uptime=OK p95=OK errors=OK → COMPLIANT\n"
        "payment-service: uptime=BREACH p95=BREACH errors=OK → NON-COMPLIANT\n"
        "search-service: uptime=BREACH p95=OK errors=BREACH → NON-COMPLIANT\n"
        "Compliant: 1/3 services"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L89 — Security Header Scanner
# ─────────────────────────────────────────────────────────────────────────────
L89 = dict(
    **_BASE,
    level_order   = 89,
    title         = "Security Header Scanner",
    difficulty    = "medium",
    difficulty_tier = 2,
    base_xp_reward = 290,
    description   = (
        "Implementa `scan_headers(responses)` que analiza las cabeceras de seguridad "
        "de varias respuestas HTTP simuladas.\n\n"
        "Headers requeridos (mínimo): `Content-Security-Policy`, `X-Frame-Options`, "
        "`X-Content-Type-Options`, `Strict-Transport-Security`.\n\n"
        "Para cada respuesta imprime:\n"
        "`<url>  score=N/4  [SECURE|INSECURE]`\n\n"
        "SECURE si score == 4. Luego lista los headers faltantes con `  MISSING: <header>`.\n\n"
        "Al final: `Overall: N/M endpoints secure`."
    ),
    syntax_hint   ="Itera sobre la lista de headers requeridos y verifica su presencia en el dict.",
    initial_code  = (
        "def scan_headers(responses):\n"
        "    pass\n\n"
        "REQUIRED = [\n"
        "    'Content-Security-Policy',\n"
        "    'X-Frame-Options',\n"
        "    'X-Content-Type-Options',\n"
        "    'Strict-Transport-Security',\n"
        "]\n\n"
        "responses = [\n"
        "    {'url': '/api/login',  'headers': {\n"
        "        'Content-Security-Policy': \"default-src 'self'\",\n"
        "        'X-Frame-Options': 'DENY',\n"
        "        'X-Content-Type-Options': 'nosniff',\n"
        "        'Strict-Transport-Security': 'max-age=31536000',\n"
        "    }},\n"
        "    {'url': '/api/users',  'headers': {\n"
        "        'X-Frame-Options': 'SAMEORIGIN',\n"
        "        'X-Content-Type-Options': 'nosniff',\n"
        "    }},\n"
        "    {'url': '/api/public', 'headers': {\n"
        "        'Content-Security-Policy': \"default-src 'self'\",\n"
        "        'X-Content-Type-Options': 'nosniff',\n"
        "    }},\n"
        "]\n"
        "scan_headers(responses)\n"
    ),
    expected_output = (
        "/api/login   score=4/4  SECURE\n"
        "/api/users   score=2/4  INSECURE\n"
        "  MISSING: Content-Security-Policy\n"
        "  MISSING: Strict-Transport-Security\n"
        "/api/public  score=2/4  INSECURE\n"
        "  MISSING: X-Frame-Options\n"
        "  MISSING: Strict-Transport-Security\n"
        "Overall: 1/3 endpoints secure"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L90 — SQL Injection Detector
# ─────────────────────────────────────────────────────────────────────────────
L90 = dict(
    **_BASE,
    level_order   = 90,
    title         = "SQL Injection Detector",
    difficulty    = "hard",
    base_xp_reward = 400,
    description   = (
        "Implementa `detect_sqli(inputs)` que analiza strings de entrada para detectar "
        "patrones típicos de SQL injection.\n\n"
        "Patrones a detectar (case-insensitive): `' OR`, `; DROP`, `--`, `UNION SELECT`, "
        "`1=1`, `' AND`.\n\n"
        "Para cada input imprime:\n"
        "`[SAFE|SUSPICIOUS] <input>`\n\n"
        "Si es SUSPICIOUS, lista en la siguiente línea los patrones detectados: "
        "`  Patterns: pattern1, pattern2`\n\n"
        "Al final: `Flagged: N/M inputs`."
    ),
    syntax_hint   ="Usa in con lower(). Un input puede tener múltiples patrones.",
    initial_code  = (
        "def detect_sqli(inputs):\n"
        "    pass\n\n"
        "PATTERNS = [\"' OR\", \"; DROP\", \"--\", \"UNION SELECT\", \"1=1\", \"' AND\"]\n\n"
        "test_inputs = [\n"
        "    \"admin\",\n"
        "    \"' OR 1=1 --\",\n"
        "    \"SELECT * FROM users\",\n"
        "    \"; DROP TABLE users;\",\n"
        "    \"john.doe@email.com\",\n"
        "    \"' AND 1=1 UNION SELECT * FROM passwords\",\n"
        "]\n"
        "detect_sqli(test_inputs)\n"
    ),
    expected_output = (
        "[SAFE] admin\n"
        "[SUSPICIOUS] ' OR 1=1 --\n"
        "  Patterns: ' OR, --, 1=1\n"
        "[SAFE] SELECT * FROM users\n"
        "[SUSPICIOUS] ; DROP TABLE users;\n"
        "  Patterns: ; DROP\n"
        "[SAFE] john.doe@email.com\n"
        "[SUSPICIOUS] ' AND 1=1 UNION SELECT * FROM passwords\n"
        "  Patterns: UNION SELECT, 1=1, ' AND\n"
        "Flagged: 3/6 inputs"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L91 — XSS Vulnerability Scanner
# ─────────────────────────────────────────────────────────────────────────────
L91 = dict(
    **_BASE,
    level_order   = 91,
    title         = "XSS Vulnerability Scanner",
    difficulty    = "hard",
    base_xp_reward = 420,
    description   = (
        "Implementa `scan_xss(payloads)` que detecta XSS payloads en inputs simulados.\n\n"
        "Patrones XSS (case-insensitive): `<script`, `javascript:`, `onerror=`, "
        "`onload=`, `alert(`, `document.cookie`.\n\n"
        "Para cada payload: `[SAFE|XSS] <payload>`\n"
        "Si es XSS: `  Vectors: v1, v2`\n\n"
        "Severidad al final:\n"
        "- `<script` o `document.cookie` → HIGH\n"
        "- otros → MEDIUM\n\n"
        "Imprime por cada XSS: `  Severity: HIGH|MEDIUM`\n\n"
        "Resumen final: `XSS found: N  High: N  Medium: N`."
    ),
    syntax_hint   ="Evalúa severidad revisando si algún vector HIGH está en los patrones detectados.",
    initial_code  = (
        "def scan_xss(payloads):\n"
        "    pass\n\n"
        "VECTORS = ['<script', 'javascript:', 'onerror=', 'onload=', 'alert(', 'document.cookie']\n"
        "HIGH_VECTORS = {'<script', 'document.cookie'}\n\n"
        "test_payloads = [\n"
        "    'Hello World',\n"
        "    '<script>alert(1)</script>',\n"
        "    '<img src=x onerror=alert(document.cookie)>',\n"
        "    'Normal <b>bold</b> text',\n"
        "    'javascript:void(0)',\n"
        "]\n"
        "scan_xss(test_payloads)\n"
    ),
    expected_output = (
        "[SAFE] Hello World\n"
        "[XSS] <script>alert(1)</script>\n"
        "  Vectors: <script, alert(\n"
        "  Severity: HIGH\n"
        "[XSS] <img src=x onerror=alert(document.cookie)>\n"
        "  Vectors: onerror=, alert(, document.cookie\n"
        "  Severity: HIGH\n"
        "[SAFE] Normal <b>bold</b> text\n"
        "[XSS] javascript:void(0)\n"
        "  Vectors: javascript:\n"
        "  Severity: MEDIUM\n"
        "XSS found: 3  High: 2  Medium: 1"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L92 — OWASP Top 10 Checklist
# ─────────────────────────────────────────────────────────────────────────────
L92 = dict(
    **_BASE,
    level_order   = 92,
    title         = "OWASP Top 10 Checklist",
    difficulty    = "hard",
    base_xp_reward = 440,
    description   = (
        "Implementa `owasp_audit(findings)` que evalúa un listado de hallazgos de seguridad "
        "contra el OWASP Top 10.\n\n"
        "Cada finding: `{'id': str, 'category': str, 'severity': str, 'mitigated': bool}`.\n\n"
        "Categorías OWASP mapeadas (las que debes cubrir):\n"
        "`A01: Broken Access Control`, `A02: Cryptographic Failures`, `A03: Injection`, "
        "`A07: XSS`, `A09: Security Logging Failures`.\n\n"
        "Imprime cada finding:\n"
        "`[OPEN|CLOSED] <id>: <category> — severity=<severity>`\n\n"
        "CLOSED si mitigated=True.\n\n"
        "Resumen: `Open: N  Closed: N  Critical open: N`\n"
        "Critical open = findings con severity='critical' y mitigated=False."
    ),
    syntax_hint   ="Itera los findings, imprime estado y cuenta en una pasada.",
    initial_code  = (
        "def owasp_audit(findings):\n"
        "    pass\n\n"
        "findings = [\n"
        "    {'id': 'F-001', 'category': 'A01: Broken Access Control',    'severity': 'critical', 'mitigated': False},\n"
        "    {'id': 'F-002', 'category': 'A03: Injection',                'severity': 'critical', 'mitigated': True},\n"
        "    {'id': 'F-003', 'category': 'A07: XSS',                      'severity': 'high',     'mitigated': False},\n"
        "    {'id': 'F-004', 'category': 'A02: Cryptographic Failures',   'severity': 'medium',   'mitigated': False},\n"
        "    {'id': 'F-005', 'category': 'A09: Security Logging Failures','severity': 'low',      'mitigated': True},\n"
        "]\n"
        "owasp_audit(findings)\n"
    ),
    expected_output = (
        "[OPEN]   F-001: A01: Broken Access Control — severity=critical\n"
        "[CLOSED] F-002: A03: Injection — severity=critical\n"
        "[OPEN]   F-003: A07: XSS — severity=high\n"
        "[OPEN]   F-004: A02: Cryptographic Failures — severity=medium\n"
        "[CLOSED] F-005: A09: Security Logging Failures — severity=low\n"
        "Open: 3  Closed: 2  Critical open: 1"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L93 — Test Team Capacity Planner
# ─────────────────────────────────────────────────────────────────────────────
L93 = dict(
    **_BASE,
    level_order   = 93,
    title         = "Test Team Capacity Planner",
    difficulty    = "medium",
    difficulty_tier = 2,
    base_xp_reward = 310,
    description   = (
        "Implementa `capacity_plan(engineers, sprints)` que distribuye el trabajo de QA "
        "entre ingenieros en múltiples sprints.\n\n"
        "Cada engineer: `{'name': str, 'hours_per_sprint': int}`.\n"
        "Cada sprint: `{'id': int, 'tasks': list[dict]}`.\n"
        "Cada task: `{'name': str, 'hours': int}`.\n\n"
        "Asigna tareas a ingenieros usando round-robin por orden de lista. "
        "Imprime por sprint: `Sprint N:` luego cada tarea asignada: "
        "`  <task> → <engineer> (Xh)`.\n\n"
        "Al final imprime la carga total por ingeniero: "
        "`Load: <name>=Xh`."
    ),
    syntax_hint   ="Usa un índice circular (i % len(engineers)) para round-robin.",
    initial_code  = (
        "def capacity_plan(engineers, sprints):\n"
        "    pass\n\n"
        "engineers = [\n"
        "    {'name': 'Ana',   'hours_per_sprint': 40},\n"
        "    {'name': 'Bruno', 'hours_per_sprint': 40},\n"
        "    {'name': 'Cata',  'hours_per_sprint': 32},\n"
        "]\n"
        "sprints = [\n"
        "    {'id': 1, 'tasks': [\n"
        "        {'name': 'regression-suite', 'hours': 8},\n"
        "        {'name': 'api-tests',        'hours': 6},\n"
        "        {'name': 'e2e-login',        'hours': 4},\n"
        "        {'name': 'perf-baseline',    'hours': 5},\n"
        "    ]},\n"
        "    {'id': 2, 'tasks': [\n"
        "        {'name': 'smoke-tests',      'hours': 3},\n"
        "        {'name': 'security-scan',    'hours': 7},\n"
        "    ]},\n"
        "]\n"
        "capacity_plan(engineers, sprints)\n"
    ),
    expected_output = (
        "Sprint 1:\n"
        "  regression-suite → Ana (8h)\n"
        "  api-tests → Bruno (6h)\n"
        "  e2e-login → Cata (4h)\n"
        "  perf-baseline → Ana (5h)\n"
        "Sprint 2:\n"
        "  smoke-tests → Bruno (3h)\n"
        "  security-scan → Cata (7h)\n"
        "Load: Ana=13h\n"
        "Load: Bruno=9h\n"
        "Load: Cata=11h"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L94 — Quality Dashboard Builder
# ─────────────────────────────────────────────────────────────────────────────
L94 = dict(
    **_BASE,
    level_order   = 94,
    title         = "Quality Dashboard Builder",
    difficulty    = "hard",
    base_xp_reward = 450,
    description   = (
        "Implementa `build_dashboard(metrics)` que construye un dashboard de calidad "
        "en texto.\n\n"
        "metrics: dict con claves:\n"
        "- `test_runs`: list de `{'suite': str, 'passed': int, 'failed': int, 'skipped': int}`\n"
        "- `coverage`: float (0-100)\n"
        "- `open_bugs`: int\n"
        "- `mttr_hours`: float (mean time to resolve)\n\n"
        "Imprime el dashboard con este formato exacto:\n"
        "```\n"
        "╔══════════════════════════════════╗\n"
        "║     QUALITY DASHBOARD — DAKI     ║\n"
        "╠══════════════════════════════════╣\n"
        "║ Suite            P    F    S     ║\n"
        "║ <suite padded>   N    N    N     ║\n"
        "╠══════════════════════════════════╣\n"
        "║ Coverage : XX.X%                 ║\n"
        "║ Open bugs: N                     ║\n"
        "║ MTTR     : X.Xh                  ║\n"
        "║ Status   : [GREEN|YELLOW|RED]    ║\n"
        "╚══════════════════════════════════╝\n"
        "```\n"
        "Status: GREEN si coverage>=80 y open_bugs<=5 y failed_total==0; "
        "RED si coverage<60 o open_bugs>20 o failed_total>10; YELLOW en otro caso."
    ),
    syntax_hint   ="Usa ljust/rjust para alinear columnas. Calcula failed_total sumando todos los suites.",
    initial_code  = (
        "def build_dashboard(metrics):\n"
        "    pass\n\n"
        "metrics = {\n"
        "    'test_runs': [\n"
        "        {'suite': 'unit',       'passed': 312, 'failed': 0, 'skipped': 5},\n"
        "        {'suite': 'integration','passed':  88, 'failed': 2, 'skipped': 1},\n"
        "        {'suite': 'e2e',        'passed':  45, 'failed': 1, 'skipped': 3},\n"
        "    ],\n"
        "    'coverage': 76.4,\n"
        "    'open_bugs': 8,\n"
        "    'mttr_hours': 4.5,\n"
        "}\n"
        "build_dashboard(metrics)\n"
    ),
    expected_output = (
        "╔══════════════════════════════════╗\n"
        "║     QUALITY DASHBOARD — DAKI     ║\n"
        "╠══════════════════════════════════╣\n"
        "║ Suite            P    F    S     ║\n"
        "║ unit             312  0    5     ║\n"
        "║ integration      88   2    1     ║\n"
        "║ e2e              45   1    3     ║\n"
        "╠══════════════════════════════════╣\n"
        "║ Coverage : 76.4%                 ║\n"
        "║ Open bugs: 8                     ║\n"
        "║ MTTR     : 4.5h                  ║\n"
        "║ Status   : YELLOW                ║\n"
        "╚══════════════════════════════════╝"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L95 — Mentoring Session Planner
# ─────────────────────────────────────────────────────────────────────────────
L95 = dict(
    **_BASE,
    level_order   = 95,
    title         = "Mentoring Session Planner",
    difficulty    = "medium",
    difficulty_tier = 2,
    base_xp_reward = 330,
    description   = (
        "Implementa `plan_mentoring(juniors)` que crea un plan de mentoring para un equipo.\n\n"
        "Cada junior: `{'name': str, 'level': int, 'weak_areas': list[str]}`.\n\n"
        "Para cada junior imprime:\n"
        "`<name> (L<level>):`\n"
        "Luego lista los temas a trabajar según sus áreas débiles con prefijo `  - `.\n\n"
        "Prioridad: juniors con nivel <= 2 reciben etiqueta `[PRIORITY]` antes del nombre.\n\n"
        "Al final imprime: `Sessions planned: N` (una por junior) y "
        "`Priority engineers: N`."
    ),
    syntax_hint   ="Imprime [PRIORITY] solo si level <= 2. Cuenta prioridad al mismo tiempo.",
    initial_code  = (
        "def plan_mentoring(juniors):\n"
        "    pass\n\n"
        "team = [\n"
        "    {'name': 'Luca',  'level': 1, 'weak_areas': ['pytest fixtures', 'test design']},\n"
        "    {'name': 'Mia',   'level': 3, 'weak_areas': ['API testing', 'CI/CD']},\n"
        "    {'name': 'Omar',  'level': 2, 'weak_areas': ['Playwright', 'performance']},\n"
        "    {'name': 'Petra', 'level': 4, 'weak_areas': ['contract testing']},\n"
        "]\n"
        "plan_mentoring(team)\n"
    ),
    expected_output = (
        "[PRIORITY] Luca (L1):\n"
        "  - pytest fixtures\n"
        "  - test design\n"
        "Mia (L3):\n"
        "  - API testing\n"
        "  - CI/CD\n"
        "[PRIORITY] Omar (L2):\n"
        "  - Playwright\n"
        "  - performance\n"
        "Petra (L4):\n"
        "  - contract testing\n"
        "Sessions planned: 4\n"
        "Priority engineers: 2"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L96 — Incident Post-Mortem Template
# ─────────────────────────────────────────────────────────────────────────────
L96 = dict(
    **_BASE,
    level_order   = 96,
    title         = "Incident Post-Mortem Template",
    difficulty    = "medium",
    difficulty_tier = 2,
    base_xp_reward = 340,
    description   = (
        "Implementa `generate_postmortem(incident)` que produce un post-mortem estructurado.\n\n"
        "incident: dict con: `id`, `title`, `severity`, `duration_min`, `impact`, "
        "`root_cause`, `timeline` (list de `{'t': str, 'event': str}`), "
        "`action_items` (list de `{'owner': str, 'task': str, 'due': str}`).\n\n"
        "Formato de salida:\n"
        "```\n"
        "POST-MORTEM: <id> — <title>\n"
        "Severity: <severity>  Duration: <N>min  Impact: <impact>\n"
        "\n"
        "ROOT CAUSE:\n"
        "  <root_cause>\n"
        "\n"
        "TIMELINE:\n"
        "  <t> — <event>\n"
        "\n"
        "ACTION ITEMS:\n"
        "  [<owner>] <task> (due: <due>)\n"
        "```"
    ),
    syntax_hint   ="Itera timeline y action_items con el formato exacto.",
    initial_code  = (
        "def generate_postmortem(incident):\n"
        "    pass\n\n"
        "incident = {\n"
        "    'id': 'INC-2024-047',\n"
        "    'title': 'Payment API Outage',\n"
        "    'severity': 'P1',\n"
        "    'duration_min': 47,\n"
        "    'impact': '12% of checkout flows failed',\n"
        "    'root_cause': 'DB connection pool exhausted due to missing index on orders table',\n"
        "    'timeline': [\n"
        "        {'t': '14:03', 'event': 'Alerts fired: payment timeout spike'},\n"
        "        {'t': '14:11', 'event': 'On-call engineer paged'},\n"
        "        {'t': '14:28', 'event': 'Root cause identified: missing index'},\n"
        "        {'t': '14:50', 'event': 'Index deployed, service recovered'},\n"
        "    ],\n"
        "    'action_items': [\n"
        "        {'owner': 'DB team',  'task': 'Add migration linter for missing indexes', 'due': '2024-02-15'},\n"
        "        {'owner': 'QA team',  'task': 'Add DB performance test to CI pipeline',   'due': '2024-02-20'},\n"
        "        {'owner': 'Platform', 'task': 'Improve connection pool monitoring alerts', 'due': '2024-02-28'},\n"
        "    ],\n"
        "}\n"
        "generate_postmortem(incident)\n"
    ),
    expected_output = (
        "POST-MORTEM: INC-2024-047 — Payment API Outage\n"
        "Severity: P1  Duration: 47min  Impact: 12% of checkout flows failed\n"
        "\n"
        "ROOT CAUSE:\n"
        "  DB connection pool exhausted due to missing index on orders table\n"
        "\n"
        "TIMELINE:\n"
        "  14:03 — Alerts fired: payment timeout spike\n"
        "  14:11 — On-call engineer paged\n"
        "  14:28 — Root cause identified: missing index\n"
        "  14:50 — Index deployed, service recovered\n"
        "\n"
        "ACTION ITEMS:\n"
        "  [DB team] Add migration linter for missing indexes (due: 2024-02-15)\n"
        "  [QA team] Add DB performance test to CI pipeline (due: 2024-02-20)\n"
        "  [Platform] Improve connection pool monitoring alerts (due: 2024-02-28)"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L97 — Test Maturity Assessment
# ─────────────────────────────────────────────────────────────────────────────
L97 = dict(
    **_BASE,
    level_order   = 97,
    title         = "Test Maturity Assessment",
    difficulty    = "hard",
    base_xp_reward = 480,
    description   = (
        "Implementa `maturity_assessment(org)` que evalúa la madurez de pruebas de una organización "
        "usando un modelo de 5 dimensiones, cada una con score 0-4.\n\n"
        "Dimensiones: `strategy`, `automation`, `tooling`, `process`, `culture`.\n\n"
        "Niveles de madurez:\n"
        "- 0-1: Initial, 2: Managed, 3: Defined, 4: Optimized\n\n"
        "Para cada dimensión imprime:\n"
        "`  <dimension>: <score>/4 — <level>`\n\n"
        "Calcula promedio (2 decimales). Nivel general por el mismo criterio.\n\n"
        "Imprime:\n"
        "`Organization: <name>`\n"
        "luego las dimensiones,\n"
        "luego `Overall: <avg>/4 — <level>`.\n\n"
        "Si alguna dimensión tiene score 0: añade `  WARNING: <dimension> needs immediate attention`."
    ),
    syntax_hint   ="Nivel: 0-1 → Initial, 2 → Managed, 3 → Defined, 4 → Optimized. Promedio con round(,2).",
    initial_code  = (
        "def maturity_level(score):\n"
        "    if score <= 1: return 'Initial'\n"
        "    if score == 2: return 'Managed'\n"
        "    if score == 3: return 'Defined'\n"
        "    return 'Optimized'\n\n"
        "def maturity_assessment(org):\n"
        "    pass\n\n"
        "org = {\n"
        "    'name': 'DAKI Platform Team',\n"
        "    'scores': {\n"
        "        'strategy':   3,\n"
        "        'automation': 4,\n"
        "        'tooling':    3,\n"
        "        'process':    2,\n"
        "        'culture':    0,\n"
        "    }\n"
        "}\n"
        "maturity_assessment(org)\n"
    ),
    expected_output = (
        "Organization: DAKI Platform Team\n"
        "  strategy:   3/4 — Defined\n"
        "  automation: 4/4 — Optimized\n"
        "  tooling:    3/4 — Defined\n"
        "  process:    2/4 — Managed\n"
        "  culture:    0/4 — Initial\n"
        "Overall: 2.4/4 — Managed\n"
        "  WARNING: culture needs immediate attention"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L98 — Risk Mitigation Strategist
# ─────────────────────────────────────────────────────────────────────────────
L98 = dict(
    **_BASE,
    level_order   = 98,
    title         = "Risk Mitigation Strategist",
    difficulty    = "hard",
    base_xp_reward = 500,
    description   = (
        "Implementa `risk_matrix(risks)` que construye una matriz de riesgos de QA.\n\n"
        "Cada riesgo: `{'id': str, 'description': str, 'probability': int, "
        "'impact': int, 'mitigation': str}`.\n"
        "probability e impact son enteros 1-5.\n\n"
        "Calcula `score = probability * impact`.\n\n"
        "Clasificación:\n"
        "- score >= 15 → CRITICAL\n"
        "- score >= 8  → HIGH\n"
        "- score >= 4  → MEDIUM\n"
        "- score < 4   → LOW\n\n"
        "Ordena los riesgos por score descendente.\n\n"
        "Imprime: `RISK MATRIX`\n"
        "Luego cada riesgo:\n"
        "`[LEVEL] <id>  score=N  <description>`\n"
        "`  Mitigation: <mitigation>`\n\n"
        "Resumen: `Critical: N  High: N  Medium: N  Low: N`."
    ),
    syntax_hint   ="Ordena con sorted(..., key=lambda r: r['probability']*r['impact'], reverse=True).",
    initial_code  = (
        "def risk_matrix(risks):\n"
        "    pass\n\n"
        "risks = [\n"
        "    {'id': 'R-01', 'description': 'No automated regression suite',\n"
        "     'probability': 4, 'impact': 5, 'mitigation': 'Build Playwright suite in Q1'},\n"
        "    {'id': 'R-02', 'description': 'Single QA engineer on critical path',\n"
        "     'probability': 3, 'impact': 4, 'mitigation': 'Cross-train 2 devs on QA practices'},\n"
        "    {'id': 'R-03', 'description': 'Flaky tests causing false alarms',\n"
        "     'probability': 5, 'impact': 2, 'mitigation': 'Quarantine and fix flaky tests weekly'},\n"
        "    {'id': 'R-04', 'description': 'No performance benchmarks defined',\n"
        "     'probability': 2, 'impact': 3, 'mitigation': 'Define SLAs with product team'},\n"
        "    {'id': 'R-05', 'description': 'Missing security scanning in CI',\n"
        "     'probability': 3, 'impact': 5, 'mitigation': 'Integrate SAST/DAST tools'},\n"
        "]\n"
        "risk_matrix(risks)\n"
    ),
    expected_output = (
        "RISK MATRIX\n"
        "[CRITICAL] R-01  score=20  No automated regression suite\n"
        "  Mitigation: Build Playwright suite in Q1\n"
        "[CRITICAL] R-05  score=15  Missing security scanning in CI\n"
        "  Mitigation: Integrate SAST/DAST tools\n"
        "[HIGH] R-02  score=12  Single QA engineer on critical path\n"
        "  Mitigation: Cross-train 2 devs on QA practices\n"
        "[HIGH] R-03  score=10  Flaky tests causing false alarms\n"
        "  Mitigation: Quarantine and fix flaky tests weekly\n"
        "[MEDIUM] R-04  score=6  No performance benchmarks defined\n"
        "  Mitigation: Define SLAs with product team\n"
        "Critical: 2  High: 2  Medium: 1  Low: 0"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L99 — QA Transformation Roadmap
# ─────────────────────────────────────────────────────────────────────────────
L99 = dict(
    **_BASE,
    level_order   = 99,
    title         = "QA Transformation Roadmap",
    difficulty    = "hard",
    base_xp_reward = 520,
    description   = (
        "Implementa `transformation_roadmap(current_state, target_state, quarters)` que "
        "genera un roadmap de transformación QA.\n\n"
        "`current_state` y `target_state` son dicts con las mismas claves (dimensiones), "
        "cuyos valores son scores enteros 0-4.\n\n"
        "`quarters` es una lista de nombres de quarter, ej. `['Q1 2025', 'Q2 2025', ...]`.\n\n"
        "Para cada dimensión con gap > 0 distribuye el crecimiento equitativamente entre quarters "
        "(floor por quarter, el sobrante en el último).\n\n"
        "Imprime la tabla de roadmap:\n"
        "Primera fila: `Dimension        | Current | ` seguido de quarters separados por ` | `\n"
        "Luego por dimensión con gap > 0: `<dim padded 16> | <cur>     | <val_q1> | <val_q2> ...`\n\n"
        "Cada celda de quarter muestra el score acumulado al final de ese quarter.\n\n"
        "Al final: `Roadmap: <N> dimensions to improve over <M> quarters`."
    ),
    syntax_hint   =(
        "Gap = target - current. Por quarter: floor(gap/M). Valor acumulado = current + step*(i+1), "
        "ajustado en último quarter a target."
    ),
    initial_code  = (
        "import math\n\n"
        "def transformation_roadmap(current_state, target_state, quarters):\n"
        "    pass\n\n"
        "current = {'automation': 1, 'tooling': 2, 'process': 1, 'culture': 2}\n"
        "target  = {'automation': 4, 'tooling': 4, 'process': 3, 'culture': 2}\n"
        "qs = ['Q1', 'Q2', 'Q3']\n"
        "transformation_roadmap(current, target, qs)\n"
    ),
    expected_output = (
        "Dimension        | Current | Q1 | Q2 | Q3\n"
        "automation       | 1       | 2  | 3  | 4\n"
        "tooling          | 2       | 2  | 3  | 4\n"
        "process          | 1       | 1  | 2  | 3\n"
        "Roadmap: 3 dimensions to improve over 3 quarters"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L100 — BOSS FINAL: El Arquitecto Centinela
# ─────────────────────────────────────────────────────────────────────────────
_BASE_BOSS = {k: v for k, v in _BASE.items() if k not in ('is_phase_boss', 'is_project')}

L100 = dict(
    **_BASE_BOSS,
    level_order   = 100,
    title         = "CONTRATO-QA-100: El Arquitecto Centinela",
    difficulty    = "legendary",
    base_xp_reward = 800,
    is_phase_boss = True,
    is_project    = True,
    description   = (
        "Misión final del Arquitecto Centinela. Debes construir `QACommandCenter` — "
        "el sistema integrado que un QA Senior Architect usa para evaluar la salud completa "
        "de una plataforma antes del go-live.\n\n"
        "Implementa la clase con los siguientes métodos:\n\n"
        "1. `add_perf_result(endpoint, p95_ms, error_rate)` — registra resultado de perf\n"
        "2. `add_security_finding(severity, description)` — registra hallazgo de seguridad\n"
        "3. `add_test_suite(name, passed, failed)` — registra suite de pruebas\n"
        "4. `go_live_decision()` — imprime el reporte de decisión final\n\n"
        "Reglas de go_live_decision():\n"
        "- Imprime `=== QA COMMAND CENTER — GO/NO-GO REPORT ===`\n"
        "- Sección PERFORMANCE: lista cada endpoint con estado [OK|WARN|FAIL]\n"
        "  FAIL: p95>1000 o error_rate>5; WARN: p95>500 o error_rate>2; OK: resto\n"
        "- Sección SECURITY: lista cada finding; si severity='critical' → BLOCKER\n"
        "- Sección TEST SUITES: lista cada suite con pass rate (total_passed/total_tests*100, 1 dec)\n"
        "- DECISION: GO si no hay FAIL en perf, no hay critical en security, y todas las suites "
        "tienen pass_rate >= 95; NO-GO en otro caso con lista de razones\n"
        "- Última línea: `DECISION: GO` o `DECISION: NO-GO`"
    ),
    syntax_hint   =(
        "Guarda listas internas en __init__. go_live_decision() recorre cada lista y acumula "
        "razones para el NO-GO. Imprime secciones antes de calcular la decisión final."
    ),
    initial_code  = (
        "class QACommandCenter:\n"
        "    def __init__(self):\n"
        "        self.perf_results = []\n"
        "        self.security_findings = []\n"
        "        self.test_suites = []\n\n"
        "    def add_perf_result(self, endpoint, p95_ms, error_rate):\n"
        "        pass\n\n"
        "    def add_security_finding(self, severity, description):\n"
        "        pass\n\n"
        "    def add_test_suite(self, name, passed, failed):\n"
        "        pass\n\n"
        "    def go_live_decision(self):\n"
        "        pass\n\n\n"
        "# === SIMULACIÓN GO-LIVE: DAKI Platform v3.0 ===\n"
        "cc = QACommandCenter()\n\n"
        "cc.add_perf_result('/api/login',    p95_ms=280,  error_rate=0.3)\n"
        "cc.add_perf_result('/api/checkout', p95_ms=720,  error_rate=1.8)\n"
        "cc.add_perf_result('/api/reports',  p95_ms=1200, error_rate=0.5)\n\n"
        "cc.add_security_finding('high',     'JWT tokens not rotated after password change')\n"
        "cc.add_security_finding('medium',   'Rate limiting missing on /api/search')\n"
        "cc.add_security_finding('critical', 'SQL injection vector found in /api/reports filter')\n\n"
        "cc.add_test_suite('unit',        passed=847, failed=0)\n"
        "cc.add_test_suite('integration', passed=203, failed=4)\n"
        "cc.add_test_suite('e2e',         passed=91,  failed=1)\n\n"
        "cc.go_live_decision()\n"
    ),
    expected_output = (
        "=== QA COMMAND CENTER — GO/NO-GO REPORT ===\n"
        "\n"
        "PERFORMANCE:\n"
        "  /api/login     p95=280ms   errors=0.3%  → OK\n"
        "  /api/checkout  p95=720ms   errors=1.8%  → WARN\n"
        "  /api/reports   p95=1200ms  errors=0.5%  → FAIL\n"
        "\n"
        "SECURITY:\n"
        "  [high]     JWT tokens not rotated after password change\n"
        "  [medium]   Rate limiting missing on /api/search\n"
        "  [critical] SQL injection vector found in /api/reports filter — BLOCKER\n"
        "\n"
        "TEST SUITES:\n"
        "  unit:         847/847  pass_rate=100.0%\n"
        "  integration:  203/207  pass_rate=98.1%\n"
        "  e2e:           91/92   pass_rate=98.9%\n"
        "\n"
        "NO-GO REASONS:\n"
        "  - PERF FAIL: /api/reports\n"
        "  - SECURITY BLOCKER: SQL injection vector found in /api/reports filter\n"
        "\n"
        "DECISION: NO-GO"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# Exportar BLOQUE5
# ─────────────────────────────────────────────────────────────────────────────
BLOQUE5 = [
    L81, L82, L83, L84, L85,
    L86, L87, L88, L89, L90,
    L91, L92, L93, L94, L95,
    L96, L97, L98, L99, L100,
]
