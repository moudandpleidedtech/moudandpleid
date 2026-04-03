# DAKI_LOG.md — Historial de Operaciones

> Archivo de auto-documentación obligatoria.
> Actualizado al finalizar cada tarea exitosa.

---

## Stack de Producción

| Capa       | Tecnología              |
|------------|-------------------------|
| Frontend   | Next.js 14 (App Router) |
| Backend    | FastAPI (Python)        |
| Base datos | PostgreSQL (Neon)       |
| ORM        | SQLAlchemy async        |
| Auth       | JWT (bcrypt)            |
| IA         | Anthropic Claude API    |
| Deploy     | (pendiente definir)     |

---

## Stack de Producción (actualizado)

| Capa       | Tecnología              |
|------------|-------------------------|
| Frontend   | Next.js 14 (App Router) |
| Backend    | FastAPI (Python)        |
| Base datos | PostgreSQL (Neon)       |
| ORM        | SQLAlchemy async        |
| Auth       | JWT (bcrypt)            |
| IA         | Anthropic Claude API    |
| Pagos      | Stripe (suscripciones)  |
| Deploy     | (pendiente definir)     |

---

## Estado del Sistema

| Módulo                  | Estado         |
|-------------------------|----------------|
| Auth (login/register)   | ✅ Operativo   |
| Hub de usuario          | ✅ Operativo   |
| IDE / CodeWorkspace     | ✅ Operativo   |
| Sistema de niveles XP   | ✅ Operativo   |
| Logros (Achievements)   | ✅ Operativo   |
| InsightFlash            | ✅ Operativo   |
| DAKI Memory (hints)     | ✅ Operativo   |
| Landing Page (slider)   | ✅ Operativo   |
| Dev user seed           | ✅ Operativo   |
| Sala de Contratos       | ✅ Operativo   |
| Audio Engine (DAKI V4)  | ✅ Operativo   |
| Sistema de Sesiones     | ✅ Operativo   |
| Bóveda Alpha (códigos)  | ✅ 100% Operativa — Operación Vanguardia completa |
| **Pasarela Global Stripe** | ✅ **Lista para producción** — checkout + webhook + frontend |

---

## Infraestructura de Producción

| Capa       | Servicio              | Estado         |
|------------|-----------------------|----------------|
| Frontend   | Vercel (Next.js 14)   | ✅ Configurado  |
| Backend    | Render (FastAPI)      | ✅ Configurado  |
| Base datos | Neon (PostgreSQL 15)  | ✅ Configurado  |
| Auth       | JWT + bcrypt          | ✅ Operativo    |
| IA Mentor  | Anthropic Claude API  | ✅ Configurado  |
| Pagos      | Stripe (Fase 2)       | ⏸ Pendiente    |

### Variables de entorno requeridas — Render (Backend)
```
DATABASE_URL     = postgresql+asyncpg://...neon...?ssl=require
DB_SSL           = True
SECRET_KEY       = <secrets.token_hex(32)>
DEBUG            = False
ANTHROPIC_API_KEY = sk-ant-...
ALLOWED_ORIGINS  = ["https://tu-app.vercel.app","https://dakiedtech.com"]
FRONTEND_URL     = https://tu-app.vercel.app
```

### Variables de entorno requeridas — Vercel (Frontend)
```
API_URL = https://tu-api.onrender.com
```
> `API_URL` (sin NEXT_PUBLIC_) es server-side. El next.config.mjs lo usa para el proxy
> rewrite `/api/v1/*` → backend. El frontend nunca expone la URL del backend al browser.

### Arquitectura del proxy (CORS-free)
```
Browser → /api/v1/...  (relativo)
  → Vercel Next.js rewrite (server-side)
  → https://render-api.onrender.com/api/v1/...
```
No se necesita configurar CORS en Render para el frontend. Solo para clientes externos.

### Startup automático del backend (main.py lifespan)
Al arrancar Render, el backend ejecuta en orden:
1. `init_db()` — aplica ~50 ALTER TABLE idempotentes (sin Alembic, seguro)
2. Si `challenges` vacía → `seed_master.seed()` — carga 1000+ niveles de todos los sectores
3. `seed_incursions.seed()` — sincroniza catálogo de incursiones (incluye qa-automation-ops)
4. `seed_tactical_keys.seed()` — llaves tácticas
5. Crea usuario FOUNDER `admin@daki.dev` si no existe

### Secuencia de primer deploy
```bash
# 1. Configurar env vars en Render y Vercel (ver arriba)
# 2. Push a main
git push origin main
# → Render auto-deploy (~3-5 min) → seed automático en primer arranque
# → Vercel auto-deploy (~2 min)
# 3. Verificar en Render Logs: "✅ [seed_incursions] Catálogo sincronizado"
# 4. Testear flujo: / → /register (con VANG-code) → /hub → /misiones
```

### Generación de códigos Alpha para primeros usuarios
```bash
# En Render Shell (o local con DATABASE_URL de prod):
python -m scripts.generate_alpha_codes --count 50
# Verifica en Neon:
SELECT code, is_used FROM alpha_codes ORDER BY created_at DESC LIMIT 10;
```

---

## REFERENCIA TÉCNICA COMPLETA — DAKI EdTech
> Generada el 2026-04-02. Consultar antes de explorar el codebase.

---

### RT-1 · API ENDPOINTS (Backend FastAPI)

#### AUTENTICACIÓN — `/api/v1/auth`
| Método | Ruta | Auth | Body | Respuesta clave |
|--------|------|------|------|----------------|
| POST | `/auth/register` | No | `email, callsign, password, [founder_code]` | `access_token, user_id, callsign, level, role` + cookie `daki_auth` |
| POST | `/auth/login` | No | `email, password` | idem + actualiza `streak_days` + otorga logro login |
| POST | `/auth/logout` | No | — | 204, elimina cookie `daki_auth` |

#### DESAFÍOS — `/api/v1/challenges`
| Método | Ruta | Auth | Params | Respuesta clave |
|--------|------|------|--------|----------------|
| GET | `/challenges` | Opcional | `user_id?` | Lista de `ChallengeOut` con `unlocked`, `completed`, `status` |
| GET | `/challenges/{id}` | Opcional | `user_id?` | `ChallengeOut` completo (hints, theory_content, lore_briefing, test_inputs) |

`ChallengeOut` incluye: `id, title, description, difficulty_tier (1/2/3), base_xp_reward, initial_code, test_inputs, completed, unlocked, level_order, challenge_type, theory_content, lore_briefing, hints[], is_free, codex_id, sector_id`

#### EJECUCIÓN — `/api/v1`
| Método | Ruta | Auth | Body | Respuesta clave |
|--------|------|------|------|----------------|
| POST | `/execute` | Cookie/Bearer | `user_id, challenge_id, source_code (max 20KB), test_inputs, time_spent_ms, daki_level (1-3)` | `output_matched, stdout, stderr, execution_time_ms, error_info{type,line,detail}, daki_message, gamification{xp_earned, new_level, new_total_xp, already_completed, efficiency_bonus_applied}, achievements_unlocked[], insight` |
| POST | `/evaluate` | Opcional | `challenge_id, code (max 20KB), daki_level?, user_id?` | `status, output_matched, stdout, stderr, execution_time_ms, error_info, daki_message` |
| POST | `/compiler/execute` | Cookie/Bearer | `user_id, challenge_id, source_code, daki_level, hints_used` | Similar a `/execute` |
| POST | `/hint` | No | `user_id, challenge_id, source_code, error_output?, fail_count, operator_level` | `hint` (texto, gen. por Claude Haiku). Rate limit: 10/min |

#### USUARIOS — `/api/v1`
| Método | Ruta | Auth | Respuesta clave |
|--------|------|------|----------------|
| GET | `/user/me` | Cookie/Bearer | `UserOut` completo |
| POST | `/users/login` | No | `UserOut` por `callsign` (legacy) |

`UserOut`: `id, callsign, email, total_xp, current_level, streak_days, is_licensed, points, current_rank, subscription_status, trial_end_date, role, league_tier`

#### DAKI IA — `/api/v1/daki`
| Método | Ruta | Body | Respuesta |
|--------|------|------|-----------|
| POST | `/daki/stagnation` | `user_id, challenge_id, idle_minutes, operator_level` | `daki_message` |
| POST | `/daki/intervene` | `user_id, challenge_id, current_code, error_output?, idle_minutes, operator_level` | `daki_message` (max 120 tokens) |
| POST | `/daki/ask` | `user_id, challenge_id, question` | `daki_message` (consulta conceptual libre) |

Motor: Claude Haiku + `context_router` (selecciona persona: DAKI, SALES, TPM) + `memory_service` (últimos 5 eventos del usuario).

#### PvP y ARENA — `/api/v1/duels`
| Método | Ruta | Body | Respuesta |
|--------|------|------|-----------|
| POST | `/duels/challenge` | `user_id` | `DuelOut` (duel_id, challenger, defender, challenge) |
| POST | `/duels/{id}/submit` | `user_id, source_code` | `SubmitOut` (correct, execution_time_ms, elo_delta, winner_id) |
| GET | `/duels/inbox` | `user_id` | Lista duelos pendientes como defensor |
| GET | `/duels/{id}` | — | Estado actual del duelo |

Elo: K=32, emparejamiento ±200 puntos. Ganador = más rápido si ambos correctos.

#### BOSS — `/api/v1/boss`
- POST `/boss/execute` → valida `factorial_iterativo(7) == 5040`, otorga 1500 XP + badge `SYSTEM_KILLER`.

#### ADMIN — `/api/v1/admin`
| Método | Ruta | Auth | Respuesta |
|--------|------|------|-----------|
| POST | `/admin/auth/token` | callsign+pass (is_admin=True) | JWT admin (8h). Rate limit: 5/min |
| GET | `/admin/overview` | JWT admin | total_users, paid_users, conversion_rate, active_last_24h |
| GET | `/admin/drop-off` | JWT admin | Usuarios estancados por nivel |
| GET | `/admin/daki-stats` | JWT admin | Uso de IA por nivel |
| GET | `/admin/recent-users` | JWT admin | Últimos 10 usuarios |

#### PAGOS — `/api/v1/payments`
| Método | Ruta | Auth | Respuesta |
|--------|------|------|-----------|
| POST | `/payments/create-checkout-session` | Cookie/Bearer | `checkout_url` (Stripe) |
| POST | `/payments/webhook` | Stripe-Signature | 200 OK — activa `subscription_status=ACTIVE` |
| POST | `/payments/verify` | X-Admin-Key | Activación manual |

#### ALPHA CODES — `/api/v1/alpha`
- POST `/alpha/redeem` → `{code}` — SELECT FOR UPDATE (bloqueo pesimista), activa TRIAL 30 días.

#### INCURSIONES — `/api/v1/incursions`
- GET `/incursions` — Catálogo de 6 paths: `{id, slug, titulo, status (ACTIVE/ENCRYPTED), ruta, color_acento, icono, orden}`

#### SALUD
- GET `/health` → `{status, app, version}`

---

### RT-2 · PÁGINAS FRONTEND (Next.js 14 App Router)

| Ruta | Acceso | Fetch principal | Renderiza |
|------|--------|-----------------|-----------|
| `/` | Público | Ninguno | HeroSection, VideoDemoSection, SolucionSection, ActivacionSection |
| `/login` | Público | POST `/auth/login` | Terminal de autenticación |
| `/register` | Público | POST `/auth/register` | Protocolo de reclutamiento + migración sesión anterior |
| `/boot-sequence` | Privado | Ninguno | NeuralBoot (onboarding cinematic → `/misiones`) |
| `/hub` | Privado | GET `/user/me`, GET `/incursions` | CampaignMap (6 zonas), DakiChatTerminal, IncursionSelector, DistincionesPanel, RadarMaestriaModal |
| `/misiones` | Privado | GET `/challenges?user_id=` | Lista scrollable + briefing derecho. Soporta `?selected=<id>` para scroll y auto-selección |
| `/challenge/[id]` | Privado | GET `/challenges/{id}`, POST `/execute` | CodeWorkspace completo (Monaco + consola + hints + HUD) |
| `/enigma` | Privado | POST `/enigma/submit` | Grid-based pathfinding (5 mapas, mini-juego dron) |
| `/arena` | Privado | POST `/duels/challenge`, POST `/duels/{id}/submit` | Duelo PvP en tiempo real con timer y elo_delta |
| `/leaderboard` | Privado | GET `/leaderboard` | Top 50 por XP, badges de liga (Bronce/Plata/Oro/Diamante/Arquitecto) |
| `/boss` | Privado | POST `/boss/execute` | TheInfiniteLooper (boss final, 1500 XP, SYSTEM_KILLER) |
| `/bounty` | Privado | — | Generador DDA de misiones personalizadas |
| `/codex/[slug]` | Privado | GET `/incursions` | Módulo de curso secundario (Sales, TPM, QA) |
| `/sector/[id]` | Privado | GET `/sectors/{id}` | Mapa de sector con nodos desbloqueables |
| `/admin/dashboard` | Privado (admin) | GET `/admin/overview`, `/admin/drop-off` | KPIs, moderación, estadísticas |
| `/god-mode` | Privado (FOUNDER) | — | Panel de debug/override total |
| `/contratos/[id]` | Privado | GET `/contracts/{id}` | Contrato individual |
| `/certificado` | Privado | — | Descarga de certificado PDF |

**Middleware (`src/middleware.ts`):** Cookie `enigma_user` requerida para rutas privadas → redirige a `/login`. Si autenticado accede a `/login` o `/register` → redirige a `/hub`.

---

### RT-3 · ZUSTAND STORE (`pq-user`)

```
Campos persistidos en localStorage (key: "pq-user"):
  userId, username, level, previousLevel, totalXp, streakDays,
  completedChallengeIds[], badges[], dakiLevel (1|2|3),
  currentRank, points, isPaid, subscriptionStatus, trialEndDate, role

Actions principales:
  setUser({id, username, current_level, total_xp, streak_days, ...})
  applyGamificationResult({new_level, new_total_xp})  ← llamado tras cada ejecución
  markChallengeCompleted(id)
  earnBadge(badge)
  setIsPaid(bool)
  setSubscription(status, endDate)
  clearUser()  ← logout
```

---

### RT-4 · LOCALSTORAGE KEYS

| Key | Contenido | Cuándo se usa |
|-----|-----------|---------------|
| `pq-user` | Zustand store serializado | Siempre (persist automático) |
| `boot_seen` | `"1"` | Login/Hub: si absent → redirige a `/boot-sequence` |
| `daki_tutorial_step_<challengeId>` | Número de paso (1-4) | Persistir progreso del tutorial tutorial entre recargas |
| `code_draft_<challengeId>` | Código fuente del usuario | Auto-guardado cada 800ms en IDE; limpiado al completar |

---

### RT-5 · MODELOS DE BASE DE DATOS

#### Tabla `users` (campos clave)
`id (UUID PK), email (UNIQUE), callsign (UNIQUE), password_hash, current_level, total_xp, streak_days, elo_rating (default 1200), league_tier, subscription_status (INACTIVE/TRIAL/ACTIVE), trial_end_date, is_licensed, is_admin, role (USER/FOUNDER/ADMIN), stripe_customer_id, daki_level (1-3), badges_json, points, current_rank, mission_state (JSONB), created_at, last_login`

#### Tabla `challenges` (campos clave)
`id (UUID PK), title, description, difficulty_tier (1/2/3), base_xp_reward, initial_code, expected_output, test_inputs_json, level_order, challenge_type, theory_content, lore_briefing, hints_json (array de 3), sector_id, codex_id, is_free, is_phase_boss, prerequisite_challenge_id (FK), strict_match`

#### Tabla `user_progress`
`id, user_id (FK), challenge_id (FK), completed, attempts, hints_used, completed_at, boss_completed, codex_id, score`

#### Tabla `alpha_codes`
`id, code (UNIQUE, formato VANG-XXXX-XXXX), is_used, used_by_user_id (FK), used_at`

#### Tabla `incursions`
`id, slug (UNIQUE), titulo, status (ACTIVE/ENCRYPTED), system_prompt_id, ruta, color_acento, icono, orden`

#### Tabla `duels`
`id, challenger_id (FK), defender_id (FK), challenge_id (FK), status (active/completed/expired), winner_id, elo_delta, challenger_code, defender_code, challenger_time_ms, defender_time_ms`

#### Tabla `daki_interceptions`
`id, user_id (FK), concept_name, mision_flash_json, daki_message, status (pending/passed/expired), expires_at`

#### Otras tablas
`user_metrics, concept_mastery, user_core_memory (event_type: error_frecuente/exito_rapido/tiempo_estancado/subida_rango), daki_session_logs, user_achievements, intelligence_reports, tactical_access_keys, beta_codes, challenge_prerequisites`

---

### RT-6 · SERVICIOS BACKEND (app/services/)

| Servicio | Función principal |
|----------|-------------------|
| `execution_service.py` | Ejecuta código via Piston API (timeout 3s); fallback local solo en DEBUG |
| `gamification_service.py` | XP → Level: `floor(0.1 * sqrt(XP)) + 1`. Bonus eficiencia +20% si time < 50ms (BEGINNER) |
| `elo_service.py` | K=32, expected = `1/(1+10^((loser-winner)/400))`, delta = `max(1, round(32*(1-exp)))` |
| `mastery_service.py` | ConceptMastery: <3 att → +15pts; 3-5 att → +5pts; >5 att → +2pts. Refuerzo si score<40 |
| `achievement_service.py` | Triggers: login, boss_defeated, level_up, challenge_completed |
| `memory_service.py` | CRUD de UserCoreMemory; `format_operator_history()` inyecta contexto en prompts DAKI |
| `context_router.py` | Selecciona persona DAKI según `incursion_id` y `operator_level` |
| `ai_mentor.py` | `get_execute_feedback()` y `get_hint()` — Claude Haiku |
| `league_service.py` | `compute_tier(elo_rating)` → Bronce/Plata/Oro/Diamante |
| `rank_service.py` | `compute_rank(points)` → "Trainee" → "Comandante Supremo" |
| `semantic_cache.py` | Cache LLM en memoria; interfaz Redis-ready (swap transparente) |
| `llm_router.py` | Haiku si nivel≤10 y prompt<150 chars; Sonnet si nivel>10 o Boss Battle |
| `daki_session_service.py` | Abre/cierra sesiones DAKI con opening_message y closing_briefing |
| `alerts.py` | `fire_sale_alert()` → Discord/Telegram al confirmar pago |

---

### RT-7 · COMPONENTES IDE (CodeWorkspace.tsx)

**Refs clave:**
- `editorRef.current` — Instancia Monaco Editor
- `decorationsRef.current` — IEditorDecorationsCollection (error/victory line highlights)
- `challengeStartMs.current` — `Date.now()` al cambiar de challenge (para `time_spent_ms`)
- `handleEjecutarRef.current` — Ref estable para Ctrl+Enter (evita stale closure)
- `audioVictoryRef`, `audioRunRef`, `audioHintRef`, `audioAmbientRef` — HTMLAudioElement refs

**Estado de gaming:**
- `focusMode` — Oculta header; Escape para salir; botón ⊞ en header
- `ambientOn` — Música ambiente loop (`/sounds/hub-ambient.mp3`); botón ♪ en header
- `soundEnabled` — Efectos de sonido; botón SFX en header
- `sessionSecs` — Timer en header (`⏱ MM:SS`), reset al cambiar challenge
- `failStreak` — Intentos fallidos (`N✕` en header); dispara hints en posiciones [1,3,5] (tier 1) o [2,4,6] (tier 2/3)

**Decoraciones Monaco:**
- `.daki-error-line` — Fondo rojo + borde izquierdo (se limpia automáticamente a los 4s)
- `.daki-victory-line` — Fondo verde + borde izquierdo en todas las líneas (2.2s)

**Tutorial multi-step (challenge_type = "tutorial"):**
- 4 pasos: TUTORIAL_STEP_CODES[1..4]
- `syncProgress` barra de calibración: 0% / 25% / 50% / 75% / 100%
- Paso 4 usa evaluación normal del backend (`output_matched`)

**Flujo de ejecución:**
1. Ctrl+Enter o botón EJECUTAR → `handleEjecutar()`
2. `playSound(audioRunRef)` + `resetIdleTimer()`
3. POST `/execute` con `credentials: 'include'`
4. Si `output_matched && !already_completed` → victoria: partículas, `applyVictoryDecoration()`, `playSound(audioVictoryRef)`, combo si ≤ par lines, VictoryModal 700ms después
5. Si error → `triggerShake()`, `anim-error-flash`, `applyErrorDecoration(line)`

---

### RT-8 · FLUJOS DE USUARIO COMPLETOS

#### Flujo 1 — Registro nuevo operador
```
/register → POST /auth/register {email, callsign, password, [founder_code]}
  → cookie daki_auth (httpOnly) + Zustand setUser()
  → si !localStorage.boot_seen → /boot-sequence → /misiones
  → si localStorage.boot_seen → /hub
```

#### Flujo 2 — Login operador existente
```
/login → POST /auth/login {email, password}
  → backend actualiza streak_days + last_login
  → cookie daki_auth + Zustand setUser()
  → si !boot_seen → /boot-sequence → /misiones
  → si boot_seen → /hub
  (Hub: si level > 1 → localStorage.setItem('boot_seen', '1') para retrocompatibilidad)
```

#### Flujo 3 — Misión completa
```
/misiones → GET /challenges?user_id → seleccionar misión
  → /challenge/[id]
  → GET /challenges/{id} → cargar challenge (teoría si theory_content y no completado)
  → Restaurar borrador: localStorage.getItem('code_draft_{id}') ?? initial_code
  → Editar código en Monaco → Ctrl+Enter o EJECUTAR
  → POST /execute → evaluar
  → Si correcto: partículas + victory glow + applyVictoryDecoration + VictoryModal
  → VictoryModal: "CONTINUAR" → /challenge/{next_id} ó /enigma (si challenge_type=drone)
  → VOLVER → /misiones?selected={id} (scroll automático al nodo)
```

#### Flujo 4 — Tutorial
```
/challenge/[tutorial_id] (challenge_type="tutorial")
  → Restaura paso desde localStorage.daki_tutorial_step_{id}
  → 4 pasos: Paso 1 (ejecutar), 2 (sin SyntaxError), 3 (variable operador=), 4 (función correcta)
  → Barra de calibración: 0→25→50→75→100%
  → Al completar: clearItem(daki_tutorial_step_{id}), VictoryModal especial
```

#### Flujo 5 — Pago / desbloqueo premium
```
/hub → nivel 11+ bloqueado → PaywallModal
  → POST /payments/create-checkout-session → checkout_url Stripe
  → Stripe checkout → pago exitoso → webhook POST /payments/webhook
  → Backend: subscription_status=ACTIVE, is_licensed=True
  → Frontend: setIsPaid(true)
```

#### Flujo 6 — PvP Arena
```
/arena → POST /duels/challenge {user_id}
  → Emparejamiento ±200 Elo → DuelOut
  → Editor Monaco → Enviar → POST /duels/{id}/submit
  → Si ambos enviaron → winner = más rápido correcto → elo_delta en pantalla
```

#### Flujo 7 — Alpha Code (primeros usuarios)
```
/register → campo CÓDIGO VANG
  → POST /alpha/redeem {code}
  → SELECT FOR UPDATE → is_used=False?
  → SET is_used=True, subscription_status=TRIAL, trial_end_date=+30 días
```

#### Flujo 8 — DAKI intervención proactiva
```
CodeWorkspace: 2 min sin escribir ni ejecutar
  → useIdleDetection.onStuck()
  → POST /daki/intervene {current_code, error_output, idle_minutes:2}
  → Respuesta: daki_message inyectado en consola como "DAKI INTERRUPT"
  → speakDaki(msg) + activateWaveform(msg)
```

---

### RT-9 · STARTUP Y SEEDS (main.py)

```
Startup order:
  1. Validar SECRET_KEY != "change-me-in-production" (fail-fast)
  2. init_db() → CREATE TABLE IF NOT EXISTS + ALTER TABLE idempotentes
  3. Si challenges vacía → seed_master.seed() + seed_tactical_keys.seed()
  4. seed_incursions.seed() → UPSERT idempotente de 6 incursiones (siempre)
  5. Si DEBUG=True → _ensure_dev_user() → admin@daki.dev / NEXO / DAKIadmin2025 (level 99, FOUNDER)
```

**Generación de alpha codes:**
```bash
python -m scripts.generate_alpha_codes --count 50 --prefix VANG
# Formato: VANG-XXXX-XXXX (alphabet sin O/I/0/1)
# Carga: SELECT FOR UPDATE en redención — anti-race-condition
```

**Incursiones seedeadas (estado actual):**
| Slug | Título | Status | Orden |
|------|--------|--------|-------|
| python-core | Operación Vanguardia | ACTIVE | 1 |
| tpm-mastery | Technical Project Manager | ACTIVE | 2 |
| red-team | Ciberseguridad: Red Team | ENCRYPTED | 3 |
| sales-mastery | Technical Sales Mastery | ACTIVE | 4 |
| qa-senior-architect | QA Senior Architect | ACTIVE | 5 |
| qa-automation-ops | QA Automation: Ops Especiales | ACTIVE | 6 |

---

### RT-10 · CONFIGURACIÓN (Variables de Entorno)

#### Backend (Render)
| Variable | Requerida | Notas |
|----------|-----------|-------|
| `DATABASE_URL` | ✅ | `postgresql+asyncpg://...neon...?ssl=require` |
| `SECRET_KEY` | ✅ | `secrets.token_hex(32)` — fail-fast si valor default |
| `ANTHROPIC_API_KEY` | ✅ | `sk-ant-...` |
| `DEBUG` | ✅ | `False` en producción (oculta /docs, habilita seed devuser) |
| `ALLOWED_ORIGINS` | ✅ | `["https://dakiedtech.com","https://daki-edtech.vercel.app"]` |
| `FRONTEND_URL` | ✅ | URL de Vercel (inyectada en CORS dinámico) |
| `STRIPE_SECRET_KEY` | Pagos | `sk_live_...` |
| `STRIPE_WEBHOOK_SECRET` | Pagos | `whsec_...` |
| `STRIPE_PRICE_ID` | Pagos | `price_...` ($25/mes) |
| `ALERT_DISCORD_WEBHOOK` | Opcional | URL Discord para alertas de venta |

#### Frontend (Vercel)
| Variable | Requerida | Notas |
|----------|-----------|-------|
| `API_URL` | ✅ | Server-side, usado en `next.config.mjs` para el proxy rewrite |
| `NEXT_PUBLIC_API_URL` | ✅ | Client-side fallback (`http://localhost:8000` en dev) |

**Proxy Next.js:** `/api/v1/*` → backend (browser nunca ve la URL de Render).

---

### RT-11 · HOOKS Y UTILIDADES FRONTEND

| Hook/Util | Firma | Uso |
|-----------|-------|-----|
| `useIdleDetection` | `({timeoutMs, onStuck, enabled}) → {resetTimer}` | CodeWorkspace: 2 min inactividad → DAKI interviene |
| `useDakiVoice` | `(dakiLevel, {enabled}) → {speak, cancel, isSpeaking}` | Síntesis de voz Web Speech API para mensajes DAKI |
| `useUserStore` | Zustand store | Global en toda la app |
| `playSound(ref)` | `(HTMLAudioElement ref) → void` | IDE: victory/run/hint sounds (respeta `soundEnabled`) |
| `applyVictoryDecoration()` | `() → void` | Flash verde en todas las líneas del editor (2.2s) |
| `applyErrorDecoration(line)` | `(number) → void` | Resaltado rojo en línea con error (4s) |
| `triggerShake(intensity)` | `('soft'|'hard') → void` | Framer Motion screen shake |

---

### RT-12 · SONIDOS Y ASSETS

| Archivo | Uso | Volumen |
|---------|-----|---------|
| `/sounds/victory.mp3` | Victoria en misión | 100% |
| `/sounds/data-stream.mp3` | Al ejecutar código | 40% |
| `/sounds/daki_alert.mp3` | Al mostrar pista DAKI | 100% |
| `/sounds/hub-ambient.mp3` | Música ambiente IDE (loop) | 12% |
| `/assets/backgrounds/map1-5.png` | Fondos según `level_order` | — |

---

## Arquitectura del Sistema — Mapa de Módulos

### Backend — Endpoints registrados (33 rutas)
| Router          | Prefijo                    | Función                           |
|-----------------|----------------------------|-----------------------------------|
| auth            | /api/v1/auth               | Login, register, JWT              |
| sectors         | /api/v1/levels             | Niveles por sector + codex        |
| challenges      | /api/v1/challenges         | Obtener/evaluar misiones          |
| daki            | /api/v1/daki               | IA Mentor (Anthropic)             |
| payments        | /api/v1/payments           | Stripe checkout + webhooks        |
| gamification    | /api/v1/gamification       | XP, badges, Elo                   |
| admin           | /api/v1/admin              | Solo FOUNDER                      |
| leaderboard     | /api/v1/leaderboard        | Rankings globales                 |
| duels           | /api/v1/duels              | Duelos 1v1                        |
| arena           | /api/v1/arena              | Arena PvP                         |
| contracts       | /api/v1/contracts          | Contratos (D024)                  |
| bounty          | /api/v1/bounty             | Misiones de recompensa            |
| boss            | /api/v1/boss               | Boss fights                       |
| alpha           | /api/v1/alpha              | Canje de códigos VANG-XXXX-XXXX   |
| incursions      | /api/v1/incursions         | Catálogo de formaciones (D021)    |

### Frontend — Páginas (27 rutas)
| Ruta                        | Acceso     | Estado    |
|-----------------------------|------------|-----------|
| /                           | Pública    | ✅ Landing |
| /login                      | Pública    | ✅ JWT     |
| /register                   | Pública    | ✅ Alpha-only |
| /hub                        | Privada    | ✅ Dashboard |
| /misiones                   | Privada    | ✅ Sectores |
| /challenge/[id]             | Privada    | ✅ Monaco IDE |
| /sector/[id]                | Privada    | ✅ Mapa     |
| /boss                       | Privada    | ✅ PvP      |
| /arena                      | Privada    | ✅ Competitivo |
| /leaderboard                | Privada    | ✅ Rankings |
| /codex/[slug]               | Privada    | ✅ Formaciones |
| /admin/dashboard            | FOUNDER    | ✅ Admin    |
| /god-mode                   | FOUNDER    | ✅ God Mode |

### Modelos de base de datos
```
users, challenges, user_progress, daki_interceptions,
alpha_codes, beta_codes, boss_fights, contracts,
bounty_missions, leaderboard_entries, duels, arena_matches,
incursions, certificates, sessions, tactical_keys,
gamification_events, badges, user_badges, payments
```

### Catálogo de Incursiones (seed_incursions.py)
| Slug                  | Título                            | Status    | Orden |
|-----------------------|-----------------------------------|-----------|-------|
| python-core           | Operación Vanguardia              | ACTIVE    | 1     |
| tpm-mastery           | Technical Project Manager (TPM)   | ACTIVE    | 2     |
| red-team              | Ciberseguridad: Red Team          | ENCRYPTED | 3     |
| sales-mastery         | Technical Sales Mastery           | ACTIVE    | 4     |
| qa-senior-architect   | QA Senior Architect               | ACTIVE    | 5     |
| qa-automation-ops     | QA Automation: Operaciones Especiales | ACTIVE | 6     |

### Seeds disponibles (scripts/)
| Script                  | Exporta          | Sector/Codex       |
|-------------------------|------------------|--------------------|
| seed_sector_00..10.py   | SECTOR_0X        | sector_id 0–10     |
| seed_contratos.py       | CONTRATOS        | contratos          |
| seed_qa_architect.py    | QA_ARCHITECT     | sector_id=20       |
| seed_tpm.py             | TPM_MASTERY      | tpm                |
| seed_sales.py           | SALES_MASTERY    | sales              |
| seed_incursions.py      | —                | catálogo incursiones|
| seed_master.py          | —                | orquestador global  |
| generate_alpha_codes.py | —                | CLI generador VANG  |

---

## Estado del Sistema (actualizado 2026-03-30)

| Módulo                      | Estado                                          |
|-----------------------------|-------------------------------------------------|
| Auth (login/register)       | ✅ Alpha-only — código VANG requerido            |
| Hub de usuario              | ✅ Refactor D026 — IntelReport, IncursionSelector|
| IDE / CodeWorkspace         | ✅ Monaco Editor                                 |
| Sistema de niveles XP       | ✅ 1000+ niveles en 11 sectores                  |
| Formaciones (Codex)         | ✅ 6 incursiones — QA, TPM, Sales, Python, RedTeam |
| QA Automation (nueva)       | ✅ Seeded — qa-automation-ops ACTIVE             |
| DAKI IA Mentor              | ✅ Anthropic API integrado                       |
| Sistema de Sesiones         | ✅ session/open + telemetría                     |
| Pasarela Stripe             | ✅ Lista — pendiente vars en Render              |
| Alpha Gate                  | ✅ Códigos VANG-XXXX-XXXX — generador CLI        |
| Landing Page                | ✅ Pública (no autenticados)                     |
| Deploy Backend              | ✅ Render — Dockerfile + Procfile                |
| Deploy Frontend             | ✅ Vercel — proxy rewrite configurado            |

---

## Historial de Operaciones

### 2026-04-02 — Directiva 031: Estructuración del Path QA Automation (10 Niveles Evaluables) ✅

#### Problema resuelto:
El seed de QA Automation existía con 50 niveles teóricos (`expected_output: "OK"`, no evaluables).
D031 reemplaza eso con 10 niveles completamente evaluables auto-corregidos por el motor Piston.

#### Cambios aplicados:

**`temporal-master/app/services/execution_service.py`**
- `_execute_via_piston()` ahora acepta `language: str = "python"` y `version: str = "3.10.0"` como parámetros
- `execute_node_code()` puede llamar Piston con `language="typescript", version="5.0.4"` sin TypeError

**`temporal-master/app/api/v1/endpoints/compiler.py`**
- Import: agregado `execute_node_code` junto a `execute_python_code`
- Routing por `challenge_type`:
  ```python
  challenge_type = getattr(challenge, "challenge_type", "python") or "python"
  if challenge_type == "typescript":
      exec_result = await execute_node_code(payload.source_code, payload.test_inputs)
  else:
      exec_result = await execute_python_code(payload.source_code, payload.test_inputs)
  ```

**`temporal-master/scripts/seed_qa_automation.py`** (reescrito completo)
- 10 niveles reales evaluables (antes: 50 teóricos no evaluables)
- 4 fases con boss fights marcados con `is_phase_boss=True`:

| Level | Título                  | Tipo       | Boss | XP  |
|-------|-------------------------|------------|------|-----|
| L01   | Validador de Email      | python     | -    | 120 |
| L02   | Motor de Assertions     | python     | -    | 140 |
| L03   | Test Suite Class        | python     | ✅   | 200 |
| L04   | Validador Respuesta API | typescript | -    | 160 |
| L05   | Page Object Model       | typescript | ✅   | 220 |
| L06   | Async Flow Simulator    | typescript | -    | 180 |
| L07   | CSS Selector Builder    | typescript | -    | 190 |
| L08   | Test Data Generator     | typescript | ✅   | 240 |
| L09   | Validador Config CI     | typescript | -    | 260 |
| L10   | Orquestador de Suite    | typescript | ✅   | 500 |

- `codex_id = "qa_automation_ops"` en todos
- `expected_output` real y determinístico por nivel
- `initial_code` con TODOs claros (scaffolding evaluable)
- `is_free=True` en L01-L03 (fase ALPHA); `is_free=False` en L04-L10

#### Para activar:
```bash
python -m scripts.seed_qa_automation
```

---

### 2026-04-02 — Directiva 030: Progresión entre Incursiones (Unlock Logic) ✅

#### Cambios:
- `temporal-master/app/models/incursion.py` — campos `prerequisite_incursion_slug`, `total_levels`
- `temporal-master/app/core/database.py` — `ALTER TABLE IF NOT EXISTS` en `init_db()`
- `temporal-master/scripts/seed_incursions.py` — qa-automation-ops: `prerequisite_incursion_slug="python-core"`, `status="ACTIVE"`
- `temporal-master/app/api/v1/endpoints/incursions.py` — endpoint reescrito: `is_unlocked` computado por usuario; `SYSTEM_KILLER` badge desbloquea QA Automation; FOUNDER bypassa todo
- `temporal-master/frontend/src/components/Hub/IncursionSelector.tsx` — `QAAutomationCard` renderizada cuando `slug === 'qa-automation-ops'`; card muestra estado bloqueado/desbloqueado

---

### 2026-04-02 — Directiva 029: Card QA Automation en Hub ✅

#### Cambios:
- `IncursionSelector.tsx`: nueva `QAAutomationCard` con diseño Cyan/Emerald, badges de stack (Python, TypeScript, Playwright, CI/CD), estado bloqueado (candado dorado) y desbloqueado (punto pulsante)
- `hub/page.tsx`: pasa `userId` al `IncursionSelector`
- Lucide icons: `ShieldCheck`, `Zap`, `Lock`, `Terminal`, `GitBranch`

---

### 2026-03-30 — Directiva 014: Auditoría Pre-Lanzamiento y Alpha Gate Enforcement ✅

#### Auditoría de producción ejecutada:
| Área                        | Hallazgo                                    | Acción               |
|-----------------------------|---------------------------------------------|----------------------|
| Endpoint `test-reload`      | Expuesto sin auth en `/api/v1/levels/test-reload` | ✅ Eliminado    |
| `SECRET_KEY` débil          | `"change-me-in-production"` en .env         | Configurar en Render |
| `DEBUG=True`                | Expone /docs y /redoc en prod               | Configurar False en Render |
| `.env` en git               | Verificado: NUNCA committeado — .gitignore correcto | ✅ Seguro    |
| Alpha Gate en register      | Código alpha OPCIONAL (toggle oculto)       | ✅ Hecho obligatorio |
| Nueva incursión QA Automation | `qa-automation-ops` faltaba en catálogo   | ✅ Agregada ACTIVE   |
| `next.config.mjs` proxy     | `API_URL` server-side — correcto            | ✅ Sin cambios       |
| Middleware `/`              | Landing pública → redirect a /hub si auth  | ✅ Correcto          |

#### Archivos modificados:
- `app/api/v1/endpoints/sectors.py` — eliminado endpoint `GET /test-reload`
- `scripts/seed_incursions.py` — agregada incursión `qa-automation-ops` (orden=6, ACTIVE)
- `frontend/src/app/register/page.tsx` — alpha code visible por defecto, obligatorio en submit
- `DAKI_LOG.md` — este registro

#### Decisión de producto confirmada:
- Registro **solo por código Alpha** (`VANG-XXXX-XXXX`). Sin código = sin acceso.
- Estrategia de primeros usuarios: distribución manual de códigos alpha a red cercana.

- **Estado:** ✅ LISTO PARA DEPLOY — pendiente configurar env vars en Render/Vercel

---

### 2026-03-25 — Directiva 013: Conexión E2E Landing → Register → Hub — FLUJO E2E FRONTEND-BACKEND: CERRADO Y AUDITADO ✅

#### Auditoría de estado (pre-fix):
| Componente | Estado | Acción |
|---|---|---|
| Landing CTAs → `/register` | ✅ Correcto | Sin cambios |
| Pase Alpha en register form | ✅ Existe | Error del backend se tragaba silenciosamente → **corregido** |
| `AlphaAccessModal` errores 404/409/429 | ✅ Completo | Sin cambios |
| `DakiChatTerminal` openingMessage | ✅ Prop cableada | Haikus con `\n` se renderizaban en línea única → **corregido** |
| Hub `POST /session/open` | ✅ Cableado | Sin cambios |
| `BossWarningBanner` | ✅ Operativo | Sin cambios |

#### Archivos modificados:
- `frontend/src/app/register/page.tsx` — manejo de errores tácticos del canje alpha
- `frontend/src/components/Hub/DakiChatTerminal.tsx` — `white-space: pre-wrap` en mensajes

#### Fix 1 — Errores tácticos del Pase Alpha en register:
Antes: `catch { /* silent */ }` — si el código era 404/409/429, el usuario veía "REGISTRADO. ABRIENDO EL NEXO..." sin saber que su VANG fue rechazado.
Después:
- 404 → `REGISTRO OK · PASE ALPHA RECHAZADO: CÓDIGO NO ENCONTRADO EN LA BÓVEDA ALPHA.`
- 409 → `REGISTRO OK · PASE ALPHA RECHAZADO: CÓDIGO YA UTILIZADO POR OTRO OPERADOR.`
- 429 → `REGISTRO OK · PASE ALPHA RECHAZADO: DEMASIADOS INTENTOS — ESPERA 60 SEGUNDOS.`
- Red error → `...SIN SEÑAL CON LA BÓVEDA ALPHA. PODRÁS CANJEAR DESDE EL HUB.`
- Estado consola: `'error'` (rojo) cuando hay fallo de alpha, delay extendido a 2400ms para leerlo

#### Fix 2 — Haikus y respuestas multi-línea en DakiChatTerminal:
Antes: `<p>{msg.text}</p>` — los `\n` del backend se ignoraban, haikus aparecían en una sola línea.
Después: `style={{ whiteSpace: 'pre-wrap' }}` — saltos de línea preservados, haikus renderizados correctamente.

- **Estado:** ✅ FLUJO E2E FRONTEND-BACKEND: CERRADO Y AUDITADO

---

### 2026-03-25 — Directiva 012: Auditoría Pre-Vuelo — INFRAESTRUCTURA ALPHA: LISTA PARA FUEGO REAL ✅

#### Resultado de auditoría:
| Componente                          | Estado                                              |
|-------------------------------------|-----------------------------------------------------|
| `users.subscription_status`         | ✅ En modelo + migration `init_db()`                |
| `users.trial_end_date`              | ✅ En modelo + migration `init_db()`                |
| `users.stripe_customer_id`          | ✅ En modelo + migration `init_db()`                |
| `alpha_codes` tabla                 | ✅ Modelo registrado, `create_all` + índice `is_used` |
| `generate_alpha_codes.py`           | ✅ Llama `init_db()` internamente — autocontenido   |
| `.env` local `DATABASE_URL`         | ⚠️ Apuntaba a Docker (`db:5432`) — debe actualizarse a Neon antes de ejecución |
| `DB_SSL=True`                       | ⚠️ Ausente en `.env` local — requerido para Neon    |

#### Bloqueante resuelto (acción requerida por el operador):
Actualizar `.env` con Neon DATABASE_URL + `DB_SSL=True` antes de correr el script.

#### Comandos de activación (secuencia exacta):
```bash
# 1. Instalar stripe (añadido en D011)
pip install -r requirements.txt

# 2. Schema + 50 municiones en un solo comando
cd temporal-master/
python -m scripts.generate_alpha_codes --count 50
```
El script aplica `init_db()` (migrations) y genera los tokens en una sola ejecución.

#### Verificación post-ejecución (Neon SQL Editor):
```sql
SELECT code, is_used, created_at FROM alpha_codes ORDER BY created_at DESC LIMIT 5;
```

- **Estado:** ✅ INFRAESTRUCTURA ALPHA: LISTA PARA FUEGO REAL — schema completo, script validado, comandos confirmados

---

### 2026-03-25 — Directiva 011: Pasarela Global Stripe — El Nexo tiene capacidad de cobro ✅

#### Diagnóstico pre-implementación:
| Componente                          | Estado previo                                                     |
|-------------------------------------|-------------------------------------------------------------------|
| `payments.py` webhook               | ✅ Existente — HMAC genérico, sin `stripe.Webhook.construct_event` |
| `payments.py` checkout-session      | ❌ No existía                                                      |
| `user.stripe_customer_id`           | ❌ No existía — necesario para no duplicar clientes en Stripe      |
| `config.py` STRIPE_*                | ❌ No existía — sin vars de entorno Stripe                         |
| Hub botón de suscripción Stripe     | ❌ No existía                                                      |
| Manejo `?checkout=success`          | ❌ No existía                                                      |

#### Archivos modificados:
- `requirements.txt` — `stripe>=8.0.0` añadido
- `app/models/user.py` — campo `stripe_customer_id: VARCHAR(255)` añadido
- `app/core/config.py` — `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, `STRIPE_PRICE_ID`
- `app/core/database.py` — `ALTER TABLE users ADD COLUMN IF NOT EXISTS stripe_customer_id`
- `app/api/v1/endpoints/payments.py` — reescrito completamente
- `frontend/src/app/hub/page.tsx` — botón Stripe + handler + retorno checkout

#### Arquitectura del flujo de cobro:
```
Usuario → [Hub] → click "SUSCRIBIRSE AL NEXO"
  → POST /api/v1/payments/create-checkout-session  (Bearer JWT)
  → Stripe crea Session con client_reference_id=user_id
  → window.location.href = checkout_url  (abre Stripe Checkout)
  → Usuario paga en Stripe
  → Stripe redirige a /hub?checkout=success  (actualización optimista del store)
  → Stripe envía POST /api/v1/payments/webhook  (Stripe-Signature header)
  → stripe.Webhook.construct_event() valida firma + timestamp
  → checkout.session.completed → user.subscription_status='ACTIVE', stripe_customer_id guardado
```

#### Seguridad del webhook:
- `stripe.Webhook.construct_event()` — valida HMAC-SHA256 + timestamp (ventana 5min, previene replay attacks)
- `client_reference_id` = user UUID — no depende de email (más robusto)
- Rama Stripe separada de la rama HMAC genérica (PayPal/Hotmart compatibilidad preservada)
- `stripe_customer_id` reutilizado en futuros checkouts → no crea clientes duplicados

#### Variables de entorno a configurar en producción (Render/Vercel):
```
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...   # Dashboard → Developers → Webhooks → Signing secret
STRIPE_PRICE_ID=price_...         # Dashboard → Products → precio mensual $25 USD
```

#### Hub — botón de suscripción:
- Visible cuando `!isPaid && subscriptionStatus !== 'ACTIVE'`
- Estética dorada (#FFD700) — diferenciada del verde Pase Alpha (TRIAL)
- Texto contextual: TRIAL → "Convierte tu TRIAL a acceso pleno"; INACTIVE → "$25/mes"
- Estado de carga con spinner mientras redirige a Stripe
- `?checkout=success` → actualización optimista del store + clean URL

- **Estado:** ✅ Nexo listo para cobro global. Primer operador puede pagar hoy.

---

### 2026-03-25 — Directiva 010: Auditoría E2E + Integración Orgánica Frontend ✅

#### Diagnóstico pre-implementación:
| Componente                              | Estado previo                                                |
|-----------------------------------------|--------------------------------------------------------------|
| `BetaProtocolSection` CTAs              | ✅ Ambos `<Link href="/register">` — sin campo alpha          |
| `register/page.tsx` founderCode         | ✅ Existente — toggle `[+]` para Código de Fundador (is_paid) |
| `register/page.tsx` Pase Alpha          | ❌ No existía — canje TRIAL post-registro no implementado    |
| `DakiChatTerminal` opening message      | ❌ Mensaje inicial hardcodeado — no usaba `/session/open`    |
| `hub/page.tsx` session/open             | ❌ No llamaba `POST /api/v1/session/open` en mount            |

#### Archivos modificados:
- `frontend/src/app/register/page.tsx` — Pase Alpha field + canje post-registro
- `frontend/src/components/Hub/DakiChatTerminal.tsx` — prop `openingMessage?` + reemplazo reactivo
- `frontend/src/app/hub/page.tsx` — `POST /session/open` en mount + wiring a `DakiChatTerminal`

#### Flujo orgánico de intercepción (register → Pase Alpha):
1. Usuario llega a `/register` desde landing CTA
2. Al final del form aparece toggle `[+] ¿Tienes un Pase Alpha? Ingresar código VANG-XXXX-XXXX`
3. Campo opcional, desactivado durante submit
4. Tras registro exitoso: si `paseAlpha` → `POST /api/v1/alpha/redeem` con nuevo JWT
5. Si OK → consola muestra `PASE ALPHA ACTIVADO — ACCESO TRIAL CONCEDIDO.`
6. Si falla (silent) → redirige igual a `/hub`, el operador puede canjear desde el modal de hub
7. El hub carga el perfil → `subscription_status='TRIAL'` ya está en el backend

#### DakiChatTerminal — wiring de opening message:
- Nueva prop `openingMessage?: string`
- `useEffect` reactivo: cuando `openingMessage` llega del backend, reemplaza el mensaje inicial hardcodeado
- Si el backend falla → fallback al mensaje hardcodeado de siempre

#### Hub — session/open:
- `useRef` guard (`sessionOpenedRef`) — previene doble llamada en React Strict Mode
- `POST /api/v1/session/open` con `operator_level`, `streak_days`, `callsign`, `hour`
- `session_id` guardado en state (para futura llamada a `close_session`)
- `opening_message` del backend inyectado en `DakiChatTerminal` via prop

- **Estado:** ✅ Flujo E2E completo — landing → register → hub con Pase Alpha orgánico + AI Mentor contextual

---

### 2026-03-25 — Directiva 009: Integración Frontend — Operación Vanguardia + AI Mentor ✅

#### Diagnóstico pre-implementación:
| Componente                        | Estado previo                                      |
|-----------------------------------|----------------------------------------------------|
| `PaywallModal` (checkout/redeem)  | ✅ Existente — multi-uso TacticalKey — **sin cambios** |
| `AlphaAccessModal` (alpha/redeem) | ❌ No existía                                       |
| `BossWarningBanner`               | ❌ No existía                                       |
| `userStore` subscription fields   | ❌ Solo `isPaid`, sin `subscriptionStatus`          |
| Hub wiring                        | ❌ Sin botón Alpha ni Boss Warning                  |

#### Archivos creados:
- `frontend/src/components/UI/AlphaAccessModal.tsx` — modal de canje de Pase Alpha
- `frontend/src/components/UI/BossWarningBanner.tsx` — banner de pre-anuncio Boss Battle

#### Archivos modificados:
- `frontend/src/store/userStore.ts` — nuevos campos + acción `setSubscription`
- `frontend/src/app/hub/page.tsx` — 4 cambios precisos (imports, state, banner, modal)

#### AlphaAccessModal — especificaciones:
- Llama `POST /api/v1/alpha/redeem` con `Authorization: Bearer <JWT>` (token de localStorage)
- Payload: `{ code: "VANG-XXXX-XXXX" }` — user_id viene del JWT, no del body
- Estados: `idle → loading → success → auto-close(1.8s) / error`
- Mensajes de error diferenciados por HTTP status: 401 / 404 / 409 / 429
- On success: `setSubscription('TRIAL', trial_end_date)` + `setIsPaid(true)`
- Formato fecha de expiración: `DD MMM YYYY` en español

#### BossWarningBanner — especificaciones:
- Consulta `GET /api/v1/session/boss-check/{level}` al montarse
- Se muestra solo si `warning=true` (≤ 2 niveles de boss 10/25/50)
- Auto-dismiss a los 12s o con botón de cierre
- Estética: border/text ámbar `#FFB800` — diferenciada del verde operacional

#### userStore — campos nuevos:
```ts
subscriptionStatus: string   // 'INACTIVE' | 'TRIAL' | 'ACTIVE' — persisted
trialEndDate: string | null  // ISO 8601 — persisted
setSubscription(status, endDate): void
```

#### Hub — wiring:
- `BossWarningBanner` montado entre header y contenido principal
- Botón "ACTIVAR PASE ALPHA" visible solo cuando `!isPaid && subscriptionStatus === 'INACTIVE'`
- `AlphaAccessModal` montado al final del JSX, controlled por `showAlphaModal` state

- **Estado:** ✅ Frontend Operación Vanguardia cableado — flujo end-to-end completo

---

### 2026-03-24 — Directiva 008: Auditoría de Bóveda Alpha — Estado de DB ✅

#### Informe de auditoría:

| Elemento                    | Estado en código | Estado en Neon DB        |
|-----------------------------|------------------|--------------------------|
| Tabla `alpha_codes`         | ✅ Definida       | ⏳ Pendiente de `init_db()` |
| `users.subscription_status` | ✅ En `ALTER TABLE` | ⏳ Pendiente de `init_db()` |
| `users.trial_end_date`      | ✅ En `ALTER TABLE` | ⏳ Pendiente de `init_db()` |
| Tabla `daki_session_logs`   | ✅ Definida       | ⏳ Pendiente de `init_db()` |
| 50 Alpha Codes              | ✅ Script listo   | ⏳ Script nunca ejecutado  |

#### Conclusión:
- **Sin Prisma ni Drizzle** — ORM: SQLAlchemy async. Migraciones vía `init_db()` en startup.
- `init_db()` se ejecuta automáticamente en `lifespan()` al arrancar el servidor.
- El script `generate_alpha_codes.py` invoca `init_db()` como primer paso — aplica esquema Y genera códigos en un solo comando.

#### Comando único para aplicar todo:
```bash
cd temporal-master
.venv\Scripts\activate.bat        # Windows CMD
python -m scripts.generate_alpha_codes --count 50
```

- **Estado:** ✅ Auditoría completa — comandos entregados — ejecución pendiente del operador

---

### 2026-03-24 — Directiva 007: Candado Atómico — POST /api/v1/alpha/redeem ✅

- **Archivo creado:** `temporal-master/app/api/v1/endpoints/alpha.py`
- **Archivo modificado:** `temporal-master/app/api/v1/router.py` — router `alpha` añadido

#### Especificaciones del Candado Atómico:

**Input:**
- `Authorization: Bearer <JWT>` — user_id extraído del token (no del body — previene suplantación)
- `body.code` — Alpha Code en formato `VANG-XXXX-XXXX`

**Flujo de transacción (orden estricto):**
```
SELECT alpha_codes WHERE code=? FOR UPDATE   → lock exclusivo de fila
├── código no existe   → HTTP 404
├── is_used = True     → HTTP 409 CONFLICT
└── código válido:
    ├── alpha.is_used = True
    ├── alpha.used_by_user_id = operator.id
    ├── alpha.used_at = now()
    ├── operator.subscription_status = 'TRIAL'
    ├── operator.trial_end_date = now() + 30 días
    └── COMMIT → locks liberados simultáneamente
```

**Prevención de Race Condition:**
- Request A y B llegan con el mismo código en el mismo milisegundo
- A adquiere `FOR UPDATE` lock primero → actualiza → commit
- B espera el lock → lo obtiene → ve `is_used=True` → devuelve 409
- Resultado garantizado: exactamente 1 activación, nunca 2

**Rate limiting:** `5/minute` por IP — anti-brute-force en la Bóveda

**Respuesta de éxito:**
```json
{
    "status": "granted",
    "message": "Acceso Nivel Vanguardia Concedido. Bienvenido al Nexo.",
    "subscription": "TRIAL",
    "trial_end_date": "2026-04-23T15:30:00+00:00"
}
```

- **Estado:** ✅ Backend Operación Vanguardia 100% completado y listo para producción

---

### 🔐 OPERACIÓN VANGUARDIA — BACKEND COMPLETO

| Componente                  | Archivo                                    | Estado      |
|-----------------------------|--------------------------------------------|-------------|
| Schema AlphaCode            | `app/models/alpha_code.py`                 | ✅ Operativo |
| Campos subscription en User | `app/models/user.py`                       | ✅ Operativo |
| Migraciones en init_db()    | `app/core/database.py`                     | ✅ Operativo |
| Fabricante de Munición CLI  | `scripts/generate_alpha_codes.py`          | ✅ Operativo |
| Endpoint de Canje           | `app/api/v1/endpoints/alpha.py`            | ✅ Operativo |

**Endpoint expuesto:** `POST /api/v1/alpha/redeem`
**Siguiente frontera:** Frontend — modal de canje + integración con JWT del hub

---

### 2026-03-24 — Directiva 006: Fabricante de Munición — CLI Generador de Alpha Codes ✅

- **Archivo actualizado:** `temporal-master/scripts/generate_alpha_codes.py`
- **Estrategia de unicidad (sin IntegrityError mid-transaction):**
  1. Genera todos los códigos en memoria con `secrets.choice()` (CSPRNG)
  2. Deduplica el batch con `set()` en memoria
  3. Filtra preexistentes con `SELECT ... WHERE code IN (...)` — una sola query
  4. Inserta solo los nuevos en `session.begin()` atómico (`add_all`)
  → Transacción nunca se aborta a mitad — todos los códigos o ninguno
- **Output en consola:**
  ```
  ▶  Conectando con la Bóveda Alpha (init_db)...
  ▶  Fabricando 50 municiones [VANG-XXXX-XXXX]...
  ▶  Almacenando 50 código(s) en la Bóveda Alpha...

  ──────────────────────────────────────────────
    #    CÓDIGO               ESTADO
  ──────────────────────────────────────────────
    1.   VANG-3K7P-X9QR       [ DISPONIBLE ]
    2.   VANG-8X9P-L2MQ       [ DISPONIBLE ]
    ...
  ──────────────────────────────────────────────

  ✅  50 municiones generadas y almacenadas en la Bóveda Alpha.
  ```
- **Manejo de errores:**
  - `init_db()` falla → `sys.exit(1)` con mensaje claro
  - Duplicados en DB → filtrados vía pre-SELECT, nunca causan abort
  - Error en `session.begin()` → rollback automático del context manager + mensaje
  - Validación de `--count` (1–10.000) antes de conectar a la DB
- **Seguridad del token:**
  - Alfabeto: `[A-Z][0-9]` sin O/0/I/1 (anti-confusión visual)
  - Entropía por código: ~25 bits por segmento × 2 = ~50 bits (resistente a fuerza bruta)

- **Estado:** ✅ Fabricante de Munición operativo · Operación Vanguardia (Fase de Datos) COMPLETA

#### Comando de ejecución:
```bash
cd temporal-master
python -m scripts.generate_alpha_codes --count 50
```

---

### 2026-03-24 — Directiva 005M: Bóveda Alpha — Single-Use Token Schema ✅

- **Diseño de seguridad:** Single-Use Tokens (1 código = 1 activación, nunca reutilizable)
- **Archivos creados:**
  - `temporal-master/app/models/alpha_code.py` — modelo `AlphaCode` (tabla `alpha_codes`)
  - `temporal-master/scripts/generate_alpha_codes.py` — generador seguro de tokens
- **Archivos modificados:**
  - `temporal-master/app/models/user.py` — campos `subscription_status` + `trial_end_date`
  - `temporal-master/app/core/database.py` — imports + `ALTER TABLE` + índices en `init_db()`

#### Modelo `AlphaCode` (tabla `alpha_codes`):
| Campo             | Tipo          | Descripción                                     |
|-------------------|---------------|-------------------------------------------------|
| `id`              | UUID PK       | Identificador único del token                   |
| `code`            | VARCHAR(24)   | Token formato `VANG-8X9P-L2MQ` (único, indexado)|
| `is_used`         | BOOLEAN       | False hasta redención, nunca vuelve a False      |
| `used_by_user_id` | UUID FK→users | Quién lo redimió (NULL hasta redención)          |
| `used_at`         | TIMESTAMPTZ   | Cuándo fue redimido (NULL hasta redención)       |
| `created_at`      | TIMESTAMPTZ   | Cuándo fue generado (auditoría)                  |

#### Campos nuevos en `users`:
| Campo                 | Tipo         | Valores                          |
|-----------------------|--------------|----------------------------------|
| `subscription_status` | VARCHAR(20)  | `'INACTIVE'` \| `'TRIAL'` \| `'ACTIVE'` |
| `trial_end_date`      | TIMESTAMPTZ  | NULL si no está en TRIAL         |

#### Seguridad del token:
- Generado con `secrets.choice()` — criptográficamente seguro
- Excluye caracteres ambiguos: O, 0, I, 1 (anti-confusión visual)
- `SELECT FOR UPDATE` requerido en el endpoint de redención (anti race-condition)
- Índice parcial en `is_used` — acelera dashboards admin de códigos disponibles

#### Comandos para aplicar:
```bash
# Desde temporal-master/ — aplicar schema (se ejecuta automáticamente en startup)
python -m uvicorn main:app --reload

# Generar 50 Alpha Codes para la Operación Vanguardia
python -m scripts.generate_alpha_codes --count 50

# Generar con prefijo personalizado
python -m scripts.generate_alpha_codes --count 100 --prefix VANG
```

- **Estado:** ✅ Schema diseñado con alta seguridad (Single-Use Tokens) · listo para endpoint `/api/v1/alpha/redeem`
- **Próximo paso:** Implementar `POST /api/v1/alpha/redeem` con `SELECT FOR UPDATE` atómico

---

### 2026-03-24 — Directiva 005: Sistema Tutora 24/7 — 6 Características de Sesión ✅

- **Archivos creados:**
  - `temporal-master/app/models/session_log.py` — modelo `DakiSessionLog` (tabla `daki_session_logs`)
  - `temporal-master/app/services/daki_session_service.py` — servicio de sesiones
  - `temporal-master/app/api/v1/endpoints/session.py` — 3 endpoints REST
- **Archivos modificados:**
  - `temporal-master/app/services/daki_persona.py` — nueva función `get_tone_for_context()`
  - `temporal-master/app/api/v1/router.py` — router `session` añadido

#### Feature 1 — Memoria Persistente (`DakiSessionLog`):
  - Tabla: `daki_session_logs`
  - Campos clave: `operator_level`, `streak_days`, `weak_concept`, `dominant_error_type`, `opening_message`, `closing_briefing`
  - Cada sesión guarda el estado completo del Operador para personalizar la siguiente apertura

#### Feature 2 — Voz de Apertura (`POST /api/v1/session/open`):
  - Recupera `ConceptMastery` con `needs_reinforcement=True` y score más bajo
  - Llama a `get_tone_for_context()` para calibrar el tono
  - Genera mensaje con Haiku en ≤160 tokens (contexto ligero)
  - Fallback sin LLM: mensaje pre-escrito basado en racha/concepto/nivel

#### Feature 3 — Pre-anuncio Boss Battle (`GET /api/v1/session/boss-check/{level}`):
  - Bosses en niveles: 10, 25, 50
  - Alerta cuando `_BOSS_WARN_DISTANCE = 2` niveles de distancia
  - Sin DB — cálculo local inmediato, 0ms latencia

#### Feature 4 — Revisión No Solicitada:
  - Wire a través del evento `no_tests_run` ya presente en `_PROACTIVE_EVENTS` de `AIMentorService`
  - El frontend llama a `generate_proactive_hint(user_id, "no_tests_run", current_code)` tras 20min sin ejecución

#### Feature 5 — Tono Diferenciado (`get_tone_for_context` en `daki_persona.py`):
  - Parámetros: `hour (0–23)`, `streak_days`, `error_count`
  - Segmentos temporales: matutino / diurno / nocturno / madrugada
  - Segmentos de racha: élite (14+) / momentum (7+) / buen ritmo (3+) / sin racha
  - Segmentos de errores: alta frustración (5+) / estancamiento (3+) / normal

#### Feature 6 — Briefing de Cierre (`POST /api/v1/session/close`):
  - 3 líneas exactas: consolidado hoy / frente abierto / próxima misión
  - Genera con Haiku en ≤200 tokens
  - Fallback sin LLM: líneas pre-escritas con datos reales de la sesión
  - Persiste `closing_briefing` en `DakiSessionLog` para historial

- **Modelos usados:** `claude-haiku-4-5-20251001` (ambos mensajes — contexto ligero, costo mínimo)
- **Dependencias nuevas:** ninguna
- **Estado:** ✅ DAKI ahora es tutora con memoria persistente y presencia 24/7

---

### 2026-03-24 — Directiva 004.1: AIMentorService — Proactividad y Auto-Escalada ✅

- **Archivo modificado:** `temporal-master/app/services/ai_mentor.py`
- **Cambios en `process_operator_request`:**
  - Nuevo parámetro `failed_attempts: int = 0`
  - Paso B (Auto-escalada): si `failed_attempts >= 3` → fuerza `PREMIUM_MODEL` antes de llamar al router, loggea el evento con `user_id` e `intentos`
  - Nuevo campo en retorno: `escalated: bool`
  - Constante `_ESCALATION_THRESHOLD = 3` (configurable sin tocar lógica)
- **Nuevo método `generate_proactive_hint(user_id, telemetry_event, current_code) -> str`:**
  - Siempre usa `FAST_MODEL` (intervención puntual, no análisis profundo)
  - `chat_history=[]` — sin historial, contexto mínimo
  - `_PROACTIVE_RULES` como `mission_rules` — identidad táctica específica para proactividad
  - Diccionario `_PROACTIVE_EVENTS` con 6 eventos predefinidos: `idle_15_min`, `idle_30_min`, `infinite_loop_warning`, `repeated_same_error`, `copy_paste_detected`, `no_tests_run`
  - Fallback propio independiente del flujo principal
- **Dependencias nuevas:** ninguna
- **Estado:** ✅ Cerebro Táctico de DAKI actualizado con proactividad y auto-escalada

### 2026-03-24 — Directiva 004: AIMentorService — Middleware Integrador ✅

- **Archivo modificado:** `temporal-master/app/services/ai_mentor.py` (añadido al final, sin romper código existente)
- **Clase añadida:** `AIMentorService`
- **Método principal:** `async process_operator_request(user_id, mission_level, mission_rules, user_code, prompt, chat_history, error_msg) -> dict`
- **Flujo de ejecución (orden estricto):**
  - A. `SemanticCacheService.get_cached_response()` → hit: retorno $0, sin LLM
  - B. `PromptBuilderService.build_tactical_prompt()` → compresión de historial + reglas
  - C. `LLMRouterService.route_prompt()` → selección de modelo por nivel/complejidad
  - D. `_call_llm()` → llamada Anthropic real (extrae system msg de la lista, usa API key)
  - E. `SemanticCacheService.save_to_cache()` → persiste para futuros hits
  - F. Retorna `{response, source, model_used, cost, tokens_estimated, latency_ms}`
- **Función auxiliar:** `_call_llm(model_id, messages)` → separa system message, llama `client.messages.create`, retorna `(text, tokens_used)`
- **Fallback de error:** mensaje estándar "Nexo saturado" sin propagar excepción al endpoint
- **Singleton exportado:** `ai_mentor_service`
- **Dependencias nuevas:** ninguna (reutiliza los 3 singletons de la Trinidad ya creados)
- **Preservación:** todas las funciones existentes (`get_hint`, `get_execute_feedback`, `_build_user_message`, etc.) intactas

---

### 🏗️ ESTADO DE LA TRINIDAD — INTEGRADA Y OPERATIVA

| Capa                   | Servicio                | Estado              |
|------------------------|-------------------------|---------------------|
| Selección de modelo    | `LLMRouterService`      | ✅ Operativo        |
| Caché semántico        | `SemanticCacheService`  | ✅ Operativo        |
| Compresión de prompts  | `PromptBuilderService`  | ✅ Operativo        |
| **Orquestador**        | **`AIMentorService`**   | ✅ **Integrado**    |

**Próximo paso sugerido:** exponer `ai_mentor_service.process_operator_request()` en un endpoint `/api/v1/mentor/ask` y conectar con el IDE del Operador.

---

### 2026-03-24 — Directiva 003: PromptBuilderService ✅ TRINIDAD COMPLETADA

- **Archivo creado:** `temporal-master/app/services/prompt_builder.py`
- **Clase:** `PromptBuilderService`
- **Método principal:** `build_tactical_prompt(current_mission_rules, chat_history, new_user_message) -> list[dict]`
- **Lógica de compresión:**
  - System: `DAKI_SYSTEM_IDENTITY` (fija) + `current_mission_rules` del nivel actual únicamente. Temario global prohibido.
  - History: sanitización completa + trim a últimos 3 pares (6 msgs). Mensajes `system` del historial descartados siempre.
  - Salida: `[{"role": ..., "content": ...}]` estándar para Anthropic y OpenAI SDK.
- **Schemas Pydantic:** `ChatMessage` (frozen, validado), `TacticalPrompt` (resultado + métricas)
- **Constantes:** `MAX_HISTORY_PAIRS=3`, `MAX_MISSION_RULES_LEN=2000`, `MAX_USER_MESSAGE_LEN=4000`
- **Estimación de tokens:** heurística ~4 chars/token para logging (sin tiktoken)
- **Dependencias nuevas:** ninguna (solo stdlib)
- **Singleton exportado:** `prompt_builder_service`
- **Estado:** ✅ Operativo

---

### 🛡️ TRINIDAD DE AHORRO DE TOKENS — COMPLETADA

| Servicio               | Responsabilidad                        | Estado      |
|------------------------|----------------------------------------|-------------|
| `LLMRouterService`     | Modelo correcto según nivel/complejidad | ✅ Operativo |
| `SemanticCacheService` | $0 en consultas repetidas (SHA-256)    | ✅ Operativo |
| `PromptBuilderService` | Input tokens mínimos y suficientes     | ✅ Operativo |

**Próximo paso:** Integrar la Trinidad en `ai_mentor.py` y los endpoints de hint/daki.

---

### 2026-03-24 — Directiva 002: SemanticCacheService

- **Archivo creado:** `temporal-master/app/services/semantic_cache.py`
- **Clase:** `SemanticCacheService`
- **Métodos implementados:**
  - `async generate_cache_key(mission_level, user_code, compiler_error) -> str` — SHA-256 sobre inputs normalizados
  - `async get_cached_response(cache_key) -> Optional[str]` — hit/miss con TTL (1h por defecto)
  - `async save_to_cache(cache_key, ai_response)` — escritura con evicción FIFO al llegar a 10.000 entradas
  - `check_error_frequency(mission_level, error_type) -> int` — contador acumulativo por (nivel, tipo_error)
  - `get_stats() -> dict` — métricas en tiempo real (hits, misses, evictions, entradas activas)
  - `invalidate(cache_key)` / `flush()` — control manual del estado
- **Almacenamiento:** dict en memoria (`CacheEntry` dataclass con timestamp y hit counter)
- **Interfaz Redis-ready:** swap transparente implementando `_get`/`_set` con `aioredis` sin cambiar contratos públicos
- **Dependencias nuevas:** ninguna (solo stdlib: `hashlib`, `collections`, `dataclasses`, `time`)
- **Singleton exportado:** `semantic_cache_service`
- **Estado:** ✅ Operativo en memoria · listo para integrar en middleware de endpoints AI

### 2026-03-24 — Directiva 001: LLMRouterService

- **Archivo creado:** `temporal-master/app/services/llm_router.py`
- **Clase:** `LLMRouterService`
- **Método principal:** `async route_prompt(prompt_text: str, mission_level: int) -> str`
- **Lógica:**
  - `FAST_MODEL` (`claude-haiku-4-5-20251001`) → nivel ≤ 10 **y** prompt < 150 chars
  - `PREMIUM_MODEL` (`claude-sonnet-4-6`) → nivel > 10 (Boss Battle) **o** prompt ≥ 150 chars
  - Fallback ante excepción: `PREMIUM_MODEL` (seguridad sobre ahorro)
- **Schemas Pydantic:** `RouterInput`, `RoutingDecision`, `RoutingTier` (enum)
- **Singleton exportado:** `llm_router_service` (listo para `Depends()` en FastAPI)
- **Dependencias nuevas:** ninguna (usa `pydantic` ya presente en el stack)
- **Estado:** mockeado · interfaz estable · listo para inyectar SDK calls

### 2026-04-02 — Directiva 030: Progresión entre Incursiones — QA Automation Unlock ✅

#### Objetivo
Que el sistema reconozca QA Automation como siguiente paso al completar Python Core.
La misión se desbloquea automáticamente cuando el Operador derrota al Boss ∞ LOOPER (medalla `SYSTEM_KILLER`).

#### Cambios por capa

**1. Modelo SQL (`app/models/incursion.py`)**
- `prerequisite_incursion_slug: String(60), nullable` — slug de la Incursión prerequisito
- `total_levels: Integer, nullable` — cantidad total de niveles en la Incursión
- Import agregado: `Integer` de sqlalchemy

**2. Migración idempotente (`app/core/database.py` → `init_db()`)**
```sql
ALTER TABLE incursions ADD COLUMN IF NOT EXISTS prerequisite_incursion_slug VARCHAR(60);
ALTER TABLE incursions ADD COLUMN IF NOT EXISTS total_levels INTEGER;
```
Se ejecuta en cada startup — seguro en Neon producción y local.

**3. Seed (`scripts/seed_incursions.py`)**
- `qa-automation-ops` actualizado:
  - `prerequisite_incursion_slug = "python-core"` 
  - `total_levels = 10`
  - `status = "ACTIVE"` (visible en el Hub)
  - `color_acento = "#06B6D4"` (Cyan, coincide con la card D029)
- Función `seed()` actualiza los nuevos campos en el UPSERT

**4. Endpoint (`app/api/v1/endpoints/incursions.py`)**
- Nueva query param: `user_id: Optional[UUID] = Query(None)`
- `IncursionOut` schema extendido con `prerequisite_incursion_slug`, `total_levels`, `is_unlocked: bool`
- Función `_compute_is_unlocked(incursion, user) → bool`:
  - Sin prerequisito → `True`
  - FOUNDER → `True` (bypassa todo)
  - prerequisito `"python-core"` → verifica badge `SYSTEM_KILLER` en `user.badges_json`
  - Sin user_id → `False` (bloqueada por defecto)
- Función helper `_has_badge(user, badge) → bool` (safe parse de JSON)

**Flujo de desbloqueo:**
```
/boss → POST /boss/execute → éxito → SYSTEM_KILLER badge en users.badges_json
                                        ↓
GET /incursions?user_id={id} → _compute_is_unlocked → is_unlocked=True para qa-automation-ops
                                        ↓
Frontend: QAAutomationCard.locked = False → botón "INGRESAR AL SECTOR" habilitado
```

**5. Frontend `IncursionSelector.tsx`**
- Prop nuevo: `userId?: string`
- Fetch: `/api/v1/incursions?user_id=${userId}` cuando userId disponible
- `IncursionData` interface: agrega `prerequisite_incursion_slug`, `total_levels`, `is_unlocked`
- `QAAutomationCard` props: `isFounder` → `isUnlocked` (más explícito)
- Render: `isUnlocked={inc.is_unlocked || isFounder}` (FOUNDER siempre entra)

**6. Hub (`frontend/src/app/hub/page.tsx`)**
- `<IncursionSelector userId={userId ?? undefined} ...>`

#### Archivos modificados
| Archivo | Cambio |
|---------|--------|
| `app/models/incursion.py` | + `prerequisite_incursion_slug`, `total_levels` |
| `app/core/database.py` | + 2 ALTER TABLE en init_db() |
| `scripts/seed_incursions.py` | qa-automation-ops: prerequisito + total_levels + UPSERT actualizado |
| `app/api/v1/endpoints/incursions.py` | Reescrito con `user_id`, `is_unlocked`, helpers |
| `frontend/src/components/Hub/IncursionSelector.tsx` | userId prop, fetch con query param, `isUnlocked` |
| `frontend/src/app/hub/page.tsx` | Pasa `userId` a IncursionSelector |

#### Estado: ✅ Operativo · Sin migraciones manuales (init_db idempotente)

---

### 2026-04-02 — Directiva 029: Card de Especialidad QA Automation ✅

#### Objetivo
Agregar tarjeta visual imponente para QA Automation (Playwright + TS) en el Hub, diferenciada del Core Python.

#### Implementación
- **Componente nuevo:** `QAAutomationCard` en `IncursionSelector.tsx`
- **Lógica de intercepción:** cuando `slug === 'qa-automation-ops'` → renderiza la card especializada en lugar de la genérica
- **Detección de lock:** `locked = !isFounder` (estado inicial bloqueado; FOUNDER puede entrar)

#### Diseño visual
| Elemento | Detalle |
|----------|---------|
| Gradiente fondo | `rgba(6,182,212,0.05)` → `rgba(16,185,129,0.03)` (Cyan → Emerald) |
| Borde | `rgba(6,182,212,0.28)` → hover `rgba(6,182,212,0.70)` |
| Línea pulso dual-color | Gradiente Cyan + Emerald, animado |
| Hex grid background | `radial-gradient` puntitos Cyan, opacidad 4% |
| Íconos Lucide | `ShieldCheck` (Cyan) + `Zap` (Emerald) con glow animado en hover |
| Stack badges | Python, TypeScript, Playwright, CI/CD — color individual por tag |
| Badge estado | Lock dorado (🔒 + `FFC700`) cuando bloqueado; punto pulsante Cyan cuando activo |
| Descripción hover | "Domina el asedio de software moderno. De scripts locales a Pipelines de élite." |
| CTA bloqueado | "REQUIERE: OPERACIÓN PYTHON FINALIZADA" → hover revela "🔒 COMPLETA EL CORE PYTHON PRIMERO" |
| CTA desbloqueado | "INGRESAR AL SECTOR" con ícono `Terminal` |

#### Dependencia nueva
- `lucide-react@^1.7.0` — instalada en `package.json`

#### Archivos modificados
- `frontend/src/components/Hub/IncursionSelector.tsx`
  - Import: `ShieldCheck, Zap, Lock, GitBranch, Terminal` de `lucide-react`
  - Constantes: `QA_STACK_BADGES`, `BADGE_COLORS`
  - Nuevo componente: `QAAutomationCard`
  - Intercepción en el loop: `slug === 'qa-automation-ops'` → `<QAAutomationCard />`

#### Próximo paso
- Directiva 030: Lógica de desbloqueo real (nivel Python completado → `locked = false`)

#### Estado: ✅ Operativo

---

### 2026-04-02 — Directiva 018: Gaming Experience Desktop — IDE Maximizado ✅

#### Objetivo
Maximizar la experiencia gaming en escritorio antes de adaptar a móvil.

#### 8 mejoras implementadas en `CodeWorkspace.tsx` + `globals.css`:

| # | Mejora | Implementación |
|---|--------|----------------|
| 1 | **Ctrl+Enter** ejecuta código | `editor.addCommand(monaco.KeyMod.CtrlCmd \| monaco.KeyCode.Enter, ...)` en `onMount` |
| 2 | **Efectos de sonido** | `audioVictoryRef`, `audioRunRef`, `audioHintRef` + helper `playSound()` |
| 3 | **Música ambiente** | `audioAmbientRef` loop a 12% volumen + botón ♪ en header |
| 4 | **Session HUD** | Timer `⏱ MM:SS` en tiempo real + contador de intentos `N✕` |
| 5 | **Focus Mode** | Botón ⊞ oculta el header; Escape lo restaura |
| 6 | **Victory line flash** | `applyVictoryDecoration()` → decoraciones Monaco `.daki-victory-line` (2.2s) |
| 7 | **Level-up dramático** | `NivelSubidoOverlay` full-screen: overlay oscuro + scan beam animado + anillos pulsantes |
| 8 | **Cursor cyberpunk** | `.ide-view` CSS con SVG crosshair verde (#00FF41) data-URL |

#### Archivos modificados:
- `frontend/src/components/IDE/CodeWorkspace.tsx`
  - Clase `ide-view` en contenedor principal (activa cursor cyberpunk)
  - Botones en header derecho: ♪ ambient, SFX toggle, ⊞ focus mode
  - Timer `formatTime(sessionSecs)` y contador `failStreak` visibles en HUD
  - **Bugfix:** `useEffect` de `handleEjecutarRef` movido después de la declaración de `handleEjecutar` (error de TDZ — variable usada antes de ser asignada)
- `frontend/src/app/globals.css`
  - `.ide-view` + `.ide-view button/a/[role=button]` con cursor SVG crosshair
  - `.daki-victory-line` — fondo verde semitransparente + borde izquierdo en Monaco
  - `.level-up-scan-beam` + `@keyframes level-up-scan`

#### Estado: ✅ Operativo

---

### 2026-04-02 — Directiva 017: Restauración Misiones, Boot Sequence y UX Hub ✅

#### Restauración de selección en Misiones (`misiones/page.tsx`)
- Parámetro URL `?selected=<UUID>`: al volver del IDE, la misión activa queda visible y seleccionada
- `listRef` + `data-mission-id` en cada botón → `scrollIntoView({ behavior: 'smooth', block: 'center' })`
- "VOLVER A MISIONES" en CodeWorkspace navega a `/misiones?selected=${challengeId}`

#### Persistencia de paso tutorial (`CodeWorkspace.tsx`)
- `localStorage.setItem('daki_tutorial_step_<id>', step)` al cambiar de paso
- Al recargar, restaura paso, progreso y código correspondiente
- Al completar tutorial, limpia la clave

#### Boot Sequence (`login/page.tsx`, `hub/page.tsx`)
- Login: si `localStorage.getItem('boot_seen')` es null → redirige a `/boot-sequence` (nuevo usuario)
- Hub: si `level > 1` → `localStorage.setItem('boot_seen', '1')` (retrocompatibilidad usuarios existentes)
- Usuarios nuevos ven la cinemática de bienvenida; usuarios existentes entran directo al hub

#### Hub — Restauración de Arena y Ligas (`hub/page.tsx`)
- Botón **MODO ARENA** (rojo, ⚔, etiqueta PvP) entre CONTINUAR MISIÓN y Formaciones
- Badge de **liga** en Rango Operacional: ◆ + nombre con color del tier, clickable a `/leaderboard`
- Quick access **LEADERBOARD** renombrado a **LIGAS** con ícono ◆ dorado
- `leagueTier` state extraído del campo `league_tier` en `/user/me`

#### Archivos modificados:
- `frontend/src/app/misiones/page.tsx` — `?selected` URL param + scroll automático
- `frontend/src/components/IDE/CodeWorkspace.tsx` — tutorial step persistence, navegación con `?selected`
- `frontend/src/app/login/page.tsx` — routing a `/boot-sequence` para nuevos usuarios
- `frontend/src/app/hub/page.tsx` — Arena button, league badge, LIGAS, boot_seen guard
- `frontend/src/app/users.py` (backend) — campo `league_tier: str = "Bronce"` en `UserOut`

#### Estado: ✅ Operativo

---

### 2026-04-02 — Directiva 016: Auditoría de Seguridad — Vulnerabilidades Cerradas ✅

#### Vulnerabilidades identificadas y cerradas:

| # | Vulnerabilidad | Solución |
|---|----------------|----------|
| 1 | Token JWT en localStorage (XSS-vulnerable) | Cookie `daki_auth` HttpOnly; Secure en prod, SameSite=Lax en dev |
| 2 | `user_id` spoofing en `/execute` y `/compiler` | JWT del operador autenticado debe coincidir con `body.user_id`; 403 si no coincide |
| 3 | Sin rate limiting en admin y evaluate | `@limiter.limit("5/minute")` en admin login; `"20/minute"` en evaluate |
| 4 | `SECRET_KEY` débil en arranque | `RuntimeError` en startup si valor por defecto |
| 5 | `_ensure_dev_user()` en producción | Guarda `if settings.DEBUG:` |
| 6 | Subprocess fallback sin control en prod | `if os.getenv("DEBUG") in ("1","true"):` else retorna error seguro |
| 7 | Mensajes 409 distintos revelan si email o callsign existe | Unificados: `"Credenciales ya en uso. Verifica tu email o callsign."` |
| 8 | Sin validación de tamaño de entrada en execute/compiler | `Field(max_length=20_000)`, `Field(ge=1, le=3)`, `Field(ge=0, le=100)` |
| 9 | Sin logout que invalide cookie | `POST /auth/logout` con `response.delete_cookie("daki_auth")` |

#### Migración de autenticación frontend (`credentials: 'include'`):
- Todos los fetch a endpoints autenticados usan `credentials: 'include'` en lugar de `Authorization: Bearer ${token}`
- `localStorage.getItem('daki_token')` eliminado de todos los componentes
- Componentes migrados: `hub/page.tsx`, `AlphaAccessModal.tsx`, `IntelReportModal.tsx`, `DakiChatTerminal.tsx`

#### Archivos modificados (backend):
- `app/api/v1/endpoints/auth.py` — `_set_auth_cookie()`, cookie en login/register, `/auth/logout`, 409 unificado
- `app/core/security.py` — `Cookie` import, fallback `daki_auth` cookie en `get_current_operator` y `_optional`
- `app/api/v1/endpoints/compiler.py` — validación user_id vs JWT, Field bounds
- `app/api/v1/endpoints/evaluate.py` — rate limit 20/min, Field bounds
- `app/api/v1/endpoints/admin.py` — rate limit 5/min en admin login
- `app/services/execution_service.py` — subprocess fallback guardado por DEBUG
- `main.py` — SECRET_KEY check + `_ensure_dev_user()` guarded

#### Archivos modificados (frontend):
- `frontend/src/app/register/page.tsx` — sin `localStorage.setItem('daki_token', ...)`
- `frontend/src/app/login/page.tsx` — sin `localStorage.setItem('daki_token', ...)`
- `frontend/src/app/hub/page.tsx` — `credentials: 'include'`, logout llama `POST /auth/logout`
- `frontend/src/components/UI/AlphaAccessModal.tsx` — `credentials: 'include'`
- `frontend/src/components/Hub/IntelReportModal.tsx` — `credentials: 'include'`
- `frontend/src/components/Hub/DakiChatTerminal.tsx` — `credentials: 'include'`

#### Estado: ✅ Cerradas · Listo para producción

---

### 2026-03-24 — Inicialización del Log

- **Acción:** Creación del archivo DAKI_LOG.md y .cursorrules como base del sistema de documentación.
- **Archivos creados:** `DAKI_LOG.md`, `.cursorrules`
- **Dependencias nuevas:** ninguna
- **Estado:** Sistema inicializado. Log activo.

---
