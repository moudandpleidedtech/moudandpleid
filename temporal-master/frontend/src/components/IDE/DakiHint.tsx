'use client'

import { motion, AnimatePresence } from 'framer-motion'

// ─── Props ────────────────────────────────────────────────────────────────────

interface Props {
  visible: boolean       // hintIndex >= 0
  hints: string[]        // array de 3 pistas progresivas de la API
  hintIndex: number      // índice actual (0-based, nunca retrocede)
}

// ─── Componente ───────────────────────────────────────────────────────────────

export default function DakiHint({ visible, hints, hintIndex }: Props) {
  if (!hints || hints.length === 0) return null

  const idx = Math.min(Math.max(hintIndex, 0), hints.length - 1)
  const currentHint = hints[idx]
  const total = hints.length

  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          key="daki-hint"
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          exit={{ opacity: 0, height: 0 }}
          transition={{ duration: 0.32, ease: 'easeInOut' }}
          className="overflow-hidden shrink-0"
        >
          <div
            className="mx-0 border-t border-b border-cyan-500/30 bg-[#050f0f] font-mono"
            style={{ boxShadow: 'inset 0 0 20px rgba(0,229,255,0.04)' }}
          >
            {/* Header parpadeante */}
            <motion.div
              className="flex items-center justify-between px-3 py-1.5 border-b border-cyan-500/20"
              animate={{ opacity: [1, 0.45, 1] }}
              transition={{ duration: 2, repeat: Infinity, ease: 'easeInOut' }}
            >
              <div className="flex items-center gap-2">
                <motion.span
                  className="w-1.5 h-1.5 rounded-full bg-cyan-400 shrink-0"
                  animate={{ opacity: [0.4, 1, 0.4] }}
                  transition={{ duration: 1.2, repeat: Infinity }}
                  style={{ boxShadow: '0 0 6px rgba(0,229,255,0.8)' }}
                />
                <span
                  className="text-[9px] tracking-[0.45em] text-cyan-400/80 font-bold"
                  style={{ textShadow: '0 0 8px rgba(0,229,255,0.5)' }}
                >
                  [ MENSAJE ENTRANTE DE DAKI ]
                </span>
              </div>
              {/* Indicador de progreso de pista */}
              <span className="text-[8px] tracking-widest text-cyan-400/40 font-bold">
                PISTA {idx + 1}/{total}
              </span>
            </motion.div>

            {/* Cuerpo del mensaje — animado al cambiar de pista */}
            <AnimatePresence mode="wait">
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 4 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -4 }}
                transition={{ duration: 0.22 }}
                className="px-3 py-2.5"
              >
                <div className="flex items-start gap-2">
                  <span className="text-cyan-400/40 text-[9px] shrink-0 mt-0.5">▸</span>
                  <p className="text-[10px] text-cyan-300/65 leading-relaxed">
                    {currentHint}
                  </p>
                </div>
              </motion.div>
            </AnimatePresence>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}
