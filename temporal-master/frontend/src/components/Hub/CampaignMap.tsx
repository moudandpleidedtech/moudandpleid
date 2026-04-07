'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { motion, AnimatePresence } from 'framer-motion'
import { useUserStore } from '@/store/userStore'

// ─── Types ────────────────────────────────────────────────────────────────────

interface MapNode {
  id: string
  title: string
  subtitle: string
  level_range: string
  is_boss: boolean
  /** Texto que aparece en el modal de bloqueo: "Superar el Boss de X" */
  required_boss_name?: string
  nav_path: string
}

interface CampaignZone {
  codex_id: string
  title: string
  subtitle: string
  color: string
  icon: string
  status: 'active' | 'coming_soon'
  nodes: MapNode[]
}

type NodeState = 'completed' | 'unlocked' | 'locked'

interface NodeProgress {
  completed: boolean
  unlocked: boolean
  boss_completed: boolean
}

type ProgressMap = Record<string, Record<string, NodeProgress>>

interface LockedModalState {
  node: MapNode
  zone: CampaignZone
}

// ─── Estructura del Mapa de Campaña ───────────────────────────────────────────
// Los IDs de nodos deben coincidir con _NODES en campaign.py (backend).

const ZONES: CampaignZone[] = [
  {
    codex_id: 'python_core',
    title: 'PYTHON CORE',
    subtitle: 'Protocolo de Iniciación — S00 a S07',
    color: '#00FF41',
    icon: '⬡',
    status: 'active',
    nodes: [
      {
        id: 's00_s03',
        title: 'INICIACIÓN',
        subtitle: 'Tutorial · Variables · Flujo · Ciclos',
        level_range: 'L00 – L30',
        is_boss: false,
        nav_path: '/sector/0',
      },
      {
        id: 's04_s07',
        title: 'ESTRUCTURAS & FUNCIONES',
        subtitle: 'While · Listas · Funciones · Comprensiones',
        level_range: 'L31 – L66',
        is_boss: true,
        required_boss_name: 'Boss de Iniciación (L30)',
        nav_path: '/sector/4',
      },
    ],
  },
  {
    codex_id: 'python_avanzado',
    title: 'OPERACIONES AVANZADAS',
    subtitle: 'Práctica de profundidad — S08 a S13',
    color: '#00E5FF',
    icon: '◈',
    status: 'active',
    nodes: [
      {
        id: 's08_s10',
        title: 'CADENAS & BÓVEDA',
        subtitle: 'Strings · Lógica compleja · Contratos',
        level_range: 'L67 – L96',
        is_boss: false,
        required_boss_name: 'Boss NEXUS-06 (L59)',
        nav_path: '/sector/8',
      },
      {
        id: 's11_s13',
        title: 'PRÁCTICA INTENSIVA',
        subtitle: '30 misiones de consolidación táctica',
        level_range: 'L97 – L126',
        is_boss: false,
        required_boss_name: 'Boss del Sector 10',
        nav_path: '/sector/11',
      },
    ],
  },
  {
    codex_id: 'python_elite',
    title: 'ESPECIALIZACIÓN DE ÉLITE',
    subtitle: 'Módulos · OOP · Errores · Proyecto — S14 a S18',
    color: '#FFB800',
    icon: '▣',
    status: 'active',
    nodes: [
      {
        id: 's14_s15',
        title: 'MÓDULOS & ARCHIVOS',
        subtitle: 'stdlib · math · datetime · File I/O · CSV',
        level_range: 'L127 – L142',
        is_boss: true,
        required_boss_name: 'Boss Práctica Intensiva (L126)',
        nav_path: '/sector/14',
      },
      {
        id: 's16_s18',
        title: 'OOP & PROYECTO FINAL',
        subtitle: 'Clases · Herencia · Errores · Boss Integrador',
        level_range: 'L143 – L161',
        is_boss: true,
        required_boss_name: 'Boss ARCHIVO-01 (L142)',
        nav_path: '/sector/16',
      },
    ],
  },
  {
    codex_id: 'protocolos_elite',
    title: 'PROTOCOLOS DE ÉLITE',
    subtitle: 'Debug · Entrevistas · Predicción — S19 a S21',
    color: '#BD00FF',
    icon: '◉',
    status: 'active',
    nodes: [
      {
        id: 's19_debug',
        title: 'MODO DEBUG',
        subtitle: 'Bugs reales: NameError · TypeError · Off-by-one',
        level_range: 'L162 – L169',
        is_boss: false,
        required_boss_name: 'Boss NEXUS-FINAL (L161)',
        nav_path: '/sector/19',
      },
      {
        id: 's20_interview',
        title: 'PROTOCOLO DE ENTREVISTA',
        subtitle: 'Two Sum · Palíndromo · Greedy · Boss Screening',
        level_range: 'L170 – L179',
        is_boss: false,
        required_boss_name: 'Boss Debug (L169)',
        nav_path: '/sector/20',
      },
      {
        id: 's21_predict',
        title: 'SISTEMA DE PREDICCIÓN',
        subtitle: 'Leer código · Predecir output · Sin ejecutar',
        level_range: 'L180 – L189',
        is_boss: true,
        required_boss_name: 'Boss Interview (L179)',
        nav_path: '/sector/21',
      },
    ],
  },
]

// ─── Fallback de progreso — solo el primer sector desbloqueado ────────────────

function buildFallbackProgress(): ProgressMap {
  const p: ProgressMap = {}
  for (const zone of ZONES) {
    p[zone.codex_id] = {}
    zone.nodes.forEach((node, i) => {
      p[zone.codex_id][node.id] = {
        completed: false,
        unlocked: zone.codex_id === 'python_core' && i === 0,
        boss_completed: false,
      }
    })
  }
  return p
}

// ─── Helpers ──────────────────────────────────────────────────────────────────

function getNodeState(
  zone: CampaignZone,
  node: MapNode,
  progress: ProgressMap,
): NodeState {
  if (zone.status === 'coming_soon') return 'locked'
  const zp = progress[zone.codex_id]?.[node.id]
  if (!zp) return 'locked'
  if (zp.completed || zp.boss_completed) return 'completed'
  if (zp.unlocked) return 'unlocked'
  return 'locked'
}

function getZoneCompletion(zone: CampaignZone, progress: ProgressMap) {
  if (!zone.nodes.length) return { done: 0, total: 0 }
  const zp = progress[zone.codex_id] ?? {}
  const done = zone.nodes.filter(
    (n) => zp[n.id]?.completed || zp[n.id]?.boss_completed,
  ).length
  return { done, total: zone.nodes.length }
}

// ─── Conector vertical entre nodos ────────────────────────────────────────────

function NodeConnector({
  upperState,
  color,
}: {
  upperState: NodeState
  color: string
}) {
  const isActive   = upperState === 'completed'
  const isCurrent  = upperState === 'unlocked'

  if (isActive) {
    return (
      <div className="flex justify-center" style={{ height: '28px' }}>
        <motion.div
          className="w-px"
          style={{ background: color, height: '28px', opacity: 0.7 }}
          animate={{ scaleY: [1, 1.05, 1], opacity: [0.5, 0.8, 0.5] }}
          transition={{ duration: 2, repeat: Infinity, ease: 'easeInOut' }}
        />
      </div>
    )
  }

  if (isCurrent) {
    return (
      <div className="flex justify-center" style={{ height: '28px' }}>
        <motion.div
          className="w-px"
          style={{ height: '28px' }}
          animate={{
            background: [
              `${color}33`,
              `${color}88`,
              `${color}33`,
            ],
          }}
          transition={{ duration: 1.5, repeat: Infinity, ease: 'easeInOut' }}
        />
      </div>
    )
  }

  return (
    <div
      className="flex justify-center"
      style={{ height: '28px' }}
    >
      <div
        className="w-px"
        style={{ height: '28px', background: '#1f1f1f' }}
      />
    </div>
  )
}

// ─── Tarjeta de nodo individual ───────────────────────────────────────────────

function CampaignNodeCard({
  node,
  zone,
  state,
  index,
  onClickLocked,
  onClickUnlocked,
}: {
  node: MapNode
  zone: CampaignZone
  state: NodeState
  index: number
  onClickLocked: () => void
  onClickUnlocked: () => void
}) {
  const color      = zone.color
  const isDone     = state === 'completed'
  const isUnlocked = state === 'unlocked'
  const isLocked   = state === 'locked'

  const borderColor = isDone
    ? `${color}99`
    : isUnlocked
      ? `${color}66`
      : 'rgba(255,255,255,0.05)'

  const bg = isDone
    ? `linear-gradient(135deg, ${color}0a 0%, rgba(0,10,5,0.96) 100%)`
    : isUnlocked
      ? `linear-gradient(135deg, ${color}07 0%, rgba(10,10,5,0.96) 100%)`
      : 'rgba(8,8,8,0.95)'

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.06, duration: 0.3, ease: 'easeOut' }}
      className="relative"
    >
      {/* Pulso de fondo para nodos desbloqueados */}
      {isUnlocked && (
        <motion.div
          className="absolute inset-0 rounded pointer-events-none"
          animate={{
            boxShadow: [
              `0 0 0 0 ${color}00`,
              `0 0 0 6px ${color}22`,
              `0 0 0 0 ${color}00`,
            ],
          }}
          transition={{ duration: 2.2, repeat: Infinity, ease: 'easeOut' }}
          style={{ borderRadius: '4px' }}
        />
      )}

      <motion.button
        onClick={isLocked ? onClickLocked : onClickUnlocked}
        className="relative w-full text-left focus:outline-none"
        style={{
          background: bg,
          border: `1px solid ${borderColor}`,
          borderRadius: '4px',
          cursor: isLocked ? 'pointer' : 'pointer',
          opacity: isLocked ? 0.45 : 1,
        }}
        whileHover={
          isLocked
            ? { opacity: 0.6 }
            : { scale: 1.02, y: -1 }
        }
        whileTap={{ scale: 0.98 }}
      >
        {/* Línea de acento superior (boss / completado) */}
        {(node.is_boss || isDone) && (
          <div
            className="absolute top-0 left-0 right-0 h-[2px] rounded-t"
            style={{
              background: isDone
                ? `linear-gradient(90deg, transparent, ${color}, transparent)`
                : node.is_boss
                  ? `linear-gradient(90deg, transparent, ${color}44, transparent)`
                  : 'none',
              opacity: isDone ? 0.8 : 0.5,
            }}
          />
        )}

        <div className="px-3 pt-3 pb-2.5">
          {/* Fila superior */}
          <div className="flex items-start justify-between gap-2 mb-1.5">
            <div className="flex items-center gap-1.5 min-w-0">
              {/* Ícono de estado */}
              <span style={{ fontSize: '11px', flexShrink: 0 }}>
                {isDone    ? <span style={{ color }}         >✓</span>  : null}
                {isUnlocked ? (
                  <motion.span
                    style={{ color, fontFamily: 'monospace' }}
                    animate={{ opacity: [1, 0.3, 1] }}
                    transition={{ duration: 1.4, repeat: Infinity }}
                  >▶</motion.span>
                ) : null}
                {isLocked  ? <span style={{ color: '#2a2a2a' }}>▷</span>  : null}
              </span>

              {/* Título */}
              <span
                className="text-[11px] font-bold tracking-widest truncate"
                style={{
                  fontFamily: 'monospace',
                  color: isDone ? color : isUnlocked ? color : '#2e2e2e',
                  textShadow: isDone ? `0 0 8px ${color}88` : 'none',
                }}
              >
                {node.title}
              </span>
            </div>

            {/* Badge BOSS */}
            {node.is_boss && (
              <span
                className="text-[8px] tracking-widest px-1.5 py-0.5 shrink-0"
                style={{
                  fontFamily: 'monospace',
                  border: `1px solid ${isDone ? color + '88' : '#333'}`,
                  color: isDone ? color : '#333',
                  background: isDone ? `${color}10` : 'transparent',
                  borderRadius: '2px',
                }}
              >
                BOSS
              </span>
            )}
          </div>

          {/* Subtítulo */}
          <p
            className="text-[10px] leading-tight mb-2"
            style={{
              fontFamily: 'monospace',
              color: isDone ? `${color}77` : isUnlocked ? `${color}55` : '#222',
            }}
          >
            {isLocked && node.required_boss_name
              ? <span style={{ color: '#2a2a2a' }}>🔒 BLOQUEADO</span>
              : node.subtitle
            }
          </p>

          {/* Range */}
          <div className="flex items-center justify-between">
            <span
              className="text-[9px] tracking-widest"
              style={{
                fontFamily: 'monospace',
                color: isDone ? `${color}55` : isUnlocked ? `${color}44` : '#1a1a1a',
              }}
            >
              {node.level_range}
            </span>

            {isLocked && (
              <span
                className="text-[8px] tracking-wider"
                style={{ fontFamily: 'monospace', color: '#FF2D7866' }}
              >
                VER RUTA →
              </span>
            )}
          </div>
        </div>
      </motion.button>
    </motion.div>
  )
}

// ─── Columna de disciplina ─────────────────────────────────────────────────────

function ZoneColumn({
  zone,
  progress,
  onNodeLocked,
  onNodeUnlocked,
}: {
  zone: CampaignZone
  progress: ProgressMap
  onNodeLocked:   (node: MapNode, zone: CampaignZone) => void
  onNodeUnlocked: (node: MapNode, zone: CampaignZone) => void
}) {
  const color = zone.color
  const { done, total } = getZoneCompletion(zone, progress)
  const pct = total > 0 ? (done / total) * 100 : 0

  return (
    <div
      className="flex flex-col min-w-[200px] flex-1"
      style={{ maxWidth: '240px' }}
    >
      {/* Cabecera de zona */}
      <div
        className="p-3 mb-3 rounded"
        style={{
          background: zone.status === 'coming_soon'
            ? 'rgba(255,255,255,0.02)'
            : `${color}08`,
          border: `1px solid ${zone.status === 'coming_soon' ? '#1a1a1a' : color + '33'}`,
        }}
      >
        <div className="flex items-center gap-2 mb-1">
          <span style={{ color: zone.status === 'coming_soon' ? '#222' : color, fontSize: '16px' }}>
            {zone.icon}
          </span>
          <span
            className="text-[11px] font-black tracking-widest"
            style={{
              fontFamily: 'monospace',
              color: zone.status === 'coming_soon' ? '#1e1e1e' : color,
              textShadow: zone.status === 'coming_soon' ? 'none' : `0 0 8px ${color}55`,
            }}
          >
            {zone.title}
          </span>
        </div>

        <p
          className="text-[9px] tracking-wider mb-2"
          style={{
            fontFamily: 'monospace',
            color: zone.status === 'coming_soon' ? '#151515' : `${color}55`,
          }}
        >
          {zone.status === 'coming_soon' ? 'CLASIFICADO — PRÓXIMAMENTE' : zone.subtitle}
        </p>

        {/* Barra de progreso */}
        {zone.status === 'active' && total > 0 && (
          <div className="flex items-center gap-2">
            <div
              className="flex-1 h-[2px] rounded-full overflow-hidden"
              style={{ background: 'rgba(255,255,255,0.05)' }}
            >
              <motion.div
                className="h-full rounded-full"
                initial={{ width: 0 }}
                animate={{ width: `${pct}%` }}
                transition={{ duration: 0.9, ease: 'easeOut', delay: 0.3 }}
                style={{ background: pct === 100 ? color : `${color}77` }}
              />
            </div>
            <span
              className="text-[8px] shrink-0"
              style={{ fontFamily: 'monospace', color: `${color}55` }}
            >
              {done}/{total}
            </span>
          </div>
        )}
      </div>

      {/* Nodos */}
      {zone.status === 'coming_soon' ? (
        <div
          className="flex-1 flex items-center justify-center rounded"
          style={{
            minHeight: '160px',
            border: '1px dashed #111',
            background: 'rgba(255,255,255,0.01)',
          }}
        >
          <div className="text-center">
            <motion.p
              className="text-[20px] mb-2"
              style={{ color: '#111' }}
              animate={{ opacity: [0.3, 0.7, 0.3] }}
              transition={{ duration: 3, repeat: Infinity, ease: 'easeInOut' }}
            >
              {zone.icon}
            </motion.p>
            <p
              className="text-[9px] tracking-widest"
              style={{ fontFamily: 'monospace', color: '#1a1a1a' }}
            >
              ACCESO DENEGADO
            </p>
          </div>
        </div>
      ) : (
        <div className="flex flex-col">
          {zone.nodes.map((node, i) => {
            const state = getNodeState(zone, node, progress)
            const prevState = i > 0
              ? getNodeState(zone, zone.nodes[i - 1], progress)
              : 'unlocked'

            return (
              <div key={node.id}>
                {i > 0 && (
                  <NodeConnector upperState={prevState} color={color} />
                )}
                <CampaignNodeCard
                  node={node}
                  zone={zone}
                  state={state}
                  index={i}
                  onClickLocked={() => onNodeLocked(node, zone)}
                  onClickUnlocked={() => onNodeUnlocked(node, zone)}
                />
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}

// ─── Modal: nodo bloqueado ────────────────────────────────────────────────────

function LockedNodeModal({
  info,
  onClose,
}: {
  info: LockedModalState
  onClose: () => void
}) {
  const { node, zone } = info
  const color = zone.color

  return (
    <motion.div
      className="fixed inset-0 z-50 flex items-center justify-center p-4"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      style={{ background: 'rgba(0,0,0,0.88)' }}
      onClick={onClose}
    >
      {/* Scanlines overlay */}
      <div
        className="absolute inset-0 pointer-events-none"
        style={{
          background: 'repeating-linear-gradient(0deg, transparent, transparent 3px, rgba(0,255,65,0.008) 3px, rgba(0,255,65,0.008) 4px)',
        }}
      />

      <motion.div
        className="relative w-full max-w-sm"
        initial={{ scale: 0.92, y: 16 }}
        animate={{ scale: 1, y: 0 }}
        exit={{ scale: 0.92, y: 8 }}
        transition={{ duration: 0.2, ease: 'easeOut' }}
        onClick={(e) => e.stopPropagation()}
        style={{
          background: '#060606',
          border: `1px solid ${color}33`,
          borderRadius: '6px',
          boxShadow: `0 0 40px ${color}15, 0 0 80px rgba(0,0,0,0.8)`,
        }}
      >
        {/* Header */}
        <div
          className="px-5 pt-5 pb-4"
          style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}
        >
          <div className="flex items-center justify-between mb-1">
            <span
              className="text-[9px] tracking-[0.3em]"
              style={{ fontFamily: 'monospace', color: '#FF2D7888' }}
            >
              SECTOR BLOQUEADO
            </span>
            <button
              onClick={onClose}
              className="text-[11px] opacity-40 hover:opacity-80 transition-opacity"
              style={{ fontFamily: 'monospace', color: '#fff' }}
            >
              ✕
            </button>
          </div>

          <h2
            className="text-base font-black tracking-widest"
            style={{ fontFamily: 'monospace', color }}
          >
            {node.title}
          </h2>
          <p
            className="text-[11px] mt-0.5"
            style={{ fontFamily: 'monospace', color: `${color}66` }}
          >
            {node.subtitle} · {node.level_range}
          </p>
        </div>

        {/* Cuerpo */}
        <div className="px-5 py-4">
          <p
            className="text-[10px] tracking-widest mb-3"
            style={{ fontFamily: 'monospace', color: '#ffffff33' }}
          >
            PROTOCOLO DE ACCESO
          </p>

          {/* Prerequisito */}
          {node.required_boss_name ? (
            <div
              className="flex items-start gap-3 p-3 rounded mb-4"
              style={{
                background: 'rgba(255,45,120,0.06)',
                border: '1px solid rgba(255,45,120,0.2)',
              }}
            >
              <span style={{ color: '#FF2D78', fontSize: '14px', marginTop: '1px' }}>⊘</span>
              <div>
                <p
                  className="text-[10px] tracking-wider font-bold mb-0.5"
                  style={{ fontFamily: 'monospace', color: '#FF2D78' }}
                >
                  ACCESO DENEGADO
                </p>
                <p
                  className="text-[11px] leading-relaxed"
                  style={{ fontFamily: 'monospace', color: '#ffffff66' }}
                >
                  Requiere:{' '}
                  <span
                    style={{ color: '#FF6B35', fontWeight: 'bold' }}
                  >
                    Superar el Boss de {node.required_boss_name}
                  </span>
                </p>
              </div>
            </div>
          ) : (
            <div
              className="flex items-start gap-3 p-3 rounded mb-4"
              style={{
                background: `${color}08`,
                border: `1px solid ${color}22`,
              }}
            >
              <span style={{ color, fontSize: '14px' }}>◉</span>
              <p
                className="text-[11px] leading-relaxed"
                style={{ fontFamily: 'monospace', color: '#ffffff66' }}
              >
                Completa los prerequisites para desbloquear este sector.
              </p>
            </div>
          )}

          {/* Mensaje táctico de DAKI */}
          <p
            className="text-[10px] leading-relaxed italic"
            style={{ fontFamily: 'monospace', color: '#ffffff22' }}
          >
            &quot;El Nexo detecta entrenamiento previo incompleto. Neutraliza las
            incursiones faltantes antes de solicitar acceso a este sector.&quot;
            <span style={{ color: `${color}44` }}> — DAKI</span>
          </p>
        </div>

        {/* Footer */}
        <div
          className="px-5 pb-5"
          style={{ borderTop: '1px solid rgba(255,255,255,0.04)' }}
        >
          <motion.button
            onClick={onClose}
            className="w-full mt-4 py-2.5 text-[11px] tracking-[0.2em] font-bold"
            style={{
              fontFamily: 'monospace',
              color,
              border: `1px solid ${color}44`,
              background: `${color}0a`,
              borderRadius: '3px',
            }}
            whileHover={{ background: `${color}18`, borderColor: `${color}88` }}
            whileTap={{ scale: 0.98 }}
          >
            ENTENDIDO — REANUDAR ENTRENAMIENTO
          </motion.button>
        </div>
      </motion.div>
    </motion.div>
  )
}

// ─── Componente principal ─────────────────────────────────────────────────────

export default function CampaignMap() {
  const router = useRouter()
  const { userId } = useUserStore()

  const [progress, setProgress]     = useState<ProgressMap>(buildFallbackProgress)
  const [loading,  setLoading]      = useState(true)
  const [lockedModal, setLockedModal] = useState<LockedModalState | null>(null)

  useEffect(() => {
    const uid = userId
    if (!uid) {
      setLoading(false)
      return
    }

    const API = process.env.NEXT_PUBLIC_API_URL ?? ''
    const controller = new AbortController()

    fetch(`${API}/api/v1/campaign/map?user_id=${uid}`, { signal: controller.signal })
      .then((r) => {
        if (!r.ok) throw new Error('no campaign endpoint')
        return r.json() as Promise<{ zones: ProgressMap }>
      })
      .then((data) => {
        setProgress(data.zones)
        setLoading(false)
      })
      .catch((e) => {
        if (e.name !== 'AbortError') setLoading(false)
      })

    return () => controller.abort()
  }, [userId])

  const handleLockedNode = (node: MapNode, zone: CampaignZone) => {
    setLockedModal({ node, zone })
  }

  const handleUnlockedNode = (node: MapNode, _zone: CampaignZone) => {
    router.push(node.nav_path)
  }

  return (
    <div
      className="w-full min-h-screen"
      style={{ background: '#0A0A0A', color: '#00FF41' }}
    >
      {/* Scanlines + grid táctica */}
      <div
        className="pointer-events-none fixed inset-0 z-0"
        style={{
          background: [
            'repeating-linear-gradient(0deg, transparent, transparent 39px, rgba(0,255,65,0.025) 39px, rgba(0,255,65,0.025) 40px)',
            'repeating-linear-gradient(90deg, transparent, transparent 39px, rgba(0,255,65,0.015) 39px, rgba(0,255,65,0.015) 40px)',
          ].join(','),
        }}
      />
      <div
        className="pointer-events-none fixed inset-0 z-0"
        style={{
          background: 'repeating-linear-gradient(0deg, transparent, transparent 3px, rgba(0,0,0,0.15) 3px, rgba(0,0,0,0.15) 4px)',
        }}
      />

      <div className="relative z-10 max-w-[1400px] mx-auto px-4 py-8">

        {/* ── Header ── */}
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.35 }}
          className="mb-8"
        >
          <p
            className="text-[9px] tracking-[0.4em] mb-1"
            style={{ fontFamily: 'monospace', color: '#00FF4144' }}
          >
            NEXO DAKI · MAPA DE CAMPAÑA
          </p>
          <div className="flex items-end justify-between flex-wrap gap-4">
            <h1
              className="text-2xl sm:text-3xl font-black tracking-widest"
              style={{
                fontFamily: 'monospace',
                color: '#00FF41',
                textShadow: '0 0 30px rgba(0,255,65,0.35)',
              }}
            >
              [ ÁRBOL DE PROGRESIÓN TÁCTICA ]
            </h1>

            {loading && (
              <motion.p
                className="text-[10px] tracking-widest"
                style={{ fontFamily: 'monospace', color: '#00FF4155' }}
                animate={{ opacity: [0.4, 1, 0.4] }}
                transition={{ duration: 1.2, repeat: Infinity }}
              >
                SINCRONIZANDO NEXO...
              </motion.p>
            )}
          </div>

          <div
            className="mt-4 h-px"
            style={{ background: 'linear-gradient(90deg, #00FF4130, transparent)' }}
          />
        </motion.div>

        {/* ── Grid de disciplinas ── */}
        <div
          className="flex gap-5 overflow-x-auto pb-8"
          style={{ scrollbarWidth: 'thin', scrollbarColor: '#00FF4122 transparent' }}
        >
          <AnimatePresence>
            {ZONES.map((zone, zi) => (
              <motion.div
                key={zone.codex_id}
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: zi * 0.08, duration: 0.35, ease: 'easeOut' }}
                className="flex-1 min-w-[200px]"
                style={{ maxWidth: '240px' }}
              >
                <ZoneColumn
                  zone={zone}
                  progress={progress}
                  onNodeLocked={handleLockedNode}
                  onNodeUnlocked={handleUnlockedNode}
                />
              </motion.div>
            ))}
          </AnimatePresence>
        </div>

        {/* ── Leyenda ── */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8 }}
          className="flex flex-wrap gap-6 justify-center mt-2"
        >
          {[
            { color: '#00FF41', icon: '✓',  label: 'COMPLETADO' },
            { color: '#FFC700', icon: '▶',  label: 'DISPONIBLE' },
            { color: '#2a2a2a', icon: '▷',  label: 'BLOQUEADO' },
            { color: '#FF6B35', icon: 'BOSS', label: 'BOSS BATTLE' },
          ].map(({ color, icon, label }) => (
            <div key={label} className="flex items-center gap-2">
              <span style={{ color, fontSize: '11px', fontFamily: 'monospace' }}>
                {icon}
              </span>
              <span
                className="text-[9px] tracking-widest"
                style={{ fontFamily: 'monospace', color: '#ffffff33' }}
              >
                {label}
              </span>
            </div>
          ))}
        </motion.div>

      </div>

      {/* ── Modal de nodo bloqueado ── */}
      <AnimatePresence>
        {lockedModal && (
          <LockedNodeModal
            info={lockedModal}
            onClose={() => setLockedModal(null)}
          />
        )}
      </AnimatePresence>
    </div>
  )
}
