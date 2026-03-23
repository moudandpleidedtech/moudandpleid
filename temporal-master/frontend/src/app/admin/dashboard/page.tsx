'use client'

import { useState, useEffect, useCallback } from 'react'
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, Cell, LineChart, Line, Legend,
} from 'recharts'

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000'

// ─── Types ─────────────────────────────────────────────────────────────────────

interface OverviewData {
  total_users: number
  paid_users: number
  unpaid_users: number
  conversion_rate: number
  license_price_usd: number
  projected_revenue_usd: number
  users_with_progress: number
  users_who_started: number
  users_completed_all: number
  active_last_24h: number
  generated_at: string
}

interface DropOffLevel {
  level_order: number
  title: string
  sector_id: number | null
  difficulty: string | null
  users_attempted: number
  users_completed: number
  users_stuck: number
  drop_off_rate: number
  avg_attempts_stuck: number
  is_bottleneck: boolean
}

interface DropOffData {
  total_levels_with_data: number
  top_bottlenecks: string[]
  levels: DropOffLevel[]
}

interface DakiLevelStat {
  level_order: number
  title: string
  sector_id: number | null
  total_users: number
  avg_hints: number
  pct_no_hints: number
  pct_max_hints: number
  daki_dependency_score: number
  autonomy_alert: boolean
}

interface DakiStatsData {
  most_independent_level: string | null
  most_dependent_level: string | null
  global_avg_hints: number
  levels: DakiLevelStat[]
}

interface RecentUser {
  id: string
  username: string
  email: string
  current_level: number
  total_xp: number
  is_paid: boolean
  league_tier: string
  created_at: string
}

interface SectorBar {
  sector: string
  sectorNum: number
  dropOff: number
  users: number
  hasBottleneck: boolean
  dakiScore: number
}

// ─── API helpers ───────────────────────────────────────────────────────────────

async function apiFetch<T>(path: string, token: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { Authorization: `Bearer ${token}` },
  })
  if (res.status === 401) throw new Error('unauthorized')
  if (!res.ok) throw new Error(`HTTP ${res.status}`)
  return res.json()
}

async function apiLogin(username: string, password: string) {
  const res = await fetch(`${API_BASE}/api/v1/admin/auth/token`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  })
  if (!res.ok) throw new Error('Credenciales inválidas')
  return res.json() as Promise<{ access_token: string; username: string; expires_in_minutes: number }>
}

// ─── Data aggregation ──────────────────────────────────────────────────────────

function buildSectorBars(dropOff: DropOffData, daki: DakiStatsData): SectorBar[] {
  const sMap: Record<number, { drop: number[]; daki: number[]; users: number; bottleneck: boolean }> = {}

  for (const lv of dropOff.levels) {
    const s = lv.sector_id ?? Math.ceil(lv.level_order / 10)
    if (!sMap[s]) sMap[s] = { drop: [], daki: [], users: 0, bottleneck: false }
    sMap[s].drop.push(lv.drop_off_rate)
    sMap[s].users += lv.users_attempted
    if (lv.is_bottleneck) sMap[s].bottleneck = true
  }

  for (const lv of daki.levels) {
    const s = lv.sector_id ?? Math.ceil(lv.level_order / 10)
    if (!sMap[s]) sMap[s] = { drop: [], daki: [], users: 0, bottleneck: false }
    sMap[s].daki.push(lv.daki_dependency_score)
  }

  return Object.entries(sMap)
    .map(([sid, d]) => ({
      sector: `S${sid}`,
      sectorNum: Number(sid),
      dropOff: d.drop.length ? Math.round((d.drop.reduce((a, b) => a + b, 0) / d.drop.length) * 10) / 10 : 0,
      dakiScore: d.daki.length ? Math.round((d.daki.reduce((a, b) => a + b, 0) / d.daki.length) * 10) / 10 : 0,
      users: d.users,
      hasBottleneck: d.bottleneck,
    }))
    .sort((a, b) => a.sectorNum - b.sectorNum)
}

function formatDate(iso: string) {
  return new Date(iso).toLocaleDateString('es-AR', {
    day: '2-digit', month: 'short', year: 'numeric',
  })
}

// ─── Sub-components ────────────────────────────────────────────────────────────

function StatCard({
  label, value, sub, accent = '#00FF41', icon,
}: {
  label: string
  value: string | number
  sub?: string
  accent?: string
  icon: string
}) {
  return (
    <div
      className="rounded border p-5 flex flex-col gap-2"
      style={{ background: '#0d0d1a', borderColor: '#1a1a2e' }}
    >
      <div className="flex items-center gap-2">
        <span className="text-lg">{icon}</span>
        <span className="text-xs tracking-widest uppercase" style={{ color: '#6b7280' }}>
          {label}
        </span>
      </div>
      <span className="text-3xl font-black font-mono" style={{ color: accent }}>
        {value}
      </span>
      {sub && <span className="text-xs" style={{ color: '#4b5563' }}>{sub}</span>}
    </div>
  )
}

const CHART_TOOLTIP_STYLE = {
  contentStyle: { background: '#0d0d1a', border: '1px solid #1a1a2e', borderRadius: 4 },
  labelStyle: { color: '#9ca3af', fontSize: 11 },
  itemStyle: { color: '#00FF41', fontSize: 12 },
}

function DropOffChart({ data }: { data: SectorBar[] }) {
  if (!data.length) return <EmptyChart label="Sin datos de deserción aún" />
  return (
    <ResponsiveContainer width="100%" height={240}>
      <BarChart data={data} margin={{ top: 4, right: 8, left: -16, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#1a1a2e" />
        <XAxis dataKey="sector" tick={{ fill: '#6b7280', fontSize: 11 }} axisLine={false} tickLine={false} />
        <YAxis tick={{ fill: '#6b7280', fontSize: 11 }} axisLine={false} tickLine={false} unit="%" domain={[0, 100]} />
        <Tooltip
          {...CHART_TOOLTIP_STYLE}
          formatter={(v: number, name: string) => [`${v}%`, 'Deserción']}
          labelFormatter={(l) => `Sector ${l.slice(1)}`}
        />
        <Bar dataKey="dropOff" radius={[3, 3, 0, 0]} maxBarSize={48}>
          {data.map((entry) => (
            <Cell
              key={entry.sector}
              fill={entry.hasBottleneck ? '#ef4444' : entry.dropOff > 25 ? '#f97316' : '#00FF41'}
            />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  )
}

function DakiChart({ data }: { data: SectorBar[] }) {
  if (!data.length) return <EmptyChart label="Sin datos de DAKI aún" />
  return (
    <ResponsiveContainer width="100%" height={240}>
      <LineChart data={data} margin={{ top: 4, right: 8, left: -16, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#1a1a2e" />
        <XAxis dataKey="sector" tick={{ fill: '#6b7280', fontSize: 11 }} axisLine={false} tickLine={false} />
        <YAxis tick={{ fill: '#6b7280', fontSize: 11 }} axisLine={false} tickLine={false} domain={[0, 100]} />
        <Tooltip
          {...CHART_TOOLTIP_STYLE}
          formatter={(v: number) => [`${v} / 100`, 'Dependencia']}
          labelFormatter={(l) => `Sector ${l.slice(1)}`}
        />
        <Legend
          formatter={() => 'Score de dependencia DAKI'}
          wrapperStyle={{ color: '#6b7280', fontSize: 11 }}
        />
        <Line
          type="monotone"
          dataKey="dakiScore"
          stroke="#00bfff"
          strokeWidth={2}
          dot={{ r: 4, fill: '#00bfff', strokeWidth: 0 }}
          activeDot={{ r: 6, fill: '#ffffff' }}
        />
      </LineChart>
    </ResponsiveContainer>
  )
}

function EmptyChart({ label }: { label: string }) {
  return (
    <div className="flex items-center justify-center h-[240px]" style={{ color: '#374151' }}>
      <span className="text-sm tracking-widest uppercase">{label}</span>
    </div>
  )
}

function SectionTitle({ children }: { children: React.ReactNode }) {
  return (
    <h2 className="text-xs tracking-[0.35em] uppercase mb-4 flex items-center gap-2" style={{ color: '#4b5563' }}>
      <span className="w-4 h-px inline-block" style={{ background: '#00FF41' }} />
      {children}
    </h2>
  )
}

function Pill({ label, active }: { label: string; active: boolean }) {
  return (
    <span
      className="text-[10px] px-1.5 py-0.5 rounded font-mono tracking-wider"
      style={{
        background: active ? '#052e16' : '#1a1a1a',
        color: active ? '#22c55e' : '#374151',
        border: `1px solid ${active ? '#166534' : '#1f2937'}`,
      }}
    >
      {active ? 'PAGADO' : 'FREE'}
    </span>
  )
}

function LeagueBadge({ tier }: { tier: string }) {
  const colors: Record<string, string> = {
    Bronce: '#92400e', Plata: '#6b7280', Oro: '#b45309',
    Platino: '#0e7490', Diamante: '#1d4ed8', Maestro: '#7c3aed',
  }
  return (
    <span
      className="text-[10px] px-1.5 py-0.5 rounded font-mono"
      style={{ background: '#111827', color: colors[tier] ?? '#6b7280', border: '1px solid #1f2937' }}
    >
      {tier.toUpperCase()}
    </span>
  )
}

// ─── Login Screen ──────────────────────────────────────────────────────────────

function LoginScreen({ onLogin }: { onLogin: (token: string, username: string) => void }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError]       = useState('')
  const [loading, setLoading]   = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const data = await apiLogin(username, password)
      onLogin(data.access_token, data.username)
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Error desconocido')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center" style={{ background: '#050508' }}>
      {/* Scanline overlay */}
      <div
        className="fixed inset-0 pointer-events-none z-10"
        style={{
          backgroundImage: 'repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,0.08) 2px,rgba(0,0,0,0.08) 4px)',
        }}
      />
      <div className="relative z-20 w-full max-w-sm mx-4">
        {/* Header */}
        <div className="text-center mb-8 space-y-1">
          <p className="text-[10px] tracking-[0.7em] uppercase" style={{ color: '#00FF41', opacity: 0.4 }}>
            DAKI EdTech
          </p>
          <h1 className="text-xl font-black font-mono tracking-[0.2em] uppercase" style={{ color: '#e5e7eb' }}>
            Centro de Comando
          </h1>
          <p className="text-[10px] tracking-[0.5em] uppercase" style={{ color: '#374151' }}>
            Acceso Restringido — Solo CEO
          </p>
        </div>

        {/* Form */}
        <form
          onSubmit={handleSubmit}
          className="rounded border p-6 space-y-4"
          style={{ background: '#0d0d1a', borderColor: '#1a1a2e' }}
        >
          <div>
            <label className="block text-[10px] tracking-widest uppercase mb-2" style={{ color: '#4b5563' }}>
              Usuario
            </label>
            <input
              type="text"
              value={username}
              onChange={e => setUsername(e.target.value)}
              required
              autoFocus
              className="w-full px-3 py-2.5 rounded font-mono text-sm outline-none"
              style={{
                background: '#050508',
                border: '1px solid #1a1a2e',
                color: '#e5e7eb',
                caretColor: '#00FF41',
              }}
            />
          </div>
          <div>
            <label className="block text-[10px] tracking-widest uppercase mb-2" style={{ color: '#4b5563' }}>
              Contraseña
            </label>
            <input
              type="password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              required
              className="w-full px-3 py-2.5 rounded font-mono text-sm outline-none"
              style={{
                background: '#050508',
                border: '1px solid #1a1a2e',
                color: '#e5e7eb',
                caretColor: '#00FF41',
              }}
            />
          </div>

          {error && (
            <p className="text-xs font-mono" style={{ color: '#ef4444' }}>
              {'// ERROR: '}{error}
            </p>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 font-mono text-sm tracking-[0.25em] uppercase transition-all duration-200"
            style={{
              background: loading ? '#052e16' : '#00FF41',
              color: loading ? '#166534' : '#000000',
              border: 'none',
              cursor: loading ? 'not-allowed' : 'pointer',
            }}
          >
            {loading ? '[ AUTENTICANDO... ]' : '[ ACCEDER AL NEXO ]'}
          </button>
        </form>
      </div>
    </div>
  )
}

// ─── Sidebar ───────────────────────────────────────────────────────────────────

type Section = 'overview' | 'funnel' | 'daki' | 'users'

const NAV_ITEMS: { id: Section; label: string; icon: string }[] = [
  { id: 'overview', label: 'Overview',  icon: '◈' },
  { id: 'funnel',   label: 'Embudo',    icon: '▼' },
  { id: 'daki',     label: 'DAKI',      icon: '◎' },
  { id: 'users',    label: 'Usuarios',  icon: '◷' },
]

function Sidebar({
  active,
  onNav,
  username,
  onLogout,
}: {
  active: Section
  onNav: (s: Section) => void
  username: string
  onLogout: () => void
}) {
  return (
    <aside
      className="fixed left-0 top-0 h-full w-14 md:w-52 flex flex-col border-r z-50"
      style={{ background: '#08080f', borderColor: '#0f0f1a' }}
    >
      {/* Logo */}
      <div className="px-3 md:px-4 py-5 border-b" style={{ borderColor: '#0f0f1a' }}>
        <div className="hidden md:block">
          <p className="text-[9px] tracking-[0.6em] uppercase" style={{ color: '#00FF41', opacity: 0.5 }}>
            DAKI EdTech
          </p>
          <p className="text-xs font-black font-mono tracking-wider uppercase" style={{ color: '#e5e7eb' }}>
            CMD Center
          </p>
        </div>
        <div className="md:hidden flex justify-center">
          <span style={{ color: '#00FF41', fontSize: 18 }}>◈</span>
        </div>
      </div>

      {/* Nav */}
      <nav className="flex-1 py-4 space-y-1 px-2">
        {NAV_ITEMS.map(item => (
          <button
            key={item.id}
            onClick={() => onNav(item.id)}
            className="w-full flex items-center gap-3 px-2 py-2.5 rounded transition-all duration-150 text-left"
            style={{
              background: active === item.id ? '#0d0d1a' : 'transparent',
              color: active === item.id ? '#00FF41' : '#4b5563',
              borderLeft: active === item.id ? '2px solid #00FF41' : '2px solid transparent',
            }}
          >
            <span className="text-base w-5 text-center flex-shrink-0">{item.icon}</span>
            <span className="hidden md:block text-[11px] tracking-[0.2em] uppercase font-mono">
              {item.label}
            </span>
          </button>
        ))}
      </nav>

      {/* Footer */}
      <div className="border-t px-2 py-3 space-y-2" style={{ borderColor: '#0f0f1a' }}>
        <div className="hidden md:block px-2 py-1">
          <p className="text-[9px] tracking-widest uppercase" style={{ color: '#374151' }}>Sesión activa</p>
          <p className="text-[11px] font-mono truncate" style={{ color: '#6b7280' }}>{username}</p>
        </div>
        <button
          onClick={onLogout}
          className="w-full flex items-center gap-3 px-2 py-2 rounded transition-all duration-150"
          style={{ color: '#374151' }}
          onMouseEnter={e => (e.currentTarget.style.color = '#ef4444')}
          onMouseLeave={e => (e.currentTarget.style.color = '#374151')}
        >
          <span className="text-base w-5 text-center flex-shrink-0">⏻</span>
          <span className="hidden md:block text-[11px] tracking-[0.2em] uppercase font-mono">Salir</span>
        </button>
      </div>
    </aside>
  )
}

// ─── Main Dashboard ────────────────────────────────────────────────────────────

function Dashboard({ token, username, onLogout }: { token: string; username: string; onLogout: () => void }) {
  const [section, setSection] = useState<Section>('overview')

  const [overview,    setOverview]    = useState<OverviewData | null>(null)
  const [dropOff,     setDropOff]     = useState<DropOffData | null>(null)
  const [dakiStats,   setDakiStats]   = useState<DakiStatsData | null>(null)
  const [recentUsers, setRecentUsers] = useState<RecentUser[]>([])
  const [sectorBars,  setSectorBars]  = useState<SectorBar[]>([])
  const [loading,     setLoading]     = useState(true)
  const [error,       setError]       = useState('')

  const fetchAll = useCallback(async () => {
    setLoading(true)
    setError('')
    try {
      const [ov, do_, dk, ru] = await Promise.all([
        apiFetch<OverviewData>('/api/v1/admin/overview', token),
        apiFetch<DropOffData>('/api/v1/admin/drop-off', token),
        apiFetch<DakiStatsData>('/api/v1/admin/daki-stats', token),
        apiFetch<{ users: RecentUser[] }>('/api/v1/admin/recent-users', token),
      ])
      setOverview(ov)
      setDropOff(do_)
      setDakiStats(dk)
      setRecentUsers(ru.users)
      setSectorBars(buildSectorBars(do_, dk))
    } catch (err: unknown) {
      if (err instanceof Error && err.message === 'unauthorized') {
        onLogout()
      } else {
        setError('Error al cargar datos. Reintenta.')
      }
    } finally {
      setLoading(false)
    }
  }, [token, onLogout])

  useEffect(() => { fetchAll() }, [fetchAll])

  const CONTENT_CLS = 'ml-14 md:ml-52 min-h-screen p-6 md:p-8'

  if (loading) {
    return (
      <>
        <Sidebar active={section} onNav={setSection} username={username} onLogout={onLogout} />
        <main className={CONTENT_CLS} style={{ background: '#050508' }}>
          <div className="flex items-center justify-center h-[60vh]">
            <span className="font-mono text-sm animate-pulse" style={{ color: '#00FF41' }}>
              {'// CARGANDO DATOS DEL NEXO...'}
            </span>
          </div>
        </main>
      </>
    )
  }

  if (error) {
    return (
      <>
        <Sidebar active={section} onNav={setSection} username={username} onLogout={onLogout} />
        <main className={CONTENT_CLS} style={{ background: '#050508' }}>
          <div className="flex flex-col items-center justify-center h-[60vh] gap-4">
            <span className="font-mono text-sm" style={{ color: '#ef4444' }}>{'// '}{error}</span>
            <button
              onClick={fetchAll}
              className="font-mono text-xs px-4 py-2 tracking-widest"
              style={{ border: '1px solid #374151', color: '#6b7280' }}
            >
              REINTENTAR
            </button>
          </div>
        </main>
      </>
    )
  }

  return (
    <>
      <Sidebar active={section} onNav={setSection} username={username} onLogout={onLogout} />

      <main
        className={CONTENT_CLS}
        style={{ background: '#050508', color: '#e5e7eb' }}
      >
        {/* ── Scanlines ── */}
        <div
          className="fixed inset-0 pointer-events-none z-[1]"
          style={{
            backgroundImage: 'repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,0.05) 2px,rgba(0,0,0,0.05) 4px)',
          }}
        />

        <div className="relative z-[2] max-w-6xl mx-auto space-y-8">

          {/* ─ Header ─────────────────────────────────────────────────── */}
          <div className="flex items-start justify-between">
            <div>
              <p className="text-[9px] tracking-[0.7em] uppercase mb-1" style={{ color: '#00FF41', opacity: 0.5 }}>
                DAKI EdTech // CEO Dashboard
              </p>
              <h1 className="text-2xl font-black font-mono tracking-wider" style={{ color: '#f9fafb' }}>
                {section === 'overview' && 'Vista General'}
                {section === 'funnel'   && 'Embudo de Deserción'}
                {section === 'daki'     && 'Estadísticas DAKI'}
                {section === 'users'    && 'Usuarios Recientes'}
              </h1>
            </div>
            <div className="text-right hidden md:block">
              <p className="text-[10px] tracking-widest uppercase" style={{ color: '#374151' }}>Actualizado</p>
              <p className="text-[11px] font-mono" style={{ color: '#4b5563' }}>
                {overview ? formatDate(overview.generated_at) : '—'}
              </p>
              <button
                onClick={fetchAll}
                className="mt-1 text-[10px] tracking-widest uppercase transition-colors duration-150"
                style={{ color: '#374151' }}
                onMouseEnter={e => (e.currentTarget.style.color = '#00FF41')}
                onMouseLeave={e => (e.currentTarget.style.color = '#374151')}
              >
                ↻ Actualizar
              </button>
            </div>
          </div>

          {/* ════════════════════════════════════════════════════════════ */}
          {/* OVERVIEW                                                     */}
          {/* ════════════════════════════════════════════════════════════ */}
          {section === 'overview' && overview && (
            <div className="space-y-6">
              {/* KPI Cards */}
              <div>
                <SectionTitle>KPIs del Negocio</SectionTitle>
                <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
                  <StatCard
                    icon="◎"
                    label="Total Usuarios"
                    value={overview.total_users.toLocaleString()}
                    sub={`${overview.users_who_started} iniciaron algún nivel`}
                    accent="#00FF41"
                  />
                  <StatCard
                    icon="◷"
                    label="Activos (24h)"
                    value={overview.active_last_24h.toLocaleString()}
                    sub="usuarios con actividad reciente"
                    accent="#00bfff"
                  />
                  <StatCard
                    icon="◈"
                    label="Tasa Conversión"
                    value={`${overview.conversion_rate}%`}
                    sub={`${overview.paid_users} cuentas pagas`}
                    accent={overview.conversion_rate >= 5 ? '#22c55e' : '#f97316'}
                  />
                  <StatCard
                    icon="$"
                    label="Ingresos Proy."
                    value={`$${overview.projected_revenue_usd.toLocaleString('en-US', { minimumFractionDigits: 0 })}`}
                    sub={`USD · $${overview.license_price_usd}/licencia`}
                    accent="#a78bfa"
                  />
                </div>
              </div>

              {/* Retención */}
              <div>
                <SectionTitle>Retención y Progreso</SectionTitle>
                <div className="grid grid-cols-2 lg:grid-cols-3 gap-4">
                  <StatCard
                    icon="▶"
                    label="Empezaron"
                    value={overview.users_who_started}
                    sub="usuarios con ≥ 1 intento"
                    accent="#6b7280"
                  />
                  <StatCard
                    icon="✓"
                    label="Con Progreso"
                    value={overview.users_with_progress}
                    sub="completaron ≥ 1 nivel"
                    accent="#22c55e"
                  />
                  <StatCard
                    icon="★"
                    label="Completaron Todo"
                    value={overview.users_completed_all}
                    sub="llegaron al nivel 100"
                    accent="#f59e0b"
                  />
                </div>
              </div>

              {/* Top bottlenecks alert */}
              {dropOff && dropOff.top_bottlenecks.length > 0 && (
                <div
                  className="rounded border p-4"
                  style={{ background: '#150a0a', borderColor: '#7f1d1d' }}
                >
                  <p className="text-[10px] tracking-[0.4em] uppercase mb-2" style={{ color: '#ef4444' }}>
                    ⚠ Cuellos de botella detectados
                  </p>
                  <ul className="space-y-1">
                    {dropOff.top_bottlenecks.map(title => (
                      <li key={title} className="text-sm font-mono" style={{ color: '#fca5a5' }}>
                        → {title}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* DAKI global */}
              {dakiStats && (
                <div
                  className="rounded border p-4 flex flex-wrap gap-6"
                  style={{ background: '#0a0a15', borderColor: '#1a1a2e' }}
                >
                  <div>
                    <p className="text-[10px] tracking-widest uppercase mb-1" style={{ color: '#374151' }}>
                      Promedio pistas / nivel
                    </p>
                    <p className="text-2xl font-black font-mono" style={{ color: '#00bfff' }}>
                      {dakiStats.global_avg_hints}
                    </p>
                  </div>
                  {dakiStats.most_independent_level && (
                    <div>
                      <p className="text-[10px] tracking-widest uppercase mb-1" style={{ color: '#374151' }}>
                        Más autónomo
                      </p>
                      <p className="text-sm font-mono truncate max-w-[200px]" style={{ color: '#22c55e' }}>
                        {dakiStats.most_independent_level}
                      </p>
                    </div>
                  )}
                  {dakiStats.most_dependent_level && (
                    <div>
                      <p className="text-[10px] tracking-widest uppercase mb-1" style={{ color: '#374151' }}>
                        Más dependiente
                      </p>
                      <p className="text-sm font-mono truncate max-w-[200px]" style={{ color: '#f97316' }}>
                        {dakiStats.most_dependent_level}
                      </p>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}

          {/* ════════════════════════════════════════════════════════════ */}
          {/* FUNNEL                                                       */}
          {/* ════════════════════════════════════════════════════════════ */}
          {section === 'funnel' && dropOff && (
            <div className="space-y-6">
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-2">
                <StatCard icon="◈" label="Niveles con datos" value={dropOff.total_levels_with_data} accent="#00FF41" />
                <StatCard icon="⚠" label="Cuellos de botella" value={dropOff.top_bottlenecks.length} accent="#ef4444" />
                <StatCard
                  icon="▼"
                  label="Mayor deserción"
                  value={
                    sectorBars.length
                      ? `${Math.max(...sectorBars.map(s => s.dropOff))}%`
                      : '—'
                  }
                  accent="#f97316"
                />
              </div>

              <div className="rounded border p-5" style={{ background: '#0d0d1a', borderColor: '#1a1a2e' }}>
                <SectionTitle>Tasa de Deserción por Sector</SectionTitle>
                <p className="text-xs mb-4" style={{ color: '#374151' }}>
                  Verde {'<'} 25% · Naranja 25-40% · Rojo {'>'} 40% (cuello de botella)
                </p>
                <DropOffChart data={sectorBars} />
              </div>

              {/* Level detail table */}
              <div className="rounded border" style={{ background: '#0d0d1a', borderColor: '#1a1a2e' }}>
                <div className="px-5 py-4 border-b" style={{ borderColor: '#1a1a2e' }}>
                  <SectionTitle>Detalle por Nivel (Cuellos de Botella)</SectionTitle>
                </div>
                <div className="overflow-x-auto">
                  <table className="w-full text-xs font-mono">
                    <thead>
                      <tr style={{ color: '#374151', borderBottom: '1px solid #1a1a2e' }}>
                        {['#', 'Nivel', 'Intentaron', 'Atascados', 'Deserción', 'Avg. Intentos'].map(h => (
                          <th key={h} className="px-4 py-2.5 text-left tracking-widest uppercase text-[10px]">{h}</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {dropOff.levels
                        .filter(lv => lv.is_bottleneck)
                        .map(lv => (
                          <tr
                            key={lv.level_order}
                            style={{ borderBottom: '1px solid #0f0f1a', color: '#9ca3af' }}
                          >
                            <td className="px-4 py-2.5" style={{ color: '#4b5563' }}>{lv.level_order}</td>
                            <td className="px-4 py-2.5 max-w-[200px] truncate" style={{ color: '#fca5a5' }}>
                              {lv.title}
                            </td>
                            <td className="px-4 py-2.5">{lv.users_attempted}</td>
                            <td className="px-4 py-2.5" style={{ color: '#ef4444' }}>{lv.users_stuck}</td>
                            <td className="px-4 py-2.5" style={{ color: '#ef4444', fontWeight: 700 }}>
                              {lv.drop_off_rate}%
                            </td>
                            <td className="px-4 py-2.5">{lv.avg_attempts_stuck}</td>
                          </tr>
                        ))}
                      {dropOff.levels.filter(lv => lv.is_bottleneck).length === 0 && (
                        <tr>
                          <td colSpan={6} className="px-4 py-6 text-center" style={{ color: '#374151' }}>
                            {'// Sin cuellos de botella detectados'}
                          </td>
                        </tr>
                      )}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}

          {/* ════════════════════════════════════════════════════════════ */}
          {/* DAKI STATS                                                   */}
          {/* ════════════════════════════════════════════════════════════ */}
          {section === 'daki' && dakiStats && (
            <div className="space-y-6">
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-2">
                <StatCard icon="◎" label="Promedio pistas" value={dakiStats.global_avg_hints} accent="#00bfff" sub="por nivel" />
                <StatCard
                  icon="!"
                  label="Alertas autonomía"
                  value={dakiStats.levels.filter(l => l.autonomy_alert).length}
                  accent="#f97316"
                  sub="niveles con dependencia > 60"
                />
                <StatCard
                  icon="◈"
                  label="Niveles analizados"
                  value={dakiStats.levels.length}
                  accent="#6b7280"
                />
              </div>

              <div className="rounded border p-5" style={{ background: '#0d0d1a', borderColor: '#1a1a2e' }}>
                <SectionTitle>Score de Dependencia DAKI por Sector</SectionTitle>
                <p className="text-xs mb-4" style={{ color: '#374151' }}>
                  0 = usuarios autónomos · 100 = máxima dependencia de pistas
                </p>
                <DakiChart data={sectorBars} />
              </div>

              {/* Autonomy alerts */}
              {dakiStats.levels.filter(l => l.autonomy_alert).length > 0 && (
                <div className="rounded border" style={{ background: '#0d0d1a', borderColor: '#1a1a2e' }}>
                  <div className="px-5 py-4 border-b" style={{ borderColor: '#1a1a2e' }}>
                    <SectionTitle>Niveles con Alerta de Dependencia</SectionTitle>
                  </div>
                  <div className="overflow-x-auto">
                    <table className="w-full text-xs font-mono">
                      <thead>
                        <tr style={{ color: '#374151', borderBottom: '1px solid #1a1a2e' }}>
                          {['#', 'Nivel', 'Usuarios', 'Avg Pistas', '% Sin Pistas', '% Máx Pistas', 'Score'].map(h => (
                            <th key={h} className="px-4 py-2.5 text-left tracking-widest uppercase text-[10px]">{h}</th>
                          ))}
                        </tr>
                      </thead>
                      <tbody>
                        {dakiStats.levels
                          .filter(l => l.autonomy_alert)
                          .map(lv => (
                            <tr key={lv.level_order} style={{ borderBottom: '1px solid #0f0f1a', color: '#9ca3af' }}>
                              <td className="px-4 py-2.5" style={{ color: '#4b5563' }}>{lv.level_order}</td>
                              <td className="px-4 py-2.5 max-w-[200px] truncate" style={{ color: '#fdba74' }}>
                                {lv.title}
                              </td>
                              <td className="px-4 py-2.5">{lv.total_users}</td>
                              <td className="px-4 py-2.5">{lv.avg_hints}</td>
                              <td className="px-4 py-2.5" style={{ color: '#22c55e' }}>{lv.pct_no_hints}%</td>
                              <td className="px-4 py-2.5" style={{ color: '#f97316' }}>{lv.pct_max_hints}%</td>
                              <td className="px-4 py-2.5 font-bold" style={{ color: '#f97316' }}>
                                {lv.daki_dependency_score}
                              </td>
                            </tr>
                          ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* ════════════════════════════════════════════════════════════ */}
          {/* RECENT USERS                                                 */}
          {/* ════════════════════════════════════════════════════════════ */}
          {section === 'users' && (
            <div className="space-y-6">
              <div className="rounded border" style={{ background: '#0d0d1a', borderColor: '#1a1a2e' }}>
                <div className="px-5 py-4 border-b flex items-center justify-between" style={{ borderColor: '#1a1a2e' }}>
                  <SectionTitle>Últimos 10 Usuarios Registrados</SectionTitle>
                  <span className="text-[10px] tracking-widest uppercase" style={{ color: '#374151' }}>
                    {recentUsers.length} operadores
                  </span>
                </div>
                <div className="overflow-x-auto">
                  <table className="w-full text-xs font-mono">
                    <thead>
                      <tr style={{ color: '#374151', borderBottom: '1px solid #1a1a2e' }}>
                        {['Usuario', 'Email', 'Nivel', 'XP Total', 'Liga', 'Estado', 'Registro'].map(h => (
                          <th key={h} className="px-4 py-3 text-left tracking-widest uppercase text-[10px]">{h}</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {recentUsers.length === 0 && (
                        <tr>
                          <td colSpan={7} className="px-4 py-8 text-center" style={{ color: '#374151' }}>
                            {'// Sin usuarios registrados aún'}
                          </td>
                        </tr>
                      )}
                      {recentUsers.map((u, i) => (
                        <tr
                          key={u.id}
                          style={{
                            borderBottom: '1px solid #0f0f1a',
                            color: '#9ca3af',
                            background: i % 2 === 0 ? 'transparent' : '#0a0a10',
                          }}
                        >
                          <td className="px-4 py-3 font-bold" style={{ color: '#e5e7eb' }}>
                            {u.username}
                          </td>
                          <td className="px-4 py-3 max-w-[180px] truncate" style={{ color: '#6b7280' }}>
                            {u.email}
                          </td>
                          <td className="px-4 py-3">
                            <span
                              className="px-2 py-0.5 rounded"
                              style={{ background: '#0f172a', color: '#60a5fa', border: '1px solid #1e3a5f' }}
                            >
                              Lv. {u.current_level}
                            </span>
                          </td>
                          <td className="px-4 py-3" style={{ color: '#f59e0b' }}>
                            {u.total_xp.toLocaleString()} XP
                          </td>
                          <td className="px-4 py-3">
                            <LeagueBadge tier={u.league_tier} />
                          </td>
                          <td className="px-4 py-3">
                            <Pill label={u.is_paid ? 'PAID' : 'FREE'} active={u.is_paid} />
                          </td>
                          <td className="px-4 py-3" style={{ color: '#4b5563' }}>
                            {formatDate(u.created_at)}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}

        </div>
      </main>
    </>
  )
}

// ─── Root export ───────────────────────────────────────────────────────────────

export default function AdminDashboardPage() {
  const [token,    setToken]    = useState<string | null>(null)
  const [username, setUsername] = useState('')

  useEffect(() => {
    const stored = localStorage.getItem('daki_admin_token')
    const storedUser = localStorage.getItem('daki_admin_username')
    if (stored) { setToken(stored); setUsername(storedUser ?? '') }
  }, [])

  const handleLogin = (tok: string, user: string) => {
    localStorage.setItem('daki_admin_token', tok)
    localStorage.setItem('daki_admin_username', user)
    setToken(tok)
    setUsername(user)
  }

  const handleLogout = () => {
    localStorage.removeItem('daki_admin_token')
    localStorage.removeItem('daki_admin_username')
    setToken(null)
    setUsername('')
  }

  if (!token) return <LoginScreen onLogin={handleLogin} />
  return <Dashboard token={token} username={username} onLogout={handleLogout} />
}
