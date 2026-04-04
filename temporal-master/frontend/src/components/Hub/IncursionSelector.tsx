'use client'

import { useEffect, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { ShieldCheck, Zap, Lock, Terminal } from 'lucide-react'

// ─── Types ────────────────────────────────────────────────────────────────────

interface IncursionData {
  id:                          string
  slug:                        string
  titulo:                      string
  descripcion:                 string
  status:                      'ACTIVE' | 'ENCRYPTED'
  system_prompt_id:            string | null
  ruta:                        string | null
  color_acento:                string
  icono:                       string
  orden:                       number
  // D030 — Progresión entre Incursiones
  prerequisite_incursion_slug: string | null
  total_levels:                number | null
  is_unlocked:                 boolean
}

interface Props {
  onNavigate:      (path: string) => void
  isFounder?:      boolean
  hasAccess?:      boolean   // TRIAL | ACTIVE | FOUNDER
  onAccessDenied?: () => void // muestra AlphaAccessModal
  userId?:         string    // D030 — para calcular is_unlocked por incursión
}

// ─── Componente ───────────────────────────────────────────────────────────────

export default function IncursionSelector({ onNavigate, isFounder = false, hasAccess = false, onAccessDenied, userId }: Props) {
  const [incursions, setIncursions] = useState<IncursionData[]>([])
  const [loading,    setLoading]    = useState(true)
  const [fetchError, setFetchError] = useState(false)
  const [glitching,  setGlitching]  = useState<string | null>(null)

  useEffect(() => {
    const API = process.env.NEXT_PUBLIC_API_URL ?? ''
    const controller = new AbortController()
    const url = userId
      ? `${API}/api/v1/incursions?user_id=${userId}`
      : `${API}/api/v1/incursions`

    fetch(url, { signal: controller.signal })
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
          FORMACIONES PYTHON
        </p>
        <div className="flex items-center justify-center py-10">
          <p className="text-[9px] tracking-[0.3em] font-mono" style={{ color: 'rgba(255,80,50,0.55)' }}>
            SIN SEÑAL CON EL NEXO — RECARGA PARA REINTENTAR
          </p>
        </div>
      </div>
    )
  }

  // Solo formaciones relacionadas con Python (filtro de identidad de marca)
  const pythonIncursions = incursions.filter(i =>
    i.slug.toLowerCase().includes('python') ||
    (i.ruta?.toLowerCase().includes('python') ?? false) ||
    i.titulo.toLowerCase().includes('python') ||
    i.slug === 'qa-automation-ops'   // rama QA Python del Skill Tree
  )

  // ACTIVE primero (ordenadas por `orden`), luego ENCRYPTED — solo Python
  const visible = [
    ...pythonIncursions.filter(i => i.status === 'ACTIVE'),
    ...pythonIncursions.filter(i => i.status === 'ENCRYPTED'),
  ]

  return (
    <div className="flex flex-col gap-3">
      {/* ── Header ── */}
      <div className="flex items-center justify-between">
        <p className="text-[8px] tracking-[0.5em] text-[#00FF41]/20 font-mono uppercase">
          Formaciones Python
        </p>
        <span className="text-[7px] tracking-[0.3em] font-mono" style={{ color: 'rgba(0,255,65,0.18)' }}>
          {pythonIncursions.filter(i => i.status === 'ACTIVE').length} ACTIVOS · {pythonIncursions.filter(i => i.status === 'ENCRYPTED').length} PRÓXIMOS
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
                {inc.slug === 'qa-automation-ops' ? (
                  <QAAutomationCard
                    isUnlocked={inc.is_unlocked || isFounder}
                    onEnter={() => inc.ruta && onNavigate(inc.ruta)}
                  />
                ) : isActive ? (
                  <ActiveCard
                    inc={inc}
                    onEnter={() => {
                      if (!hasAccess && !isFounder) { onAccessDenied?.(); return }
                      if (inc.ruta) onNavigate(inc.ruta)
                    }}
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

// ─── Tarjeta QA Automation (Especialidad) ─────────────────────────────────────

const QA_STACK_BADGES = ['Python', 'pytest', 'Playwright', 'CI/CD']

const BADGE_COLORS: Record<string, { bg: string; text: string; border: string }> = {
  Python:     { bg: 'rgba(6,182,212,0.12)',  text: '#67E8F9', border: 'rgba(6,182,212,0.35)' },
  pytest:     { bg: 'rgba(16,185,129,0.12)', text: '#6EE7B7', border: 'rgba(16,185,129,0.35)' },
  Playwright: { bg: 'rgba(139,92,246,0.12)', text: '#C4B5FD', border: 'rgba(139,92,246,0.35)' },
  'CI/CD':    { bg: 'rgba(251,191,36,0.10)', text: '#FDE68A', border: 'rgba(251,191,36,0.30)' },
}

function QAAutomationCard({
  isUnlocked,
  onEnter,
}: {
  isUnlocked: boolean
  onEnter:    () => void
}) {
  const [hovered, setHovered] = useState(false)

  // Bloqueada hasta que el backend confirme acceso (SYSTEM_KILLER badge o FOUNDER)
  const locked = !isUnlocked

  const CYAN    = '#06B6D4'
  const EMERALD = '#10B981'

  return (
    <motion.div
      className="relative overflow-hidden flex flex-col group"
      style={{
        background:  hovered
          ? 'linear-gradient(135deg, rgba(6,182,212,0.10) 0%, rgba(16,185,129,0.07) 100%)'
          : 'linear-gradient(135deg, rgba(6,182,212,0.05) 0%, rgba(16,185,129,0.03) 100%)',
        border:      hovered
          ? `1px solid rgba(6,182,212,0.70)`
          : `1px solid rgba(6,182,212,0.28)`,
        boxShadow:   hovered
          ? `0 0 32px rgba(6,182,212,0.18), 0 0 64px rgba(16,185,129,0.08), inset 0 0 24px rgba(6,182,212,0.06)`
          : `0 0 16px rgba(6,182,212,0.06), inset 0 0 12px rgba(6,182,212,0.02)`,
        minHeight:   '200px',
        cursor:      locked ? 'default' : 'pointer',
        transition:  'all 0.2s ease',
      }}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      onClick={locked ? undefined : onEnter}
      whileTap={locked ? {} : { scale: 0.98 }}
    >
      {/* ── Línea superior de pulso dual-color ── */}
      <motion.div
        className="absolute top-0 left-0 right-0 h-[2px] pointer-events-none"
        style={{
          background: `linear-gradient(90deg, transparent, ${CYAN}cc, ${EMERALD}cc, transparent)`,
        }}
        animate={{ opacity: hovered ? [0.6, 1, 0.6] : [0.2, 0.5, 0.2] }}
        transition={{ duration: 2, repeat: Infinity, ease: 'easeInOut' }}
      />

      {/* ── Partículas de fondo (hex grid) ── */}
      <div
        className="absolute inset-0 pointer-events-none opacity-[0.04]"
        style={{
          backgroundImage: `radial-gradient(circle, ${CYAN} 1px, transparent 1px)`,
          backgroundSize:  '18px 18px',
        }}
      />

      {/* ── Badge de estado (top-right) ── */}
      <div className="absolute top-3 right-3 flex items-center gap-1.5 z-10">
        {locked ? (
          <>
            <motion.span
              animate={{ opacity: [0.5, 1, 0.5] }}
              transition={{ duration: 2.4, repeat: Infinity }}
            >
              <Lock size={11} color="#FFC700" strokeWidth={2.5} />
            </motion.span>
            <span className="text-[8px] tracking-[0.25em] font-mono" style={{ color: '#FFC70099' }}>
              BLOQUEADO
            </span>
          </>
        ) : (
          <>
            <motion.span
              className="w-2 h-2 rounded-full"
              style={{ background: CYAN, boxShadow: `0 0 6px ${CYAN}` }}
              animate={{ opacity: [1, 0.3, 1], scale: [1, 1.5, 1] }}
              transition={{ duration: 1.6, repeat: Infinity }}
            />
            <span className="text-[8px] tracking-widest font-mono" style={{ color: `${CYAN}aa` }}>
              ACTIVO
            </span>
          </>
        )}
      </div>

      <div className="flex flex-col flex-1 p-5 pt-4 z-10 relative">

        {/* ── Íconos Lucide ── */}
        <div className="flex items-center gap-2 mb-3">
          <motion.div
            animate={hovered
              ? { filter: [`drop-shadow(0 0 6px ${CYAN})`, `drop-shadow(0 0 14px ${CYAN})`, `drop-shadow(0 0 6px ${CYAN})`] }
              : { filter: `drop-shadow(0 0 4px ${CYAN}66)` }
            }
            transition={{ duration: 1.4, repeat: hovered ? Infinity : 0 }}
          >
            <ShieldCheck size={26} color={locked ? '#334155' : CYAN} strokeWidth={1.8} />
          </motion.div>
          <motion.div
            animate={hovered
              ? { y: [-1, 1, -1], filter: [`drop-shadow(0 0 4px ${EMERALD})`, `drop-shadow(0 0 10px ${EMERALD})`, `drop-shadow(0 0 4px ${EMERALD})`] }
              : { y: 0, filter: `drop-shadow(0 0 3px ${EMERALD}55)` }
            }
            transition={{ duration: 1.2, repeat: hovered ? Infinity : 0 }}
          >
            <Zap size={18} color={locked ? '#1e3a3a' : EMERALD} strokeWidth={2} />
          </motion.div>
        </div>

        {/* ── Título ── */}
        <span
          className="text-sm font-black tracking-widest uppercase font-mono leading-snug mb-1 block"
          style={{
            color:      locked ? 'rgba(100,140,150,0.7)' : CYAN,
            textShadow: locked ? 'none' : `0 0 14px ${CYAN}55`,
            transition: 'all 0.2s ease',
          }}
        >
          QA Automation
        </span>
        <span
          className="text-[9px] tracking-[0.2em] font-mono mb-2 block"
          style={{ color: locked ? 'rgba(70,100,110,0.6)' : `${EMERALD}aa` }}
        >
          STACK PYTHON · PYTEST + PLAYWRIGHT
        </span>

        {/* ── Descripción (aparece en hover) ── */}
        <div className="mb-2 overflow-hidden" style={{ height: hovered ? 'auto' : '2.8rem' }}>
          <AnimatePresence>
            {hovered ? (
              <motion.p
                key="desc-full"
                className="text-[10px] leading-relaxed font-mono"
                style={{ color: locked ? 'rgba(100,140,150,0.55)' : `${CYAN}cc` }}
                initial={{ opacity: 0, y: 4 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -4 }}
                transition={{ duration: 0.18 }}
              >
                Domina el asedio de software moderno. De scripts locales a Pipelines de élite.
              </motion.p>
            ) : (
              <motion.p
                key="desc-short"
                className="text-[10px] leading-relaxed font-mono line-clamp-2"
                style={{ color: locked ? 'rgba(80,110,120,0.5)' : `${CYAN}88` }}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.15 }}
              >
                Automatización de pruebas, CI/CD pipelines y cobertura de calidad a escala.
              </motion.p>
            )}
          </AnimatePresence>
        </div>

        {/* ── Stack Badges ── */}
        <div className="flex flex-wrap gap-1.5 mb-3">
          {QA_STACK_BADGES.map((tag) => {
            const c = BADGE_COLORS[tag]
            return (
              <span
                key={tag}
                className="text-[8px] font-mono tracking-widest px-2 py-0.5"
                style={{
                  background:   locked ? 'rgba(30,50,60,0.5)' : c.bg,
                  color:        locked ? 'rgba(60,80,90,0.7)' : c.text,
                  border:       `1px solid ${locked ? 'rgba(40,60,70,0.4)' : c.border}`,
                  transition:   'all 0.2s ease',
                }}
              >
                {tag}
              </span>
            )
          })}
        </div>

        {/* ── CTA / Lock message ── */}
        {locked ? (
          <div className="mt-auto">
            <div
              className="w-full text-center py-2.5 font-mono relative overflow-hidden"
              style={{
                border:     '1px solid rgba(255,199,0,0.25)',
                background: 'rgba(255,199,0,0.04)',
              }}
            >
              {/* Texto base */}
              <span
                className="text-[9px] tracking-[0.18em] uppercase block transition-opacity duration-200 group-hover:opacity-0"
                style={{ color: 'rgba(255,199,0,0.55)' }}
              >
                <Lock size={9} className="inline mr-1.5 mb-0.5" />
                REQUIERE: PYTHON CORE AVANZADO
              </span>
              {/* Texto hover */}
              <span
                className="absolute inset-0 flex items-center justify-center text-[9px] tracking-[0.15em] uppercase opacity-0 group-hover:opacity-100 transition-opacity duration-200"
                style={{ color: 'rgba(255,199,0,0.85)', background: 'rgba(255,199,0,0.06)' }}
              >
                🔒 COMPLETA EL CORE PYTHON PRIMERO
              </span>
            </div>
          </div>
        ) : (
          <motion.button
            onClick={(e) => { e.stopPropagation(); onEnter() }}
            className="mt-auto w-full text-center text-[10px] tracking-[0.35em] uppercase font-mono py-2.5"
            style={{
              border:     `1px solid ${CYAN}66`,
              color:      CYAN,
              background: `${CYAN}12`,
            }}
            whileHover={{ background: `${CYAN}28`, borderColor: `${CYAN}cc`, boxShadow: `0 0 14px ${CYAN}30` }}
            whileTap={{ scale: 0.96 }}
          >
            <div className="flex items-center justify-center gap-2">
              <Terminal size={11} />
              INGRESAR AL SECTOR
            </div>
          </motion.button>
        )}
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
              {inc.slug === 'red-team' ? 'ACCESO RESTRINGIDO' : 'PRÓXIMAMENTE'}
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
