'use client'

/**
 * AdminDashboard.tsx — God Mode: Telemetría de Beta para el CEO.
 *
 * Acceso: ruta /god-mode, protegida por ADMIN_SECRET en header.
 * Datos: GET /api/v1/admin/dashboard
 *
 * Secciones:
 *  1. KPI Cards globales (usuarios, intentos, tasa éxito)
 *  2. Alertas de Fricción — niveles con avg_attempts > 10
 *  3. Alertas DAKI Overload — niveles con daki_dependency > 50%
 *  4. Tabla analítica completa por nivel
 */

import { useState, useEffect, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? ''

// ─── Tipos ────────────────────────────────────────────────────────────────────

interface LevelMetric {
  challenge_id: string
  title: string
  sector_id: number | null
  level_order: number | null
  difficulty: string | null
  total_users: number
  resolved_users: number
  success_rate: number
  avg_attempts: number
  avg_time_min: number
  max_attempts: number
  daki_dependency: number
  avg_hints: number
  top_errors: string[]
  friction_alert: boolean
  daki_overload: boolean
}

interface DashboardStats {
  total_users: number
  total_attempts: number
  global_success_rate: number
  most_played_level: string | null
  hardest_level: string | null
}

interface DashboardData {
  stats: DashboardStats
  levels: LevelMetric[]
}

// ─── Helpers de presentación ──────────────────────────────────────────────────

const DIFF_COLORS: Record<string, string> = {
  easy:   '#00FF41',
  medium: '#FFB800',
  hard:   '#FF6B35',
  expert: '#FF0080',
}

const SECTOR_COLORS = ['#00E5FF', '#00FF41', '#FFB800', '#FF6B35', '#BD00FF', '#FF0080', '#00FFCC']

function diffColor(d: string | null) {
  return DIFF_COLORS[d ?? ''] ?? '#888'
}

function successColor(rate: number) {
  if (rate >= 70) return '#00FF41'
  if (rate >= 40) return '#FFB800'
  return '#FF4444'
}

function Bar({ value, max, color }: { value: number; max: number; color: string }) {
  const pct = Math.min((value / max) * 100, 100)
  return (
    <div className="w-full h-1.5 rounded-full bg-white/5 overflow-hidden">
      <motion.div
        className="h-full rounded-full"
        style={{ background: color }}
        initial={{ width: 0 }}
        animate={{ width: `${pct}%` }}
        transition={{ duration: 0.6, ease: 'easeOut' }}
      />
    </div>
  )
}

// ─── KPI Card ─────────────────────────────────────────────────────────────────

function KpiCard({
  label, value, sub, color,
}: {
  label: string; value: string | number; sub?: string; color: string
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded border p-4 flex flex-col gap-1"
      style={{ borderColor: `${color}30`, background: `${color}08` }}
    >
      <span className="text-[9px] tracking-[0.4em] font-bold font-mono" style={{ color: `${color}88` }}>
        {label}
      </span>
      <span className="text-2xl font-bold font-mono" style={{ color }}>
        {value}
      </span>
      {sub && (
        <span className="text-[9px] font-mono" style={{ color: `${color}55` }}>{sub}</span>
      )}
    </motion.div>
  )
}

// ─── Alert Card ───────────────────────────────────────────────────────────────

function AlertCard({ level, type }: { level: LevelMetric; type: 'friction' | 'daki' }) {
  const isFriction = type === 'friction'
  const color      = isFriction ? '#FF4444' : '#BD00FF'
  const icon       = isFriction ? '⚡' : '🤖'

  return (
    <motion.div
      initial={{ opacity: 0, x: -8 }}
      animate={{ opacity: 1, x: 0 }}
      className="rounded border px-3 py-2 flex items-start gap-3"
      style={{
        borderColor: `${color}40`,
        background:  `${color}08`,
        boxShadow:   `0 0 12px ${color}18`,
      }}
    >
      <span className="text-base shrink-0 mt-0.5">{icon}</span>
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 flex-wrap">
          <span className="text-[10px] font-bold font-mono truncate" style={{ color }}>
            {level.title}
          </span>
          {level.sector_id && (
            <span className="text-[8px] font-mono px-1.5 py-0.5 rounded"
              style={{ background: `${color}15`, color: `${color}99` }}>
              S{level.sector_id}
            </span>
          )}
        </div>
        <p className="text-[9px] font-mono mt-0.5" style={{ color: `${color}88` }}>
          {isFriction
            ? `Promedio ${level.avg_attempts} intentos · max ${level.max_attempts} · El diseño del nivel debe ser revisado`
            : `${level.daki_dependency}% de usuarios usó las 3 pistas de DAKI · avg ${level.avg_hints} pistas`
          }
        </p>
      </div>
      <span className="text-[9px] font-bold font-mono shrink-0" style={{ color }}>
        {isFriction ? `${level.avg_attempts}x` : `${level.daki_dependency}%`}
      </span>
    </motion.div>
  )
}

// ─── Fila de tabla ────────────────────────────────────────────────────────────

function LevelRow({ level, index }: { level: LevelMetric; index: number }) {
  const [expanded, setExpanded] = useState(false)
  const rowBase = level.friction_alert
    ? 'border-l-2 border-l-[#FF4444]'
    : level.daki_overload
      ? 'border-l-2 border-l-[#BD00FF]'
      : 'border-l-2 border-l-transparent'

  const sColor = SECTOR_COLORS[(level.sector_id ?? 1) % SECTOR_COLORS.length]

  return (
    <>
      <motion.tr
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: index * 0.015 }}
        onClick={() => setExpanded(e => !e)}
        className={`cursor-pointer border-b border-white/5 hover:bg-white/[0.02] transition-colors ${rowBase}`}
        style={level.friction_alert ? { background: 'rgba(255,68,68,0.03)' } : undefined}
      >
        {/* Nivel / Título */}
        <td className="px-3 py-2.5">
          <div className="flex items-center gap-2">
            <span className="text-[9px] font-mono font-bold w-6 text-center rounded"
              style={{ color: sColor, background: `${sColor}15` }}>
              {level.level_order ?? '—'}
            </span>
            <div>
              <div className="text-[10px] font-mono text-white/80 truncate max-w-[160px]">
                {level.title}
              </div>
              <div className="flex items-center gap-1 mt-0.5">
                {level.sector_id && (
                  <span className="text-[7px] font-mono" style={{ color: `${sColor}66` }}>
                    S{level.sector_id}
                  </span>
                )}
                {level.difficulty && (
                  <span className="text-[7px] font-mono font-bold"
                    style={{ color: diffColor(level.difficulty) }}>
                    {level.difficulty.toUpperCase()}
                  </span>
                )}
              </div>
            </div>
          </div>
        </td>

        {/* Usuarios */}
        <td className="px-3 py-2.5 text-center">
          <span className="text-[10px] font-mono text-white/60">
            {level.total_users}
          </span>
        </td>

        {/* Tasa de éxito */}
        <td className="px-3 py-2.5">
          <div className="flex items-center gap-2">
            <span className="text-[10px] font-mono font-bold w-12 text-right"
              style={{ color: successColor(level.success_rate) }}>
              {level.success_rate}%
            </span>
            <div className="flex-1 min-w-[48px]">
              <Bar value={level.success_rate} max={100} color={successColor(level.success_rate)} />
            </div>
          </div>
        </td>

        {/* Intentos promedio */}
        <td className="px-3 py-2.5">
          <div className="flex items-center gap-1.5">
            {level.friction_alert && (
              <motion.span
                animate={{ opacity: [1, 0.3, 1] }}
                transition={{ duration: 0.8, repeat: Infinity }}
                className="text-[8px]"
              >🔴</motion.span>
            )}
            <span className="text-[10px] font-mono font-bold"
              style={{ color: level.friction_alert ? '#FF4444' : 'rgba(255,255,255,0.7)' }}>
              {level.avg_attempts}
            </span>
            <span className="text-[8px] font-mono text-white/25">avg</span>
          </div>
        </td>

        {/* Dependencia DAKI */}
        <td className="px-3 py-2.5">
          <div className="flex items-center gap-2">
            <span className="text-[10px] font-mono font-bold w-12 text-right"
              style={{ color: level.daki_overload ? '#BD00FF' : 'rgba(255,255,255,0.5)' }}>
              {level.daki_dependency}%
            </span>
            <div className="flex-1 min-w-[48px]">
              <Bar
                value={level.daki_dependency}
                max={100}
                color={level.daki_overload ? '#BD00FF' : '#00E5FF'}
              />
            </div>
          </div>
        </td>

        {/* Tiempo promedio */}
        <td className="px-3 py-2.5 text-center">
          <span className="text-[10px] font-mono text-white/50">
            {level.avg_time_min}m
          </span>
        </td>

        {/* Alertas */}
        <td className="px-3 py-2.5">
          <div className="flex gap-1 justify-end">
            {level.friction_alert && (
              <span className="text-[7px] font-mono font-bold px-1.5 py-0.5 rounded"
                style={{ background: '#FF444420', color: '#FF4444' }}>
                FRICCIÓN
              </span>
            )}
            {level.daki_overload && (
              <span className="text-[7px] font-mono font-bold px-1.5 py-0.5 rounded"
                style={{ background: '#BD00FF20', color: '#BD00FF' }}>
                DAKI↑
              </span>
            )}
          </div>
        </td>
      </motion.tr>

      {/* Fila expandida con errores frecuentes */}
      <AnimatePresence>
        {expanded && (
          <motion.tr
            key="expanded"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <td colSpan={7} className="px-3 pb-3 pt-0">
              <div className="rounded border border-white/5 bg-white/[0.02] px-3 py-2 flex gap-6 flex-wrap">
                <div>
                  <span className="text-[7px] tracking-widest font-mono text-white/30 block mb-1">
                    TOP ERRORES
                  </span>
                  {level.top_errors.length > 0 ? (
                    <div className="flex gap-1.5 flex-wrap">
                      {level.top_errors.map(e => (
                        <span key={e} className="text-[8px] font-mono px-1.5 py-0.5 rounded"
                          style={{ background: '#FF444418', color: '#FF8888' }}>
                          {e}
                        </span>
                      ))}
                    </div>
                  ) : (
                    <span className="text-[8px] font-mono text-white/20">sin errores registrados</span>
                  )}
                </div>
                <div>
                  <span className="text-[7px] tracking-widest font-mono text-white/30 block mb-1">
                    DETALLE
                  </span>
                  <div className="text-[8px] font-mono text-white/40 space-y-0.5">
                    <div>Resueltos: <span className="text-white/70">{level.resolved_users}/{level.total_users}</span></div>
                    <div>Máx intentos: <span className="text-white/70">{level.max_attempts}</span></div>
                    <div>Pistas avg: <span className="text-white/70">{level.avg_hints}</span></div>
                    <div>ID: <span className="text-white/30">{level.challenge_id.slice(0, 8)}</span></div>
                  </div>
                </div>
                {level.friction_alert && (
                  <div className="flex items-center">
                    <div className="rounded border border-[#FF444430] bg-[#FF444408] px-3 py-1.5 max-w-xs">
                      <p className="text-[8px] font-mono" style={{ color: '#FF4444CC' }}>
                        ⚠ El diseño del nivel debe ser revisado. El promedio de intentos supera el umbral
                        crítico de 10. Considera simplificar el enunciado o añadir una pista adicional.
                      </p>
                    </div>
                  </div>
                )}
              </div>
            </td>
          </motion.tr>
        )}
      </AnimatePresence>
    </>
  )
}

// ─── Componente principal ─────────────────────────────────────────────────────

interface AdminDashboardProps {
  adminSecret: string
}

type SortKey = 'level_order' | 'success_rate' | 'avg_attempts' | 'daki_dependency' | 'total_users'
type FilterMode = 'all' | 'friction' | 'daki' | 'ok'

export default function AdminDashboard({ adminSecret }: AdminDashboardProps) {
  const [data, setData]       = useState<DashboardData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError]     = useState('')
  const [sortKey, setSortKey] = useState<SortKey>('level_order')
  const [sortAsc, setSortAsc] = useState(true)
  const [filter, setFilter]   = useState<FilterMode>('all')
  const [search, setSearch]   = useState('')

  const load = useCallback(async () => {
    setLoading(true); setError('')
    try {
      const res = await fetch(`${API_BASE}/api/v1/admin/dashboard`, {
        headers: { 'X-Admin-Secret': adminSecret },
      })
      if (!res.ok) throw new Error(`${res.status} ${res.statusText}`)
      setData(await res.json())
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Error desconocido')
    } finally {
      setLoading(false)
    }
  }, [adminSecret])

  useEffect(() => { load() }, [load])

  // ── Ordenado + filtrado ───────────────────────────────────────────────────
  const displayed = (data?.levels ?? [])
    .filter(l => {
      const matchSearch = search === '' ||
        l.title.toLowerCase().includes(search.toLowerCase())
      const matchFilter =
        filter === 'all'     ? true :
        filter === 'friction' ? l.friction_alert :
        filter === 'daki'    ? l.daki_overload :
        /* ok */               !l.friction_alert && !l.daki_overload
      return matchSearch && matchFilter
    })
    .sort((a, b) => {
      const va = a[sortKey] ?? 0
      const vb = b[sortKey] ?? 0
      return sortAsc
        ? (va as number) - (vb as number)
        : (vb as number) - (va as number)
    })

  const frictionLevels = data?.levels.filter(l => l.friction_alert) ?? []
  const dakiLevels     = data?.levels.filter(l => l.daki_overload)  ?? []

  function toggleSort(key: SortKey) {
    if (sortKey === key) setSortAsc(a => !a)
    else { setSortKey(key); setSortAsc(key === 'level_order') }
  }

  function SortTh({ k, label }: { k: SortKey; label: string }) {
    const active = sortKey === k
    return (
      <th
        onClick={() => toggleSort(k)}
        className="px-3 py-2 text-left cursor-pointer select-none hover:text-white/70 transition-colors"
        style={{ color: active ? '#00E5FF' : 'rgba(255,255,255,0.35)' }}
      >
        <span className="text-[8px] tracking-widest font-bold font-mono">
          {label} {active ? (sortAsc ? '↑' : '↓') : ''}
        </span>
      </th>
    )
  }

  // ── Loading ───────────────────────────────────────────────────────────────
  if (loading) {
    return (
      <div className="min-h-screen bg-[#020a05] flex items-center justify-center">
        <motion.div
          animate={{ opacity: [0.3, 1, 0.3] }}
          transition={{ duration: 1.5, repeat: Infinity }}
          className="text-[#00E5FF] font-mono text-sm tracking-widest"
        >
          CARGANDO TELEMETRÍA...
        </motion.div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-[#020a05] flex items-center justify-center">
        <div className="text-center space-y-3">
          <p className="text-[#FF4444] font-mono text-sm">ACCESO DENEGADO</p>
          <p className="text-white/30 font-mono text-xs">{error}</p>
          <button
            onClick={load}
            className="text-[9px] tracking-widest font-mono border border-[#FF444440] text-[#FF4444] px-4 py-1.5 rounded hover:bg-[#FF444410] transition-colors"
          >
            REINTENTAR
          </button>
        </div>
      </div>
    )
  }

  const stats = data!.stats

  return (
    <div className="min-h-screen bg-[#020a05] text-white font-mono">
      {/* ── Header ── */}
      <div className="border-b border-white/5 px-6 py-4 flex items-center justify-between">
        <div>
          <div className="flex items-center gap-3">
            <motion.div
              animate={{ opacity: [0.5, 1, 0.5] }}
              transition={{ duration: 2, repeat: Infinity }}
              className="w-2 h-2 rounded-full bg-[#00FF41]"
              style={{ boxShadow: '0 0 8px #00FF41' }}
            />
            <h1 className="text-sm tracking-[0.3em] font-bold text-white/90">
              GOD MODE
            </h1>
            <span className="text-[8px] tracking-widest text-white/25 border border-white/10 px-2 py-0.5 rounded">
              BETA ANALYTICS
            </span>
          </div>
          <p className="text-[9px] text-white/25 mt-1 tracking-wider">
            DAKI EdTech · Telemetría de aprendizaje en tiempo real
          </p>
        </div>
        <button
          onClick={load}
          className="text-[8px] tracking-widest text-[#00E5FF]/60 border border-[#00E5FF]/20 px-3 py-1.5 rounded hover:bg-[#00E5FF]/5 transition-colors"
        >
          ↻ REFRESH
        </button>
      </div>

      <div className="px-6 py-6 space-y-6 max-w-7xl mx-auto">

        {/* ── KPI Cards ── */}
        <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
          <KpiCard label="USUARIOS BETA" value={stats.total_users}
            color="#00E5FF" sub="usuarios únicos" />
          <KpiCard label="TOTAL INTENTOS" value={stats.total_attempts.toLocaleString()}
            color="#00FF41" sub="ejecuciones registradas" />
          <KpiCard label="TASA ÉXITO GLOBAL" value={`${stats.global_success_rate}%`}
            color={successColor(stats.global_success_rate)} />
          <KpiCard label="NIVEL MÁS JUGADO" value={stats.most_played_level ?? '—'}
            color="#FFB800" sub="mayor tráfico" />
          <KpiCard label="NIVEL MÁS DIFÍCIL" value={stats.hardest_level ?? '—'}
            color="#FF6B35" sub="mayor avg intentos" />
        </div>

        {/* ── Alertas de Fricción ── */}
        {frictionLevels.length > 0 && (
          <section>
            <div className="flex items-center gap-2 mb-3">
              <motion.div
                animate={{ opacity: [1, 0.3, 1] }}
                transition={{ duration: 0.9, repeat: Infinity }}
                className="w-1.5 h-1.5 rounded-full bg-[#FF4444]"
                style={{ boxShadow: '0 0 6px #FF4444' }}
              />
              <h2 className="text-[9px] tracking-[0.4em] font-bold text-[#FF4444]/80">
                ALERTAS DE FRICCIÓN
              </h2>
              <span className="text-[8px] font-mono text-[#FF4444]/40">
                avg intentos {'>'} 10 — revisar diseño
              </span>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-2">
              {frictionLevels.map(l => (
                <AlertCard key={l.challenge_id} level={l} type="friction" />
              ))}
            </div>
          </section>
        )}

        {/* ── Alertas DAKI Overload ── */}
        {dakiLevels.length > 0 && (
          <section>
            <div className="flex items-center gap-2 mb-3">
              <motion.div
                animate={{ opacity: [1, 0.3, 1] }}
                transition={{ duration: 1.4, repeat: Infinity }}
                className="w-1.5 h-1.5 rounded-full bg-[#BD00FF]"
                style={{ boxShadow: '0 0 6px #BD00FF' }}
              />
              <h2 className="text-[9px] tracking-[0.4em] font-bold text-[#BD00FF]/80">
                DAKI OVERLOAD
              </h2>
              <span className="text-[8px] font-mono text-[#BD00FF]/40">
                {'>'} 50% usuarios usó las 3 pistas — nivel puede necesitar más andamiaje
              </span>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-2">
              {dakiLevels.map(l => (
                <AlertCard key={l.challenge_id} level={l} type="daki" />
              ))}
            </div>
          </section>
        )}

        {/* ── Tabla analítica ── */}
        <section>
          <div className="flex items-center justify-between mb-3 flex-wrap gap-2">
            <h2 className="text-[9px] tracking-[0.4em] font-bold text-white/40">
              TABLA ANALÍTICA · {displayed.length}/{data!.levels.length} NIVELES
            </h2>

            {/* Filtros */}
            <div className="flex items-center gap-2 flex-wrap">
              <input
                value={search}
                onChange={e => setSearch(e.target.value)}
                placeholder="Buscar nivel..."
                className="text-[9px] font-mono bg-white/5 border border-white/10 rounded px-2 py-1 text-white/60 placeholder-white/20 focus:outline-none focus:border-[#00E5FF]/30 w-36"
              />
              {(['all', 'friction', 'daki', 'ok'] as FilterMode[]).map(f => (
                <button
                  key={f}
                  onClick={() => setFilter(f)}
                  className="text-[7px] tracking-widest font-bold px-2.5 py-1 rounded border transition-colors"
                  style={filter === f ? {
                    borderColor: '#00E5FF40', background: '#00E5FF12', color: '#00E5FF',
                  } : {
                    borderColor: 'rgba(255,255,255,0.08)', color: 'rgba(255,255,255,0.3)',
                  }}
                >
                  {f === 'all' ? 'TODOS' : f === 'friction' ? '⚡ FRICCIÓN' : f === 'daki' ? '🤖 DAKI↑' : '✓ OK'}
                </button>
              ))}
            </div>
          </div>

          <div className="rounded border border-white/5 overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full border-collapse">
                <thead>
                  <tr className="border-b border-white/8 bg-white/[0.02]">
                    <SortTh k="level_order" label="NIVEL / TÍTULO" />
                    <SortTh k="total_users"  label="USUARIOS" />
                    <SortTh k="success_rate" label="ÉXITO %" />
                    <SortTh k="avg_attempts" label="AVG INTENTOS" />
                    <SortTh k="daki_dependency" label="DAKI DEP." />
                    <th className="px-3 py-2 text-left">
                      <span className="text-[8px] tracking-widest font-bold font-mono text-white/30">TIEMPO</span>
                    </th>
                    <th className="px-3 py-2 text-right">
                      <span className="text-[8px] tracking-widest font-bold font-mono text-white/30">ALERTAS</span>
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {displayed.length === 0 ? (
                    <tr>
                      <td colSpan={7} className="px-3 py-8 text-center text-[9px] font-mono text-white/20">
                        {data!.levels.length === 0
                          ? 'Sin telemetría registrada. Los datos aparecerán cuando los usuarios jueguen.'
                          : 'Sin resultados para los filtros actuales.'}
                      </td>
                    </tr>
                  ) : (
                    displayed.map((level, i) => (
                      <LevelRow key={level.challenge_id} level={level} index={i} />
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>

          <p className="text-[7px] font-mono text-white/15 mt-2 text-right">
            Haz clic en una fila para ver errores frecuentes y detalle del nivel.
          </p>
        </section>

      </div>
    </div>
  )
}
