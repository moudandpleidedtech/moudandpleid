/**
 * useMilestones — Detección de momentos héroe en el journey del Operador
 *
 * Chequea condiciones de milestone después de cada victoria y dispara
 * el callback onUnlock cuando se cumple una por primera vez.
 * Estado persistido en localStorage 'daki-milestones'.
 */

import { useCallback } from 'react'

const MILESTONES_KEY = 'daki-milestones'  // Set<string> de IDs ya desbloqueados

export interface MilestoneUnlock {
  id: string
  title: string
  message: string
  icon: string
}

interface MilestoneData {
  totalMissions:     number   // total histórico completadas
  hintsUsed:         boolean  // se usó ENIGMA en esta misión
  timeMs:            number   // tiempo de esta misión
  attempts:          number   // intentos en esta misión
  tier:              number   // tier del challenge (1/2/3)
  consecutiveNoHint: number   // racha sin ENIGMA
  streakDays:        number   // racha de días consecutivos
}

const MILESTONES: Array<{
  id: string
  title: string
  message: string
  icon: string
  check: (d: MilestoneData) => boolean
}> = [
  {
    id: 'primera_victoria',
    title: 'PRIMER PROTOCOLO EJECUTADO',
    icon: '⚡',
    message: 'El primer paso de mil. Tu código acaba de hablarle a la máquina por primera vez. El Nexo registra este momento, Operador.',
    check: ({ totalMissions }) => totalMissions === 1,
  },
  {
    id: 'primera_sin_enigma',
    title: 'OPERADOR INDEPENDIENTE',
    icon: '◎',
    message: 'Sin protocolos de ayuda táctica. Resolución pura. Esto es lo que DAKI espera de cada incursión — que la respuesta venga de tu razonamiento, no del sistema.',
    check: ({ totalMissions, hintsUsed }) => totalMissions >= 2 && !hintsUsed,
  },
  {
    id: 'cinco_misiones',
    title: 'CINCO INCURSIONES COMPLETADAS',
    icon: '▲',
    message: 'Cinco misiones. El patrón empieza a grabarse en la memoria muscular. Los operadores que llegan aquí tienen 3 veces más probabilidad de completar el programa.',
    check: ({ totalMissions }) => totalMissions === 5,
  },
  {
    id: 'diez_misiones',
    title: 'DÉCIMA INCURSIÓN',
    icon: '◆',
    message: 'Diez misiones completadas. Ya no eres un principiante — eres un operador en formación activa. El Nexo ha actualizado tu perfil de amenaza.',
    check: ({ totalMissions }) => totalMissions === 10,
  },
  {
    id: 'velocista_primera',
    title: 'PROTOCOLO RELÁMPAGO',
    icon: '◈',
    message: 'Bajo 60 segundos. Tu cerebro procesó el problema, diseñó la solución y la ejecutó antes de que el sistema esperara. Velocidad de élite detectada.',
    check: ({ timeMs }) => timeMs < 60_000,
  },
  {
    id: 'primer_tier2',
    title: 'NIVEL DE DIFICULTAD ESCALADO',
    icon: '★',
    message: 'Primera misión de nivel INTERMEDIO completada. La zona de confort es el enemigo del expertise. El Nexo eleva el nivel de amenaza.',
    check: ({ tier }) => tier >= 2,
  },
  {
    id: 'primer_tier3',
    title: 'OPERADOR AVANZADO',
    icon: '✦',
    message: 'Nivel AVANZADO. Pocos llegan aquí en las primeras semanas. Muchos lo intentan, pocos lo ejecutan. DAKI registra este acceso.',
    check: ({ tier }) => tier >= 3,
  },
  {
    id: 'racha_3_sin_enigma',
    title: 'MODO FANTASMA ACTIVADO',
    icon: '◉',
    message: 'Tres misiones seguidas sin tocar ENIGMA. Estás razonando por cuenta propia. Esto es exactamente lo que significa volverse operador — el sistema ya no es un salvavidas.',
    check: ({ consecutiveNoHint }) => consecutiveNoHint === 3,
  },
  {
    id: 'primer_intento',
    title: 'DISPARO DE PRECISIÓN',
    icon: '◀',
    message: 'Primer intento. Sin dudas. Sin iteración. Escribiste la solución, la ejecutaste, pasó. Hay operadores que nunca logran esto en meses de práctica.',
    check: ({ attempts }) => attempts === 1,
  },
  {
    id: 'veinte_misiones',
    title: 'VETERANO DEL NEXO',
    icon: '⬡',
    message: 'Veinte misiones. No es suerte, no es casualidad — es consistencia. DAKI actualiza tu clasificación: Operador Veterano en formación activa.',
    check: ({ totalMissions }) => totalMissions === 20,
  },
]

function loadUnlocked(): Set<string> {
  try {
    const raw = localStorage.getItem(MILESTONES_KEY)
    return raw ? new Set(JSON.parse(raw)) : new Set()
  } catch { return new Set() }
}

function saveUnlocked(s: Set<string>): void {
  try { localStorage.setItem(MILESTONES_KEY, JSON.stringify([...s])) } catch {}
}

export function useMilestones(onUnlock: (m: MilestoneUnlock) => void) {
  const checkMilestones = useCallback((data: MilestoneData) => {
    const unlocked = loadUnlocked()
    const newUnlocks: MilestoneUnlock[] = []

    for (const m of MILESTONES) {
      if (unlocked.has(m.id)) continue
      if (m.check(data)) {
        unlocked.add(m.id)
        newUnlocks.push({ id: m.id, title: m.title, message: m.message, icon: m.icon })
      }
    }

    if (newUnlocks.length > 0) {
      saveUnlocked(unlocked)
      // Disparar con pequeño delay para no solapar con la victoria
      newUnlocks.forEach((u, i) => {
        setTimeout(() => onUnlock(u), 800 + i * 400)
      })
    }
  }, [onUnlock])

  return { checkMilestones }
}
