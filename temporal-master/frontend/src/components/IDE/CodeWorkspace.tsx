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
import VictoryModal, { type VictoryNext } from '@/components/UI/VictoryModal'
import DakiHint from '@/components/IDE/DakiHint'
import TutorialPanel from '@/components/IDE/TutorialPanel'
import DakiWaveform from '@/components/UI/DakiWaveform'
import DakiTerminalLine from '@/components/IDE/DakiTerminalLine'
import PaywallModal from '@/components/UI/PaywallModal'
import AchievementToast, { type Achievement } from '@/components/UI/AchievementToast'
import InsightFlash from '@/components/UI/InsightFlash'
import { useDakiVoice } from '@/hooks/useDakiVoice'
import { useIdleDetection } from '@/hooks/useIdleDetection'

const MonacoEditor = dynamic(() => import('@monaco-editor/react'), { ssr: false })
const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? ''

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
  lore_briefing?: string | null
  level_order?: number | null
  challenge_type?: string
  hints?: string[]
  is_free?: boolean
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
  kind: 'stdout' | 'stderr' | 'info' | 'success' | 'enigma' | 'intervention' | 'daki-cli'
}

interface ErrorInfo {
  error_type: string
  line: number | null
  detail: string
}

interface Props {
  challengeId: string
}

// ─── Background por nivel ─────────────────────────────────────────────────────

const LEVEL_BACKGROUNDS: Record<number, string> = {
  1: '/assets/backgrounds/map1.png',
  2: '/assets/backgrounds/map2.png',
  3: '/assets/backgrounds/map3.png',
  4: '/assets/backgrounds/map4.png',
  5: '/assets/backgrounds/map5.png',
}

function getMissionBackground(levelOrder: number | null | undefined): string {
  if (levelOrder && LEVEL_BACKGROUNDS[levelOrder]) {
    return LEVEL_BACKGROUNDS[levelOrder]
  }
  return LEVEL_BACKGROUNDS[1]
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

// ─── Código por fase del tutorial ────────────────────────────────────────────

const TUTORIAL_STEP_CODES: Record<number, string> = {
  1: 'print("Iniciando enlace neuronal...")\n',
  2: 'print("Estabilizando pulso...)\n',
  3: '# Escribe tu código debajo:\n',
  4: 'def finalizar_enlace():\n    print("Enlace Listo")\n\nprint(finalizar_enlace())\n',
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
    <motion.div
      className="fixed inset-0 z-[9900] flex items-center justify-center overflow-hidden"
      initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
      transition={{ duration: 0.3 }}
    >
      {/* Dramatic dark overlay with green radial glow */}
      <div className="absolute inset-0" style={{
        background: 'radial-gradient(ellipse at center, rgba(0,25,10,0.97) 0%, rgba(0,0,0,0.99) 65%)',
      }} />

      {/* Animated scan beam */}
      <div
        className="absolute inset-x-0 h-0.5 pointer-events-none level-up-scan-beam"
        style={{
          background: 'linear-gradient(90deg, transparent, #00FF41, rgba(0,255,65,0.6), #00FF41, transparent)',
          boxShadow: '0 0 24px #00FF41, 0 0 48px #00FF4180',
        }}
      />

      {/* Subtle grid */}
      <div className="absolute inset-0 opacity-[0.035] pointer-events-none" style={{
        backgroundImage: 'linear-gradient(rgba(0,255,65,0.8) 1px, transparent 1px), linear-gradient(90deg,rgba(0,255,65,0.8) 1px,transparent 1px)',
        backgroundSize: '60px 60px',
      }} />

      {/* Content */}
      <motion.div
        className="relative z-10 text-center select-none px-10"
        initial={{ scale: 0.3, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 1.08, opacity: 0 }}
        transition={{ type: 'spring', stiffness: 260, damping: 22 }}
      >
        {/* Outer pulsing ring */}
        <motion.div
          className="absolute inset-[-5rem] rounded-full border border-[#00FF41]/15 pointer-events-none"
          animate={{ scale: [1, 1.07, 1], opacity: [0.3, 0.7, 0.3] }}
          transition={{ duration: 1.8, repeat: Infinity }}
        />
        {/* Inner pulsing ring */}
        <motion.div
          className="absolute inset-[-2.5rem] rounded-full border border-[#00FF41]/30 pointer-events-none"
          animate={{ scale: [1, 1.04, 1], opacity: [0.5, 1, 0.5] }}
          transition={{ duration: 1.3, repeat: Infinity, delay: 0.2 }}
        />

        {/* Top label */}
        <motion.div
          className="text-[#00FF41]/50 text-[10px] tracking-[0.7em] uppercase mb-5"
          initial={{ opacity: 0, y: -12 }} animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.08 }}
        >
          // NEXO — PROTOCOLO DE ASCENSO //
        </motion.div>

        {/* Main title */}
        <div
          className="font-mono font-black leading-none"
          style={{
            fontSize: 'clamp(2.8rem, 7vw, 5.5rem)',
            letterSpacing: '0.12em',
            color: '#00FF41',
            textShadow: '0 0 30px #00FF41, 0 0 70px #00FF4170, 0 0 120px #00FF4130',
          }}
        >
          RANGO
        </div>
        <div
          className="font-mono font-black leading-none"
          style={{
            fontSize: 'clamp(2.8rem, 7vw, 5.5rem)',
            letterSpacing: '0.12em',
            color: '#00FF41',
            textShadow: '0 0 30px #00FF41, 0 0 70px #00FF4170, 0 0 120px #00FF4130',
          }}
        >
          ASCENDIDO
        </div>

        {/* Level number — outline style */}
        <motion.div
          className="mt-5 font-mono font-black tracking-[0.35em]"
          style={{
            fontSize: 'clamp(2rem, 5vw, 3.5rem)',
            color: 'transparent',
            WebkitTextStroke: '2px #00FF41',
            textShadow: '0 0 40px #00FF4190',
          }}
          initial={{ opacity: 0, scale: 0.6 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.22, type: 'spring', stiffness: 300, damping: 20 }}
        >
          [{level.toString().padStart(2, '0')}]
        </motion.div>

        {/* Separator */}
        <motion.div
          className="flex items-center gap-3 justify-center mt-5"
          initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.38 }}
        >
          <div className="h-px w-20" style={{ background: 'linear-gradient(90deg, transparent, #00FF41)' }} />
          <span className="text-[#00FF41]/45 text-[9px] tracking-[0.55em]">ACCESO AMPLIADO</span>
          <div className="h-px w-20" style={{ background: 'linear-gradient(90deg, #00FF41, transparent)' }} />
        </motion.div>
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
          CONEXIÓN CON DAKI PERDIDA
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

// ─── Intel Drawer: renderiza theory_content con formato cyberpunk mínimo ──────

function TheoryRenderer({ text }: { text: string }) {
  const lines = text.split('\n')
  return (
    <div className="space-y-0.5">
      {lines.map((line, i) => {
        if (line.startsWith('# '))
          return (
            <div key={i} className="text-[#00FF41] font-black text-xs tracking-[0.2em] uppercase mt-5 mb-1"
              style={{ textShadow: '0 0 10px rgba(0,255,65,0.4)' }}>
              {line.slice(2)}
            </div>
          )
        if (line.startsWith('## '))
          return (
            <div key={i} className="text-[#00FF41]/80 font-bold text-[11px] tracking-[0.15em] uppercase mt-3 mb-0.5">
              {line.slice(3)}
            </div>
          )
        if (line.startsWith('```') || line === '```')
          return null
        if (!line.trim())
          return <div key={i} className="h-2" />

        // inline: `code` and **bold**
        const parts = line.split(/(`[^`]+`|\*\*[^*]+\*\*)/)
        if (parts.length > 1) {
          return (
            <div key={i} className="text-[#00FF41]/65 text-[11px] leading-6">
              {parts.map((p, j) => {
                if (p.startsWith('`') && p.endsWith('`'))
                  return <code key={j} className="text-[#00FF41] bg-[#00FF41]/10 px-1 rounded text-[10px] font-mono">{p.slice(1, -1)}</code>
                if (p.startsWith('**') && p.endsWith('**'))
                  return <strong key={j} className="text-[#00FF41]/90 font-bold">{p.slice(2, -2)}</strong>
                return <span key={j}>{p}</span>
              })}
            </div>
          )
        }
        return <div key={i} className="text-[#00FF41]/65 text-[11px] leading-6">{line}</div>
      })}
    </div>
  )
}


// ─── Componente principal ─────────────────────────────────────────────────────

export default function CodeWorkspace({ challengeId }: Props) {
  const router = useRouter()
  const {
    userId, username, level, previousLevel, totalXp, streakDays,
    completedChallengeIds, applyGamificationResult, markChallengeCompleted,
    dakiLevel, isPaid, setIsPaid,
  } = useUserStore()

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

  // Game feel states
  const [editorAnim, setEditorAnim] = useState<'anim-shake' | 'anim-victory-glow' | 'anim-error-flash' | ''>('')
  const triggerEditorAnim = (cls: 'anim-shake' | 'anim-victory-glow' | 'anim-error-flash', ms = 500) => {
    setEditorAnim(cls)
    setTimeout(() => setEditorAnim(''), ms)
  }

  // Terminal (right panel) flash — mismo juego de clases, panel separado
  const [terminalAnim, setTerminalAnim] = useState<'anim-victory-glow' | 'anim-error-flash' | ''>('')
  const triggerTerminalAnim = (cls: 'anim-victory-glow' | 'anim-error-flash', ms = 600) => {
    setTerminalAnim(cls)
    setTimeout(() => setTerminalAnim(''), ms)
  }

  // Waveform: true mientras DAKI "habla" (~duración estimada del mensaje)
  const [waveformActive, setWaveformActive] = useState(false)

  // Gaming experience
  const [ambientOn,    setAmbientOn]    = useState(false)
  const [soundEnabled, setSoundEnabled] = useState(true)
  const [sessionSecs,  setSessionSecs]  = useState(0)
  const [focusMode,    setFocusMode]    = useState(false)
  const waveformTimerRef = useRef<ReturnType<typeof setTimeout>>()

  const activateWaveform = useCallback((msg: string) => {
    if (waveformTimerRef.current) clearTimeout(waveformTimerRef.current)
    setWaveformActive(true)
    // ~40ms por carácter (ritmo de TTS), mínimo 2s, máximo 8s
    const duration = Math.min(Math.max(msg.length * 40, 2000), 8000)
    waveformTimerRef.current = setTimeout(() => setWaveformActive(false), duration)
  }, [])

  // Paywall modal: se muestra si el backend devuelve 402
  const [showPaywall, setShowPaywall] = useState(false)

  // ── Intel Drawer (Fase 1) ─────────────────────────────────────────────────
  const [showIntelDrawer, setShowIntelDrawer] = useState(false)

  // ── DAKI CLI (Fase 2) ─────────────────────────────────────────────────────
  const [cliInput, setCliInput]   = useState('')
  const [cliLoading, setCliLoading] = useState(false)

  // Intervención proactiva — último error para contexto (Prompt 57)
  const lastErrorRef = useRef('')

  // Toast para nivel bloqueado
  const [toastMsg, setToastMsg]           = useState('')
  const [showToast, setShowToast]         = useState(false)

  // Juice states
  const [keywordFlash, setKeywordFlash]   = useState<string | null>(null)
  const [showParticles, setShowParticles] = useState(false)
  const [comboXp, setComboXp]             = useState(0)
  const [showCombo, setShowCombo]         = useState(false)

  const kwFlashRef       = useRef<ReturnType<typeof setTimeout>>()
  const shakeCtrl        = useAnimation()
  const consoleRef       = useRef<HTMLDivElement>(null)
  const codeDraftRef     = useRef<ReturnType<typeof setTimeout>>()  // debounce para localStorage
  const challengeStartMs = useRef<number>(Date.now())               // para telemetría time_spent
  const editorRef        = useRef<any>(null)                        // instancia Monaco editor
  const decorationsRef   = useRef<any>(null)                        // IEditorDecorationsCollection
  const handleEjecutarRef = useRef<() => void>(() => {})            // stable ref for Ctrl+Enter
  const audioVictoryRef  = useRef<HTMLAudioElement | null>(null)
  const audioRunRef      = useRef<HTMLAudioElement | null>(null)
  const audioHintRef     = useRef<HTMLAudioElement | null>(null)
  const audioAmbientRef  = useRef<HTMLAudioElement | null>(null)

  const [failStreak, setFailStreak]       = useState(0)
  const [loadingHint, setLoadingHint]     = useState(false)
  const [hintIndex, setHintIndex]         = useState(-1)   // -1 = oculto, 0/1/2 = pista visible
  const [dakiMessage, setDakiMessage]     = useState('')   // frase narrativa de DAKI Intel
  const [activeAchievements, setActiveAchievements] = useState<Achievement[]>([])
  const [activeInsight, setActiveInsight] = useState<string | null>(null)

  // Voz de DAKI Intel — habla automáticamente cuando dakiMessage cambia
  const { speak: speakDaki } = useDakiVoice(dakiLevel, { enabled: true })

  // Tutorial multi-step
  const [tutorialStep, setTutorialStep]   = useState(1)
  const [syncProgress, setSyncProgress]   = useState(0)
  const [tutorialFlash, setTutorialFlash] = useState(false)

  // Guardia de hidratación: esperar a que Zustand lea localStorage antes de evaluar userId
  const [hydrated, setHydrated] = useState(false)
  useEffect(() => { setHydrated(true) }, [])

  useEffect(() => {
    if (!hydrated) return
    if (!userId) router.replace('/')
  }, [hydrated, userId, router])

  // ─── Intervención proactiva (Prompt 57) ─────────────────────────────────────
  // useIdleDetection monitorea inactividad *semántica*: ausencia de cambios de código
  // o envíos de solución (no mouse/keyboard genérico). resetTimer() se llama desde
  // handleCodeChange y al inicio de handleEjecutar.
  const handleStuck = useCallback(async () => {
    if (!challenge || !userId) return
    try {
      const res = await fetch(`${API_BASE}/api/v1/daki/intervene`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId,
          challenge_id: challengeId,
          current_code: code,
          error_output: lastErrorRef.current,
          idle_minutes: 2,
          operator_level: level ?? 1,
        }),
      })
      if (!res.ok) return
      const data = await res.json()
      const msg: string = data.daki_message ?? ''
      if (!msg) return

      // Forzar vista de editor para que el terminal sea visible
      setViewMode('editor')

      // Inyectar en terminal como líneas de intervención prominentes
      setOutput((prev) => [
        ...prev,
        { text: '━━━ DAKI INTERRUPT ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━', kind: 'intervention' as const },
        ...msg.split('\n').filter(Boolean).map((line) => ({
          text: `  ${line}`, kind: 'intervention' as const,
        })),
        { text: '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━', kind: 'intervention' as const },
      ])
      scrollConsole()
      speakDaki(msg)
      activateWaveform(msg)
    } catch { /* silencioso */ }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [challenge, userId, challengeId, code, speakDaki, activateWaveform])

  const { resetTimer: resetIdleTimer } = useIdleDetection({
    timeoutMs: 2 * 60 * 1000,
    onStuck: handleStuck,
    enabled: hydrated && !!userId && !!challengeId,
  })

  // ── Initialize audio (client-only) ───────────────────────────────────────
  useEffect(() => {
    audioVictoryRef.current = new Audio('/sounds/victory.mp3')
    audioRunRef.current     = new Audio('/sounds/data-stream.mp3')
    audioRunRef.current.volume  = 0.4
    audioHintRef.current    = new Audio('/sounds/daki_alert.mp3')
    audioAmbientRef.current = new Audio('/sounds/hub-ambient.mp3')
    audioAmbientRef.current.loop   = true
    audioAmbientRef.current.volume = 0.12
    return () => { audioAmbientRef.current?.pause() }
  }, [])

  // ── Ambient music toggle ──────────────────────────────────────────────────
  useEffect(() => {
    if (ambientOn) { audioAmbientRef.current?.play().catch(() => {}) }
    else           { audioAmbientRef.current?.pause() }
  }, [ambientOn])

  // ── Session HUD timer — resets on each new challenge ─────────────────────
  useEffect(() => {
    setSessionSecs(0)
    const id = setInterval(() => {
      setSessionSecs(Math.floor((Date.now() - challengeStartMs.current) / 1000))
    }, 1000)
    return () => clearInterval(id)
  }, [challengeId])

  // ── Focus mode: Escape key exits ──────────────────────────────────────────
  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === 'Escape') setFocusMode(false) }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [])

  // ── DAKI CLI: envía la pregunta del Operador y muestra respuesta en terminal ─
  const handleDakiAsk = useCallback(async () => {
    const q = cliInput.trim()
    if (!q || cliLoading || !userId || !challengeId) return
    setCliInput('')
    setCliLoading(true)

    setOutput((prev) => [
      ...prev,
      { text: `> ${q}`, kind: 'daki-cli' as const },
    ])
    scrollConsole()

    try {
      const res = await fetch(`${API_BASE}/api/v1/daki/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, challenge_id: challengeId, question: q }),
      })
      const data = await res.json()
      const reply: string = data.daki_message ?? '// [DAKI] Sin señal.'
      setOutput((prev) => [
        ...prev,
        ...reply.split('\n').filter(Boolean).map((line) => ({
          text: `[DAKI] ${line}`, kind: 'daki-cli' as const,
        })),
      ])
      activateWaveform(reply)
    } catch {
      setOutput((prev) => [
        ...prev,
        { text: '[DAKI] Señal interrumpida. Intenta de nuevo.', kind: 'daki-cli' as const },
      ])
    } finally {
      setCliLoading(false)
      scrollConsole()
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [cliInput, cliLoading, userId, challengeId, activateWaveform])

  // Carga la lista completa de misiones para detectar el siguiente nodo
  useEffect(() => {
    if (!hydrated || !userId) return
    fetch(`${API_BASE}/api/v1/challenges?user_id=${userId}`)
      .then((r) => r.json())
      .then((data: ChallengeListItem[]) => setAllChallenges(data))
      .catch(() => {})
  }, [hydrated, userId])

  // Limpiar consola, rachas y resetear timer al cambiar de reto
  useEffect(() => {
    setOutput([{ text: '> Terminal lista.', kind: 'info' }])
    setFailStreak(0)
    setHintIndex(-1)
    challengeStartMs.current = Date.now()
    // Limpiar debounce pendiente del reto anterior
    if (codeDraftRef.current) clearTimeout(codeDraftRef.current)
  }, [challengeId])

  // Guardar borrador del código en localStorage (debounce 800ms)
  // Clave: code_draft_<challengeId>  — así cada reto tiene su propio borrador
  useEffect(() => {
    if (!code || !challengeId) return
    if (codeDraftRef.current) clearTimeout(codeDraftRef.current)
    codeDraftRef.current = setTimeout(() => {
      try {
        localStorage.setItem(`code_draft_${challengeId}`, code)
      } catch { /* localStorage lleno o bloqueado — ignorar silenciosamente */ }
    }, 800)
    return () => {
      if (codeDraftRef.current) clearTimeout(codeDraftRef.current)
    }
  }, [code, challengeId])

  // Persistir paso del tutorial en localStorage para sobrevivir recargas
  useEffect(() => {
    if (!challenge || challenge.challenge_type !== 'tutorial' || !challengeId) return
    try { localStorage.setItem(`daki_tutorial_step_${challengeId}`, String(tutorialStep)) } catch { /* */ }
  }, [tutorialStep, challengeId, challenge])

  // Carga el reto actual
  useEffect(() => {
    if (!hydrated || !userId) return
    const controller = new AbortController()
    fetch(`${API_BASE}/api/v1/challenges/${challengeId}?user_id=${userId}`, { signal: controller.signal })
      .then((r) => r.json())
      .then((data: Challenge) => {
        // Reto bloqueado → toast + redirección
        if (data.unlocked === false) {
          setToastMsg('ACCESO DENEGADO: Secuencia de aprendizaje no completada')
          setShowToast(true)
          setTimeout(() => router.replace('/misiones'), 2200)
          return
        }
        // Misión de pago + usuario freemium → mostrar paywall inmediatamente
        if (data.is_free === false && !isPaid) {
          setShowPaywall(true)
        }
        // Merge local cache: si ya se completó en esta sesión, reflejarlo sin esperar a la API
        const mergedData = completedChallengeIds.includes(data.id)
          ? { ...data, completed: true }
          : data
        setChallenge(mergedData)
        // Restaurar borrador desde localStorage si existe;
        // si no, usar initial_code. Garantiza string no-undefined durante hidratación.
        const draft = (() => {
          try { return localStorage.getItem(`code_draft_${data.id}`) } catch { return null }
        })()
        // Restaurar paso del tutorial desde localStorage si existe
        if (data.challenge_type === 'tutorial') {
          const savedStep = (() => { try { return localStorage.getItem(`daki_tutorial_step_${data.id}`) } catch { return null } })()
          const step = savedStep ? parseInt(savedStep, 10) : 1
          if (step >= 2 && step <= 4) {
            setTutorialStep(step)
            setSyncProgress((step - 1) * 25)
            setCode(TUTORIAL_STEP_CODES[step] ?? mergedData.initial_code ?? '')
          } else {
            setCode(draft ?? mergedData.initial_code ?? '')
          }
        } else {
          setCode(draft ?? mergedData.initial_code ?? '')
        }
        // Briefing teórico: solo para misiones normales no completadas
        if (mergedData.theory_content && !mergedData.completed && mergedData.challenge_type !== 'tutorial') {
          setViewMode('briefing')
        }
      })
      .catch((err) => { if (err?.name !== 'AbortError') {} })
    return () => controller.abort()
  }, [hydrated, challengeId, userId, isPaid, router])

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

  // ─── DAKI Linter: decoración de línea errónea en Monaco ────────────────────
  const applyErrorDecoration = useCallback((line: number | null) => {
    if (!editorRef.current || !line) return
    const model = editorRef.current.getModel()
    if (!model) return
    const newDecorations = [{
      range: new (window as any).monaco.Range(line, 1, line, model.getLineMaxColumn(line)),
      options: {
        isWholeLine: true,
        className: 'daki-error-line',
        glyphMarginClassName: 'daki-error-glyph',
        overviewRuler: { color: 'rgba(255,50,50,0.8)', position: 1 },
      },
    }]
    if (decorationsRef.current) {
      decorationsRef.current.set(newDecorations)
    } else {
      decorationsRef.current = editorRef.current.createDecorationsCollection(newDecorations)
    }
    // Auto-clear after 4s
    setTimeout(() => decorationsRef.current?.clear(), 4000)
  }, [])

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

  // Sound helper
  const playSound = useCallback((ref: React.MutableRefObject<HTMLAudioElement | null>) => {
    if (!soundEnabled) return
    try {
      if (ref.current) { ref.current.currentTime = 0; ref.current.play().catch(() => {}) }
    } catch { /* silent */ }
  }, [soundEnabled])

  // Victory line glow — whole-document Monaco decoration
  const applyVictoryDecoration = useCallback(() => {
    if (!editorRef.current) return
    const model = editorRef.current.getModel()
    if (!model) return
    const lineCount = model.getLineCount()
    const newDecs = Array.from({ length: lineCount }, (_, i) => ({
      range: new (window as any).monaco.Range(i + 1, 1, i + 1, model.getLineMaxColumn(i + 1)),
      options: { isWholeLine: true, className: 'daki-victory-line' },
    }))
    if (decorationsRef.current) {
      decorationsRef.current.set(newDecs)
    } else {
      decorationsRef.current = editorRef.current.createDecorationsCollection(newDecs)
    }
    setTimeout(() => decorationsRef.current?.clear(), 2200)
  }, [])

  // Session timer formatter
  const formatTime = (secs: number) => {
    const m = Math.floor(secs / 60).toString().padStart(2, '0')
    const s = (secs % 60).toString().padStart(2, '0')
    return `${m}:${s}`
  }

  // Keyword glow
  const handleCodeChange = useCallback((val: string) => {
    setCode(val ?? '')
    resetIdleTimer()   // actividad semántica: el Operador está editando
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
  }, [resetIdleTimer])

  const scrollConsole = () =>
    setTimeout(() => consoleRef.current?.scrollTo(0, consoleRef.current.scrollHeight), 60)

  // Detecta el siguiente nodo en la lista ordenada.
  // optimisticUnlock=true cuando acabamos de completar el nivel actual por primera vez
  // — el backend ya desbloqueó el siguiente, pero allChallenges está en caché.
  const findNextChallenge = useCallback(
    (currentId: string, optimisticUnlock = false): VictoryNext | null => {
      const idx = allChallenges.findIndex((c) => c.id === currentId)
      if (idx === -1 || idx >= allChallenges.length - 1) return null
      const next = allChallenges[idx + 1]
      const isLocked = !optimisticUnlock && !next.unlocked
      return { id: next.id, title: next.title, isDrone: next.challenge_type === 'drone', isLocked }
    },
    [allChallenges]
  )

  // Pista DAKI
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
          fail_count: Math.max(1, failStreak),
          operator_level: level ?? 1,
        }),
      })
      const data = await res.json()
      if (data.hint) {
        playSound(audioHintRef)
        setOutput((prev) => {
          const next = [
            ...prev,
            { text: '', kind: 'enigma' as const },
            { text: '[DAKI] Transmisión entrante...', kind: 'enigma' as const },
            ...data.hint.split('\n').map((line: string) => ({
              text: `[DAKI] ${line}`, kind: 'enigma' as const,
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
    resetIdleTimer()   // actividad semántica: el Operador ejecutó código
    playSound(audioRunRef)

    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), 12_000)

    try {
      const res = await fetch(`${API_BASE}/api/v1/execute`, {
        method:      'POST',
        credentials: 'include',
        headers:     { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId, challenge_id: challengeId,
          source_code: code, test_inputs: challenge?.test_inputs ?? [],
          time_spent_ms: Date.now() - challengeStartMs.current,
          daki_level: dakiLevel,
        }),
        signal: controller.signal,
      })

      if (!res.ok) {
        // ── 402: paywall — el usuario llegó al límite freemium ────────────────
        if (res.status === 402) {
          setShowPaywall(true)
          return
        }
        const err = await res.json()
        triggerShake('soft')
        triggerTerminalAnim('anim-error-flash', 600)
        setOutput([{ text: `[ERROR] ${err.detail ?? res.statusText}`, kind: 'stderr' }])
        return
      }

      const data = await res.json()

      // ── Tutorial multi-step override ─────────────────────────────────────────
      if (challenge?.challenge_type === 'tutorial') {
        const lines: ConsoleLine[] = []
        if (data.stdout) lines.push({ text: data.stdout, kind: 'stdout' })
        if (data.stderr) lines.push({ text: data.stderr, kind: 'stderr' })

        let stepPassed = false
        let stepError  = false

        switch (tutorialStep) {
          case 1:
            // Solo ejecutar → siempre pasa
            stepPassed = true
            break

          case 2:
            // Sin SyntaxError → pasa
            if (!data.stderr || !data.stderr.includes('SyntaxError')) {
              stepPassed = true
            } else {
              stepError = true
              lines.push({ text: '> [DAKI]: Ruido sintáctico detectado. Cierra las comillas e intenta de nuevo.', kind: 'enigma' })
            }
            break

          case 3:
            // Código contiene "operador =" y sin error → pasa
            if (/\boperador\s*=/.test(code) && !data.stderr) {
              stepPassed = true
            } else if (data.stderr) {
              stepError = true
              lines.push({ text: '> [DAKI]: Error en el canal de memoria. Revisa la sintaxis.', kind: 'enigma' })
            } else {
              stepError = true
              lines.push({ text: '> [DAKI]: Variable no detectada. Escribe: operador = 1', kind: 'enigma' })
            }
            break

          case 4:
            // Usa output_matched del backend (step 4 produce "Enlace Listo" si es correcto)
            applyGamificationResult({
              new_level: data.gamification.new_level,
              new_total_xp: data.gamification.new_total_xp,
            })
            if (data.output_matched && !data.gamification.already_completed) {
              markChallengeCompleted(challengeId)
              try { localStorage.removeItem(`daki_tutorial_step_${challengeId}`) } catch { /* */ }
              setSyncProgress(100)
              setTutorialFlash(true)
              triggerEditorAnim('anim-victory-glow', 1400)
              setShowParticles(true)
              setTimeout(() => setShowParticles(false), 1400)
              setVictoryXp(data.gamification.xp_earned)
              setVictoryNext(findNextChallenge(challengeId, true))
              lines.push({ text: '> [DAKI]: ¡Calibración completada! Acceso al Nexo concedido.', kind: 'success' })
              setTimeout(() => setShowVictory(true), 700)
            } else if (data.gamification.already_completed) {
              setSyncProgress(100)
              setVictoryXp(0)
              setVictoryNext(findNextChallenge(challengeId))
              setTimeout(() => setShowVictory(true), 700)
            } else {
              stepError = true
              lines.push({ text: '> [DAKI]: Función sin retorno. Cambia print por return dentro de finalizar_enlace().', kind: 'enigma' })
            }
            break
        }

        if (stepPassed && tutorialStep < 4) {
          const nextStep    = tutorialStep + 1
          const nextProgress = (nextStep - 1) * 25   // progress = completed steps, not current step
          lines.push({ text: `> [DAKI]: Fase ${tutorialStep} completada — Sincronización al ${nextProgress}%.`, kind: 'success' })
          setOutput(lines)
          scrollConsole()
          setTutorialFlash(true)
          triggerEditorAnim('anim-victory-glow', 900)
          setTimeout(() => {
            setTutorialStep(nextStep)
            setSyncProgress(nextProgress)
            setCode(TUTORIAL_STEP_CODES[nextStep])
            setOutput([{ text: '> Terminal lista.', kind: 'info' }])
          }, 900)
        } else {
          if (stepError) {
            triggerShake('soft')
            triggerEditorAnim('anim-error-flash', 500)
          }
          setOutput(lines)
          scrollConsole()
        }

        return  // ← evita que corra la lógica normal de misiones
      }
      // ── Fin override tutorial ─────────────────────────────────────────────────

      const lines: ConsoleLine[] = []

      // ── Interceptar timeout: bucle infinito o código sin fin ─────────────────
      if (data.stderr?.toLowerCase().includes('timed out') || data.stderr?.toLowerCase().includes('time limit')) {
        setOutput([
          { text: '[ FALLO NEURONAL: BUCLE INFINITO DETECTADO ]', kind: 'stderr' },
          { text: '> El Nexo detectó un proceso sin fin. Revisa si tienes un bucle sin condición de salida.', kind: 'enigma' },
        ])
        triggerShake('hard')
        triggerEditorAnim('anim-error-flash', 600)
        scrollConsole()
        setFailStreak((prev) => prev + 1)
        return
      }
      // ─────────────────────────────────────────────────────────────────────────

      if (data.stdout) lines.push({ text: data.stdout, kind: 'stdout' })
      if (data.stderr) {
        lines.push({ text: data.stderr, kind: 'stderr' })
        lastErrorRef.current = data.stderr  // contexto para intervención proactiva
      }

      // ── Error info: decoración del editor + contexto técnico en consola ───────
      const ei = data.error_info as ErrorInfo | null
      if (ei) {
        const lineLabel = ei.line ? `${ei.line}` : '?'
        lines.push({ text: `[${ei.error_type}] Línea ${lineLabel}: ${ei.detail}`, kind: 'stderr' })
        applyErrorDecoration(ei.line)
      }

      // ── DAKI: reacción contextual del LLM → DakiHint + voz + waveform ────────
      if (data.daki_message) {
        setDakiMessage(data.daki_message)
        speakDaki(data.daki_message)
        activateWaveform(data.daki_message)
      }
      // ─────────────────────────────────────────────────────────────────────────

      // Diferenciar "error de ejecución" (excepción Python) de "salida incorrecta" (output mismatch)
      lines.push({
        text: `${data.execution_time_ms.toFixed(1)}ms  |  ${
          data.output_matched
            ? 'Salida correcta ✓'
            : data.error_info
            ? 'Error de ejecución ✗'
            : 'Salida incorrecta ✗'
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

      // Borrador cumplió su misión en cuanto el código es correcto — lo limpiamos siempre
      if (data.output_matched) {
        try { localStorage.removeItem(`code_draft_${challengeId}`) } catch { /* ignorar */ }
      }

      if (data.output_matched && !data.gamification.already_completed) {
        markChallengeCompleted(challengeId)
        triggerShake('soft')
        triggerEditorAnim('anim-victory-glow', 1400)
        triggerTerminalAnim('anim-victory-glow', 1400)
        setShowParticles(true)
        setTimeout(() => setShowParticles(false), 1400)
        playSound(audioVictoryRef)
        applyVictoryDecoration()

        // Combo de eficiencia
        const effectiveLines = countEffectiveLines(code)
        if (effectiveLines <= parLines && data.gamification.xp_earned > 0) {
          setComboXp(data.gamification.xp_earned)
          setTimeout(() => setShowCombo(true), 320)
        }

        // Logros desbloqueados
        if (data.achievements_unlocked?.length) {
          setTimeout(() => setActiveAchievements(data.achievements_unlocked), 400)
        }

        // Insight flash (conexión mundo real)
        if (data.insight) {
          setTimeout(() => setActiveInsight(data.insight), 800)
        }

        // Modal de victoria — primer compleción: asume que el backend ya desbloqueó el siguiente
        const next = findNextChallenge(challengeId, true)
        setVictoryNext(next)
        setVictoryXp(data.gamification.xp_earned)
        setTimeout(() => setShowVictory(true), 700)
      } else if (!data.output_matched) {
        triggerShake('soft')
        triggerEditorAnim('anim-error-flash', 500)
        triggerTerminalAnim('anim-error-flash', 600)
      }

      if (!data.output_matched) {
        const newStreak = failStreak + 1
        setFailStreak(newStreak)
        // Niveles BEGINNER (tier 1): pistas en el 1er, 3er y 5to fallo — el principiante no puede esperar
        // Niveles INTERMEDIATE/ADVANCED: pistas en el 2do, 4to y 6to fallo
        const isEasy = (challenge?.difficulty_tier ?? 2) === 1
        const hintTriggers = isEasy ? [1, 3, 5] : [2, 4, 6]
        if (hintTriggers.includes(newStreak)) {
          setHintIndex((prev: number) => {
            const maxIdx = (challenge?.hints?.length ?? 1) - 1
            return Math.min(prev + 1, maxIdx)
          })
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
      tutorialStep, triggerShake, countEffectiveLines, findNextChallenge,
      applyGamificationResult, markChallengeCompleted, activateWaveform, resetIdleTimer])

  // ── Keep handleEjecutarRef current so Ctrl+Enter never captures a stale closure ──
  useEffect(() => { handleEjecutarRef.current = handleEjecutar }, [handleEjecutar])

  // Navegar al siguiente nodo desde el modal de victoria
  const handleNextChallenge = useCallback(() => {
    setShowVictory(false)
    if (!victoryNext || victoryNext.isLocked) {
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

      <VictoryModal
        visible={showVictory}
        next={victoryNext}
        xpEarned={victoryXp}
        onNext={handleNextChallenge}
        onReview={() => setShowVictory(false)}
        titleOverride={challenge?.challenge_type === 'tutorial'
          ? '[ CALIBRACIÓN COMPLETADA. RIESGO CEREBRAL AL 0%. ACCESO AL NEXO CONCEDIDO ]'
          : undefined
        }
      />

      <PaywallModal
        visible={showPaywall}
        onClose={() => setShowPaywall(false)}
        onGranted={() => setIsPaid(true)}
        userId={userId}
      />

      {/* ── Logros desbloqueados ────────────────────────────────────────────── */}
      <AchievementToast
        achievements={activeAchievements}
        onDismiss={(id) => setActiveAchievements((prev) => prev.filter((a) => a.id !== id))}
      />

      {/* ── Insight flash post-nivel ─────────────────────────────────────────── */}
      <AnimatePresence>
        {activeInsight && (
          <InsightFlash
            insight={activeInsight}
            onClose={() => setActiveInsight(null)}
          />
        )}
      </AnimatePresence>

      {/* ── Intel Drawer — Panel lateral deslizable con el Códice/Briefing ── */}
      <AnimatePresence>
        {showIntelDrawer && (
          <>
            {/* Backdrop */}
            <motion.div
              className="fixed inset-0 z-[8800] bg-black/60 backdrop-blur-sm"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.2 }}
              onClick={() => setShowIntelDrawer(false)}
            />
            {/* Drawer */}
            <motion.div
              className="fixed left-0 top-0 bottom-0 z-[8900] w-[440px] max-w-[90vw] flex flex-col font-mono overflow-hidden"
              style={{
                background:   '#030A06',
                borderRight:  '1px solid rgba(0,255,65,0.25)',
                boxShadow:    '6px 0 40px rgba(0,255,65,0.06), inset 0 0 60px rgba(0,255,65,0.02)',
              }}
              initial={{ x: '-100%' }}
              animate={{ x: 0 }}
              exit={{ x: '-100%' }}
              transition={{ type: 'spring', stiffness: 340, damping: 32 }}
            >
              {/* Scanline overlay */}
              <div
                className="absolute inset-0 pointer-events-none z-0"
                style={{ background: 'repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,0.04) 2px,rgba(0,0,0,0.04) 4px)' }}
              />

              {/* Header */}
              <div
                className="relative z-10 flex items-center gap-3 px-5 py-3 shrink-0"
                style={{ borderBottom: '1px solid rgba(0,255,65,0.15)', background: 'rgba(0,255,65,0.03)' }}
              >
                <motion.span
                  className="w-2 h-2 rounded-full"
                  style={{ background: '#00FF41', boxShadow: '0 0 8px rgba(0,255,65,0.9)' }}
                  animate={{ opacity: [0.4, 1, 0.4] }}
                  transition={{ duration: 1.8, repeat: Infinity }}
                />
                <span
                  className="text-xs font-black tracking-[0.35em] uppercase flex-1"
                  style={{ color: 'rgba(0,255,65,0.85)', textShadow: '0 0 12px rgba(0,255,65,0.3)' }}
                >
                  [ ARCHIVO DE MISIÓN ]
                </span>
                <button
                  onClick={() => setShowIntelDrawer(false)}
                  className="text-[#00FF41]/30 hover:text-[#00FF41]/70 transition-colors text-sm leading-none"
                  aria-label="Cerrar"
                >✕</button>
              </div>

              {/* Subheader — nombre del nivel */}
              <div
                className="relative z-10 px-5 py-2.5 shrink-0"
                style={{ borderBottom: '1px solid rgba(0,255,65,0.08)' }}
              >
                <div className="text-[9px] tracking-[0.5em] text-[#00FF41]/30 mb-0.5">INCURSIÓN ACTIVA</div>
                <div className="text-[#00FF41]/80 font-bold text-xs tracking-[0.12em]">{challenge?.title?.toUpperCase()}</div>
              </div>

              {/* Body — scrollable */}
              <div className="relative z-10 flex-1 overflow-y-auto px-5 py-4 space-y-4">
                {/* Lore briefing */}
                {challenge?.lore_briefing && (
                  <div>
                    <div className="text-[9px] tracking-[0.5em] text-[#00FF41]/30 mb-2 uppercase">Briefing de la Misión</div>
                    <p className="text-[#00FF41]/60 text-[11px] leading-relaxed italic border-l-2 pl-3"
                      style={{ borderColor: 'rgba(0,255,65,0.2)' }}>
                      {challenge.lore_briefing}
                    </p>
                  </div>
                )}

                {/* Divider */}
                {challenge?.lore_briefing && challenge?.theory_content && (
                  <div className="h-px" style={{ background: 'linear-gradient(90deg,transparent,rgba(0,255,65,0.15),transparent)' }} />
                )}

                {/* Theory content */}
                {challenge?.theory_content ? (
                  <div>
                    <div className="text-[9px] tracking-[0.5em] text-[#00FF41]/30 mb-3 uppercase">Teoría del Concepto</div>
                    <TheoryRenderer text={challenge.theory_content} />
                  </div>
                ) : (
                  /* Fallback: description */
                  <div>
                    <div className="text-[9px] tracking-[0.5em] text-[#00FF41]/30 mb-2 uppercase">Objetivo de la Incursión</div>
                    <p className="text-[#00FF41]/65 text-[11px] leading-relaxed whitespace-pre-wrap">
                      {challenge?.description}
                    </p>
                  </div>
                )}
              </div>

              {/* Footer CTA */}
              <div
                className="relative z-10 px-5 py-3 shrink-0"
                style={{ borderTop: '1px solid rgba(0,255,65,0.10)' }}
              >
                <button
                  onClick={() => setShowIntelDrawer(false)}
                  className="w-full py-2 text-[10px] tracking-[0.4em] font-bold transition-all duration-150"
                  style={{
                    border:     '1px solid rgba(0,255,65,0.30)',
                    color:      'rgba(0,255,65,0.60)',
                    background: 'rgba(0,255,65,0.04)',
                  }}
                  onMouseEnter={(e) => { e.currentTarget.style.background = 'rgba(0,255,65,0.08)'; e.currentTarget.style.color = 'rgba(0,255,65,0.9)' }}
                  onMouseLeave={(e) => { e.currentTarget.style.background = 'rgba(0,255,65,0.04)'; e.currentTarget.style.color = 'rgba(0,255,65,0.60)' }}
                >
                  VOLVER AL EDITOR →
                </button>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>

      {/* Layout con screen shake */}
      <motion.div
        animate={shakeCtrl}
        className="ide-view relative flex flex-col h-[calc(100vh-2rem)] bg-cover bg-center bg-no-repeat text-[#00FF41] font-mono overflow-hidden"
        style={{
          backgroundImage: `url('${getMissionBackground(challenge?.level_order)}'), radial-gradient(ellipse at center, #0a1a0a 0%, #000000 70%)`,
        }}
      >
        {/* Overlay: oscurece 80% + blur para que el editor y el tablero brillen */}
        <div className="absolute inset-0 bg-black/80 backdrop-blur-sm z-0 pointer-events-none" />

        {/* Grid ciberpunk — visible solo cuando no carga la imagen */}
        <div
          className="absolute inset-0 z-0 pointer-events-none opacity-[0.07]"
          style={{
            backgroundImage:
              'linear-gradient(rgba(0,255,65,0.8) 1px, transparent 1px), linear-gradient(90deg, rgba(0,255,65,0.8) 1px, transparent 1px)',
            backgroundSize: '40px 40px',
          }}
        />

        {/* Todo el contenido sobre el overlay */}
        <div className="relative z-10 flex flex-col flex-1 overflow-hidden">

        {/* Flash verde al avanzar fase tutorial */}
        <AnimatePresence>
          {tutorialFlash && (
            <motion.div
              key="tutorial-flash"
              className="fixed inset-0 z-[8500] pointer-events-none"
              style={{ background: 'rgba(0,255,65,0.10)', mixBlendMode: 'screen' }}
              initial={{ opacity: 1 }}
              animate={{ opacity: 0 }}
              transition={{ duration: 0.55, ease: 'easeOut' }}
              onAnimationComplete={() => setTutorialFlash(false)}
            />
          )}
        </AnimatePresence>

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

        {/* HUD de navegación */}
        <header className={`grid grid-cols-3 items-center px-4 py-1.5 bg-[#0D0D0D] border-b border-[#00FF41]/20 text-xs shrink-0 transition-all duration-300 ${focusMode ? 'opacity-0 h-0 overflow-hidden py-0 border-0' : ''}`}>

          {/* Izquierda — botón abortar + archivo de misión */}
          <div className="flex items-center gap-2">
            <button
              onClick={() => {
                setNetworkError(false)
                router.push(`/misiones?selected=${challengeId}`)
              }}
              className="flex items-center gap-1.5 px-3 py-1 border border-orange-500/40 text-orange-400/80
                         tracking-widest hover:border-orange-400/80 hover:text-orange-300 hover:bg-orange-500/10
                         active:scale-95 transition-all duration-150"
            >
              <span className="text-orange-400/60">◀</span> VOLVER A MISIONES
            </button>
            {challenge && (
              <button
                onClick={() => setShowIntelDrawer(true)}
                className="flex items-center gap-1.5 px-3 py-1 border border-[#00FF41]/30 text-[#00FF41]/60
                           tracking-widest hover:border-[#00FF41]/60 hover:text-[#00FF41]/90 hover:bg-[#00FF41]/05
                           active:scale-95 transition-all duration-150 text-xs"
              >
                <motion.span
                  animate={{ opacity: [0.4, 1, 0.4] }}
                  transition={{ duration: 2.4, repeat: Infinity }}
                  className="text-[#00FF41]/50"
                >◉</motion.span>
                ARCHIVO DE MISIÓN
              </button>
            )}
          </div>

          {/* Centro — nombre de la misión */}
          <div className="flex justify-center">
            {challenge ? (
              <span
                className="font-black tracking-[0.15em] text-[#00FF41] truncate max-w-xs text-center"
                style={{ textShadow: '0 0 8px #00FF4160' }}
              >
                {challenge.title.toUpperCase()}
              </span>
            ) : (
              <span className="text-[#00FF41]/25 tracking-widest animate-pulse">CARGANDO...</span>
            )}
          </div>

          {/* Derecha — stats + HUD controles */}
          <div className="flex items-center justify-end gap-3 text-[#00FF41]/70">
            <span className="text-[#00FF41]/40 tabular-nums">⏱ {formatTime(sessionSecs)}</span>
            {failStreak > 0 && (
              <span className="text-[#FFB800]/60 tabular-nums">{failStreak}✕</span>
            )}
            <span className="text-[#00FF41]/40">{username}</span>
            <span>RNG <strong className="text-[#00FF41]">{level}</strong></span>
            <span id="xp-display">XP <strong className="text-[#00FF41]">{totalXp.toLocaleString()}</strong></span>
            {streakDays > 0 && (
              <span>🔥<strong className="text-[#00FF41]">{streakDays}d</strong></span>
            )}
            {failStreak >= 2 && !loadingHint && (
              <motion.span
                initial={{ opacity: 0 }} animate={{ opacity: [0.5, 1, 0.5] }}
                transition={{ duration: 1.2, repeat: Infinity }}
                className="text-[#FFB800] text-xs tracking-widest cursor-pointer"
                onClick={() => requestHint(output)}
                title="Solicitar pista de DAKI"
              >
                ENIGMA?
              </motion.span>
            )}
            {/* Ambient music toggle */}
            <button
              onClick={() => setAmbientOn((v) => !v)}
              title={ambientOn ? 'Silenciar música' : 'Activar música ambiente'}
              className="text-xs px-2 py-0.5 border transition-all duration-150 select-none"
              style={{
                borderColor: ambientOn ? 'rgba(0,255,65,0.6)' : 'rgba(0,255,65,0.2)',
                color:       ambientOn ? 'rgba(0,255,65,0.9)' : 'rgba(0,255,65,0.35)',
                background:  ambientOn ? 'rgba(0,255,65,0.08)' : 'transparent',
              }}
            >♪</button>
            {/* Sound effects toggle */}
            <button
              onClick={() => setSoundEnabled((v) => !v)}
              title={soundEnabled ? 'Silenciar efectos' : 'Activar efectos de sonido'}
              className="text-xs px-2 py-0.5 border transition-all duration-150 select-none"
              style={{
                borderColor: soundEnabled ? 'rgba(0,255,65,0.6)' : 'rgba(0,255,65,0.2)',
                color:       soundEnabled ? 'rgba(0,255,65,0.9)' : 'rgba(0,255,65,0.35)',
                background:  soundEnabled ? 'rgba(0,255,65,0.08)' : 'transparent',
              }}
            >SFX</button>
            {/* Focus mode toggle */}
            <button
              onClick={() => setFocusMode((v) => !v)}
              title="Modo enfoque (Esc para salir)"
              className="text-xs px-2 py-0.5 border transition-all duration-150 select-none"
              style={{
                borderColor: 'rgba(0,255,65,0.2)',
                color:       'rgba(0,255,65,0.4)',
              }}
            >⊞</button>
          </div>
        </header>

        {/* ── Barra de progreso del tutorial ── */}
        {challenge?.challenge_type === 'tutorial' && (
          <div className="shrink-0 px-4 py-2.5 bg-black/50 border-b border-cyan-500/15 backdrop-blur-sm">
            <div className="flex items-center gap-3">
              <span className="text-[8px] tracking-[0.5em] text-cyan-400/55 font-bold uppercase shrink-0">
                Enlace Neuronal
              </span>
              <div className="flex-1 h-1.5 bg-cyan-950/40 overflow-hidden">
                <motion.div
                  className="h-full"
                  style={{
                    background: 'linear-gradient(90deg, rgba(0,180,255,0.8), rgba(0,255,65,0.8))',
                    boxShadow: '0 0 8px rgba(0,229,255,0.5)',
                  }}
                  animate={{ width: `${syncProgress}%` }}
                  transition={{ duration: 0.5, ease: 'easeOut' }}
                />
              </div>
              <motion.span
                key={syncProgress}
                className="text-[13px] font-black tracking-widest text-cyan-400 shrink-0"
                style={{ textShadow: '0 0 10px rgba(0,229,255,0.7)', minWidth: '2.8rem', textAlign: 'right' }}
                initial={{ scale: 1.3, opacity: 0.5 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ duration: 0.25 }}
              >
                {syncProgress}%
              </motion.span>
            </div>
          </div>
        )}

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
          <div id="code-editor-panel" className={`flex-1 flex flex-col min-w-0 border border-transparent ${editorAnim}`}>
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
                onMount={(editor: any, monaco: any) => {
                  editorRef.current = editor
                  editor.addCommand(
                    monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter,
                    () => handleEjecutarRef.current()
                  )
                }}
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

          {/* Panel derecho — flash verde/rojo en éxito/error */}
          <div className={`w-80 flex flex-col border-l border-[#00FF41]/20 bg-[#0D0D0D] shrink-0 ${terminalAnim}`}>

            {/* Tutorial — panel guiado de DAKI (reemplaza la descripción habitual) */}
            {challenge?.challenge_type === 'tutorial' ? (
              <TutorialPanel tutorialStep={tutorialStep} syncProgress={syncProgress} />
            ) : (
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
            )}

            {/* Panel de pistas DAKI + botón de solicitud */}
            {challenge?.challenge_type !== 'tutorial' && (challenge?.hints?.length ?? 0) > 0 && (
              <>
                {/* Botón de solicitud de pista */}
                <div className="shrink-0 px-3 py-2 border-b border-[#00FF41]/10">
                  <button
                    onClick={() => setHintIndex((prev: number) => Math.min(prev + 1, (challenge?.hints?.length ?? 1) - 1))}
                    disabled={hintIndex >= (challenge?.hints?.length ?? 1) - 1 && hintIndex >= 0}
                    className="w-full text-left px-3 py-1.5 text-[9px] tracking-[0.35em] font-bold border transition-all duration-150 disabled:opacity-30 disabled:cursor-not-allowed"
                    style={{
                      borderColor: hintIndex < 0 ? 'rgba(0,229,255,0.4)' : 'rgba(0,229,255,0.2)',
                      color: hintIndex < 0 ? 'rgba(0,229,255,0.8)' : 'rgba(0,229,255,0.4)',
                      background: hintIndex < 0 ? 'rgba(0,229,255,0.05)' : 'transparent',
                    }}
                  >
                    {hintIndex < 0
                      ? '▸ SOLICITAR PISTA DE DAKI'
                      : hintIndex < (challenge?.hints?.length ?? 1) - 1
                        ? `▸ SIGUIENTE PISTA  [${hintIndex + 2}/${challenge?.hints?.length}]`
                        : `✓ PISTA FINAL REVELADA  [${challenge?.hints?.length}/${challenge?.hints?.length}]`
                    }
                  </button>
                </div>
                <DakiHint
                  visible={hintIndex >= 0}
                  hints={challenge?.hints ?? []}
                  hintIndex={hintIndex}
                  dakiLevel={dakiLevel}
                />
              </>
            )}

            {/* ── DAKI Intel: respuesta narrativa al último run ── */}
            {dakiMessage && (
              <motion.div
                key={dakiMessage}
                initial={{ opacity: 0, y: 4 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.25 }}
                className="mx-0 border-t border-b shrink-0 font-mono"
                style={{
                  borderColor: 'rgba(189,0,255,0.25)',
                  background: 'rgba(189,0,255,0.04)',
                  boxShadow: 'inset 0 0 16px rgba(189,0,255,0.03)',
                }}
              >
                <div className="flex items-center gap-2 px-3 py-1.5 border-b" style={{ borderColor: 'rgba(189,0,255,0.15)' }}>
                  <motion.span
                    className="w-1.5 h-1.5 rounded-full shrink-0"
                    style={{ background: '#BD00FF', boxShadow: '0 0 6px rgba(189,0,255,0.8)' }}
                    animate={{ opacity: [0.4, 1, 0.4] }}
                    transition={{ duration: 1.5, repeat: Infinity }}
                  />
                  <span className="text-[9px] tracking-[0.4em] font-bold" style={{ color: 'rgba(189,0,255,0.7)' }}>
                    [ DAKI INTEL ]
                  </span>
                  <div className="ml-auto">
                    <DakiWaveform isActive={waveformActive} color="#BD00FF" size="sm" />
                  </div>
                </div>
                <div className="px-3 py-2">
                  <p className="text-[10px] leading-relaxed" style={{ color: 'rgba(189,0,255,0.8)', fontFamily: 'monospace' }}>
                    {dakiMessage}
                  </p>
                </div>
              </motion.div>
            )}

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
                      line.kind === 'stderr'       ? 'text-red-400'
                      : line.kind === 'success'   ? 'text-[#00FF41]'
                      : line.kind === 'enigma'    ? 'enigma-line'
                      : line.kind === 'info'      ? 'text-[#00FF41]/45'
                      : line.kind === 'intervention'
                        ? 'text-[#BD00FF] font-semibold tracking-wide'
                      : line.kind === 'daki-cli'
                        ? 'text-cyan-400/80'
                      : 'text-[#00FF41]/85'
                    }`}
                    style={
                      line.kind === 'intervention' ? {
                        textShadow: '0 0 8px #BD00FF60',
                        borderLeft: '2px solid #BD00FF80',
                        paddingLeft: '6px',
                      }
                      : line.kind === 'daki-cli' && line.text.startsWith('[DAKI]') ? {
                        textShadow: '0 0 8px rgba(0,229,255,0.3)',
                        borderLeft: '2px solid rgba(0,229,255,0.4)',
                        paddingLeft: '6px',
                      }
                      : undefined
                    }
                  >
                    <DakiTerminalLine text={line.text} kind={line.kind} />
                  </div>
                ))}
              </div>

              {/* ── DAKI CLI — Línea de Comandos ── */}
              <div
                className="shrink-0 border-t px-3 py-2"
                style={{ borderColor: 'rgba(0,229,255,0.15)', background: 'rgba(0,229,255,0.02)' }}
              >
                <div className="flex items-center gap-2">
                  <motion.span
                    className="text-cyan-400/50 text-xs select-none shrink-0"
                    animate={{ opacity: cliLoading ? [0.3, 0.9, 0.3] : 1 }}
                    transition={{ duration: 0.8, repeat: cliLoading ? Infinity : 0 }}
                  >▶</motion.span>
                  <input
                    type="text"
                    value={cliInput}
                    onChange={(e) => setCliInput(e.target.value)}
                    onKeyDown={(e) => { if (e.key === 'Enter') handleDakiAsk() }}
                    placeholder={cliLoading ? '[ DAKI PROCESANDO... ]' : 'Consulta a DAKI... [Presiona Enter]'}
                    disabled={cliLoading}
                    className="flex-1 bg-transparent text-xs text-cyan-400 placeholder-cyan-400/20 outline-none font-mono tracking-wide disabled:cursor-wait"
                    spellCheck={false}
                    autoComplete="off"
                  />
                </div>
              </div>
            </div>

          </div>
        </div>
        </div> {/* end z-10 content wrapper */}
      </motion.div>
    </>
  )
}
