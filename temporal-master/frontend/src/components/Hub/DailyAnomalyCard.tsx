'use client'

/**
 * DailyAnomalyCard — Anomalía del Día en el hub
 * Llama a GET /api/v1/daily-anomaly y muestra la misión especial del día.
 * Cambia cada día de forma determinista (sin DB).
 */

import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? ''

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
  const [anomaly, setAnomaly] = useState<Anomaly | null>(null)
  const [expanded, setExpanded] = useState(false)

  useEffect(() => {
    fetch(`${API_BASE}/api/v1/daily-anomaly`)
      .then((r) => r.json())
      .then(setAnomaly)
      .catch(() => {})
  }, [])

  if (!anomaly) return null

  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.3 }}
      className="font-mono border cursor-pointer select-none"
      style={{
        borderColor: `${anomaly.difficulty_color}30`,
        background: '#030A03',
        boxShadow: `0 0 20px ${anomaly.difficulty_color}0C`,
      }}
      onClick={() => setExpanded((v) => !v)}
    >
      {/* Top bar */}
      <div
        className="h-0.5 w-full"
        style={{ background: `linear-gradient(90deg, ${anomaly.difficulty_color}, transparent)` }}
      />

      <div className="px-4 py-3 flex items-start gap-3">
        {/* Glyph */}
        <motion.div
          className="shrink-0 w-9 h-9 flex items-center justify-center text-lg border"
          style={{ borderColor: `${anomaly.difficulty_color}25`, background: `${anomaly.difficulty_color}08` }}
          animate={{ opacity: [0.7, 1, 0.7] }}
          transition={{ duration: 2.2, repeat: Infinity }}
        >
          {anomaly.glyph}
        </motion.div>

        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-0.5">
            <span className="text-[7px] tracking-[0.5em]" style={{ color: `${anomaly.difficulty_color}50` }}>
              ANOMALÍA DEL DÍA
            </span>
            <span
              className="text-[7px] tracking-widest px-1 border"
              style={{ color: anomaly.difficulty_color, borderColor: `${anomaly.difficulty_color}30` }}
            >
              {anomaly.difficulty}
            </span>
          </div>

          <div className="text-[11px] font-black tracking-wider" style={{ color: anomaly.difficulty_color }}>
            {anomaly.title}
          </div>

          {expanded && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              className="text-[9px] leading-relaxed mt-1.5 text-[#C0FFC0]/60"
            >
              {anomaly.description}
            </motion.div>
          )}
        </div>

        <div className="shrink-0 text-right">
          <div className="text-[8px] font-bold" style={{ color: `${anomaly.difficulty_color}70` }}>
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
