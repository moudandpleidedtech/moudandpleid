"""Fase 2 — TypeScript Operative (L09-L16)"""
from __future__ import annotations
import json

FASE2 = [
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ AUTO-009: GENERICS — FUNCIONES REUTILIZABLES TIPADAS ]",
"description": (
    "Implementa la función genérica `first<T>(arr: T[]): T | null` que retorna el primer elemento o null. "
    "Implementa `filterByProperty<T>(items: T[], key: keyof T, value: T[keyof T]): T[]` "
    "que retorna los elementos donde `items[key] === value`."
),
"difficulty_tier": 1, "difficulty": "easy",
"sector_id": None, "codex_id": "qa_automation_ops",
"level_order": 9, "base_xp_reward": 160,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 210, "challenge_type": "typescript",
"phase": "BRAVO", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["generics", "TypeScript", "keyof", "funciones_tipadas"]),
"initial_code": (
    "// TODO: implementa first<T>(arr: T[]): T | null\n"
    "// Retorna el primer elemento o null si el array está vacío\n"
    "function first<T>(arr: T[]): T | null {\n"
    "    // COMPLETAR\n"
    "    return null;\n"
    "}\n"
    "\n"
    "\n"
    "// TODO: implementa filterByProperty<T>(items, key, value)\n"
    "// Retorna los elementos donde items[key] === value\n"
    "function filterByProperty<T>(items: T[], key: keyof T, value: T[keyof T]): T[] {\n"
    "    // COMPLETAR\n"
    "    return [];\n"
    "}\n"
    "\n"
    "\n"
    "interface User {\n"
    "    id: number;\n"
    "    name: string;\n"
    "    role: 'ADMIN' | 'USER';\n"
    "}\n"
    "\n"
    "const users: User[] = [\n"
    "    { id: 1, name: 'Alice', role: 'ADMIN' },\n"
    "    { id: 2, name: 'Bob',   role: 'USER'  },\n"
    "    { id: 3, name: 'Carol', role: 'USER'  },\n"
    "];\n"
    "\n"
    "console.log(first(users)?.name);\n"
    "console.log(first<number>([]) ?? 'empty');\n"
    "console.log(filterByProperty(users, 'role', 'USER').length);\n"
    "console.log(filterByProperty(users, 'role', 'ADMIN')[0].name);\n"
),
"expected_output": "Alice\nempty\n2\nAlice",
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "TypeScript sin generics es JavaScript con sintaxis extra. "
    "Los generics permiten escribir una función una vez y usarla con cualquier tipo — "
    "el compilador garantiza que los tipos sean consistentes."
),
"theory_content": (
    "## Generics en TypeScript\n\n"
    "Un generic es un placeholder de tipo que se resuelve en el momento de uso:\n\n"
    "```typescript\n"
    "function first<T>(arr: T[]): T | null {\n"
    "    return arr.length > 0 ? arr[0] : null;\n"
    "}\n\n"
    "first([1, 2, 3])      // T = number → retorna 1\n"
    "first(['a', 'b'])     // T = string → retorna 'a'\n"
    "first([])             // T = never  → retorna null\n"
    "```\n\n"
    "**`keyof T`** — tipo que representa las claves de T. Si T = User, `keyof T = 'id' | 'name' | 'role'`\n"
    "**`?.`** — optional chaining: si `first(users)` es null, no lanza error, retorna undefined."
),
"pedagogical_objective": "Escribir funciones genéricas tipadas — base de cualquier helper de testing reutilizable.",
"syntax_hint": "`return arr.length > 0 ? arr[0] : null;` para first. Para filter: `return items.filter(item => item[key] === value);`",
"hints_json": json.dumps([
    "first: `return arr.length > 0 ? arr[0] : null;`",
    "filterByProperty: `return items.filter(item => item[key] === value);`",
    "`?? 'empty'` es el operador nullish coalescing: retorna 'empty' si el lado izquierdo es null o undefined.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ AUTO-010: PROMISE.ALL Y ALLSETTLED — ASYNC AVANZADO ]",
"description": (
    "Implementa `fetchUser(id)` que retorna `'User-{id}'` y `fetchPermissions(userId)` "
    "que retorna `['READ','WRITE','ADMIN']` si userId===1, si no `['READ']`. "
    "Completa `main()` usando `Promise.all` para obtener usuario+permisos en paralelo "
    "y `Promise.allSettled` para manejar resultados mixtos."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": None, "codex_id": "qa_automation_ops",
"level_order": 10, "base_xp_reward": 170,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 220, "challenge_type": "typescript",
"phase": "BRAVO", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["Promise.all", "Promise.allSettled", "async_await", "parallel"]),
"initial_code": (
    "async function fetchUser(id: number): Promise<string> {\n"
    "    // TODO: retorna `User-${id}`\n"
    "    return '';\n"
    "}\n"
    "\n"
    "async function fetchPermissions(userId: number): Promise<string[]> {\n"
    "    // TODO: retorna ['READ','WRITE','ADMIN'] si userId===1, si no ['READ']\n"
    "    return [];\n"
    "}\n"
    "\n"
    "\n"
    "async function main(): Promise<void> {\n"
    "    // TODO 1: Promise.all — obtén user y permissions en paralelo\n"
    "    // Imprime: `User: ${user}` y `Permissions: ${permissions.join(', ')}`\n"
    "    const [user, permissions] = await Promise.all([/* COMPLETAR */]);\n"
    "    console.log(`User: ${user}`);\n"
    "    console.log(`Permissions: ${permissions.join(', ')}`);\n"
    "\n"
    "    // TODO 2: Promise.allSettled — fetchUser(2), Promise.reject(new Error('DB timeout')), fetchUser(3)\n"
    "    // Por cada resultado: `Task N: OK — ${value}` o `Task N: FAILED — ${reason.message}`\n"
    "    const results = await Promise.allSettled([/* COMPLETAR */]);\n"
    "    results.forEach((result, i) => {\n"
    "        if (result.status === 'fulfilled') {\n"
    "            console.log(`Task ${i + 1}: OK \u2014 ${result.value}`);\n"
    "        } else {\n"
    "            console.log(`Task ${i + 1}: FAILED \u2014 ${(result.reason as Error).message}`);\n"
    "        }\n"
    "    });\n"
    "}\n"
    "\n"
    "main();\n"
),
"expected_output": (
    "User: User-1\n"
    "Permissions: READ, WRITE, ADMIN\n"
    "Task 1: OK \u2014 User-2\n"
    "Task 2: FAILED \u2014 DB timeout\n"
    "Task 3: OK \u2014 User-3"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "En QA de microservicios, múltiples APIs responden al mismo tiempo. "
    "`Promise.all` falla si cualquiera falla. `Promise.allSettled` recoge todos los resultados — "
    "tanto los exitosos como los fallidos — sin abortar."
),
"theory_content": (
    "## Promise.all vs Promise.allSettled\n\n"
    "```typescript\n"
    "// Promise.all — todos deben resolver; si uno rechaza, rechaza todo\n"
    "const [a, b] = await Promise.all([fetchA(), fetchB()]);\n\n"
    "// Promise.allSettled — recoge todos los resultados sin importar fallos\n"
    "const results = await Promise.allSettled([fetchA(), fetchB()]);\n"
    "results.forEach(r => {\n"
    "    if (r.status === 'fulfilled') console.log(r.value);\n"
    "    else console.log(r.reason.message);\n"
    "});\n"
    "```\n\n"
    "**Cuándo usar cada uno:**\n"
    "- `Promise.all`: necesitas TODOS los datos para continuar.\n"
    "- `Promise.allSettled`: quieres reportar qué falló sin detener el flujo."
),
"pedagogical_objective": "Dominar Promise.all y allSettled — esencial en tests de APIs paralelas.",
"syntax_hint": "`await Promise.all([fetchUser(1), fetchPermissions(1)])` para el primer bloque.",
"hints_json": json.dumps([
    "fetchUser: `return \\`User-${id}\\``",
    "fetchPermissions: `return userId === 1 ? ['READ','WRITE','ADMIN'] : ['READ']`",
    "Para allSettled: `Promise.allSettled([fetchUser(2), Promise.reject(new Error('DB timeout')), fetchUser(3)])`",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ AUTO-011: NODE.JS ENTORNO — PROCESS.ENV PARA TESTS ]",
"description": (
    "Implementa `loadConfig(): TestConfig` que lee variables de entorno y aplica defaults: "
    "`BASE_URL → 'http://localhost:3000'`, `TIMEOUT → 5000`, `HEADLESS → true`, `RETRIES → 2`. "
    "Para HEADLESS: string `'false'` = false, cualquier otro valor = true. "
    "Para TIMEOUT y RETRIES: parsear como número entero."
),
"difficulty_tier": 1, "difficulty": "easy",
"sector_id": None, "codex_id": "qa_automation_ops",
"level_order": 11, "base_xp_reward": 155,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 200, "challenge_type": "typescript",
"phase": "BRAVO", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["process.env", "environment_variables", "Node.js", "config"]),
"initial_code": (
    "interface TestConfig {\n"
    "    baseUrl: string;\n"
    "    timeout: number;\n"
    "    headless: boolean;\n"
    "    retries: number;\n"
    "}\n"
    "\n"
    "\n"
    "function loadConfig(): TestConfig {\n"
    "    // TODO: lee process.env y aplica defaults:\n"
    "    // BASE_URL  → 'http://localhost:3000'\n"
    "    // TIMEOUT   → 5000 (número)\n"
    "    // HEADLESS  → true (boolean; 'false' string = false)\n"
    "    // RETRIES   → 2 (número)\n"
    "    return {\n"
    "        baseUrl:  '',\n"
    "        timeout:  0,\n"
    "        headless: true,\n"
    "        retries:  0,\n"
    "    };\n"
    "}\n"
    "\n"
    "\n"
    "// Simular variables de entorno\n"
    "process.env.BASE_URL = 'https://staging.daki.io';\n"
    "process.env.TIMEOUT  = '10000';\n"
    "// HEADLESS y RETRIES no están seteados — deben usar defaults\n"
    "\n"
    "const config = loadConfig();\n"
    "console.log(`baseUrl: ${config.baseUrl}`);\n"
    "console.log(`timeout: ${config.timeout}`);\n"
    "console.log(`headless: ${config.headless}`);\n"
    "console.log(`retries: ${config.retries}`);\n"
),
"expected_output": (
    "baseUrl: https://staging.daki.io\n"
    "timeout: 10000\n"
    "headless: true\n"
    "retries: 2"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Un test suite que hardcodea URLs no sirve en CI. "
    "Las variables de entorno permiten que el mismo código corra en local, staging y producción "
    "sin modificar una línea."
),
"theory_content": (
    "## process.env en Node.js/TypeScript\n\n"
    "```typescript\n"
    "const baseUrl = process.env.BASE_URL ?? 'http://localhost:3000';\n"
    "const timeout = parseInt(process.env.TIMEOUT ?? '5000', 10);\n"
    "const headless = process.env.HEADLESS !== 'false'; // 'false' → false, todo lo demás → true\n"
    "```\n\n"
    "**`??` (nullish coalescing)** — retorna el lado derecho si el izquierdo es `null` o `undefined`.\n"
    "**`parseInt(str, 10)`** — convierte string a número entero en base 10.\n\n"
    "En CI/CD (GitHub Actions, Render), las variables de entorno se inyectan en el workflow."
),
"pedagogical_objective": "Gestionar configuración por entorno con process.env — práctica estándar en automation.",
"syntax_hint": "`const headless = process.env.HEADLESS !== 'false';` — si no está seteado, `undefined !== 'false'` = true.",
"hints_json": json.dumps([
    "baseUrl: `process.env.BASE_URL ?? 'http://localhost:3000'`",
    "timeout: `parseInt(process.env.TIMEOUT ?? '5000', 10)`",
    "headless: `process.env.HEADLESS !== 'false'` — undefined !== 'false' es true (default correcto).",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ AUTO-012: VALIDADOR DE PACKAGE.JSON ]",
"description": (
    "Implementa `validatePackage(pkg: PackageJson): string[]` que retorna una lista de problemas. "
    "Valida: name no vacío, scripts con `'test'`, `'test:e2e'`, `'test:api'`, "
    "devDependencies con `'@playwright/test'` y `'typescript'`. "
    "Mensajes: `'name cannot be empty'`, `'missing script: <name>'`, `'missing devDependency: <name>'`."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": None, "codex_id": "qa_automation_ops",
"level_order": 12, "base_xp_reward": 165,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 215, "challenge_type": "typescript",
"phase": "BRAVO", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["npm", "package.json", "validación", "Record", "proyectos_QA"]),
"initial_code": (
    "interface PackageJson {\n"
    "    name: string;\n"
    "    version: string;\n"
    "    scripts: Record<string, string>;\n"
    "    devDependencies: Record<string, string>;\n"
    "}\n"
    "\n"
    "\n"
    "function validatePackage(pkg: PackageJson): string[] {\n"
    "    const issues: string[] = [];\n"
    "    // TODO: valida name, scripts requeridos y devDependencies requeridas\n"
    "    // Scripts requeridos: 'test', 'test:e2e', 'test:api'\n"
    "    // DevDeps requeridas: '@playwright/test', 'typescript'\n"
    "    return issues;\n"
    "}\n"
    "\n"
    "\n"
    "const validPkg: PackageJson = {\n"
    "    name: 'qa-nexo-suite',\n"
    "    version: '1.0.0',\n"
    "    scripts: { 'test': 'jest', 'test:e2e': 'playwright test', 'test:api': 'jest --testPathPattern=api' },\n"
    "    devDependencies: { '@playwright/test': '^1.40.0', 'typescript': '^5.0.0', 'jest': '^29.0.0' },\n"
    "};\n"
    "\n"
    "const invalidPkg: PackageJson = {\n"
    "    name: '',\n"
    "    version: '0.0.1',\n"
    "    scripts: { 'test': 'jest' },\n"
    "    devDependencies: { 'jest': '^29.0.0' },\n"
    "};\n"
    "\n"
    "const v1 = validatePackage(validPkg);\n"
    "const v2 = validatePackage(invalidPkg);\n"
    "\n"
    "console.log(`Valid pkg: ${v1.length === 0 ? 'OK' : v1.join(', ')}`);\n"
    "v2.forEach(err => console.log(`Issue: ${err}`));\n"
),
"expected_output": (
    "Valid pkg: OK\n"
    "Issue: name cannot be empty\n"
    "Issue: missing script: test:e2e\n"
    "Issue: missing script: test:api\n"
    "Issue: missing devDependency: @playwright/test\n"
    "Issue: missing devDependency: typescript"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Un proyecto de QA Automation sin las dependencias correctas es un proyecto roto. "
    "El validador de package.json es el primer check del pipeline: "
    "si Playwright y TypeScript no están declarados, el CI ni empieza."
),
"theory_content": (
    "## Validar package.json programáticamente\n\n"
    "```typescript\n"
    "const requiredScripts = ['test', 'test:e2e', 'test:api'];\n"
    "requiredScripts.forEach(script => {\n"
    "    if (!pkg.scripts[script]) {\n"
    "        issues.push(`missing script: ${script}`);\n"
    "    }\n"
    "});\n"
    "```\n\n"
    "**`in` operator vs `!obj[key]`:**\n"
    "Usa `!(key in obj)` para verificar que la clave no existe. "
    "`!obj[key]` también falla si el valor es `''` o `0`."
),
"pedagogical_objective": "Validar configuraciones de proyecto — skill de QA Lead al onboardear nuevos repositorios.",
"syntax_hint": "`if (!pkg.name) issues.push('name cannot be empty')` — string vacío es falsy en JS.",
"hints_json": json.dumps([
    "Name: `if (!pkg.name) issues.push('name cannot be empty')`",
    "Scripts: `['test','test:e2e','test:api'].forEach(s => { if (!(s in pkg.scripts)) issues.push(\\`missing script: ${s}\\`) })`",
    "DevDeps: igual con `['@playwright/test','typescript']` y `'missing devDependency: ...'`",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ AUTO-013: ERROR HANDLING ASYNC — TRY/CATCH EN TESTS ]",
"description": (
    "Implementa `safeGet(client, endpoint)` que llama `client.get(endpoint)` con await. "
    "Si la promesa rechaza (throw): imprime `'ERROR: <message>'` y retorna null. "
    "Si `status >= 400`: imprime `'HTTP <status>: <data.error>'` y retorna null. "
    "Si OK: imprime `'OK <status>: <JSON.stringify(data)>'` y retorna la respuesta."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": None, "codex_id": "qa_automation_ops",
"level_order": 13, "base_xp_reward": 175,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 220, "challenge_type": "typescript",
"phase": "BRAVO", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["try_catch", "async_await", "error_handling", "HTTP_errors"]),
"initial_code": (
    "class APIClient {\n"
    "    async get(endpoint: string): Promise<{ status: number; data: unknown }> {\n"
    "        if (endpoint === '/health') return { status: 200, data: { ok: true } };\n"
    "        if (endpoint === '/auth')   return { status: 401, data: { error: 'Unauthorized' } };\n"
    "        if (endpoint === '/crash')  throw new Error('Network error: connection refused');\n"
    "        return { status: 404, data: { error: 'Not found' } };\n"
    "    }\n"
    "}\n"
    "\n"
    "\n"
    "async function safeGet(client: APIClient, endpoint: string) {\n"
    "    // TODO:\n"
    "    // try { const resp = await client.get(endpoint) }\n"
    "    // Si resp.status >= 400: imprime 'HTTP <status>: <(resp.data as any).error>'\n"
    "    // Si OK: imprime 'OK <status>: <JSON.stringify(resp.data)>'\n"
    "    // catch (err): imprime 'ERROR: <(err as Error).message>'\n"
    "    // Retorna null en caso de error o status >= 400, resp en caso de éxito\n"
    "}\n"
    "\n"
    "\n"
    "async function main() {\n"
    "    const client = new APIClient();\n"
    "    await safeGet(client, '/health');\n"
    "    await safeGet(client, '/auth');\n"
    "    await safeGet(client, '/crash');\n"
    "    await safeGet(client, '/missing');\n"
    "}\n"
    "\n"
    "main();\n"
),
"expected_output": (
    'OK 200: {"ok":true}\n'
    "HTTP 401: Unauthorized\n"
    "ERROR: Network error: connection refused\n"
    "HTTP 404: Not found"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Los tests que lanzan excepciones no controladas matan el runner. "
    "En QA de APIs, envuelves cada request en un `try/catch` — "
    "así un endpoint caído no aborta toda la suite."
),
"theory_content": (
    "## try/catch con async/await\n\n"
    "```typescript\n"
    "async function safeGet(client: APIClient, endpoint: string) {\n"
    "    try {\n"
    "        const resp = await client.get(endpoint);\n"
    "        if (resp.status >= 400) {\n"
    "            console.log(`HTTP ${resp.status}: ${(resp.data as any).error}`);\n"
    "            return null;\n"
    "        }\n"
    "        console.log(`OK ${resp.status}: ${JSON.stringify(resp.data)}`);\n"
    "        return resp;\n"
    "    } catch (err) {\n"
    "        console.log(`ERROR: ${(err as Error).message}`);\n"
    "        return null;\n"
    "    }\n"
    "}\n"
    "```\n\n"
    "**`(err as Error).message`** — TypeScript requiere castear `unknown` a `Error` para acceder a `.message`."
),
"pedagogical_objective": "Manejar errores async en tests de API sin abortar el runner.",
"syntax_hint": "`(resp.data as any).error` para acceder a la propiedad error del body.",
"hints_json": json.dumps([
    "Estructura: `try { const resp = await client.get(endpoint); if (resp.status >= 400) { ... } else { ... } } catch (err) { ... }`",
    "Error HTTP: `console.log(\\`HTTP ${resp.status}: ${(resp.data as any).error}\\`)`",
    "Catch: `console.log(\\`ERROR: ${(err as Error).message}\\`)`",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ AUTO-014: ARRAY UTILITIES — FILTER, MAP, REDUCE EN TEST DATA ]",
"description": (
    "Implementa las tres funciones usando métodos de array: "
    "`getFailedTests(runs)` retorna IDs de tests fallidos. "
    "`getSuiteSummary(runs)` retorna `Record<suite, {pass, fail}>`. "
    "`getTotalDuration(runs)` suma todas las duraciones."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": None, "codex_id": "qa_automation_ops",
"level_order": 14, "base_xp_reward": 170,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 220, "challenge_type": "typescript",
"phase": "BRAVO", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["filter", "map", "reduce", "array_methods", "test_data"]),
"initial_code": (
    "interface TestRun {\n"
    "    id: string;\n"
    "    status: 'PASS' | 'FAIL' | 'SKIP';\n"
    "    duration: number;\n"
    "    suite: string;\n"
    "}\n"
    "\n"
    "\n"
    "function getFailedTests(runs: TestRun[]): string[] {\n"
    "    // TODO: retorna array de IDs donde status === 'FAIL'\n"
    "    return [];\n"
    "}\n"
    "\n"
    "function getSuiteSummary(runs: TestRun[]): Record<string, { pass: number; fail: number }> {\n"
    "    // TODO: agrupa por suite y cuenta PASS y FAIL\n"
    "    // Usa reduce para construir el objeto\n"
    "    return {};\n"
    "}\n"
    "\n"
    "function getTotalDuration(runs: TestRun[]): number {\n"
    "    // TODO: suma todas las duraciones con reduce\n"
    "    return 0;\n"
    "}\n"
    "\n"
    "\n"
    "const runs: TestRun[] = [\n"
    "    { id: 'T01', status: 'PASS', duration: 200,  suite: 'auth'      },\n"
    "    { id: 'T02', status: 'FAIL', duration: 450,  suite: 'auth'      },\n"
    "    { id: 'T03', status: 'PASS', duration: 120,  suite: 'dashboard' },\n"
    "    { id: 'T04', status: 'FAIL', duration: 800,  suite: 'dashboard' },\n"
    "    { id: 'T05', status: 'SKIP', duration:   0,  suite: 'auth'      },\n"
    "];\n"
    "\n"
    "console.log(`Failed: ${getFailedTests(runs).join(', ')}`);\n"
    "const summary = getSuiteSummary(runs);\n"
    "console.log(`auth: ${summary.auth.pass}P ${summary.auth.fail}F`);\n"
    "console.log(`dashboard: ${summary.dashboard.pass}P ${summary.dashboard.fail}F`);\n"
    "console.log(`Total duration: ${getTotalDuration(runs)}ms`);\n"
),
"expected_output": (
    "Failed: T02, T04\n"
    "auth: 1P 1F\n"
    "dashboard: 1P 1F\n"
    "Total duration: 1570ms"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Los datos de un test run son un array de resultados. "
    "filter, map y reduce son las tres operaciones que cubren el 90% del procesamiento — "
    "sin loops, sin variables mutables, sin bugs ocultos."
),
"theory_content": (
    "## filter / map / reduce — El trío de arrays\n\n"
    "```typescript\n"
    "// filter: subconjunto\n"
    "const failed = runs.filter(r => r.status === 'FAIL').map(r => r.id);\n\n"
    "// reduce: acumular en un objeto\n"
    "const summary = runs.reduce((acc, run) => {\n"
    "    if (!acc[run.suite]) acc[run.suite] = { pass: 0, fail: 0 };\n"
    "    if (run.status === 'PASS') acc[run.suite].pass++;\n"
    "    if (run.status === 'FAIL') acc[run.suite].fail++;\n"
    "    return acc;\n"
    "}, {} as Record<string, { pass: number; fail: number }>);\n\n"
    "// reduce: sumar\n"
    "const total = runs.reduce((sum, r) => sum + r.duration, 0);\n"
    "```"
),
"pedagogical_objective": "Procesar datos de test runs con array methods — skills diarios de un automation engineer.",
"syntax_hint": "getFailedTests: `.filter(r => r.status === 'FAIL').map(r => r.id)`",
"hints_json": json.dumps([
    "getFailedTests: `return runs.filter(r => r.status === 'FAIL').map(r => r.id);`",
    "getSuiteSummary: usa reduce con `acc[run.suite] = acc[run.suite] || { pass: 0, fail: 0 }` luego incrementa.",
    "getTotalDuration: `return runs.reduce((sum, r) => sum + r.duration, 0);`",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ AUTO-015: TYPE UTILITIES — PARTIAL, PICK, OMIT, RECORD ]",
"description": (
    "Implementa `createUserDraft(overrides)` que mezcla defaults con overrides usando spread. "
    "Implementa `toLoginInfo(user)` que extrae solo `id` y `email`. "
    "`sanitizeForLog` ya está implementada. "
    "Implementa `buildRoleMap(users)` que agrupa usuarios por role en un `Record<string, User[]>`."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": None, "codex_id": "qa_automation_ops",
"level_order": 15, "base_xp_reward": 175,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 230, "challenge_type": "typescript",
"phase": "BRAVO", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["Partial", "Pick", "Omit", "Record", "spread", "type_utilities"]),
"initial_code": (
    "interface User {\n"
    "    id: number;\n"
    "    email: string;\n"
    "    name: string;\n"
    "    role: 'ADMIN' | 'USER';\n"
    "    createdAt: string;\n"
    "}\n"
    "\n"
    "\n"
    "function createUserDraft(overrides: Partial<User> = {}): User {\n"
    "    // TODO: retorna un User con estos defaults + overrides:\n"
    "    // id:0, email:'draft@test.io', name:'Draft User', role:'USER', createdAt:'2026-01-01'\n"
    "    return {} as User;\n"
    "}\n"
    "\n"
    "function toLoginInfo(user: User): Pick<User, 'id' | 'email'> {\n"
    "    // TODO: retorna solo { id, email }\n"
    "    return {} as Pick<User, 'id' | 'email'>;\n"
    "}\n"
    "\n"
    "function sanitizeForLog(user: User): Omit<User, 'email'> {\n"
    "    const { email, ...rest } = user;  // email removido\n"
    "    return rest;\n"
    "}\n"
    "\n"
    "function buildRoleMap(users: User[]): Record<string, User[]> {\n"
    "    // TODO: agrupa por role usando reduce\n"
    "    return {};\n"
    "}\n"
    "\n"
    "\n"
    "const testUser = createUserDraft({ name: 'Test Operator', role: 'ADMIN' });\n"
    "const loginInfo = toLoginInfo(testUser);\n"
    "const safeLog = sanitizeForLog(testUser);\n"
    "const roleMap = buildRoleMap([testUser, createUserDraft({ role: 'USER' })]);\n"
    "\n"
    "console.log(`Draft: ${testUser.name} (${testUser.role}) id=${testUser.id}`);\n"
    "console.log(`Login: id=${loginInfo.id} email=${loginInfo.email}`);\n"
    "console.log(`Safe log fields: ${Object.keys(safeLog).sort().join(', ')}`);\n"
    "console.log(`ADMIN count: ${roleMap['ADMIN'].length}`);\n"
    "console.log(`USER count: ${roleMap['USER'].length}`);\n"
),
"expected_output": (
    "Draft: Test Operator (ADMIN) id=0\n"
    "Login: id=0 email=draft@test.io\n"
    "Safe log fields: createdAt, id, name, role\n"
    "ADMIN count: 1\n"
    "USER count: 1"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "En test data management, necesitas crear objetos con mínima fricción. "
    "`Partial<T>` permite sobrescribir solo lo que necesitas. "
    "`Pick` y `Omit` evitan exponer datos sensibles en los logs."
),
"theory_content": (
    "## Type Utilities de TypeScript\n\n"
    "```typescript\n"
    "// Partial<T> — todos los campos opcionales\n"
    "function createDraft(overrides: Partial<User> = {}): User {\n"
    "    return { id: 0, email: 'draft@test.io', ...overrides };\n"
    "}\n\n"
    "// Pick<T, K> — solo esos campos\n"
    "function toLoginInfo(user: User): Pick<User, 'id' | 'email'> {\n"
    "    return { id: user.id, email: user.email };\n"
    "}\n\n"
    "// Omit<T, K> — todos los campos EXCEPTO esos\n"
    "const { email, ...safe } = user; // destructuring\n"
    "```\n\n"
    "**Spread para merge de defaults:** `{ ...defaults, ...overrides }` — overrides sobreescribe defaults."
),
"pedagogical_objective": "Usar type utilities para manejar test data de forma tipada y segura.",
"syntax_hint": "createUserDraft: `return { id:0, email:'draft@test.io', name:'Draft User', role:'USER', createdAt:'2026-01-01', ...overrides }`",
"hints_json": json.dumps([
    "createUserDraft: `return { id:0, email:'draft@test.io', name:'Draft User', role:'USER', createdAt:'2026-01-01', ...overrides };`",
    "toLoginInfo: `return { id: user.id, email: user.email };`",
    "buildRoleMap: `return users.reduce((acc, u) => { acc[u.role] = [...(acc[u.role] || []), u]; return acc; }, {} as Record<string, User[]>);`",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ AUTO-016 \u221e BOSS: TEST DATA FACTORY — GENERADOR TIPADO ]",
"description": (
    "Implementa la clase `TestUserFactory` completa:\n"
    "- constructor: inicializa contador interno en 1\n"
    "- `create(overrides?)`: crea User con id auto-incremental, `email='user{id}@test.io'`, "
    "`status='active'`, `permissions=['READ']` + overrides\n"
    "- `createAdmin()`: como create() pero `email='admin{id}@test.io'`, `permissions=['READ','WRITE','ADMIN']`\n"
    "- `createBatch(n)`: retorna array de n usuarios con defaults\n"
    "- `reset()`: reinicia el contador a 1"
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": None, "codex_id": "qa_automation_ops",
"level_order": 16, "base_xp_reward": 280,
"is_project": False, "is_phase_boss": True,
"telemetry_goal_time": 300, "challenge_type": "typescript",
"phase": "BRAVO", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["Factory pattern", "auto-increment", "test data", "OOP", "TypeScript"]),
"initial_code": (
    "type Status = 'active' | 'inactive' | 'suspended';\n"
    "\n"
    "interface UserFactory {\n"
    "    id: number;\n"
    "    email: string;\n"
    "    status: Status;\n"
    "    permissions: string[];\n"
    "}\n"
    "\n"
    "\n"
    "class TestUserFactory {\n"
    "    private counter: number = 1;\n"
    "\n"
    "    create(overrides: Partial<UserFactory> = {}): UserFactory {\n"
    "        // TODO: crea user con id=this.counter (luego incrementa),\n"
    "        // email='user{id}@test.io', status='active', permissions=['READ']\n"
    "        // aplica overrides con spread\n"
    "        return {} as UserFactory;\n"
    "    }\n"
    "\n"
    "    createAdmin(): UserFactory {\n"
    "        // TODO: usa this.counter para el id, email='admin{id}@test.io',\n"
    "        // permissions=['READ','WRITE','ADMIN'], status='active'\n"
    "        // incrementa el contador\n"
    "        return {} as UserFactory;\n"
    "    }\n"
    "\n"
    "    createBatch(n: number): UserFactory[] {\n"
    "        // TODO: crea n usuarios con create()\n"
    "        return [];\n"
    "    }\n"
    "\n"
    "    reset(): void {\n"
    "        // TODO: reinicia this.counter a 1\n"
    "    }\n"
    "}\n"
    "\n"
    "\n"
    "const factory = new TestUserFactory();\n"
    "\n"
    "const u1 = factory.create();\n"
    "const u2 = factory.create({ status: 'inactive', permissions: ['READ', 'WRITE'] });\n"
    "const admin = factory.createAdmin();\n"
    "\n"
    "console.log(`U1: ${u1.email} | ${u1.status} | [${u1.permissions.join(',')}]`);\n"
    "console.log(`U2: ${u2.email} | ${u2.status} | [${u2.permissions.join(',')}]`);\n"
    "console.log(`Admin: ${admin.email} | [${admin.permissions.join(',')}]`);\n"
    "\n"
    "factory.reset();\n"
    "const batch = factory.createBatch(3);\n"
    "console.log(`Batch size: ${batch.length}`);\n"
    "console.log(`Batch[0]: ${batch[0].email}`);\n"
    "console.log(`Batch[2]: ${batch[2].email}`);\n"
),
"expected_output": (
    "U1: user1@test.io | active | [READ]\n"
    "U2: user2@test.io | inactive | [READ,WRITE]\n"
    "Admin: admin3@test.io | [READ,WRITE,ADMIN]\n"
    "Batch size: 3\n"
    "Batch[0]: user1@test.io\n"
    "Batch[2]: user3@test.io"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "\u221e BOSS BRAVO \u2014 El sistema de roles del Nexo requiere 50 usuarios de prueba con combinaciones específicas. "
    "Crear cada uno a mano es un error esperando ocurrir. "
    "La Factory genera usuarios determinísticos, reutilizables y fáciles de auditar."
),
"theory_content": (
    "## Factory Pattern para Test Data\n\n"
    "```typescript\n"
    "class TestUserFactory {\n"
    "    private counter = 1;\n\n"
    "    create(overrides: Partial<UserFactory> = {}): UserFactory {\n"
    "        const id = this.counter++;\n"
    "        return {\n"
    "            id,\n"
    "            email: `user${id}@test.io`,\n"
    "            status: 'active',\n"
    "            permissions: ['READ'],\n"
    "            ...overrides,  // overrides después para sobreescribir\n"
    "        };\n"
    "    }\n"
    "}\n"
    "```\n\n"
    "**El orden del spread importa:** `{ defaults, ...overrides }` → overrides sobreescribe defaults.\n"
    "**`this.counter++`** — post-incremento: usa el valor actual, luego incrementa."
),
"pedagogical_objective": "Implementar el Factory Pattern para test data — elimina hardcoding y duplicación.",
"syntax_hint": "En create(): `const id = this.counter++;` luego `return { id, email: \\`user${id}@test.io\\`, ..., ...overrides }`",
"hints_json": json.dumps([
    "create: `const id = this.counter++; return { id, email: \\`user${id}@test.io\\`, status: 'active', permissions: ['READ'], ...overrides };`",
    "createAdmin: similar pero email=`admin${id}@test.io` y permissions=['READ','WRITE','ADMIN'] — NO aplica overrides.",
    "createBatch: `return Array.from({ length: n }, () => this.create());` o un loop con push.",
]),
"grid_map_json": None,
},
]
