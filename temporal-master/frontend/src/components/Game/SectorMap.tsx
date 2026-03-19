'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { motion, AnimatePresence } from 'framer-motion'

// ─── Tipos ────────────────────────────────────────────────────────────────────

interface DakiStateOut {
  daki_level: 1 | 2 | 3
  mood: string
  label: string
  description: string
  completed_sectors: number
  next_threshold: number | null
}

interface SectorResponse {
  levels: LevelOut[]
  daki_state: DakiStateOut | null
}

interface LevelOut {
  id: string
  title: string
  level_order: number | null
  difficulty: string | null
  difficulty_tier: number
  base_xp_reward: number
  telemetry_goal_time: number | null
  is_project: boolean
  sector_id: number | null
  lore_briefing: string | null
  completed: boolean
  attempts: number
  unlocked: boolean
}

interface SectorMapProps {
  sectorId: number
  /** Ruta destino al hacer click en un nivel — recibe el ID del challenge */
  challengeBasePath?: string
}

// ─── Helpers ──────────────────────────────────────────────────────────────────

const DIFFICULTY_COLOR: Record<string, string> = {
  easy:   '#00FF41',
  medium: '#FFC700',
  hard:   '#FF6B35',
  expert: '#FF2D78',
}

const DIFFICULTY_LABEL: Record<string, string> = {
  easy:   'FÁCIL',
  medium: 'MEDIO',
  hard:   'DIFÍCIL',
  expert: 'EXPERTO',
}

function formatTime(seconds: number | null): string {
  if (!seconds) return '—'
  if (seconds < 60) return `${seconds}s`
  return `${Math.floor(seconds / 60)}m ${seconds % 60}s`
}

function getLevelState(level: LevelOut): 'completed' | 'current' | 'locked' {
  if (level.completed) return 'completed'
  if (level.unlocked)  return 'current'
  return 'locked'
}

// ─── Tarjeta de nivel ─────────────────────────────────────────────────────────

function LevelCard({
  level,
  index,
  onClick,
}: {
  level: LevelOut
  index: number
  onClick: () => void
}) {
  const state      = getLevelState(level)
  const diffColor  = DIFFICULTY_COLOR[level.difficulty ?? 'easy'] ?? '#00FF41'
  const isLocked   = state === 'locked'
  const isCurrent  = state === 'current'
  const isDone     = state === 'completed'

  const borderColor = isDone
    ? 'rgba(0,255,65,0.7)'
    : isCurrent
      ? 'rgba(255,199,0,0.8)'
      : 'rgba(255,255,255,0.06)'

  const glowColor = isDone
    ? '0 0 18px rgba(0,255,65,0.25)'
    : isCurrent
      ? '0 0 18px rgba(255,199,0,0.2)'
      : 'none'

  return (
    <motion.button
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: isLocked ? 0.38 : 1, y: 0 }}
      transition={{ delay: index * 0.045, duration: 0.35, ease: 'easeOut' }}
      whileHover={!isLocked ? { scale: 1.03, y: -2 } : {}}
      whileTap={!isLocked ? { scale: 0.98 } : {}}
      onClick={!isLocked ? onClick : undefined}
      disabled={isLocked}
      className="relative text-left w-full focus:outline-none group"
      style={{
        background: isDone
          ? 'linear-gradient(135deg, rgba(0,255,65,0.06) 0%, rgba(0,10,5,0.95) 100%)'
          : isCurrent
            ? 'linear-gradient(135deg, rgba(255,199,0,0.05) 0%, rgba(10,10,5,0.95) 100%)'
            : 'rgba(10,10,10,0.9)',
        border: `1px solid ${borderColor}`,
        borderRadius: '6px',
        boxShadow: glowColor,
        cursor: isLocked ? 'not-allowed' : 'pointer',
      }}
    >
      {/* ── Fila superior ── */}
      <div className="flex items-start justify-between px-4 pt-4 pb-2">

        {/* Número de nivel */}
        <span
          className="text-2xl font-bold leading-none"
          style={{
            fontFamily: 'monospace',
            color: isDone ? '#00FF41' : isCurrent ? '#FFC700' : '#333',
            textShadow: isDone
              ? '0 0 12px rgba(0,255,65,0.7)'
              : isCurrent
                ? '0 0 12px rgba(255,199,0,0.6)'
                : 'none',
          }}
        >
          {String(level.level_order ?? 0).padStart(2, '0')}
        </span>

        {/* Badges derechos */}
        <div className="flex flex-col items-end gap-1">

          {/* Badge de proyecto */}
          {level.is_project && (
            <span
              className="text-[9px] tracking-widest px-2 py-0.5 rounded"
              style={{
                background: 'rgba(255,199,0,0.12)',
                border: '1px solid rgba(255,199,0,0.5)',
                color: '#FFC700',
                fontFamily: 'monospace',
              }}
            >
              ★ PROYECTO
            </span>
          )}

          {/* Dificultad */}
          {level.difficulty && (
            <span
              className="text-[8px] tracking-widest px-1.5 py-0.5 rounded"
              style={{
                background: `${diffColor}18`,
                border: `1px solid ${diffColor}55`,
                color: diffColor,
                fontFamily: 'monospace',
              }}
            >
              {DIFFICULTY_LABEL[level.difficulty] ?? level.difficulty.toUpperCase()}
            </span>
          )}
        </div>
      </div>

      {/* ── Título ── */}
      <div className="px-4 pb-1">
        <p
          className="text-sm leading-tight line-clamp-2"
          style={{
            fontFamily: 'monospace',
            color: isDone ? '#ccffcc' : isCurrent ? '#fff8e0' : '#555',
          }}
        >
          {level.title}
        </p>
      </div>

      {/* ── Fila inferior ── */}
      <div className="flex items-center justify-between px-4 pb-4 pt-2">
        <span
          className="text-[10px] tracking-wide"
          style={{ fontFamily: 'monospace', color: isDone ? '#00FF4199' : '#3a3a3a' }}
        >
          +{level.base_xp_reward} XP · {formatTime(level.telemetry_goal_time)}
        </span>

        {/* Estado */}
        {isDone && (
          <span style={{ color: '#00FF41', fontSize: '16px' }} title="Completado">✓</span>
        )}
        {isCurrent && (
          <motion.span
            style={{ color: '#FFC700', fontSize: '14px', fontFamily: 'monospace' }}
            animate={{ opacity: [1, 0.3, 1] }}
            transition={{ duration: 1.4, repeat: Infinity }}
          >
            ▶
          </motion.span>
        )}
        {isLocked && (
          <span style={{ color: '#2a2a2a', fontSize: '14px' }}>🔒</span>
        )}
      </div>

      {/* ── Línea de acento inferior (completado / actual) ── */}
      {!isLocked && (
        <div
          className="absolute bottom-0 left-0 right-0 h-[2px] rounded-b"
          style={{
            background: isDone
              ? 'linear-gradient(90deg, transparent, #00FF41, transparent)'
              : 'linear-gradient(90deg, transparent, #FFC700, transparent)',
            opacity: isDone ? 0.6 : 0.4,
          }}
        />
      )}

      {/* ── Escáner hover (solo nivel desbloqueado) ── */}
      {isCurrent && (
        <motion.div
          className="absolute inset-0 rounded pointer-events-none"
          initial={{ opacity: 0 }}
          whileHover={{ opacity: 1 }}
          style={{
            background: 'linear-gradient(180deg, rgba(255,199,0,0.04) 0%, transparent 100%)',
          }}
        />
      )}
    </motion.button>
  )
}

// ─── Barra de progreso del sector ─────────────────────────────────────────────

function SectorProgressBar({ completed, total }: { completed: number; total: number }) {
  const pct = total > 0 ? (completed / total) * 100 : 0
  return (
    <div className="flex items-center gap-3">
      <div
        className="flex-1 h-1 rounded-full overflow-hidden"
        style={{ background: 'rgba(255,255,255,0.06)' }}
      >
        <motion.div
          className="h-full rounded-full"
          initial={{ width: 0 }}
          animate={{ width: `${pct}%` }}
          transition={{ duration: 0.8, ease: 'easeOut' }}
          style={{ background: pct === 100 ? '#00FF41' : 'rgba(0,255,65,0.5)' }}
        />
      </div>
      <span
        className="text-xs shrink-0"
        style={{ fontFamily: 'monospace', color: '#00FF4199' }}
      >
        {completed}/{total}
      </span>
    </div>
  )
}

// ─── Componente principal ─────────────────────────────────────────────────────

export default function SectorMap({
  sectorId,
  challengeBasePath = '/challenge',
}: SectorMapProps) {
  const router   = useRouter()
  const [levels, setLevels]       = useState<LevelOut[]>([])
  const [dakiState, setDakiState] = useState<DakiStateOut | null>(null)
  const [loading, setLoading]     = useState(true)
  const [error, setError]         = useState<string | null>(null)

  // userId desde Zustand — solo en cliente para evitar SSR mismatch
  const [userId, setUserId] = useState<string | null>(null)
  useEffect(() => {
    try {
      const raw = localStorage.getItem('pq-user')
      if (raw) {
        const parsed = JSON.parse(raw)
        setUserId(parsed?.state?.userId ?? null)
      }
    } catch { /* sin usuario */ }
  }, [])

  useEffect(() => {
    const controller = new AbortController()
    const uid = userId ? `?user_id=${userId}` : ''

    fetch(`/api/v1/levels/sector/${sectorId}${uid}`, { signal: controller.signal })
      .then((r) => {
        if (!r.ok) throw new Error(`Sector ${sectorId} no encontrado`)
        return r.json()
      })
      .then((data: SectorResponse) => {
        setLevels(data.levels)
        setDakiState(data.daki_state)
        setLoading(false)
      })
      .catch((e) => {
        if (e.name !== 'AbortError') {
          setError(e.message ?? 'Error de conexión')
          setLoading(false)
        }
      })

    return () => controller.abort()
  }, [sectorId, userId])

  const completed = levels.filter((l) => l.completed).length

  // ── Loading ──
  if (loading) {
    return (
      <div
        className="min-h-screen flex items-center justify-center"
        style={{ background: '#0A0A0A' }}
      >
        <motion.p
          className="text-sm tracking-widest"
          style={{ fontFamily: 'monospace', color: '#00FF41' }}
          animate={{ opacity: [0.4, 1, 0.4] }}
          transition={{ duration: 1.2, repeat: Infinity }}
        >
          [ CARGANDO SECTOR {String(sectorId).padStart(2, '0')} ]
        </motion.p>
      </div>
    )
  }

  // ── Error ──
  if (error) {
    return (
      <div
        className="min-h-screen flex flex-col items-center justify-center gap-4"
        style={{ background: '#0A0A0A' }}
      >
        <p className="text-sm tracking-widest" style={{ fontFamily: 'monospace', color: '#FF2D78' }}>
          [ ERROR: {error} ]
        </p>
        <button
          onClick={() => router.back()}
          className="text-xs tracking-widest underline"
          style={{ fontFamily: 'monospace', color: '#00FF4199' }}
        >
          ← VOLVER AL NEXO
        </button>
      </div>
    )
  }

  // ── Vista principal ──
  return (
    <div
      className="min-h-screen crt"
      style={{ background: '#0A0A0A', color: '#00FF41' }}
    >
      {/* Scanlines decorativas */}
      <div
        className="pointer-events-none fixed inset-0 z-0"
        style={{
          background: 'repeating-linear-gradient(0deg, transparent, transparent 3px, rgba(0,255,65,0.012) 3px, rgba(0,255,65,0.012) 4px)',
        }}
      />

      <div className="relative z-10 max-w-4xl mx-auto px-4 py-10">

        {/* ── Header ── */}
        <motion.div
          initial={{ opacity: 0, y: -12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
          className="mb-8"
        >
          {/* Breadcrumb */}
          <button
            onClick={() => router.back()}
            className="text-[10px] tracking-widest mb-4 block hover:opacity-100 transition-opacity"
            style={{ fontFamily: 'monospace', color: '#00FF4155' }}
          >
            ← NEXO / SECTORES
          </button>

          {/* Título del sector */}
          <div className="flex items-end justify-between flex-wrap gap-4">
            <div>
              <p
                className="text-[10px] tracking-[0.3em] mb-1"
                style={{ fontFamily: 'monospace', color: '#00FF4155' }}
              >
                PROTOCOLO DE MISIONES
              </p>
              <h1
                className="text-2xl sm:text-3xl font-bold tracking-wider"
                style={{
                  fontFamily: 'monospace',
                  color: '#00FF41',
                  textShadow: '0 0 30px rgba(0,255,65,0.4)',
                }}
              >
                [ SECTOR {String(sectorId).padStart(2, '0')} ]
              </h1>
            </div>

            {/* XP total del sector */}
            <div className="text-right">
              <p
                className="text-[10px] tracking-widest"
                style={{ fontFamily: 'monospace', color: '#00FF4155' }}
              >
                RECOMPENSA TOTAL
              </p>
              <p
                className="text-xl font-bold"
                style={{ fontFamily: 'monospace', color: '#FFC700' }}
              >
                +{levels.reduce((acc, l) => acc + l.base_xp_reward, 0).toLocaleString()} XP
              </p>
            </div>
          </div>

          {/* Progreso */}
          <div className="mt-4">
            <SectorProgressBar completed={completed} total={levels.length} />
          </div>

          {/* Divider */}
          <div
            className="mt-6 h-px"
            style={{ background: 'linear-gradient(90deg, #00FF4130, transparent)' }}
          />
        </motion.div>

        {/* ── Grid de niveles ── */}
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3">
          <AnimatePresence>
            {levels.map((level, i) => (
              <LevelCard
                key={level.id}
                level={level}
                index={i}
                onClick={() => router.push(`${challengeBasePath}?id=${level.id}`)}
              />
            ))}
          </AnimatePresence>
        </div>

        {/* ── Estado DAKI ── */}
        {dakiState && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.7 }}
            className="mt-8 p-4 rounded"
            style={{
              background: 'rgba(0,255,65,0.03)',
              border: '1px solid rgba(0,255,65,0.15)',
            }}
          >
            <div className="flex items-start gap-4 flex-wrap">
              {/* Nivel DAKI */}
              <div className="shrink-0">
                <p className="text-[9px] tracking-widest mb-1" style={{ fontFamily: 'monospace', color: '#00FF4155' }}>
                  ESTADO DAKI
                </p>
                <div className="flex gap-1">
                  {([1, 2, 3] as const).map((n) => (
                    <div
                      key={n}
                      className="w-5 h-5 rounded-sm flex items-center justify-center text-[9px]"
                      style={{
                        background: dakiState.daki_level >= n ? 'rgba(0,255,65,0.2)' : 'rgba(255,255,255,0.04)',
                        border: `1px solid ${dakiState.daki_level >= n ? 'rgba(0,255,65,0.6)' : 'rgba(255,255,255,0.08)'}`,
                        color: dakiState.daki_level >= n ? '#00FF41' : '#333',
                        fontFamily: 'monospace',
                      }}
                    >
                      {n}
                    </div>
                  ))}
                </div>
              </div>

              {/* Info */}
              <div className="flex-1 min-w-0">
                <p
                  className="text-sm font-bold tracking-wide mb-0.5"
                  style={{ fontFamily: 'monospace', color: '#00FF41' }}
                >
                  {dakiState.label}
                </p>
                <p
                  className="text-[11px] leading-relaxed"
                  style={{ fontFamily: 'monospace', color: '#00FF4177' }}
                >
                  {dakiState.description}
                </p>
              </div>

              {/* Próximo umbral */}
              {dakiState.next_threshold !== null && (
                <div className="shrink-0 text-right">
                  <p className="text-[9px] tracking-widest" style={{ fontFamily: 'monospace', color: '#00FF4133' }}>
                    PRÓXIMA EVOLUCIÓN
                  </p>
                  <p className="text-xs" style={{ fontFamily: 'monospace', color: '#FFC70099' }}>
                    {dakiState.completed_sectors}/{dakiState.next_threshold} sectores
                  </p>
                </div>
              )}
            </div>
          </motion.div>
        )}

        {/* ── Leyenda ── */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6 }}
          className="mt-10 flex flex-wrap gap-6 justify-center"
        >
          {[
            { color: '#00FF41', icon: '✓', label: 'COMPLETADO' },
            { color: '#FFC700', icon: '▶', label: 'DISPONIBLE' },
            { color: '#333',    icon: '🔒', label: 'BLOQUEADO' },
            { color: '#FFC700', icon: '★', label: 'PROYECTO FINAL' },
          ].map(({ color, icon, label }) => (
            <div key={label} className="flex items-center gap-2">
              <span style={{ color, fontSize: '12px' }}>{icon}</span>
              <span
                className="text-[9px] tracking-widest"
                style={{ fontFamily: 'monospace', color: '#ffffff44' }}
              >
                {label}
              </span>
            </div>
          ))}
        </motion.div>

      </div>
    </div>
  )
}
