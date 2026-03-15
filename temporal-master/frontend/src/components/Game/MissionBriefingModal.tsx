'use client'

import { motion, AnimatePresence } from 'framer-motion'

interface Props {
  visible: boolean
  title: string
  loreBriefing: string
  pedagogicalObjective: string
  syntaxHint: string
  onInitialize: () => void
  onClose: () => void
}

export default function MissionBriefingModal({
  visible,
  title,
  loreBriefing,
  pedagogicalObjective,
  syntaxHint,
  onInitialize,
  onClose,
}: Props) {
  return (
    <AnimatePresence>
      {visible && (
        <>
          {/* Backdrop */}
          <motion.div
            key="backdrop"
            className="fixed inset-0 z-[90] bg-black/75"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
          />

          {/* Modal */}
          <motion.div
            key="modal"
            className="fixed inset-0 z-[91] flex items-center justify-center p-4"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <motion.div
              className="relative w-full max-w-lg bg-[#070D07] border border-[#00FF41]/30 font-mono overflow-hidden"
              style={{ boxShadow: '0 0 60px #00FF4118, 0 0 120px #00FF4108' }}
              initial={{ scale: 0.88, y: 24 }}
              animate={{ scale: 1, y: 0 }}
              exit={{ scale: 0.92, y: 16, opacity: 0 }}
              transition={{ type: 'spring', stiffness: 320, damping: 28 }}
            >
              {/* Scanlines */}
              <div
                className="absolute inset-0 pointer-events-none opacity-[0.03]"
                style={{
                  backgroundImage:
                    'repeating-linear-gradient(0deg,transparent,transparent 3px,#00FF41 3px,#00FF41 4px)',
                }}
              />

              {/* Header */}
              <div className="relative px-6 pt-5 pb-4 border-b border-[#00FF41]/15">
                <div className="flex items-center justify-between mb-2">
                  <motion.span
                    className="text-[10px] tracking-[0.35em] text-red-400/70 border border-red-500/30 px-2 py-0.5"
                    animate={{ opacity: [0.5, 1, 0.5] }}
                    transition={{ duration: 2, repeat: Infinity }}
                  >
                    TRANSMISIÓN ENTRANTE
                  </motion.span>
                  <button
                    onClick={onClose}
                    className="text-[#00FF41]/25 hover:text-[#00FF41]/60 text-xs tracking-widest transition-colors"
                  >
                    [ ESC ]
                  </button>
                </div>
                <h2
                  className="text-base font-black tracking-[0.15em] text-[#00FF41]"
                  style={{ textShadow: '0 0 12px #00FF4150' }}
                >
                  {title.toUpperCase()}
                </h2>
              </div>

              {/* Lore briefing */}
              <div className="relative px-6 py-5 border-b border-[#00FF41]/10">
                <div className="text-[10px] tracking-[0.3em] text-[#00FF41]/35 mb-3 uppercase">
                  Situación Táctica
                </div>
                <p className="text-xs leading-6 text-[#00FF41]/75">
                  {loreBriefing}
                </p>
              </div>

              {/* Inteligencia táctica */}
              <div className="relative px-6 py-5 border-b border-[#00FF41]/10 bg-[#050A05]">
                <div className="text-[10px] tracking-[0.3em] text-[#00FF41]/35 mb-4 uppercase">
                  Inteligencia Táctica
                </div>

                {/* Objetivo pedagógico */}
                <div className="flex items-start gap-2 mb-4">
                  <span className="text-[#00FF41]/30 text-xs mt-0.5 shrink-0">▸</span>
                  <div>
                    <div className="text-[9px] tracking-widest text-[#00FF41]/30 mb-1">OBJETIVO</div>
                    <p className="text-xs text-[#00FF41]/65 leading-5">{pedagogicalObjective}</p>
                  </div>
                </div>

                {/* Syntax hint */}
                <div>
                  <div className="text-[9px] tracking-widest text-[#00FF41]/30 mb-2">PROTOCOLO DE REFERENCIA</div>
                  <div className="relative bg-[#030D05] border border-[#00FF41]/20 overflow-hidden">
                    <div className="px-3 py-1 bg-[#040A04] border-b border-[#00FF41]/10">
                      <span className="text-[9px] font-mono text-[#00FF41]/25 tracking-widest">python</span>
                    </div>
                    <pre className="p-3 text-[12px] leading-5 font-mono text-[#00FF41]/80 overflow-x-auto">
                      <code>{syntaxHint}</code>
                    </pre>
                  </div>
                </div>
              </div>

              {/* CTA */}
              <div className="relative px-6 py-4 bg-[#030803]">
                <motion.button
                  onClick={onInitialize}
                  className="w-full py-3.5 bg-[#00FF41] text-black text-sm font-black tracking-[0.2em]
                             hover:bg-[#00FF41]/90 active:scale-[0.99] transition-all duration-100"
                  style={{ boxShadow: '0 0 30px #00FF4140' }}
                  animate={{
                    boxShadow: ['0 0 20px #00FF4130', '0 0 45px #00FF4165', '0 0 20px #00FF4130'],
                  }}
                  transition={{ duration: 2, repeat: Infinity }}
                  whileTap={{ scale: 0.98 }}
                >
                  INICIALIZAR ENLACE ▶
                </motion.button>
              </div>
            </motion.div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}
