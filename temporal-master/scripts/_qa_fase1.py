"""Fase 1 — Pytest Assault (L01-L08) — Python"""
from __future__ import annotations
import json

FASE1 = [
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ AUTO-001: PRIMEROS TESTS CON PYTEST ]",
"description": (
    "Implementa `sum_numbers(a, b)` que retorna la suma y `is_even(n)` que retorna True si n es par. "
    "Los tests ya están escritos — solo debes hacer que pasen sin modificarlos."
),
"difficulty_tier": 1, "difficulty": "easy",
"sector_id": None, "codex_id": "qa_automation_ops",
"level_order": 1, "base_xp_reward": 120,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 180, "challenge_type": "python",
"phase": "ALPHA", "strict_match": False, "is_free": True,
"concepts_taught_json": json.dumps(["pytest", "assert", "funciones", "TDD"]),
"initial_code": (
    "def sum_numbers(a: int, b: int) -> int:\n"
    "    # TODO: retorna la suma de a y b\n"
    "    pass\n"
    "\n"
    "\n"
    "def is_even(n: int) -> bool:\n"
    "    # TODO: retorna True si n es par, False si es impar\n"
    "    pass\n"
    "\n"
    "\n"
    "# ── Tests (no modificar) ──────────────────────────────────\n"
    "def test_sum_positives():\n"
    "    assert sum_numbers(3, 4) == 7\n"
    "    print('PASSED test_sum_positives')\n"
    "\n"
    "def test_sum_with_zero():\n"
    "    assert sum_numbers(0, 5) == 5\n"
    "    print('PASSED test_sum_with_zero')\n"
    "\n"
    "def test_is_even_true():\n"
    "    assert is_even(4) == True\n"
    "    print('PASSED test_is_even_true')\n"
    "\n"
    "def test_is_even_false():\n"
    "    assert is_even(7) == False\n"
    "    print('PASSED test_is_even_false')\n"
    "\n"
    "\n"
    "test_sum_positives()\n"
    "test_sum_with_zero()\n"
    "test_is_even_true()\n"
    "test_is_even_false()\n"
    "print('4 passed')\n"
),
"expected_output": (
    "PASSED test_sum_positives\n"
    "PASSED test_sum_with_zero\n"
    "PASSED test_is_even_true\n"
    "PASSED test_is_even_false\n"
    "4 passed"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Operador, bienvenido al Protocolo QA. "
    "El primer axioma del testing: si no hay tests, no hay certeza. "
    "Escribe las funciones que hacen que estos tests pasen."
),
"theory_content": (
    "## Tu primer test con pytest\n\n"
    "En pytest, un test es simplemente una función que usa `assert`:\n\n"
    "```python\n"
    "def test_suma():\n"
    "    assert 2 + 2 == 4  # si esto es False, pytest marca el test como FAILED\n"
    "```\n\n"
    "**El ciclo TDD (Test-Driven Development):**\n"
    "1. Escribe el test → falla (RED)\n"
    "2. Implementa la función mínima para que pase (GREEN)\n"
    "3. Refactoriza si es necesario (REFACTOR)\n\n"
    "En este nivel, los tests ya están escritos. Tu tarea: implementar las funciones."
),
"pedagogical_objective": "Entender el ciclo TDD implementando funciones para hacer pasar tests existentes.",
"syntax_hint": "Para is_even usa el operador módulo: `return n % 2 == 0`",
"hints_json": json.dumps([
    "sum_numbers: `return a + b`",
    "is_even: usa el operador módulo. `n % 2 == 0` es True cuando n es par.",
    "Si un assert falla lanza AssertionError. Implementa las funciones correctamente para evitarlo.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ AUTO-002: FIXTURES — SETUP Y TEARDOWN ]",
"description": (
    "Implementa `TestDatabase.insert(key, value)` y `TestDatabase.get(key)` para que "
    "los tests pasen. La función `fixture_db()` ya simula el ciclo setup/teardown usando un generator."
),
"difficulty_tier": 1, "difficulty": "easy",
"sector_id": None, "codex_id": "qa_automation_ops",
"level_order": 2, "base_xp_reward": 130,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 190, "challenge_type": "python",
"phase": "ALPHA", "strict_match": False, "is_free": True,
"concepts_taught_json": json.dumps(["fixtures", "setup_teardown", "generators", "yield"]),
"initial_code": (
    "class TestDatabase:\n"
    "    def __init__(self):\n"
    "        self.connected = False\n"
    "        self.data = {}\n"
    "\n"
    "    def connect(self) -> str:\n"
    "        self.connected = True\n"
    "        return 'DB conectada'\n"
    "\n"
    "    def insert(self, key: str, value: str) -> None:\n"
    "        # TODO: guarda value en self.data bajo la clave key\n"
    "        pass\n"
    "\n"
    "    def get(self, key: str) -> str:\n"
    "        # TODO: retorna self.data[key] si existe, o 'NOT_FOUND' si no\n"
    "        pass\n"
    "\n"
    "    def disconnect(self) -> str:\n"
    "        self.connected = False\n"
    "        return 'DB desconectada'\n"
    "\n"
    "\n"
    "# ── Fixture (generator = setup / yield / teardown) ───────\n"
    "def fixture_db():\n"
    "    db = TestDatabase()\n"
    "    print(db.connect())\n"
    "    yield db\n"
    "    print(db.disconnect())\n"
    "\n"
    "\n"
    "# ── Tests ─────────────────────────────────────────────────\n"
    "def run_tests():\n"
    "    gen = fixture_db()\n"
    "    db = next(gen)\n"
    "\n"
    "    db.insert('user_id', 'USR-001')\n"
    "    assert db.get('user_id') == 'USR-001'\n"
    "    print('PASSED test_insert_and_get')\n"
    "\n"
    "    assert db.get('missing') == 'NOT_FOUND'\n"
    "    print('PASSED test_missing_key')\n"
    "\n"
    "    try:\n"
    "        next(gen)\n"
    "    except StopIteration:\n"
    "        pass\n"
    "\n"
    "\n"
    "run_tests()\n"
),
"expected_output": (
    "DB conectada\n"
    "PASSED test_insert_and_get\n"
    "PASSED test_missing_key\n"
    "DB desconectada"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Un test sin estado controlado es una trampa. "
    "Los fixtures son el contrato entre el test y el estado del sistema: "
    "conectan antes, desconectan después. "
    "En pytest esto se hace con `yield`. Aquí lo simulamos con un generator."
),
"theory_content": (
    "## Fixtures con yield en pytest\n\n"
    "Un fixture en pytest es una función que prepara el contexto antes del test y lo limpia después:\n\n"
    "```python\n"
    "@pytest.fixture\n"
    "def db_connection():\n"
    "    conn = Database.connect()  # SETUP\n"
    "    yield conn                 # el test recibe 'conn'\n"
    "    conn.close()               # TEARDOWN (siempre se ejecuta)\n"
    "```\n\n"
    "El `yield` divide la función en dos partes: antes (setup) y después (teardown).\n"
    "Si el test falla, el teardown igual se ejecuta — garantiza limpieza."
),
"pedagogical_objective": "Implementar el patrón fixture setup/teardown con generators Python.",
"syntax_hint": "insert: `self.data[key] = value` — get: `return self.data.get(key, 'NOT_FOUND')`",
"hints_json": json.dumps([
    "insert: `self.data[key] = value`",
    "get: usa `dict.get()` con default: `return self.data.get(key, 'NOT_FOUND')`",
    "El generator yield hace que fixture_db() ejecute el código después del yield al llamar next() por segunda vez.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ AUTO-003: @PYTEST.MARK.PARAMETRIZE — DATA-DRIVEN ]",
"description": (
    "Implementa `calculate_discount(price, pct)` que retorna `round(price * (1 - pct/100), 2)`. "
    "Los casos de prueba ya están definidos en `test_cases` — la función debe producir exactamente los resultados esperados."
),
"difficulty_tier": 1, "difficulty": "easy",
"sector_id": None, "codex_id": "qa_automation_ops",
"level_order": 3, "base_xp_reward": 140,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 190, "challenge_type": "python",
"phase": "ALPHA", "strict_match": False, "is_free": True,
"concepts_taught_json": json.dumps(["parametrize", "data_driven", "round", "porcentajes"]),
"initial_code": (
    "def calculate_discount(price: float, pct: float) -> float:\n"
    "    # TODO: retorna price * (1 - pct/100), redondeado a 2 decimales\n"
    "    pass\n"
    "\n"
    "\n"
    "# ── Simulación de @pytest.mark.parametrize ────────────────\n"
    "test_cases = [\n"
    "    (100.0, 10.0, 90.0),\n"
    "    (200.0, 25.0, 150.0),\n"
    "    (50.0,   0.0,  50.0),\n"
    "    (80.0, 100.0,   0.0),\n"
    "]\n"
    "\n"
    "passed = 0\n"
    "for price, pct, expected in test_cases:\n"
    "    result = calculate_discount(price, pct)\n"
    "    if result == expected:\n"
    "        print(f'PASSED [{price}, {pct}%] \u2192 {result}')\n"
    "        passed += 1\n"
    "    else:\n"
    "        print(f'FAILED [{price}, {pct}%] expected={expected} got={result}')\n"
    "\n"
    "print(f'{passed}/{len(test_cases)} passed')\n"
),
"expected_output": (
    "PASSED [100.0, 10.0%] \u2192 90.0\n"
    "PASSED [200.0, 25.0%] \u2192 150.0\n"
    "PASSED [50.0, 0.0%] \u2192 50.0\n"
    "PASSED [80.0, 100.0%] \u2192 0.0\n"
    "4/4 passed"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Un test parametrizado reemplaza diez tests casi idénticos. "
    "`@pytest.mark.parametrize` es la herramienta para probar el mismo comportamiento "
    "con distintos datos. Aquí lo simulamos con una lista de casos."
),
"theory_content": (
    "## @pytest.mark.parametrize\n\n"
    "En pytest real:\n\n"
    "```python\n"
    "@pytest.mark.parametrize('price,pct,expected', [\n"
    "    (100.0, 10.0, 90.0),\n"
    "    (200.0, 25.0, 150.0),\n"
    "])\n"
    "def test_discount(price, pct, expected):\n"
    "    assert calculate_discount(price, pct) == expected\n"
    "```\n\n"
    "pytest genera un test separado por cada fila. Si uno falla, los demás siguen corriendo.\n\n"
    "**`round(x, 2)`** — redondea a 2 decimales para evitar errores de punto flotante:\n"
    "`0.1 + 0.2 == 0.30000000000000004` sin redondeo."
),
"pedagogical_objective": "Aplicar testing data-driven con parametrize — elimina duplicación de tests.",
"syntax_hint": "`return round(price * (1 - pct / 100), 2)`",
"hints_json": json.dumps([
    "La fórmula: `price * (1 - pct / 100)`. Para 100 con 10%: 100 * (1 - 0.1) = 90.0",
    "Usa `round(resultado, 2)` para evitar errores de punto flotante.",
    "Para pct=100.0: `price * (1 - 1.0) = price * 0.0 = 0.0` ✓",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ AUTO-004: MOCK HTTP CLIENT — REQUESTS TESTING ]",
"description": (
    "Implementa `MockHttpClient.get(path)` y `MockHttpClient.post(path, data)`. "
    "Cada método busca la respuesta registrada en `self._responses` con la clave `'METHOD /path'` "
    "y la retorna. Si no existe, retorna `{'status': 404, 'body': {}}`."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": None, "codex_id": "qa_automation_ops",
"level_order": 4, "base_xp_reward": 160,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 210, "challenge_type": "python",
"phase": "ALPHA", "strict_match": False, "is_free": True,
"concepts_taught_json": json.dumps(["requests", "HTTP_testing", "mocking", "diccionarios"]),
"initial_code": (
    "class MockHttpClient:\n"
    "    def __init__(self, base_url: str):\n"
    "        self.base_url = base_url\n"
    "        self._responses = {}\n"
    "\n"
    "    def register(self, method: str, path: str, status: int, body: dict) -> None:\n"
    "        self._responses[f'{method} {path}'] = {'status': status, 'body': body}\n"
    "\n"
    "    def get(self, path: str) -> dict:\n"
    "        # TODO: busca 'GET {path}' en self._responses\n"
    "        # retorna {'status': 404, 'body': {}} si no existe\n"
    "        pass\n"
    "\n"
    "    def post(self, path: str, data: dict) -> dict:\n"
    "        # TODO: busca 'POST {path}' en self._responses\n"
    "        # retorna {'status': 404, 'body': {}} si no existe\n"
    "        pass\n"
    "\n"
    "\n"
    "client = MockHttpClient('https://api.daki.io')\n"
    "client.register('GET',  '/health',      200, {'status': 'ok'})\n"
    "client.register('POST', '/auth/login',  200, {'token': 'jwt-xyz'})\n"
    "client.register('GET',  '/protected',   403, {'error': 'forbidden'})\n"
    "\n"
    "resp = client.get('/health')\n"
    "assert resp['status'] == 200\n"
    "print(f\"GET /health \u2192 {resp['status']} {resp['body']['status']}\")\n"
    "\n"
    "resp = client.post('/auth/login', {'user': 'admin'})\n"
    "assert resp['status'] == 200\n"
    "print(f\"POST /auth/login \u2192 {resp['status']} token={resp['body']['token']}\")\n"
    "\n"
    "resp = client.get('/protected')\n"
    "assert resp['status'] == 403\n"
    "print(f\"GET /protected \u2192 {resp['status']} {resp['body']['error']}\")\n"
),
"expected_output": (
    "GET /health \u2192 200 ok\n"
    "POST /auth/login \u2192 200 token=jwt-xyz\n"
    "GET /protected \u2192 403 forbidden"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "En QA Automation no podemos depender de APIs externas en los tests — "
    "son lentas, costosas y pueden estar caídas. "
    "Mockeamos el cliente HTTP para controlar exactamente qué responde el servidor."
),
"theory_content": (
    "## Mocking de HTTP en tests\n\n"
    "La biblioteca `requests` hace llamadas HTTP reales. En tests, la reemplazamos:\n\n"
    "```python\n"
    "# En producción:\n"
    "import requests\n"
    "resp = requests.get('https://api.daki.io/health')\n\n"
    "# En tests (mock):\n"
    "client = MockHttpClient('https://api.daki.io')\n"
    "client.register('GET', '/health', 200, {'status': 'ok'})\n"
    "resp = client.get('/health')  # sin red, determinístico\n"
    "```\n\n"
    "**`dict.get(key, default)`** — retorna el valor o el default si la clave no existe."
),
"pedagogical_objective": "Entender el patrón mock HTTP — base de todo testing de integración sin red.",
"syntax_hint": "`return self._responses.get(f'GET {path}', {'status': 404, 'body': {}})`",
"hints_json": json.dumps([
    "Usa `self._responses.get(key, default)` para buscar sin lanzar KeyError.",
    "La clave es `f'GET {path}'` o `f'POST {path}'` según el método.",
    "El default cuando no existe: `{'status': 404, 'body': {}}`",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ AUTO-005: JSON SCHEMA — VALIDAR RESPUESTAS API ]",
"description": (
    "Implementa `validate_schema(data, schema)` que verifica que `data` tenga todos los campos "
    "del `schema` con los tipos correctos. Retorna lista de errores: "
    "`'MISSING: <field>'` si no existe, `'TYPE_ERROR: <field> expected <type>'` si el tipo no coincide. "
    "Mapeo de tipos: `'str'→str`, `'int'→int`, `'bool'→bool`, `'list'→list`."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": None, "codex_id": "qa_automation_ops",
"level_order": 5, "base_xp_reward": 170,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 220, "challenge_type": "python",
"phase": "ALPHA", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["json_schema", "validación", "isinstance", "API_testing"]),
"initial_code": (
    "def validate_schema(data: dict, schema: dict) -> list:\n"
    "    \"\"\"\n"
    "    Valida que data tenga los campos requeridos con los tipos correctos.\n"
    "    schema = {'field': 'type_str'}  — type_str: 'str'|'int'|'bool'|'list'\n"
    "    Retorna lista de strings de error (vacía si todo está bien).\n"
    "    \"\"\"\n"
    "    errors = []\n"
    "    type_map = {'str': str, 'int': int, 'bool': bool, 'list': list}\n"
    "    # TODO: por cada (field, type_str) en schema.items():\n"
    "    #   Si field no está en data: agrega 'MISSING: <field>'\n"
    "    #   Si está pero el tipo no coincide: agrega 'TYPE_ERROR: <field> expected <type_str>'\n"
    "    return errors\n"
    "\n"
    "\n"
    "schema = {'id': 'int', 'name': 'str', 'active': 'bool', 'tags': 'list'}\n"
    "\n"
    "responses = [\n"
    "    {'id': 1, 'name': 'daki_op', 'active': True, 'tags': ['qa', 'python']},\n"
    "    {'id': 'X', 'name': 'agent', 'active': True},\n"
    "    {'id': 2, 'active': False, 'tags': []},\n"
    "]\n"
    "\n"
    "for i, resp in enumerate(responses, 1):\n"
    "    errs = validate_schema(resp, schema)\n"
    "    if errs:\n"
    "        print(f'Response {i}: INVALID \u2014 {\", \".join(errs)}')\n"
    "    else:\n"
    "        print(f'Response {i}: VALID')\n"
),
"expected_output": (
    "Response 1: VALID\n"
    "Response 2: INVALID \u2014 TYPE_ERROR: id expected int, MISSING: tags\n"
    "Response 3: INVALID \u2014 MISSING: name"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "La API del Nexo retorna JSON sin documentación actualizada. "
    "Los campos cambian entre versiones y los tipos no son confiables. "
    "Un validador de schema detecta contratos rotos antes de que lleguen a producción."
),
"theory_content": (
    "## Validación de JSON Schema\n\n"
    "En QA real se usa `jsonschema.validate()`. Aquí construimos uno básico:\n\n"
    "```python\n"
    "def validate_schema(data, schema):\n"
    "    errors = []\n"
    "    type_map = {'str': str, 'int': int, 'bool': bool, 'list': list}\n"
    "    for field, type_str in schema.items():\n"
    "        if field not in data:\n"
    "            errors.append(f'MISSING: {field}')\n"
    "        elif not isinstance(data[field], type_map[type_str]):\n"
    "            errors.append(f'TYPE_ERROR: {field} expected {type_str}')\n"
    "    return errors\n"
    "```\n\n"
    "**`isinstance(valor, tipo)`** — verifica el tipo sin comparar strings."
),
"pedagogical_objective": "Construir un validador de schema JSON — skill crítico en API testing.",
"syntax_hint": "Itera `for field, type_str in schema.items()` y usa `isinstance(data[field], type_map[type_str])`",
"hints_json": json.dumps([
    "Itera `for field, type_str in schema.items():`",
    "Verifica existencia: `if field not in data: errors.append(f'MISSING: {field}')`",
    "Verifica tipo: `elif not isinstance(data[field], type_map[type_str]): errors.append(f'TYPE_ERROR: {field} expected {type_str}')`",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ AUTO-006: UNITTEST.MOCK — PARCHEAR DEPENDENCIAS ]",
"description": (
    "Implementa `UserNotifier.notify_registration(user_email)` que llama a "
    "`self.email_service.send(user_email, 'Bienvenido al Nexo')`. "
    "Si retorna `True`: retorna `'Notification sent to <email>'`. "
    "Si retorna `False`: retorna `'Notification failed for <email>'`."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": None, "codex_id": "qa_automation_ops",
"level_order": 6, "base_xp_reward": 180,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 230, "challenge_type": "python",
"phase": "ALPHA", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["unittest.mock", "MagicMock", "dependency_injection", "side_effects"]),
"initial_code": (
    "from unittest.mock import MagicMock\n"
    "\n"
    "\n"
    "class EmailService:\n"
    "    def send(self, to: str, subject: str) -> bool:\n"
    "        raise ConnectionError('No SMTP en este entorno')\n"
    "\n"
    "\n"
    "class UserNotifier:\n"
    "    def __init__(self, email_service: EmailService):\n"
    "        self.email_service = email_service\n"
    "\n"
    "    def notify_registration(self, user_email: str) -> str:\n"
    "        # TODO: llama self.email_service.send(user_email, 'Bienvenido al Nexo')\n"
    "        # Si True: retorna 'Notification sent to <user_email>'\n"
    "        # Si False: retorna 'Notification failed for <user_email>'\n"
    "        pass\n"
    "\n"
    "\n"
    "# ── Tests con mock ────────────────────────────────────────\n"
    "mock_service = MagicMock(spec=EmailService)\n"
    "\n"
    "mock_service.send.return_value = True\n"
    "notifier = UserNotifier(mock_service)\n"
    "result = notifier.notify_registration('op@daki.io')\n"
    "print(result)\n"
    "mock_service.send.assert_called_once_with('op@daki.io', 'Bienvenido al Nexo')\n"
    "print('PASSED mock_send_called_correctly')\n"
    "\n"
    "mock_service.send.return_value = False\n"
    "result = notifier.notify_registration('unknown@daki.io')\n"
    "print(result)\n"
    "print('PASSED mock_send_failure_handled')\n"
),
"expected_output": (
    "Notification sent to op@daki.io\n"
    "PASSED mock_send_called_correctly\n"
    "Notification failed for unknown@daki.io\n"
    "PASSED mock_send_failure_handled"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "El servicio de email de producción requiere SMTP. En los tests no hay SMTP. "
    "`MagicMock` reemplaza el servicio con un objeto que podemos programar: "
    "decide qué retorna, y luego verifica que fue llamado correctamente."
),
"theory_content": (
    "## MagicMock — Controla lo que no controlas\n\n"
    "```python\n"
    "from unittest.mock import MagicMock\n\n"
    "mock = MagicMock()\n"
    "mock.send.return_value = True     # programas la respuesta\n"
    "resultado = mock.send('a@b.com', 'Hola')  # llamada registrada\n"
    "mock.send.assert_called_once_with('a@b.com', 'Hola')  # verificación\n"
    "```\n\n"
    "**`spec=EmailService`** — el mock solo acepta métodos que existen en EmailService. "
    "Si llamas un método inexistente, falla inmediatamente — evita errores silenciosos."
),
"pedagogical_objective": "Usar MagicMock para testear clases con dependencias externas no disponibles.",
"syntax_hint": "`sent = self.email_service.send(user_email, 'Bienvenido al Nexo')` luego `if sent:`",
"hints_json": json.dumps([
    "Llama: `sent = self.email_service.send(user_email, 'Bienvenido al Nexo')`",
    "El resultado de send() es el mock.send.return_value que configuramos externamente.",
    "`if sent: return f'Notification sent to {user_email}'` — else: retorna el mensaje de fallo.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ AUTO-007: COVERAGE TRACKER — ARQUITECTURA DE SUITE ]",
"description": (
    "Implementa `CoverageTracker.mark_covered(func_name)` y `CoverageTracker.report()`. "
    "`report()` imprime `'Coverage Report:'`, luego cada función en `self._total` ordenada alfabéticamente "
    "con `'  ✓ <name>'` o `'  ✗ <name>'`, y al final `'Coverage: N/M (XX%)'` donde XX es entero."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": None, "codex_id": "qa_automation_ops",
"level_order": 7, "base_xp_reward": 185,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "python",
"phase": "ALPHA", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["coverage", "sets", "sorted", "reporting"]),
"initial_code": (
    "class CoverageTracker:\n"
    "    def __init__(self):\n"
    "        self._covered = set()\n"
    "        self._total = set()\n"
    "\n"
    "    def register(self, func_name: str) -> None:\n"
    "        self._total.add(func_name)\n"
    "\n"
    "    def mark_covered(self, func_name: str) -> None:\n"
    "        # TODO: agrega func_name a self._covered\n"
    "        pass\n"
    "\n"
    "    def report(self) -> None:\n"
    "        # TODO: imprime 'Coverage Report:'\n"
    "        # TODO: por cada func en sorted(self._total):\n"
    "        #   '  ✓ <func>' si está cubierta, '  ✗ <func>' si no\n"
    "        # TODO: imprime 'Coverage: <covered>/<total> (<pct>%)'\n"
    "        #   pct = int(covered/total * 100)\n"
    "        pass\n"
    "\n"
    "\n"
    "tracker = CoverageTracker()\n"
    "\n"
    "for fn in ['calculate_tax', 'format_currency', 'parse_date', 'send_notification', 'validate_email']:\n"
    "    tracker.register(fn)\n"
    "\n"
    "tracker.mark_covered('calculate_tax')\n"
    "tracker.mark_covered('format_currency')\n"
    "tracker.mark_covered('validate_email')\n"
    "\n"
    "tracker.report()\n"
),
"expected_output": (
    "Coverage Report:\n"
    "  \u2713 calculate_tax\n"
    "  \u2713 format_currency\n"
    "  \u2717 parse_date\n"
    "  \u2717 send_notification\n"
    "  \u2713 validate_email\n"
    "Coverage: 3/5 (60%)"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "El equipo dice que el sistema tiene '80% de cobertura'. "
    "Pero nadie sabe qué funciones están cubiertas y cuáles no. "
    "Un tracker de cobertura responde esa pregunta con precisión."
),
"theory_content": (
    "## Code Coverage — Qué significa realmente\n\n"
    "Coverage mide qué líneas/funciones de código fueron ejecutadas durante los tests:\n\n"
    "```python\n"
    "# 100% coverage: todos los caminos ejecutados\n"
    "# 60% coverage: 2 de cada 5 funciones sin tests\n"
    "```\n\n"
    "**Por qué 100% no es suficiente:**\n"
    "Puedes tener 100% coverage y aún tener bugs si los asserts son incorrectos.\n"
    "Coverage es condición necesaria, no suficiente.\n\n"
    "```python\n"
    "pct = int(len(covered) / len(total) * 100)\n"
    "# sorted(set) ordena alfabéticamente\n"
    "```"
),
"pedagogical_objective": "Construir un tracker de cobertura — comprende qué mide coverage y sus limitaciones.",
"syntax_hint": "Para el porcentaje: `pct = int(len(self._covered) / len(self._total) * 100)`",
"hints_json": json.dumps([
    "mark_covered: `self._covered.add(func_name)`",
    "En report, itera `for fn in sorted(self._total):` y usa `'✓' if fn in self._covered else '✗'`",
    "Para el porcentaje: `pct = int(len(self._covered) / len(self._total) * 100)` — muestra como entero.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ AUTO-008 \u221e BOSS: PRICING ENGINE — MOCK + PARAMETRIZE ]",
"description": (
    "Implementa `PricingEngine.calculate_final_price(base_price, discount_pct)`: "
    "1) aplica descuento: `discounted = base_price * (1 - discount_pct / 100)`, "
    "2) obtiene la tasa llamando `self.tax_service.get_rate()`, "
    "3) aplica impuesto: `final = discounted * (1 + rate)`, "
    "4) retorna `round(final, 2)`. "
    "No modifiques el bloque de tests."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": None, "codex_id": "qa_automation_ops",
"level_order": 8, "base_xp_reward": 260,
"is_project": False, "is_phase_boss": True,
"telemetry_goal_time": 280, "challenge_type": "python",
"phase": "ALPHA", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["MagicMock", "parametrize", "OOP", "impuesto", "descuento"]),
"initial_code": (
    "from unittest.mock import MagicMock\n"
    "\n"
    "\n"
    "class PricingEngine:\n"
    "    def __init__(self, tax_service):\n"
    "        self.tax_service = tax_service\n"
    "\n"
    "    def calculate_final_price(self, base_price: float, discount_pct: float) -> float:\n"
    "        # TODO:\n"
    "        # 1. discounted = base_price * (1 - discount_pct / 100)\n"
    "        # 2. rate = self.tax_service.get_rate()\n"
    "        # 3. final = discounted * (1 + rate)\n"
    "        # 4. retorna round(final, 2)\n"
    "        pass\n"
    "\n"
    "\n"
    "# ── Fixture ───────────────────────────────────────────────\n"
    "def make_engine(tax_rate: float) -> PricingEngine:\n"
    "    mock_tax = MagicMock()\n"
    "    mock_tax.get_rate.return_value = tax_rate\n"
    "    return PricingEngine(mock_tax)\n"
    "\n"
    "\n"
    "# ── Casos parametrizados (base, disc%, tax_rate, expected) ─\n"
    "cases = [\n"
    "    (100.0,  0.0, 0.21, 121.0),\n"
    "    (200.0, 10.0, 0.21, 217.8),\n"
    "    ( 50.0, 50.0, 0.00,  25.0),\n"
    "    (300.0, 20.0, 0.10, 264.0),\n"
    "]\n"
    "\n"
    "passed = 0\n"
    "for base, disc, rate, expected in cases:\n"
    "    engine = make_engine(rate)\n"
    "    result = engine.calculate_final_price(base, disc)\n"
    "    status = 'PASSED' if result == expected else 'FAILED'\n"
    "    if status == 'PASSED':\n"
    "        passed += 1\n"
    "    print(f'{status} price={base} disc={disc}% tax={int(rate*100)}% \u2192 {result}')\n"
    "\n"
    "print(f'\\nSuite: {passed}/{len(cases)} passed')\n"
    "print('STATUS: SUCCESS' if passed == len(cases) else 'STATUS: FAILED')\n"
),
"expected_output": (
    "PASSED price=100.0 disc=0.0% tax=21% \u2192 121.0\n"
    "PASSED price=200.0 disc=10.0% tax=21% \u2192 217.8\n"
    "PASSED price=50.0 disc=50.0% tax=0% \u2192 25.0\n"
    "PASSED price=300.0 disc=20.0% tax=10% \u2192 264.0\n"
    "\n"
    "Suite: 4/4 passed\n"
    "STATUS: SUCCESS"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "\u221e BOSS ALPHA \u2014 El módulo de facturación del Nexo tiene un bug en producción. "
    "El tax_service es un sistema externo que no podemos tocar. "
    "Necesitas un PricingEngine testeado con mock: 4 casos, 0 fallos. Tiempo límite: ahora."
),
"theory_content": (
    "## Combinando Mock + Parametrize\n\n"
    "Esta es la combinación más poderosa en pytest:\n\n"
    "```python\n"
    "@pytest.mark.parametrize('base,disc,rate,expected', casos)\n"
    "def test_pricing(base, disc, rate, expected):\n"
    "    mock_tax = MagicMock()\n"
    "    mock_tax.get_rate.return_value = rate\n"
    "    engine = PricingEngine(mock_tax)\n"
    "    assert engine.calculate_final_price(base, disc) == expected\n"
    "```\n\n"
    "El mock reemplaza el tax_service real. Parametrize genera 4 tests desde una sola función.\n\n"
    "**Verificación manual del caso 2:**\n"
    "`200 * (1 - 10/100) = 200 * 0.9 = 180`\n"
    "`180 * (1 + 0.21) = 180 * 1.21 = 217.8` ✓"
),
"pedagogical_objective": "Integrar mock + parametrize en un test suite real — patrón core del testing profesional.",
"syntax_hint": "El `\\n` al inicio del print genera la línea en blanco: `print(f'\\nSuite: {passed}/{len(cases)} passed')`",
"hints_json": json.dumps([
    "Paso 1: `discounted = base_price * (1 - discount_pct / 100)`",
    "Paso 2: `rate = self.tax_service.get_rate()` — el mock retorna el valor que configuramos.",
    "Paso 3+4: `return round(discounted * (1 + rate), 2)` — round para evitar errores de punto flotante.",
]),
"grid_map_json": None,
},
]
