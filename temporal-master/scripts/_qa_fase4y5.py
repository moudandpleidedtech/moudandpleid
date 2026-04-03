"""Fases 4 (L28-L35) y 5 (L36-L40)"""
from __future__ import annotations
import json

FASE4 = [
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ AUTO-028: HTTP FUNDAMENTALS PARA TESTERS ]",
"description": (
    "Implementa los tres métodos de `HttpAnalyzer`:\n"
    "- `categorizeStatus(code)`: 2xx→`'SUCCESS'`, 3xx→`'REDIRECT'`, 4xx→`'CLIENT_ERROR'`, 5xx→`'SERVER_ERROR'`, otro→`'UNKNOWN'`\n"
    "- `parseContentType(header)`: extrae type y charset (`'utf-8'` por default si no hay charset)\n"
    "- `isIdempotent(method)`: GET, HEAD, PUT, DELETE, OPTIONS → true; POST, PATCH → false"
),
"difficulty_tier": 1, "difficulty": "easy",
"sector_id": None, "codex_id": "qa_automation_ops",
"level_order": 28, "base_xp_reward": 165,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 210, "challenge_type": "typescript",
"phase": "DELTA_API", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["HTTP", "status_codes", "content_type", "idempotencia"]),
"initial_code": (
    "class HttpAnalyzer {\n"
    "    categorizeStatus(code: number): string {\n"
    "        // TODO: 2xx→SUCCESS, 3xx→REDIRECT, 4xx→CLIENT_ERROR, 5xx→SERVER_ERROR, otro→UNKNOWN\n"
    "        return 'UNKNOWN';\n"
    "    }\n"
    "\n"
    "    parseContentType(header: string): { type: string; charset: string } {\n"
    "        // TODO: divide por '; ' — primer parte es type, segunda tiene 'charset=<val>'\n"
    "        // Si no hay charset: default 'utf-8'\n"
    "        return { type: '', charset: '' };\n"
    "    }\n"
    "\n"
    "    isIdempotent(method: string): boolean {\n"
    "        // TODO: GET, HEAD, PUT, DELETE, OPTIONS → true; POST, PATCH → false\n"
    "        return false;\n"
    "    }\n"
    "}\n"
    "\n"
    "\n"
    "const analyzer = new HttpAnalyzer();\n"
    "\n"
    "[200, 201, 301, 404, 429, 500, 503].forEach(code => {\n"
    "    console.log(`${code}: ${analyzer.categorizeStatus(code)}`);\n"
    "});\n"
    "\n"
    "const ct1 = analyzer.parseContentType('application/json; charset=utf-8');\n"
    "const ct2 = analyzer.parseContentType('text/html');\n"
    "console.log(`CT1: ${ct1.type} / ${ct1.charset}`);\n"
    "console.log(`CT2: ${ct2.type} / ${ct2.charset}`);\n"
    "\n"
    "['GET', 'POST', 'PUT', 'DELETE', 'PATCH'].forEach(method => {\n"
    "    console.log(`${method}: idempotent=${analyzer.isIdempotent(method)}`);\n"
    "});\n"
),
"expected_output": (
    "200: SUCCESS\n"
    "201: SUCCESS\n"
    "301: REDIRECT\n"
    "404: CLIENT_ERROR\n"
    "429: CLIENT_ERROR\n"
    "500: SERVER_ERROR\n"
    "503: SERVER_ERROR\n"
    "CT1: application/json / utf-8\n"
    "CT2: text/html / utf-8\n"
    "GET: idempotent=true\n"
    "POST: idempotent=false\n"
    "PUT: idempotent=true\n"
    "DELETE: idempotent=true\n"
    "PATCH: idempotent=false"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Un QA que no conoce HTTP es un QA que adivina. "
    "Status codes, content types e idempotencia son el vocabulario básico — "
    "sin ellos, no puedes diseñar casos de prueba correctos para APIs."
),
"theory_content": (
    "## HTTP Fundamentals para QA\n\n"
    "**Status codes:**\n"
    "- `2xx` — éxito (200 OK, 201 Created, 204 No Content)\n"
    "- `3xx` — redirección (301 Moved, 302 Found)\n"
    "- `4xx` — error del cliente (400 Bad Request, 401 Unauthorized, 404 Not Found)\n"
    "- `5xx` — error del servidor (500 Internal Server Error, 503 Service Unavailable)\n\n"
    "**Idempotencia:** una operación es idempotente si aplicarla N veces tiene el mismo resultado que aplicarla 1 vez.\n"
    "- GET/DELETE: idempotentes (pedir el mismo recurso N veces = mismo resultado)\n"
    "- POST: NO idempotente (crear el mismo recurso N veces = N recursos)"
),
"pedagogical_objective": "Dominar los fundamentos HTTP — prerequisito para cualquier API testing profesional.",
"syntax_hint": "`Math.floor(code / 100)` te da el primer dígito del status code.",
"hints_json": json.dumps([
    "categorizeStatus: `const cat = Math.floor(code / 100); if (cat === 2) return 'SUCCESS'; if (cat === 3) return 'REDIRECT'; ...`",
    "parseContentType: `const parts = header.split('; '); const type = parts[0]; const charsetPart = parts.find(p => p.startsWith('charset=')); const charset = charsetPart ? charsetPart.split('=')[1] : 'utf-8';`",
    "isIdempotent: `return ['GET','HEAD','PUT','DELETE','OPTIONS'].includes(method);`",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ AUTO-029: SUPERTEST — FLUENT API TESTING ]",
"description": (
    "Implementa `SupertestClient` con API fluent:\n"
    "- `get(path)` y `post(path, body)`: configuran la request y ejecutan inmediatamente contra el server\n"
    "- `expect(status)`: verifica el status e imprime `'ASSERT status: <exp> got <actual> → PASS/FAIL'`\n"
    "- `expectBody(key, value)`: verifica body[key] e imprime `'ASSERT body.<key>: <exp> got <actual> → PASS/FAIL'`\n"
    "- `end()`: retorna la respuesta almacenada"
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": None, "codex_id": "qa_automation_ops",
"level_order": 29, "base_xp_reward": 195,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 250, "challenge_type": "typescript",
"phase": "DELTA_API", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["supertest", "fluent_API", "API_testing", "method_chaining"]),
"initial_code": (
    "interface MockResponse {\n"
    "    status: number;\n"
    "    body:   Record<string, unknown>;\n"
    "}\n"
    "\n"
    "class TestServer {\n"
    "    private routes = new Map<string, MockResponse>([\n"
    "        ['GET /api/status',    { status: 200, body: { ok: true, version: '2.0' }  }],\n"
    "        ['POST /api/auth',     { status: 200, body: { token: 'jwt-abc' }          }],\n"
    "        ['POST /api/auth/bad', { status: 401, body: { error: 'Invalid' }          }],\n"
    "    ]);\n"
    "\n"
    "    handle(method: string, path: string): MockResponse {\n"
    "        return this.routes.get(`${method} ${path}`) ?? { status: 404, body: { error: 'Not found' } };\n"
    "    }\n"
    "}\n"
    "\n"
    "\n"
    "class SupertestClient {\n"
    "    private _response: MockResponse | null = null;\n"
    "\n"
    "    constructor(private server: TestServer) {}\n"
    "\n"
    "    get(path: string): this {\n"
    "        // TODO: llama this.server.handle('GET', path) y guarda en this._response\n"
    "        return this;\n"
    "    }\n"
    "\n"
    "    post(path: string, _body?: unknown): this {\n"
    "        // TODO: igual con 'POST'\n"
    "        return this;\n"
    "    }\n"
    "\n"
    "    expect(status: number): this {\n"
    "        // TODO: imprime 'ASSERT status: <status> got <actual> → PASS' o 'FAIL'\n"
    "        return this;\n"
    "    }\n"
    "\n"
    "    expectBody(key: string, value: unknown): this {\n"
    "        // TODO: imprime 'ASSERT body.<key>: <value> got <actual> → PASS' o 'FAIL'\n"
    "        return this;\n"
    "    }\n"
    "\n"
    "    end(): MockResponse | null {\n"
    "        return this._response;\n"
    "    }\n"
    "}\n"
    "\n"
    "\n"
    "const server = new TestServer();\n"
    "const client = new SupertestClient(server);\n"
    "\n"
    "client.get('/api/status').expect(200).expectBody('ok', true).end();\n"
    "client.post('/api/auth', { password: 'nexo-2099' }).expect(200).expectBody('token', 'jwt-abc').end();\n"
    "client.post('/api/auth/bad', { password: 'wrong' }).expect(401).end();\n"
),
"expected_output": (
    "ASSERT status: 200 got 200 \u2192 PASS\n"
    "ASSERT body.ok: true got true \u2192 PASS\n"
    "ASSERT status: 200 got 200 \u2192 PASS\n"
    "ASSERT body.token: jwt-abc got jwt-abc \u2192 PASS\n"
    "ASSERT status: 401 got 401 \u2192 PASS"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "supertest es la librería estándar para testear APIs Node.js. "
    "Su API fluent permite encadenar el método, las assertions y la ejecución en una sola línea. "
    "Aquí la implementamos para entender el patrón por dentro."
),
"theory_content": (
    "## supertest en la vida real\n\n"
    "```typescript\n"
    "import request from 'supertest';\n"
    "import app from '../app';\n\n"
    "describe('GET /api/users', () => {\n"
    "    it('retorna 200 con lista de usuarios', async () => {\n"
    "        const response = await request(app)\n"
    "            .get('/api/users')\n"
    "            .set('Authorization', 'Bearer token')\n"
    "            .expect(200);\n\n"
    "        expect(response.body).toHaveLength(3);\n"
    "    });\n"
    "});\n"
    "```\n\n"
    "supertest levanta el servidor Express/Fastify en memoria — no necesita un puerto real."
),
"pedagogical_objective": "Implementar una API fluent de testing — entiende el patrón que usa supertest.",
"syntax_hint": "En get(): `this._response = this.server.handle('GET', path); return this;`",
"hints_json": json.dumps([
    "get: `this._response = this.server.handle('GET', path); return this;`",
    "expect: `const actual = this._response?.status ?? 0; const pass = actual === status; console.log(\\`ASSERT status: ${status} got ${actual} → ${pass ? 'PASS' : 'FAIL'}\\`); return this;`",
    "expectBody: `const actual = this._response?.body[key]; const pass = actual === value; console.log(\\`ASSERT body.${key}: ${value} got ${actual} → ${pass ? 'PASS' : 'FAIL'}\\`); return this;`",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ AUTO-030: JWT AUTH TESTING — ANÁLISIS DE TOKENS ]",
"description": (
    "Implementa `analyzeToken(token)` que divide por `'.'`, verifica que tenga 3 partes, "
    "usa `mockDecode()` para obtener header y payload, extrae los campos relevantes "
    "y determina si el token está expirado (exp < 1000000000 = pasado, exp > 9000000000 = futuro)."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": None, "codex_id": "qa_automation_ops",
"level_order": 30, "base_xp_reward": 200,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 250, "challenge_type": "typescript",
"phase": "DELTA_API", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["JWT", "auth_testing", "token_validation", "claims"]),
"initial_code": (
    "interface JWTAnalysis {\n"
    "    isValid:      boolean;\n"
    "    parts:        number;\n"
    "    headerAlg?:   string;\n"
    "    payloadSub?:  string;\n"
    "    payloadRole?: string;\n"
    "    isExpired?:   boolean;\n"
    "}\n"
    "\n"
    "// Decodificador simulado para el sandbox\n"
    "function mockDecode(part: string): Record<string, unknown> {\n"
    "    const map: Record<string, Record<string, unknown>> = {\n"
    "        'eyJhbGciOiJIUzI1NiJ9': { alg: 'HS256' },\n"
    "        'eyJzdWIiOiJvcC0wMDEiLCJyb2xlIjoiQURNSU4iLCJleHAiOjk5OTk5OTk5OTl9': { sub: 'op-001', role: 'ADMIN', exp: 9999999999 },\n"
    "        'eyJzdWIiOiJndWVzdCIsInJvbGUiOiJVU0VSIiwiZXhwIjoxfQ': { sub: 'guest', role: 'USER', exp: 1 },\n"
    "    };\n"
    "    return map[part] ?? {};\n"
    "}\n"
    "\n"
    "\n"
    "function analyzeToken(token: string): JWTAnalysis {\n"
    "    // TODO:\n"
    "    // 1. Divide por '.' → si partes !== 3: retorna { isValid: false, parts: n }\n"
    "    // 2. Decodifica header (partes[0]) y payload (partes[1]) con mockDecode\n"
    "    // 3. Extrae alg, sub, role, exp\n"
    "    // 4. isExpired: exp < 1000000000 → true (pasado), exp > 9000000000 → false (futuro)\n"
    "    // 5. Retorna JWTAnalysis completo con isValid: true\n"
    "    return { isValid: false, parts: 0 };\n"
    "}\n"
    "\n"
    "\n"
    "const tokens = [\n"
    "    'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJvcC0wMDEiLCJyb2xlIjoiQURNSU4iLCJleHAiOjk5OTk5OTk5OTl9.sig',\n"
    "    'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJndWVzdCIsInJvbGUiOiJVU0VSIiwiZXhwIjoxfQ.sig',\n"
    "    'malformed-token',\n"
    "];\n"
    "\n"
    "for (const token of tokens) {\n"
    "    const a = analyzeToken(token);\n"
    "    if (!a.isValid) {\n"
    "        console.log(`INVALID: ${a.parts} parts`);\n"
    "    } else {\n"
    "        const expStatus = a.isExpired ? 'EXPIRED' : 'VALID';\n"
    "        console.log(`OK: sub=${a.payloadSub} role=${a.payloadRole} exp=${expStatus}`);\n"
    "    }\n"
    "}\n"
),
"expected_output": (
    "OK: sub=op-001 role=ADMIN exp=VALID\n"
    "OK: sub=guest role=USER exp=EXPIRED\n"
    "INVALID: 1 parts"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Los tokens JWT son el mecanismo de autenticación de casi todas las APIs modernas. "
    "Un QA que puede inspeccionar un JWT puede verificar roles, expiración y claims "
    "sin depender del frontend para debuggear fallos de autenticación."
),
"theory_content": (
    "## JWT para QA — Lo que necesitas saber\n\n"
    "Un JWT tiene tres partes: `HEADER.PAYLOAD.SIGNATURE`\n\n"
    "```\n"
    "eyJhbGciOiJIUzI1NiJ9  ← Header  (base64url de {\"alg\":\"HS256\"})\n"
    ".eyJzdWIiOiJ1c3IifQ   ← Payload (base64url de {\"sub\":\"usr\", \"role\":\"ADMIN\"})\n"
    ".abc123xyz            ← Signature (no se verifica en QA sin la secret key)\n"
    "```\n\n"
    "**Claims importantes en QA:**\n"
    "- `sub` — subject (user ID)\n"
    "- `role` — rol del usuario\n"
    "- `exp` — Unix timestamp de expiración\n"
    "- `iat` — issued at (cuándo se creó)"
),
"pedagogical_objective": "Analizar JWTs en tests de autenticación — verificar claims sin backend.",
"syntax_hint": "`const parts = token.split('.'); if (parts.length !== 3) return { isValid: false, parts: parts.length };`",
"hints_json": json.dumps([
    "Divide: `const parts = token.split('.');` si `parts.length !== 3` retorna `{ isValid: false, parts: parts.length }`",
    "Decodifica: `const header = mockDecode(parts[0]); const payload = mockDecode(parts[1]);`",
    "isExpired: `const exp = payload.exp as number; const isExpired = exp < 1000000000;` — retorna el análisis completo.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ AUTO-031: SCHEMA VALIDATION — ZOD API SIMPLIFICADA ]",
"description": (
    "Implementa `Schema.parse(value)` que verifica el tipo y ejecuta los validators. "
    "Retorna `{success: true}` si todo está bien, o `{success: false, error: '<mensaje>'}`. "
    "Implementa `validateObject(data, schema)` que retorna errores en formato `'<field>: <error>'`."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": None, "codex_id": "qa_automation_ops",
"level_order": 31, "base_xp_reward": 205,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 255, "challenge_type": "typescript",
"phase": "DELTA_API", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["Zod", "schema_validation", "runtime_types", "API_contracts"]),
"initial_code": (
    "class Schema {\n"
    "    private validators: Array<(val: unknown) => string | null> = [];\n"
    "    private _type: string;\n"
    "\n"
    "    constructor(type: string) {\n"
    "        this._type = type;\n"
    "    }\n"
    "\n"
    "    min(n: number): Schema {\n"
    "        this.validators.push((val) => {\n"
    "            if (typeof val === 'string' && val.length < n) return `min length ${n}`;\n"
    "            if (typeof val === 'number' && val < n) return `min value ${n}`;\n"
    "            return null;\n"
    "        });\n"
    "        return this;\n"
    "    }\n"
    "\n"
    "    max(n: number): Schema {\n"
    "        this.validators.push((val) => {\n"
    "            if (typeof val === 'string' && val.length > n) return `max length ${n}`;\n"
    "            if (typeof val === 'number' && val > n) return `max value ${n}`;\n"
    "            return null;\n"
    "        });\n"
    "        return this;\n"
    "    }\n"
    "\n"
    "    parse(value: unknown): { success: boolean; error?: string } {\n"
    "        // TODO:\n"
    "        // 1. Si typeof value !== this._type: retorna { success: false, error: 'expected <type>' }\n"
    "        // 2. Ejecuta cada validator — si retorna string: retorna { success: false, error: msg }\n"
    "        // 3. Retorna { success: true }\n"
    "        return { success: false };\n"
    "    }\n"
    "}\n"
    "\n"
    "const z = {\n"
    "    string: () => new Schema('string'),\n"
    "    number: () => new Schema('number'),\n"
    "};\n"
    "\n"
    "\n"
    "function validateObject(\n"
    "    data: Record<string, unknown>,\n"
    "    schema: Record<string, Schema>\n"
    "): string[] {\n"
    "    // TODO: para cada (field, schema) retorna errores '<field>: <error>'\n"
    "    return [];\n"
    "}\n"
    "\n"
    "\n"
    "const userSchema = {\n"
    "    name:  z.string().min(2).max(50),\n"
    "    age:   z.number().min(18).max(120),\n"
    "    email: z.string().min(5),\n"
    "};\n"
    "\n"
    "const validUser   = { name: 'Alice Operator', age: 28,    email: 'alice@daki.io' };\n"
    "const invalidUser = { name: 'X',              age: 15,    email: 12345           };\n"
    "\n"
    "const errors1 = validateObject(validUser, userSchema);\n"
    "const errors2 = validateObject(invalidUser, userSchema);\n"
    "\n"
    "console.log(`Valid user: ${errors1.length === 0 ? 'OK' : errors1.join(', ')}`);\n"
    "errors2.forEach(err => console.log(`Error: ${err}`));\n"
),
"expected_output": (
    "Valid user: OK\n"
    "Error: name: min length 2\n"
    "Error: age: min value 18\n"
    "Error: email: expected string"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Zod es la librería de validación de schemas más usada en TypeScript. "
    "Valida datos en runtime con tipos definidos en tiempo de compilación. "
    "Un QA que conoce Zod puede validar contratos de API de forma tipada."
),
"theory_content": (
    "## Zod en la práctica\n\n"
    "```typescript\n"
    "import { z } from 'zod';\n\n"
    "const UserSchema = z.object({\n"
    "    name:  z.string().min(2),\n"
    "    age:   z.number().min(18),\n"
    "    email: z.string().email(),\n"
    "});\n\n"
    "// En un test de API:\n"
    "const response = await request.get('/api/users/1').json();\n"
    "const result = UserSchema.safeParse(response);\n"
    "if (!result.success) {\n"
    "    console.log('Schema mismatch:', result.error.issues);\n"
    "}\n"
    "```\n\n"
    "**`safeParse`** — no lanza excepciones, retorna `{ success, data }` o `{ success, error }`."
),
"pedagogical_objective": "Implementar validación de schema runtime — base del contract testing con Zod.",
"syntax_hint": "parse: `if (typeof value !== this._type) return { success: false, error: \\`expected ${this._type}\\` };`",
"hints_json": json.dumps([
    "parse: primero verifica tipo, luego `for (const validator of this.validators) { const err = validator(value); if (err) return { success: false, error: err }; } return { success: true };`",
    "validateObject: `const errors: string[] = []; for (const [field, schema] of Object.entries(schemaObj)) { const result = schema.parse(data[field]); if (!result.success) errors.push(\\`${field}: ${result.error}\\`); } return errors;`",
    "El orden de los errores sigue el orden de los campos en el schema.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ AUTO-032: PERFORMANCE BASELINE — ANÁLISIS DE LOAD TEST ]",
"description": (
    "Implementa `analyzeLoadTest(durations, statusCodes)` que calcula métricas de performance. "
    "Implementa `printLoadReport(result, threshold)` que imprime el reporte con veredictos PASS/FAIL. "
    "P95 y P99: índice `Math.ceil(percentile * n) - 1` del array ordenado ascendente."
),
"difficulty_tier": 3, "difficulty": "hard",
"sector_id": None, "codex_id": "qa_automation_ops",
"level_order": 32, "base_xp_reward": 215,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 270, "challenge_type": "typescript",
"phase": "DELTA_API", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["performance_testing", "percentiles", "p95", "k6", "load_testing"]),
"initial_code": (
    "interface LoadTestResult {\n"
    "    requestCount: number;\n"
    "    successCount: number;\n"
    "    failCount:    number;\n"
    "    avgDurationMs: number;\n"
    "    p95DurationMs: number;\n"
    "    p99DurationMs: number;\n"
    "}\n"
    "\n"
    "\n"
    "function analyzeLoadTest(durations: number[], statusCodes: number[]): LoadTestResult {\n"
    "    // TODO:\n"
    "    // - requestCount = durations.length\n"
    "    // - successCount = status codes < 400\n"
    "    // - failCount = status codes >= 400\n"
    "    // - avgDurationMs = Math.round(promedio)\n"
    "    // - sorted = [...durations].sort((a,b) => a-b)\n"
    "    // - p95 = sorted[Math.ceil(0.95 * n) - 1]\n"
    "    // - p99 = sorted[Math.ceil(0.99 * n) - 1]\n"
    "    return {} as LoadTestResult;\n"
    "}\n"
    "\n"
    "function printLoadReport(\n"
    "    result: LoadTestResult,\n"
    "    threshold: { p95: number; errorRate: number }\n"
    "): void {\n"
    "    // TODO: imprime:\n"
    "    // 'Requests: <total> | OK: <success> | FAIL: <fail>'\n"
    "    // 'Avg: <avg>ms | P95: <p95>ms | P99: <p99>ms'\n"
    "    // 'Error rate: <pct>%'  (1 decimal, failCount/requestCount*100)\n"
    "    // 'P95 threshold: <threshold.p95>ms \u2192 PASS' si p95 <= threshold, si no '\u2192 FAIL'\n"
    "    // 'Error threshold: <threshold.errorRate>% \u2192 PASS' si errorRate <= threshold, si no '\u2192 FAIL'\n"
    "}\n"
    "\n"
    "\n"
    "const durations    = [120, 95, 200, 450, 180, 320, 88, 560, 290, 110];\n"
    "const statusCodes  = [200, 200, 200, 500, 200, 200, 200, 503, 200, 200];\n"
    "\n"
    "const result = analyzeLoadTest(durations, statusCodes);\n"
    "printLoadReport(result, { p95: 500, errorRate: 20 });\n"
),
"expected_output": (
    "Requests: 10 | OK: 8 | FAIL: 2\n"
    "Avg: 241ms | P95: 560ms | P99: 560ms\n"
    "Error rate: 20.0%\n"
    "P95 threshold: 500ms \u2192 FAIL\n"
    "Error threshold: 20% \u2192 PASS"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "El performance testing decide si el sistema aguanta producción. "
    "P95 = 560ms significa que el 95% de las requests responden en menos de 560ms. "
    "Si el P95 supera el threshold del SLA, el deploy no debería proceder."
),
"theory_content": (
    "## Percentiles en Performance Testing\n\n"
    "El **P95** (percentil 95) es el valor que el 95% de las mediciones no supera.\n\n"
    "```typescript\n"
    "const sorted = [...durations].sort((a, b) => a - b);\n"
    "const p95Index = Math.ceil(0.95 * n) - 1;\n"
    "const p95 = sorted[p95Index];\n"
    "```\n\n"
    "**Por qué P95 y no el promedio:**\n"
    "El promedio oculta los outliers. Si el 95% responde en 100ms pero el 5% tarda 10s, "
    "el promedio puede ser 600ms — el P95 revela el problema.\n\n"
    "**k6** — la herramienta de performance testing más usada con TypeScript."
),
"pedagogical_objective": "Calcular métricas de performance y evaluar contra thresholds — skill de QA performance.",
"syntax_hint": "avg: `Math.round(durations.reduce((s, d) => s + d, 0) / durations.length)`. Error rate: `(failCount / requestCount * 100).toFixed(1)`",
"hints_json": json.dumps([
    "analyzeLoadTest: `const sorted = [...durations].sort((a,b) => a-b); const n = durations.length; const p95 = sorted[Math.ceil(0.95*n)-1]; const p99 = sorted[Math.ceil(0.99*n)-1];`",
    "successCount: `statusCodes.filter(s => s < 400).length` — failCount: `statusCodes.filter(s => s >= 400).length`",
    "printLoadReport: error rate = `(result.failCount / result.requestCount * 100).toFixed(1)` — threshold check: `result.p95DurationMs <= threshold.p95 ? 'PASS' : 'FAIL'`",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ AUTO-033: GRAPHQL — MOCK DE QUERIES Y MUTATIONS ]",
"description": (
    "Implementa `assertGraphQL(response, expectedData?, expectedErrors?)`. "
    "Si hay errores inesperados: imprime `'FAIL: unexpected errors — <msgs>'`. "
    "Si errors y expectedErrors: verifica que el mensaje contiene expectedErrors[0]. "
    "Si data y expectedData: compara con `JSON.stringify`. "
    "Si data sin expectedData: `'PASS: data received'`."
),
"difficulty_tier": 3, "difficulty": "hard",
"sector_id": None, "codex_id": "qa_automation_ops",
"level_order": 33, "base_xp_reward": 210,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 260, "challenge_type": "typescript",
"phase": "DELTA_API", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["GraphQL", "queries", "mutations", "API_testing", "mocking"]),
"initial_code": (
    "interface GraphQLResponse<T = unknown> {\n"
    "    data?:   T;\n"
    "    errors?: Array<{ message: string }>;\n"
    "}\n"
    "\n"
    "class GraphQLMock {\n"
    "    private _resolvers = new Map<string, (vars: Record<string, unknown>) => unknown>();\n"
    "\n"
    "    addResolver(operation: string, resolver: (vars: Record<string, unknown>) => unknown): void {\n"
    "        this._resolvers.set(operation, resolver);\n"
    "    }\n"
    "\n"
    "    execute<T>(query: string, variables: Record<string, unknown> = {}): GraphQLResponse<T> {\n"
    "        const match = query.match(/(query|mutation)\\s+(\\w+)/);\n"
    "        if (!match) return { errors: [{ message: 'Invalid query' }] };\n"
    "        const resolver = this._resolvers.get(match[2]);\n"
    "        if (!resolver) return { errors: [{ message: `No resolver for ${match[2]}` }] };\n"
    "        try {\n"
    "            return { data: resolver(variables) as T };\n"
    "        } catch (err) {\n"
    "            return { errors: [{ message: (err as Error).message }] };\n"
    "        }\n"
    "    }\n"
    "}\n"
    "\n"
    "\n"
    "function assertGraphQL<T>(\n"
    "    response: GraphQLResponse<T>,\n"
    "    expectedData?: T,\n"
    "    expectedErrors?: string[]\n"
    "): void {\n"
    "    // TODO:\n"
    "    // Si response.errors && !expectedErrors: 'FAIL: unexpected errors \u2014 <msgs>'\n"
    "    // Si response.errors && expectedErrors:\n"
    "    //   verifica que response.errors[0].message contiene expectedErrors[0]\n"
    "    //   'PASS: error contains \"<expectedErrors[0]>\"' o 'FAIL: ...'\n"
    "    // Si response.data && expectedData:\n"
    "    //   JSON.stringify comparison: 'PASS: data matches' o 'FAIL: expected <exp> got <actual>'\n"
    "    // Si response.data && !expectedData: 'PASS: data received'\n"
    "}\n"
    "\n"
    "\n"
    "const mock = new GraphQLMock();\n"
    "\n"
    "mock.addResolver('GetUser', (vars) => ({\n"
    "    user: { id: vars.id, name: 'Operator', role: 'ADMIN' }\n"
    "}));\n"
    "\n"
    "mock.addResolver('Login', (vars) => {\n"
    "    if (vars.password !== 'nexo-2099') throw new Error('Invalid credentials');\n"
    "    return { token: 'jwt-abc123' };\n"
    "});\n"
    "\n"
    "const r1 = mock.execute<{ user: { id: string; name: string; role: string } }>(\n"
    "    'query GetUser { user { id name role } }',\n"
    "    { id: 'usr-001' }\n"
    ");\n"
    "assertGraphQL(r1, { user: { id: 'usr-001', name: 'Operator', role: 'ADMIN' } });\n"
    "\n"
    "const r2 = mock.execute<{ token: string }>('mutation Login { token }', { password: 'nexo-2099' });\n"
    "assertGraphQL(r2);\n"
    "\n"
    "const r3 = mock.execute('mutation Login { token }', { password: 'wrong' });\n"
    "assertGraphQL(r3, undefined, ['Invalid credentials']);\n"
),
"expected_output": (
    "PASS: data matches\n"
    "PASS: data received\n"
    'PASS: error contains "Invalid credentials"'
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Las APIs GraphQL no tienen endpoints fijos — tienen un único endpoint y el cliente decide qué datos pide. "
    "Para QA, esto significa testear que las queries retornan exactamente los campos solicitados "
    "y que las mutations producen los errores correctos."
),
"theory_content": (
    "## GraphQL Testing — Lo esencial\n\n"
    "```typescript\n"
    "// Query: obtener datos\n"
    "const GET_USER = `query GetUser($id: ID!) { user(id: $id) { name role } }`;\n\n"
    "// Mutation: modificar datos\n"
    "const LOGIN = `mutation Login($email: String!, $password: String!) {\n"
    "    login(email: $email, password: $password) { token }\n"
    "}`;\n\n"
    "// Test con supertest o fetch:\n"
    "const response = await request.post('/graphql').send({\n"
    "    query: GET_USER,\n"
    "    variables: { id: 'usr-001' }\n"
    "});\n"
    "expect(response.body.data.user.name).toBe('Alice');\n"
    "```"
),
"pedagogical_objective": "Testear queries y mutations GraphQL — skill creciente en el mercado QA.",
"syntax_hint": "Para verificar error: `response.errors[0].message.includes(expectedErrors[0])` — PASS si es true.",
"hints_json": json.dumps([
    "Rama 1 (errors sin expectedErrors): `if (response.errors && !expectedErrors) { console.log(\\`FAIL: unexpected errors — ${response.errors.map(e=>e.message).join(', ')}\\`); return; }`",
    "Rama 2 (errors con expectedErrors): `const msg = response.errors?.[0].message ?? ''; const pass = msg.includes(expectedErrors[0]); console.log(pass ? \\`PASS: error contains \"${expectedErrors[0]}\"\\` : \\`FAIL: ...\\`)`",
    "Rama 3 (data): `if (JSON.stringify(response.data) === JSON.stringify(expectedData)) console.log('PASS: data matches'); else ...` — si !expectedData: `console.log('PASS: data received')`",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ AUTO-034: CONTRACT TESTING — PACT SIMPLIFICADO ]",
"description": (
    "Implementa `verifyContract(contract, actualResponses)` que verifica cada interacción. "
    "Para cada interacción busca la respuesta en `actualResponses` con clave `'METHOD /path'`. "
    "Si no existe: `'MISSING: <description>'`. Si status != esperado: `'STATUS MISMATCH [...]'`. "
    "Si body difiere (JSON.stringify): `'BODY MISMATCH [...]'`. Si todo OK: `'PASS: <description>'`."
),
"difficulty_tier": 3, "difficulty": "hard",
"sector_id": None, "codex_id": "qa_automation_ops",
"level_order": 34, "base_xp_reward": 218,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 265, "challenge_type": "typescript",
"phase": "DELTA_API", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["contract_testing", "Pact", "consumer_driven", "API_contracts"]),
"initial_code": (
    "interface Interaction {\n"
    "    description: string;\n"
    "    request:     { method: string; path: string };\n"
    "    response:    { status: number; body: Record<string, unknown> };\n"
    "}\n"
    "\n"
    "interface Contract {\n"
    "    consumer: string;\n"
    "    provider: string;\n"
    "    interactions: Interaction[];\n"
    "}\n"
    "\n"
    "\n"
    "function verifyContract(\n"
    "    contract: Contract,\n"
    "    actualResponses: Map<string, { status: number; body: Record<string, unknown> }>\n"
    "): void {\n"
    "    // TODO: por cada interaction:\n"
    "    //   key = '<method> <path>'\n"
    "    //   Si no existe en actualResponses: 'MISSING: <description>'\n"
    "    //   Si status != response.status: 'STATUS MISMATCH [<desc>]: expected <exp> got <actual>'\n"
    "    //   Si JSON.stringify(body) != JSON.stringify(response.body): 'BODY MISMATCH [<desc>]: expected <expJson> got <actualJson>'\n"
    "    //   Si OK: 'PASS: <description>'\n"
    "    // Al final: 'Contract: <consumer> \u2194 <provider> | PASS: <n> | FAIL: <n>'\n"
    "}\n"
    "\n"
    "\n"
    "const contract: Contract = {\n"
    "    consumer: 'Frontend',\n"
    "    provider: 'API',\n"
    "    interactions: [\n"
    "        {\n"
    "            description: 'GET /api/status returns 200',\n"
    "            request:  { method: 'GET',  path: '/api/status' },\n"
    "            response: { status: 200, body: { ok: true } },\n"
    "        },\n"
    "        {\n"
    "            description: 'POST /api/auth returns token',\n"
    "            request:  { method: 'POST', path: '/api/auth' },\n"
    "            response: { status: 200, body: { token: 'any' } },\n"
    "        },\n"
    "        {\n"
    "            description: 'GET /api/users returns list',\n"
    "            request:  { method: 'GET',  path: '/api/users' },\n"
    "            response: { status: 200, body: { users: [] } },\n"
    "        },\n"
    "    ],\n"
    "};\n"
    "\n"
    "const actual = new Map([\n"
    "    ['GET /api/status', { status: 200, body: { ok: true }       }],\n"
    "    ['POST /api/auth',  { status: 200, body: { token: 'jwt-abc' }}],\n"
    "]);\n"
    "\n"
    "verifyContract(contract, actual);\n"
),
"expected_output": (
    "PASS: GET /api/status returns 200\n"
    'BODY MISMATCH [POST /api/auth returns token]: expected {"token":"any"} got {"token":"jwt-abc"}\n'
    "MISSING: GET /api/users returns list\n"
    "Contract: Frontend \u2194 API | PASS: 1 | FAIL: 2"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Contract testing previene el problema clásico: el frontend y el backend evolucionan independientemente "
    "y un día se rompe la integración. Pact formaliza el contrato: "
    "el consumidor define lo que espera, el proveedor debe cumplirlo."
),
"theory_content": (
    "## Consumer-Driven Contract Testing\n\n"
    "**Sin contract testing:**\n"
    "```\n"
    "Frontend: { token: 'jwt-abc' }\n"
    "API cambia a: { accessToken: 'jwt-abc' }  ← breaking change silencioso\n"
    "```\n\n"
    "**Con Pact:**\n"
    "1. Frontend define: `POST /api/auth → { token: string }`\n"
    "2. CI verifica que la API retorna exactamente eso\n"
    "3. Si la API cambia `token` a `accessToken` → CI falla antes del deploy\n\n"
    "**`JSON.stringify` para comparar objetos:**\n"
    "`JSON.stringify({ok:true}) === JSON.stringify({ok:true})` → true"
),
"pedagogical_objective": "Implementar contract testing — previene breaking changes en integraciones frontend-backend.",
"syntax_hint": "Para BODY MISMATCH: `console.log(\\`BODY MISMATCH [${i.description}]: expected ${JSON.stringify(i.response.body)} got ${JSON.stringify(actual.body)}\\`)`",
"hints_json": json.dumps([
    "Para cada interaction: `const key = \\`${i.request.method} ${i.request.path}\\`; const actual = actualResponses.get(key);`",
    "Si !actual: MISSING. Luego verifica status. Luego: `if (JSON.stringify(actual.body) !== JSON.stringify(i.response.body))` → BODY MISMATCH.",
    "Contadores: `let pass = 0, fail = 0;` — incrementa según el resultado de cada interacción.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ AUTO-035 \u221e BOSS: NEXO API REGRESSION SUITE ]",
"description": (
    "Implementa `APITestSuite.runAll()` que ejecuta todos los tests contra el servidor simulado. "
    "Por cada test: verifica status, verifica body keys si aplica, imprime `'[PASS] <name>'` o `'[FAIL] <name>: <motivo>'`. "
    "Al final imprime el reporte con `=== <name> [<url>] ===`, conteos y `STATUS: OK` o `STATUS: FAILED`."
),
"difficulty_tier": 3, "difficulty": "hard",
"sector_id": None, "codex_id": "qa_automation_ops",
"level_order": 35, "base_xp_reward": 380,
"is_project": False, "is_phase_boss": True,
"telemetry_goal_time": 380, "challenge_type": "typescript",
"phase": "DELTA_API", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["API_regression", "test_suite", "CRUD_testing", "auth_testing"]),
"initial_code": (
    "interface APITest {\n"
    "    name:            string;\n"
    "    method:          string;\n"
    "    path:            string;\n"
    "    expectedStatus:  number;\n"
    "    expectedBodyKeys?: string[];\n"
    "}\n"
    "\n"
    "class APITestSuite {\n"
    "    private tests: APITest[] = [];\n"
    "\n"
    "    private _server = new Map<string, { status: number; body: Record<string, unknown> }>([\n"
    "        ['GET /api/health',         { status: 200, body: { ok: true, version: '2.1.0' }           }],\n"
    "        ['POST /api/auth/login',    { status: 200, body: { token: 'jwt-nexo', userId: 'usr-001' } }],\n"
    "        ['GET /api/users/usr-001',  { status: 200, body: { id: 'usr-001', name: 'Operator', role: 'ADMIN' } }],\n"
    "        ['DELETE /api/sessions',   { status: 204, body: {}                                        }],\n"
    "        ['GET /api/admin/secret',  { status: 403, body: { error: 'Forbidden' }                   }],\n"
    "    ]);\n"
    "\n"
    "    constructor(private suiteName: string, private baseURL: string) {}\n"
    "\n"
    "    add(test: APITest): void {\n"
    "        this.tests.push(test);\n"
    "    }\n"
    "\n"
    "    runAll(): void {\n"
    "        // TODO: por cada test:\n"
    "        //   Obtén la respuesta de this._server (o 404 si no existe)\n"
    "        //   Si status !== expectedStatus: '[FAIL] <name>: status expected=<exp> got=<actual>'\n"
    "        //   Si expectedBodyKeys: por cada key faltante: '[FAIL] <name>: missing key <key>'\n"
    "        //   Si todo OK: '[PASS] <name>'\n"
    "        // Al final:\n"
    "        //   '=== <suiteName> [<baseURL>] ==='\n"
    "        //   'PASS: <n> | FAIL: <n>'\n"
    "        //   'STATUS: OK' si fails===0, 'STATUS: FAILED' si no\n"
    "    }\n"
    "}\n"
    "\n"
    "\n"
    "const suite = new APITestSuite('Nexo API Regression', 'https://api.daki.io');\n"
    "\n"
    "suite.add({ name: 'health_check',  method: 'GET',    path: '/api/health',         expectedStatus: 200, expectedBodyKeys: ['ok', 'version'] });\n"
    "suite.add({ name: 'login',         method: 'POST',   path: '/api/auth/login',     expectedStatus: 200, expectedBodyKeys: ['token', 'userId'] });\n"
    "suite.add({ name: 'get_profile',   method: 'GET',    path: '/api/users/usr-001',  expectedStatus: 200, expectedBodyKeys: ['id', 'name', 'role'] });\n"
    "suite.add({ name: 'logout',        method: 'DELETE', path: '/api/sessions',       expectedStatus: 204 });\n"
    "suite.add({ name: 'access_denied', method: 'GET',    path: '/api/admin/secret',   expectedStatus: 200 });\n"
    "\n"
    "suite.runAll();\n"
),
"expected_output": (
    "[PASS] health_check\n"
    "[PASS] login\n"
    "[PASS] get_profile\n"
    "[PASS] logout\n"
    "[FAIL] access_denied: status expected=200 got=403\n"
    "=== Nexo API Regression [https://api.daki.io] ===\n"
    "PASS: 4 | FAIL: 1\n"
    "STATUS: FAILED"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "\u221e BOSS DELTA \u2014 El equipo va a hacer deploy en 30 minutos. "
    "Necesitas correr la suite de regresión de la API del Nexo: "
    "health, auth, profile, logout, y el endpoint admin que debería denegar acceso. "
    "Un fallo intencional en el último test — el sistema funciona correctamente."
),
"theory_content": (
    "## API Regression Suite — La última línea de defensa\n\n"
    "Una regression suite verifica que los cambios nuevos no rompieron lo que ya funcionaba.\n\n"
    "**Estructura típica:**\n"
    "1. Health check — ¿el servidor responde?\n"
    "2. Auth flow — ¿login y logout funcionan?\n"
    "3. CRUD básico — ¿leer y crear recursos funciona?\n"
    "4. Permisos — ¿los endpoints protegidos rechazan accesos no autorizados?\n\n"
    "El test `access_denied` falla intencionalmente: esperamos 200 pero el servidor retorna 403. "
    "Esto es correcto — la API está funcionando bien, el test tiene el expected status equivocado."
),
"pedagogical_objective": "Construir una API regression suite completa — el entregable final de un QA Automation Engineer.",
"syntax_hint": "Para obtener la respuesta: `const resp = this._server.get(\\`${test.method} ${test.path}\\`) ?? { status: 404, body: {} };`",
"hints_json": json.dumps([
    "Para cada test: `const resp = this._server.get(\\`${test.method} ${test.path}\\`) ?? { status: 404, body: {} }; let failed = false;`",
    "Status check: `if (resp.status !== test.expectedStatus) { console.log(\\`[FAIL] ${test.name}: status expected=${test.expectedStatus} got=${resp.status}\\`); failed = true; }`",
    "Si !failed y expectedBodyKeys: verifica keys, si falta alguna marca como failed. Si !failed al final: `console.log(\\`[PASS] ${test.name}\\`)`",
]),
"grid_map_json": None,
},
]

FASE5 = [
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ AUTO-036: GITHUB ACTIONS — ESTRUCTURA DE WORKFLOW ]",
"description": (
    "Implementa `generateWorkflow(testCommand, reportDir)` que retorna un `WorkflowConfig`. "
    "El workflow tiene nombre `'QA Pipeline'`, triggers push+PR a `['main']`, "
    "y dos jobs: `test` (3 steps: checkout, install, test) y `report` (3 steps: checkout, generate, upload; needs: ['test']). "
    "Implementa `describeWorkflow(config)` que imprime la estructura."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": None, "codex_id": "qa_automation_ops",
"level_order": 36, "base_xp_reward": 200,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 250, "challenge_type": "typescript",
"phase": "ECHO_DEVOPS", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["GitHub_Actions", "CI_CD", "workflows", "jobs", "steps"]),
"initial_code": (
    "interface WorkflowStep {\n"
    "    name: string;\n"
    "    uses?: string;\n"
    "    run?:  string;\n"
    "}\n"
    "\n"
    "interface WorkflowJob {\n"
    "    name:     string;\n"
    "    runsOn:   string;\n"
    "    steps:    WorkflowStep[];\n"
    "    needs?:   string[];\n"
    "}\n"
    "\n"
    "interface WorkflowConfig {\n"
    "    name: string;\n"
    "    on:   { push: { branches: string[] }; pull_request: { branches: string[] } };\n"
    "    jobs: Record<string, WorkflowJob>;\n"
    "}\n"
    "\n"
    "\n"
    "function generateWorkflow(testCommand: string, reportDir: string): WorkflowConfig {\n"
    "    // TODO: retorna WorkflowConfig con:\n"
    "    // name: 'QA Pipeline'\n"
    "    // on: push+pull_request a ['main']\n"
    "    // jobs:\n"
    "    //   test: { runsOn:'ubuntu-latest', steps: [checkout(uses:'actions/checkout@v4'), install(run:'npm ci'), test(run:testCommand)] }\n"
    "    //   report: { runsOn:'ubuntu-latest', needs:['test'], steps:[checkout, generate(run:'npm run report'), upload(run:'cp -r '+reportDir+' ./artifacts')] }\n"
    "    return {} as WorkflowConfig;\n"
    "}\n"
    "\n"
    "function describeWorkflow(config: WorkflowConfig): void {\n"
    "    // TODO: imprime:\n"
    "    // 'Workflow: <name>'\n"
    "    // 'Triggers: push(main), pull_request(main)'\n"
    "    // Por cada job: 'Job <jobName>: <steps.length> steps'\n"
    "    //   Si tiene needs: '  needs: <needs.join(',')>'\n"
    "}\n"
    "\n"
    "\n"
    "const workflow = generateWorkflow('npx playwright test', './playwright-report');\n"
    "describeWorkflow(workflow);\n"
),
"expected_output": (
    "Workflow: QA Pipeline\n"
    "Triggers: push(main), pull_request(main)\n"
    "Job test: 3 steps\n"
    "Job report: 3 steps\n"
    "  needs: test"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Sin CI, los tests solo corren cuando el developer recuerda correrlos. "
    "Un workflow de GitHub Actions los ejecuta automáticamente en cada push — "
    "sin excepción, sin olvidos, con reporte automático."
),
"theory_content": (
    "## GitHub Actions — Anatomía de un workflow\n\n"
    "```yaml\n"
    "# .github/workflows/qa.yml\n"
    "name: QA Pipeline\n"
    "on:\n"
    "  push:\n"
    "    branches: [main]\n"
    "  pull_request:\n"
    "    branches: [main]\n"
    "jobs:\n"
    "  test:\n"
    "    runs-on: ubuntu-latest\n"
    "    steps:\n"
    "      - uses: actions/checkout@v4\n"
    "      - run: npm ci\n"
    "      - run: npx playwright test\n"
    "  report:\n"
    "    needs: [test]\n"
    "    steps:\n"
    "      - run: npm run report\n"
    "```\n\n"
    "**`needs: [test]`** — el job `report` no corre hasta que `test` termine con éxito."
),
"pedagogical_objective": "Estructurar un workflow de GitHub Actions — conocimiento esencial para QA en DevOps.",
"syntax_hint": "Para el job report: `{ runsOn: 'ubuntu-latest', needs: ['test'], steps: [...] }`",
"hints_json": json.dumps([
    "generateWorkflow retorna el objeto completo con name, on y jobs — define la estructura paso a paso.",
    "describeWorkflow: `console.log(\\`Workflow: ${config.name}\\`); console.log('Triggers: push(main), pull_request(main)');`",
    "Para los jobs: `Object.entries(config.jobs).forEach(([name, job]) => { console.log(\\`Job ${name}: ${job.steps.length} steps\\`); if (job.needs) console.log(\\`  needs: ${job.needs.join(',')}\\`); })`",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ AUTO-037: ALLURE REPORT — GENERADOR DE REPORTE ]",
"description": (
    "Implementa `formatAllureReport(tests)` que imprime el reporte completo. "
    "Por cada test: `'[<STATUS>] <fullName> (<duration>ms)'`, "
    "si tiene steps fallidos: `'  FAILED STEPS: <names>'`, "
    "luego `'  Labels: <name>=<value>'` por cada label separados por coma. "
    "Al final: `'---'` y `'Total: N | Passed: N | Failed: N | Skipped: N'`."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": None, "codex_id": "qa_automation_ops",
"level_order": 37, "base_xp_reward": 205,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 255, "challenge_type": "typescript",
"phase": "ECHO_DEVOPS", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["Allure", "reporting", "test_results", "CI_reporting"]),
"initial_code": (
    "interface TestStep {\n"
    "    name:   string;\n"
    "    status: 'passed' | 'failed' | 'broken';\n"
    "}\n"
    "\n"
    "interface AllureTest {\n"
    "    fullName: string;\n"
    "    status:   'passed' | 'failed' | 'broken' | 'skipped';\n"
    "    duration: number;\n"
    "    steps:    TestStep[];\n"
    "    labels:   Array<{ name: string; value: string }>;\n"
    "}\n"
    "\n"
    "\n"
    "function formatAllureReport(tests: AllureTest[]): void {\n"
    "    // TODO: imprime 'ALLURE REPORT' y '============='\n"
    "    // Por cada test:\n"
    "    //   '[<STATUS.toUpperCase()>] <fullName> (<duration>ms)'\n"
    "    //   Si hay steps con status === 'failed': '  FAILED STEPS: <names separados por ', '>'\n"
    "    //   '  Labels: <name>=<value>, <name>=<value>, ...'\n"
    "    // '---'\n"
    "    // 'Total: <n> | Passed: <n> | Failed: <n> | Skipped: <n>'\n"
    "}\n"
    "\n"
    "\n"
    "formatAllureReport([\n"
    "    {\n"
    "        fullName: 'Login Suite > should login successfully',\n"
    "        status:   'passed',\n"
    "        duration: 1200,\n"
    "        steps: [\n"
    "            { name: 'Navigate to login',  status: 'passed' },\n"
    "            { name: 'Fill credentials',   status: 'passed' },\n"
    "        ],\n"
    "        labels: [{ name: 'suite', value: 'Login' }, { name: 'severity', value: 'critical' }],\n"
    "    },\n"
    "    {\n"
    "        fullName: 'Dashboard Suite > should load within 2s',\n"
    "        status:   'failed',\n"
    "        duration: 8500,\n"
    "        steps: [\n"
    "            { name: 'Navigate to dashboard', status: 'passed' },\n"
    "            { name: 'Assert load time',      status: 'failed' },\n"
    "        ],\n"
    "        labels: [{ name: 'suite', value: 'Dashboard' }],\n"
    "    },\n"
    "    {\n"
    "        fullName: 'Mobile Suite > smoke test',\n"
    "        status:   'skipped',\n"
    "        duration: 0,\n"
    "        steps: [],\n"
    "        labels: [{ name: 'suite', value: 'Mobile' }],\n"
    "    },\n"
    "]);\n"
),
"expected_output": (
    "ALLURE REPORT\n"
    "=============\n"
    "[PASSED] Login Suite > should login successfully (1200ms)\n"
    "  Labels: suite=Login, severity=critical\n"
    "[FAILED] Dashboard Suite > should load within 2s (8500ms)\n"
    "  FAILED STEPS: Assert load time\n"
    "  Labels: suite=Dashboard\n"
    "[SKIPPED] Mobile Suite > smoke test (0ms)\n"
    "  Labels: suite=Mobile\n"
    "---\n"
    "Total: 3 | Passed: 1 | Failed: 1 | Skipped: 1"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Allure Report transforma los resultados de tests en un reporte visual con "
    "steps, attachments, labels y métricas. "
    "En CI, se genera automáticamente y se publica en GitHub Pages — "
    "el equipo ve exactamente qué falló sin abrir la consola."
),
"theory_content": (
    "## Allure Report — Setup básico\n\n"
    "```typescript\n"
    "// playwright.config.ts\n"
    "reporter: [\n"
    "    ['allure-playwright', { outputFolder: 'allure-results' }]\n"
    "]\n\n"
    "// En el test, agregar metadata:\n"
    "test('login flujo', async ({ page }) => {\n"
    "    allure.label('suite', 'Login');\n"
    "    allure.severity('critical');\n"
    "    // ... steps\n"
    "});\n"
    "```\n\n"
    "```bash\n"
    "# Generar el reporte:\n"
    "npx allure generate allure-results --clean\n"
    "npx allure open\n"
    "```"
),
"pedagogical_objective": "Generar reportes Allure — comunicar resultados de QA al equipo sin acceso a la consola.",
"syntax_hint": "Failed steps: `const failedSteps = test.steps.filter(s => s.status === 'failed').map(s => s.name); if (failedSteps.length > 0) console.log(\\`  FAILED STEPS: ${failedSteps.join(', ')}\\`)`",
"hints_json": json.dumps([
    "Status en mayúscula: `test.status.toUpperCase()` — primera línea: `console.log(\\`[${test.status.toUpperCase()}] ${test.fullName} (${test.duration}ms)\\`)`",
    "Labels: `console.log(\\`  Labels: ${test.labels.map(l => \\`${l.name}=${l.value}\\`).join(', ')}\\`)`",
    "Conteos: `const passed = tests.filter(t=>t.status==='passed').length` etc.",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ AUTO-038: ENVIRONMENT CONFIG MANAGER — MULTI-ENTORNO ]",
"description": (
    "Implementa el constructor de `ConfigManager` inicializando los 3 entornos. "
    "Implementa `compare(env1, env2)` que imprime las diferencias entre las dos configs, "
    "una línea por campo distinto: `'<field>: <val1> vs <val2>'`. "
    "Si no hay diferencias: `'Configs are identical'`."
),
"difficulty_tier": 2, "difficulty": "medium",
"sector_id": None, "codex_id": "qa_automation_ops",
"level_order": 38, "base_xp_reward": 200,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 250, "challenge_type": "typescript",
"phase": "ECHO_DEVOPS", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["environments", "config_management", "staging", "CI_CD"]),
"initial_code": (
    "type Environment = 'local' | 'staging' | 'production';\n"
    "\n"
    "interface EnvConfig {\n"
    "    baseUrl:  string;\n"
    "    apiKey:   string;\n"
    "    timeout:  number;\n"
    "    retries:  number;\n"
    "    headless: boolean;\n"
    "}\n"
    "\n"
    "\n"
    "class ConfigManager {\n"
    "    private configs: Map<Environment, EnvConfig>;\n"
    "\n"
    "    constructor() {\n"
    "        this.configs = new Map();\n"
    "        // TODO: inicializa con los 3 entornos:\n"
    "        // local:      { baseUrl:'http://localhost:3000', apiKey:'dev-key-123', timeout:5000, retries:3, headless:false }\n"
    "        // staging:    { baseUrl:'https://staging.daki.io', apiKey:'stg-key-456', timeout:8000, retries:2, headless:true }\n"
    "        // production: { baseUrl:'https://app.daki.io', apiKey:'REDACTED', timeout:10000, retries:1, headless:true }\n"
    "    }\n"
    "\n"
    "    get(env: Environment): EnvConfig {\n"
    "        return this.configs.get(env)!;\n"
    "    }\n"
    "\n"
    "    compare(env1: Environment, env2: Environment): void {\n"
    "        // TODO: obtén las dos configs con this.get()\n"
    "        // Por cada campo (baseUrl, apiKey, timeout, retries, headless):\n"
    "        //   Si son distintos: '<campo>: <val1> vs <val2>'\n"
    "        // Si todos iguales: 'Configs are identical'\n"
    "    }\n"
    "}\n"
    "\n"
    "\n"
    "const mgr = new ConfigManager();\n"
    "const local   = mgr.get('local');\n"
    "const staging = mgr.get('staging');\n"
    "\n"
    "console.log(`local.baseUrl: ${local.baseUrl}`);\n"
    "console.log(`staging.timeout: ${staging.timeout}`);\n"
    "console.log('--- local vs staging ---');\n"
    "mgr.compare('local', 'staging');\n"
),
"expected_output": (
    "local.baseUrl: http://localhost:3000\n"
    "staging.timeout: 8000\n"
    "--- local vs staging ---\n"
    "baseUrl: http://localhost:3000 vs https://staging.daki.io\n"
    "apiKey: dev-key-123 vs stg-key-456\n"
    "timeout: 5000 vs 8000\n"
    "retries: 3 vs 2\n"
    "headless: false vs true"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "En producción se usa `https://app.daki.io`. En staging, `https://staging.daki.io`. "
    "En local, `http://localhost:3000`. "
    "Un config manager centraliza estas diferencias — cambiar de entorno es una línea de código."
),
"theory_content": (
    "## Config por Entorno — Patrón estándar\n\n"
    "```typescript\n"
    "// El patrón más común en equipos de QA:\n"
    "const ENV = process.env.TEST_ENV as Environment ?? 'local';\n"
    "const config = configManager.get(ENV);\n\n"
    "// En GitHub Actions:\n"
    "# env:\n"
    "#   TEST_ENV: staging\n"
    "```\n\n"
    "**Principio de menor privilegio en QA:**\n"
    "- Local: headless=false (puedes ver el browser)\n"
    "- CI/Staging: headless=true (no hay pantalla)\n"
    "- Producción: retries=1, timeout alto (tráfico real, no hay segunda oportunidad)"
),
"pedagogical_objective": "Gestionar configuración multi-entorno — práctica estándar en QA Automation empresarial.",
"syntax_hint": "Para compare: `const fields: (keyof EnvConfig)[] = ['baseUrl','apiKey','timeout','retries','headless']; fields.forEach(f => { if (c1[f] !== c2[f]) console.log(\\`${f}: ${c1[f]} vs ${c2[f]}\\`); })`",
"hints_json": json.dumps([
    "constructor: `this.configs.set('local', { baseUrl:'http://localhost:3000', apiKey:'dev-key-123', timeout:5000, retries:3, headless:false });` — igual para staging y production.",
    "compare: `const c1 = this.get(env1); const c2 = this.get(env2); let diffs = 0; const fields: (keyof EnvConfig)[] = ['baseUrl','apiKey','timeout','retries','headless'];`",
    "Por cada campo: `if (c1[f] !== c2[f]) { console.log(\\`${f}: ${c1[f]} vs ${c2[f]}\\`); diffs++; }` — al final: `if (diffs === 0) console.log('Configs are identical')`",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ AUTO-039: DOCKER COMPOSE PARA TEST ENVIRONMENTS ]",
"description": (
    "Implementa `buildTestCompose()` con los servicios `app`, `db` y `selenium` "
    "según los valores especificados. "
    "Implementa `printComposeInfo(config)` que imprime los servicios ordenados alfabéticamente "
    "con sus ports, env vars y healthCheck si existe."
),
"difficulty_tier": 3, "difficulty": "hard",
"sector_id": None, "codex_id": "qa_automation_ops",
"level_order": 39, "base_xp_reward": 215,
"is_project": False, "is_phase_boss": False,
"telemetry_goal_time": 265, "challenge_type": "typescript",
"phase": "ECHO_DEVOPS", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["Docker", "docker-compose", "test_environments", "containers"]),
"initial_code": (
    "interface DockerService {\n"
    "    image:        string;\n"
    "    ports:        string[];\n"
    "    env:          Record<string, string>;\n"
    "    healthCheck?: string;\n"
    "}\n"
    "\n"
    "interface ComposeConfig {\n"
    "    version:  string;\n"
    "    services: Record<string, DockerService>;\n"
    "}\n"
    "\n"
    "\n"
    "function buildTestCompose(): ComposeConfig {\n"
    "    // TODO: retorna ComposeConfig con version:'3.8' y services:\n"
    "    // app:      { image:'daki-app:test', ports:['3000:3000'], env:{NODE_ENV:'test',DB_URL:'postgres://db/test'}, healthCheck:'curl -f http://localhost:3000/health' }\n"
    "    // db:       { image:'postgres:15-alpine', ports:['5432:5432'], env:{POSTGRES_DB:'test',POSTGRES_PASSWORD:'test'} }\n"
    "    // selenium: { image:'selenium/standalone-chrome:latest', ports:['4444:4444'], env:{} }\n"
    "    return { version: '', services: {} };\n"
    "}\n"
    "\n"
    "function printComposeInfo(config: ComposeConfig): void {\n"
    "    // TODO: imprime 'Docker Compose v<version>'\n"
    "    // Por cada servicio ordenado alfabéticamente:\n"
    "    //   '<name>: <image>'\n"
    "    //   '  Ports: <ports.join(', ')>' o '  Ports: none' si vacío\n"
    "    //   '  Env vars: <Object.keys(env).length>'\n"
    "    //   Si tiene healthCheck: '  Health: <healthCheck>'\n"
    "}\n"
    "\n"
    "\n"
    "printComposeInfo(buildTestCompose());\n"
),
"expected_output": (
    "Docker Compose v3.8\n"
    "app: daki-app:test\n"
    "  Ports: 3000:3000\n"
    "  Env vars: 2\n"
    "  Health: curl -f http://localhost:3000/health\n"
    "db: postgres:15-alpine\n"
    "  Ports: 5432:5432\n"
    "  Env vars: 2\n"
    "selenium: selenium/standalone-chrome:latest\n"
    "  Ports: 4444:4444\n"
    "  Env vars: 0"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "Docker Compose levanta todo el stack de test en una sola línea: "
    "la app, la base de datos y el Selenium Grid. "
    "En CI, el runner levanta los contenedores, corre los tests, y los destruye. "
    "Reproducible, aislado, sin conflictos de estado."
),
"theory_content": (
    "## docker-compose para QA\n\n"
    "```yaml\n"
    "# docker-compose.test.yml\n"
    "version: '3.8'\n"
    "services:\n"
    "  app:\n"
    "    image: daki-app:test\n"
    "    ports: ['3000:3000']\n"
    "    environment:\n"
    "      NODE_ENV: test\n"
    "    healthcheck:\n"
    "      test: curl -f http://localhost:3000/health\n"
    "  selenium:\n"
    "    image: selenium/standalone-chrome:latest\n"
    "    ports: ['4444:4444']\n"
    "```\n\n"
    "```bash\n"
    "docker-compose -f docker-compose.test.yml up -d\n"
    "npx playwright test --config=playwright.ci.config.ts\n"
    "docker-compose -f docker-compose.test.yml down\n"
    "```"
),
"pedagogical_objective": "Configurar un entorno de test con Docker Compose — skill DevOps esencial para QA leads.",
"syntax_hint": "Para ordenar: `Object.keys(config.services).sort().forEach(name => { const svc = config.services[name]; ... })`",
"hints_json": json.dumps([
    "buildTestCompose: define los 3 servicios con los valores exactos del enunciado.",
    "printComposeInfo: `console.log(\\`Docker Compose v${config.version}\\`); Object.keys(config.services).sort().forEach(name => { ... })`",
    "Para cada servicio: `console.log(\\`${name}: ${svc.image}\\`); console.log(\\`  Ports: ${svc.ports.length > 0 ? svc.ports.join(', ') : 'none'}\\`); console.log(\\`  Env vars: ${Object.keys(svc.env).length}\\`); if (svc.healthCheck) console.log(\\`  Health: ${svc.healthCheck}\\`)`",
]),
"grid_map_json": None,
},
# ─────────────────────────────────────────────────────────────────────────────
{
"title": "[ AUTO-040 \u221e BOSS FINAL: CI PIPELINE — DEPLOY GATE ]",
"description": (
    "Implementa `CIPipeline.addStage(stage)`, `run()` y `report()`. "
    "`run()`: por cada stage imprime `'[RUNNING] <name>...'` luego `'[PASS/FAIL] <name> (<duration>ms)'` "
    "o `'[SKIPPED] <name>'` si el pipeline fue abortado. "
    "Si un stage blocking falla, activa el abort. "
    "`report()` imprime el resumen completo con veredicto final."
),
"difficulty_tier": 3, "difficulty": "hard",
"sector_id": None, "codex_id": "qa_automation_ops",
"level_order": 40, "base_xp_reward": 600,
"is_project": True, "is_phase_boss": True,
"telemetry_goal_time": 420, "challenge_type": "typescript",
"phase": "ECHO_DEVOPS", "strict_match": False, "is_free": False,
"concepts_taught_json": json.dumps(["CI_pipeline", "deploy_gate", "quality_gates", "orchestration", "DevOps"]),
"initial_code": (
    "type StageStatus = 'PENDING' | 'RUNNING' | 'PASS' | 'FAIL' | 'SKIPPED';\n"
    "\n"
    "interface PipelineStage {\n"
    "    name:     string;\n"
    "    status:   StageStatus;\n"
    "    duration: number;\n"
    "    blocking: boolean;\n"
    "}\n"
    "\n"
    "\n"
    "class CIPipeline {\n"
    "    private stages: PipelineStage[] = [];\n"
    "    private pipelineName: string;\n"
    "    private aborted   = false;\n"
    "    private abortedAt?: string;\n"
    "\n"
    "    constructor(name: string) {\n"
    "        this.pipelineName = name;\n"
    "    }\n"
    "\n"
    "    addStage(stage: PipelineStage): void {\n"
    "        // TODO: agrega a this.stages\n"
    "    }\n"
    "\n"
    "    run(): void {\n"
    "        // TODO: por cada stage:\n"
    "        //   Si this.aborted y stage.blocking: stage.status='SKIPPED'; console.log('[SKIPPED] <name>'); continue\n"
    "        //   Si no: console.log('[RUNNING] <name>...')\n"
    "        //          console.log('[<PASS|FAIL>] <name> (<duration>ms)')\n"
    "        //          Si status==='FAIL' y blocking: this.aborted=true; this.abortedAt=stage.name\n"
    "    }\n"
    "\n"
    "    report(): void {\n"
    "        // TODO:\n"
    "        // '=== PIPELINE: <pipelineName> ==='\n"
    "        // Por cada stage: '<STATUS> <name> <duration>ms'\n"
    "        // '---'\n"
    "        // 'PASS: <n> | FAIL: <n> | SKIPPED: <n>'\n"
    "        // Si aborted: 'PIPELINE FAILED at: <abortedAt>'\n"
    "        // Si no: 'PIPELINE SUCCESS'\n"
    "    }\n"
    "}\n"
    "\n"
    "\n"
    "const pipeline = new CIPipeline('QA Automation \u2014 Deploy Gate');\n"
    "\n"
    "pipeline.addStage({ name: 'install',    status: 'PASS', duration:  45000, blocking: true });\n"
    "pipeline.addStage({ name: 'lint',       status: 'PASS', duration:   8000, blocking: true });\n"
    "pipeline.addStage({ name: 'unit-tests', status: 'PASS', duration:  32000, blocking: true });\n"
    "pipeline.addStage({ name: 'e2e-tests',  status: 'FAIL', duration: 120000, blocking: true });\n"
    "pipeline.addStage({ name: 'deploy',     status: 'PASS', duration:      0, blocking: true });\n"
    "\n"
    "pipeline.run();\n"
    "pipeline.report();\n"
),
"expected_output": (
    "[RUNNING] install...\n"
    "[PASS] install (45000ms)\n"
    "[RUNNING] lint...\n"
    "[PASS] lint (8000ms)\n"
    "[RUNNING] unit-tests...\n"
    "[PASS] unit-tests (32000ms)\n"
    "[RUNNING] e2e-tests...\n"
    "[FAIL] e2e-tests (120000ms)\n"
    "[SKIPPED] deploy\n"
    "=== PIPELINE: QA Automation \u2014 Deploy Gate ===\n"
    "PASS install 45000ms\n"
    "PASS lint 8000ms\n"
    "PASS unit-tests 32000ms\n"
    "FAIL e2e-tests 120000ms\n"
    "SKIPPED deploy 0ms\n"
    "---\n"
    "PASS: 3 | FAIL: 1 | SKIPPED: 1\n"
    "PIPELINE FAILED at: e2e-tests"
),
"test_inputs_json": json.dumps([]),
"lore_briefing": (
    "\u221e BOSS FINAL \u2014 El equipo quiere hacer deploy en producción. "
    "El pipeline es el guardián: si los E2E fallan, el deploy no procede. "
    "Implementa el orquestador completo. "
    "Esta es la última misión del Protocolo QA. "
    "Si llegas aquí, eres un QA Automation Engineer."
),
"theory_content": (
    "## Quality Gates en CI/CD\n\n"
    "Un quality gate es una condición que el pipeline debe cumplir para continuar:\n\n"
    "```yaml\n"
    "# En GitHub Actions:\n"
    "jobs:\n"
    "  e2e-tests:\n"
    "    runs-on: ubuntu-latest\n"
    "    steps:\n"
    "      - run: npx playwright test\n"
    "  deploy:\n"
    "    needs: [e2e-tests]  # ← QUALITY GATE\n"
    "    if: success()       # solo si e2e-tests pasó\n"
    "    steps:\n"
    "      - run: ./deploy.sh\n"
    "```\n\n"
    "**El pipeline que implementas aquí es exactamente este patrón:**\n"
    "Si `e2e-tests` falla, `deploy` se marca como SKIPPED y el sistema no se despliega."
),
"pedagogical_objective": "Construir un CI pipeline con quality gates — el deployment guardian de un equipo de QA.",
"syntax_hint": "En run(): usa un flag `this.aborted` para saltar stages bloqueantes. Un stage SKIPPED no ejecuta [RUNNING].",
"hints_json": json.dumps([
    "addStage: `this.stages.push(stage)`",
    "run: `for (const stage of this.stages) { if (this.aborted && stage.blocking) { stage.status = 'SKIPPED'; console.log(\\`[SKIPPED] ${stage.name}\\`); continue; } console.log(\\`[RUNNING] ${stage.name}...\\`); console.log(\\`[${stage.status}] ${stage.name} (${stage.duration}ms)\\`); if (stage.status === 'FAIL' && stage.blocking) { this.aborted = true; this.abortedAt = stage.name; } }`",
    "report: `console.log(\\`=== PIPELINE: ${this.pipelineName} ===\\`); this.stages.forEach(s => console.log(\\`${s.status} ${s.name} ${s.duration}ms\\`)); console.log('---'); conteos; veredicto`",
]),
"grid_map_json": None,
},
]
