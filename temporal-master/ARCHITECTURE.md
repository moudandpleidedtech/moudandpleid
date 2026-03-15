# MOUD AND PLEID — ARCHITECTURE v1.0
> Protocolo DAKI · Documentación Oficial · 2026-03-15

---

## 1. FLUJO DE USUARIO (HAPPY PATH)

```
[/]  Login
  │  POST /api/v1/users/login
  │  → Cookie: enigma_user  |  localStorage: pq-user (Zustand persist)
  │
  ├─ Primera vez ──→ [/boot-sequence]  Secuencia intro ENIGMA
  │                       └─ localStorage: boot_seen = 1
  │
  └─ Retorno ──────→ [/hub]  Centro de Mando · DAKI
                        │
                        ├─ [INICIAR AUDITORÍA] ───────────→ [/misiones]  HUD Táctico
                        │                                       │
                        │                                       ├─ Seleccionar incursión
                        │                                       ├─ MissionBriefingModal  (si lore_briefing)
                        │                                       ├─ HackingTransition  1500ms
                        │                                       │
                        │                                       ├─ [/challenge/:id]  Monaco IDE
                        │                                       │     POST /api/v1/compiler
                        │                                       │     POST /api/v1/gamification
                        │                                       │     → +XP · Level check
                        │                                       │
                        │                                       └─ [/enigma]  Juego de drones isométrico
                        │                                             (challenge_type === 'drone')
                        │
                        ├─ [BASE DE DATOS TÁCTICA] ──────→ BitacoraModal  Códice de Infiltración
                        │                                       │  completedOrders prop → archivos desbloqueados
                        │                                       └─ read tracking → user_bitacora_read (DB)
                        │
                        ├─ [BOUNTIES IA] ────────────────→ [/bounty]   Misiones IA dinámicas
                        │                                       POST /api/v1/bounty/generate (Anthropic SDK)
                        │
                        ├─ [LEADERBOARD] ────────────────→ [/leaderboard]  Ranking global
                        │
                        └─ [THE INFINITE LOOPER] ────────→ [/boss]  Jefe Final
```

---

## 2. ESTRUCTURA DEL PROYECTO

```
temporal-master/
│
├── app/                            # Backend · FastAPI (Python 3.12)
│   ├── api/v1/endpoints/           # 15 endpoints REST
│   │   ├── users.py                # Auth · registro · login
│   │   ├── challenges.py           # GET /challenges?user_id=  (con unlock logic)
│   │   ├── compiler.py             # POST /compiler  (ejecución Python sandboxed)
│   │   ├── gamification.py         # POST /gamification  (+XP · level up)
│   │   ├── bounty.py               # POST /bounty/generate  (Anthropic SDK)
│   │   ├── leaderboard.py          # GET /leaderboard
│   │   ├── boss.py                 # Boss fight endpoints
│   │   ├── hint.py                 # GET /hint  (AI Mentor)
│   │   └── ...                     # analytics, duels, activity, simulate, health
│   │
│   ├── models/                     # SQLAlchemy ORM (PostgreSQL async)
│   │   ├── user.py                 # users  — auth + XP + level + ELO
│   │   ├── challenge.py            # challenges  — contenido + lore + tipo
│   │   ├── user_progress.py        # user_progress  — completed · attempts · telemetry
│   │   ├── concept_mastery.py      # concept_mastery  — mastery por concepto Python
│   │   ├── duel.py                 # duels  — PvP 1v1
│   │   └── bitacora_read.py        # user_bitacora_read  — tracking Bitácora DAKI ✨NEW
│   │
│   ├── services/                   # Lógica de negocio
│   │   ├── gamification_service.py # XP · level · streak
│   │   ├── dda_service.py          # Dynamic Difficulty Adjustment
│   │   ├── level_generator.py      # Generación de bounties con Anthropic
│   │   ├── ai_mentor.py            # Hints inteligentes
│   │   ├── execution_service.py    # Sandbox de ejecución Python
│   │   ├── elo_service.py          # Rating PvP
│   │   └── ...
│   │
│   └── core/
│       ├── database.py             # Engine async + init_db() con migrations idempotentes
│       └── config.py               # Settings (env vars)
│
├── frontend/                       # Frontend · Next.js 14 App Router
│   └── src/
│       ├── app/                    # Rutas
│       │   ├── page.tsx            # [/]           Login
│       │   ├── boot-sequence/      # [/boot-sequence]  Intro ENIGMA
│       │   ├── hub/                # [/hub]         ✨ Centro de Mando DAKI
│       │   ├── misiones/           # [/misiones]    ✨ HUD Táctico de Incursiones
│       │   ├── challenge/[id]/     # [/challenge/:id]  Monaco IDE
│       │   ├── enigma/             # [/enigma]      Juego de drones isométrico
│       │   ├── boss/               # [/boss]        The Infinite Looper
│       │   ├── bounty/             # [/bounty]      Misiones generadas por IA
│       │   ├── leaderboard/        # [/leaderboard] Ranking global
│       │   ├── codice/             # [/codice]      (en desarrollo)
│       │   └── arena/              # [/arena]       (en desarrollo)
│       │
│       ├── components/
│       │   ├── Game/
│       │   │   ├── BitacoraModal.tsx       # ✨ Códice de Infiltración progresivo
│       │   │   ├── HackingTransition.tsx   # ✨ Pantalla de infiltración entre rutas
│       │   │   ├── MissionBriefingModal.tsx # Lore pre-misión
│       │   │   ├── ManualModal.tsx         # Manual táctico Python (6 protocolos)
│       │   │   ├── GlitchTransition.tsx    # Intro tutorial ENIGMA
│       │   │   ├── MissionBriefing.tsx     # Componente de briefing
│       │   │   ├── GridCanvas.tsx          # Canvas isométrico del juego drones
│       │   │   ├── ByteDrone.tsx           # Sprite del dron
│       │   │   └── EnemyCell.tsx           # Células enemigas
│       │   ├── IDE/
│       │   │   └── CodeWorkspace.tsx       # Monaco Editor + ejecución + feedback
│       │   ├── Boss/
│       │   │   └── TheInfiniteLooper.tsx   # Componente jefe final
│       │   └── UI/
│       │       ├── Toast.tsx               # Notificaciones
│       │       ├── ComboEffect.tsx         # Efecto combo visual
│       │       ├── ParticleBurst.tsx       # Partículas de XP
│       │       ├── LiveActivityFeed.tsx    # Feed en tiempo real
│       │       └── TopNav.tsx              # Navegación superior
│       │
│       ├── store/
│       │   └── userStore.ts        # Zustand + persist → localStorage 'pq-user'
│       │                           # State: userId · username · level · totalXp · streakDays
│       │
│       └── middleware.ts           # Cookie 'enigma_user' → redirect /hub si autenticado
│
├── scripts/
│   └── seed_database.py            # Seed de misiones iniciales
│
├── docker-compose.yml              # API + Frontend + PostgreSQL
└── ARCHITECTURE.md                 # Este archivo
```

---

## 3. MANUAL DE LORE — DAKI Y EL UNIVERSO M&P

### ¿Quién es DAKI?

**DAKI** (Dynamic Artificial Knowledge Interface) es la IA simbionte del jugador.
No es un asistente — es un co-piloto táctico que vive en el Centro de Mando (`/hub`).

DAKI se manifiesta como un núcleo de energía verde neón con anillos orbitantes.
Habla en frases cortas, técnicas y urgentes. Cada sesión elige aleatoriamente
una frase distinta que mezcla lore narrativo con un concepto Python concreto.

> *"He interceptado transmisiones de los Syntax Swarms. Son vulnerables a los ataques de área (for loops)."*

### Auditoría vs. Misión — distinción de concepto

| Término | Contexto UI | Significado real |
|---|---|---|
| **AUDITORÍA** | Botón en Hub | La sesión completa de misiones del día |
| **INCURSIÓN** | Lista en `/misiones` | Una misión individual de código |
| **INFILTRACIÓN** | HackingTransition | El momento de entrada al editor de código |
| **BOTÍN** | XP ganado | Conocimiento + puntos de experiencia obtenidos |
| **ARCHIVO** | Bitácora DAKI | Documento pedagógico desbloqueado tras completar una incursión |

### El Códice de Infiltración (Bitácora)

Cada incursión completada desbloquea un **Archivo** en el Códice.
Los Archivos contienen el reporte post-misión de DAKI: qué ocurrió tácticamente
y por qué el concepto Python utilizado fue la clave del éxito.

Los Archivos no son recompensas opcionales — son la capa pedagógica
que conecta la narrativa de hackeo con el aprendizaje real.

### The Infinite Looper — El Jefe Final

El antagonista final del sistema. Un proceso recursivo sin condición de salida
que ha corrompido los núcleos del Área 51. Solo puede ser derrotado
demostrando maestría en control de flujo con Python.

---

## 4. SISTEMA DE AUTENTICACIÓN Y PERSISTENCIA

```
Login exitoso
    │
    ├─ Backend:  cookie HTTP 'enigma_user' (httpOnly recomendado)
    │
    └─ Frontend: Zustand userStore.ts
                 persist({ name: 'pq-user' }) → localStorage
                 Fields: userId · username · level · totalXp · streakDays

middleware.ts
    └─ matcher: ['/']
    └─ Si cookie 'enigma_user' existe → redirect /hub
    ⚠️  Las demás rutas se protegen client-side via useEffect(userId check)
    TODO Fase 2: extender matcher a ['/hub', '/misiones', '/challenge/:path*']
```

---

## 5. MIGRATION LOG

| Nombre | Tabla afectada | Descripción |
|---|---|---|
| initial | users, challenges, user_progress | Tablas base |
| add_test_inputs | challenges | test_inputs_json |
| add_curriculum_fields | challenges | level_order, phase, concepts_taught_json, grid_map_json, challenge_type |
| add_telemetry | user_progress | hints_used, syntax_errors_total |
| add_theory_content | challenges | theory_content |
| add_league_tier | users | league_tier |
| add_elo_rating | users | elo_rating |
| add_mission_briefing | challenges | lore_briefing, pedagogical_objective, syntax_hint |
| **add_daki_bitacora_tracking** | **user_bitacora_read** | **Nueva tabla: tracking de archivos leídos** ✨ |

Todas las migrations son idempotentes (`ADD COLUMN IF NOT EXISTS` / `CREATE TABLE IF NOT EXISTS`)
y se ejecutan automáticamente en `init_db()` al iniciar el servidor.

---

## 6. VARIABLES DE ENTORNO REQUERIDAS

```bash
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/moudandpleid
ANTHROPIC_API_KEY=sk-ant-...          # Bounty generation (requiere créditos)
NEXT_PUBLIC_API_URL=http://localhost:8000
DEBUG=false
```

---

*DAKI Protocol · Moud and Pleid · v1.0 · 2026-03-15*
