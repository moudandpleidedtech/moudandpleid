'use client'

import { useState, useId } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useDakiVoice } from '@/hooks/useDakiVoice'
import type { DakiLevel } from '@/lib/dakiVoice'

interface Props {
  visible: boolean
  hints: string[]
  hintIndex: number
  dakiLevel?: DakiLevel
}

// ─── Líneas eléctricas SVG animadas ──────────────────────────────────────────

function ElectricLines({ active, color }: { active: boolean; color: string }) {
  const id = useId()
  // 5 líneas horizontales con paths irregulares que simulan arcos eléctricos
  const lines = [
    'M0,10 Q20,4 40,10 Q60,16 80,10 Q100,4 120,10 Q140,16 160,10 Q180,4 200,10',
    'M0,10 Q25,2  50,10 Q75,18 100,10 Q125,2 150,10 Q175,18 200,10',
    'M0,10 Q15,6  30,10 Q50,14 70,8  Q90,12 110,8 Q130,14 150,10 Q175,6 200,10',
    'M0,10 Q30,3  60,11 Q90,19 120,9 Q150,2 180,11 Q190,14 200,10',
    'M0,10 Q22,7  44,13 Q66,3  88,10 Q110,17 132,9 Q154,3 176,10 Q188,14 200,10',
  ]

  return (
    <div className="w-full overflow-hidden" style={{ height: 32 }}>
      <svg width="100%" height="32" viewBox="0 0 200 20" preserveAspectRatio="none">
        <defs>
          <filter id={`${id}-glow`}>
            <feGaussianBlur stdDeviation="1.2" result="blur" />
            <feMerge><feMergeNode in="blur" /><feMergeNode in="SourceGraphic" /></feMerge>
          </filter>
        </defs>
        {lines.map((d, i) => (
          <motion.path
            key={i}
            d={d}
            fill="none"
            stroke={color}
            strokeWidth={i === 2 ? 1.2 : 0.6}
            filter={`url(#${id}-glow)`}
            style={{ opacity: active ? (i === 2 ? 0.85 : 0.35) : 0.08 }}
            animate={active ? {
              d: [
                d,
                d.replace(/Q(\d+),(\d+)/g, (_, x, y) =>
                  `Q${x},${Math.max(1, parseInt(y) + (Math.random() > 0.5 ? 3 : -3))}`
                ),
                d,
              ],
              opacity: [
                i === 2 ? 0.85 : 0.35,
                i === 2 ? 1 : 0.55,
                i === 2 ? 0.85 : 0.35,
              ],
            } : { opacity: 0.08 }}
            transition={active ? {
              duration: 0.18 + i * 0.07,
              repeat: Infinity,
              ease: 'easeInOut',
            } : { duration: 0.4 }}
          />
        ))}
      </svg>
    </div>
  )
}

// ─── Ojo de DAKI pulsante ─────────────────────────────────────────────────────

function DakiEye({ speaking, color }: { speaking: boolean; color: string }) {
  return (
    <div className="relative flex items-center justify-center" style={{ width: 64, height: 64 }}>
      {/* Halo exterior */}
      <motion.div
        className="absolute rounded-full"
        style={{ width: 64, height: 64, background: `radial-gradient(circle, ${color}22 0%, transparent 70%)` }}
        animate={speaking
          ? { scale: [1, 1.35, 1.1, 1.3, 1], opacity: [0.6, 1, 0.7, 1, 0.6] }
          : { scale: [1, 1.08, 1], opacity: [0.3, 0.5, 0.3] }
        }
        transition={{ duration: speaking ? 0.5 : 2.5, repeat: Infinity, ease: 'easeInOut' }}
      />
      {/* Anillo medio */}
      <motion.div
        className="absolute rounded-full border"
        style={{ width: 46, height: 46, borderColor: `${color}40` }}
        animate={speaking
          ? { scale: [1, 1.2, 0.95, 1.15, 1], opacity: [0.5, 1, 0.4, 0.9, 0.5] }
          : { scale: [1, 1.04, 1], opacity: [0.2, 0.4, 0.2] }
        }
        transition={{ duration: speaking ? 0.45 : 3, repeat: Infinity, ease: 'easeInOut', delay: 0.05 }}
      />
      {/* Símbolo ◈ */}
      <motion.span
        className="relative text-4xl leading-none select-none"
        style={{ color, textShadow: `0 0 18px ${color}90, 0 0 40px ${color}40` }}
        animate={speaking
          ? { scale: [1, 1.18, 0.92, 1.12, 1], opacity: [1, 0.8, 1, 0.9, 1] }
          : { scale: [1, 1.05, 1], opacity: [0.7, 1, 0.7] }
        }
        transition={{ duration: speaking ? 0.42 : 2.8, repeat: Infinity, ease: 'easeInOut' }}
      >
        ◈
      </motion.span>
    </div>
  )
}

// ─── Componente principal ─────────────────────────────────────────────────────

export default function DakiHint({ visible, hints, hintIndex, dakiLevel = 1 }: Props) {
  const [voiceEnabled, setVoiceEnabled] = useState(true)

  const idx         = Math.min(Math.max(hintIndex, 0), hints.length - 1)
  const currentHint = hints[idx] ?? ''
  const total       = hints.length

  const { speak, cancel, isSpeaking } = useDakiVoice(dakiLevel, {
    text:     visible ? currentHint : undefined,
    autoPlay: voiceEnabled && visible,
    enabled:  voiceEnabled,
  })

  if (!hints || hints.length === 0) return null

  const color   = '#00CFFF'
  const speaking = isSpeaking

  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          key="daki-hint"
          initial={{ opacity: 0, y: 16, scaleY: 0.85 }}
          animate={{ opacity: 1, y: 0, scaleY: 1 }}
          exit={{ opacity: 0, y: 8, scaleY: 0.9 }}
          transition={{ duration: 0.28, ease: 'easeOut' }}
          className="shrink-0 font-mono overflow-hidden"
          style={{
            border:     `1px solid ${color}35`,
            background: `linear-gradient(180deg, ${color}08 0%, rgba(0,0,0,0.6) 100%)`,
            boxShadow:  `0 0 28px ${color}12, inset 0 0 20px ${color}05`,
          }}
        >
          {/* ── Líneas eléctricas superiores ── */}
          <ElectricLines active={speaking} color={color} />

          {/* ── Avatar + header ── */}
          <div
            className="flex items-center gap-3 px-4 pb-3 border-b"
            style={{ borderColor: `${color}20` }}
          >
            <DakiEye speaking={speaking} color={color} />

            <div className="flex-1 min-w-0">
              {/* Etiqueta superior */}
              <div className="flex items-center gap-2 mb-0.5">
                <motion.span
                  className="w-1.5 h-1.5 rounded-full shrink-0"
                  style={{ background: color, boxShadow: `0 0 6px ${color}` }}
                  animate={{ opacity: [0.4, 1, 0.4] }}
                  transition={{ duration: 1.1, repeat: Infinity }}
                />
                <span
                  className="text-[9px] tracking-[0.4em] font-black uppercase"
                  style={{ color: `${color}90` }}
                >
                  TRANSMISIÓN DE DAKI
                </span>
              </div>

              {/* Pista N/total */}
              <div className="flex items-center justify-between">
                <span className="text-[8px] tracking-[0.25em]" style={{ color: `${color}45` }}>
                  PISTA {idx + 1} / {total}
                </span>
                <div className="flex items-center gap-2">
                  {speaking && (
                    <motion.span
                      className="text-[7px] tracking-[0.3em] font-bold"
                      style={{ color: `${color}70` }}
                      animate={{ opacity: [0.3, 1, 0.3] }}
                      transition={{ duration: 0.55, repeat: Infinity }}
                    >
                      ◉ VOZ ACTIVA
                    </motion.span>
                  )}
                  <button
                    onClick={() => {
                      if (voiceEnabled) { cancel(); setVoiceEnabled(false) }
                      else { setVoiceEnabled(true); speak(currentHint) }
                    }}
                    className="text-[11px] transition-opacity hover:opacity-100"
                    style={{ color: voiceEnabled ? `${color}80` : '#ffffff20' }}
                    title={voiceEnabled ? 'Silenciar DAKI' : 'Activar voz de DAKI'}
                  >
                    {voiceEnabled ? '🔊' : '🔇'}
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* ── Mensaje ── */}
          <AnimatePresence mode="wait">
            <motion.div
              key={idx}
              initial={{ opacity: 0, x: 8 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -8 }}
              transition={{ duration: 0.2 }}
              className="px-4 py-3"
            >
              <p
                className="text-[11px] leading-relaxed"
                style={{ color: `${color}CC` }}
              >
                {currentHint}
              </p>
            </motion.div>
          </AnimatePresence>

          {/* ── Líneas eléctricas inferiores ── */}
          <ElectricLines active={speaking} color={color} />
        </motion.div>
      )}
    </AnimatePresence>
  )
}
