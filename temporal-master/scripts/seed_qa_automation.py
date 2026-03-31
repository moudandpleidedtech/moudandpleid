"""
seed_qa_automation.py — QA Automation: Operaciones Especiales (50 Niveles)
==========================================================================
Disciplina: De QA Manual a Automation Engineer
codex_id: qa_automation_ops

Fases:
    001–010: Fundamentos de TypeScript para QA
    011–020: Playwright — E2E Automation
    021–030: API Testing con Supertest & REST Assured
    031–040: CI/CD con GitHub Actions para QA
    041–050: Reporting, Estrategia y Transición Profesional

Uso:  python -m scripts.seed_qa_automation
"""
from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# ─── Helpers ──────────────────────────────────────────────────────────────────

def _level(n, title, desc, briefing, theory, difficulty, xp, phase, concepts):
    tier_map = {"easy": 1, "medium": 2, "hard": 3}
    return {
        "title":                  f"[ AUTO-{n:03d}: {title.upper()} ]",
        "description":            desc,
        "difficulty_tier":        tier_map.get(difficulty, 2),
        "difficulty":             difficulty,
        "sector_id":              None,
        "codex_id":               "qa_automation_ops",
        "level_order":            n,
        "base_xp_reward":         xp,
        "is_project":             n % 10 == 0,
        "telemetry_goal_time":    180 + n * 4,
        "challenge_type":         "scenario",
        "phase":                  phase,
        "concepts_taught_json":   json.dumps(concepts, ensure_ascii=False),
        "initial_code":           (
            f"// ╔══════════════════════════════════════════════════════╗\n"
            f"// ║  QA AUTOMATION OPS — MISIÓN {n:03d}                    ║\n"
            f"// ║  {title[:48]:<48} ║\n"
            f"// ╚══════════════════════════════════════════════════════╝\n"
            f"//\n"
            f"// Implementa la solución aquí\n"
            f"\n"
            f"const resultado = 'OK';\n"
            f"console.log(resultado);\n"
        ),
        "expected_output":        "OK",
        "test_inputs_json":       json.dumps(["OK"]),
        "lore_briefing":          briefing,
        "theory_content":         theory if theory else f"## {title}\n\n{desc}",
        "pedagogical_objective":  f"Nivel {n} de QA Automation Ops: {desc[:80]}",
        "syntax_hint":            "",
        "hints_json":             json.dumps([
            f"Revisa la teoría de {title} para entender el concepto.",
            f"Los conceptos clave son: {', '.join(concepts[:3])}.",
            f"Misión {n}: aplica {concepts[0]} para resolver el desafío.",
        ], ensure_ascii=False),
        "grid_map_json":          None,
        "strict_match":           False,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# FASE 1 (1–10): Fundamentos de TypeScript para QA
# ═══════════════════════════════════════════════════════════════════════════════

F1 = [
    (1, "TypeScript vs JavaScript",
     "Explica las 3 diferencias críticas entre TypeScript y JavaScript para un contexto QA.",
     "Operador, TypeScript no es moderno — es obligatorio. El type system previene bugs antes del runtime.",
     "## TypeScript para QA\n\nTypeScript agrega **tipos estáticos** a JavaScript:\n\n```ts\n// JS — se cae en runtime\nconst url: any = null;\nconsole.log(url.length); // TypeError!\n\n// TS — se cae en compilación\nconst url: string = null; // Error: Type 'null' is not assignable to type 'string'\n```\n\n**Por qué importa para QA:**\n- Menos bugs de tipo en tus scripts de automation\n- Autocompletado real en tus page objects\n- Documentación viva del contrato de tus helpers",
     "easy", 100, "typescript_fundamentos", ["TypeScript", "tipado_estático", "QA"]),

    (2, "Tipos Primitivos en Tests",
     "Declara variables tipadas para representar los datos de un test case: URL, status code, timeout.",
     "Cada test tiene datos. Si esos datos no tienen tipos, los errores llegan de noche y en producción.",
     "## Tipos Primitivos\n\n```ts\nconst baseUrl: string = 'https://api.daki.io';\nconst timeout: number = 5000;\nconst isCI: boolean = process.env.CI === 'true';\nconst tags: string[] = ['smoke', 'regression'];\n```\n\n**Tipos comunes en automation:**\n- `string` — URLs, selectores, mensajes\n- `number` — timeouts, status codes, conteos\n- `boolean` — flags de entorno, assertions\n- `string[]` — tags, suites de tests",
     "easy", 110, "typescript_fundamentos", ["tipos_primitivos", "variables_tipadas", "datos_test"]),

    (3, "Interfaces para Page Objects",
     "Crea una interface TypeScript que modele un LoginPage con sus métodos y propiedades.",
     "Una interface es el contrato de tu Page Object. Rómpelo y el compilador te avisa antes que el usuario.",
     "## Interfaces en Page Objects\n\n```ts\ninterface ILoginPage {\n  url: string;\n  fill(selector: string, value: string): Promise<void>;\n  submit(): Promise<void>;\n  getErrorMessage(): Promise<string>;\n  isLoggedIn(): Promise<boolean>;\n}\n\nclass LoginPage implements ILoginPage {\n  url = '/login';\n  // ...\n}\n```\n\n**Beneficios:**\n- Contratos explícitos entre pages\n- Mockeable para unit tests\n- Documentación automática",
     "easy", 120, "typescript_fundamentos", ["interfaces", "page_objects", "contratos"]),

    (4, "Async/Await en Automation",
     "Reescribe una función callback-based a async/await para esperar un elemento en pantalla.",
     "Playwright es async. Si no entiendes async/await, tus tests van a race condition permanente.",
     "## Async/Await\n\n```ts\n// ❌ Callback hell\npage.waitForSelector('.modal', (el) => {\n  el.click(() => {\n    page.screenshot(() => { /* ... */ })\n  })\n})\n\n// ✅ Async/Await — lineal y legible\nasync function closeModal(page: Page): Promise<void> {\n  await page.waitForSelector('.modal');\n  await page.click('.modal .close-btn');\n  await page.screenshot({ path: 'after-close.png' });\n}\n```",
     "easy", 130, "typescript_fundamentos", ["async_await", "promesas", "playwright"]),

    (5, "Enums para Estados de Test",
     "Define un enum TestStatus con los estados: PASSED, FAILED, SKIPPED, PENDING, FLAKY.",
     "Los strings sueltos en tu test runner son bugs esperando ocurrir. Los enums los previenen.",
     "## Enums en QA\n\n```ts\nenum TestStatus {\n  PASSED  = 'PASSED',\n  FAILED  = 'FAILED',\n  SKIPPED = 'SKIPPED',\n  PENDING = 'PENDING',\n  FLAKY   = 'FLAKY',\n}\n\ninterface TestResult {\n  name: string;\n  status: TestStatus;\n  duration: number;\n  error?: string;\n}\n\nconst result: TestResult = {\n  name: 'login flow',\n  status: TestStatus.PASSED,\n  duration: 1234,\n};\n```",
     "easy", 130, "typescript_fundamentos", ["enums", "estados", "type_safety"]),

    (6, "Generics en Helpers de Test",
     "Crea una función genérica waitUntil<T> que espera hasta que un predicate retorne truthy.",
     "Los generics evitan repetir el mismo helper para cada tipo de dato. Un helper, infinitos casos.",
     "## Generics para QA\n\n```ts\nasync function waitUntil<T>(\n  fn: () => Promise<T>,\n  predicate: (val: T) => boolean,\n  timeout = 5000\n): Promise<T> {\n  const start = Date.now();\n  while (Date.now() - start < timeout) {\n    const val = await fn();\n    if (predicate(val)) return val;\n    await new Promise(r => setTimeout(r, 200));\n  }\n  throw new Error(`waitUntil timed out after ${timeout}ms`);\n}\n\n// Uso:\nconst count = await waitUntil(\n  () => page.locator('.items').count(),\n  n => n > 0\n);\n```",
     "medium", 160, "typescript_fundamentos", ["generics", "helpers", "polling"]),

    (7, "Tipos Union para Selectores",
     "Crea un tipo LocatorStrategy = 'css' | 'xpath' | 'text' | 'role' y úsalo en una factory.",
     "Los selectores son el talón de Aquiles del E2E. Tiparloos previene estrategias inválidas.",
     "## Union Types para Selectores\n\n```ts\ntype LocatorStrategy = 'css' | 'xpath' | 'text' | 'role' | 'testid';\n\nfunction buildLocator(\n  page: Page,\n  strategy: LocatorStrategy,\n  value: string\n) {\n  switch (strategy) {\n    case 'css':    return page.locator(value);\n    case 'xpath':  return page.locator(`xpath=${value}`);\n    case 'text':   return page.getByText(value);\n    case 'role':   return page.getByRole(value as any);\n    case 'testid': return page.getByTestId(value);\n  }\n}\n```",
     "medium", 160, "typescript_fundamentos", ["union_types", "selectores", "locators"]),

    (8, "Configuración con Types",
     "Tipea un objeto de configuración para una suite E2E: browsers, baseURL, retries, workers.",
     "Una config tipada es una config que te avisa cuando te equivocas de key. Antes del run.",
     "## Config Tipada\n\n```ts\ntype Browser = 'chromium' | 'firefox' | 'webkit';\n\ninterface E2EConfig {\n  baseURL: string;\n  browsers: Browser[];\n  retries: number;\n  workers: number;\n  timeout: number;\n  headless: boolean;\n  reportDir: string;\n}\n\nconst config: E2EConfig = {\n  baseURL: process.env.BASE_URL ?? 'http://localhost:3000',\n  browsers: ['chromium', 'firefox'],\n  retries: process.env.CI ? 2 : 0,\n  workers: 4,\n  timeout: 30_000,\n  headless: true,\n  reportDir: './test-results',\n};\n```",
     "medium", 170, "typescript_fundamentos", ["configuración", "tipos", "playwright_config"]),

    (9, "Type Guards en Assertions",
     "Implementa un type guard isApiError(response) que distingue entre respuesta exitosa y error.",
     "Los type guards transforman un any caótico en un tipo seguro. Tus assertions se vuelven precisas.",
     "## Type Guards\n\n```ts\ninterface ApiSuccess<T> {\n  data: T;\n  status: 'success';\n}\n\ninterface ApiError {\n  message: string;\n  code: number;\n  status: 'error';\n}\n\ntype ApiResponse<T> = ApiSuccess<T> | ApiError;\n\nfunction isApiError<T>(res: ApiResponse<T>): res is ApiError {\n  return res.status === 'error';\n}\n\n// Uso:\nconst res = await api.get('/users/999');\nif (isApiError(res)) {\n  expect(res.code).toBe(404);\n} else {\n  expect(res.data).toBeDefined();\n}\n```",
     "medium", 180, "typescript_fundamentos", ["type_guards", "assertions", "API"]),

    (10, "CONTRATO-TS-10: Librería de Helpers",
     "Proyecto: construye una mini-librería de helpers tipados: retry, poll, formatDuration, groupBy.",
     "La batalla TypeScript termina donde empieza la automatización real. Tus helpers son tus armas.",
     "## Proyecto: Helper Library\n\nCombina todo lo aprendido:\n\n```ts\n// retry con backoff exponencial\nexport async function retry<T>(\n  fn: () => Promise<T>,\n  options: { attempts: number; delay: number }\n): Promise<T> { /* ... */ }\n\n// poll hasta condición\nexport async function poll<T>(\n  fn: () => Promise<T>,\n  until: (v: T) => boolean,\n  timeout: number\n): Promise<T> { /* ... */ }\n\n// formatea duración en ms\nexport function formatDuration(ms: number): string { /* ... */ }\n\n// agrupa resultados de tests\nexport function groupBy<T>(\n  items: T[],\n  key: keyof T\n): Record<string, T[]> { /* ... */ }\n```",
     "hard", 400, "typescript_fundamentos", ["librería", "helpers", "integración_ts"]),
]

# ═══════════════════════════════════════════════════════════════════════════════
# FASE 2 (11–20): Playwright — E2E Automation
# ═══════════════════════════════════════════════════════════════════════════════

F2 = [
    (11, "Setup de Playwright",
     "Configura un proyecto Playwright desde cero: install, playwright.config.ts, primer test.",
     "Operador, todo deployment empieza con un setup. Playwright no es la excepción.",
     "## Playwright Setup\n\n```bash\nnpm init playwright@latest\n```\n\n```ts\n// playwright.config.ts\nimport { defineConfig } from '@playwright/test';\n\nexport default defineConfig({\n  testDir: './tests',\n  timeout: 30_000,\n  retries: process.env.CI ? 2 : 0,\n  use: {\n    baseURL: 'http://localhost:3000',\n    screenshot: 'only-on-failure',\n    video: 'retain-on-failure',\n    trace: 'on-first-retry',\n  },\n  projects: [\n    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },\n    { name: 'firefox',  use: { ...devices['Desktop Firefox'] } },\n  ],\n});\n```",
     "easy", 150, "playwright_e2e", ["playwright", "setup", "configuración"]),

    (12, "Page Object Model",
     "Implementa un LoginPage POM con métodos: goto, fillCredentials, submit, getError.",
     "El POM es el patrón rey de E2E. Un selector cambia → lo arreglas en un lugar, no en 50 tests.",
     "## Page Object Model\n\n```ts\nimport { type Page, type Locator } from '@playwright/test';\n\nexport class LoginPage {\n  readonly page: Page;\n  readonly emailInput: Locator;\n  readonly passwordInput: Locator;\n  readonly submitBtn: Locator;\n  readonly errorMsg: Locator;\n\n  constructor(page: Page) {\n    this.page = page;\n    this.emailInput    = page.getByLabel('Email');\n    this.passwordInput = page.getByLabel('Password');\n    this.submitBtn     = page.getByRole('button', { name: 'Ingresar' });\n    this.errorMsg      = page.getByRole('alert');\n  }\n\n  async goto() { await this.page.goto('/login'); }\n\n  async login(email: string, password: string) {\n    await this.emailInput.fill(email);\n    await this.passwordInput.fill(password);\n    await this.submitBtn.click();\n  }\n\n  async getError() { return this.errorMsg.textContent(); }\n}\n```",
     "easy", 160, "playwright_e2e", ["POM", "locators", "encapsulación"]),

    (13, "Fixtures Personalizados",
     "Crea un fixture authenticatedPage que hace login automático antes de cada test.",
     "Las fixtures son el inject de dependencias de Playwright. Código que no se repite, tests que no fallan por setup.",
     "## Fixtures en Playwright\n\n```ts\nimport { test as base } from '@playwright/test';\nimport { LoginPage } from './pages/LoginPage';\n\ntype Fixtures = { loggedInPage: Page };\n\nexport const test = base.extend<Fixtures>({\n  loggedInPage: async ({ page }, use) => {\n    const login = new LoginPage(page);\n    await login.goto();\n    await login.login(\n      process.env.TEST_USER!,\n      process.env.TEST_PASS!\n    );\n    await page.waitForURL('/hub');\n    await use(page);  // ← aquí corre el test\n    // teardown automático aquí si hace falta\n  },\n});\n```",
     "medium", 180, "playwright_e2e", ["fixtures", "setup", "autenticación"]),

    (14, "Locators Resilientes",
     "Refactoriza 5 selectores frágiles (CSS por posición) a selectores semánticos resilientes.",
     "Los selectores por posición son bombas de tiempo. Un reordenamiento de la UI y se rompen todos.",
     "## Selectores Resilientes\n\n```ts\n// ❌ Frágil — se rompe con cualquier cambio de layout\npage.locator('div:nth-child(3) > button:first-child');\npage.locator('#root > div > main > form > input[2]');\n\n// ✅ Resiliente — atado al comportamiento, no al layout\npage.getByRole('button', { name: 'Enviar' });         // ARIA\npage.getByLabel('Email');                              // label asociado\npage.getByPlaceholder('Ingresa tu email');             // placeholder\npage.getByTestId('submit-btn');                        // data-testid\npage.getByText('Error: usuario no encontrado');        // texto visible\n```\n\n**Regla:** prefiere roles y labels sobre CSS.",
     "medium", 170, "playwright_e2e", ["locators", "resilencia", "ARIA"]),

    (15, "Assertions Avanzadas",
     "Usa expect() de Playwright para validar: visibilidad, texto, URL, network response y screenshot.",
     "Un test sin assertions es un test que nunca falla. Y un test que nunca falla no detecta nada.",
     "## Assertions Playwright\n\n```ts\n// Visibilidad\nawait expect(page.getByRole('dialog')).toBeVisible();\nawait expect(page.getByRole('dialog')).toBeHidden();\n\n// Texto\nawait expect(page.getByRole('heading')).toHaveText('Bienvenido');\nawait expect(page.getByRole('heading')).toContainText('Bienven');\n\n// URL\nawait expect(page).toHaveURL('/hub');\nawait expect(page).toHaveURL(/\\/hub$/);\n\n// Count\nawait expect(page.locator('.mission-card')).toHaveCount(6);\n\n// Snapshot visual\nawait expect(page).toMatchSnapshot('hub-state.png', { threshold: 0.1 });\n```",
     "medium", 180, "playwright_e2e", ["assertions", "expect", "validaciones"]),

    (16, "Network Interception",
     "Intercepta llamadas a /api/v1/users y mockea una respuesta de error 500 para testear el fallback UI.",
     "Mock de red = tests deterministas. Sin dependencias externas, sin fallos por API inestable.",
     "## Network Mocking\n\n```ts\ntest('muestra error cuando la API falla', async ({ page }) => {\n  // interceptar ANTES de navegar\n  await page.route('**/api/v1/users', route =>\n    route.fulfill({\n      status: 500,\n      contentType: 'application/json',\n      body: JSON.stringify({ message: 'Internal Server Error' }),\n    })\n  );\n\n  await page.goto('/usuarios');\n\n  await expect(\n    page.getByRole('alert')\n  ).toContainText('Error del servidor');\n});\n```",
     "medium", 200, "playwright_e2e", ["network_mock", "route", "determinismo"]),

    (17, "Tests Paralelos y Sharding",
     "Configura Playwright para correr tests en paralelo por archivo y agrega sharding para CI.",
     "Los tests lentos matan la adopción. Paralelismo + sharding = feedback en segundos, no minutos.",
     "## Paralelismo y Sharding\n\n```ts\n// playwright.config.ts\nexport default defineConfig({\n  fullyParallel: true,  // paralelo dentro del mismo archivo\n  workers: process.env.CI ? 2 : '50%', // workers según entorno\n});\n```\n\n```bash\n# Sharding en CI (4 máquinas paralelas)\nnpx playwright test --shard=1/4\nnpx playwright test --shard=2/4\nnpx playwright test --shard=3/4\nnpx playwright test --shard=4/4\n```\n\n**Cuándo usar:**\n- `fullyParallel`: tests independientes (no comparten estado)\n- `workers`: según CPU disponible en CI",
     "medium", 200, "playwright_e2e", ["paralelismo", "sharding", "CI"]),

    (18, "Visual Regression Testing",
     "Configura tests de regresión visual con snapshots y define el threshold de diferencia aceptable.",
     "Los cambios de UI no intencionales son bugs silenciosos. El visual regression los expone.",
     "## Visual Regression\n\n```ts\ntest('hero section sin cambios visuales', async ({ page }) => {\n  await page.goto('/');\n  // Espera a que la animación termine\n  await page.waitForTimeout(500);\n\n  await expect(page).toMatchSnapshot('homepage-hero.png', {\n    threshold: 0.05,      // 5% de píxeles pueden diferir\n    maxDiffPixels: 100,   // o máximo 100 píxeles\n  });\n});\n\n// Actualizar snapshots:\n// npx playwright test --update-snapshots\n```\n\n**CI:** guardar snapshots en el repo, comparar en cada PR.",
     "medium", 210, "playwright_e2e", ["visual_regression", "snapshots", "UI_testing"]),

    (19, "Tracing y Debug",
     "Habilita Playwright Trace para un test fallido y extrae: timeline, screenshots, network calls.",
     "Cuando un test falla en CI y pasa local, el trace es el único testigo. Úsalo.",
     "## Playwright Trace\n\n```ts\n// playwright.config.ts\nuse: {\n  trace: 'on-first-retry',   // solo captura en el primer retry\n  screenshot: 'only-on-failure',\n  video: 'retain-on-failure',\n}\n```\n\n```bash\n# Ver el trace localmente\nnpx playwright show-trace test-results/trace.zip\n```\n\n**El trace incluye:**\n- Timeline de acciones con timestamps\n- Screenshot en cada paso\n- Network calls (request/response)\n- Console logs\n- Snapshots del DOM",
     "medium", 200, "playwright_e2e", ["trace", "debugging", "CI"]),

    (20, "CONTRATO-PW-20: Suite E2E Completa",
     "Proyecto: crea una suite E2E con POM, fixtures, assertions, network mock y reporte HTML.",
     "La batalla Playwright termina con una suite que otro QA puede ejecutar sin instrucciones.",
     "## Proyecto Final — Suite E2E\n\n```\ntests/\n  e2e/\n    auth/\n      login.spec.ts          # happy path + error cases\n      register.spec.ts\n    hub/\n      navigation.spec.ts     # acceso a incursiones\n    api-mocks/\n      error-states.spec.ts   # todos los 4xx/5xx\n  pages/\n    LoginPage.ts\n    HubPage.ts\n  fixtures/\n    auth.fixture.ts\n  helpers/\n    retry.ts\n    wait.ts\nplaywright.config.ts\n```\n\n**Requerimientos:**\n- Mínimo 10 tests\n- POM para cada página\n- Fixture de autenticación\n- 1 test de network mock\n- Reporte HTML generado",
     "hard", 500, "playwright_e2e", ["suite_completa", "POM", "integración"]),
]

# ═══════════════════════════════════════════════════════════════════════════════
# FASE 3 (21–30): API Testing
# ═══════════════════════════════════════════════════════════════════════════════

F3 = [
    (21, "HTTP Fundamentals para QA",
     "Identifica qué status codes son aceptables para: crear recurso, recurso inexistente, sin autorización.",
     "Operador, las APIs hablan en status codes. Si no los entiendes, tus tests son adivinanzas.",
     "## HTTP Status Codes para QA\n\n| Acción | Código Esperado | Descripción |\n|--------|----------------|-------------|\n| GET recurso existente | 200 | OK |\n| POST crear recurso | 201 | Created |\n| DELETE exitoso | 204 | No Content |\n| Recurso inexistente | 404 | Not Found |\n| Sin token | 401 | Unauthorized |\n| Token válido, sin permiso | 403 | Forbidden |\n| Payload inválido | 422 | Unprocessable Entity |\n| Error del servidor | 500 | Internal Server Error |\n\n**Regla QA:** siempre valida tanto el status code como el body.",
     "easy", 150, "api_testing", ["HTTP", "status_codes", "REST"]),

    (22, "Supertest Básico",
     "Escribe un test con Supertest que valide el endpoint GET /api/v1/incursions: status, structure, count.",
     "Supertest es el bisturí del API testing en Node. Limpio, chaineable, sin boilerplate.",
     "## Supertest\n\n```ts\nimport request from 'supertest';\nimport app from '../app';\n\ndescribe('GET /api/v1/incursions', () => {\n  it('retorna lista de incursiones activas', async () => {\n    const res = await request(app)\n      .get('/api/v1/incursions')\n      .set('Authorization', `Bearer ${testToken}`)\n      .expect(200)\n      .expect('Content-Type', /json/);\n\n    expect(Array.isArray(res.body)).toBe(true);\n    expect(res.body.length).toBeGreaterThan(0);\n    expect(res.body[0]).toMatchObject({\n      slug: expect.any(String),\n      titulo: expect.any(String),\n      status: expect.stringMatching(/ACTIVE|ENCRYPTED/),\n    });\n  });\n});\n```",
     "easy", 160, "api_testing", ["Supertest", "GET", "assertions"]),

    (23, "Contract Testing",
     "Define el contrato JSON Schema de la respuesta /api/v1/users/me y valida contra él.",
     "El contract testing detecta breaking changes en la API antes de que rompan el frontend.",
     "## Contract Testing con JSON Schema\n\n```ts\nimport Ajv from 'ajv';\nimport addFormats from 'ajv-formats';\n\nconst ajv = new Ajv();\naddFormats(ajv);\n\nconst userSchema = {\n  type: 'object',\n  required: ['id', 'callsign', 'email', 'role'],\n  properties: {\n    id:        { type: 'string', format: 'uuid' },\n    callsign:  { type: 'string', minLength: 1 },\n    email:     { type: 'string', format: 'email' },\n    role:      { type: 'string', enum: ['USER', 'FOUNDER'] },\n    xp_total:  { type: 'number', minimum: 0 },\n  },\n  additionalProperties: false,  // ← strict mode\n};\n\nconst validate = ajv.compile(userSchema);\n// ...\nexpect(validate(res.body)).toBe(true);\n```",
     "medium", 200, "api_testing", ["contract_testing", "JSON_Schema", "validación"]),

    (24, "Auth Flow Testing",
     "Testea el flujo completo: register → login → acceder recurso protegido → token expirado.",
     "El flujo de auth es el test de mayor ROI. Si falla, no existe la app.",
     "## Auth Flow\n\n```ts\ndescribe('Auth Flow', () => {\n  let token: string;\n\n  it('1. Register', async () => {\n    const res = await request(app)\n      .post('/api/v1/auth/register')\n      .send({ callsign: 'TESTER', email: 'test@daki.io', password: 'test123' })\n      .expect(201);\n    expect(res.body.callsign).toBe('TESTER');\n  });\n\n  it('2. Login', async () => {\n    const res = await request(app)\n      .post('/api/v1/auth/login')\n      .send({ email: 'test@daki.io', password: 'test123' })\n      .expect(200);\n    token = res.body.access_token;\n    expect(token).toBeDefined();\n  });\n\n  it('3. Acceder recurso protegido', async () => {\n    await request(app)\n      .get('/api/v1/users/me')\n      .set('Authorization', `Bearer ${token}`)\n      .expect(200);\n  });\n\n  it('4. Rechazar token inválido', async () => {\n    await request(app)\n      .get('/api/v1/users/me')\n      .set('Authorization', 'Bearer TOKEN_FALSO')\n      .expect(401);\n  });\n});\n```",
     "medium", 220, "api_testing", ["auth_flow", "JWT", "end_to_end"]),

    (25, "Boundary Value Testing",
     "Diseña tests de boundary values para un endpoint que acepta XP entre 0 y 10000.",
     "Los bugs viven en los bordes. El BVA es la técnica que los encuentra sistemáticamente.",
     "## Boundary Value Analysis\n\n```ts\ndescribe('POST /api/v1/xp — Boundary Values', () => {\n  // Válidos: exactamente en el límite\n  test.each([\n    [0,     true,  'mínimo válido'],\n    [1,     true,  'justo sobre el mínimo'],\n    [5000,  true,  'valor medio'],\n    [9999,  true,  'justo bajo el máximo'],\n    [10000, true,  'máximo válido'],\n  ])('xp=%i → válido=%s (%s)', async (xp, valid) => {\n    const res = await request(app).post('/api/v1/xp').send({ xp });\n    expect(res.status).toBe(valid ? 200 : 422);\n  });\n\n  // Inválidos: fuera del límite\n  test.each([\n    [-1,    false, 'justo bajo el mínimo'],\n    [10001, false, 'justo sobre el máximo'],\n  ])('xp=%i → válido=%s (%s)', async (xp, valid) => {\n    const res = await request(app).post('/api/v1/xp').send({ xp });\n    expect(res.status).toBe(422);\n  });\n});\n```",
     "medium", 200, "api_testing", ["BVA", "boundary_values", "partición_equivalencia"]),

    (26, "Pact: Consumer-Driven Contracts",
     "Crea un consumer pact para la interacción frontend → /api/v1/incursions.",
     "Pact invierte el flujo: el consumer define qué espera, el provider verifica que lo cumple.",
     "## Consumer-Driven Contracts con Pact\n\n```ts\n// consumer.pact.spec.ts\nimport { PactV3, MatchersV3 } from '@pact-foundation/pact';\n\nconst provider = new PactV3({\n  consumer: 'daki-frontend',\n  provider: 'daki-api',\n});\n\ndescribe('GET /incursions', () => {\n  it('retorna lista de incursiones', () =>\n    provider\n      .given('hay incursiones activas')\n      .uponReceiving('una solicitud de incursiones')\n      .withRequest({ method: 'GET', path: '/api/v1/incursions' })\n      .willRespondWith({\n        status: 200,\n        body: MatchersV3.eachLike({\n          slug: MatchersV3.string('python-core'),\n          status: MatchersV3.string('ACTIVE'),\n        }),\n      })\n      .executeTest(async (mockServer) => {\n        const res = await fetch(`${mockServer.url}/api/v1/incursions`);\n        const data = await res.json();\n        expect(Array.isArray(data)).toBe(true);\n      })\n  );\n});\n```",
     "hard", 280, "api_testing", ["Pact", "contract_testing", "consumer_driven"]),

    (27, "Performance Benchmarking de API",
     "Implementa un test que mida el percentil P95 de latencia de /api/v1/levels/sectors y alerte si > 500ms.",
     "Las APIs lentas son bugs invisibles. El QA automation los vuelve visibles y alertables.",
     "## Latency Benchmarking\n\n```ts\nasync function measureLatency(\n  fn: () => Promise<void>,\n  samples = 20\n): Promise<{ p50: number; p95: number; p99: number }> {\n  const times: number[] = [];\n  for (let i = 0; i < samples; i++) {\n    const start = performance.now();\n    await fn();\n    times.push(performance.now() - start);\n  }\n  times.sort((a, b) => a - b);\n  return {\n    p50: times[Math.floor(samples * 0.50)],\n    p95: times[Math.floor(samples * 0.95)],\n    p99: times[Math.floor(samples * 0.99)],\n  };\n}\n\ntest('P95 latency < 500ms', async () => {\n  const stats = await measureLatency(() =>\n    request(app).get('/api/v1/levels/sectors').set('Authorization', `Bearer ${token}`)\n  );\n  expect(stats.p95).toBeLessThan(500);\n});\n```",
     "hard", 280, "api_testing", ["performance", "latencia", "P95"]),

    (28, "Error Injection Testing",
     "Diseña tests para validar que la API maneja correctamente: payload malformado, campos faltantes, tipos inválidos.",
     "Si no pruebas el caso de error, no pruebas la mitad del código. Y esa mitad es la que más falla.",
     "## Error Injection\n\n```ts\ndescribe('POST /api/v1/auth/register — Error Cases', () => {\n  test.each([\n    [{ email: 'no-valid', password: 'abc', callsign: 'X' },  422, 'email inválido'],\n    [{ email: 'a@b.com', password: 'ab',  callsign: 'X' },  422, 'password muy corta'],\n    [{ email: 'a@b.com', password: 'abc123'               },  422, 'callsign faltante'],\n    [{                                                     },  422, 'body vacío'],\n    ['string invalido',                                       422, 'body no-JSON'],\n  ])('rechaza: %s', async (body, expectedStatus, reason) => {\n    const res = await request(app)\n      .post('/api/v1/auth/register')\n      .send(body);\n    expect(res.status).toBe(expectedStatus);\n    expect(res.body.detail ?? res.body.message).toBeDefined();\n  });\n});\n```",
     "medium", 220, "api_testing", ["error_injection", "validación", "edge_cases"]),

    (29, "Load Testing Básico",
     "Usa k6 para simular 50 usuarios concurrentes en /api/v1/incursions y mide el throughput.",
     "Los tests funcionales prueban que funciona. El load testing prueba que funciona bajo presión.",
     "## k6 Load Test\n\n```js\n// load-test.k6.js\nimport http from 'k6/http';\nimport { check, sleep } from 'k6';\n\nexport const options = {\n  vus: 50,           // 50 usuarios virtuales\n  duration: '30s',   // durante 30 segundos\n  thresholds: {\n    http_req_duration: ['p(95)<500'],  // P95 < 500ms\n    http_req_failed:   ['rate<0.01'],  // < 1% errores\n  },\n};\n\nexport default function () {\n  const res = http.get('https://api.dakiedtech.com/api/v1/incursions', {\n    headers: { Authorization: `Bearer ${__ENV.TOKEN}` },\n  });\n\n  check(res, {\n    'status 200': (r) => r.status === 200,\n    'latencia < 500ms': (r) => r.timings.duration < 500,\n  });\n\n  sleep(1);\n}\n```\n\n```bash\nk6 run --env TOKEN=xxx load-test.k6.js\n```",
     "hard", 280, "api_testing", ["k6", "load_testing", "performance"]),

    (30, "CONTRATO-API-30: Test Suite Full-Stack",
     "Proyecto: suite API que cubre auth, CRUD, contratos, error injection y benchmark de latencia.",
     "Treinta misiones de API testing y ahora posees el arsenal completo. Úsalo.",
     "## Proyecto: API Test Suite\n\n```\ntests/\n  api/\n    auth/\n      login.spec.ts\n      register.spec.ts\n      token-refresh.spec.ts\n    incursions/\n      list.spec.ts\n      contract.spec.ts       # JSON Schema\n    levels/\n      get-codex.spec.ts\n      boundary.spec.ts       # BVA\n    error-cases/\n      malformed-payloads.spec.ts\n      missing-fields.spec.ts\n  load/\n    smoke.k6.js\n    stress.k6.js\n  contracts/\n    pact/\n      consumer.pact.spec.ts\n```\n\n**KPIs del proyecto:**\n- Coverage: >80% de endpoints\n- Contract: 100% de endpoints críticos\n- Load: P95 < 500ms en smoke test",
     "hard", 500, "api_testing", ["suite_completa", "integración", "API"]),
]

# ═══════════════════════════════════════════════════════════════════════════════
# FASE 4 (31–40): CI/CD con GitHub Actions para QA
# ═══════════════════════════════════════════════════════════════════════════════

F4 = [
    (31, "GitHub Actions Básico",
     "Crea un workflow que corra tus tests E2E en cada PR a main con Playwright en Ubuntu.",
     "Operador, un test que solo corre en tu máquina no es un test. Es un script local.",
     "## GitHub Actions — Playwright\n\n```yaml\n# .github/workflows/e2e.yml\nname: E2E Tests\n\non:\n  pull_request:\n    branches: [main]\n\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n\n      - uses: actions/setup-node@v4\n        with:\n          node-version: 20\n          cache: npm\n\n      - name: Install dependencies\n        run: npm ci\n\n      - name: Install Playwright browsers\n        run: npx playwright install --with-deps chromium\n\n      - name: Run E2E tests\n        run: npx playwright test\n        env:\n          BASE_URL: ${{ secrets.STAGING_URL }}\n          TEST_USER: ${{ secrets.TEST_USER }}\n          TEST_PASS: ${{ secrets.TEST_PASS }}\n\n      - name: Upload test report\n        if: always()   # siempre, incluso si fallan\n        uses: actions/upload-artifact@v4\n        with:\n          name: playwright-report\n          path: playwright-report/\n          retention-days: 30\n```",
     "easy", 200, "cicd_qa", ["GitHub_Actions", "CI", "Playwright"]),

    (32, "Secrets y Environments",
     "Configura secrets para TEST_USER, TEST_PASS y BASE_URL y úsalos en el workflow de QA.",
     "Los secrets en el código son la brecha de seguridad más común. Los environments los previenen.",
     "## Secrets en GitHub Actions\n\n```yaml\n# 1. En GitHub: Settings → Secrets → Actions → New\n#    TEST_USER = qa_automation@test.daki.io\n#    TEST_PASS = [generado seguro]\n#    STAGING_URL = https://staging.dakiedtech.com\n\n# 2. En el workflow:\njobs:\n  test:\n    environment: staging  # ← limita quién puede deployar a staging\n    steps:\n      - name: Run tests\n        env:\n          BASE_URL:   ${{ secrets.STAGING_URL }}\n          TEST_USER:  ${{ secrets.TEST_USER }}\n          TEST_PASS:  ${{ secrets.TEST_PASS }}\n        run: npx playwright test\n```\n\n**Regla:** nunca logguear secrets. `echo $TEST_PASS` en CI expone el secret en los logs.",
     "easy", 190, "cicd_qa", ["secrets", "environments", "seguridad"]),

    (33, "Caching de Dependencias",
     "Optimiza el workflow para cachear node_modules y browsers de Playwright entre runs.",
     "Sin cache, cada run descarga 500MB de browsers. Con cache, son 3 segundos. Elige bien.",
     "## Caching en CI\n\n```yaml\n- name: Cache Playwright browsers\n  uses: actions/cache@v4\n  id: playwright-cache\n  with:\n    path: ~/.cache/ms-playwright\n    key: playwright-${{ runner.os }}-${{ hashFiles('package-lock.json') }}\n    restore-keys: playwright-${{ runner.os }}-\n\n- name: Install Playwright browsers\n  if: steps.playwright-cache.outputs.cache-hit != 'true'\n  run: npx playwright install --with-deps chromium\n\n- name: Install deps only if needed\n  if: steps.playwright-cache.outputs.cache-hit != 'true'\n  run: npx playwright install-deps chromium\n```\n\n**Resultado:** de 4 minutos a 45 segundos en CI.",
     "medium", 220, "cicd_qa", ["caching", "optimización", "CI"]),

    (34, "Matrix Testing por Browser",
     "Configura una matrix strategy para correr los tests en chromium, firefox y webkit.",
     "La matrix de browsers es la diferencia entre 'funciona en Chrome' y 'funciona para todos'.",
     "## Matrix Strategy\n\n```yaml\njobs:\n  test:\n    strategy:\n      fail-fast: false   # continúa aunque un browser falle\n      matrix:\n        browser: [chromium, firefox, webkit]\n        os: [ubuntu-latest, windows-latest]\n    runs-on: ${{ matrix.os }}\n    name: Tests on ${{ matrix.browser }} / ${{ matrix.os }}\n    steps:\n      - name: Run tests\n        run: npx playwright test --project=${{ matrix.browser }}\n        env:\n          CI: true\n```\n\n**Tradeoff:** 6 jobs paralelos vs 6x el tiempo si es secuencial. La matrix paraleliza automáticamente.",
     "medium", 230, "cicd_qa", ["matrix", "browsers", "cross-browser"]),

    (35, "Quality Gate con Coverage",
     "Agrega un step que falle el PR si el coverage de tests API cae por debajo del 80%.",
     "Un quality gate sin enforcement es una sugerencia. Con enforcement, es un estándar.",
     "## Quality Gate\n\n```yaml\n- name: Run tests with coverage\n  run: npx jest --coverage --coverageThreshold='{\"global\":{\"lines\":80}}'\n\n- name: Upload coverage to Codecov\n  uses: codecov/codecov-action@v4\n  with:\n    token: ${{ secrets.CODECOV_TOKEN }}\n    fail_ci_if_error: true\n```\n\n```json\n// jest.config.json\n{\n  \"coverageThreshold\": {\n    \"global\": {\n      \"branches\": 70,\n      \"functions\": 80,\n      \"lines\": 80,\n      \"statements\": 80\n    }\n  }\n}\n```\n\n**Regla:** el threshold se sube, nunca se baja.",
     "medium", 230, "cicd_qa", ["coverage", "quality_gate", "thresholds"]),

    (36, "Notificaciones de Fallo",
     "Configura Slack notification cuando el pipeline de QA falla en main.",
     "Un fallo silencioso en main es un incendio que nadie apaga. Las notificaciones son las alarmas.",
     "## Slack Notifications\n\n```yaml\n- name: Notificar fallo a Slack\n  if: failure() && github.ref == 'refs/heads/main'\n  uses: slackapi/slack-github-action@v1.25.0\n  with:\n    payload: |\n      {\n        \"text\": \"🔴 *QA Pipeline FAILED* en `main`\",\n        \"attachments\": [{\n          \"color\": \"danger\",\n          \"fields\": [\n            { \"title\": \"Branch\", \"value\": \"${{ github.ref_name }}\", \"short\": true },\n            { \"title\": \"Commit\",  \"value\": \"${{ github.sha }}\", \"short\": true },\n            { \"title\": \"Run\",     \"value\": \"<${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}|Ver logs>\" }\n          ]\n        }]\n      }\n  env:\n    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}\n    SLACK_WEBHOOK_TYPE: INCOMING_WEBHOOK\n```",
     "medium", 220, "cicd_qa", ["Slack", "notificaciones", "alertas"]),

    (37, "Docker para Ambientes de Test",
     "Crea un docker-compose.test.yml que levanta la API, la DB y corre los tests en contenedor.",
     "Si tus tests dependen del entorno local, no son tests reproducibles. Docker lo resuelve.",
     "## Docker para QA\n\n```yaml\n# docker-compose.test.yml\nversion: '3.9'\nservices:\n  db:\n    image: postgres:16-alpine\n    environment:\n      POSTGRES_DB: daki_test\n      POSTGRES_USER: test\n      POSTGRES_PASSWORD: test\n    healthcheck:\n      test: [\"CMD\", \"pg_isready\", \"-U\", \"test\"]\n      interval: 5s\n      retries: 5\n\n  api:\n    build: .\n    depends_on:\n      db:\n        condition: service_healthy\n    environment:\n      DATABASE_URL: postgresql://test:test@db:5432/daki_test\n      SECRET_KEY: test_secret_key_not_for_prod\n    command: uvicorn app.main:app --host 0.0.0.0 --port 8000\n\n  tests:\n    build:\n      context: ./frontend\n      dockerfile: Dockerfile.test\n    depends_on: [api]\n    command: npx playwright test\n    environment:\n      BASE_URL: http://api:8000\n```\n\n```bash\ndocker compose -f docker-compose.test.yml up --abort-on-container-exit\n```",
     "hard", 300, "cicd_qa", ["Docker", "contenedores", "reproducibilidad"]),

    (38, "Deployment Verification Tests",
     "Crea smoke tests que se ejecutan automáticamente después de cada deploy a staging.",
     "El deployment verification test es el primer operador en llegar a staging. Si cae, nadie más entra.",
     "## Post-Deploy Smoke Tests\n\n```yaml\n# .github/workflows/smoke-post-deploy.yml\nname: Smoke Tests — Post Deploy\n\non:\n  workflow_run:\n    workflows: [\"Deploy to Staging\"]\n    types: [completed]\n\njobs:\n  smoke:\n    if: ${{ github.event.workflow_run.conclusion == 'success' }}\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - run: npm ci\n      - run: npx playwright install chromium --with-deps\n      - name: Smoke tests\n        run: npx playwright test --grep @smoke\n        env:\n          BASE_URL: ${{ secrets.STAGING_URL }}\n```\n\n```ts\n// Marcar tests como smoke:\ntest('@smoke: login exitoso', async ({ page }) => { ... });\ntest('@smoke: hub carga', async ({ page }) => { ... });\ntest('@smoke: API health', async ({ page }) => { ... });\n```",
     "hard", 280, "cicd_qa", ["smoke_tests", "post_deploy", "staging"]),

    (39, "Test Reporting Dashboard",
     "Configura Allure Report para generar un dashboard HTML con historial de test runs.",
     "Un reporte que solo ves tú no impacta al equipo. El dashboard convierte datos en cultura.",
     "## Allure Report\n\n```bash\nnpm install --save-dev allure-playwright allure-commandline\n```\n\n```ts\n// playwright.config.ts\nreporter: [\n  ['list'],\n  ['allure-playwright'],\n  ['html', { outputFolder: 'playwright-report' }],\n],\n```\n\n```yaml\n# En CI:\n- name: Generate Allure Report\n  if: always()\n  run: npx allure generate allure-results --clean -o allure-report\n\n- name: Deploy to GitHub Pages\n  if: always()\n  uses: JamesIves/github-pages-deploy-action@v4\n  with:\n    folder: allure-report\n    branch: gh-pages\n```\n\n**El dashboard muestra:**\n- Historial de éxito/fallo por suite\n- Tendencias de flakiness\n- Tests más lentos\n- Screenshots de fallos",
     "medium", 250, "cicd_qa", ["Allure", "reporting", "dashboard"]),

    (40, "CONTRATO-CICD-40: Pipeline Completo",
     "Proyecto: pipeline GitHub Actions con matrix, cache, quality gate, Docker y Allure Report.",
     "Cuarenta misiones de CI/CD y tienes el pipeline que separa a los QA Senior de los Junior.",
     "## Proyecto Final — Pipeline QA\n\n```yaml\n# Un pipeline que incluye:\n\n1. Lint & Type Check     → tsc --noEmit + eslint\n2. Unit Tests            → jest --coverage (gate: 80%)\n3. API Tests             → supertest suite completa\n4. E2E Matrix            → chromium + firefox en ubuntu + windows\n5. Post-deploy Smoke     → @smoke tags en staging\n6. Allure Report         → publicado en GitHub Pages\n7. Slack notification    → solo si falla en main\n```\n\n**Tiempo objetivo:**\n- PR check: < 8 minutos\n- Post-deploy smoke: < 2 minutos\n- Feedback al developer: < 10 minutos del push",
     "hard", 600, "cicd_qa", ["pipeline_completo", "GitHub_Actions", "integración"]),
]

# ═══════════════════════════════════════════════════════════════════════════════
# FASE 5 (41–50): Reporting, Estrategia y Transición Profesional
# ═══════════════════════════════════════════════════════════════════════════════

F5 = [
    (41, "Métricas de Calidad",
     "Define y calcula: defect density, test coverage, escaped defects, flaky test rate.",
     "Operador, lo que no se mide no se mejora. Las métricas de calidad convierten opiniones en datos.",
     "## Métricas de QA\n\n| Métrica | Fórmula | Target |\n|---------|---------|--------|\n| Defect Density | bugs / KLOC | < 1 por release |\n| Test Coverage | líneas probadas / total | > 80% crítico |\n| Escaped Defects | bugs en prod / bugs totales | < 5% |\n| Flaky Rate | tests flacos / total | < 2% |\n| MTTR (Mean Time to Repair) | tiempo desde detección → fix | < 4h para P1 |\n\n```ts\ninterface QAMetrics {\n  defectDensity:    number;  // bugs per KLOC\n  testCoverage:     number;  // 0-100%\n  escapedDefects:   number;  // 0-100%\n  flakyRate:        number;  // 0-100%\n  mttrHours:        number;  // horas promedio\n}\n```",
     "easy", 200, "estrategia_qa", ["métricas", "KPIs", "calidad"]),

    (42, "Test Strategy Document",
     "Redacta una test strategy para una feature nueva: alcance, tipos de tests, criterios de entrada/salida.",
     "Sin estrategia escrita, cada QA prueba lo que le parece. Con ella, el equipo prueba lo mismo.",
     "## Test Strategy Template\n\n```markdown\n# Test Strategy — [Feature Name]\n\n## Alcance\n- IN: login flow, JWT, dashboard inicial\n- OUT: perfil de usuario, notificaciones\n\n## Tipos de Tests\n| Tipo | Herramienta | Cobertura Target |\n|------|-------------|------------------|\n| Unit | Jest | 80% |\n| Integration | Supertest | 100% endpoints críticos |\n| E2E | Playwright | Happy path + 3 error cases |\n| Performance | k6 | P95 < 500ms |\n\n## Entry Criteria\n- [ ] Código en staging\n- [ ] Smoke tests pasando\n- [ ] Datos de test preparados\n\n## Exit Criteria\n- [ ] 0 bugs P1/P2 abiertos\n- [ ] Coverage > 80%\n- [ ] Sign-off de Product\n```",
     "medium", 220, "estrategia_qa", ["estrategia", "documentación", "planning"]),

    (43, "Risk-Based Testing",
     "Aplica risk-based testing a un release: identifica las 5 áreas de mayor riesgo y prioriza la cobertura.",
     "No tienes tiempo para probar todo. El risk-based testing te dice qué probar primero.",
     "## Risk-Based Testing\n\n**Paso 1: Identificar riesgos**\n| Área | Probabilidad | Impacto | Score |\n|------|-------------|---------|-------|\n| Auth/JWT | Alta | Crítico | 9 |\n| Pagos | Media | Crítico | 8 |\n| Dashboard | Baja | Alto | 4 |\n| UI/typos | Alta | Bajo | 3 |\n\n**Paso 2: Priorizar tests**\n```\nScore 8-9 → 100% coverage, automatizado\nScore 5-7 → 80% coverage, smoke E2E\nScore 1-4 → manual exploratorio\n```\n\n**Paso 3: Asignar tiempo**\n```\nAuth:    4h de automation\nPagos:   3h de automation + 1h manual\nDashboard: 1h manual exploratorio\n```",
     "medium", 230, "estrategia_qa", ["risk_based", "priorización", "estrategia"]),

    (44, "Shift-Left Testing",
     "Diseña un proceso shift-left: cómo involucrar QA desde los requirements, no desde el testing.",
     "Shift-left no es detectar bugs antes — es no crearlos. QA en el diseño previene 10x más que QA en el test.",
     "## Shift-Left en Práctica\n\n**Fase 1: Requirements Review**\n- QA revisa los tickets antes de sprint planning\n- Agrega Acceptance Criteria en formato Gherkin\n- Identifica edge cases que el desarrollador no vio\n\n**Fase 2: Design Review**\n- QA asiste al tech design para plantear testabilidad\n- Pregunta: ¿cómo voy a testear esto?\n- Propone: data-testid, logging, observability\n\n**Fase 3: Definition of Done**\n```\n✅ Unit tests escritos por el dev\n✅ Code review aprobado\n✅ QA automation actualizado\n✅ No nuevos bugs P1/P2\n✅ Coverage no decreció\n```",
     "medium", 220, "estrategia_qa", ["shift_left", "proceso", "prevención"]),

    (45, "Flaky Test Management",
     "Implementa una estrategia para detectar, categorizar y eliminar tests flaky en tu suite.",
     "Un test flaky es peor que no tener el test. Genera ruido, bloquea PRs y destruye la confianza en QA.",
     "## Flaky Test Management\n\n**Detección:**\n```bash\n# Correr el test 10 veces y medir fallo rate\nnpx playwright test --repeat-each=10 tests/auth/login.spec.ts\n```\n\n**Categorías de flakiness:**\n| Causa | Solución |\n|-------|----------|\n| Race condition | `waitForSelector` antes de `click` |\n| Data compartida | Tests independientes con datos únicos |\n| Timing | `toBeVisible()` en vez de `waitForTimeout` |\n| Red inestable | `page.route()` para mockear |\n| Orden de tests | `test.describe.configure({ mode: 'parallel' })` |\n\n**Dashboard de flakiness:**\n```ts\n// En Allure, etiquetar automáticamente:\nif (test.retry > 0) test.annotations.push({ type: 'flaky' });\n```",
     "hard", 260, "estrategia_qa", ["flaky_tests", "estabilidad", "confiabilidad"]),

    (46, "Test Data Management",
     "Diseña una estrategia de test data: factories, seeds, cleanup y aislamiento entre tests.",
     "El test data sucio es la primera causa de tests no reproducibles. La gestión de data es infraestructura.",
     "## Test Data Management\n\n**Factories (no fixtures hardcodeados):**\n```ts\n// factories/user.factory.ts\nexport function createTestUser(overrides = {}) {\n  return {\n    callsign: `TEST_${Date.now()}`,  // único por run\n    email: `test_${Date.now()}@daki.io`,\n    password: 'TestPass123!',\n    ...overrides,\n  };\n}\n```\n\n**Cleanup Strategy:**\n```ts\ntest.afterEach(async ({ request }) => {\n  // Eliminar usuario creado en el test\n  await request.delete(`/api/v1/test/users/${testUserId}`,\n    { headers: { 'X-Test-Cleanup': process.env.TEST_SECRET! } }\n  );\n});\n```\n\n**Principio:** cada test crea su data, cada test la limpia.",
     "hard", 260, "estrategia_qa", ["test_data", "factories", "cleanup"]),

    (47, "Exploratory Testing Sistematizado",
     "Crea una sesión de testing exploratorio con charter, notas y reporte de hallazgos.",
     "El testing exploratorio sin estructura es navegar sin mapa. El charter lo convierte en misión.",
     "## Exploratory Testing Charter\n\n```markdown\n# Session Charter\n**Operador:** [nombre]\n**Fecha:** 2026-03-31\n**Duración:** 90 minutos\n**Área:** Flujo de onboarding — registro → hub → primera misión\n\n## Misión\nExplorar el flujo de nuevo usuario buscando:\n- Puntos de fricción en el registro\n- Mensajes de error confusos\n- Estados inesperados en el hub\n- Comportamiento con slow network\n\n## Notas (durante la sesión)\n- [10:03] Al crear usuario con callsign de 1 char → acepta sin error\n- [10:18] Hub muestra 'undefined' si la API tarda > 3s\n- [10:34] Back button desde la primera misión rompe el state\n\n## Bugs encontrados\n| ID | Descripción | Severidad |\n|----|-------------|----------|\n| BUG-47 | callsign sin validación mínima | HIGH |\n| BUG-48 | Hub state undefined en slow network | MEDIUM |\n```",
     "medium", 220, "estrategia_qa", ["exploratory_testing", "charter", "descubrimiento"]),

    (48, "Construir tu Portfolio QA",
     "Diseña un portfolio de QA Automation Engineer: qué proyectos incluir, cómo documentarlos, dónde publicarlos.",
     "El portfolio es tu primer test de QA como automation engineer. Si está mal documentado, falla la revisión.",
     "## Portfolio QA Automation\n\n**Proyectos esenciales:**\n```\n1. E2E Suite con Playwright\n   - GitHub: nombre-apellido/playwright-suite\n   - README: setup, arquitectura, cómo correr\n   - CI badge: GitHub Actions passing\n   - Demo: Loom video de 3 minutos\n\n2. API Test Suite\n   - Supertest + contract testing\n   - Coverage badge > 80%\n\n3. Pipeline CI/CD\n   - workflow completo documentado\n   - diagrama de flujo\n```\n\n**README template:**\n```markdown\n# [Nombre del Proyecto]\n\n## Stack\nPlaywright · TypeScript · GitHub Actions · Allure\n\n## Cobertura\n- 45 tests E2E\n- 30 tests de API\n- Matriz: Chromium + Firefox\n\n## Setup\nbash\nnpm install\nnpx playwright install\nnpm test\n\n```\n\n**Publicar en:** GitHub + LinkedIn artículo.",
     "medium", 240, "estrategia_qa", ["portfolio", "carrera", "documentación"]),

    (49, "De QA Manual a Automation — Plan de 90 Días",
     "Crea un plan de transición de 90 días: semana a semana, hitos, métricas de éxito.",
     "La transición no es un salto — es una escalera. Este plan es la escalera.",
     "## Plan de Transición — 90 Días\n\n**Mes 1: Fundamentos (semanas 1-4)**\n- Semana 1-2: TypeScript + Node básico\n- Semana 3-4: Primer script Playwright funcionando\n- Hito: 5 tests E2E automatizados del smoke test actual\n\n**Mes 2: Profundización (semanas 5-8)**\n- Semana 5-6: POM + Fixtures + API testing\n- Semana 7-8: Pipeline CI/CD básico\n- Hito: Suite en CI, reporte automático en cada PR\n\n**Mes 3: Consolidación (semanas 9-12)**\n- Semana 9-10: Métricas + estrategia + flaky management\n- Semana 11-12: Portfolio completo + primera aplicación\n- Hito: 3 aplicaciones enviadas como QA Automation Engineer\n\n**Métricas de éxito:**\n```\n✅ 50+ tests automatizados\n✅ Pipeline CI/CD propio\n✅ Portfolio en GitHub\n✅ 1 entrevista técnica superada\n```",
     "medium", 250, "estrategia_qa", ["plan_transición", "carrera", "90_días"]),

    (50, "CONTRATO-FINAL-50: Certification SPECTRE",
     "Proyecto final: suite completa con TypeScript + Playwright + API Testing + CI/CD + Allure Dashboard.",
     "Cincuenta misiones. Has completado el Protocolo SPECTRE. Ahora eres un QA Automation Engineer.",
     "## Proyecto Final — Certificación SPECTRE\n\n### Entregables\n\n**1. Repositorio GitHub**\n```\nqa-automation-spectre/\n  tests/\n    e2e/           # 20+ tests Playwright\n    api/           # 15+ tests Supertest\n    contracts/     # JSON Schema + Pact\n  pages/           # POM completo\n  fixtures/        # Auth + data fixtures\n  helpers/         # TypeScript helpers\n  .github/\n    workflows/\n      e2e.yml      # matrix chromium+firefox\n      api.yml      # coverage gate 80%\n      smoke.yml    # post-deploy\n  playwright.config.ts\n  jest.config.ts\n  README.md\n```\n\n**2. Métricas del proyecto**\n```\n✅ Coverage > 80%\n✅ Flaky rate < 2%\n✅ P95 latency documentado\n✅ Allure dashboard público\n✅ 0 secrets hardcodeados\n```\n\n**3. Documentación**\n```\n✅ Architecture Decision Records (ADR)\n✅ Test Strategy document\n✅ Runbook de ejecución local y CI\n```\n\n**Certificación SPECTRE concedida.**\nEl operador que completa este contrato no describe la calidad — la programa.",
     "hard", 1000, "estrategia_qa", ["certificación", "integración_total", "SPECTRE"]),
]

# ─── Build all 50 levels ──────────────────────────────────────────────────────

def _build() -> list[dict]:
    levels = []
    for group in [F1, F2, F3, F4, F5]:
        for item in group:
            levels.append(_level(*item))
    return levels

QA_AUTOMATION = _build()

# ─── Seed standalone ──────────────────────────────────────────────────────────

async def seed() -> None:
    import asyncio
    from sqlalchemy import delete
    from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
    from app.core.config import settings
    from app.models.challenge import Challenge

    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    Session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with Session() as session:
        deleted = await session.execute(
            delete(Challenge).where(Challenge.codex_id == "qa_automation_ops")
        )
        print(f"🧹  QA Automation anterior eliminado — {deleted.rowcount} challenge(s) removidos.")
        print(f"\n🌱  Insertando {len(QA_AUTOMATION)} niveles de QA Automation Ops...\n")
        for data in QA_AUTOMATION:
            session.add(Challenge(**data))
            if data["level_order"] % 10 == 0 or data["level_order"] <= 3:
                print(f"    [{data['level_order']:03d}] {data['title']:<60} ({data['difficulty'].upper()}, {data['base_xp_reward']} XP)")
        await session.commit()

    await engine.dispose()
    print(f"\n✅  QA Automation Ops — {len(QA_AUTOMATION)} niveles cargados.")
    print(f"    codex_id = 'qa_automation_ops'\n")


if __name__ == "__main__":
    import asyncio
    asyncio.run(seed())
