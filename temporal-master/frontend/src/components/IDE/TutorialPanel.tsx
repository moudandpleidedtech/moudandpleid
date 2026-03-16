'use client'

import { motion, AnimatePresence } from 'framer-motion'

// ─── Contenido por fase ───────────────────────────────────────────────────────

interface StepContent {
  dakiLore: string
  instruction: string
}

const STEP_CONTENT: Record<number, StepContent> = {
  1: {
    dakiLore:
      '[DAKI]: Operador, primero probaremos los reflejos del sistema. El código ya está inyectado. Ubica el botón verde [EJECUTAR] en la esquina superior derecha y presiónalo.',
    instruction: 'Presiona el botón verde [ EJECUTAR ] para iniciar la secuencia de diagnóstico.',
  },
  2: {
    dakiLore:
      '[DAKI]: Excelente. Ahora la sintaxis. Hay ruido en la línea 2. Faltan las comillas de cierre al final del texto. Corrígelo y vuelve a ejecutar.',
    instruction: 'Añade las comillas de cierre " antes del ) al final de la línea print.',
  },
  3: {
    dakiLore:
      '[DAKI]: El Nexo necesita almacenar tu ID. Crea una variable llamada operador y asígnale el valor 1.',
    instruction: 'Escribe debajo del comentario: operador = 1 y ejecuta.',
  },
  4: {
    dakiLore:
      '[DAKI]: Fase final. En el Nexo no solo imprimimos datos, los devolvemos al sistema para que abran las compuertas. En la línea 2, borra print("Enlace Listo") y escribe exactamente esto: return "Enlace Listo"',
    instruction: 'En la línea 2, dentro de finalizar_enlace(), borra print("Enlace Listo") y escribe: return "Enlace Listo"',
  },
}

const TOTAL_STEPS = 4

// ─── Props ────────────────────────────────────────────────────────────────────

interface Props {
  tutorialStep: number
  syncProgress: number
}

// ─── Componente ───────────────────────────────────────────────────────────────

export default function TutorialPanel({ tutorialStep, syncProgress }: Props) {
  const content = STEP_CONTENT[tutorialStep] ?? STEP_CONTENT[1]
  const allDone = syncProgress >= 100

  return (
    <div className="flex-1 flex flex-col overflow-hidden border-b border-[#00FF41]/20">

      {/* ── Cabecera ── */}
      <div className="px-3 py-2 border-b border-[#00FF41]/10 shrink-0">
        <div className="flex items-center gap-2 mb-2.5">
          <motion.span
            className="w-1.5 h-1.5 rounded-full bg-cyan-400 shrink-0"
            animate={{ opacity: [0.4, 1, 0.4] }}
            transition={{ duration: 1.4, repeat: Infinity }}
            style={{ boxShadow: '0 0 6px rgba(0,229,255,0.8)' }}
          />
          <span className="text-[9px] tracking-[0.4em] text-cyan-400/70 font-bold uppercase">
            Calibración Sináptica — DAKI
          </span>
        </div>

        {/* Indicadores de fase */}
        <div className="flex items-center gap-1.5">
          {Array.from({ length: TOTAL_STEPS }, (_, i) => i + 1).map((s) => {
            const done   = s < tutorialStep || allDone
            const active = s === tutorialStep && !allDone
            return (
              <div
                key={s}
                className={[
                  'flex items-center justify-center w-6 h-6 text-[8px] font-black border transition-all duration-300',
                  done
                    ? 'bg-[#00FF41]/15 border-[#00FF41]/50 text-[#00FF41]'
                    : active
                    ? 'bg-cyan-500/15 border-cyan-400/60 text-cyan-300'
                    : 'bg-transparent border-[#00FF41]/12 text-[#00FF41]/18',
                ].join(' ')}
                style={
                  done
                    ? { boxShadow: '0 0 5px rgba(0,255,65,0.25)' }
                    : active
                    ? { boxShadow: '0 0 8px rgba(0,229,255,0.35)' }
                    : undefined
                }
              >
                {done ? '✓' : s}
              </div>
            )
          })}
          <span className="text-[9px] text-[#00FF41]/25 tracking-widest ml-1.5">
            {allDone ? 'COMPLETADO' : `FASE ${tutorialStep}/${TOTAL_STEPS}`}
          </span>
        </div>
      </div>

      {/* ── Contenido dinámico ── */}
      <div className="flex-1 overflow-y-auto p-3 space-y-3">
        <AnimatePresence mode="wait">
          {allDone ? (
            <motion.div
              key="done"
              className="border border-[#00FF41]/40 bg-[#00FF41]/5 p-4 text-center"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              style={{ boxShadow: '0 0 20px rgba(0,255,65,0.12)' }}
            >
              <motion.div
                className="text-[#00FF41] font-black text-sm tracking-[0.25em] mb-1"
                animate={{ opacity: [1, 0.5, 1] }}
                transition={{ duration: 1.2, repeat: Infinity }}
                style={{ textShadow: '0 0 12px #00FF41' }}
              >
                ✓ ENLACE AL 100%
              </motion.div>
              <p className="text-[10px] text-[#00FF41]/50 tracking-widest">
                Calibración completa. Acceso al Nexo concedido.
              </p>
            </motion.div>
          ) : (
            <motion.div
              key={tutorialStep}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 10 }}
              transition={{ duration: 0.22 }}
              className="space-y-3"
            >
              {/* Transmisión DAKI */}
              <div
                className="border border-cyan-500/30 bg-[#050f0f] p-3"
                style={{ boxShadow: 'inset 0 0 12px rgba(0,229,255,0.03)' }}
              >
                <div className="flex items-center gap-2 mb-2">
                  <motion.span
                    className="w-1 h-1 rounded-full bg-cyan-400 shrink-0"
                    animate={{ opacity: [0.35, 1, 0.35] }}
                    transition={{ duration: 1.1, repeat: Infinity }}
                  />
                  <span className="text-[8px] tracking-[0.4em] text-cyan-400/55 font-bold uppercase">
                    DAKI :: Transmisión
                  </span>
                </div>
                <p className="text-[10px] text-cyan-200/70 leading-relaxed">
                  {content.dakiLore}
                </p>
              </div>

              {/* Instrucción técnica */}
              <div className="border border-[#00FF41]/15 bg-black/30 px-3 py-2.5">
                <p className="text-[8px] tracking-[0.4em] text-[#00FF41]/35 mb-1.5 uppercase">
                  Acción Requerida
                </p>
                <p className="text-[11px] text-green-200/70 leading-relaxed">
                  {content.instruction}
                </p>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  )
}
