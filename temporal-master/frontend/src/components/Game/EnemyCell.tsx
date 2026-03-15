'use client'

import { useMemo } from 'react'
import { motion } from 'framer-motion'

// ─── Syntax Swarm (tipo 4) ────────────────────────────────────────────────────
// Enjambre de ceros y unos parpadeantes en rojo

const BINARY_CHARS = ['0','1','0','1','1','0','0','1','1','0','1','0']
const BINARY_POS = [
  { top: '8%',  left: '10%' }, { top: '8%',  left: '50%' }, { top: '8%',  left: '78%' },
  { top: '28%', left: '4%'  }, { top: '28%', left: '36%' }, { top: '28%', left: '68%' },
  { top: '52%', left: '16%' }, { top: '52%', left: '48%' }, { top: '52%', left: '78%' },
  { top: '74%', left: '8%'  }, { top: '74%', left: '40%' }, { top: '74%', left: '70%' },
]
const BLINK_DURATIONS = [0.4, 0.6, 0.3, 0.7, 0.5, 0.4, 0.6, 0.3, 0.5, 0.7, 0.4, 0.6]

export function SyntaxSwarm({ size }: { size: number }) {
  const fontSize = Math.max(7, Math.floor(size * 0.18))
  return (
    <motion.div
      className="relative overflow-hidden bg-[#1A0000] border border-red-600/80"
      style={{ width: size, height: size }}
      animate={{
        boxShadow: [
          '0 0 6px #FF000040 inset, 0 0 4px #FF000060',
          '0 0 18px #FF000080 inset, 0 0 14px #FF3333',
          '0 0 6px #FF000040 inset, 0 0 4px #FF000060',
        ],
      }}
      transition={{ duration: 1.1, repeat: Infinity, ease: 'easeInOut' }}
    >
      {BINARY_CHARS.map((bit, i) => (
        <motion.span
          key={i}
          className="absolute font-mono text-red-500 select-none pointer-events-none"
          style={{ fontSize, top: BINARY_POS[i].top, left: BINARY_POS[i].left, lineHeight: 1 }}
          animate={{ opacity: [1, 0.08, 1, 0.35, 1] }}
          transition={{
            duration: BLINK_DURATIONS[i],
            repeat: Infinity,
            ease: 'linear',
            delay: i * 0.06,
          }}
        >
          {bit}
        </motion.span>
      ))}
    </motion.div>
  )
}

// ─── Logic Brute (tipo 5) ─────────────────────────────────────────────────────
// Bloque sólido con candado holográfico

export function LogicBrute({ size }: { size: number }) {
  const lockSize = Math.round(size * 0.48)
  return (
    <motion.div
      className="relative overflow-hidden bg-[#0A0A18] border border-amber-500/80"
      style={{ width: size, height: size }}
      animate={{
        boxShadow: [
          '0 0 6px #F59E0B30, inset 0 0 8px #F59E0B20',
          '0 0 20px #F59E0B70, inset 0 0 18px #F59E0B50',
          '0 0 6px #F59E0B30, inset 0 0 8px #F59E0B20',
        ],
      }}
      transition={{ duration: 2.2, repeat: Infinity, ease: 'easeInOut' }}
    >
      {/* Candado */}
      <div className="absolute inset-0 flex items-center justify-center">
        <svg
          viewBox="0 0 24 24"
          fill="none"
          style={{ width: lockSize, height: lockSize }}
        >
          <rect x="5" y="11" width="14" height="10" rx="2"
            fill="#F59E0B18" stroke="#F59E0B" strokeWidth="1.5" />
          <path d="M8 11V7a4 4 0 0 1 8 0v4"
            fill="none" stroke="#F59E0B" strokeWidth="1.5" />
          <circle cx="12" cy="16" r="1.5" fill="#F59E0B" />
        </svg>
      </div>
      {/* Línea de escaneo holográfica */}
      <motion.div
        className="absolute left-0 right-0 pointer-events-none"
        style={{
          height: 2,
          background: 'linear-gradient(90deg, transparent 0%, #F59E0B70 40%, #FFF8 50%, #F59E0B70 60%, transparent 100%)',
          zIndex: 5,
        }}
        animate={{ top: ['0%', '100%', '0%'] }}
        transition={{ duration: 2.8, repeat: Infinity, ease: 'linear' }}
      />
      {/* Esquinas decorativas */}
      <div className="absolute top-0 left-0 w-2 h-2 border-t border-l border-amber-400/60" />
      <div className="absolute top-0 right-0 w-2 h-2 border-t border-r border-amber-400/60" />
      <div className="absolute bottom-0 left-0 w-2 h-2 border-b border-l border-amber-400/60" />
      <div className="absolute bottom-0 right-0 w-2 h-2 border-b border-r border-amber-400/60" />
    </motion.div>
  )
}

// ─── Explosión de píxeles ─────────────────────────────────────────────────────

interface Particle {
  angle: number
  distance: number
  delay: number
  size: number
}

interface PixelExplosionProps {
  cellSize: number
  enemyType: number   // 4 = rojo · 5 = ámbar
  onComplete?: () => void
}

export function PixelExplosion({ cellSize, enemyType, onComplete }: PixelExplosionProps) {
  const color = enemyType === 4 ? '#FF3333' : '#F59E0B'
  const glow  = enemyType === 4 ? '#FF000080' : '#F59E0B80'

  // Partículas deterministas (no random en render para evitar mismatches)
  const particles = useMemo<Particle[]>(() => {
    const N = 16
    return Array.from({ length: N }, (_, i) => {
      const spread = (i % 3) * 0.18          // spread pseudo-aleatorio determinista
      return {
        angle:    (i / N) * Math.PI * 2 + spread,
        distance: cellSize * (0.35 + (i % 5) * 0.08),
        delay:    i * 0.025,
        size:     2 + (i % 4),
      }
    })
  }, [cellSize])

  return (
    <div className="relative" style={{ width: cellSize, height: cellSize }}>
      {/* Flash inicial */}
      <motion.div
        className="absolute inset-0"
        style={{ background: color, zIndex: 2 }}
        initial={{ opacity: 0.75 }}
        animate={{ opacity: 0 }}
        transition={{ duration: 0.25 }}
      />
      {/* Partículas */}
      {particles.map((p, i) => (
        <motion.div
          key={i}
          className="absolute rounded-sm"
          style={{
            width: p.size,
            height: p.size,
            background: color,
            boxShadow: `0 0 4px ${glow}`,
            left: cellSize / 2 - p.size / 2,
            top:  cellSize / 2 - p.size / 2,
            zIndex: 3,
          }}
          initial={{ x: 0, y: 0, opacity: 1, scale: 1 }}
          animate={{
            x: Math.cos(p.angle) * p.distance,
            y: Math.sin(p.angle) * p.distance,
            opacity: 0,
            scale: 0.2,
          }}
          transition={{ duration: 0.75, delay: p.delay, ease: 'easeOut' }}
          onAnimationComplete={i === particles.length - 1 ? onComplete : undefined}
        />
      ))}
    </div>
  )
}
