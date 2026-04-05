'use client'

import { useEffect, useState, useCallback } from 'react'
import { useRouter } from 'next/navigation'
import { motion, AnimatePresence } from 'framer-motion'
import { useUserStore } from '@/store/userStore'
import MissionBriefingModal from '@/components/Game/MissionBriefingModal'
import HackingTransition from '@/components/Game/HackingTransition'
import MobileGate from '@/components/UI/MobileGate'
import { TIER_LABEL, TIER_COLOR } from '@/lib/tierLabels'

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? ''

// ─── Tipos ─────────────────────────────────────────────────────────────────────

interface Level {
  id: string
  title: string
  description: string
  difficulty_tier: number
  difficulty: string | null
  base_xp_reward: number
  level_order: number | null
  phase: string | null
  concepts_taught: string[]
  challenge_type: string
  theory_content: string | null
  lore_briefing: string | null
  pedagogical_objective: string | null
  syntax_hint: string | null
  hints: string[]
  completed: boolean
  attempts: number
  unlocked: boolean
  status: string
  sector_id: number | null
  is_project: boolean
  telemetry_goal_time: number | null
  strict_match: boolean
  initial_code: string
  test_inputs: string[]
}

// ─── Mapa de slug → codex_id (solo Python) ───────────────────────────────────

const SLUG_TO_CODEX: Record<string, { codex_id: string; label: string; color: string }> = {
  'python-core': { codex_id: 'python_core', label: 'PYTHON CORE', color: '#00FF41' },
}

// ─── Constantes UI ─────────────────────────────────────────────────────────────

const PHASE_LABELS: Record<string, string> = {}

// ─── Panel de Briefing ─────────────────────────────────────────────────────────

function BriefingPanel({
  level,
  accentColor,
  onDeploy,
}: {
  level: Level | null
  accentColor: string
  onDeploy: (l: Level) => void
}) {
  if (!level) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center text-center px-12">
        <motion.div
          className="w-16 h-16 rounded-full border flex items-center justify-center mb-6"
          style={{ borderColor: `${accentColor}25` }}
          animate={{ opacity: [0.3, 0.7, 0.3] }}
          transition={{ duration: 2.5, repeat: Infinity }}
        >
          <span style={{ color: `${accentColor}40` }} className="text-2xl">🛡</span>
        </motion.div>
        <p className="text-[10px] tracking-[0.5em]" style={{ color: `${accentColor}30` }}>
          SELECCIONA UNA MISIÓN
        </p>
      </div>
    )
  }

  const order = level.level_order ?? 0
  const tierColor = TIER_COLOR[level.difficulty_tier]
  const isLocked = !level.unlocked
  const phaseLabel = level.phase ? (PHASE_LABELS[level.phase] ?? level.phase.toUpperCase()) : null

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={level.id}
        className="flex-1 flex flex-col px-8 py-8 overflow-y-auto"
        initial={{ opacity: 0, x: 16 }}
        animate={{ opacity: 1, x: 0 }}
        exit={{ opacity: 0, x: -8 }}
        transition={{ duration: 0.25 }}
      >
        {/* Tag de clasificación */}
        <div className="flex items-center gap-3 mb-5">
          <span className="text-[8px] tracking-[0.6em]" style={{ color: `${accentColor}40` }}>
            MISIÓN #{String(order).padStart(3, '0')}
            {phaseLabel && <> // {phaseLabel}</>}
          </span>
          {level.completed && (
            <span
              className="text-[8px] tracking-widest border px-2 py-0.5"
              style={{ color: accentColor, borderColor: `${accentColor}50`, textShadow: `0 0 6px ${accentColor}` }}
            >
              ✓ COMPLETADA
            </span>
          )}
        </div>

        {/* Título */}
        <h2
          className="text-2xl font-black tracking-wider mb-1"
          style={{ color: accentColor, textShadow: `0 0 12px ${accentColor}70` }}
        >
          {level.title.toUpperCase()}
        </h2>

        {/* Dificultad + XP */}
        <div className="flex items-center gap-4 mb-6">
          <span className="text-[10px] tracking-widest font-bold" style={{ color: `${tierColor}90` }}>
            {TIER_LABEL[level.difficulty_tier]}
          </span>
          <span style={{ color: `${accentColor}30` }}>·</span>
          <span
            className="text-sm font-black text-[#FFD700]"
            style={{ textShadow: '0 0 8px rgba(255,215,0,0.5)' }}
          >
            {level.base_xp_reward} XP
          </span>
          {level.attempts > 0 && !level.completed && (
            <>
              <span style={{ color: `${accentColor}30` }}>·</span>
              <span className="text-[10px]" style={{ color: `${accentColor}50` }}>
                {level.attempts} intento{level.attempts !== 1 ? 's' : ''}
              </span>
            </>
          )}
        </div>

        {/* Separador */}
        <div
          className="h-px mb-6"
          style={{ background: `linear-gradient(to right, ${accentColor}30, ${accentColor}15, transparent)` }}
        />

        {/* Descripción / Objetivo */}
        <div className="mb-5">
          <p className="text-[9px] tracking-[0.5em] mb-3" style={{ color: `${accentColor}40` }}>◆ OBJETIVO TÁCTICO</p>
          <div
            className="pl-4 bg-black/40 backdrop-blur-sm py-3 pr-3"
            style={{ borderLeft: `2px solid ${accentColor}40`, boxShadow: `inset 0 0 20px ${accentColor}05` }}
          >
            <p className="text-[12px] leading-relaxed" style={{ color: `${accentColor}80` }}>
              {level.description}
            </p>
          </div>
        </div>

        {/* Lore briefing */}
        {level.lore_briefing && (
          <div className="mb-6">
            <p className="text-[9px] tracking-[0.5em] mb-2" style={{ color: `${accentColor}30` }}>TRANSMISIÓN DE DAKI</p>
            <p className="text-[11px] leading-relaxed italic" style={{ color: `${accentColor}50` }}>
              &ldquo;{level.lore_briefing}&rdquo;
            </p>
          </div>
        )}

        {/* Spacer */}
        <div className="flex-1" />

        {/* Botón */}
        {isLocked ? (
          <div className="border bg-black/40 px-5 py-4 text-center" style={{ borderColor: `${accentColor}15` }}>
            <p className="text-[10px] tracking-[0.5em]" style={{ color: `${accentColor}30` }}>
              🔒 MISIÓN BLOQUEADA
            </p>
            <p className="text-[9px] mt-1 tracking-widest" style={{ color: `${accentColor}15` }}>
              COMPLETA LA MISIÓN ANTERIOR PARA DESBLOQUEAR
            </p>
          </div>
        ) : (
          <motion.button
            onClick={() => onDeploy(level)}
            className="w-full py-4 border-2 font-black text-sm tracking-[0.3em] transition-all duration-200 cursor-pointer"
            style={{
              borderColor: `${accentColor}90`,
              color: accentColor,
              background: `${accentColor}10`,
              boxShadow: `0 0 20px ${accentColor}15`,
              textShadow: `0 0 8px ${accentColor}90`,
            }}
            whileHover={{
              background: `${accentColor}20`,
              boxShadow: `0 0 40px ${accentColor}30, inset 0 0 20px ${accentColor}08`,
            }}
            whileTap={{ scale: 0.98 }}
          >
            ▶ INICIALIZAR ENLACE — ENTRAR A LA MISIÓN
          </motion.button>
        )}
      </motion.div>
    </AnimatePresence>
  )
}

// ─── Página principal ──────────────────────────────────────────────────────────

export default function CodexPage({ params }: { params: { slug: string } }) {
  const { slug } = params
  const router = useRouter()
  const { _hasHydrated, userId, username, level, totalXp } = useUserStore()

  const config = SLUG_TO_CODEX[slug]

  const [levels, setLevels] = useState<Level[]>([])
  const [loading, setLoading] = useState(true)
  const [fetchError, setFetchError] = useState(false)
  const [selected, setSelected] = useState<Level | null>(null)
  const [briefingLevel, setBriefingLevel] = useState<Level | null>(null)
  const [isHacking, setIsHacking] = useState(false)
  const [hackingTitle, setHackingTitle] = useState('')

  const accentColor = config?.color ?? '#00D4FF'
  const codexLabel = config?.label ?? slug.toUpperCase().replace(/-/g, ' ')
  const codexId = config?.codex_id ?? slug.replace(/-/g, '_')

  useEffect(() => {
    if (!_hasHydrated) return
    if (!userId) { router.replace('/login'); setLoading(false); return }

    fetch(`${API_BASE}/api/v1/levels/codex/${codexId}?user_id=${userId}`)
      .then(r => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`)
        return r.json()
      })
      .then((data: Level[]) => {
        if (!data || data.length === 0) {
            setFetchError(true)
            setTimeout(() => router.replace('/hub'), 2500)
            return
        }
        setLevels(data)
        const first = data.find(l => l.unlocked && !l.completed) ?? data[0]
        if (first) setSelected(first)
      })
      .catch(err => { 
          console.error('[Codex] Error:', err); 
          setFetchError(true);
          setTimeout(() => router.replace('/hub'), 2500);
      })
      .finally(() => setLoading(false))
  }, [_hasHydrated, userId, router, codexId])

  const completadas = levels.filter(l => l.completed).length

  const handleDeploy = useCallback((level: Level) => {
    if (!level.unlocked) return
    if (level.lore_briefing) { setBriefingLevel(level); return }
    setHackingTitle(level.title)
    setIsHacking(true)
    setTimeout(() => router.push(`/challenge/${level.id}`), 1500)
  }, [router])

  const handleBriefingInitialize = useCallback(() => {
    if (!briefingLevel) return
    const lv = briefingLevel
    setBriefingLevel(null)
    setHackingTitle(lv.title)
    setIsHacking(true)
    setTimeout(() => router.push(`/challenge/${lv.id}`), 1500)
  }, [briefingLevel, router])

  if (!config) {
    return (
      <div
        className="min-h-screen flex items-center justify-center"
        style={{ background: '#0A0A0A', fontFamily: 'monospace', color: '#FF2D78' }}
      >
        [ ERROR: CODEX &quot;{slug}&quot; NO RECONOCIDO ]
      </div>
    )
  }

  return (
    <MobileGate>
      <div
        className="h-[calc(100vh-2rem)] flex flex-col font-mono relative overflow-hidden"
        style={{
          color: accentColor,
          background: `radial-gradient(circle at 50% 40%, ${accentColor}08 0%, #000000 60%)`,
        }}
      >
        {/* Scanlines */}
        <div
          className="fixed inset-0 pointer-events-none z-10"
          style={{ backgroundImage: 'repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,0.07) 2px,rgba(0,0,0,0.07) 4px)' }}
        />
        <div
          className="fixed inset-0 pointer-events-none z-10"
          style={{ background: 'radial-gradient(ellipse at center, transparent 40%, rgba(0,0,0,0.75) 100%)' }}
        />

        {/* Modal de briefing */}
        <MissionBriefingModal
          visible={briefingLevel !== null}
          title={briefingLevel?.title ?? ''}
          loreBriefing={briefingLevel?.lore_briefing ?? ''}
          pedagogicalObjective={briefingLevel?.pedagogical_objective ?? ''}
          syntaxHint={briefingLevel?.syntax_hint ?? ''}
          onInitialize={handleBriefingInitialize}
          onClose={() => setBriefingLevel(null)}
        />

        {/* Transición de hackeo */}
        <HackingTransition isActive={isHacking} missionTitle={hackingTitle} />

        {/* Header */}
        <header className="relative z-20 shrink-0 flex items-center justify-between px-6 py-2.5 border-b bg-black/50 backdrop-blur-sm"
          style={{ borderColor: `${accentColor}18` }}>
          <div className="flex items-center gap-4">
            <button
              onClick={() => router.push('/hub')}
              className="text-xs tracking-widest transition-colors border px-2.5 py-1 cursor-pointer"
              style={{ color: `${accentColor}55`, borderColor: `${accentColor}20` }}
            >
              ← HUB
            </button>
            <span
              className="font-black tracking-widest text-sm hidden sm:block"
              style={{ color: accentColor, textShadow: `0 0 8px ${accentColor}` }}
            >
              {codexLabel}
            </span>
          </div>
          <div className="flex items-center gap-5 text-xs" style={{ color: `${accentColor}60` }}>
            <span style={{ color: `${accentColor}40` }} className="hidden sm:block">{username}</span>
            <span>RANGO <strong style={{ color: accentColor }}>{level}</strong></span>
            <span>XP <strong style={{ color: accentColor }}>{totalXp.toLocaleString()}</strong></span>
          </div>
        </header>

        {/* Split screen */}
        <main className="relative z-20 flex-1 flex overflow-hidden gap-px">

          {/* COLUMNA IZQUIERDA — Lista de misiones */}
          <div
            className="w-[340px] shrink-0 flex flex-col overflow-hidden bg-black/40 backdrop-blur-md border-r"
            style={{ borderColor: `${accentColor}20`, boxShadow: `4px 0 30px ${accentColor}08` }}
          >
            {/* Cabecera columna */}
            <div className="shrink-0 px-5 py-4 border-b bg-black/30"
              style={{ borderColor: `${accentColor}15` }}>
              <h2
                className="text-xs font-black tracking-[0.4em] mb-1"
                style={{ color: `${accentColor}80`, textShadow: `0 0 6px ${accentColor}60` }}
              >
                MISIONES
              </h2>
              <div className="flex items-center gap-3 mt-2">
                <div className="flex-1 h-px relative overflow-hidden" style={{ background: `${accentColor}15` }}>
                  <motion.div
                    className="absolute left-0 top-0 h-full"
                    style={{ background: accentColor, boxShadow: `0 0 6px ${accentColor}` }}
                    initial={{ width: 0 }}
                    animate={{ width: levels.length ? `${(completadas / levels.length) * 100}%` : '0%' }}
                    transition={{ duration: 1, ease: 'easeOut' }}
                  />
                </div>
                <span className="text-[9px] tracking-widest shrink-0" style={{ color: `${accentColor}40` }}>
                  {completadas}/{levels.length}
                </span>
              </div>
            </div>

            {/* Lista scrollable */}
            <div className="flex-1 overflow-y-auto py-2">
              {loading ? (
                <p className="text-[10px] tracking-widest animate-pulse px-5 py-6" style={{ color: `${accentColor}30` }}>
                  CARGANDO MISIONES...
                </p>
              ) : fetchError ? (
                <div className="flex flex-col items-center justify-center text-center px-5 py-10 mt-10">
                  <p className="text-red-400/80 text-[11px] font-black tracking-widest mb-3">
                    [ CONEXIÓN FRAGMENTADA ]
                  </p>
                  <p className="text-[9px] tracking-[0.2em]" style={{ color: `${accentColor}50` }}>
                    Módulos no disponibles. Reconectando al Hub...
                  </p>
                </div>
              ) : (
                levels.map((l, idx) => {
                  const isLocked = !l.unlocked
                  const isSelected = selected?.id === l.id
                  const isAvailable = l.unlocked && !l.completed

                  return (
                    <motion.button
                      key={l.id}
                      initial={{ opacity: 0, x: -12 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: Math.min(idx * 0.03, 1.5) }}
                      onClick={() => { if (!isLocked) setSelected(l) }}
                      disabled={isLocked}
                      className={[
                        'w-full text-left px-5 py-3.5 border-b transition-all duration-200 relative border-l-4',
                        isLocked
                          ? 'opacity-40 grayscale cursor-not-allowed border-l-transparent'
                          : isSelected
                            ? 'cursor-pointer'
                            : 'cursor-pointer hover:translate-x-1',
                      ].join(' ')}
                      style={{
                        borderBottomColor: `${accentColor}08`,
                        borderLeftColor: isLocked ? 'transparent' : isSelected ? accentColor : `${accentColor}35`,
                        background: isSelected ? `${accentColor}10` : 'transparent',
                        boxShadow: isSelected ? `inset 0 0 20px ${accentColor}08` : 'none',
                      }}
                    >
                      <div className="flex items-center justify-between gap-3">
                        <div className="flex items-center gap-3 min-w-0">
                          <span className="text-[10px] w-6 shrink-0 tabular-nums" style={{ color: `${accentColor}30` }}>
                            {String(l.level_order ?? idx + 1).padStart(3, '0')}
                          </span>
                          <span
                            className="text-[11px] font-bold tracking-wide truncate"
                            style={{
                              color: isLocked ? `${accentColor}30`
                                : isSelected ? accentColor
                                  : `${accentColor}90`,
                              textShadow: isSelected ? `0 0 8px ${accentColor}80` : 'none',
                            }}
                          >
                            {l.title}
                          </span>
                        </div>
                        <div className="shrink-0 text-[9px] flex items-center gap-1.5">
                          {isLocked ? (
                            <span style={{ color: `${accentColor}25` }}>🔒</span>
                          ) : l.completed ? (
                            <span style={{ color: accentColor, textShadow: `0 0 6px ${accentColor}` }}>✓</span>
                          ) : isAvailable ? (
                            <>
                              <span
                                className="w-1.5 h-1.5 rounded-full animate-pulse shrink-0"
                                style={{ background: accentColor, boxShadow: `0 0 4px ${accentColor}` }}
                              />
                              <span style={{ color: `${accentColor}70` }}>▶</span>
                            </>
                          ) : null}
                        </div>
                      </div>
                      <div className="pl-9 mt-0.5 flex items-center gap-2">
                        <span className="text-[8px] tracking-widest" style={{ color: `${TIER_COLOR[l.difficulty_tier]}50` }}>
                          {TIER_LABEL[l.difficulty_tier]}
                        </span>
                        {l.attempts > 0 && !l.completed && (
                          <span className="text-[8px]" style={{ color: `${accentColor}30` }}>
                            · {l.attempts} intento{l.attempts !== 1 ? 's' : ''}
                          </span>
                        )}
                      </div>
                    </motion.button>
                  )
                })
              )}
            </div>
          </div>

          {/* COLUMNA DERECHA — Panel de Briefing */}
          <div
            className="flex-1 bg-black/40 backdrop-blur-md overflow-hidden"
            style={{ boxShadow: 'inset 4px 0 30px rgba(0,0,0,0.3)' }}
          >
            <BriefingPanel level={selected} accentColor={accentColor} onDeploy={handleDeploy} />
          </div>

        </main>
      </div>
    </MobileGate>
  )
}
