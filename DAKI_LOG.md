# DAKI_LOG — Contexto Completo del Proyecto Nexo EdTech

> Archivo de contexto para sesiones futuras.
> Ultima actualizacion: 2026-04-07 (sesion 5 — Protocolo Guerrero: 11 features pedagogicas)

---

## 1. Vision del Producto

**Nexo** — Plataforma gamificada para formar **Operadores Python** desde cero.
- Identidad: Python-only. No JavaScript, no multi-lenguaje.
- Usuario objetivo: completo principiante.
- Dinamicas: misiones -> feedback inmediato -> reflexion metacognitiva -> XP + progresion.
- DAKI = IA mentora interna (Claude Haiku 4.5, Tool Use).

---

## 2. Stack Tecnico

| Capa | Tecnologia |
|------|-----------|
| Frontend | Next.js 14 App Router, TypeScript, Tailwind CSS, Framer Motion, Zustand |
| Editor | Monaco Editor (tema oscuro, Python syntax) |
| Backend | FastAPI + async SQLAlchemy + init_db() self-migrating (no Alembic) |
| DB | PostgreSQL Neon (cloud) |
| IA | Anthropic Claude Haiku 4.5 (Tool Use) |
| Ejecucion codigo | Piston API (timeout 6s) + fallback subprocess Python (timeout 4s) |
| Deploy frontend | Vercel |
| Deploy backend | Render (Docker) |
| Auth | JWT (jose) + Google OAuth 2.0 (redirect-based) |

---

## 3. Rutas y Paginas

/                   -> Redirect a /onboarding si no completado, sino /hub
/onboarding         -> Intro (modo estandar o principiante absoluto)
/hub                -> Centro de operaciones: skill tree, widgets, misiones del dia
/misiones           -> Lista de misiones filtradas por tier
/codex/[slug]       -> Vista de challenge por slug
/auth/google        -> Bridge page JWT (decodifica token URL -> localStorage + cookie)
/login              -> Formulario login + boton Google OAuth
/register           -> Formulario registro + boton Google OAuth

---

## 4. Backend — Endpoints Principales

- POST /api/v1/users/
- POST /api/v1/auth/google          -> inicia flujo OAuth (redirect a Google)
- GET  /api/v1/auth/google/callback -> recibe code, genera JWT, redirige a /auth/google?token=JWT
- GET  /api/v1/users/{id}
- GET  /api/v1/challenges/
- GET  /api/v1/challenges/{id}
- POST /api/v1/challenges/{id}/submit  ->  { passed, output, xp_earned }
- POST /api/v1/daki/hint               ->  { hint_text, questions[] }  (Modo Socrático)
- POST /api/v1/daki/debrief
- POST /api/v1/daki/intervention
- POST /api/v1/daki/session-summary    ->  { summary }  (Fin de Turno)
- POST /api/v1/session/open            ->  { session_id, opening_message, weak_concept }
- GET  /api/v1/daily-anomaly           (sin auth, determinista SHA-256)
- GET  /api/v1/achievements/{user_id}
- GET  /api/v1/skill-tree/{user_id}

---

## 5. Modelos de Base de Datos

User:          id, username, email, level, xp, created_at, last_seen
Challenge:     id, slug, title, description, starter_code, solution,
               hints (JSON), concepts_taught_json (JSON), difficulty_tier (1/2/3),
               xp_reward, theory_content (nullable), lore_briefing (nullable)
UserChallenge: user_id, challenge_id, completed, attempts, best_time_ms, completed_at
Achievement:   id, user_id, name, description, icon, xp_bonus, rarity, unlocked_at
DakiLog:       id, user_id, challenge_id, error_type, hint_used, time_ms, created_at

Patron init_db(): no usa Alembic. Cada startup corre ALTER TABLE IF NOT EXISTS +
CREATE TABLE IF NOT EXISTS. Idempotente.

---

## 6. Google OAuth — Flujo Cross-Domain

Problema: backend (daki-api.onrender.com) no puede setear cookies para frontend (dakiedtech.com).

Solucion implementada:
1. Backend genera JWT y redirige a: /auth/google?token=JWT&new=0|1
2. /auth/google/page.tsx (bridge page) decodifica JWT del URL
3. Popula localStorage + Zustand + cookie enigma_user
4. Navega a /hub

Archivo bridge: temporal-master/frontend/src/app/auth/google/page.tsx
- Usa <Suspense> alrededor del componente que llama useSearchParams() (req. Next.js 14)
- JWT decode: JSON.parse(atob(payloadB64.replace(/-/g,'+').replace(/_/g,'/')))

---

## 7. CodeWorkspace — Estado y Logica Central

Archivo: temporal-master/frontend/src/components/IDE/CodeWorkspace.tsx

### States relevantes

```
viewMode: 'briefing' | 'intel' | 'editor'   // intel = DakiIntelCard
secretReveal: boolean                         // SecretMissionRevealModal
activeMilestone: MilestoneId | null           // MilestoneModal
sessionAttempts: number                       // para useMilestones
showDebrief, debriefAttempts
showRadar, showFlashRecall
hintFreeStreak
```

### Flujo de carga de challenge

1. Fetch challenge data
2. Si no completado y no tutorial:
   - theory_content presente -> viewMode = 'briefing' (MisionBriefing)
   - sin theory_content + concepts_taught_json -> viewMode = 'intel' (DakiIntelCard)
   - ya completado -> viewMode = 'editor'
3. Layout se oculta si viewMode !== 'editor'

### Flujo de victoria

1. handleRun() llama /challenges/{id}/submit
2. Si passed === true:
   - Victory audio vol 0.3
   - pushMission() -> sessionStorage (para Fin de Turno y DakiMemoriaCard)
   - checkMilestones() -> useMilestones hook (milestones narrativos)
   - [700ms] showDebrief=true
   - checkSecretMissions()
   - [1.2s] fireMicro()
3. Al cerrar debrief -> handleNextChallenge()

### Flujo de pista (DAKI hint — Modo Socrático)

1. requestHint() extrae errorType con regex
2. POST /api/v1/daki/hint  { fail_count, ... }
3. Si fail_count <= 1: respuesta incluye questions[] (2 preguntas socraticas)
   -> se insertan en consola con header "// MODO SOCRÁTICO"
4. Luego aparece el hint normal
5. setHintFreeStreak(0)

---

## 8. Sistema DAKI (IA Mentor)

Archivo: temporal-master/app/services/ai_mentor.py

get_hint(user_id, challenge, error_output, error_type, hint_index, ...)
- Claude Haiku 4.5 con Tool Use
- Herramientas: get_concept_explanation, get_next_hint, escalate_to_human
- Retorna: { hint_text, tool_used, escalated }

### Calibracion debrief (daki.py)

```python
def _get_debrief_tier(operator_level, difficulty_tier):
    if operator_level <= 5 or difficulty_tier <= 1: return "beginner"
    elif operator_level <= 15 or difficulty_tier <= 2: return "intermediate"
    else: return "advanced"

_DEBRIEF_FALLBACKS = {
    "beginner":     "Con tus palabras, que hace el codigo que escribiste?",
    "intermediate": "Que cambiarias si el tipo de datos fuera diferente?",
    "advanced":     "Como aplicarias este patron con multiples modulos?",
}
```

### Endpoint session-summary (daki.py)

POST /api/v1/daki/session-summary
- Recibe: { missions[], operator_level, user_id }
- Genera informe 3 lineas en voz DAKI (directiva final incluida)
- Usa _SESSION_SUMMARY_DIRECTIVE como system prompt

---

## 9. Gamification — Las 10 Features Originales

### F1 — Flash Recall Modal (Spaced Repetition)
Archivo: src/components/Game/FlashRecallModal.tsx
- 15 preguntas Python, trigger cada 3 misiones
- Weighted pickQuestion(): errores pasados +2, concepto match +3, dominadas -1
- Historia guardada en localStorage 'daki-flash-history'

### F2 — RadarMaestriaModal + SINAPSIS Button
Archivo: src/components/Hub/RadarMaestriaModal.tsx
- Radar SVG de maestria por concepto, boton SINAPSIS en HUD

### F3 — Daily Anomaly Card (Hub)
Archivos: src/components/Hub/DailyAnomalyCard.tsx
          app/api/v1/endpoints/daily_anomaly.py
- GET /api/v1/daily-anomaly — SHA-256 determinista, sin DB
- localStorage 'daki-anomaly-today' y 'daki-anomaly-done' para tracking
- Estado completada: borde verde, badge "COMPLETADA", boton "MARCAR COMPLETADA"

### F4 — MisionDebriefModal (Metacognicion post-mision)
Archivo: src/components/Game/MisionDebriefModal.tsx
- 700ms despues de victoria
- Pregunta calibrada por operatorLevel y difficultyTier

### F5 — Hint-Free Streak + Multiplier Badge
- hintFreeStreak state en CodeWorkspace
- Badge HUD cuando hintFreeStreak >= 2

### F6 — MicroBroadcast (30 Python Tips)
Archivos: src/hooks/useMicroBroadcast.ts, src/components/UI/MicroBroadcast.tsx
- 30 tips curados, cooldown 90s localStorage 'daki_microbroadcast_last'

### F7 — Error Pattern Detection
- errorHistoryRef, mismo error x3 -> AchievementToast epic

### F8 — Secret Missions (Variable Reward)
Archivo: src/hooks/useSecretMissions.ts
- 5 misiones: VELOCISTA, PURO, PERSISTENTE, MADRUGADOR, PERFECCIONISTA
- SecretMissionRevealModal: gold theme, pulsing star, 6s auto-dismiss

### F9 — Centralizacion TIER_LABEL/TIER_COLOR
Archivo: src/lib/tierLabels.ts

### F10 — Error Type para DAKI LLM Prompt
- Frontend extrae error_type con regex, enviado en POST hint

---

## 10. 5 Features UX — DAKI Presente en Todo el Journey

### UX1 — Fin de Turno (FinDeTurnoModal)
Archivo: src/components/Game/FinDeTurnoModal.tsx
- Trigger: Hub, boton "VER INFORME DE TURNO" (aparece con sessionLog.length >= 2)
- Stats strip: misiones, tiempo total, usos ENIGMA, promedio intentos
- Lista de misiones de la sesion
- Llama POST /api/v1/daki/session-summary -> resumen personalizado DAKI
- Al cerrar: clearSessionLog() + setSessionLog([])

### UX2 — Milestones Narrativos (MilestoneModal + useMilestones)
Archivos: src/components/Game/MilestoneModal.tsx
          src/hooks/useMilestones.ts
- 10 milestones: primera_victoria, primera_sin_enigma, cinco_misiones, diez_misiones,
  velocista_primera (<60s), primer_tier2, primer_tier3, racha_3_sin_enigma,
  primer_intento, veinte_misiones
- Persistidos en localStorage 'daki-milestones'
- Slide up desde bottom (z-280), 7s auto-dismiss, staggered 800+400ms por unlock

### UX3 — Modo Socrático (hint.py + CodeWorkspace)
- Backend: si fail_count <= 1, genera 2 preguntas socraticas via Haiku
- Frontend: questions[] formateadas en consola con "// MODO SOCRÁTICO" header
- Sin cambios de UI — contenidas en flujo de consola existente

### UX4 — Hub con Memoria de Sesion
Archivos: src/components/Hub/DakiMemoriaCard.tsx
          src/hooks/useSessionLog.ts
- useSessionLog: pushMission() | getSessionLog() | clearSessionLog() en sessionStorage
- DakiMemoriaCard: template-based (sin LLM), analiza hints usados, promedio intentos,
  tiempo total — visible si hay 1+ mision en sesion
- Se carga via useEffect en hub/page.tsx

### UX5 — Theory Universal (DakiIntelCard + conceptGlossary)
Archivos: src/components/IDE/DakiIntelCard.tsx
          src/lib/conceptGlossary.ts
- 14 conceptos: variable, for_loop, while_loop, function, string, list, dict,
  boolean, if_else, number, input_fn, print_fn, range_fn, return_stmt
- Cada entrada: title, theory (2-3 lineas voz DAKI), example (Python), realWorld
- Si challenge sin theory_content + tiene concepts -> viewMode = 'intel'
- "VER APLICACION REAL" toggle, "INICIAR INCURSION" boton
- Respuesta instantanea (sin LLM)

---

## 11. Hub — Orden de Widgets (Panel Derecho)

1. Badge de Rango (XP, nivel, streak, liga)
2. CTA Principal "CONTINUAR MISION"
3. MODO ARENA (PvP)
4. PythonCoreStatus (4 nodos, barra progreso)
5. DailyAnomalyCard (F3)
6. DakiMemoriaCard (UX4 — solo si hay sesion activa)
7. "VER INFORME DE TURNO" (UX1 — solo si sessionLog.length >= 2)
8. Separador
9. Accesos Rapidos (grid 3x2: Bitacora, Contratos, Ligas, Radar, Fallas, Intel)
10. DistincionesPanel
11. Pase Alpha / Stripe (si no tiene acceso)
12. Registro de Conquistas (badges)
13. Estado del Sistema

---

## 12. Onboarding

Archivo: temporal-master/frontend/src/app/onboarding/page.tsx

Modos: choose | standard | beginner

### Beginner Steps (11 pasos, lenguaje cotidiano, analogias fisicas)
Finalizacion: localStorage.setItem("onboarding_done", "true") -> router.push("/hub")

Hub Onboarding Modal (primera visita al hub):
- 3 pasos: Bienvenida, Python Core explicacion, Primera mision
- Trigger: !localStorage.getItem('nexo_onboarded')
- Guarda 'nexo_onboarded' en localStorage al completar

---

## 13. Audio

- Archivo: /public/sounds/victory.mp3
- Volumen: audioVictoryRef.current.volume = 0.3

---

## 14. localStorage / sessionStorage Keys

| Key | Storage | Descripcion |
|-----|---------|-------------|
| onboarding_done | local | "true" si completo onboarding |
| nexo_onboarded | local | "1" si vio modal onboarding del hub |
| pq-missions-completed | local | counter misiones (string number) |
| pq-behavior-log | local | JSON BehaviorLog para secret missions |
| daki_microbroadcast_last | local | timestamp cooldown microbroadcast |
| daki-flash-history | local | historial respuestas Flash Recall |
| daki-milestones | local | milestones desbloqueados (Set serializado) |
| daki-anomaly-today | local | slug anomalia diaria actual |
| daki-anomaly-done | local | fecha ISO en que se completo la anomalia |
| daki-session-current | session | SessionMission[] del turno activo |
| daki_greeted | session | "1" si DAKI ya saludo en este tab |
| daki_last_hub_visit | local | timestamp ultima visita hub (reenganche) |

---

## 15. AchievementToast

Archivo: src/components/UI/AchievementToast.tsx
Raridades: common (verde) | rare (azul) | epic (morado) | legendary (dorado)

---

## 16. Flujo Completo de una Mision

1. IDE carga challenge
2. Si sin theory y con concepts -> DakiIntelCard (UX5) -> click -> editor
3. Si con theory -> MisionBriefing -> click -> editor
4. challengeStartMs.current = Date.now()
5. [30s] MicroBroadcast tip Python (F6)
6. Usuario escribe -> Ctrl+Enter o RUN
7. POST /challenges/{id}/submit
   passed=false:
     errorHistoryRef.push(error_type)
     failStreak++
     Si failStreak===4 -> DAKI intervention
     Si mismo error x3 -> AchievementToast epic (F7)
   passed=true:
     Victory audio vol 0.3
     XP + animaciones
     pushMission() -> sessionStorage (UX4)
     checkMilestones() -> MilestoneModal si unlock (UX2)
     [700ms] showDebrief=true (F4)
     checkSecretMissions() (F8) -> SecretMissionRevealModal si unlock
     [1.2s] fireMicro() (F6)
8. Debrief Modal -> DAKI pregunta calibrada
9. Responde/salta -> handleNextChallenge()
10. missions-completed++
    Si missions % 3 === 0 -> FlashRecallModal (F1)
    Si no -> siguiente challenge

Al pedir pista (ENIGMA):
1. requestHint() extrae errorType
2. POST /daki/hint
3. Si primer fallo: MODO SOCRÁTICO en consola (UX3)
4. Luego hint normal
5. hintFreeStreak = 0

---

## 17. Decisiones Tecnicas Clave

1. Sin Alembic: init_db() self-migrating
2. Daily Anomaly sin DB: SHA-256 determinista
3. Flash Recall cada 3 misiones
4. Error type via regex en frontend
5. DAKI calibrado por AMBOS operator_level Y difficulty_tier
6. Beginner onboarding: analogias fisicas latinas, zero jargon
7. OAuth cross-domain: JWT en URL params (no cookies cross-domain)
8. Theory universal: glossary estatico TypeScript (sin LLM, respuesta inmediata)
9. Session log en sessionStorage (no localStorage) — limpia al cerrar tab
10. Modo Socrático en consola (sin refactor de UI de hint)

---

## 18. Variables de Entorno

Frontend (.env.local):
  NEXT_PUBLIC_API_URL=https://daki-api.onrender.com

Backend (.env):
  DATABASE_URL=postgresql+asyncpg://...@neon.tech/nexo
  ANTHROPIC_API_KEY=sk-ant-...
  PISTON_API_URL=https://emkc.org/api/v2/piston
  SECRET_KEY=...
  GOOGLE_CLIENT_ID=...
  GOOGLE_CLIENT_SECRET=...
  GOOGLE_REDIRECT_URI=https://daki-api.onrender.com/api/v1/auth/google/callback
  FRONTEND_BASE_URL=https://dakiedtech.com

---

## 19. Bugs Conocidos / Tech Debt

- Monaco no funciona en mobile (no es prioridad — plataforma desktop)
- ~~RadarMaestriaModal puede mostrar datos hardcoded~~ RESUELTO: conectado a GET /intel/mastery-radar
- ~~conceptGlossary.ts tiene 14 conceptos~~ RESUELTO: expandido a 50+ en sesion 2026-04-05
- SecretMissionRevealModal: UI de revelacion existe, pero no hay pantalla de historial

---

## 20. 5 Bloques de Inversion — Inmersion y Aprendizaje (2026-04-06)

### Block 1 — Pure frontend (CodeWorkspace.tsx + DakiTerminalLine.tsx)
- **Timer color**: verde <60s, amarillo 60-120s, rojo >120s con glow pulsante
- **Concept badges HUD**: `challenge.concepts_taught_json` muestra hasta 4 badges cyan bajo el titulo
- **Editor glow dorado**: cuando `hintFreeStreak >= 3` (indicador de autonomia tactca)
- **stderr border**: borde izquierdo rojo + nuevo kind `daki-explain` (naranja) para explicaciones
- **DAKI Error Explainer**: mapa estatico de 11 error_type -> explicacion en espanol, inyectada en consola tras cada error

### Block 2 — Backend + frontend
- **failed_case** en CodeExecuteResponse: `{ got: str, expected: str }` cuando hay mismatch sin excepcion
- **new_concepts** en CodeExecuteResponse: lista de conceptos de la mision, solo en primera complecion
- **Toast "NODOS DESBLOQUEADOS"** (success, 5s) post-victoria con conceptos desbloqueados
- Consola muestra `── Salida obtenida / Salida esperada` cuando hay mismatch

### Block 3 — Pedagogical objective post-victoria
- Tras primera victoria: seccion `▸ ¿POR QUE FUNCIONA?` en consola
- Usa `challenge.pedagogical_objective` si existe, fallback a `challenge.syntax_hint`
- kind: `daki-explain` (naranja, border izquierdo)

### Block 4 — Revision Semanal
- **GET /intel/weekly-review**: conceptos con `mastery_score < 70` y `updated_at < 7 dias`
- **RevisionSemanalCard** en Hub: muestra hasta 8 conceptos debiles ordenados por score
- Cada badge muestra: concepto, score%, color segun urgencia (rojo si needs_reinforcement)

### Block 5 — DAKI Guia Paso a Paso
- Boton `▸ GUIA PASO A PASO` en HUD cuando `failStreak >= 8`
- Revela hints de `challenge.hints[]` en secuencia: PISTA 1/3 -> PISTA 2/3 -> PISTA FINAL
- Kind: `intervention` (purpura) para el header, `enigma` para el contenido
- Estado `guidedHintStep` se resetea al cambiar de challenge

---

## 22. Expansion del Ecosistema Python — Plan 7 Partes (2026-04-06)

### Estado del curriculo (actualizado con Part 1 + 2 + 3)
- Total: **127 challenges** (102 originales + 11 funciones + 8 comprensiones + 7 while)

### Mapa completo de sectores POST Part 3
| s | Fase | Niveles | N |
|---|------|---------|---|
| 0 | tutorial | 0 | 1 |
| 1 | fundamentos | 1-10 | 10 |
| 2 | flujo | 11-20 | 10 |
| 3 | ciclos (for) | 21-30 | 10 |
| **4** | **while (NUEVO)** | **31-37** | **7** |
| 5 | estructuras | 38-47 | 10 |
| **6** | **funciones (NUEVO)** | **48-58** | **11** |
| **7** | **comprensiones (NUEVO)** | **59-66** | **8** |
| 8 | cadenas | 67-76 | 10 |
| 9 | boveda | 77-86 | 10 |
| 10 | contrato | 87-96 | 10 |
| 11-13 | practica | 97-126 | 30 |

### Sector 4: While Avanzado (L31-37) — NUEVO
| L | Titulo | Concepto | XP |
|---|--------|----------|----|
| 31 | Escalada de Potencia | while + contador + *= | 175 |
| 32 | Dos Guardianes | while + AND | 200 |
| 33 | Cuenta de Digitos | while + // | 225 |
| 34 | Suma Hasta Superar | while + acumulador umbral | 225 |
| 35 | Clave de Acceso | while + flag booleano + input | 250 |
| 36 | Patron de Estrellas | while anidado | 275 |
| 37 | El Maximo Comun Divisor | while + Euclides | 350 |
- Sectores: 0-11 (anteriormente 0-10)
- Niveles: 0-111 (anteriormente 0-100)
- Eliminado: "La Cosita del Viernes" (boss_battle vacio, sector None)

### Mapa de Sectores — Estado Final (162 challenges, sesion 3)
| Sector | Fase | Niveles | Challenges |
|--------|------|---------|-----------|
| 0 | tutorial | 0 | 1 |
| 1 | fundamentos | 1-10 | 10 |
| 2 | flujo | 11-20 | 10 |
| 3 | ciclos | 21-30 | 10 |
| 4 | while | 31-37 | 7 |
| 5 | estructuras | 38-47 | 10 |
| 6 | funciones | 48-58 | 11 |
| 7 | comprensiones | 59-66 | 8 |
| 8 | cadenas | 67-76 | 10 |
| 9 | boveda | 77-86 | 10 |
| 10 | contrato | 87-96 | 10 |
| 11 | practica | 97-106 | 10 |
| 12 | practica | 107-116 | 10 |
| 13 | practica | 117-126 | 10 |
| **14** | **modulos** | **127-136** | **10** |
| **15** | **archivos** | **137-142** | **6** |
| **16** | **oop** | **143-150** | **8** |
| **17** | **errores** | **151-155** | **5** |
| **18** | **proyecto** | **156-161** | **6** |

### Sector 6: Comprensiones (L52-59) — NUEVO
| Level | Titulo | Concepto | XP |
|-------|--------|----------|----|
| 52 | La Lista Comprimida | list comprehension basica | 225 |
| 53 | El Filtro Integrado | comprehension con if | 250 |
| 54 | Transforma y Filtra | expresion + filtro combinados | 275 |
| 55 | El Mapa de Datos | dict comprehension basica | 300 |
| 56 | Inventario Activo | dict comprehension con filtro | 325 |
| 57 | El Bucle Comprimido | comprension vs bucle for | 300 |
| 58 | La Matriz Plana | comprension anidada | 375 |
| 59 | NEXUS-06: El Analizador | boss — integracion completa | 750 |

### Sector 5: Funciones Avanzadas (L41-51)
| Level | Titulo | Concepto | XP |
|-------|--------|----------|----|
| 41 | El Saludo Configurable | parametros default | 200 |
| 42 | Estadisticas del Escaner | retorno multiple | 225 |
| 43 | Cuenta Regresiva | recursion intro + caso base | 250 |
| 44 | El Factorial del Sistema | recursion clasica | 275 |
| 45 | Funciones en una Linea | lambda basica | 300 |
| 46 | Ordenamiento Inteligente | sorted() con key=lambda | 325 |
| 47 | Funciones que Reciben Funciones | orden superior | 350 |
| 48 | Transformacion en Masa | map() | 375 |
| 49 | Filtro de Frecuencias | filter() | 400 |
| 50 | Fabricas de Funciones | closures | 425 |
| 51 | NEXUS-05: Pipeline Funcional | integracion filter+map | 750 |

### Estado Final del Plan de Expansion (sesion 3 — 2026-04-07) — TODO COMPLETADO

| # | Descripcion | Challenges | Sector | Niveles | Estado |
|---|-------------|-----------|--------|---------|--------|
| 1 | Funciones avanzadas (default, recursion, lambda, HOF, closures) | 11 | 6 | 48-58 | COMPLETADO |
| 2 | Comprensiones (list, dict, nested, boss) | 8 | 7 | 59-66 | COMPLETADO |
| 3 | While profundo (retry, menu, multiple exit, boss) | 7 | 4 | 31-37 | COMPLETADO |
| 4 | Modulos stdlib (math, random, datetime, collections, string, os.path) | 10 | 14 | 127-136 | COMPLETADO |
| 5 | File I/O (open w/r/a, readlines, CSV) | 6 | 15 | 137-142 | COMPLETADO |
| 6 | OOP (class, __init__, metodos, __str__, classmethod, herencia, super) | 8 | 16 | 143-150 | COMPLETADO |
| 7 | Error handling (try/except, finally, raise, custom Exception) | 5 | 17 | 151-155 | COMPLETADO |
| 8 | Proyecto integrador (__main__, JSON, sys.argv, modulo propio, boss final) | 6 | 18 | 156-161 | COMPLETADO |
| 9 | Quality repairs (test_inputs_json para L23, L28, L29) | — | — | — | COMPLETADO |

**Total sesion 3: 35 challenges nuevos insertados. Curriculo: 127 → 162 challenges.**

### Sector 14: Modulos Stdlib (L127-136)
| Level | Titulo | Concepto | XP |
|-------|--------|----------|----|
| 127 | El Modulo math | sqrt, ceil, floor, pi | 250 |
| 128 | Geometria con math | hipotenusa + area circulo | 275 |
| 129 | random: Propiedades Garantizadas | seed, randint, choice | 275 |
| 130 | random: Muestras y Mezclas | sample, shuffle | 300 |
| 131 | datetime: Fechas y Diferencias | date(), timedelta | 300 |
| 132 | datetime: Formato de Fechas | strftime | 300 |
| 133 | collections.Counter | Counter, most_common | 325 |
| 134 | string: Caracteres y Validacion | ascii_lowercase, digits, any() | 325 |
| 135 | os.path: Rutas Portables | join, basename, dirname, splitext | 350 |
| 136 | MODULO-01: El Inspector de Datos | Counter + sum/len integration boss | 700 |

### Sector 15: File I/O (L137-142)
| Level | Titulo | Concepto | XP |
|-------|--------|----------|----|
| 137 | Escribir y Leer un Archivo | open w/r, with, f.read() | 300 |
| 138 | Leer Linea por Linea | writelines, for line in f, strip | 300 |
| 139 | Modo Append | open 'a', acumulacion de logs | 325 |
| 140 | readlines() y Comprensiones | readlines + list comprehension | 350 |
| 141 | CSV: Leer y Escribir | csv.writer, csv.reader, writerows | 400 |
| 142 | ARCHIVO-01: Procesador CSV | csv.DictReader + Counter boss | 750 |

### Sector 16: OOP (L143-150)
| Level | Titulo | Concepto | XP |
|-------|--------|----------|----|
| 143 | Tu Primera Clase | class, atributo de clase, isinstance | 300 |
| 144 | __init__ y Atributos de Instancia | __init__, self, instancia | 325 |
| 145 | Metodos de Instancia | metodos, mutacion via self | 350 |
| 146 | __str__: Representacion Legible | __str__, dunder methods | 350 |
| 147 | Atributos de Clase y @classmethod | @classmethod, cls | 375 |
| 148 | Herencia: Polimorfismo | herencia, override, polimorfismo | 400 |
| 149 | super() y Herencia Avanzada | super(), isinstance avanzado | 425 |
| 150 | OOP-01: La Red de Nodos | OOP + comprehensions boss | 800 |

### Sector 17: Error Handling (L151-155)
| Level | Titulo | Concepto | XP |
|-------|--------|----------|----|
| 151 | try/except: El Escudo del Error | try/except, ZeroDivisionError | 325 |
| 152 | Multiples Excepciones | nested try/except, ValueError | 350 |
| 153 | except as e: Inspeccionar el Error | except as e, IndexError | 350 |
| 154 | finally: Siempre se Ejecuta | finally, cleanup garantizado | 375 |
| 155 | raise: Lanzar Excepciones Custom | raise, clase Exception custom | 500 |

### Sector 18: Proyecto Integrador (L156-161)
| Level | Titulo | Concepto | XP |
|-------|--------|----------|----|
| 156 | El Guardian del Main | if __name__ == '__main__' | 375 |
| 157 | JSON: El Lenguaje de los Datos | json.dumps, json.loads | 375 |
| 158 | Verificador de Modulos | __import__, ImportError | 375 |
| 159 | Argumentos de Linea de Comandos | sys.argv pattern | 400 |
| 160 | El Modulo Propio | estructura de modulo, constantes | 425 |
| 161 | NEXUS-FINAL: El Proyecto Integrador | OOP+comprehensions+json+datetime boss | 1000 |

---

## 22. 4 Mejoras de Experiencia Profesional (2026-04-07 — Sesion 4)

### Feature 1 — DAKI Code Review post-victoria
- `POST /api/v1/daki/code-review`: envia codigo real del operador a Claude Haiku 4.5
- Haiku actua como senior Python engineer: Pythonicidad, PEP 8, patrones idiomatic
- Respuesta <= 3 lineas de feedback concreto
- `MisionDebriefModal`: muestra code review en seccion ambar antes de la pregunta metacognitiva
- `CodeWorkspace`: captura codigo ganador en `lastWinCodeRef`

### Feature 2 — Modo Debug (Sector 19, L162-169)
- `challenge_type = 'debug'`: misiones donde el codigo tiene bugs intencionales
- Banner rojo en HUD: `▸ MODO DEBUG — Encontra y corrige el bug`
- 8 challenges: NameError, TypeError, off-by-one, return faltante, KeyError, acumulador roto, condicion invertida, IndexError

### Feature 3 — Perfil Publico del Operador
- `GET /api/v1/users/profile/{callsign}`: sin auth, retorna nivel, XP, misiones, racha, liga, rango, badges
- Pagina `/p/[callsign]`: XP bar animada, grid de stats 3 columnas, badges, boton share, CTA registro

### Feature 4 — Protocolo de Entrevista (Sector 20, L170-179)
- 10 challenges con patrones clasicos de screening tecnico Python:
  two sum, palindromo, anagramas, fibonacci iterativo, elemento mas frecuente,
  invertir palabras, eliminar duplicados con orden, parentesis validos,
  maxima ganancia (greedy), boss de agrupamiento + filtering

---

## 23. Protocolo Guerrero — 7 Features Pedagogicas (2026-04-07 — Sesion 5)

### Filosofia
El operador debe **sufrir, pensar y superar** — no solo teclear. Cada feature esta guardada
para que los niveles iniciales (L0-L30) sigan siendo accesibles y el operador avance.

### F1 — Prediccion de Output (L30+)
- Widget sobre el boton RUN: input de prediccion antes de ejecutar
- Post-ejecucion: feedback verde (acertaste) o rojo (fallaste) + muestra el output real
- Solo activo en challenges `level_order >= 30`, tipo != 'predict', !ironman, !retrieval

### F2 — Predict Challenges (Sector 21, L180-L189)
- `challenge_type = 'predict'`: el operador lee codigo y escribe el output exacto SIN ejecutar
- 10 challenges sembrados via `_seed_predict_challenges()` en startup con uuid5 (idempotente)
- Correcta prediccion → llama `/execute` con `initial_code` para registrar XP
- Boss L189: map + filter + lambda con prediccion de 3 lineas exactas

| Level | Titulo | Concepto Principal | XP |
|-------|--------|-------------------|----|
| 180 | PREDICCION 01: Precedencia de Operadores | operator_precedence | 120 |
| 181 | PREDICCION 02: Indexing de Strings | string_indexing | 120 |
| 182 | PREDICCION 03: Booleanos como Enteros | boolean arithmetic | 130 |
| 183 | PREDICCION 04: Slicing de Listas | slice, negative_index | 130 |
| 184 | PREDICCION 05: Cadena de Metodos | method_chaining | 140 |
| 185 | PREDICCION 06: List Comprehension con Filtro | comprehension, filter | 160 |
| 186 | PREDICCION 07: Mutacion de Diccionario | dict, mutation | 160 |
| 187 | PREDICCION 08: Scope de Variables | scope, local vs global | 170 |
| 188 | PREDICCION 09: El Argumento Mutable (Gotcha) | mutable_default | 200 |
| 189 | PREDICCION 10 — BOSS: Map, Filter y Lambda | map, filter, lambda | 350 |

### F3 — Rubber Duck Gate (L30+, failStreak >= 3)
- Antes de pedir ENIGMA: modal azul/cyan requiere articular el razonamiento (min 15 chars)
- "¿Por que crees que falla? Describilo en al menos una oraicion." 
- Boton `ACTIVAR ENIGMA` post-explicacion redirige al flujo normal de hints
- Implementado via `pendingHintRef.current` flag para evitar doble trigger

### F4 — Modo Ironman (is_ironman=TRUE)
- Sin pistas (ENIGMA deshabilitado), sin error explainer, sin DAKI proactivo
- Banner dorado/ambar en HUD con texto `MODO IRONMAN — SIN ASISTENCIA`
- 1 challenge por sector marcado automaticamente en `init_db()` via CTE:
  - Sectores 8-20: el 2° challenge no-boss no-project por level_order
  - Idempotente: siempre marca el mismo challenge

### F5 — Pattern Callout (L20+)
- 1.5s tras cargar el challenge: fetch `GET /intel/pattern-callout?user_id=X&challenge_id=Y`
- Si hay overlap de conceptos con un challenge completado anterior → linea en consola:
  `[DAKI] Ya trabajaste '{concepto}' en '{titulo prev}' (L{N})`
- Kind: `pattern` (tono info, text blanco 40%)
- Solo activo en `level_order >= 20`

### F6 — Edge Case Gauntlet (post-victoria)
- Tras primera victoria: si el challenge tiene `edge_cases[]`, se revelan en consola
- Formato: `▸ CASO EXTREMO: {description}` — 3 casos por boss challenge
- Kind: `edge-case` (color ambar oscuro)
- Edge cases sembrados en boss challenges L136, L142, L150, L155, L161, L169, L179

### F7 — Retrieval Mode (?mode=retrieval)
- `RevisionSemanalCard`: boton `↺ PRACTICAR` por concepto debil
- `GET /intel/retrieval-challenge?user_id=X&concept=Y`: retorna challenge completado random (top 5)
- Navega a `/challenge/{id}?mode=retrieval`
- En modo retrieval: sin pistas, sin error explainer, banner morado `PROTOCOLO DE RECUPERACION`

### Archivos modificados (sesion 5)
| Archivo | Cambios |
|---------|---------|
| `app/models/challenge.py` | +2 campos: `is_ironman`, `edge_cases_json` |
| `app/api/v1/endpoints/challenges.py` | +`is_ironman`, `edge_cases`, `expected_output` en ChallengeOut |
| `app/api/v1/endpoints/intel.py` | +`GET /intel/pattern-callout`, +`GET /intel/retrieval-challenge` |
| `app/core/database.py` | +ALTER TABLE `is_ironman`/`edge_cases_json`, +ironman CTE UPDATE, +boss edge cases |
| `main.py` | +`_seed_predict_challenges()` (10 challenges uuid5 idempotentes) |
| `CodeWorkspace.tsx` | +380 lineas: todos los banners, modales, efectos y logica pedagogica |
| `RevisionSemanalCard.tsx` | Reescrito con boton PRACTICAR por concepto |

---

## 24. Checklist para Retomar Trabajo

- [ ] Verificar DakiIntelCard en challenge sin theory_content (probar en produccion)
- [ ] Verificar Fin de Turno: completar 2+ misiones -> volver al Hub -> boton aparece
- [ ] Verificar Milestones: primera victoria debe disparar MilestoneModal
- [ ] Verificar Modo Socrático: primer fail debe mostrar preguntas en consola
- [ ] Verificar Block 1-5 en produccion (deploy Vercel + Render)
- [ ] Verificar RevisionSemanalCard en Hub con datos reales (requiere 7+ dias de uso)
- [ ] Verificar DAKI Error Explainer en produccion con cada tipo de error
- [ ] Verificar Predict Challenges L180-L189 sembrados correctamente en startup
- [ ] Verificar ironman marking en init_db() (1 challenge por sector 8-20)
- [ ] Verificar Rubber Duck Gate dispara correctamente con failStreak >= 3 en L30+
- [ ] Verificar Edge Cases visibles en consola post-victoria de boss challenges
- [ ] Verificar Pattern Callout en L20+ con overlap de conceptos
- [ ] Verificar Retrieval Mode desde RevisionSemanalCard

---

## 25. Estado del Curriculo — Post Sesion 5

| Sector | Fase | Niveles | Challenges | Ironman |
|--------|------|---------|-----------|---------|
| 0 | tutorial | 0 | 1 | — |
| 1 | fundamentos | 1-10 | 10 | — |
| 2 | flujo | 11-20 | 10 | — |
| 3 | ciclos | 21-30 | 10 | — |
| 4 | while | 31-37 | 7 | — |
| 5 | estructuras | 38-47 | 10 | — |
| 6 | funciones | 48-58 | 11 | — |
| 7 | comprensiones | 59-66 | 8 | — |
| 8-13 | practica | 67-126 | 60 | 1/sector |
| 14 | modulos | 127-136 | 10 | 1 |
| 15 | archivos | 137-142 | 6 | 1 |
| 16 | oop | 143-150 | 8 | 1 |
| 17 | errores | 151-155 | 5 | 1 |
| 18 | proyecto | 156-161 | 6 | 1 |
| 19 | debug | 162-169 | 8 | 1 |
| 20 | interview | 170-179 | 10 | 1 |
| **21** | **predict** | **180-189** | **10** | — |

**Total: 190 challenges. 13 con Modo Ironman. 7 con Edge Case Gauntlet.**

---

Actualizar este archivo al final de cada sesion de trabajo significativa.
