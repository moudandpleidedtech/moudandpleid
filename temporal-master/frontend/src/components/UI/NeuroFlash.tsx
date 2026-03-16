'use client'

import { useEffect, useState, useRef } from 'react'

// ─── Biblioteca de fragmentos ─────────────────────────────────────────────────

const FRAGMENTS = [
  '01101001 01100110',
  'def __init__(self)',
  'ptr_access = 0xAF32',
  'SyntaxError: Unexpected Token',
  'while True: pass',
  '>>> import consciousness',
  'null != undefined',
  'segfault (core dumped)',
  '[NEURAL_LOAD: 88%]',
  '[SYNAPTIC_STATIC_DETECTED]',
  '¿Esto es real?',
  'Ajustando dopamina...',
  '[FIREWALL_COUNTERMEASURE_ACTIVE]',
  '[NEXO :: SYNC_LOST 0.3ms]',
  'MEMORIA_RESIDUAL_DETECTADA',
  '[LATENCIA_SINÁPTICA: 2ms]',
  '> reconexión neuronal...',
  '0xDEAD_BEEF != 0xC0FFEE',
  'kernel panic — not syncing',
  'ERR_CONSCIOUSNESS_OVERFLOW',
]

const BLOCK = '█▄▀▐░▒▓▌▍▎▏'
const HEX   = '0123456789ABCDEF'

// ─── Generador de ruido ───────────────────────────────────────────────────────

function makeNoise(len: number): string {
  return Array.from({ length: len }, () => {
    const r = Math.random()
    if (r < 0.28) return BLOCK[Math.floor(Math.random() * BLOCK.length)]
    if (r < 0.50) return HEX[Math.floor(Math.random() * 16)]
    if (r < 0.65) return Math.random() > 0.5 ? '0' : '1'
    return r < 0.80 ? ' ' : '_'
  }).join('')
}

// ─── Estado del destello ──────────────────────────────────────────────────────

interface FlashState {
  text: string
  noiseTop: string
  noiseBottom: string
  skewX: number       // grados
  offsetX: number     // px
  offsetY: number     // px
  opacity: number     // 0.7 – 0.9
  scanY: number       // % de la pantalla para la barra de barrido (0 = desactivado)
}

// ─── Componente ───────────────────────────────────────────────────────────────

export default function NeuroFlash() {
  const [flash, setFlash] = useState<FlashState | null>(null)
  const timerRef          = useRef<ReturnType<typeof setTimeout>>()

  useEffect(() => {
    const schedule = () => {
      // Intervalo irregular: 12 – 40 segundos
      const delay = 12_000 + Math.random() * 28_000

      timerRef.current = setTimeout(() => {
        // Duración agresiva: 100 – 200 ms
        const duration = 100 + Math.random() * 100

        setFlash({
          text:        FRAGMENTS[Math.floor(Math.random() * FRAGMENTS.length)],
          noiseTop:    makeNoise(22),
          noiseBottom: makeNoise(18),
          skewX:       (Math.random() - 0.5) * 22,    // ± 11 °
          offsetX:     (Math.random() - 0.5) * 140,   // ± 70 px
          offsetY:     (Math.random() - 0.5) * 90,    // ± 45 px
          opacity:     0.70 + Math.random() * 0.20,   // 0.70 – 0.90
          // 40 % de los flashes incluyen barra de barrido horizontal
          scanY:       Math.random() > 0.6 ? 15 + Math.random() * 70 : 0,
        })

        setTimeout(() => {
          setFlash(null)
          schedule()
        }, duration)
      }, delay)
    }

    // Primer destello tras 8 – 20 s (no interrumpe el onboarding)
    timerRef.current = setTimeout(() => {
      clearTimeout(timerRef.current)
      schedule()
    }, 8_000 + Math.random() * 12_000)

    return () => clearTimeout(timerRef.current)
  }, [])

  if (!flash) return null

  return (
    <div
      className="fixed inset-0 z-[9000] pointer-events-none"
      aria-hidden="true"
    >

      {/* ── Barra de barrido horizontal (scan line) ───────────────────────── */}
      {flash.scanY > 0 && (
        <div
          className="absolute left-0 right-0 h-[1px] md:h-[2px]"
          style={{
            top: `${flash.scanY}%`,
            background: 'linear-gradient(90deg, transparent 0%, rgba(0,255,65,0.9) 20%, rgba(0,255,65,1) 50%, rgba(0,255,65,0.9) 80%, transparent 100%)',
            boxShadow: '0 0 12px rgba(0,255,65,1), 0 0 30px rgba(0,255,65,0.5)',
            mixBlendMode: 'screen',
          }}
        />
      )}

      {/* ── Destello central con aberración cromática ─────────────────────── */}
      <div className="w-full h-full flex items-center justify-center">
        <div
          style={{
            transform:    `translate(${flash.offsetX}px, ${flash.offsetY}px) skewX(${flash.skewX}deg)`,
            opacity:       flash.opacity,
            mixBlendMode: 'screen',
          }}
          className="font-mono select-none"
        >
          {/* Línea de ruido superior */}
          <div
            className="text-green-400 text-[11px] tracking-[0.18em] mb-1 overflow-hidden whitespace-nowrap"
            style={{ textShadow: '0 0 8px rgba(0,255,65,0.9)' }}
          >
            {flash.noiseTop}
          </div>

          {/* Texto principal — RGB split */}
          <div className="relative text-sm md:text-base tracking-[0.28em] font-black whitespace-nowrap">

            {/* Ghost rojo — desplazado a la izquierda */}
            <span
              className="absolute inset-0"
              style={{
                color:       'rgba(255,30,60,0.75)',
                transform:   'translateX(-4px) translateY(1px)',
                textShadow:  '0 0 8px rgba(255,30,60,0.6)',
              }}
            >
              {flash.text}
            </span>

            {/* Ghost cian — desplazado a la derecha */}
            <span
              className="absolute inset-0"
              style={{
                color:       'rgba(0,229,255,0.75)',
                transform:   'translateX(4px) translateY(-1px)',
                textShadow:  '0 0 8px rgba(0,229,255,0.6)',
              }}
            >
              {flash.text}
            </span>

            {/* Capa verde principal */}
            <span
              className="relative text-green-400"
              style={{
                textShadow: '0 0 15px rgba(0,255,0,1), 0 0 35px rgba(0,255,65,0.7), 0 0 60px rgba(0,255,65,0.3)',
              }}
            >
              {flash.text}
            </span>
          </div>

          {/* Línea de ruido inferior */}
          <div
            className="text-green-400/70 text-[10px] tracking-[0.15em] mt-1 overflow-hidden whitespace-nowrap"
            style={{ textShadow: '0 0 6px rgba(0,255,65,0.7)' }}
          >
            {flash.noiseBottom}
          </div>
        </div>
      </div>

    </div>
  )
}
