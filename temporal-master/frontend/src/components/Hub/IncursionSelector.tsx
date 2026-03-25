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
            className="h-10 rounded"
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
                // ── ACTIVE: verde neón, botón de entrada ──────────────────────
                <ActiveCard
                  inc={inc}
                  color={color}
                  onEnter={() => inc.ruta && onNavigate(inc.ruta)}
                />
              ) : (
                // ── ENCRYPTED: nodo fantasma — candado dorado (FOUNDER) o rojo (USER) ──
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

      {/* Indicador de estado ACTIVO */}
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

      <div className="px-3 pt-2.5 pb-2">
        {/* Ícono + Título */}
        <div className="flex items-center gap-1.5 mb-0.5 pr-14">
          <span style={{ color, fontSize: '11px' }}>{inc.icono}</span>
          <span
            className="text-[9px] font-black tracking-widest uppercase truncate font-mono"
            style={{ color, textShadow: `0 0 6px ${color}66` }}
          >
            {inc.titulo.length > 28 ? inc.titulo.slice(0, 27) + '…' : inc.titulo}
          </span>
        </div>

        {/* Botón de entrada */}
        <motion.button
          onClick={onEnter}
          className="mt-2 w-full text-center text-[8px] tracking-[0.25em] uppercase font-mono py-1.5"
          style={{
            border:     `1px solid ${color}55`,
            color:      color,
            background: `${color}10`,
          }}
          whileHover={{
            background: `${color}20`,
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
  // FOUNDER: candado dorado + opacidad completa + badge "ACCESO FOUNDER"
  // USER:    candado rojo + opacidad reducida + badge "ENCRIPTADO"
  const lockColor   = isFounder ? '#FFC700' : '#FF2D78'
  const borderAlpha = isFounder ? '0.25'    : '0.12'
  const bgAlpha     = isFounder ? '0.04'    : '0.02'
  const opacity     = isFounder ? 1         : 0.55
  const lockIcon    = isFounder ? '🔓'      : '🔒'
  const lockFilter  = isFounder
    ? 'drop-shadow(0 0 4px #FFC70099)'
    : 'drop-shadow(0 0 3px #FF2D7866)'

  return (
    <motion.div
      className="relative overflow-hidden"
      style={{
        border:     `1px solid rgba(${isFounder ? '255,199,0' : '255,45,120'},${borderAlpha})`,
        background: `rgba(${isFounder ? '255,199,0' : '255,45,120'},${bgAlpha})`,
        opacity,
      }}
      animate={
        glitching && !isFounder
          ? { x: [-2, 3, -1, 2, 0], opacity: [0.55, 0.8, 0.4, 0.7, 0.55] }
          : {}
      }
      transition={{ duration: 0.25, ease: 'linear' }}
    >
      {/* Scanline de cifrado (solo en USER) */}
      {glitching && !isFounder && (
        <motion.div
          className="absolute inset-0 pointer-events-none"
          style={{
            background: 'repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(255,45,120,0.06) 2px, rgba(255,45,120,0.06) 3px)',
          }}
          initial={{ opacity: 0 }}
          animate={{ opacity: [0, 1, 0] }}
          transition={{ duration: 0.28 }}
        />
      )}

      {/* Línea de pulso dorado (solo FOUNDER) */}
      {isFounder && (
        <motion.div
          className="absolute top-0 left-0 right-0 h-px"
          style={{ background: 'linear-gradient(90deg, transparent, #FFC70060, transparent)' }}
          animate={{ opacity: [0.3, 0.9, 0.3] }}
          transition={{ duration: 2.5, repeat: Infinity, ease: 'easeInOut' }}
        />
      )}

      <div className="px-3 pt-2.5 pb-2">
        {/* Ícono + Título cifrado */}
        <div className="flex items-center justify-between gap-2 mb-1.5">
          <div className="flex items-center gap-1.5 min-w-0">
            <span style={{ color: isFounder ? `${color}aa` : `${color}55`, fontSize: '11px' }}>{inc.icono}</span>
            <span
              className="text-[9px] font-black tracking-widest uppercase truncate font-mono"
              style={{ color: isFounder ? `${color}99` : `${color}50` }}
            >
              {inc.titulo.length > 22 ? inc.titulo.slice(0, 21) + '…' : inc.titulo}
            </span>
          </div>

          {/* Candado — dorado (FOUNDER) o rojo (USER) */}
          <span
            className="text-[10px] shrink-0"
            style={{ color: lockColor, filter: lockFilter }}
          >
            {lockIcon}
          </span>
        </div>

        {/* Status badge */}
        <div
          className="inline-flex items-center gap-1 px-1.5 py-0.5"
          style={{
            border:     `1px solid rgba(${isFounder ? '255,199,0' : '255,45,120'},0.25)`,
            background: `rgba(${isFounder ? '255,199,0' : '255,45,120'},0.06)`,
          }}
        >
          <motion.span
            className="w-1 h-1 rounded-full"
            style={{ background: lockColor }}
            animate={{ opacity: [1, 0.2, 1] }}
            transition={{ duration: isFounder ? 1.2 : 2, repeat: Infinity }}
          />
          <span
            className="text-[7px] tracking-widest font-mono uppercase"
            style={{ color: `${lockColor}99` }}
          >
            {isFounder ? 'ACCESO FOUNDER · GOD MODE ACTIVO' : 'ESTADO: ENCRIPTADO · DESBLOQUEO EN FASE BETA'}
          </span>
        </div>
      </div>
    </motion.div>
  )
}
