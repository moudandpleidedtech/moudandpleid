"""Bloque 2 — Automatización E2E (L21–L40) — Python (patrones simulados)"""
from __future__ import annotations
import json

BLOQUE2 = [
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-021: SELECTOR STRATEGY ]",
"description": (
    "Implementa `best_selector(element: dict) -> str` que elija el selector más estable: "
    "data-testid > id > aria-label > css_class. Retorna el selector como string."
),
"difficulty_tier": 1, "difficulty": "easy",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 21, "base_xp_reward": 160,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 200, "challenge_type": "python",
"phase": "automatizacion_e2e", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["selectores", "CSS", "locators", "estabilidad"]),
"initial_code": (
    "def best_selector(element: dict) -> str:\n"
    "    # TODO: retorna el selector más estable disponible\n"
    "    # Prioridad: data-testid > id > aria-label > css_class\n"
    "    # Formato de retorno:\n"
    "    #   data-testid → '[data-testid=\"{valor}\"]'\n"
    "    #   id          → '#{ valor}'\n"
    "    #   aria-label  → '[aria-label=\"{valor}\"]'\n"
    "    #   css_class   → '.{valor}'\n"
    "    pass\n"
    "\n"
    "\n"
    "elements = [\n"
    "    {'data-testid': 'submit-btn', 'id': 'btn1', 'css_class': 'btn-primary'},\n"
    "    {'id': 'username-field', 'css_class': 'form-input'},\n"
    "    {'aria-label': 'Close dialog', 'css_class': 'icon-close'},\n"
    "    {'css_class': 'nav-item'},\n"
    "]\n"
    "for el in elements:\n"
    "    print(best_selector(el))\n"
),
"expected_output": (
    '[data-testid="submit-btn"]\n'
    "#username-field\n"
    '[aria-label="Close dialog"]\n'
    ".nav-item"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "El selector correcto es la diferencia entre un test estable "
    "y un test que falla en cada deploy por nada."
),
"theory_content": (
    "## Jerarquía de Selectores\n\n"
    "| Prioridad | Selector        | Estabilidad |\n"
    "|-----------|-----------------|-------------|\n"
    "| 1 (mejor) | data-testid     | Alta — diseñado para tests |\n"
    "| 2         | id              | Media — puede ser auto-generado |\n"
    "| 3         | aria-label      | Media — accesibilidad |\n"
    "| 4 (peor)  | css_class       | Baja — cambia con refactoring |\n\n"
    "**Regla de oro**: si el elemento no tiene `data-testid`, pídele al dev que lo agregue."
),
"pedagogical_objective": "Seleccionar el locator más estable usando una jerarquía de prioridades.",
"syntax_hint": "Usa `.get()` para verificar cada atributo en orden de prioridad.",
"hints_json": json.dumps([
    "if element.get('data-testid'): return f'[data-testid=\"{element[\"data-testid\"]}\"]'",
    "elif element.get('id'): return f'#{element[\"id\"]}'",
    "elif element.get('aria-label'): return f'[aria-label=\"{element[\"aria-label\"]}\"]'",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-022: PAGE OBJECT MODEL ]",
"description": (
    "Implementa la clase `LoginPage` con atributos de locators y métodos: "
    "`fill_username(val)`, `fill_password(val)`, `click_submit()`, `get_error() -> str`."
),
"difficulty_tier": 1, "difficulty": "easy",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 22, "base_xp_reward": 170,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 200, "challenge_type": "python",
"phase": "automatizacion_e2e", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["POM", "page_object", "abstraccion"]),
"initial_code": (
    "class SimBrowser:\n"
    "    \"\"\"Simulador de browser para el ejercicio.\"\"\"\n"
    "    def __init__(self):\n"
    "        self._inputs = {}\n"
    "        self._submitted = False\n"
    "        self._valid_users = {'admin': 'secret123'}\n"
    "\n"
    "    def fill(self, selector: str, value: str):\n"
    "        self._inputs[selector] = value\n"
    "\n"
    "    def click(self, selector: str):\n"
    "        if selector == '[data-testid=\"submit-btn\"]':\n"
    "            self._submitted = True\n"
    "\n"
    "    def get_text(self, selector: str) -> str:\n"
    "        if selector == '[data-testid=\"error-msg\"]' and self._submitted:\n"
    "            user = self._inputs.get('[data-testid=\"username\"]', '')\n"
    "            pwd  = self._inputs.get('[data-testid=\"password\"]', '')\n"
    "            if self._valid_users.get(user) == pwd:\n"
    "                return ''\n"
    "            return 'Invalid credentials'\n"
    "        return ''\n"
    "\n"
    "\n"
    "class LoginPage:\n"
    "    # Locators\n"
    "    USERNAME = '[data-testid=\"username\"]'\n"
    "    PASSWORD = '[data-testid=\"password\"]'\n"
    "    SUBMIT   = '[data-testid=\"submit-btn\"]'\n"
    "    ERROR    = '[data-testid=\"error-msg\"]'\n"
    "\n"
    "    def __init__(self, browser: SimBrowser):\n"
    "        self.browser = browser\n"
    "\n"
    "    def fill_username(self, value: str):\n"
    "        # TODO: usa self.browser.fill con el locator USERNAME\n"
    "        pass\n"
    "\n"
    "    def fill_password(self, value: str):\n"
    "        # TODO: usa self.browser.fill con el locator PASSWORD\n"
    "        pass\n"
    "\n"
    "    def click_submit(self):\n"
    "        # TODO: usa self.browser.click con el locator SUBMIT\n"
    "        pass\n"
    "\n"
    "    def get_error(self) -> str:\n"
    "        # TODO: usa self.browser.get_text con el locator ERROR\n"
    "        pass\n"
    "\n"
    "\n"
    "browser = SimBrowser()\n"
    "page = LoginPage(browser)\n"
    "\n"
    "# Test 1: credenciales incorrectas\n"
    "page.fill_username('hacker')\n"
    "page.fill_password('wrong')\n"
    "page.click_submit()\n"
    "print(f'Error msg: {page.get_error()}')\n"
    "\n"
    "# Test 2: credenciales correctas\n"
    "browser2 = SimBrowser()\n"
    "page2 = LoginPage(browser2)\n"
    "page2.fill_username('admin')\n"
    "page2.fill_password('secret123')\n"
    "page2.click_submit()\n"
    "error = page2.get_error()\n"
    "print(f'Login OK: {error == \"\"}')\n"
),
"expected_output": (
    "Error msg: Invalid credentials\n"
    "Login OK: True"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Sin POM, tus tests son espagueti de selectores repetidos. "
    "Con POM, son arquitectura — un cambio de locator afecta un solo lugar."
),
"theory_content": (
    "## Page Object Model (POM)\n\n"
    "Patrón de diseño que encapsula:\n"
    "1. **Locators**: como constantes de clase\n"
    "2. **Acciones**: como métodos (fill, click, submit)\n"
    "3. **Assertions**: como métodos que retornan estado\n\n"
    "```python\nclass LoginPage:\n    USERNAME = '[data-testid=\"username\"]'\n    \n    def fill_username(self, val):\n        self.browser.fill(self.USERNAME, val)\n```\n\n"
    "**Beneficio**: si el selector de username cambia, solo lo cambias en `LoginPage.USERNAME`."
),
"pedagogical_objective": "Implementar el patrón POM encapsulando locators y acciones en una clase de página.",
"syntax_hint": "Cada método usa `self.browser.{action}(self.LOCATOR, ...)` — un método por acción.",
"hints_json": json.dumps([
    "fill_username: `self.browser.fill(self.USERNAME, value)`",
    "fill_password: `self.browser.fill(self.PASSWORD, value)`",
    "click_submit: `self.browser.click(self.SUBMIT)`. get_error: `return self.browser.get_text(self.ERROR)`",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-023: WAIT STRATEGY ENGINE ]",
"description": (
    "Implementa `WaitStrategy` con 3 métodos: `implicit_wait(timeout)`, "
    "`explicit_wait(condition_fn, timeout, poll)` que reintenta hasta que `condition_fn()` sea True, "
    "`fluent_wait(condition_fn, timeout, poll, ignored_exceptions)` que ignora excepciones al sondear."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 23, "base_xp_reward": 180,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "python",
"phase": "automatizacion_e2e", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["waits", "explicit_wait", "fluent_wait", "polling"]),
"initial_code": (
    "class WaitStrategy:\n"
    "    def implicit_wait(self, timeout: int) -> str:\n"
    "        # TODO: retorna 'implicit({timeout}s) configured'\n"
    "        pass\n"
    "\n"
    "    def explicit_wait(self, condition_fn, timeout: int, poll: float) -> str:\n"
    "        # TODO: llama condition_fn() repetidamente cada `poll` segundos\n"
    "        # Simula: llama condition_fn() hasta que retorne True o se agoten los intentos\n"
    "        # max_attempts = int(timeout / poll)\n"
    "        # Si condition_fn() retorna True en algún intento: retorna 'condition met'\n"
    "        # Si se agotan los intentos: retorna 'timeout after {timeout}s'\n"
    "        pass\n"
    "\n"
    "    def fluent_wait(self, condition_fn, timeout: int, poll: float,\n"
    "                    ignored_exceptions: tuple) -> str:\n"
    "        # TODO: igual que explicit_wait pero captura ignored_exceptions sin fallar\n"
    "        # Si condition_fn() lanza una excepción en ignored_exceptions → continúa\n"
    "        # Si retorna True → retorna 'condition met (fluent)'\n"
    "        # Si timeout → retorna 'timeout after {timeout}s'\n"
    "        pass\n"
    "\n"
    "\n"
    "ws = WaitStrategy()\n"
    "\n"
    "# Test implicit\n"
    "print(ws.implicit_wait(30))\n"
    "\n"
    "# Test explicit: condición que se cumple al 3er intento\n"
    "counter = [0]\n"
    "def becomes_visible():\n"
    "    counter[0] += 1\n"
    "    return counter[0] >= 3\n"
    "print(ws.explicit_wait(becomes_visible, timeout=10, poll=0.1))\n"
    "\n"
    "# Test explicit: timeout\n"
    "print(ws.explicit_wait(lambda: False, timeout=5, poll=1))\n"
    "\n"
    "# Test fluent: condition lanza excepción hasta el 2do intento\n"
    "attempt = [0]\n"
    "def stale_then_ok():\n"
    "    attempt[0] += 1\n"
    "    if attempt[0] < 2:\n"
    "        raise ValueError('stale element')\n"
    "    return True\n"
    "print(ws.fluent_wait(stale_then_ok, timeout=10, poll=0.1,\n"
    "                     ignored_exceptions=(ValueError,)))\n"
),
"expected_output": (
    "implicit(30s) configured\n"
    "condition met\n"
    "timeout after 5s\n"
    "condition met (fluent)"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "El 90% de los tests flaky se arreglan con la estrategia de wait correcta. "
    "Saber cuándo usar implicit vs explicit vs fluent es conocimiento de Architect."
),
"theory_content": (
    "## Estrategias de Wait\n\n"
    "| Tipo     | Uso | Riesgo |\n"
    "|----------|-----|--------|\n"
    "| Implicit | Global, aplica a todos los finds | Oculta lentitud real |\n"
    "| Explicit | Condición específica, local | Ninguno — recomendado |\n"
    "| Fluent   | Como explicit + ignora excepciones transitorias | Para elementos volátiles |\n\n"
    "**Nunca uses `time.sleep()`** — es un hard wait que no se adapta al DOM."
),
"pedagogical_objective": "Implementar las 3 estrategias de wait de Playwright/Selenium con polling y timeout.",
"syntax_hint": "Para explicit_wait: `for _ in range(int(timeout/poll)): if condition_fn(): return 'condition met'`",
"hints_json": json.dumps([
    "implicit_wait: return f'implicit({timeout}s) configured'",
    "explicit_wait: max_attempts=int(timeout/poll), loop, llama condition_fn(), retorna 'condition met' o timeout.",
    "fluent_wait: igual pero envuelve condition_fn() en try/except ignored_exceptions — si lanza, continúa.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-024: TEST DATA FACTORY ]",
"description": (
    "Implementa `UserFactory` con método `create(role='USER', active=True) -> dict` "
    "que genere usuarios con id autoincremental, email único y campos válidos."
),
"difficulty_tier": 1, "difficulty": "easy",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 24, "base_xp_reward": 180,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 200, "challenge_type": "python",
"phase": "automatizacion_e2e", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["test_data_factory", "fixtures", "generacion"]),
"initial_code": (
    "class UserFactory:\n"
    "    def __init__(self):\n"
    "        self._counter = 0\n"
    "\n"
    "    def create(self, role: str = 'USER', active: bool = True) -> dict:\n"
    "        # TODO: incrementa self._counter y retorna dict con:\n"
    "        # 'id':     self._counter\n"
    "        # 'email':  f'user{self._counter}@test.io'\n"
    "        # 'role':   role\n"
    "        # 'active': active\n"
    "        pass\n"
    "\n"
    "\n"
    "factory = UserFactory()\n"
    "u1 = factory.create()\n"
    "u2 = factory.create(role='ADMIN')\n"
    "u3 = factory.create(active=False)\n"
    "\n"
    "for u in [u1, u2, u3]:\n"
    "    print(f'id={u[\"id\"]} email={u[\"email\"]} role={u[\"role\"]} active={u[\"active\"]}')\n"
),
"expected_output": (
    "id=1 email=user1@test.io role=USER active=True\n"
    "id=2 email=user2@test.io role=ADMIN active=True\n"
    "id=3 email=user3@test.io role=USER active=False"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Los tests que dependen de datos hardcodeados son frágiles. "
    "Las factories generan datos frescos y únicos en cada ejecución."
),
"theory_content": (
    "## Test Data Factory\n\n"
    "Una factory genera datos de prueba **válidos y únicos** bajo demanda:\n\n"
    "```python\nfactory = UserFactory()\nu1 = factory.create()            # {id: 1, email: 'user1@test.io', ...}\nu2 = factory.create(role='ADMIN')# {id: 2, email: 'user2@test.io', role: 'ADMIN'}\n```\n\n"
    "**Ventajas:**\n"
    "- No hay colisiones de datos entre tests\n"
    "- Fácil de parametrizar (role, active, etc.)\n"
    "- Los datos son predecibles y trazables"
),
"pedagogical_objective": "Implementar una factory de datos de prueba con estado autoincremental.",
"syntax_hint": "`self._counter += 1` al inicio de `create()` para que el primer id sea 1.",
"hints_json": json.dumps([
    "self._counter += 1 — incrementa primero, luego úsalo en el dict.",
    "return {'id': self._counter, 'email': f'user{self._counter}@test.io', 'role': role, 'active': active}",
    "u1: id=1, u2: id=2 (role='ADMIN'), u3: id=3 (active=False).",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-025: SCREENSHOT ON FAILURE ]",
"description": (
    "Implementa el decorador `capture_on_failure(fn)` que ejecute `fn()` y, "
    "si lanza cualquier excepción, imprima `'[SCREENSHOT] {fn.__name__}_failure.png captured'` "
    "antes de re-lanzar la excepción."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 25, "base_xp_reward": 200,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "python",
"phase": "automatizacion_e2e", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["decoradores", "screenshots", "debugging", "evidencia"]),
"initial_code": (
    "def capture_on_failure(fn):\n"
    "    # TODO: retorna un wrapper que:\n"
    "    # 1. llama fn()\n"
    "    # 2. si lanza excepción: imprime '[SCREENSHOT] {fn.__name__}_failure.png captured'\n"
    "    # 3. re-lanza la excepción\n"
    "    pass\n"
    "\n"
    "\n"
    "@capture_on_failure\n"
    "def test_login_success():\n"
    "    print('Login test passed')\n"
    "\n"
    "@capture_on_failure\n"
    "def test_checkout_flow():\n"
    "    raise AssertionError('Element not found: [data-testid=\"pay-btn\"]')\n"
    "\n"
    "@capture_on_failure\n"
    "def test_search():\n"
    "    raise TimeoutError('Timeout waiting for results')\n"
    "\n"
    "\n"
    "test_login_success()\n"
    "\n"
    "try:\n"
    "    test_checkout_flow()\n"
    "except AssertionError as e:\n"
    "    print(f'CAUGHT: {e}')\n"
    "\n"
    "try:\n"
    "    test_search()\n"
    "except TimeoutError as e:\n"
    "    print(f'CAUGHT: {e}')\n"
),
"expected_output": (
    "Login test passed\n"
    "[SCREENSHOT] test_checkout_flow_failure.png captured\n"
    "CAUGHT: Element not found: [data-testid=\"pay-btn\"]\n"
    "[SCREENSHOT] test_search_failure.png captured\n"
    "CAUGHT: Timeout waiting for results"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Un test que falla sin evidencia es un misterio. "
    "El screenshot es tu testigo — aparece justo antes del error."
),
"theory_content": (
    "## Decoradores en Testing\n\n"
    "Un decorador envuelve una función para añadir comportamiento:\n\n"
    "```python\ndef capture_on_failure(fn):\n    def wrapper(*args, **kwargs):\n        try:\n            return fn(*args, **kwargs)\n        except Exception:\n            take_screenshot(fn.__name__)\n            raise\n    return wrapper\n```\n\n"
    "**Patrón clave**: `raise` sin argumentos re-lanza la excepción original con su traceback."
),
"pedagogical_objective": "Implementar un decorador que capture evidencia automáticamente cuando un test falla.",
"syntax_hint": "Usa `functools.wraps(fn)` en el wrapper para preservar el nombre de la función.",
"hints_json": json.dumps([
    "def wrapper(*args, **kwargs): try: return fn(*args, **kwargs) except Exception: print(...) raise",
    "f'[SCREENSHOT] {fn.__name__}_failure.png captured' — usa fn.__name__ del closure.",
    "No olvides el `raise` al final del except — sin él, la excepción se 'come' y el test no falla.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-026: CROSS-BROWSER MATRIX ]",
"description": (
    "Implementa `build_matrix(browsers: list, os_list: list) -> list` que retorne "
    "todas las combinaciones browser × OS como dicts `{'browser': ..., 'os': ...}`. "
    "También implementa `count_combinations(matrix) -> int`."
),
"difficulty_tier": 1, "difficulty": "easy",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 26, "base_xp_reward": 210,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 200, "challenge_type": "python",
"phase": "automatizacion_e2e", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["cross_browser", "matrix", "combinatoria"]),
"initial_code": (
    "from itertools import product\n"
    "\n"
    "\n"
    "def build_matrix(browsers: list, os_list: list) -> list:\n"
    "    # TODO: retorna lista de dicts {'browser': b, 'os': o} para cada combinacion\n"
    "    pass\n"
    "\n"
    "\n"
    "def count_combinations(matrix: list) -> int:\n"
    "    # TODO: retorna len(matrix)\n"
    "    pass\n"
    "\n"
    "\n"
    "browsers = ['Chrome', 'Firefox', 'Safari']\n"
    "os_list  = ['Windows', 'macOS', 'Linux']\n"
    "\n"
    "matrix = build_matrix(browsers, os_list)\n"
    "print(f'Total combinations: {count_combinations(matrix)}')\n"
    "for combo in matrix:\n"
    "    print(f'{combo[\"browser\"]} | {combo[\"os\"]}')\n"
),
"expected_output": (
    "Total combinations: 9\n"
    "Chrome | Windows\n"
    "Chrome | macOS\n"
    "Chrome | Linux\n"
    "Firefox | Windows\n"
    "Firefox | macOS\n"
    "Firefox | Linux\n"
    "Safari | Windows\n"
    "Safari | macOS\n"
    "Safari | Linux"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Chrome en Mac != Chrome en Windows. "
    "La matriz de compatibilidad define tu superficie de prueba real."
),
"theory_content": (
    "## Cross-Browser Testing Matrix\n\n"
    "Con 3 browsers y 3 OS: 3 × 3 = **9 combinaciones**.\n\n"
    "En la práctica no se prueba todo — se prioriza:\n"
    "1. Las combinaciones más usadas por los usuarios (analytics)\n"
    "2. Las combinaciones más propensas a diferencias (Safari/iOS)\n\n"
    "Herramientas como BrowserStack o Sauce Labs ejecutan la matrix en paralelo."
),
"pedagogical_objective": "Generar la matriz cartesiana de combinaciones browser × OS para cross-browser testing.",
"syntax_hint": "`return [{'browser': b, 'os': o} for b, o in product(browsers, os_list)]`",
"hints_json": json.dumps([
    "from itertools import product — ya está importado en el template.",
    "[{'browser': b, 'os': o} for b, o in product(browsers, os_list)]",
    "count_combinations: simplemente `return len(matrix)`.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-027: RETRY MECHANISM ]",
"description": (
    "Implementa el decorador `retry(max_attempts: int, delay: float = 0)` "
    "que reintente la función hasta `max_attempts` veces si lanza excepción. "
    "En cada intento imprime `'Attempt {n}/{max}'`."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 27, "base_xp_reward": 220,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "python",
"phase": "automatizacion_e2e", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["retry", "flaky_tests", "decoradores", "resiliencia"]),
"initial_code": (
    "def retry(max_attempts: int, delay: float = 0):\n"
    "    # TODO: retorna un decorador que reintente fn hasta max_attempts veces\n"
    "    # En cada intento imprime 'Attempt {n}/{max_attempts}'\n"
    "    # Si tiene éxito: retorna el resultado\n"
    "    # Si se agotan los intentos: re-lanza la última excepción\n"
    "    pass\n"
    "\n"
    "\n"
    "attempt_log = [0]\n"
    "\n"
    "@retry(max_attempts=3)\n"
    "def flaky_test():\n"
    "    attempt_log[0] += 1\n"
    "    if attempt_log[0] < 3:\n"
    "        raise ConnectionError('network blip')\n"
    "    return 'PASS'\n"
    "\n"
    "\n"
    "result = flaky_test()\n"
    "print(f'Result: {result}')\n"
    "\n"
    "# Test que agota los intentos\n"
    "@retry(max_attempts=2)\n"
    "def always_fails():\n"
    "    raise AssertionError('always broken')\n"
    "\n"
    "try:\n"
    "    always_fails()\n"
    "except AssertionError as e:\n"
    "    print(f'Failed after retries: {e}')\n"
),
"expected_output": (
    "Attempt 1/3\n"
    "Attempt 2/3\n"
    "Attempt 3/3\n"
    "Result: PASS\n"
    "Attempt 1/2\n"
    "Attempt 2/2\n"
    "Failed after retries: always broken"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Los tests flaky existen. El retry los contiene mientras investigas la causa raíz. "
    "No es un fix — es un contención."
),
"theory_content": (
    "## Retry Pattern\n\n"
    "```python\n@retry(max_attempts=3)\ndef test_flaky():\n    ...\n```\n\n"
    "**Implementación**: decorador de orden superior (decorator factory):\n"
    "```python\ndef retry(max_attempts):\n    def decorator(fn):\n        def wrapper(*args, **kwargs):\n            for attempt in range(1, max_attempts+1):\n                try:\n                    return fn(*args, **kwargs)\n                except Exception:\n                    if attempt == max_attempts: raise\n        return wrapper\n    return decorator\n```"
),
"pedagogical_objective": "Implementar un retry decorator con contador de intentos y re-lanzamiento de la última excepción.",
"syntax_hint": "Necesitas 3 niveles de función: `retry(max)` → `decorator(fn)` → `wrapper(*args)`.",
"hints_json": json.dumps([
    "retry retorna decorator; decorator recibe fn y retorna wrapper.",
    "En wrapper: for i in range(1, max_attempts+1): print(f'Attempt {i}/{max_attempts}'); try: return fn(...); except: if i==max_attempts: raise",
    "El print va ANTES del try — así aparece para cada intento incluyendo el exitoso.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-028: PARALLEL TEST SPLITTER ]",
"description": (
    "Implementa `split_tests(tests: list, workers: int) -> list` "
    "que distribuya los tests en `workers` grupos balanceados por duración estimada. "
    "Asigna cada test al worker con menor carga total."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 28, "base_xp_reward": 230,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "python",
"phase": "automatizacion_e2e", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["paralelismo", "balanceo", "CI", "optimizacion"]),
"initial_code": (
    "def split_tests(tests: list, workers: int) -> list:\n"
    "    # TODO: distribuye tests en workers grupos balanceados\n"
    "    # tests: lista de dicts {'name': str, 'duration': int}\n"
    "    # Asigna cada test al worker con menor carga total acumulada\n"
    "    # Retorna lista de workers: [[test1, test2, ...], [test3, ...], ...]\n"
    "    pass\n"
    "\n"
    "\n"
    "tests = [\n"
    "    {'name': 'auth_suite',     'duration': 120},\n"
    "    {'name': 'checkout_suite', 'duration': 95},\n"
    "    {'name': 'search_suite',   'duration': 80},\n"
    "    {'name': 'api_suite',      'duration': 60},\n"
    "    {'name': 'smoke_suite',    'duration': 40},\n"
    "]\n"
    "groups = split_tests(tests, workers=3)\n"
    "for i, group in enumerate(groups, 1):\n"
    "    names = [t['name'] for t in group]\n"
    "    total = sum(t['duration'] for t in group)\n"
    "    print(f'Worker {i} ({total}s): {\", \".join(names)}')\n"
),
"expected_output": (
    "Worker 1 (160s): auth_suite, api_suite\n"
    "Worker 2 (135s): checkout_suite, smoke_suite\n"
    "Worker 3 (80s): search_suite"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Paralelizar sin balancear crea workers ociosos. "
    "El splitter optimiza el throughput asignando trabajo con criterio."
),
"theory_content": (
    "## Greedy Load Balancing\n\n"
    "Algoritmo: ordena tests de mayor a menor duración (greedy), "
    "asigna cada uno al worker con menor carga acumulada:\n\n"
    "```\nauthentication(120) → Worker 1\ncheckout(95) → Worker 2\nsearch(80) → Worker 3\napi(60) → Worker 1 (carga: 120 < 95+80)\nsmoke(40) → Worker 2 (carga: 95 < 120+60)\n```\n\n"
    "Resultado: cargas de 180, 135, 80 — mucho más balanceado que round-robin."
),
"pedagogical_objective": "Implementar distribución balanceada de tests entre workers usando greedy por menor carga.",
"syntax_hint": "Ordena por duración desc, luego usa `min(range(workers), key=lambda i: loads[i])`.",
"hints_json": json.dumps([
    "Inicializa: groups=[[] for _ in range(workers)], loads=[0]*workers.",
    "Ordena tests por duration desc: sorted(tests, key=lambda t: t['duration'], reverse=True).",
    "Para cada test: worker_idx = loads.index(min(loads)); groups[worker_idx].append(test); loads[worker_idx] += test['duration'].",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-029: VISUAL REGRESSION DETECTOR ]",
"description": (
    "Implementa `compare_snapshots(baseline: str, current: str) -> dict` "
    "que compare dos strings carácter a carácter y retorne "
    "`{'similarity': float, 'diff_chars': int, 'status': str}`. "
    "`similarity = round(1 - diff_chars/total, 2)`. Status: `'PASS'` si similarity >= 0.95, `'FAIL'` si no."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 29, "base_xp_reward": 240,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "python",
"phase": "automatizacion_e2e", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["visual_regression", "snapshot", "similitud"]),
"initial_code": (
    "def compare_snapshots(baseline: str, current: str) -> dict:\n"
    "    # TODO: compara char por char\n"
    "    # total = len(baseline)\n"
    "    # diff_chars = cantidad de posiciones donde baseline[i] != current[i]\n"
    "    # similarity = round(1 - diff_chars / total, 2)\n"
    "    # status = 'PASS' si similarity >= 0.95, else 'FAIL'\n"
    "    pass\n"
    "\n"
    "\n"
    "baseline = 'HELLO WORLD 2024'\n"
    "tests = [\n"
    "    ('HELLO WORLD 2024', 'identical'),\n"
    "    ('HELLO WORLD 2025', '1 char diff'),\n"
    "    ('HELLO EARTH 2024', '5 char diff'),\n"
    "]\n"
    "for current, label in tests:\n"
    "    result = compare_snapshots(baseline, current)\n"
    "    print(f'{label}: sim={result[\"similarity\"]} diffs={result[\"diff_chars\"]} [{result[\"status\"]}]')\n"
),
"expected_output": (
    "identical: sim=1.0 diffs=0 [PASS]\n"
    "1 char diff: sim=0.94 diffs=1 [FAIL]\n"
    "5 char diff: sim=0.69 diffs=5 [FAIL]"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "El CSS cambió y nadie lo notó. "
    "La regresión visual detecta lo que el ojo humano pierde en revisiones rápidas."
),
"theory_content": (
    "## Visual Regression Testing\n\n"
    "Comparación pixel a pixel (o char a char en simulación):\n\n"
    "```python\nsimilarity = 1 - (diff_pixels / total_pixels)\n```\n\n"
    "**Thresholds comunes:**\n"
    "- >= 0.99: sin cambios (tolerancia para anti-aliasing)\n"
    "- >= 0.95: cambios menores aceptables\n"
    "- < 0.95: regresión detectada — revisar manualmente\n\n"
    "Herramientas: Percy, Applitools, Playwright screenshots."
),
"pedagogical_objective": "Implementar comparación de snapshots con cálculo de similitud y threshold de aprobación.",
"syntax_hint": "`diff_chars = sum(1 for a, b in zip(baseline, current) if a != b)`",
"hints_json": json.dumps([
    "total = len(baseline). diff_chars = sum(1 for a,b in zip(baseline,current) if a != b).",
    "'HELLO WORLD 2024' tiene 16 chars. 1 diff → sim=1-1/16=0.9375→round=0.94.",
    "'HELLO EARTH 2024' vs 'HELLO WORLD 2024': E≠W, A≠O, R≠R(ok), T≠L, H≠D → 5 diffs. sim=1-5/16=0.6875→0.69.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-030: TEST REPORT GENERATOR ]",
"description": (
    "Implementa `generate_report(results: list) -> str` que procese una lista de resultados "
    "y genere un reporte con conteos, duración total y pass rate."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 30, "base_xp_reward": 250,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "python",
"phase": "automatizacion_e2e", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["reporting", "metricas", "pass_rate"]),
"initial_code": (
    "def generate_report(results: list) -> str:\n"
    "    # TODO: genera reporte de resultados\n"
    "    # results: lista de dicts {'name': str, 'status': 'PASS'|'FAIL'|'SKIP', 'duration': int}\n"
    "    # Calcula: passed, failed, skipped, total_duration\n"
    "    # pass_rate = round(passed / len(results) * 100, 1)\n"
    "    # Formato:\n"
    "    # === TEST REPORT ===\n"
    "    # PASSED:  {n}  FAILED: {n}  SKIPPED: {n}\n"
    "    # DURATION: {total}ms\n"
    "    # PASS RATE: {rate}%\n"
    "    # ==================\n"
    "    pass\n"
    "\n"
    "\n"
    "results = [\n"
    "    {'name': 'test_login',    'status': 'PASS', 'duration': 320},\n"
    "    {'name': 'test_checkout', 'status': 'PASS', 'duration': 580},\n"
    "    {'name': 'test_search',   'status': 'FAIL', 'duration': 210},\n"
    "    {'name': 'test_profile',  'status': 'PASS', 'duration': 190},\n"
    "    {'name': 'test_admin',    'status': 'SKIP', 'duration':   0},\n"
    "]\n"
    "print(generate_report(results))\n"
),
"expected_output": (
    "=== TEST REPORT ===\n"
    "PASSED:  3  FAILED: 1  SKIPPED: 1\n"
    "DURATION: 1300ms\n"
    "PASS RATE: 60.0%\n"
    "=================="
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Los resultados crudos son datos. El reporte es información. "
    "El stakeholder necesita información — no un JSON de 500 líneas."
),
"theory_content": (
    "## Test Reporting\n\n"
    "Las métricas mínimas de un reporte:\n\n"
    "| Métrica     | Fórmula |\n"
    "|-------------|----------|\n"
    "| Pass Rate   | passed / total * 100 |\n"
    "| Duration    | sum de todas las duraciones |\n"
    "| Failed      | count donde status == 'FAIL' |\n\n"
    "**Pass Rate** es la métrica más comunicada a stakeholders. "
    "Un 60% de pass rate en CI es una señal de alerta."
),
"pedagogical_objective": "Generar un reporte de resultados de test con métricas clave formateadas.",
"syntax_hint": "`passed = sum(1 for r in results if r['status'] == 'PASS')`",
"hints_json": json.dumps([
    "passed=3, failed=1, skipped=1, total_duration=320+580+210+190+0=1300.",
    "pass_rate=round(3/5*100, 1)=60.0.",
    "El formato usa 2 espacios entre PASSED/FAILED/SKIPPED para alinear.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-031: LOCATOR VALIDATOR ]",
"description": (
    "Implementa `validate_locators(locators: list) -> list` que retorne "
    "una lista de issues para locators problemáticos: "
    "IDs auto-generados (contienen dígitos al inicio o `__`), "
    "índices CSS (`nth-child`, `:eq(`), o clases genéricas (`col-`, `row-`)."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 31, "base_xp_reward": 260,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "python",
"phase": "automatizacion_e2e", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["locators", "validacion", "best_practices"]),
"initial_code": (
    "import re\n"
    "\n"
    "\n"
    "def validate_locators(locators: list) -> list:\n"
    "    # TODO: retorna lista de dicts {'locator': str, 'issue': str}\n"
    "    # Reglas de detección:\n"
    "    # - '#\\d' o '__' en el locator → 'auto-generated id'\n"
    "    # - 'nth-child' o ':eq(' en el locator → 'index-based selector'\n"
    "    # - '.col-' o '.row-' en el locator → 'generic class'\n"
    "    # Si ninguna regla aplica → locator OK (no incluir en la lista)\n"
    "    pass\n"
    "\n"
    "\n"
    "locators = [\n"
    "    '[data-testid=\"submit-btn\"]',\n"
    "    '#form123',\n"
    "    'div:nth-child(3) > button',\n"
    "    '.col-md-6 > input',\n"
    "    '#__next > div',\n"
    "    '.login-form button[type=\"submit\"]',\n"
    "]\n"
    "issues = validate_locators(locators)\n"
    "print(f'{len(issues)} issue(s) found:')\n"
    "for issue in issues:\n"
    "    print(f'  [{issue[\"issue\"]}] {issue[\"locator\"]}')\n"
),
"expected_output": (
    "3 issue(s) found:\n"
    "  [auto-generated id] #form123\n"
    "  [index-based selector] div:nth-child(3) > button\n"
    "  [generic class] .col-md-6 > input"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Un locator frágil es una deuda técnica que paga intereses en cada CI run. "
    "El validator la detecta antes de que el test llegue a producción."
),
"theory_content": (
    "## Locator Best Practices\n\n"
    "**Evitar:**\n"
    "- IDs auto-generados: `#form123`, `#__next` — cambian en cada build\n"
    "- Índices: `nth-child(3)` — se rompen si se agrega un elemento\n"
    "- Clases de framework: `.col-md-6`, `.row-` — refactoring las mueve\n\n"
    "**Preferir:**\n"
    "- `[data-testid=\"nombre-descriptivo\"]` — estable y semántico\n"
    "- `[aria-label=\"Submit form\"]` — accesibilidad + estabilidad"
),
"pedagogical_objective": "Validar locators CSS/XPath contra reglas de best practices usando expresiones regulares.",
"syntax_hint": "Usa `re.search(r'#\\d', loc)` para detectar IDs numéricos.",
"hints_json": json.dumps([
    "Para auto-generated: re.search(r'#\\d', loc) OR '__' in loc.",
    "Para index-based: 'nth-child' in loc OR ':eq(' in loc.",
    "Para generic class: '.col-' in loc OR '.row-' in loc. '#__next' tiene '__' → auto-generated.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-032: ACTION CHAIN BUILDER ]",
"description": (
    "Implementa `ActionChain` con método `chain(*actions)` que registre y ejecute "
    "acciones en secuencia. Cada acción es un string que se imprime al ejecutar."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 32, "base_xp_reward": 270,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "python",
"phase": "automatizacion_e2e", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["action_chains", "fluent_interface", "secuencia"]),
"initial_code": (
    "class ActionChain:\n"
    "    def __init__(self):\n"
    "        self._actions = []\n"
    "\n"
    "    def hover(self, selector: str):\n"
    "        # TODO: agrega 'hover({selector})' a self._actions, retorna self\n"
    "        pass\n"
    "\n"
    "    def click(self, selector: str):\n"
    "        # TODO: agrega 'click({selector})' a self._actions, retorna self\n"
    "        pass\n"
    "\n"
    "    def type_text(self, selector: str, text: str):\n"
    "        # TODO: agrega 'type({selector}, \"{text}\")' a self._actions, retorna self\n"
    "        pass\n"
    "\n"
    "    def submit(self, selector: str):\n"
    "        # TODO: agrega 'submit({selector})' a self._actions, retorna self\n"
    "        pass\n"
    "\n"
    "    def execute(self):\n"
    "        # TODO: imprime cada acción en self._actions numerada, luego limpia la lista\n"
    "        # Formato: 'Step {i}: {accion}'\n"
    "        pass\n"
    "\n"
    "\n"
    "chain = ActionChain()\n"
    "chain.hover('[data-testid=\"menu\"]') \\\n"
    "     .click('[data-testid=\"login-link\"]') \\\n"
    "     .type_text('[data-testid=\"username\"]', 'operator') \\\n"
    "     .type_text('[data-testid=\"password\"]', 'secret') \\\n"
    "     .submit('[data-testid=\"login-form\"]')\n"
    "chain.execute()\n"
),
"expected_output": (
    "Step 1: hover([data-testid=\"menu\"])\n"
    "Step 2: click([data-testid=\"login-link\"])\n"
    "Step 3: type([data-testid=\"username\"], \"operator\")\n"
    "Step 4: type([data-testid=\"password\"], \"secret\")\n"
    'Step 5: submit([data-testid="login-form"])'
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Las interacciones complejas requieren cadenas de acciones precisas y ordenadas. "
    "Un fluent interface hace el código legible como prosa."
),
"theory_content": (
    "## Fluent Interface / Method Chaining\n\n"
    "Cada método retorna `self` para permitir encadenamiento:\n\n"
    "```python\nchain.hover('#menu').click('#link').type('#field', 'text').submit('#form')\n```\n\n"
    "**Patrón**: usado extensamente en Playwright, Selenium, y builders en general. "
    "Hace el código de tests más legible y reduce variables intermedias."
),
"pedagogical_objective": "Implementar el patrón fluent interface (method chaining) para construir cadenas de acciones.",
"syntax_hint": "Cada método debe terminar con `return self` para habilitar el encadenamiento.",
"hints_json": json.dumps([
    "Todos los métodos (hover, click, type_text, submit) deben hacer append y retornar self.",
    "hover: self._actions.append(f'hover({selector})'); return self",
    "execute: for i, action in enumerate(self._actions, 1): print(f'Step {i}: {action}'). No olvides limpiar: self._actions = []",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-033: IFRAME NAVIGATOR ]",
"description": (
    "Implementa `IframeNavigator` con `enter_frame(name)`, `exit_frame()`, "
    "`current_context() -> str` y `find_in_frame(frame: str, selector: str) -> str`."
),
"difficulty_tier": 3, "difficulty": "hard",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 33, "base_xp_reward": 290,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 300, "challenge_type": "python",
"phase": "automatizacion_e2e", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["iframes", "navegacion", "contexto", "DOM"]),
"initial_code": (
    "class IframeNavigator:\n"
    "    def __init__(self):\n"
    "        self._stack = ['main']\n"
    "        self._elements = {\n"
    "            'payment-frame': {'[data-testid=\"card-number\"]': 'card-input'},\n"
    "            'address-frame': {'[data-testid=\"street\"]': 'street-input'},\n"
    "            'main':          {'[data-testid=\"checkout-btn\"]': 'checkout-button'},\n"
    "        }\n"
    "\n"
    "    def enter_frame(self, name: str):\n"
    "        # TODO: agrega name al stack, imprime 'Entered frame: {name}'\n"
    "        pass\n"
    "\n"
    "    def exit_frame(self):\n"
    "        # TODO: si no estamos en 'main', saca el frame del stack\n"
    "        # imprime 'Exited to: {nuevo contexto actual}'\n"
    "        pass\n"
    "\n"
    "    def current_context(self) -> str:\n"
    "        # TODO: retorna self._stack[-1]\n"
    "        pass\n"
    "\n"
    "    def find_in_frame(self, frame: str, selector: str) -> str:\n"
    "        # TODO: retorna self._elements.get(frame, {}).get(selector, 'NOT_FOUND')\n"
    "        pass\n"
    "\n"
    "\n"
    "nav = IframeNavigator()\n"
    "print(f'Context: {nav.current_context()}')\n"
    "nav.enter_frame('payment-frame')\n"
    "print(f'Context: {nav.current_context()}')\n"
    "found = nav.find_in_frame('payment-frame', '[data-testid=\"card-number\"]')\n"
    "print(f'Found: {found}')\n"
    "nav.exit_frame()\n"
    "print(f'Context: {nav.current_context()}')\n"
),
"expected_output": (
    "Context: main\n"
    "Entered frame: payment-frame\n"
    "Context: payment-frame\n"
    "Found: card-input\n"
    "Exited to: main\n"
    "Context: main"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Los iframes son el laberinto del DOM. "
    "Sin navegación precisa de contexto, tus tests buscan elementos en el lugar equivocado."
),
"theory_content": (
    "## Iframe Navigation\n\n"
    "En Playwright:\n"
    "```python\nframe = page.frame('payment-frame')\nframe.fill('[data-testid=\"card\"]', '4111')\n```\n\n"
    "El error más común: intentar interactuar con elementos dentro de un iframe "
    "desde el contexto del frame principal → `ElementNotFound`.\n\n"
    "**Stack de contextos**: modelarlo como una pila te permite entrar y salir de iframes anidados."
),
"pedagogical_objective": "Modelar la navegación de contextos de iframes usando una pila (stack) de frames.",
"syntax_hint": "Usa `self._stack` como pila: `append` para entrar, `pop` para salir.",
"hints_json": json.dumps([
    "enter_frame: self._stack.append(name); print(f'Entered frame: {name}')",
    "exit_frame: if self._stack[-1] != 'main': self._stack.pop(); print(f'Exited to: {self._stack[-1]}')",
    "current_context: return self._stack[-1]. find_in_frame: return self._elements.get(frame, {}).get(selector, 'NOT_FOUND')",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-034: FILE UPLOAD TESTER ]",
"description": (
    "Implementa `FileUploadValidator.validate(filename: str, size_kb: int) -> dict` "
    "que retorne `{'valid': bool, 'issues': list}`. "
    "Reglas: tamaño máximo 5MB (5120 KB), extensiones permitidas: pdf, jpg, png, docx."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 34, "base_xp_reward": 300,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "python",
"phase": "automatizacion_e2e", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["file_upload", "validacion", "edge_cases"]),
"initial_code": (
    "class FileUploadValidator:\n"
    "    MAX_SIZE_KB = 5120\n"
    "    ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'png', 'docx'}\n"
    "\n"
    "    def validate(self, filename: str, size_kb: int) -> dict:\n"
    "        # TODO: retorna {'valid': bool, 'issues': list}\n"
    "        # Verifica:\n"
    "        # 1. Extensión: si no está en ALLOWED_EXTENSIONS → 'invalid extension: {ext}'\n"
    "        # 2. Tamaño: si size_kb > MAX_SIZE_KB → 'file too large: {size_kb}KB (max 5120KB)'\n"
    "        pass\n"
    "\n"
    "\n"
    "validator = FileUploadValidator()\n"
    "files = [\n"
    "    ('report.pdf',    1024),\n"
    "    ('photo.jpg',     6000),\n"
    "    ('script.exe',     512),\n"
    "    ('data.csv',      2048),\n"
    "    ('diagram.png',   4096),\n"
    "]\n"
    "for fname, size in files:\n"
    "    result = validator.validate(fname, size)\n"
    "    status = 'OK' if result['valid'] else f'ERROR: {\"; \".join(result[\"issues\"])}'\n"
    "    print(f'{fname:<20}: {status}')\n"
),
"expected_output": (
    "report.pdf          : OK\n"
    "photo.jpg           : ERROR: file too large: 6000KB (max 5120KB)\n"
    "script.exe          : ERROR: invalid extension: exe\n"
    "data.csv            : ERROR: invalid extension: csv\n"
    "diagram.png         : OK"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "El upload de archivos tiene edge cases clásicos: tipo inválido, tamaño excesivo, "
    "nombre con caracteres especiales. Cúbrelos todos."
),
"theory_content": (
    "## File Upload Testing\n\n"
    "Test cases obligatorios para cualquier file upload:\n\n"
    "| Escenario | Resultado esperado |\n"
    "|-----------|-------------------|\n"
    "| Extensión válida, tamaño OK | Aceptar |\n"
    "| Extensión inválida | Rechazar con mensaje |\n"
    "| Tamaño > máximo | Rechazar con mensaje |\n"
    "| Nombre con espacios/chars especiales | Sanitizar o rechazar |\n"
    "| Archivo vacío (0 KB) | Rechazar |\n\n"
    "Extrae la extensión con: `filename.rsplit('.', 1)[-1].lower()`"
),
"pedagogical_objective": "Validar archivos subidos verificando extensión y tamaño con mensajes de error específicos.",
"syntax_hint": "`ext = filename.rsplit('.', 1)[-1].lower()` para extraer la extensión.",
"hints_json": json.dumps([
    "ext = filename.rsplit('.', 1)[-1].lower() — separa por el último punto.",
    "issues = []; if ext not in self.ALLOWED_EXTENSIONS: issues.append(f'invalid extension: {ext}')",
    "if size_kb > self.MAX_SIZE_KB: issues.append(f'file too large: {size_kb}KB (max 5120KB)'). valid = len(issues) == 0.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-035: MOBILE RESPONSIVE TESTER ]",
"description": (
    "Implementa `ResponsiveTester.check_visibility(viewport_width: int, component: str) -> str` "
    "según las reglas de breakpoints: "
    "sidebar visible solo si width >= 768, mobile-menu visible solo si width < 768, "
    "hero-banner visible solo si width >= 1024."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 35, "base_xp_reward": 350,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "python",
"phase": "automatizacion_e2e", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["responsive", "mobile", "viewports", "breakpoints"]),
"initial_code": (
    "class ResponsiveTester:\n"
    "    BREAKPOINTS = {\n"
    "        'sidebar':     {'min': 768},\n"
    "        'mobile-menu': {'max': 767},\n"
    "        'hero-banner': {'min': 1024},\n"
    "        'footer':      {},        # siempre visible\n"
    "    }\n"
    "\n"
    "    def check_visibility(self, viewport_width: int, component: str) -> str:\n"
    "        # TODO: retorna 'VISIBLE' o 'HIDDEN' según breakpoints\n"
    "        # Si el componente no tiene restricciones → siempre 'VISIBLE'\n"
    "        # Si tiene 'min': visible solo si viewport_width >= min\n"
    "        # Si tiene 'max': visible solo si viewport_width <= max\n"
    "        pass\n"
    "\n"
    "\n"
    "tester = ResponsiveTester()\n"
    "viewports = [375, 768, 1024, 1440]\n"
    "components = ['sidebar', 'mobile-menu', 'hero-banner', 'footer']\n"
    "print(f'{'Component':<15} | {' | '.join(f'{v}px' for v in viewports)}')\n"
    "print('-' * 55)\n"
    "for comp in components:\n"
    "    results = [tester.check_visibility(vp, comp)[:3] for vp in viewports]\n"
    "    print(f'{comp:<15} | {\" | \".join(f\"{r:<5}\" for r in results)}')\n"
),
"expected_output": (
    "Component       | 375px | 768px | 1024px | 1440px\n"
    "-------------------------------------------------------\n"
    "sidebar         | HID   | VIS   | VIS    | VIS  \n"
    "mobile-menu     | VIS   | HID   | HID    | HID  \n"
    "hero-banner     | HID   | HID   | VIS    | VIS  \n"
    "footer          | VIS   | VIS   | VIS    | VIS  "
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "El 60% del tráfico es mobile. "
    "Si tus tests solo cubren desktop, cubres el 40% — y la mitad de tus usuarios sufren."
),
"theory_content": (
    "## Responsive Testing\n\n"
    "Breakpoints estándar:\n"
    "| Nombre  | Ancho     |\n"
    "|---------|----------|\n"
    "| Mobile  | < 768px   |\n"
    "| Tablet  | 768-1023px|\n"
    "| Desktop | >= 1024px |\n\n"
    "En Playwright: `await page.set_viewport_size({'width': 375, 'height': 667})`\n\n"
    "**Automatiza**: verifica que elementos críticos sean visibles en cada breakpoint."
),
"pedagogical_objective": "Evaluar visibilidad de componentes según breakpoints de viewport responsive.",
"syntax_hint": "Extrae `min` y `max` del dict de BREAKPOINTS con `.get()` y compara con viewport_width.",
"hints_json": json.dumps([
    "rules = self.BREAKPOINTS.get(component, {}). Si rules está vacío → return 'VISIBLE'.",
    "if 'min' in rules and viewport_width < rules['min']: return 'HIDDEN'",
    "if 'max' in rules and viewport_width > rules['max']: return 'HIDDEN'. else: return 'VISIBLE'.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-036: ACCESSIBILITY AUDIT ENGINE ]",
"description": (
    "Implementa `a11y_audit(elements: list) -> list` que detecte violaciones WCAG: "
    "imágenes sin `alt`, contraste insuficiente (ratio < 4.5), "
    "y elementos interactivos sin `aria-label`."
),
"difficulty_tier": 3, "difficulty": "hard",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 36, "base_xp_reward": 380,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 300, "challenge_type": "python",
"phase": "automatizacion_e2e", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["a11y", "WCAG", "accesibilidad", "auditoria"]),
"initial_code": (
    "def a11y_audit(elements: list) -> list:\n"
    "    # TODO: retorna lista de dicts {'element': str, 'violation': str}\n"
    "    # Reglas:\n"
    "    # - tipo 'img' sin 'alt' → 'missing alt text'\n"
    "    # - contrast_ratio < 4.5 → 'insufficient contrast: {ratio}'\n"
    "    # - tipo 'button' o 'input' sin 'aria_label' → 'missing aria-label'\n"
    "    pass\n"
    "\n"
    "\n"
    "elements = [\n"
    "    {'id': 'logo',      'type': 'img',    'alt': 'DAKI Logo', 'contrast_ratio': 7.0},\n"
    "    {'id': 'banner',    'type': 'img',    'alt': None,        'contrast_ratio': 7.0},\n"
    "    {'id': 'submit',    'type': 'button', 'aria_label': 'Submit form', 'contrast_ratio': 5.2},\n"
    "    {'id': 'close',     'type': 'button', 'aria_label': None, 'contrast_ratio': 3.1},\n"
    "    {'id': 'search',    'type': 'input',  'aria_label': None, 'contrast_ratio': 4.5},\n"
    "]\n"
    "violations = a11y_audit(elements)\n"
    "print(f'{len(violations)} violation(s):')\n"
    "for v in violations:\n"
    "    print(f'  #{v[\"element\"]}: {v[\"violation\"]}')\n"
),
"expected_output": (
    "3 violation(s):\n"
    "  #banner: missing alt text\n"
    "  #close: missing aria-label; insufficient contrast: 3.1\n"
    "  #search: missing aria-label"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "La accesibilidad no es opcional — es un requisito legal y ético. "
    "El QA Architect la audita y la defiende ante el equipo."
),
"theory_content": (
    "## WCAG 2.1 — Reglas Mínimas\n\n"
    "| Criterio | Regla |\n"
    "|----------|-------|\n"
    "| 1.1.1 Non-text content | Toda imagen debe tener `alt` |\n"
    "| 1.4.3 Contrast (minimum) | Ratio >= 4.5:1 para texto normal |\n"
    "| 4.1.2 Name, Role, Value | Controles interactivos necesitan nombre accesible |\n\n"
    "Herramientas: axe-core, Lighthouse, Playwright accessibility API."
),
"pedagogical_objective": "Implementar un auditor de accesibilidad que detecte violaciones WCAG básicas.",
"syntax_hint": "Acumula violations en una lista, verifica cada regla independientemente por elemento.",
"hints_json": json.dumps([
    "Para cada elemento: issues = []; si img y no alt → issues.append('missing alt text')",
    "Si contrast_ratio < 4.5 → issues.append(f'insufficient contrast: {ratio}'). Si button/input y no aria_label → issues.append('missing aria-label')",
    "Si issues: violations.append({'element': el['id'], 'violation': '; '.join(issues)}). close tiene 2 violaciones separadas por '; '.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-037: DRAG AND DROP AUTOMATOR ]",
"description": (
    "Implementa `DragDropSimulator.drag(source: str, target: str) -> str` "
    "que retorne el resultado de la operación. "
    "Implementa `verify_order(items: list, expected: list) -> bool`."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 37, "base_xp_reward": 320,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "python",
"phase": "automatizacion_e2e", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["drag_drop", "interacciones", "simulacion"]),
"initial_code": (
    "class DragDropSimulator:\n"
    "    def __init__(self):\n"
    "        self._items = ['Task A', 'Task B', 'Task C', 'Task D']\n"
    "\n"
    "    def drag(self, source: str, target: str) -> str:\n"
    "        # TODO: mueve source antes de target en self._items\n"
    "        # Si source o target no existen: retorna 'ERROR: element not found'\n"
    "        # Si source == target: retorna 'NO-OP: same element'\n"
    "        # Si éxito: retorna 'DROPPED: {source} before {target}'\n"
    "        pass\n"
    "\n"
    "    def verify_order(self, expected: list) -> bool:\n"
    "        # TODO: retorna True si self._items == expected\n"
    "        pass\n"
    "\n"
    "    def current_order(self) -> list:\n"
    "        return list(self._items)\n"
    "\n"
    "\n"
    "sim = DragDropSimulator()\n"
    "print(f'Initial: {sim.current_order()}')\n"
    "print(sim.drag('Task C', 'Task A'))\n"
    "print(f'After:   {sim.current_order()}')\n"
    "print(f'Verified: {sim.verify_order([\"Task C\", \"Task A\", \"Task B\", \"Task D\"])}')\n"
    "print(sim.drag('Task X', 'Task A'))\n"
    "print(sim.drag('Task A', 'Task A'))\n"
),
"expected_output": (
    "Initial: ['Task A', 'Task B', 'Task C', 'Task D']\n"
    "DROPPED: Task C before Task A\n"
    "After:   ['Task C', 'Task A', 'Task B', 'Task D']\n"
    "Verified: True\n"
    "ERROR: element not found\n"
    "NO-OP: same element"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "El drag & drop es una de las interacciones más propensas a flakiness. "
    "Modelar y verificar el estado resultante es la clave."
),
"theory_content": (
    "## Drag & Drop Testing\n\n"
    "En Playwright:\n"
    "```python\nawait page.drag_and_drop('#source', '#target')\n```\n\n"
    "**Edge cases a cubrir:**\n"
    "- Source o target no existen\n"
    "- Drop sobre sí mismo\n"
    "- Drop fuera del área válida\n"
    "- Verificación del orden resultante\n\n"
    "La verificación post-drag es tan importante como la acción misma."
),
"pedagogical_objective": "Simular drag & drop con validación de estado resultante y manejo de casos edge.",
"syntax_hint": "Para mover: `self._items.remove(source)` y luego `self._items.insert(target_idx, source)`.",
"hints_json": json.dumps([
    "Primero verifica: if source not in self._items or target not in self._items: return 'ERROR: element not found'",
    "if source == target: return 'NO-OP: same element'",
    "target_idx = self._items.index(target); self._items.remove(source); self._items.insert(target_idx, source); return f'DROPPED: {source} before {target}'",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-038: MULTI-TAB HANDLER ]",
"description": (
    "Implementa `TabManager` con `open_tab(url)`, `switch_to(idx)`, `close_current()`, "
    "`current_url() -> str`. Simula la gestión de múltiples tabs de browser."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 38, "base_xp_reward": 320,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "python",
"phase": "automatizacion_e2e", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["multi_tab", "window_handles", "gestion"]),
"initial_code": (
    "class TabManager:\n"
    "    def __init__(self, initial_url: str = 'about:blank'):\n"
    "        self._tabs = [initial_url]\n"
    "        self._active = 0\n"
    "\n"
    "    def open_tab(self, url: str):\n"
    "        # TODO: agrega url a self._tabs, cambia _active al nuevo tab, imprime 'Opened: {url}'\n"
    "        pass\n"
    "\n"
    "    def switch_to(self, idx: int):\n"
    "        # TODO: si idx válido: cambia _active e imprime 'Switched to tab {idx}: {url}'\n"
    "        #       si no: imprime 'ERROR: tab {idx} not found'\n"
    "        pass\n"
    "\n"
    "    def close_current(self):\n"
    "        # TODO: elimina el tab activo, activa el anterior (o 0 si es el primero)\n"
    "        # imprime 'Closed tab. Active: {nueva url}'\n"
    "        pass\n"
    "\n"
    "    def current_url(self) -> str:\n"
    "        # TODO: retorna self._tabs[self._active]\n"
    "        pass\n"
    "\n"
    "\n"
    "tm = TabManager('https://daki.io')\n"
    "tm.open_tab('https://daki.io/hub')\n"
    "tm.open_tab('https://daki.io/missions')\n"
    "print(f'Active: {tm.current_url()}')\n"
    "tm.switch_to(0)\n"
    "print(f'Active: {tm.current_url()}')\n"
    "tm.close_current()\n"
    "print(f'Active: {tm.current_url()}')\n"
    "tm.switch_to(5)\n"
),
"expected_output": (
    "Opened: https://daki.io/hub\n"
    "Opened: https://daki.io/missions\n"
    "Active: https://daki.io/missions\n"
    "Switched to tab 0: https://daki.io\n"
    "Active: https://daki.io\n"
    "Closed tab. Active: https://daki.io/hub\n"
    "Active: https://daki.io/hub\n"
    "ERROR: tab 5 not found"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Los tests multi-tab son frágiles si no gestionas el window handle correctamente. "
    "El TabManager modela exactamente ese manejo."
),
"theory_content": (
    "## Multi-Tab Testing\n\n"
    "En Playwright:\n"
    "```python\n# Nueva tab\nwith context.expect_page() as new_page_info:\n    page.click('#open-new-tab')\nnew_page = new_page_info.value\n# Volver a tab original\npage.bring_to_front()\n```\n\n"
    "**Error común**: no actualizar el window handle activo después de abrir/cerrar tabs."
),
"pedagogical_objective": "Gestionar múltiples tabs de browser con una estructura de lista indexada.",
"syntax_hint": "open_tab: `self._tabs.append(url); self._active = len(self._tabs) - 1`",
"hints_json": json.dumps([
    "open_tab: self._tabs.append(url); self._active = len(self._tabs)-1; print(f'Opened: {url}')",
    "switch_to: if 0 <= idx < len(self._tabs): self._active = idx; print(f'Switched to tab {idx}: {self._tabs[idx]}') else: print error",
    "close_current: self._tabs.pop(self._active); self._active = max(0, self._active-1); print(f'Closed tab. Active: {self._tabs[self._active]}')",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-039: SHADOW DOM PIERCER ]",
"description": (
    "Implementa `ShadowDOMResolver.pierce(host_selector: str, inner_selector: str) -> str` "
    "que simule acceso a elementos dentro de Shadow DOM. "
    "Si el host no existe o el inner no existe en ese host: retorna `'NOT_FOUND'`."
),
"difficulty_tier": 3, "difficulty": "hard",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 39, "base_xp_reward": 330,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 300, "challenge_type": "python",
"phase": "automatizacion_e2e", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["shadow_DOM", "encapsulacion", "web_components"]),
"initial_code": (
    "class ShadowDOMResolver:\n"
    "    def __init__(self):\n"
    "        # Shadow DOM tree: {host → {inner_selector → element_id}}\n"
    "        self._shadow_tree = {\n"
    "            'payment-widget':  {'#card-number': 'card-field', '#expiry': 'expiry-field'},\n"
    "            'chat-component':  {'#message-input': 'chat-input', '#send-btn': 'chat-send'},\n"
    "            'video-player':    {'#play-btn': 'play-button', '#progress': 'progress-bar'},\n"
    "        }\n"
    "\n"
    "    def pierce(self, host_selector: str, inner_selector: str) -> str:\n"
    "        # TODO: retorna el element_id si existe, 'NOT_FOUND' si no\n"
    "        pass\n"
    "\n"
    "    def list_shadow_roots(self) -> list:\n"
    "        # TODO: retorna lista de hosts (keys de self._shadow_tree) ordenados\n"
    "        pass\n"
    "\n"
    "\n"
    "resolver = ShadowDOMResolver()\n"
    "print('Shadow roots:', sorted(resolver.list_shadow_roots()))\n"
    "print(resolver.pierce('payment-widget', '#card-number'))\n"
    "print(resolver.pierce('payment-widget', '#cvv'))\n"
    "print(resolver.pierce('unknown-host', '#any'))\n"
    "print(resolver.pierce('chat-component', '#send-btn'))\n"
),
"expected_output": (
    "Shadow roots: ['chat-component', 'payment-widget', 'video-player']\n"
    "card-field\n"
    "NOT_FOUND\n"
    "NOT_FOUND\n"
    "chat-send"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "El Shadow DOM encapsula componentes web. "
    "Para testearlo, necesitas piercing strategies — de lo contrario, Playwright no lo encuentra."
),
"theory_content": (
    "## Shadow DOM Testing\n\n"
    "El Shadow DOM encapsula CSS y estructura HTML dentro de un web component:\n\n"
    "```python\n# Playwright — piercing automático\npage.locator('payment-widget >> #card-number')\n# O usando evaluate\npage.evaluate('document.querySelector(\"payment-widget\").shadowRoot.querySelector(\"#card-number\")')\n```\n\n"
    "**Key insight**: el selector estándar no puede encontrar elementos dentro del Shadow Root."
),
"pedagogical_objective": "Modelar la navegación de Shadow DOM con resolución de host + inner selector.",
"syntax_hint": "`return self._shadow_tree.get(host_selector, {}).get(inner_selector, 'NOT_FOUND')`",
"hints_json": json.dumps([
    "pierce: return self._shadow_tree.get(host_selector, {}).get(inner_selector, 'NOT_FOUND')",
    "list_shadow_roots: return list(self._shadow_tree.keys())",
    "El print usa sorted() externamente — list_shadow_roots puede retornar en cualquier orden.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ QA-040: CONTRATO — SUITE E2E COMPLETA ]",
"description": (
    "Proyecto integrador: implementa `E2ESuite` con `add_test(name, steps)`, "
    "`run_all() -> dict`, y `report() -> str`. "
    "Cada test tiene steps (lista de acciones). Falla si algún step contiene 'FAIL'."
),
"difficulty_tier": 3, "difficulty": "hard",
"sector_id": 20, "codex_id": "qa_senior_architect",
"level_order": 40, "base_xp_reward": 500,
"is_project": True, "is_phase_boss": True,
"telemetry_goal_time": 420, "challenge_type": "python",
"phase": "automatizacion_e2e", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["suite_e2e", "integracion", "POM", "reporting"]),
"initial_code": (
    "class E2ESuite:\n"
    "    def __init__(self, name: str):\n"
    "        self.name = name\n"
    "        self._tests = []\n"
    "\n"
    "    def add_test(self, test_name: str, steps: list):\n"
    "        # TODO: agrega {'name': test_name, 'steps': steps} a self._tests\n"
    "        pass\n"
    "\n"
    "    def run_all(self) -> dict:\n"
    "        # TODO: ejecuta cada test. Un test falla si CUALQUIER step contiene 'FAIL'\n"
    "        # Para cada step imprime: 'Running: {step}'\n"
    "        # Si el test falla: imprime 'FAIL: {test_name}'\n"
    "        # Si el test pasa: imprime 'PASS: {test_name}'\n"
    "        # Retorna {'passed': int, 'failed': int, 'total': int}\n"
    "        pass\n"
    "\n"
    "    def report(self, results: dict) -> str:\n"
    "        # TODO: retorna reporte formateado:\n"
    "        # === {self.name} ===\n"
    "        # Passed: {n}  Failed: {n}  Total: {n}\n"
    "        # Status: SUITE PASS si failed==0, SUITE FAIL si no\n"
    "        pass\n"
    "\n"
    "\n"
    "suite = E2ESuite('Checkout Flow')\n"
    "suite.add_test('login_and_navigate', [\n"
    "    'navigate to /login',\n"
    "    'fill username',\n"
    "    'fill password',\n"
    "    'click submit',\n"
    "])\n"
    "suite.add_test('add_to_cart', [\n"
    "    'navigate to /products',\n"
    "    'click add-to-cart',\n"
    "    'FAIL: cart counter not updated',\n"
    "])\n"
    "suite.add_test('complete_checkout', [\n"
    "    'navigate to /checkout',\n"
    "    'fill payment details',\n"
    "    'click confirm',\n"
    "])\n"
    "results = suite.run_all()\n"
    "print(suite.report(results))\n"
),
"expected_output": (
    "Running: navigate to /login\n"
    "Running: fill username\n"
    "Running: fill password\n"
    "Running: click submit\n"
    "PASS: login_and_navigate\n"
    "Running: navigate to /products\n"
    "Running: click add-to-cart\n"
    "Running: FAIL: cart counter not updated\n"
    "FAIL: add_to_cart\n"
    "Running: navigate to /checkout\n"
    "Running: fill payment details\n"
    "Running: click confirm\n"
    "PASS: complete_checkout\n"
    "=== Checkout Flow ===\n"
    "Passed: 2  Failed: 1  Total: 3\n"
    "Status: SUITE FAIL"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Has dominado la automatización E2E. "
    "Este contrato integra POM, reporting, y lógica de suite en un solo sistema."
),
"theory_content": (
    "## Proyecto: Suite E2E Completa\n\n"
    "Integra los conceptos del Bloque 2:\n\n"
    "- **add_test**: registro de test cases con pasos\n"
    "- **run_all**: ejecución secuencial con detección de fallos\n"
    "- **report**: agregación de resultados y veredicto de suite\n\n"
    "**Regla de detección de fallo**: si cualquier step contiene 'FAIL', el test completo falla."
),
"pedagogical_objective": "Implementar una suite E2E completa con ejecución, detección de fallos y reporte.",
"syntax_hint": "Un test falla si `any('FAIL' in step for step in steps)`.",
"hints_json": json.dumps([
    "run_all: para cada test, imprime cada step, luego verifica any('FAIL' in s for s in test['steps']).",
    "report: f'=== {self.name} ===\\nPassed: {n}  Failed: {n}  Total: {n}\\nStatus: SUITE PASS/FAIL'",
    "El reporte solo se imprime una vez al final — run_all hace el print en tiempo real.",
]),
"grid_map_json": None,
},
]
