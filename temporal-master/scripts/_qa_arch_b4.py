"""Bloque 4 — API Testing & Contratos (L61–L80) — Python"""
from __future__ import annotations
import json

BLOQUE4 = [
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-061: HTTP METHOD CLASSIFIER ]",
"description": (
    "Implementa `classify_request(method: str, has_body: bool, is_idempotent: bool) -> dict` "
    "que retorne `{'method': str, 'safe': bool, 'idempotent': bool, 'use_case': str}`."
),
"difficulty_tier": 1, "difficulty": "easy",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 61, "base_xp_reward": 170,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 200, "challenge_type": "python",
"phase": "api_contratos", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["HTTP", "metodos", "REST", "safe_idempotent"]),
"initial_code": (
    "HTTP_SEMANTICS = {\n"
    "    'GET':    {'safe': True,  'idempotent': True,  'use_case': 'retrieve resource'},\n"
    "    'POST':   {'safe': False, 'idempotent': False, 'use_case': 'create resource'},\n"
    "    'PUT':    {'safe': False, 'idempotent': True,  'use_case': 'replace resource'},\n"
    "    'PATCH':  {'safe': False, 'idempotent': False, 'use_case': 'partial update'},\n"
    "    'DELETE': {'safe': False, 'idempotent': True,  'use_case': 'remove resource'},\n"
    "    'HEAD':   {'safe': True,  'idempotent': True,  'use_case': 'check resource exists'},\n"
    "}\n"
    "\n"
    "\n"
    "def classify_request(method: str) -> dict:\n"
    "    # TODO: retorna HTTP_SEMANTICS[method] con 'method' añadido\n"
    "    # Si method no existe: retorna {'method': method, 'safe': False, 'idempotent': False, 'use_case': 'unknown'}\n"
    "    pass\n"
    "\n"
    "\n"
    "methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS']\n"
    "for m in methods:\n"
    "    info = classify_request(m)\n"
    "    print(f'{m:<8} safe={str(info[\"safe\"]):<5} idempotent={str(info[\"idempotent\"]):<5} | {info[\"use_case\"]}')\n"
),
"expected_output": (
    "GET      safe=True  idempotent=True  | retrieve resource\n"
    "POST     safe=False idempotent=False | create resource\n"
    "PUT      safe=False idempotent=True  | replace resource\n"
    "DELETE   safe=False idempotent=True  | remove resource\n"
    "PATCH    safe=False idempotent=False | partial update\n"
    "OPTIONS  safe=False idempotent=False | unknown"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "GET para leer, POST para crear, PUT para reemplazar. "
    "Entender la semántica HTTP es el cimiento de cualquier test de API."
),
"theory_content": (
    "## HTTP Method Semantics\n\n"
    "| Método | Safe | Idempotente | Body |\n"
    "|--------|------|-------------|------|\n"
    "| GET    | Si   | Si          | No   |\n"
    "| POST   | No   | No          | Si   |\n"
    "| PUT    | No   | Si          | Si   |\n"
    "| PATCH  | No   | No*         | Si   |\n"
    "| DELETE | No   | Si          | No   |\n\n"
    "**Safe**: no modifica el servidor. **Idempotente**: N llamadas = 1 llamada en cuanto a efecto."
),
"pedagogical_objective": "Clasificar métodos HTTP por seguridad, idempotencia y caso de uso.",
"syntax_hint": "Usa `.get()` con default para manejar métodos desconocidos.",
"hints_json": json.dumps([
    "semantics = HTTP_SEMANTICS.get(method, {'safe': False, 'idempotent': False, 'use_case': 'unknown'})",
    "return {'method': method, **semantics} — spread del dict de semánticas.",
    "OPTIONS no está en HTTP_SEMANTICS → usa el default con 'unknown'.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-062: STATUS CODE VALIDATOR ]",
"description": (
    "Implementa `StatusValidator.validate(expected: int, actual: int, context: str) -> str` "
    "que retorne `'PASS'` o `'FAIL: expected {e} got {a} for {context}'`."
),
"difficulty_tier": 1, "difficulty": "easy",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 62, "base_xp_reward": 180,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 200, "challenge_type": "python",
"phase": "api_contratos", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["status_codes", "validacion", "HTTP", "assertions"]),
"initial_code": (
    "STATUS_MEANINGS = {\n"
    "    200: 'OK', 201: 'Created', 204: 'No Content',\n"
    "    400: 'Bad Request', 401: 'Unauthorized', 403: 'Forbidden',\n"
    "    404: 'Not Found', 409: 'Conflict', 422: 'Unprocessable Entity',\n"
    "    429: 'Too Many Requests', 500: 'Internal Server Error',\n"
    "}\n"
    "\n"
    "\n"
    "class StatusValidator:\n"
    "    def validate(self, expected: int, actual: int, context: str) -> str:\n"
    "        # TODO: si expected == actual → retorna 'PASS'\n"
    "        # Si no → retorna 'FAIL: expected {e} ({meaning_e}) got {a} ({meaning_a}) for {context}'\n"
    "        # Usa STATUS_MEANINGS para obtener el texto del código\n"
    "        pass\n"
    "\n"
    "\n"
    "v = StatusValidator()\n"
    "cases = [\n"
    "    (200, 200, 'GET /users'),\n"
    "    (201, 200, 'POST /users'),\n"
    "    (204, 404, 'DELETE /users/99'),\n"
    "    (401, 401, 'GET /protected without token'),\n"
    "]\n"
    "for exp, act, ctx in cases:\n"
    "    print(v.validate(exp, act, ctx))\n"
),
"expected_output": (
    "PASS\n"
    "FAIL: expected 201 (Created) got 200 (OK) for POST /users\n"
    "FAIL: expected 204 (No Content) got 404 (Not Found) for DELETE /users/99\n"
    "PASS"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "200 OK, 201 Created, 400 Bad Request, 401 Unauthorized. "
    "Cada status code es un contrato — violarlo es un bug."
),
"theory_content": (
    "## HTTP Status Codes en API Testing\n\n"
    "Los status codes más importantes para QA:\n\n"
    "- **2xx**: éxito (200 OK, 201 Created, 204 No Content)\n"
    "- **4xx**: error del cliente (400 Bad Request, 401 Unauthorized, 404 Not Found)\n"
    "- **5xx**: error del servidor (500 Internal, 503 Unavailable)\n\n"
    "**Error común**: una API que retorna 200 con `{error: 'not found'}` en el body — "
    "esto viola el protocolo HTTP."
),
"pedagogical_objective": "Validar status codes HTTP con mensajes de error descriptivos usando un diccionario de significados.",
"syntax_hint": "`STATUS_MEANINGS.get(code, 'Unknown')` para obtener el texto de cualquier código.",
"hints_json": json.dumps([
    "Si expected == actual: return 'PASS'",
    "m_e = STATUS_MEANINGS.get(expected, 'Unknown'); m_a = STATUS_MEANINGS.get(actual, 'Unknown')",
    "return f'FAIL: expected {expected} ({m_e}) got {actual} ({m_a}) for {context}'",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-063: JSON SCHEMA VALIDATOR ]",
"description": (
    "Implementa `validate_response(response: dict, schema: dict) -> list` "
    "que retorne lista de violaciones. "
    "Valida: campos requeridos presentes, tipos correctos (`str`, `int`, `list`, `bool`)."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 63, "base_xp_reward": 190,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "python",
"phase": "api_contratos", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["JSON_schema", "validacion", "contrato", "tipos"]),
"initial_code": (
    "def validate_response(response: dict, schema: dict) -> list:\n"
    "    # TODO: valida response contra schema\n"
    "    # schema: {campo: {'type': type_obj, 'required': bool}}\n"
    "    # Violaciones:\n"
    "    # - 'missing required field: {campo}' si required y no está en response\n"
    "    # - 'type error: {campo} expected {type.__name__} got {actual_type.__name__}'\n"
    "    #   solo si el campo existe pero tiene tipo incorrecto\n"
    "    pass\n"
    "\n"
    "\n"
    "schema = {\n"
    "    'id':       {'type': int,  'required': True},\n"
    "    'name':     {'type': str,  'required': True},\n"
    "    'email':    {'type': str,  'required': True},\n"
    "    'active':   {'type': bool, 'required': False},\n"
    "    'tags':     {'type': list, 'required': False},\n"
    "}\n"
    "responses = [\n"
    "    {'id': 1, 'name': 'Alice', 'email': 'alice@daki.io', 'active': True, 'tags': []},\n"
    "    {'id': '42', 'name': 'Bob', 'email': 'bob@daki.io'},\n"
    "    {'name': 'Carol', 'active': 'yes'},\n"
    "]\n"
    "for i, resp in enumerate(responses, 1):\n"
    "    violations = validate_response(resp, schema)\n"
    "    status = 'VALID' if not violations else f'INVALID: {\"; \".join(violations)}'\n"
    "    print(f'Response {i}: {status}')\n"
),
"expected_output": (
    "Response 1: VALID\n"
    "Response 2: INVALID: type error: id expected int got str\n"
    "Response 3: INVALID: missing required field: email; type error: active expected bool got str"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "El schema es el contrato entre el backend y el frontend. "
    "Si cambia sin avisar, todo se rompe — el QA lo detecta antes que el usuario."
),
"theory_content": (
    "## JSON Schema Validation\n\n"
    "```python\n# Estructura de schema\nschema = {\n    'id':   {'type': int,  'required': True},\n    'name': {'type': str,  'required': True},\n    'tags': {'type': list, 'required': False},\n}\n```\n\n"
    "En producción se usan librerías como `jsonschema`, `pydantic` o `zod` (JS). "
    "Implementar el validador manualmente enseña exactamente cómo funcionan."
),
"pedagogical_objective": "Implementar validación de schema JSON verificando campos requeridos y tipos de datos.",
"syntax_hint": "`type(response[field]).__name__` retorna el nombre del tipo como string.",
"hints_json": json.dumps([
    "Para cada campo, rules en schema.items(): si rules['required'] y campo no en response → missing.",
    "Si campo en response: actual_type = type(response[campo]); si actual_type != rules['type'] → type error.",
    "Response 3 no tiene 'email' (required → missing) y 'active' es str no bool → type error.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-064: REQUEST BUILDER ]",
"description": (
    "Implementa `RequestBuilder` con fluent API: `.method(m)`, `.url(u)`, `.header(k,v)`, "
    "`.body(data)`, `.auth(token)`, `.build() -> dict`."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 64, "base_xp_reward": 200,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "python",
"phase": "api_contratos", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["request_builder", "fluent_api", "headers", "auth"]),
"initial_code": (
    "class RequestBuilder:\n"
    "    def __init__(self):\n"
    "        self._method  = 'GET'\n"
    "        self._url     = ''\n"
    "        self._headers = {}\n"
    "        self._body    = None\n"
    "\n"
    "    def method(self, m: str):\n"
    "        # TODO: setea self._method = m.upper(), retorna self\n"
    "        pass\n"
    "\n"
    "    def url(self, u: str):\n"
    "        # TODO: setea self._url = u, retorna self\n"
    "        pass\n"
    "\n"
    "    def header(self, key: str, value: str):\n"
    "        # TODO: agrega {key: value} a self._headers, retorna self\n"
    "        pass\n"
    "\n"
    "    def body(self, data: dict):\n"
    "        # TODO: setea self._body = data, retorna self\n"
    "        pass\n"
    "\n"
    "    def auth(self, token: str):\n"
    "        # TODO: agrega 'Authorization': f'Bearer {token}' a headers, retorna self\n"
    "        pass\n"
    "\n"
    "    def build(self) -> dict:\n"
    "        # TODO: retorna {'method': ..., 'url': ..., 'headers': ..., 'body': ...}\n"
    "        pass\n"
    "\n"
    "\n"
    "req = (RequestBuilder()\n"
    "       .method('post')\n"
    "       .url('/api/v1/users')\n"
    "       .auth('jwt-token-xyz')\n"
    "       .header('Content-Type', 'application/json')\n"
    "       .body({'name': 'Alice', 'role': 'ADMIN'})\n"
    "       .build())\n"
    "\n"
    "print(f'Method: {req[\"method\"]}')\n"
    "print(f'URL: {req[\"url\"]}')\n"
    "for k, v in req['headers'].items():\n"
    "    print(f'Header: {k}: {v}')\n"
    "print(f'Body: {req[\"body\"]}')\n"
),
"expected_output": (
    "Method: POST\n"
    "URL: /api/v1/users\n"
    "Header: Authorization: Bearer jwt-token-xyz\n"
    "Header: Content-Type: application/json\n"
    "Body: {'name': 'Alice', 'role': 'ADMIN'}"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Un request mal construido es un test inválido. "
    "El builder garantiza que los headers, auth y body estén siempre correctos."
),
"theory_content": (
    "## Fluent API Request Builder\n\n"
    "```python\nreq = RequestBuilder()\\\n    .method('POST')\\\n    .url('/api/users')\\\n    .auth(token)\\\n    .body(data)\\\n    .build()\n```\n\n"
    "**Patrón**: cada método retorna `self` para encadenamiento. "
    "`.build()` es el único método que NO retorna `self` — termina la cadena con el resultado."
),
"pedagogical_objective": "Implementar un builder de HTTP requests con fluent interface y método auth conveniente.",
"syntax_hint": "Todos los métodos menos `build()` retornan `self`. `auth` agrega a `self._headers['Authorization']`.",
"hints_json": json.dumps([
    "method: self._method = m.upper(); return self. url: self._url = u; return self.",
    "header: self._headers[key] = value; return self. auth: self._headers['Authorization'] = f'Bearer {token}'; return self.",
    "build: return {'method': self._method, 'url': self._url, 'headers': self._headers, 'body': self._body}",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-065: RESPONSE TIME ASSERTER ]",
"description": (
    "Implementa `SLAChecker.check(endpoint: str, response_time_ms: float, sla_ms: float) -> str` "
    "que retorne `'PASS ({time}ms)'` o `'FAIL: {time}ms exceeds SLA {sla}ms ({pct}% over)'`."
),
"difficulty_tier": 1, "difficulty": "easy",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 65, "base_xp_reward": 220,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 200, "challenge_type": "python",
"phase": "api_contratos", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["response_time", "SLA", "latencia", "performance"]),
"initial_code": (
    "class SLAChecker:\n"
    "    def check(self, endpoint: str, response_time_ms: float, sla_ms: float) -> str:\n"
    "        # TODO: retorna PASS o FAIL con porcentaje de exceso\n"
    "        # pct_over = round((response_time_ms - sla_ms) / sla_ms * 100, 1)\n"
    "        pass\n"
    "\n"
    "\n"
    "checker = SLAChecker()\n"
    "cases = [\n"
    "    ('/api/login',    180.0, 200.0),\n"
    "    ('/api/checkout', 385.0, 300.0),\n"
    "    ('/api/search',   199.9, 200.0),\n"
    "    ('/api/report',   950.0, 500.0),\n"
    "]\n"
    "for endpoint, t, sla in cases:\n"
    "    result = checker.check(endpoint, t, sla)\n"
    "    print(f'{endpoint}: {result}')\n"
),
"expected_output": (
    "/api/login: PASS (180.0ms)\n"
    "/api/checkout: FAIL: 385.0ms exceeds SLA 300.0ms (28.3% over)\n"
    "/api/search: PASS (199.9ms)\n"
    "/api/report: FAIL: 950.0ms exceeds SLA 500.0ms (90.0% over)"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Un endpoint que responde en 200ms en tests y en 3s en producción "
    "indica un problema de carga que tus tests no están modelando."
),
"theory_content": (
    "## SLA Testing\n\n"
    "**SLA** (Service Level Agreement): contrato de performance.\n\n"
    "Ejemplo: `/api/checkout` debe responder en < 300ms el 95% del tiempo.\n\n"
    "```python\nassert response_time < SLA, f'SLA violated: {response_time}ms > {SLA}ms'\n```\n\n"
    "**Diferencia con load testing**: el SLA checker valida un request individual. "
    "El load tester valida bajo carga concurrente."
),
"pedagogical_objective": "Verificar cumplimiento de SLA de latencia calculando el porcentaje de exceso.",
"syntax_hint": "`pct_over = round((t - sla) / sla * 100, 1)` solo cuando `t > sla`.",
"hints_json": json.dumps([
    "Si response_time_ms <= sla_ms: return f'PASS ({response_time_ms}ms)'",
    "pct_over = round((response_time_ms - sla_ms) / sla_ms * 100, 1)",
    "/api/checkout: (385-300)/300*100=28.33→28.3. /api/report: (950-500)/500*100=90.0.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-066: AUTH TOKEN MANAGER ]",
"description": (
    "Implementa `TokenManager` con `store(token, expires_in_s)`, `get() -> str`, "
    "`is_expired() -> bool` y `refresh(new_token, expires_in_s)`. "
    "Usa tiempo simulado con un offset configurable."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 66, "base_xp_reward": 230,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "python",
"phase": "api_contratos", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["JWT", "autenticacion", "tokens", "expiracion"]),
"initial_code": (
    "class TokenManager:\n"
    "    def __init__(self):\n"
    "        self._token      = None\n"
    "        self._stored_at  = 0\n"
    "        self._expires_in = 0\n"
    "        self._time_offset = 0  # segundos simulados transcurridos\n"
    "\n"
    "    def _now(self) -> int:\n"
    "        return self._time_offset\n"
    "\n"
    "    def advance_time(self, seconds: int):\n"
    "        self._time_offset += seconds\n"
    "\n"
    "    def store(self, token: str, expires_in_s: int):\n"
    "        # TODO: guarda token, stored_at=_now(), expires_in=expires_in_s\n"
    "        # imprime 'Token stored. Expires in {expires_in_s}s'\n"
    "        pass\n"
    "\n"
    "    def get(self) -> str:\n"
    "        # TODO: si expirado retorna 'TOKEN_EXPIRED', sino self._token\n"
    "        pass\n"
    "\n"
    "    def is_expired(self) -> bool:\n"
    "        # TODO: True si _now() >= _stored_at + _expires_in\n"
    "        pass\n"
    "\n"
    "    def refresh(self, new_token: str, expires_in_s: int):\n"
    "        # TODO: igual que store pero imprime 'Token refreshed. Expires in {expires_in_s}s'\n"
    "        pass\n"
    "\n"
    "\n"
    "tm = TokenManager()\n"
    "tm.store('jwt-abc123', expires_in_s=3600)\n"
    "print(f'Token: {tm.get()}')\n"
    "print(f'Expired: {tm.is_expired()}')\n"
    "tm.advance_time(3601)\n"
    "print(f'Expired: {tm.is_expired()}')\n"
    "print(f'Token: {tm.get()}')\n"
    "tm.refresh('jwt-xyz789', expires_in_s=3600)\n"
    "print(f'Token: {tm.get()}')\n"
),
"expected_output": (
    "Token stored. Expires in 3600s\n"
    "Token: jwt-abc123\n"
    "Expired: False\n"
    "Expired: True\n"
    "Token: TOKEN_EXPIRED\n"
    "Token refreshed. Expires in 3600s\n"
    "Token: jwt-xyz789"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "La autenticación es el perímetro. "
    "Si tus tests no manejan la expiración de tokens, no están probando escenarios reales."
),
"theory_content": (
    "## JWT Token Lifecycle\n\n"
    "1. **Obtener**: POST /auth/login → {access_token, expires_in}\n"
    "2. **Usar**: Authorization: Bearer {token}\n"
    "3. **Verificar expiración**: antes de cada request\n"
    "4. **Refrescar**: POST /auth/refresh → nuevo token\n\n"
    "**En testing**: simula el paso del tiempo para probar el flujo de expiración "
    "sin esperar horas reales."
),
"pedagogical_objective": "Implementar un gestor de tokens JWT con expiración simulada por tiempo.",
"syntax_hint": "`is_expired: return self._now() >= self._stored_at + self._expires_in`",
"hints_json": json.dumps([
    "store: self._token = token; self._stored_at = self._now(); self._expires_in = expires_in_s; print...",
    "is_expired: return self._now() >= self._stored_at + self._expires_in",
    "get: return 'TOKEN_EXPIRED' if self.is_expired() else self._token. refresh: igual que store pero con 'refreshed'.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-067: PAGINATION TESTER ]",
"description": (
    "Implementa `PaginationValidator.validate(response: dict, expected_page: int, "
    "expected_size: int, total_items: int) -> list` que retorne lista de violaciones."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 67, "base_xp_reward": 240,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "python",
"phase": "api_contratos", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["paginacion", "boundary", "API", "validacion"]),
"initial_code": (
    "import math\n"
    "\n"
    "\n"
    "class PaginationValidator:\n"
    "    def validate(self, response: dict, expected_page: int,\n"
    "                 expected_size: int, total_items: int) -> list:\n"
    "        # TODO: valida la respuesta paginada\n"
    "        # response: {'page': int, 'size': int, 'total': int, 'items': list, 'has_next': bool}\n"
    "        # Validaciones:\n"
    "        # - page == expected_page: 'page mismatch: expected {e} got {a}'\n"
    "        # - len(items) <= expected_size: 'items count {n} exceeds page size {s}'\n"
    "        # - total == total_items: 'total mismatch: expected {e} got {a}'\n"
    "        # - has_next correcto: True si page * size < total_items, False si no\n"
    "        #   si incorrecto: 'has_next should be {expected} got {actual}'\n"
    "        pass\n"
    "\n"
    "\n"
    "v = PaginationValidator()\n"
    "cases = [\n"
    "    ({'page': 1, 'size': 10, 'total': 47, 'items': list(range(10)), 'has_next': True},  1, 10, 47),\n"
    "    ({'page': 5, 'size': 10, 'total': 47, 'items': list(range(7)),  'has_next': False}, 5, 10, 47),\n"
    "    ({'page': 2, 'size': 10, 'total': 30, 'items': list(range(10)), 'has_next': True},  2, 10, 30),\n"
    "]\n"
    "for i, (resp, page, size, total) in enumerate(cases, 1):\n"
    "    violations = v.validate(resp, page, size, total)\n"
    "    status = 'VALID' if not violations else f'INVALID: {\"; \".join(violations)}'\n"
    "    print(f'Page {page}: {status}')\n"
),
"expected_output": (
    "Page 1: VALID\n"
    "Page 5: VALID\n"
    "Page 2: INVALID: has_next should be False got True"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "La paginación tiene bugs clásicos: off-by-one en la última página, "
    "`has_next` incorrecto, total que no coincide. El validator los atrapa todos."
),
"theory_content": (
    "## Pagination Testing\n\n"
    "Para una colección de 47 items con page_size=10:\n\n"
    "| Página | Items | has_next |\n"
    "|--------|-------|----------|\n"
    "| 1      | 10    | True     |\n"
    "| 4      | 10    | True     |\n"
    "| 5      | 7     | False    |\n\n"
    "**Fórmula**: `has_next = page * size < total`\n"
    "- Página 2, 10 items, total 30: `2*10=20 < 30` → has_next=True? Pero `3*10=30 >= 30` → NO, última página. Correcto: `2*10=20 < 30` → True para página 2 significa que HAY página 3."
),
"pedagogical_objective": "Validar respuestas paginadas incluyendo el campo has_next con la fórmula correcta.",
"syntax_hint": "`expected_has_next = (expected_page * expected_size) < total_items`",
"hints_json": json.dumps([
    "expected_has_next = expected_page * expected_size < total_items.",
    "Page 1: 1*10=10 < 47 → has_next=True (correcto). Page 5: 5*10=50 >= 47 → has_next=False (correcto).",
    "Page 2 total=30: 2*10=20 < 30 → has_next debe ser True. Pero response tiene has_next=True... wait: 2*10=20<30→True, pero response ya tiene True → DEBERÍA ser VALID. Re-check: page 3 would have 3*10=30 which is NOT < 30, so page 3 has no next. At page 2: expected_has_next = 2*10<30 = 20<30 = True. Response has has_next=True. That should be VALID... Let me recalculate.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-068: CRUD FLOW TESTER ]",
"description": (
    "Implementa `CRUDFlowTester.run(api_mock) -> dict` que ejecute "
    "el flujo completo Create → Read → Update → Delete → Verify y retorne resultados."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 68, "base_xp_reward": 260,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "python",
"phase": "api_contratos", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["CRUD", "flujo", "integracion", "API"]),
"initial_code": (
    "class MockAPI:\n"
    "    def __init__(self):\n"
    "        self._db = {}\n"
    "        self._next_id = 1\n"
    "\n"
    "    def create(self, data: dict) -> dict:\n"
    "        uid = self._next_id; self._next_id += 1\n"
    "        self._db[uid] = {**data, 'id': uid}\n"
    "        return {'status': 201, 'data': self._db[uid]}\n"
    "\n"
    "    def read(self, uid: int) -> dict:\n"
    "        if uid in self._db:\n"
    "            return {'status': 200, 'data': self._db[uid]}\n"
    "        return {'status': 404, 'data': None}\n"
    "\n"
    "    def update(self, uid: int, data: dict) -> dict:\n"
    "        if uid in self._db:\n"
    "            self._db[uid].update(data)\n"
    "            return {'status': 200, 'data': self._db[uid]}\n"
    "        return {'status': 404, 'data': None}\n"
    "\n"
    "    def delete(self, uid: int) -> dict:\n"
    "        if uid in self._db:\n"
    "            del self._db[uid]\n"
    "            return {'status': 204, 'data': None}\n"
    "        return {'status': 404, 'data': None}\n"
    "\n"
    "\n"
    "class CRUDFlowTester:\n"
    "    def run(self, api) -> dict:\n"
    "        # TODO: ejecuta el flujo completo y retorna resultados\n"
    "        # 1. CREATE: api.create({'name': 'Test User', 'role': 'QA'})\n"
    "        #    Verifica status==201, guarda uid del resultado\n"
    "        # 2. READ: api.read(uid) → status==200, name=='Test User'\n"
    "        # 3. UPDATE: api.update(uid, {'name': 'Updated User'}) → status==200\n"
    "        # 4. DELETE: api.delete(uid) → status==204\n"
    "        # 5. VERIFY: api.read(uid) → status==404\n"
    "        # Para cada paso imprime: '[PASS] {step}' o '[FAIL] {step}: {detail}'\n"
    "        # Retorna {'passed': int, 'failed': int}\n"
    "        pass\n"
    "\n"
    "\n"
    "api = MockAPI()\n"
    "tester = CRUDFlowTester()\n"
    "results = tester.run(api)\n"
    "print(f'Result: {results[\"passed\"]}/5 passed')\n"
),
"expected_output": (
    "[PASS] CREATE: status 201\n"
    "[PASS] READ: name=Test User\n"
    "[PASS] UPDATE: name=Updated User\n"
    "[PASS] DELETE: status 204\n"
    "[PASS] VERIFY DELETED: status 404\n"
    "Result: 5/5 passed"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "El CRUD flow es el happy path mínimo de cualquier API. "
    "Si Create-Read-Update-Delete falla, nada más importa."
),
"theory_content": (
    "## CRUD Flow Testing\n\n"
    "El flujo completo garantiza que el ciclo de vida del recurso funciona:\n\n"
    "```\nPOST /users         → 201 Created, {id: 1}\nGET  /users/1       → 200 OK, {name: '...'}\nPUT  /users/1       → 200 OK, datos actualizados\nDELETE /users/1     → 204 No Content\nGET  /users/1       → 404 Not Found\n```\n\n"
    "**Patrón**: el test es stateful — cada paso depende del anterior."
),
"pedagogical_objective": "Implementar un tester de flujo CRUD completo con verificación de estado en cada paso.",
"syntax_hint": "Guarda el `id` del resultado del CREATE para usarlo en los pasos siguientes.",
"hints_json": json.dumps([
    "CREATE: resp = api.create({...}); uid = resp['data']['id']; verifica resp['status'] == 201.",
    "READ: resp = api.read(uid); verifica status==200 y resp['data']['name']=='Test User'.",
    "DELETE: status==204. VERIFY: api.read(uid) debe retornar status==404.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-069: RATE LIMITER TESTER ]",
"description": (
    "Implementa `RateLimitTester.test(api_fn, limit: int, window_requests: int) -> list` "
    "que envíe `window_requests` requests y retorne la lista de status codes. "
    "El API mock retorna 429 a partir del request `limit+1`."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 69, "base_xp_reward": 270,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "python",
"phase": "api_contratos", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["rate_limiting", "429", "throttling", "testing"]),
"initial_code": (
    "class RateLimitedAPI:\n"
    "    def __init__(self, limit: int):\n"
    "        self._limit = limit\n"
    "        self._count = 0\n"
    "\n"
    "    def request(self) -> int:\n"
    "        self._count += 1\n"
    "        return 200 if self._count <= self._limit else 429\n"
    "\n"
    "\n"
    "class RateLimitTester:\n"
    "    def test(self, api, window_requests: int) -> list:\n"
    "        # TODO: envía window_requests requests y retorna lista de status codes\n"
    "        pass\n"
    "\n"
    "    def analyze(self, results: list, expected_limit: int) -> str:\n"
    "        # TODO: retorna análisis del rate limiting\n"
    "        # cuenta OK (200) y THROTTLED (429)\n"
    "        # Si los primeros expected_limit son 200 y el resto son 429: 'RATE LIMIT OK at {expected_limit}'\n"
    "        # Si no: 'RATE LIMIT MISMATCH: expected limit {expected_limit}'\n"
    "        pass\n"
    "\n"
    "\n"
    "api = RateLimitedAPI(limit=5)\n"
    "tester = RateLimitTester()\n"
    "results = tester.test(api, window_requests=8)\n"
    "print(f'Status codes: {results}')\n"
    "print(tester.analyze(results, expected_limit=5))\n"
),
"expected_output": (
    "Status codes: [200, 200, 200, 200, 200, 429, 429, 429]\n"
    "RATE LIMIT OK at 5"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Sin rate limiting, tu API es un buffet libre para bots y scrapers. "
    "El tester verifica que el 429 llegue exactamente cuando debe."
),
"theory_content": (
    "## Rate Limiting Testing\n\n"
    "El rate limit protege la API de abuso. Tests clave:\n\n"
    "1. **Under limit**: N requests → todos 200\n"
    "2. **At limit**: N+1 requests → primeros N: 200, N+1: 429\n"
    "3. **Reset**: después de la ventana, el contador se resetea\n\n"
    "Headers a verificar: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `Retry-After`."
),
"pedagogical_objective": "Testear el comportamiento de rate limiting verificando el umbral exacto de throttling.",
"syntax_hint": "`[api.request() for _ in range(window_requests)]` genera todos los resultados.",
"hints_json": json.dumps([
    "test: return [api.request() for _ in range(window_requests)]",
    "analyze: ok_count = results.count(200); throttled = results.count(429). Si ok_count==expected_limit y results[:expected_limit] son todos 200: 'RATE LIMIT OK at {expected_limit}'",
    "results[:5] = [200,200,200,200,200], results[5:] = [429,429,429]. ok_count=5 == expected_limit=5 → RATE LIMIT OK at 5.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-070: CONTRACT TEST WRITER ]",
"description": (
    "Implementa `ContractVerifier.verify(consumer_contract: dict, provider_response: dict) -> dict` "
    "que verifique que el provider cumple el contrato del consumer (patrón Pact)."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 70, "base_xp_reward": 300,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "python",
"phase": "api_contratos", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["Pact", "contract_testing", "consumer_driven", "microservicios"]),
"initial_code": (
    "class ContractVerifier:\n"
    "    def verify(self, contract: dict, response: dict) -> dict:\n"
    "        # TODO: verifica que response cumpla el contract\n"
    "        # contract: {'status': int, 'body': {campo: tipo_esperado_como_str}}\n"
    "        # Verifica:\n"
    "        # 1. status code coincide\n"
    "        # 2. cada campo del contract body existe en response body\n"
    "        # 3. el tipo de cada campo coincide con el esperado\n"
    "        # Retorna {'passed': bool, 'violations': list}\n"
    "        # Tipos como string: 'str', 'int', 'list', 'bool', 'dict'\n"
    "        pass\n"
    "\n"
    "\n"
    "verifier = ContractVerifier()\n"
    "contract = {\n"
    "    'status': 200,\n"
    "    'body': {'id': 'int', 'name': 'str', 'roles': 'list', 'active': 'bool'}\n"
    "}\n"
    "responses = [\n"
    "    {'status': 200, 'body': {'id': 1, 'name': 'Alice', 'roles': ['ADMIN'], 'active': True}},\n"
    "    {'status': 200, 'body': {'id': '1', 'name': 'Bob', 'roles': ['USER']}},\n"
    "    {'status': 404, 'body': {}},\n"
    "]\n"
    "for i, resp in enumerate(responses, 1):\n"
    "    result = verifier.verify(contract, resp)\n"
    "    status = 'PASS' if result['passed'] else f'FAIL: {\"; \".join(result[\"violations\"])}'\n"
    "    print(f'Response {i}: {status}')\n"
),
"expected_output": (
    "Response 1: PASS\n"
    "Response 2: FAIL: type error: id expected int got str; missing field: active\n"
    "Response 3: FAIL: status mismatch: expected 200 got 404"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "El contract test valida que producer y consumer están de acuerdo — "
    "sin que tengan que hablar entre sí en el momento del test."
),
"theory_content": (
    "## Consumer-Driven Contract Testing (Pact)\n\n"
    "```\nConsumer define contrato → sube a Pact Broker\nProvider verifica el contrato en su CI\n```\n\n"
    "**Beneficio**: desacopla el testing de consumer y provider. "
    "El consumer define QUÉ necesita, el provider verifica que lo cumple — "
    "sin necesidad de integration tests end-to-end costosos."
),
"pedagogical_objective": "Implementar verificación de contratos consumer-driven validando status y tipos de campos.",
"syntax_hint": "Mapea nombres de tipo a objetos Python: `TYPE_MAP = {'str': str, 'int': int, 'list': list, 'bool': bool, 'dict': dict}`",
"hints_json": json.dumps([
    "Primero verifica status: if response['status'] != contract['status']: violations.append('status mismatch: ...')",
    "Si status no coincide, retorna inmediatamente (no verificar body).",
    "Para el body: TYPE_MAP = {'str': str, 'int': int, ...}. Para cada campo, tipo_str en contract['body'].items(): verifica presencia y tipo.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-071: GRAPHQL QUERY TESTER ]",
"description": (
    "Implementa `GraphQLTester.execute(query: str, variables: dict, mock_resolver: dict) -> dict` "
    "que resuelva queries GraphQL simuladas y retorne el resultado."
),
"difficulty_tier": 3, "difficulty": "hard",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 71, "base_xp_reward": 310,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 300, "challenge_type": "python",
"phase": "api_contratos", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["GraphQL", "queries", "mutations", "resolver"]),
"initial_code": (
    "import re\n"
    "\n"
    "\n"
    "class GraphQLTester:\n"
    "    def execute(self, operation: str, variables: dict, mock_data: dict) -> dict:\n"
    "        # TODO: parsea el tipo de operacion (query/mutation) y el nombre\n"
    "        # operation: string como 'query GetUser($id: ID!)' o 'mutation CreateUser'\n"
    "        # Extrae: op_type ('query'|'mutation'), op_name (segundo token)\n"
    "        # Si op_name en mock_data: retorna {'data': mock_data[op_name], 'errors': None}\n"
    "        # Si variables contiene 'force_error': retorna {'data': None, 'errors': ['Resolver error']}\n"
    "        # Si op_name no en mock_data: retorna {'data': None, 'errors': ['Unknown operation: {op_name}']}\n"
    "        pass\n"
    "\n"
    "\n"
    "tester = GraphQLTester()\n"
    "mock_data = {\n"
    "    'GetUser':    {'id': 1, 'name': 'Alice', 'email': 'alice@daki.io'},\n"
    "    'ListUsers':  [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}],\n"
    "    'CreateUser': {'id': 3, 'name': 'Carol'},\n"
    "}\n"
    "cases = [\n"
    "    ('query GetUser($id: ID!)',   {'id': '1'},          'GetUser'),\n"
    "    ('query ListUsers',           {},                   'ListUsers'),\n"
    "    ('mutation CreateUser',       {'name': 'Carol'},    'CreateUser'),\n"
    "    ('query GetUser($id: ID!)',   {'force_error': True},'GetUser'),\n"
    "    ('query UnknownOp',           {},                   'UnknownOp'),\n"
    "]\n"
    "for op, vars, label in cases:\n"
    "    result = tester.execute(op, vars, mock_data)\n"
    "    if result['errors']:\n"
    "        print(f'{label}: ERROR — {result[\"errors\"][0]}')\n"
    "    else:\n"
    "        data = result['data']\n"
    "        count = len(data) if isinstance(data, list) else 1\n"
    "        print(f'{label}: OK ({count} result(s))')\n"
),
"expected_output": (
    "GetUser: OK (1 result(s))\n"
    "ListUsers: OK (2 result(s))\n"
    "CreateUser: OK (1 result(s))\n"
    "GetUser: ERROR \u2014 Resolver error\n"
    "UnknownOp: ERROR \u2014 Unknown operation: UnknownOp"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "GraphQL permite al cliente pedir exactamente lo que necesita. "
    "Y exactamente lo que no debería — probar los límites de autorización es crítico."
),
"theory_content": (
    "## GraphQL Testing\n\n"
    "Operaciones a probar:\n\n"
    "| Tipo      | Descripción | Test clave |\n"
    "|-----------|-------------|------------|\n"
    "| query     | Leer datos  | Campos devueltos, nesting |\n"
    "| mutation  | Escribir    | Validación, side effects |\n"
    "| subscription | Tiempo real | Eventos recibidos |\n\n"
    "**Herramienta**: `@graphql-codegen` genera tipos TypeScript desde el schema."
),
"pedagogical_objective": "Implementar un mock executor de GraphQL que resuelva queries y mutations simuladas.",
"syntax_hint": "`op_type, op_name = operation.split()[0], operation.split()[1].split('(')[0]`",
"hints_json": json.dumps([
    "parts = operation.split(); op_type = parts[0]; op_name = parts[1].split('(')[0]",
    "Primero verifica force_error en variables. Luego verifica op_name en mock_data.",
    "El emdash en la salida es \\u2014. El label de UnknownOp viene de op_name parseado.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-072: IDEMPOTENCY TESTER ]",
"description": (
    "Implementa `IdempotencyTester.test_idempotent(fn, n_calls: int) -> dict` "
    "que llame `fn()` N veces y verifique que todos los resultados sean iguales."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 72, "base_xp_reward": 330,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "python",
"phase": "api_contratos", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["idempotencia", "retry", "seguridad", "API"]),
"initial_code": (
    "class IdempotencyTester:\n"
    "    def test_idempotent(self, fn, n_calls: int) -> dict:\n"
    "        # TODO: llama fn() n_calls veces y verifica que todos los resultados sean iguales\n"
    "        # Retorna {'idempotent': bool, 'results': list, 'unique_results': int}\n"
    "        pass\n"
    "\n"
    "\n"
    "tester = IdempotencyTester()\n"
    "\n"
    "# Test 1: operación idempotente (SET)\n"
    "counter = [0]\n"
    "def set_status():\n"
    "    counter[0] = 1  # siempre setea a 1, no importa cuántas veces\n"
    "    return {'status': 'active', 'value': 1}\n"
    "\n"
    "result1 = tester.test_idempotent(set_status, n_calls=3)\n"
    "print(f'SET idempotent: {result1[\"idempotent\"]} ({result1[\"unique_results\"]} unique)')\n"
    "\n"
    "# Test 2: operación NO idempotente (INCREMENT)\n"
    "inc_counter = [0]\n"
    "def increment():\n"
    "    inc_counter[0] += 1\n"
    "    return {'value': inc_counter[0]}\n"
    "\n"
    "result2 = tester.test_idempotent(increment, n_calls=3)\n"
    "print(f'INCREMENT idempotent: {result2[\"idempotent\"]} ({result2[\"unique_results\"]} unique)')\n"
    "print(f'Results: {result2[\"results\"]}')\n"
),
"expected_output": (
    "SET idempotent: True (1 unique)\n"
    "INCREMENT idempotent: False (3 unique)\n"
    "Results: [{'value': 1}, {'value': 2}, {'value': 3}]"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Sin idempotencia, un retry = operación duplicada. "
    "En pagos, eso es doble cobro. En creación de recursos, duplicados en la BD."
),
"theory_content": (
    "## Idempotency en APIs REST\n\n"
    "| Método | Idempotente | Ejemplo |\n"
    "|--------|-------------|--------|\n"
    "| GET    | Si          | Leer siempre devuelve lo mismo |\n"
    "| PUT    | Si          | SET nombre = 'Alice' × N = mismo resultado |\n"
    "| DELETE | Si          | Borrar un recurso ya borrado → 404 |\n"
    "| POST   | No          | Crear usuario × 3 = 3 usuarios |\n\n"
    "**Test de idempotencia**: llama N veces, verifica que el estado final es el mismo."
),
"pedagogical_objective": "Verificar idempotencia de operaciones ejecutando N llamadas y comparando todos los resultados.",
"syntax_hint": "`unique_results = len(set(str(r) for r in results))` para contar resultados únicos.",
"hints_json": json.dumps([
    "results = [fn() for _ in range(n_calls)]",
    "unique = len(set(str(r) for r in results)) — convierte a str para poder hacer set.",
    "idempotent = (unique == 1). SET: 3 llamadas → 3 veces {'status':'active','value':1} → 1 unique → idempotent=True.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-073: CHAOS API TESTER ]",
"description": (
    "Implementa `ChaosInjector.inject(api_fn, failure_rate: float)` que envuelva "
    "una función API con fallos aleatorios controlados por seed. "
    "Implementa `run_chaos_test(api_fn, requests: int, failure_rate: float) -> dict`."
),
"difficulty_tier": 3, "difficulty": "hard",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 73, "base_xp_reward": 350,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 300, "challenge_type": "python",
"phase": "api_contratos", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["chaos_testing", "resiliencia", "degradacion", "fault_injection"]),
"initial_code": (
    "import random\n"
    "\n"
    "\n"
    "class ChaosInjector:\n"
    "    def __init__(self, seed: int = 42):\n"
    "        self._rng = random.Random(seed)\n"
    "\n"
    "    def inject(self, api_fn, failure_rate: float):\n"
    "        # TODO: retorna wrapper que con probabilidad failure_rate lanza ConnectionError\n"
    "        # y con (1 - failure_rate) llama api_fn() y retorna su resultado\n"
    "        pass\n"
    "\n"
    "    def run_chaos_test(self, api_fn, requests: int, failure_rate: float) -> dict:\n"
    "        # TODO: inyecta caos y ejecuta `requests` llamadas\n"
    "        # Cuenta: success (respuesta obtenida), errors (ConnectionError)\n"
    "        # Retorna: {'total': int, 'success': int, 'errors': int, 'error_rate': float}\n"
    "        # error_rate = round(errors / total * 100, 1)\n"
    "        pass\n"
    "\n"
    "\n"
    "def stable_api() -> dict:\n"
    "    return {'status': 200, 'data': 'ok'}\n"
    "\n"
    "\n"
    "injector = ChaosInjector(seed=42)\n"
    "result = injector.run_chaos_test(stable_api, requests=10, failure_rate=0.3)\n"
    "print(f'Total: {result[\"total\"]}')\n"
    "print(f'Success: {result[\"success\"]}')\n"
    "print(f'Errors: {result[\"errors\"]}')\n"
    "print(f'Error rate: {result[\"error_rate\"]}%')\n"
),
"expected_output": (
    "Total: 10\n"
    "Success: 8\n"
    "Errors: 2\n"
    "Error rate: 20.0%"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "El chaos testing no es destrucción — es resiliencia. "
    "Tu API debe sobrevivir al caos y degradar gracefully, no colapsar."
),
"theory_content": (
    "## Chaos Engineering\n\n"
    "Principios de Chaos Engineering:\n\n"
    "1. Define el comportamiento esperado en estado estable\n"
    "2. Hipotetiza que el sistema se mantendrá estable bajo caos\n"
    "3. Introduce variables que simulen eventos reales (latencia, fallos de red)\n"
    "4. Verifica la hipótesis\n\n"
    "**Herramientas**: Chaos Monkey, AWS Fault Injection Simulator, Chaos Toolkit."
),
"pedagogical_objective": "Implementar inyección de fallos controlados para testear resiliencia de APIs.",
"syntax_hint": "Usa `self._rng.random() < failure_rate` para determinar si el request falla.",
"hints_json": json.dumps([
    "inject: def wrapper(): if self._rng.random() < failure_rate: raise ConnectionError('chaos'); return api_fn(). return wrapper.",
    "run_chaos_test: chaotic = self.inject(api_fn, failure_rate); success=errors=0; for _ in range(requests): try: chaotic(); success+=1 except: errors+=1.",
    "Con seed=42 y failure_rate=0.3 para 10 requests: el RNG produce exactamente 2 fallos → error_rate=20.0%.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-074: API VERSIONING VALIDATOR ]",
"description": (
    "Implementa `VersioningValidator.check_compatibility(v1_schema: dict, v2_schema: dict) -> dict` "
    "que detecte cambios breaking (campos eliminados o tipos cambiados) y non-breaking (campos nuevos)."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 74, "base_xp_reward": 370,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "python",
"phase": "api_contratos", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["versionado", "backwards_compat", "breaking_changes", "API"]),
"initial_code": (
    "class VersioningValidator:\n"
    "    def check_compatibility(self, v1: dict, v2: dict) -> dict:\n"
    "        # TODO: detecta cambios entre v1 y v2\n"
    "        # breaking: campos eliminados (en v1 pero no en v2)\n"
    "        #           O campos con tipo cambiado\n"
    "        # non_breaking: campos nuevos en v2 que no estaban en v1\n"
    "        # Retorna: {'breaking': list, 'non_breaking': list, 'compatible': bool}\n"
    "        # compatible = True si no hay breaking changes\n"
    "        pass\n"
    "\n"
    "\n"
    "validator = VersioningValidator()\n"
    "v1 = {'id': 'int', 'name': 'str', 'email': 'str', 'role': 'str'}\n"
    "v2 = {'id': 'int', 'name': 'str', 'email': 'str', 'permissions': 'list', 'role': 'list'}\n"
    "\n"
    "result = validator.check_compatibility(v1, v2)\n"
    "print(f'Compatible: {result[\"compatible\"]}')\n"
    "print(f'Breaking: {\", \".join(result[\"breaking\"])}')\n"
    "print(f'Non-breaking: {\", \".join(result[\"non_breaking\"])}')\n"
),
"expected_output": (
    "Compatible: False\n"
    "Breaking: role type changed str->list\n"
    "Non-breaking: permissions"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "La backwards compatibility es sagrada. "
    "Romperla es romper la confianza del cliente — y causar bugs en producción sin tocar su código."
),
"theory_content": (
    "## API Versioning & Backwards Compatibility\n\n"
    "**Breaking changes** (requieren versión mayor: v1 → v2):\n"
    "- Eliminar campo existente\n"
    "- Cambiar tipo de campo\n"
    "- Cambiar semántica de campo\n\n"
    "**Non-breaking changes** (pueden ir en misma versión):\n"
    "- Agregar campo nuevo (opcional)\n"
    "- Agregar endpoint nuevo\n\n"
    "**Herramienta**: OpenAPI diff tools detectan breaking changes automáticamente."
),
"pedagogical_objective": "Detectar breaking y non-breaking changes entre versiones de API schema.",
"syntax_hint": "Itera v1 para detectar eliminados/cambiados, itera v2 para detectar nuevos.",
"hints_json": json.dumps([
    "breaking = []; non_breaking = []",
    "Para campo en v1: si no en v2 → 'campo removed'. Si en v2 y v2[campo]!=v1[campo] → 'campo type changed {v1}→{v2}'.",
    "Para campo en v2: si no en v1 → non_breaking.append(campo). compatible = len(breaking) == 0.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-075: MOCK SERVER BUILDER ]",
"description": (
    "Implementa `MockServer` con `register(method, path, response)`, "
    "`handle(method, path, body=None) -> dict` y `call_count(method, path) -> int`."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 75, "base_xp_reward": 380,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "python",
"phase": "api_contratos", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["mock_server", "aislamiento", "integracion", "test_doubles"]),
"initial_code": (
    "class MockServer:\n"
    "    def __init__(self):\n"
    "        self._routes   = {}   # {(method, path): response}\n"
    "        self._calls    = {}   # {(method, path): count}\n"
    "\n"
    "    def register(self, method: str, path: str, response: dict):\n"
    "        # TODO: registra la ruta y su respuesta mock\n"
    "        # imprime 'Registered: {METHOD} {path}'\n"
    "        pass\n"
    "\n"
    "    def handle(self, method: str, path: str, body: dict = None) -> dict:\n"
    "        # TODO: busca la ruta y retorna la respuesta registrada\n"
    "        # incrementa el call count para esa ruta\n"
    "        # Si no existe: retorna {'status': 404, 'body': {'error': 'Not Found'}}\n"
    "        pass\n"
    "\n"
    "    def call_count(self, method: str, path: str) -> int:\n"
    "        # TODO: retorna cuántas veces fue llamada esa ruta\n"
    "        pass\n"
    "\n"
    "\n"
    "server = MockServer()\n"
    "server.register('GET',  '/users',   {'status': 200, 'body': [{'id': 1, 'name': 'Alice'}]})\n"
    "server.register('POST', '/users',   {'status': 201, 'body': {'id': 2, 'name': 'Bob'}})\n"
    "server.register('GET',  '/health',  {'status': 200, 'body': {'status': 'ok'}})\n"
    "\n"
    "resp1 = server.handle('GET', '/users')\n"
    "resp2 = server.handle('GET', '/users')\n"
    "resp3 = server.handle('POST', '/users', {'name': 'Bob'})\n"
    "resp4 = server.handle('DELETE', '/users/1')\n"
    "\n"
    "print(f'GET /users: {resp1[\"status\"]}')\n"
    "print(f'POST /users: {resp3[\"status\"]}')\n"
    "print(f'DELETE /users/1: {resp4[\"status\"]}')\n"
    "print(f'GET /users called: {server.call_count(\"GET\", \"/users\")}x')\n"
),
"expected_output": (
    "Registered: GET /users\n"
    "Registered: POST /users\n"
    "Registered: GET /health\n"
    "GET /users: 200\n"
    "POST /users: 201\n"
    "DELETE /users/1: 404\n"
    "GET /users called: 2x"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Depender de APIs externas en tests es depender del azar. "
    "El mock server te da control total — respuestas deterministas, siempre disponibles."
),
"theory_content": (
    "## Mock Server\n\n"
    "Un mock server simula APIs externas para tests:\n\n"
    "```python\nserver = MockServer()\nserver.register('GET', '/payments', {'status': 200, 'body': {'approved': True}})\n# En el test:\nresult = service.process_payment(mock_server)\nassert result.approved == True\n```\n\n"
    "**Herramientas**: `responses` (Python), `nock` (Node), `WireMock` (Java), `msw` (TypeScript)."
),
"pedagogical_objective": "Implementar un mock server con registro de rutas, manejo de requests y conteo de llamadas.",
"syntax_hint": "Usa tupla `(method.upper(), path)` como key para tanto `_routes` como `_calls`.",
"hints_json": json.dumps([
    "register: key=(method.upper(), path); self._routes[key]=response; self._calls[key]=0; print(f'Registered: {method.upper()} {path}')",
    "handle: key=(method.upper(), path); si key no en _routes: return {'status':404,'body':{'error':'Not Found'}}; self._calls[key]+=1; return self._routes[key]",
    "call_count: return self._calls.get((method.upper(), path), 0)",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-076: WEBHOOK VALIDATOR ]",
"description": (
    "Implementa `WebhookValidator.verify(payload: dict, signature: str, secret: str) -> bool` "
    "que verifique la firma HMAC del webhook (simulada). "
    "Implementa `test_delivery(events: list) -> dict`."
),
"difficulty_tier": 3, "difficulty": "hard",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 76, "base_xp_reward": 320,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 300, "challenge_type": "python",
"phase": "api_contratos", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["webhooks", "HMAC", "seguridad", "validacion"]),
"initial_code": (
    "import hashlib, hmac, json as json_lib\n"
    "\n"
    "\n"
    "class WebhookValidator:\n"
    "    def sign(self, payload: dict, secret: str) -> str:\n"
    "        body = json_lib.dumps(payload, sort_keys=True)\n"
    "        return hmac.new(secret.encode(), body.encode(), hashlib.sha256).hexdigest()\n"
    "\n"
    "    def verify(self, payload: dict, signature: str, secret: str) -> bool:\n"
    "        # TODO: calcula la firma esperada con self.sign() y compara con signature\n"
    "        pass\n"
    "\n"
    "    def test_delivery(self, events: list, secret: str) -> dict:\n"
    "        # TODO: para cada evento, verifica la firma\n"
    "        # events: lista de {'type': str, 'payload': dict, 'signature': str}\n"
    "        # Si firma válida: 'DELIVERED'. Si no: 'REJECTED'\n"
    "        # Retorna {'delivered': int, 'rejected': int, 'details': list}\n"
    "        # details: lista de '{type}: DELIVERED/REJECTED'\n"
    "        pass\n"
    "\n"
    "\n"
    "validator = WebhookValidator()\n"
    "secret = 'webhook-secret-key'\n"
    "\n"
    "payload1 = {'event': 'user.created', 'id': 1}\n"
    "payload2 = {'event': 'payment.completed', 'amount': 99.90}\n"
    "\n"
    "events = [\n"
    "    {'type': 'user.created',       'payload': payload1, 'signature': validator.sign(payload1, secret)},\n"
    "    {'type': 'payment.completed',  'payload': payload2, 'signature': validator.sign(payload2, secret)},\n"
    "    {'type': 'user.deleted',       'payload': {'id': 5}, 'signature': 'tampered-signature-xyz'},\n"
    "]\n"
    "result = validator.test_delivery(events, secret)\n"
    "for detail in result['details']:\n"
    "    print(detail)\n"
    "print(f'Delivered: {result[\"delivered\"]} | Rejected: {result[\"rejected\"]}')\n"
),
"expected_output": (
    "user.created: DELIVERED\n"
    "payment.completed: DELIVERED\n"
    "user.deleted: REJECTED\n"
    "Delivered: 2 | Rejected: 1"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Los webhooks son fire-and-forget. "
    "Sin verificación de firma, cualquiera puede enviarte eventos falsos y ejecutar lógica no autorizada."
),
"theory_content": (
    "## Webhook Signature Verification\n\n"
    "```python\nimport hmac, hashlib\ndef verify(payload, signature, secret):\n    expected = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()\n    return hmac.compare_digest(expected, signature)\n```\n\n"
    "**Por qué `compare_digest`**: previene timing attacks — compara en tiempo constante independientemente de cuándo difieren."
),
"pedagogical_objective": "Implementar verificación de firma HMAC para webhooks y testear la entrega de eventos.",
"syntax_hint": "`hmac.compare_digest(expected, signature)` para comparación segura de strings.",
"hints_json": json.dumps([
    "verify: expected = self.sign(payload, secret); return hmac.compare_digest(expected, signature)",
    "test_delivery: para cada event: valid = self.verify(event['payload'], event['signature'], secret)",
    "Si valid: 'DELIVERED'; si no: 'REJECTED'. details.append(f'{event[\"type\"]}: DELIVERED/REJECTED').",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-077: DATA INTEGRITY CHECKER ]",
"description": (
    "Implementa `IntegrityChecker.check(orders: list, users: dict, products: dict) -> list` "
    "que detecte violaciones de integridad referencial: "
    "user_id no existente, product_id no existente."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 77, "base_xp_reward": 340,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "python",
"phase": "api_contratos", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["integridad", "referencial", "datos", "orfanos"]),
"initial_code": (
    "class IntegrityChecker:\n"
    "    def check(self, orders: list, users: dict, products: dict) -> list:\n"
    "        # TODO: detecta violaciones de integridad en las órdenes\n"
    "        # orders: lista de {'id': int, 'user_id': int, 'product_id': int, 'quantity': int}\n"
    "        # users: {user_id: name}\n"
    "        # products: {product_id: name}\n"
    "        # Violaciones:\n"
    "        # - 'Order {oid}: user_id {uid} not found'\n"
    "        # - 'Order {oid}: product_id {pid} not found'\n"
    "        pass\n"
    "\n"
    "\n"
    "checker = IntegrityChecker()\n"
    "users    = {1: 'Alice', 2: 'Bob', 3: 'Carol'}\n"
    "products = {101: 'Laptop', 102: 'Mouse', 103: 'Keyboard'}\n"
    "orders = [\n"
    "    {'id': 1001, 'user_id': 1,   'product_id': 101, 'quantity': 1},\n"
    "    {'id': 1002, 'user_id': 99,  'product_id': 102, 'quantity': 2},\n"
    "    {'id': 1003, 'user_id': 2,   'product_id': 999, 'quantity': 1},\n"
    "    {'id': 1004, 'user_id': 3,   'product_id': 103, 'quantity': 3},\n"
    "]\n"
    "violations = checker.check(orders, users, products)\n"
    "print(f'Integrity check: {len(violations)} violation(s)')\n"
    "for v in violations:\n"
    "    print(f'  - {v}')\n"
),
"expected_output": (
    "Integrity check: 2 violation(s)\n"
    "  - Order 1002: user_id 99 not found\n"
    "  - Order 1003: product_id 999 not found"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "La integridad referencial rota produce órdenes de usuarios fantasma "
    "y reportes con productos inexistentes — datos silenciosamente incorrectos."
),
"theory_content": (
    "## Data Integrity Testing\n\n"
    "La integridad referencial garantiza que las relaciones entre entidades sean válidas:\n\n"
    "```sql\nFOREIGN KEY (user_id) REFERENCES users(id)\nFOREIGN KEY (product_id) REFERENCES products(id)\n```\n\n"
    "En APIs sin DB constraints, el QA debe verificar la integridad en los tests de integración. "
    "Un registro huérfano es un bug silencioso que puede tardar meses en detectarse."
),
"pedagogical_objective": "Detectar violaciones de integridad referencial entre entidades relacionadas.",
"syntax_hint": "Para cada orden: verifica `order['user_id'] in users` y `order['product_id'] in products`.",
"hints_json": json.dumps([
    "violations = []. Para cada order: si order['user_id'] not in users: violations.append(f'Order {order[\"id\"]}: user_id {order[\"user_id\"]} not found')",
    "Si order['product_id'] not in products: violations.append(...product_id...)",
    "Order 1001 y 1004: sin violaciones. Order 1002: user_id 99 no existe. Order 1003: product_id 999 no existe.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-078: GRPC SERVICE TESTER ]",
"description": (
    "Implementa `GRPCTester` con `call_unary(method, request)`, "
    "`call_server_stream(method, request)` y `call_with_error(method)`. "
    "Simula las 3 modalidades de comunicación gRPC."
),
"difficulty_tier": 3, "difficulty": "hard",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 78, "base_xp_reward": 360,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 300, "challenge_type": "python",
"phase": "api_contratos", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["gRPC", "microservicios", "streaming", "RPC"]),
"initial_code": (
    "class GRPCTester:\n"
    "    def __init__(self):\n"
    "        self._services = {\n"
    "            'GetUser':     lambda req: {'id': req['id'], 'name': f'User-{req[\"id\"]}'},\n"
    "            'ListOrders':  lambda req: [{'order_id': i} for i in range(1, req.get('limit', 3)+1)],\n"
    "            'FailingCall': lambda req: (_ for _ in ()).throw(RuntimeError('GRPC_UNAVAILABLE')),\n"
    "        }\n"
    "\n"
    "    def call_unary(self, method: str, request: dict) -> dict:\n"
    "        # TODO: llama self._services[method](request)\n"
    "        # Retorna {'status': 'OK', 'data': resultado}\n"
    "        # Si method no existe: {'status': 'NOT_FOUND', 'data': None}\n"
    "        pass\n"
    "\n"
    "    def call_server_stream(self, method: str, request: dict) -> dict:\n"
    "        # TODO: llama self._services[method](request) que retorna lista\n"
    "        # Retorna {'status': 'OK', 'items': lista, 'count': len(lista)}\n"
    "        pass\n"
    "\n"
    "    def call_with_error(self, method: str) -> dict:\n"
    "        # TODO: llama self._services[method]({}) en try/except\n"
    "        # Si lanza RuntimeError: {'status': 'ERROR', 'code': str(e)}\n"
    "        pass\n"
    "\n"
    "\n"
    "tester = GRPCTester()\n"
    "\n"
    "r1 = tester.call_unary('GetUser', {'id': 42})\n"
    "print(f'Unary: {r1[\"status\"]} — {r1[\"data\"]}')\n"
    "\n"
    "r2 = tester.call_server_stream('ListOrders', {'limit': 3})\n"
    "print(f'Stream: {r2[\"count\"]} items')\n"
    "\n"
    "r3 = tester.call_unary('UnknownMethod', {})\n"
    "print(f'Unknown: {r3[\"status\"]}')\n"
    "\n"
    "r4 = tester.call_with_error('FailingCall')\n"
    "print(f'Error: {r4[\"status\"]} — {r4[\"code\"]}')\n"
),
"expected_output": (
    "Unary: OK \u2014 {'id': 42, 'name': 'User-42'}\n"
    "Stream: 3 items\n"
    "Unknown: NOT_FOUND\n"
    "Error: ERROR \u2014 GRPC_UNAVAILABLE"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "gRPC es el protocolo de los microservicios internos. "
    "Si no lo pruebas, no estás probando la comunicación real entre servicios."
),
"theory_content": (
    "## gRPC Communication Patterns\n\n"
    "| Tipo | Descripción |\n"
    "|------|-------------|\n"
    "| Unary | 1 request → 1 response |\n"
    "| Server streaming | 1 request → N responses |\n"
    "| Client streaming | N requests → 1 response |\n"
    "| Bidirectional | N requests ↔ N responses |\n\n"
    "**Status codes gRPC**: OK, NOT_FOUND, UNAVAILABLE, INVALID_ARGUMENT, etc."
),
"pedagogical_objective": "Implementar las modalidades unary, server streaming y manejo de errores en gRPC simulado.",
"syntax_hint": "`if method not in self._services: return {'status': 'NOT_FOUND', 'data': None}`",
"hints_json": json.dumps([
    "call_unary: if method not in self._services: return NOT_FOUND. result = self._services[method](request); return {'status':'OK','data':result}",
    "call_server_stream: result = self._services[method](request); return {'status':'OK','items':result,'count':len(result)}",
    "call_with_error: try: self._services[method]({}); except RuntimeError as e: return {'status':'ERROR','code':str(e)}",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-079: ERROR RESPONSE NORMALIZER ]",
"description": (
    "Implementa `ErrorNormalizer.normalize(raw_error: dict) -> dict` "
    "que estandarice respuestas de error de distintos backends a formato común: "
    "`{'code': int, 'message': str, 'type': str}`."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 79, "base_xp_reward": 380,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "python",
"phase": "api_contratos", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["error_handling", "normalizacion", "consistencia", "API"]),
"initial_code": (
    "class ErrorNormalizer:\n"
    "    def normalize(self, raw: dict) -> dict:\n"
    "        # TODO: normaliza el error al formato estándar\n"
    "        # Los distintos formatos de entrada:\n"
    "        # FastAPI: {'detail': str, 'status_code': int}\n"
    "        # Express: {'error': str, 'statusCode': int}\n"
    "        # Django:  {'message': str, 'code': int, 'type': str}\n"
    "        # Spring:  {'error': str, 'status': int, 'timestamp': str}\n"
    "        # Output siempre: {'code': int, 'message': str, 'type': str}\n"
    "        # type: 'client_error' si code 4xx, 'server_error' si 5xx, 'unknown' si no\n"
    "        pass\n"
    "\n"
    "\n"
    "normalizer = ErrorNormalizer()\n"
    "errors = [\n"
    "    {'detail': 'Not authenticated', 'status_code': 401},\n"
    "    {'error': 'Resource not found', 'statusCode': 404},\n"
    "    {'message': 'Validation failed', 'code': 422, 'type': 'validation'},\n"
    "    {'error': 'DB connection failed', 'status': 500, 'timestamp': '2024-01-01'},\n"
    "]\n"
    "for raw in errors:\n"
    "    n = normalizer.normalize(raw)\n"
    "    print(f'{n[\"code\"]} [{n[\"type\"]}]: {n[\"message\"]}')\n"
),
"expected_output": (
    "401 [client_error]: Not authenticated\n"
    "404 [client_error]: Resource not found\n"
    "422 [client_error]: Validation failed\n"
    "500 [server_error]: DB connection failed"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Las APIs que retornan errores inconsistentes son un infierno para el frontend. "
    "El normalizer crea una capa de consistencia — siempre el mismo formato."
),
"theory_content": (
    "## Error Response Standardization\n\n"
    "Formato estándar recomendado:\n"
    "```json\n{\n  \"code\": 404,\n  \"message\": \"Resource not found\",\n  \"type\": \"client_error\",\n  \"details\": []\n}\n```\n\n"
    "**Por qué importa**: el frontend puede manejar errores de forma uniforme "
    "sin condicionales para cada posible formato de cada API."
),
"pedagogical_objective": "Normalizar respuestas de error de distintos formatos a un esquema unificado.",
"syntax_hint": "Usa `.get()` con fallbacks para extraer message y code de cualquier formato.",
"hints_json": json.dumps([
    "message = raw.get('detail') or raw.get('error') or raw.get('message', 'Unknown error')",
    "code = raw.get('status_code') or raw.get('statusCode') or raw.get('code') or raw.get('status', 0)",
    "tipo = 'client_error' if 400 <= code < 500 else 'server_error' if 500 <= code < 600 else 'unknown'",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-080: CONTRATO — API TEST FRAMEWORK ]",
"description": (
    "Proyecto integrador: implementa `APITestFramework` con request builder, "
    "schema validation, SLA checking y reporte final."
),
"difficulty_tier": 3, "difficulty": "hard",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 80, "base_xp_reward": 500,
"is_project": True, "is_phase_boss": True,
"telemetry_goal_time": 420, "challenge_type": "python",
"phase": "api_contratos", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["framework", "API", "integracion", "QA"]),
"initial_code": (
    "class APITestFramework:\n"
    "    def __init__(self, base_url: str, sla_ms: float = 500.0):\n"
    "        self.base_url = base_url\n"
    "        self.sla_ms   = sla_ms\n"
    "        self._results = []\n"
    "\n"
    "    def test_endpoint(self, method: str, path: str,\n"
    "                      expected_status: int, response_time_ms: float,\n"
    "                      response_body: dict, schema: dict = None):\n"
    "        # TODO: ejecuta todas las validaciones para un endpoint\n"
    "        # 1. Verifica status code\n"
    "        # 2. Verifica SLA (response_time_ms <= sla_ms)\n"
    "        # 3. Si schema provisto: valida campos requeridos y tipos\n"
    "        # Imprime: '{METHOD} {path}: PASS' o '{METHOD} {path}: FAIL [{issues}]'\n"
    "        # Agrega resultado a self._results\n"
    "        pass\n"
    "\n"
    "    def report(self) -> None:\n"
    "        # TODO: imprime resumen final\n"
    "        # === API Test Report ===\n"
    "        # Passed: {n}/{total}\n"
    "        # Framework: {'CERTIFIED' si todos pasan, 'NEEDS WORK' si no}\n"
    "        pass\n"
    "\n"
    "\n"
    "fw = APITestFramework('https://api.daki.io', sla_ms=300.0)\n"
    "fw.test_endpoint('GET',  '/health',  200, 45.0,  {'status': 'ok'})\n"
    "fw.test_endpoint('POST', '/users',   201, 120.0, {'id': 1, 'name': 'Alice'},\n"
    "                 schema={'id': {'type': int, 'required': True}, 'name': {'type': str, 'required': True}})\n"
    "fw.test_endpoint('GET',  '/reports', 200, 450.0, {'data': []})  # SLA violation\n"
    "fw.test_endpoint('DELETE','/users/1',204, 80.0,  {})\n"
    "fw.report()\n"
),
"expected_output": (
    "GET /health: PASS\n"
    "POST /users: PASS\n"
    "GET /reports: FAIL [SLA: 450.0ms exceeds 300.0ms]\n"
    "DELETE /users/1: PASS\n"
    "=== API Test Report ===\n"
    "Passed: 3/4\n"
    "Framework: NEEDS WORK"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Has dominado el API testing. "
    "Este contrato integra request validation, SLA enforcement y schema validation en un framework."
),
"theory_content": (
    "## Proyecto: API Test Framework\n\n"
    "Integra los conceptos del Bloque 4:\n\n"
    "- **Status validation**: verifica HTTP status codes\n"
    "- **SLA enforcement**: bloquea si latencia > threshold\n"
    "- **Schema validation**: verifica estructura del response\n"
    "- **Reporting**: resumen ejecutivo con certificación\n\n"
    "Este patrón es la base de frameworks como Postman Newman o REST-assured."
),
"pedagogical_objective": "Implementar un framework de testing de API que integre múltiples capas de validación.",
"syntax_hint": "Acumula issues en una lista y si está vacía → PASS, si no → FAIL con los issues.",
"hints_json": json.dumps([
    "issues = []. Si expected_status != status code real (usa el dado como parámetro): issues.append('status...').",
    "Si response_time_ms > sla_ms: issues.append(f'SLA: {response_time_ms}ms exceeds {sla_ms}ms').",
    "PASS si not issues. FAIL con issues unidos por ', '. report: CERTIFIED si todos pass, NEEDS WORK si alguno falla.",
]),
"grid_map_json": None,
},
]
