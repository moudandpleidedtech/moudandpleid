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
  onNavigate: (path: string) => void
  isFounder?: boolean
}

// ─── Componente ───────────────────────────────────────────────────────────────

export default function IncursionSelector({ onNavigate, isFounder = false }: Props) {
  const [incursions, setIncursions] = useState<IncursionData[]>([])
  const [loading,    setLoading]    = useState(true)
  const [fetchError, setFetchError] = useState(false)
  const [glitching,  setGlitching]  = useState<string | null>(null)

  useEffect(() => {
    const API = process.env.NEXT_PUBLIC_API_URL ?? ''
    const controller = new AbortController()

    fetch(`${API}/api/v1/incursions`, { signal: controller.signal })
      .then(r => r.json() as Promise<unknown>)
      .then(data => {
        console.log('DATA DEL BACKEND:', data)
        setIncursions(Array.isArray(data) ? data as IncursionData[] : [])
        setLoading(false)
      })
      .catch(e => {
        if (e.name === 'AbortError') return
        setFetchError(true)
        setLoading(false)
      })

    return () => controller.abort()
  }, [])

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

  if (loading) {
    return (
      <div className="flex flex-col gap-2">
        <p className="text-[8px] tracking-[0.5em] text-[#00FF41]/15 mb-1 font-mono">
          CARGANDO INTEL...
        </p>
        <div className="grid grid-cols-2 gap-3">
          {[1, 2, 3, 4].map(i => (
            <motion.div
              key={i}
              className="h-[160px] rounded-sm"
              style={{ background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.05)' }}
              animate={{ opacity: [0.2, 0.5, 0.2] }}
              transition={{ duration: 1.6, repeat: Infinity, delay: i * 0.2 }}
            />
          ))}
        </div>
      </div>
    )
  }

  if (fetchError) {
    return (
      <div className="flex flex-col gap-2">
        <p className="text-[8px] tracking-[0.5em] text-[#00FF41]/15 mb-1 font-mono">
          MÓDULOS DE FORMACIÓN
        </p>
        <div className="flex items-center justify-center py-10">
          <p className="text-[9px] tracking-[0.3em] font-mono" style={{ color: 'rgba(255,80,50,0.55)' }}>
            SIN SEÑAL CON EL NEXO — RECARGA PARA REINTENTAR
          </p>
        </div>
      </div>
    )
  }

  // ACTIVE primero (ordenadas por `orden`), luego ENCRYPTED — todas visibles
  const visible = [
    ...incursions.filter(i => i.status === 'ACTIVE'),
    ...incursions.filter(i => i.status === 'ENCRYPTED'),
  ]

  return (
    <div className="flex flex-col gap-3">
      {/* ── Header ── */}
      <div className="flex items-center justify-between">
        <p className="text-[8px] tracking-[0.5em] text-[#00FF41]/20 font-mono uppercase">
          Módulos de Formación
        </p>
        <span className="text-[7px] tracking-[0.3em] font-mono" style={{ color: 'rgba(0,255,65,0.18)' }}>
          {incursions.filter(i => i.status === 'ACTIVE').length} ACTIVOS · {incursions.filter(i => i.status === 'ENCRYPTED').length} PRÓXIMOS
        </span>
      </div>

      {/* ── Grid de tarjetas — todas visibles ── */}
      <div className="grid grid-cols-2 gap-4 min-h-[200px]">
        <AnimatePresence mode="popLayout">
          {visible.map((inc, i) => {
            const isActive    = inc.status === 'ACTIVE'
            const isGlitching = glitching === inc.slug

            return (
              <motion.div
                key={inc.slug}
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -8 }}
                transition={{ delay: i * 0.06, duration: 0.25, ease: 'easeOut' }}
              >
                {isActive ? (
                  <ActiveCard
                    inc={inc}
                    onEnter={() => inc.ruta && onNavigate(inc.ruta)}
                  />
                ) : (
                  <EncryptedCard
                    inc={inc}
                    glitching={isGlitching}
                    isFounder={isFounder}
                    onEnter={() => inc.ruta && onNavigate(inc.ruta)}
                  />
                )}
              </motion.div>
            )
          })}
          {visible.length === 0 && (
            <motion.div
              key="empty"
              className="col-span-2 flex items-center justify-center py-10"
              initial={{ opacity: 0 }} animate={{ opacity: 1 }}
            >
              <p className="text-[9px] tracking-[0.4em] text-[#00FF41]/20 font-mono">
                SIN FORMACIONES DISPONIBLES
              </p>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  )
}

// ─── Tarjeta ACTIVE ───────────────────────────────────────────────────────────

function ActiveCard({
  inc,
  onEnter,
}: {
  inc:     IncursionData
  onEnter: () => void
}) {
  const color = inc.color_acento

  return (
    <motion.div
      className="relative overflow-hidden flex flex-col cursor-pointer"
      style={{
        border:     `1px solid ${color}55`,
        background: `${color}08`,
        boxShadow:  `0 0 24px ${color}12, inset 0 0 20px ${color}04`,
        minHeight:  '200px',
      }}
      whileHover={{
        borderColor: `${color}cc`,
        boxShadow:   `0 0 32px ${color}30, inset 0 0 20px ${color}08`,
      }}
      whileTap={{ scale: 0.98 }}
      transition={{ duration: 0.15 }}
      onClick={onEnter}
    >
      {/* Línea de pulso superior */}
      <motion.div
        className="absolute top-0 left-0 right-0 h-[2px]"
        style={{ background: `linear-gradient(90deg, transparent, ${color}cc, transparent)` }}
        animate={{ opacity: [0.3, 1, 0.3] }}
        transition={{ duration: 2.2, repeat: Infinity, ease: 'easeInOut' }}
      />

      {/* Badge ACTIVO */}
      <div className="absolute top-3 right-3 flex items-center gap-1.5">
        <motion.span
          className="w-2 h-2 rounded-full"
          style={{ background: color }}
          animate={{ opacity: [1, 0.3, 1], scale: [1, 1.5, 1] }}
          transition={{ duration: 1.6, repeat: Infinity }}
        />
        <span className="text-[8px] tracking-widest font-mono" style={{ color: `${color}99` }}>
          ACTIVO
        </span>
      </div>

      <div className="flex flex-col flex-1 p-5 pt-4">
        {/* Ícono */}
        <motion.span
          className="text-3xl mb-2 block leading-none select-none"
          style={{ filter: `drop-shadow(0 0 12px ${color}aa)` }}
          animate={{ opacity: [0.85, 1, 0.85] }}
          transition={{ duration: 3, repeat: Infinity }}
        >
          {inc.icono}
        </motion.span>

        {/* Título */}
        <span
          className="text-base font-black tracking-widest uppercase font-mono leading-snug mb-1 block"
          style={{ color, textShadow: `0 0 12px ${color}66` }}
        >
          {inc.titulo}
        </span>

        {/* Teaser Description */}
        <p
          className="text-[11px] leading-relaxed font-mono opacity-80 line-clamp-3 mb-auto"
          style={{ color }}
        >
          {inc.descripcion || 'Módulo de formación confidencial en estado activo.'}
        </p>

        {/* Botón INGRESAR */}
        <motion.button
          onClick={(e) => { e.stopPropagation(); onEnter() }}
          className="mt-4 w-full text-center text-[10px] tracking-[0.35em] uppercase font-mono py-2.5 relative overflow-hidden"
          style={{
            border:     `1px solid ${color}66`,
            color:      color,
            background: `${color}12`,
          }}
          whileHover={{
            background:  `${color}28`,
            borderColor: `${color}cc`,
            boxShadow:   `0 0 14px ${color}30`,
          }}
          whileTap={{ scale: 0.96 }}
        >
          ▶ INGRESAR
        </motion.button>
      </div>
    </motion.div>
  )
}

// ─── Tarjeta ENCRYPTED ────────────────────────────────────────────────────────

function EncryptedCard({
  inc,
  glitching,
  isFounder,
  onEnter,
}: {
  inc:       IncursionData
  glitching: boolean
  isFounder: boolean
  onEnter:   () => void
}) {
  const color = inc.color_acento

  return (
    <motion.div
      className={`relative overflow-hidden flex flex-col group${isFounder ? ' cursor-pointer' : ''}`}
      style={{
        border:     `1px solid ${isFounder ? color + '55' : 'rgba(60,60,80,0.5)'}`,
        background: isFounder ? `${color}08` : 'rgba(8,8,14,0.7)',
        minHeight:  '200px',
        boxShadow:  isFounder ? `0 0 24px ${color}12` : 'none',
      }}
      animate={
        glitching && !isFounder
          ? { x: [-2, 3, -1, 2, 0], opacity: [0.55, 0.85, 0.45, 0.65, 0.55] }
          : {}
      }
      whileHover={isFounder ? { borderColor: `${color}cc`, boxShadow: `0 0 32px ${color}30` } : { borderColor: 'rgba(90,90,120,0.6)' }}
      whileTap={isFounder ? { scale: 0.98 } : {}}
      transition={{ duration: 0.15, ease: 'linear' }}
      onClick={isFounder ? onEnter : undefined}
    >
      {/* Scanlines de cifrado (solo durante glitch) */}
      {glitching && !isFounder && (
        <motion.div
          className="absolute inset-0 pointer-events-none z-10"
          style={{
            background: `repeating-linear-gradient(0deg, transparent, transparent 2px, ${color}0a 2px, ${color}0a 3px)`,
          }}
          initial={{ opacity: 0 }}
          animate={{ opacity: [0, 1, 0] }}
          transition={{ duration: 0.28 }}
        />
      )}

      {/* Línea superior */}
      <motion.div
        className="absolute top-0 left-0 right-0 h-px"
        style={{
          background: isFounder
            ? 'linear-gradient(90deg, transparent, #FFC70044, transparent)'
            : 'linear-gradient(90deg, transparent, rgba(60,60,80,0.5), transparent)',
        }}
        animate={{ opacity: [0.2, 0.7, 0.2] }}
        transition={{ duration: isFounder ? 2.5 : 5, repeat: Infinity }}
      />

      {/* Badge */}
      <div className="absolute top-3 right-3 flex items-center gap-1.5">
        {isFounder ? (
          <>
            <motion.span
              className="w-2 h-2 rounded-full"
              style={{ background: color }}
              animate={{ opacity: [1, 0.3, 1], scale: [1, 1.5, 1] }}
              transition={{ duration: 1.6, repeat: Infinity }}
            />
            <span className="text-[8px] tracking-widest font-mono" style={{ color: `${color}99` }}>
              FOUNDER
            </span>
          </>
        ) : (
          <span className="text-sm leading-none" style={{ opacity: 0.25 }}>🔒</span>
        )}
      </div>

      <div className="flex flex-col flex-1 p-5 pt-4 z-10 relative">
        {/* Ícono y Lock */}
        <div className="flex justify-between items-start mb-2 group">
          <span
            className="text-3xl leading-none select-none transition-opacity duration-300"
            style={{
              color:   isFounder ? color : 'rgba(80,80,110,0.8)',
              opacity: isFounder ? 0.6 : 1,
              filter:  isFounder ? `drop-shadow(0 0 8px ${color}55)` : 'none',
            }}
          >
            {inc.icono}
          </span>
          {!isFounder && (
            <span className="text-[rgba(60,60,80,0.8)] transition-colors duration-300 group-hover:text-[rgba(255,184,0,0.75)]">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
              </svg>
            </span>
          )}
        </div>

        {/* Título */}
        <span
          className="text-base font-black tracking-widest uppercase font-mono leading-snug mb-1 block"
          style={{
            color: isFounder ? `${color}88` : 'rgba(110,110,130,0.9)',
          }}
        >
          {inc.titulo}
        </span>

        {/* Teaser Description */}
        <p
          className="text-[11px] leading-relaxed font-mono opacity-80 line-clamp-3 mb-auto"
          style={{ color: isFounder ? `${color}aa` : 'rgba(90,90,110,0.85)' }}
        >
          {inc.descripcion || 'Archivo clasificado. Se requiere autorización de Nivel Superior para visibilidad.'}
        </p>

        {/* CTA Hover Efecto */}
        {isFounder ? (
          <motion.button
            onClick={(e) => { e.stopPropagation(); onEnter() }}
            className="mt-4 w-full text-center text-[10px] tracking-[0.35em] uppercase font-mono py-2.5"
            style={{
              border:     `1px solid ${color}66`,
              color:      color,
              background: `${color}12`,
            }}
            whileHover={{
              background:  `${color}28`,
              borderColor: `${color}cc`,
              boxShadow:   `0 0 14px ${color}30`,
            }}
            whileTap={{ scale: 0.96 }}
          >
            ▶ INGRESAR
          </motion.button>
        ) : (
          <div className="relative mt-4">
            <div
              className="w-full text-center text-[10px] tracking-[0.2em] uppercase font-mono py-2.5 select-none transition-opacity duration-300 opacity-100 group-hover:opacity-0"
              style={{
                border:     '1px solid rgba(60,60,80,0.35)',
                color:      'rgba(80,80,100,0.75)',
                background: 'transparent',
              }}
            >
              {inc.slug === 'tpm-mastery' || inc.slug.includes('tpm') ? 'EXPANSIÓN PENDIENTE'
              : inc.slug === 'red-team' || inc.slug.includes('sales')  ? 'ACCESO RESTRINGIDO'
              : 'PRÓXIMAMENTE'}
            </div>
            
            <div
              className="absolute inset-0 flex items-center justify-center w-full text-center text-[9px] tracking-[0.1em] uppercase font-mono py-2.5 select-none transition-all duration-300 opacity-0 group-hover:opacity-100 scale-[0.98] group-hover:scale-100"
              style={{
                border:     '1px dashed rgba(255,184,0,0.4)',
                color:      'rgba(255,184,0,0.85)',
                background: 'rgba(255,184,0,0.08)',
              }}
            >
              [ DESBLOQUEA DOMINANDO EL NIVEL ANTERIOR ]
            </div>
          </div>
        )}
      </div>
    </motion.div>
  )
}
