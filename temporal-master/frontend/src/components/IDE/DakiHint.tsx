'use client'

import { motion, AnimatePresence } from 'framer-motion'

// ─── Pistas por level_order ────────────────────────────────────────────────────
// Usamos level_order en lugar de UUID para no acoplar al ID de BD.

const HINTS: Record<number, { lore: string; tech: string }> = {
  1: {
    lore: 'Operador, en este entorno puedes usar el operador matemático de suma (+) para soldar ambas cadenas de texto. No olvides usar return para enviar la llave terminada.',
    tech: 'Usa el operador + para unir parte_izq y parte_der, y retorna el resultado. Sin int(), sin f-strings — solo concatenación directa.',
  },
  2: {
    lore: 'Los registros sinápticos llegan encriptados como texto, pero la Matriz los convierte a números en el canal de entrada.',
    tech: 'Solo necesitas el operador + y retornar el resultado. No hace falta int() ni conversión manual.',
  },
  3: {
    lore: 'Para atravesar el firewall neuronal, el flujo de datos debe leerse en orden inverso — así el Nexo no lo reconoce.',
    tech: 'Recuerda el Slicing de Python: cadena[::-1] invierte cualquier string en un solo paso.',
  },
  4: {
    lore: 'Los nodos de energía activos de la Matriz son vocales. Escanea el tejido de código carácter a carácter.',
    tech: 'Usa un for para recorrer la cadena y un if para comprobar si cada letra está en "aeiouAEIOU".',
  },
  5: {
    lore: 'La frecuencia fractal del Nexo sigue el patrón Fibonacci — dos nodos de estado que evolucionan en cada pulso sináptico.',
    tech: 'Empieza con a=0, b=1. En cada iteración: a, b = b, a+b. El valor a retornar es a.',
  },
}

const DEFAULT_HINT = {
  lore: 'Operador, analiza el enunciado de la misión con detenimiento.',
  tech: 'Revisa la sintaxis de tu función y asegúrate de que retornas el valor correcto.',
}

// ─── Props ────────────────────────────────────────────────────────────────────

interface Props {
  visible: boolean          // failStreak >= 2
  levelOrder: number | null | undefined
}

// ─── Componente ───────────────────────────────────────────────────────────────

export default function DakiHint({ visible, levelOrder }: Props) {
  const hint = (levelOrder && HINTS[levelOrder]) ?? DEFAULT_HINT

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
              className="flex items-center gap-2 px-3 py-1.5 border-b border-cyan-500/20"
              animate={{ opacity: [1, 0.45, 1] }}
              transition={{ duration: 2, repeat: Infinity, ease: 'easeInOut' }}
            >
              {/* Indicador de señal */}
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
            </motion.div>

            {/* Cuerpo del mensaje */}
            <div className="px-3 py-2.5 space-y-2">
              {/* Lore */}
              <p className="text-[10px] text-cyan-200/50 leading-relaxed italic">
                &ldquo;{hint.lore}&rdquo;
              </p>

              {/* Separador */}
              <div className="h-px bg-cyan-500/10" />

              {/* Pista técnica */}
              <div className="flex items-start gap-2">
                <span className="text-cyan-400/40 text-[9px] shrink-0 mt-0.5">▸</span>
                <p className="text-[10px] text-cyan-300/65 leading-relaxed">
                  {hint.tech}
                </p>
              </div>
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}
