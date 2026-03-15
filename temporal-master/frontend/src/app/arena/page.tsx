'use client'

import { useState, useEffect, useCallback, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useUserStore } from '@/store/userStore'
import { useRouter } from 'next/navigation'

const API = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000'

// ─── Types ───────────────────────────────────────────────────────────────────

type DuelPhase = 'idle' | 'searching' | 'matched' | 'dueling' | 'submitted' | 'result'

interface DuelData {
  duel_id: string
  status: string
  challenger_id: string
  defender_id: string
  challenge_id: string
  challenge_title: string | null
  challenge_description: string | null
  challenge_initial_code: string | null
  challenge_expected_output: string | null
  challenger_elo: number
  defender_elo: number
  challenger_correct: boolean | null
  challenger_time_ms: number | null
  defender_correct: boolean | null
  defender_time_ms: number | null
  winner_id: string | null
  elo_delta: number
  created_at: string
  completed_at: string | null
}

interface SubmitResult {
  duel_id: string
  correct: boolean
  execution_time_ms: number
  stdout: string
  stderr: string
  status: string
  winner_id: string | null
  elo_delta: number
  your_new_elo: number | null
}

interface InboxItem {
  duel_id: string
  challenger_id: string
  challenger_username: string
  challenger_elo: number
  challenge_title: string
  created_at: string
}

// ─── Animated scanline ───────────────────────────────────────────────────────

function ScanLine() {
  return (
    <motion.div
      className="absolute left-0 right-0 h-px bg-gradient-to-r from-transparent via-[#FF0040]/60 to-transparent pointer-events-none"
      animate={{ top: ['0%', '100%'] }}
      transition={{ duration: 3, repeat: Infinity, ease: 'linear' }}
    />
  )
}

// ─── Elo badge ───────────────────────────────────────────────────────────────

function EloBadge({ elo, label, color }: { elo: number; label: string; color: string }) {
  return (
    <div className="flex flex-col items-center gap-1">
      <span className="text-[10px] tracking-[0.3em] opacity-50" style={{ color }}>
        {label}
      </span>
      <motion.span
        className="text-3xl font-black tabular-nums"
        style={{ color, textShadow: `0 0 20px ${color}80` }}
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.4, type: 'spring' }}
      >
        {elo}
      </motion.span>
      <span className="text-[9px] tracking-widest opacity-40" style={{ color }}>ELO</span>
    </div>
  )
}

// ─── VS card ─────────────────────────────────────────────────────────────────

function VSCard({ duel, myId }: { duel: DuelData; myId: string }) {
  const isChallenger = duel.challenger_id === myId
  const myElo = isChallenger ? duel.challenger_elo : duel.defender_elo
  const rivalElo = isChallenger ? duel.defender_elo : duel.challenger_elo

  return (
    <motion.div
      className="relative w-full max-w-xl mx-auto border border-[#FF0040]/40 bg-[#0A0A0A] overflow-hidden"
      initial={{ scaleX: 0 }}
      animate={{ scaleX: 1 }}
      transition={{ duration: 0.5, ease: 'easeOut' }}
    >
      <ScanLine />
      <div className="flex items-center justify-between px-8 py-6">
        <EloBadge elo={myElo} label="TÚ" color="#00FF41" />

        <div className="flex flex-col items-center">
          <motion.span
            className="text-4xl font-black text-[#FF0040]"
            style={{ textShadow: '0 0 30px #FF004099' }}
            animate={{ opacity: [1, 0.4, 1] }}
            transition={{ duration: 1.2, repeat: Infinity }}
          >
            VS
          </motion.span>
          <span className="text-[9px] tracking-[0.4em] text-[#FF0040]/40 mt-1">DUELO PVP</span>
        </div>

        <EloBadge elo={rivalElo} label="RIVAL" color="#7DF9FF" />
      </div>

      {duel.challenge_title && (
        <div className="border-t border-[#FF0040]/20 px-8 py-3 text-center">
          <span className="text-[10px] tracking-[0.25em] text-[#FFD700]/60">MISIÓN: </span>
          <span className="text-[10px] tracking-[0.2em] text-[#FFD700]">{duel.challenge_title}</span>
        </div>
      )}
    </motion.div>
  )
}

// ─── Inbox row ───────────────────────────────────────────────────────────────

function InboxRow({ item, onAccept }: { item: InboxItem; onAccept: (id: string) => void }) {
  return (
    <motion.div
      className="flex items-center justify-between border border-[#7DF9FF]/15 px-4 py-3 hover:border-[#7DF9FF]/40 transition-colors"
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
    >
      <div className="flex flex-col gap-0.5">
        <span className="text-[#7DF9FF] text-xs tracking-wider font-bold">{item.challenger_username}</span>
        <span className="text-[10px] text-[#7DF9FF]/40 tracking-widest">ELO {item.challenger_elo} · {item.challenge_title}</span>
      </div>
      <button
        onClick={() => onAccept(item.duel_id)}
        className="text-[10px] tracking-[0.2em] text-[#FF0040] border border-[#FF0040]/40 hover:border-[#FF0040] hover:bg-[#FF0040]/10 px-3 py-1 transition-all"
      >
        ACEPTAR
      </button>
    </motion.div>
  )
}

// ─── Result screen ───────────────────────────────────────────────────────────

function ResultScreen({
  submitResult,
  myId,
  onReset,
}: {
  submitResult: SubmitResult
  myId: string
  onReset: () => void
}) {
  const won = submitResult.winner_id === myId
  const draw = submitResult.winner_id === null
  const color = draw ? '#FFD700' : won ? '#00FF41' : '#FF0040'
  const label = draw ? 'EMPATE' : won ? '¡VICTORIA!' : 'DERROTA'

  return (
    <motion.div
      className="flex flex-col items-center gap-6 w-full max-w-md mx-auto"
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
    >
      <motion.div
        className="text-5xl font-black tracking-[0.15em]"
        style={{ color, textShadow: `0 0 40px ${color}80` }}
        animate={{ scale: [1, 1.06, 1] }}
        transition={{ duration: 1.5, repeat: Infinity }}
      >
        {label}
      </motion.div>

      {submitResult.elo_delta > 0 && (
        <div className="flex flex-col items-center gap-1">
          <span className="text-[10px] tracking-[0.3em] text-white/40">CAMBIO ELO</span>
          <span
            className="text-2xl font-bold"
            style={{ color: won ? '#00FF41' : '#FF0040' }}
          >
            {won ? '+' : '-'}{submitResult.elo_delta}
          </span>
          {submitResult.your_new_elo !== null && (
            <span className="text-sm text-white/50 tracking-widest">
              NUEVO ELO: <span className="text-white font-bold">{submitResult.your_new_elo}</span>
            </span>
          )}
        </div>
      )}

      {submitResult.stdout && (
        <div className="w-full border border-white/10 bg-[#080808] p-3">
          <p className="text-[10px] tracking-widest text-white/30 mb-1">SALIDA</p>
          <pre className="text-[11px] text-[#00FF41]/80 font-mono whitespace-pre-wrap">{submitResult.stdout}</pre>
        </div>
      )}

      <div className="flex gap-3">
        <button
          onClick={onReset}
          className="text-[11px] tracking-[0.2em] text-[#00FF41] border border-[#00FF41]/40 hover:border-[#00FF41] hover:bg-[#00FF41]/10 px-5 py-2 transition-all"
        >
          NUEVA PARTIDA
        </button>
      </div>
    </motion.div>
  )
}

// ─── Main Page ────────────────────────────────────────────────────────────────

export default function ArenaPage() {
  const router = useRouter()
  const { userId, username, level } = useUserStore()

  const [phase, setPhase] = useState<DuelPhase>('idle')
  const [duel, setDuel] = useState<DuelData | null>(null)
  const [code, setCode] = useState('')
  const [submitResult, setSubmitResult] = useState<SubmitResult | null>(null)
  const [inbox, setInbox] = useState<InboxItem[]>([])
  const [error, setError] = useState<string | null>(null)
  const [isRunning, setIsRunning] = useState(false)
  const [elapsedMs, setElapsedMs] = useState(0)
  const timerRef = useRef<NodeJS.Timeout | null>(null)

  // Redirect if not logged in
  useEffect(() => {
    if (!userId) router.replace('/')
  }, [userId, router])

  // Fetch inbox on mount
  useEffect(() => {
    if (!userId) return
    fetch(`${API}/api/v1/duels/inbox?user_id=${userId}`)
      .then(r => r.json())
      .then((data: InboxItem[]) => setInbox(Array.isArray(data) ? data : []))
      .catch(() => {})
  }, [userId])

  // Timer when dueling
  useEffect(() => {
    if (phase === 'dueling') {
      const start = Date.now()
      timerRef.current = setInterval(() => setElapsedMs(Date.now() - start), 100)
    } else {
      if (timerRef.current) clearInterval(timerRef.current)
      setElapsedMs(0)
    }
    return () => { if (timerRef.current) clearInterval(timerRef.current) }
  }, [phase])

  const handleSearch = useCallback(async () => {
    if (!userId) return
    setPhase('searching')
    setError(null)
    try {
      const res = await fetch(`${API}/api/v1/duels/challenge`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId }),
      })
      if (!res.ok) {
        const body = await res.json().catch(() => ({}))
        throw new Error(body.detail ?? 'Error al buscar oponente')
      }
      const data: DuelData = await res.json()
      setDuel(data)
      setCode(data.challenge_initial_code ?? '')
      setPhase('matched')
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Error desconocido')
      setPhase('idle')
    }
  }, [userId])

  const handleStartDuel = () => setPhase('dueling')

  const handleSubmit = useCallback(async () => {
    if (!duel || !userId || isRunning) return
    setIsRunning(true)
    setError(null)
    try {
      const res = await fetch(`${API}/api/v1/duels/${duel.duel_id}/submit`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, source_code: code }),
      })
      const data: SubmitResult = await res.json()
      if (!res.ok) {
        const detail = (data as unknown as { detail?: string }).detail
        throw new Error(detail ?? 'Error al enviar')
      }
      setSubmitResult(data)
      setPhase(data.status === 'completed' ? 'result' : 'submitted')
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Error desconocido')
    } finally {
      setIsRunning(false)
    }
  }, [duel, userId, code, isRunning])

  const handleAcceptInbox = useCallback(async (duelId: string) => {
    if (!userId) return
    const res = await fetch(`${API}/api/v1/duels/${duelId}`)
    if (!res.ok) return
    const data: DuelData = await res.json()
    setDuel(data)
    setCode(data.challenge_initial_code ?? '')
    setInbox(prev => prev.filter(i => i.duel_id !== duelId))
    setPhase('dueling')
  }, [userId])

  const handleReset = () => {
    setDuel(null)
    setCode('')
    setSubmitResult(null)
    setError(null)
    setPhase('idle')
  }

  const formatTime = (ms: number) => {
    const s = Math.floor(ms / 1000)
    const dec = Math.floor((ms % 1000) / 100)
    return `${s}.${dec}s`
  }

  if (!userId) return null

  return (
    <div className="min-h-screen bg-[#050505] font-mono text-white flex flex-col items-center py-10 px-4">

      {/* Header */}
      <div className="w-full max-w-2xl mb-8">
        <motion.h1
          className="text-2xl font-black tracking-[0.3em] text-[#FF0040]"
          style={{ textShadow: '0 0 25px #FF004060' }}
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
        >
          ARENA PVP
        </motion.h1>
        <p className="text-[10px] tracking-[0.3em] text-white/25 mt-1">
          COMBATE DE CÓDIGO EN TIEMPO REAL · ELO MATCHMAKING
        </p>
      </div>

      {/* Error banner */}
      <AnimatePresence>
        {error && (
          <motion.div
            className="w-full max-w-2xl mb-4 border border-[#FF4444]/50 bg-[#FF4444]/10 px-4 py-3 text-[11px] tracking-wider text-[#FF4444]"
            initial={{ opacity: 0, y: -8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
          >
            ⚠ {error}
          </motion.div>
        )}
      </AnimatePresence>

      <div className="w-full max-w-2xl flex flex-col gap-6">

        {/* ── IDLE phase ── */}
        <AnimatePresence mode="wait">
          {phase === 'idle' && (
            <motion.div
              key="idle"
              className="flex flex-col gap-6"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              {/* Search button */}
              <motion.button
                onClick={handleSearch}
                className="relative w-full py-5 border-2 border-[#FF0040]/60 hover:border-[#FF0040] bg-[#FF0040]/5 hover:bg-[#FF0040]/12 text-[#FF0040] text-sm tracking-[0.3em] font-bold overflow-hidden transition-all duration-200 group"
                whileHover={{ scale: 1.01 }}
                whileTap={{ scale: 0.99 }}
              >
                <ScanLine />
                BUSCAR OPONENTE
                <span className="block text-[9px] tracking-[0.4em] text-[#FF0040]/50 mt-1 font-normal">
                  MATCHMAKING ±200 ELO
                </span>
              </motion.button>

              {/* Inbox */}
              {inbox.length > 0 && (
                <div className="flex flex-col gap-2">
                  <p className="text-[10px] tracking-[0.35em] text-[#7DF9FF]/50 mb-1">
                    DESAFÍOS PENDIENTES — {inbox.length}
                  </p>
                  {inbox.map(item => (
                    <InboxRow key={item.duel_id} item={item} onAccept={handleAcceptInbox} />
                  ))}
                </div>
              )}
            </motion.div>
          )}

          {/* ── SEARCHING phase ── */}
          {phase === 'searching' && (
            <motion.div
              key="searching"
              className="flex flex-col items-center gap-4 py-12"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              <motion.div
                className="w-16 h-16 border-2 border-[#FF0040]/40 border-t-[#FF0040]"
                animate={{ rotate: 360 }}
                transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
              />
              <p className="text-[11px] tracking-[0.4em] text-[#FF0040]/70">ESCANEANDO RED...</p>
            </motion.div>
          )}

          {/* ── MATCHED phase ── */}
          {phase === 'matched' && duel && (
            <motion.div
              key="matched"
              className="flex flex-col gap-6"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              <VSCard duel={duel} myId={userId} />

              {duel.challenge_description && (
                <div className="border border-white/10 bg-[#080808] p-4">
                  <p className="text-[10px] tracking-[0.3em] text-white/30 mb-2">BRIEFING DE MISIÓN</p>
                  <p className="text-xs text-white/70 leading-relaxed">{duel.challenge_description}</p>
                </div>
              )}

              <motion.button
                onClick={handleStartDuel}
                className="w-full py-3 bg-[#FF0040] hover:bg-[#FF0040]/85 text-white text-sm tracking-[0.3em] font-bold transition-all"
                whileTap={{ scale: 0.98 }}
              >
                ¡INICIAR DUELO! ▶
              </motion.button>
            </motion.div>
          )}

          {/* ── DUELING phase ── */}
          {phase === 'dueling' && duel && (
            <motion.div
              key="dueling"
              className="flex flex-col gap-4"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              {/* Timer bar */}
              <div className="flex items-center justify-between border border-[#FF0040]/20 px-4 py-2">
                <span className="text-[10px] tracking-widest text-white/40">{duel.challenge_title}</span>
                <motion.span
                  className="text-sm font-black text-[#FF0040] tabular-nums"
                  animate={{ opacity: [1, 0.6, 1] }}
                  transition={{ duration: 0.8, repeat: Infinity }}
                >
                  ⏱ {formatTime(elapsedMs)}
                </motion.span>
              </div>

              {/* Code editor */}
              <div className="relative border border-[#FF0040]/20 bg-[#080808]">
                <div className="flex items-center gap-2 px-3 py-1.5 border-b border-[#FF0040]/15">
                  <span className="w-2 h-2 rounded-full bg-[#FF0040]/50" />
                  <span className="text-[9px] tracking-widest text-white/25">EDITOR DE COMBATE</span>
                </div>
                <textarea
                  value={code}
                  onChange={e => setCode(e.target.value)}
                  className="w-full h-64 bg-transparent text-[#00FF41] text-xs font-mono p-4 resize-none outline-none leading-relaxed"
                  spellCheck={false}
                  autoCapitalize="none"
                  autoCorrect="off"
                  placeholder="# Escribe tu solución aquí..."
                />
              </div>

              <motion.button
                onClick={handleSubmit}
                disabled={isRunning || !code.trim()}
                className="w-full py-3 border border-[#FF0040] hover:bg-[#FF0040]/15 text-[#FF0040] text-sm tracking-[0.3em] font-bold disabled:opacity-40 disabled:cursor-not-allowed transition-all"
                whileTap={{ scale: isRunning ? 1 : 0.98 }}
              >
                {isRunning ? (
                  <span className="flex items-center justify-center gap-2">
                    <motion.span animate={{ opacity: [1, 0, 1] }} transition={{ duration: 0.6, repeat: Infinity }}>◆</motion.span>
                    EJECUTANDO...
                  </span>
                ) : 'ENVIAR SOLUCIÓN ▶'}
              </motion.button>
            </motion.div>
          )}

          {/* ── SUBMITTED phase (waiting for rival) ── */}
          {phase === 'submitted' && (
            <motion.div
              key="submitted"
              className="flex flex-col items-center gap-4 py-10"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              <p className="text-sm tracking-[0.3em] text-[#FFD700]">SOLUCIÓN ENVIADA</p>
              <motion.p
                className="text-[10px] tracking-[0.35em] text-white/40"
                animate={{ opacity: [0.4, 0.8, 0.4] }}
                transition={{ duration: 2, repeat: Infinity }}
              >
                ESPERANDO AL RIVAL...
              </motion.p>
              {submitResult && (
                <div className="text-[10px] text-white/30 mt-2 text-center">
                  <span>{submitResult.correct ? '✓ CORRECTO' : '✗ INCORRECTO'}</span>
                  <span className="ml-4">⏱ {submitResult.execution_time_ms.toFixed(0)}ms</span>
                </div>
              )}
              <button
                onClick={handleReset}
                className="text-[10px] tracking-widest text-white/25 hover:text-white/50 transition-colors mt-4"
              >
                VOLVER A LA ARENA
              </button>
            </motion.div>
          )}

          {/* ── RESULT phase ── */}
          {phase === 'result' && submitResult && (
            <motion.div key="result" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
              <ResultScreen submitResult={submitResult} myId={userId} onReset={handleReset} />
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  )
}
