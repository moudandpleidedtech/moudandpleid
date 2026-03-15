'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { motion, AnimatePresence } from 'framer-motion'
import { useUserStore } from '@/store/userStore'

// ─── Script de ENIGMA ────────────────────────────────────────────────────────

interface ScriptLine {
  delay: number
  text: string
  kind: 'system' | 'enigma' | 'blank'
}

const SCRIPT: ScriptLine[] = [
  { delay: 300,  kind: 'system',  text: '> ESTABLECIENDO CONEXION CON NUCLEOS CENTRALES...' },
  { delay: 900,  kind: 'system',  text: '> CONEXION ESTABLECIDA. PROTOCOLO ENIGMA ACTIVO.' },
  { delay: 1600, kind: 'blank',   text: '' },
  { delay: 2100, kind: 'enigma',  text: 'ENIGMA > Sistemas críticos caídos.' },
  { delay: 3100, kind: 'enigma',  text: 'ENIGMA > Arquitecto... lo estábamos esperando.' },
  { delay: 4300, kind: 'blank',   text: '' },
  { delay: 4800, kind: 'enigma',  text: 'ENIGMA > El repositorio central reporta 5 misiones activas.' },
  { delay: 5900, kind: 'enigma',  text: 'ENIGMA > Tu protocolo de autenticación ha sido registrado.' },
  { delay: 7000, kind: 'blank',   text: '' },
  { delay: 7500, kind: 'enigma',  text: 'ENIGMA > Cada fallo tuyo es información para mí.' },
  { delay: 8500, kind: 'enigma',  text: 'ENIGMA > No me decepciones.' },
  { delay: 9400, kind: 'blank',   text: '' },
  { delay: 9900, kind: 'system',  text: '> CARGANDO ENTORNO DE MISIONES...' },
]

export default function BootSequencePage() {
  const router = useRouter()
  const { username, userId } = useUserStore()
  const [visibleCount, setVisibleCount] = useState(0)
  const [showButton, setShowButton] = useState(false)

  // Guard: si no hay sesión activa, volver al login
  useEffect(() => {
    if (!userId) router.replace('/')
  }, [userId, router])

  useEffect(() => {
    if (!userId) return
    const timers: ReturnType<typeof setTimeout>[] = []

    SCRIPT.forEach((line, i) => {
      timers.push(setTimeout(() => setVisibleCount(i + 1), line.delay))
    })

    const last = SCRIPT[SCRIPT.length - 1].delay
    timers.push(setTimeout(() => setShowButton(true), last + 700))

    return () => timers.forEach(clearTimeout)
  }, [userId])

  const handleEnter = () => {
    localStorage.setItem('boot_seen', '1')
    router.push('/misiones')
  }

  return (
    <div className="min-h-screen bg-[#0A0A0A] font-mono text-[#00FF41] flex flex-col justify-center px-8 md:px-32 relative overflow-hidden">

      {/* CRT scanlines */}
      <div className="fixed inset-0 pointer-events-none z-10"
        style={{ backgroundImage: 'repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,0.06) 2px,rgba(0,0,0,0.06) 4px)' }} />

      {/* Vignette */}
      <div className="fixed inset-0 pointer-events-none z-10"
        style={{ background: 'radial-gradient(ellipse at center,transparent 55%,rgba(0,0,0,0.6) 100%)' }} />

      <div className="relative z-20 max-w-2xl w-full">

        {/* Header */}
        <div className="text-[#00FF41]/20 text-xs tracking-[0.5em] mb-10 uppercase">
          Enigma // Protocolo de Arranque // Secuencia 01
        </div>

        {/* Arquitecto identificado */}
        {username && (
          <div className="text-[#00FF41]/25 text-xs mb-8 tracking-widest">
            ARQUITECTO IDENTIFICADO:{' '}
            <span className="text-[#00FF41]/50">{username.toUpperCase()}</span>
          </div>
        )}

        {/* Script lines */}
        <div className="space-y-2">
          {SCRIPT.slice(0, visibleCount).map((line, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, x: -12 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.18 }}
              className={`text-sm leading-7 ${
                line.kind === 'blank'   ? 'h-2' :
                line.kind === 'enigma' ? 'text-[#00FF41]' :
                'text-[#00FF41]/40'
              }`}
              style={line.kind === 'enigma' ? { textShadow: '0 0 10px #00FF4155' } : undefined}
            >
              {line.text || '\u00A0'}
            </motion.div>
          ))}
        </div>

        {/* CTA */}
        <AnimatePresence>
          {showButton && (
            <motion.div
              className="mt-14"
              initial={{ opacity: 0, y: 18 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4 }}
            >
              <button
                onClick={handleEnter}
                className="px-10 py-3 bg-[#00FF41] text-black font-black text-sm
                           tracking-[0.3em] hover:bg-[#00FF41]/85 active:scale-95 transition-all"
                style={{ boxShadow: '0 0 20px #00FF41, 0 0 40px #00FF4140' }}
              >
                ACCEDER AL SISTEMA
              </button>
            </motion.div>
          )}
        </AnimatePresence>

      </div>
    </div>
  )
}
