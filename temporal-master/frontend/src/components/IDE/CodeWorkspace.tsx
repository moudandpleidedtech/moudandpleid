'use client'

import dynamic from 'next/dynamic'
import { useState, useEffect, useRef, useMemo, useCallback } from 'react'
import { useRouter } from 'next/navigation'
import { motion, AnimatePresence, useAnimation } from 'framer-motion'
import { useUserStore } from '@/store/userStore'
import QuestTour from '@/components/Tutorial/QuestTour'
import ParticleBurst from '@/components/UI/ParticleBurst'
import ComboEffect from '@/components/UI/ComboEffect'
import Toast from '@/components/UI/Toast'
import MissionBriefing from '@/components/Game/MissionBriefing'

const MonacoEditor = dynamic(() => import('@monaco-editor/react'), { ssr: false })
const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000'

// ─── Tipos ────────────────────────────────────────────────────────────────────

interface Challenge {
  id: string
  title: string
  description: string
  difficulty_tier: number
  base_xp_reward: number
  initial_code: string
  test_inputs: string[]
  completed: boolean
  unlocked?: boolean
  theory_content?: string | null
}

interface ChallengeListItem {
  id: string
  title: string
  level_order: number | null
  challenge_type: string
  unlocked: boolean
}

interface ConsoleLine {
  text: string
  kind: 'stdout' | 'stderr' | 'info' | 'success' | 'enigma'
}

interface Props {
  challengeId: string
}

const TIER_LABEL: Record<number, string> = {
  1: 'INICIANTE',
  2: 'INTERMEDIO',
  3: 'AVANZADO',
}

const TIER_PAR_LINES: Record<number, number> = {
  1: 8,
  2: 14,
  3: 22,
}

const KEYWORD_GLOW: Record<string, string> = {
  def:    '#60A5FA',
  class:  '#60A5FA',
  for:    '#FBBF24',
  while:  '#FBBF24',
  if:     '#A78BFA',
  else:   '#A78BFA',
  elif:   '#A78BFA',
  return: '#34D399',
  range:  '#00FF41',
  import: '#F87171',
}

// ─── Sub-componentes ──────────────────────────────────────────────────────────

function NivelSubidoOverlay({ level }: { level: number }) {
  return (
    <motion.div className="fixed inset-0 z-50 flex items-center justify-center"
      initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
      transition={{ duration: 0.25 }}>
      <div className="absolute inset-0 bg-black/75" />
      <motion.div className="relative z-10 text-center select-none"
        initial={{ scale: 0.4, y: 50, opacity: 0 }} animate={{ scale: 1, y: 0, opacity: 1 }}
        exit={{ scale: 1.15, opacity: 0 }}
        transition={{ type: 'spring', stiffness: 280, damping: 22 }}>
        <div className="font-mono font-black tracking-[0.2em] text-7xl text-[#00FF41]"
          style={{ textShadow: '0 0 20px #00FF41, 0 0 60px #00FF4180' }}>
          NIVEL ARRIBA
        </div>
        <motion.div className="mt-3 font-mono text-3xl text-[#00FF41]/80 tracking-widest"
          initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.15 }}>
          NIVEL {level}
        </motion.div>
        <motion.div className="absolute inset-[-2rem] border border-[#00FF41]/30"
          animate={{ opacity: [0.3, 0.8, 0.3] }} transition={{ duration: 1, repeat: Infinity }} />
      </motion.div>
    </motion.div>
  )
}

// Puntos animados para el botón de ejecución
function AnimatedDots() {
  const [dots, setDots] = useState('.')
  useEffect(() => {
    const id = setInterval(() => setDots((d) => (d.length >= 3 ? '.' : d + '.')), 380)
    return () => clearInterval(id)
  }, [])
  return <span className="inline-block w-4 text-left">{dots}</span>
}

// Modal de victoria con dos botones diferenciados
interface VictoryNext { id: string; title: string; isDrone: boolean }

function VictoryModal({
  next,
  xpEarned,
  onNext,
  onReview,
}: {
  next: VictoryNext | null
  xpEarned: number
  onNext: () => void
  onReview: () => void
}) {
  return (
    <motion.div
      className="fixed inset-0 z-[80] flex items-center justify-center"
      initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
    >
      <div className="absolute inset-0 bg-black/80" onClick={onReview} />
      <motion.div
        className="relative z-10 w-full max-w-sm mx-4 p-7 bg-[#0A0A0A] border border-[#00FF41]/40 font-mono"
        style={{ boxShadow: '0 0 60px #00FF4118' }}
        initial={{ scale: 0.82, y: 28, opacity: 0 }}
        animate={{ scale: 1, y: 0, opacity: 1 }}
        transition={{ type: 'spring', stiffness: 300, damping: 26 }}
      >
        {/* Título */}
        <div className="text-center mb-5">
          <div
            className="text-[#00FF41] font-black text-2xl tracking-[0.2em] mb-1"
            style={{ textShadow: '0 0 20px #00FF41, 0 0 40px #00FF4160' }}
          >
            NODO COMPLETADO
          </div>
          <div className="text-[#00FF41]/35 text-[10px] tracking-[0.35em]">
            PROTOCOLO VERIFICADO · +{xpEarned} XP
          </div>
        </div>

        <div className="flex flex-col gap-3">
          {/* Botón primario — Siguiente Nodo */}
          <button
            onClick={onNext}
            className="w-full py-3 bg-[#00FF41] text-black font-black text-sm tracking-[0.2em] hover:bg-[#00FF41]/90 active:scale-[0.98] transition-all duration-100"
            style={{ boxShadow: '0 0 24px #00FF4155' }}
          >
            {next ? 'SIGUIENTE NODO →' : 'VOLVER A MISIONES →'}
          </button>
          {next && (
            <div className="text-center text-[9px] text-[#00FF41]/28 tracking-widest truncate px-2">
              {next.title}
            </div>
          )}

          {/* Botón secundario — Revisar código */}
          <button
            onClick={onReview}
            className="w-full py-2.5 text-[#00FF41]/55 text-xs font-bold tracking-[0.18em] border border-[#00FF41]/20 hover:border-[#00FF41]/50 hover:text-[#00FF41] transition-all duration-150"
          >
            REVISAR MI CÓDIGO
          </button>
        </div>
      </motion.div>
    </motion.div>
  )
}

// Overlay de error de red / timeout
function NetworkErrorFallback({ onRetry }: { onRetry: () => void }) {
  return (
    <motion.div
      className="absolute inset-0 z-[70] bg-[#0A0A0A]/97 flex flex-col items-center justify-center font-mono"
      initial={{ opacity: 0 }} animate={{ opacity: 1 }}
    >
      <motion.div
        className="text-center mb-8"
        animate={{ opacity: [0.55, 1, 0.55] }}
        transition={{ duration: 2.2, repeat: Infinity }}
      >
        <div
          className="text-red-400 font-black text-base tracking-[0.2em] mb-2"
          style={{ textShadow: '0 0 16px #FF444480' }}
        >
          CONEXIÓN CON ENIGMA PERDIDA
        </div>
        <div className="text-red-400/45 text-xs tracking-[0.35em]">
          REINTENTANDO PROTOCOLO...
        </div>
      </motion.div>
      <button
        onClick={onRetry}
        className="px-6 py-2.5 border border-red-500/40 text-red-400 text-xs tracking-[0.2em] hover:border-red-500/80 hover:text-red-300 transition-all duration-150"
      >
        REINTENTAR CONEXIÓN
      </button>
    </motion.div>
  )
}

// ─── Componente principal ─────────────────────────────────────────────────────

export default function CodeWorkspace({ challengeId }: Props) {
  const router = useRouter()
  const { userId, username, level, previousLevel, totalXp, streakDays, applyGamificationResult } =
    useUserStore()

  const [challenge, setChallenge]         = useState<Challenge | null>(null)
  const [allChallenges, setAllChallenges] = useState<ChallengeListItem[]>([])
  // 'briefing' → muestra teoría antes del editor; 'editor' → modo normal
  const [viewMode, setViewMode]           = useState<'briefing' | 'editor'>('editor')
  const [code, setCode]                   = useState('')
  const [output, setOutput]               = useState<ConsoleLine[]>([
    { text: '> Terminal lista.', kind: 'info' },
  ])
  const [isRunning, setIsRunning]         = useState(false)
  const [showNivelSubido, setShowNivelSubido] = useState(false)

  // Victory modal
  const [showVictory, setShowVictory]     = useState(false)
  const [victoryNext, setVictoryNext]     = useState<VictoryNext | null>(null)
  const [victoryXp, setVictoryXp]         = useState(0)

  // Network error fallback
  const [networkError, setNetworkError]   = useState(false)
  const lastCodeRef = useRef('')

  // Toast para nivel bloqueado
  const [toastMsg, setToastMsg]           = useState('')
  const [showToast, setShowToast]         = useState(false)

  // Juice states
  const [keywordFlash, setKeywordFlash]   = useState<string | null>(null)
  const [showParticles, setShowParticles] = useState(false)
  const [comboXp, setComboXp]             = useState(0)
  const [showCombo, setShowCombo]         = useState(false)

  const kwFlashRef = useRef<ReturnType<typeof setTimeout>>()
  const shakeCtrl  = useAnimation()
  const consoleRef = useRef<HTMLDivElement>(null)

  const [failStreak, setFailStreak]       = useState(0)
  const [loadingHint, setLoadingHint]     = useState(false)

  useEffect(() => { if (!userId) router.replace('/') }, [userId, router])

  // Carga la lista completa de misiones para detectar el siguiente nodo
  useEffect(() => {
    if (!userId) return
    fetch(`${API_BASE}/api/v1/challenges?user_id=${userId}`)
      .then((r) => r.json())
      .then((data: ChallengeListItem[]) => setAllChallenges(data))
      .catch(() => {})
  }, [userId])

  // Carga el reto actual
  useEffect(() => {
    if (!userId) return
    fetch(`${API_BASE}/api/v1/challenges/${challengeId}?user_id=${userId}`)
      .then((r) => r.json())
      .then((data: Challenge) => {
        // Reto bloqueado → toast + redirección
        if (data.unlocked === false) {
          setToastMsg('ACCESO DENEGADO: Secuencia de aprendizaje no completada')
          setShowToast(true)
          setTimeout(() => router.replace('/misiones'), 2200)
          return
        }
        setChallenge(data)
        if (data.initial_code) setCode(data.initial_code)
        // Si hay contenido teórico, mostrar briefing antes del editor
        if (data.theory_content) setViewMode('briefing')
      })
      .catch(() => {})
  }, [challengeId, userId, router])

  useEffect(() => {
    if (level > previousLevel) {
      setShowNivelSubido(true)
      const t = setTimeout(() => setShowNivelSubido(false), 2800)
      return () => clearTimeout(t)
    }
  }, [level, previousLevel])

  // Par de líneas del reto actual
  const parLines = useMemo(() => {
    if (!challenge) return 15
    return TIER_PAR_LINES[challenge.difficulty_tier] ?? 14
  }, [challenge])

  const countEffectiveLines = useCallback(
    (src: string): number =>
      src.split('\n').filter((l) => l.trim() && !l.trim().startsWith('#')).length,
    []
  )

  // Screen shake
  const triggerShake = useCallback(
    async (intensity: 'soft' | 'hard' = 'soft') => {
      if (intensity === 'hard') {
        await shakeCtrl.start({
          x: [0, -14, 14, -10, 10, -6, 6, -2, 2, 0],
          transition: { duration: 0.5, ease: 'easeInOut' },
        })
      } else {
        await shakeCtrl.start({
          x: [0, -5, 5, -3, 3, -1, 1, 0],
          transition: { duration: 0.28, ease: 'easeInOut' },
        })
      }
      shakeCtrl.set({ x: 0 })
    },
    [shakeCtrl]
  )

  // Keyword glow
  const handleCodeChange = useCallback((val: string) => {
    setCode(val ?? '')
    const lastLine = (val ?? '').split('\n').pop() ?? ''
    const lastToken =
      lastLine
        .split(/[\s()\[\]{},.:=+\-*/!<>&|]+/)
        .filter(Boolean)
        .pop() ?? ''
    if (KEYWORD_GLOW[lastToken]) {
      clearTimeout(kwFlashRef.current)
      setKeywordFlash(lastToken)
      kwFlashRef.current = setTimeout(() => setKeywordFlash(null), 700)
    }
  }, [])

  const scrollConsole = () =>
    setTimeout(() => consoleRef.current?.scrollTo(0, consoleRef.current.scrollHeight), 60)

  // Detecta el siguiente nodo en la lista ordenada
  const findNextChallenge = useCallback(
    (currentId: string): VictoryNext | null => {
      const idx = allChallenges.findIndex((c) => c.id === currentId)
      if (idx === -1 || idx >= allChallenges.length - 1) return null
      const next = allChallenges[idx + 1]
      return { id: next.id, title: next.title, isDrone: next.challenge_type === 'drone' }
    },
    [allChallenges]
  )

  // Pista ENIGMA
  const requestHint = async (currentOutput: ConsoleLine[]) => {
    if (loadingHint || !challenge) return
    setLoadingHint(true)
    const errorText = currentOutput
      .filter((l) => l.kind === 'stderr' || l.kind === 'info')
      .map((l) => l.text)
      .join('\n')
    try {
      const res = await fetch(`${API_BASE}/api/v1/hint`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId, challenge_id: challengeId,
          source_code: code, error_output: errorText,
        }),
      })
      const data = await res.json()
      if (data.hint) {
        setOutput((prev) => {
          const next = [
            ...prev,
            { text: '', kind: 'enigma' as const },
            { text: '[ENIGMA] Transmision entrante...', kind: 'enigma' as const },
            ...data.hint.split('\n').map((line: string) => ({
              text: `[ENIGMA] ${line}`, kind: 'enigma' as const,
            })),
          ]
          scrollConsole()
          return next
        })
      }
    } catch { /* fallo silencioso */ }
    finally { setLoadingHint(false) }
  }

  // Ejecutar código con timeout y manejo de error de red
  const handleEjecutar = useCallback(async () => {
    if (!code.trim() || isRunning) return
    setIsRunning(true)
    setNetworkError(false)
    setOutput([{ text: '> Compilando...', kind: 'info' }])
    lastCodeRef.current = code

    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), 12_000)

    try {
      const res = await fetch(`${API_BASE}/api/v1/execute`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId, challenge_id: challengeId,
          source_code: code, test_inputs: challenge?.test_inputs ?? [],
        }),
        signal: controller.signal,
      })

      if (!res.ok) {
        const err = await res.json()
        triggerShake('soft')
        setOutput([{ text: `[ERROR] ${err.detail ?? res.statusText}`, kind: 'stderr' }])
        return
      }

      const data = await res.json()
      const lines: ConsoleLine[] = []

      if (data.stdout) lines.push({ text: data.stdout, kind: 'stdout' })
      if (data.stderr) lines.push({ text: data.stderr, kind: 'stderr' })

      lines.push({
        text: `${data.execution_time_ms.toFixed(1)}ms  |  ${
          data.output_matched ? 'Salida correcta ✓' : 'Salida incorrecta ✗'
        }`,
        kind: data.output_matched ? 'success' : 'info',
      })

      if (data.gamification.xp_earned > 0) {
        lines.push({
          text: `+${data.gamification.xp_earned} XP${
            data.gamification.efficiency_bonus_applied ? '  · Bono por velocidad!' : ''
          }`,
          kind: 'success',
        })
      }

      if (data.gamification.already_completed) {
        lines.push({ text: '(Mision ya completada — sin XP adicional)', kind: 'info' })
      }

      setOutput(lines)
      scrollConsole()

      applyGamificationResult({
        new_level: data.gamification.new_level,
        new_total_xp: data.gamification.new_total_xp,
      })

      if (data.output_matched && !data.gamification.already_completed) {
        triggerShake('soft')
        setShowParticles(true)
        setTimeout(() => setShowParticles(false), 1400)

        // Combo de eficiencia
        const effectiveLines = countEffectiveLines(code)
        if (effectiveLines <= parLines && data.gamification.xp_earned > 0) {
          setComboXp(data.gamification.xp_earned)
          setTimeout(() => setShowCombo(true), 320)
        }

        // Modal de victoria
        const next = findNextChallenge(challengeId)
        setVictoryNext(next)
        setVictoryXp(data.gamification.xp_earned)
        setTimeout(() => setShowVictory(true), 700)
      } else if (!data.output_matched) {
        triggerShake('soft')
      }

      if (!data.output_matched) {
        const newStreak = failStreak + 1
        setFailStreak(newStreak)
        if (newStreak >= 3) {
          setFailStreak(0)
          setTimeout(() => requestHint(lines), 800)
        }
      } else {
        setFailStreak(0)
      }
    } catch (e) {
      const isAbort = e instanceof DOMException && e.name === 'AbortError'
      if (isAbort) {
        setNetworkError(true)
      } else {
        setOutput([{ text: `[RED] ${String(e)}`, kind: 'stderr' }])
      }
    } finally {
      clearTimeout(timeoutId)
      setIsRunning(false)
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [code, isRunning, userId, challengeId, challenge, failStreak, parLines,
      triggerShake, countEffectiveLines, findNextChallenge, applyGamificationResult])

  // Navegar al siguiente nodo desde el modal de victoria
  const handleNextChallenge = useCallback(() => {
    setShowVictory(false)
    if (!victoryNext) {
      router.push('/misiones')
      return
    }
    if (victoryNext.isDrone) {
      router.push('/enigma')
    } else {
      router.push(`/challenge/${victoryNext.id}`)
    }
  }, [victoryNext, router])

  // Editor glow
  const editorGlow = keywordFlash ? KEYWORD_GLOW[keywordFlash] : null
  const editorStyle = editorGlow
    ? { boxShadow: `0 0 0 1px ${editorGlow}50, inset 0 0 24px ${editorGlow}15`, transition: 'box-shadow 0.1s ease-out' }
    : { transition: 'box-shadow 0.4s ease-out' }

  return (
    <>
      <QuestTour />
      <ParticleBurst visible={showParticles} />
      <ComboEffect visible={showCombo} xpEarned={comboXp} onDone={() => setShowCombo(false)} />
      <Toast
        message={toastMsg}
        visible={showToast}
        onClose={() => setShowToast(false)}
        variant="warning"
      />

      <AnimatePresence>
        {showNivelSubido && <NivelSubidoOverlay level={level} />}
      </AnimatePresence>

      <AnimatePresence>
        {showVictory && (
          <VictoryModal
            next={victoryNext}
            xpEarned={victoryXp}
            onNext={handleNextChallenge}
            onReview={() => setShowVictory(false)}
          />
        )}
      </AnimatePresence>

      {/* Layout con screen shake */}
      <motion.div
        animate={shakeCtrl}
        className="relative flex flex-col h-[calc(100vh-2rem)] bg-[#0A0A0A] text-[#00FF41] font-mono overflow-hidden"
      >
        {/* Error de red: overlay sobre todo */}
        <AnimatePresence>
          {networkError && (
            <NetworkErrorFallback
              onRetry={() => {
                setNetworkError(false)
                handleEjecutar()
              }}
            />
          )}
        </AnimatePresence>

        {/* Barra de estado */}
        <header className="flex items-center justify-between px-4 py-1.5 bg-[#0D0D0D] border-b border-[#00FF41]/20 text-xs shrink-0">
          <div className="flex items-center gap-3">
            <button onClick={() => router.push('/misiones')}
              className="text-[#00FF41]/40 hover:text-[#00FF41] transition-colors tracking-widest">
              MISIONES
            </button>
            <span className="text-[#00FF41]/20">|</span>
            <span className="font-bold tracking-widest text-[#00FF41]"
              style={{ textShadow: '0 0 8px #00FF41' }}>
              PYTHON QUEST
            </span>
          </div>
          <div className="flex items-center gap-5 text-[#00FF41]/70">
            <span className="text-[#00FF41]/40">{username}</span>
            <span>NVL <strong className="text-[#00FF41]">{level}</strong></span>
            <span id="xp-display">XP <strong className="text-[#00FF41]">{totalXp.toLocaleString()}</strong></span>
            {streakDays > 0 && (
              <span>RACHA <strong className="text-[#00FF41]">{streakDays}d</strong></span>
            )}
            {failStreak >= 2 && !loadingHint && (
              <motion.span
                initial={{ opacity: 0 }} animate={{ opacity: [0.5, 1, 0.5] }}
                transition={{ duration: 1.2, repeat: Infinity }}
                className="text-[#FFB800] text-xs tracking-widest cursor-pointer"
                onClick={() => requestHint(output)}
                title="Solicitar pista de ENIGMA"
              >
                ENIGMA?
              </motion.span>
            )}
          </div>
        </header>

        {/* Briefing — se muestra antes del editor si hay theory_content */}
        <AnimatePresence mode="wait">
          {viewMode === 'briefing' && challenge?.theory_content && (
            <motion.div
              key="briefing-wrapper"
              className="flex-1 overflow-hidden"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              <MissionBriefing
                title={challenge.title}
                theoryContent={challenge.theory_content}
                challengeId={challenge.id}
                onInitialize={() => setViewMode('editor')}
              />
            </motion.div>
          )}
        </AnimatePresence>

        {/* Layout principal — editor + consola */}
        <div className={`flex flex-1 overflow-hidden transition-all ${viewMode === 'briefing' ? 'hidden' : ''}`}>

          {/* Editor */}
          <div id="code-editor-panel" className="flex-1 flex flex-col min-w-0">
            <div className="flex items-center justify-between px-4 py-2 border-b border-[#00FF41]/10 bg-[#0D0D0D] shrink-0">
              <div className="flex items-center gap-2">
                <span className="text-[#00FF41]/40 text-xs tracking-widest">editor · python</span>
                <AnimatePresence>
                  {keywordFlash && (
                    <motion.span
                      key={keywordFlash}
                      className="text-[10px] font-mono font-bold px-1.5 py-0.5 tracking-widest"
                      style={{
                        color: KEYWORD_GLOW[keywordFlash],
                        border: `1px solid ${KEYWORD_GLOW[keywordFlash]}60`,
                        boxShadow: `0 0 8px ${KEYWORD_GLOW[keywordFlash]}40`,
                      }}
                      initial={{ opacity: 0, x: -8, scale: 0.8 }}
                      animate={{ opacity: 1, x: 0, scale: 1 }}
                      exit={{ opacity: 0, scale: 0.7 }}
                      transition={{ duration: 0.14 }}
                    >
                      {keywordFlash}
                    </motion.span>
                  )}
                </AnimatePresence>
              </div>

              {/* Botón ejecutar — deshabilitado y con texto animado durante compilación */}
              <button
                id="execute-button"
                onClick={handleEjecutar}
                disabled={isRunning}
                className="flex items-center gap-1 px-5 py-1 bg-[#00FF41] text-black text-xs font-black tracking-widest hover:bg-[#00FF41]/85 active:scale-95 disabled:opacity-40 disabled:cursor-not-allowed transition-all duration-100"
              >
                {isRunning ? (
                  <>COMPILANDO RED NEURAL<AnimatedDots /></>
                ) : (
                  'EJECUTAR'
                )}
              </button>
            </div>

            <div className="flex-1 overflow-hidden" style={editorStyle}>
              <MonacoEditor
                height="100%"
                language="python"
                theme="vs-dark"
                value={code}
                onChange={(val) => handleCodeChange(val ?? '')}
                options={{
                  minimap: { enabled: false },
                  fontSize: 14,
                  fontFamily: '"Fira Code", "Cascadia Code", Consolas, monospace',
                  lineHeight: 22,
                  padding: { top: 16, bottom: 16 },
                  scrollBeyondLastLine: false,
                  renderLineHighlight: 'line',
                  cursorBlinking: 'phase',
                  smoothScrolling: true,
                }}
              />
            </div>
          </div>

          {/* Panel derecho */}
          <div className="w-80 flex flex-col border-l border-[#00FF41]/20 bg-[#0D0D0D] shrink-0">

            {/* Descripción del reto */}
            <div className="flex-1 flex flex-col overflow-hidden border-b border-[#00FF41]/20">
              <div className="px-3 py-2 text-[#00FF41]/40 text-xs tracking-widest uppercase border-b border-[#00FF41]/10 shrink-0">
                mision
              </div>
              <div className="flex-1 overflow-y-auto p-3 leading-relaxed">
                {challenge ? (
                  <>
                    <h2 className="text-[#00FF41] font-bold text-sm mb-1 leading-snug">
                      {challenge.title}
                    </h2>
                    <div className="text-[#00FF41]/40 text-xs mb-3 tracking-widest">
                      {TIER_LABEL[challenge.difficulty_tier]} · {challenge.base_xp_reward} XP
                      {challenge.completed && (
                        <span className="ml-2 text-[#00FF41]">· Completada</span>
                      )}
                    </div>
                    <p className="text-xs leading-5 text-[#00FF41]/70 whitespace-pre-wrap">
                      {challenge.description}
                    </p>
                    <div className="mt-3 pt-3 border-t border-[#00FF41]/10 text-[10px] text-[#00FF41]/25 tracking-widest">
                      PAR: {parLines} líneas · combo si usas ≤{parLines}
                    </div>
                  </>
                ) : (
                  <p className="text-[#00FF41]/25 text-xs animate-pulse">Cargando mision...</p>
                )}
              </div>
            </div>

            {/* Consola */}
            <div className="flex-1 flex flex-col overflow-hidden">
              <div className="flex items-center justify-between px-3 py-2 border-b border-[#00FF41]/10 shrink-0">
                <span className="text-[#00FF41]/40 text-xs tracking-widest uppercase">consola</span>
                {loadingHint && (
                  <span className="text-[#FFB800]/60 text-xs animate-pulse tracking-widest">
                    ENIGMA...
                  </span>
                )}
              </div>
              <div ref={consoleRef} className="flex-1 overflow-y-auto p-3 space-y-0.5">
                {output.map((line, i) => (
                  <div key={i}
                    className={`text-xs leading-5 whitespace-pre-wrap break-all ${
                      line.kind === 'stderr'   ? 'text-red-400'
                      : line.kind === 'success' ? 'text-[#00FF41]'
                      : line.kind === 'enigma'  ? 'enigma-line'
                      : line.kind === 'info'    ? 'text-[#00FF41]/45'
                      : 'text-[#00FF41]/85'
                    }`}>
                    {line.text}
                  </div>
                ))}
              </div>
            </div>

          </div>
        </div>
      </motion.div>
    </>
  )
}
