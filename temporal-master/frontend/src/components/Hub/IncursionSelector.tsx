'use client'

import { useEffect, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

// ─── Types ────────────────────────────────────────────────────────────────────

interface IncursionData {
  id:               string
  slug:             string
  titulo:           string
  descripcion:      string
  status:           'ACTIVE' | 'ENCRYPTED'
  system_prompt_id: string | null
  ruta:             string | null
  color_acento:     string
  icono:            string
  orden:            number
}

interface Props {
  /** Callback de navegación — recibe la ruta destino (ej. "/misiones") */
  onNavigate: (path: string) => void
  /** True si el usuario autenticado tiene rol FOUNDER — muestra candado dorado en nodos ENCRYPTED */
  isFounder?: boolean
}

// ─── Componente ───────────────────────────────────────────────────────────────

export default function IncursionSelector({ onNavigate, isFounder = false }: Props) {
  const [incursions, setIncursions] = useState<IncursionData[]>([])
  const [loading,    setLoading]    = useState(true)
  const [glitching,  setGlitching]  = useState<string | null>(null)

  useEffect(() => {
    const API = process.env.NEXT_PUBLIC_API_URL ?? ''
    const controller = new AbortController()

    fetch(`${API}/api/v1/incursions`, { signal: controller.signal })
      .then(r => r.ok ? r.json() as Promise<IncursionData[]> : [])
      .then(data => { setIncursions(data); setLoading(false) })
      .catch(e => { if (e.name !== 'AbortError') setLoading(false) })

    return () => controller.abort()
  }, [])

  // Activa efecto glitch aleatorio en nodos ENCRYPTED cada ~5 segundos
  useEffect(() => {
    const encrypted = incursions.filter(i => i.status === 'ENCRYPTED')
    if (!encrypted.length) return

    const iv = setInterval(() => {
      const target = encrypted[Math.floor(Math.random() * encrypted.length)]
      setGlitching(target.slug)
      setTimeout(() => setGlitching(null), 280)
    }, 4800)

    return () => clearInterval(iv)
  }, [incursions])

  // ── Loading skeleton ────────────────────────────────────────────────────────
  if (loading) {
    return (
      <div className="flex flex-col gap-2">
        <p className="text-[8px] tracking-[0.5em] text-[#00FF41]/15 mb-1 font-mono">
          MÓDULOS DE ESPECIALIZACIÓN
        </p>
        {[1, 2, 3, 4].map(i => (
          <motion.div
            key={i}
            className="h-20 rounded"
            style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.05)' }}
            animate={{ opacity: [0.3, 0.6, 0.3] }}
            transition={{ duration: 1.4, repeat: Infinity, delay: i * 0.15 }}
          />
        ))}
      </div>
    )
  }

  return (
    <div className="flex flex-col gap-2">
      {/* Header */}
      <p className="text-[8px] tracking-[0.5em] text-[#00FF41]/15 mb-1 font-mono uppercase">
        Módulos de Especialización
      </p>

      {/* Incursion cards */}
      <AnimatePresence>
        {incursions.map((inc, i) => {
          const isActive    = inc.status === 'ACTIVE'
          const isGlitching = glitching === inc.slug
          const color       = inc.color_acento

          return (
            <motion.div
              key={inc.slug}
              initial={{ opacity: 0, x: 12 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.07, duration: 0.3, ease: 'easeOut' }}
            >
              {isActive ? (
                <ActiveCard
                  inc={inc}
                  color={color}
                  onEnter={() => inc.ruta && onNavigate(inc.ruta)}
                />
              ) : (
                <EncryptedCard
                  inc={inc}
                  color={color}
                  glitching={isGlitching}
                  isFounder={isFounder}
                />
              )}
            </motion.div>
          )
        })}
      </AnimatePresence>
    </div>
  )
}

// ─── Tarjeta ACTIVE ───────────────────────────────────────────────────────────

function ActiveCard({
  inc,
  color,
  onEnter,
}: {
  inc:     IncursionData
  color:   string
  onEnter: () => void
}) {
  return (
    <motion.div
      className="relative overflow-hidden"
      style={{
        border:     `1px solid ${color}40`,
        background: `${color}06`,
        boxShadow:  `0 0 14px ${color}10`,
      }}
      whileHover={{
        borderColor: `${color}88`,
        boxShadow:   `0 0 22px ${color}20`,
      }}
      transition={{ duration: 0.15 }}
    >
      {/* Línea de pulso superior */}
      <motion.div
        className="absolute top-0 left-0 right-0 h-px"
        style={{ background: `linear-gradient(90deg, transparent, ${color}60, transparent)` }}
        animate={{ opacity: [0.3, 0.9, 0.3] }}
        transition={{ duration: 2.5, repeat: Infinity, ease: 'easeInOut' }}
      />

      {/* Badge ACTIVO */}
      <div className="absolute top-2 right-2 flex items-center gap-1">
        <motion.span
          className="w-1.5 h-1.5 rounded-full"
          style={{ background: color }}
          animate={{ opacity: [1, 0.3, 1], scale: [1, 1.3, 1] }}
          transition={{ duration: 1.6, repeat: Infinity }}
        />
        <span className="text-[7px] tracking-widest font-mono" style={{ color: `${color}77` }}>
          ACTIVO
        </span>
      </div>

      <div className="px-3 pt-2.5 pb-2.5">
        {/* Ícono + Título */}
        <div className="flex items-start gap-1.5 mb-1.5 pr-14">
          <span style={{ color, fontSize: '11px', marginTop: '1px', flexShrink: 0 }}>{inc.icono}</span>
          <span
            className="text-[9px] font-black tracking-widest uppercase font-mono leading-tight"
            style={{ color, textShadow: `0 0 6px ${color}66` }}
          >
            {inc.titulo}
          </span>
        </div>

        {/* Descripción */}
        <p
          className="text-[7px] leading-relaxed font-mono mb-2.5 line-clamp-2"
          style={{ color: `${color}60` }}
        >
          {inc.descripcion}
        </p>

        {/* Botón de entrada */}
        <motion.button
          onClick={onEnter}
          className="w-full text-center text-[8px] tracking-[0.25em] uppercase font-mono py-1.5"
          style={{
            border:     `1px solid ${color}55`,
            color:      color,
            background: `${color}10`,
          }}
          whileHover={{
            background:  `${color}20`,
            borderColor: `${color}99`,
            boxShadow:   `0 0 12px ${color}25`,
          }}
          whileTap={{ scale: 0.97 }}
        >
          ▶ INICIAR INCURSIÓN
        </motion.button>
      </div>
    </motion.div>
  )
}

// ─── Tarjeta ENCRYPTED ────────────────────────────────────────────────────────

function EncryptedCard({
  inc,
  color,
  glitching,
  isFounder,
}: {
  inc:       IncursionData
  color:     string
  glitching: boolean
  isFounder: boolean
}) {
  const lockColor = isFounder ? '#FFC700' : color
  const dimFactor = isFounder ? 1 : 0.65

  return (
    <motion.div
      className="relative overflow-hidden"
      style={{
        border:     `1px solid ${color}${isFounder ? '35' : '22'}`,
        background: `${color}${isFounder ? '06' : '03'}`,
        opacity:    dimFactor,
      }}
      animate={
        glitching && !isFounder
          ? { x: [-2, 3, -1, 2, 0], opacity: [0.65, 0.9, 0.45, 0.75, 0.65] }
          : {}
      }
      transition={{ duration: 0.25, ease: 'linear' }}
    >
      {/* Scanline de cifrado (solo en USER durante glitch) */}
      {glitching && !isFounder && (
        <motion.div
          className="absolute inset-0 pointer-events-none z-10"
          style={{
            background: `repeating-linear-gradient(0deg, transparent, transparent 2px, ${color}08 2px, ${color}08 3px)`,
          }}
          initial={{ opacity: 0 }}
          animate={{ opacity: [0, 1, 0] }}
          transition={{ duration: 0.28 }}
        />
      )}

      {/* Línea de pulso superior (FOUNDER: dorado | USER: color del acento dimmed) */}
      <motion.div
        className="absolute top-0 left-0 right-0 h-px"
        style={{
          background: isFounder
            ? 'linear-gradient(90deg, transparent, #FFC70055, transparent)'
            : `linear-gradient(90deg, transparent, ${color}25, transparent)`,
        }}
        animate={{ opacity: [0.2, 0.7, 0.2] }}
        transition={{ duration: isFounder ? 2.5 : 4, repeat: Infinity, ease: 'easeInOut' }}
      />

      {/* Overlay de cifrado — rejilla sutil (solo USER) */}
      {!isFounder && (
        <div
          className="absolute inset-0 pointer-events-none"
          style={{
            background: 'repeating-linear-gradient(90deg, transparent, transparent 8px, rgba(255,255,255,0.008) 8px, rgba(255,255,255,0.008) 9px)',
          }}
        />
      )}

      {/* Badge de estado — esquina superior derecha */}
      <div className="absolute top-2 right-2 flex items-center gap-1">
        {isFounder ? (
          <>
            <motion.span
              className="text-[8px]"
              style={{ filter: 'drop-shadow(0 0 4px #FFC70099)' }}
              animate={{ opacity: [1, 0.6, 1] }}
              transition={{ duration: 1.2, repeat: Infinity }}
            >
              🔓
            </motion.span>
            <span className="text-[6px] tracking-widest font-mono" style={{ color: '#FFC70077' }}>
              GOD MODE
            </span>
          </>
        ) : (
          <>
            <span className="text-[8px]" style={{ filter: `drop-shadow(0 0 3px ${color}55)` }}>
              🔒
            </span>
          </>
        )}
      </div>

      <div className="px-3 pt-2.5 pb-2.5">
        {/* Ícono + Título */}
        <div className="flex items-start gap-1.5 mb-1.5 pr-14">
          <span style={{ color: `${color}${isFounder ? 'bb' : '66'}`, fontSize: '11px', marginTop: '1px', flexShrink: 0 }}>
            {inc.icono}
          </span>
          <span
            className="text-[9px] font-black tracking-widest uppercase font-mono leading-tight"
            style={{
              color:      isFounder ? `${color}cc` : `${color}77`,
              textShadow: isFounder ? `0 0 6px ${color}44` : 'none',
            }}
          >
            {inc.titulo}
          </span>
        </div>

        {/* Descripción */}
        <p
          className="text-[7px] leading-relaxed font-mono mb-2.5 line-clamp-2"
          style={{ color: isFounder ? `${color}55` : `${color}35` }}
        >
          {inc.descripcion}
        </p>

        {/* CTA — deshabilitado pero visualmente consistente */}
        <div
          className="w-full text-center text-[8px] tracking-[0.2em] uppercase font-mono py-1.5 select-none"
          style={{
            border:     isFounder
              ? `1px solid #FFC70030`
              : `1px solid ${color}18`,
            color:      isFounder ? '#FFC70055' : `${color}35`,
            background: isFounder ? '#FFC70008' : `${color}04`,
          }}
        >
          {isFounder
            ? '🔓 ACCESO FOUNDER — EN CONSTRUCCIÓN'
            : `▸ ${inc.slug === 'tpm-mastery'      ? 'PRÓXIMAMENTE · FASE 2'
                : inc.slug === 'red-team'           ? 'PRÓXIMAMENTE · FASE 3'
                :                                    'PRÓXIMAMENTE · FASE 4'}`
          }
        </div>
      </div>
    </motion.div>
  )
}
