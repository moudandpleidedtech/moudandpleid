'use client'

/**
 * SecretMissionRevealModal — Revelación dramática de Misión Secreta (F8)
 * Se muestra cuando el operador desbloquea una misión secreta por comportamiento de élite.
 * Auto-dismiss a los 6s o al hacer click en CONFIRMAR.
 */

import { useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

interface Props {
  visible: boolean
  missionName: string
  description: string
  onClose: () => void
}

export default function SecretMissionRevealModal({ visible, missionName, description, onClose }: Props) {
  useEffect(() => {
    if (!visible) return
    const t = setTimeout(onClose, 6000)
    return () => clearTimeout(t)
  }, [visible, onClose])

  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          className="fixed inset-0 z-[300] flex items-center justify-center"
          style={{ background: 'rgba(0,0,0,0.93)' }}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={onClose}
        >
          {/* Scanlines overlay */}
          <div
            className="absolute inset-0 pointer-events-none"
            style={{
              backgroundImage: 'repeating-linear-gradient(0deg,transparent,transparent 3px,rgba(255,215,0,0.015) 3px,rgba(255,215,0,0.015) 4px)',
            }}
          />

          <motion.div
            initial={{ scale: 0.78, opacity: 0, y: 32 }}
            animate={{ scale: 1, opacity: 1, y: 0 }}
            exit={{ scale: 0.90, opacity: 0 }}
            transition={{ type: 'spring', stiffness: 260, damping: 22 }}
            className="relative w-full max-w-sm mx-4 font-mono text-center overflow-hidden"
            onClick={e => e.stopPropagation()}
            style={{
              background: '#08060A',
              border: '1px solid rgba(255,215,0,0.35)',
              boxShadow: '0 0 60px rgba(255,215,0,0.12), 0 0 120px rgba(255,215,0,0.05), inset 0 0 40px rgba(255,215,0,0.03)',
            }}
          >
            {/* Top accent */}
            <div className="h-px w-full" style={{ background: 'linear-gradient(90deg, transparent, #FFD700, transparent)' }} />

            <div className="px-7 pt-8 pb-7">
              {/* Classification header */}
              <p className="text-[7px] tracking-[0.7em] mb-7" style={{ color: 'rgba(255,215,0,0.35)' }}>
                // ARCHIVO CLASIFICADO DESBLOQUEADO
              </p>

              {/* Pulsing star */}
              <motion.div
                animate={{ scale: [1, 1.18, 1], opacity: [0.75, 1, 0.75] }}
                transition={{ duration: 2.4, repeat: Infinity, ease: 'easeInOut' }}
                className="text-5xl mb-6 select-none"
                style={{ filter: 'drop-shadow(0 0 24px rgba(255,215,0,0.55))' }}
              >
                ★
              </motion.div>

              {/* Mission name */}
              <motion.h2
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.15 }}
                className="text-base font-black tracking-[0.18em] mb-3 uppercase"
                style={{ color: '#FFD700', textShadow: '0 0 24px rgba(255,215,0,0.45)' }}
              >
                {missionName}
              </motion.h2>

              {/* Description */}
              <motion.p
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.28 }}
                className="text-[10px] leading-relaxed mb-7"
                style={{ color: 'rgba(255,215,0,0.50)' }}
              >
                {description}
              </motion.p>

              {/* Rarity badge */}
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.4 }}
                className="inline-block text-[7px] tracking-[0.5em] px-3 py-1 mb-7 border"
                style={{ borderColor: 'rgba(255,215,0,0.25)', color: 'rgba(255,215,0,0.50)' }}
              >
                CLASIFICACIÓN: LEGENDARIO
              </motion.div>

              {/* Confirm button */}
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.5 }}
              >
                <button
                  onClick={onClose}
                  className="text-[9px] tracking-[0.45em] px-4 py-2 border transition-all duration-150"
                  style={{ borderColor: 'rgba(255,215,0,0.25)', color: 'rgba(255,215,0,0.40)' }}
                  onMouseEnter={e => {
                    e.currentTarget.style.color = '#FFD700'
                    e.currentTarget.style.borderColor = 'rgba(255,215,0,0.60)'
                    e.currentTarget.style.boxShadow = '0 0 12px rgba(255,215,0,0.15)'
                  }}
                  onMouseLeave={e => {
                    e.currentTarget.style.color = 'rgba(255,215,0,0.40)'
                    e.currentTarget.style.borderColor = 'rgba(255,215,0,0.25)'
                    e.currentTarget.style.boxShadow = 'none'
                  }}
                >
                  [ CONFIRMAR RECIBO ]
                </button>
              </motion.div>
            </div>

            {/* Bottom accent */}
            <div className="h-px w-full" style={{ background: 'linear-gradient(90deg, transparent, #FFD700, transparent)' }} />
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}
