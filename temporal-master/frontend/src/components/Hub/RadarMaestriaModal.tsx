'use client'

/**
 * RadarMaestriaModal — Spider chart de maestría conceptual del Operador
 * Llama a GET /api/v1/intel/mastery-radar y renderiza SVG puro (sin librerías).
 */

import { useEffect, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? ''

interface Axis {
  category: string
  score: number
  count: number
  needs_reinforcement: boolean
}

interface RadarData {
  axes: Axis[]
  total_concepts: number
  total_mastered: number
  total_reinforcement_needed: number
}

interface Props {
  userId: string
  onClose: () => void
}

// ── SVG Radar Chart ────────────────────────────────────────────────────────────

const CX = 240
const CY = 220
const MAX_R = 110
const RINGS = [25, 50, 75, 100]
const RING_LABELS = ['25', '50', '75', '100']

function polarToXY(angleDeg: number, radius: number): [number, number] {
  const rad = ((angleDeg - 90) * Math.PI) / 180
  return [CX + radius * Math.cos(rad), CY + radius * Math.sin(rad)]
}

function RadarSVG({ axes }: { axes: Axis[] }) {
  const n = axes.length
  if (n === 0) return null

  const angles = axes.map((_, i) => (i * 360) / n)

  // Polígono de datos
  const dataPoints = axes.map((a, i) => {
    const r = (a.score / 100) * MAX_R
    return polarToXY(angles[i], r)
  })
  const dataPath = dataPoints.map((p, i) => `${i === 0 ? 'M' : 'L'} ${p[0].toFixed(1)} ${p[1].toFixed(1)}`).join(' ') + ' Z'

  // Polígono de anillos (para cada nivel 25/50/75/100)
  function ringPath(pct: number): string {
    const r = (pct / 100) * MAX_R
    const pts = angles.map(a => polarToXY(a, r))
    return pts.map((p, i) => `${i === 0 ? 'M' : 'L'} ${p[0].toFixed(1)} ${p[1].toFixed(1)}`).join(' ') + ' Z'
  }

  return (
    <svg width="100%" height="auto" viewBox="0 0 480 440" className="mx-auto overflow-visible" style={{ maxWidth: '480px' }}>
      {/* Anillos de referencia */}
      {RINGS.map((r, i) => (
        <path
          key={r}
          d={ringPath(r)}
          fill="none"
          stroke="rgba(0,255,65,0.08)"
          strokeWidth="1"
        />
      ))}

      {/* Etiquetas de anillos */}
      {RING_LABELS.map((label, i) => (
        <text
          key={label}
          x={CX + 3}
          y={CY - ((RINGS[i] / 100) * MAX_R) + 4}
          fill="rgba(0,255,65,0.40)"
          fontSize="9"
          fontFamily="monospace"
        >
          {label}
        </text>
      ))}

      {/* Ejes */}
      {axes.map((_, i) => {
        const [x, y] = polarToXY(angles[i], MAX_R)
        return (
          <line
            key={i}
            x1={CX} y1={CY}
            x2={x.toFixed(1)} y2={y.toFixed(1)}
            stroke="rgba(0,255,65,0.10)"
            strokeWidth="1"
          />
        )
      })}

      {/* Área de datos */}
      <path
        d={dataPath}
        fill="rgba(0,255,65,0.12)"
        stroke="rgba(0,255,65,0.60)"
        strokeWidth="1.5"
      />

      {/* Puntos de datos */}
      {dataPoints.map(([x, y], i) => (
        <circle
          key={i}
          cx={x.toFixed(1)}
          cy={y.toFixed(1)}
          r="3"
          fill={axes[i].needs_reinforcement ? '#FFB800' : '#00FF41'}
          style={{ filter: `drop-shadow(0 0 4px ${axes[i].needs_reinforcement ? '#FFB800' : '#00FF41'})` }}
        />
      ))}

      {/* Etiquetas de categorías */}
      {axes.map((a, i) => {
        const [x, y] = polarToXY(angles[i], MAX_R + 25)
        const anchor = x < CX - 5 ? 'end' : x > CX + 5 ? 'start' : 'middle'
        return (
          <text
            key={a.category}
            x={x.toFixed(1)}
            y={y.toFixed(1)}
            textAnchor={anchor}
            dominantBaseline="middle"
            fill={a.needs_reinforcement ? '#FFB800' : '#00FF41'}
            fontSize="12"
            fontFamily="monospace"
            fontWeight="bold"
            letterSpacing="0.05em"
            style={{ textShadow: '0 0 4px rgba(0,0,0,1), 0 0 8px rgba(0,0,0,1)' }}
          >
            {a.category.toUpperCase()}
          </text>
        )
      })}
    </svg>
  )
}

// ── Modal ──────────────────────────────────────────────────────────────────────

export default function RadarMaestriaModal({ userId, onClose }: Props) {
  const [data, setData]       = useState<RadarData | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!userId) return
    fetch(`${API_BASE}/api/v1/intel/mastery-radar?user_id=${userId}`)
      .then(r => r.ok ? r.json() : null)
      .then((d: RadarData | null) => { if (d) setData(d) })
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [userId])

  return (
    <AnimatePresence>
      <>
        <motion.div
          className="fixed inset-0 z-[90] bg-black/80"
          initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
          onClick={onClose}
        />
        <motion.div
          className="fixed inset-0 z-[91] flex items-center justify-center p-4"
          initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
        >
          <motion.div
            className="relative w-full max-w-lg font-mono overflow-hidden"
            style={{ background: '#020617', border: '1px solid rgba(6,182,212,0.40)', boxShadow: '0 0 0 1px rgba(6,182,212,0.18), 0 0 40px rgba(6,182,212,0.12)' }}
            initial={{ scale: 0.90, y: 20 }} animate={{ scale: 1, y: 0 }}
            exit={{ scale: 0.92, opacity: 0 }}
            transition={{ type: 'spring', stiffness: 320, damping: 28 }}
          >
            {/* Scanlines */}
            <div className="absolute inset-0 pointer-events-none opacity-[0.02]"
              style={{ backgroundImage: 'repeating-linear-gradient(0deg,transparent,transparent 3px,#00FF41 3px,#00FF41 4px)' }}
            />

            {/* Header */}
            <div className="flex items-center justify-between px-5 py-4 border-b border-[rgba(6,182,212,0.12)]">
              <div>
                <p className="text-[9px] tracking-[0.5em] uppercase mb-0.5" style={{ color: 'rgba(74,222,128,0.50)' }}>
                  {'// INTEL OPERACIONAL'}
                </p>
                <h2 className="text-sm font-black tracking-[0.2em]" style={{ color: 'rgba(6,182,212,0.90)', textShadow: '0 0 10px rgba(6,182,212,0.40)' }}>
                  RADAR DE MAESTRÍA
                </h2>
              </div>
              <button
                onClick={onClose}
                className="text-xs tracking-widest transition-colors"
                style={{ color: 'rgba(6,182,212,0.30)' }}
                onMouseEnter={e => (e.currentTarget.style.color = 'rgba(6,182,212,0.70)')}
                onMouseLeave={e => (e.currentTarget.style.color = 'rgba(6,182,212,0.30)')}
              >
                [ ESC ]
              </button>
            </div>

            {/* Body */}
            <div className="px-5 py-5">
              {loading ? (
                <div className="text-center py-12">
                  <p className="text-[10px] tracking-[0.4em] text-[#00FF41]/30 animate-pulse">
                    CARGANDO DATOS DE MAESTRÍA...
                  </p>
                </div>
              ) : !data || data.total_concepts === 0 ? (
                <div className="text-center py-12">
                  <p className="text-[10px] tracking-[0.4em] text-[#00FF41]/30">
                    SIN DATOS AÚN — COMPLETA MISIONES PARA ACTIVAR EL RADAR
                  </p>
                </div>
              ) : (
                <>
                  <RadarSVG axes={data.axes} />

                  {/* Stats strip */}
                  <div className="grid grid-cols-3 gap-2 mt-4">
                    {[
                      { n: data.total_concepts,            label: 'CONCEPTOS' },
                      { n: data.total_mastered,            label: 'DOMINADOS' },
                      { n: data.total_reinforcement_needed, label: 'REFUERZO' },
                    ].map(({ n, label }) => (
                      <div key={label} className="border border-[#00FF41]/10 p-2 text-center">
                        <p className="text-lg font-black text-[#00FF41]"
                          style={{ textShadow: '0 0 8px rgba(0,255,65,0.3)' }}>{n}</p>
                        <p className="text-[7px] tracking-[0.3em] text-[#00FF41]/25 mt-0.5">{label}</p>
                      </div>
                    ))}
                  </div>

                  {/* Leyenda */}
                  <div className="flex items-center gap-4 mt-3 justify-center">
                    <div className="flex items-center gap-1.5">
                      <div className="w-2 h-2 rounded-full bg-[#00FF41]" />
                      <span className="text-[8px] tracking-wider text-[#00FF41]/40">DOMINADO (≥40)</span>
                    </div>
                    <div className="flex items-center gap-1.5">
                      <div className="w-2 h-2 rounded-full bg-[#FFB800]" />
                      <span className="text-[8px] tracking-wider text-[#FFB800]/50">REFUERZO PENDIENTE</span>
                    </div>
                  </div>
                </>
              )}
            </div>
          </motion.div>
        </motion.div>
      </>
    </AnimatePresence>
  )
}
