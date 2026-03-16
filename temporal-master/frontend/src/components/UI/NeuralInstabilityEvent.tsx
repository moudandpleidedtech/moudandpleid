'use client'

import { useEffect, useState, useRef, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

// ─── Duraciones ───────────────────────────────────────────────────────────────

const INSTABILITY_MS = 1200   // duración del evento visual
const DAKI_VISIBLE_MS = 4500  // tiempo que la notificación permanece visible
const FIRST_DELAY_MS  = 25_000 + Math.random() * 15_000  // primer evento: 25-40 s

// ─── Contenido narrativo ──────────────────────────────────────────────────────

const DAKI_MESSAGES = [
  'Pico de estrés detectado. Ritmo cardíaco a 110 BPM. Ajustando amortiguadores sinápticos... Enlace estabilizado.',
  'Desincronización del córtex visual. Compensando pérdida de paquetes... Listo, operador.',
  'El firewall enemigo intentó una inyección de ruido. Filtrando estímulos nocivos. Respira profundo.',
  'Latencia sináptica anómala: 48ms. Recalibrando canal neuronal... Parámetros restaurados.',
  'Fluctuación de voltaje en el enlace. Activando redundancia de protocolo. Continúa, operador.',
]

const ALERT_TEXTS = [
  '[ ALERTA: FLUCTUACIÓN DE ENLACE ]',
  '[ WARNING: SYNAPTIC_OVERFLOW ]',
  '[ NEXO :: SIGNAL_CORRUPTED ]',
  '[ ALERTA: PÉRDIDA DE COHERENCIA ]',
]

const HEX = '0123456789ABCDEF'
function randHex(n: number) {
  return '0x' + Array.from({ length: n }, () => HEX[Math.floor(Math.random() * 16)]).join('')
}
function makeHexBlock() {
  return [
    `${randHex(4)}  ${randHex(4)}  ${randHex(4)}`,
    `${randHex(4)}  ${randHex(4)}  ${randHex(4)}`,
    `${randHex(4)}  ${randHex(4)}  ${randHex(4)}`,
  ].join('\n')
}

// ─── Componente ───────────────────────────────────────────────────────────────

export default function NeuralInstabilityEvent() {
  const [isInstable, setIsInstable]   = useState(false)
  const [alertText, setAlertText]     = useState('')
  const [isHex, setIsHex]             = useState(false)
  const [showDaki, setShowDaki]       = useState(false)
  const [dakiMsg, setDakiMsg]         = useState('')

  const audioRef   = useRef<HTMLAudioElement | null>(null)
  const mainTimer  = useRef<ReturnType<typeof setTimeout>>()
  const subTimers  = useRef<ReturnType<typeof setTimeout>[]>([])

  const clearSubs  = () => { subTimers.current.forEach(clearTimeout); subTimers.current = [] }

  // ── Inicializar audio (solo cliente) ────────────────────────────────────────
  useEffect(() => {
    audioRef.current = new Audio('/sounds/data-stream.mp3')
    audioRef.current.volume = 0.4
  }, [])

  // ── Ciclo de eventos ────────────────────────────────────────────────────────
  const scheduleNext = useCallback((delayMs: number) => {
    clearTimeout(mainTimer.current)
    mainTimer.current = setTimeout(() => fireEvent(), delayMs)
  }, []) // eslint-disable-line react-hooks/exhaustive-deps

  const fireEvent = useCallback(() => {
    // Contenido del evento (aleatorio cada vez)
    const useHex = Math.random() > 0.55
    setIsHex(useHex)
    setAlertText(useHex
      ? makeHexBlock()
      : ALERT_TEXTS[Math.floor(Math.random() * ALERT_TEXTS.length)]
    )
    setIsInstable(true)

    // Reproducir audio sin bloquear
    const audio = audioRef.current
    if (audio) {
      audio.currentTime = 0
      audio.play().catch(() => {/* autoplay policy — silencioso */})
    }

    // Apagar evento visual + audio al vencer 1.2 s
    subTimers.current.push(setTimeout(() => {
      setIsInstable(false)
      if (audio) { audio.pause(); audio.currentTime = 0 }

      // Notificación DAKI
      const msg = DAKI_MESSAGES[Math.floor(Math.random() * DAKI_MESSAGES.length)]
      setDakiMsg(msg)
      setShowDaki(true)

      // Ocultar notificación tras 4.5 s (AnimatePresence maneja el fade)
      subTimers.current.push(setTimeout(() => {
        setShowDaki(false)
        // Programar siguiente evento: 45 – 90 s
        scheduleNext(45_000 + Math.random() * 45_000)
      }, DAKI_VISIBLE_MS))

    }, INSTABILITY_MS))
  }, [scheduleNext])

  // Arranque del ciclo
  useEffect(() => {
    mainTimer.current = setTimeout(() => fireEvent(), FIRST_DELAY_MS)

    return () => {
      clearTimeout(mainTimer.current)
      clearSubs()
      const a = audioRef.current
      if (a) { a.pause(); a.currentTime = 0 }
    }
  }, [fireEvent])

  return (
    <>
      {/* ══════════════════════════════════════════
          OVERLAY DE INESTABILIDAD (1.2 s)
          pointer-events-none — nunca roba el foco
      ══════════════════════════════════════════ */}
      <AnimatePresence>
        {isInstable && (
          <motion.div
            key="instability"
            className="fixed inset-0 z-[9000] pointer-events-none overflow-hidden"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.04 }}
          >
            {/* Tinte verde + filtros de pantalla */}
            <div
              className="absolute inset-0 bg-green-900/20"
              style={{ backdropFilter: 'contrast(1.5) brightness(1.1) saturate(1.4)' }}
            />

            {/* Borde interior resplandeciente */}
            <div
              className="absolute inset-0"
              style={{ boxShadow: 'inset 0 0 90px rgba(0,255,65,0.35)' }}
            />

            {/* Texto central parpadeante */}
            <div className="absolute inset-0 flex items-center justify-center">
              <motion.div
                animate={{ opacity: [1, 0.15, 1, 0.15, 1, 0.15, 1] }}
                transition={{
                  duration: 1.2,
                  times: [0, 0.12, 0.28, 0.44, 0.60, 0.76, 1],
                  ease: 'linear',
                }}
                className={isHex ? 'text-center' : 'text-center px-6'}
              >
                {isHex ? (
                  <pre
                    className="text-green-400 font-mono text-lg md:text-2xl font-black leading-loose tracking-[0.2em]"
                    style={{
                      textShadow: '0 0 18px rgba(0,255,65,1), 0 0 45px rgba(0,255,65,0.65)',
                    }}
                  >
                    {alertText}
                  </pre>
                ) : (
                  <div
                    className="text-green-400 font-mono font-black text-2xl md:text-4xl tracking-[0.22em]"
                    style={{
                      textShadow: '0 0 22px rgba(0,255,65,1), 0 0 55px rgba(0,255,65,0.6)',
                    }}
                  >
                    {alertText}
                  </div>
                )}
              </motion.div>
            </div>

            {/* Líneas de escaneo horizontales aleatorias */}
            {[22, 58, 77].map((pct) => (
              <div
                key={pct}
                className="absolute left-0 right-0 h-[1px]"
                style={{
                  top: `${pct}%`,
                  background: 'linear-gradient(90deg, transparent 0%, rgba(0,255,65,0.6) 30%, rgba(0,255,65,0.8) 50%, rgba(0,255,65,0.6) 70%, transparent 100%)',
                  boxShadow: '0 0 8px rgba(0,255,65,0.6)',
                  mixBlendMode: 'screen',
                }}
              />
            ))}
          </motion.div>
        )}
      </AnimatePresence>

      {/* ══════════════════════════════════════════
          NOTIFICACIÓN DE DAKI (post-evento, 4.5 s)
          pointer-events-none — nunca roba el foco
      ══════════════════════════════════════════ */}
      <AnimatePresence>
        {showDaki && (
          <motion.div
            key="daki-alert"
            className="fixed bottom-6 right-6 z-[9001] pointer-events-none max-w-xs md:max-w-sm"
            initial={{ opacity: 0, y: 14, scale: 0.94 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 8, scale: 0.97 }}
            transition={{ duration: 0.28, ease: 'easeOut' }}
          >
            <div
              className="border border-cyan-500/50 bg-black/80 backdrop-blur-md px-4 py-3 font-mono"
              style={{ boxShadow: '0 0 24px rgba(0,229,255,0.12), inset 0 0 16px rgba(0,229,255,0.04)' }}
            >
              {/* Header DAKI */}
              <div className="flex items-center gap-2 mb-2">
                <motion.span
                  className="w-1.5 h-1.5 rounded-full bg-cyan-400 shrink-0"
                  animate={{ opacity: [0.35, 1, 0.35] }}
                  transition={{ duration: 1.4, repeat: Infinity }}
                  style={{ boxShadow: '0 0 6px rgba(0,229,255,0.9)' }}
                />
                <span
                  className="text-[9px] tracking-[0.5em] text-cyan-400/85 font-bold"
                  style={{ textShadow: '0 0 6px rgba(0,229,255,0.5)' }}
                >
                  [DAKI]::
                </span>
                {/* Barra de progreso de 4.5 s */}
                <div className="flex-1 h-px bg-cyan-500/10 overflow-hidden ml-1">
                  <motion.div
                    className="h-full bg-cyan-400/50"
                    initial={{ width: '100%' }}
                    animate={{ width: '0%' }}
                    transition={{ duration: DAKI_VISIBLE_MS / 1000, ease: 'linear' }}
                  />
                </div>
              </div>

              {/* Mensaje */}
              <p className="text-[11px] text-cyan-200/65 leading-relaxed">
                {dakiMsg}
              </p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  )
}
