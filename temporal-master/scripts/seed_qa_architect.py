"""
seed_qa_architect.py — QA Senior Architect: 100 Niveles (Sector 20)
====================================================================
Disciplina: QA de Ecosistemas Críticos

Bloques:
    001–020: Arquitectura de Pruebas y Estrategia Shift-Left
    021–040: Automatización E2E (Playwright/Cypress/Selenium)
    041–060: CI/CD, GitHub Actions, Jenkins, Docker para QA
    061–080: API Testing, Microservicios y Contratos (Postman, Pact)
    081–100: Pruebas No Funcionales + Liderazgo Técnico

Uso:  python -m scripts.seed_qa_architect
"""
from __future__ import annotations
import asyncio, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.core.config import settings
from app.models.challenge import Challenge, DifficultyTier

# ─── Helpers ──────────────────────────────────────────────────────────────────

def _t(tier: str) -> DifficultyTier:
    return {"easy": DifficultyTier.BEGINNER, "medium": DifficultyTier.INTERMEDIATE, "hard": DifficultyTier.ADVANCED}[tier]

def _level(n, title, desc, briefing, theory, difficulty, xp, phase, concepts, code, expected, inputs, hints):
    return {
        "title": title, "description": desc, "difficulty_tier": _t(difficulty),
        "difficulty": difficulty, "sector_id": 20, "level_order": n,
        "base_xp_reward": xp, "is_project": n % 20 == 0, "telemetry_goal_time": 180 + n * 3,
        "challenge_type": "python", "phase": phase, "codex_id": "qa_senior_architect",
        "concepts_taught_json": json.dumps(concepts, ensure_ascii=False),
        "initial_code": code, "expected_output": expected,
        "test_inputs_json": json.dumps(inputs), "lore_briefing": briefing,
        "theory_content": theory, "pedagogical_objective": f"Nivel {n} de QA Senior Architect.",
        "syntax_hint": "", "hints_json": json.dumps(hints, ensure_ascii=False),
    }

# ═══════════════════════════════════════════════════════════════════════════════
# BLOQUE 1: Niveles 1–20 — Arquitectura de Pruebas & Shift-Left
# ═══════════════════════════════════════════════════════════════════════════════

B1_DATA = [
  ("Clasificador de Severidades",
   "Implementa classify_bug(desc) que retorne CRITICAL, HIGH, MEDIUM o LOW según palabras clave.",
   "Operador, un triage eficiente separa al QA junior del architect. Aprende a clasificar la amenaza antes de perseguirla.",
   "## Severidad de Bugs\n\nLa severidad clasifica el **impacto técnico**:\n- CRITICAL: data loss, security breach\n- HIGH: feature broken, no workaround\n- MEDIUM: feature broken, workaround exists\n- LOW: cosmetic, typo\n\n```python\ndef classify_bug(desc):\n    d = desc.lower()\n    if 'data loss' in d or 'security' in d:\n        return 'CRITICAL'\n    # ...\n```",
   "easy", 100, ["clasificación_bugs","severidad","triage"]),
  ("Prioridad vs Severidad",
   "Dado un bug con severidad y contexto de negocio, determina la prioridad de fix.",
   "No todo bug crítico se arregla primero. La prioridad la dicta el negocio, no la técnica.",
   "## Prioridad ≠ Severidad\n\n| Severidad | Prioridad | Ejemplo |\n|-----------|-----------|--------|\n| CRITICAL | LOW | Bug en feature deprecated |\n| LOW | CRITICAL | Typo en precio del checkout |",
   "easy", 110, ["prioridad","severidad","contexto_negocio"]),
  ("Matriz de Riesgo",
   "Calcula risk_score = probability * impact para una lista de features y ordena de mayor a menor.",
   "El QA Architect prioriza por riesgo, no por intuición. La matriz es tu brújula.",
   "## Risk-Based Testing\n\n```python\nrisk = probability * impact\n```\nProbability: 1-5, Impact: 1-5. Score máximo = 25.",
   "easy", 120, ["risk_matrix","probabilidad","impacto"]),
  ("Test Plan Generator",
   "Genera un test plan básico: dado un feature name, produce las secciones requeridas.",
   "Un test plan no es burocracia — es la arquitectura de tu defensa.",
   "## Estructura de un Test Plan\n\n1. Scope\n2. Approach\n3. Test Items\n4. Pass/Fail Criteria\n5. Deliverables",
   "easy", 130, ["test_plan","documentación","scope"]),
  ("Shift-Left Calculator",
   "Calcula el costo de un bug en cada fase: requisitos ($1x), desarrollo ($10x), QA ($100x), producción ($1000x).",
   "Cuanto más tarde encuentras un bug, más caro es matarlo. Shift-Left no es filosofía — es matemática.",
   "## Costo del Defecto por Fase\n\nLa regla del 10x:\n```\nRequisitos:  $100\nDesarrollo:  $1,000\nQA:          $10,000\nProducción:  $100,000\n```",
   "easy", 140, ["shift_left","costo_defecto","fases"]),
  ("Boundary Detector",
   "Dada una especificación de rango [min, max], genera los 5 boundary values canónicos.",
   "Los bugs habitan en las fronteras. Tu trabajo es vigilar cada una.",
   "## Boundary Value Analysis\n\nPara rango [18, 65]:\n- min-1: 17\n- min: 18\n- nominal: 41\n- max: 65\n- max+1: 66",
   "easy", 150, ["BVA","boundary_values","edge_cases"]),
  ("Equivalence Partitioner",
   "Divide un dominio de entrada en clases de equivalencia válidas e inválidas.",
   "No puedes probar todo. Pero puedes probar inteligentemente dividiendo el universo en clases.",
   "## Equivalence Partitioning\n\nCada clase de equivalencia se comporta igual ante el sistema.\nPrueba 1 valor por clase = cobertura máxima con mínimos tests.",
   "easy", 150, ["equivalence_partitioning","clases","dominio"]),
  ("Decision Table Builder",
   "Construye una tabla de decisión para un sistema de descuentos con 3 condiciones booleanas.",
   "Cuando hay múltiples condiciones combinadas, la tabla de decisión elimina la ambigüedad.",
   "## Decision Tables\n\n| Cond1 | Cond2 | Cond3 | Acción |\n|-------|-------|-------|--------|\n| T | T | T | Desc 30% |\n| T | T | F | Desc 20% |",
   "medium", 180, ["decision_table","combinatoria","condiciones"]),
  ("State Transition Mapper",
   "Modela las transiciones de estado de un pedido: PENDING→PAID→SHIPPED→DELIVERED.",
   "Un sistema sin modelo de estados es un sistema sin control. Mapea antes de probar.",
   "## State Transition Testing\n\nEstados: PENDING, PAID, SHIPPED, DELIVERED, CANCELLED\nTransiciones válidas definen el happy path.\nTransiciones inválidas son vectores de ataque.",
   "medium", 190, ["state_machine","transiciones","estados"]),
  ("Test Case Prioritizer",
   "Ordena test cases por prioridad usando: risk * frequency * visibility.",
   "Con 10,000 tests y 2 horas de sprint, ¿cuáles ejecutas? El prioritizer decide.",
   "## Test Prioritization\n\n```python\nscore = risk * frequency * visibility\n```\nEjecuta primero los de mayor score. Esto es regression testing inteligente.",
   "medium", 200, ["priorización","regression","scoring"]),
  ("Defect Density Analyzer",
   "Calcula defect density = bugs_found / KLOC para cada módulo y encuentra el más problemático.",
   "El módulo con mayor densidad de defectos necesita más cobertura — o un refactor.",
   "## Defect Density\n\n```\nDD = bugs / (lines_of_code / 1000)\n```\nUn DD > 10 indica código de alto riesgo.",
   "medium", 210, ["defect_density","métricas","KLOC"]),
  ("Coverage Gap Finder",
   "Compara features implementadas vs features con tests y reporta el gap de cobertura.",
   "La cobertura del 80% suena bien hasta que descubres que el 20% sin cubrir es el checkout.",
   "## Coverage Analysis\n\nCobertura = features_tested / total_features * 100\nEl gap son las features sin tests — y cada una es una bomba de tiempo.",
   "medium", 220, ["cobertura","gap_analysis","features"]),
  ("Regression Suite Optimizer",
   "Dado un changeset (lista de archivos modificados), selecciona solo los tests afectados.",
   "Ejecutar 10,000 tests por cada PR no escala. Impact analysis te dice cuáles importan.",
   "## Impact Analysis\n\nMapea: archivo_modificado → tests_que_lo_cubren\nEjecuta solo los impactados. Reduce el CI de 45min a 3min.",
   "medium", 230, ["regression","impact_analysis","optimización"]),
  ("Exploratory Testing Charter",
   "Genera un charter de testing exploratorio: Target, Resources, Information, Duration.",
   "El testing exploratorio no es 'clickear random' — es una misión con objetivo y tiempo límite.",
   "## Session-Based Test Management\n\nCharter = qué explorar + por qué + cuánto tiempo\n```\nTarget: Checkout flow\nRisk: Double charging\nDuration: 30 min\n```",
   "medium", 240, ["exploratory_testing","charter","SBTM"]),
  ("Bug Report Validator",
   "Valida que un bug report tenga todos los campos obligatorios: title, steps, expected, actual, severity.",
   "Un bug report incompleto es ruido. El QA Architect establece el estándar de calidad del reporte.",
   "## Bug Report Quality\n\nCampos obligatorios:\n1. Title (< 80 chars, descriptivo)\n2. Steps to reproduce\n3. Expected result\n4. Actual result\n5. Severity + Priority",
   "medium", 250, ["bug_report","calidad","validación"]),
  ("Test Estimation Engine",
   "Estima horas de testing usando: test_cases * avg_time * complexity_factor.",
   "Cuando el PM pregunta '¿cuánto tarda QA?', tu respuesta debe ser un número, no 'depende'.",
   "## Test Estimation\n\n```python\nhours = (test_cases * avg_minutes * complexity) / 60\n```\nComplexity: 1.0 (simple), 1.5 (medium), 2.0 (complex)",
   "hard", 280, ["estimación","planning","métricas"]),
  ("Quality Gate Enforcer",
   "Implementa un quality gate que bloquee el release si: bug_count > threshold OR coverage < min.",
   "El quality gate es la última línea de defensa antes de producción. Si no pasa, no sale.",
   "## Quality Gates\n\n```python\ndef can_release(bugs, coverage, threshold=0, min_cov=80):\n    return bugs <= threshold and coverage >= min_cov\n```",
   "hard", 300, ["quality_gate","release","bloqueo"]),
  ("Root Cause Analyzer",
   "Implementa el método de los 5 Porqués: dado un síntoma, encadena causas hasta la raíz.",
   "El QA junior arregla el síntoma. El QA Architect mata la causa raíz.",
   "## 5 Whys Method\n\nPor qué falló → timeout\nPor qué timeout → query lenta\nPor qué lenta → sin índice\nPor qué sin índice → no hay DBA review\nPor qué no review → no está en el checklist\n\n**Causa raíz: proceso, no código.**",
   "hard", 320, ["root_cause","5_whys","análisis"]),
  ("Test Strategy Document",
   "Genera un test strategy completo: approach, tools, environments, risks, schedule.",
   "La estrategia define el CÓMO global. Sin ella, cada QA prueba a su manera — y eso es caos.",
   "## Test Strategy vs Test Plan\n\nStrategy = visión global del proyecto\nPlan = detalle por fase/sprint\n\nEl Architect escribe la Strategy. El equipo ejecuta el Plan.",
   "hard", 350, ["strategy","documentación","visión"]),
  ("CONTRATO-QA-020: Auditoría de Calidad",
   "Proyecto integrador: analiza un sistema completo, calcula métricas de calidad y emite veredicto GO/NO-GO.",
   "Has completado el primer bloque. Este contrato demuestra que puedes auditar un sistema real.",
   "## Proyecto: Auditoría de Calidad\n\nCombina: severidad, prioridad, densidad de defectos,\ncobertura, quality gates y estimación.\n\nInput: métricas del sistema\nOutput: Reporte GO / NO-GO con justificación",
   "hard", 500, ["auditoría","integración","go_no_go"]),
]

# ═══════════════════════════════════════════════════════════════════════════════
# BLOQUE 2: Niveles 21–40 — Automatización E2E
# ═══════════════════════════════════════════════════════════════════════════════

B2_DATA = [
  ("Selector Strategy",
   "Implementa una función que elija el mejor selector CSS/XPath para un elemento dado.",
   "El selector correcto es la diferencia entre un test estable y un test flaky.", "", "easy", 160, ["selectores","CSS","XPath"]),
  ("Page Object Model",
   "Diseña un Page Object para una página de login: locators + actions + assertions.",
   "Sin POM, tus tests son espagueti. Con POM, son arquitectura.", "", "easy", 170, ["POM","page_object","abstracción"]),
  ("Wait Strategy Engine",
   "Implementa 3 tipos de wait: implicit, explicit, fluent — y decide cuándo usar cada uno.",
   "El 90% de los tests flaky se arreglan con la estrategia de wait correcta.", "", "easy", 180, ["waits","explicit_wait","flaky"]),
  ("Test Data Factory",
   "Crea una factory que genere datos de prueba válidos: users, emails, addresses.",
   "Los tests que dependen de datos hardcodeados son frágiles. Las factories son resilientes.", "", "easy", 180, ["test_data","factory","generación"]),
  ("Screenshot on Failure",
   "Implementa un decorator que capture screenshot automáticamente cuando un test falla.",
   "Un test que falla sin evidencia es un misterio. El screenshot es tu testigo.", "", "medium", 200, ["screenshots","debugging","decorators"]),
  ("Cross-Browser Matrix",
   "Genera una matriz de compatibilidad browser × OS y calcula el total de combinaciones.",
   "Chrome en Mac ≠ Chrome en Windows. La matriz de compatibilidad define tu superficie de prueba.", "", "medium", 210, ["cross_browser","matriz","compatibilidad"]),
  ("Retry Mechanism",
   "Implementa un retry decorator: reintenta un test N veces antes de marcarlo como FAIL.",
   "Los tests flaky existen. El retry los contiene mientras investigas la causa raíz.", "", "medium", 220, ["retry","flaky_tests","resiliencia"]),
  ("Parallel Test Splitter",
   "Divide una suite de N tests en M workers balanceando por tiempo de ejecución estimado.",
   "Paralelizar sin balancear crea workers ociosos. El splitter optimiza el throughput.", "", "medium", 230, ["paralelismo","splitting","balanceo"]),
  ("Visual Regression Detector",
   "Compara dos snapshots pixel a pixel y calcula el porcentaje de diferencia.",
   "El CSS cambió y nadie lo notó. La regresión visual detecta lo que el ojo humano no ve.", "", "medium", 240, ["visual_regression","pixel_diff","snapshots"]),
  ("Test Report Generator",
   "Genera un reporte HTML de resultados: passed, failed, skipped, duration, pass rate.",
   "Los resultados crudos son datos. El reporte es información. El stakeholder necesita información.", "", "medium", 250, ["reporting","HTML","métricas"]),
  ("Locator Validator",
   "Valida que un conjunto de locators CSS sigan las best practices: no IDs auto-generados, no índices.",
   "Un locator frágil es una deuda técnica que paga intereses en cada CI run.", "", "medium", 260, ["locators","validación","best_practices"]),
  ("Action Chain Builder",
   "Construye una cadena de acciones: hover → wait → click → type → submit.",
   "Las interacciones complejas requieren cadenas de acciones precisas y ordenadas.", "", "medium", 270, ["action_chains","interacciones","secuencias"]),
  ("Iframe Navigator",
   "Implementa switch_to_frame y switch_back para navegar entre iframes anidados.",
   "Los iframes son el laberinto del DOM. Sin navegación precisa, tus tests se pierden.", "", "hard", 290, ["iframes","navegación","DOM"]),
  ("File Upload Tester",
   "Implementa un test que sube un archivo, verifica el nombre y tamaño mostrados.",
   "El upload de archivos tiene edge cases: tamaño máximo, tipo inválido, nombre con caracteres especiales.", "", "hard", 300, ["file_upload","edge_cases","validación"]),
  ("Drag & Drop Automator",
   "Simula drag and drop entre dos elementos y verifica el estado resultante.",
   "Las interacciones de drag & drop requieren coordinación precisa de eventos del mouse.", "", "hard", 310, ["drag_drop","eventos","interacción"]),
  ("Multi-Tab Handler",
   "Gestiona tests que abren múltiples tabs: switch, verify, close en orden correcto.",
   "Los tests multi-tab son frágiles si no gestionas el window handle correctamente.", "", "hard", 320, ["multi_tab","window_handles","gestión"]),
  ("Shadow DOM Piercer",
   "Accede a elementos dentro de Shadow DOM usando la estrategia correcta.",
   "El Shadow DOM encapsula componentes. Para testearlo, necesitas piercing strategies.", "", "hard", 330, ["shadow_DOM","encapsulación","piercing"]),
  ("Mobile Responsive Tester",
   "Configura viewports móviles y verifica que elementos se muestren/oculten según breakpoint.",
   "El 60% del tráfico es mobile. Si tus tests solo cubren desktop, cubres el 40%.", "", "hard", 350, ["responsive","mobile","viewports"]),
  ("Accessibility Audit Engine",
   "Ejecuta validaciones WCAG básicas: alt text, contrast ratio, tab order.",
   "La accesibilidad no es opcional — es un requisito legal y ético. El QA Architect lo audita.", "", "hard", 380, ["a11y","WCAG","accesibilidad"]),
  ("CONTRATO-QA-040: Suite E2E Completa",
   "Proyecto integrador: diseña y ejecuta una suite E2E completa para un checkout flow.",
   "Has dominado la automatización E2E. Este contrato demuestra tu arquitectura de tests.",
   "## Proyecto: Suite E2E\n\nCombina: POM, waits, retries, reporting, cross-browser.\nInput: especificación del checkout\nOutput: suite ejecutable con reporte", "hard", 500, ["suite_e2e","integración","checkout"]),
]

# ═══════════════════════════════════════════════════════════════════════════════
# BLOQUE 3: Niveles 41–60 — CI/CD & Infraestructura
# ═══════════════════════════════════════════════════════════════════════════════

B3_DATA = [
  ("YAML Pipeline Parser","Parsea un archivo YAML de CI/CD y extrae los stages definidos.","El pipeline es el corazón del CI. Si no lo entiendes, no puedes optimizarlo.","","easy",170,["YAML","CI_CD","parsing"]),
  ("Git Hook Validator","Valida que un pre-commit hook ejecute linting y tests antes del push.","El pre-commit hook es tu primera línea de defensa — antes de que el código entre al repo.","","easy",180,["git_hooks","pre_commit","linting"]),
  ("Docker Test Environment","Genera un Dockerfile para un entorno de testing con Python + pytest.","Docker garantiza que tus tests corran igual en local que en CI. Sin 'works on my machine'.","","easy",190,["Docker","entorno","reproducibilidad"]),
  ("GitHub Actions Workflow","Diseña un workflow de GitHub Actions que ejecute tests en push y PR.","GitHub Actions es el CI/CD más accesible. Domínalo y dominas el pipeline de calidad.","","easy",200,["GitHub_Actions","workflow","automatización"]),
  ("Environment Variable Manager","Gestiona secrets y config para diferentes entornos: dev, staging, prod.","Los secrets hardcodeados son vulnerabilidades. El env manager los centraliza y protege.","","medium",220,["env_vars","secrets","configuración"]),
  ("Test Parallelization Config","Configura pytest-xdist para ejecutar tests en paralelo en CI.","Un CI de 45 minutos mata la productividad. La paralelización lo baja a 8.","","medium",230,["paralelismo","pytest_xdist","CI"]),
  ("Artifact Collector","Recolecta y almacena artifacts de test: reports, screenshots, logs.","Sin artifacts, un test fallido en CI es un misterio. Con artifacts, es un caso resuelto.","","medium",240,["artifacts","logs","evidencia"]),
  ("Matrix Build Strategy","Configura una build matrix: Python 3.10/3.11/3.12 × Ubuntu/Windows.","La matrix build garantiza compatibilidad cross-platform sin duplicar workflows.","","medium",250,["matrix_build","cross_platform","versiones"]),
  ("Pipeline Stage Gate","Implementa gates entre stages: si smoke tests fallan, no ejecuta regression.","Los stage gates ahorran recursos: si lo básico falla, no tiene sentido ejecutar lo complejo.","","medium",260,["stage_gate","pipeline","optimización"]),
  ("Flaky Test Quarantine","Detecta tests flaky por historial y muévelos a quarantine automáticamente.","Un test flaky que bloquea el CI es peor que no tener test. La quarantine lo contiene.","","medium",270,["flaky_tests","quarantine","estabilidad"]),
  ("Docker Compose Test Stack","Orquesta un stack de testing: app + DB + redis usando docker-compose.","Los integration tests necesitan infraestructura real. Docker Compose la orquesta.","","hard",290,["docker_compose","stack","integración"]),
  ("Jenkins Pipeline Converter","Convierte un Jenkinsfile declarativo a GitHub Actions y viceversa.","La migración de CI es inevitable. El QA Architect traduce pipelines entre plataformas.","","hard",300,["Jenkins","migración","traducción"]),
  ("Test Coverage Reporter","Integra coverage.py con el CI y bloquea merges si coverage < threshold.","La cobertura sin enforcement es una métrica vanidosa. El gate la hace accionable.","","hard",310,["coverage","threshold","enforcement"]),
  ("Notification Bot","Envía notificaciones de resultados de tests a Slack/Teams con resumen.","El equipo necesita saber el estado del build sin abrir el CI. El bot lo comunica.","","hard",320,["notificaciones","Slack","comunicación"]),
  ("Performance Baseline CI","Establece baselines de performance en CI y alerta si hay regresión.","La regresión de performance es silenciosa. Sin baseline, no la detectas hasta producción.","","hard",330,["performance","baseline","regresión"]),
  ("Scheduled Test Runner","Configura ejecución programada de tests: nightly regression, weekly full suite.","No todo test debe correr en cada push. Los schedules optimizan el uso de recursos.","","hard",340,["scheduling","nightly","regression"]),
  ("Multi-Repo Test Orchestrator","Coordina tests que dependen de múltiples repositorios desplegados juntos.","Los microservicios se despliegan por separado pero fallan juntos. El orquestador los prueba juntos.","","hard",350,["multi_repo","orquestación","microservicios"]),
  ("Rollback Detector","Detecta si un deployment necesita rollback basado en error rate post-deploy.","El canary deployment sin detector de rollback es un kamikaze. El detector es tu paracaídas.","","hard",360,["rollback","canary","deployment"]),
  ("Infrastructure as Test Code","Define la infraestructura de testing como código versionado y reproducible.","Si tu entorno de testing no es código, no es reproducible. Y si no es reproducible, no es confiable.","","hard",380,["IaC","testing_infra","versionado"]),
  ("CONTRATO-QA-060: Pipeline QA Enterprise","Proyecto integrador: diseña un pipeline CI/CD completo con gates, parallelism, y reporting.","Has dominado la infraestructura de QA. Este contrato integra todo en un pipeline enterprise.","","hard",500,["pipeline","enterprise","integración"]),
]

# ═══════════════════════════════════════════════════════════════════════════════
# BLOQUE 4: Niveles 61–80 — API Testing & Contratos
# ═══════════════════════════════════════════════════════════════════════════════

B4_DATA = [
  ("HTTP Method Classifier","Clasifica requests por método HTTP y valida que usen el verbo correcto.","GET para leer, POST para crear, PUT para reemplazar, PATCH para modificar, DELETE para eliminar.","","easy",170,["HTTP","métodos","REST"]),
  ("Status Code Validator","Valida que una API retorne el status code correcto para cada escenario.","200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, 404 Not Found, 500 Internal Error.","","easy",180,["status_codes","validación","HTTP"]),
  ("JSON Schema Validator","Valida que un response JSON cumpla con un schema esperado: tipos, campos requeridos.","El schema es el contrato entre frontend y backend. Si cambia sin avisar, todo se rompe.","","easy",190,["JSON_schema","validación","contrato"]),
  ("Request Builder","Construye requests HTTP con headers, body, query params y auth tokens.","Un request mal construido es un test inválido. El builder garantiza la estructura correcta.","","easy",200,["request","builder","headers"]),
  ("Response Time Asserter","Mide el response time de una API y falla si excede el SLA definido.","Un endpoint que responde en 3s en tests y 30s en producción indica un problema de carga.","","medium",220,["response_time","SLA","latencia"]),
  ("Auth Token Manager","Gestiona tokens JWT: obtener, refrescar, verificar expiración, invalidar.","La autenticación es el perímetro. Si tus tests no manejan tokens correctamente, no prueban nada real.","","medium",230,["JWT","autenticación","tokens"]),
  ("Pagination Tester","Valida paginación: page size, next/prev links, total count, boundary pages.","La paginación tiene bugs clásicos: off-by-one, última página vacía, count incorrecto.","","medium",240,["paginación","boundary","API"]),
  ("Error Response Validator","Valida que los errores de API tengan formato consistente: code, message, details.","Las APIs que retornan errores inconsistentes son un infierno para el frontend.","","medium",250,["error_handling","consistencia","formato"]),
  ("CRUD Flow Tester","Implementa un test completo de CRUD: Create → Read → Update → Delete → Verify deletion.","El CRUD flow es el happy path mínimo. Si esto falla, nada más importa.","","medium",260,["CRUD","flujo","integración"]),
  ("Rate Limiter Tester","Verifica que el rate limiting de una API funcione: N requests/min, luego 429.","Sin rate limiting, tu API es un buffet libre para bots y abusadores.","","medium",270,["rate_limiting","429","throttling"]),
  ("Contract Test Writer","Escribe un consumer-driven contract test usando el patrón Pact.","El contract test valida que producer y consumer están de acuerdo — sin hablar entre sí.","","hard",300,["Pact","contract_testing","consumer_driven"]),
  ("GraphQL Query Tester","Valida queries, mutations y subscriptions de una API GraphQL.","GraphQL permite al cliente pedir exactamente lo que necesita. Y exactamente lo que no debería.","","hard",310,["GraphQL","queries","mutations"]),
  ("Webhook Validator","Valida que un webhook envíe el payload correcto al endpoint de callback.","Los webhooks son fire-and-forget. Si fallan silenciosamente, pierdes datos.","","hard",320,["webhooks","callback","validación"]),
  ("Idempotency Tester","Verifica que operaciones POST/PUT sean idempotentes: misma request = mismo resultado.","Sin idempotencia, un retry = operación duplicada. En pagos, eso es doble cobro.","","hard",330,["idempotencia","retry","seguridad"]),
  ("Data Integrity Checker","Valida integridad referencial entre entidades: orders → users → products.","La integridad referencial rota produce datos huérfanos y reportes incorrectos.","","hard",340,["integridad","referencial","datos"]),
  ("Chaos API Tester","Simula fallos en dependencias externas y valida que tu API degrade gracefully.","El chaos testing no es destrucción — es resiliencia. Tu API debe sobrevivir al caos.","","hard",350,["chaos_testing","resiliencia","degradación"]),
  ("gRPC Service Tester","Valida un servicio gRPC: request/response, streaming, error codes.","gRPC es el protocolo de los microservicios internos. Si no lo pruebas, no pruebas la comunicación real.","","hard",360,["gRPC","microservicios","streaming"]),
  ("API Versioning Validator","Verifica que v1 y v2 de una API coexistan sin romper backwards compatibility.","La backwards compatibility es sagrada. Romperla es romper la confianza del cliente.","","hard",370,["versionado","backwards_compat","migración"]),
  ("Mock Server Builder","Construye un mock server que simule una API externa para tests de integración.","Depender de APIs externas en tests es depender del azar. El mock server te da control total.","","hard",380,["mock_server","aislamiento","integración"]),
  ("CONTRATO-QA-080: API Test Framework","Proyecto integrador: construye un framework de testing de API con auth, validation, reporting.","Has dominado API Testing. Este contrato integra todo en un framework reutilizable.","","hard",500,["framework","API","integración"]),
]

# ═══════════════════════════════════════════════════════════════════════════════
# BLOQUE 5: Niveles 81–100 — Performance & Liderazgo
# ═══════════════════════════════════════════════════════════════════════════════

B5_DATA = [
  ("Load Test Planner","Calcula la carga esperada: concurrent users * requests/sec * test duration.","No puedes testear performance sin un plan de carga. Los números definen la misión.","","easy",180,["load_testing","planificación","carga"]),
  ("Response Time Percentiles","Calcula p50, p90, p95, p99 de una lista de response times.","El promedio miente. Un p99 de 30s significa que 1 de cada 100 usuarios sufre.","","easy",190,["percentiles","latencia","métricas"]),
  ("Throughput Calculator","Mide throughput: requests procesados por segundo bajo carga constante.","El throughput define la capacidad real de tu sistema. Sin medirlo, estás adivinando.","","easy",200,["throughput","capacidad","medición"]),
  ("Resource Monitor","Monitorea CPU, memoria, disco durante un test de carga y detecta bottlenecks.","El bottleneck puede estar en CPU, memoria, disco o red. El monitor te dice dónde buscar.","","medium",220,["monitoring","recursos","bottleneck"]),
  ("Stress Test Escalator","Incrementa carga progresivamente hasta encontrar el breaking point del sistema.","El stress test no busca que funcione — busca dónde se rompe. Y cuánto tarda en recuperarse.","","medium",240,["stress_test","breaking_point","escalación"]),
  ("Spike Test Simulator","Simula un spike de tráfico: 10x carga instantánea durante 30 segundos.","Black Friday, lanzamiento viral, DDoS accidental. Tu sistema debe sobrevivir al spike.","","medium",250,["spike_test","tráfico","resiliencia"]),
  ("Endurance Test Monitor","Ejecuta un test de carga sostenida durante N horas y detecta memory leaks.","Los memory leaks no aparecen en tests cortos. Solo el endurance test los expone.","","medium",260,["endurance","memory_leak","sostenido"]),
  ("SLA Compliance Checker","Verifica que un sistema cumple con su SLA: uptime 99.9%, latency < 200ms.","El SLA es una promesa al cliente. El QA Architect verifica que se cumpla.","","medium",280,["SLA","compliance","uptime"]),
  ("Security Header Scanner","Valida que las responses tengan los security headers requeridos: CSP, HSTS, X-Frame.","Los security headers son gratis de implementar y caros de olvidar.","","hard",300,["security","headers","OWASP"]),
  ("SQL Injection Detector","Prueba inputs maliciosos contra endpoints y detecta vulnerabilidades SQLi.","SQLi es el ataque más antiguo y sigue siendo el más efectivo. El QA lo detecta antes que el hacker.","","hard",320,["SQLi","seguridad","inyección"]),
  ("XSS Vulnerability Scanner","Inyecta payloads XSS en campos de input y verifica que sean sanitizados.","XSS permite ejecutar JavaScript arbitrario en el browser del usuario. Es robo de sesión.","","hard",330,["XSS","sanitización","seguridad"]),
  ("OWASP Top 10 Checklist","Implementa un checklist automatizado de OWASP Top 10 para una API.","OWASP Top 10 es el mínimo de seguridad. Si no lo cubres, no estás probando seguridad.","","hard",340,["OWASP","checklist","seguridad"]),
  ("Test Team Capacity Planner","Calcula la capacidad del equipo de QA: stories/sprint * velocity * availability.","El QA lead necesita números para negociar scope y deadline con el PM.","","medium",260,["capacity","planning","equipo"]),
  ("Quality Dashboard Builder","Diseña un dashboard de calidad: bugs open/closed, coverage trend, flaky rate.","Los stakeholders no leen test reports. Leen dashboards. Dales lo que necesitan.","","medium",280,["dashboard","métricas","visualización"]),
  ("Mentoring Session Planner","Genera un plan de mentoría: skills gap analysis → training path → milestones.","El QA Architect no solo prueba — forma al equipo. La mentoría multiplica el impacto.","","medium",290,["mentoría","skills_gap","formación"]),
  ("Incident Post-Mortem Template","Genera un post-mortem estructurado: timeline, impact, root cause, action items.","El post-mortem no busca culpables — busca mejoras. El template garantiza que no se olvide nada.","","hard",320,["post_mortem","incidentes","mejora_continua"]),
  ("Test Maturity Assessment","Evalúa la madurez del testing en una organización: nivel 1 (ad-hoc) a nivel 5 (optimizado).","Sin assessment, no sabes dónde estás. Sin saber dónde estás, no puedes planificar hacia dónde ir.","","hard",340,["madurez","assessment","TMM"]),
  ("Risk Mitigation Strategist","Diseña estrategias de mitigación para los 5 riesgos más críticos de un proyecto.","El riesgo no mitigado es un bug que aún no ha ocurrido. El Architect mitiga antes de que ocurra.","","hard",360,["riesgo","mitigación","estrategia"]),
  ("QA Transformation Roadmap","Diseña un roadmap de transformación QA: de manual a automatizado en 6 meses.","La transformación QA no es comprar herramientas — es cambiar cultura, procesos y habilidades.","","hard",400,["transformación","roadmap","cultura"]),
  ("CONTRATO-QA-100: El Arquitecto Centinela","Proyecto final: audita calidad, performance, seguridad y emite certificación CENTINELA.","Has llegado al final. Este contrato demuestra que eres un QA Senior Architect completo.","## Proyecto Final\n\nIntegra TODAS las disciplinas:\nCalidad + Performance + Seguridad + Liderazgo\n\nEmite certificación: CENTINELA LEVEL 5","hard",1000,["certificación","integración_total","CENTINELA"]),
]

# ─── Build all 100 levels ─────────────────────────────────────────────────────

def _build_code(n, title):
    return (
        f"# ╔══════════════════════════════════════════════════════╗\n"
        f"# ║  QA SENIOR ARCHITECT — MISIÓN {n:03d}                  ║\n"
        f"# ║  {title[:48]:<48} ║\n"
        f"# ╚══════════════════════════════════════════════════════╝\n"
        f"#\n"
        f"# Implementa la solución aquí\n"
        f"\n"
        f"resultado = input()\n"
        f"print(resultado)\n"
    )

PHASES = ["fundamentos"]*20 + ["automatizacion_e2e"]*20 + ["cicd_infra"]*20 + ["api_contratos"]*20 + ["perf_liderazgo"]*20
ALL_BLOCKS = [B1_DATA, B2_DATA, B3_DATA, B4_DATA, B5_DATA]

def build_all_levels() -> list[dict]:
    levels = []
    for block_idx, block in enumerate(ALL_BLOCKS):
        for i, entry in enumerate(block):
            n = block_idx * 20 + i + 1
            title, desc, briefing, theory, diff, xp, concepts = entry
            full_title = f"[ QA-{n:03d}: {title.upper()} ]"
            levels.append(_level(
                n=n, title=full_title, desc=desc, briefing=briefing,
                theory=theory if theory else f"## {title}\n\n{desc}",
                difficulty=diff, xp=xp, phase=PHASES[n-1], concepts=concepts,
                code=_build_code(n, title),
                expected="OK", inputs=["OK"],
                hints=[
                    f"Revisa la teoría de {title} para entender el concepto.",
                    f"Los conceptos clave son: {', '.join(concepts[:3])}.",
                    f"Misión {n}: aplica {concepts[0]} para resolver el desafío.",
                ],
            ))
    return levels

QA_ARCHITECT = build_all_levels()

# ─── Seed ──────────────────────────────────────────────────────────────────────

async def seed() -> None:
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    async with SessionLocal() as session:
        deleted = await session.execute(delete(Challenge).where(Challenge.sector_id == 20))
        print(f"🧹  QA Architect anterior eliminado — {deleted.rowcount} challenge(s) removidos.")
        print(f"\n🌱  Insertando {len(QA_ARCHITECT)} niveles de QA Senior Architect...\n")
        for data in QA_ARCHITECT:
            challenge = Challenge(**data)
            session.add(challenge)
            if data["level_order"] % 10 == 0 or data["level_order"] <= 5:
                print(f"    [{data['level_order']:03d}] {data['title']:<55} ({data['difficulty'].upper()}, {data['base_xp_reward']} XP)")
        await session.commit()
    await engine.dispose()
    print(f"\n✅  QA Senior Architect — {len(QA_ARCHITECT)} niveles cargados.")
    print(f"    Sector 20 operativo. codex_id = 'qa_senior_architect'\n")

if __name__ == "__main__":
    asyncio.run(seed())
