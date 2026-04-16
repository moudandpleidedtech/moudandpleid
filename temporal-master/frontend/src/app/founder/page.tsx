'use client'

import { useState, useEffect, useCallback } from 'react'
import { useRouter } from 'next/navigation'
import { useUserStore } from '@/store/userStore'

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? ''

// ─── JWT helpers ──────────────────────────────────────────────────────────────

/** Decodifica el payload del JWT sin verificar firma (solo para leer exp). */
function jwtExpiry(token: string): number {
  try {
    const payload = token.split('.')[1]
    const decoded = JSON.parse(atob(payload.replace(/-/g, '+').replace(/_/g, '/')))
    return typeof decoded.exp === 'number' ? decoded.exp : 0
  } catch {
    return 0
  }
}

/** Retorna el token solo si existe y NO está vencido (con 30s de margen). */
function getValidToken(): string {
  if (typeof window === 'undefined') return ''
  const raw = localStorage.getItem('daki_token') ?? ''
  if (!raw) return ''
  const exp = jwtExpiry(raw)
  return exp > 0 && Date.now() / 1000 < exp - 30 ? raw : ''
}

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
  return `hace ${Math.floor(h / 24)}d`
}

function subBadge(status: string) {
  if (status === 'ACTIVE')  return { label: 'ACTIVE',   color: '#00FF41' }
  if (status === 'TRIAL')   return { label: 'TRIAL',    color: '#FFC700' }
  return                           { label: 'INACTIVE', color: '#6b7280' }
}

// ─── Page ──────────────────────────────────────────────────────────────────────

export default function FounderPage() {
  const router = useRouter()
  const { _hasHydrated, userId } = useUserStore()

  const [data,    setData]    = useState<UsersProgressResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error,   setError]   = useState('')
  const [search,  setSearch]  = useState('')
  const [sortBy,  setSortBy]  = useState<'last_login' | 'current_level' | 'total_xp' | 'challenges_completed'>('last_login')
  const [sortAsc, setSortAsc] = useState(false)

  // Guard: redirige si no está autenticado (el API responde 403 si no es FOUNDER)
  useEffect(() => {
    if (!_hasHydrated) return
    if (!userId) router.replace('/hub')
  }, [_hasHydrated, userId, router])

  const fetchData = useCallback(async () => {
    setLoading(true); setError('')
    try {
      // Producción: frontend y backend son cross-domain (Vercel ↔ Render).
      // Usamos el JWT de localStorage solo si está vigente (SameSite=lax bloquea
      // la cookie en fetch cross-origin en Firefox/Safari). Si el JWT expiró,
      // lo omitimos y dejamos que la cookie httpOnly actúe vía el proxy de Next.js.
      const token = getValidToken()

      const res = await fetch(`${API_BASE}/api/v1/admin/users-progress`, {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
        credentials: 'include',
      })
      if (res.status === 401 || res.status === 403) {
        router.replace('/hub'); return
      }
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      const json = await res.json() as UsersProgressResponse
      setData(json)
    } catch {
      setError('Error al cargar datos. Intentá de nuevo.')
    } finally {
      setLoading(false)
    }
  }, [router])

  useEffect(() => {
    if (_hasHydrated && userId) fetchData()
  }, [_hasHydrated, userId, fetchData])

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
      const va = a[sortBy] ?? ''
      const vb = b[sortBy] ?? ''
      const cmp = va < vb ? -1 : va > vb ? 1 : 0
      return sortAsc ? cmp : -cmp
    })

  const users         = data?.users ?? []
  const activeCount   = users.filter(u => u.subscription_status === 'ACTIVE').length
  const trialCount    = users.filter(u => u.subscription_status === 'TRIAL').length
  const avgLevel      = users.length ? Math.round(users.reduce((s, u) => s + (u.current_level ?? 0), 0) / users.length) : 0
  const activeLast24h = users.filter(u => {
    if (!u.last_login) return false
    try { return Date.now() - new Date(u.last_login).getTime() < 86_400_000 } catch { return false }
  }).length

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

  if (!_hasHydrated) return null

  return (
    <div className="min-h-screen font-mono" style={{ background: '#020617', color: '#e5e7eb' }}>

      {/* ── Header ── */}
      <header className="flex items-center justify-between px-6 py-3 border-b" style={{ borderColor: 'rgba(6,182,212,0.20)' }}>
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
          <span style={{ color: '#1a1a2e' }}>|</span>
          <h1 className="text-sm font-black tracking-[0.3em]" style={{ color: '#FFC700', textShadow: '0 0 10px rgba(255,199,0,0.3)' }}>
            ◈ PANEL DE DATOS
          </h1>
        </div>
        <div className="flex items-center gap-4">
          <button
            onClick={fetchData}
            className="text-[9px] tracking-widest uppercase border px-3 py-1 transition-all"
            style={{ borderColor: '#1a1a2e', color: '#4b5563' }}
            onMouseEnter={e => { e.currentTarget.style.color = '#00FF41'; e.currentTarget.style.borderColor = '#00FF4133' }}
            onMouseLeave={e => { e.currentTarget.style.color = '#4b5563'; e.currentTarget.style.borderColor = '#1a1a2e' }}
          >
            ↻ REFRESH
          </button>
        </div>
      </header>

      <main className="p-6 space-y-6">

        {/* ── KPI Cards ── */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {[
            { label: 'Usuarios totales',  value: data?.total ?? '—', color: '#e5e7eb' },
            { label: 'Suscritos activos', value: activeCount,         color: '#00FF41' },
            { label: 'En trial',          value: trialCount,          color: '#FFC700' },
            { label: 'Activos (24h)',      value: activeLast24h,       color: '#60a5fa' },
          ].map(k => (
            <div key={k.label} className="rounded border p-4 space-y-1" style={{ background: '#030b18', borderColor: 'rgba(6,182,212,0.18)' }}>
              <p className="text-[9px] tracking-widest uppercase" style={{ color: '#4b5563' }}>{k.label}</p>
              <p className="text-2xl font-black" style={{ color: k.color }}>{k.value}</p>
            </div>
          ))}
        </div>

        {/* ── Search ── */}
        <div className="flex flex-wrap items-center gap-3">
          <input
            value={search}
            onChange={e => setSearch(e.target.value)}
            placeholder="Buscar por email o callsign..."
            className="flex-1 min-w-[220px] px-3 py-2 rounded text-sm font-mono outline-none"
            style={{ background: '#030b18', border: '1px solid rgba(6,182,212,0.20)', color: '#e5e7eb', caretColor: '#FFC700' }}
          />
          <span className="text-[9px] tracking-widest uppercase" style={{ color: '#374151' }}>
            {filtered.length} / {data?.total ?? '—'} usuarios
          </span>
        </div>

        {/* ── Table ── */}
        {loading ? (
          <p className="text-sm animate-pulse text-center py-16" style={{ color: '#374151' }}>
            {'// CARGANDO DATOS...'}
          </p>
        ) : error ? (
          <div className="text-center py-8 space-y-3">
            <p className="text-sm" style={{ color: '#ef4444' }}>{error}</p>
            <button onClick={fetchData} className="text-xs border px-4 py-2" style={{ borderColor: '#374151', color: '#6b7280' }}>
              Reintentar
            </button>
          </div>
        ) : (
          <div className="rounded border overflow-x-auto" style={{ borderColor: 'rgba(6,182,212,0.18)' }}>
            <table className="w-full text-xs font-mono">
              <thead>
                <tr style={{ background: '#030b18', borderBottom: '1px solid rgba(6,182,212,0.12)' }}>
                  <th className="text-left px-4 py-3 text-[9px] tracking-widest uppercase" style={{ color: '#4b5563' }}>Callsign</th>
                  <th className="text-left px-4 py-3 text-[9px] tracking-widest uppercase" style={{ color: '#4b5563' }}>Email</th>
                  <th className="px-4 py-3 text-center"><SortBtn col="current_level"        label="Nivel" /></th>
                  <th className="px-4 py-3 text-center"><SortBtn col="total_xp"             label="XP" /></th>
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
                      style={{ background: i % 2 === 0 ? '#020617' : '#030c1a', borderBottom: '1px solid rgba(6,182,212,0.06)' }}
                    >
                      <td className="px-4 py-2.5 font-black" style={{ color: '#e5e7eb' }}>
                        {u.callsign}
                        {u.streak_days > 0 && (
                          <span className="ml-2 text-[9px]" style={{ color: '#f97316' }}>🔥{u.streak_days}</span>
                        )}
                      </td>
                      <td className="px-4 py-2.5" style={{ color: '#6b7280' }}>{u.email}</td>
                      <td className="px-4 py-2.5 text-center font-black" style={{ color: '#00FF41' }}>{u.current_level}</td>
                      <td className="px-4 py-2.5 text-center" style={{ color: '#9ca3af' }}>{(u.total_xp ?? 0).toLocaleString()}</td>
                      <td className="px-4 py-2.5 text-center" style={{ color: '#60a5fa' }}>{u.challenges_completed ?? 0}</td>
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
            <div className="px-4 py-2 border-t flex items-center gap-6" style={{ borderColor: 'rgba(6,182,212,0.10)', background: '#030b18' }}>
              <span className="text-[9px] tracking-widest uppercase" style={{ color: '#374151' }}>
                NIV. PROMEDIO: <strong style={{ color: '#e5e7eb' }}>{avgLevel}</strong>
              </span>
              <span className="text-[9px] tracking-widest uppercase" style={{ color: '#374151' }}>
                XP TOTAL: <strong style={{ color: '#e5e7eb' }}>{users.reduce((s, u) => s + (u.total_xp ?? 0), 0).toLocaleString()}</strong>
              </span>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}
