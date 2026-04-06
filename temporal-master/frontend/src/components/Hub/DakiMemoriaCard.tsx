'use client'

/**
 * DakiMemoriaCard — DAKI recuerda tu última sesión en el Hub
 *
 * Lee sessionStorage 'daki-session-current' para mostrar un resumen
 * contextual de la sesión activa. Solo aparece si hay 1+ misión registrada.
 * No usa LLM — las frases son template-based para ser instantáneas.
 */

import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { getSessionLog } from '@/hooks/useSessionLog'
import type { SessionMission } from '@/hooks/useSessionLog'

function buildMessage(missions: SessionMission[]): string {
  if (missions.length === 0) return ''

  const total       = missions.length
  const withHints   = missions.filter(m => m.hints_used).length
  const noHints     = total - withHints
  const totalTimeMs = missions.reduce((s, m) => s + m.time_ms, 0)
  const minutes     = Math.floor(totalTimeMs / 60000)
  const avgAttempts = (missions.reduce((s, m) => s + m.attempts, 0) / total).toFixed(1)

  const lines: string[] = []

  if (total === 1) {
    lines.push(`Primera incursión del turno completada — ${missions[0].title}.`)
  } else {
    lines.push(`${total} incursiones ejecutadas en este turno (${minutes}m de tiempo activo).`)
  }

  if (noHints === total) {
    lines.push('Operaste sin ENIGMA en toda la sesión. Autonomía táctica confirmada.')
  } else if (withHints > 0) {
    lines.push(`ENIGMA activada en ${withHints} de ${total} misiones. Registrado para análisis.`)
  }

  if (parseFloat(avgAttempts) === 1.0) {
    lines.push('Ratio de primer intento: perfecto. Precisión fuera del margen promedio.')
  } else if (parseFloat(avgAttempts) > 3) {
    lines.push(`Promedio de ${avgAttempts} intentos. El patrón sugiere un concepto que necesita refuerzo.`)
  }

  return lines.join(' ')
}

export default function DakiMemoriaCard() {
  const [missions, setMissions] = useState<SessionMission[]>([])
  const [message,  setMessage]  = useState('')

  useEffect(() => {
    const log = getSessionLog()
    if (log.length === 0) return
    setMissions(log)
    setMessage(buildMessage(log))
  }, [])

  if (missions.length === 0 || !message) return null

  return (
    <motion.div
      initial={{ opacity: 0, y: -6 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.5 }}
      className="font-mono border"
      style={{
        borderColor: 'rgba(0,255,65,0.18)',
        background:  '#030A03',
        boxShadow:   '0 0 16px rgba(0,255,65,0.05)',
      }}
    >
      <div className="h-px" style={{ background: 'linear-gradient(90deg, #00FF41, transparent)' }} />

      <div className="px-4 py-3 flex gap-3">
        {/* DAKI icon */}
        <motion.div
          className="shrink-0 w-8 h-8 flex items-center justify-center text-sm border border-[#00FF41]/20"
          style={{ background: 'rgba(0,255,65,0.06)', color: '#00FF41' }}
          animate={{ opacity: [0.6, 1, 0.6] }}
          transition={{ duration: 3, repeat: Infinity }}
        >
          ◈
        </motion.div>

        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <span className="text-[7px] tracking-[0.5em] text-[#00FF41]/35">DAKI MEMORIA</span>
            <span className="text-[7px] tracking-widest px-1 border border-[#00FF41]/20 text-[#00FF41]/40">
              TURNO ACTIVO · {missions.length} MISIÓN{missions.length > 1 ? 'ES' : ''}
            </span>
          </div>
          <p className="text-[9px] leading-relaxed text-[#00FF41]/60">
            {message}
          </p>
        </div>
      </div>
    </motion.div>
  )
}
