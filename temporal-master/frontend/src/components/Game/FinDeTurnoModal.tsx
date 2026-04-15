'use client'

/**
 * FinDeTurnoModal — Informe de Fin de Turno de DAKI
 *
 * Se muestra en el hub cuando el operador completó 2+ misiones en la sesión.
 * Llama a POST /api/v1/daki/session-summary con los datos de la sesión.
 * DAKI analiza el rendimiento y genera un informe personalizado con directiva.
 */

import { useEffect, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import type { SessionMission } from '@/hooks/useSessionLog'

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? ''

interface Props {
  visible: boolean
  missions: SessionMission[]
  operatorLevel: number
  userId: string
  onClose: () => void
}

export default function FinDeTurnoModal({ visible, missions, operatorLevel, userId, onClose }: Props) {
  const [summary,  setSummary]  = useState('')
  const [loading,  setLoading]  = useState(false)

  useEffect(() => {
    if (!visible || missions.length === 0) return
    setLoading(true)
    setSummary('')

    fetch(`${API_BASE}/api/v1/daki/session-summary`, {
      method:      'POST',
      credentials: 'include',
      headers:     { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id:        userId,
        missions,
        operator_level: operatorLevel,
      }),
    })
      .then(r => r.ok ? r.json() : null)
      .then(data => { if (data?.summary) setSummary(data.summary) })
      .catch(() => setSummary('Turno cerrado. Analiza tu rendimiento y prepara la siguiente ofensiva.'))
      .finally(() => setLoading(false))
  }, [visible]) // eslint-disable-line react-hooks/exhaustive-deps

  // Stats de la sesión
  const totalTime   = missions.reduce((s, m) => s + m.time_ms, 0)
  const hintsUsed   = missions.filter(m => m.hints_used).length
  const avgAttempts = missions.length
    ? (missions.reduce((s, m) => s + m.attempts, 0) / missions.length).toFixed(1)
    : '0'
  const minutes = Math.floor(totalTime / 60000)
  const seconds = Math.floor((totalTime % 60000) / 1000)

  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          className="fixed inset-0 z-[250] flex items-center justify-center"
          style={{ background: 'rgba(0,0,0,0.90)' }}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={onClose}
        >
          <div
            className="absolute inset-0 pointer-events-none"
            style={{ backgroundImage: 'repeating-linear-gradient(0deg,transparent,transparent 3px,rgba(0,255,65,0.012) 3px,rgba(0,255,65,0.012) 4px)' }}
          />

          <motion.div
            initial={{ scale: 0.88, y: 24, opacity: 0 }}
            animate={{ scale: 1,    y: 0,  opacity: 1 }}
            exit={{ scale: 0.92, opacity: 0 }}
            transition={{ type: 'spring', stiffness: 280, damping: 24 }}
            className="relative w-full max-w-md mx-4 font-mono overflow-hidden"
            onClick={e => e.stopPropagation()}
            style={{
              background:   '#030A03',
              border:       '1px solid rgba(0,255,65,0.25)',
              boxShadow:    '0 0 60px rgba(0,255,65,0.08)',
            }}
          >
            <div className="h-px w-full" style={{ background: 'linear-gradient(90deg, transparent, #00FF41, transparent)' }} />

            {/* Header */}
            <div className="flex items-center justify-between px-5 pt-5 pb-3 border-b border-[#00FF41]/10">
              <div>
                <p className="text-[7px] tracking-[0.7em] text-[#00FF41]/35 mb-0.5">// DAKI INTEL</p>
                <h2 className="text-sm font-black tracking-[0.2em] text-[#00FF41]"
                  style={{ textShadow: '0 0 12px rgba(0,255,65,0.35)' }}>
                  INFORME DE FIN DE TURNO
                </h2>
              </div>
              <button
                onClick={onClose}
                className="text-[9px] tracking-[0.4em] text-[#00FF41]/25 hover:text-[#00FF41]/60 transition-colors"
              >
                [ CERRAR ]
              </button>
            </div>

            {/* Stats strip */}
            <div className="grid grid-cols-4 border-b border-[#00FF41]/08">
              {[
                { label: 'MISIONES', value: String(missions.length) },
                { label: 'TIEMPO',   value: `${minutes}m${seconds}s` },
                { label: 'ENIGMA',   value: `${hintsUsed}x` },
                { label: 'Ø INTENTOS', value: avgAttempts },
              ].map(({ label, value }) => (
                <div key={label} className="px-3 py-3 text-center border-r border-[#00FF41]/08 last:border-r-0">
                  <p className="text-base font-black text-[#00FF41]"
                    style={{ textShadow: '0 0 8px rgba(0,255,65,0.4)' }}>{value}</p>
                  <p className="text-[6px] tracking-[0.3em] text-[#00FF41]/30 mt-0.5">{label}</p>
                </div>
              ))}
            </div>

            {/* Mission list */}
            <div className="px-5 pt-3 pb-2 space-y-1 max-h-28 overflow-y-auto">
              {missions.map((m, i) => (
                <div key={i} className="flex items-center gap-2 text-[9px]">
                  <span className="text-[#00FF41]/20">▸</span>
                  <span className="text-[#00FF41]/55 flex-1 truncate">{m.title}</span>
                  <span style={{ color: m.hints_used ? '#FFB800' : '#00FF41', opacity: 0.5 }}>
                    {m.hints_used ? '⚑' : '◎'}
                  </span>
                </div>
              ))}
            </div>

            {/* DAKI summary */}
            <div className="px-5 py-4 border-t border-[#00FF41]/08 min-h-[90px]">
              {loading ? (
                <p className="text-[10px] tracking-[0.3em] text-[#00FF41]/30 animate-pulse">
                  {'> DAKI ANALIZANDO TURNO...'}
                </p>
              ) : summary ? (
                <motion.div
                  initial={{ opacity: 0, y: 4 }}
                  animate={{ opacity: 1, y: 0 }}
                >
                  <p className="text-[7px] tracking-[0.5em] text-[#00FF41]/30 mb-2">ANÁLISIS DAKI</p>
                  <p className="text-[10px] leading-relaxed text-[#00FF41]/75 whitespace-pre-line">
                    {summary}
                  </p>
                </motion.div>
              ) : null}
            </div>

            {/* Footer */}
            <div className="px-5 pb-5 flex justify-end">
              <button
                onClick={onClose}
                className="text-[9px] tracking-[0.4em] px-4 py-2 border transition-all duration-150"
                style={{ borderColor: 'rgba(0,255,65,0.25)', color: 'rgba(0,255,65,0.50)' }}
                onMouseEnter={e => {
                  e.currentTarget.style.color = '#00FF41'
                  e.currentTarget.style.borderColor = 'rgba(0,255,65,0.60)'
                  e.currentTarget.style.boxShadow = '0 0 12px rgba(0,255,65,0.15)'
                }}
                onMouseLeave={e => {
                  e.currentTarget.style.color = 'rgba(0,255,65,0.50)'
                  e.currentTarget.style.borderColor = 'rgba(0,255,65,0.25)'
                  e.currentTarget.style.boxShadow = 'none'
                }}
              >
                [ SIGUIENTE TURNO ]
              </button>
            </div>

            <div className="h-px w-full" style={{ background: 'linear-gradient(90deg, transparent, #00FF41, transparent)' }} />
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}
