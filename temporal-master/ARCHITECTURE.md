# MOUD & PLEID — PYTHON QUEST
## Documentación Técnica & Arquitectura del Sistema

> Versión: 0.1.0 · Actualizado: 2026-03-17

---

## Tabla de Contenidos

1. [Visión General](#1-visión-general)
2. [Stack Tecnológico](#2-stack-tecnológico)
3. [Estructura del Proyecto](#3-estructura-del-proyecto)
4. [Backend — FastAPI](#4-backend--fastapi)
5. [Frontend — Next.js](#5-frontend--nextjs)
6. [Base de Datos](#6-base-de-datos)
7. [Servicios & Lógica de Negocio](#7-servicios--lógica-de-negocio)
8. [Infraestructura & Docker](#8-infraestructura--docker)
9. [Variables de Entorno](#9-variables-de-entorno)
10. [Flujo Narrativo](#10-flujo-narrativo)
11. [Sistema de Gamificación](#11-sistema-de-gamificación)
12. [Ejecución de Código (Sandbox)](#12-ejecución-de-código-sandbox)
13. [Sistema de IA (ENIGMA & Bounties)](#13-sistema-de-ia-enigma--bounties)
14. [Audio & Assets](#14-audio--assets)
15. [Guía de Desarrollo Local](#15-guía-de-desarrollo-local)
16. [Checklist de Producción](#16-checklist-de-producción)

---

## 1. Visión General

**Python Quest** es una plataforma educativa gamificada para aprender Python, envuelta en una narrativa cyberpunk. Los usuarios son "Operadores" que trabajan junto a **DAKI** (IA Simbionte) para completar **Incursiones** (misiones de código) dentro del **Nexo Digital**.

### Características Principales

| Característica | Estado |
|---|---|
| Editor de código Monaco con ejecución real | ✅ Activo |
| Sistema XP / Niveles / Streaks | ✅ Activo |
| Pistas progresivas DAKI (3 niveles por misión) | ✅ Activo |
| DAKI Linter (errores Python en español) | ✅ Activo |
| Jefe Final: ∞ LOOPER | ✅ Activo |
| Medallas (badges) y Registro de Conquistas | ✅ Activo |
| BGM Ambiental con fade-out de navegación | ✅ Activo |
| Bitácora Táctica (Códice narrativo progresivo) | ✅ Activo |
| Tutorial interactivo Protocolo 00 | ✅ Activo |
| Juego Drones Isométrico (Enigma) | ✅ Activo |
| Leaderboard global (top 50) | ✅ Activo |
| Bounties IA (misiones generadas por Claude) | ✅ Activo |
| PvP Duelos 1v1 con Elo | 🟡 En desarrollo |
| Arena competitiva | 🟡 En desarrollo |

---

## 2. Stack Tecnológico

### Backend
| Tecnología | Versión | Rol |
|---|---|---|
| Python | 3.12 | Lenguaje base |
| FastAPI | 0.115.0 | Framework web async |
| SQLAlchemy | 2.0.35 | ORM async |
| asyncpg | 0.29.0 | Driver PostgreSQL async |
| PostgreSQL | 15-alpine | Base de datos principal |
| Pydantic | 2.9.2 | Validación y serialización |
| pydantic-settings | 2.5.2 | Configuración desde env |
| uvicorn | 0.30.6 | ASGI server |
| httpx | 0.27.2 | Cliente HTTP (Piston API) |
| anthropic | ≥0.50.0 | Claude API (hints + bounties) |
| passlib[bcrypt] | 1.7.4 | Hashing (preparado para Fase 2) |
| python-jose | 3.3.0 | JWT (preparado para Fase 2) |

### Frontend
| Tecnología | Versión | Rol |
|---|---|---|
| Next.js | 14.2.15 | Framework React (App Router) |
| React | 18.3.1 | UI |
| TypeScript | — | Tipado estático |
| Tailwind CSS | — | Estilos utilitarios |
| Framer Motion | 11.11.17 | Animaciones declarativas |
| @monaco-editor/react | 4.6.0 | Editor de código Monaco |
| Zustand | 4.5.5 | State management + persist |
| react-joyride | 2.9.3 | Onboarding interactivo |

### Infraestructura
| Tecnología | Rol |
|---|---|
| Docker + Docker Compose | Orquestación de servicios |
| Piston API (emkc.org) | Sandbox ejecución código remoto |

---

## 3. Estructura del Proyecto

```
temporal-master/
│
├── app/                          # Backend FastAPI
│   ├── api/v1/
│   │   ├── endpoints/            # 14 routers
│   │   └── router.py             # Router principal con prefijo /api/v1
│   ├── models/                   # SQLAlchemy ORM (8 modelos)
│   ├── schemas/                  # Pydantic schemas (request/response)
│   ├── services/                 # Lógica de negocio (9 servicios)
│   └── core/
│       ├── config.py             # Settings (pydantic-settings desde .env)
│       └── database.py           # Engine async + init_db() con migraciones
│
├── frontend/                     # Next.js 14 App Router
│   ├── src/
│   │   ├── app/                  # Páginas (rutas) — App Router
│   │   ├── components/
│   │   │   ├── Boss/             # TheInfiniteLooper
│   │   │   ├── Game/             # BitacoraModal, Drones, MissionBriefing…
│   │   │   ├── IDE/              # CodeWorkspace, DakiHint, TutorialPanel
│   │   │   ├── Tutorial/         # QuestTour (onboarding Joyride)
│   │   │   └── UI/               # HubAudio, ParticleBurst, Toast, TopNav…
│   │   ├── store/
│   │   │   └── userStore.ts      # Zustand + persistencia localStorage
│   │   └── middleware.ts         # Protección de rutas por cookie
│   ├── public/
│   │   ├── sounds/               # Assets de audio (4 archivos MP3)
│   │   └── assets/backgrounds/   # Fondos por nivel de misión (map1–map5)
│   ├── next.config.mjs           # Proxy /api/v1/* → backend
│   └── Dockerfile                # Node 20 Alpine
│
├── scripts/
│   └── seed_database.py          # Seed de 6 misiones con teoría y hints
│
├── main.py                       # Entrada FastAPI + CORS + init_db()
├── requirements.txt
├── docker-compose.yml
├── Dockerfile                    # Python 3.12-slim
├── .env                          # Variables de entorno (NO commitear)
├── .env.example                  # Plantilla pública
└── ARCHITECTURE.md               # Este archivo
```

---

## 4. Backend — FastAPI

### Endpoints (14 routers bajo `/api/v1`)

#### **POST `/users/login`**
Login o creación automática de usuario por username.
```json
// Request
{ "username": "operador_01" }

// Response
{
  "id": "uuid",
  "username": "operador_01",
  "total_xp": 0,
  "current_level": 1,
  "streak_days": 0
}
```
> ⚠️ v0.1: Sin contraseña real. Fase 2 implementará JWT + bcrypt.

---

#### **GET `/challenges?user_id={uuid}`**
Lista todas las misiones con estado de unlock y completado por usuario.
- Unlock secuencial: cada misión requiere que la anterior esté completada.
- Misión 1 (Protocolo 00) siempre desbloqueada.

#### **GET `/challenges/{id}?user_id={uuid}`**
Obtiene una misión específica con `hints` (array de 3 pistas progresivas), teoría y lore.

---

#### **POST `/execute`**
Ejecuta código Python contra los test cases de la misión.
```json
// Request
{
  "user_id": "uuid",
  "challenge_id": "uuid",
  "source_code": "def fusionar_token(a, b): return a + b\n...",
  "test_inputs": ["NEXO-", "A99"],
  "hints_used": 0,
  "time_spent_ms": 12000
}

// Response
{
  "stdout": "NEXO-A99",
  "stderr": "",
  "execution_time_ms": 148.3,
  "output_matched": true,
  "gamification": {
    "xp_earned": 100,
    "new_total_xp": 100,
    "new_level": 1,
    "level_up": false,
    "first_completion": true
  },
  "error_info": null
}
```

**`error_info`** (cuando hay error Python):
```json
{ "error_type": "SyntaxError", "line": 2, "detail": "invalid syntax" }
```

---

#### **POST `/boss/execute`**
Valida código del jefe final (∞ LOOPER).
- Test: `factorial_iterativo(7)` → `5040`
- Requiere uso de `for`, no recursión ni `while True`
- Recompensa: 1500 XP + medalla `SYSTEM_KILLER`

#### **GET `/boss/config`**
Retorna configuración del combate (tiempo límite, XP, descripción).

---

#### **POST `/hint`**
Pista dinámica generada por Claude (ENIGMA) basada en el código actual.
```json
// Request
{
  "user_id": "uuid",
  "challenge_id": "uuid",
  "source_code": "...",
  "error_output": "NameError: name 'resultado' is not defined"
}
// Response
{ "hint": "[ENIGMA]: El canal de datos espera una variable llamada..." }
```

---

#### **GET `/leaderboard?user_id={uuid}`**
Top 50 global + posición del usuario actual.
```json
{
  "top50": [{ "rank": 1, "username": "...", "total_xp": 5000, "level": 8, "league_tier": "Oro" }],
  "user_rank": 23,
  "total_players": 150
}
```

---

#### **GET `/analytics/user-profile?user_id={uuid}`**
Radar de maestría por concepto Python (strings, variables, funciones, bucles, etc.).

---

#### **POST `/bounty/generate`**
Genera misión dinámica con Claude API según nivel y perfil del usuario.
- Modos DDA: `standard`, `mastery_push`, `stealth_review`

---

#### **Duels (`/duels/*`)**
| Endpoint | Descripción |
|---|---|
| `POST /duels/challenge` | Busca oponente (±200 Elo) y crea duelo |
| `POST /duels/{id}/submit` | Envía solución (challenger o defender) |
| `GET /duels/inbox` | Duelos pendientes como defensor |
| `GET /duels/{id}` | Estado completo del duelo |

---

#### **GET `/activity/stream`**
Server-Sent Events (SSE) — feed de actividad global en tiempo real.
(Boss derrotados, misiones completadas, subidas de nivel)

#### **GET `/health`**
`{ "status": "ok", "app": "...", "version": "0.1.0" }`

---

## 5. Frontend — Next.js

### Rutas (App Router)

| Ruta | Descripción | Guard |
|---|---|---|
| `/` | Login cyberpunk (typewriter boot) | Redirect → /hub si cookie activa |
| `/boot-sequence` | Secuencia intro ENIGMA | Cookie |
| `/hub` | Centro de Mando DAKI | Cookie |
| `/misiones` | HUD Táctico — listado de incursiones | Cookie |
| `/challenge/[id]` | Monaco IDE + ejecución + DAKI Hints | Cookie |
| `/boss` | The Infinite Looper (jefe final) | Cookie |
| `/enigma` | Juego drones isométrico | Cookie |
| `/bounty` | Misiones generadas IA | Cookie |
| `/leaderboard` | Ranking global | Cookie |
| `/arena` | PvP (en desarrollo) | Cookie |
| `/healthcheck` | Status de la API | Público |

> **Guard**: Protección client-side via `useEffect` + cookie `enigma_user`.
> Fase 2: Middleware server-side extendido a todas las rutas protegidas.

---

### Store Zustand (`userStore.ts`)

```typescript
// Persistido en localStorage bajo clave "pq-user"
interface UserState {
  userId: string              // UUID del usuario
  username: string
  level: number
  totalXp: number
  streakDays: number
  previousLevel: number       // Para detectar level-up
  completedChallengeIds: string[]
  badges: string[]            // Ej: ['SYSTEM_KILLER']

  setUser(user: LoginResponse): void
  applyGamificationResult(result: GamificationResult): void
  markChallengeCompleted(id: string): void
  earnBadge(badge: string): void
  clearUser(): void
}
```

---

### Componentes Clave

#### `CodeWorkspace.tsx`
Componente principal del IDE. Incluye:
- Monaco Editor (Python, tema dark, Fira Code)
- Sistema de ejecución con AbortController (timeout 12s cliente / 3s servidor)
- `hintIndex` monotónico + botón "SOLICITAR PISTA DE DAKI"
- Auto-avance de hint cada 2 fallos consecutivos
- DAKI Linter: decoraciones Monaco (línea roja) + mensajes error en español
- Persistencia de borrador en localStorage (debounce 800ms)
- Animaciones: ParticleBurst (XP), ComboEffect, NivelSubidoOverlay

#### `TheInfiniteLooper.tsx`
Componente del jefe final. Fases:
- `intro` → Presentación animada del ∞ LOOPER
- `fighting` → Grid de corrupción 8×6 + Monaco + timer absoluto (45s)
- `victory` → [ SISTEMA CONQUISTADO ] + badge SYSTEM_KILLER + fanfarria audio
- `defeat` → Traceback animado estilo Python

**Timer**: Basado en `endTime` absoluto guardado en localStorage — resiste minimizar pestaña y throttling del navegador.

#### `DakiHint.tsx`
Widget de pistas. Props:
- `visible: boolean` — animado con AnimatePresence
- `hints: string[]` — array dinámico de 3 pistas desde la API
- `hintIndex: number` — índice actual (0-based, nunca retrocede)

#### `HubAudio.tsx`
Reproductor BGM ambiental del Hub:
- Autoplay con `.play().catch()` (respeta políticas del navegador)
- Toggle mute/unmute con persistencia en localStorage (`hub_bgm_muted`)
- Fade-out 18 pasos × 30ms ≈ 540ms antes de navegar a otra página
- Botón fijo en esquina superior derecha

#### `BitacoraModal.tsx`
Códice de Infiltración con archivos narrativos desbloqueables progresivamente.
- Archivos se desbloquean según misiones completadas (`level_order`)
- Ping dot en el Hub si hay archivos sin leer

---

### Proxy Next.js (`next.config.mjs`)

```javascript
// Todos los requests /api/v1/* → backend (evita CORS en desarrollo)
rewrites() → '/api/v1/:path*' → `${NEXT_PUBLIC_API_URL}/api/v1/:path*`
```

---

## 6. Base de Datos

### Schema Completo (8 tablas)

```sql
-- ── users ─────────────────────────────────────────────────────────────────────
CREATE TABLE users (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  username        VARCHAR(50)  UNIQUE NOT NULL,
  email           VARCHAR(255) UNIQUE NOT NULL,
  hashed_password VARCHAR(255) NOT NULL,
  total_xp        INTEGER     DEFAULT 0,
  current_level   INTEGER     DEFAULT 1,
  streak_days     INTEGER     DEFAULT 0,
  league_tier     VARCHAR(30) DEFAULT 'Bronce',
  elo_rating      INTEGER     DEFAULT 1200,
  badges_json     TEXT        DEFAULT '[]',
  created_at      TIMESTAMPTZ DEFAULT now(),
  updated_at      TIMESTAMPTZ DEFAULT now()
);

-- ── challenges ────────────────────────────────────────────────────────────────
CREATE TABLE challenges (
  id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title                 VARCHAR(200) NOT NULL,
  description           TEXT NOT NULL,
  difficulty_tier       INTEGER NOT NULL,        -- 1=BEGINNER, 2=INTERMEDIATE, 3=ADVANCED
  base_xp_reward        INTEGER NOT NULL,
  initial_code          TEXT NOT NULL DEFAULT '',
  expected_output       TEXT NOT NULL,
  test_inputs_json      TEXT DEFAULT '[]',       -- JSON array de strings
  level_order           INTEGER,                 -- Orden curricular (1-N)
  challenge_type        VARCHAR(20) DEFAULT 'python',  -- python | drone | tutorial
  theory_content        TEXT,                    -- Markdown pedagógico
  lore_briefing         TEXT,                    -- Narrativa cyberpunk
  pedagogical_objective TEXT,
  syntax_hint           TEXT,
  hints_json            TEXT DEFAULT '[]'        -- JSON array de 3 pistas progresivas
);

-- ── user_progress ─────────────────────────────────────────────────────────────
CREATE TABLE user_progress (
  id                  UUID PRIMARY KEY,
  user_id             UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  challenge_id        UUID NOT NULL REFERENCES challenges(id) ON DELETE CASCADE,
  completed           BOOLEAN   DEFAULT FALSE,
  attempts            INTEGER   DEFAULT 0,
  completed_at        TIMESTAMPTZ,
  hints_used          INTEGER   DEFAULT 0,
  syntax_errors_total INTEGER   DEFAULT 0,
  UNIQUE(user_id, challenge_id)
);

-- ── user_metrics (telemetría) ──────────────────────────────────────────────────
CREATE TABLE user_metrics (
  id               UUID PRIMARY KEY,
  user_id          UUID NOT NULL,
  challenge_id     UUID NOT NULL,
  attempts         INTEGER     DEFAULT 1,
  time_spent_ms    INTEGER     DEFAULT 0,
  status           VARCHAR(10) DEFAULT 'fail',   -- success | fail
  first_attempt_at TIMESTAMPTZ DEFAULT now(),
  last_attempt_at  TIMESTAMPTZ DEFAULT now(),
  UNIQUE(user_id, challenge_id)
);

-- ── concept_mastery ───────────────────────────────────────────────────────────
CREATE TABLE concept_mastery (
  id                   UUID PRIMARY KEY,
  user_id              UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  concept_name         VARCHAR(100) NOT NULL,
  mastery_score        FLOAT   DEFAULT 0.0,
  needs_reinforcement  BOOLEAN DEFAULT FALSE,
  updated_at           TIMESTAMPTZ DEFAULT now(),
  UNIQUE(user_id, concept_name)
);

-- ── duels (PvP 1v1) ───────────────────────────────────────────────────────────
CREATE TABLE duels (
  id                 UUID PRIMARY KEY,
  challenger_id      UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  defender_id        UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  challenge_id       UUID NOT NULL REFERENCES challenges(id) ON DELETE CASCADE,
  status             VARCHAR(30) DEFAULT 'active',
  -- active | awaiting_defender | completed | expired
  winner_id          UUID REFERENCES users(id) ON DELETE SET NULL,
  challenger_code    TEXT,
  challenger_time_ms FLOAT,
  challenger_correct BOOLEAN,
  defender_code      TEXT,
  defender_time_ms   FLOAT,
  defender_correct   BOOLEAN,
  elo_delta          INTEGER DEFAULT 0,
  created_at         TIMESTAMPTZ DEFAULT now(),
  completed_at       TIMESTAMPTZ
);

-- ── user_bitacora_read ────────────────────────────────────────────────────────
CREATE TABLE user_bitacora_read (
  id         UUID PRIMARY KEY,
  user_id    UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  archivo_id VARCHAR(50) NOT NULL,
  read_at    TIMESTAMPTZ DEFAULT now(),
  UNIQUE(user_id, archivo_id)
);
```

### Migraciones

Ejecutadas en `app/core/database.py → init_db()` usando `ALTER TABLE ... ADD COLUMN IF NOT EXISTS` (idempotentes, sin Alembic). Se corren automáticamente al iniciar el servicio `api`.

---

## 7. Servicios & Lógica de Negocio

### `execution_service.py` — Ejecución de Código
```
execute_python_code(source_code, test_inputs)
  ├── _execute_via_piston()       # Remote sandbox (emkc.org, timeout 10s HTTP / 3s run)
  └── _execute_via_subprocess()   # Fallback local (asyncio.wait_for timeout 3s)

_parse_python_error(stderr) → { error_type, line, detail }
  Detecta: SyntaxError, IndentationError, NameError, TypeError,
           ValueError, AttributeError, IndexError, KeyError,
           ZeroDivisionError, RecursionError, RuntimeError
```

### `gamification_service.py` — XP & Niveles
```
Fórmula nivel: level = floor(0.1 × sqrt(total_xp)) + 1
XP base: BEGINNER=40 · INTERMEDIATE=100 · ADVANCED=200
Bonus eficiencia (+20%): BEGINNER completada en < 50ms
XP se otorga solo en primer éxito (first_completion=True)
```

### `ai_mentor.py` — ENIGMA (Mentor IA)
```
Modelo: claude-haiku-4-5-20251001
Sistema: cyberpunk, máx 2 líneas, nunca revela solución completa
Fallback: Mensaje genérico si ANTHROPIC_API_KEY no configurada
```

### `dda_service.py` — Dynamic Difficulty Adjustment
```
Modos:
  standard      → dificultad normal según nivel
  mastery_push  → enfoca concepto con mastery_score < 40
  stealth_review → repasa conceptos débiles sin avisar
```

### `elo_service.py` — Rating PvP
```
Rating inicial: 1200
Ventana matchmaking: ±200 Elo
Transfer estándar tras duelo completado
```

### `level_generator.py` — Bounties Dinámicos
```
Llama Claude API para generar misiones Python completas:
  - Enunciado narrativo
  - Código inicial con placeholders
  - Expected output verificable
```

---

## 8. Infraestructura & Docker

### docker-compose.yml (3 servicios)

```
db  (postgres:15-alpine)
 └─ puerto 5432 · volumen pgdata (persistente)
 └─ healthcheck: pg_isready (10 retries × 5s)

api  (Dockerfile — Python 3.12-slim)
 └─ puerto 8000 · hot-reload --reload (dev)
 └─ depends_on: db (condition: service_healthy)

web  (frontend/Dockerfile — Node 20-alpine)
 └─ puerto 3000 · npm run dev
 └─ depends_on: api
```

### Comandos de Desarrollo

```bash
# Levantar todos los servicios
docker compose up --build

# Re-seed base de datos
docker compose exec api python -m scripts.seed_database

# Logs en vivo
docker compose logs -f api
docker compose logs -f web

# Shell en el contenedor API
docker compose exec api bash

# Limpiar todo (incluyendo BD)
docker compose down -v

# Ver tablas PostgreSQL
docker compose exec db psql -U quest_user -d pythonquest -c "\dt"
```

---

## 9. Variables de Entorno

### `.env` (backend — NO commitear a Git)

| Variable | Descripción | Producción |
|---|---|---|
| `POSTGRES_USER` | Usuario PostgreSQL | Valor seguro único |
| `POSTGRES_PASSWORD` | Contraseña PostgreSQL | `openssl rand -base64 32` |
| `POSTGRES_DB` | Nombre de la base | OK mantener |
| `DATABASE_URL` | URL conexión async | Añadir `?ssl=require` |
| `DEBUG` | Modo debug | **`False`** |
| `SECRET_KEY` | Firma JWT | `openssl rand -base64 32` |
| `ALLOWED_ORIGINS` | CORS orígenes permitidos | `["https://tu-dominio.com"]` |
| `ANTHROPIC_API_KEY` | Claude API key | Variable segura del host |
| `NEXT_PUBLIC_API_URL` | URL API pública | `https://api.tu-dominio.com` |

### `.env.local` (frontend)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 10. Flujo Narrativo

```
[/]  Login
  └─ Escribe username → POST /users/login → cookie "enigma_user"
  └─ Redirect → /boot-sequence (1ª vez) o /hub (visitas siguientes)

[/boot-sequence]  Intro ENIGMA
  └─ Secuencia cinematográfica de bienvenida al Nexo
  └─ Redirect → /hub

[/hub]  Centro de Mando
  └─ DAKI presenta el estado del Nexo
  └─ Registro de Conquistas (medallas ganadas)
  └─ BGM ambiental (hub-ambient.mp3)
  └─ Navegación → /misiones / /bounty / /leaderboard

[/misiones]  HUD Táctico
  └─ Grid de incursiones con unlock secuencial
  └─ Click → HackingTransition (1.5s) → /challenge/[id]
  └─ Acceso Boss cuando unlock

[/challenge/[id]]  Monaco IDE
  └─ MissionBriefing → CodeWorkspace
  └─ Ejecutar → POST /execute → XP + feedback
  └─ Pistas DAKI (3 niveles, monotónicas, nunca retroceden)
  └─ Éxito → VictoryModal → siguiente misión

[/boss]  The Infinite Looper
  └─ intro → fighting (45s timer) → victory / defeat
  └─ Victoria → SYSTEM_KILLER badge + 1500 XP + victory.mp3

[/hub]  Volver al Centro de Mando
  └─ Registro de Conquistas muestra medalla ganada
```

---

## 11. Sistema de Gamificación

### Fórmula de Nivel

```
level = floor(0.1 × sqrt(total_xp)) + 1
```

| XP | Nivel |
|---|---|
| 0 | 1 |
| 100 | 2 |
| 400 | 3 |
| 900 | 4 |
| 1600 | 5 |
| 2500 | 6 |

### XP por Misión

| Dificultad | XP Base | Con bonus eficiencia |
|---|---|---|
| BEGINNER | 40 | 48 |
| INTERMEDIATE | 100 | 120 |
| ADVANCED | 200 | 240 |

> XP se otorga **solo en la primera** finalización exitosa.

### Medallas (Badges)

| Badge | Condición | XP |
|---|---|---|
| `SYSTEM_KILLER` | Derrotar al ∞ LOOPER | 1500 |

Guardadas en `userStore.badges[]` (Zustand persist) y `users.badges_json` (BD).

### Ligas Competitivas
`Bronce → Plata → Oro → Platino → Diamante`
Calculadas por `league_service.py` (máx 1 actualización/hora).

---

## 12. Ejecución de Código (Sandbox)

### Flujo

```
POST /execute
  ├─ 1. Piston API (emkc.org)         timeout HTTP: 10s / ejecución: 3s
  ├─ 2. Fallback subprocess local      asyncio.wait_for timeout: 3s → proc.kill()
  └─ 3. _normalize_output(stdout)
         ├─ CRLF → LF
         ├─ strip() por línea
         └─ global strip()
       Comparar vs expected_output
```

### DAKI Linter — Mensajes de Error en Español

| Error Python | Mensaje DAKI |
|---|---|
| `SyntaxError` | "Error de sintaxis en Línea {line}. Revisa los dos puntos, comillas o paréntesis." |
| `NameError` | "Variable no encontrada en Línea {line}. ¿La definiste antes de usarla?" |
| `IndentationError` | "Indentación incorrecta en Línea {line}. Usa 4 espacios, no tabs." |
| `TypeError` | "Tipo de datos incorrecto en Línea {line}." |
| `ValueError` | "Valor inválido en Línea {line}. ¿Convirtiendo correctamente con int() o float()?" |
| `ZeroDivisionError` | "División por cero en Línea {line}. El sistema no acepta el vacío absoluto." |
| `RecursionError` | "Recursión infinita detectada. ¿Falta un caso base?" |

---

## 13. Sistema de IA (ENIGMA & Bounties)

### ENIGMA — Mentor IA

**Modelo**: `claude-haiku-4-5-20251001`

**Sistema de Pistas Progresivas** (3 niveles, por misión en BD):
1. **Pista 1** — Conceptual: qué operador/concepto usar
2. **Pista 2** — Sintáctica: cómo se escribe en Python
3. **Pista 3** — Directiva: casi la solución, sin revelarla completa

Almacenadas en `challenges.hints_json` (JSON array de 3 strings).

**Pistas Dinámicas** (via `/hint` + Claude):
- Contextual al código actual del usuario
- Máx 2 líneas, estilo cyberpunk, nunca revela solución

### Bounties Dinámicos

Genera misiones Python completas (enunciado + código inicial + expected output) basadas en nivel del usuario, concepto objetivo y modo DDA.

---

## 14. Audio & Assets

### Archivos de Sonido

| Archivo | Tamaño | Uso | Componente |
|---|---|---|---|
| `boot-sequence.mp3` | 691 KB | Secuencia intro ENIGMA | boot-sequence/page.tsx |
| `data-stream.mp3` | 42 KB | Efecto sonido datos | — |
| `hub-ambient.mp3` | 3.2 MB | BGM ambiental Hub (loop) | HubAudio.tsx |
| `victory.mp3` | 2.4 MB | Fanfarria victoria Boss | TheInfiniteLooper.tsx |

### Control de Audio (HubAudio.tsx)

- **Volumen ambiental**: 0.28 · **Fanfarria victoria**: 0.72
- **Persistencia mute**: `localStorage['hub_bgm_muted']`
- **Fade-out navegación**: 18 pasos × 30ms ≈ 540ms → luego `router.push()`

### Fondos por Nivel

```
public/assets/backgrounds/
├── map1.png  ← Nivel 1 (Protocolo 00 / Fusión de Nodos)
├── map2.png  ← Nivel 2
├── map3.png  ← Nivel 3
├── map4.png  ← Nivel 4
└── map5.png  ← Nivel 5
```

---

## 15. Guía de Desarrollo Local

### Requisitos

- Docker Desktop ≥ 4.x
- Git

### Setup Inicial

```bash
# 1. Clonar
git clone https://github.com/moudandpleidedtech/moudandpleid.git
cd moudandpleid/temporal-master

# 2. Variables de entorno
cp .env.example .env
# Editar .env: añadir ANTHROPIC_API_KEY y ajustar si es necesario

# 3. Levantar servicios
docker compose up --build

# 4. Seed de la BD
docker compose exec api python -m scripts.seed_database

# 5. Acceder
# Frontend:  http://localhost:3000
# API:       http://localhost:8000
# Swagger:   http://localhost:8000/docs
```

### Comandos de Uso Frecuente

```bash
# Re-seed (tras cambios en seed_database.py)
docker compose exec api python -m scripts.seed_database

# Logs combinados
docker compose logs -f

# Reiniciar solo frontend
docker compose restart web

# Limpiar BD completamente
docker compose down -v && docker compose up --build
docker compose exec api python -m scripts.seed_database
```

---

## 16. Checklist de Producción

### Crítico (antes de cualquier deploy público)

- [ ] Revocar y regenerar `ANTHROPIC_API_KEY`
- [ ] `SECRET_KEY` → `openssl rand -base64 32`
- [ ] `POSTGRES_PASSWORD` → valor seguro único
- [ ] `DEBUG=False`
- [ ] `ALLOWED_ORIGINS` → dominio real en producción
- [ ] `NEXT_PUBLIC_API_URL` → URL HTTPS de la API

### Dockerfiles de Producción

**Backend** — quitar `--reload`:
```dockerfile
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
```

**Frontend** — build de producción:
```dockerfile
RUN npm run build
CMD ["npm", "start"]
```

### Seguridad (Fase 2)

- [ ] Rate limiting en `/execute`, `/hint`, `/users/login`
- [ ] `max_length` en `source_code` (prevenir DoS)
- [ ] Middleware server-side extendido a todas las rutas protegidas
- [ ] HTTPS/TLS en todos los endpoints
- [ ] `DATABASE_URL` con `?ssl=require`
- [ ] Autenticación JWT real + contraseña bcrypt
- [ ] httpOnly cookies para sesión

### Performance

- [ ] Índice en `users.elo_rating` (matchmaking PvP)
- [ ] CDN para assets (backgrounds, audio)
- [ ] Health check Piston API antes de aceptar requests de ejecución

---

*Python Quest v0.1.0 · Documentación generada 2026-03-17*
