'use client'

import { useEffect, useState, useCallback } from 'react'
import { useRouter } from 'next/navigation'
import { motion, AnimatePresence } from 'framer-motion'
import { useUserStore } from '@/store/userStore'
import MobileGate from '@/components/UI/MobileGate'

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? ''

// ─── Tipos ────────────────────────────────────────────────────────────────────

interface Contract {
  id: string
  level_order: number
  title: string
  description: string
  difficulty: string
  base_xp_reward: number
  telemetry_goal_time: number | null
  concepts_taught: string[]
  lore_briefing: string | null
  pedagogical_objective: string | null
  completed: boolean
  unlocked: boolean
  criteria_count: number
}

// ─── Ciclo de rotación — cada 14 días desde epoch fijo ───────────────────────

const ROTATION_DAYS = 14
// Epoch: primer lunes de 2025 como base de ciclos
const EPOCH = new Date('2025-01-06T00:00:00Z')

function getRotationInfo() {
  const now = Date.now()
  const msPerCycle = ROTATION_DAYS * 24 * 60 * 60 * 1000
  const elapsed = now - EPOCH.getTime()
  const cycleNumber = Math.floor(elapsed / msPerCycle) + 1
  const nextRotationMs = EPOCH.getTime() + cycleNumber * msPerCycle
  const msLeft = nextRotationMs - now
  return { cycleNumber, msLeft, nextRotationMs }
}

function formatCountdown(ms: number) {
  if (ms <= 0) return { d: '00', h: '00', m: '00', s: '00' }
  const s = Math.floor(ms / 1000)
  return {
    d: String(Math.floor(s / 86400)).padStart(2, '0'),
    h: String(Math.floor((s % 86400) / 3600)).padStart(2, '0'),
    m: String(Math.floor((s % 3600) / 60)).padStart(2, '0'),
    s: String(s % 60).padStart(2, '0'),
  }
}

// ─── Config visual por contrato ───────────────────────────────────────────────

const CFG: Record<number, { glyph: string; color: string; rank: string }> = {
  50: { glyph: '⬡', color: '#00FF41', rank: 'ALFA' },
  60: { glyph: '◈', color: '#FFB800', rank: 'BETA' },
  70: { glyph: '⬟', color: '#FF6B35', rank: 'GAMMA' },
}
const CFG_DEFAULT = { glyph: '◆', color: '#00CFFF', rank: 'DELTA' }

// ─── Countdown pill ───────────────────────────────────────────────────────────

function CountdownPill({ msLeft }: { msLeft: number }) {
  const [ms, setMs] = useState(msLeft)
  useEffect(() => {
    const id = setInterval(() => setMs(v => Math.max(0, v - 1000)), 1000)
    return () => clearInterval(id)
  }, [])
  const t = formatCountdown(ms)
  return (
    <div className="flex items-center gap-1 font-mono text-[10px] tracking-[0.2em]"
      style={{ color: 'rgba(0,255,65,0.5)' }}>
      <span style={{ color: 'rgba(0,255,65,0.25)' }}>ROTA EN</span>
      {([t.d, t.h, t.m, t.s] as string[]).map((v, i) => (
        <span key={i} className="flex items-center gap-1">
          <span className="px-1.5 py-0.5 border font-black"
            style={{ borderColor: 'rgba(0,255,65,0.2)', color: '#00FF41', background: 'rgba(0,255,65,0.05)' }}>
            {v}
          </span>
          {i < 3 && <span style={{ color: 'rgba(0,255,65,0.2)' }}>:</span>}
        </span>
      ))}
      <span style={{ color: 'rgba(0,255,65,0.25)' }} className="ml-1">
        {['D', 'H', 'M', 'S'][0]}
      </span>
    </div>
  )
}

// ─── Tarjeta de contrato ──────────────────────────────────────────────────────

function ContractCard({
  contract, idx, onOpen,
}: {
  contract: Contract; idx: number; onOpen: () => void
}) {
  const cfg  = CFG[contract.level_order] ?? CFG_DEFAULT
  const reqLvl = Math.max(0, contract.level_order - 10)

  const status = contract.completed ? 'done'
    : contract.unlocked ? 'open'
    : 'locked'

  const statusLabel = {
    done:   'VALIDADO ✓',
    open:   'ACTIVO',
    locked: `CLASIFICADO — NIV ${reqLvl}`,
  }[status]

  const statusColor = {
    done:   cfg.color,
    open:   cfg.color,
    locked: 'rgba(255,255,255,0.18)',
  }[status]

  const title = contract.title.replace(`CONTRATO-${contract.level_order}: `, '')

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: idx * 0.08, duration: 0.3 }}
      onClick={() => status !== 'locked' && onOpen()}
      className={`relative overflow-hidden ${status !== 'locked' ? 'cursor-pointer group' : 'cursor-not-allowed'}`}
      style={{
        border:     `1px solid ${status !== 'locked' ? cfg.color + '28' : 'rgba(255,255,255,0.06)'}`,
        background: status === 'done'
          ? `linear-gradient(135deg, ${cfg.color}07 0%, rgba(0,0,0,0.6) 100%)`
          : 'rgba(0,0,0,0.5)',
        opacity:    status === 'locked' ? 0.45 : 1,
      }}
      whileHover={status !== 'locked' ? {
        borderColor: cfg.color + '55',
        boxShadow:   `0 0 30px ${cfg.color}10`,
      } : {}}
    >
      {/* Acento superior */}
      <div className="absolute top-0 left-0 right-0 h-px transition-all duration-300"
        style={{ background: `linear-gradient(90deg, transparent, ${cfg.color}${status !== 'locked' ? '60' : '20'}, transparent)` }}
      />

      {/* Franja lateral */}
      <div className="absolute left-0 top-0 bottom-0 w-0.5"
        style={{ background: status === 'done' ? cfg.color : status === 'open' ? `${cfg.color}50` : 'rgba(255,255,255,0.08)' }}
      />

      <div className="pl-5 pr-5 py-5">

        {/* Fila superior: ID + status */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-center gap-3">
            {/* Glyph */}
            <motion.span
              className="text-3xl leading-none shrink-0 select-none"
              style={{
                color:      status !== 'locked' ? cfg.color : 'rgba(255,255,255,0.15)',
                textShadow: status !== 'locked' ? `0 0 18px ${cfg.color}60` : 'none',
              }}
              animate={status === 'open' ? { opacity: [0.7, 1, 0.7] } : {}}
              transition={{ duration: 2.5, repeat: Infinity, ease: 'easeInOut' }}
            >
              {cfg.glyph}
            </motion.span>

            <div>
              <div className="text-[8px] tracking-[0.5em] mb-0.5 font-bold"
                style={{ color: `${status !== 'locked' ? cfg.color : 'rgba(255,255,255,0.2)'}60` }}>
                CONTRATO-{contract.level_order} · RANGO {cfg.rank}
              </div>
              <div className="font-black tracking-[0.08em] text-base leading-tight"
                style={{ color: status !== 'locked' ? 'rgba(255,255,255,0.9)' : 'rgba(255,255,255,0.25)' }}>
                {title}
              </div>
            </div>
          </div>

          {/* Status badge */}
          <div className="shrink-0 flex items-center gap-1.5 ml-4">
            {status === 'open' && (
              <motion.span className="w-1.5 h-1.5 rounded-full"
                style={{ background: cfg.color, boxShadow: `0 0 6px ${cfg.color}` }}
                animate={{ opacity: [0.4, 1, 0.4] }}
                transition={{ duration: 1, repeat: Infinity }}
              />
            )}
            <span className="text-[9px] tracking-[0.3em] font-bold"
              style={{ color: statusColor }}>
              {statusLabel}
            </span>
          </div>
        </div>

        {/* Briefing */}
        <p className="text-[11px] leading-relaxed mb-4 line-clamp-2"
          style={{ color: status !== 'locked' ? 'rgba(255,255,255,0.45)' : 'rgba(255,255,255,0.2)' }}>
          {contract.lore_briefing ?? contract.description}
        </p>

        {/* Métricas */}
        <div className="grid grid-cols-3 gap-2 mb-4">
          {[
            { label: 'XP',        value: contract.base_xp_reward.toLocaleString() },
            { label: 'CRITERIOS', value: String(contract.criteria_count) },
            { label: 'TIEMPO',    value: contract.telemetry_goal_time ? `${Math.round(contract.telemetry_goal_time / 60)}min` : '—' },
          ].map(({ label, value }) => (
            <div key={label} className="text-center py-2 border"
              style={{ borderColor: `${status !== 'locked' ? cfg.color : 'rgba(255,255,255,0.08)'}18` }}>
              <div className="text-[8px] tracking-[0.35em] mb-1"
                style={{ color: `${status !== 'locked' ? cfg.color : 'rgba(255,255,255,0.2)'}55` }}>
                {label}
              </div>
              <div className="text-sm font-black"
                style={{ color: status !== 'locked' ? cfg.color : 'rgba(255,255,255,0.2)' }}>
                {value}
              </div>
            </div>
          ))}
        </div>

        {/* Conceptos */}
        <div className="flex flex-wrap gap-1.5 mb-4">
          {contract.concepts_taught.slice(0, 5).map(c => (
            <span key={c} className="text-[9px] tracking-widest border px-2 py-0.5"
              style={{
                borderColor: `${status !== 'locked' ? cfg.color : 'rgba(255,255,255,0.12)'}22`,
                color:       `${status !== 'locked' ? cfg.color : 'rgba(255,255,255,0.2)'}70`,
              }}>
              {c}
            </span>
          ))}
          {contract.concepts_taught.length > 5 && (
            <span className="text-[9px] tracking-widest px-1"
              style={{ color: 'rgba(255,255,255,0.2)' }}>
              +{contract.concepts_taught.length - 5}
            </span>
          )}
        </div>

        {/* CTA */}
        {status !== 'locked' && (
          <div className="flex items-center justify-end">
            <motion.span
              className="text-[10px] tracking-[0.35em] font-black"
              style={{ color: cfg.color }}
              animate={{ opacity: status === 'open' ? [0.6, 1, 0.6] : 1 }}
              transition={{ duration: 1.8, repeat: Infinity }}
            >
              {status === 'done' ? '[ REVISAR CONTRATO ]' : '[[ INICIAR MISIÓN ]]'} →
            </motion.span>
          </div>
        )}
      </div>
    </motion.div>
  )
}

// ─── Página principal ─────────────────────────────────────────────────────────

export default function ContratosPage() {
  const router = useRouter()
  const { _hasHydrated, userId, username, level } = useUserStore()
  const [contracts, setContracts] = useState<Contract[]>([])
  const [loading, setLoading] = useState(true)
  const { cycleNumber, msLeft } = getRotationInfo()

  useEffect(() => {
    if (!_hasHydrated) return
    if (!userId) { router.replace('/login'); return }
    fetch(`${API_BASE}/api/v1/contracts?user_id=${userId}`)
      .then(r => r.json())
      .then((data: Contract[]) => setContracts(data))
      .catch(() => setContracts([]))
      .finally(() => setLoading(false))
  }, [_hasHydrated, userId, router])

  const completed = contracts.filter(c => c.completed).length
  const total     = contracts.length

  return (
    <MobileGate>
    <div className="min-h-screen bg-[#020202] font-mono text-[#00FF41] relative">

      {/* Scanlines */}
      <div className="fixed inset-0 pointer-events-none z-0 opacity-[0.012]"
        style={{ backgroundImage: 'repeating-linear-gradient(0deg,transparent,transparent 3px,#00FF41 3px,#00FF41 4px)' }}
      />
      {/* Grid */}
      <div className="fixed inset-0 pointer-events-none z-0"
        style={{
          backgroundImage: 'linear-gradient(rgba(0,255,65,0.03) 1px,transparent 1px),linear-gradient(90deg,rgba(0,255,65,0.03) 1px,transparent 1px)',
          backgroundSize:  '72px 72px',
        }}
      />

      {/* ── Header ── */}
      <header className="relative z-10 flex items-center justify-between px-6 py-3 border-b border-[#00FF41]/10 bg-[#020202]/90 backdrop-blur-sm">
        <div className="flex items-center gap-4">
          <button onClick={() => router.push('/hub')}
            className="text-[10px] tracking-[0.3em] border border-[#00FF41]/15 px-3 py-1 text-[#00FF41]/40 hover:text-[#00FF41]/70 hover:border-[#00FF41]/35 transition-all duration-150">
            ← HUB
          </button>
          <span className="text-[#00FF41]/15">|</span>
          <span className="font-black tracking-[0.25em] text-sm"
            style={{ textShadow: '0 0 12px rgba(0,255,65,0.4)' }}>
            SALA DE CONTRATOS
          </span>
        </div>
        <div className="flex items-center gap-5 text-[10px] text-[#00FF41]/40 tracking-widest">
          <span>{username}</span>
          <span>RNG <strong className="text-[#00FF41]">{level}</strong></span>
        </div>
      </header>

      <main className="relative z-10 max-w-3xl mx-auto px-6 py-10">

        {/* ── Hero ── */}
        <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}
          className="mb-8">

          <p className="text-[9px] tracking-[0.55em] text-[#00FF41]/25 mb-2">
            {'// SISTEMA — CERTIFICACIÓN OPERACIONAL'}
          </p>
          <h1 className="text-3xl font-black tracking-[0.12em] text-white/90 leading-tight mb-1">
            CONTRATOS
            <span className="text-[#00FF41]" style={{ textShadow: '0 0 28px rgba(0,255,65,0.5)' }}>
              {' '}ACTIVOS
            </span>
          </h1>
          <p className="text-[11px] text-white/30 leading-relaxed max-w-lg">
            Proyectos reales evaluados por DAKI contra criterios de aceptación técnicos.
            Completa uno para publicar en GitHub y recibir tu certificado de mando.
          </p>
        </motion.div>

        {/* ── Ciclo operacional ── */}
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}
          transition={{ delay: 0.15 }}
          className="mb-8 border border-[#00FF41]/12 p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4"
          style={{ background: 'rgba(0,255,65,0.03)' }}>

          <div className="flex items-center gap-4">
            {/* Ciclo badge */}
            <div className="text-center px-4 py-2 border border-[#00FF41]/20"
              style={{ background: 'rgba(0,255,65,0.05)' }}>
              <div className="text-[7px] tracking-[0.5em] text-[#00FF41]/35 mb-0.5">CICLO</div>
              <div className="text-xl font-black text-[#00FF41]"
                style={{ textShadow: '0 0 12px rgba(0,255,65,0.6)' }}>
                #{String(cycleNumber).padStart(3, '0')}
              </div>
            </div>

            <div>
              <div className="text-[9px] tracking-[0.4em] text-[#00FF41]/45 font-bold mb-1">
                CICLO OPERACIONAL ACTIVO
              </div>
              <div className="text-[10px] text-white/25 leading-relaxed">
                Contratos rotan cada {ROTATION_DAYS} días.<br />
                Completa el contrato antes de la próxima rotación.
              </div>
            </div>
          </div>

          <div className="flex flex-col items-end gap-1">
            <div className="text-[8px] tracking-[0.4em] text-[#00FF41]/25 mb-1">PRÓXIMA ROTACIÓN</div>
            <CountdownPill msLeft={msLeft} />
          </div>
        </motion.div>

        {/* ── Progreso ── */}
        <div className="flex items-center gap-4 mb-8">
          <div className="flex-1 h-px bg-[#00FF41]/08 relative overflow-hidden">
            <motion.div className="absolute left-0 top-0 h-full bg-[#00FF41]"
              initial={{ width: 0 }}
              animate={{ width: total ? `${(completed / total) * 100}%` : '0%' }}
              transition={{ duration: 1, ease: 'easeOut' }}
              style={{ boxShadow: '0 0 8px rgba(0,255,65,0.6)' }}
            />
          </div>
          <span className="text-[10px] text-[#00FF41]/25 tracking-widest shrink-0">
            {completed}/{total} VALIDADOS
          </span>
        </div>

        {/* ── Certificado ── */}
        <AnimatePresence>
          {completed === total && total > 0 && (
            <motion.div
              initial={{ opacity: 0, y: -8 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              className="mb-8 border border-[#00FF41]/40 p-4 flex items-center gap-4"
              style={{ background: 'rgba(0,255,65,0.05)', boxShadow: '0 0 30px rgba(0,255,65,0.08)' }}>
              <span className="text-2xl" style={{ color: '#00FF41', textShadow: '0 0 14px rgba(0,255,65,0.8)' }}>✓</span>
              <div className="flex-1">
                <div className="text-[11px] font-black tracking-[0.2em] text-[#00FF41]">
                  CERTIFICADO DE MANDO DESBLOQUEADO
                </div>
                <div className="text-[10px] text-[#00FF41]/45 tracking-widest mt-0.5">
                  Todos los contratos del ciclo #{String(cycleNumber).padStart(3,'0')} validados
                </div>
              </div>
              <a href={`/api/v1/certificate/download?user_id=${userId}`}
                target="_blank" rel="noopener noreferrer"
                className="text-[10px] tracking-[0.35em] border border-[#00FF41]/40 px-4 py-2 hover:bg-[#00FF41]/10 transition-colors shrink-0"
                style={{ color: '#00FF41' }}>
                [[ DESCARGAR ]]
              </a>
            </motion.div>
          )}
        </AnimatePresence>

        {/* ── Lista ── */}
        {loading ? (
          <div className="flex items-center gap-3 py-12">
            <motion.span
              className="text-lg text-[#00FF41]/40"
              animate={{ opacity: [0.3, 1, 0.3] }}
              transition={{ duration: 1.2, repeat: Infinity }}
            >◈</motion.span>
            <span className="text-[10px] tracking-[0.4em] text-[#00FF41]/30">
              CARGANDO CONTRATOS DEL CICLO...
            </span>
          </div>
        ) : (
          <div className="flex flex-col gap-4">
            {contracts.map((contract, idx) => (
              <ContractCard
                key={contract.id}
                contract={contract}
                idx={idx}
                onOpen={() => router.push(`/contratos/${contract.id}`)}
              />
            ))}
          </div>
        )}

        {/* ── Footer ── */}
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="mt-10 border-t border-[#00FF41]/08 pt-6">
          <p className="text-[9px] text-[#00FF41]/18 tracking-[0.25em] leading-7">
            {'// CONTRATOS EVALUADOS POR DAKI CONTRA CRITERIOS TÉCNICOS ESPECÍFICOS.'}<br />
            {'// AL VALIDAR UN CONTRATO RECIBIRÁS UN TUTORIAL PARA PUBLICARLO EN GITHUB.'}<br />
            {'// TRES CONTRATOS COMPLETADOS = CERTIFICADO DE MANDO DAKI EDTECH.'}
          </p>
        </motion.div>

      </main>
    </div>
    </MobileGate>
  )
}
