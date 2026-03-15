'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { motion } from 'framer-motion'
import { useUserStore } from '@/store/userStore'
import LiveActivityFeed from '@/components/UI/LiveActivityFeed'

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000'

interface Mission {
  id: string
  title: string
  description: string
  difficulty_tier: number
  base_xp_reward: number
  completed: boolean
  attempts: number
  unlocked: boolean
  level_order: number | null
  phase: string | null
  concepts_taught: string[]
  challenge_type: string
}

const TIER_LABEL: Record<number, string> = {
  1: 'INICIANTE',
  2: 'INTERMEDIO',
  3: 'AVANZADO',
}

const TIER_COLOR: Record<number, string> = {
  1: '#00FF41',
  2: '#FFD700',
  3: '#FF4444',
}

const PHASE_LABEL: Record<string, string> = {
  fase0:   'FASE 0 · DRONE',
  basico:  'BÁSICO',
  control: 'CONTROL',
  bucles:  'BUCLES',
}

export default function MisionesPage() {
  const router = useRouter()
  const { userId, username, level, totalXp, streakDays } = useUserStore()
  const [missions, setMissions] = useState<Mission[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!userId) {
      router.replace('/')
      return
    }
    fetch(`${API_BASE}/api/v1/challenges?user_id=${userId}`)
      .then((r) => r.json())
      .then((data) => setMissions(data))
      .finally(() => setLoading(false))
  }, [userId, router])

  const completadas = missions.filter((m) => m.completed).length

  return (
    <div className="min-h-screen bg-[#0A0A0A] font-mono text-[#00FF41]">

      {/* Cabecera */}
      <header className="flex items-center justify-between px-6 py-3 bg-[#0D0D0D] border-b border-[#00FF41]/20">
        <div className="flex items-center gap-4">
          <span
            className="font-black tracking-widest text-sm"
            style={{ textShadow: '0 0 8px #00FF41' }}
          >
            PYTHON QUEST
          </span>
          <button
            onClick={() => router.push('/enigma')}
            className="text-[#00FF41]/35 hover:text-[#00FF41]/70 text-xs tracking-widest transition-colors border border-[#00FF41]/15 px-2.5 py-1 hover:border-[#00FF41]/30"
          >
            ENIGMA
          </button>
        </div>
        <div className="flex items-center gap-6 text-xs text-[#00FF41]/70">
          <span className="text-[#00FF41]/50">{username}</span>
          <span>NVL <strong className="text-[#00FF41]">{level}</strong></span>
          <span>XP <strong className="text-[#00FF41]">{totalXp.toLocaleString()}</strong></span>
          {streakDays > 0 && (
            <span>🔥 <strong className="text-[#00FF41]">{streakDays}d</strong></span>
          )}
        </div>
      </header>

      <main className="flex gap-0 max-w-5xl mx-auto px-4 py-10">
        {/* ── Columna principal ── */}
        <div className="flex-1 min-w-0 pr-6">

        {/* Título de sección */}
        <div className="mb-8">
          <h2 className="text-2xl font-black tracking-[0.15em] mb-1">MISIONES</h2>
          <p className="text-[#00FF41]/40 text-xs tracking-widest">
            {completadas}/{missions.length} COMPLETADAS
          </p>
          {/* Barra de progreso */}
          <div className="mt-3 h-px bg-[#00FF41]/10 w-full relative overflow-hidden">
            <motion.div
              className="absolute left-0 top-0 h-full bg-[#00FF41]"
              initial={{ width: 0 }}
              animate={{ width: missions.length ? `${(completadas / missions.length) * 100}%` : '0%' }}
              transition={{ duration: 0.8, ease: 'easeOut' }}
            />
          </div>
        </div>

        {/* Lista de misiones */}
        {loading ? (
          <p className="text-[#00FF41]/30 text-xs tracking-widest animate-pulse">
            CARGANDO MISIONES...
          </p>
        ) : (
          <div className="flex flex-col gap-3">
            {missions.map((mission, idx) => {
              const tierColor = TIER_COLOR[mission.difficulty_tier]
              const isLocked = !mission.unlocked
              const isDrone = mission.challenge_type === 'drone'
              const target = isDrone ? '/enigma' : `/challenge/${mission.id}`
              return (
                <motion.button
                  key={mission.id}
                  initial={{ opacity: 0, x: -16 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: idx * 0.07 }}
                  onClick={() => !isLocked && router.push(target)}
                  disabled={isLocked}
                  className={`w-full text-left px-5 py-4 border transition-all duration-150 ${
                    isLocked
                      ? 'border-[#00FF41]/10 opacity-35 cursor-not-allowed'
                      : mission.completed
                      ? 'border-[#00FF41]/40 bg-[#00FF41]/5 hover:bg-[#00FF41]/10'
                      : 'border-[#00FF41]/25 bg-[#0D0D0D] hover:border-[#00FF41]/60 hover:bg-[#00FF41]/5'
                  }`}
                >
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-3 mb-1">
                        {/* Número de misión */}
                        <span className="text-[#00FF41]/30 text-xs w-5 shrink-0">
                          {String(mission.level_order ?? idx + 1).padStart(2, '0')}
                        </span>
                        <h3 className="text-sm font-bold truncate">{mission.title}</h3>
                        {isDrone && (
                          <span className="text-[10px] tracking-widest text-[#00BFFF]/70 border border-[#00BFFF]/30 px-1.5 shrink-0">
                            DRONE
                          </span>
                        )}
                      </div>
                      <div className="flex items-center gap-3 pl-8 text-xs text-[#00FF41]/40">
                        {mission.phase && (
                          <>
                            <span className="text-[#00FF41]/30">
                              {PHASE_LABEL[mission.phase] ?? mission.phase.toUpperCase()}
                            </span>
                            <span>·</span>
                          </>
                        )}
                        <span style={{ color: `${tierColor}80` }}>
                          {TIER_LABEL[mission.difficulty_tier]}
                        </span>
                        <span>·</span>
                        <span>{mission.base_xp_reward} XP</span>
                        {mission.attempts > 0 && !mission.completed && (
                          <>
                            <span>·</span>
                            <span>{mission.attempts} intento{mission.attempts !== 1 ? 's' : ''}</span>
                          </>
                        )}
                      </div>
                    </div>

                    {/* Estado */}
                    <div className="shrink-0 text-xs tracking-widest pt-0.5">
                      {isLocked ? (
                        <span className="text-[#00FF41]/25">BLOQUEADA</span>
                      ) : mission.completed ? (
                        <span className="text-[#00FF41]" style={{ textShadow: '0 0 6px #00FF41' }}>
                          ✓ COMPLETA
                        </span>
                      ) : (
                        <span className="text-[#00FF41]/50">DISPONIBLE ▶</span>
                      )}
                    </div>
                  </div>
                </motion.button>
              )
            })}
          </div>
        )}

        {/* ── Tarjeta de Boss Fight ───────────────────────────────────────── */}
        {!loading && (
          <motion.div
            className="mt-10"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
          >
            {/* Separador */}
            <div className="flex items-center gap-3 mb-5">
              <div className="h-px flex-1 bg-red-500/20" />
              <span className="text-red-500/60 text-xs tracking-[0.3em] font-bold">JEFE FINAL</span>
              <div className="h-px flex-1 bg-red-500/20" />
            </div>

            <motion.button
              onClick={() => router.push('/boss')}
              className="w-full text-left px-5 py-5 border-2 border-red-500/40 bg-red-950/20 hover:border-red-500/80 hover:bg-red-950/35 transition-all duration-200"
              whileHover={{ scale: 1.01 }}
              whileTap={{ scale: 0.99 }}
            >
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <motion.span
                      className="text-red-500 font-black text-xl"
                      animate={{ textShadow: ['0 0 10px #FF4444', '0 0 25px #FF4444', '0 0 10px #FF4444'] }}
                      transition={{ duration: 1.2, repeat: Infinity }}
                    >
                      ∞
                    </motion.span>
                    <h3 className="text-base font-black text-red-400 tracking-wider">
                      THE INFINITE LOOPER
                    </h3>
                    <span className="text-[10px] tracking-widest text-red-500/60 border border-red-500/30 px-1.5">
                      BOSS
                    </span>
                  </div>
                  <p className="text-xs text-red-400/50 leading-relaxed pl-8 mb-2">
                    Módulo: Bucles · Detén el bucle infinito usando <code className="bg-red-900/40 px-1 rounded">for</code> acotado.
                    Tienes 45 segundos antes de que el sistema colapse.
                  </p>
                  <div className="pl-8 flex items-center gap-3 text-xs text-red-500/40">
                    <span>AVANZADO</span>
                    <span>·</span>
                    <span className="text-yellow-400/80 font-bold">1 500 XP</span>
                    <span>·</span>
                    <span>Tiempo límite: 45 s</span>
                  </div>
                </div>
                <div className="shrink-0 text-xs tracking-widest text-red-400/60 pt-0.5">
                  COMBATIR ▶
                </div>
              </div>
            </motion.button>
          </motion.div>
        )}
        {/* ── Tarjeta de Bounties ────────────────────────────────────────── */}
        {!loading && (
          <motion.div
            className="mt-6"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.75 }}
          >
            <div className="flex items-center gap-3 mb-5">
              <div className="h-px flex-1 bg-[#FFD700]/15" />
              <span className="text-[#FFD700]/50 text-xs tracking-[0.3em] font-bold">BOUNTIES IA</span>
              <div className="h-px flex-1 bg-[#FFD700]/15" />
            </div>

            <motion.button
              onClick={() => router.push('/bounty')}
              className="w-full text-left px-5 py-5 border border-[#FFD700]/30 bg-[#0A0A08] hover:border-[#FFD700]/70 hover:bg-[#FFD700]/5 transition-all duration-200"
              whileHover={{ scale: 1.01 }}
              whileTap={{ scale: 0.99 }}
            >
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <span className="text-[#FFD700] font-black text-xl">◆</span>
                    <h3 className="text-base font-black text-[#FFD700]/80 tracking-wider">
                      MISIONES BOUNTY
                    </h3>
                    <span className="text-[10px] tracking-widest text-[#FFD700]/50 border border-[#FFD700]/25 px-1.5">
                      IA
                    </span>
                  </div>
                  <p className="text-xs text-[#FFD700]/40 leading-relaxed pl-8">
                    Genera retos únicos con Claude Opus. Elige concepto y dificultad — misiones infinitas.
                  </p>
                </div>
                <div className="shrink-0 text-xs tracking-widest text-[#FFD700]/40 pt-0.5">
                  GENERAR ▶
                </div>
              </div>
            </motion.button>
          </motion.div>
        )}

        </div>{/* end columna principal */}

        {/* ── Sidebar Feed ── */}
        <aside className="w-64 shrink-0 hidden lg:flex flex-col sticky top-8 self-start h-[calc(100vh-7rem)] border border-white/8 bg-[#080808]">
          <LiveActivityFeed />
        </aside>
      </main>
    </div>
  )
}
