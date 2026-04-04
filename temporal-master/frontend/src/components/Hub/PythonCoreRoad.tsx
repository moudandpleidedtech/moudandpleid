'use client'

import { motion } from 'framer-motion'

// ─── Tipos ─────────────────────────────────────────────────────────────────────

type NodeState = 'completed' | 'active' | 'locked'

interface SkillNode {
  id: number
  label: string
  sublabel: string
  description: string
  state: NodeState
}

// ─── Datos del eje Python Core ─────────────────────────────────────────────────

const PYTHON_CORE_NODES: SkillNode[] = [
  {
    id:          1,
    label:       'Básico',
    sublabel:    'Fundamentos',
    description: 'Variables, tipos de datos y control de flujo',
    state:       'completed',
  },
  {
    id:          2,
    label:       'Medio',
    sublabel:    'Estructuras y Lógica',
    description: 'Funciones, colecciones y manejo de errores',
    state:       'active',
  },
  {
    id:          3,
    label:       'Avanzado',
    sublabel:    'Algoritmos y OOP',
    description: 'Programación orientada a objetos y algoritmos',
    state:       'locked',
  },
  {
    id:          4,
    label:       'Expert',
    sublabel:    'Patrones y Producción',
    description: 'Design patterns, testing y código de producción',
    state:       'locked',
  },
]

// ─── Paletas por estado ────────────────────────────────────────────────────────

const STATE_COLORS: Record<NodeState, {
  border: string; bg: string; glow: string
  text: string; dim: string; desc: string
}> = {
  completed: {
    border: 'rgba(0,255,65,0.75)',
    bg:     'rgba(0,255,65,0.10)',
    glow:   '0 0 18px rgba(0,255,65,0.40), 0 0 36px rgba(0,255,65,0.14)',
    text:   '#00FF41',
    dim:    'rgba(0,255,65,0.50)',
    desc:   'rgba(0,255,65,0.25)',
  },
  active: {
    border: 'rgba(0,255,65,0.95)',
    bg:     'rgba(0,255,65,0.07)',
    glow:   '0 0 24px rgba(0,255,65,0.60), 0 0 48px rgba(0,255,65,0.22)',
    text:   '#00FF41',
    dim:    'rgba(0,255,65,0.65)',
    desc:   'rgba(0,255,65,0.30)',
  },
  locked: {
    border: 'rgba(255,255,255,0.09)',
    bg:     'rgba(255,255,255,0.015)',
    glow:   'none',
    text:   'rgba(255,255,255,0.20)',
    dim:    'rgba(255,255,255,0.12)',
    desc:   'rgba(255,255,255,0.07)',
  },
}

// ─── Conector vertical entre nodos ────────────────────────────────────────────

function VerticalConnector({ filled }: { filled: boolean }) {
  return (
    <div className="flex justify-center" style={{ height: 24, width: '100%' }}>
      <div className="relative flex flex-col items-center" style={{ width: 36 }}>
        {/* Punto superior en el conector */}
        <div
          className="w-px flex-1"
          style={filled
            ? {
                background: 'linear-gradient(180deg, rgba(0,255,65,0.55), rgba(0,255,65,0.20))',
                boxShadow:  '0 0 4px rgba(0,255,65,0.25)',
              }
            : {
                background: 'repeating-linear-gradient(180deg, rgba(255,255,255,0.10) 0px, rgba(255,255,255,0.10) 3px, transparent 3px, transparent 7px)',
              }
          }
        />
      </div>
    </div>
  )
}

// ─── Tarjeta de un nodo ────────────────────────────────────────────────────────

function NodeCard({ node, index }: { node: SkillNode; index: number }) {
  const s          = STATE_COLORS[node.state]
  const isActive   = node.state === 'active'
  const isCompleted = node.state === 'completed'
  const isLocked   = node.state === 'locked'

  return (
    <motion.div
      className="relative border overflow-hidden w-full"
      style={{
        borderColor: s.border,
        background:  s.bg,
      }}
      initial={{ opacity: 0, x: -16 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: 0.18 + index * 0.10, duration: 0.40 }}
    >
      {/* Pulso superior — activo */}
      {isActive && (
        <motion.div
          className="absolute top-0 left-0 right-0 h-px pointer-events-none"
          style={{ background: `linear-gradient(90deg, transparent, ${s.border}, transparent)` }}
          animate={{ opacity: [0.3, 1, 0.3] }}
          transition={{ duration: 1.8, repeat: Infinity }}
        />
      )}

      {/* Glow animado — activo */}
      {isActive && (
        <motion.div
          className="absolute inset-0 pointer-events-none"
          animate={{
            boxShadow: [
              '0 0 18px rgba(0,255,65,0.20) inset',
              '0 0 32px rgba(0,255,65,0.40) inset',
              '0 0 18px rgba(0,255,65,0.20) inset',
            ],
          }}
          transition={{ duration: 2, repeat: Infinity, ease: 'easeInOut' }}
        />
      )}

      {/* Esquinas decorativas — solo activo y completado */}
      {(isCompleted || isActive) && (
        <>
          <span className="absolute top-0 left-0  w-2.5 h-2.5 border-t border-l" style={{ borderColor: s.border }} />
          <span className="absolute top-0 right-0 w-2.5 h-2.5 border-t border-r" style={{ borderColor: s.border }} />
          <span className="absolute bottom-0 left-0  w-2.5 h-2.5 border-b border-l" style={{ borderColor: s.border }} />
          <span className="absolute bottom-0 right-0 w-2.5 h-2.5 border-b border-r" style={{ borderColor: s.border }} />
        </>
      )}

      <div className="px-4 py-3.5 flex items-center gap-4">

        {/* ── Ícono circular ── */}
        <div className="relative shrink-0">
          {/* Halo pulsante — activo/completado */}
          {(isActive || isCompleted) && (
            <motion.div
              className="absolute inset-0 rounded-full"
              style={{ border: `1px solid ${s.border}`, borderRadius: '50%' }}
              animate={isActive
                ? { scale: [1, 1.65, 1], opacity: [0.4, 0, 0.4] }
                : { scale: [1, 1.30, 1], opacity: [0.2, 0, 0.2] }
              }
              transition={{ duration: isActive ? 1.5 : 2.5, repeat: Infinity, ease: 'easeOut' }}
            />
          )}

          <motion.div
            className="w-10 h-10 rounded-full flex items-center justify-center relative z-10"
            style={{
              border:     `1.5px solid ${s.border}`,
              background: s.bg,
              boxShadow:  isActive
                ? undefined
                : (isCompleted ? s.glow : 'none'),
            }}
            animate={isActive
              ? { boxShadow: [
                    '0 0 16px rgba(0,255,65,0.45)',
                    '0 0 30px rgba(0,255,65,0.75)',
                    '0 0 16px rgba(0,255,65,0.45)',
                  ] }
              : {}
            }
            transition={isActive ? { duration: 1.8, repeat: Infinity, ease: 'easeInOut' } : {}}
          >
            {isCompleted && (
              <span style={{ color: '#00FF41', textShadow: '0 0 10px rgba(0,255,65,1)', fontSize: 16, lineHeight: 1 }}>
                ✓
              </span>
            )}
            {isActive && (
              <motion.span
                style={{ color: '#00FF41', textShadow: '0 0 10px rgba(0,255,65,1)', fontSize: 11, lineHeight: 1 }}
                animate={{ opacity: [0.55, 1, 0.55] }}
                transition={{ duration: 1.0, repeat: Infinity }}
              >
                ▶
              </motion.span>
            )}
            {isLocked && (
              <span style={{ fontSize: 13, lineHeight: 1 }}>🔒</span>
            )}
          </motion.div>

          {/* Número de secuencia */}
          <span
            className="absolute -bottom-0.5 -right-0.5 text-[6px] font-black font-mono leading-none"
            style={{ color: s.dim }}
          >
            {String(node.id).padStart(2, '0')}
          </span>
        </div>

        {/* ── Texto del nodo ── */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between gap-2 mb-0.5">
            <p
              className="text-[11px] font-black tracking-[0.3em] uppercase font-mono leading-tight"
              style={{
                color:      s.text,
                textShadow: isActive || isCompleted ? `0 0 10px ${s.text}66` : 'none',
              }}
            >
              {node.label}
            </p>

            {/* Badge estado */}
            {isCompleted && (
              <span
                className="text-[6px] tracking-[0.35em] font-black font-mono px-1.5 py-0.5 border shrink-0"
                style={{
                  color:       'rgba(0,255,65,0.55)',
                  borderColor: 'rgba(0,255,65,0.22)',
                  background:  'rgba(0,255,65,0.04)',
                }}
              >
                ✓ COMPLETADO
              </span>
            )}
            {isActive && (
              <motion.span
                className="text-[6px] tracking-[0.35em] font-black font-mono px-1.5 py-0.5 border shrink-0"
                style={{
                  color:       '#00FF41',
                  borderColor: 'rgba(0,255,65,0.55)',
                  background:  'rgba(0,255,65,0.10)',
                  textShadow:  '0 0 8px rgba(0,255,65,0.6)',
                }}
                animate={{ opacity: [0.6, 1, 0.6] }}
                transition={{ duration: 1.2, repeat: Infinity }}
              >
                ▶ ACTIVO
              </motion.span>
            )}
            {isLocked && (
              <span
                className="text-[6px] tracking-[0.35em] font-black font-mono px-1.5 py-0.5 border shrink-0"
                style={{
                  color:       'rgba(255,255,255,0.15)',
                  borderColor: 'rgba(255,255,255,0.07)',
                  background:  'rgba(255,255,255,0.02)',
                }}
              >
                BLOQUEADO
              </span>
            )}
          </div>

          <p
            className="text-[8px] tracking-[0.2em] font-mono"
            style={{ color: s.dim }}
          >
            {node.sublabel}
          </p>
          <p
            className="text-[7px] tracking-[0.1em] font-mono mt-1 leading-relaxed"
            style={{ color: s.desc }}
          >
            {node.description}
          </p>
        </div>
      </div>
    </motion.div>
  )
}

// ─── Componente principal ──────────────────────────────────────────────────────

export default function PythonCoreRoad() {
  const completedCount = PYTHON_CORE_NODES.filter(n => n.state === 'completed').length
  const progressPct    = Math.round((completedCount / PYTHON_CORE_NODES.length) * 100)

  return (
    <div className="h-full flex flex-col overflow-y-auto [&::-webkit-scrollbar]:hidden [-ms-overflow-style:none] [scrollbar-width:none]">
      <div className="flex flex-col flex-1 max-w-sm mx-auto w-full px-6 py-6">

        {/* ── Header del eje ── */}
        <motion.div
          className="mb-6 text-center"
          initial={{ opacity: 0, y: -8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.10, duration: 0.4 }}
        >
          <p className="text-[7px] tracking-[0.7em] text-[#00FF41]/22 mb-2 font-mono uppercase">
            Árbol de Habilidades
          </p>

          <div className="flex items-center justify-center gap-2 mb-1">
            <motion.span
              className="text-[9px] font-black tracking-[0.55em] font-mono"
              style={{ color: 'rgba(0,255,65,0.55)', textShadow: '0 0 8px rgba(0,255,65,0.4)' }}
              animate={{ opacity: [0.6, 1, 0.6] }}
              transition={{ duration: 2.2, repeat: Infinity }}
            >
              EJE //
            </motion.span>
            <span
              className="text-lg font-black tracking-[0.35em] font-mono"
              style={{ color: '#00FF41', textShadow: '0 0 16px rgba(0,255,65,0.55), 0 0 40px rgba(0,255,65,0.20)' }}
            >
              PYTHON CORE
            </span>
          </div>

          <p className="text-[7px] tracking-[0.4em] text-[#00FF41]/20 font-mono mb-4">
            RUTA PRINCIPAL · FORMACIÓN ACTIVA
          </p>

          {/* Divisor con pulso */}
          <motion.div
            className="h-px mx-auto"
            style={{
              width:      '80%',
              background: 'linear-gradient(90deg, transparent, rgba(0,255,65,0.40), transparent)',
            }}
            animate={{ opacity: [0.35, 0.85, 0.35] }}
            transition={{ duration: 2.5, repeat: Infinity }}
          />
        </motion.div>

        {/* ── Timeline vertical de nodos ── */}
        <div className="flex flex-col items-stretch flex-1">
          {PYTHON_CORE_NODES.map((node, i) => {
            const isLast        = i === PYTHON_CORE_NODES.length - 1
            const nextIsUnlocked = !isLast && PYTHON_CORE_NODES[i + 1].state !== 'locked'

            return (
              <div key={node.id} className="flex flex-col">
                <NodeCard node={node} index={i} />
                {!isLast && <VerticalConnector filled={nextIsUnlocked} />}
              </div>
            )
          })}
        </div>

        {/* ── Barra de progreso del eje ── */}
        <motion.div
          className="mt-6 pt-5"
          style={{ borderTop: '1px solid rgba(0,255,65,0.08)' }}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.75 }}
        >
          <div className="flex items-center justify-between mb-2">
            <span className="text-[7px] tracking-[0.4em] font-mono" style={{ color: 'rgba(0,255,65,0.22)' }}>
              DOMINIO DEL EJE
            </span>
            <span className="text-[8px] tracking-[0.3em] font-black font-mono" style={{ color: 'rgba(0,255,65,0.50)' }}>
              {progressPct}%
            </span>
          </div>
          <div className="w-full h-0.5 overflow-hidden" style={{ background: 'rgba(0,255,65,0.07)' }}>
            <motion.div
              className="h-full"
              style={{ background: '#00FF41', boxShadow: '0 0 6px rgba(0,255,65,0.55)' }}
              initial={{ width: 0 }}
              animate={{ width: `${progressPct}%` }}
              transition={{ delay: 0.95, duration: 1.0, ease: 'easeOut' }}
            />
          </div>
          <div className="flex justify-between mt-1.5">
            <span className="text-[6px] tracking-widest font-mono" style={{ color: 'rgba(0,255,65,0.16)' }}>
              {completedCount}/{PYTHON_CORE_NODES.length} NODOS
            </span>
            <span className="text-[6px] tracking-widest font-mono" style={{ color: 'rgba(0,255,65,0.16)' }}>
              {PYTHON_CORE_NODES.length - completedCount} BLOQUEADOS
            </span>
          </div>
        </motion.div>

      </div>
    </div>
  )
}
