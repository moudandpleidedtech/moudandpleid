'use client'

import { useEffect, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

// ─── Contenido de los 5 archivos ───────────────────────────────────────────────

interface Archivo {
  id: string
  order: number          // coincide con level_order de la misión
  label: string
  title: string
  subtitle: string
  missionName: string
  dakiReport: string
  code: string
  codeCaption: string
}

const ARCHIVOS: Archivo[] = [
  {
    id: 'arch-01',
    order: 1,
    label: 'ARCHIVO 01',
    title: 'Nodos de Memoria y Ecos',
    subtitle: 'Variables y Print',
    missionName: 'Misión 1 — Eco del Sistema',
    dakiReport:
      'Operador, lograste engañar al radar. Para hacerlo, usaste Variables — contenedores ' +
      'que guardan información valiosa en la memoria RAM del dron — y la función Print, ' +
      'que emite esa información hacia los canales de salida. ' +
      'Acabas de dominar la entrada y salida de datos. El Área 51 no sabe que ya estás dentro.',
    code:
      '# Asignar datos vitales de la misión\nnombre = "Dron"\ncoordenadas = [51, 7]\n\n# Emitir señal de ping\nprint(nombre)\nprint(f"Sector: {coordenadas}")',
    codeCaption: 'Variables + Print',
  },
  {
    id: 'arch-02',
    order: 2,
    label: 'ARCHIVO 02',
    title: 'Operadores Aritméticos Base',
    subtitle: 'Matemáticas en el campo',
    missionName: 'Misión 2 — Calculadora Binaria',
    dakiReport:
      'La suma de los registros fue un éxito. En Python, los procesadores nativos nos permiten ' +
      'usar +, -, * y / para manipular datos numéricos y descifrar coordenadas enemigas. ' +
      'Los operadores son las instrucciones más primitivas del sistema — y las más potentes ' +
      'cuando se combinan con variables. Las cámaras del sector han sido burladas.',
    code:
      '# Descifrar coordenadas sumando registros\nreg_a = 128\nreg_b = 64\nreg_c = 32\n\ncoord_x = reg_a + reg_b\ncoord_y = reg_a - reg_c\nescala  = reg_b * 2\nfrecuencia = reg_a / reg_c\n\nprint(f"X:{coord_x} Y:{coord_y} F:{frecuencia}")',
    codeCaption: 'Operadores: + - * /',
  },
  {
    id: 'arch-03',
    order: 3,
    label: 'ARCHIVO 03',
    title: 'Inversión de Flujos de Datos',
    subtitle: 'Slicing de Strings',
    missionName: 'Misión 3 — Inversor de Cadenas',
    dakiReport:
      'El firewall ha caído. El slicing es la técnica que permite manipular cadenas de texto ' +
      'como si fueran secuencias de bytes: puedes extraer fragmentos, invertir flujos y ' +
      'reordenar señales encriptadas. En Python, los strings son indexables — cada carácter ' +
      'tiene una posición y puede ser aislado o invertido a voluntad.',
    code:
      '# Señal enemiga encriptada\nsenal = "51AERA_OTCELES"\n\n# Invertir el flujo de datos\nsenal_invertida = senal[::-1]\nprint(senal_invertida)  # SELECTO_AREA15\n\n# Extraer fragmento específico\nsector = senal[2:6]\nprint(sector)  # AREA',
    codeCaption: 'Slicing: [inicio:fin:paso]',
  },
  {
    id: 'arch-04',
    order: 4,
    label: 'ARCHIVO 04',
    title: 'Protocolos de Escaneo Iterativo',
    subtitle: 'For Loops + Condicionales IF',
    missionName: 'Misión 4 — Contador de Vocales',
    dakiReport:
      'Los nodos de energía fueron identificados. El bucle FOR combinado con IF es el arma ' +
      'de exploración del dron: itera sobre cada elemento de una secuencia y decide en tiempo ' +
      'real qué acción tomar. Sin este protocolo, el dron no puede escanear el código fuente ' +
      'enemigo ni detectar los nodos activos. Es la base de toda IA de combate.',
    code:
      '# Escanear código enemigo buscando nodos (vocales)\ncodigo = "infiltracion"\nnodos_activos = 0\n\nfor caracter in codigo:\n    if caracter in "aeiouAEIOU":\n        nodos_activos += 1\n        print(f"Nodo detectado: {caracter}")\n\nprint(f"Total nodos: {nodos_activos}")',
    codeCaption: 'for … in + if … in',
  },
  {
    id: 'arch-05',
    order: 5,
    label: 'ARCHIVO 05',
    title: 'Frecuencia Fractal de Fibonacci',
    subtitle: 'Lógica Avanzada e Iteración',
    missionName: 'Misión 5 — Secuencia de Fibonacci',
    dakiReport:
      'La sincronía fractal fue lograda. La secuencia de Fibonacci demuestra que los algoritmos ' +
      'pueden modelar patrones que existen en la naturaleza misma. El motor de salto del dron ' +
      'opera en frecuencias no lineales — solo Fibonacci puede predecirlas. ' +
      'Has alcanzado el nivel de lógica algorítmica que el Área 51 creía imposible para un humano.',
    code:
      '# Generar frecuencia fractal de Fibonacci\ndef fibonacci(n):\n    a, b = 0, 1\n    secuencia = []\n    for _ in range(n):\n        secuencia.append(a)\n        a, b = b, a + b\n    return secuencia\n\nfrecuencias = fibonacci(8)\nprint(frecuencias)\n# [0, 1, 1, 2, 3, 5, 8, 13]',
    codeCaption: 'Funciones + iteración avanzada',
  },
]

const LS_KEY = 'pq-bitacora-read'

function getReadIds(): string[] {
  if (typeof window === 'undefined') return []
  try { return JSON.parse(localStorage.getItem(LS_KEY) ?? '[]') } catch { return [] }
}
function markRead(id: string) {
  const current = getReadIds()
  if (!current.includes(id)) localStorage.setItem(LS_KEY, JSON.stringify([...current, id]))
}

// ─── Bloque de código ──────────────────────────────────────────────────────────

function CodeBlock({ code, caption }: { code: string; caption: string }) {
  return (
    <div className="bg-black border border-[#00FF41]/15 overflow-hidden">
      <div className="flex items-center gap-2 px-3 py-1.5 border-b border-[#00FF41]/10 bg-[#00FF41]/3">
        <span className="w-1.5 h-1.5 rounded-full bg-[#00FF41]/60" />
        <span className="text-[8px] tracking-[0.4em] text-[#00FF41]/30 font-mono">SINTAXIS RECUPERADA // {caption.toUpperCase()}</span>
      </div>
      <pre className="px-4 py-3 text-[11px] font-mono text-[#00FF41]/80 leading-relaxed overflow-x-auto whitespace-pre">
        {code}
      </pre>
    </div>
  )
}

// ─── Props ─────────────────────────────────────────────────────────────────────

interface BitacoraModalProps {
  isOpen: boolean
  onClose: () => void
  completedOrders: number[]   // level_orders de misiones completadas
}

// ─── Componente ────────────────────────────────────────────────────────────────

export default function BitacoraModal({ isOpen, onClose, completedOrders }: BitacoraModalProps) {
  const [selected, setSelected] = useState<Archivo>(ARCHIVOS[0])
  const [readIds, setReadIds] = useState<string[]>([])

  // Cargar leídos del localStorage al abrir
  useEffect(() => { if (isOpen) setReadIds(getReadIds()) }, [isOpen])

  // Marcar como leído al seleccionar (solo si está desbloqueado)
  useEffect(() => {
    if (!isOpen) return
    const unlocked = completedOrders.includes(selected.order)
    if (unlocked && !readIds.includes(selected.id)) {
      markRead(selected.id)
      setReadIds(getReadIds())
    }
  }, [selected, isOpen, completedOrders, readIds])

  // Cerrar con Escape
  useEffect(() => {
    if (!isOpen) return
    const h = (e: KeyboardEvent) => { if (e.key === 'Escape') onClose() }
    window.addEventListener('keydown', h)
    return () => window.removeEventListener('keydown', h)
  }, [isOpen, onClose])

  // Auto-seleccionar primer archivo desbloqueado al abrir
  useEffect(() => {
    if (!isOpen) return
    const first = ARCHIVOS.find(a => completedOrders.includes(a.order)) ?? ARCHIVOS[0]
    setSelected(first)
  }, [isOpen, completedOrders])

  const isUnlocked = (a: Archivo) => completedOrders.includes(a.order)
  const isNew = (a: Archivo) => isUnlocked(a) && !readIds.includes(a.id)

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          className="fixed inset-0 z-50 flex items-center justify-center p-4"
          initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
          transition={{ duration: 0.18 }}
        >
          {/* Backdrop */}
          <motion.div className="absolute inset-0 bg-black/88 backdrop-blur-md" onClick={onClose} />

          {/* Panel principal */}
          <motion.div
            className="relative z-10 w-full max-w-4xl h-[82vh] flex border font-mono overflow-hidden"
            style={{ borderColor: 'rgba(0,255,65,0.25)', background: 'linear-gradient(135deg,#030a05 0%,#020604 100%)' }}
            initial={{ scale: 0.92, y: 24 }} animate={{ scale: 1, y: 0 }}
            exit={{ scale: 0.92, y: 24 }} transition={{ duration: 0.22, ease: [0.16,1,0.3,1] }}
          >
            {/* Esquinas */}
            <span className="absolute top-0 left-0 w-5 h-5 border-t-2 border-l-2 border-[#00FF41]/60 z-10" />
            <span className="absolute top-0 right-0 w-5 h-5 border-t-2 border-r-2 border-[#00FF41]/60 z-10" />
            <span className="absolute bottom-0 left-0 w-5 h-5 border-b-2 border-l-2 border-[#00FF41]/60 z-10" />
            <span className="absolute bottom-0 right-0 w-5 h-5 border-b-2 border-r-2 border-[#00FF41]/60 z-10" />

            {/* ── Columna izquierda — Lista de archivos ── */}
            <div className="w-56 shrink-0 flex flex-col border-r border-[#00FF41]/12 overflow-hidden">

              {/* Header lista */}
              <div className="px-4 py-4 border-b border-[#00FF41]/10 shrink-0">
                <p className="text-[8px] tracking-[0.6em] text-[#00FF41]/40 mb-0.5">CÓDICE DE INFILTRACIÓN</p>
                <p className="text-[7px] tracking-wider text-[#00FF41]/20">
                  {completedOrders.length}/{ARCHIVOS.length} ARCHIVOS DESBLOQUEADOS
                </p>
                {/* Mini barra de progreso */}
                <div className="mt-2 h-px bg-[#00FF41]/10 relative overflow-hidden">
                  <motion.div
                    className="absolute left-0 top-0 h-full bg-[#00FF41]"
                    initial={{ width: 0 }}
                    animate={{ width: `${(completedOrders.length / ARCHIVOS.length) * 100}%` }}
                    transition={{ duration: 0.8, ease: 'easeOut' }}
                  />
                </div>
              </div>

              {/* Lista */}
              <div className="flex-1 overflow-y-auto py-1">
                {ARCHIVOS.map((a, idx) => {
                  const unlocked = isUnlocked(a)
                  const isSelected = selected.id === a.id
                  const hasNew = isNew(a)
                  return (
                    <motion.button
                      key={a.id}
                      initial={{ opacity: 0, x: -8 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: idx * 0.05 }}
                      onClick={() => { if (unlocked) setSelected(a) }}
                      disabled={!unlocked}
                      className="w-full text-left px-4 py-3 border-b border-[#00FF41]/6 transition-all duration-150 relative"
                      style={isSelected && unlocked ? {
                        background: 'rgba(0,255,65,0.07)',
                        borderLeft: '2px solid rgba(0,255,65,0.6)',
                      } : !unlocked ? {
                        opacity: 0.45,
                        cursor: 'not-allowed',
                      } : {}}
                      onMouseEnter={e => { if (unlocked && !isSelected) e.currentTarget.style.background = 'rgba(0,255,65,0.04)' }}
                      onMouseLeave={e => { if (!isSelected) e.currentTarget.style.background = 'transparent' }}
                    >
                      <div className="flex items-start gap-2.5">
                        {/* Icono estado */}
                        <span className={`text-sm mt-0.5 shrink-0 ${unlocked ? 'text-[#00FF41]/60' : 'text-[#00FF41]/20'}`}>
                          {unlocked ? '◈' : '🔒'}
                        </span>
                        <div className="flex flex-col gap-0.5 min-w-0 flex-1">
                          <div className="flex items-center gap-1.5">
                            <span className={`text-[9px] font-bold tracking-wider truncate ${
                              isSelected ? 'text-[#00FF41]' : unlocked ? 'text-[#00FF41]/65' : 'text-[#00FF41]/25'
                            }`}>
                              {a.label}
                            </span>
                            {/* Indicador NEW */}
                            {hasNew && (
                              <motion.span
                                className="w-1.5 h-1.5 rounded-full bg-[#00FF41] shrink-0"
                                animate={{ opacity: [1, 0.2, 1] }}
                                transition={{ duration: 0.8, repeat: Infinity }}
                              />
                            )}
                          </div>
                          {unlocked ? (
                            <span className="text-[8px] text-[#00FF41]/35 truncate">{a.subtitle}</span>
                          ) : (
                            <span className="text-[7px] text-[#00FF41]/18 leading-snug">
                              [ DATOS ENCRIPTADOS ]
                              <br />Requiere {a.missionName.split('—')[0].trim()}
                            </span>
                          )}
                        </div>
                      </div>
                    </motion.button>
                  )
                })}
              </div>
            </div>

            {/* ── Columna derecha — Contenido del archivo ── */}
            <div className="flex-1 flex flex-col overflow-hidden">

              {/* Header del panel derecho */}
              <div className="shrink-0 flex items-center justify-between px-6 py-4 border-b border-[#00FF41]/10">
                <div>
                  <p className="text-[8px] tracking-[0.5em] text-[#00FF41]/30 mb-0.5">
                    {selected.label} // {selected.missionName.toUpperCase()}
                  </p>
                  <h2 className="text-sm font-black tracking-wider text-[#00FF41]"
                    style={{ textShadow: '0 0 10px rgba(0,255,65,0.4)' }}>
                    {selected.title.toUpperCase()}
                  </h2>
                </div>
                <button
                  onClick={onClose}
                  className="text-[9px] tracking-widest text-[#00FF41]/30 hover:text-[#00FF41]/70 transition-colors border border-[#00FF41]/15 px-2.5 py-1 hover:border-[#00FF41]/35"
                >
                  [ ESC ]
                </button>
              </div>

              {/* Cuerpo scrollable */}
              <AnimatePresence mode="wait">
                {isUnlocked(selected) ? (
                  <motion.div
                    key={selected.id}
                    className="flex-1 overflow-y-auto px-6 py-6 flex flex-col gap-6"
                    initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -6 }} transition={{ duration: 0.2 }}
                  >
                    {/* Reporte de DAKI */}
                    <div>
                      <div className="flex items-center gap-2 mb-3">
                        <motion.span
                          className="w-1.5 h-1.5 rounded-full bg-[#00FF41]"
                          animate={{ opacity: [1, 0.2, 1] }}
                          transition={{ duration: 1.2, repeat: Infinity }}
                        />
                        <span className="text-[9px] tracking-[0.5em] text-[#00FF41]/40">
                          REPORTE DE DAKI // ANÁLISIS POST-MISIÓN
                        </span>
                      </div>
                      <div className="border-l-2 border-[#00FF41]/25 pl-4">
                        <p className="text-[12px] text-white/55 leading-relaxed italic">
                          "{selected.dakiReport}"
                        </p>
                      </div>
                    </div>

                    {/* Separador */}
                    <div className="h-px bg-gradient-to-r from-[#00FF41]/20 via-[#00FF41]/8 to-transparent" />

                    {/* Código */}
                    <div>
                      <p className="text-[9px] tracking-[0.5em] text-[#00FF41]/30 mb-3">
                        ◆ SINTAXIS RECUPERADA DEL CAMPO
                      </p>
                      <CodeBlock code={selected.code} caption={selected.codeCaption} />
                    </div>

                    {/* Footer del archivo */}
                    <div className="mt-auto pt-4 border-t border-[#00FF41]/8 flex items-center justify-between">
                      <span className="text-[7px] tracking-[0.5em] text-[#00FF41]/15">
                        ARCHIVO DESBLOQUEADO // CONOCIMIENTO INTEGRADO
                      </span>
                      <span className="text-[7px] tracking-[0.4em] text-[#00FF41]/12">
                        ENIGMA CORP
                      </span>
                    </div>
                  </motion.div>
                ) : (
                  <motion.div
                    key="locked"
                    className="flex-1 flex flex-col items-center justify-center gap-4 px-8"
                    initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                  >
                    <motion.div
                      className="text-4xl"
                      animate={{ opacity: [0.3, 0.7, 0.3] }}
                      transition={{ duration: 2, repeat: Infinity }}
                    >
                      🔒
                    </motion.div>
                    <div className="text-center">
                      <p className="text-[11px] font-bold tracking-[0.3em] text-[#00FF41]/30 mb-2">
                        DATOS ENCRIPTADOS
                      </p>
                      <p className="text-[10px] text-[#00FF41]/18 tracking-wider">
                        Completa {selected.missionName} para desbloquear este archivo
                      </p>
                    </div>
                    <div className="border border-[#00FF41]/10 px-6 py-3 text-center max-w-xs">
                      <p className="text-[9px] tracking-widest text-[#00FF41]/20">
                        DAKI: "Aún no tienes autorización para acceder a este nivel de inteligencia. Completa la misión primero."
                      </p>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}

// ─── Export helper para calcular archivos nuevos ───────────────────────────────

export function countNewArchives(completedOrders: number[]): number {
  const readIds = getReadIds()
  return ARCHIVOS.filter(a => completedOrders.includes(a.order) && !readIds.includes(a.id)).length
}
