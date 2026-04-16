'use client'

import { useMemo } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useRouter } from 'next/navigation'

// ─── Habilidades adquiridas en el Sector 01 ───────────────────────────────────
const SECTOR_01_SKILLS = [
  { icon: '◈', label: 'print()',      desc: 'Transmisión de datos' },
  { icon: '◈', label: 'Variables',    desc: 'Memoria del sistema' },
  { icon: '◈', label: 'input()',      desc: 'Recepción de señales' },
  { icon: '◈', label: 'int() / str()', desc: 'Conversión de tipos' },
  { icon: '◈', label: 'Aritmética',   desc: 'Cálculo de recursos' },
  { icon: '◈', label: 'f-strings',    desc: 'Formato de datos' },
  { icon: '◈', label: 'if / else',    desc: 'Toma de decisiones' },
]

// ─── Preview bloqueado del Sector 02 ─────────────────────────────────────────
const SECTOR_02_PREVIEW = [
  { title: 'El Ciclo Infinito',      concept: 'while loops' },
  { title: 'Patrulla de Secuencias', concept: 'for loops + range()' },
  { title: 'Lista de Objetivos',     concept: 'listas y append()' },
]

interface Props {
  visible: boolean
  xpEarned: number
  totalAttempts: number
  onUpgrade: () => void
  onHub: () => void
}

export default function SectorCompleteModal({ visible, xpEarned, totalAttempts, onUpgrade, onHub }: Props) {
  const router = useRouter()

  // Feature 5: guardar flag de "calibrado" para el badge del Hub
  useMemo(() => {
    if (visible) {
      try { localStorage.setItem('nexo_calibrated', '1') } catch { /* */ }
    }
  }, [visible])

  const rating = useMemo(() => {
    if (totalAttempts <= 15) return { text: 'OPERADOR ÉLITE',          color: '#FFD700' }
    if (totalAttempts <= 30) return { text: 'OPERADOR ESTÁNDAR',       color: '#00FF41' }
    return                         { text: 'OPERADOR EN FORMACIÓN',    color: '#60A5FA' }
  }, [totalAttempts])

  // router usado en onHub prop — suprime warning de lint
  void router

  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          className="fixed inset-0 z-[90] flex items-center justify-center overflow-y-auto py-8"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.3 }}
        >
          {/* Backdrop */}
          <div
            className="absolute inset-0"
            style={{ background: 'radial-gradient(ellipse at center, rgba(0,20,5,0.98) 0%, rgba(0,0,0,0.99) 70%)' }}
          />

          {/* Grid pattern */}
          <div className="absolute inset-0 opacity-[0.025] pointer-events-none" style={{
            backgroundImage: 'linear-gradient(rgba(0,255,65,0.8) 1px, transparent 1px), linear-gradient(90deg,rgba(0,255,65,0.8) 1px,transparent 1px)',
            backgroundSize: '48px 48px',
          }} />

          {/* Scan beam */}
          <motion.div
            className="absolute inset-x-0 h-px pointer-events-none"
            style={{ background: 'linear-gradient(90deg, transparent, #00FF41, transparent)', boxShadow: '0 0 20px #00FF41' }}
            initial={{ top: '-2px' }}
            animate={{ top: '102%' }}
            transition={{ duration: 3, ease: 'linear', repeat: Infinity, repeatDelay: 1 }}
          />

          {/* Modal card */}
          <motion.div
            className="relative z-10 w-full max-w-lg mx-4 font-mono"
            style={{
              border: '1px solid rgba(0,255,65,0.4)',
              background: 'rgba(0,10,2,0.97)',
              boxShadow: '0 0 60px rgba(0,255,65,0.15), inset 0 0 40px rgba(0,255,65,0.03)',
            }}
            initial={{ scale: 0.85, y: 40, opacity: 0 }}
            animate={{ scale: 1, y: 0, opacity: 1 }}
            exit={{ scale: 0.92, opacity: 0 }}
            transition={{ type: 'spring', stiffness: 260, damping: 22, delay: 0.1 }}
          >
            {/* Esquinas decorativas */}
            {[
              'top-0 left-0 border-t-2 border-l-2',
              'top-0 right-0 border-t-2 border-r-2',
              'bottom-0 left-0 border-b-2 border-l-2',
              'bottom-0 right-0 border-b-2 border-r-2',
            ].map((cls, i) => (
              <div key={i} className={`absolute w-5 h-5 border-[#00FF41]/50 ${cls}`} />
            ))}

            <div className="p-7">
              {/* Header */}
              <motion.div
                className="text-center mb-6"
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
              >
                <div className="text-[#00FF41]/40 text-[9px] tracking-[0.8em] uppercase mb-3">
                  // NEXO — PROTOCOLO DE ASCENSO //
                </div>
                <div
                  className="font-black leading-none mb-1"
                  style={{
                    fontSize: 'clamp(1.8rem, 5vw, 2.8rem)',
                    letterSpacing: '0.1em',
                    color: '#00FF41',
                    textShadow: '0 0 30px #00FF41, 0 0 60px #00FF4150',
                  }}
                >
                  SECTOR 01
                </div>
                <div
                  className="font-black leading-none"
                  style={{
                    fontSize: 'clamp(1.2rem, 3vw, 1.8rem)',
                    letterSpacing: '0.15em',
                    color: '#00FF41',
                    textShadow: '0 0 20px #00FF4170',
                  }}
                >
                  COMPLETADO
                </div>
                <div className="mt-3 text-xs tracking-[0.3em]" style={{ color: rating.color }}>
                  {rating.text}
                </div>
              </motion.div>

              {/* Stats strip */}
              <motion.div
                className="flex justify-center gap-8 mb-6 py-3 border-y border-[#00FF41]/15"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.3 }}
              >
                <div className="text-center">
                  <div className="text-[#FFD700] font-black text-xl">+{xpEarned}</div>
                  <div className="text-[#00FF41]/40 text-[9px] tracking-[0.3em]">XP TOTAL</div>
                </div>
                <div className="w-px bg-[#00FF41]/10" />
                <div className="text-center">
                  <div className="text-[#00FF41] font-black text-xl">10</div>
                  <div className="text-[#00FF41]/40 text-[9px] tracking-[0.3em]">MISIONES</div>
                </div>
                <div className="w-px bg-[#00FF41]/10" />
                <div className="text-center">
                  <div className="text-[#00FF41] font-black text-xl">7</div>
                  <div className="text-[#00FF41]/40 text-[9px] tracking-[0.3em]">HABILIDADES</div>
                </div>
              </motion.div>

              {/* Habilidades adquiridas */}
              <motion.div
                className="mb-6"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.4 }}
              >
                <div className="text-[#00FF41]/40 text-[9px] tracking-[0.5em] uppercase mb-3">
                  HABILIDADES ADQUIRIDAS
                </div>
                <div className="grid grid-cols-2 gap-1.5">
                  {SECTOR_01_SKILLS.map((skill, i) => (
                    <motion.div
                      key={skill.label}
                      className="flex items-center gap-2 px-2.5 py-1.5 border border-[#00FF41]/15 bg-[#00FF41]/[0.03]"
                      initial={{ opacity: 0, x: -8 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: 0.45 + i * 0.05 }}
                    >
                      <span className="text-[#00FF41]/60 text-[10px]">{skill.icon}</span>
                      <div>
                        <div className="text-[#00FF41]/90 text-[10px] font-bold tracking-wider">{skill.label}</div>
                        <div className="text-[#00FF41]/30 text-[8px] tracking-wider">{skill.desc}</div>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </motion.div>

              {/* Separador */}
              <motion.div
                className="flex items-center gap-3 mb-5"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.65 }}
              >
                <div className="flex-1 h-px bg-[#00FF41]/10" />
                <div className="text-[#00FF41]/30 text-[8px] tracking-[0.5em]">SIGUIENTE SECTOR — BLOQUEADO</div>
                <div className="flex-1 h-px bg-[#00FF41]/10" />
              </motion.div>

              {/* Preview Sector 02 */}
              <motion.div
                className="mb-6"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.7 }}
              >
                <div className="space-y-1.5">
                  {SECTOR_02_PREVIEW.map((level) => (
                    <div
                      key={level.title}
                      className="flex items-center justify-between px-3 py-2 border border-[#FFFFFF]/5 opacity-55"
                      style={{ filter: 'blur(0.3px)' }}
                    >
                      <div className="flex items-center gap-2.5">
                        <div className="w-4 h-4 border border-[#00FF41]/20 flex items-center justify-center">
                          <div className="w-1.5 h-1.5 bg-[#00FF41]/20" />
                        </div>
                        <div>
                          <div className="text-white/40 text-[10px] font-bold tracking-wider">{level.title}</div>
                          <div className="text-[#00FF41]/25 text-[8px] tracking-wider">{level.concept}</div>
                        </div>
                      </div>
                      <span className="text-[#00FF41]/25 text-[10px]">🔒</span>
                    </div>
                  ))}
                  <div className="text-center py-1">
                    <span className="text-[#00FF41]/20 text-[8px] tracking-[0.4em]">+ 90 MISIONES MÁS</span>
                  </div>
                </div>
              </motion.div>

              {/* Transmisión DAKI */}
              <motion.div
                className="mb-6 px-4 py-3 border-l-2 border-[#00FF41]/30 bg-[#00FF41]/[0.02]"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.8 }}
              >
                <div className="text-[9px] tracking-[0.4em] text-[#00FF41]/30 mb-1.5">TRANSMISIÓN DAKI</div>
                <p className="text-[11px] text-green-200/55 leading-relaxed">
                  Sector 01 neutralizado. Tus métricas son sólidas, Operador.
                  El Sector 02 introduce los bucles — el concepto que separa
                  a los operadores de los programadores reales.
                  La puerta está ahí. Solo necesitás la llave.
                </p>
              </motion.div>

              {/* Feature 4: Anomalía diaria — retención gratuita post-tier */}
              <motion.div
                className="mb-5 px-4 py-3 border border-[#00FF41]/15 bg-[#00FF41]/[0.02]"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.85 }}
              >
                <div className="flex items-center gap-2 mb-1.5">
                  <motion.span
                    className="w-1.5 h-1.5 rounded-full bg-[#00FF41]"
                    animate={{ opacity: [0.4, 1, 0.4] }}
                    transition={{ duration: 2, repeat: Infinity }}
                  />
                  <span className="text-[9px] tracking-[0.45em] font-bold" style={{ color: 'rgba(0,255,65,0.60)' }}>
                    MIENTRAS DECIDÍS
                  </span>
                </div>
                <p className="text-[10px] leading-relaxed" style={{ color: 'rgba(0,255,65,0.50)' }}>
                  DAKI te manda una incursión distinta cada día — gratis, sin límite de tiempo.
                  Accedé desde el Centro de Mando. El hábito no espera.
                </p>
              </motion.div>

              {/* CTAs */}
              <motion.div
                className="flex flex-col gap-2.5"
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.9 }}
              >
                <button
                  onClick={onUpgrade}
                  className="w-full py-3.5 font-black text-xs tracking-[0.22em] transition-all duration-150 active:scale-[0.98]"
                  style={{ background: '#00FF41', color: '#000', boxShadow: '0 0 25px rgba(0,255,65,0.5)' }}
                >
                  [ DESBLOQUEAR ACCESO COMPLETO → ]
                </button>
                <button
                  onClick={onHub}
                  className="w-full py-2.5 text-[#00FF41]/50 text-xs font-bold tracking-[0.18em] border border-[#00FF41]/15 hover:border-[#00FF41]/35 hover:text-[#00FF41]/75 transition-all duration-150"
                >
                  VOLVER AL CENTRO DE MANDO
                </button>
              </motion.div>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}
