'use client'

/**
 * BossWarningBanner — Pre-anuncio de Boss Battle
 *
 * Consulta GET /api/v1/session/boss-check/{level} al montarse.
 * Si el Operador está a <= 2 niveles de un Boss (10, 25, 50),
 * muestra un banner dismissible de alerta táctica.
 *
 * Se auto-descarta en 12s o con el botón de cierre.
 */

import { useEffect, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000'

interface Props {
  level: number
}

interface BossCheck {
  warning:     boolean
  boss_level:  number | null
  levels_away: number | null
  message:     string | null
}

export default function BossWarningBanner({ level }: Props) {
  const [data,    setData]    = useState<BossCheck | null>(null)
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    if (!level || level < 1) return

    fetch(`${API_BASE}/api/v1/session/boss-check/${level}`)
      .then(r => r.ok ? r.json() : null)
      .then((res: BossCheck | null) => {
        if (res?.warning) {
          setData(res)
          // Mostrar tras 1.4s para no competir con la animación de entrada del hub
          setTimeout(() => setVisible(true), 1400)
          // Auto-dismiss en 12s
          setTimeout(() => setVisible(false), 13_400)
        }
      })
      .catch(() => {})
  }, [level])

  return (
    <AnimatePresence>
      {visible && data && (
        <motion.div
          className="relative z-30 mx-4 mt-2 shrink-0 overflow-hidden font-mono"
          style={{
            border:     '1px solid rgba(255,184,0,0.40)',
            background: 'rgba(255,184,0,0.05)',
            boxShadow:  '0 0 24px rgba(255,184,0,0.08)',
          }}
          initial={{ opacity: 0, y: -10, scaleY: 0.85 }}
          animate={{ opacity: 1, y: 0,   scaleY: 1 }}
          exit={{    opacity: 0, y: -6,  scaleY: 0.9 }}
          transition={{ type: 'spring', stiffness: 360, damping: 28 }}
        >
          {/* Línea superior pulsante */}
          <motion.div
            className="absolute top-0 left-0 right-0 h-px"
            style={{ background: 'linear-gradient(90deg,transparent,rgba(255,184,0,0.7),transparent)' }}
            animate={{ opacity: [0.4, 1, 0.4] }}
            transition={{ duration: 1.4, repeat: Infinity }}
          />

          <div className="flex items-center gap-3 px-5 py-2.5">
            {/* Ícono de alerta pulsante */}
            <motion.span
              className="text-base shrink-0"
              animate={{ opacity: [0.6, 1, 0.6] }}
              transition={{ duration: 0.8, repeat: Infinity }}
            >
              ⚠
            </motion.span>

            {/* Texto */}
            <div className="flex-1 min-w-0">
              <span
                className="text-[9px] font-black tracking-[0.4em] uppercase mr-3"
                style={{ color: 'rgba(255,184,0,0.9)', textShadow: '0 0 8px rgba(255,184,0,0.5)' }}
              >
                ALERTA TÁCTICA
              </span>
              <span className="text-[9px] tracking-[0.1em]" style={{ color: 'rgba(255,184,0,0.65)' }}>
                Boss Battle en Nivel <strong style={{ color: '#FFB800' }}>{data.boss_level}</strong>
                {' — '}faltan{' '}
                <strong style={{ color: '#FFB800' }}>
                  {data.levels_away} misión{data.levels_away !== 1 ? 'es' : ''}
                </strong>.
                {' '}Los Boss Battles no tienen pistas — prepárate, Operador.
              </span>
            </div>

            {/* Cerrar */}
            <button
              onClick={() => setVisible(false)}
              className="shrink-0 ml-2 text-xs transition-colors leading-none"
              style={{ color: 'rgba(255,184,0,0.30)' }}
              onMouseEnter={(e) => (e.currentTarget.style.color = 'rgba(255,184,0,0.70)')}
              onMouseLeave={(e) => (e.currentTarget.style.color = 'rgba(255,184,0,0.30)')}
              aria-label="Cerrar alerta"
            >
              ✕
            </button>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}
