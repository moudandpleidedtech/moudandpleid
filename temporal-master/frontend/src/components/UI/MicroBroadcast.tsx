'use client'

/**
 * MicroBroadcast — Micro-transmisiones de DAKI
 * Aparece en la esquina inferior izquierda del IDE.
 * Muestra un tip táctico de Python de 1-2 líneas durante 6 segundos.
 * Variable reward: mensaje aleatorio del banco, con cooldown para no repetirse.
 */

import { motion, AnimatePresence } from 'framer-motion'

interface Props {
  message: string | null
  onDismiss: () => void
}

export default function MicroBroadcast({ message, onDismiss }: Props) {
  return (
    <AnimatePresence>
      {message && (
        <motion.div
          key={message}
          initial={{ opacity: 0, y: 16, x: -8 }}
          animate={{ opacity: 1, y: 0, x: 0 }}
          exit={{ opacity: 0, y: 8 }}
          transition={{ type: 'spring', stiffness: 260, damping: 22 }}
          className="fixed bottom-20 left-4 z-50 max-w-xs font-mono pointer-events-auto"
          style={{
            background: 'rgba(0,8,0,0.92)',
            border: '1px solid #00FF4130',
            boxShadow: '0 0 18px #00FF4115',
          }}
        >
          {/* Header bar */}
          <div
            className="flex items-center gap-2 px-3 py-1.5 border-b"
            style={{ borderColor: '#00FF4118' }}
          >
            <motion.span
              className="text-[#00FF41] text-[10px]"
              animate={{ opacity: [0.4, 1, 0.4] }}
              transition={{ duration: 1.4, repeat: Infinity }}
            >
              ◈
            </motion.span>
            <span className="text-[8px] tracking-[0.4em] text-[#00FF41]/50">
              MICRO-TRANSMISIÓN DAKI
            </span>
            <button
              onClick={onDismiss}
              className="ml-auto text-[#00FF41]/30 hover:text-[#00FF41]/70 text-xs leading-none"
            >
              ×
            </button>
          </div>

          {/* Message */}
          <div className="px-3 py-2">
            <p className="text-[10px] leading-relaxed text-[#C0FFC0]/70">
              {message}
            </p>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}
