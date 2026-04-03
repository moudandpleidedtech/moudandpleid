"""
_tpm_b4.py — TPM Mastery · BLOQUE 4 (L46–L60)
===============================================
Fase: comunicacion_ejecutiva
Niveles: 46 a 60 (15 desafíos Python)
Boss: L60 — Communication Hub
"""
from __future__ import annotations

_BASE = dict(
    codex_id       = "tpm_mastery",
    sector_id      = 21,
    challenge_type = "python",
    phase          = "comunicacion_ejecutiva",
    is_free        = False,
    strict_match   = False,
    is_phase_boss  = False,
    is_project     = False,
)
_BASE_BOSS = {k: v for k, v in _BASE.items() if k not in ("is_phase_boss", "is_project")}

# ─────────────────────────────────────────────────────────────────────────────
# L46 — Status Report Builder
# ─────────────────────────────────────────────────────────────────────────────
L46 = dict(
    **_BASE,
    level_order   = 46,
    title         = "Status Report Builder",
    difficulty    = "easy",
    description   = (
        "El status report semanal es el artefacto de comunicación más leído por un TPM. "
        "Implementa `status_report(program, week, components)` que genera el reporte.\n\n"
        "Cada component: `{'name': str, 'status': str, 'update': str, 'next': str}`.\n\n"
        "Formato exacto:\n"
        "```\n"
        "STATUS REPORT — <program>\n"
        "Week: <week>\n"
        "══════════════════════════════════\n"
        "<name padded 16> [<STATUS>]\n"
        "  Update: <update>\n"
        "  Next:   <next>\n"
        "══════════════════════════════════\n"
        "Overall: <worst> (N RED, N YELLOW, N GREEN)\n"
        "```\n"
        "Overall = el peor estado entre todos los componentes (RED > YELLOW > GREEN)."
    ),
    hint          = "Usa ljust(16) para el nombre del componente. Acumula contadores de cada estado.",
    initial_code  = (
        "def status_report(program, week, components):\n"
        "    pass\n\n"
        "status_report(\n"
        "    program='DAKI Platform v3.0',\n"
        "    week='2024-03-25',\n"
        "    components=[\n"
        "        {'name': 'Backend API', 'status': 'GREEN',  'update': 'All APIs stable',             'next': 'Performance sprint'},\n"
        "        {'name': 'Frontend',    'status': 'YELLOW', 'update': '2 features delayed',          'next': 'Design review Wednesday'},\n"
        "        {'name': 'Mobile App',  'status': 'RED',    'update': 'Critical crash in checkout',  'next': 'Hotfix release today'},\n"
        "    ]\n"
        ")\n"
    ),
    expected_output = (
        "STATUS REPORT — DAKI Platform v3.0\n"
        "Week: 2024-03-25\n"
        "══════════════════════════════════\n"
        "Backend API      [GREEN]\n"
        "  Update: All APIs stable\n"
        "  Next:   Performance sprint\n"
        "Frontend         [YELLOW]\n"
        "  Update: 2 features delayed\n"
        "  Next:   Design review Wednesday\n"
        "Mobile App       [RED]\n"
        "  Update: Critical crash in checkout\n"
        "  Next:   Hotfix release today\n"
        "══════════════════════════════════\n"
        "Overall: RED (1 RED, 1 YELLOW, 1 GREEN)"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L47 — Executive Summary Formatter
# ─────────────────────────────────────────────────────────────────────────────
L47 = dict(
    **_BASE,
    level_order   = 47,
    title         = "Executive Summary Formatter",
    difficulty    = "easy",
    description   = (
        "Los ejecutivos leen el resumen, no el detalle. "
        "Implementa `exec_summary(data)` que formatea un resumen ejecutivo en 4 secciones.\n\n"
        "data: `{'title': str, 'situation': str, 'complication': str, "
        "'resolution': str, 'ask': str, 'owner': str, 'deadline': str}`\n\n"
        "Formato exacto:\n"
        "```\n"
        "━━━ EXECUTIVE SUMMARY ━━━\n"
        "<title>\n"
        "\n"
        "SITUATION:\n"
        "  <situation>\n"
        "\n"
        "COMPLICATION:\n"
        "  <complication>\n"
        "\n"
        "RESOLUTION:\n"
        "  <resolution>\n"
        "\n"
        "ASK:\n"
        "  <ask>\n"
        "\n"
        "Owner: <owner>  |  Deadline: <deadline>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "```"
    ),
    hint          = "El framework SCR (Situation-Complication-Resolution) es el estándar McKinsey.",
    initial_code  = (
        "def exec_summary(data):\n"
        "    pass\n\n"
        "exec_summary({\n"
        "    'title':        'Q3 Platform Migration: Decision Required',\n"
        "    'situation':    'Our current infrastructure serves 45k users at 92% capacity.',\n"
        "    'complication': 'Projected 80k users by Q4 will exceed capacity by 30%.',\n"
        "    'resolution':   'Migrate to multi-region cloud setup in 8 weeks for $280k.',\n"
        "    'ask':          'Approve $280k budget and assign 2 senior engineers.',\n"
        "    'owner':        'Maria Chen, TPM',\n"
        "    'deadline':     '2024-04-05',\n"
        "})\n"
    ),
    expected_output = (
        "━━━ EXECUTIVE SUMMARY ━━━\n"
        "Q3 Platform Migration: Decision Required\n"
        "\n"
        "SITUATION:\n"
        "  Our current infrastructure serves 45k users at 92% capacity.\n"
        "\n"
        "COMPLICATION:\n"
        "  Projected 80k users by Q4 will exceed capacity by 30%.\n"
        "\n"
        "RESOLUTION:\n"
        "  Migrate to multi-region cloud setup in 8 weeks for $280k.\n"
        "\n"
        "ASK:\n"
        "  Approve $280k budget and assign 2 senior engineers.\n"
        "\n"
        "Owner: Maria Chen, TPM  |  Deadline: 2024-04-05\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L48 — Escalation Classifier
# ─────────────────────────────────────────────────────────────────────────────
L48 = dict(
    **_BASE,
    level_order   = 48,
    title         = "Escalation Classifier",
    difficulty    = "medium",
    description   = (
        "Escalar en el momento correcto, al nivel correcto, es una habilidad de TPM senior. "
        "Implementa `classify_escalation(issues)` que determina tipo y urgencia.\n\n"
        "Cada issue: `{'id': str, 'description': str, 'blocked_days': int, "
        "'impact': str, 'attempted_resolution': bool}`.\n\n"
        "Tipo de escalación:\n"
        "- `DECISION` si 'decision' o 'approve' en description (case-insensitive)\n"
        "- `RESOURCE`  si 'resource' o 'headcount' o 'budget' en description\n"
        "- `BLOCKER`   en otro caso\n\n"
        "Urgencia:\n"
        "- `CRITICAL` si blocked_days >= 5 o impact == 'revenue'\n"
        "- `HIGH`     si blocked_days >= 2 o impact == 'schedule'\n"
        "- `MEDIUM`   en otro caso\n\n"
        "Imprime: `[<TYPE>/<URGENCY>] <id>: <description>`\n"
        "`  Blocked: Nd  |  Impact: <impact>  |  Attempted: [Y|N]`\n\n"
        "Al final: `Critical: N  High: N  Medium: N`"
    ),
    hint          = "Evalúa tipo con 'keyword in description.lower()'. Urgencia: CRITICAL antes que HIGH.",
    initial_code  = (
        "def classify_escalation(issues):\n"
        "    pass\n\n"
        "issues = [\n"
        "    {'id': 'ESC-01', 'description': 'Need VP to approve cloud budget increase',\n"
        "     'blocked_days': 3, 'impact': 'schedule', 'attempted_resolution': True},\n"
        "    {'id': 'ESC-02', 'description': 'Missing resource: no backend engineer for auth module',\n"
        "     'blocked_days': 7, 'impact': 'revenue',  'attempted_resolution': False},\n"
        "    {'id': 'ESC-03', 'description': 'Vendor not responding to integration requests',\n"
        "     'blocked_days': 1, 'impact': 'quality',  'attempted_resolution': True},\n"
        "    {'id': 'ESC-04', 'description': 'Security team decision needed for data encryption approach',\n"
        "     'blocked_days': 5, 'impact': 'schedule', 'attempted_resolution': True},\n"
        "]\n"
        "classify_escalation(issues)\n"
    ),
    expected_output = (
        "[DECISION/HIGH] ESC-01: Need VP to approve cloud budget increase\n"
        "  Blocked: 3d  |  Impact: schedule  |  Attempted: Y\n"
        "[RESOURCE/CRITICAL] ESC-02: Missing resource: no backend engineer for auth module\n"
        "  Blocked: 7d  |  Impact: revenue  |  Attempted: N\n"
        "[BLOCKER/MEDIUM] ESC-03: Vendor not responding to integration requests\n"
        "  Blocked: 1d  |  Impact: quality  |  Attempted: Y\n"
        "[DECISION/CRITICAL] ESC-04: Security team decision needed for data encryption approach\n"
        "  Blocked: 5d  |  Impact: schedule  |  Attempted: Y\n"
        "Critical: 2  High: 1  Medium: 1"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L49 — Decision Log Builder
# ─────────────────────────────────────────────────────────────────────────────
L49 = dict(
    **_BASE,
    level_order   = 49,
    title         = "Decision Log Builder",
    difficulty    = "medium",
    description   = (
        "Un TPM documenta decisiones para que no se repitan discusiones. "
        "Implementa `decision_log(decisions)` que genera un registro formal.\n\n"
        "Cada decisión: `{'id': str, 'title': str, 'date': str, 'owner': str, "
        "'context': str, 'options': list[str], 'chosen': str, 'rationale': str, 'reversible': bool}`.\n\n"
        "Formato por decisión:\n"
        "```\n"
        "[<id>] <title>  (<date>)\n"
        "Owner: <owner>\n"
        "Context: <context>\n"
        "Options considered:\n"
        "  - <option>  ← CHOSEN  (solo la elegida)\n"
        "  - <option>\n"
        "Rationale: <rationale>\n"
        "Reversible: [Yes|No]\n"
        "```\n"
        "Línea en blanco entre decisiones."
    ),
    hint          = "Marca la opción elegida con '← CHOSEN' al final de esa línea.",
    initial_code  = (
        "def decision_log(decisions):\n"
        "    pass\n\n"
        "decisions = [\n"
        "    {'id': 'DEC-001', 'title': 'Database for user events',\n"
        "     'date': '2024-03-10', 'owner': 'Ana Torres',\n"
        "     'context': 'Need to store 500M events/month with fast reads',\n"
        "     'options': ['PostgreSQL', 'Cassandra', 'DynamoDB'],\n"
        "     'chosen': 'Cassandra',\n"
        "     'rationale': 'Best write throughput and horizontal scaling for event data',\n"
        "     'reversible': False},\n"
        "    {'id': 'DEC-002', 'title': 'API versioning strategy',\n"
        "     'date': '2024-03-15', 'owner': 'Bruno Rivas',\n"
        "     'context': 'Multiple clients need stable API contracts',\n"
        "     'options': ['URL versioning', 'Header versioning'],\n"
        "     'chosen': 'URL versioning',\n"
        "     'rationale': 'Simpler for clients, easier to test and document',\n"
        "     'reversible': True},\n"
        "]\n"
        "decision_log(decisions)\n"
    ),
    expected_output = (
        "[DEC-001] Database for user events  (2024-03-10)\n"
        "Owner: Ana Torres\n"
        "Context: Need to store 500M events/month with fast reads\n"
        "Options considered:\n"
        "  - PostgreSQL\n"
        "  - Cassandra  ← CHOSEN\n"
        "  - DynamoDB\n"
        "Rationale: Best write throughput and horizontal scaling for event data\n"
        "Reversible: No\n"
        "\n"
        "[DEC-002] API versioning strategy  (2024-03-15)\n"
        "Owner: Bruno Rivas\n"
        "Context: Multiple clients need stable API contracts\n"
        "Options considered:\n"
        "  - URL versioning  ← CHOSEN\n"
        "  - Header versioning\n"
        "Rationale: Simpler for clients, easier to test and document\n"
        "Reversible: Yes"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L50 — Async Standup Formatter
# ─────────────────────────────────────────────────────────────────────────────
L50 = dict(
    **_BASE,
    level_order   = 50,
    title         = "Async Standup Formatter",
    difficulty    = "easy",
    description   = (
        "Los equipos distribuidos corren en async. "
        "Implementa `format_standup(updates)` que consolida los standups del equipo.\n\n"
        "Cada update: `{'name': str, 'yesterday': str, 'today': str, 'blockers': str|None}`.\n\n"
        "Formato por miembro:\n"
        "```\n"
        "👤 <name>\n"
        "  Yesterday: <yesterday>\n"
        "  Today:     <today>\n"
        "  Blockers:  <blocker|None>\n"
        "```\n"
        "Al final imprime: `Team blockers: N` y lista los nombres con blocker activo: "
        "`  ⚠ <name>: <blocker>`\n\n"
        "Si no hay blockers: `Team blockers: 0 — all clear`"
    ),
    hint          = "blocker es None si no hay. Filtra los que tienen blocker != None para el resumen.",
    initial_code  = (
        "def format_standup(updates):\n"
        "    pass\n\n"
        "updates = [\n"
        "    {'name': 'Ana',   'yesterday': 'Finished auth API endpoints',   'today': 'Start unit tests',        'blockers': None},\n"
        "    {'name': 'Bruno', 'yesterday': 'Reviewed DB schema',            'today': 'Implement migrations',    'blockers': 'Waiting for DBA approval'},\n"
        "    {'name': 'Cata',  'yesterday': 'Fixed 3 UI bugs',               'today': 'Continue dashboard work', 'blockers': None},\n"
        "    {'name': 'Diego', 'yesterday': 'Wrote QA test plan',            'today': 'Begin smoke tests',       'blockers': 'Need staging access'},\n"
        "]\n"
        "format_standup(updates)\n"
    ),
    expected_output = (
        "👤 Ana\n"
        "  Yesterday: Finished auth API endpoints\n"
        "  Today:     Start unit tests\n"
        "  Blockers:  None\n"
        "👤 Bruno\n"
        "  Yesterday: Reviewed DB schema\n"
        "  Today:     Implement migrations\n"
        "  Blockers:  Waiting for DBA approval\n"
        "👤 Cata\n"
        "  Yesterday: Fixed 3 UI bugs\n"
        "  Today:     Continue dashboard work\n"
        "  Blockers:  None\n"
        "👤 Diego\n"
        "  Yesterday: Wrote QA test plan\n"
        "  Today:     Begin smoke tests\n"
        "  Blockers:  Need staging access\n"
        "Team blockers: 2\n"
        "  ⚠ Bruno: Waiting for DBA approval\n"
        "  ⚠ Diego: Need staging access"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L51 — Meeting Minutes Generator
# ─────────────────────────────────────────────────────────────────────────────
L51 = dict(
    **_BASE,
    level_order   = 51,
    title         = "Meeting Minutes Generator",
    difficulty    = "medium",
    description   = (
        "Los action items sin dueño mueren. "
        "Implementa `meeting_minutes(meeting)` que genera el acta formal.\n\n"
        "meeting: `{'title': str, 'date': str, 'attendees': list[str], "
        "'decisions': list[str], "
        "'action_items': list[{'task': str, 'owner': str, 'due': str}]}`.\n\n"
        "Formato:\n"
        "```\n"
        "MEETING MINUTES\n"
        "<title>  |  <date>\n"
        "Attendees: <name1>, <name2>, ...\n"
        "\n"
        "DECISIONS:\n"
        "  N. <decision>\n"
        "\n"
        "ACTION ITEMS:\n"
        "  [ ] <task>  —  Owner: <owner>  Due: <due>\n"
        "```\n"
        "Al final: `Action items: N  |  Owners: <lista única de owners separada por coma>`"
    ),
    hint          = "Usa un set para owners únicos, luego conviértelo a lista ordenada.",
    initial_code  = (
        "def meeting_minutes(meeting):\n"
        "    pass\n\n"
        "meeting_minutes({\n"
        "    'title': 'Q2 Planning Kickoff',\n"
        "    'date':  '2024-04-01',\n"
        "    'attendees': ['Maria Chen', 'Ana Torres', 'Bruno Rivas', 'VP Engineering'],\n"
        "    'decisions': [\n"
        "        'Adopt microservices architecture for payment module',\n"
        "        'Target GA release for June 30',\n"
        "    ],\n"
        "    'action_items': [\n"
        "        {'task': 'Draft architecture proposal',     'owner': 'Ana Torres',   'due': '2024-04-08'},\n"
        "        {'task': 'Update Q2 roadmap in Notion',     'owner': 'Maria Chen',   'due': '2024-04-03'},\n"
        "        {'task': 'Schedule design review session',  'owner': 'Bruno Rivas',  'due': '2024-04-05'},\n"
        "        {'task': 'Share updated budget forecast',   'owner': 'Maria Chen',   'due': '2024-04-05'},\n"
        "    ],\n"
        "})\n"
    ),
    expected_output = (
        "MEETING MINUTES\n"
        "Q2 Planning Kickoff  |  2024-04-01\n"
        "Attendees: Maria Chen, Ana Torres, Bruno Rivas, VP Engineering\n"
        "\n"
        "DECISIONS:\n"
        "  1. Adopt microservices architecture for payment module\n"
        "  2. Target GA release for June 30\n"
        "\n"
        "ACTION ITEMS:\n"
        "  [ ] Draft architecture proposal  —  Owner: Ana Torres  Due: 2024-04-08\n"
        "  [ ] Update Q2 roadmap in Notion  —  Owner: Maria Chen  Due: 2024-04-03\n"
        "  [ ] Schedule design review session  —  Owner: Bruno Rivas  Due: 2024-04-05\n"
        "  [ ] Share updated budget forecast  —  Owner: Maria Chen  Due: 2024-04-05\n"
        "Action items: 4  |  Owners: Ana Torres, Bruno Rivas, Maria Chen"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L52 — OKR Progress Update
# ─────────────────────────────────────────────────────────────────────────────
L52 = dict(
    **_BASE,
    level_order   = 52,
    title         = "OKR Progress Update",
    difficulty    = "medium",
    description   = (
        "Comunicar el progreso de OKRs es la reunión mensual más importante del TPM. "
        "Implementa `okr_progress_update(okrs, month)` que genera el reporte.\n\n"
        "Cada OKR: `{'objective': str, 'key_results': list[dict]}`.\n"
        "Cada KR: `{'description': str, 'target': float, 'current': float, 'unit': str}`.\n\n"
        "Para cada KR calcula `progress_pct = current / target * 100` (entero).\n"
        "Estado del KR: >= 80% → ON TRACK, >= 50% → AT RISK, < 50% → OFF TRACK.\n"
        "Estado del OKR: el peor de sus KRs.\n\n"
        "Formato:\n"
        "`OKR N: <objective> — [ON TRACK|AT RISK|OFF TRACK]`\n"
        "`  KR N.M: <description>`\n"
        "`    Progress: X/X <unit> (N%) [estado]`"
    ),
    hint          = "Progreso como entero: int(current/target*100). Evalúa OFF TRACK antes que AT RISK.",
    initial_code  = (
        "def okr_progress_update(okrs, month):\n"
        "    print(f'OKR Progress — {month}')\n"
        "    pass\n\n"
        "okrs = [\n"
        "    {'objective': 'Scale to 50k active learners', 'key_results': [\n"
        "        {'description': 'Monthly active users',     'target': 50000, 'current': 38000, 'unit': 'users'},\n"
        "        {'description': 'Course completion rate',   'target': 85,    'current': 71,    'unit': '%'},\n"
        "        {'description': 'Mobile app installs',      'target': 20000, 'current': 4500,  'unit': 'installs'},\n"
        "    ]},\n"
        "    {'objective': 'Achieve platform excellence', 'key_results': [\n"
        "        {'description': 'Uptime SLA',               'target': 99.9,  'current': 99.95, 'unit': '%'},\n"
        "        {'description': 'P95 latency',              'target': 300,   'current': 280,   'unit': 'ms'},\n"
        "    ]},\n"
        "]\n"
        "okr_progress_update(okrs, 'March 2024')\n"
    ),
    expected_output = (
        "OKR Progress — March 2024\n"
        "OKR 1: Scale to 50k active learners — AT RISK\n"
        "  KR 1.1: Monthly active users\n"
        "    Progress: 38000/50000 users (76%) AT RISK\n"
        "  KR 1.2: Course completion rate\n"
        "    Progress: 71/85 % (83%) ON TRACK\n"
        "  KR 1.3: Mobile app installs\n"
        "    Progress: 4500/20000 installs (22%) OFF TRACK\n"
        "OKR 2: Achieve platform excellence — ON TRACK\n"
        "  KR 2.1: Uptime SLA\n"
        "    Progress: 99.95/99.9 % (100%) ON TRACK\n"
        "  KR 2.2: P95 latency\n"
        "    Progress: 280/300 ms (93%) ON TRACK"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L53 — Risk Communication Memo
# ─────────────────────────────────────────────────────────────────────────────
L53 = dict(
    **_BASE,
    level_order   = 53,
    title         = "Risk Communication Memo",
    difficulty    = "medium",
    description   = (
        "Comunicar un riesgo activo sin crear pánico ni subestimarlo es un arte. "
        "Implementa `risk_memo(risks, audience)` que adapta el mensaje al receptor.\n\n"
        "Cada riesgo: `{'id': str, 'title': str, 'impact': str, 'probability': str, "
        "'mitigation': str, 'owner': str}`.\n\n"
        "audience puede ser: `'executive'`, `'team'`, o `'stakeholder'`.\n\n"
        "Para `executive`: solo riesgos con impact='high' o probability='high'. Imprime título + impacto + acción.\n"
        "Para `team`: todos los riesgos con detalle técnico completo.\n"
        "Para `stakeholder`: todos, pero sin el campo `owner`, con lenguaje más suave.\n\n"
        "Prefijo de cada mensaje: `RISK MEMO — Audience: <audience>`\n\n"
        "Ejecutivo: `⚡ <title>: <impact> impact. Action: <mitigation>`\n"
        "Team: `[<id>] <title>  prob=<probability>  impact=<impact>  owner=<owner>\\n  Mitigation: <mitigation>`\n"
        "Stakeholder: `• <title>: We are monitoring this and have a mitigation plan in place.`"
    ),
    hint          = "Filtra para 'executive': impact=='high' or probability=='high'.",
    initial_code  = (
        "def risk_memo(risks, audience):\n"
        "    pass\n\n"
        "risks = [\n"
        "    {'id': 'R1', 'title': 'API vendor sunset',      'impact': 'high',   'probability': 'medium', 'mitigation': 'Evaluate 3 alternatives by Apr 15', 'owner': 'Ana'},\n"
        "    {'id': 'R2', 'title': 'Test coverage gap',      'impact': 'medium', 'probability': 'high',   'mitigation': 'Add 200 unit tests this sprint',     'owner': 'Diego'},\n"
        "    {'id': 'R3', 'title': 'Minor UI inconsistency', 'impact': 'low',    'probability': 'low',    'mitigation': 'Address in next design sprint',       'owner': 'Cata'},\n"
        "]\n"
        "risk_memo(risks, 'executive')\n"
    ),
    expected_output = (
        "RISK MEMO — Audience: executive\n"
        "⚡ API vendor sunset: high impact. Action: Evaluate 3 alternatives by Apr 15\n"
        "⚡ Test coverage gap: medium impact. Action: Add 200 unit tests this sprint"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L54 — Incident Post-Mortem Communication
# ─────────────────────────────────────────────────────────────────────────────
L54 = dict(
    **_BASE,
    level_order   = 54,
    title         = "Incident Post-Mortem Communication",
    difficulty    = "hard",
    description   = (
        "Una comunicación de post-mortem bien escrita reconstruye la confianza. "
        "Implementa `incident_communication(incident, audience)` que genera el mensaje.\n\n"
        "incident: `{'id': str, 'title': str, 'start': str, 'end': str, "
        "'users_affected': int, 'root_cause': str, 'timeline': list[str], "
        "'action_items': list[str]}`.\n\n"
        "audience='internal': reporte técnico completo con timeline.\n"
        "audience='external': comunicación al cliente (sin root cause técnico, sin timeline detallado).\n\n"
        "Duración = diferencia entre start y end en minutos "
        "(formato: HH:MM → convierte a minutos).\n\n"
        "Internal: Header + Duration + Root Cause + Timeline + Action Items.\n"
        "External: Header genérico + apologetic summary + what we're doing + next update."
    ),
    hint          = "Parsea HH:MM con int(t.split(':')[0])*60 + int(t.split(':')[1]).",
    initial_code  = (
        "def incident_communication(incident, audience):\n"
        "    pass\n\n"
        "inc = {\n"
        "    'id': 'INC-2024-031', 'title': 'Payment Service Degradation',\n"
        "    'start': '14:22', 'end': '15:09',\n"
        "    'users_affected': 3400,\n"
        "    'root_cause': 'Connection pool exhausted due to N+1 query in checkout flow',\n"
        "    'timeline': ['14:22 — Alerts triggered', '14:35 — On-call engineer engaged', '15:09 — Service restored'],\n"
        "    'action_items': ['Fix N+1 query', 'Add connection pool monitoring', 'Load test checkout flow'],\n"
        "}\n"
        "incident_communication(inc, 'internal')\n"
    ),
    expected_output = (
        "INTERNAL POST-MORTEM: INC-2024-031\n"
        "Payment Service Degradation\n"
        "Duration: 47 minutes  |  Users affected: 3,400\n"
        "\n"
        "ROOT CAUSE:\n"
        "  Connection pool exhausted due to N+1 query in checkout flow\n"
        "\n"
        "TIMELINE:\n"
        "  14:22 — Alerts triggered\n"
        "  14:35 — On-call engineer engaged\n"
        "  15:09 — Service restored\n"
        "\n"
        "ACTION ITEMS:\n"
        "  [ ] Fix N+1 query\n"
        "  [ ] Add connection pool monitoring\n"
        "  [ ] Load test checkout flow"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L55 — Weekly 5-Bullet Update
# ─────────────────────────────────────────────────────────────────────────────
L55 = dict(
    **_BASE,
    level_order   = 55,
    title         = "Weekly 5-Bullet Update",
    difficulty    = "easy",
    description   = (
        "El update semanal de 5 bullets es el formato favorito de los líderes ocupados. "
        "Implementa `five_bullet_update(program, week, bullets)` donde bullets es una lista "
        "de dicts `{'category': str, 'message': str}`.\n\n"
        "Categorías disponibles: `WIN`, `RISK`, `DECISION`, `METRIC`, `NEXT`.\n\n"
        "Formato:\n"
        "```\n"
        "📋 <program> — Week of <week>\n"
        "─────────────────────────────────\n"
        "✅ [WIN]      <message>\n"
        "⚠️  [RISK]     <message>\n"
        "🔷 [DECISION] <message>\n"
        "📊 [METRIC]   <message>\n"
        "🎯 [NEXT]     <message>\n"
        "─────────────────────────────────\n"
        "```\n"
        "Emojis por categoría: WIN=✅, RISK=⚠️, DECISION=🔷, METRIC=📊, NEXT=🎯."
    ),
    hint          = "Usa un dict de categoría→emoji para el lookup.",
    initial_code  = (
        "def five_bullet_update(program, week, bullets):\n"
        "    pass\n\n"
        "five_bullet_update(\n"
        "    program='DAKI Platform v3.0',\n"
        "    week='2024-03-25',\n"
        "    bullets=[\n"
        "        {'category': 'WIN',      'message': 'Auth module shipped 2 days early'},\n"
        "        {'category': 'RISK',     'message': 'Mobile dev 1 week behind — mitigation in place'},\n"
        "        {'category': 'DECISION', 'message': 'Chose Cassandra for event storage (see DEC-001)'},\n"
        "        {'category': 'METRIC',   'message': 'P95 latency improved from 450ms to 280ms'},\n"
        "        {'category': 'NEXT',     'message': 'Beta launch target: April 15'},\n"
        "    ]\n"
        ")\n"
    ),
    expected_output = (
        "📋 DAKI Platform v3.0 — Week of 2024-03-25\n"
        "─────────────────────────────────\n"
        "✅ [WIN]      Auth module shipped 2 days early\n"
        "⚠️  [RISK]     Mobile dev 1 week behind — mitigation in place\n"
        "🔷 [DECISION] Chose Cassandra for event storage (see DEC-001)\n"
        "📊 [METRIC]   P95 latency improved from 450ms to 280ms\n"
        "🎯 [NEXT]     Beta launch target: April 15\n"
        "─────────────────────────────────"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L56 — C-Level Briefing Builder
# ─────────────────────────────────────────────────────────────────────────────
L56 = dict(
    **_BASE,
    level_order   = 56,
    title         = "C-Level Briefing Builder",
    difficulty    = "hard",
    description   = (
        "Un briefing para el CEO debe ser breve, directo y orientado a decisiones. "
        "Implementa `clevel_briefing(data)` que genera el one-pager ejecutivo.\n\n"
        "data: `{'program': str, 'date': str, 'headline': str, 'status': str, "
        "'key_metrics': list[dict], 'risks': list[str], 'decision_needed': str, 'timeline': str}`.\n\n"
        "key_metric: `{'label': str, 'value': str, 'trend': str}` "
        "(trend: '↑', '↓', '→').\n\n"
        "Formato (una sola página):\n"
        "```\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "<program>  [<STATUS>]  <date>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "HEADLINE: <headline>\n"
        "\n"
        "KEY METRICS:\n"
        "  <label>: <value> <trend>\n"
        "\n"
        "TOP RISKS:\n"
        "  • <risk>\n"
        "\n"
        "DECISION NEEDED:\n"
        "  <decision_needed>\n"
        "\n"
        "TIMELINE: <timeline>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "```"
    ),
    hint          = "El formato es estricto — línea a línea. No hay cálculos, solo formateo.",
    initial_code  = (
        "def clevel_briefing(data):\n"
        "    pass\n\n"
        "clevel_briefing({\n"
        "    'program': 'DAKI Platform v3.0',\n"
        "    'date':    '2024-04-01',\n"
        "    'headline': 'On track for Q2 launch; 1 critical risk requires decision',\n"
        "    'status':   'YELLOW',\n"
        "    'key_metrics': [\n"
        "        {'label': 'Sprint velocity',  'value': '94 pts', 'trend': '↑'},\n"
        "        {'label': 'P95 latency',      'value': '280ms',  'trend': '↓'},\n"
        "        {'label': 'Test coverage',    'value': '74%',    'trend': '→'},\n"
        "    ],\n"
        "    'risks': ['Mobile timeline 1 week behind', 'Vendor contract renewal pending'],\n"
        "    'decision_needed': 'Approve $40k for additional QA resources to close coverage gap',\n"
        "    'timeline': 'Beta: Apr 15  |  GA: Jun 30',\n"
        "})\n"
    ),
    expected_output = (
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "DAKI Platform v3.0  [YELLOW]  2024-04-01\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "HEADLINE: On track for Q2 launch; 1 critical risk requires decision\n"
        "\n"
        "KEY METRICS:\n"
        "  Sprint velocity: 94 pts ↑\n"
        "  P95 latency: 280ms ↓\n"
        "  Test coverage: 74% →\n"
        "\n"
        "TOP RISKS:\n"
        "  • Mobile timeline 1 week behind\n"
        "  • Vendor contract renewal pending\n"
        "\n"
        "DECISION NEEDED:\n"
        "  Approve $40k for additional QA resources to close coverage gap\n"
        "\n"
        "TIMELINE: Beta: Apr 15  |  GA: Jun 30\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L57 — Stakeholder Newsletter
# ─────────────────────────────────────────────────────────────────────────────
L57 = dict(
    **_BASE,
    level_order   = 57,
    title         = "Stakeholder Newsletter",
    difficulty    = "medium",
    description   = (
        "El newsletter mensual mantiene al ecosistema informado sin reuniones extras. "
        "Implementa `stakeholder_newsletter(data)` que genera el boletín.\n\n"
        "data: `{'program': str, 'month': str, 'highlights': list[str], "
        "'metrics': list[dict], 'upcoming': list[str], 'team_spotlight': str}`.\n\n"
        "metric: `{'name': str, 'value': str, 'vs_last_month': str}`.\n\n"
        "Formato:\n"
        "```\n"
        "═══════════════════════════════════\n"
        " <program> Monthly Update — <month>\n"
        "═══════════════════════════════════\n"
        "HIGHLIGHTS\n"
        "  ★ <highlight>\n"
        "\n"
        "BY THE NUMBERS\n"
        "  <name>: <value>  (vs last month: <vs_last_month>)\n"
        "\n"
        "COMING UP\n"
        "  → <upcoming item>\n"
        "\n"
        "TEAM SPOTLIGHT\n"
        "  <team_spotlight>\n"
        "═══════════════════════════════════\n"
        "```"
    ),
    hint          = "Cada lista usa un prefijo diferente: ★ highlights, numbers inline, → upcoming.",
    initial_code  = (
        "def stakeholder_newsletter(data):\n"
        "    pass\n\n"
        "stakeholder_newsletter({\n"
        "    'program': 'DAKI Platform',\n"
        "    'month': 'March 2024',\n"
        "    'highlights': ['Auth module launched on time', 'P95 latency reduced by 37%'],\n"
        "    'metrics': [\n"
        "        {'name': 'Active users',  'value': '38,000',  'vs_last_month': '+12%'},\n"
        "        {'name': 'Uptime',        'value': '99.97%',  'vs_last_month': '+0.05%'},\n"
        "    ],\n"
        "    'upcoming': ['Beta launch April 15', 'Performance load test April 20'],\n"
        "    'team_spotlight': 'Ana Torres led the auth refactor delivering 40% faster login times.',\n"
        "})\n"
    ),
    expected_output = (
        "═══════════════════════════════════\n"
        " DAKI Platform Monthly Update — March 2024\n"
        "═══════════════════════════════════\n"
        "HIGHLIGHTS\n"
        "  ★ Auth module launched on time\n"
        "  ★ P95 latency reduced by 37%\n"
        "\n"
        "BY THE NUMBERS\n"
        "  Active users: 38,000  (vs last month: +12%)\n"
        "  Uptime: 99.97%  (vs last month: +0.05%)\n"
        "\n"
        "COMING UP\n"
        "  → Beta launch April 15\n"
        "  → Performance load test April 20\n"
        "\n"
        "TEAM SPOTLIGHT\n"
        "  Ana Torres led the auth refactor delivering 40% faster login times.\n"
        "═══════════════════════════════════"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L58 — Program Health Dashboard (text)
# ─────────────────────────────────────────────────────────────────────────────
L58 = dict(
    **_BASE,
    level_order   = 58,
    title         = "Program Health Dashboard",
    difficulty    = "hard",
    description   = (
        "Implementa `health_dashboard(program_name, pillars)` que genera un dashboard "
        "de salud del programa en formato texto.\n\n"
        "Cada pilar: `{'name': str, 'score': int, 'trend': str, 'top_issue': str}`.\n"
        "score: 1-10. trend: 'improving', 'stable', 'declining'.\n\n"
        "Barra visual: cada punto = 1 char '█'. Rellena hasta 10 con '░'.\n\n"
        "Score color label: 8-10 → HEALTHY, 5-7 → CAUTION, 1-4 → CRITICAL.\n\n"
        "Formato:\n"
        "```\n"
        "PROGRAM HEALTH: <program_name>\n"
        "─────────────────────────────────────────\n"
        "<name padded 20> █████░░░░░  N/10  [LABEL]  trend↑|→|↓\n"
        "  Issue: <top_issue>\n"
        "─────────────────────────────────────────\n"
        "Overall: X.X/10  [LABEL]\n"
        "```\n"
        "Overall = promedio redondeado a 1 decimal. trend symbol: improving=↑, stable=→, declining=↓."
    ),
    hint          = "Barra = '█'*score + '░'*(10-score). overall = sum(scores)/len, round a 1 dec.",
    initial_code  = (
        "def health_dashboard(program_name, pillars):\n"
        "    pass\n\n"
        "health_dashboard('DAKI Platform v3.0', [\n"
        "    {'name': 'Delivery',    'score': 8, 'trend': 'improving', 'top_issue': 'Mobile 1 week behind'},\n"
        "    {'name': 'Quality',     'score': 6, 'trend': 'stable',    'top_issue': 'Coverage at 74%, target 80%'},\n"
        "    {'name': 'Team Health', 'score': 9, 'trend': 'improving', 'top_issue': 'None'},\n"
        "    {'name': 'Budget',      'score': 4, 'trend': 'declining', 'top_issue': 'Eng overspend +8%'},\n"
        "])\n"
    ),
    expected_output = (
        "PROGRAM HEALTH: DAKI Platform v3.0\n"
        "─────────────────────────────────────────\n"
        "Delivery             ████████░░  8/10  [HEALTHY]   trend↑\n"
        "Quality              ██████░░░░  6/10  [CAUTION]   trend→\n"
        "Team Health          █████████░  9/10  [HEALTHY]   trend↑\n"
        "Budget               ████░░░░░░  4/10  [CRITICAL]  trend↓\n"
        "─────────────────────────────────────────\n"
        "Overall: 6.8/10  [CAUTION]"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L59 — Quarterly Business Review (QBR) Builder
# ─────────────────────────────────────────────────────────────────────────────
L59 = dict(
    **_BASE,
    level_order   = 59,
    title         = "Quarterly Business Review Builder",
    difficulty    = "hard",
    description   = (
        "El QBR es la reunión más importante del trimestre. "
        "Implementa `build_qbr(data)` que genera el documento completo.\n\n"
        "data incluye: `program`, `quarter`, `okr_results` (lista de OKRs con achievement_pct), "
        "`wins`, `misses`, `learnings`, `next_quarter_priorities`.\n\n"
        "OKR: `{'objective': str, 'achievement_pct': float}`.\n\n"
        "Formato (7 secciones):\n"
        "1. Header\n"
        "2. OKR RESULTS — cada OKR con barra de progreso y grade (A/B/C/F: >=90/>=70/>=50/<50)\n"
        "3. WINS (lista)\n"
        "4. MISSES (lista)\n"
        "5. LEARNINGS (lista)\n"
        "6. NEXT QUARTER PRIORITIES (numerada)\n"
        "7. Footer con score promedio de OKRs"
    ),
    hint          = "Grade: A si >=90%, B si >=70%, C si >=50%, F si <50%.",
    initial_code  = (
        "def build_qbr(data):\n"
        "    pass\n\n"
        "build_qbr({\n"
        "    'program': 'DAKI Platform',\n"
        "    'quarter': 'Q1 2024',\n"
        "    'okr_results': [\n"
        "        {'objective': 'Scale to 30k users',      'achievement_pct': 92},\n"
        "        {'objective': 'Achieve 99.9% uptime',    'achievement_pct': 100},\n"
        "        {'objective': 'Launch mobile beta',      'achievement_pct': 65},\n"
        "    ],\n"
        "    'wins':    ['Auth module delivered early', '37% latency improvement'],\n"
        "    'misses':  ['Mobile beta delayed 3 weeks', 'Coverage target missed'],\n"
        "    'learnings': ['Mobile requires dedicated QA from day 1'],\n"
        "    'next_quarter_priorities': ['GA launch', 'AI personalization MVP', 'Security audit'],\n"
        "})\n"
    ),
    expected_output = (
        "╔══════════════════════════════════════╗\n"
        "║  QBR: DAKI Platform — Q1 2024       ║\n"
        "╚══════════════════════════════════════╝\n"
        "\n"
        "OKR RESULTS:\n"
        "  Scale to 30k users      ████████████████████░░  92%  Grade: A\n"
        "  Achieve 99.9% uptime    ██████████████████████  100%  Grade: A\n"
        "  Launch mobile beta      ██████████████░░░░░░░░  65%  Grade: C\n"
        "\n"
        "WINS:\n"
        "  ✓ Auth module delivered early\n"
        "  ✓ 37% latency improvement\n"
        "\n"
        "MISSES:\n"
        "  ✗ Mobile beta delayed 3 weeks\n"
        "  ✗ Coverage target missed\n"
        "\n"
        "LEARNINGS:\n"
        "  → Mobile requires dedicated QA from day 1\n"
        "\n"
        "NEXT QUARTER PRIORITIES:\n"
        "  1. GA launch\n"
        "  2. AI personalization MVP\n"
        "  3. Security audit\n"
        "\n"
        "Quarter Score: 85.7% — Grade: B"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# L60 — BOSS: Communication Hub
# ─────────────────────────────────────────────────────────────────────────────
L60 = dict(
    **_BASE_BOSS,
    level_order   = 60,
    title         = "CONTRATO-TPM-60: Communication Hub",
    difficulty    = "legendary",
    is_phase_boss = True,
    is_project    = True,
    description   = (
        "El TPM como hub de comunicación: el mensaje correcto, al público correcto, en el momento correcto. "
        "Implementa la clase `CommunicationHub` que gestiona todos los canales.\n\n"
        "Métodos:\n"
        "- `__init__(program, week)`\n"
        "- `add_component_update(name, status, message)` — agrega actualización\n"
        "- `add_metric(label, value, trend)` — agrega métrica clave\n"
        "- `add_decision(title, chosen)` — agrega decisión tomada\n"
        "- `broadcast(channel)` — genera mensaje según canal\n\n"
        "Canales:\n"
        "- `'slack-engineering'`: lista de updates con status en brackets + métricas\n"
        "- `'email-stakeholders'`: formato newsletter conciso con métricas y decisiones\n"
        "- `'exec-briefing'`: one-liner de status global + 3 bullets (worst component, best metric, last decision)\n\n"
        "Status global = el peor de los componentes."
    ),
    hint          = "Cada canal tiene su propio formato. broadcast() usa if/elif para el canal.",
    initial_code  = (
        "class CommunicationHub:\n"
        "    def __init__(self, program, week):\n"
        "        self.program    = program\n"
        "        self.week       = week\n"
        "        self.components = []\n"
        "        self.metrics    = []\n"
        "        self.decisions  = []\n\n"
        "    def add_component_update(self, name, status, message):\n"
        "        pass\n\n"
        "    def add_metric(self, label, value, trend):\n"
        "        pass\n\n"
        "    def add_decision(self, title, chosen):\n"
        "        pass\n\n"
        "    def broadcast(self, channel):\n"
        "        pass\n\n\n"
        "hub = CommunicationHub('DAKI Platform v3.0', '2024-04-01')\n"
        "hub.add_component_update('Backend',  'GREEN',  'All services nominal')\n"
        "hub.add_component_update('Frontend', 'YELLOW', '1 feature delayed')\n"
        "hub.add_component_update('Mobile',   'RED',    'Crash bug in checkout')\n"
        "hub.add_metric('P95 latency', '280ms', '↓')\n"
        "hub.add_metric('Uptime',      '99.97%','↑')\n"
        "hub.add_decision('Auth provider', 'Auth0')\n\n"
        "hub.broadcast('slack-engineering')\n"
        "print('---')\n"
        "hub.broadcast('exec-briefing')\n"
    ),
    expected_output = (
        "[DAKI Platform v3.0 | Week 2024-04-01]\n"
        "Backend  [GREEN]  All services nominal\n"
        "Frontend [YELLOW] 1 feature delayed\n"
        "Mobile   [RED]    Crash bug in checkout\n"
        "Metrics: P95 latency=280ms ↓ | Uptime=99.97% ↑\n"
        "---\n"
        "DAKI Platform v3.0 | 2024-04-01 | Status: RED\n"
        "• Attention needed: Mobile — Crash bug in checkout\n"
        "• Best metric: P95 latency = 280ms ↓\n"
        "• Latest decision: Auth provider → Auth0"
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
BLOQUE4 = [L46, L47, L48, L49, L50, L51, L52, L53, L54, L55, L56, L57, L58, L59, L60]
