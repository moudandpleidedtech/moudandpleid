'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { motion, AnimatePresence } from 'framer-motion'
import { useUserStore } from '@/store/userStore'
import MissionBriefingModal from '@/components/Game/MissionBriefingModal'
import HackingTransition from '@/components/Game/HackingTransition'

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000'

// ─── Tipos ─────────────────────────────────────────────────────────────────────

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
  lore_briefing: string | null
  pedagogical_objective: string | null
  syntax_hint: string | null
}

// ─── Lore por level_order ──────────────────────────────────────────────────────

const MISSION_LORE: Record<number, { lore: string; requires: string; chapter: string }> = {
  0: {
    lore: 'Los sistemas del dron están desincronizados. Antes de infiltrarte en el Nexo debes completar la calibración sináptica obligatoria. DAKI te guiará paso a paso para restablecer el enlace neuronal.',
    requires: 'Sintaxis Python Básica',
    chapter: 'Manual Cap. 0',
  },
  1: {
    lore: 'Establece un pulso de identidad para atravesar los nodos de reconocimiento del Nexo. El sistema espera una señal de confirmación neuronal. Si el protocolo falla, la Matriz aislará tu consciencia.',
    requires: 'Print y Variables',
    chapter: 'Manual Cap. 1',
  },
  2: {
    lore: 'Descifra las coordenadas del nodo de acceso sumando los registros sinápticos cifrados. Los valores están fragmentados en la Matriz Neuronal — reconstruyelos con operaciones precisas.',
    requires: 'Operadores Matemáticos',
    chapter: 'Manual Cap. 1',
  },
  3: {
    lore: 'Invierte el flujo de datos del firewall neuronal para crear un canal de retorno. La secuencia del Nexo debe leerse en orden inverso para que el protocolo de bypass sináptico funcione.',
    requires: 'Slicing de Strings',
    chapter: 'Manual Cap. 2',
  },
  4: {
    lore: 'Escanea el tejido de código enemigo en busca de nodos de energía activos (vocales). Cada nodo amplifica la señal de tu dron neural. Localízalos y cuéntalos antes de que el Nexo los enmascare.',
    requires: 'For Loops e If',
    chapter: 'Manual Cap. 2',
  },
  5: {
    lore: 'Sincroniza el motor de salto neuronal con la frecuencia fractal de Fibonacci para evadir los detectores de patrones del Nexo. Un solo error de sincronía colapsa el canal sináptico.',
    requires: 'Lógica Avanzada',
    chapter: 'Manual Cap. 3',
  },
}

// ─── Constantes UI ─────────────────────────────────────────────────────────────

const TIER_LABEL: Record<number, string> = { 1: 'INICIANTE', 2: 'INTERMEDIO', 3: 'AVANZADO' }
const TIER_COLOR: Record<number, string> = { 1: '#00FF41', 2: '#FFD700', 3: '#FF4444' }

// ─── Panel de Briefing (columna derecha) ───────────────────────────────────────

function BriefingPanel({
  mission,
  onDeploy,
}: {
  mission: Mission | null
  onDeploy: (_m: Mission) => void
}) {
  if (!mission) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center text-center px-12">
        <motion.div
          className="w-16 h-16 rounded-full border border-[#00FF41]/15 flex items-center justify-center mb-6"
          animate={{ opacity: [0.3, 0.7, 0.3] }}
          transition={{ duration: 2.5, repeat: Infinity }}
        >
          <span className="text-[#00FF41]/30 text-2xl">◈</span>
        </motion.div>
        <p className="text-[10px] tracking-[0.5em] text-[#00FF41]/20">
          SELECCIONA UNA INCURSIÓN
        </p>
        <p className="text-[9px] tracking-widest text-[#00FF41]/12 mt-2">
          PARA VER EL BRIEFING TÁCTICO
        </p>
      </div>
    )
  }

  const order = mission.level_order ?? 0
  const lore = MISSION_LORE[order]
  const tierColor = TIER_COLOR[mission.difficulty_tier]
  const isLocked = !mission.unlocked

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={mission.id}
        className="flex-1 flex flex-col px-8 py-8 overflow-y-auto"
        initial={{ opacity: 0, x: 16 }}
        animate={{ opacity: 1, x: 0 }}
        exit={{ opacity: 0, x: -8 }}
        transition={{ duration: 0.25 }}
      >
        {/* Tag de clasificación */}
        <div className="flex items-center gap-3 mb-5">
          <span className={`text-[8px] tracking-[0.6em] ${mission.challenge_type === 'tutorial' ? 'text-cyan-400/40' : 'text-[#00FF41]/25'}`}>
            {mission.challenge_type === 'tutorial'
              ? 'PROTOCOLO 00 // CALIBRACIÓN OBLIGATORIA'
              : `INCURSIÓN #${String(order).padStart(2, '0')} // EL NEXO`}
          </span>
          {mission.completed && (
            <span
              className="text-[8px] tracking-widest border px-2 py-0.5"
              style={mission.challenge_type === 'tutorial'
                ? { color: 'rgba(0,229,255,0.9)', borderColor: 'rgba(0,229,255,0.3)', textShadow: '0 0 6px rgba(0,229,255,0.6)' }
                : { color: '#00FF41', borderColor: 'rgba(0,255,65,0.3)', textShadow: '0 0 6px #00FF41' }
              }
            >
              ✓ COMPLETADA
            </span>
          )}
        </div>

        {/* Título */}
        <h2
          className="text-2xl font-black tracking-wider mb-1 drop-shadow-[0_0_12px_rgba(0,255,65,0.7)]"
          style={{ color: '#00FF41' }}
        >
          {mission.title.toUpperCase()}
        </h2>

        {/* Dificultad + XP */}
        <div className="flex items-center gap-4 mb-6">
          <span className="text-[10px] tracking-widest font-bold" style={{ color: `${tierColor}90` }}>
            {TIER_LABEL[mission.difficulty_tier]}
          </span>
          <span className="text-[#00FF41]/20">·</span>
          <span
            className="text-sm font-black text-[#FFD700]"
            style={{ textShadow: '0 0 8px rgba(255,215,0,0.5)' }}
          >
            {mission.base_xp_reward} XP
          </span>
          {mission.attempts > 0 && !mission.completed && (
            <>
              <span className="text-[#00FF41]/20">·</span>
              <span className="text-[10px] text-green-200/50">
                {mission.attempts} intento{mission.attempts !== 1 ? 's' : ''}
              </span>
            </>
          )}
        </div>

        {/* Separador */}
        <div className="h-px bg-gradient-to-r from-[#00FF41]/20 via-[#00FF41]/10 to-transparent mb-6" />

        {/* Lore / Objetivo táctico */}
        <div className="mb-5">
          <p className="text-[9px] tracking-[0.5em] text-[#00FF41]/30 mb-3">◆ OBJETIVO TÁCTICO</p>
          <div
            className="border-l-2 border-[#00FF41]/30 pl-4 bg-black/40 backdrop-blur-sm py-3 pr-3"
            style={{ boxShadow: 'inset 0 0 20px rgba(0,255,65,0.03)' }}
          >
            <p className="text-[12px] text-green-200/70 leading-relaxed">
              {lore?.lore ?? mission.description}
            </p>
          </div>
        </div>

        {/* Conocimiento requerido */}
        {lore && (
          <div
            className="border border-[#00E5FF]/20 bg-black/40 backdrop-blur-sm px-4 py-3 mb-6"
            style={{ boxShadow: '0 4px 20px rgba(0,229,255,0.06)' }}
          >
            <p className="text-[8px] tracking-[0.5em] text-[#00E5FF]/35 mb-2">CONOCIMIENTO REQUERIDO</p>
            <div className="flex items-center gap-3">
              <span className="text-[11px] text-[#00E5FF]/70 font-bold tracking-wider">
                {lore.requires}
              </span>
              <span className="text-[#00E5FF]/20">·</span>
              <span className="text-[9px] tracking-widest text-[#00E5FF]/35 border border-[#00E5FF]/15 px-2 py-0.5">
                {lore.chapter}
              </span>
            </div>
          </div>
        )}

        {/* Lore briefing si existe */}
        {mission.lore_briefing && (
          <div className="mb-6">
            <p className="text-[9px] tracking-[0.5em] text-[#00FF41]/25 mb-2">TRANSMISIÓN DE DAKI</p>
            <p className="text-[11px] text-[#00FF41]/40 leading-relaxed italic">
              &ldquo;{mission.lore_briefing}&rdquo;
            </p>
          </div>
        )}

        {/* Spacer */}
        <div className="flex-1" />

        {/* Botón de despliegue */}
        {isLocked ? (
          <div className="border border-[#00FF41]/10 bg-black/40 backdrop-blur-sm px-5 py-4 text-center">
            <p className="text-[10px] tracking-[0.5em] text-[#00FF41]/25">
              🔒 INCURSIÓN BLOQUEADA
            </p>
            <p className="text-[9px] text-[#00FF41]/12 mt-1 tracking-widest">
              COMPLETA EL PROTOCOLO 00 PARA DESBLOQUEAR
            </p>
          </div>
        ) : mission.challenge_type === 'tutorial' ? (
          <motion.button
            onClick={() => onDeploy(mission)}
            className="w-full py-4 border-2 font-black text-sm tracking-[0.28em] transition-all duration-200 cursor-pointer"
            style={{
              borderColor: 'rgba(0,229,255,0.6)',
              color: 'rgba(0,229,255,0.9)',
              background: 'rgba(0,229,255,0.06)',
              boxShadow: '0 0 20px rgba(0,229,255,0.1)',
              textShadow: '0 0 8px rgba(0,229,255,0.6)',
            }}
            whileHover={{
              background: 'rgba(0,229,255,0.12)',
              boxShadow: '0 0 40px rgba(0,229,255,0.25), inset 0 0 20px rgba(0,229,255,0.05)',
            }}
            whileTap={{ scale: 0.98 }}
          >
            ▶ INICIALIZAR CALIBRACIÓN SINÁPTICA
          </motion.button>
        ) : (
          <motion.button
            onClick={() => onDeploy(mission)}
            className="w-full py-4 border-2 font-black text-sm tracking-[0.3em] transition-all duration-200 cursor-pointer"
            style={{
              borderColor: 'rgba(0,255,65,0.6)',
              color: '#00FF41',
              background: 'rgba(0,255,65,0.07)',
              boxShadow: '0 0 20px rgba(0,255,65,0.1)',
              textShadow: '0 0 8px rgba(0,255,65,0.6)',
            }}
            whileHover={{
              background: 'rgba(0,255,65,0.14)',
              boxShadow: '0 0 40px rgba(0,255,65,0.3), inset 0 0 20px rgba(0,255,65,0.05)',
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

export default function MisionesPage() {
  const router = useRouter()
  const { userId, username, level, totalXp, streakDays, completedChallengeIds } = useUserStore()
  const [missions, setMissions] = useState<Mission[]>([])
  const [loading, setLoading] = useState(true)
  const [fetchError, setFetchError] = useState(false)
  const [selected, setSelected] = useState<Mission | null>(null)
  const [briefingMission, setBriefingMission] = useState<Mission | null>(null)
  const [isHacking, setIsHacking] = useState(false)
  const [hackingTitle, setHackingTitle] = useState('')
  // Esperar a que Zustand hidrate desde localStorage antes de evaluar userId
  const [hydrated, setHydrated] = useState(false)
  useEffect(() => { setHydrated(true) }, [])

  useEffect(() => {
    if (!hydrated) return
    if (!userId) { router.replace('/'); setLoading(false); return }
    fetch(`${API_BASE}/api/v1/challenges?user_id=${userId}`)
      .then(r => r.json())
      .then((data: Mission[]) => {
        // Merge local cache: marcar como completadas las misiones que constan en localStorage
        const merged = data.map(m =>
          completedChallengeIds.includes(m.id) ? { ...m, completed: true } : m
        )
        setMissions(merged)
        const first = merged.find(m => m.unlocked && !m.completed) ?? merged[0]
        if (first) setSelected(first)
      })
      .catch(err => { console.log('[Misiones] Error:', err); setFetchError(true) })
      .finally(() => setLoading(false))
  }, [hydrated, userId, router])

  const completadas = missions.filter(m => m.completed).length
  const tutorial = missions.find(m => m.challenge_type === 'tutorial')
  const tutorialDone = tutorial?.completed ?? true

  const handleDeploy = (mission: Mission) => {
    if (!mission.unlocked) return
    // Misiones drone no tienen transición de hackeo (van a /enigma directamente)
    if (mission.challenge_type === 'drone') { router.push('/enigma'); return }
    // Si tiene lore briefing, mostrarlo antes de la transición
    if (mission.lore_briefing) { setBriefingMission(mission); return }
    // Transición de hackeo → luego push
    setHackingTitle(mission.title)
    setIsHacking(true)
    setTimeout(() => router.push(`/challenge/${mission.id}`), 1500)
  }

  const handleBriefingInitialize = () => {
    if (!briefingMission) return
    const mission = briefingMission
    setBriefingMission(null)
    setHackingTitle(mission.title)
    setIsHacking(true)
    setTimeout(() => router.push(`/challenge/${mission.id}`), 1500)
  }

  return (
    <div
      className="h-[calc(100vh-2rem)] flex flex-col font-mono text-[#00FF41] relative overflow-hidden"
      style={{ background: 'radial-gradient(circle at 50% 40%, #001a0d 0%, #000000 60%)' }}
    >
      {/* Scanlines */}
      <div
        className="fixed inset-0 pointer-events-none z-10"
        style={{ backgroundImage: 'repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,0.07) 2px,rgba(0,0,0,0.07) 4px)' }}
      />
      {/* Viñeta */}
      <div
        className="fixed inset-0 pointer-events-none z-10"
        style={{ background: 'radial-gradient(ellipse at center, transparent 40%, rgba(0,0,0,0.75) 100%)' }}
      />

      {/* Modal de briefing */}
      <MissionBriefingModal
        visible={briefingMission !== null}
        title={briefingMission?.title ?? ''}
        loreBriefing={briefingMission?.lore_briefing ?? ''}
        pedagogicalObjective={briefingMission?.pedagogical_objective ?? ''}
        syntaxHint={briefingMission?.syntax_hint ?? ''}
        onInitialize={handleBriefingInitialize}
        onClose={() => setBriefingMission(null)}
      />

      {/* Transición de hackeo — z-[9999] cubre todo */}
      <HackingTransition isActive={isHacking} missionTitle={hackingTitle} />

      {/* ── Header ── */}
      <header className="relative z-20 shrink-0 flex items-center justify-between px-6 py-2.5 border-b border-[#00FF41]/12 bg-black/50 backdrop-blur-sm">
        <div className="flex items-center gap-4">
          <button
            onClick={() => router.push('/hub')}
            className="text-[#00FF41]/40 hover:text-[#00FF41]/80 text-xs tracking-widest transition-colors border border-[#00FF41]/15 px-2.5 py-1 hover:border-[#00FF41]/35 cursor-pointer"
          >
            ← VOLVER A DAKI
          </button>
          <span
            className="font-black tracking-widest text-sm hidden sm:block"
            style={{ textShadow: '0 0 8px #00FF41' }}
          >
            PYTHON QUEST
          </span>
        </div>
        <div className="flex items-center gap-5 text-xs text-[#00FF41]/50">
          <span className="text-[#00FF41]/30 hidden sm:block">{username}</span>
          <span>RANGO <strong className="text-[#00FF41]">{level}</strong></span>
          <span>XP <strong className="text-[#00FF41]">{totalXp.toLocaleString()}</strong></span>
          {streakDays > 0 && <span>🔥 <strong className="text-[#00FF41]">{streakDays}d</strong></span>}
        </div>
      </header>

      {/* ── Split screen ── */}
      <main className="relative z-20 flex-1 flex overflow-hidden gap-px">

        {/* ══════════════════════════════════════════
            COLUMNA IZQUIERDA — Lista de incursiones
        ══════════════════════════════════════════ */}
        <div
          className="w-[340px] shrink-0 flex flex-col overflow-hidden bg-black/40 backdrop-blur-md border-r border-green-500/20"
          style={{ boxShadow: '4px 0 30px rgba(0,255,65,0.06)' }}
        >

          {/* Cabecera columna */}
          <div className="shrink-0 px-5 py-4 border-b border-green-500/15 bg-black/30 backdrop-blur-sm">
            <h2 className="text-xs font-black tracking-[0.4em] text-[#00FF41]/70 mb-1 drop-shadow-[0_0_6px_rgba(0,255,65,0.5)]">
              SELECTOR DE INCURSIONES
            </h2>
            {/* Barra de progreso */}
            <div className="flex items-center gap-3 mt-2">
              <div className="flex-1 h-px bg-[#00FF41]/10 relative overflow-hidden">
                <motion.div
                  className="absolute left-0 top-0 h-full bg-[#00FF41]"
                  initial={{ width: 0 }}
                  animate={{ width: missions.length ? `${(completadas / missions.length) * 100}%` : '0%' }}
                  transition={{ duration: 1, ease: 'easeOut' }}
                  style={{ boxShadow: '0 0 6px #00FF41' }}
                />
              </div>
              <span className="text-[9px] tracking-widest text-[#00FF41]/30 shrink-0">
                {completadas}/{missions.length}
              </span>
            </div>
          </div>

          {/* Lista scrollable */}
          <div className="flex-1 overflow-y-auto py-2">
            {loading ? (
              <p className="text-[#00FF41]/25 text-[10px] tracking-widest animate-pulse px-5 py-6">
                CARGANDO INCURSIONES...
              </p>
            ) : fetchError ? (
              <p className="text-red-400/50 text-[10px] tracking-widest px-5 py-6">
                ERROR DE CONEXIÓN
              </p>
            ) : (
              <>
                {/* ── Banner: calibración requerida ── */}
                {!tutorialDone && (
                  <motion.div
                    className="mx-3 mb-2 mt-1 border border-cyan-500/35 bg-cyan-900/10 px-4 py-3"
                    initial={{ opacity: 0, y: -6 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.3 }}
                    style={{ boxShadow: '0 0 16px rgba(0,229,255,0.07), inset 0 0 12px rgba(0,229,255,0.04)' }}
                  >
                    <div className="flex items-center gap-2 mb-1">
                      <motion.span
                        className="w-1.5 h-1.5 rounded-full bg-cyan-400 shrink-0"
                        animate={{ opacity: [0.4, 1, 0.4] }}
                        transition={{ duration: 1.2, repeat: Infinity }}
                        style={{ boxShadow: '0 0 5px rgba(0,229,255,0.8)' }}
                      />
                      <span className="text-[9px] tracking-[0.45em] text-cyan-400/80 font-bold uppercase">
                        Calibración Sináptica Requerida
                      </span>
                    </div>
                    <p className="text-[10px] text-cyan-200/50 leading-relaxed">
                      Completa el Protocolo 00 para desbloquear las incursiones del Nexo.
                    </p>
                  </motion.div>
                )}

                {missions.map((m, idx) => {
                  const isLocked = !m.unlocked
                  const isSelected = selected?.id === m.id
                  const tierColor = TIER_COLOR[m.difficulty_tier]
                  const isAvailable = m.unlocked && !m.completed

                  const isTutorial = m.challenge_type === 'tutorial'
                  const tutorialSelectedBg = 'rgba(0,229,255,0.08)'
                  const tutorialHoverBg    = 'rgba(0,229,255,0.05)'

                  return (
                    <motion.button
                      key={m.id}
                      initial={{ opacity: 0, x: -12 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: idx * 0.06 }}
                      onClick={() => { if (!isLocked) setSelected(m) }}
                      disabled={isLocked}
                      className={[
                        'w-full text-left px-5 py-3.5 border-b transition-all duration-200 relative',
                        'border-l-4',
                        isLocked
                          ? 'opacity-40 grayscale cursor-not-allowed border-l-transparent border-b-green-500/5'
                          : isSelected
                          ? isTutorial
                            ? 'border-l-cyan-400 border-b-cyan-500/10 cursor-pointer'
                            : 'border-l-[#00FF41] border-b-green-500/10 cursor-pointer'
                          : isTutorial
                          ? 'border-l-cyan-700/60 border-b-cyan-500/8 cursor-pointer hover:translate-x-1'
                          : 'border-l-green-800/50 border-b-green-500/8 cursor-pointer hover:translate-x-1',
                      ].join(' ')}
                      style={
                        isSelected
                          ? {
                              background: isTutorial ? tutorialSelectedBg : 'rgba(0,255,65,0.08)',
                              boxShadow: isTutorial
                                ? 'inset 0 0 20px rgba(0,229,255,0.06), 0 0 10px rgba(0,229,255,0.05)'
                                : 'inset 0 0 20px rgba(0,255,65,0.06), 0 0 10px rgba(0,255,65,0.05)',
                            }
                          : {}
                      }
                      onMouseEnter={e => {
                        if (!isLocked && !isSelected) {
                          e.currentTarget.style.background = isTutorial ? tutorialHoverBg : 'rgba(0,255,65,0.05)'
                          e.currentTarget.style.boxShadow = isTutorial
                            ? 'inset 0 0 20px rgba(0,229,255,0.08)'
                            : 'inset 0 0 20px rgba(0,255,65,0.08)'
                          e.currentTarget.style.borderLeftColor = isTutorial ? 'rgba(0,229,255,0.6)' : 'rgba(0,255,65,0.5)'
                        }
                      }}
                      onMouseLeave={e => {
                        if (!isSelected) {
                          e.currentTarget.style.background = 'transparent'
                          e.currentTarget.style.boxShadow = 'none'
                          e.currentTarget.style.borderLeftColor = isLocked
                            ? 'transparent'
                            : isTutorial ? 'rgba(0,100,120,0.6)' : 'rgba(0,100,30,0.5)'
                        }
                      }}
                    >
                      {/* Badge tutorial */}
                      {isTutorial && (
                        <div className="flex items-center gap-1.5 mb-1.5">
                          <motion.span
                            className="w-1 h-1 rounded-full bg-cyan-400 shrink-0"
                            animate={{ opacity: [0.4, 1, 0.4] }}
                            transition={{ duration: 1.4, repeat: Infinity }}
                          />
                          <span className="text-[8px] tracking-[0.4em] text-cyan-400/70 font-bold uppercase">
                            Protocolo 00 · Obligatorio
                          </span>
                        </div>
                      )}

                      <div className="flex items-center justify-between gap-3">
                        <div className="flex items-center gap-3 min-w-0">
                          <span className={`text-[10px] w-4 shrink-0 tabular-nums ${isTutorial ? 'text-cyan-400/40' : 'text-[#00FF41]/25'}`}>
                            {String(m.level_order ?? idx + 1).padStart(2, '0')}
                          </span>
                          <span
                            className={[
                              'text-[11px] font-bold tracking-wide truncate',
                              isLocked
                                ? 'text-[#00FF41]/25'
                                : isSelected
                                ? isTutorial
                                  ? 'text-cyan-300 drop-shadow-[0_0_8px_rgba(0,229,255,0.8)]'
                                  : 'text-[#00FF41] drop-shadow-[0_0_8px_rgba(0,255,65,0.8)]'
                                : isTutorial
                                ? 'text-cyan-400/80'
                                : 'text-green-400',
                            ].join(' ')}
                          >
                            {m.title}
                          </span>
                        </div>
                        <div className="shrink-0 text-[9px] flex items-center gap-1.5">
                          {isLocked ? (
                            <span className="text-[#00FF41]/20">🔒</span>
                          ) : m.completed ? (
                            <span
                              style={isTutorial
                                ? { color: 'rgba(0,229,255,0.9)', textShadow: '0 0 6px rgba(0,229,255,0.7)' }
                                : { color: '#00FF41', textShadow: '0 0 6px #00FF41' }}
                            >✓</span>
                          ) : isAvailable ? (
                            <>
                              <span
                                className={`w-1.5 h-1.5 rounded-full animate-pulse shrink-0 ${isTutorial ? 'bg-cyan-400' : 'bg-green-500'}`}
                                style={{ boxShadow: isTutorial ? '0 0 4px rgba(0,229,255,0.8)' : '0 0 4px #00FF41' }}
                              />
                              <span style={{ color: isTutorial ? 'rgba(0,229,255,0.7)' : `${tierColor}70` }}>▶</span>
                            </>
                          ) : null}
                        </div>
                      </div>

                      {/* Fila inferior: dificultad + intentos */}
                      <div className="pl-7 mt-0.5 flex items-center gap-2">
                        <span
                          className="text-[8px] tracking-widest"
                          style={{ color: isTutorial ? 'rgba(0,229,255,0.35)' : `${tierColor}40` }}
                        >
                          {isTutorial ? 'CALIBRACIÓN' : TIER_LABEL[m.difficulty_tier]}
                        </span>
                        {m.attempts > 0 && !m.completed && (
                          <span className="text-[8px] text-green-200/30">
                            · {m.attempts} intento{m.attempts !== 1 ? 's' : ''}
                          </span>
                        )}
                      </div>
                    </motion.button>
                  )
                })}

                {/* ── Separadores especiales ── */}
                {!loading && (
                  <>
                    {/* JEFE FINAL */}
                    <div className="px-5 pt-5 pb-1">
                      <div className="flex items-center gap-2 mb-2">
                        <div className="h-px flex-1 bg-red-500/20" />
                        <span className="text-[8px] tracking-[0.4em] text-red-500/50">JEFE FINAL</span>
                        <div className="h-px flex-1 bg-red-500/20" />
                      </div>
                    </div>
                    <button
                      onClick={() => router.push('/boss')}
                      className="w-full text-left px-5 py-3.5 border-b border-l-4 border-l-red-700/60 border-b-red-500/10 transition-all duration-200 cursor-pointer hover:translate-x-1"
                      style={{ background: 'rgba(127,0,0,0.15)' }}
                      onMouseEnter={e => {
                        e.currentTarget.style.background = 'rgba(127,0,0,0.25)'
                        e.currentTarget.style.boxShadow = '0 0 30px rgba(255,0,0,0.15), inset 0 0 20px rgba(255,0,0,0.08)'
                        e.currentTarget.style.borderLeftColor = 'rgba(239,68,68,0.8)'
                      }}
                      onMouseLeave={e => {
                        e.currentTarget.style.background = 'rgba(127,0,0,0.15)'
                        e.currentTarget.style.boxShadow = 'none'
                        e.currentTarget.style.borderLeftColor = 'rgba(185,28,28,0.6)'
                      }}
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                          <motion.span
                            className="text-red-500/70 text-base"
                            animate={{ opacity: [0.5, 1, 0.5] }}
                            transition={{ duration: 1.8, repeat: Infinity }}
                          >
                            ∞
                          </motion.span>
                          <span className="text-[11px] font-bold tracking-wide text-red-400 drop-shadow-[0_0_8px_rgba(255,0,0,0.6)]">
                            THE INFINITE LOOPER
                          </span>
                        </div>
                        <span className="text-[8px] tracking-widest text-red-400/50 border border-red-500/30 px-1.5 py-0.5">
                          BOSS
                        </span>
                      </div>
                    </button>

                  </>
                )}
              </>
            )}
          </div>
        </div>

        {/* ══════════════════════════════════════════
            COLUMNA DERECHA — Panel de Briefing
        ══════════════════════════════════════════ */}
        <div
          className="flex-1 bg-black/40 backdrop-blur-md overflow-hidden"
          style={{ boxShadow: 'inset 4px 0 30px rgba(0,0,0,0.3)' }}
        >
          <BriefingPanel mission={selected} onDeploy={handleDeploy} />
        </div>

      </main>
    </div>
  )
}
