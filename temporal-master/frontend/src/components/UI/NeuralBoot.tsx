'use client'

import { useEffect, useRef, useState, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

// ─── Mensajes de estado durante el arranque ───────────────────────────────────

const STATUS_MESSAGES = [
  { text: 'INICIANDO SINAPSIS...',         delay: 0    },
  { text: 'BYPASS DE CÓRTEX VISUAL...',    delay: 850  },
  { text: 'SINCRONIZANDO CON EL NEXO...', delay: 1750 },
  { text: '[ ENLACE ESTABLECIDO ]',        delay: 2650 },
]

const TOTAL_MS   = 3500   // duración total de la secuencia
const FADE_AT_MS = 3100   // cuándo empieza el fade-out

// Charset: ASCII técnico + katakana lite + binario
const CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789アイウエオカサタナハマ@#$&*{}[]<>|'

// ─── Props ────────────────────────────────────────────────────────────────────

interface Props {
  username?: string
  onComplete: () => void
}

// ─── Matrix rain (canvas) ─────────────────────────────────────────────────────

function MatrixCanvas() {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const resize = () => {
      canvas.width  = window.innerWidth
      canvas.height = window.innerHeight
    }
    resize()
    window.addEventListener('resize', resize)

    const fontSize = 13
    let cols = Math.floor(canvas.width / fontSize)
    let drops = Array.from({ length: cols }, () => Math.floor(Math.random() * -50))

    const draw = () => {
      // Recalcular si resize cambió las columnas
      const newCols = Math.floor(canvas.width / fontSize)
      if (newCols !== cols) {
        cols  = newCols
        drops = Array.from({ length: cols }, () => Math.floor(Math.random() * -50))
      }

      ctx.fillStyle = 'rgba(0,0,0,0.055)'
      ctx.fillRect(0, 0, canvas.width, canvas.height)

      ctx.font = `${fontSize}px monospace`

      for (let i = 0; i < drops.length; i++) {
        const y = drops[i] * fontSize
        if (y < 0) { drops[i]++; continue }

        const char = CHARS[Math.floor(Math.random() * CHARS.length)]

        // Cabeza: blanco brillante; cuerpo: verde neón; cola implícita por fade
        const isHead = drops[i] % 28 < 2
        ctx.fillStyle = isHead ? '#FFFFFF' : '#00FF41'
        ctx.shadowColor = isHead ? '#FFFFFF' : '#00FF41'
        ctx.shadowBlur  = isHead ? 8 : 4
        ctx.fillText(char, i * fontSize, y)

        // Reiniciar columna aleatoriamente al llegar al fondo
        if (y > canvas.height && Math.random() > 0.972) {
          drops[i] = 0
        }
        drops[i]++
      }
      ctx.shadowBlur = 0
    }

    const id = setInterval(draw, 42)  // ~24 fps — suficiente, no sobrecarga el editor
    return () => {
      clearInterval(id)
      window.removeEventListener('resize', resize)
    }
  }, [])

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 z-10"
      aria-hidden="true"
    />
  )
}

// ─── Componente principal ─────────────────────────────────────────────────────

type Phase = 'waiting' | 'booting' | 'fading'

export default function NeuralBoot({ username, onComplete }: Props) {
  const [phase, setPhase]               = useState<Phase>('waiting')
  const [currentMsg, setCurrentMsg]     = useState('')
  const [msgKey, setMsgKey]             = useState(0)
  const timersRef                       = useRef<ReturnType<typeof setTimeout>[]>([])

  // ── Audio (instanciados en ref para evitar re-renders y problemas SSR) ───────
  const bootSoundRef = useRef<HTMLAudioElement | null>(null)
  const dataSoundRef = useRef<HTMLAudioElement | null>(null)

  useEffect(() => {
    bootSoundRef.current = new Audio('/sounds/boot-sequence.mp3')
    dataSoundRef.current = new Audio('/sounds/data-stream.mp3')
    bootSoundRef.current.volume = 0.8
    dataSoundRef.current.volume = 0.5
  }, [])

  const stopAudio = () => {
    if (dataSoundRef.current) {
      dataSoundRef.current.pause()
      dataSoundRef.current.currentTime = 0
    }
    if (bootSoundRef.current) {
      bootSoundRef.current.pause()
      bootSoundRef.current.currentTime = 0
    }
  }

  const clearTimers = () => timersRef.current.forEach(clearTimeout)

  const handleConnect = useCallback(() => {
    setPhase('booting')

    // Reproducir sonido de arranque inmediatamente
    bootSoundRef.current?.play().catch(() => {/* autoplay policy — silencioso */})

    // Data stream con 200ms de retraso
    timersRef.current.push(
      setTimeout(() => {
        dataSoundRef.current?.play().catch(() => {})
      }, 200)
    )

    // Mensajes en cascada
    STATUS_MESSAGES.forEach(({ text, delay }) => {
      timersRef.current.push(
        setTimeout(() => {
          setCurrentMsg(text)
          setMsgKey(k => k + 1)
        }, delay)
      )
    })

    // Fade-out
    timersRef.current.push(
      setTimeout(() => setPhase('fading'), FADE_AT_MS)
    )

    // Detener audio y navegar
    timersRef.current.push(
      setTimeout(() => {
        stopAudio()
        onComplete()
      }, TOTAL_MS)
    )
  }, [onComplete])

  useEffect(() => () => {
    clearTimers()
    stopAudio()
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  return (
    <div
      className={[
        'fixed inset-0 z-[9998] bg-black font-mono select-none',
        phase === 'fading' ? 'opacity-0 transition-opacity duration-500 ease-in' : 'opacity-100',
      ].join(' ')}
    >
      {/* ── CRT Scanlines (siempre presentes) ──────────────────────────────── */}
      <div
        className="fixed inset-0 z-[9999] pointer-events-none"
        style={{
          backgroundImage:
            'repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,0.10) 2px,rgba(0,0,0,0.10) 4px)',
        }}
        aria-hidden="true"
      />

      {/* ── Matrix rain (solo en booting / fading) ─────────────────────────── */}
      {phase !== 'waiting' && <MatrixCanvas />}

      {/* ── Contenido central ──────────────────────────────────────────────── */}
      <div className="fixed inset-0 z-[9999] flex flex-col items-center justify-center pointer-events-none">

        {/* ── WAITING: botón de conexión ─────────────────────────────────── */}
        <AnimatePresence>
          {phase === 'waiting' && (
            <motion.div
              key="idle"
              className="flex flex-col items-center gap-8 pointer-events-auto"
              initial={{ opacity: 0, scale: 0.92 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 1.06, transition: { duration: 0.2 } }}
              transition={{ duration: 0.5 }}
            >
              {/* Header */}
              <div className="text-center space-y-1">
                <p className="text-[#00FF41]/20 text-[9px] tracking-[0.7em] uppercase">
                  ENIGMA // PROTOCOLO NEURONAL // v4.2.1
                </p>
                {username && (
                  <p className="text-[#00FF41]/35 text-[10px] tracking-[0.4em] uppercase">
                    OPERADOR IDENTIFICADO:{' '}
                    <span className="text-[#00FF41]/60">{username.toUpperCase()}</span>
                  </p>
                )}
              </div>

              {/* Núcleo pulsante decorativo */}
              <div className="relative flex items-center justify-center">
                <motion.div
                  className="w-24 h-24 rounded-full border border-[#00FF41]/10"
                  animate={{ scale: [1, 1.15, 1], opacity: [0.2, 0.5, 0.2] }}
                  transition={{ duration: 3, repeat: Infinity, ease: 'easeInOut' }}
                />
                <motion.div
                  className="absolute w-16 h-16 rounded-full border border-[#00FF41]/20"
                  animate={{ scale: [1, 1.2, 1], opacity: [0.3, 0.7, 0.3] }}
                  transition={{ duration: 2.2, repeat: Infinity, ease: 'easeInOut', delay: 0.4 }}
                />
                <div
                  className="absolute w-4 h-4 rounded-full bg-[#00FF41]"
                  style={{ boxShadow: '0 0 16px #00FF41, 0 0 40px #00FF4160' }}
                />
              </div>

              {/* Botón principal */}
              <button
                onClick={handleConnect}
                className="border-2 border-green-500 text-green-500 hover:bg-green-500 hover:text-black
                           font-mono text-xl md:text-2xl px-10 md:px-14 py-5 tracking-[0.28em] uppercase
                           transition-all duration-300
                           shadow-[0_0_40px_rgba(0,255,0,0.35)]
                           hover:shadow-[0_0_80px_rgba(0,255,0,0.75)]
                           active:scale-95"
              >
                [ ESTABLECER ENLACE NEURONAL ]
              </button>

              <p className="text-[#00FF41]/15 text-[9px] tracking-[0.6em]">
                PRESIONE EL BOTÓN PARA INICIAR LA SECUENCIA
              </p>
            </motion.div>
          )}
        </AnimatePresence>

        {/* ── BOOTING / FADING: mensaje de estado central ────────────────── */}
        <AnimatePresence mode="wait">
          {phase !== 'waiting' && currentMsg && (
            <motion.div
              key={msgKey}
              className="text-center px-8"
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -8 }}
              transition={{ duration: 0.22 }}
            >
              <p
                className={[
                  'font-mono tracking-[0.3em] text-base md:text-lg',
                  currentMsg.includes('ENLACE')
                    ? 'text-[#00FF41] font-black'
                    : 'text-[#00FF41]/70',
                ].join(' ')}
                style={
                  currentMsg.includes('ENLACE')
                    ? { textShadow: '0 0 20px #00FF41, 0 0 50px #00FF4170' }
                    : { textShadow: '0 0 8px #00FF4150' }
                }
              >
                {currentMsg}
              </p>
            </motion.div>
          )}
        </AnimatePresence>

      </div>
    </div>
  )
}
