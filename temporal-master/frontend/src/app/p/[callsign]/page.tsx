'use client'

/**
 * /p/[callsign] — Perfil público del Operador
 *
 * Página sin autenticación. Muestra: nivel, XP, misiones completadas,
 * racha, liga y badges. Comparte vía link.
 */

import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import { motion } from 'framer-motion'

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? ''

interface PublicProfile {
  callsign: string
  current_level: number
  total_xp: number
  streak_days: number
  league_tier: string
  current_rank: string
  completed_challenges: number
  badges: string[]
}

// ─── Helpers ─────────────────────────────────────────────────────────────────

function XpBar({ level, xp }: { level: number; xp: number }) {
  const xpPerLevel = 500
  const progress = Math.min((xp % xpPerLevel) / xpPerLevel * 100, 100)
  return (
    <div className="w-full">
      <div className="flex justify-between text-[8px] tracking-widest mb-1"
        style={{ color: 'rgba(0,255,65,0.35)' }}>
        <span>NIVEL {level}</span>
        <span>{xp.toLocaleString()} XP</span>
      </div>
      <div className="h-1 w-full" style={{ background: 'rgba(0,255,65,0.08)' }}>
        <motion.div
          className="h-full"
          style={{ background: 'linear-gradient(90deg, rgba(0,255,65,0.7), rgba(0,180,255,0.7))' }}
          initial={{ width: 0 }}
          animate={{ width: `${progress}%` }}
          transition={{ duration: 1, ease: 'easeOut', delay: 0.3 }}
        />
      </div>
    </div>
  )
}

function StatBlock({ label, value, color = '#00FF41' }: { label: string; value: string | number; color?: string }) {
  return (
    <div className="flex flex-col items-center gap-1 px-4 py-3 border"
      style={{ borderColor: `${color}18`, background: `${color}05` }}>
      <span className="font-black text-xl tracking-widest" style={{ color, textShadow: `0 0 16px ${color}60` }}>
        {value}
      </span>
      <span className="text-[7px] tracking-[0.45em]" style={{ color: `${color}50` }}>
        {label}
      </span>
    </div>
  )
}

// ─── Main ─────────────────────────────────────────────────────────────────────

export default function PublicProfilePage() {
  const params = useParams()
  const callsign = params?.callsign as string

  const [profile, setProfile] = useState<PublicProfile | null>(null)
  const [loading, setLoading] = useState(true)
  const [notFound, setNotFound] = useState(false)
  const [copied, setCopied] = useState(false)

  useEffect(() => {
    if (!callsign) return
    fetch(`${API_BASE}/api/v1/users/profile/${encodeURIComponent(callsign)}`)
      .then(r => {
        if (r.status === 404) { setNotFound(true); return null }
        return r.ok ? r.json() : null
      })
      .then((d: PublicProfile | null) => {
        if (d) setProfile(d)
      })
      .catch(() => setNotFound(true))
      .finally(() => setLoading(false))
  }, [callsign])

  const handleCopy = () => {
    navigator.clipboard.writeText(window.location.href).then(() => {
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    })
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-[#030308] flex items-center justify-center font-mono">
        <motion.p
          className="text-[#00FF41]/30 text-xs tracking-[0.5em]"
          animate={{ opacity: [0.3, 1, 0.3] }}
          transition={{ duration: 1.5, repeat: Infinity }}
        >
          LOCALIZANDO OPERADOR...
        </motion.p>
      </div>
    )
  }

  if (notFound || !profile) {
    return (
      <div className="min-h-screen bg-[#030308] flex flex-col items-center justify-center font-mono gap-4">
        <p className="text-[#FF5050]/60 text-xs tracking-[0.4em]">OPERADOR NO ENCONTRADO</p>
        <p className="text-[#00FF41]/20 text-[10px] tracking-widest">{callsign}</p>
        <a href="/hub" className="text-[9px] tracking-[0.35em] text-[#00FF41]/30 hover:text-[#00FF41]/60 transition-colors">
          [ VOLVER AL NEXO ]
        </a>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-[#030308] flex items-start justify-center p-6 font-mono"
      style={{
        backgroundImage: 'radial-gradient(ellipse at 50% 0%, rgba(0,255,65,0.04) 0%, transparent 70%)',
      }}>

      {/* Scanlines */}
      <div className="fixed inset-0 pointer-events-none"
        style={{ backgroundImage: 'repeating-linear-gradient(0deg,transparent,transparent 3px,rgba(0,255,65,0.012) 3px,rgba(0,255,65,0.012) 4px)' }}
      />

      <motion.div
        className="relative z-10 w-full max-w-sm mt-12"
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
      >
        {/* ── Header ── */}
        <div className="border border-[#00FF41]/15 bg-[#060D06] overflow-hidden mb-3">
          <div className="h-px w-full"
            style={{ background: 'linear-gradient(90deg, transparent, rgba(0,255,65,0.5), transparent)' }}
          />

          <div className="px-6 pt-6 pb-5">
            {/* Badge */}
            <div className="flex items-center gap-2 mb-4">
              <motion.span
                className="text-[9px] tracking-[0.45em] border px-2 py-0.5"
                style={{ color: 'rgba(0,255,65,0.5)', borderColor: 'rgba(0,255,65,0.2)' }}
                animate={{ opacity: [0.5, 1, 0.5] }}
                transition={{ duration: 2.2, repeat: Infinity }}
              >
                PERFIL OPERACIONAL
              </motion.span>
              <span className="text-[8px] tracking-widest px-1.5 py-0.5 border"
                style={{ color: 'rgba(255,184,0,0.55)', borderColor: 'rgba(255,184,0,0.2)', background: 'rgba(255,184,0,0.04)' }}>
                {profile.league_tier.toUpperCase()}
              </span>
            </div>

            {/* Callsign */}
            <motion.h1
              className="text-3xl font-black tracking-widest uppercase mb-1 truncate"
              style={{ color: '#00FF41', textShadow: '0 0 24px rgba(0,255,65,0.5)' }}
              animate={{ textShadow: ['0 0 24px rgba(0,255,65,0.4)', '0 0 40px rgba(0,255,65,0.7)', '0 0 24px rgba(0,255,65,0.4)'] }}
              transition={{ duration: 3, repeat: Infinity }}
            >
              {profile.callsign}
            </motion.h1>
            <p className="text-[10px] tracking-[0.3em] mb-4"
              style={{ color: 'rgba(255,184,0,0.6)' }}>
              {profile.current_rank.toUpperCase()}
            </p>

            {/* XP bar */}
            <XpBar level={profile.current_level} xp={profile.total_xp} />
          </div>
        </div>

        {/* ── Stats grid ── */}
        <div className="grid grid-cols-3 gap-2 mb-3">
          <StatBlock label="NIVEL" value={profile.current_level} color="#00FF41" />
          <StatBlock label="MISIONES" value={profile.completed_challenges} color="#00B4D8" />
          <StatBlock label="RACHA" value={`${profile.streak_days}d`} color="#FFB800" />
        </div>

        {/* ── Badges ── */}
        {profile.badges.length > 0 && (
          <div className="border border-[#00FF41]/10 bg-[#060D06] px-5 py-4 mb-3">
            <p className="text-[7px] tracking-[0.5em] mb-3" style={{ color: 'rgba(0,255,65,0.3)' }}>
              DISTINCIONES DESBLOQUEADAS
            </p>
            <div className="flex flex-wrap gap-1.5">
              {profile.badges.slice(0, 12).map((badge, i) => (
                <span key={i}
                  className="text-[9px] tracking-widest px-2 py-0.5 border"
                  style={{ color: 'rgba(255,215,0,0.6)', borderColor: 'rgba(255,215,0,0.2)', background: 'rgba(255,215,0,0.04)' }}
                >
                  {typeof badge === 'string' ? badge.toUpperCase().replace(/_/g, ' ') : '★'}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* ── Share + CTA ── */}
        <div className="flex gap-2">
          <button
            onClick={handleCopy}
            className="flex-1 py-3 border text-[9px] tracking-[0.35em] uppercase transition-all"
            style={{
              borderColor: copied ? 'rgba(0,255,65,0.5)' : 'rgba(0,255,65,0.2)',
              color: copied ? 'rgba(0,255,65,0.9)' : 'rgba(0,255,65,0.4)',
              background: copied ? 'rgba(0,255,65,0.06)' : 'transparent',
            }}
          >
            {copied ? '[ LINK COPIADO ✓ ]' : '[ COMPARTIR PERFIL ]'}
          </button>
          <a href="/register"
            className="flex-1 py-3 border text-[9px] tracking-[0.35em] uppercase text-center transition-all"
            style={{ borderColor: 'rgba(255,184,0,0.25)', color: 'rgba(255,184,0,0.55)', background: 'rgba(255,184,0,0.04)' }}
          >
            UNIRSE AL NEXO
          </a>
        </div>

        {/* Footer */}
        <p className="text-center text-[7px] tracking-[0.4em] mt-5"
          style={{ color: 'rgba(0,255,65,0.15)' }}>
          NEXO EDTECH · OPERADORES PYTHON · DAKI v1
        </p>
      </motion.div>
    </div>
  )
}
