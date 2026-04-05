'use client'

/**
 * DistincionesPanel — Panel de logros desbloqueados en el Hub.
 * Muestra las últimas distinciones ganadas y el contador total.
 * Datos: GET /api/v1/achievements?user_id=<uuid>
 */

import { useEffect, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

interface Achievement {
  id: string
  name: string
  description: string
  icon: string
  xp_bonus: number
  rarity: string
  unlocked: boolean
  unlocked_at: string | null
}

const RARITY_COLORS: Record<string, string> = {
  common:    '#00FF41',
  uncommon:  '#00B4D8',
  rare:      '#9B5DE5',
  epic:      '#FFB800',
  legendary: '#FF4444',
}

const RARITY_LABEL: Record<string, string> = {
  common:    'COMÚN',
  uncommon:  'POCO COMÚN',
  rare:      'RARO',
  epic:      'ÉPICO',
  legendary: 'LEGENDARIO',
}

interface Props {
  userId: string
}

export default function DistincionesPanel({ userId }: Props) {
  const [unlocked,  setUnlocked]  = useState<Achievement[]>([])
  const [total,     setTotal]     = useState(0)
  const [expanded,  setExpanded]  = useState(false)
  const [loading,   setLoading]   = useState(true)

  useEffect(() => {
    if (!userId) return
    const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? ''
    fetch(`${API_BASE}/api/v1/achievements?user_id=${userId}`)
      .then(r => r.ok ? r.json() : null)
      .then((data: { unlocked_count: number; total_count: number; achievements: Achievement[] } | null) => {
        if (!data) return
        const earned = data.achievements
          .filter(a => a.unlocked && a.unlocked_at)
          .sort((a, b) => new Date(b.unlocked_at!).getTime() - new Date(a.unlocked_at!).getTime())
        setUnlocked(earned)
        setTotal(data.total_count)
      })
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [userId])

  const preview = unlocked.slice(0, 3)
  const hasAny  = unlocked.length > 0

  return (
    <div className="w-full font-mono">
      {/* ── Cabecera ── */}
      <button
        onClick={() => setExpanded(v => !v)}
        className="w-full flex items-center justify-between px-3 py-2 border transition-all duration-200 border-neon"
      >
        <div className="flex items-center gap-2">
          <span className="text-[9px] tracking-[0.4em] uppercase font-bold" style={{ color: 'rgba(74,222,128,0.65)' }}>
            Distinciones
          </span>
          {!loading && (
            <span
              className="text-[8px] px-1.5 py-0.5 border tracking-wider"
              style={{
                borderColor: hasAny ? 'rgba(74,222,128,0.40)' : 'rgba(74,222,128,0.15)',
                color:       hasAny ? 'rgba(74,222,128,0.80)' : 'rgba(74,222,128,0.30)',
              }}
            >
              {unlocked.length}/{total}
            </span>
          )}
        </div>
        <motion.span
          className="text-[#00FF41]/25 text-[10px]"
          animate={{ rotate: expanded ? 90 : 0 }}
          transition={{ duration: 0.2 }}
        >
          ▶
        </motion.span>
      </button>

      {/* ── Contenido ── */}
      <AnimatePresence>
        {!expanded ? (
          /* Vista compacta: últimas 3 medallas en fila de iconos */
          hasAny && !loading ? (
            <motion.div
              key="compact"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="flex items-center gap-1.5 px-3 py-2"
            >
              {preview.map(a => {
                const color = RARITY_COLORS[a.rarity] ?? '#00FF41'
                return (
                  <div
                    key={a.id}
                    title={`${a.name} — ${a.description}`}
                    className="w-7 h-7 flex items-center justify-center text-base border shrink-0"
                    style={{
                      borderColor: `${color}30`,
                      background:  `${color}08`,
                      boxShadow:   `0 0 6px ${color}18`,
                    }}
                  >
                    {a.icon}
                  </div>
                )
              })}
              {unlocked.length > 3 && (
                <span className="text-[9px] text-[#00FF41]/30 tracking-widest ml-1">
                  +{unlocked.length - 3}
                </span>
              )}
            </motion.div>
          ) : null
        ) : (
          /* Vista expandida: lista completa */
          <motion.div
            key="full"
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.22 }}
            className="overflow-hidden"
          >
            {loading ? (
              <div className="px-3 py-3 text-[9px] text-[#00FF41]/25 tracking-widest">
                Cargando...
              </div>
            ) : !hasAny ? (
              <div className="px-3 py-3 text-[9px] text-[#00FF41]/20 tracking-widest leading-relaxed">
                Completa misiones para desbloquear distinciones.
              </div>
            ) : (
              <div className="max-h-72 overflow-y-auto">
                {unlocked.map((a, idx) => {
                  const color = RARITY_COLORS[a.rarity] ?? '#00FF41'
                  const date  = a.unlocked_at
                    ? new Date(a.unlocked_at).toLocaleDateString('es', { day: '2-digit', month: 'short' })
                    : ''
                  return (
                    <motion.div
                      key={a.id}
                      initial={{ opacity: 0, x: -8 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: idx * 0.04 }}
                      className="flex items-center gap-2.5 px-3 py-2 border-b border-[#00FF41]/06
                                 hover:bg-[#00FF41]/03 transition-colors duration-150"
                    >
                      {/* Icono */}
                      <div
                        className="shrink-0 w-8 h-8 flex items-center justify-center text-sm border"
                        style={{ borderColor: `${color}25`, background: `${color}08` }}
                      >
                        {a.icon}
                      </div>

                      {/* Texto */}
                      <div className="flex-1 min-w-0">
                        <div className="text-[10px] font-bold tracking-wide truncate" style={{ color }}>
                          {a.name}
                        </div>
                        <div className="text-[8px] text-[#C0C0C0]/35 leading-3 truncate mt-0.5">
                          {a.description}
                        </div>
                        <div className="text-[7px] tracking-widest mt-0.5" style={{ color: `${color}40` }}>
                          {RARITY_LABEL[a.rarity] ?? a.rarity} · +{a.xp_bonus} XP
                        </div>
                      </div>

                      {/* Fecha */}
                      {date && (
                        <span className="text-[7px] text-[#00FF41]/20 tracking-widest shrink-0">
                          {date}
                        </span>
                      )}
                    </motion.div>
                  )
                })}
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
