import Link from 'next/link'
import type { Metadata } from 'next'
import LeaderboardRow from '@/components/UI/LeaderboardRow'

export const metadata: Metadata = {
  title: 'Comunidad | DAKI EdTech — Operadores de Python en LATAM',
  description: 'El ranking de Operadores de Python de DAKI EdTech. Competí, subí de liga y demostrá tu dominio del lenguaje con código real.',
  alternates: { canonical: 'https://dakiedtech.com/comunidad' },
}

export const revalidate = 60

interface LeaderboardEntry {
  rank:                 number
  callsign:             string
  total_xp:             number
  current_level:        number
  streak_days:          number
  league_tier:          string
  completed_challenges: number
}

interface LeaderboardResponse {
  top50:         LeaderboardEntry[]
  total_players: number
}

const TIER_COLOR: Record<string, string> = {
  'Arquitecto Supremo': '#f59e0b',
  'Diamante':           '#06b6d4',
  'Oro':                '#fbbf24',
  'Plata':              '#94a3b8',
  'Bronce':             '#b45309',
}

const TIER_GLYPH: Record<string, string> = {
  'Arquitecto Supremo': '◆',
  'Diamante':           '◈',
  'Oro':                '▲',
  'Plata':              '▸',
  'Bronce':             '·',
}

async function getLeaderboard(): Promise<LeaderboardResponse | null> {
  const api = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000'
  try {
    const res = await fetch(`${api}/api/v1/leaderboard`, {
      next: { revalidate: 60 },
    })
    if (!res.ok) return null
    return res.json()
  } catch {
    return null
  }
}

export default async function ComunidadPage() {
  const data = await getLeaderboard()
  const entries    = data?.top50         ?? []
  const totalPlayers = data?.total_players ?? 0

  return (
    <main className="min-h-screen bg-[#020202] font-mono text-[#00FF41] pt-14">

      <div
        className="fixed inset-0 pointer-events-none z-0 opacity-[0.015]"
        style={{ backgroundImage: 'repeating-linear-gradient(0deg,transparent,transparent 3px,#00FF41 3px,#00FF41 4px)' }}
      />

      <div className="relative z-10 max-w-4xl mx-auto px-6 py-16">

        {/* Breadcrumb */}
        <div className="flex items-center gap-2 mb-10 text-[8px] tracking-[0.35em] uppercase">
          <Link href="/" className="text-[#00FF41]/28 hover:text-[#00FF41]/55 transition-colors">NEXO</Link>
          <span className="text-[#00FF41]/15">›</span>
          <span className="text-[#00FF41]/45">COMUNIDAD</span>
        </div>

        {/* Header */}
        <header className="mb-10">
          <p className="text-[8px] tracking-[0.6em] text-[#00FF41]/25 uppercase mb-3">
            {'// CLASIFICACIÓN GLOBAL — OPERADORES EN ACTIVO'}
          </p>
          <h1 className="text-3xl sm:text-4xl font-black tracking-[0.05em] uppercase text-white/85 mb-4 leading-tight">
            El Nexo{' '}
            <span className="text-[#00FF41]" style={{ textShadow: '0 0 28px rgba(0,255,65,0.4)' }}>
              compite.
            </span>
          </h1>
          <p className="text-sm text-white/40 leading-relaxed max-w-xl mb-4">
            Ranking en tiempo real de Operadores activos. XP ganado con código real — no con múltiple choice.
          </p>

          {/* Stats strip */}
          <div className="flex flex-wrap gap-6 border-t border-[#00FF41]/10 pt-4">
            <div>
              <span className="text-lg font-black text-[#00FF41]">{totalPlayers}</span>
              <span className="text-[9px] tracking-[0.35em] text-[#00FF41]/35 ml-2 uppercase">Operadores</span>
            </div>
            <div>
              <span className="text-lg font-black text-[#00FF41]">5</span>
              <span className="text-[9px] tracking-[0.35em] text-[#00FF41]/35 ml-2 uppercase">Ligas</span>
            </div>
            <div>
              <span className="text-lg font-black text-[#00FF41]">195</span>
              <span className="text-[9px] tracking-[0.35em] text-[#00FF41]/35 ml-2 uppercase">Misiones</span>
            </div>
          </div>
        </header>

        {/* Liga legend */}
        <div className="flex flex-wrap gap-3 mb-6">
          {Object.entries(TIER_GLYPH).map(([tier, glyph]) => {
            const color = TIER_COLOR[tier] ?? '#00FF41'
            return (
              <div key={tier} className="flex items-center gap-1.5">
                <span className="text-xs font-bold" style={{ color }}>{glyph}</span>
                <span className="text-[9px] tracking-[0.3em] uppercase" style={{ color: `${color}70` }}>{tier}</span>
              </div>
            )
          })}
        </div>

        {/* Leaderboard table */}
        {entries.length === 0 ? (
          <div className="border border-[#00FF41]/10 p-8 text-center">
            <p className="text-[#00FF41]/30 text-[10px] tracking-[0.4em] uppercase">
              {data === null
                ? '// CONECTANDO CON EL NEXO...'
                : '// AÚN NO HAY OPERADORES CLASIFICADOS'}
            </p>
            {data === null && (
              <p className="text-white/20 text-[9px] mt-2">Intentá de nuevo en unos segundos.</p>
            )}
          </div>
        ) : (
          <div className="border border-[#00FF41]/10 overflow-hidden">

            {/* Table header */}
            <div
              className="grid text-[8px] tracking-[0.35em] uppercase px-4 py-2.5 border-b"
              style={{
                gridTemplateColumns: '40px 1fr 80px 70px 70px 80px',
                borderColor: 'rgba(0,255,65,0.10)',
                background: 'rgba(0,255,65,0.03)',
                color: 'rgba(0,255,65,0.30)',
              }}
            >
              <span>#</span>
              <span>Operador</span>
              <span className="text-right">XP</span>
              <span className="text-right hidden sm:block">Nivel</span>
              <span className="text-right hidden sm:block">Racha</span>
              <span className="text-right hidden sm:block">Misiones</span>
            </div>

            {/* Rows */}
            {entries.map((entry, i) => {
              const tierColor = TIER_COLOR[entry.league_tier] ?? '#00FF41'
              const tierGlyph = TIER_GLYPH[entry.league_tier] ?? '·'
              const isTop3    = entry.rank <= 3

              return (
                <LeaderboardRow
                  key={entry.rank}
                  tierColor={tierColor}
                  isTop3={isTop3}
                  className="grid items-center px-4 py-3 border-b transition-colors duration-150"
                  style={{
                    gridTemplateColumns: '40px 1fr 80px 70px 70px 80px',
                    borderColor: 'rgba(0,255,65,0.06)',
                  }}
                >
                  {/* Rank */}
                  <span
                    className="text-sm font-black"
                    style={{ color: isTop3 ? tierColor : 'rgba(255,255,255,0.2)' }}
                  >
                    {entry.rank <= 3
                      ? ['①', '②', '③'][entry.rank - 1]
                      : entry.rank
                    }
                  </span>

                  {/* Callsign + liga */}
                  <div className="flex items-center gap-2 min-w-0">
                    <span
                      className="text-sm font-bold shrink-0"
                      style={{ color: tierColor, textShadow: isTop3 ? `0 0 12px ${tierColor}60` : 'none' }}
                    >
                      {tierGlyph}
                    </span>
                    <div className="min-w-0">
                      <p
                        className="text-[11px] font-bold tracking-wide truncate"
                        style={{ color: isTop3 ? 'rgba(255,255,255,0.85)' : 'rgba(255,255,255,0.60)' }}
                      >
                        {entry.callsign}
                      </p>
                      <p className="text-[8px] tracking-[0.25em] uppercase" style={{ color: `${tierColor}55` }}>
                        {entry.league_tier}
                      </p>
                    </div>
                  </div>

                  {/* XP */}
                  <span
                    className="text-[11px] font-bold text-right"
                    style={{ color: isTop3 ? tierColor : 'rgba(255,255,255,0.45)' }}
                  >
                    {entry.total_xp.toLocaleString()}
                  </span>

                  {/* Nivel */}
                  <span className="text-[10px] text-right text-white/35 hidden sm:block">
                    Lv {entry.current_level}
                  </span>

                  {/* Racha */}
                  <span className="text-[10px] text-right text-white/30 hidden sm:block">
                    {entry.streak_days > 0 ? `🔥 ${entry.streak_days}d` : '—'}
                  </span>

                  {/* Misiones */}
                  <span className="text-[10px] text-right text-white/30 hidden sm:block">
                    {entry.completed_challenges}
                  </span>
                </LeaderboardRow>
              )
            })}
          </div>
        )}

        {/* CTA para entrar */}
        <div
          className="mt-8 p-6 border-l-2"
          style={{ borderColor: '#00FF41', background: 'rgba(0,255,65,0.03)' }}
        >
          <p className="text-[8px] tracking-[0.5em] text-[#00FF41]/30 uppercase mb-2">
            {'// ¿TU NOMBRE ACA ARRIBA?'}
          </p>
          <p className="text-base font-black text-white/80 uppercase tracking-wide mb-4">
            Empezá gratis. Las primeras 10 misiones no cuestan nada.
          </p>
          <div className="flex flex-col sm:flex-row gap-3">
            <Link
              href="/register"
              className="text-[9px] tracking-[0.4em] uppercase border border-[#00FF41]/40 px-6 py-3 text-[#00FF41] hover:bg-[#00FF41]/08 hover:border-[#00FF41]/70 transition-all duration-200 text-center"
            >
              {'[[ CREAR CUENTA DE OPERADOR ]]'}
            </Link>
            <Link
              href="/precios"
              className="text-[9px] tracking-[0.35em] uppercase text-[#00FF41]/35 hover:text-[#00FF41]/65 transition-colors py-3 text-center"
            >
              Ver planes →
            </Link>
          </div>
        </div>

        {/* Footer nav */}
        <div className="mt-10 pt-6 border-t border-[#00FF41]/8 flex items-center justify-between">
          <Link href="/" className="text-[#00FF41]/30 text-[9px] tracking-[0.3em] uppercase hover:text-[#00FF41]/60 transition-colors">
            ← NEXO CENTRAL
          </Link>
          <Link href="/blog" className="text-[#00FF41]/30 text-[9px] tracking-[0.3em] uppercase hover:text-[#00FF41]/60 transition-colors">
            INTEL CODEX →
          </Link>
        </div>
      </div>
    </main>
  )
}
