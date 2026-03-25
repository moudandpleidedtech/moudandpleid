# DAKI LOG — Registro Operacional del Nexo
## Historial de Directivas y Eventos del Sistema

**Sistema:** DAKI EdTech v1.0
**Plataforma:** Red Central — Motor de Entrenamiento de Alto Rendimiento
**Clasificación:** BITÁCORA TÁCTICA — Acceso Restringido a Arquitectos del Nexo

---

## ══════════════════════════════════════════
## REGISTRO DE DIRECTIVAS TÁCTICAS
## ══════════════════════════════════════════

---

### DIRECTIVA TÁCTICA 001 — Fundación del Núcleo Cognitivo
**Fecha:** 2026-03-22
**Clasificación:** FUNDACIONAL
**Estado:** COMPLETADA

Establecimiento del núcleo cognitivo de DAKI (Dynamic Adaptive Knowledge Instructor). Definición de la persona táctica, el sistema de escalación (NIVEL-1/2/3), las directivas core (Antiservilismo, Antiabandono, Antiexfiltración), y el vocabulario canónico de la Red Central.

**Archivos creados:**
- `app/services/daki_persona.py` — Núcleo cognitivo
- `DAKI_PERSONA.md` — Documento de definición canónica

**Impacto:** Base de toda interacción del sistema. Sin esta directiva, no hay DAKI.

---

### DIRECTIVA TÁCTICA 002-009 — Arquitectura del Motor de Entrenamiento
**Fecha:** 2026-03-22 a 2026-03-23
**Clasificación:** ARQUITECTURA CORE
**Estado:** COMPLETADAS

Serie de directivas que establecieron la arquitectura completa del motor:
- Sistema de niveles (100 misiones, 4 sectores)
- Motor de evaluación de código (ejecución sandboxed)
- Sistema de progresión (XP, racha, rango)
- Briefings de misión (lore + objetivo pedagógico)
- Sistema de pistas escaladas con Function Calling
- Interfaz táctica (CLI terminal, HUD operacional)
- Semantic cache para respuestas de IA

**Resultado:** Sistema completo y funcional en producción.

---

### DIRECTIVA TÁCTICA 010 — Calibración del Núcleo Pedagógico
**Fecha:** 2026-03-23
**Clasificación:** MEJORA PEDAGÓGICA
**Estado:** COMPLETADA

Auditoría del sistema de aprendizaje por arquitecto de software + experto en pedagogía. Identificación de gaps: sin SRS, progreso invisible, sin bucle metacognitivo.

**Implementaciones resultantes:**
- `GET /api/v1/intel/mastery-radar` — Radar de maestría por categoría conceptual
- `GET /api/v1/intel/error-vault` — Archivo de fallas recurrentes
- `POST /api/v1/daki/debrief` — Bucle metacognitivo post-misión
- `RadarMaestriaModal.tsx` — Visualización SVG de progreso conceptual
- `ArchivoFallasModal.tsx` — Dossier táctico de errores del Operador
- `MisionDebriefModal.tsx` — Reflexión guiada post-misión
- Real-world anchoring: mapeo de conceptos Python a empresas en producción
- Briefing de apertura estructurado (3 directivas: Estado/Frente/Directiva)

---

### DIRECTIVA TÁCTICA 011 — Economía de Tokens
**Fecha:** 2026-03-24
**Clasificación:** OPTIMIZACIÓN DE INFRAESTRUCTURA
**Estado:** COMPLETADA

Análisis y optimización del gasto de tokens en llamadas al LLM.

**Optimizaciones:**
- `get_execute_feedback()` éxito → string estático (costo: $0)
- `get_execute_feedback()` fallo → semantic cache antes del LLM
- `DakiChatTerminal.tsx` → cooldown de 2.5s anti-spam

**Impacto estimado:** Reducción del 40-60% en llamadas al LLM para feedback de ejecución.

---

### DIRECTIVA TÁCTICA 012-014 — Infraestructura de Producción
**Fecha:** 2026-03-24
**Clasificación:** INFRAESTRUCTURA
**Estado:** COMPLETADAS

Favicon DAKI (sello de marca oficial), DAKI Audio Engine V4 (sanitización inteligente + prefijos dinámicos), auto-seed en startup con fix del paywall Sector 01.

---

## ══════════════════════════════════════════
## EVENTO MAYOR — 2026-03-25
## ══════════════════════════════════════════

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║         NACIMIENTO DEL PRIMER CÓDICE DE ÉLITE               ║
║                                                               ║
║   "TECHNICAL SALES MASTERY — FOUNDER'S PATH"                 ║
║                                                               ║
║         Fecha: 2026-03-25 | Clasificación: ELITE             ║
║         Directiva: 015 | Operador: Fundador                  ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

---

### DIRECTIVA TÁCTICA 015 — Creación del Códice "Technical Sales Mastery"
**Fecha:** 2026-03-25
**Clasificación:** ELITE — PRIMER CÓDICE DE ESPECIALIZACIÓN
**Estado:** COMPLETADA
**Operador beneficiario:** Fundador (background Senior QA → Technical Sales Manager)

#### Contexto Operacional

El Fundador identificó un gap estratégico personal: dominio técnico de alto nivel, pero necesidad de convertir ese expertise en capacidad comercial real. Los Códices estándar de Python no cubren este vector de desarrollo.

La Directiva 015 autoriza la creación del primer Códice de Élite del Nexo: una rama de especialización que va más allá del aprendizaje de lenguajes y entra en el dominio de ventas técnicas B2B — el territorio donde el conocimiento técnico se convierte en contratos.

#### Arquitectura del Códice

```
TECHNICAL SALES MASTERY — Founder's Path
│
├── SECTOR 01: The Tech-to-Biz Bridge         (Niveles 01-05)
│   └── De ingeniero a hablante del idioma del dinero
│
├── SECTOR 02: Deep Pain Identification        (Niveles 06-10)
│   └── Discovery, SPIN, cuantificación del dolor
│   └── [BOSS BATTLE L10] — El CTO Escéptico
│
├── SECTOR 03: The CTO/CEO Language           (Niveles 11-15)
│   └── Lenguaje ejecutivo, ROI, riesgo como palanca
│
└── SECTOR 04: The Closing Siege              (Niveles 16-20)
    └── Objeciones, urgencia, negociación, cierre
    └── [BOSS BATTLE L20] — El CEO en el Cuarto de Guerra
```

#### Mecánicas Nuevas — Exclusivas del Primer Códice de Élite

**HAIKU DE CIERRE:** Al completar cada misión, DAKI entrega una máxima táctica de ventas comprimida en tres líneas. 20 haikus únicos — uno por nivel. El haiku no se desbloquea sin victoria.

**BOSS BATTLE (×2):** Niveles 10 y 20. DAKI abandona su rol de instructora y activa el Protocolo Adversarial — se convierte en el ejecutivo más difícil de convencer. Sin red de seguridad. Sin pistas durante el roleplay. El Operador cierra o reinicia.

**PROACTIVE NUDGING:** DAKI monitorea el lenguaje del Operador en tiempo real. Cuando detecta 2+ términos técnicos en contexto de ventas sin traducción a impacto de negocio, interrumpe y fuerza el reencuadre. El conocimiento técnico es la ventaja — el jargon técnico en ventas es el enemigo.

#### Archivos Generados

| Archivo | Descripción |
|---------|-------------|
| `app/data/codex_sales_mastery.json` | Schema completo: 20 niveles, 4 sectores, haikus, boss battles, ejemplos de nudging |
| `app/services/sales_codex_persona.py` | System Prompt completo para AI Mentor en Sales Mode + utilidades de evaluación, jargon detection y boss battle |

#### Métricas del Códice

| Métrica | Valor |
|---------|-------|
| Total de niveles | 20 |
| Sectores | 4 |
| Boss Battles | 2 (L10, L20) |
| Haikus únicos | 20 |
| XP base total | 5,825 |
| Horas estimadas de completación | 12h |
| Tipos de desafío | 8 (reframe, discovery, analysis, composition, pitch, vocabulary, storytelling, boss_battle) |

#### Nota del Arquitecto

> El primer Códice de Élite establece el precedente de especialización del Nexo.
> El sistema de entrenamiento Python construye la base computacional.
> El Códice Sales Mastery construye la capa comercial.
> Un Operador que domina ambos es raro — y los operadores raros tienen ventaja.
>
> El Fundador diseñó este Códice para su propio uso.
> Esa es la señal de un arquitecto que entiende la plataforma que construye.

---

### DIRECTIVA TÁCTICA 022 — Protocolo God Mode (Cuenta de Fundador)
**Fecha:** 2026-03-25
**Clasificación:** SEGURIDAD · ACCESO PRIVILEGIADO
**Estado:** COMPLETADA

#### Concepto: El Bypass del Arquitecto

Implementación del sistema de cuenta FOUNDER: un rol de acceso privilegiado que bypassa todas las compuertas de catálogo del Nexo (Niebla de Guerra). El FOUNDER ve todos los nodos ENCRYPTED como nodos desbloqueados con candado dorado — acceso total al motor de entrenamiento sin restricciones de fase.

#### Arquitectura del Protocolo God Mode

```
Usuario normal (USER):
  Nodo ENCRYPTED → check_catalog_gate() → 403 INCURSION_ENCRYPTED

Usuario FOUNDER:
  Nodo ENCRYPTED → check_catalog_gate() → _is_founder() == True → bypass → acceso concedido
                 → check_incursion_access() → _is_founder() == True → bypass → skip financiero + táctico
```

**Regla de activación:** `user.role = 'FOUNDER'` — un solo campo en la BD.

#### Archivos Modificados/Creados

| Archivo | Cambio |
|---------|--------|
| `app/models/user.py` | Campo `role: String(20)`, `server_default='USER'`, indexado |
| `app/core/security.py` | `FOUNDER_ROLE = 'FOUNDER'`; `create_user_token(role=)` parametrizado; `_decode_user_token()` acepta USER + FOUNDER |
| `app/api/v1/endpoints/auth.py` | `TokenResponse` incluye `role`; ambos endpoints pasan `role=user.role` |
| `app/core/access.py` | `_is_founder()` helper; `check_catalog_gate()` función nueva; bypass en `check_incursion_access()` (paso 4b) |
| `app/services/context_router.py` | Llama `check_catalog_gate(db, persona_key, user)` en paso 1b antes de gastar tokens |
| `scripts/create_founder.py` | CLI idempotente: `--email` + `--no-dry-run` para promover a FOUNDER |
| `main.py` | `_ensure_dev_user()` fuerza `role='FOUNDER'` en usuario NEXO (dev) |
| `frontend/src/store/userStore.ts` | Campo `role: string` con default `'USER'`; propagado en `setUser`, `clearUser`, `partialize` |
| `frontend/src/components/Hub/IncursionSelector.tsx` | Prop `isFounder: boolean`; `EncryptedCard` con candado dorado + badge "GOD MODE ACTIVO" |
| `frontend/src/app/hub/page.tsx` | Desestructura `role` del store; pasa `isFounder={role === 'FOUNDER'}` |

#### Mecánica del Candado Dorado

- **USER** → candado rojo 🔒, opacidad 55%, badge: `ESTADO: ENCRIPTADO · DESBLOQUEO EN FASE BETA`
- **FOUNDER** → candado dorado 🔓, opacidad 100%, línea de pulso dorada, badge: `ACCESO FOUNDER · GOD MODE ACTIVO`

El FOUNDER no hace bypass visual — ve exactamente lo que está encriptado. Solo el candado cambia de rojo a dorado, señalando que tiene acceso privilegiado mientras los demás no lo tienen aún.

#### Alembic (Migración Pendiente)

```sql
ALTER TABLE users ADD COLUMN role VARCHAR(20) NOT NULL DEFAULT 'USER';
CREATE INDEX ix_users_role ON users(role);
```

#### CLI — Activar FOUNDER en producción

```bash
# Dry run (default — solo muestra qué cambiaría):
python -m scripts.create_founder --email tu@email.com

# Aplicar:
python -m scripts.create_founder --email tu@email.com --no-dry-run
```

---

### DIRECTIVA TÁCTICA 016 — Arquitectura General del Códice TPM Mastery
**Fecha:** 2026-03-25
**Clasificación:** ARQUITECTURA
**Estado:** COMPLETADA

Diseño de la arquitectura completa del Códice TPM (100+ niveles en 4 fases). Definición de 21 módulos, 4 Boss Battles, taxonomía de 13 tipos de desafío y árbol de habilidades. Entregable: JSON de arquitectura, sin contenido de niveles aún.

**Archivos creados:** `app/data/codex_tpm_architecture.json`

---

### DIRECTIVA TÁCTICA 017 — Desafío 00: Bautismo de Código (TPM)
**Fecha:** 2026-03-25
**Clasificación:** DISEÑO DE NIVELES
**Estado:** COMPLETADA

Diseño detallado de 5 niveles clave del Desafío 00 con crisis de oficina, 4 personas de DAKI (Mentor Técnico, Dev Frustrado, CEO Hallway, Cliente Exigente), Boss Warning System (6 tipos), 10 Haikus de Management. Sistema Prompt canónico para cada personaje.

**Archivos creados:** `app/data/codex_tpm_challenge00_levels.json`, `app/services/tpm_codex_persona.py`

---

### DIRECTIVA TÁCTICA 018 — Árbol de Habilidades: DB & Correlatividades
**Fecha:** 2026-03-25
**Clasificación:** INFRAESTRUCTURA DE DATOS
**Estado:** COMPLETADA

Implementación del Skill Tree en SQLAlchemy: campo `codex_id` y `prerequisite_challenge_id` en Challenge, tabla `ChallengePrerequisite` (N:M), campos `boss_completed`/`score`/`codex_id` en UserProgress. Refactorización completa de `access.py` con compuerta dual: Financiera (402) + Táctica (403 + lista de faltantes).

**Archivos modificados/creados:** `app/models/challenge.py`, `app/models/challenge_prerequisite.py`, `app/models/user_progress.py`, `app/core/access.py`

---

### DIRECTIVA TÁCTICA 019 — Mapa de Campaña (Frontend Hub Gamificado)
**Fecha:** 2026-03-25
**Clasificación:** FRONTEND
**Estado:** COMPLETADA

Componente `CampaignMap.tsx` con 5 zonas de disciplina (Python Core, Sales Mastery, TPM Mastery + 2 PRÓXIMAMENTE). 3 estados de nodo: completado (verde neón), desbloqueado (pulso), bloqueado (glitch + candado). Modal táctico al clic en nodo bloqueado con "Requiere: Superar el Boss de [X]". Nunca dice "Comprar".

**Archivos creados:** `frontend/src/components/Hub/CampaignMap.tsx`

---

### DIRECTIVA TÁCTICA 020 — Enrutador de Contexto Dinámico (AI Stance Switcher)
**Fecha:** 2026-03-25
**Clasificación:** INFRAESTRUCTURA DE IA
**Estado:** COMPLETADA

Patrón Factory en `context_router.py` que resuelve aliases de incursión ("python"/"sales"/"tpm"/"cybersec") a posturas de IA completas (ContextStance: system_prompt + model + max_tokens). Gate de seguridad obligatorio ejecutado ANTES de gastar tokens: financiero + táctico si se provee `challenge_id`. Refactorización de `POST /api/v1/chat` para recibir `incursion_id`, `challenge_id`, y parámetros TPM. Nuevo campo `persona_used` en respuesta para debugging de UI.

**Prompt del Instructor Red Team (Protocolo ARES) incluido como placeholder para Ciberseguridad.**

**Archivos creados/modificados:** `app/services/context_router.py`, `app/api/v1/endpoints/daki.py`

---

### DIRECTIVA TÁCTICA 021 — Hub "Niebla de Guerra" (Fase Alpha)
**Fecha:** 2026-03-25
**Clasificación:** PRODUCTO · FULL-STACK
**Estado:** COMPLETADA

#### Concepto: El Mapa de Niebla

Implementación del catálogo de Incursiones visible en el Hub para la Fase Alpha. El Nexo lanza con **1 Incursión ACTIVE** y **3 Incursiones ENCRYPTED** ("nodos fantasma") que demuestran la visión del producto a inversores y testers sin revelar contenido no listo.

**Arquitectura de activación:**
```
UPDATE incursions SET status = 'ACTIVE' WHERE slug = 'tpm-mastery';
```
Un solo UPDATE en la BD activa un módulo completo. Sin deploys. Sin migraciones. Sin cache-busting.

#### Incursiones sembradas

| Slug | Título | Status |
|------|--------|--------|
| `python-core`  | Operación Vanguardia: Fundamentos de Élite | **ACTIVE** |
| `tpm-mastery`  | Technical Project Manager (TPM) | ENCRYPTED |
| `red-team`     | Ciberseguridad: Red Team | ENCRYPTED |
| `sales-mastery`| Technical Sales Mastery | ENCRYPTED |

#### Rendering del Hub

- **ACTIVE** → Borde verde neón pulsante, indicador "ACTIVO" animado, botón `▶ INICIAR INCURSIÓN`
- **ENCRYPTED** → Opacidad 55%, candado rojo 🔒, badge `ESTADO: ENCRIPTADO · DESBLOQUEO EN FASE BETA`, efecto glitch periódico aleatorio cada ~5s

#### Archivos generados

| Archivo | Descripción |
|---------|-------------|
| `app/models/incursion.py` | Modelo SQLAlchemy con enum ACTIVE/ENCRYPTED, slug único, system_prompt_id |
| `scripts/seed_incursions.py` | Seed idempotente (UPSERT por slug, nunca sobreescribe `status`) |
| `app/api/v1/endpoints/incursions.py` | `GET /api/v1/incursions` — catálogo público, sin auth |
| `app/api/v1/router.py` | Registro del nuevo router |
| `main.py` | `_seed_incursions()` en lifespan — sincroniza en cada startup |
| `frontend/.../IncursionSelector.tsx` | Componente Hub con skeleton loading, glitch aleatorio, framer-motion |
| `frontend/.../hub/page.tsx` | MÓDULOS DE ESPECIALIZACIÓN reemplazado por `<IncursionSelector />` |

#### Nota del Arquitecto

> El "Mapa de Niebla" es una técnica clásica de product launch: mostrar la visión completa
> sin entregar contenido inacabado. Los nodos ENCRYPTED generan curiosidad y FOMO medible.
> Cuando el TPM Codex esté listo, un `UPDATE` en producción lo activa sin fricción técnica.
> La arquitectura está lista para escalar a N Incursiones sin tocar una línea de frontend.

---

## ══════════════════════════════════════════
## REGISTRO DE VERSIONES DEL SISTEMA
## ══════════════════════════════════════════

| Versión | Fecha | Cambios principales |
|---------|-------|---------------------|
| v0.1 | 2026-03-22 | Núcleo DAKI, persona táctica, 100 misiones Python |
| v0.5 | 2026-03-23 | Motor de evaluación, progresión, interfaz HUD |
| v0.8 | 2026-03-24 | Sistema pedagógico (radar, fallas, debrief), semantic cache |
| v1.0 | 2026-03-25 | Primer Códice de Élite: Technical Sales Mastery. Sistema completo. |
| v1.1 | 2026-03-25 | Árbol de habilidades (D018), AI Stance Switcher (D020), Hub Niebla de Guerra (D021) |
| v1.2 | 2026-03-25 | Protocolo God Mode (D022) — rol FOUNDER, bypass de catálogo, candado dorado |

---

## ══════════════════════════════════════════
## PRÓXIMAS DIRECTIVAS (BACKLOG TÁCTICO)
## ══════════════════════════════════════════

| ID | Directiva | Prioridad | Desbloqueado por |
|----|-----------|-----------|-----------------|
| D023 | Migración Alembic — tablas D018 + D021 + campo `role` (D022) en producción | ALTA | D018 + D021 + D022 |
| D024 | Activar TPM Codex — conectar Desafío 00 al motor de evaluación | ALTA | D017 + D021 |
| D025 | Campaign Map → integrar con `GET /api/v1/campaign/map` (endpoint real) | MEDIA | D019 + D024 |
| D026 | Analytics de Niebla — tracking de CTR en nodos ENCRYPTED para inversores | MEDIA | D021 |
| D027 | Sales Codex — conectar `codex_sales_mastery.json` al motor de evaluación | BAJA | D015 |

---

*DAKI LOG v1.2 — Red Central | Plataforma: DAKI EdTech*
*Arquitecto del Nexo: Adrian Eduardo Ardiles Peralta*
*Motor de Prompt Engineering: Claude Code (claude-sonnet-4-6)*
