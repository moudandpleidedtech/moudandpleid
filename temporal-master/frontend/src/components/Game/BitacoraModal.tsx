'use client'

import { useEffect, useState, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? ''

// ─── Tipos ─────────────────────────────────────────────────────────────────────

interface Archivo {
  id: string
  order: number
  label: string
  title: string
  subtitle: string
  missionName: string
  theoryContent: string
  completed: boolean
}

const TIER_SUBTITLE: Record<number, string> = {
  1: 'NIVEL INICIANTE',
  2: 'NIVEL INTERMEDIO',
  3: 'NIVEL AVANZADO',
}

// ─── localStorage helpers ──────────────────────────────────────────────────────

const LS_KEY = 'pq-bitacora-read'

function getReadOrders(): number[] {
  if (typeof window === 'undefined') return []
  try { return JSON.parse(localStorage.getItem(LS_KEY) ?? '[]') } catch { return [] }
}
function markOrderRead(order: number) {
  const current = getReadOrders()
  if (!current.includes(order)) localStorage.setItem(LS_KEY, JSON.stringify([...current, order]))
}

// ─── Exportado para uso externo ────────────────────────────────────────────────

export function countNewArchives(completedOrders: number[]): number {
  const readOrders = getReadOrders()
  return completedOrders.filter(o => !readOrders.includes(o)).length
}

// ─── Renderizador de markdown-lite ────────────────────────────────────────────

function TheoryContent({ text }: { text: string }) {
  const lines = text.split('\n')
  return (
    <div className="flex flex-col gap-1.5">
      {lines.map((line, i) => {
        if (line.startsWith('## '))
          return <p key={i} className="text-[11px] font-bold tracking-[0.25em] text-[#00FF41]/80 mt-3 mb-0.5">{line.slice(3)}</p>
        if (line.startsWith('# '))
          return <p key={i} className="text-[13px] font-black tracking-[0.2em] text-[#00FF41] mt-2 mb-1">{line.slice(2)}</p>
        if (line.trim() === '')
          return <div key={i} className="h-1" />
        // inline code + bold
        const parts = line.split(/(`[^`]+`|\*\*[^*]+\*\*)/g)
        const rendered = parts.map((part, j) => {
          if (part.startsWith('`') && part.endsWith('`'))
            return <code key={j} className="px-1 py-0.5 bg-[#00FF41]/10 border border-[#00FF41]/20 text-[#00FF41] text-[10px] font-mono">{part.slice(1, -1)}</code>
          if (part.startsWith('**') && part.endsWith('**'))
            return <strong key={j} className="text-[#00FF41]/90 font-bold">{part.slice(2, -2)}</strong>
          return <span key={j}>{part}</span>
        })
        return <p key={i} className="text-[11px] text-white/50 leading-relaxed">{rendered}</p>
      })}
    </div>
  )
}

// ─── Props ─────────────────────────────────────────────────────────────────────

interface BitacoraModalProps {
  isOpen: boolean
  onClose: () => void
  userId: string
  completedOrders: number[]   // usado para badge count en hub
}

// ─── Componente ────────────────────────────────────────────────────────────────

export default function BitacoraModal({ isOpen, onClose, userId, completedOrders: _completedOrders }: BitacoraModalProps) {
  const [archivos, setArchivos] = useState<Archivo[]>([])
  const [loading, setLoading] = useState(false)
  const [selected, setSelected] = useState<Archivo | null>(null)
  const [readOrders, setReadOrders] = useState<number[]>([])

  // Fetch dinámico al abrir
  useEffect(() => {
    if (!isOpen || !userId) return
    setLoading(true)
    setReadOrders(getReadOrders())
    fetch(`${API_BASE}/api/v1/challenges?user_id=${userId}`)
      .then(r => r.ok ? r.json() : [])
      .then((data: { id: string; title: string; difficulty_tier: number; level_order: number | null; theory_content: string | null; completed: boolean }[]) => {
        const mapped: Archivo[] = data
          .filter(e => e.theory_content && e.level_order != null)
          .sort((a, b) => (a.level_order ?? 0) - (b.level_order ?? 0))
          .map(e => ({
            id: e.id,
            order: e.level_order as number,
            label: `ARCHIVO ${String(e.level_order).padStart(2, '0')}`,
            title: e.title,
            subtitle: TIER_SUBTITLE[e.difficulty_tier] ?? 'NIVEL',
            missionName: `Misión ${e.level_order}`,
            theoryContent: e.theory_content as string,
            completed: e.completed,
          }))
        setArchivos(mapped)
        // Auto-seleccionar primer archivo desbloqueado
        const first = mapped.find(a => a.completed) ?? mapped[0] ?? null
        setSelected(first)
      })
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [isOpen, userId])

  // Marcar como leído al seleccionar
  useEffect(() => {
    if (!isOpen || !selected || !selected.completed) return
    markOrderRead(selected.order)
    setReadOrders(getReadOrders())
  }, [selected, isOpen])

  // Cerrar con Escape
  useEffect(() => {
    if (!isOpen) return
    const h = (e: KeyboardEvent) => { if (e.key === 'Escape') onClose() }
    window.addEventListener('keydown', h)
    return () => window.removeEventListener('keydown', h)
  }, [isOpen, onClose])

  const handleSelect = useCallback((a: Archivo) => {
    if (a.completed) setSelected(a)
  }, [])

  const isNew = (a: Archivo) => a.completed && !readOrders.includes(a.order)
  const completedArchivos = archivos.filter(a => a.completed)

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          className="fixed inset-0 z-50 flex items-center justify-center p-4"
          initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
          transition={{ duration: 0.18 }}
        >
          {/* Backdrop */}
          <motion.div className="absolute inset-0 bg-black/88 backdrop-blur-md" onClick={onClose} />

          {/* Panel principal */}
          <motion.div
            className="relative z-10 w-full max-w-4xl h-[82vh] flex border font-mono overflow-hidden"
            style={{ borderColor: 'rgba(0,255,65,0.25)', background: 'linear-gradient(135deg,#030a05 0%,#020604 100%)' }}
            initial={{ scale: 0.92, y: 24 }} animate={{ scale: 1, y: 0 }}
            exit={{ scale: 0.92, y: 24 }} transition={{ duration: 0.22, ease: [0.16,1,0.3,1] }}
          >
            {/* Esquinas */}
            <span className="absolute top-0 left-0 w-5 h-5 border-t-2 border-l-2 border-[#00FF41]/60 z-10" />
            <span className="absolute top-0 right-0 w-5 h-5 border-t-2 border-r-2 border-[#00FF41]/60 z-10" />
            <span className="absolute bottom-0 left-0 w-5 h-5 border-b-2 border-l-2 border-[#00FF41]/60 z-10" />
            <span className="absolute bottom-0 right-0 w-5 h-5 border-b-2 border-r-2 border-[#00FF41]/60 z-10" />

            {/* ── Columna izquierda — Lista de archivos ── */}
            <div className="w-56 shrink-0 flex flex-col border-r border-[#00FF41]/12 overflow-hidden">

              {/* Header lista */}
              <div className="px-4 py-4 border-b border-[#00FF41]/10 shrink-0">
                <p className="text-[8px] tracking-[0.6em] text-[#00FF41]/40 mb-0.5">CÓDICE DE INFILTRACIÓN</p>
                <p className="text-[7px] tracking-wider text-[#00FF41]/20">
                  {loading ? 'CARGANDO...' : `${completedArchivos.length}/${archivos.length} ARCHIVOS DESBLOQUEADOS`}
                </p>
                {/* Mini barra de progreso */}
                <div className="mt-2 h-px bg-[#00FF41]/10 relative overflow-hidden">
                  <motion.div
                    className="absolute left-0 top-0 h-full bg-[#00FF41]"
                    initial={{ width: 0 }}
                    animate={{ width: archivos.length ? `${(completedArchivos.length / archivos.length) * 100}%` : '0%' }}
                    transition={{ duration: 0.8, ease: 'easeOut' }}
                  />
                </div>
              </div>

              {/* Lista */}
              <div className="flex-1 overflow-y-auto py-1">
                {loading ? (
                  <div className="px-4 py-6 text-center">
                    <motion.p
                      className="text-[8px] tracking-widest text-[#00FF41]/30"
                      animate={{ opacity: [0.3, 0.7, 0.3] }}
                      transition={{ duration: 1.2, repeat: Infinity }}
                    >
                      CARGANDO BÓVEDA...
                    </motion.p>
                  </div>
                ) : (
                  archivos.map((a, idx) => {
                    const isSelected = selected?.id === a.id
                    const hasNew = isNew(a)
                    return (
                      <motion.button
                        key={a.id}
                        initial={{ opacity: 0, x: -8 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: idx * 0.04 }}
                        onClick={() => handleSelect(a)}
                        disabled={!a.completed}
                        className="w-full text-left px-4 py-3 border-b border-[#00FF41]/6 transition-all duration-150 relative"
                        style={isSelected && a.completed ? {
                          background: 'rgba(0,255,65,0.07)',
                          borderLeft: '2px solid rgba(0,255,65,0.6)',
                        } : !a.completed ? {
                          opacity: 0.45,
                          cursor: 'not-allowed',
                        } : {}}
                        onMouseEnter={e => { if (a.completed && !isSelected) e.currentTarget.style.background = 'rgba(0,255,65,0.04)' }}
                        onMouseLeave={e => { if (!isSelected) e.currentTarget.style.background = 'transparent' }}
                      >
                        <div className="flex items-start gap-2.5">
                          {/* Icono estado */}
                          <span className={`text-sm mt-0.5 shrink-0 ${a.completed ? 'text-[#00FF41]/60' : 'text-[#00FF41]/20'}`}>
                            {a.completed ? '◈' : '🔒'}
                          </span>
                          <div className="flex flex-col gap-0.5 min-w-0 flex-1">
                            <div className="flex items-center gap-1.5">
                              <span className={`text-[9px] font-bold tracking-wider truncate ${
                                isSelected ? 'text-[#00FF41]' : a.completed ? 'text-[#00FF41]/65' : 'text-[#00FF41]/25'
                              }`}>
                                {a.label}
                              </span>
                              {/* Indicador NEW */}
                              {hasNew && (
                                <motion.span
                                  className="w-1.5 h-1.5 rounded-full bg-[#00FF41] shrink-0"
                                  animate={{ opacity: [1, 0.2, 1] }}
                                  transition={{ duration: 0.8, repeat: Infinity }}
                                />
                              )}
                            </div>
                            {a.completed ? (
                              <span className="text-[8px] text-[#00FF41]/35 truncate">{a.subtitle}</span>
                            ) : (
                              <span className="text-[7px] text-[#00FF41]/18 leading-snug">
                                [ DATOS ENCRIPTADOS ]
                                <br />Requiere {a.missionName}
                              </span>
                            )}
                          </div>
                        </div>
                      </motion.button>
                    )
                  })
                )}
              </div>
            </div>

            {/* ── Columna derecha — Contenido del archivo ── */}
            <div className="flex-1 flex flex-col overflow-hidden">

              {/* Header del panel derecho */}
              <div className="shrink-0 flex items-center justify-between px-6 py-4 border-b border-[#00FF41]/10">
                <div>
                  <p className="text-[8px] tracking-[0.5em] text-[#00FF41]/30 mb-0.5">
                    {selected ? `${selected.label} // ${selected.missionName.toUpperCase()}` : 'SELECCIONA UN ARCHIVO'}
                  </p>
                  <h2 className="text-sm font-black tracking-wider text-[#00FF41]"
                    style={{ textShadow: '0 0 10px rgba(0,255,65,0.4)' }}>
                    {selected ? selected.title.toUpperCase() : '—'}
                  </h2>
                </div>
                <button
                  onClick={onClose}
                  className="text-[9px] tracking-widest text-[#00FF41]/30 hover:text-[#00FF41]/70 transition-colors border border-[#00FF41]/15 px-2.5 py-1 hover:border-[#00FF41]/35"
                >
                  [ ESC ]
                </button>
              </div>

              {/* Cuerpo scrollable */}
              <AnimatePresence mode="wait">
                {!selected ? (
                  <motion.div
                    key="empty"
                    className="flex-1 flex items-center justify-center"
                    initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                  >
                    <p className="text-[9px] tracking-widest text-[#00FF41]/20">SELECCIONA UN ARCHIVO DE LA LISTA</p>
                  </motion.div>
                ) : selected.completed ? (
                  <motion.div
                    key={selected.id}
                    className="flex-1 overflow-y-auto px-6 py-6 flex flex-col gap-5"
                    initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -6 }} transition={{ duration: 0.2 }}
                  >
                    {/* Encabezado de sección */}
                    <div className="flex items-center gap-2">
                      <motion.span
                        className="w-1.5 h-1.5 rounded-full bg-[#00FF41]"
                        animate={{ opacity: [1, 0.2, 1] }}
                        transition={{ duration: 1.2, repeat: Infinity }}
                      />
                      <span className="text-[9px] tracking-[0.5em] text-[#00FF41]/40">
                        REGISTRO TÁCTICO // CONOCIMIENTO RECUPERADO
                      </span>
                    </div>

                    {/* Teoría */}
                    <div className="border-l-2 border-[#00FF41]/20 pl-4">
                      <TheoryContent text={selected.theoryContent} />
                    </div>

                    {/* Footer del archivo */}
                    <div className="mt-auto pt-4 border-t border-[#00FF41]/8 flex items-center justify-between">
                      <span className="text-[7px] tracking-[0.5em] text-[#00FF41]/15">
                        ARCHIVO DESBLOQUEADO // CONOCIMIENTO INTEGRADO
                      </span>
                      <span className="text-[7px] tracking-[0.4em] text-[#00FF41]/12">
                        DAKI EdTech
                      </span>
                    </div>
                  </motion.div>
                ) : (
                  <motion.div
                    key="locked"
                    className="flex-1 flex flex-col items-center justify-center gap-4 px-8"
                    initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                  >
                    <motion.div
                      className="text-4xl"
                      animate={{ opacity: [0.3, 0.7, 0.3] }}
                      transition={{ duration: 2, repeat: Infinity }}
                    >
                      🔒
                    </motion.div>
                    <div className="text-center">
                      <p className="text-[11px] font-bold tracking-[0.3em] text-[#00FF41]/30 mb-2">
                        DATOS ENCRIPTADOS
                      </p>
                      <p className="text-[10px] text-[#00FF41]/18 tracking-wider">
                        Completa {selected.missionName} para desbloquear este archivo
                      </p>
                    </div>
                    <div className="border border-[#00FF41]/10 px-6 py-3 text-center max-w-xs">
                      <p className="text-[9px] tracking-widest text-[#00FF41]/20">
                        DAKI: &quot;Aún no tienes autorización para acceder a este nivel de inteligencia. Completa la misión primero.&quot;
                      </p>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}
