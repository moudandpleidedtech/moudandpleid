'use client'

/**
 * ParticleBurst — ráfaga de partículas verde neón al pasar un nivel.
 * Se renderiza en `position: fixed` sobre toda la pantalla.
 * Las partículas emergen desde el área del botón EJECUTAR (inferior-derecha)
 * y vuelan hacia la barra de XP en el header (superior-derecha).
 */
import { useMemo } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

interface Particle {
  id: number
  startX: number    // % from left
  startY: number    // % from top
  endX: number
  endY: number
  size: number
  duration: number
  delay: number
  color: string
}

const NEON_PALETTE = [
  '#00FF41', '#00FF41', '#00FF41',   // predomina el verde neón
  '#39FF14', '#7FFF00', '#00CC33',
]

interface Props {
  visible: boolean
}

export default function ParticleBurst({ visible }: Props) {
  // Partículas deterministas (sin Math.random() en render para evitar hydration)
  const particles = useMemo<Particle[]>(() => {
    const N = 28
    return Array.from({ length: N }, (_, i) => {
      // Origen: zona del botón EJECUTAR (~83% derecha, ~10% top del panel editor)
      const spreadX = ((i * 7) % 16) - 8          // -8 a +8 vw
      const spreadY = ((i * 11) % 12) - 6          // -6 a +6 vh
      return {
        id: i,
        startX: 80 + (i % 6) - 3,                 // ~77–83 vw
        startY: 8 + (i % 4),                       // ~8–11 vh
        endX: 75 + spreadX + ((i * 3) % 20) - 10, // dispersa hacia arriba
        endY: 1 + ((i * 5) % 5),                   // ~1–5 vh (header XP)
        size: 3 + (i % 4),
        duration: 0.7 + (i % 5) * 0.08,
        delay: (i % 8) * 0.045,
        color: NEON_PALETTE[i % NEON_PALETTE.length],
      }
    })
  }, [])

  return (
    <AnimatePresence>
      {visible && (
        <div className="fixed inset-0 pointer-events-none overflow-hidden" style={{ zIndex: 60 }}>
          {particles.map((p) => (
            <motion.div
              key={p.id}
              className="absolute rounded-full"
              style={{
                width: p.size,
                height: p.size,
                background: p.color,
                boxShadow: `0 0 ${p.size * 2}px ${p.color}, 0 0 ${p.size * 4}px ${p.color}60`,
                left: `${p.startX}vw`,
                top: `${p.startY}vh`,
              }}
              initial={{ opacity: 1, scale: 1, x: 0, y: 0 }}
              animate={{
                opacity: [1, 1, 0.6, 0],
                scale: [1, 1.4, 0.6],
                x: `${(p.endX - p.startX)}vw`,
                y: `${(p.endY - p.startY)}vh`,
              }}
              exit={{ opacity: 0 }}
              transition={{
                duration: p.duration,
                delay: p.delay,
                ease: 'easeOut',
              }}
            />
          ))}
          {/* Flash de destello en el área del botón */}
          <motion.div
            className="absolute rounded"
            style={{
              left: '74vw', top: '5vh',
              width: '14vw', height: '4vh',
              background: 'radial-gradient(ellipse at center, #00FF4130 0%, transparent 70%)',
            }}
            initial={{ opacity: 0 }}
            animate={{ opacity: [0, 1, 0] }}
            transition={{ duration: 0.4 }}
          />
        </div>
      )}
    </AnimatePresence>
  )
}
