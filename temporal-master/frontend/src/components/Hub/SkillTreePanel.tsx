'use client'

import { useRef, useState, useEffect, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Check, Zap, Lock, X, BookOpen, Trophy, ChevronRight } from 'lucide-react'

// ─── Umbrales DDA ─────────────────────────────────────────────────────────────
// Ajustables sin tocar el render. Refleja cuántas misiones completan cada nodo.

const THRESHOLDS = {
  BASICO_DONE:        45,  // misiones para completar Básico   (~24% de 190)
  MEDIO_DONE:         95,  // misiones para completar Medio    (~50%)
  AVANZADO_DONE:     140,  // misiones para completar Avanzado (~74%)
  BRANCHES_UNLOCK:    95,  // misiones para desbloquear ramas  (= completar Medio)
} as const

// ─── Tipos ─────────────────────────────────────────────────────────────────────

type NodeState = 'completed' | 'active' | 'locked'

interface CoreNode { id: number; label: string; sublabel: string; state: NodeState }
interface SpecCard  { id: string; icon: string; title: string; tag: string; branchId: string; jobs: string[]; unlockAt: number }
interface NodeBrief { missions: number; xpRange: string; concepts: string[] }

// ─── Datos estáticos ───────────────────────────────────────────────────────────

const BASE_NODES: Omit<CoreNode, 'state'>[] = [
  { id: 1, label: 'Básico',   sublabel: 'Fundamentos'           },
  { id: 2, label: 'Medio',    sublabel: 'Estructuras y Lógica'  },
  { id: 3, label: 'Avanzado', sublabel: 'Algoritmos y OOP'      },
  { id: 4, label: 'Expert',   sublabel: 'Patrones y Producción' },
]

const SPEC_CARDS: SpecCard[] = [
  { id: 'auto', icon: '⚙', branchId: 'auto', title: 'Automatización y Scripting',  tag: 'Scripts · CLI · Bots',           jobs: ['DevOps Engineer', 'SRE', 'Backend Dev'],          unlockAt: 150 },
  { id: 'qa',   icon: '⬡', branchId: 'qa',   title: 'Testing y QA',               tag: 'Pytest · Playwright · CI',        jobs: ['QA Engineer', 'SDET', 'Test Automation'],         unlockAt: 160 },
  { id: 'api',  icon: '◈', branchId: 'api',  title: 'APIs y Backend',             tag: 'FastAPI · Django · REST',         jobs: ['Backend Developer', 'API Engineer', 'Full Stack'], unlockAt: 165 },
  { id: 'data', icon: '◉', branchId: 'data', title: 'Data Science y Análisis',    tag: 'Pandas · NumPy · Visualización',  jobs: ['Data Analyst', 'Data Scientist', 'BI Developer'],  unlockAt: 170 },
  { id: 'ai',   icon: '◬', branchId: 'ai',   title: 'Inteligencia Artificial',    tag: 'ML · Modelos base',               jobs: ['ML Engineer', 'AI Developer', 'Data Scientist'],   unlockAt: 180 },
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
              <p className="text-[11px] tracking-[0.45em] mb-1" style={{ color: accentColor.replace('1)', '0.65)') }}>
                MÓDULO {String(nodeIdx + 1).padStart(2, '0')} // PYTHON CORE
              </p>
              <h3 className="text-lg font-black tracking-[0.25em] uppercase"
                style={{ color: accentColor, textShadow: `0 0 12px ${accentColor.replace('1)', '0.40)')}` }}>
                {node.label}
              </h3>
              <p className="text-xs tracking-wider mt-0.5" style={{ color: accentColor.replace('1)', '0.70)') }}>
                {node.sublabel}
              </p>
            </div>
            <button onClick={onClose}
              className="text-gray-400 hover:text-gray-200 transition-colors mt-0.5">
              <X size={16} />
            </button>
          </div>

          {/* Estado */}
          <div className="flex gap-2 mb-4">
            {isCompleted && (
              <span className="text-[11px] tracking-[0.35em] font-black px-2 py-0.5 border"
                style={{ color: 'rgba(6,182,212,0.90)', borderColor: 'rgba(6,182,212,0.35)', background: 'rgba(6,182,212,0.08)' }}>
                ✓ COMPLETADO
              </span>
            )}
            {node.state === 'active' && (
              <motion.span className="text-[11px] tracking-[0.35em] font-black px-2 py-0.5 border"
                style={{ color: 'rgba(16,185,129,1)', borderColor: 'rgba(16,185,129,0.45)', background: 'rgba(16,185,129,0.10)' }}
                animate={{ opacity: [0.7, 1, 0.7] }} transition={{ duration: 1.3, repeat: Infinity }}>
                ▶ EN CURSO
              </motion.span>
            )}
            {isLocked && (
              <span className="text-[11px] tracking-[0.35em] font-black px-2 py-0.5 border"
                style={{ color: 'rgba(245,158,11,0.75)', borderColor: 'rgba(245,158,11,0.32)', background: 'rgba(245,158,11,0.06)' }}>
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
                style={{ borderColor: accentColor.replace('1)', '0.18)'), background: accentColor.replace('1)', '0.06)') }}>
                <div className="flex items-center gap-1.5 mb-1" style={{ color: accentColor.replace('1)', '0.70)') }}>
                  {icon}
                  <span className="text-[11px] tracking-[0.35em] font-black">{label}</span>
                </div>
                <p className="text-xs font-black" style={{ color: accentColor.replace('1)', '0.90)') }}>
                  {value}
                </p>
              </div>
            ))}
          </div>

          {/* Conceptos */}
          <div className="mb-4">
            <p className="text-[11px] tracking-[0.45em] mb-2" style={{ color: accentColor.replace('1)', '0.60)') }}>
              CONCEPTOS CUBIERTOS
            </p>
            <ul className="flex flex-col gap-1.5">
              {brief.concepts.map(c => (
                <li key={c} className="flex items-center gap-2">
                  <span style={{ color: accentColor.replace('1)', '0.70)'), fontSize: 10 }}>▸</span>
                  <span className="text-[11px] tracking-wider text-gray-300">{c}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* CTA */}
          {isLocked ? (
            <div className="border px-3 py-2.5 text-center"
              style={{ borderColor: 'rgba(245,158,11,0.22)', background: 'rgba(245,158,11,0.05)' }}>
              <p className="text-xs tracking-[0.25em] text-gray-400">
                Completa <span style={{ color: 'rgba(245,158,11,0.85)' }}>
                  {prevLabel ? `"${prevLabel}"` : 'el módulo anterior'}
                </span> para desbloquear
              </p>
            </div>
          ) : isCompleted ? (
            <motion.button onClick={onGo}
              className="w-full py-2.5 text-[11px] font-black tracking-[0.4em] flex items-center justify-center gap-2 border transition-colors"
              style={{ borderColor: 'rgba(6,182,212,0.40)', color: 'rgba(6,182,212,0.85)', background: 'rgba(6,182,212,0.07)' }}
              whileHover={{ background: 'rgba(6,182,212,0.14)', borderColor: 'rgba(6,182,212,0.70)' }}
              whileTap={{ scale: 0.98 }}>
              ✓ REVISAR MISIONES
              <ChevronRight size={12} />
            </motion.button>
          ) : (
            <motion.button onClick={onGo}
              className="w-full py-2.5 font-black tracking-[0.3em] text-[11px] flex items-center justify-center gap-2 border transition-all"
              style={{ borderColor: 'rgba(16,185,129,0.55)', color: 'rgba(16,185,129,1)', background: 'rgba(16,185,129,0.10)' }}
              whileHover={{ background: 'rgba(16,185,129,0.18)', boxShadow: '0 0 20px rgba(16,185,129,0.22)' }}
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
      className="relative w-full h-full bg-nexo-deep-bg overflow-auto [&::-webkit-scrollbar]:hidden [-ms-overflow-style:none] [scrollbar-width:none]"
    >
      {/* ── Cuadrícula táctica — patrón casi invisible ── */}
      <div className="absolute inset-0 pointer-events-none z-0" style={{
        backgroundImage: `linear-gradient(rgba(6,182,212,0.035) 1px, transparent 1px),
                          linear-gradient(90deg, rgba(6,182,212,0.035) 1px, transparent 1px)`,
        backgroundSize: '32px 32px',
      }} />

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
            <filter id="vein-glow" x="-80%" y="-80%" width="260%" height="260%">
              <feGaussianBlur in="SourceGraphic" stdDeviation="5" result="blur" />
              <feMerge>
                <feMergeNode in="blur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
          </defs>

          {svgPaths.map((d, i) => (
            <g key={i}>
              {/* Halo exterior difuso */}
              <motion.path d={d} fill="none" stroke="#06b6d4" strokeWidth={6}
                strokeLinecap="round" filter="url(#vein-glow)"
                initial={{ pathLength: 0, opacity: 0 }}
                animate={{ pathLength: 1, opacity: 0.18 }}
                transition={{ delay: 0.72 + i * 0.13, duration: 0.85, ease: 'easeOut' }}
              />
              {/* Línea base principal */}
              <motion.path d={d} fill="none" stroke="#06b6d4" strokeWidth={3}
                strokeLinecap="round" filter="url(#vein-glow)"
                initial={{ pathLength: 0, opacity: 0 }}
                animate={{ pathLength: 1, opacity: 0.85 }}
                transition={{ delay: 0.72 + i * 0.13, duration: 0.85, ease: 'easeOut' }}
              />
              {/* S4 — Pulso viajero */}
              <motion.path d={d} fill="none" stroke="#06b6d4" strokeWidth={5}
                strokeLinecap="round" filter="url(#vein-glow)"
                strokeDasharray="18 800"
                animate={{ strokeDashoffset: [820, 0], opacity: [0, 1, 1, 0] }}
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
        <div className="md:w-[210px] shrink-0 flex flex-col items-center gap-5 py-2">

          <motion.div className="text-center"
            initial={{ opacity: 0, y: -6 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.06 }}>
            <p className="text-[6px] tracking-[0.65em] font-mono uppercase mb-1"
              style={{ color: 'rgba(6,182,212,0.55)' }}>Eje Central</p>
            <h3 className="text-[11px] font-black tracking-[0.45em] text-neon-cyan font-mono"
              style={{ textShadow: '0 0 18px rgba(6,182,212,0.70), 0 0 40px rgba(6,182,212,0.25)' }}>
              PYTHON CORE
            </h3>
          </motion.div>

          {/* Nodos */}
          <div className="relative flex flex-col items-center gap-7 w-full">

            {/* Línea vertical base */}
            <div className="absolute top-0 bottom-0 left-1/2 -translate-x-1/2 w-[2px] z-0"
              style={{ background: 'linear-gradient(180deg, transparent 2%, rgba(6,182,212,0.35) 8%, rgba(6,182,212,0.35) 92%, transparent 98%)', boxShadow: '0 0 8px rgba(6,182,212,0.20)' }}
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
                  className={[
                    'relative z-10 flex flex-col items-center gap-2 cursor-pointer group',
                    isLocked ? 'opacity-40' : '',
                  ].filter(Boolean).join(' ')}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: isLocked ? 0.40 : 1, y: 0 }}
                  transition={{ delay: 0.10 + i * 0.09, duration: 0.38, ease: 'easeOut' }}
                  onClick={() => setBriefNodeIdx(i)}
                  title="Ver detalles del módulo"
                >
                  {/* Aura pulsante — solo nodo activo */}
                  {isActive && (
                    <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                      <div className="neon-pulse--emerald rounded-full" style={{ width: 88, height: 88, position: 'absolute' }} />
                    </div>
                  )}

                  {/* Círculo */}
                  <div
                    ref={el => { nodeCircleRefs.current[i] = el }}
                    className={[
                      isActive ? 'w-[72px] h-[72px]' : 'w-[62px] h-[62px]',
                      'rounded-full border-2 flex flex-col items-center justify-center bg-nexo-deep-bg',
                      'transition-transform duration-150 group-hover:scale-105 relative z-10',
                      isCompleted ? 'border-neon-cyan    text-neon-cyan    shadow-glow-cyan'                          : '',
                      isActive    ? 'border-neon-emerald text-neon-emerald shadow-glow-emerald animate-energy-pulse'  : '',
                      isLocked    ? 'border-neon-gold/55 text-gray-400    shadow-glow-gold'                           : '',
                    ].filter(Boolean).join(' ')}
                    style={
                      isCompleted ? { boxShadow: '0 0 22px rgba(6,182,212,1), 0 0 50px rgba(6,182,212,0.45), inset 0 0 18px rgba(6,182,212,0.50)' } :
                      isActive    ? { boxShadow: '0 0 28px rgba(16,185,129,1), 0 0 60px rgba(16,185,129,0.50), inset 0 0 22px rgba(16,185,129,0.55)' } :
                      undefined
                    }
                  >
                    <CoreNodeIcon state={node.state} size={isActive ? 22 : 20} />
                    <span className={[
                      'text-[6px] font-black font-mono tracking-widest mt-0.5',
                      isCompleted ? 'text-neon-cyan'     : '',
                      isActive    ? 'text-neon-emerald'  : '',
                      isLocked    ? 'text-gray-600'      : '',
                    ].filter(Boolean).join(' ')}>
                      {String(node.id).padStart(2, '0')}
                    </span>
                  </div>

                  {/* Etiqueta */}
                  <div className="text-center">
                    <p
                      className={[
                        'text-[10px] font-black tracking-[0.28em] uppercase font-mono',
                        isCompleted ? 'text-neon-cyan'   : '',
                        isActive    ? 'text-neon-emerald' : '',
                        isLocked    ? 'text-neon-gold/70' : '',
                      ].filter(Boolean).join(' ')}
                      style={
                        isCompleted ? { textShadow: '0 0 12px rgba(6,182,212,0.90)' } :
                        isActive    ? { textShadow: '0 0 14px rgba(16,185,129,0.95)' } :
                        undefined
                      }
                    >
                      {node.label}
                    </p>
                    <p className={[
                      'text-[7px] font-mono tracking-wider mt-0.5',
                      isLocked ? 'text-gray-500' : 'text-gray-500',
                    ].filter(Boolean).join(' ')}>{node.sublabel}</p>
                  </div>

                  {/* Badge estado */}
                  {isActive && (
                    <motion.span
                      className="text-[6px] tracking-[0.45em] font-black font-mono px-2.5 py-0.5 border text-neon-emerald"
                      style={{ borderColor: 'rgba(16,185,129,0.70)', background: 'rgba(16,185,129,0.14)', boxShadow: '0 0 10px rgba(16,185,129,0.30)' }}
                      animate={{ opacity: [0.65, 1, 0.65] }} transition={{ duration: 1.3, repeat: Infinity }}>
                      EN CURSO
                    </motion.span>
                  )}
                  {isCompleted && (
                    <span
                      className="text-[6px] tracking-[0.4em] font-black font-mono px-2.5 py-0.5 border text-neon-cyan"
                      style={{ borderColor: 'rgba(6,182,212,0.60)', background: 'rgba(6,182,212,0.12)', boxShadow: '0 0 8px rgba(6,182,212,0.25)' }}>
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
              <span className="text-[6px] font-black text-neon-cyan font-mono" style={{ textShadow: '0 0 8px rgba(6,182,212,0.80)' }}>
                {Math.round((Math.min(completedCount, THRESHOLDS.AVANZADO_DONE) / THRESHOLDS.AVANZADO_DONE) * 100)}%
              </span>
            </div>
            <div className="w-full h-[2px] bg-white/5 overflow-hidden rounded-full">
              <motion.div className="h-full bg-neon-cyan rounded-full"
                style={{ boxShadow: '0 0 10px rgba(6,182,212,0.90), 0 0 20px rgba(6,182,212,0.40)' }}
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
            <p className="text-[6px] tracking-[0.65em] font-mono uppercase mb-1"
              style={{ color: 'rgba(245,158,11,0.50)' }}>
              Arsenal de Especialización
            </p>
            <div className="flex items-end justify-between">
              <h3 className="text-[11px] font-black tracking-[0.35em] font-mono"
                style={{ color: 'rgba(245,158,11,0.90)', textShadow: '0 0 16px rgba(245,158,11,0.35)' }}>
                RAMAS AVANZADAS
              </h3>
              {/* S3 — Contador global de desbloqueo */}
              {!branchesReady ? (
                <motion.span
                  className="text-[7px] font-black tracking-[0.3em] font-mono px-2.5 py-1 border"
                  style={{ color: 'rgba(245,158,11,0.90)', borderColor: 'rgba(245,158,11,0.45)', background: 'rgba(245,158,11,0.10)', boxShadow: '0 0 10px rgba(245,158,11,0.12)' }}
                  animate={{ opacity: [0.7, 1, 0.7] }} transition={{ duration: 1.8, repeat: Infinity }}>
                  🔒 {missionsToUnlock} misión{missionsToUnlock !== 1 ? 'es' : ''} para desbloquear
                </motion.span>
              ) : (
                <span className="text-[7px] font-black tracking-[0.3em] font-mono px-2.5 py-1 border"
                  style={{ color: 'rgba(245,158,11,0.95)', borderColor: 'rgba(245,158,11,0.55)', background: 'rgba(245,158,11,0.12)', boxShadow: '0 0 14px rgba(245,158,11,0.20)' }}>
                  ⚡ LISTAS PARA ACTIVAR
                </span>
              )}
            </div>
          </motion.div>

          {/* Grid de tarjetas */}
          <div className="grid gap-3.5 grid-cols-1 sm:grid-cols-2">
            {SPEC_CARDS.map((card, i) => {
              const cardPct = Math.min(100, Math.round((completedCount / card.unlockAt) * 100))
              const cardRemaining = Math.max(0, card.unlockAt - completedCount)
              return (
              <motion.div key={card.id}
                ref={el => { cardRefs.current[i] = el }}
                className="relative border overflow-hidden"
                style={{
                  borderColor: 'rgba(245,158,11,0.40)',
                  background:  'linear-gradient(135deg, rgba(245,158,11,0.07) 0%, rgba(245,158,11,0.03) 100%)',
                  boxShadow:   '0 0 20px rgba(245,158,11,0.06), inset 0 0 20px rgba(245,158,11,0.03)',
                }}
                initial={{ opacity: 0, x: 18 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.22 + i * 0.07, duration: 0.40, ease: 'easeOut' }}
                whileHover={{
                  borderColor: 'rgba(245,158,11,0.75)',
                  boxShadow:   '0 0 28px rgba(245,158,11,0.18), inset 0 0 20px rgba(245,158,11,0.06)',
                  transition:  { duration: 0.15 },
                }}
              >
                {/* Línea de pulso superior */}
                <motion.div
                  className="absolute top-0 left-0 right-0 h-px pointer-events-none"
                  style={{ background: 'linear-gradient(90deg, transparent, rgba(245,158,11,0.60), transparent)' }}
                  animate={{ opacity: [0.3, 0.9, 0.3] }}
                  transition={{ duration: 2.4, repeat: Infinity, delay: i * 0.35 }}
                />

                {/* Esquinas */}
                {['top-0 left-0 border-t border-l','top-0 right-0 border-t border-r','bottom-0 left-0 border-b border-l','bottom-0 right-0 border-b border-r'].map(cls => (
                  <span key={cls} className={`absolute w-2.5 h-2.5 ${cls}`}
                    style={{ borderColor: 'rgba(245,158,11,0.55)' }} />
                ))}

                {/* Candado pulsante */}
                <div className="absolute top-2.5 right-2.5">
                  <motion.div
                    animate={{ opacity: [0.65, 1, 0.65], filter: ['drop-shadow(0 0 3px rgba(245,158,11,0.4))', 'drop-shadow(0 0 8px rgba(245,158,11,0.8))', 'drop-shadow(0 0 3px rgba(245,158,11,0.4))'] }}
                    transition={{ duration: 2.2, repeat: Infinity, delay: i * 0.30 }}>
                    <Lock size={13} style={{ color: 'rgba(245,158,11,0.85)' }} />
                  </motion.div>
                </div>

                <div className="px-4 py-4">
                  {/* Ícono + título */}
                  <div className="flex items-start gap-3 mb-2.5 pr-7">
                    <motion.span
                      className="text-[26px] leading-none shrink-0 select-none"
                      style={{ color: 'rgba(245,158,11,0.90)', textShadow: '0 0 18px rgba(245,158,11,0.65), 0 0 36px rgba(245,158,11,0.25)' }}
                      animate={{ opacity: [0.75, 1, 0.75] }}
                      transition={{ duration: 3, repeat: Infinity, delay: i * 0.4 }}
                    >
                      {card.icon}
                    </motion.span>
                    <p className="text-[11px] font-black tracking-[0.15em] uppercase font-mono leading-snug"
                      style={{ color: 'rgba(245,158,11,0.97)', textShadow: '0 0 10px rgba(245,158,11,0.40)' }}>
                      {card.title}
                    </p>
                  </div>

                  <p className="text-[8px] tracking-[0.20em] font-mono mb-3.5"
                    style={{ color: 'rgba(245,158,11,0.65)' }}>
                    {card.tag}
                  </p>

                  {/* Roles + barra de desbloqueo individual */}
                  <div className="border px-3 py-2"
                    style={{ borderColor: 'rgba(245,158,11,0.30)', background: 'rgba(245,158,11,0.07)' }}>
                    <p className="text-[8px] tracking-[0.25em] font-mono mb-1.5"
                      style={{ color: 'rgba(245,158,11,0.45)' }}>
                      SALIDAS LABORALES
                    </p>
                    <div className="flex flex-wrap gap-1 mb-2">
                      {card.jobs.map(job => (
                        <span key={job} className="text-[9px] font-mono px-1.5 py-0.5 border"
                          style={{ color: 'rgba(245,158,11,0.75)', borderColor: 'rgba(245,158,11,0.25)', background: 'rgba(245,158,11,0.06)' }}>
                          {job}
                        </span>
                      ))}
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="flex-1 h-[3px] rounded-full overflow-hidden" style={{ background: 'rgba(245,158,11,0.12)' }}>
                        <motion.div className="h-full rounded-full"
                          initial={{ width: 0 }}
                          animate={{ width: `${cardPct}%` }}
                          transition={{ duration: 0.8, ease: 'easeOut', delay: 0.3 + i * 0.06 }}
                          style={{ background: cardPct >= 100 ? 'rgba(245,158,11,0.95)' : 'rgba(245,158,11,0.50)' }}
                        />
                      </div>
                      <span className="text-[8px] font-mono shrink-0" style={{ color: 'rgba(245,158,11,0.55)' }}>
                        {cardRemaining > 0 ? `−${cardRemaining}` : '⚡'}
                      </span>
                    </div>
                  </div>
                </div>
              </motion.div>
              )
            })}
          </div>
        </div>

      </div>
    </div>
  )
}
