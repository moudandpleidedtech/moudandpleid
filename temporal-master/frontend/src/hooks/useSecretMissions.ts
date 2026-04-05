/**
 * useSecretMissions — Misiones Secretas (Variable Reward, Skinner)
 *
 * Detecta comportamientos de élite y desbloquea misiones secretas sin anuncio previo.
 * Tracking en localStorage bajo la clave 'pq-behavior-log'.
 *
 * Behaviors tracked (keys en pq-behavior-log):
 *   consecutive_no_hint  — misiones completadas consecutivamente sin pistas
 *   fast_solves          — soluciones en < 90s
 *   perfect_first_try    — missiones resueltas en el primer intento
 *
 * Retorna: { checkBehavior } — call after each mission completion
 */

import { useCallback } from 'react'

const LOG_KEY = 'pq-behavior-log'

interface BehaviorLog {
  consecutive_no_hint: number
  fast_solves: number
  perfect_first_try: number
  unlocked_missions: string[]
}

const DEFAULT_LOG: BehaviorLog = {
  consecutive_no_hint: 0,
  fast_solves: 0,
  perfect_first_try: 0,
  unlocked_missions: [],
}

function loadLog(): BehaviorLog {
  try {
    const raw = localStorage.getItem(LOG_KEY)
    return raw ? { ...DEFAULT_LOG, ...JSON.parse(raw) } : { ...DEFAULT_LOG }
  } catch { return { ...DEFAULT_LOG } }
}

function saveLog(log: BehaviorLog): void {
  try { localStorage.setItem(LOG_KEY, JSON.stringify(log)) } catch { /* storage blocked */ }
}

interface SecretMission {
  id: string
  name: string
  description: string
  trigger: string
  threshold: number
}

const SECRET_MISSIONS: SecretMission[] = [
  { id: 'sm_ghost',   name: 'MODO FANTASMA',       description: 'Completaste 5 misiones seguidas sin usar ENIGMA.',                    trigger: 'consecutive_no_hint', threshold: 5 },
  { id: 'sm_sniper',  name: 'DISPARO DE FRANCOTIRADOR', description: 'Resolviste 3 misiones a la primera tentativa.',                  trigger: 'perfect_first_try',   threshold: 3 },
  { id: 'sm_blitz',   name: 'PROTOCOLO RELÁMPAGO',  description: 'Completaste 5 misiones en menos de 90 segundos cada una.',           trigger: 'fast_solves',         threshold: 5 },
  { id: 'sm_shadow',  name: 'AGENTE SOMBRA',         description: 'Completaste 10 misiones seguidas sin usar ENIGMA.',                  trigger: 'consecutive_no_hint', threshold: 10 },
  { id: 'sm_elite',   name: 'OPERADOR DE ÉLITE',     description: 'Resolviste 10 misiones a la primera tentativa — sin errores.',       trigger: 'perfect_first_try',   threshold: 10 },
]

export interface SecretUnlock {
  missionName: string
  description: string
  rarity: 'legendary'
}

export function useSecretMissions(onUnlock: (unlock: SecretUnlock) => void) {
  const checkBehavior = useCallback((
    hintUsed: boolean,
    timeSpentMs: number,
    firstTry: boolean,
  ) => {
    const log = loadLog()

    // Update counters
    if (!hintUsed) log.consecutive_no_hint += 1
    else           log.consecutive_no_hint  = 0

    if (timeSpentMs < 90_000) log.fast_solves += 1
    if (firstTry)             log.perfect_first_try += 1

    // Check for new unlocks
    for (const mission of SECRET_MISSIONS) {
      if (log.unlocked_missions.includes(mission.id)) continue
      const count = mission.trigger === 'consecutive_no_hint' ? log.consecutive_no_hint
                  : mission.trigger === 'fast_solves'         ? log.fast_solves
                  : log.perfect_first_try
      if (count >= mission.threshold) {
        log.unlocked_missions.push(mission.id)
        onUnlock({ missionName: mission.name, description: mission.description, rarity: 'legendary' })
      }
    }

    saveLog(log)
  }, [onUnlock])

  return { checkBehavior }
}
