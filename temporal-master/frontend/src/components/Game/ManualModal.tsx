'use client'

import { useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

// ─── Bloque de código ──────────────────────────────────────────────────────────

function CodeBlock({ code }: { code: string }) {
  return (
    <div className="bg-gray-900 border border-cyan-500/20 rounded-sm overflow-hidden">
      <div className="flex items-center gap-1.5 px-3 py-1.5 border-b border-cyan-500/10 bg-black/40">
        <span className="w-2 h-2 rounded-full bg-red-500/50" />
        <span className="w-2 h-2 rounded-full bg-yellow-500/50" />
        <span className="w-2 h-2 rounded-full bg-green-500/50" />
        <span className="ml-2 text-[8px] tracking-[0.4em] text-cyan-500/30 font-mono">TERMINAL // DAKI EdTech</span>
      </div>
      <pre className="px-4 py-3 text-[12px] font-mono text-cyan-300/85 leading-relaxed overflow-x-auto whitespace-pre">
        {code}
      </pre>
    </div>
  )
}

// ─── Sección del manual ────────────────────────────────────────────────────────

interface Section {
  index: string
  tag: string
  title: string
  lore: string
  syntax?: string
  code?: string
  tactic: string
}

const SECTIONS: Section[] = [
  {
    index: '01',
    tag: 'CLASIFICACIÓN: BÁSICO',
    title: 'NODOS DE MEMORIA',
    syntax: 'Variables',
    lore: 'Antes de mover el dron, necesitamos almacenar las coordenadas y contraseñas. Sin variables, el sistema opera a ciegas y las misiones críticas fallan en el primer segundo.',
    code: '# Almacenar datos vitales de la misión\nnombre_clave = "Operación Sombra"\ncoordenadas = [51, 7]\nescudos_activos = True\n\nprint(nombre_clave)  # Operación Sombra',
    tactic: 'Usa el signo = para asignar datos vitales a una variable. El nombre va a la izquierda, el valor a la derecha.',
  },
  {
    index: '02',
    tag: 'CLASIFICACIÓN: OFENSIVO',
    title: 'PROTOCOLOS DE RÁFAGA',
    syntax: 'Bucles FOR',
    lore: 'Los enjambres enemigos ("Syntax Swarms") requieren daño de área. No envíes comandos uno por uno; automatiza el asalto. Un solo FOR puede limpiar un sector entero.',
    code: 'for i in range(3):\n    mover_derecha()  # Se ejecuta 3 veces\n\n# Atacar a cada objetivo del enjambre\nobjetivos = ["swarm_A", "swarm_B", "swarm_C"]\nfor objetivo in objetivos:\n    atacar(objetivo)',
    tactic: 'El bloque indentado debajo del for es el área de efecto. Todo lo que esté dentro se repite para cada elemento.',
  },
  {
    index: '03',
    tag: 'CLASIFICACIÓN: DEFENSIVO',
    title: 'SENSORES DE DECISIÓN',
    syntax: 'Condicionales IF / ELSE',
    lore: 'Para romper los escudos de los "Logic Brutes" (Candados Amarillos), el dron debe tomar decisiones en microsegundos. Un sensor mal calibrado = misión comprometida.',
    code: 'if enemigo_detectado:\n    atacar()\nelse:\n    avanzar()\n\n# Sensor múltiple\nif escudo == "amarillo":\n    usar_clave()\nelif escudo == "rojo":\n    llamar_soporte()\nelse:\n    forzar_entrada()',
    tactic: 'El código evalúa la situación. Solo una ruta se ejecutará. El else es el fallback cuando ninguna condición se cumple.',
  },
]

// ─── Props ─────────────────────────────────────────────────────────────────────

interface ManualModalProps {
  isOpen: boolean
  onClose: () => void
}

// ─── Componente ────────────────────────────────────────────────────────────────

export default function ManualModal({ isOpen, onClose }: ManualModalProps) {
  // Cierre con Escape
  useEffect(() => {
    if (!isOpen) return
    const handler = (e: KeyboardEvent) => { if (e.key === 'Escape') onClose() }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [isOpen, onClose])

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          className="fixed inset-0 z-50 flex items-center justify-center p-4"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.2 }}
        >
          {/* Backdrop semitransparente con blur */}
          <motion.div
            className="absolute inset-0 bg-black/80 backdrop-blur-md"
            onClick={onClose}
          />

          {/* Panel principal */}
          <motion.div
            className="relative z-10 w-full max-w-2xl max-h-[88vh] flex flex-col font-mono"
            style={{
              background: 'linear-gradient(180deg, #040a08 0%, #020606 100%)',
              border: '1px solid rgba(0,255,65,0.25)',
              boxShadow: '0 0 60px rgba(0,255,65,0.06), inset 0 0 40px rgba(0,0,0,0.5)',
            }}
            initial={{ scale: 0.9, y: 28, opacity: 0 }}
            animate={{ scale: 1, y: 0, opacity: 1 }}
            exit={{ scale: 0.9, y: 28, opacity: 0 }}
            transition={{ duration: 0.25, ease: [0.16, 1, 0.3, 1] }}
          >
            {/* Esquinas decorativas */}
            <span className="absolute top-0 left-0 w-5 h-5 border-t-2 border-l-2 border-[#00FF41]/60" />
            <span className="absolute top-0 right-0 w-5 h-5 border-t-2 border-r-2 border-[#00FF41]/60" />
            <span className="absolute bottom-0 left-0 w-5 h-5 border-b-2 border-l-2 border-[#00FF41]/60" />
            <span className="absolute bottom-0 right-0 w-5 h-5 border-b-2 border-r-2 border-[#00FF41]/60" />

            {/* ── Header fijo ── */}
            <div className="shrink-0 px-7 pt-6 pb-4 border-b border-[#00FF41]/10">

              {/* Sello clasificado */}
              <div className="flex items-center justify-center gap-3 mb-4 py-2 border border-[#00FF41]/15 bg-[#00FF41]/3">
                <span className="text-[#00FF41]/50 text-sm">▓</span>
                <span className="text-[10px] tracking-[0.6em] text-[#00FF41]/50 font-bold">
                  DOCUMENTO CLASIFICADO // NIVEL MÁXIMO
                </span>
                <span className="text-[#00FF41]/50 text-sm">▓</span>
              </div>

              {/* Título */}
              <h2
                className="text-lg font-black tracking-[0.15em] text-[#00FF41] mb-1"
                style={{ textShadow: '0 0 12px #00FF4160' }}
              >
                ARCHIVOS DE INFILTRACIÓN: SINTAXIS BÁSICA
              </h2>
              <div className="flex items-center justify-between">
                <p className="text-[9px] tracking-[0.4em] text-[#00FF41]/30">
                  MANUAL TÁCTICO // OPERADOR AUTORIZADO // DAKI EdTech
                </p>
                <button
                  onClick={onClose}
                  className="text-[10px] tracking-widest text-[#00FF41]/30 hover:text-[#00FF41]/70 transition-colors border border-[#00FF41]/15 px-2 py-0.5 hover:border-[#00FF41]/35"
                >
                  [ ESC ]
                </button>
              </div>
            </div>

            {/* ── Cuerpo scrollable ── */}
            <div className="flex-1 overflow-y-auto px-7 py-6 flex flex-col gap-7">

              {SECTIONS.map((s, idx) => (
                <motion.div
                  key={s.index}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: idx * 0.08, duration: 0.3 }}
                >
                  {/* Cabecera de sección */}
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-3">
                      <span
                        className="text-2xl font-black tabular-nums"
                        style={{ color: '#00FF41', textShadow: '0 0 10px #00FF4180', opacity: 0.35 }}
                      >
                        {s.index}
                      </span>
                      <div>
                        <p className="text-[8px] tracking-[0.5em] text-[#00FF41]/30 mb-0.5">{s.tag}</p>
                        <h3 className="text-sm font-black tracking-wider text-[#00FF41]/90">
                          {s.title}
                        </h3>
                      </div>
                    </div>
                    {s.syntax && (
                      <span className="text-[9px] tracking-widest text-cyan-400/50 border border-cyan-400/20 px-2 py-0.5">
                        {s.syntax}
                      </span>
                    )}
                  </div>

                  {/* Lore */}
                  <div className="border-l-2 border-[#00FF41]/20 pl-4 mb-3">
                    <p className="text-[11px] text-white/45 leading-relaxed italic">
                      {s.lore}
                    </p>
                  </div>

                  {/* Código */}
                  {s.code && <CodeBlock code={s.code} />}

                  {/* Táctica */}
                  <div className="mt-3 flex items-start gap-2 border border-cyan-500/15 bg-cyan-950/10 px-4 py-2.5">
                    <span className="text-cyan-400/60 text-sm shrink-0 mt-0.5">◆</span>
                    <p className="text-[10px] text-cyan-400/55 leading-relaxed">
                      <span className="text-cyan-400/80 font-bold tracking-wider">TÁCTICA: </span>
                      {s.tactic}
                    </p>
                  </div>

                  {/* Separador entre secciones */}
                  {idx < SECTIONS.length - 1 && (
                    <div className="mt-7 h-px bg-gradient-to-r from-transparent via-[#00FF41]/15 to-transparent" />
                  )}
                </motion.div>
              ))}

              {/* Footer */}
              <div className="pt-2 pb-1 border-t border-[#00FF41]/8 text-center">
                <p className="text-[8px] tracking-[0.5em] text-[#00FF41]/15">
                  FIN DEL ARCHIVO // DESTRUIR DESPUÉS DE MEMORIZAR // DAKI EdTech
                </p>
              </div>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}
