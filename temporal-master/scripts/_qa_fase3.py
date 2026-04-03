"""Fase 3 — Playwright Siege (L17-L27)"""
from __future__ import annotations
import json

FASE3 = [
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ AUTO-017: LOCATORS — ROLE, TEXT, TEST-ID ]",
"description": (
    "Implementa `getByRole(role)`, `getByText(text)` y `getByTestId(id)`. "
    "Cada función retorna un `new Locator` con la estrategia correcta: "
    "`'role'`, `'text'`, `'data-testid'` respectivamente."
),
"difficulty_tier": 1, "difficulty": "easy",
"sector_id": None, "codex_id": "qa_automation_ops",
"level_order": 17, "base_xp_reward": 160,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 200, "challenge_type": "typescript",
"phase": "CHARLIE", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["Playwright", "locators", "getByRole", "getByTestId", "selectores"]),
"initial_code": (
    "class Locator {\n"
    "    constructor(private strategy: string, private value: string) {}\n"
    "\n"
    "    toString(): string {\n"
    "        return `${this.strategy}=${this.value}`;\n"
    "    }\n"
    "\n"
    "    async click(): Promise<void> {\n"
    "        console.log(`click(${this})`);\n"
    "    }\n"
    "\n"
    "    async fill(text: string): Promise<void> {\n"
    "        console.log(`fill(${this}, \"${text}\")`);\n"
    "    }\n"
    "}\n"
    "\n"
    "\n"
    "function getByRole(role: string): Locator {\n"
    "    // TODO: retorna new Locator('role', role)\n"
    "    return new Locator('', '');\n"
    "}\n"
    "\n"
    "function getByText(text: string): Locator {\n"
    "    // TODO: retorna new Locator('text', text)\n"
    "    return new Locator('', '');\n"
    "}\n"
    "\n"
    "function getByTestId(id: string): Locator {\n"
    "    // TODO: retorna new Locator('data-testid', id)\n"
    "    return new Locator('', '');\n"
    "}\n"
    "\n"
    "\n"
    "async function main() {\n"
    "    const loginBtn = getByRole('button');\n"
    "    const heading  = getByText('Bienvenido al Nexo');\n"
    "    const input    = getByTestId('email-input');\n"
    "\n"
    "    console.log(loginBtn.toString());\n"
    "    console.log(heading.toString());\n"
    "    console.log(input.toString());\n"
    "\n"
    "    await input.fill('op@daki.io');\n"
    "    await loginBtn.click();\n"
    "}\n"
    "\n"
    "main();\n"
),
"expected_output": (
    "role=button\n"
    "text=Bienvenido al Nexo\n"
    "data-testid=email-input\n"
    'fill(data-testid=email-input, "op@daki.io")\n'
    "click(role=button)"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Playwright eliminó los selectores CSS frágiles. "
    "`getByRole`, `getByText` y `getByTestId` son selectores semánticos — "
    "resisten cambios de diseño porque seleccionan por significado, no por estructura."
),
"theory_content": (
    "## Locators de Playwright — Por qué importan\n\n"
    "```typescript\n"
    "// Frágil — se rompe si cambia el CSS\n"
    "page.locator('.btn-primary > span.label')\n\n"
    "// Robusto — selecciona por rol semántico\n"
    "page.getByRole('button', { name: 'Enviar' })\n\n"
    "// Más robusto — atributo de test explícito\n"
    "page.getByTestId('submit-button')  // <button data-testid='submit-button'>\n"
    "```\n\n"
    "**Orden de preferencia en Playwright:**\n"
    "1. `getByRole` (accesibilidad)\n"
    "2. `getByTestId` (contrato explícito con el equipo de frontend)\n"
    "3. `getByText` (visible al usuario)\n"
    "4. CSS/XPath (último recurso)"
),
"pedagogical_objective": "Entender la jerarquía de locators de Playwright y construir el patrón base.",
"syntax_hint": "`return new Locator('role', role)` — cambia la estrategia según la función.",
"hints_json": json.dumps([
    "getByRole: `return new Locator('role', role)`",
    "getByText: `return new Locator('text', text)`",
    "getByTestId: `return new Locator('data-testid', id)`",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ AUTO-018: PAGE OBJECT MODEL CON PLAYWRIGHT ]",
"description": (
    "Implementa `DashboardPage` con:\n"
    "- `constructor(page)`: guarda la referencia\n"
    "- `navigate()`: llama `page.goto('/dashboard')`\n"
    "- `getTitle()`: retorna `'Dashboard \u2014 Nexo Protocol'`\n"
    "- `clickLogout()`: llama `page.click('#logout-btn')`\n"
    "- `fillSearch(query)`: llama `page.fill('#search-input', query)`\n"
    "- `describe()`: imprime `'Page: /dashboard'` y `'Actions: clickLogout, fillSearch, getTitle, navigate'`"
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": None, "codex_id": "qa_automation_ops",
"level_order": 18, "base_xp_reward": 180,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 230, "challenge_type": "typescript",
"phase": "CHARLIE", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["Page Object Model", "Playwright", "encapsulación", "OOP"]),
"initial_code": (
    "interface MockPage {\n"
    "    goto:  (url: string) => Promise<void>;\n"
    "    fill:  (selector: string, value: string) => Promise<void>;\n"
    "    click: (selector: string) => Promise<void>;\n"
    "}\n"
    "\n"
    "\n"
    "class DashboardPage {\n"
    "    // TODO: guarda la referencia a page\n"
    "\n"
    "    constructor(page: MockPage) {\n"
    "        // COMPLETAR\n"
    "    }\n"
    "\n"
    "    async navigate(): Promise<void> {\n"
    "        // TODO: llama this.page.goto('/dashboard')\n"
    "    }\n"
    "\n"
    "    getTitle(): string {\n"
    "        // TODO: retorna 'Dashboard \u2014 Nexo Protocol'\n"
    "        return '';\n"
    "    }\n"
    "\n"
    "    async clickLogout(): Promise<void> {\n"
    "        // TODO: llama this.page.click('#logout-btn')\n"
    "    }\n"
    "\n"
    "    async fillSearch(query: string): Promise<void> {\n"
    "        // TODO: llama this.page.fill('#search-input', query)\n"
    "    }\n"
    "\n"
    "    describe(): void {\n"
    "        // TODO: imprime 'Page: /dashboard'\n"
    "        // TODO: imprime 'Actions: clickLogout, fillSearch, getTitle, navigate'\n"
    "    }\n"
    "}\n"
    "\n"
    "\n"
    "const mockPage: MockPage = {\n"
    "    goto:  async (url)       => console.log(`GOTO: ${url}`),\n"
    "    fill:  async (sel, val)  => console.log(`FILL: ${sel} = \"${val}\"`),\n"
    "    click: async (sel)       => console.log(`CLICK: ${sel}`),\n"
    "};\n"
    "\n"
    "async function main() {\n"
    "    const dashboard = new DashboardPage(mockPage);\n"
    "    dashboard.describe();\n"
    "    await dashboard.navigate();\n"
    "    await dashboard.fillSearch('pytest');\n"
    "    console.log(`Title: ${dashboard.getTitle()}`);\n"
    "    await dashboard.clickLogout();\n"
    "}\n"
    "\n"
    "main();\n"
),
"expected_output": (
    "Page: /dashboard\n"
    "Actions: clickLogout, fillSearch, getTitle, navigate\n"
    "GOTO: /dashboard\n"
    'FILL: #search-input = "pytest"\n'
    "Title: Dashboard \u2014 Nexo Protocol\n"
    "CLICK: #logout-btn"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Sin POM, cada test repite los mismos selectores. "
    "Cuando el frontend cambia `#logout-btn` a `#sign-out-btn`, caen 30 tests. "
    "Con POM, cambias un solo lugar y todos los tests siguen funcionando."
),
"theory_content": (
    "## Page Object Model — El patrón central de Playwright\n\n"
    "```typescript\n"
    "class LoginPage {\n"
    "    constructor(private page: Page) {}\n\n"
    "    async goto() { await this.page.goto('/login'); }\n"
    "    async login(email: string, password: string) {\n"
    "        await this.page.fill('#email', email);\n"
    "        await this.page.fill('#password', password);\n"
    "        await this.page.click('#submit');\n"
    "    }\n"
    "}\n\n"
    "// En el test:\n"
    "const loginPage = new LoginPage(page);\n"
    "await loginPage.goto();\n"
    "await loginPage.login('user@test.io', 'pass');\n"
    "```\n\n"
    "El test describe el flujo en términos de negocio, no de selectores."
),
"pedagogical_objective": "Implementar POM con Playwright — el patrón más solicitado en entrevistas QA.",
"syntax_hint": "En constructor: `this.page = page` (declara `private page: MockPage` en la clase).",
"hints_json": json.dumps([
    "Declara `private page: MockPage;` en la clase, luego `this.page = page;` en el constructor.",
    "navigate: `await this.page.goto('/dashboard')` — fillSearch: `await this.page.fill('#search-input', query)`",
    "describe: `console.log('Page: /dashboard'); console.log('Actions: clickLogout, fillSearch, getTitle, navigate')`",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ AUTO-019: FIXTURES DE PLAYWRIGHT — AUTH CONTEXT ]",
"description": (
    "Implementa `createAuthFixture()` que simula el proceso de autenticación y retorna un `TestContext`. "
    "Implementa `runWithFixture(fixtureFn, testFn)` que crea el contexto, ejecuta el test "
    "y en el bloque `finally` ejecuta todos los cleanups en orden inverso."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": None, "codex_id": "qa_automation_ops",
"level_order": 19, "base_xp_reward": 190,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "typescript",
"phase": "CHARLIE", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["fixtures", "auth_context", "cleanup", "finally", "Playwright"]),
"initial_code": (
    "interface TestContext {\n"
    "    url:     string;\n"
    "    user:    { email: string; token: string };\n"
    "    cleanup: Array<() => Promise<void>>;\n"
    "}\n"
    "\n"
    "\n"
    "async function createAuthFixture(): Promise<TestContext> {\n"
    "    // TODO:\n"
    "    // 1. Imprime 'AUTH: logging in as operator@daki.io'\n"
    "    // 2. Imprime 'AUTH: token acquired'\n"
    "    // 3. Retorna TestContext con:\n"
    "    //    url: 'https://app.daki.io'\n"
    "    //    user: { email: 'operator@daki.io', token: 'jwt-nexo-001' }\n"
    "    //    cleanup: [función que imprime 'AUTH: token revoked']\n"
    "    return {} as TestContext;\n"
    "}\n"
    "\n"
    "\n"
    "async function runWithFixture(\n"
    "    fixtureFn: () => Promise<TestContext>,\n"
    "    testFn: (ctx: TestContext) => Promise<void>\n"
    "): Promise<void> {\n"
    "    // TODO:\n"
    "    // 1. const ctx = await fixtureFn()\n"
    "    // 2. try { await testFn(ctx) }\n"
    "    // 3. finally { ejecuta ctx.cleanup en orden INVERSO }\n"
    "}\n"
    "\n"
    "\n"
    "runWithFixture(createAuthFixture, async (ctx) => {\n"
    "    console.log(`TEST: navigating to ${ctx.url}`);\n"
    "    console.log(`TEST: user=${ctx.user.email} token=${ctx.user.token}`);\n"
    "    console.log('TEST: assertions passed');\n"
    "});\n"
),
"expected_output": (
    "AUTH: logging in as operator@daki.io\n"
    "AUTH: token acquired\n"
    "TEST: navigating to https://app.daki.io\n"
    "TEST: user=operator@daki.io token=jwt-nexo-001\n"
    "TEST: assertions passed\n"
    "AUTH: token revoked"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Playwright tiene un sistema de fixtures similar a pytest: "
    "el fixture prepara el contexto (login, cookies, estado), "
    "el test lo usa, y el cleanup siempre se ejecuta — incluso si el test falla."
),
"theory_content": (
    "## Fixtures en Playwright\n\n"
    "```typescript\n"
    "// playwright.config.ts\n"
    "const test = base.extend<{ authPage: Page }>({\n"
    "    authPage: async ({ page }, use) => {\n"
    "        await page.goto('/login');\n"
    "        await page.fill('#email', 'user@test.io');\n"
    "        await page.click('#submit');\n"
    "        await use(page);  // el test recibe la page autenticada\n"
    "        // teardown automático al salir\n"
    "    },\n"
    "});\n"
    "```\n\n"
    "El patrón es idéntico al `yield` de pytest.\n\n"
    "**`finally`** — se ejecuta siempre, independientemente de si el try lanzó error."
),
"pedagogical_objective": "Implementar el ciclo fixture setup/use/teardown para autenticación en Playwright.",
"syntax_hint": "En finally: `for (const fn of [...ctx.cleanup].reverse()) { await fn(); }`",
"hints_json": json.dumps([
    "createAuthFixture: imprime los 2 mensajes de AUTH, luego retorna el contexto con cleanup = [async () => console.log('AUTH: token revoked')]",
    "runWithFixture: `const ctx = await fixtureFn(); try { await testFn(ctx); } finally { for (const fn of [...ctx.cleanup].reverse()) await fn(); }`",
    "`.reverse()` en orden inverso es el patrón estándar para cleanup de múltiples recursos.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ AUTO-020: ASSERTIONS DE PLAYWRIGHT — EXPECT API ]",
"description": (
    "Implementa los métodos de `PlaywrightExpect`:\n"
    "- `toBe(expected)`: verifica igualdad estricta\n"
    "- `toContain(expected)`: verifica que string o array contiene el valor\n"
    "- `toHaveLength(n)`: verifica la longitud\n"
    "Formato PASS: `'PASS: <método>(<expected>)'`. "
    "Formato FAIL: `'FAIL: <método> expected=<exp> got=<actual>'` (o variante según método)."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": None, "codex_id": "qa_automation_ops",
"level_order": 20, "base_xp_reward": 185,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 235, "challenge_type": "typescript",
"phase": "CHARLIE", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["expect", "assertions", "Playwright", "fluent_API"]),
"initial_code": (
    "class PlaywrightExpect {\n"
    "    constructor(private actual: unknown) {}\n"
    "\n"
    "    toBe(expected: unknown): void {\n"
    "        // TODO: si actual === expected: 'PASS: toBe(<expected>)'\n"
    "        // si no: 'FAIL: toBe expected=<expected> got=<actual>'\n"
    "    }\n"
    "\n"
    "    toContain(expected: string): void {\n"
    "        // TODO: verifica que this.actual (string o array) contiene expected\n"
    "        // PASS: 'PASS: toContain(<expected>)'\n"
    "        // FAIL: 'FAIL: toContain(<expected>) not found in <actual>'\n"
    "    }\n"
    "\n"
    "    toHaveLength(n: number): void {\n"
    "        // TODO: verifica que (this.actual as any).length === n\n"
    "        // PASS: 'PASS: toHaveLength(<n>)'\n"
    "        // FAIL: 'FAIL: toHaveLength expected=<n> got=<actual.length>'\n"
    "    }\n"
    "}\n"
    "\n"
    "function expect(value: unknown): PlaywrightExpect {\n"
    "    return new PlaywrightExpect(value);\n"
    "}\n"
    "\n"
    "\n"
    "expect('https://app.daki.io/dashboard').toContain('/dashboard');\n"
    "expect('https://app.daki.io/login').toBe('https://app.daki.io/login');\n"
    "expect(['READ', 'WRITE', 'ADMIN']).toHaveLength(3);\n"
    "expect(200).toBe(200);\n"
    "expect(['READ']).toHaveLength(2);\n"
    "expect('welcome page').toContain('error');\n"
),
"expected_output": (
    "PASS: toContain(/dashboard)\n"
    "PASS: toBe(https://app.daki.io/login)\n"
    "PASS: toHaveLength(3)\n"
    "PASS: toBe(200)\n"
    "FAIL: toHaveLength expected=2 got=1\n"
    "FAIL: toContain(error) not found in welcome page"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Las assertions de Playwright son más que `assert`. "
    "Esperan automáticamente que la condición se cumpla (auto-wait). "
    "Aquí implementamos la API de mensajes para entender exactamente qué valida cada método."
),
"theory_content": (
    "## expect() de Playwright — Auto-wait y matchers\n\n"
    "```typescript\n"
    "// Playwright real:\n"
    "await expect(page).toHaveURL('/dashboard');  // espera hasta 5s\n"
    "await expect(locator).toBeVisible();         // espera que el elemento aparezca\n"
    "await expect(locator).toHaveText('Hola');    // espera el texto exacto\n"
    "```\n\n"
    "**Para datos (no DOM):**\n"
    "```typescript\n"
    "expect(response.status()).toBe(200);\n"
    "expect(body).toMatchObject({ ok: true });\n"
    "```\n\n"
    "El formato de los mensajes de error es clave para debuggear fallas rápidamente."
),
"pedagogical_objective": "Construir la API de assertions — entiende el contrato que todo matcher debe cumplir.",
"syntax_hint": "toContain: `const includes = Array.isArray(this.actual) ? (this.actual as string[]).includes(expected) : (this.actual as string).includes(expected);`",
"hints_json": json.dumps([
    "toBe: `if (this.actual === expected) console.log(\\`PASS: toBe(${expected})\\`); else console.log(\\`FAIL: toBe expected=${expected} got=${this.actual}\\`)`",
    "toContain: usa `Array.isArray(this.actual)` para ramificar entre array y string, luego `.includes(expected)`",
    "toHaveLength: `const len = (this.actual as any).length; if (len === n) ... else console.log(\\`FAIL: toHaveLength expected=${n} got=${len}\\`)`",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ AUTO-021: API TESTING CON APIREQUESTCONTEXT ]",
"description": (
    "Implementa `APIRequestContext.get(path)` y `post(path, data)` que buscan la respuesta "
    "en `this._routes` con la clave `'METHOD /path'` y retornan un objeto `Response` simulado. "
    "`Response` tiene: `status()`, `json()` (async), `ok()` (status < 400)."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": None, "codex_id": "qa_automation_ops",
"level_order": 21, "base_xp_reward": 190,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "typescript",
"phase": "CHARLIE", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["APIRequestContext", "Playwright", "API_testing", "Response"]),
"initial_code": (
    "interface Response {\n"
    "    status:  () => number;\n"
    "    json:    () => Promise<unknown>;\n"
    "    ok:      () => boolean;\n"
    "}\n"
    "\n"
    "function makeResponse(statusCode: number, body: unknown): Response {\n"
    "    return {\n"
    "        status: () => statusCode,\n"
    "        json:   async () => body,\n"
    "        ok:     () => statusCode < 400,\n"
    "    };\n"
    "}\n"
    "\n"
    "\n"
    "class APIRequestContext {\n"
    "    private _routes = new Map<string, { status: number; body: unknown }>([\n"
    "        ['GET /api/users',      { status: 200, body: [{ id: 1, name: 'Alice' }] }],\n"
    "        ['POST /api/users',     { status: 201, body: { id: 2, name: 'Bob' }    }],\n"
    "        ['DELETE /api/users/1', { status: 204, body: null                       }],\n"
    "        ['GET /api/protected',  { status: 401, body: { error: 'Unauthorized' }  }],\n"
    "    ]);\n"
    "\n"
    "    async get(path: string): Promise<Response> {\n"
    "        // TODO: busca 'GET {path}' en _routes y retorna makeResponse(status, body)\n"
    "        // Si no existe: makeResponse(404, { error: 'Not found' })\n"
    "        return makeResponse(404, {});\n"
    "    }\n"
    "\n"
    "    async post(path: string, _data: unknown): Promise<Response> {\n"
    "        // TODO: igual pero con 'POST {path}'\n"
    "        return makeResponse(404, {});\n"
    "    }\n"
    "\n"
    "    async delete(path: string): Promise<Response> {\n"
    "        const route = this._routes.get(`DELETE ${path}`);\n"
    "        return route ? makeResponse(route.status, route.body) : makeResponse(404, { error: 'Not found' });\n"
    "    }\n"
    "}\n"
    "\n"
    "\n"
    "async function main() {\n"
    "    const request = new APIRequestContext();\n"
    "\n"
    "    const getResp = await request.get('/api/users');\n"
    "    console.log(`GET /api/users \u2192 ${getResp.status()} ok=${getResp.ok()}`);\n"
    "\n"
    "    const postResp  = await request.post('/api/users', { name: 'Bob' });\n"
    "    const created   = await postResp.json() as { id: number; name: string };\n"
    "    console.log(`POST /api/users \u2192 ${postResp.status()} id=${created.id}`);\n"
    "\n"
    "    const delResp = await request.delete('/api/users/1');\n"
    "    console.log(`DELETE /api/users/1 \u2192 ${delResp.status()}`);\n"
    "\n"
    "    const authResp = await request.get('/api/protected');\n"
    "    console.log(`GET /api/protected \u2192 ${authResp.status()} ok=${authResp.ok()}`);\n"
    "}\n"
    "\n"
    "main();\n"
),
"expected_output": (
    "GET /api/users \u2192 200 ok=true\n"
    "POST /api/users \u2192 201 id=2\n"
    "DELETE /api/users/1 \u2192 204\n"
    "GET /api/protected \u2192 401 ok=false"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Playwright no es solo E2E. `APIRequestContext` permite testear la API "
    "desde el mismo proceso que los tests E2E, con las mismas cookies y headers. "
    "Es la herramienta perfecta para setup/teardown de tests que requieren estado en el servidor."
),
"theory_content": (
    "## APIRequestContext en Playwright real\n\n"
    "```typescript\n"
    "test('GET /api/users retorna lista', async ({ request }) => {\n"
    "    const response = await request.get('/api/users', {\n"
    "        headers: { Authorization: `Bearer ${token}` }\n"
    "    });\n"
    "    expect(response.status()).toBe(200);\n"
    "    const body = await response.json();\n"
    "    expect(body).toHaveLength(3);\n"
    "});\n"
    "```\n\n"
    "El `request` fixture en Playwright comparte las cookies de la sesión del browser — "
    "no necesitas re-autenticar para los tests de API."
),
"pedagogical_objective": "Entender APIRequestContext — usar Playwright como herramienta de API testing.",
"syntax_hint": "`const route = this._routes.get(\\`GET ${path}\\`); return route ? makeResponse(route.status, route.body) : makeResponse(404, { error: 'Not found' });`",
"hints_json": json.dumps([
    "get: `const route = this._routes.get(\\`GET ${path}\\`); return route ? makeResponse(route.status, route.body) : makeResponse(404, { error: 'Not found' });`",
    "post: igual pero con `\\`POST ${path}\\``",
    "ok() retorna `statusCode < 400` — 204 es OK (< 400), por eso DELETE no imprime ok=.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ AUTO-022: NETWORK INTERCEPTION — ROUTE.FULFILL ]",
"description": (
    "Implementa `RouteInterceptor.route(pattern, handler)` que registra el handler "
    "(convirtiendo string a RegExp si es necesario). "
    "Implementa `intercept(url, method)` que recorre los handlers y retorna el primer match, "
    "o null si ninguno coincide."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": None, "codex_id": "qa_automation_ops",
"level_order": 22, "base_xp_reward": 195,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 245, "challenge_type": "typescript",
"phase": "CHARLIE", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["network_interception", "RegExp", "route.fulfill", "mocking_network"]),
"initial_code": (
    "type Handler = (url: string, method: string) => { status: number; body: unknown } | null;\n"
    "\n"
    "class RouteInterceptor {\n"
    "    private handlers: Array<{ pattern: RegExp; handler: Handler }> = [];\n"
    "\n"
    "    route(pattern: string | RegExp, handler: Handler): void {\n"
    "        // TODO: convierte pattern a RegExp si es string (new RegExp(pattern))\n"
    "        // luego agrega { pattern, handler } a this.handlers\n"
    "    }\n"
    "\n"
    "    intercept(url: string, method: string): { status: number; body: unknown } | null {\n"
    "        // TODO: recorre this.handlers en orden\n"
    "        // Si handler.pattern.test(url) → llama handler(url, method)\n"
    "        // Si retorna no-null → retórnalo\n"
    "        // Si ninguno hace match → retorna null\n"
    "        return null;\n"
    "    }\n"
    "\n"
    "    describe(): void {\n"
    "        console.log(`Interceptor: ${this.handlers.length} rules registered`);\n"
    "    }\n"
    "}\n"
    "\n"
    "\n"
    "const interceptor = new RouteInterceptor();\n"
    "\n"
    "interceptor.route('/api/auth', (url, method) => {\n"
    "    if (method === 'POST') return { status: 200, body: { token: 'mock-jwt' } };\n"
    "    return null;\n"
    "});\n"
    "\n"
    "interceptor.route(/\\/api\\/users\\/\\d+/, () => {\n"
    "    return { status: 200, body: { id: 1, name: 'Mocked User' } };\n"
    "});\n"
    "\n"
    "interceptor.describe();\n"
    "\n"
    "const tests = [\n"
    "    { url: '/api/auth',     method: 'POST' },\n"
    "    { url: '/api/auth',     method: 'GET'  },\n"
    "    { url: '/api/users/42', method: 'GET'  },\n"
    "    { url: '/api/other',    method: 'GET'  },\n"
    "];\n"
    "\n"
    "for (const { url, method } of tests) {\n"
    "    const result = interceptor.intercept(url, method);\n"
    "    if (result) {\n"
    "        console.log(`${method} ${url} \u2192 intercepted ${result.status}`);\n"
    "    } else {\n"
    "        console.log(`${method} ${url} \u2192 pass-through`);\n"
    "    }\n"
    "}\n"
),
"expected_output": (
    "Interceptor: 2 rules registered\n"
    "POST /api/auth \u2192 intercepted 200\n"
    "GET /api/auth \u2192 pass-through\n"
    "GET /api/users/42 \u2192 intercepted 200\n"
    "GET /api/other \u2192 pass-through"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Network interception es el superpoder de Playwright. "
    "Puedes interceptar cualquier request y retornar lo que quieras — "
    "simular errores de red, respuestas lentas, datos falsos — sin modificar el servidor."
),
"theory_content": (
    "## route.fulfill() en Playwright real\n\n"
    "```typescript\n"
    "await page.route('/api/auth', async route => {\n"
    "    await route.fulfill({\n"
    "        status: 200,\n"
    "        body: JSON.stringify({ token: 'mock-jwt' }),\n"
    "    });\n"
    "});\n"
    "```\n\n"
    "Playwright intercepta la request antes de que salga a la red y responde con el mock.\n\n"
    "**Casos de uso:**\n"
    "- Simular errores de red (status 500, 503)\n"
    "- Testear manejo de respuestas lentas\n"
    "- Testear el frontend sin backend real"
),
"pedagogical_objective": "Implementar network interception con RegExp — base del mocking de red en Playwright.",
"syntax_hint": "route: `const re = typeof pattern === 'string' ? new RegExp(pattern) : pattern; this.handlers.push({ pattern: re, handler });`",
"hints_json": json.dumps([
    "route: `const re = typeof pattern === 'string' ? new RegExp(pattern) : pattern; this.handlers.push({ pattern: re, handler });`",
    "intercept: `for (const { pattern, handler } of this.handlers) { if (pattern.test(url)) { const result = handler(url, method); if (result !== null) return result; } } return null;`",
    "La RegExp `/\\/api\\/users\\/\\d+/` matchea '/api/users/42' porque \\d+ es uno o más dígitos.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ AUTO-023: VISUAL TESTING — SCREENSHOT COMPARATOR ]",
"description": (
    "Implementa `ScreenshotComparator.captureBaseline(name, content)` que guarda el contenido "
    "en el mapa e imprime `'BASELINE saved: <name>'`. "
    "Implementa `compare(name, current)` que calcula la similitud char-a-char: "
    "`similarity = round(1 - changedChars / max(len(baseline), len(current)), 2)`, "
    "`changedRegions = ceil(changedChars / 10)`. Si no hay baseline, imprime el error."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": None, "codex_id": "qa_automation_ops",
"level_order": 23, "base_xp_reward": 190,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 245, "challenge_type": "typescript",
"phase": "CHARLIE", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["visual_testing", "screenshot", "comparación", "similitud"]),
"initial_code": (
    "interface VisualDiff {\n"
    "    hasChanges:     boolean;\n"
    "    changedRegions: number;\n"
    "    similarity:     number;\n"
    "}\n"
    "\n"
    "class ScreenshotComparator {\n"
    "    private _baseline = new Map<string, string>();\n"
    "\n"
    "    captureBaseline(name: string, content: string): void {\n"
    "        // TODO: guarda content en _baseline con key=name\n"
    "        // Imprime: 'BASELINE saved: <name>'\n"
    "    }\n"
    "\n"
    "    compare(name: string, current: string): VisualDiff {\n"
    "        // TODO:\n"
    "        // Si no hay baseline para name: imprime 'ERROR: no baseline for <name>'\n"
    "        //   y retorna { hasChanges: false, changedRegions: 0, similarity: 0 }\n"
    "        // Cuenta chars distintos comparando baseline[i] vs current[i]\n"
    "        // similarity = Math.round((1 - changed/maxLen) * 100) / 100\n"
    "        // changedRegions = Math.ceil(changed / 10)\n"
    "        // hasChanges = changed > 0\n"
    "        return { hasChanges: false, changedRegions: 0, similarity: 1 };\n"
    "    }\n"
    "}\n"
    "\n"
    "\n"
    "const comparator = new ScreenshotComparator();\n"
    "\n"
    "comparator.captureBaseline('login_page',  'AAABBBCCC');\n"
    "comparator.captureBaseline('dashboard',   'XXXXXXXXXXX');\n"
    "\n"
    "const diff1 = comparator.compare('login_page', 'AAABBBCCC');\n"
    "const diff2 = comparator.compare('login_page', 'AAAXBBCCC');\n"
    "comparator.compare('unknown_page', 'ABC');\n"
    "\n"
    "console.log(`diff1: changes=${diff1.hasChanges} regions=${diff1.changedRegions} sim=${diff1.similarity}`);\n"
    "console.log(`diff2: changes=${diff2.hasChanges} regions=${diff2.changedRegions} sim=${diff2.similarity}`);\n"
),
"expected_output": (
    "BASELINE saved: login_page\n"
    "BASELINE saved: dashboard\n"
    "ERROR: no baseline for unknown_page\n"
    "diff1: changes=false regions=0 sim=1\n"
    "diff2: changes=true regions=1 sim=0.89"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Los tests visuales detectan regresiones que los tests funcionales no ven: "
    "un botón que se movió 3px, un color que cambió, un texto que se truncó. "
    "La comparación pixel-a-pixel (aquí simplificada a char-a-char) es el corazón del visual testing."
),
"theory_content": (
    "## Visual Testing — Cómo funciona\n\n"
    "Playwright tiene `expect(page).toHaveScreenshot()` que:\n"
    "1. Primera ejecución: guarda el screenshot como baseline\n"
    "2. Ejecuciones siguientes: compara con el baseline\n"
    "3. Si hay diferencias: falla y genera un diff visual\n\n"
    "```typescript\n"
    "await expect(page).toHaveScreenshot('login.png', {\n"
    "    maxDiffPixelRatio: 0.01  // tolera hasta 1% de diferencia\n"
    "});\n"
    "```\n\n"
    "**similarity = 1 - changed/total** — si todos los chars son iguales: similarity = 1.0 (100%)"
),
"pedagogical_objective": "Entender el algoritmo de comparación visual — base del visual regression testing.",
"syntax_hint": "Para contar chars distintos: `let changed = 0; for (let i = 0; i < Math.max(base.length, current.length); i++) { if (base[i] !== current[i]) changed++; }`",
"hints_json": json.dumps([
    "captureBaseline: `this._baseline.set(name, content); console.log(\\`BASELINE saved: ${name}\\`)`",
    "compare: verifica con `this._baseline.has(name)`, si no: imprime ERROR y retorna diff vacío.",
    "Para similitud: `const maxLen = Math.max(baseline.length, current.length); const sim = Math.round((1 - changed / maxLen) * 100) / 100;`",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ AUTO-024: MULTI-BROWSER — MATRIX DE CONFIGURACIÓN ]",
"description": (
    "Implementa `buildBrowserMatrix(browsers, includeMobile)` que retorna un array de `BrowserConfig`. "
    "Para cada browser: viewport desktop `{width:1280, height:720}`, `isMobile:false`. "
    "Si `includeMobile===true`, agrega al final una entrada de Chromium mobile: "
    "`viewport:{width:375, height:667}`, `isMobile:true`, `channel:'mobile'`."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": None, "codex_id": "qa_automation_ops",
"level_order": 24, "base_xp_reward": 185,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 235, "challenge_type": "typescript",
"phase": "CHARLIE", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["multi_browser", "cross_browser", "mobile_testing", "matrix"]),
"initial_code": (
    "type Browser = 'chromium' | 'firefox' | 'webkit';\n"
    "\n"
    "interface BrowserConfig {\n"
    "    name:      Browser;\n"
    "    channel?:  string;\n"
    "    viewport:  { width: number; height: number };\n"
    "    isMobile:  boolean;\n"
    "}\n"
    "\n"
    "\n"
    "function buildBrowserMatrix(browsers: Browser[], includeMobile: boolean): BrowserConfig[] {\n"
    "    // TODO:\n"
    "    // 1. Por cada browser: { name, viewport:{1280,720}, isMobile:false }\n"
    "    // 2. Si includeMobile: agrega { name:'chromium', channel:'mobile', viewport:{375,667}, isMobile:true }\n"
    "    return [];\n"
    "}\n"
    "\n"
    "\n"
    "const matrix = buildBrowserMatrix(['chromium', 'firefox', 'webkit'], true);\n"
    "\n"
    "matrix.forEach(config => {\n"
    "    const device = config.isMobile ? 'mobile' : 'desktop';\n"
    "    console.log(`${config.name} [${device}] ${config.viewport.width}x${config.viewport.height}`);\n"
    "});\n"
    "console.log(`Matrix size: ${matrix.length}`);\n"
),
"expected_output": (
    "chromium [desktop] 1280x720\n"
    "firefox [desktop] 1280x720\n"
    "webkit [desktop] 1280x720\n"
    "chromium [mobile] 375x667\n"
    "Matrix size: 4"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Un test que solo corre en Chrome es un test incompleto. "
    "La matrix de browsers es la diferencia entre 'funciona en mi máquina' "
    "y 'funciona en producción para todos los usuarios'."
),
"theory_content": (
    "## playwright.config.ts — Matrix de browsers\n\n"
    "```typescript\n"
    "// playwright.config.ts\n"
    "export default defineConfig({\n"
    "    projects: [\n"
    "        { name: 'chromium', use: { ...devices['Desktop Chrome'] } },\n"
    "        { name: 'firefox',  use: { ...devices['Desktop Firefox'] } },\n"
    "        { name: 'webkit',   use: { ...devices['Desktop Safari'] } },\n"
    "        { name: 'mobile',   use: { ...devices['iPhone 12'] } },\n"
    "    ],\n"
    "});\n"
    "```\n\n"
    "Playwright corre todos los tests en todos los browsers en paralelo. "
    "El reporte muestra qué browser falló y cuál pasó."
),
"pedagogical_objective": "Configurar una matrix de browsers para cross-browser testing — práctica estándar en CI.",
"syntax_hint": "Para el mobile: `if (includeMobile) matrix.push({ name: 'chromium', channel: 'mobile', viewport: { width: 375, height: 667 }, isMobile: true });`",
"hints_json": json.dumps([
    "Primero mapea: `const matrix = browsers.map(name => ({ name, viewport: { width: 1280, height: 720 }, isMobile: false }));`",
    "Luego: `if (includeMobile) matrix.push({ name: 'chromium', channel: 'mobile', viewport: { width: 375, height: 667 }, isMobile: true });`",
    "Retorna el array al final: `return matrix;`",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ AUTO-025: PARALLEL EXECUTION — DISTRIBUCIÓN DE WORKERS ]",
"description": (
    "Implementa `distributeWork(tasks, workerCount)` que distribuye los tasks "
    "entre `workerCount` workers usando round-robin (T1→W1, T2→W2, T3→W3, T4→W1...). "
    "Retorna un array de arrays, uno por worker."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": None, "codex_id": "qa_automation_ops",
"level_order": 25, "base_xp_reward": 188,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 240, "challenge_type": "typescript",
"phase": "CHARLIE", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["parallel_execution", "workers", "sharding", "round_robin"]),
"initial_code": (
    "interface WorkerTask {\n"
    "    id:     string;\n"
    "    suite:  string;\n"
    "    tests:  string[];\n"
    "}\n"
    "\n"
    "\n"
    "function distributeWork(tasks: WorkerTask[], workerCount: number): WorkerTask[][] {\n"
    "    // TODO: crea workerCount arrays vacíos\n"
    "    // Distribuye tasks en round-robin: tasks[i] → workers[i % workerCount]\n"
    "    return [];\n"
    "}\n"
    "\n"
    "\n"
    "const tasks: WorkerTask[] = [\n"
    "    { id: 'T1', suite: 'auth',      tests: ['login', 'logout']       },\n"
    "    { id: 'T2', suite: 'dashboard', tests: ['load', 'search']        },\n"
    "    { id: 'T3', suite: 'profile',   tests: ['edit']                  },\n"
    "    { id: 'T4', suite: 'billing',   tests: ['checkout', 'invoice']   },\n"
    "    { id: 'T5', suite: 'settings',  tests: ['toggle']                },\n"
    "];\n"
    "\n"
    "const distribution = distributeWork(tasks, 3);\n"
    "\n"
    "distribution.forEach((workerTasks, i) => {\n"
    "    const suites = workerTasks.map(t => t.suite).join(', ') || '(idle)';\n"
    "    console.log(`Worker ${i + 1}: ${suites}`);\n"
    "});\n"
    "console.log(`Total tasks distributed: ${distribution.flat().length}`);\n"
),
"expected_output": (
    "Worker 1: auth, billing\n"
    "Worker 2: dashboard, settings\n"
    "Worker 3: profile\n"
    "Total tasks distributed: 5"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Playwright puede correr tests en paralelo con múltiples workers. "
    "Una distribución eficiente reduce el tiempo total de la suite. "
    "Round-robin es la estrategia más simple — en producción se usa sharding con tiempo estimado."
),
"theory_content": (
    "## Parallel Execution en Playwright\n\n"
    "```typescript\n"
    "// playwright.config.ts\n"
    "export default defineConfig({\n"
    "    workers: process.env.CI ? 2 : 4,  // menos workers en CI\n"
    "    fullyParallel: true,               // tests dentro de un archivo en paralelo\n"
    "});\n"
    "```\n\n"
    "**Sharding para CI (distribución entre máquinas):**\n"
    "```bash\n"
    "npx playwright test --shard=1/3  # máquina 1 de 3\n"
    "npx playwright test --shard=2/3  # máquina 2 de 3\n"
    "npx playwright test --shard=3/3  # máquina 3 de 3\n"
    "```\n\n"
    "**Round-robin:** `tasks[i] → workers[i % workerCount]`"
),
"pedagogical_objective": "Implementar distribución round-robin de tests — entiende cómo Playwright paraleliza.",
"syntax_hint": "`const workers: WorkerTask[][] = Array.from({ length: workerCount }, () => []); tasks.forEach((task, i) => workers[i % workerCount].push(task)); return workers;`",
"hints_json": json.dumps([
    "Crea el array de workers: `const workers: WorkerTask[][] = Array.from({ length: workerCount }, () => []);`",
    "Distribuye: `tasks.forEach((task, i) => workers[i % workerCount].push(task));`",
    "Retorna: `return workers;`",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ AUTO-026: RETRY — MANEJO DE TESTS FLAKY ]",
"description": (
    "Implementa `runWithRetry(testFn, maxRetries, testName)` que ejecuta `testFn(attempt)` "
    "hasta `maxRetries` veces. Por cada intento imprime el resultado. "
    "Si alguno pasa: `'TEST PASSED: <name> (attempt <n>)'`. "
    "Si todos fallan: `'TEST FAILED: <name> (all <maxRetries> retries exhausted)'`."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": None, "codex_id": "qa_automation_ops",
"level_order": 26, "base_xp_reward": 192,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 245, "challenge_type": "typescript",
"phase": "CHARLIE", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["retry", "flaky_tests", "resilience", "test_stability"]),
"initial_code": (
    "function runWithRetry(\n"
    "    testFn: (attempt: number) => { pass: boolean; error?: string },\n"
    "    maxRetries: number,\n"
    "    testName: string\n"
    "): void {\n"
    "    // TODO: itera de 1 a maxRetries (inclusive)\n"
    "    // Llama testFn(i) y verifica result.pass\n"
    "    // PASS: imprime 'Attempt <i>/<max>: PASS' luego 'TEST PASSED: <name> (attempt <i>)' y retorna\n"
    "    // FAIL: imprime 'Attempt <i>/<max>: FAIL \u2014 <result.error>'\n"
    "    // Si agota todos los intentos: 'TEST FAILED: <name> (all <max> retries exhausted)'\n"
    "}\n"
    "\n"
    "\n"
    "// Test 1: falla los primeros 2 intentos, pasa al 3\n"
    "runWithRetry(\n"
    "    (attempt) => attempt < 3\n"
    "        ? { pass: false, error: 'Element not found' }\n"
    "        : { pass: true },\n"
    "    3,\n"
    "    'login_flow'\n"
    ");\n"
    "\n"
    "// Test 2: siempre falla\n"
    "runWithRetry(\n"
    "    (_attempt) => ({ pass: false, error: 'Timeout' }),\n"
    "    2,\n"
    "    'slow_test'\n"
    ");\n"
),
"expected_output": (
    "Attempt 1/3: FAIL \u2014 Element not found\n"
    "Attempt 2/3: FAIL \u2014 Element not found\n"
    "Attempt 3/3: PASS\n"
    "TEST PASSED: login_flow (attempt 3)\n"
    "Attempt 1/2: FAIL \u2014 Timeout\n"
    "Attempt 2/2: FAIL \u2014 Timeout\n"
    "TEST FAILED: slow_test (all 2 retries exhausted)"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Un test flaky falla el 10% de las veces sin razón aparente. "
    "El retry no arregla el problema raíz — pero evita que el pipeline caiga por ruido. "
    "Playwright tiene `retries: 2` en el config para exactamente esto."
),
"theory_content": (
    "## Retry en Playwright\n\n"
    "```typescript\n"
    "// playwright.config.ts\n"
    "export default defineConfig({\n"
    "    retries: process.env.CI ? 2 : 0,  // solo reintenta en CI\n"
    "});\n"
    "```\n\n"
    "**Cuándo usar retries:**\n"
    "- Tests E2E que dependen de timing de red\n"
    "- Animaciones CSS que pueden ser lentas\n"
    "- Servicios externos con latencia variable\n\n"
    "**Cuándo NO usar retries:**\n"
    "- Tests unitarios — si fallan, hay un bug real\n"
    "- Lógica de negocio — un retry que pasa puede enmascarar un bug"
),
"pedagogical_objective": "Implementar retry logic — entiende el tradeoff entre resiliencia y falsos positivos.",
"syntax_hint": "`for (let i = 1; i <= maxRetries; i++) { const result = testFn(i); if (result.pass) { console.log(...); return; } ... }`",
"hints_json": json.dumps([
    "Loop: `for (let i = 1; i <= maxRetries; i++) { const result = testFn(i); ... }`",
    "PASS: `console.log(\\`Attempt ${i}/${maxRetries}: PASS\\`); console.log(\\`TEST PASSED: ${testName} (attempt ${i})\\`); return;`",
    "FAIL en loop: `console.log(\\`Attempt ${i}/${maxRetries}: FAIL — ${result.error}\\`)` — después del loop: `console.log(\\`TEST FAILED: ${testName} (all ${maxRetries} retries exhausted)\\`)`",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ AUTO-027 \u221e BOSS: E2E RUNNER — SUITE COMPLETA LOGIN FLOW ]",
"description": (
    "Implementa `E2ERunner.addTest(test)` y `E2ERunner.runAll()`. "
    "`runAll()` ejecuta cada test imprimiendo `'▶ Running: <name>'`, cada step, el assert, "
    "y `'  ✓ PASS (<duration>ms)'` donde `duration = test.steps.length * 120`. "
    "Al final imprime el reporte con encabezado `'═══ <suiteName> ═══'`, "
    "lista de resultados y totales."
),
"difficulty_tier": 3, "difficulty": "hard",
"sector_id": None, "codex_id": "qa_automation_ops",
"level_order": 27, "base_xp_reward": 320,
"is_project": False, "is_phase_boss": True,
"telemetry_goal_time": 340, "challenge_type": "typescript",
"phase": "CHARLIE", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["E2E_runner", "test_suite", "Playwright", "reporting", "OOP"]),
"initial_code": (
    "interface E2ETest {\n"
    "    name:      string;\n"
    "    steps:     string[];\n"
    "    assertion: string;\n"
    "    result?:   'PASS' | 'FAIL';\n"
    "    duration?: number;\n"
    "}\n"
    "\n"
    "class E2ERunner {\n"
    "    private tests: E2ETest[] = [];\n"
    "    private suiteName: string;\n"
    "\n"
    "    constructor(name: string) {\n"
    "        this.suiteName = name;\n"
    "    }\n"
    "\n"
    "    addTest(test: E2ETest): void {\n"
    "        // TODO: agrega a this.tests\n"
    "    }\n"
    "\n"
    "    runAll(): void {\n"
    "        // TODO por cada test:\n"
    "        //   console.log(`\u25b6 Running: ${test.name}`)\n"
    "        //   Por cada step: console.log(`  Step: ${step}`)\n"
    "        //   console.log(`  Assert: ${test.assertion}`)\n"
    "        //   test.result = 'PASS'; test.duration = test.steps.length * 120\n"
    "        //   console.log(`  \u2713 PASS (${test.duration}ms)`)\n"
    "        // TODO reporte:\n"
    "        //   console.log(`\u2550\u2550\u2550 ${this.suiteName} \u2550\u2550\u2550`)\n"
    "        //   Por cada test: console.log(`[PASS] ${test.name} (${test.duration}ms)`)\n"
    "        //   console.log(`Total: ${n} tests | ${n} passed | 0 failed`)\n"
    "        //   console.log('SUITE: SUCCESS')\n"
    "    }\n"
    "}\n"
    "\n"
    "\n"
    "const runner = new E2ERunner('Login Flow \u2014 Nexo Protocol');\n"
    "\n"
    "runner.addTest({\n"
    "    name:      'navigate_to_login',\n"
    "    steps:     ['goto https://app.daki.io/login'],\n"
    "    assertion: 'url contains /login',\n"
    "});\n"
    "runner.addTest({\n"
    "    name:      'submit_credentials',\n"
    "    steps:     ['fill #email', 'fill #password', 'click #submit'],\n"
    "    assertion: 'redirect to /dashboard',\n"
    "});\n"
    "runner.addTest({\n"
    "    name:      'verify_dashboard',\n"
    "    steps:     ['waitFor .welcome-panel', 'getText .user-name'],\n"
    "    assertion: 'text equals \"Operador\"',\n"
    "});\n"
    "\n"
    "runner.runAll();\n"
),
"expected_output": (
    "\u25b6 Running: navigate_to_login\n"
    "  Step: goto https://app.daki.io/login\n"
    "  Assert: url contains /login\n"
    "  \u2713 PASS (120ms)\n"
    "\u25b6 Running: submit_credentials\n"
    "  Step: fill #email\n"
    "  Step: fill #password\n"
    "  Step: click #submit\n"
    "  Assert: redirect to /dashboard\n"
    "  \u2713 PASS (360ms)\n"
    "\u25b6 Running: verify_dashboard\n"
    "  Step: waitFor .welcome-panel\n"
    "  Step: getText .user-name\n"
    "  Assert: text equals \"Operador\"\n"
    "  \u2713 PASS (240ms)\n"
    "\u2550\u2550\u2550 Login Flow \u2014 Nexo Protocol \u2550\u2550\u2550\n"
    "[PASS] navigate_to_login (120ms)\n"
    "[PASS] submit_credentials (360ms)\n"
    "[PASS] verify_dashboard (240ms)\n"
    "Total: 3 tests | 3 passed | 0 failed\n"
    "SUITE: SUCCESS"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "\u221e BOSS CHARLIE \u2014 El sector de autenticación del Nexo está bajo ataque. "
    "Necesitas un E2E runner completo para el flujo login→dashboard. "
    "3 tests, 6 steps, 0 tolerancia a fallos. El sistema no espera."
),
"theory_content": (
    "## Cómo funciona un E2E runner\n\n"
    "Un runner de E2E es essencialmente:\n"
    "1. **Collect** — recolecta los tests definidos\n"
    "2. **Execute** — corre cada test en secuencia (o paralelo)\n"
    "3. **Report** — genera el reporte de resultados\n\n"
    "Playwright implementa estos tres pasos internamente. "
    "Aquí lo construimos manualmente para entender el mecanismo.\n\n"
    "**`duration = steps.length * 120`** — cada step 'tarda' 120ms en esta simulación."
),
"pedagogical_objective": "Construir un E2E runner completo — integra todos los conceptos de la Fase 3.",
"syntax_hint": "runAll tiene dos loops: uno para ejecutar (con console.log de steps) y otro para el reporte final.",
"hints_json": json.dumps([
    "addTest: `this.tests.push(test)`",
    "En el primer loop de runAll: `console.log(\\`▶ Running: ${test.name}\\`); test.steps.forEach(s => console.log(\\`  Step: ${s}\\`)); console.log(\\`  Assert: ${test.assertion}\\`); test.duration = test.steps.length * 120; test.result = 'PASS'; console.log(\\`  ✓ PASS (${test.duration}ms)\\`)`",
    "Para el reporte: `console.log(\\`═══ ${this.suiteName} ═══\\`)` luego cada test, luego `Total: ${n} tests | ${n} passed | 0 failed` y SUITE: SUCCESS.",
]),
"grid_map_json": None,
},
]
