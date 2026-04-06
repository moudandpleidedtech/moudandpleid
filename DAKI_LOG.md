# DAKI_LOG — Contexto Completo del Proyecto Nexo EdTech

> Archivo de contexto para sesiones futuras.
> Ultima actualizacion: 2026-04-05

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
- RadarMaestriaModal puede mostrar datos hardcoded (necesita conectar progreso real)
- conceptGlossary.ts tiene 14 conceptos — expandir con mas conceptos Python avanzados
- SecretMissionRevealModal: UI de revelacion existe, pero no hay pantalla de historial

---

## 20. Checklist para Retomar Trabajo

- [ ] Verificar DakiIntelCard en challenge sin theory_content (probar en produccion)
- [ ] Verificar Fin de Turno: completar 2+ misiones -> volver al Hub -> boton aparece
- [ ] Verificar Milestones: primera victoria debe disparar MilestoneModal
- [ ] Verificar Modo Socrático: primer fail debe mostrar preguntas en consola
- [ ] RadarMaestriaModal: conectar a datos reales de progreso por concepto
- [ ] Expandir conceptGlossary.ts con mas conceptos (OOP, excepciones, comprehensions)

---

Actualizar este archivo al final de cada sesion de trabajo significativa.
