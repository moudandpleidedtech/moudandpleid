'use client'

import { useRef, useState, useEffect, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Check, Zap, Lock, X, BookOpen, Trophy, ChevronRight } from 'lucide-react'

// ─── Umbrales DDA ─────────────────────────────────────────────────────────────
// Ajustables sin tocar el render. Refleja cuántas misiones completan cada nodo.

const THRESHOLDS = {
  BASICO_DONE:        5,   // misiones para completar Básico
  MEDIO_DONE:        15,   // misiones para completar Medio
  AVANZADO_DONE:     25,   // misiones para completar Avanzado
  BRANCHES_UNLOCK:   15,   // misiones para desbloquear ramas (= empezar Avanzado)
} as const

// ─── Tipos ─────────────────────────────────────────────────────────────────────

type NodeState = 'completed' | 'active' | 'locked'

interface CoreNode { id: number; label: string; sublabel: string; state: NodeState }
interface SpecCard  { id: string; icon: string; title: string; tag: string; branchId: string }
interface NodeBrief { missions: number; xpRange: string; concepts: string[] }

// ─── Datos estáticos ───────────────────────────────────────────────────────────

const BASE_NODES: Omit<CoreNode, 'state'>[] = [
  { id: 1, label: 'Básico',   sublabel: 'Fundamentos'           },
  { id: 2, label: 'Medio',    sublabel: 'Estructuras y Lógica'  },
  { id: 3, label: 'Avanzado', sublabel: 'Algoritmos y OOP'      },
  { id: 4, label: 'Expert',   sublabel: 'Patrones y Producción' },
]

const SPEC_CARDS: SpecCard[] = [
  { id: 'auto', icon: '⚙', branchId: 'auto', title: 'Automatización y Scripting',       tag: 'Scripts · CLI · Bots'           },
  { id: 'qa',   icon: '⬡', branchId: 'qa',   title: 'Testing y QA',                     tag: 'Core Pytest / Playwright'       },
  { id: 'api',  icon: '◈', branchId: 'api',  title: 'APIs y Backend',                   tag: 'FastAPI / Django'               },
  { id: 'data', icon: '◉', branchId: 'data', title: 'Data Science y Análisis',          tag: 'Pandas · NumPy · Visualización' },
  { id: 'ai',   icon: '◬', branchId: 'ai',   title: 'Inteligencia Artificial Básica',   tag: 'ML · Modelos base'              },
]

// S2 — Contenido del pre-brief por índice de nodo
const NODE_BRIEFS: Record<number, NodeBrief> = {
  0: {
    missions: 8,
    xpRange:  '50–150 XP c/misión',
    concepts: ['Variables y tipos de datos', 'Operadores y expresiones', 'Condicionales (if/elif/else)', 'Bucles for y while', 'Strings y f-strings'],
  },
  1: {
    missions: 10,
    xpRange:  '100–300 XP c/misión',
    concepts: ['Funciones y alcance', 'Listas, tuplas y sets', 'Diccionarios', 'Manejo de errores (try/except)', 'Comprensiones de listas'],
  },
  2: {
    missions: 10,
    xpRange:  '200–500 XP c/misión',
    concepts: ['Clases y objetos (OOP)', 'Herencia y polimorfismo', 'Algoritmos de búsqueda y ordenamiento', 'Recursión y memoización', 'Complejidad algorítmica (Big O)'],
  },
  3: {
    missions: 15,
    xpRange:  '300–800 XP c/misión',
    concepts: ['Design patterns (Factory, Observer)', 'Testing con Pytest', 'Tipado estático (type hints)', 'Decoradores y metaclases', 'Optimización y profiling'],
  },
}

// Conexiones SVG: índice de nodo → índices de tarjeta
const CONNECTIONS = [
  { nodeIdx: 2, cardIdx: 0 },
  { nodeIdx: 2, cardIdx: 1 },
  { nodeIdx: 2, cardIdx: 2 },
  { nodeIdx: 3, cardIdx: 3 },
  { nodeIdx: 3, cardIdx: 4 },
]

// ─── S1: Estado dinámico de nodos ─────────────────────────────────────────────

function deriveNodeState(idx: number, count: number): NodeState {
  if (idx === 0) return count >= THRESHOLDS.BASICO_DONE   ? 'completed' : 'active'
  if (idx === 1) {
    if (count >= THRESHOLDS.MEDIO_DONE)  return 'completed'
    if (count >= THRESHOLDS.BASICO_DONE) return 'active'
    return 'locked'
  }
  if (idx === 2) {
    if (count >= THRESHOLDS.AVANZADO_DONE) return 'completed'
    if (count >= THRESHOLDS.MEDIO_DONE)    return 'active'
    return 'locked'
  }
  // Expert (idx 3)
  if (count >= THRESHOLDS.AVANZADO_DONE) return 'active'
  return 'locked'
}

// ─── Ícono del nodo (Lucide) ───────────────────────────────────────────────────

function CoreNodeIcon({ state, size = 20 }: { state: NodeState; size?: number }) {
  if (state === 'completed') return <Check size={size} strokeWidth={2.5} />
  if (state === 'active')    return <Zap   size={size} strokeWidth={2}   />
  return                            <Lock  size={size - 2} strokeWidth={2} />
}

// ─── S2: Modal de pre-brief ────────────────────────────────────────────────────

function NodeBriefModal({
  nodeIdx,
  node,
  brief,
  onClose,
  onGo,
}: {
  nodeIdx: number
  node:    CoreNode
  brief:   NodeBrief
  onClose: () => void
  onGo:    () => void
}) {
  const isLocked    = node.state === 'locked'
  const isCompleted = node.state === 'completed'
  const prevLabel   = nodeIdx > 0 ? BASE_NODES[nodeIdx - 1].label : null

  const accentColor =
    isCompleted ? 'rgba(6,182,212,1)'    :
    node.state === 'active' ? 'rgba(16,185,129,1)' :
    'rgba(245,158,11,0.6)'

  return (
    <motion.div
      className="fixed inset-0 z-[300] flex items-center justify-center px-4"
      style={{ background: 'rgba(0,0,0,0.75)', backdropFilter: 'blur(6px)' }}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      onClick={onClose}
    >
      <motion.div
        className="relative w-full max-w-sm border overflow-hidden font-mono"
        style={{
          borderColor: accentColor.replace('1)', '0.30)'),
          background:  '#0B1120',
          boxShadow:   `0 0 40px ${accentColor.replace('1)', '0.15)')}`,
        }}
        initial={{ scale: 0.92, y: 12 }}
        animate={{ scale: 1,    y: 0  }}
        exit={{    scale: 0.92, y: 12 }}
        onClick={e => e.stopPropagation()}
      >
        {/* Línea superior pulsante */}
        <motion.div
          className="h-px w-full"
          style={{ background: `linear-gradient(90deg, transparent, ${accentColor.replace('1)', '0.6)')}, transparent)` }}
          animate={{ opacity: [0.4, 1, 0.4] }}
          transition={{ duration: 2, repeat: Infinity }}
        />

        {/* Esquinas */}
        {['top-0 left-0 border-t border-l','top-0 right-0 border-t border-r','bottom-0 left-0 border-b border-l','bottom-0 right-0 border-b border-r'].map(cls => (
          <span key={cls} className={`absolute w-3 h-3 ${cls}`}
            style={{ borderColor: accentColor.replace('1)', '0.40)') }} />
        ))}

        <div className="px-5 py-5">
          {/* Header */}
          <div className="flex items-start justify-between mb-4">
            <div>
              <p className="text-[7px] tracking-[0.55em] mb-1" style={{ color: accentColor.replace('1)', '0.40)') }}>
                MÓDULO {String(nodeIdx + 1).padStart(2, '0')} // PYTHON CORE
              </p>
              <h3 className="text-lg font-black tracking-[0.25em] uppercase"
                style={{ color: accentColor, textShadow: `0 0 12px ${accentColor.replace('1)', '0.40)')}` }}>
                {node.label}
              </h3>
              <p className="text-[9px] tracking-wider mt-0.5" style={{ color: accentColor.replace('1)', '0.50)') }}>
                {node.sublabel}
              </p>
            </div>
            <button onClick={onClose}
              className="text-gray-600 hover:text-gray-400 transition-colors mt-0.5">
              <X size={16} />
            </button>
          </div>

          {/* Estado */}
          <div className="flex gap-2 mb-4">
            {isCompleted && (
              <span className="text-[7px] tracking-[0.4em] font-black px-2 py-0.5 border"
                style={{ color: 'rgba(6,182,212,0.8)', borderColor: 'rgba(6,182,212,0.30)', background: 'rgba(6,182,212,0.06)' }}>
                ✓ COMPLETADO
              </span>
            )}
            {node.state === 'active' && (
              <motion.span className="text-[7px] tracking-[0.4em] font-black px-2 py-0.5 border"
                style={{ color: 'rgba(16,185,129,0.9)', borderColor: 'rgba(16,185,129,0.35)', background: 'rgba(16,185,129,0.07)' }}
                animate={{ opacity: [0.6, 1, 0.6] }} transition={{ duration: 1.3, repeat: Infinity }}>
                ▶ EN CURSO
              </motion.span>
            )}
            {isLocked && (
              <span className="text-[7px] tracking-[0.4em] font-black px-2 py-0.5 border"
                style={{ color: 'rgba(245,158,11,0.55)', borderColor: 'rgba(245,158,11,0.22)', background: 'rgba(245,158,11,0.04)' }}>
                🔒 BLOQUEADO
              </span>
            )}
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 gap-2 mb-4">
            {[
              { icon: <BookOpen size={11} />, label: 'MISIONES', value: `${brief.missions} incursiones` },
              { icon: <Trophy   size={11} />, label: 'RECOMPENSA', value: brief.xpRange },
            ].map(({ icon, label, value }) => (
              <div key={label} className="border px-3 py-2"
                style={{ borderColor: accentColor.replace('1)', '0.12)'), background: accentColor.replace('1)', '0.04)') }}>
                <div className="flex items-center gap-1.5 mb-1" style={{ color: accentColor.replace('1)', '0.50)') }}>
                  {icon}
                  <span className="text-[6px] tracking-[0.4em] font-black">{label}</span>
                </div>
                <p className="text-[8px] font-black" style={{ color: accentColor.replace('1)', '0.75)') }}>
                  {value}
                </p>
              </div>
            ))}
          </div>

          {/* Conceptos */}
          <div className="mb-4">
            <p className="text-[6px] tracking-[0.5em] mb-2" style={{ color: accentColor.replace('1)', '0.35)') }}>
              CONCEPTOS CUBIERTOS
            </p>
            <ul className="flex flex-col gap-1.5">
              {brief.concepts.map(c => (
                <li key={c} className="flex items-center gap-2">
                  <span style={{ color: accentColor.replace('1)', '0.50)'), fontSize: 8 }}>▸</span>
                  <span className="text-[8px] tracking-wider text-gray-400">{c}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* CTA */}
          {isLocked ? (
            <div className="border px-3 py-2.5 text-center"
              style={{ borderColor: 'rgba(245,158,11,0.15)', background: 'rgba(245,158,11,0.03)' }}>
              <p className="text-[7px] tracking-[0.3em] text-gray-600">
                Completa <span style={{ color: 'rgba(245,158,11,0.65)' }}>
                  {prevLabel ? `"${prevLabel}"` : 'el módulo anterior'}
                </span> para desbloquear
              </p>
            </div>
          ) : isCompleted ? (
            <button onClick={onClose}
              className="w-full py-2.5 text-[9px] font-black tracking-[0.4em] border transition-colors"
              style={{ borderColor: 'rgba(6,182,212,0.30)', color: 'rgba(6,182,212,0.70)', background: 'rgba(6,182,212,0.05)' }}>
              ✓ MÓDULO COMPLETADO
            </button>
          ) : (
            <motion.button onClick={onGo}
              className="w-full py-2.5 font-black tracking-[0.3em] text-[9px] flex items-center justify-center gap-2 border transition-all"
              style={{ borderColor: 'rgba(16,185,129,0.50)', color: 'rgba(16,185,129,0.90)', background: 'rgba(16,185,129,0.08)' }}
              whileHover={{ background: 'rgba(16,185,129,0.14)', boxShadow: '0 0 20px rgba(16,185,129,0.18)' }}
              whileTap={{ scale: 0.98 }}>
              <span>IR A MISIONES</span>
              <ChevronRight size={12} />
            </motion.button>
          )}
        </div>
      </motion.div>
    </motion.div>
  )
}

// ─── Componente principal ──────────────────────────────────────────────────────

interface Props {
  completedCount: number
  onNavigate: (path: string) => void
}

export default function SkillTreePanel({ completedCount, onNavigate }: Props) {
  // S1 — nodos con estado calculado
  const derivedNodes: CoreNode[] = BASE_NODES.map((n, i) => ({
    ...n,
    state: deriveNodeState(i, completedCount),
  }))

  // S3 — misiones restantes para desbloquear ramas
  const missionsToUnlock = Math.max(0, THRESHOLDS.BRANCHES_UNLOCK - completedCount)
  const branchesReady    = missionsToUnlock === 0

  // S2 — modal de pre-brief
  const [briefNodeIdx, setBriefNodeIdx] = useState<number | null>(null)

  // SVG refs & state
  const containerRef   = useRef<HTMLDivElement>(null)
  const nodeCircleRefs = useRef<(HTMLDivElement | null)[]>([null, null, null, null])
  const cardRefs       = useRef<(HTMLDivElement | null)[]>([null, null, null, null, null])
  const [svgPaths, setSvgPaths] = useState<string[]>([])
  const [svgDims,  setSvgDims]  = useState({ w: 0, h: 0 })
  const [isMobile, setIsMobile] = useState(false)

  const computePaths = useCallback(() => {
    if (!containerRef.current) return
    const isNarrow = window.matchMedia('(max-width: 767px)').matches
    setIsMobile(isNarrow)
    if (isNarrow) { setSvgPaths([]); return }

    const cRect = containerRef.current.getBoundingClientRect()
    const paths: string[] = []

    for (const conn of CONNECTIONS) {
      const circleEl = nodeCircleRefs.current[conn.nodeIdx]
      const cardEl   = cardRefs.current[conn.cardIdx]
      if (!circleEl || !cardEl) continue

      const nr = circleEl.getBoundingClientRect()
      const kr = cardEl.getBoundingClientRect()

      const sx = nr.right  - cRect.left
      const sy = (nr.top + nr.bottom) / 2 - cRect.top
      const ex = kr.left   - cRect.left
      const ey = (kr.top + kr.bottom) / 2 - cRect.top
      const dx = ex - sx

      paths.push(`M ${sx},${sy} C ${sx + dx * 0.45},${sy} ${ex - dx * 0.45},${ey} ${ex},${ey}`)
    }

    setSvgDims({ w: cRect.width, h: cRect.height })
    setSvgPaths(paths)
  }, [])

  useEffect(() => {
    const t  = setTimeout(computePaths, 420)
    const ro = new ResizeObserver(computePaths)
    if (containerRef.current) ro.observe(containerRef.current)
    return () => { clearTimeout(t); ro.disconnect() }
  }, [computePaths, completedCount])

  return (
    <div ref={containerRef}
      className="relative w-full h-full bg-nexo-bg overflow-auto [&::-webkit-scrollbar]:hidden [-ms-overflow-style:none] [scrollbar-width:none]"
    >

      {/* ── S2: Modal de pre-brief ── */}
      <AnimatePresence>
        {briefNodeIdx !== null && (
          <NodeBriefModal
            nodeIdx={briefNodeIdx}
            node={derivedNodes[briefNodeIdx]}
            brief={NODE_BRIEFS[briefNodeIdx]}
            onClose={() => setBriefNodeIdx(null)}
            onGo={() => { setBriefNodeIdx(null); onNavigate('/misiones') }}
          />
        )}
      </AnimatePresence>

      {/* ── S4: SVG — venas de energía + pulso viajero ── */}
      {!isMobile && svgPaths.length > 0 && (
        <svg className="absolute top-0 left-0 pointer-events-none z-0"
          width={svgDims.w} height={svgDims.h}
          style={{ overflow: 'visible' }} aria-hidden="true">
          <defs>
            <filter id="vein-glow" x="-60%" y="-60%" width="220%" height="220%">
              <feGaussianBlur in="SourceGraphic" stdDeviation="3.5" result="blur" />
              <feMerge>
                <feMergeNode in="blur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
          </defs>

          {svgPaths.map((d, i) => (
            <g key={i}>
              {/* Línea base */}
              <motion.path d={d} fill="none" stroke="#06b6d4" strokeWidth={2}
                strokeLinecap="round" filter="url(#vein-glow)"
                initial={{ pathLength: 0, opacity: 0 }}
                animate={{ pathLength: 1, opacity: 0.45 }}
                transition={{ delay: 0.72 + i * 0.13, duration: 0.85, ease: 'easeOut' }}
              />
              {/* S4 — Pulso viajero */}
              <motion.path d={d} fill="none" stroke="#06b6d4" strokeWidth={5}
                strokeLinecap="round" filter="url(#vein-glow)"
                strokeDasharray="18 800"
                animate={{ strokeDashoffset: [820, 0], opacity: [0, 0.80, 0.80, 0] }}
                transition={{
                  strokeDashoffset: { duration: 2.2, repeat: Infinity, ease: 'linear', delay: 1.4 + i * 0.25 },
                  opacity:          { duration: 2.2, repeat: Infinity, ease: 'linear', delay: 1.4 + i * 0.25, times: [0, 0.1, 0.9, 1] },
                }}
              />
            </g>
          ))}
        </svg>
      )}

      <div className="relative z-10 flex flex-col md:flex-row gap-6 lg:gap-10 p-5 sm:p-6 min-h-full">

        {/* ─── IZQUIERDA: Core Track ─── */}
        <div className="md:w-[196px] shrink-0 flex flex-col items-center gap-5 py-2">

          <motion.div className="text-center"
            initial={{ opacity: 0, y: -6 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.06 }}>
            <p className="text-[6px] tracking-[0.65em] text-neon-cyan/28 font-mono uppercase mb-1">Eje Central</p>
            <h3 className="text-[11px] font-black tracking-[0.45em] text-neon-cyan font-mono"
              style={{ textShadow: '0 0 12px rgba(6,182,212,0.50)' }}>
              PYTHON CORE
            </h3>
          </motion.div>

          {/* Nodos */}
          <div className="relative flex flex-col items-center gap-7 w-full">

            {/* Línea vertical base */}
            <div className="absolute top-0 bottom-0 left-1/2 -translate-x-1/2 w-[2px] z-0"
              style={{ background: 'linear-gradient(180deg, transparent 2%, rgba(6,182,212,0.18) 8%, rgba(6,182,212,0.18) 92%, transparent 98%)' }}
            />

            {/* S4 — Pulso viajero sobre la línea vertical */}
            <motion.div
              className="absolute left-1/2 -translate-x-1/2 z-0 rounded-full"
              style={{
                width: 2, height: 20,
                background: 'linear-gradient(180deg, transparent, rgba(6,182,212,0.90), transparent)',
                boxShadow: '0 0 8px rgba(6,182,212,0.70)',
              }}
              animate={{ top: ['-2%', '102%'] }}
              transition={{ duration: 2.8, repeat: Infinity, ease: 'easeInOut', repeatDelay: 0.6 }}
            />

            {derivedNodes.map((node, i) => {
              const isCompleted = node.state === 'completed'
              const isActive    = node.state === 'active'
              const isLocked    = node.state === 'locked'

              return (
                <motion.div key={node.id}
                  className="relative z-10 flex flex-col items-center gap-2 cursor-pointer group"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1,  y: 0  }}
                  transition={{ delay: 0.10 + i * 0.09, duration: 0.38, ease: 'easeOut' }}
                  onClick={() => setBriefNodeIdx(i)}
                  title="Ver detalles del módulo"
                >
                  {/* Círculo */}
                  <div
                    ref={el => { nodeCircleRefs.current[i] = el }}
                    className={[
                      isActive ? 'w-[68px] h-[68px]' : 'w-[60px] h-[60px]',
                      'rounded-full border-2 flex flex-col items-center justify-center bg-nexo-bg',
                      'transition-transform duration-150 group-hover:scale-105',
                      isCompleted ? 'border-neon-cyan    text-neon-cyan    shadow-glow-cyan'                          : '',
                      isActive    ? 'border-neon-emerald text-neon-emerald shadow-glow-emerald animate-energy-pulse'  : '',
                      isLocked    ? 'border-neon-gold/40 text-gray-500    shadow-glow-gold    opacity-50'             : '',
                    ].filter(Boolean).join(' ')}
                  >
                    <CoreNodeIcon state={node.state} />
                    <span className={[
                      'text-[6px] font-black font-mono tracking-widest mt-0.5',
                      isCompleted ? 'text-neon-cyan/50'    : '',
                      isActive    ? 'text-neon-emerald/55' : '',
                      isLocked    ? 'text-gray-600'        : '',
                    ].filter(Boolean).join(' ')}>
                      {String(node.id).padStart(2, '0')}
                    </span>
                  </div>

                  {/* Etiqueta */}
                  <div className="text-center">
                    <p className={[
                      'text-[9px] font-black tracking-[0.28em] uppercase font-mono',
                      isCompleted ? 'text-neon-cyan'    : '',
                      isActive    ? 'text-neon-emerald'  : '',
                      isLocked    ? 'text-gray-500'      : '',
                    ].filter(Boolean).join(' ')}>
                      {node.label}
                    </p>
                    <p className="text-[7px] text-gray-600 font-mono tracking-wider mt-0.5">{node.sublabel}</p>
                  </div>

                  {/* Badge estado */}
                  {isActive && (
                    <motion.span
                      className="text-[5px] tracking-[0.45em] font-black font-mono px-2 py-0.5 border border-neon-emerald/45 text-neon-emerald"
                      style={{ background: 'rgba(16,185,129,0.08)' }}
                      animate={{ opacity: [0.5, 1, 0.5] }} transition={{ duration: 1.3, repeat: Infinity }}>
                      EN CURSO
                    </motion.span>
                  )}
                  {isCompleted && (
                    <span className="text-[5px] tracking-[0.4em] font-black font-mono px-2 py-0.5 border border-neon-cyan/25 text-neon-cyan/45"
                      style={{ background: 'rgba(6,182,212,0.05)' }}>
                      COMPLETADO
                    </span>
                  )}
                </motion.div>
              )
            })}
          </div>

          {/* Barra de progreso */}
          <motion.div className="w-full max-w-[140px] pt-3"
            style={{ borderTop: '1px solid rgba(6,182,212,0.10)' }}
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.60 }}>
            <div className="flex justify-between mb-1">
              <span className="text-[5px] tracking-[0.4em] text-gray-700 font-mono uppercase">Dominio</span>
              <span className="text-[6px] font-black text-neon-cyan/45 font-mono">
                {Math.round((Math.min(completedCount, THRESHOLDS.AVANZADO_DONE) / THRESHOLDS.AVANZADO_DONE) * 100)}%
              </span>
            </div>
            <div className="w-full h-[2px] bg-white/5 overflow-hidden rounded-full">
              <motion.div className="h-full bg-neon-cyan rounded-full"
                style={{ boxShadow: '0 0 6px rgba(6,182,212,0.55)' }}
                initial={{ width: 0 }}
                animate={{ width: `${Math.round((Math.min(completedCount, THRESHOLDS.AVANZADO_DONE) / THRESHOLDS.AVANZADO_DONE) * 100)}%` }}
                transition={{ delay: 0.80, duration: 0.9, ease: 'easeOut' }}
              />
            </div>
          </motion.div>
        </div>

        {/* ─── DERECHA: Tarjetas de Especialización ─── */}
        <div className="flex-1 flex flex-col justify-center gap-4 min-w-0">

          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.15 }}>
            <p className="text-[6px] tracking-[0.65em] text-neon-gold/28 font-mono uppercase mb-1">
              Arsenal de Especialización
            </p>
            <div className="flex items-end justify-between">
              <h3 className="text-[11px] font-black tracking-[0.35em] font-mono"
                style={{ color: 'rgba(245,158,11,0.55)' }}>
                RAMAS AVANZADAS
              </h3>
              {/* S3 — Contador global de desbloqueo */}
              {!branchesReady ? (
                <motion.span
                  className="text-[7px] font-black tracking-[0.3em] font-mono px-2 py-0.5 border"
                  style={{ color: 'rgba(245,158,11,0.60)', borderColor: 'rgba(245,158,11,0.22)', background: 'rgba(245,158,11,0.04)' }}
                  animate={{ opacity: [0.6, 1, 0.6] }} transition={{ duration: 2, repeat: Infinity }}>
                  🔒 {missionsToUnlock} misión{missionsToUnlock !== 1 ? 'es' : ''} para desbloquear
                </motion.span>
              ) : (
                <span className="text-[7px] font-black tracking-[0.3em] font-mono px-2 py-0.5 border"
                  style={{ color: 'rgba(245,158,11,0.70)', borderColor: 'rgba(245,158,11,0.35)', background: 'rgba(245,158,11,0.06)' }}>
                  ⚡ LISTAS PARA ACTIVAR
                </span>
              )}
            </div>
          </motion.div>

          {/* Grid de tarjetas */}
          <div className="grid gap-2.5 grid-cols-1 sm:grid-cols-2">
            {SPEC_CARDS.map((card, i) => (
              <motion.div key={card.id}
                ref={el => { cardRefs.current[i] = el }}
                className="relative border overflow-hidden cursor-pointer"
                style={{
                  borderColor: 'rgba(245,158,11,0.18)',
                  background:  'rgba(255,255,255,0.04)',
                  backdropFilter: 'blur(10px)',
                  WebkitBackdropFilter: 'blur(10px)',
                }}
                initial={{ opacity: 0, x: 18 }}
                animate={{ opacity: 0.65, x: 0 }}
                transition={{ delay: 0.22 + i * 0.07, duration: 0.40, ease: 'easeOut' }}
                whileHover={{ opacity: 0.85, transition: { duration: 0.14 } }}
                // S5 — navega a /misiones con filtro de rama
                onClick={() => onNavigate(`/misiones?branch=${card.branchId}`)}
              >
                {/* Esquinas */}
                {['top-0 left-0 border-t border-l','top-0 right-0 border-t border-r','bottom-0 left-0 border-b border-l','bottom-0 right-0 border-b border-r'].map(cls => (
                  <span key={cls} className={`absolute w-2 h-2 ${cls}`}
                    style={{ borderColor: 'rgba(245,158,11,0.32)' }} />
                ))}

                {/* Candado dorado pulsante */}
                <div className="absolute top-2.5 right-2.5">
                  <motion.div
                    animate={{ opacity: [0.45, 0.85, 0.45] }}
                    transition={{ duration: 2.6, repeat: Infinity, delay: i * 0.30 }}>
                    <Lock size={14} style={{ color: 'rgba(245,158,11,0.70)', filter: 'drop-shadow(0 0 5px rgba(245,158,11,0.55))' }} />
                  </motion.div>
                </div>

                <div className="px-3.5 py-3">
                  {/* Ícono + título */}
                  <div className="flex items-start gap-2.5 mb-2 pr-6">
                    <span className="text-[17px] leading-none shrink-0"
                      style={{ color: 'rgba(245,158,11,0.38)', textShadow: '0 0 8px rgba(245,158,11,0.18)' }}>
                      {card.icon}
                    </span>
                    <p className="text-[9px] font-black tracking-[0.18em] uppercase font-mono leading-snug"
                      style={{ color: 'rgba(245,158,11,0.55)' }}>
                      {card.title}
                    </p>
                  </div>

                  <p className="text-[7px] tracking-[0.15em] text-gray-600 font-mono mb-2.5">{card.tag}</p>

                  {/* S3 — Badge de countdown individual */}
                  <div className="border px-2 py-1"
                    style={{ borderColor: 'rgba(245,158,11,0.12)', background: 'rgba(245,158,11,0.03)' }}>
                    {!branchesReady ? (
                      <p className="text-[6px] tracking-[0.18em] font-mono leading-relaxed"
                        style={{ color: 'rgba(245,158,11,0.42)' }}>
                        <span className="font-black" style={{ color: 'rgba(245,158,11,0.60)' }}>
                          Faltan {missionsToUnlock} misión{missionsToUnlock !== 1 ? 'es'  : ''}
                        </span>
                        {' · '}Python Core (Nivel Avanzado)
                      </p>
                    ) : (
                      <p className="text-[6px] tracking-[0.18em] font-mono leading-relaxed font-black"
                        style={{ color: 'rgba(245,158,11,0.65)' }}>
                        ⚡ Completa Python Core (Avanzado) para activar
                      </p>
                    )}
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>

      </div>
    </div>
  )
}
