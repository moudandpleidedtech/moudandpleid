'use client'

/**
 * MilestoneModal — Celebración de momento héroe en el journey del Operador
 *
 * Aparece cuando el operador alcanza un hito significativo del aprendizaje.
 * Distinto del SecretMissionReveal (logros secretos) — este celebra
 * el progreso real del camino hacia el expertise en Python.
 * Auto-dismiss 7s. Click en CONTINUAR para cerrar.
 */

import { useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import type { MilestoneUnlock } from '@/hooks/useMilestones'

interface Props {
  milestone: MilestoneUnlock | null
  onClose: () => void
}

export default function MilestoneModal({ milestone, onClose }: Props) {
  useEffect(() => {
    if (!milestone) return
    const t = setTimeout(onClose, 7000)
    return () => clearTimeout(t)
  }, [milestone, onClose])

  return (
    <AnimatePresence>
      {milestone && (
        <motion.div
          className="fixed inset-0 z-[280] flex items-end justify-center pb-10"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={onClose}
        >
          <motion.div
            initial={{ y: 60, opacity: 0, scale: 0.92 }}
            animate={{ y: 0,  opacity: 1, scale: 1 }}
            exit={{ y: 40, opacity: 0 }}
            transition={{ type: 'spring', stiffness: 300, damping: 26 }}
            className="w-full max-w-sm mx-4 font-mono overflow-hidden"
            onClick={e => e.stopPropagation()}
            style={{
              background:  '#030A03',
              border:      '1px solid rgba(0,255,65,0.30)',
              boxShadow:   '0 0 40px rgba(0,255,65,0.10), 0 -4px 20px rgba(0,255,65,0.05)',
            }}
          >
            <div className="h-px" style={{ background: 'linear-gradient(90deg, transparent, #00FF41, transparent)' }} />

            <div className="px-5 py-4 flex gap-4">
              {/* Icon */}
              <motion.div
                className="shrink-0 w-11 h-11 flex items-center justify-center text-2xl border border-[#00FF41]/20"
                style={{ background: 'rgba(0,255,65,0.06)', color: '#00FF41' }}
                animate={{ opacity: [0.7, 1, 0.7] }}
                transition={{ duration: 2.5, repeat: Infinity }}
              >
                {milestone.icon}
              </motion.div>

              <div className="flex-1 min-w-0">
                <p className="text-[7px] tracking-[0.6em] text-[#00FF41]/35 mb-0.5">
                  // HITO DESBLOQUEADO
                </p>
                <p className="text-[11px] font-black tracking-wider text-[#00FF41] mb-1.5"
                  style={{ textShadow: '0 0 10px rgba(0,255,65,0.35)' }}>
                  {milestone.title}
                </p>
                <p className="text-[9px] leading-relaxed text-[#00FF41]/55">
                  {milestone.message}
                </p>
              </div>
            </div>

            <div className="px-5 pb-4 flex justify-end">
              <button
                onClick={onClose}
                className="text-[8px] tracking-[0.4em] text-[#00FF41]/30 hover:text-[#00FF41]/70 transition-colors"
              >
                [ CONTINUAR ] →
              </button>
            </div>

            <div className="h-px" style={{ background: 'linear-gradient(90deg, transparent, rgba(0,255,65,0.4), transparent)' }} />
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}
