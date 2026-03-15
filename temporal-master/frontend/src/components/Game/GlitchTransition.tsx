'use client'

import { useEffect, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

interface Props {
  onComplete: () => void
}

type Phase = 'glitch' | 'reveal' | 'modal'

const NARRATIVE = [
  'PROTOCOLO DE ALTO NIVEL COMPROMETIDO.',
  'ACCESO A CONSOLA NATIVA REQUERIDO.',
  '',
  'TODO LO QUE CREIAS QUE ERAN COMANDOS...',
  '...ERA SOLO PYTHON.',
  '',
  'BIENVENIDO AL SISTEMA REAL.',
]

export default function GlitchTransition({ onComplete }: Props) {
  const [phase, setPhase] = useState<Phase>('glitch')
  const [visibleLines, setVisibleLines] = useState(0)

  // Fase 1: glitch durante 2s → fase reveal
  useEffect(() => {
    const t = setTimeout(() => setPhase('reveal'), 2000)
    return () => clearTimeout(t)
  }, [])

  // Fase 2: revelar líneas de texto una a una → modal
  useEffect(() => {
    if (phase !== 'reveal') return
    let i = 0
    const tick = () => {
      i++
      setVisibleLines(i)
      if (i < NARRATIVE.length) setTimeout(tick, 180)
      else setTimeout(() => setPhase('modal'), 400)
    }
    const t = setTimeout(tick, 200)
    return () => clearTimeout(t)
  }, [phase])

  return (
    <motion.div
      className="fixed inset-0 z-[100] flex items-center justify-center"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.2 }}
    >
      {/* Fondo negro opaco */}
      <div className="absolute inset-0 bg-black" />

      {/* Capa de glitch activa solo en fase 1 */}
      {phase === 'glitch' && (
        <div className="absolute inset-0 glitch-active overflow-hidden">
          {/* Scanlines animadas */}
          <div className="glitch-scanlines" />

          {/* Capas de aberración cromática */}
          <div className="glitch-layer-r pointer-events-none select-none"
            style={{ background: 'repeating-linear-gradient(90deg,#FF003310 0px,transparent 3px,transparent 30px)' }}
          />
          <div className="glitch-layer-b pointer-events-none select-none"
            style={{ background: 'repeating-linear-gradient(90deg,#0033FF10 0px,transparent 3px,transparent 20px)' }}
          />

          {/* Texto de glitch decorativo */}
          <div className="absolute inset-0 flex flex-col justify-center px-12 select-none pointer-events-none opacity-30">
            {Array.from({ length: 12 }).map((_, i) => (
              <div key={i} className="font-mono text-xs text-[#00FF41] leading-5"
                style={{ marginLeft: `${(i * 37) % 60}%`, opacity: 0.5 + (i % 3) * 0.2 }}>
                {Array.from({ length: 40 }).map(() =>
                  '0123456789ABCDEF'[Math.floor(Math.random() * 16)]
                ).join('')}
              </div>
            ))}
          </div>

          {/* Texto central glitcheado */}
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="font-mono font-black text-5xl text-[#00FF41] tracking-widest select-none"
              style={{ textShadow: '0 0 20px #00FF41' }}>
              SISTEMA COMPROMETIDO
            </div>
          </div>
        </div>
      )}

      {/* Fase reveal: texto narrativo aparece línea a línea */}
      {(phase === 'reveal' || phase === 'modal') && (
        <div className="relative z-10 font-mono max-w-xl w-full px-8">
          {NARRATIVE.slice(0, visibleLines).map((line, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, x: -12 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.15 }}
              className="text-sm leading-7 tracking-wider"
              style={{
                color: line === '' ? 'transparent'
                  : i === 0 ? '#FF4444'
                  : i === 4 ? '#00FF41'
                  : i === 6 ? '#FFD700'
                  : '#00FF41',
                textShadow: line && i !== 1
                  ? `0 0 10px ${i === 0 ? '#FF4444' : i === 4 ? '#00FF41' : '#FFD70080'}`
                  : undefined,
              }}
            >
              {line || '\u00A0'}
            </motion.div>
          ))}
        </div>
      )}

      {/* Modal final con botón */}
      <AnimatePresence>
        {phase === 'modal' && (
          <motion.div
            className="absolute z-20 bottom-16 left-1/2"
            style={{ x: '-50%' }}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3, duration: 0.4 }}
          >
            <button
              onClick={onComplete}
              className="px-10 py-3 bg-[#00FF41] text-black font-mono font-black text-sm
                         tracking-[0.3em] hover:bg-[#00FF41]/85 active:scale-95 transition-all"
              style={{ boxShadow: '0 0 20px #00FF41, 0 0 40px #00FF4140' }}
            >
              INICIAR PROTOCOLO PYTHON
            </button>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  )
}
