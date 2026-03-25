'use client'

/**
 * AchievementToast — Notificación de logro desbloqueado
 * Aparece en la esquina superior derecha, se apila si hay varios,
 * desaparece sola a los 5 segundos.
 */

import { useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

export interface Achievement {
  id: string
  name: string
  description: string
  icon: string
  xp_bonus: number
  rarity: string
  unlocked_at: string
}

const RARITY_COLORS: Record<string, string> = {
  common:    '#00FF41',
  uncommon:  '#00B4D8',
  rare:      '#9B5DE5',
  epic:      '#FFB800',
  legendary: '#FF4444',
}

interface Props {
  achievements: Achievement[]
  onDismiss: (id: string) => void
}

export default function AchievementToast({ achievements, onDismiss }: Props) {
  useEffect(() => {
    if (achievements.length === 0) return
    const timers = achievements.map((a) =>
      setTimeout(() => onDismiss(a.id), 5000)
    )
    return () => timers.forEach(clearTimeout)
  }, [achievements, onDismiss])

  return (
    <div className="fixed top-4 right-4 z-[500] flex flex-col gap-2 pointer-events-none">
      <AnimatePresence>
        {achievements.map((a) => {
          const color = RARITY_COLORS[a.rarity] ?? '#00FF41'
          return (
            <motion.div
              key={a.id}
              initial={{ opacity: 0, x: 80, scale: 0.9 }}
              animate={{ opacity: 1, x: 0, scale: 1 }}
              exit={{ opacity: 0, x: 80, scale: 0.9 }}
              transition={{ type: 'spring', stiffness: 320, damping: 28 }}
              className="pointer-events-auto w-72 border font-mono overflow-hidden"
              style={{
                borderColor: `${color}50`,
                background: '#050A05',
                boxShadow: `0 0 30px ${color}20`,
              }}
            >
              {/* Barra de rareza en la parte superior */}
              <div className="h-0.5 w-full" style={{ background: color }} />

              <div className="px-4 py-3 flex items-start gap-3">
                {/* Icono */}
                <div
                  className="shrink-0 w-10 h-10 flex items-center justify-center text-xl border"
                  style={{ borderColor: `${color}30`, background: `${color}10` }}
                >
                  {a.icon}
                </div>

                <div className="flex-1 min-w-0">
                  {/* Label */}
                  <div className="text-[8px] tracking-[0.5em] mb-0.5" style={{ color: `${color}60` }}>
                    LOGRO DESBLOQUEADO
                  </div>
                  {/* Nombre */}
                  <div className="text-[11px] font-black tracking-wider" style={{ color }}>
                    {a.name}
                  </div>
                  {/* Descripción */}
                  <div className="text-[9px] text-[#C0C0C0]/50 leading-4 mt-0.5 truncate">
                    {a.description}
                  </div>
                  {/* XP bonus */}
                  <div className="text-[9px] mt-1 font-bold" style={{ color: `${color}80` }}>
                    +{a.xp_bonus} XP
                  </div>
                </div>

                {/* Dismiss */}
                <button
                  onClick={() => onDismiss(a.id)}
                  className="shrink-0 text-[10px] mt-0.5"
                  style={{ color: `${color}30` }}
                >
                  ×
                </button>
              </div>
            </motion.div>
          )
        })}
      </AnimatePresence>
    </div>
  )
}
