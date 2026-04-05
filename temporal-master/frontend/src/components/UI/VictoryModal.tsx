'use client'

import { useMemo } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useRouter } from 'next/navigation'

// ─── Partículas internas del modal ────────────────────────────────────────────

function ModalParticles() {
  const particles = useMemo(() => {
    return Array.from({ length: 20 }, (_, i) => ({
      id: i,
      x: ((i * 13 + 7) % 90) + 5,  // 5–95% horizontal
      delay: (i % 6) * 0.06,
      dur: 0.55 + (i % 4) * 0.07,
      size: 2 + (i % 3),
      color: i % 4 === 0 ? '#FFD700' : '#00FF41',
    }))
  }, [])

  return (
    <div className="absolute inset-0 pointer-events-none overflow-hidden">
      {particles.map(p => (
        <motion.div
          key={p.id}
          className="absolute rounded-full"
          style={{
            width: p.size,
            height: p.size,
            left: `${p.x}%`,
            top: '50%',
            background: p.color,
            boxShadow: `0 0 ${p.size * 3}px ${p.color}`,
          }}
          initial={{ opacity: 1, y: 0, scale: 1 }}
          animate={{ opacity: [1, 0.8, 0], y: -80 - (p.id % 40), scale: [1, 1.3, 0.4] }}
          transition={{ duration: p.dur, delay: p.delay, ease: 'easeOut' }}
        />
      ))}
    </div>
  )
}

// ─── Tipos ────────────────────────────────────────────────────────────────────

export interface VictoryNext {
  id: string
  title: string
  isDrone: boolean
  isLocked?: boolean
}

interface Props {
  visible: boolean
  xpEarned: number
  next: VictoryNext | null
  onNext: () => void
  onReview: () => void
  titleOverride?: string
}

// ─── Componente ───────────────────────────────────────────────────────────────

export default function VictoryModal({ visible, xpEarned, next, onNext, onReview, titleOverride }: Props) {
  const router = useRouter()

  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          className="fixed inset-0 z-[80] flex items-center justify-center"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.2 }}
        >
          {/* Backdrop con blur */}
          <div className="absolute inset-0 bg-black/75 backdrop-blur-md" onClick={onReview} />

          {/* Contenedor glassmorphism */}
          <motion.div
            className="relative z-10 w-full max-w-md mx-4 p-8 bg-black/90 border border-green-500/70 font-mono overflow-hidden"
            style={{
              boxShadow:
                '0 0 30px rgba(0,255,65,0.3), inset 0 0 40px rgba(0,255,65,0.03)',
            }}
            initial={{ scale: 0.72, y: 48, opacity: 0 }}
            animate={{ scale: 1, y: 0, opacity: 1 }}
            exit={{ scale: 0.88, opacity: 0 }}
            transition={{ type: 'spring', stiffness: 290, damping: 22 }}
          >
            {/* Esquinas decorativas */}
            <div className="absolute top-0 left-0 w-4 h-4 border-t-2 border-l-2 border-[#00FF41]/60" />
            <div className="absolute top-0 right-0 w-4 h-4 border-t-2 border-r-2 border-[#00FF41]/60" />
            <div className="absolute bottom-0 left-0 w-4 h-4 border-b-2 border-l-2 border-[#00FF41]/60" />
            <div className="absolute bottom-0 right-0 w-4 h-4 border-b-2 border-r-2 border-[#00FF41]/60" />

            {/* Partículas de celebración — explotan al aparecer el modal */}
            <ModalParticles />

            {/* Línea de barrido */}
            <motion.div
              className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-[#00FF41]/60 to-transparent"
              initial={{ x: '-100%' }}
              animate={{ x: '100%' }}
              transition={{ duration: 1.2, ease: 'easeInOut' }}
            />

            {/* Título parpadeante */}
            <motion.div
              className="text-center mb-1"
              animate={{ opacity: [1, 0.35, 1] }}
              transition={{ duration: 1.4, repeat: Infinity, ease: 'easeInOut' }}
            >
              <span
                className="text-[#00FF41] font-black text-xl tracking-[0.25em]"
                style={{ textShadow: '0 0 20px #00FF41, 0 0 55px #00FF4175' }}
              >
                {titleOverride ?? '[ ACCESO CONCEDIDO ]'}
              </span>
            </motion.div>

            <div className="text-center text-[#00FF41]/30 text-[9px] tracking-[0.5em] mb-5">
              {titleOverride ? 'TUTORIAL SUPERADO · DRON OPERATIVO' : 'FIREWALL VULNERADO · PROTOCOLO COMPLETADO'}
            </div>

            {/* Separador */}
            <div className="h-px bg-gradient-to-r from-transparent via-[#00FF41]/35 to-transparent mb-5" />

            {/* Badge XP */}
            <div className="flex items-center justify-center mb-5">
              <motion.div
                className="px-7 py-2 border border-[#FFD700]/50 bg-[#FFD700]/5"
                animate={{
                  boxShadow: [
                    '0 0 10px rgba(255,215,0,0.2)',
                    '0 0 28px rgba(255,215,0,0.45)',
                    '0 0 10px rgba(255,215,0,0.2)',
                  ],
                }}
                transition={{ duration: 1.8, repeat: Infinity }}
              >
                <span
                  className="text-[#FFD700] font-black text-2xl tracking-widest"
                  style={{ textShadow: '0 0 12px rgba(255,215,0,0.6)' }}
                >
                  +{xpEarned} XP
                </span>
              </motion.div>
            </div>

            {/* Transmisión DAKI */}
            <div
              className="bg-black/60 border-l-2 border-[#00FF41]/40 px-4 py-3 mb-6"
              style={{ boxShadow: 'inset 0 0 16px rgba(0,255,65,0.04)' }}
            >
              <p className="text-[9px] tracking-[0.4em] text-[#00FF41]/40 mb-1.5">
                TRANSMISIÓN DE DAKI
              </p>
              <p className="text-[11px] text-green-200/60 leading-relaxed">
                {titleOverride
                  ? 'Calibración sináptica completada. Tus nodos neuronales están sincronizados. Las incursiones del Nexo están ahora desbloqueadas, Operador.'
                  : 'Misión completada. DAKI ha desencriptado un nuevo archivo en tu Bitácora Táctica. Revísalo para extraer el conocimiento operacional del sector.'
                }
              </p>
            </div>

            {/* Botones */}
            <div className="flex flex-col gap-2.5">
              {/* Primario — Centro de Mando */}
              <button
                onClick={() => router.push('/hub')}
                className="w-full py-3 bg-[#00FF41] text-black font-black text-xs tracking-[0.22em] hover:bg-[#00FF41]/85 active:scale-[0.98] transition-all duration-100"
                style={{ boxShadow: '0 0 20px #00FF4148' }}
              >
                [ VOLVER AL CENTRO DE MANDO ]
              </button>

              {/* Secundario — Siguiente nodo (si existe) */}
              {next && (
                <button
                  onClick={onNext}
                  className={`w-full py-2.5 text-xs font-bold tracking-[0.18em] border transition-all duration-150 truncate px-3 ${
                    next.isLocked
                      ? 'text-[#00FF41]/35 border-[#00FF41]/15 hover:border-[#00FF41]/30 hover:text-[#00FF41]/50'
                      : 'text-[#00FF41]/65 border-[#00FF41]/28 hover:border-[#00FF41]/65 hover:text-[#00FF41]'
                  }`}
                >
                  {next.isLocked
                    ? 'VER LISTA DE MISIONES →'
                    : `SIGUIENTE NODO → ${next.title.toUpperCase()}`}
                </button>
              )}

              {/* Terciario — Revisar código */}
              <button
                onClick={onReview}
                className="w-full py-1.5 text-[#00FF41]/28 text-[10px] tracking-[0.2em] hover:text-[#00FF41]/55 transition-colors duration-150"
              >
                REVISAR MI CÓDIGO
              </button>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}
