/**
 * useSessionLog — Registro de misiones completadas en la sesión actual
 *
 * Persiste en sessionStorage (se borra al cerrar el tab).
 * CodeWorkspace llama pushMission() tras cada victoria.
 * Hub lee getLog() para saber si mostrar el Informe de Turno.
 */

const SESSION_KEY = 'daki-session-current'

export interface SessionMission {
  title: string
  tier: number
  time_ms: number
  hints_used: boolean
  attempts: number
}

function loadLog(): SessionMission[] {
  if (typeof window === 'undefined') return []
  try {
    const raw = sessionStorage.getItem(SESSION_KEY)
    return raw ? JSON.parse(raw) : []
  } catch { return [] }
}

function saveLog(log: SessionMission[]): void {
  if (typeof window === 'undefined') return
  try { sessionStorage.setItem(SESSION_KEY, JSON.stringify(log)) } catch {}
}

export function pushMission(mission: SessionMission): void {
  const log = loadLog()
  log.push(mission)
  saveLog(log)
}

export function getSessionLog(): SessionMission[] {
  return loadLog()
}

export function clearSessionLog(): void {
  if (typeof window === 'undefined') return
  try { sessionStorage.removeItem(SESSION_KEY) } catch {}
}
