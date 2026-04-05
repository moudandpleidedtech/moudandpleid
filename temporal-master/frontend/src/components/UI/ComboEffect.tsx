'use client'

/**
 * ComboEffect — overlay "¡COMBO DE EFICIENCIA x2!" que aparece cuando
 * el jugador resuelve un nivel usando menos líneas que el Par.
 *
 * Props:
 *   visible   — activa/desactiva la animación
 *   xpEarned  — XP base ganado (se muestra x2)
 *   onDone    — callback cuando la animación termina
 */
import { useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

interface Props {
  visible: boolean
  xpEarned: number
  multiplier?: number  // F5: multiplicador por racha sin pistas (cosmético)
  onDone?: () => void
}

export default function ComboEffect({ visible, xpEarned, multiplier = 2, onDone }: Props) {
  useEffect(() => {
    if (!visible) return
    const t = setTimeout(() => onDone?.(), 2600)
    return () => clearTimeout(t)
  }, [visible, onDone])

  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          className="fixed inset-0 flex items-center justify-center pointer-events-none"
          style={{ zIndex: 55 }}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.2 }}
        >
          {/* Fondo sutil */}
          <div className="absolute inset-0 bg-black/30" />

          {/* Contenido */}
          <motion.div
            className="relative z-10 text-center select-none px-8 py-6"
            initial={{ scale: 0.3, y: 60, opacity: 0 }}
            animate={{ scale: [0.3, 1.12, 1], y: [60, -8, 0], opacity: 1 }}
            exit={{ scale: 1.2, opacity: 0, y: -20 }}
            transition={{ type: 'spring', stiffness: 320, damping: 20, duration: 0.5 }}
          >
            {/* Línea principal */}
            <motion.div
              className="font-mono font-black tracking-[0.12em] leading-none select-none"
              style={{
                fontSize: 'clamp(2rem, 6vw, 3.5rem)',
                color: '#FFD700',
                textShadow: '0 0 20px #FFD700, 0 0 50px #FFD70080, 0 0 80px #FFD70040',
              }}
              animate={{
                textShadow: [
                  '0 0 20px #FFD700, 0 0 50px #FFD70080',
                  '0 0 40px #FFD700, 0 0 90px #FFD700',
                  '0 0 20px #FFD700, 0 0 50px #FFD70080',
                ],
              }}
              transition={{ duration: 0.8, repeat: Infinity }}
            >
              ¡COMBO DE EFICIENCIA!
            </motion.div>

            {/* Multiplicador */}
            <motion.div
              className="mt-2 font-mono font-black tracking-[0.2em]"
              style={{
                fontSize: 'clamp(1.5rem, 4vw, 2.5rem)',
                color: '#00FF41',
                textShadow: '0 0 16px #00FF41, 0 0 40px #00FF4160',
              }}
              initial={{ opacity: 0, scale: 0.5 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.18, type: 'spring', stiffness: 400 }}
            >
              x{multiplier % 1 === 0 ? multiplier : multiplier.toFixed(1)} XP
            </motion.div>

            {/* XP ganado */}
            {xpEarned > 0 && (
              <motion.div
                className="mt-3 font-mono text-lg tracking-widest"
                style={{ color: '#FFD700CC' }}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.32 }}
              >
                +{xpEarned} XP base · EFICIENCIA DETECTADA
              </motion.div>
            )}

            {/* Decoración de esquinas */}
            {['top-0 left-0 border-t border-l', 'top-0 right-0 border-t border-r',
              'bottom-0 left-0 border-b border-l', 'bottom-0 right-0 border-b border-r'].map((cls, i) => (
              <motion.div
                key={i}
                className={`absolute w-6 h-6 ${cls} border-yellow-400/60`}
                animate={{ opacity: [0.4, 1, 0.4] }}
                transition={{ duration: 1, repeat: Infinity, delay: i * 0.1 }}
              />
            ))}
          </motion.div>

          {/* Escanlines de efecto retro */}
          <div
            className="absolute inset-0 pointer-events-none opacity-10"
            style={{
              background: 'repeating-linear-gradient(0deg, transparent 0px, transparent 3px, #FFD70010 3px, #FFD70010 4px)',
            }}
          />
        </motion.div>
      )}
    </AnimatePresence>
  )
}
