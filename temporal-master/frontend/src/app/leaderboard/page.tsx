'use client'

import { useEffect, useState, useMemo } from 'react'
import { useRouter } from 'next/navigation'
import { motion } from 'framer-motion'
import { useUserStore } from '@/store/userStore'

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000'

// ─── Tipos ────────────────────────────────────────────────────────────────────

interface LeaderboardEntry {
  rank: number
  user_id: string
  username: string
  total_xp: number
  current_level: number
  streak_days: number
  league_tier: string
  completed_challenges: number
}

interface UserRankInfo {
  rank: number
  total_xp: number
  league_tier: string
  xp_to_next: number | null
  next_username: string | null
}

interface LeaderboardData {
  top50: LeaderboardEntry[]
  user_rank: UserRankInfo | null
  total_players: number
}

// ─── Liga metadata ────────────────────────────────────────────────────────────

const LEAGUE_META: Record<string, { color: string; glow: string; icon: string }> = {
  'Bronce':             { color: '#CD7F32', glow: '#CD7F3260', icon: '◆' },
  'Plata':              { color: '#C0C0C0', glow: '#C0C0C060', icon: '◆' },
  'Oro':                { color: '#FFD700', glow: '#FFD70060', icon: '◆' },
  'Diamante':           { color: '#7DF9FF', glow: '#7DF9FF60', icon: '◈' },
  'Arquitecto Supremo': { color: '#FF6B9D', glow: '#FF6B9D60', icon: '✦' },
}

function getTitleForLevel(level: number): string {
  if (level <= 2) return 'ESTUDIANTE'
  if (level <= 4) return 'CÓDIGO JOVEN'
  if (level <= 7) return 'ARQUITECTO'
  if (level <= 11) return 'MAESTRO'
  return 'LEYENDA ENIGMA'
}

// ─── Avatar de usuario (letras iniciales) ─────────────────────────────────────

function Avatar({
  username,
  size = 'md',
  leagueTier = 'Bronce',
}: {
  username: string
  size?: 'sm' | 'md' | 'lg'
  leagueTier?: string
}) {
  const initials = username.slice(0, 2).toUpperCase()
  const meta = LEAGUE_META[leagueTier] ?? LEAGUE_META['Bronce']
  const sizes = { sm: 'w-7 h-7 text-[10px]', md: 'w-9 h-9 text-xs', lg: 'w-14 h-14 text-base' }

  return (
    <div
      className={`${sizes[size]} rounded-none flex items-center justify-center font-black font-mono shrink-0`}
      style={{
        backgroundColor: `${meta.color}18`,
        border: `1px solid ${meta.color}60`,
        color: meta.color,
        boxShadow: `0 0 10px ${meta.glow}`,
      }}
    >
      {initials}
    </div>
  )
}

// ─── Badge de liga ────────────────────────────────────────────────────────────

function LeagueBadge({ tier }: { tier: string }) {
  const meta = LEAGUE_META[tier] ?? LEAGUE_META['Bronce']
  return (
    <span
      className="text-[9px] font-bold tracking-widest px-1.5 py-0.5 font-mono whitespace-nowrap"
      style={{
        color: meta.color,
        border: `1px solid ${meta.color}50`,
        backgroundColor: `${meta.color}12`,
      }}
    >
      {meta.icon} {tier.toUpperCase()}
    </span>
  )
}

// ─── Tarjeta del podio (top 3) ────────────────────────────────────────────────

const MEDAL_CONFIGS = [
  { label: '2°', color: '#C0C0C0', glow: '#C0C0C080', delay: 0.15, scale: 0.9 },
  { label: '1°', color: '#FFD700', glow: '#FFD70099', delay: 0,    scale: 1 },
  { label: '3°', color: '#CD7F32', glow: '#CD7F3280', delay: 0.25, scale: 0.85 },
]

function PodiumCard({
  entry,
  medalIdx,
}: {
  entry: LeaderboardEntry
  medalIdx: number // 0=2nd, 1=1st, 2=3rd
}) {
  const cfg = MEDAL_CONFIGS[medalIdx]
  const isFirst = medalIdx === 1

  return (
    <motion.div
      className="flex flex-col items-center gap-2 relative"
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: cfg.delay, type: 'spring', stiffness: 200, damping: 22 }}
      style={{ transform: `scale(${cfg.scale})` }}
    >
      {/* Medalla holográfica */}
      <motion.div
        className="relative"
        animate={
          isFirst
            ? {
                filter: [
                  `drop-shadow(0 0 8px ${cfg.glow})`,
                  `drop-shadow(0 0 20px ${cfg.glow})`,
                  `drop-shadow(0 0 8px ${cfg.glow})`,
                ],
              }
            : {}
        }
        transition={{ duration: 1.8, repeat: Infinity }}
      >
        {/* Anillo holográfico animado para el 1er puesto */}
        {isFirst && (
          <motion.div
            className="absolute -inset-2 rounded-none"
            style={{ border: `1px solid ${cfg.color}` }}
            animate={{ opacity: [0.2, 0.8, 0.2], scale: [1, 1.04, 1] }}
            transition={{ duration: 2, repeat: Infinity }}
          />
        )}
        <Avatar username={entry.username} size="lg" leagueTier={entry.league_tier} />
      </motion.div>

      {/* Número de medalla */}
      <div
        className="text-2xl font-black font-mono"
        style={{ color: cfg.color, textShadow: `0 0 12px ${cfg.glow}` }}
      >
        {cfg.label}
      </div>

      {/* Info */}
      <div className="text-center">
        <div
          className="font-mono font-bold text-sm tracking-widest"
          style={{ color: cfg.color }}
        >
          {entry.username}
        </div>
        <div className="text-[10px] text-[#00FF41]/40 tracking-widest mt-0.5">
          {getTitleForLevel(entry.current_level)}
        </div>
        <div
          className="font-mono font-black text-base mt-1"
          style={{ color: cfg.color, textShadow: `0 0 8px ${cfg.glow}` }}
        >
          {entry.total_xp.toLocaleString()} XP
        </div>
        <LeagueBadge tier={entry.league_tier} />
      </div>

      {/* Columna del podio */}
      <div
        className="w-full"
        style={{
          height: isFirst ? '48px' : medalIdx === 0 ? '32px' : '20px',
          backgroundColor: `${cfg.color}20`,
          borderTop: `2px solid ${cfg.color}60`,
        }}
      />
    </motion.div>
  )
}

// ─── Fila de la tabla ─────────────────────────────────────────────────────────

function TableRow({
  entry,
  isCurrentUser,
  delay,
}: {
  entry: LeaderboardEntry
  isCurrentUser: boolean
  delay: number
}) {
  const meta = LEAGUE_META[entry.league_tier] ?? LEAGUE_META['Bronce']

  return (
    <motion.tr
      initial={{ opacity: 0, x: -12 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay, duration: 0.2 }}
      className={`border-b font-mono text-xs transition-colors ${
        isCurrentUser
          ? 'border-[#00FF41]/40 bg-[#00FF41]/5'
          : 'border-[#00FF41]/8 hover:bg-[#00FF41]/3'
      }`}
    >
      {/* Rank */}
      <td className="py-2.5 pl-4 pr-3 text-[#00FF41]/30 w-10 font-bold">
        {String(entry.rank).padStart(2, '0')}
      </td>

      {/* Avatar + username */}
      <td className="py-2.5 pr-4">
        <div className="flex items-center gap-2.5">
          <Avatar username={entry.username} size="sm" leagueTier={entry.league_tier} />
          <div>
            <div
              className={`font-bold tracking-widest ${
                isCurrentUser ? 'text-[#00FF41]' : 'text-[#00FF41]/85'
              }`}
              style={isCurrentUser ? { textShadow: '0 0 6px #00FF4180' } : {}}
            >
              {entry.username}
              {isCurrentUser && (
                <span className="ml-2 text-[9px] text-[#00FF41]/50 tracking-widest">← TÚ</span>
              )}
            </div>
            <div className="text-[9px] text-[#00FF41]/30 tracking-widest mt-0.5">
              {getTitleForLevel(entry.current_level)} · RANGO {entry.current_level}
            </div>
          </div>
        </div>
      </td>

      {/* Liga */}
      <td className="py-2.5 pr-4 hidden sm:table-cell">
        <LeagueBadge tier={entry.league_tier} />
      </td>

      {/* XP */}
      <td className="py-2.5 pr-4 text-right">
        <span
          className="font-black tracking-wider"
          style={{ color: meta.color, textShadow: `0 0 6px ${meta.glow}` }}
        >
          {entry.total_xp.toLocaleString()}
        </span>
        <span className="text-[#00FF41]/25 ml-1">XP</span>
      </td>

      {/* Racha */}
      <td className="py-2.5 pr-4 hidden md:table-cell">
        {entry.streak_days > 0 ? (
          <span className="flex items-center gap-1">
            <motion.span
              className="text-[#00FF41] font-bold"
              animate={{ opacity: [0.6, 1, 0.6] }}
              transition={{ duration: 1.5, repeat: Infinity }}
            >
              ▲
            </motion.span>
            <span className="text-[#00FF41]/70">{entry.streak_days}d</span>
          </span>
        ) : (
          <span className="text-[#00FF41]/20">—</span>
        )}
      </td>

      {/* Retos */}
      <td className="py-2.5 pr-4 text-center hidden lg:table-cell text-[#00FF41]/45">
        {entry.completed_challenges}
      </td>
    </motion.tr>
  )
}

// ─── Página principal ─────────────────────────────────────────────────────────

export default function LeaderboardPage() {
  const router = useRouter()
  const { userId, username, level, totalXp } = useUserStore()

  const [data, setData] = useState<LeaderboardData | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!userId) {
      router.replace('/')
      return
    }
    fetch(`${API_BASE}/api/v1/leaderboard?user_id=${userId}`)
      .then((r) => r.json())
      .then((d: LeaderboardData) => setData(d))
      .finally(() => setLoading(false))
  }, [userId, router])

  // Top 3 en orden de podio: [2nd, 1st, 3rd]
  const podiumOrder = useMemo(() => {
    if (!data || data.top50.length < 3) return null
    return [data.top50[1], data.top50[0], data.top50[2]]
  }, [data])

  const tableRows = useMemo(
    () => (data ? data.top50.slice(3) : []),
    [data]
  )

  const isInTop50 = data?.top50.some((e) => e.user_id === userId)

  return (
    <div className="min-h-screen bg-[#050A05] font-mono text-[#00FF41] relative">
      {/* Scanlines */}
      <div
        className="fixed inset-0 pointer-events-none z-0 opacity-[0.025]"
        style={{
          backgroundImage:
            'repeating-linear-gradient(0deg,transparent,transparent 3px,#00FF41 3px,#00FF41 4px)',
        }}
      />

      {/* Header */}
      <header className="relative z-10 flex items-center justify-between px-6 py-3 bg-[#030803] border-b border-[#00FF41]/15">
        <div className="flex items-center gap-4">
          <button
            onClick={() => router.push('/misiones')}
            className="text-[#00FF41]/35 hover:text-[#00FF41]/70 text-xs tracking-widest transition-colors"
          >
            ← MISIONES
          </button>
          <span className="text-[#00FF41]/15">|</span>
          <span
            className="font-black tracking-[0.2em] text-sm"
            style={{ textShadow: '0 0 10px #00FF4150' }}
          >
            CLASIFICACIÓN GLOBAL
          </span>
        </div>
        <div className="flex items-center gap-5 text-xs text-[#00FF41]/50">
          <span>{username}</span>
          <span>RANGO <strong className="text-[#00FF41]">{level}</strong></span>
          <span>XP <strong className="text-[#00FF41]">{totalXp.toLocaleString()}</strong></span>
        </div>
      </header>

      <main className="relative z-10 max-w-3xl mx-auto px-6 py-10">

        {loading ? (
          <div className="flex flex-col items-center gap-3 py-20">
            <motion.div
              className="text-[#00FF41]/40 text-xs tracking-[0.4em]"
              animate={{ opacity: [0.3, 1, 0.3] }}
              transition={{ duration: 1.5, repeat: Infinity }}
            >
              CARGANDO CLASIFICACIÓN...
            </motion.div>
          </div>
        ) : data ? (
          <>
            {/* Conteo total */}
            <div className="mb-8 flex items-center justify-between">
              <div>
                <h1 className="text-2xl font-black tracking-[0.15em] mb-1">TABLA DE ÉLITE</h1>
                <p className="text-[#00FF41]/30 text-xs tracking-widest">
                  {data.total_players.toLocaleString()} ARQUITECTOS REGISTRADOS
                </p>
              </div>
              {/* Leyenda de ligas */}
              <div className="hidden sm:flex items-center gap-2 flex-wrap justify-end">
                {Object.entries(LEAGUE_META).map(([tier, meta]) => (
                  <span
                    key={tier}
                    className="text-[9px] tracking-widest font-bold px-1.5 py-0.5"
                    style={{ color: meta.color, border: `1px solid ${meta.color}30` }}
                  >
                    {meta.icon} {tier.toUpperCase()}
                  </span>
                ))}
              </div>
            </div>

            {/* ── Podio Top 3 ─────────────────────────────────────────────── */}
            {podiumOrder && (
              <div className="mb-10">
                <div className="text-[10px] tracking-[0.35em] text-[#00FF41]/25 mb-4 text-center">
                  ── PODIO DE HONOR ──
                </div>
                <div className="flex items-end justify-center gap-4 sm:gap-8">
                  {podiumOrder.map((entry, i) => (
                    <div key={entry.user_id} className="flex-1 max-w-[140px]">
                      <PodiumCard entry={entry} medalIdx={i} />
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* ── Tabla Top 4–50 ──────────────────────────────────────────── */}
            {tableRows.length > 0 && (
              <div className="border border-[#00FF41]/15 bg-[#030803]">
                {/* Scanner line */}
                <div className="h-px w-full overflow-hidden relative">
                  <motion.div
                    className="absolute h-px bg-[#00FF41]/60"
                    style={{ width: '30%' }}
                    animate={{ x: ['-30%', '130%'] }}
                    transition={{ duration: 3, repeat: Infinity, ease: 'linear' }}
                  />
                </div>

                <table className="w-full">
                  <thead>
                    <tr className="border-b border-[#00FF41]/10 text-[9px] tracking-[0.25em] text-[#00FF41]/30 uppercase">
                      <th className="py-2 pl-4 pr-3 text-left w-10">#</th>
                      <th className="py-2 pr-4 text-left">Agente</th>
                      <th className="py-2 pr-4 text-left hidden sm:table-cell">Liga</th>
                      <th className="py-2 pr-4 text-right">XP Total</th>
                      <th className="py-2 pr-4 text-left hidden md:table-cell">Racha</th>
                      <th className="py-2 pr-4 text-center hidden lg:table-cell">Retos</th>
                    </tr>
                  </thead>
                  <tbody>
                    {tableRows.map((entry, i) => (
                      <TableRow
                        key={entry.user_id}
                        entry={entry}
                        isCurrentUser={entry.user_id === userId}
                        delay={i * 0.03}
                      />
                    ))}
                  </tbody>
                </table>
              </div>
            )}

            {/* ── Tu posición (si no estás en el top 50) ──────────────────── */}
            {data.user_rank && !isInTop50 && (
              <motion.div
                className="mt-6 border border-[#00FF41]/30 bg-[#00FF41]/5 px-5 py-4"
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 }}
              >
                <div className="flex items-center justify-between gap-4 flex-wrap">
                  <div className="flex items-center gap-3">
                    <Avatar username={username} size="md" leagueTier={data.user_rank.league_tier} />
                    <div>
                      <div
                        className="font-bold text-sm tracking-widest text-[#00FF41]"
                        style={{ textShadow: '0 0 6px #00FF4180' }}
                      >
                        TU POSICIÓN ACTUAL
                      </div>
                      <div className="text-[10px] text-[#00FF41]/40 tracking-widest mt-0.5">
                        {getTitleForLevel(level)} · RANGO {level}
                      </div>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-3xl font-black tracking-widest text-[#00FF41]">
                      #{data.user_rank.rank.toLocaleString()}
                    </div>
                    <div className="text-xs text-[#00FF41]/40 mt-0.5">
                      de {data.total_players.toLocaleString()} jugadores
                    </div>
                  </div>
                </div>

                {/* XP para superar al siguiente */}
                {data.user_rank.xp_to_next != null && (
                  <div className="mt-3 pt-3 border-t border-[#00FF41]/15">
                    <div className="flex items-center justify-between text-xs">
                      <span className="text-[#00FF41]/40 tracking-widest">
                        A{' '}
                        <strong className="text-[#FFD700]">
                          {data.user_rank.xp_to_next.toLocaleString()} XP
                        </strong>{' '}
                        de superar a{' '}
                        <strong className="text-[#00FF41]/70">
                          {data.user_rank.next_username}
                        </strong>
                      </span>
                      <LeagueBadge tier={data.user_rank.league_tier} />
                    </div>
                    {/* Mini barra de progreso hacia el siguiente */}
                    <div className="mt-2 h-px bg-[#00FF41]/10 overflow-hidden">
                      <motion.div
                        className="h-full bg-[#00FF41]/50"
                        initial={{ width: 0 }}
                        animate={{
                          width: `${Math.min(
                            90,
                            100 - ((data.user_rank.xp_to_next ?? 1) / 200) * 100
                          )}%`,
                        }}
                        transition={{ duration: 1, ease: 'easeOut', delay: 0.6 }}
                      />
                    </div>
                  </div>
                )}
              </motion.div>
            )}
          </>
        ) : (
          <p className="text-[#00FF41]/30 text-xs tracking-widest">Sin datos disponibles.</p>
        )}
      </main>
    </div>
  )
}
