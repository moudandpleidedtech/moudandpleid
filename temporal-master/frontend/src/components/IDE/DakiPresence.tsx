'use client'

/**
 * DakiPresence — Avatar vivo de DAKI en el IDE.
 *
 * Siempre visible en el editor. Respira en idle, escanea al ejecutar,
 * señala la línea exacta del error y celebra el éxito.
 * Emite partículas de código Python cuando está activa.
 */

import { useMemo } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import DakiWaveform from '@/components/UI/DakiWaveform'

export type DakiState = 'idle' | 'scanning' | 'speaking' | 'error' | 'success'

// ─── Partículas de código flotantes ──────────────────────────────────────────

const PYTHON_TERMS = [
  'for', 'def', 'if', 'return', 'class', 'while', 'try',
  'range()', 'print()', 'len()', '[ ]', '{ }', ':=',
  'lambda', 'import', 'True', 'None', '+=', '==',
]

function CodeParticles({ color }: { color: string }) {
  const particles = useMemo(() =>
    Array.from({ length: 10 }, (_, i) => ({
      term:     PYTHON_TERMS[i % PYTHON_TERMS.length],
      rightPct: 5 + (i * 13) % 90,
      duration: 2.2 + (i * 0.38),
      delay:    i * 0.28,
      opacity:  0.06 + (i % 4) * 0.04,
    })), [])

  return (
    <div className="absolute inset-0 pointer-events-none overflow-hidden">
      {particles.map((p, i) => (
        <motion.span
          key={i}
          className="absolute font-mono text-[9px] whitespace-nowrap"
          style={{ color, right: `${p.rightPct}%`, bottom: 0 }}
          animate={{ y: [0, -140], opacity: [0, p.opacity, 0] }}
          transition={{
            duration: p.duration,
            delay:    p.delay,
            repeat:   Infinity,
            ease:    'linear',
          }}
        >
          {p.term}
        </motion.span>
      ))}
    </div>
  )
}

// ─── Componente principal ─────────────────────────────────────────────────────

interface Props {
  state:      DakiState
  errorLine?: number | null
}

const STATE_CFG = {
  idle: {
    color:       '#00FF41',
    label:       'OBSERVANDO',
    eyeAnim:     { scale: [1, 1.06, 1], opacity: [0.45, 0.75, 0.45] },
    eyeDuration: 3.4,
    glow:        false,
  },
  scanning: {
    color:       '#00FF41',
    label:       'ESCANEANDO...',
    eyeAnim:     { scale: [1, 1.18, 0.92, 1.12, 1], opacity: [0.7, 1, 0.6, 1, 0.7] },
    eyeDuration: 0.75,
    glow:        true,
  },
  speaking: {
    color:       '#00CFFF',
    label:       'TRANSMITIENDO',
    eyeAnim:     { scale: [1, 1.1, 1], opacity: [0.8, 1, 0.8] },
    eyeDuration: 0.55,
    glow:        true,
  },
  error: {
    color:       '#FF4444',
    label:       'ERROR DETECTADO',
    eyeAnim:     { scale: [1, 1.35, 0.85, 1.2, 1], opacity: [1, 0.3, 1, 0.3, 1] },
    eyeDuration: 0.38,
    glow:        true,
  },
  success: {
    color:       '#00FF41',
    label:       'CÓDIGO VALIDADO ✓',
    eyeAnim:     { scale: [1, 1.5, 1.1, 1], opacity: [1, 1, 1, 1] },
    eyeDuration: 0.45,
    glow:        true,
  },
}

export default function DakiPresence({ state, errorLine }: Props) {
  const cfg   = STATE_CFG[state]
  const label = state === 'error' && errorLine ? `LÍNEA ${errorLine} ↑` : cfg.label

  return (
    <div className="absolute bottom-14 right-3 z-30 pointer-events-none select-none">
      <div className="flex flex-col items-end gap-1">

        {/* Partículas — solo cuando DAKI está activa */}
        <AnimatePresence>
          {state !== 'idle' && (
            <motion.div
              key="particles"
              className="relative w-28 h-28"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.4 }}
            >
              <CodeParticles color={cfg.color} />
            </motion.div>
          )}
        </AnimatePresence>

        {/* Panel de presencia */}
        <motion.div
          className="flex items-center gap-2 px-2.5 py-1.5 backdrop-blur-sm"
          animate={{
            borderColor: cfg.glow ? `${cfg.color}35` : `${cfg.color}15`,
            background:  cfg.glow ? `${cfg.color}08` : `${cfg.color}04`,
            boxShadow:   cfg.glow ? `0 0 14px ${cfg.color}18` : 'none',
          }}
          transition={{ duration: 0.3 }}
          style={{ border: `1px solid ${cfg.color}15` }}
        >
          {/* Ojo de DAKI */}
          <motion.span
            className="text-xl leading-none"
            style={{ color: cfg.color, textShadow: `0 0 12px ${cfg.color}80` }}
            animate={cfg.eyeAnim}
            transition={{ duration: cfg.eyeDuration, repeat: Infinity, ease: 'easeInOut' }}
          >
            ◈
          </motion.span>

          {/* Labels */}
          <div className="flex flex-col min-w-0">
            <span
              className="text-[7px] tracking-[0.45em] font-bold"
              style={{ color: `${cfg.color}55` }}
            >
              DAKI
            </span>
            <AnimatePresence mode="wait">
              <motion.span
                key={label}
                className="text-[9px] tracking-[0.18em] font-bold"
                style={{ color: cfg.color }}
                initial={{ opacity: 0, x: 5 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -5 }}
                transition={{ duration: 0.18 }}
              >
                {label}
              </motion.span>
            </AnimatePresence>
          </div>

          {/* Waveform solo cuando transmite */}
          {state === 'speaking' && (
            <DakiWaveform isActive color={cfg.color} size="sm" />
          )}
        </motion.div>
      </div>
    </div>
  )
}
