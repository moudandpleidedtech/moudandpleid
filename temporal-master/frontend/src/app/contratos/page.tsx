'use client'

/**
 * /contratos — Sala de Contratos DAKI
 * ─────────────────────────────────────
 * Proyectos de certificación evaluados por DAKI.
 * Tres contratos (L50, L60, L70) desbloqueables por nivel.
 */

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { motion } from 'framer-motion'
import { useUserStore } from '@/store/userStore'
import MobileGate from '@/components/UI/MobileGate'

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000'

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

const CONTRACT_ICONS: Record<number, string> = {
  50: '⬡',
  60: '◈',
  70: '⬟',
}

const CONTRACT_COLORS: Record<number, { border: string; glow: string; accent: string }> = {
  50: { border: '#00FF41', glow: 'rgba(0,255,65,0.15)', accent: '#00FF41' },
  60: { border: '#FFB800', glow: 'rgba(255,184,0,0.15)', accent: '#FFB800' },
  70: { border: '#FF4444', glow: 'rgba(255,68,68,0.15)', accent: '#FF4444' },
}

export default function ContratosPage() {
  const router = useRouter()
  const { userId, username, level } = useUserStore()
  const [contracts, setContracts] = useState<Contract[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!userId) { router.replace('/'); return }
    fetch(`${API_BASE}/api/v1/contracts?user_id=${userId}`)
      .then(r => r.json())
      .then((data: Contract[]) => setContracts(data))
      .catch(() => setContracts([]))
      .finally(() => setLoading(false))
  }, [userId, router])

  const completed = contracts.filter(c => c.completed).length
  const total = contracts.length

  return (
    <MobileGate>
    <div className="min-h-screen bg-[#050A05] font-mono text-[#00FF41]">

      {/* Scanlines */}
      <div className="fixed inset-0 pointer-events-none z-0 opacity-[0.025]"
        style={{ backgroundImage: 'repeating-linear-gradient(0deg,transparent,transparent 3px,#00FF41 3px,#00FF41 4px)' }}
      />

      {/* Header */}
      <header className="relative z-10 flex items-center justify-between px-6 py-3 bg-[#030803] border-b border-[#00FF41]/15">
        <div className="flex items-center gap-4">
          <button onClick={() => router.push('/hub')}
            className="text-[#00FF41]/35 hover:text-[#00FF41]/70 text-xs tracking-widest transition-colors">
            ← HUB
          </button>
          <span className="text-[#00FF41]/15">|</span>
          <span className="font-black tracking-[0.2em] text-sm text-[#00FF41]"
            style={{ textShadow: '0 0 10px #00FF4150' }}>
            SALA DE CONTRATOS
          </span>
          <span className="text-[#00FF41]/20 text-xs tracking-widest">{'// CERTIFICACIÓN OPERACIONAL'}</span>
        </div>
        <div className="flex items-center gap-5 text-xs text-[#00FF41]/50">
          <span>{username}</span>
          <span>NIVEL <strong className="text-[#00FF41]">{level}</strong></span>
        </div>
      </header>

      <main className="relative z-10 max-w-3xl mx-auto px-6 py-10">

        {/* Título */}
        <div className="mb-10">
          <h1 className="text-2xl font-black tracking-[0.15em] mb-2">CONTRATOS DE CERTIFICACIÓN</h1>
          <p className="text-[#00FF41]/35 text-xs tracking-widest leading-relaxed max-w-lg">
            Los Contratos son proyectos reales evaluados por DAKI contra criterios de aceptación.
            Completa un contrato para desbloquear el Tutorial GitHub y exportar tu obra al mundo.
          </p>

          {/* Progreso */}
          <div className="mt-5 flex items-center gap-4">
            <div className="flex-1 h-px bg-[#00FF41]/10 relative overflow-hidden">
              <motion.div className="absolute left-0 top-0 h-full bg-[#00FF41]"
                initial={{ width: 0 }}
                animate={{ width: total ? `${(completed / total) * 100}%` : '0%' }}
                transition={{ duration: 0.9, ease: 'easeOut' }}
              />
            </div>
            <span className="text-[10px] text-[#00FF41]/25 tracking-widest shrink-0">
              {completed}/{total} CONTRATOS
            </span>
          </div>

          {/* Badge de certificación cuando todos completados */}
          {completed === total && total > 0 && (
            <motion.div
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              className="mt-4 border border-[#00FF41]/40 bg-[#00FF41]/5 px-4 py-3 inline-flex items-center gap-3"
            >
              <span className="text-[#00FF41] text-sm">✓</span>
              <div>
                <div className="text-[11px] font-bold tracking-[0.2em] text-[#00FF41]">
                  CERTIFICADO DE MANDO DISPONIBLE
                </div>
                <div className="text-[10px] text-[#00FF41]/50 tracking-widest mt-0.5">
                  Has completado todos los contratos de certificación
                </div>
              </div>
              <a
                href={`/api/v1/certificate/download?user_id=${userId}`}
                target="_blank"
                rel="noopener noreferrer"
                className="ml-auto text-[10px] tracking-[0.3em] border border-[#00FF41]/40 px-3 py-1.5 hover:bg-[#00FF41]/10 transition-colors"
              >
                [[ DESCARGAR ]]
              </a>
            </motion.div>
          )}
        </div>

        {/* Grid de contratos */}
        {loading ? (
          <p className="text-[#00FF41]/30 text-xs tracking-widest animate-pulse">CARGANDO CONTRATOS...</p>
        ) : (
          <div className="flex flex-col gap-6">
            {contracts.map((contract, idx) => {
              const colors = CONTRACT_COLORS[contract.level_order] ?? CONTRACT_COLORS[50]
              const icon = CONTRACT_ICONS[contract.level_order] ?? '◆'
              const requiredLevel = Math.max(0, contract.level_order - 10)

              return (
                <motion.div
                  key={contract.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: idx * 0.1 }}
                  className={`relative border ${contract.unlocked ? 'cursor-pointer' : 'opacity-40 cursor-not-allowed'}`}
                  style={{
                    borderColor: contract.unlocked ? `${colors.border}40` : '#00FF4120',
                    background: contract.unlocked && contract.completed
                      ? `linear-gradient(135deg, ${colors.glow}, transparent)`
                      : 'transparent',
                  }}
                  onClick={() => contract.unlocked && router.push(`/contratos/${contract.id}`)}
                  whileHover={contract.unlocked ? { scale: 1.005 } : {}}
                >
                  <div className="px-6 py-5">
                    {/* Badge de nivel */}
                    <div className="flex items-center justify-between mb-4">
                      <div className="flex items-center gap-3">
                        <span className="text-lg" style={{ color: colors.accent }}>{icon}</span>
                        <div>
                          <div className="text-[9px] tracking-[0.5em] uppercase mb-0.5"
                            style={{ color: `${colors.accent}60` }}>
                            CONTRATO-{contract.level_order}
                          </div>
                          <div className="font-black tracking-[0.1em] text-sm text-white">
                            {contract.title.replace(`CONTRATO-${contract.level_order}: `, '')}
                          </div>
                        </div>
                      </div>
                      <div className="text-right shrink-0">
                        {contract.completed ? (
                          <div className="text-xs tracking-widest" style={{ color: colors.accent }}>
                            ✓ VALIDADO
                          </div>
                        ) : contract.unlocked ? (
                          <div className="text-[10px] text-[#00FF41]/30 tracking-widest">DISPONIBLE</div>
                        ) : (
                          <div className="text-[10px] text-[#00FF41]/20 tracking-widest">
                            🔒 NIVEL {requiredLevel}
                          </div>
                        )}
                      </div>
                    </div>

                    {/* Descripción narrativa */}
                    <p className="text-[10px] text-[#C0C0C0]/50 leading-5 mb-4 line-clamp-2">
                      {contract.lore_briefing}
                    </p>

                    {/* Meta del contrato */}
                    <div className="grid grid-cols-3 gap-3 mb-4">
                      <div className="border border-[#00FF41]/10 px-3 py-2 text-center">
                        <div className="text-[9px] text-[#00FF41]/25 tracking-widest mb-1">XP</div>
                        <div className="text-sm font-bold" style={{ color: colors.accent }}>
                          {contract.base_xp_reward.toLocaleString()}
                        </div>
                      </div>
                      <div className="border border-[#00FF41]/10 px-3 py-2 text-center">
                        <div className="text-[9px] text-[#00FF41]/25 tracking-widest mb-1">CRITERIOS</div>
                        <div className="text-sm font-bold text-white">{contract.criteria_count}</div>
                      </div>
                      <div className="border border-[#00FF41]/10 px-3 py-2 text-center">
                        <div className="text-[9px] text-[#00FF41]/25 tracking-widest mb-1">TIEMPO</div>
                        <div className="text-sm font-bold text-white">
                          {contract.telemetry_goal_time ? `${Math.round(contract.telemetry_goal_time / 60)}min` : '—'}
                        </div>
                      </div>
                    </div>

                    {/* Conceptos */}
                    <div className="flex flex-wrap gap-1.5">
                      {contract.concepts_taught.slice(0, 5).map(c => (
                        <span key={c}
                          className="text-[9px] tracking-widest border px-2 py-0.5"
                          style={{ borderColor: `${colors.accent}25`, color: `${colors.accent}60` }}>
                          {c}
                        </span>
                      ))}
                      {contract.concepts_taught.length > 5 && (
                        <span className="text-[9px] text-[#00FF41]/20 tracking-widest px-1">
                          +{contract.concepts_taught.length - 5}
                        </span>
                      )}
                    </div>

                    {/* CTA */}
                    {contract.unlocked && (
                      <div className="mt-4 flex items-center justify-between">
                        <span className="text-[9px] text-[#00FF41]/20 tracking-widest">
                          {contract.completed ? 'Puedes revisionarlo en cualquier momento' : 'Revisión por DAKI al enviar'}
                        </span>
                        <span className="text-[10px] tracking-[0.3em]"
                          style={{ color: colors.accent }}>
                          {contract.completed ? '[ REVISAR ]' : '[[ ACCEDER ]]'} →
                        </span>
                      </div>
                    )}
                  </div>

                  {/* Borde lateral de estado */}
                  {contract.unlocked && (
                    <div className="absolute left-0 top-0 bottom-0 w-0.5"
                      style={{ background: contract.completed ? colors.accent : `${colors.accent}30` }}
                    />
                  )}
                </motion.div>
              )
            })}
          </div>
        )}

        {/* Info bloque */}
        <div className="mt-10 border border-[#00FF41]/8 px-5 py-4">
          <p className="text-[9px] text-[#00FF41]/20 tracking-widest leading-6">
            {'// LOS CONTRATOS SON EVALUADOS POR DAKI CONTRA CRITERIOS TÉCNICOS ESPECÍFICOS.'}<br />
            {'// AL VALIDAR UN CONTRATO, RECIBIRÁS UN TUTORIAL PARA PUBLICARLO EN GITHUB.'}<br />
            {'// TRES CONTRATOS COMPLETADOS = CERTIFICADO DE MANDO DAKI EDTECH.'}
          </p>
        </div>

      </main>
    </div>
    </MobileGate>
  )
}
