'use client'

/**
 * TheInfiniteLooper — Componente de Boss Fight del Módulo Bucles.
 *
 * Fases:
 *   intro    — presentación animada del jefe, botón "INICIAR COMBATE"
 *   fighting — editor de código + grid de corrupción en tiempo real
 *   victory  — implosión de celdas + ráfaga azul de XP
 *   defeat   — traceback animado con texto rojo
 *
 * El "grid de corrupción" es una cuadrícula 8×6 donde las filas se
 * corrompen de abajo hacia arriba conforme cae la integridad del sistema.
 */

import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { motion, AnimatePresence, useAnimation } from 'framer-motion'
import dynamic from 'next/dynamic'

const MonacoEditor = dynamic(() => import('@monaco-editor/react'), { ssr: false })

// ─── Constantes ────────────────────────────────────────────────────────────────

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000'

const GRID_COLS = 8
const GRID_ROWS = 6
const BOSS_DURATION_MS = 45_000   // 45 s para corromper todo
const TICK_MS = 100               // intervalo del timer

const INITIAL_CODE = `def factorial_iterativo(n):
    # El ∞ LOOPER ejecuta: while True: contador += 1
    # Tu misión: detenerlo con un bucle FOR acotado.
    # Retorna n! (n factorial) usando for, no recursion.
    # Ejemplo: factorial_iterativo(5) → 120
    pass

n = int(input())
print(factorial_iterativo(n))
`

// Fragmentos de "código corrupto" que se muestran en las celdas
const CORRUPT_FRAGMENTS = [
  'while True:', '∞', 'SyntaxError', 'counter++', '0xFF',
  'LOOP', 'NaN', 'OverflowError', '>>>>', 'null',
  'undefined', 'segfault', '0x00', 'inf', '///',
  'BREAK?', 'panic!', 'GOTO 0', '????', '!#!',
]

// Traceback de derrota (texto rojo estilo Python)
const DEFEAT_TRACEBACK = [
  'Traceback (most recent call last):',
  '  File "battle.py", line 42, in <module>',
  '    sistema.resist(jugador.code)',
  '  File "looper_core.py", line 1, in resist',
  '    while True: contador += 1  # HA HA HA',
  'RuntimeError: Stack overflow — EL LOOPER GANA',
  '',
  '∞ LOOPER: "¡Tus bucles no son suficientes!"',
  '>>> Sistema comprometido al 100% <<<',
]

type Phase = 'intro' | 'fighting' | 'victory' | 'defeat'

interface BossResult {
  success: boolean
  xp_earned: number
  new_total_xp: number
  new_level: number
  stdout: string
  stderr: string
  execution_time_ms: number
}

// ─── Sub-componentes ───────────────────────────────────────────────────────────

/** Celda corrupta del grid */
function CorruptedCell({ col, row, intensity }: { col: number; row: number; intensity: number }) {
  const fragment = CORRUPT_FRAGMENTS[(col * 3 + row * 7 + col * row) % CORRUPT_FRAGMENTS.length]
  const glitchDelay = ((col + row * 2) % 8) * 0.12

  return (
    <motion.div
      className="relative overflow-hidden flex items-center justify-center"
      style={{
        background: `rgba(${Math.floor(180 * intensity)}, 0, 0, ${0.3 + intensity * 0.5})`,
        border: `1px solid rgba(255, 0, 0, ${0.2 + intensity * 0.6})`,
        boxShadow: intensity > 0.7 ? `inset 0 0 8px rgba(255,0,0,0.4)` : 'none',
      }}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.3, delay: glitchDelay }}
    >
      <motion.span
        className="font-mono text-xs select-none"
        style={{ color: `rgba(255, ${Math.floor(60 * (1 - intensity))}, 0, ${0.6 + intensity * 0.4})` }}
        animate={{
          opacity: [0.4, 1, 0.4],
          x: [0, (col % 2 === 0 ? 1 : -1) * intensity * 2, 0],
        }}
        transition={{ duration: 0.4 + glitchDelay, repeat: Infinity }}
      >
        {fragment}
      </motion.span>
      {/* Scanline de corrupción */}
      <motion.div
        className="absolute inset-0 pointer-events-none"
        style={{
          background: 'repeating-linear-gradient(0deg, transparent 0px, transparent 2px, rgba(255,0,0,0.06) 2px, rgba(255,0,0,0.06) 3px)',
        }}
      />
    </motion.div>
  )
}

/** Celda intacta del grid (zona del jugador) */
function IntactCell({ col: _col, row }: { col: number; row: number }) {
  const isDefenseLine = row === GRID_ROWS - 1
  const isBossZone = row <= 1

  let bg = 'rgba(0, 20, 0, 0.4)'
  let border = 'rgba(0, 255, 65, 0.15)'
  if (isBossZone) { bg = 'rgba(20, 0, 0, 0.4)'; border = 'rgba(255, 0, 0, 0.2)' }
  if (isDefenseLine) { bg = 'rgba(0, 15, 30, 0.6)'; border = 'rgba(0, 120, 255, 0.3)' }

  return (
    <div
      style={{
        background: bg,
        border: `1px solid ${border}`,
      }}
    />
  )
}

/** Partícula azul de victoria */
interface VictoryParticle { id: number; x: number; y: number; tx: number; ty: number; delay: number; size: number }

function VictoryBurst({ visible }: { visible: boolean }) {
  const particles = useMemo<VictoryParticle[]>(() => {
    return Array.from({ length: 40 }, (_, i) => ({
      id: i,
      x: 50 + ((i * 7) % 20) - 10,
      y: 50 + ((i * 5) % 20) - 10,
      tx: 50 + ((i * 13) % 80) - 40,
      ty: 2 + ((i * 3) % 8),
      delay: (i % 10) * 0.04,
      size: 3 + (i % 4),
    }))
  }, [])

  return (
    <AnimatePresence>
      {visible && (
        <div className="fixed inset-0 pointer-events-none overflow-hidden" style={{ zIndex: 70 }}>
          {particles.map((p) => (
            <motion.div
              key={p.id}
              className="absolute rounded-full"
              style={{
                width: p.size,
                height: p.size,
                background: '#0080FF',
                boxShadow: `0 0 ${p.size * 2}px #0080FF, 0 0 ${p.size * 4}px #0040FF60`,
                left: `${p.x}vw`,
                top: `${p.y}vh`,
              }}
              initial={{ opacity: 1, scale: 1, x: 0, y: 0 }}
              animate={{
                opacity: [1, 1, 0.6, 0],
                scale: [1, 1.4, 0.6],
                x: `${p.tx - p.x}vw`,
                y: `${p.ty - p.y}vh`,
              }}
              transition={{ duration: 0.9, delay: p.delay, ease: 'easeOut' }}
            />
          ))}
        </div>
      )}
    </AnimatePresence>
  )
}

// ─── Componente principal ──────────────────────────────────────────────────────

interface Props {
  userId: string
  onVictory?: (_result: BossResult) => void
  onDefeat?: () => void
}

export default function TheInfiniteLooper({ userId, onVictory, onDefeat }: Props) {
  const [phase, setPhase] = useState<Phase>('intro')
  const [integrity, setIntegrity] = useState(100)           // 0–100
  const [code, setCode] = useState(INITIAL_CODE)
  const [isExecuting, setIsExecuting] = useState(false)
  const [bossResult, setBossResult] = useState<BossResult | null>(null)
  const [tracebackLine, setTracebackLine] = useState(0)     // para animación escalonada
  const [victoryBurst, setVictoryBurst] = useState(false)
  const [implodingCells, setImplodingCells] = useState<Set<string>>(new Set())
  const [stderr, setStderr] = useState('')

  const timerRef  = useRef<ReturnType<typeof setInterval> | null>(null)
  const endMsRef  = useRef<number>(0)
  const containerCtrl = useAnimation()

  // Cuántas filas están corrompidas (de abajo hacia arriba)
  const corruptedRows = Math.ceil(((100 - integrity) / 100) * GRID_ROWS)

  // ── Timer de integridad (endTime-based — persiste aunque la pestaña se minimice) ──
  //
  // En lugar de decrementar un contador por tick, guardamos el instante de
  // finalización (endMs) en localStorage y calculamos el tiempo restante como
  // endMs - Date.now() en cada frame.  Así, si el usuario minimiza la pestaña
  // y el intervalo se ralentiza (throttling del navegador), el tiempo real sigue
  // corriendo y el estado se corrige en cuanto la pestaña vuelve a estar activa.

  const BOSS_STORAGE_KEY = 'boss_fight_end_ms'

  const startTimer = useCallback((resumeEndMs?: number) => {
    if (timerRef.current) return
    const endMs = resumeEndMs ?? Date.now() + BOSS_DURATION_MS
    endMsRef.current = endMs
    if (!resumeEndMs) localStorage.setItem(BOSS_STORAGE_KEY, String(endMs))

    timerRef.current = setInterval(() => {
      const remaining = endMsRef.current - Date.now()
      if (remaining <= 0) {
        clearInterval(timerRef.current!)
        timerRef.current = null
        localStorage.removeItem(BOSS_STORAGE_KEY)
        setIntegrity(0)
        setPhase('defeat')
        return
      }
      setIntegrity(+(remaining / BOSS_DURATION_MS * 100).toFixed(2))
    }, TICK_MS)
  }, []) // eslint-disable-line react-hooks/exhaustive-deps

  const stopTimer = useCallback(() => {
    if (timerRef.current) {
      clearInterval(timerRef.current)
      timerRef.current = null
    }
    localStorage.removeItem(BOSS_STORAGE_KEY)
  }, []) // eslint-disable-line react-hooks/exhaustive-deps

  // Reanudar sesión activa si el usuario refresca durante el combate
  useEffect(() => {
    const stored = localStorage.getItem(BOSS_STORAGE_KEY)
    if (!stored) return
    const endMs = Number(stored)
    const remaining = endMs - Date.now()
    if (remaining > 0) {
      setIntegrity(+(remaining / BOSS_DURATION_MS * 100).toFixed(2))
      setPhase('fighting')
      startTimer(endMs)
    } else {
      localStorage.removeItem(BOSS_STORAGE_KEY)
    }
  }, [startTimer]) // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => () => stopTimer(), [stopTimer])

  // ── Pantalla de sacudida ───────────────────────────────────────────────────
  const triggerShake = useCallback(async (intensity: 'soft' | 'hard') => {
    const amp = intensity === 'hard' ? 10 : 4
    await containerCtrl.start({
      x: [0, -amp, amp, -amp * 0.6, amp * 0.6, 0],
      transition: { duration: 0.4 },
    })
    containerCtrl.set({ x: 0 })
  }, [containerCtrl])

  // ── Ejecución del código ───────────────────────────────────────────────────
  const handleExecute = useCallback(async () => {
    if (isExecuting || phase !== 'fighting') return
    setIsExecuting(true)
    setStderr('')
    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), 12_000)
    try {
      const res = await fetch(`${API_BASE}/api/v1/boss/execute`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, source_code: code }),
        signal: controller.signal,
      })
      const data: BossResult = await res.json()
      setBossResult(data)

      if (data.success) {
        stopTimer()
        // Implosión de celdas
        const all = new Set<string>()
        for (let r = 0; r < GRID_ROWS; r++)
          for (let c = 0; c < GRID_COLS; c++)
            all.add(`${r}-${c}`)
        setImplodingCells(all)
        setTimeout(() => {
          setVictoryBurst(true)
          setPhase('victory')
          onVictory?.(data)
        }, 600)
        setTimeout(() => setVictoryBurst(false), 2500)
      } else {
        setStderr(data.stderr || 'Salida incorrecta.')
        triggerShake('hard')
        // Acelerar la corrupción como penalización
        setIntegrity((prev) => Math.max(0, prev - 8))
      }
    } catch (err) {
      const isAbort = err instanceof DOMException && err.name === 'AbortError'
      setStderr(isAbort ? '[ FALLO NEURONAL: TIEMPO LÍMITE EXCEDIDO ]' : 'Error de conexión con el servidor.')
      triggerShake('soft')
    } finally {
      clearTimeout(timeoutId)
      setIsExecuting(false)
    }
  }, [code, isExecuting, onVictory, phase, stopTimer, triggerShake, userId])

  // ── Animación del traceback en derrota ────────────────────────────────────
  useEffect(() => {
    if (phase !== 'defeat') return
    stopTimer()
    onDefeat?.()
    let i = 0
    const id = setInterval(() => {
      i++
      setTracebackLine(i)
      if (i >= DEFEAT_TRACEBACK.length) clearInterval(id)
    }, 280)
    return () => clearInterval(id)
  }, [phase, stopTimer, onDefeat])

  // ── Intensidad de la celda corrupta (más intensa más abajo) ───────────────
  const cellIntensity = (row: number) => {
    const distFromBottom = GRID_ROWS - 1 - row
    return Math.max(0.2, 1 - distFromBottom * 0.15)
  }

  // ─── Render helpers ────────────────────────────────────────────────────────

  const integrityColor = integrity > 60 ? '#00FF41' : integrity > 30 ? '#FFD700' : '#FF4444'

  // ─── Fases ────────────────────────────────────────────────────────────────

  if (phase === 'intro') {
    return (
      <div className="min-h-screen bg-black flex flex-col items-center justify-center p-8" style={{
        background: 'radial-gradient(ellipse at center, #1a0000 0%, #000 70%)',
      }}>
        <VictoryBurst visible={false} />

        {/* Título pulsante */}
        <motion.div
          className="text-center mb-12"
          initial={{ opacity: 0, y: -40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <motion.div
            className="font-mono font-black tracking-[0.2em] leading-none"
            style={{
              fontSize: 'clamp(2.5rem, 8vw, 5rem)',
              color: '#FF4444',
              textShadow: '0 0 30px #FF4444, 0 0 80px #FF444440',
            }}
            animate={{
              textShadow: [
                '0 0 30px #FF4444, 0 0 80px #FF444440',
                '0 0 60px #FF4444, 0 0 120px #FF4444',
                '0 0 30px #FF4444, 0 0 80px #FF444440',
              ],
            }}
            transition={{ duration: 1.2, repeat: Infinity }}
          >
            ∞ LOOPER
          </motion.div>
          <motion.div
            className="mt-3 font-mono text-red-400/70 tracking-[0.3em] text-sm"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
          >
            MÓDULO: BUCLES — JEFE FINAL
          </motion.div>
        </motion.div>

        {/* Descripción */}
        <motion.div
          className="max-w-lg text-center font-mono text-sm text-gray-400 leading-relaxed mb-10 px-4"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8 }}
        >
          <p className="mb-3">
            El <span className="text-red-400 font-bold">∞ LOOPER</span> ejecuta{' '}
            <code className="bg-red-900/40 text-red-300 px-1 rounded">while True: contador += 1</code>{' '}
            sin parar, corrompiendo el sistema línea a línea.
          </p>
          <p>
            Escribe <span className="text-green-400 font-semibold">factorial_iterativo(n)</span> usando un{' '}
            <code className="bg-green-900/40 text-green-300 px-1 rounded">for</code> acotado
            para detenerlo antes de que la integridad llegue a 0.
          </p>
          <p className="mt-4 text-yellow-400 font-semibold">
            Tienes 45 segundos. Recompensa: 1 500 XP.
          </p>
        </motion.div>

        {/* Botón */}
        <motion.button
          className="font-mono font-black tracking-[0.2em] px-10 py-4 text-lg border-2 border-red-500 text-red-400"
          style={{
            background: 'rgba(255, 0, 0, 0.1)',
            boxShadow: '0 0 20px rgba(255,0,0,0.3)',
          }}
          whileHover={{
            scale: 1.04,
            boxShadow: '0 0 40px rgba(255,0,0,0.6)',
            backgroundColor: 'rgba(255,0,0,0.2)',
          }}
          whileTap={{ scale: 0.97 }}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.2 }}
          onClick={() => { setPhase('fighting'); startTimer() }}
        >
          ⚔ INICIAR COMBATE
        </motion.button>
      </div>
    )
  }

  if (phase === 'defeat') {
    return (
      <div className="min-h-screen bg-black flex flex-col items-center justify-center p-8"
        style={{ background: 'radial-gradient(ellipse at center, #1a0000 0%, #000 70%)' }}
      >
        <motion.div
          className="w-full max-w-2xl font-mono text-sm"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          <div className="text-red-500 font-bold text-xl mb-6 tracking-widest text-center">
            — SISTEMA COMPROMETIDO —
          </div>
          <div className="bg-gray-950 border border-red-900 rounded p-6 space-y-1">
            {DEFEAT_TRACEBACK.slice(0, tracebackLine).map((line, i) => (
              <motion.div
                key={i}
                className="text-red-400"
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.2 }}
                style={{ fontFamily: 'monospace', whiteSpace: 'pre' }}
              >
                {line || '\u00A0'}
              </motion.div>
            ))}
            {tracebackLine < DEFEAT_TRACEBACK.length && (
              <motion.span
                className="text-red-500"
                animate={{ opacity: [1, 0] }}
                transition={{ duration: 0.5, repeat: Infinity }}
              >▌</motion.span>
            )}
          </div>

          {tracebackLine >= DEFEAT_TRACEBACK.length && (
            <motion.div
              className="mt-8 text-center"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.5 }}
            >
              <a
                href="/boss"
                className="font-mono font-bold px-8 py-3 border border-red-500 text-red-400 hover:bg-red-900/30 transition-colors"
              >
                REINTENTAR BATALLA
              </a>
            </motion.div>
          )}
        </motion.div>
      </div>
    )
  }

  if (phase === 'victory') {
    return (
      <div className="min-h-screen bg-black flex flex-col items-center justify-center p-8"
        style={{ background: 'radial-gradient(ellipse at center, #000a1a 0%, #000 70%)' }}
      >
        <VictoryBurst visible={victoryBurst} />
        <motion.div
          className="text-center"
          initial={{ scale: 0.5, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ type: 'spring', stiffness: 200, damping: 18 }}
        >
          <div
            className="font-mono font-black tracking-[0.15em] text-5xl"
            style={{ color: '#0080FF', textShadow: '0 0 40px #0080FF, 0 0 100px #0040FF' }}
          >
            VICTORIA
          </div>
          <div className="mt-3 font-mono text-blue-400 tracking-widest text-sm">
            ∞ LOOPER DERROTADO
          </div>
          {bossResult && (
            <motion.div
              className="mt-8 font-mono space-y-2"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
            >
              <div className="text-2xl text-blue-300 font-bold">
                +{bossResult.xp_earned} XP
              </div>
              <div className="text-sm text-gray-400">
                Total: {bossResult.new_total_xp} XP · Nivel {bossResult.new_level}
              </div>
              <div className="text-xs text-green-400 mt-2">
                Salida: {bossResult.stdout.trim()}
              </div>
            </motion.div>
          )}
          <motion.div
            className="mt-10"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1.2 }}
          >
            <a
              href="/misiones"
              className="font-mono font-bold px-8 py-3 border-2 border-blue-500 text-blue-400 hover:bg-blue-900/30 transition-colors"
            >
              VOLVER AL MAPA
            </a>
          </motion.div>
        </motion.div>
      </div>
    )
  }

  // ─── Fase: fighting ────────────────────────────────────────────────────────

  return (
    <motion.div
      className="min-h-screen bg-black flex flex-col"
      style={{ background: '#050505' }}
      animate={containerCtrl}
    >
      <VictoryBurst visible={victoryBurst} />

      {/* ── Header: barra de integridad ── */}
      <div className="flex items-center justify-between px-6 py-3 border-b border-gray-900">
        <div className="font-mono font-black text-red-500 tracking-[0.15em] text-lg">
          ∞ LOOPER
        </div>

        <div className="flex-1 mx-6">
          <div className="flex items-center gap-3">
            <span className="font-mono text-xs text-gray-500 shrink-0">INTEGRIDAD</span>
            <div className="flex-1 h-3 bg-gray-900 rounded overflow-hidden border border-gray-800">
              <motion.div
                className="h-full rounded"
                style={{ background: integrityColor }}
                animate={{ width: `${integrity}%` }}
                transition={{ duration: 0.1 }}
              />
            </div>
            <span className="font-mono text-xs shrink-0" style={{ color: integrityColor }}>
              {Math.ceil(integrity)}%
            </span>
          </div>
        </div>

        <div className="font-mono text-xs text-gray-600 tracking-widest">
          MÓDULO: BUCLES
        </div>
      </div>

      {/* ── Body ── */}
      <div className="flex flex-1 overflow-hidden">

        {/* Panel izquierdo: grid de corrupción */}
        <div className="w-72 shrink-0 flex flex-col border-r border-gray-900 p-4 gap-4">
          <div className="font-mono text-xs text-gray-600 tracking-widest text-center">
            ESTADO DEL SISTEMA
          </div>

          {/* Grid 8×6 */}
          <div
            className="grid gap-0.5"
            style={{
              gridTemplateColumns: `repeat(${GRID_COLS}, 1fr)`,
              gridTemplateRows: `repeat(${GRID_ROWS}, 1fr)`,
              aspectRatio: `${GRID_COLS}/${GRID_ROWS}`,
            }}
          >
            {Array.from({ length: GRID_ROWS }, (_, rowIdx) =>
              Array.from({ length: GRID_COLS }, (_, colIdx) => {
                // Las filas corrompidas van de abajo hacia arriba
                const isCorrupted = rowIdx >= GRID_ROWS - corruptedRows

                const key = `${rowIdx}-${colIdx}`
                const isImploding = implodingCells.has(key)

                if (isImploding) {
                  return (
                    <motion.div
                      key={key}
                      style={{ background: '#0080FF', border: '1px solid #0040FF' }}
                      animate={{ scale: 0, opacity: 0 }}
                      transition={{ duration: 0.5, delay: ((rowIdx * GRID_COLS + colIdx) % 12) * 0.04 }}
                    />
                  )
                }

                if (isCorrupted) {
                  return (
                    <CorruptedCell
                      key={key}
                      col={colIdx}
                      row={rowIdx}
                      intensity={cellIntensity(rowIdx)}
                    />
                  )
                }

                return <IntactCell key={key} col={colIdx} row={rowIdx} />
              })
            )}
          </div>

          {/* Leyenda de zonas */}
          <div className="font-mono text-xs space-y-1 mt-2">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 border border-red-500/40" style={{ background: 'rgba(100,0,0,0.4)' }} />
              <span className="text-gray-600">Zona del LOOPER (fila 0–1)</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 border border-green-500/20" style={{ background: 'rgba(0,20,0,0.4)' }} />
              <span className="text-gray-600">Zona de batalla</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 border border-blue-500/30" style={{ background: 'rgba(0,15,30,0.6)' }} />
              <span className="text-gray-600">Línea de defensa</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3" style={{ background: 'rgba(180,0,0,0.6)', border: '1px solid rgba(255,0,0,0.5)' }} />
              <span className="text-red-500/70">Corrompido</span>
            </div>
          </div>

          {/* Consejo */}
          <div className="mt-auto border border-yellow-900/40 bg-yellow-950/20 rounded p-3">
            <div className="font-mono text-xs text-yellow-500/80 leading-relaxed">
              <strong>Pista:</strong> usa <code className="bg-yellow-900/40 px-0.5 rounded">for i in range(1, n+1)</code> y
              multiplica en cada iteración.
            </div>
          </div>
        </div>

        {/* Panel central: editor */}
        <div className="flex-1 flex flex-col">
          <div className="flex items-center justify-between px-4 py-2 border-b border-gray-900">
            <span className="font-mono text-xs text-gray-600">factorial_iterativo.py</span>
            <span className="font-mono text-xs text-gray-700">
              Test: <code className="text-gray-500">factorial_iterativo(7) → 5040</code>
            </span>
          </div>

          <div className="flex-1">
            <MonacoEditor
              height="100%"
              defaultLanguage="python"
              value={code}
              onChange={(v) => setCode(v ?? '')}
              theme="vs-dark"
              options={{
                fontSize: 14,
                fontFamily: "'Fira Code', 'Cascadia Code', monospace",
                minimap: { enabled: false },
                scrollBeyondLastLine: false,
                lineNumbers: 'on',
                padding: { top: 16 },
              }}
            />
          </div>

          {/* Salida / errores */}
          {(bossResult || stderr) && (
            <div className="border-t border-gray-900 px-4 py-3 font-mono text-sm max-h-36 overflow-y-auto">
              {stderr ? (
                <div className="text-red-400 whitespace-pre-wrap">{stderr}</div>
              ) : bossResult && (
                <div className="space-y-1">
                  <div className="text-gray-500 text-xs">SALIDA:</div>
                  <div className="text-green-400">{bossResult.stdout}</div>
                  <div className="text-gray-600 text-xs">
                    {bossResult.execution_time_ms.toFixed(1)} ms
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Panel derecho: botón ejecutar + info */}
        <div className="w-52 shrink-0 flex flex-col border-l border-gray-900 p-4 gap-4">
          <motion.button
            className="font-mono font-black tracking-widest py-4 w-full text-sm border-2"
            style={{
              borderColor: '#00FF41',
              color: '#00FF41',
              background: 'rgba(0,255,65,0.08)',
            }}
            whileHover={{ background: 'rgba(0,255,65,0.18)', boxShadow: '0 0 20px rgba(0,255,65,0.4)' }}
            whileTap={{ scale: 0.97 }}
            onClick={handleExecute}
            disabled={isExecuting}
          >
            {isExecuting ? '...' : '▶ EJECUTAR'}
          </motion.button>

          <div className="font-mono text-xs space-y-3 text-gray-600">
            <div>
              <div className="text-gray-500 mb-1">RECOMPENSA</div>
              <div className="text-yellow-400 font-bold text-base">1 500 XP</div>
            </div>
            <div>
              <div className="text-gray-500 mb-1">ENTRADA DE PRUEBA</div>
              <code className="text-gray-400">7</code>
            </div>
            <div>
              <div className="text-gray-500 mb-1">SALIDA ESPERADA</div>
              <code className="text-green-500">5040</code>
            </div>
            <div>
              <div className="text-gray-500 mb-1">TIEMPO RESTANTE</div>
              <div className="text-red-400 font-bold">
                {Math.ceil((integrity / 100) * (BOSS_DURATION_MS / 1000))}s
              </div>
            </div>
          </div>

          <div className="mt-auto">
            <a href="/misiones" className="font-mono text-xs text-gray-700 hover:text-gray-500 transition-colors">
              ← Abandonar
            </a>
          </div>
        </div>
      </div>
    </motion.div>
  )
}
