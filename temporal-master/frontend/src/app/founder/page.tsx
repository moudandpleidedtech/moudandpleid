'use client'

import { useState, useEffect, useCallback } from 'react'
import { useRouter } from 'next/navigation'

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? ''
const TOKEN_KEY = 'daki_admin_token'
const USER_KEY  = 'daki_admin_user'

// ─── Types ─────────────────────────────────────────────────────────────────────

interface UserRow {
  id: string
  callsign: string
  email: string
  current_level: number
  total_xp: number
  subscription_status: string
  last_login: string | null
  created_at: string
  challenges_completed: number
  streak_days: number
}

interface UsersProgressResponse {
  total: number
  users: UserRow[]
}

// ─── Helpers ───────────────────────────────────────────────────────────────────

function fmtDate(iso: string | null): string {
  if (!iso) return '—'
  return new Date(iso).toLocaleDateString('es-AR', {
    day: '2-digit', month: 'short', year: '2-digit',
  })
}

function fmtRelative(iso: string | null): string {
  if (!iso) return '—'
  const diff = Date.now() - new Date(iso).getTime()
  const m = Math.floor(diff / 60000)
  if (m < 60)  return `hace ${m}m`
  const h = Math.floor(m / 60)
  if (h < 24)  return `hace ${h}h`
  const d = Math.floor(h / 24)
  return `hace ${d}d`
}

function subBadge(status: string) {
  if (status === 'ACTIVE')   return { label: 'ACTIVE',  color: '#00FF41' }
  if (status === 'TRIAL')    return { label: 'TRIAL',   color: '#FFC700' }
  return                            { label: 'INACTIVE', color: '#6b7280' }
}

// ─── Login Gate ────────────────────────────────────────────────────────────────

function LoginGate({ onLogin }: { onLogin: (token: string, user: string) => void }) {
  const [callsign, setCallsign] = useState('')
  const [password, setPassword] = useState('')
  const [error,    setError]    = useState('')
  const [loading,  setLoading]  = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true); setError('')
    try {
      const res = await fetch(`${API_BASE}/api/v1/admin/auth/token`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ callsign, password }),
      })
      if (!res.ok) throw new Error('Credenciales inválidas')
      const data = await res.json() as { access_token: string; callsign: string }
      localStorage.setItem(TOKEN_KEY, data.access_token)
      localStorage.setItem(USER_KEY,  data.callsign)
      onLogin(data.access_token, data.callsign)
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Error desconocido')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center font-mono" style={{ background: '#050508', color: '#e5e7eb' }}>
      <div className="w-full max-w-sm space-y-6 px-4">
        <div className="text-center space-y-1">
          <p className="text-[9px] tracking-[0.6em] uppercase" style={{ color: '#374151' }}>DAKI // FOUNDER ACCESS</p>
          <h1 className="text-xl font-black tracking-widest" style={{ color: '#FFC700', textShadow: '0 0 16px rgba(255,199,0,0.4)' }}>
            PANEL DE DATOS
          </h1>
        </div>
        <form onSubmit={handleSubmit} className="rounded border p-6 space-y-4" style={{ background: '#0d0d1a', borderColor: '#1a1a2e' }}>
          <div>
            <label className="block text-[10px] tracking-widest uppercase mb-2" style={{ color: '#4b5563' }}>Callsign</label>
            <input
              value={callsign}
              onChange={e => setCallsign(e.target.value)}
              required autoFocus
              className="w-full px-3 py-2.5 rounded font-mono text-sm outline-none"
              style={{ background: '#050508', border: '1px solid #1a1a2e', color: '#e5e7eb', caretColor: '#FFC700' }}
            />
          </div>
          <div>
            <label className="block text-[10px] tracking-widest uppercase mb-2" style={{ color: '#4b5563' }}>Contraseña</label>
            <input
              type="password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              required
              className="w-full px-3 py-2.5 rounded font-mono text-sm outline-none"
              style={{ background: '#050508', border: '1px solid #1a1a2e', color: '#e5e7eb', caretColor: '#FFC700' }}
            />
          </div>
          {error && <p className="text-xs" style={{ color: '#ef4444' }}>{error}</p>}
          <button
            type="submit" disabled={loading}
            className="w-full py-3 font-mono text-sm tracking-[0.2em] uppercase transition-all"
            style={{ background: loading ? '#1c1505' : '#FFC700', color: '#000', cursor: loading ? 'not-allowed' : 'pointer' }}
          >
            {loading ? '[ AUTENTICANDO... ]' : '[ ACCEDER ]'}
          </button>
        </form>
      </div>
    </div>
  )
}

// ─── Dashboard ─────────────────────────────────────────────────────────────────

function FounderDashboard({ token, adminUser, onLogout }: { token: string; adminUser: string; onLogout: () => void }) {
  const router = useRouter()
  const [data,    setData]    = useState<UsersProgressResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error,   setError]   = useState('')
  const [search,  setSearch]  = useState('')
  const [sortBy,  setSortBy]  = useState<'last_login' | 'current_level' | 'total_xp' | 'challenges_completed'>('last_login')
  const [sortAsc, setSortAsc] = useState(false)

  const fetchData = useCallback(async () => {
    setLoading(true); setError('')
    try {
      const res = await fetch(`${API_BASE}/api/v1/admin/users-progress`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      if (res.status === 401) { onLogout(); return }
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      const json = await res.json() as UsersProgressResponse
      setData(json)
    } catch {
      setError('Error al cargar datos.')
    } finally {
      setLoading(false)
    }
  }, [token, onLogout])

  useEffect(() => { fetchData() }, [fetchData])

  const toggleSort = (col: typeof sortBy) => {
    if (sortBy === col) setSortAsc(v => !v)
    else { setSortBy(col); setSortAsc(false) }
  }

  const filtered = (data?.users ?? [])
    .filter(u =>
      u.email.toLowerCase().includes(search.toLowerCase()) ||
      u.callsign.toLowerCase().includes(search.toLowerCase())
    )
    .sort((a, b) => {
      let va: number | string = a[sortBy] ?? ''
      let vb: number | string = b[sortBy] ?? ''
      if (sortBy === 'last_login') { va = va || ''; vb = vb || '' }
      const cmp = va < vb ? -1 : va > vb ? 1 : 0
      return sortAsc ? cmp : -cmp
    })

  // Quick stats
  const users = data?.users ?? []
  const activeCount   = users.filter(u => u.subscription_status === 'ACTIVE').length
  const trialCount    = users.filter(u => u.subscription_status === 'TRIAL').length
  const avgLevel      = users.length ? Math.round(users.reduce((s, u) => s + u.current_level, 0) / users.length) : 0
  const activeLast24h = users.filter(u => u.last_login && (Date.now() - new Date(u.last_login).getTime()) < 86400000).length

  const SortBtn = ({ col, label }: { col: typeof sortBy; label: string }) => (
    <button
      onClick={() => toggleSort(col)}
      className="flex items-center gap-1 text-[10px] tracking-widest uppercase transition-colors"
      style={{ color: sortBy === col ? '#FFC700' : '#4b5563' }}
    >
      {label}
      <span style={{ opacity: sortBy === col ? 1 : 0.3 }}>{sortAsc ? '↑' : '↓'}</span>
    </button>
  )

  return (
    <div className="min-h-screen font-mono" style={{ background: '#050508', color: '#e5e7eb' }}>

      {/* ── Header ─────────────────────────────────────────────── */}
      <header className="flex items-center justify-between px-6 py-3 border-b" style={{ borderColor: '#0f0f1a' }}>
        <div className="flex items-center gap-4">
          <button
            onClick={() => router.push('/hub')}
            className="text-[10px] tracking-widest uppercase transition-colors"
            style={{ color: '#374151' }}
            onMouseEnter={e => (e.currentTarget.style.color = '#FFC700')}
            onMouseLeave={e => (e.currentTarget.style.color = '#374151')}
          >
            ← HUB
          </button>
          <span className="text-[8px] tracking-[0.5em] uppercase" style={{ color: '#1a1a2e' }}>|</span>
          <h1 className="text-sm font-black tracking-[0.3em]" style={{ color: '#FFC700', textShadow: '0 0 10px rgba(255,199,0,0.3)' }}>
            ◈ PANEL DE DATOS
          </h1>
        </div>
        <div className="flex items-center gap-4">
          <span className="text-[9px] tracking-wider hidden sm:block" style={{ color: '#374151' }}>{adminUser}</span>
          <button
            onClick={() => { fetchData() }}
            className="text-[9px] tracking-widest uppercase border px-3 py-1 transition-all"
            style={{ borderColor: '#1a1a2e', color: '#4b5563' }}
            onMouseEnter={e => { e.currentTarget.style.color = '#00FF41'; e.currentTarget.style.borderColor = '#00FF4133' }}
            onMouseLeave={e => { e.currentTarget.style.color = '#4b5563'; e.currentTarget.style.borderColor = '#1a1a2e' }}
          >
            ↻ REFRESH
          </button>
          <button
            onClick={onLogout}
            className="text-[9px] tracking-widest uppercase transition-colors"
            style={{ color: '#374151' }}
            onMouseEnter={e => (e.currentTarget.style.color = '#ef4444')}
            onMouseLeave={e => (e.currentTarget.style.color = '#374151')}
          >
            SALIR
          </button>
        </div>
      </header>

      <main className="p-6 space-y-6">

        {/* ── KPI Cards ──────────────────────────────────────────── */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {[
            { label: 'Usuarios totales',  value: data?.total ?? '—',  color: '#e5e7eb' },
            { label: 'Suscritos activos', value: activeCount,          color: '#00FF41' },
            { label: 'En trial',          value: trialCount,           color: '#FFC700' },
            { label: 'Activos (24h)',      value: activeLast24h,        color: '#60a5fa' },
          ].map(k => (
            <div key={k.label} className="rounded border p-4 space-y-1" style={{ background: '#0d0d1a', borderColor: '#1a1a2e' }}>
              <p className="text-[9px] tracking-widest uppercase" style={{ color: '#4b5563' }}>{k.label}</p>
              <p className="text-2xl font-black" style={{ color: k.color }}>{k.value}</p>
            </div>
          ))}
        </div>

        {/* ── Search + Sort ──────────────────────────────────────── */}
        <div className="flex flex-wrap items-center gap-3">
          <input
            value={search}
            onChange={e => setSearch(e.target.value)}
            placeholder="Buscar por email o callsign..."
            className="flex-1 min-w-[220px] px-3 py-2 rounded text-sm font-mono outline-none"
            style={{ background: '#0d0d1a', border: '1px solid #1a1a2e', color: '#e5e7eb', caretColor: '#FFC700' }}
          />
          <span className="text-[9px] tracking-widest uppercase" style={{ color: '#374151' }}>
            {filtered.length} / {data?.total ?? '—'} usuarios
          </span>
        </div>

        {/* ── Table ─────────────────────────────────────────────── */}
        {loading ? (
          <p className="text-sm animate-pulse text-center py-16" style={{ color: '#374151' }}>
            {'// CARGANDO DATOS...'}
          </p>
        ) : error ? (
          <p className="text-sm text-center py-8" style={{ color: '#ef4444' }}>{error}</p>
        ) : (
          <div className="rounded border overflow-x-auto" style={{ borderColor: '#1a1a2e' }}>
            <table className="w-full text-xs font-mono">
              <thead>
                <tr style={{ background: '#0d0d1a', borderBottom: '1px solid #1a1a2e' }}>
                  <th className="text-left px-4 py-3 text-[9px] tracking-widest uppercase" style={{ color: '#4b5563' }}>Callsign</th>
                  <th className="text-left px-4 py-3 text-[9px] tracking-widest uppercase" style={{ color: '#4b5563' }}>Email</th>
                  <th className="px-4 py-3 text-center"><SortBtn col="current_level"       label="Nivel" /></th>
                  <th className="px-4 py-3 text-center"><SortBtn col="total_xp"            label="XP" /></th>
                  <th className="px-4 py-3 text-center"><SortBtn col="challenges_completed" label="Completados" /></th>
                  <th className="text-left px-4 py-3 text-[9px] tracking-widest uppercase" style={{ color: '#4b5563' }}>Suscripción</th>
                  <th className="px-4 py-3 text-center"><SortBtn col="last_login" label="Último login" /></th>
                  <th className="text-left px-4 py-3 text-[9px] tracking-widest uppercase" style={{ color: '#4b5563' }}>Registro</th>
                </tr>
              </thead>
              <tbody>
                {filtered.length === 0 ? (
                  <tr>
                    <td colSpan={8} className="text-center py-12" style={{ color: '#374151' }}>
                      No se encontraron usuarios.
                    </td>
                  </tr>
                ) : filtered.map((u, i) => {
                  const badge = subBadge(u.subscription_status)
                  return (
                    <tr
                      key={u.id}
                      style={{
                        background: i % 2 === 0 ? '#050508' : '#080810',
                        borderBottom: '1px solid #0f0f1a',
                      }}
                    >
                      <td className="px-4 py-2.5 font-black" style={{ color: '#e5e7eb' }}>
                        {u.callsign}
                        {u.streak_days > 0 && (
                          <span className="ml-2 text-[9px]" style={{ color: '#f97316' }}>
                            🔥{u.streak_days}
                          </span>
                        )}
                      </td>
                      <td className="px-4 py-2.5" style={{ color: '#6b7280' }}>{u.email}</td>
                      <td className="px-4 py-2.5 text-center font-black" style={{ color: '#00FF41' }}>
                        {u.current_level}
                      </td>
                      <td className="px-4 py-2.5 text-center" style={{ color: '#9ca3af' }}>
                        {u.total_xp.toLocaleString()}
                      </td>
                      <td className="px-4 py-2.5 text-center" style={{ color: '#60a5fa' }}>
                        {u.challenges_completed}
                      </td>
                      <td className="px-4 py-2.5">
                        <span
                          className="text-[9px] font-black tracking-widest border px-2 py-0.5 rounded"
                          style={{ color: badge.color, borderColor: `${badge.color}40`, background: `${badge.color}10` }}
                        >
                          {badge.label}
                        </span>
                      </td>
                      <td className="px-4 py-2.5 text-center" style={{ color: '#6b7280' }}>
                        <span title={u.last_login ?? undefined}>{fmtRelative(u.last_login)}</span>
                      </td>
                      <td className="px-4 py-2.5" style={{ color: '#374151' }}>{fmtDate(u.created_at)}</td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
            {/* Footer summary */}
            <div className="px-4 py-2 border-t flex items-center gap-6" style={{ borderColor: '#0f0f1a', background: '#0d0d1a' }}>
              <span className="text-[9px] tracking-widest uppercase" style={{ color: '#374151' }}>
                NIV. PROMEDIO: <strong style={{ color: '#e5e7eb' }}>{avgLevel}</strong>
              </span>
              <span className="text-[9px] tracking-widest uppercase" style={{ color: '#374151' }}>
                XP TOTAL PLATAFORMA: <strong style={{ color: '#e5e7eb' }}>
                  {users.reduce((s, u) => s + u.total_xp, 0).toLocaleString()}
                </strong>
              </span>
            </div>
          </div>
        )}

      </main>
    </div>
  )
}

// ─── Page ──────────────────────────────────────────────────────────────────────

export default function FounderPage() {
  const [token,     setToken]     = useState<string | null>(null)
  const [adminUser, setAdminUser] = useState('')

  useEffect(() => {
    const stored = localStorage.getItem(TOKEN_KEY)
    const user   = localStorage.getItem(USER_KEY)
    if (stored) { setToken(stored); setAdminUser(user ?? '') }
  }, [])

  const handleLogin = (tok: string, user: string) => {
    setToken(tok); setAdminUser(user)
  }

  const handleLogout = () => {
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(USER_KEY)
    setToken(null); setAdminUser('')
  }

  if (!token) return <LoginGate onLogin={handleLogin} />
  return <FounderDashboard token={token} adminUser={adminUser} onLogout={handleLogout} />
}
