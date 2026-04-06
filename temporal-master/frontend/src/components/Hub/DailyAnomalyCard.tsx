'use client'

/**
 * DailyAnomalyCard — Anomalía del Día en el hub
 * Llama a GET /api/v1/daily-anomaly y muestra la misión especial del día.
 * Cambia cada día de forma determinista (sin DB).
 *
 * Tracking local: guarda {id, date} en localStorage cuando carga.
 * El operador puede marcar la anomalía como completada manualmente.
 * CodeWorkspace también la marca al completar el challenge coincidente.
 */

import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? ''
const ANOMALY_KEY  = 'daki-anomaly-today'   // {id, date} de la anomalía activa
const DONE_KEY     = 'daki-anomaly-done'    // fecha ISO si fue completada hoy

interface Anomaly {
  id: string
  title: string
  description: string
  concept: string
  glyph: string
  difficulty: string
  difficulty_color: string
  xp_bonus: number
  date: string
}

export default function DailyAnomalyCard() {
  const [anomaly,   setAnomaly]   = useState<Anomaly | null>(null)
  const [expanded,  setExpanded]  = useState(false)
  const [completed, setCompleted] = useState(false)

  useEffect(() => {
    fetch(`${API_BASE}/api/v1/daily-anomaly`)
      .then((r) => r.json())
      .then((data: Anomaly) => {
        setAnomaly(data)
        // Persistir para que CodeWorkspace pueda detectar la coincidencia
        try { localStorage.setItem(ANOMALY_KEY, JSON.stringify({ id: data.id, date: data.date })) } catch {}
        // Verificar si ya fue completada hoy
        try {
          const done = localStorage.getItem(DONE_KEY)
          if (done === data.date) setCompleted(true)
        } catch {}
      })
      .catch(() => {})
  }, [])

  const markCompleted = (e: React.MouseEvent) => {
    e.stopPropagation()
    if (!anomaly || completed) return
    try { localStorage.setItem(DONE_KEY, anomaly.date) } catch {}
    setCompleted(true)
  }

  if (!anomaly) return null

  const color = anomaly.difficulty_color

  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.3 }}
      className="font-mono border cursor-pointer select-none"
      style={{
        borderColor: completed ? 'rgba(0,255,65,0.35)' : `${color}30`,
        background: '#030A03',
        boxShadow: completed
          ? '0 0 20px rgba(0,255,65,0.08)'
          : `0 0 20px ${color}0C`,
      }}
      onClick={() => setExpanded((v) => !v)}
    >
      {/* Top bar */}
      <div
        className="h-0.5 w-full"
        style={{
          background: completed
            ? 'linear-gradient(90deg, #00FF41, transparent)'
            : `linear-gradient(90deg, ${color}, transparent)`,
        }}
      />

      <div className="px-4 py-3 flex items-start gap-3">
        {/* Glyph */}
        <motion.div
          className="shrink-0 w-9 h-9 flex items-center justify-center text-lg border"
          style={{
            borderColor: completed ? 'rgba(0,255,65,0.25)' : `${color}25`,
            background:  completed ? 'rgba(0,255,65,0.08)' : `${color}08`,
          }}
          animate={completed ? {} : { opacity: [0.7, 1, 0.7] }}
          transition={{ duration: 2.2, repeat: Infinity }}
        >
          {completed ? '✓' : anomaly.glyph}
        </motion.div>

        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-0.5">
            <span className="text-[7px] tracking-[0.5em]" style={{ color: completed ? 'rgba(0,255,65,0.50)' : `${color}50` }}>
              ANOMALÍA DEL DÍA
            </span>
            <span
              className="text-[7px] tracking-widest px-1 border"
              style={{
                color:       completed ? '#00FF41' : color,
                borderColor: completed ? 'rgba(0,255,65,0.30)' : `${color}30`,
              }}
            >
              {completed ? 'COMPLETADA' : anomaly.difficulty}
            </span>
          </div>

          <div
            className="text-[11px] font-black tracking-wider"
            style={{ color: completed ? '#00FF41' : color }}
          >
            {anomaly.title}
          </div>

          {expanded && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              className="mt-1.5 space-y-2"
            >
              <p className="text-[9px] leading-relaxed text-[#C0FFC0]/60">
                {anomaly.description}
              </p>

              <p className="text-[8px] tracking-wider" style={{ color: `${color}50` }}>
                CONCEPTO: {anomaly.concept.toUpperCase()}
              </p>

              {!completed && (
                <button
                  onClick={markCompleted}
                  className="text-[8px] tracking-[0.35em] px-2 py-1 border transition-all duration-150 mt-1"
                  style={{ borderColor: 'rgba(0,255,65,0.20)', color: 'rgba(0,255,65,0.40)' }}
                  onMouseEnter={e => {
                    e.currentTarget.style.color = '#00FF41'
                    e.currentTarget.style.borderColor = 'rgba(0,255,65,0.50)'
                  }}
                  onMouseLeave={e => {
                    e.currentTarget.style.color = 'rgba(0,255,65,0.40)'
                    e.currentTarget.style.borderColor = 'rgba(0,255,65,0.20)'
                  }}
                >
                  ✓ MARCAR COMPLETADA
                </button>
              )}
            </motion.div>
          )}
        </div>

        <div className="shrink-0 text-right">
          <div className="text-[8px] font-bold" style={{ color: completed ? 'rgba(0,255,65,0.70)' : `${color}70` }}>
            +{anomaly.xp_bonus} XP
          </div>
          <div className="text-[7px] text-[#00FF41]/25 mt-0.5">
            {expanded ? '▲ cerrar' : '▼ ver'}
          </div>
        </div>
      </div>
    </motion.div>
  )
}
