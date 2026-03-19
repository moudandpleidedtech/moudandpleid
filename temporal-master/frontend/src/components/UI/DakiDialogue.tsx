'use client'

/**
 * DakiDialogue.tsx — Avatar visual + texto + voz de DAKI
 *
 * Props:
 *   message    Texto que DAKI va a decir (reproduce voz al cambiar)
 *   dakiLevel  1 = Robótico | 2 = Amistoso | 3 = Compañero
 *   size       'sm' | 'md' | 'lg'  (default: 'md')
 *   showText   Si mostrar el bloque de texto abajo del avatar (default: true)
 */

import { useEffect, useRef, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useDakiVoice } from '@/hooks/useDakiVoice'
import type { DakiLevel } from '@/lib/dakiVoice'

// ─── Configuración visual por nivel ──────────────────────────────────────────

const LEVEL_CONFIG = {
  1: {
    color:       '#00FF41',
    colorDim:    'rgba(0,255,65,0.12)',
    label:       'DAKI v1.0',
    moodLabel:   'ROBÓTICO',
    glowColor:   'rgba(0,255,65,0.5)',
    glowStrong:  'rgba(0,255,65,0.9)',
    coreSymbol:  '◈',
    rings:       1,
    particles:   0,
    glitchRate:  1.8,   // segundos entre glitches visuales
  },
  2: {
    color:       '#00E5FF',
    colorDim:    'rgba(0,229,255,0.12)',
    label:       'DAKI v2.0',
    moodLabel:   'AMISTOSO',
    glowColor:   'rgba(0,229,255,0.5)',
    glowStrong:  'rgba(0,229,255,0.9)',
    coreSymbol:  '◉',
    rings:       2,
    particles:   3,
    glitchRate:  4,
  },
  3: {
    color:       '#BD00FF',
    colorDim:    'rgba(189,0,255,0.12)',
    label:       'DAKI v3.0',
    moodLabel:   'COMPAÑERO',
    glowColor:   'rgba(189,0,255,0.5)',
    glowStrong:  'rgba(189,0,255,0.9)',
    coreSymbol:  '✦',
    rings:       3,
    particles:   5,
    glitchRate:  8,
  },
} as const

const SIZE_CONFIG = {
  sm: { container: 'w-16 h-16', core: 'w-8 h-8',  coreText: 'text-sm',  ringBase: 8  },
  md: { container: 'w-28 h-28', core: 'w-14 h-14', coreText: 'text-xl',  ringBase: 14 },
  lg: { container: 'w-44 h-44', core: 'w-20 h-20', coreText: 'text-3xl', ringBase: 20 },
}

// ─── Typewriter ───────────────────────────────────────────────────────────────

function useTypewriter(text: string, speed = 18) {
  const [displayed, setDisplayed] = useState('')
  const [done, setDone]           = useState(false)

  useEffect(() => {
    setDisplayed(''); setDone(false)
    if (!text) return
    let i = 0
    const iv = setInterval(() => {
      i++; setDisplayed(text.slice(0, i))
      if (i >= text.length) { clearInterval(iv); setDone(true) }
    }, speed)
    return () => clearInterval(iv)
  }, [text, speed])

  return { displayed, done }
}

// ─── Avatar SVG por nivel ─────────────────────────────────────────────────────

function DakiAvatar({
  dakiLevel,
  isSpeaking,
  size = 'md',
}: {
  dakiLevel: DakiLevel
  isSpeaking: boolean
  size?: 'sm' | 'md' | 'lg'
}) {
  const cfg  = LEVEL_CONFIG[dakiLevel]
  const sz   = SIZE_CONFIG[size]

  // Animaciones condicionales al hablar
  const speakPulse = isSpeaking
    ? { scale: [1, 1.08, 1, 1.05, 1], transition: { duration: 0.4, repeat: Infinity } }
    : { scale: [1, 1.03, 1],          transition: { duration: 2.8, repeat: Infinity, ease: 'easeInOut' } }

  const glowAnim = isSpeaking
    ? {
        boxShadow: [
          `0 0 12px ${cfg.glowColor}, 0 0 28px ${cfg.colorDim}`,
          `0 0 28px ${cfg.glowStrong}, 0 0 55px ${cfg.glowColor}`,
          `0 0 12px ${cfg.glowColor}, 0 0 28px ${cfg.colorDim}`,
        ],
        transition: { duration: 0.35, repeat: Infinity },
      }
    : {
        boxShadow: [
          `0 0 12px ${cfg.glowColor}, 0 0 28px ${cfg.colorDim}`,
          `0 0 22px ${cfg.glowStrong}, 0 0 44px ${cfg.glowColor}`,
          `0 0 12px ${cfg.glowColor}, 0 0 28px ${cfg.colorDim}`,
        ],
        transition: { duration: 2.5, repeat: Infinity, ease: 'easeInOut' },
      }

  return (
    <div className={`relative flex items-center justify-center ${sz.container} mx-auto`}>

      {/* Halo de fondo */}
      <motion.div
        className="absolute inset-0 rounded-full"
        style={{ background: `radial-gradient(circle, ${cfg.colorDim} 0%, transparent 70%)` }}
        animate={{ scale: [1, 1.25, 1], opacity: [0.4, 0.9, 0.4] }}
        transition={{ duration: 3, repeat: Infinity, ease: 'easeInOut' }}
      />

      {/* Anillos orbitantes — cantidad según daki_level */}
      {Array.from({ length: cfg.rings }).map((_, i) => {
        const inset     = sz.ringBase * (i + 1)
        const duration  = 18 - i * 4
        const direction = i % 2 === 0 ? 360 : -360
        return (
          <motion.div
            key={i}
            className="absolute rounded-full"
            style={{
              inset,
              border: `1px solid ${cfg.color}${i === 0 ? '22' : i === 1 ? '18' : '12'}`,
            }}
            animate={{ rotate: direction }}
            transition={{ duration, repeat: Infinity, ease: 'linear' }}
          />
        )
      })}

      {/* Partículas orbitantes — solo niveles 2 y 3 */}
      {Array.from({ length: cfg.particles }).map((_, i) => {
        const angle = (360 / cfg.particles) * i
        const radius = size === 'lg' ? 52 : size === 'md' ? 36 : 22
        return (
          <motion.div
            key={`p-${i}`}
            className="absolute rounded-full"
            style={{
              width:  size === 'sm' ? 3 : 5,
              height: size === 'sm' ? 3 : 5,
              background: cfg.color,
              boxShadow: `0 0 6px ${cfg.glowColor}`,
            }}
            animate={{
              rotate:  [angle, angle + 360],
              x:       [Math.cos((angle * Math.PI) / 180) * radius],
              y:       [Math.sin((angle * Math.PI) / 180) * radius],
            }}
            transition={{
              rotate:   { duration: 8 + i * 1.5, repeat: Infinity, ease: 'linear' },
              x:        { duration: 0 },
              y:        { duration: 0 },
            }}
          />
        )
      })}

      {/* Núcleo principal */}
      <motion.div
        className={`relative z-10 ${sz.core} rounded-full flex items-center justify-center`}
        style={{
          background: `radial-gradient(circle at 38% 38%, ${cfg.colorDim}, rgba(0,5,3,0.95))`,
          border: `1.5px solid ${cfg.color}99`,
        }}
        animate={glowAnim}
      >
        {/* Símbolo central — glitch sutil en nivel 1 */}
        <motion.span
          className={`${sz.coreText} select-none`}
          style={{
            color: cfg.color,
            textShadow: `0 0 10px ${cfg.glowColor}, 0 0 22px ${cfg.colorDim}`,
          }}
          animate={
            dakiLevel === 1
              ? { opacity: [0.7, 1, 0.85, 1, 0.7], x: [0, 1, -1, 0] }
              : { opacity: [0.8, 1, 0.8] }
          }
          transition={
            dakiLevel === 1
              ? { duration: cfg.glitchRate, repeat: Infinity, times: [0, 0.3, 0.5, 0.7, 1] }
              : { duration: 2.5, repeat: Infinity, ease: 'easeInOut' }
          }
        >
          {cfg.coreSymbol}
        </motion.span>

        {/* Pulso de habla — ondas concéntricas mientras la voz está activa */}
        <AnimatePresence>
          {isSpeaking && (
            <>
              {[0, 1, 2].map((i) => (
                <motion.div
                  key={`wave-${i}`}
                  className="absolute inset-0 rounded-full"
                  style={{ border: `1px solid ${cfg.color}` }}
                  initial={{ scale: 1, opacity: 0.6 }}
                  animate={{ scale: 2.5 + i * 0.5, opacity: 0 }}
                  exit={{ opacity: 0 }}
                  transition={{ duration: 1.2, delay: i * 0.3, repeat: Infinity, ease: 'easeOut' }}
                />
              ))}
            </>
          )}
        </AnimatePresence>
      </motion.div>

      {/* Barra de audio — igual que un VU meter, solo al hablar */}
      <AnimatePresence>
        {isSpeaking && size !== 'sm' && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="absolute -bottom-5 flex gap-0.5 items-end"
          >
            {[3, 6, 9, 6, 4, 8, 5, 3, 7].map((h, i) => (
              <motion.div
                key={i}
                className="w-1 rounded-sm"
                style={{ background: cfg.color, opacity: 0.7 }}
                animate={{ height: [`${h}px`, `${h * 1.8}px`, `${h * 0.5}px`, `${h}px`] }}
                transition={{
                  duration: 0.35 + i * 0.04,
                  repeat: Infinity,
                  ease: 'easeInOut',
                  delay: i * 0.05,
                }}
              />
            ))}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

// ─── Componente principal ─────────────────────────────────────────────────────

interface DakiDialogueProps {
  message: string
  dakiLevel?: DakiLevel
  size?: 'sm' | 'md' | 'lg'
  showText?: boolean
  /** Si false, no reproduce voz (útil en la vista de IDE donde ya hay DakiHint) */
  voiceEnabled?: boolean
}

export default function DakiDialogue({
  message,
  dakiLevel = 1,
  size = 'md',
  showText = true,
  voiceEnabled = true,
}: DakiDialogueProps) {
  const cfg = LEVEL_CONFIG[dakiLevel]
  const { displayed, done } = useTypewriter(message, dakiLevel === 1 ? 22 : 15)

  const { isSpeaking } = useDakiVoice(dakiLevel, {
    text: message,
    autoPlay: voiceEnabled,
    enabled: voiceEnabled,
  })

  // Contador de caracteres procesados (sólo se muestra en nivel 1)
  const charCount = useRef(0)
  useEffect(() => { charCount.current++ }, [message])

  return (
    <div className="flex flex-col items-center gap-5">

      {/* ── Avatar ── */}
      <DakiAvatar dakiLevel={dakiLevel} isSpeaking={isSpeaking} size={size} />

      {/* ── Label de nivel ── */}
      <div className="flex flex-col items-center gap-1">
        <motion.span
          className="text-[9px] tracking-[0.4em] font-bold"
          style={{ fontFamily: 'monospace', color: cfg.color, opacity: 0.7 }}
          animate={{ opacity: [0.5, 0.9, 0.5] }}
          transition={{ duration: 3, repeat: Infinity }}
        >
          {cfg.label} — {cfg.moodLabel}
        </motion.span>

        {/* Indicador de voz */}
        {voiceEnabled && (
          <div className="flex items-center gap-1.5">
            <motion.div
              className="w-1 h-1 rounded-full"
              style={{ background: cfg.color }}
              animate={isSpeaking
                ? { opacity: [1, 0.2, 1], scale: [1, 1.5, 1] }
                : { opacity: [0.3, 0.6, 0.3] }
              }
              transition={{ duration: isSpeaking ? 0.4 : 2, repeat: Infinity }}
            />
            <span
              className="text-[8px] tracking-widest"
              style={{ fontFamily: 'monospace', color: `${cfg.color}55` }}
            >
              {isSpeaking ? 'TRANSMITIENDO' : 'EN ESPERA'}
            </span>
          </div>
        )}
      </div>

      {/* ── Bloque de texto ── */}
      {showText && message && (
        <motion.div
          initial={{ opacity: 0, y: 6 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
          className="w-full max-w-sm"
          style={{
            background: `linear-gradient(135deg, ${cfg.colorDim}, rgba(0,0,0,0.6))`,
            border: `1px solid ${cfg.color}22`,
            borderRadius: '6px',
          }}
        >
          {/* Header terminal */}
          <div
            className="flex items-center gap-2 px-3 py-1.5 border-b"
            style={{ borderColor: `${cfg.color}18` }}
          >
            <motion.span
              className="w-1.5 h-1.5 rounded-full shrink-0"
              style={{ background: cfg.color }}
              animate={{ opacity: [0.4, 1, 0.4] }}
              transition={{ duration: 1.2, repeat: Infinity }}
            />
            <span
              className="text-[8px] tracking-[0.35em] font-bold"
              style={{ fontFamily: 'monospace', color: `${cfg.color}88` }}
            >
              [ DAKI TRANSMISIÓN #{String(charCount.current).padStart(3, '0')} ]
            </span>
          </div>

          {/* Texto con efecto typewriter */}
          <div className="px-3 py-2.5 min-h-[3rem]">
            <p
              className="text-[11px] leading-relaxed"
              style={{ fontFamily: 'monospace', color: `${cfg.color}cc` }}
            >
              {displayed}
              {/* Cursor parpadeante mientras escribe */}
              {!done && (
                <motion.span
                  animate={{ opacity: [1, 0] }}
                  transition={{ duration: 0.5, repeat: Infinity }}
                  style={{ color: cfg.color }}
                >
                  ▌
                </motion.span>
              )}
            </p>
          </div>
        </motion.div>
      )}
    </div>
  )
}
