'use client'

import { motion } from 'framer-motion'
import { Check, Zap, Lock } from 'lucide-react'

// ─── Tipos ─────────────────────────────────────────────────────────────────────

type NodeState = 'completed' | 'active' | 'locked'

interface TrackNode {
  id:       number
  label:    string
  sublabel: string
  state:    NodeState
}

// ─── Datos del track ───────────────────────────────────────────────────────────

const NODES: TrackNode[] = [
  { id: 1, label: 'Básico',   sublabel: 'Fundamentos',           state: 'completed' },
  { id: 2, label: 'Medio',    sublabel: 'Estructuras y Lógica',  state: 'active'    },
  { id: 3, label: 'Avanzado', sublabel: 'Algoritmos y OOP',      state: 'locked'    },
  { id: 4, label: 'Expert',   sublabel: 'Patrones y Producción', state: 'locked'    },
]

// ─── Icono por estado (Lucide React) ──────────────────────────────────────────

function NodeIcon({ state }: { state: NodeState }) {
  if (state === 'completed') return <Check   size={26} strokeWidth={2.5} />
  if (state === 'active')    return <Zap     size={26} strokeWidth={2}   />
  return                            <Lock    size={22} strokeWidth={2}   />
}

// ─── Nodo circular ────────────────────────────────────────────────────────────

function TrackNode({ node, index }: { node: TrackNode; index: number }) {
  const isCompleted = node.state === 'completed'
  const isActive    = node.state === 'active'
  const isLocked    = node.state === 'locked'

  return (
    <motion.div
      className="relative z-10 flex flex-col items-center gap-2.5"
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.12 + index * 0.10, duration: 0.40, ease: 'easeOut' }}
    >
      {/* ── Círculo del nodo ── */}
      <div
        className={[
          // Tamaño — activo es más grande para resaltar
          isActive ? 'w-24 h-24' : 'w-20 h-20',
          'rounded-full border-2 flex flex-col items-center justify-center bg-nexo-bg',
          // Estilos por estado
          isCompleted ? 'border-neon-cyan   text-neon-cyan    shadow-glow-cyan'                              : '',
          isActive    ? 'border-neon-emerald text-neon-emerald shadow-glow-emerald animate-energy-pulse'     : '',
          isLocked    ? 'border-neon-gold/40 text-gray-500    shadow-glow-gold    opacity-50'                : '',
        ].filter(Boolean).join(' ')}
      >
        <NodeIcon state={node.state} />

        {/* Número de secuencia */}
        <span
          className={[
            'text-[7px] font-black tracking-widest font-mono mt-0.5',
            isCompleted ? 'text-neon-cyan/50'    : '',
            isActive    ? 'text-neon-emerald/60'  : '',
            isLocked    ? 'text-gray-600'         : '',
          ].filter(Boolean).join(' ')}
        >
          {String(node.id).padStart(2, '0')}
        </span>
      </div>

      {/* ── Etiqueta ── */}
      <div className="text-center">
        <p
          className={[
            'text-[11px] font-black tracking-[0.3em] uppercase font-mono',
            isCompleted ? 'text-neon-cyan'    : '',
            isActive    ? 'text-neon-emerald'  : '',
            isLocked    ? 'text-gray-500'      : '',
          ].filter(Boolean).join(' ')}
        >
          {node.label}
        </p>
        <p className="text-[8px] tracking-[0.2em] text-gray-600 font-mono mt-0.5">
          {node.sublabel}
        </p>
      </div>

      {/* Badge "ACTIVO" — solo para el nodo activo */}
      {isActive && (
        <motion.span
          className="text-[6px] tracking-[0.45em] font-black font-mono px-2 py-0.5 border border-neon-emerald/50 text-neon-emerald bg-neon-emerald/10"
          animate={{ opacity: [0.55, 1, 0.55] }}
          transition={{ duration: 1.3, repeat: Infinity }}
        >
          EN CURSO
        </motion.span>
      )}

      {/* Badge "COMPLETADO" — solo para el nodo completado */}
      {isCompleted && (
        <span className="text-[6px] tracking-[0.35em] font-black font-mono px-2 py-0.5 border border-neon-cyan/30 text-neon-cyan/50 bg-neon-cyan/5">
          COMPLETADO
        </span>
      )}
    </motion.div>
  )
}

// ─── Componente principal ──────────────────────────────────────────────────────

export default function PythonCoreTrack() {
  return (
    <div className="relative flex flex-col items-center gap-8 py-8 px-6 bg-nexo-bg text-white w-full h-full overflow-y-auto [&::-webkit-scrollbar]:hidden [-ms-overflow-style:none] [scrollbar-width:none]">

      {/* ── Línea vertical conectora — detrás de los nodos (z-0) ── */}
      <div
        className="absolute top-0 bottom-0 left-1/2 -translate-x-1/2 w-[2px] z-0"
        style={{
          background: 'linear-gradient(180deg, transparent 2%, rgba(6,182,212,0.20) 8%, rgba(6,182,212,0.20) 92%, transparent 98%)',
        }}
      />

      {/* ── Header ── */}
      <motion.div
        className="relative z-10 text-center"
        initial={{ opacity: 0, y: -8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.06, duration: 0.4 }}
      >
        <p className="text-[7px] tracking-[0.7em] text-neon-cyan/30 font-mono uppercase mb-1.5">
          Árbol de Habilidades
        </p>
        <h3
          className="text-sm font-black tracking-[0.45em] text-neon-cyan font-mono"
          style={{ textShadow: '0 0 14px rgba(6,182,212,0.55)' }}
        >
          PYTHON CORE
        </h3>
        <p className="text-[7px] tracking-[0.35em] text-gray-600 font-mono mt-1">
          RUTA PRINCIPAL · FORMACIÓN ACTIVA
        </p>
      </motion.div>

      {/* ── Nodos ── */}
      {NODES.map((node, i) => (
        <TrackNode key={node.id} node={node} index={i} />
      ))}

      {/* ── Barra de progreso ── */}
      <motion.div
        className="relative z-10 w-full max-w-[180px] pt-4"
        style={{ borderTop: '1px solid rgba(6,182,212,0.10)' }}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.65 }}
      >
        <div className="flex justify-between mb-1.5">
          <span className="text-[6px] tracking-[0.4em] text-gray-700 font-mono uppercase">Dominio</span>
          <span className="text-[7px] font-black text-neon-cyan/50 font-mono">25%</span>
        </div>
        <div className="w-full h-[2px] bg-white/5 overflow-hidden rounded-full">
          <motion.div
            className="h-full bg-neon-cyan rounded-full"
            style={{ boxShadow: '0 0 6px rgba(6,182,212,0.6)' }}
            initial={{ width: 0 }}
            animate={{ width: '25%' }}
            transition={{ delay: 0.85, duration: 0.9, ease: 'easeOut' }}
          />
        </div>
        <div className="flex justify-between mt-1">
          <span className="text-[5px] tracking-widest text-gray-700 font-mono">1/4 NODOS</span>
          <span className="text-[5px] tracking-widest text-gray-700 font-mono">3 BLOQUEADOS</span>
        </div>
      </motion.div>

    </div>
  )
}
