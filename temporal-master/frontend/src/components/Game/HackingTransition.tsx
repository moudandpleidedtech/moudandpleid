'use client'

import { useEffect, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

// ─── Líneas de terminal que aparecen en secuencia ──────────────────────────────

const TERMINAL_LINES = [
  { text: '> VERIFICANDO CREDENCIALES DE OPERADOR...', color: '#00FF41', delay: 0 },
  { text: '> ANALIZANDO PROTOCOLO DE SEGURIDAD ÁREA 51...', color: '#00FF41', delay: 160 },
  { text: '> BYPASS FIREWALL: [██████████░░░░░░] 62%', color: '#FFD700', delay: 320 },
  { text: '> INYECTANDO PAYLOAD DE INFILTRACIÓN...', color: '#00FF41', delay: 480 },
  { text: '> BYPASS FIREWALL: [████████████████] 100%', color: '#FFD700', delay: 620 },
  { text: '> COMPILANDO MÓDULOS DE PYTHON...', color: '#00FF41', delay: 760 },
  { text: '> ENLACE DE DAKI ESTABLECIDO ◈', color: '#00FF41', delay: 880 },
  { text: '> ACCESO CONCEDIDO — INICIANDO MISIÓN', color: '#00FF41', delay: 980 },
]

// ─── Caracteres de ruido de fondo ──────────────────────────────────────────────

function NoiseRow({ seed }: { seed: number }) {
  const chars = Array.from({ length: 48 }, (_, i) =>
    '0123456789ABCDEF∴∵∶∷'[(seed * 7 + i * 13) % 22]
  ).join(' ')
  return (
    <div
      className="font-mono text-[9px] text-[#00FF41]/8 leading-4 whitespace-nowrap overflow-hidden select-none pointer-events-none"
      style={{ marginLeft: `${(seed * 17) % 40}%` }}
    >
      {chars}
    </div>
  )
}

// ─── Componente principal ──────────────────────────────────────────────────────

interface HackingTransitionProps {
  isActive: boolean
  missionTitle?: string
}

export default function HackingTransition({ isActive, missionTitle }: HackingTransitionProps) {
  const [visibleLines, setVisibleLines] = useState(0)
  const [phase, setPhase] = useState<'boot' | 'terminal' | 'granted'>('boot')

  // Reiniciar estado cada vez que se activa
  useEffect(() => {
    if (!isActive) {
      // Reset para la próxima vez
      setVisibleLines(0)
      setPhase('boot')
      return
    }

    // Fase 1: pantalla de boot (300ms)
    const t1 = setTimeout(() => setPhase('terminal'), 300)

    return () => clearTimeout(t1)
  }, [isActive])

  // Fase 2: revelar líneas de terminal
  useEffect(() => {
    if (phase !== 'terminal') return

    const timers: ReturnType<typeof setTimeout>[] = []

    TERMINAL_LINES.forEach((_, i) => {
      const t = setTimeout(() => setVisibleLines(i + 1), TERMINAL_LINES[i].delay)
      timers.push(t)
    })

    // Fase 3: ACCESO CONCEDIDO
    const lastDelay = TERMINAL_LINES[TERMINAL_LINES.length - 1].delay
    const t3 = setTimeout(() => setPhase('granted'), lastDelay + 180)
    timers.push(t3)

    return () => timers.forEach(clearTimeout)
  }, [phase])

  if (!isActive) return null

  return (
    <AnimatePresence>
      <motion.div
        className="fixed inset-0 z-[9999] bg-black flex flex-col overflow-hidden"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        transition={{ duration: 0.15 }}
      >
        {/* Scanlines */}
        <div
          className="absolute inset-0 pointer-events-none"
          style={{
            backgroundImage:
              'repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,255,65,0.025) 2px,rgba(0,255,65,0.025) 4px)',
          }}
        />

        {/* Ruido de fondo */}
        <div className="absolute inset-0 flex flex-col justify-around py-6 pointer-events-none">
          {Array.from({ length: 14 }).map((_, i) => (
            <NoiseRow key={i} seed={i} />
          ))}
        </div>

        {/* Contenido central */}
        <div className="relative z-10 flex flex-col items-center justify-center flex-1 px-8">

          {/* Anillo de escaneo */}
          <div className="relative flex items-center justify-center mb-10">
            <motion.div
              className="w-24 h-24 rounded-full border-2 border-[#00FF41]/30"
              animate={{ scale: [1, 1.15, 1], opacity: [0.3, 0.6, 0.3] }}
              transition={{ duration: 1.8, repeat: Infinity, ease: 'easeInOut' }}
            />
            <motion.div
              className="absolute w-20 h-20 rounded-full border border-[#00FF41]/50"
              animate={{ rotate: 360 }}
              transition={{ duration: 2.4, repeat: Infinity, ease: 'linear' }}
              style={{
                borderTopColor: '#00FF41',
                borderRightColor: 'transparent',
                borderBottomColor: 'transparent',
                borderLeftColor: 'transparent',
              }}
            />
            <motion.div
              className="absolute w-14 h-14 rounded-full border border-[#00FF41]/30"
              animate={{ rotate: -360 }}
              transition={{ duration: 1.6, repeat: Infinity, ease: 'linear' }}
              style={{
                borderTopColor: 'transparent',
                borderRightColor: '#00FF41',
                borderBottomColor: 'transparent',
                borderLeftColor: 'transparent',
              }}
            />
            {/* Núcleo */}
            <motion.div
              className="absolute w-6 h-6 rounded-full bg-[#00FF41]/20 flex items-center justify-center"
              animate={{ opacity: [0.4, 1, 0.4] }}
              transition={{ duration: 0.8, repeat: Infinity }}
            >
              <span className="text-[#00FF41] text-sm" style={{ textShadow: '0 0 8px #00FF41' }}>◈</span>
            </motion.div>
          </div>

          {/* Terminal de hackeo */}
          <div
            className="w-full max-w-lg border border-[#00FF41]/20 bg-black/70 px-6 py-5"
            style={{ boxShadow: '0 0 40px rgba(0,255,65,0.08), inset 0 0 20px rgba(0,255,65,0.03)' }}
          >
            {/* Header del terminal */}
            <div className="flex items-center gap-2 mb-4 pb-3 border-b border-[#00FF41]/10">
              <div className="w-2.5 h-2.5 rounded-full bg-red-500/60" />
              <div className="w-2.5 h-2.5 rounded-full bg-yellow-500/60" />
              <div className="w-2.5 h-2.5 rounded-full bg-green-500/60" />
              <span className="ml-2 text-[9px] tracking-[0.4em] text-[#00FF41]/30 font-mono">
                DAKI // CANAL DE INFILTRACIÓN
              </span>
              {missionTitle && (
                <span className="ml-auto text-[9px] tracking-wider text-[#00FF41]/20 truncate max-w-[160px]">
                  {missionTitle.toUpperCase()}
                </span>
              )}
            </div>

            {/* Líneas de terminal */}
            <div className="font-mono text-[11px] leading-6 min-h-[10rem]">
              {TERMINAL_LINES.slice(0, visibleLines).map((line, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, x: -8 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.12 }}
                  style={{ color: line.color }}
                >
                  {line.text}
                  {/* Cursor solo en la última línea visible */}
                  {i === visibleLines - 1 && phase !== 'granted' && (
                    <motion.span
                      className="inline-block w-2 h-3 ml-1 bg-[#00FF41] align-middle"
                      animate={{ opacity: [1, 0] }}
                      transition={{ duration: 0.5, repeat: Infinity, repeatType: 'reverse' }}
                    />
                  )}
                </motion.div>
              ))}
            </div>
          </div>

          {/* Flash de acceso concedido */}
          <AnimatePresence>
            {phase === 'granted' && (
              <motion.div
                className="mt-8 text-center"
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.2 }}
              >
                <motion.p
                  className="font-mono font-black text-lg tracking-[0.4em] text-[#00FF41]"
                  style={{ textShadow: '0 0 20px #00FF41, 0 0 40px rgba(0,255,65,0.5)' }}
                  animate={{ opacity: [1, 0.5, 1] }}
                  transition={{ duration: 0.4, repeat: Infinity }}
                >
                  [ ACCESO CONCEDIDO ]
                </motion.p>
                <p className="font-mono text-[9px] tracking-[0.5em] text-[#00FF41]/30 mt-2">
                  CARGANDO ENTORNO DE MISIÓN...
                </p>
              </motion.div>
            )}
          </AnimatePresence>

        </div>
      </motion.div>
    </AnimatePresence>
  )
}
