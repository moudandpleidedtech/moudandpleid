'use client'

/**
 * InsightFlash — Tarjeta post-nivel
 * Aparece 800ms después de completar un nivel.
 * Conecta lo que el usuario acaba de codear con el mundo real.
 * Se cierra sola a los 8s o al hacer click.
 */

import { useEffect } from 'react'
import { motion } from 'framer-motion'

interface Props {
  insight: string
  onClose: () => void
}

export default function InsightFlash({ insight, onClose }: Props) {
  useEffect(() => {
    const t = setTimeout(onClose, 8000)
    return () => clearTimeout(t)
  }, [onClose])

  return (
    <motion.div
      className="fixed bottom-6 left-1/2 z-[400] w-full max-w-lg -translate-x-1/2 font-mono"
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 30 }}
      transition={{ type: 'spring', stiffness: 260, damping: 24 }}
    >
      <div
        className="border px-5 py-4 relative overflow-hidden"
        style={{
          borderColor: 'rgba(0,255,65,0.25)',
          background: '#050A05',
          boxShadow: '0 0 40px rgba(0,255,65,0.08)',
        }}
      >
        {/* Línea superior decorativa */}
        <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-[#00FF41]/40 to-transparent" />

        <div className="flex items-start gap-4">
          {/* Icono DAKI */}
          <div className="shrink-0 text-2xl mt-0.5">⚡</div>

          <div className="flex-1">
            <div className="text-[8px] tracking-[0.5em] text-[#00FF41]/30 mb-1.5 uppercase">
              DAKI // Conexión con el mundo real
            </div>
            <p className="text-[11px] text-[#C0C0C0]/70 leading-5">
              {insight}
            </p>
          </div>

          <button
            onClick={onClose}
            className="shrink-0 text-xs text-[#00FF41]/20 hover:text-[#00FF41]/50 transition-colors mt-0.5"
          >
            ×
          </button>
        </div>

        {/* Barra de progreso de tiempo */}
        <motion.div
          className="absolute bottom-0 left-0 h-px bg-[#00FF41]/20"
          initial={{ width: '100%' }}
          animate={{ width: '0%' }}
          transition={{ duration: 8, ease: 'linear' }}
        />
      </div>
    </motion.div>
  )
}
