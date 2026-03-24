'use client'

import { useRef, useState } from 'react'
import { useRouter } from 'next/navigation'
import { motion, AnimatePresence } from 'framer-motion'
import GridCanvas, { type CellType, type Coord, type EnemyEvent } from '@/components/Game/GridCanvas'
import GlitchTransition from '@/components/Game/GlitchTransition'
import MobileGate from '@/components/UI/MobileGate'

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000'

// ─── Backgrounds por mapa ─────────────────────────────────────────────────────
const MAP_BACKGROUNDS: Record<number, string> = {
  0: '/assets/backgrounds/map1.png', // Mapa 1 — cyan/blue   · Iniciación
  1: '/assets/backgrounds/map2.png', // Mapa 2 — yellow/orange · El Muro
  2: '/assets/backgrounds/map3.png', // Mapa 3 — electric purple · Condicionales
  3: '/assets/backgrounds/map4.png', // Mapa 4 — blood red    · El Enjambre
  4: '/assets/backgrounds/map5.png', // Mapa 5 — magenta/green · Asedio Total
}

// ─── Mapas ────────────────────────────────────────────────────────────────────

const MAPS: {
  label: string
  level: number
  grid: CellType[][]
  hint: string
}[] = [
  {
    label: 'Mapa 1 — Iniciante',
    level: 1,
    grid: [
      [3, 0, 0, 1, 0],
      [0, 1, 0, 1, 0],
      [0, 0, 0, 0, 0],
      [1, 0, 1, 1, 0],
      [0, 0, 0, 0, 2],
    ],
    hint: 'Navega al nucleo usando los comandos de movimiento.',
  },
  {
    label: 'Mapa 2 — Laberinto',
    level: 2,
    grid: [
      [3, 1, 0, 0, 0],
      [0, 1, 0, 1, 0],
      [0, 0, 0, 1, 0],
      [0, 1, 1, 1, 0],
      [0, 0, 0, 0, 2],
    ],
    hint: 'Encuentra el camino al nucleo esquivando los muros.',
  },
  {
    label: 'Mapa 3 — Zona Infectada',
    level: 3,
    grid: [
      [3, 0, 4, 0, 0],
      [0, 0, 0, 1, 0],
      [4, 0, 0, 0, 4],
      [0, 1, 0, 0, 0],
      [0, 0, 4, 0, 2],
    ],
    hint: 'Usa un bucle for para destruir los Syntax Swarm (rojo).',
  },
  {
    label: 'Mapa 4 — Bastion Blindado',
    level: 4,
    grid: [
      [3, 0, 5, 0, 0],
      [0, 1, 0, 0, 0],
      [0, 0, 5, 1, 0],
      [0, 0, 0, 0, 5],
      [0, 0, 0, 0, 2],
    ],
    hint: 'Los Logic Brute requieren if/else para romper su escudo.',
  },
  {
    label: 'Mapa 5 — Asedio Total',
    level: 5,
    grid: [
      [3, 4, 0, 5, 0],
      [0, 0, 1, 0, 0],
      [4, 0, 0, 0, 5],
      [0, 1, 4, 1, 0],
      [0, 0, 0, 5, 2],
    ],
    hint: 'Combina for e if/else para eliminar todos los enemigos.',
  },
]

// ─── Códigos de ejemplo por mapa ─────────────────────────────────────────────

const EXAMPLE_CODES: Record<number, string> = {
  0: `# Comandos del dron:
# mover_arriba()  mover_abajo()
# mover_izquierda()  mover_derecha()
# recolectar()

mover_abajo()
mover_abajo()
mover_derecha()
mover_derecha()
mover_derecha()
mover_derecha()
mover_abajo()
mover_abajo()
recolectar()`,
  1: `# Mapa 2: Laberinto denso
mover_abajo()
mover_abajo()
mover_abajo()
mover_abajo()
mover_derecha()
mover_derecha()
mover_derecha()
mover_derecha()
recolectar()`,
  2: `# Mapa 3: Zona Infectada
# usa for para atacar en area a los Syntax Swarm

for i in range(4):
    mover_derecha()

for i in range(4):
    mover_abajo()

recolectar()`,
  3: `# Mapa 4: Bastion Blindado
# usa if/else para el ataque de precision contra Logic Brute

posicion = 0
for i in range(4):
    mover_abajo()
    posicion += 1
    if posicion >= 2:
        mover_derecha()
    else:
        mover_abajo()

recolectar()`,
  4: `# Mapa 5: Asedio Total
# combina for + if/else

for i in range(4):
    mover_derecha()
    if i % 2 == 0:
        mover_abajo()
    else:
        mover_derecha()

recolectar()`,
}

// ─── Leyenda ─────────────────────────────────────────────────────────────────

const LEGEND = [
  { label: 'Inicio',           cls: 'border-[#00FF41]/40 bg-[#001A00]' },
  { label: 'Suelo',            cls: 'border-[#1A1A1A] bg-[#0D0D0D]' },
  { label: 'Muro',             cls: 'border-red-600/70 bg-[#1A0000]' },
  { label: 'Nucleo',           cls: 'border-blue-400 bg-[#000D1A]' },
  { label: 'Syntax Swarm',     cls: 'border-red-600 bg-[#1A0000]', badge: '01' },
  { label: 'Logic Brute',      cls: 'border-amber-500 bg-[#0A0A18]', badge: '🔒' },
]

// ─── Página ───────────────────────────────────────────────────────────────────

export default function EnigmaPage() {
  const router = useRouter()
  const [mapIdx, setMapIdx] = useState(0)
  const [code, setCode] = useState(EXAMPLE_CODES[0])
  const [activePath, setActivePath] = useState<Coord[] | undefined>(undefined)
  const [activeEnemyEvents, setActiveEnemyEvents] = useState<EnemyEvent[] | undefined>(undefined)
  const [log, setLog] = useState<string[]>(['> Sistema listo. Escribe comandos y presiona EJECUTAR.'])
  const [canvasKey, setCanvasKey] = useState(0)
  const [loading, setLoading] = useState(false)
  const [showAwakening, setShowAwakening] = useState(false)
  const [boardAnim, setBoardAnim] = useState<'anim-shake' | 'anim-victory-glow' | 'anim-error-flash' | ''>('')
  const logRef = useRef<HTMLDivElement>(null)

  const triggerBoardAnim = (cls: 'anim-shake' | 'anim-victory-glow' | 'anim-error-flash', ms = 500) => {
    setBoardAnim(cls)
    setTimeout(() => setBoardAnim(''), ms)
  }

  const addLog = (line: string) => {
    setLog((prev) => {
      const next = [...prev, line]
      setTimeout(() => logRef.current?.scrollTo(0, logRef.current.scrollHeight), 50)
      return next
    })
  }

  const handleReset = () => {
    setActivePath(undefined)
    setActiveEnemyEvents(undefined)
    setCanvasKey((k) => k + 1)
    setLog(['> Simulacion reiniciada.'])
  }

  const handleExecute = async () => {
    if (!code.trim() || loading) return
    setActivePath(undefined)
    setActiveEnemyEvents(undefined)
    setCanvasKey((k) => k + 1)
    setLog(['> Enviando codigo al simulador...'])
    setLoading(true)

    try {
      const res = await fetch(`${API_BASE}/api/v1/simulate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code, matrix: MAPS[mapIdx].grid }),
      })
      const data = await res.json()

      if (!res.ok) {
        addLog(`[ERROR] ${data.detail ?? res.statusText}`)
        return
      }

      addLog(`> Ruta calculada: ${data.steps} paso${data.steps !== 1 ? 's' : ''} · ${data.execution_time_ms}ms`)
      if (data.error) addLog(`> Advertencia: ${data.error}`)

      const enemyEvts: EnemyEvent[] = data.enemy_events ?? []
      if (enemyEvts.length > 0) {
        const swarmKills  = enemyEvts.filter((e: EnemyEvent) => e.enemy_type === 4).length
        const bruteKills  = enemyEvts.filter((e: EnemyEvent) => e.enemy_type === 5).length
        if (swarmKills) addLog(`> ATAQUE AOE — ${swarmKills} Syntax Swarm eliminado${swarmKills > 1 ? 's' : ''}.`)
        if (bruteKills) addLog(`> PRECISION — ${bruteKills} Logic Brute destruido${bruteKills > 1 ? 's' : ''}.`)
      }

      setTimeout(() => {
        setActivePath(data.path as Coord[])
        setActiveEnemyEvents(enemyEvts)
      }, 100)
    } catch (e) {
      addLog(`[RED] ${String(e)}`)
    } finally {
      setLoading(false)
    }
  }

  const handleMissionComplete = () => {
    addLog('> Nucleo de datos alcanzado.')
    triggerBoardAnim('anim-victory-glow', 1400)
    if (MAPS[mapIdx].level === 5) {
      setTimeout(() => setShowAwakening(true), 1200)
    } else {
      addLog('> MISION COMPLETA.')
    }
  }

  const currentMap = MAPS[mapIdx]

  return (
    <MobileGate>
    <>
      <AnimatePresence>
        {showAwakening && (
          <GlitchTransition
            onComplete={() => {
              setShowAwakening(false)
              router.push('/misiones')
            }}
          />
        )}
      </AnimatePresence>

      <div
        className="relative min-h-screen bg-[#0A0A0A] bg-cover bg-center font-mono text-[#00FF41] transition-all duration-700"
        style={{ backgroundImage: `url('${MAP_BACKGROUNDS[mapIdx]}'), none` }}
      >
        {/* Overlay: oscurece 80% + blur sutil para no competir con el editor */}
        <div className="absolute inset-0 bg-black/80 backdrop-blur-sm z-0 pointer-events-none" />

        {/* Todo el contenido sobre el overlay */}
        <div className="relative z-10 flex flex-col min-h-screen">

        {/* Cabecera */}
        <header className="flex items-center justify-between px-6 py-3 bg-[#0D0D0D] border-b border-[#00FF41]/20">
          <div className="flex items-center gap-3">
            <button onClick={() => router.push('/misiones')}
              className="text-[#00FF41]/40 hover:text-[#00FF41] transition-colors tracking-widest text-xs">
              MISIONES
            </button>
            <span className="text-[#00FF41]/20">|</span>
            <span className="font-black tracking-widest text-sm"
              style={{ textShadow: '0 0 8px #00FF41' }}>
              PROYECTO ENIGMA
            </span>
          </div>
          <span className="text-[#00FF41]/30 text-xs tracking-widest">FASE 0 // PRE-PYTHON</span>
        </header>

        {/* Selector de mapa — barra superior completa */}
        <div className="flex flex-wrap gap-2 px-6 pt-6 max-w-6xl mx-auto">
          {MAPS.map((m, i) => (
            <button key={i}
              onClick={() => {
                setMapIdx(i)
                setCode(EXAMPLE_CODES[i])
                handleReset()
                setLog([`> Mapa "${m.label}" cargado.`])
              }}
              className={`px-3 py-1.5 text-xs tracking-widest border transition-all ${
                mapIdx === i
                  ? 'border-[#00FF41] bg-[#00FF41]/10 text-[#00FF41]'
                  : 'border-[#00FF41]/20 text-[#00FF41]/40 hover:border-[#00FF41]/50'
              }`}>
              {m.label}
              {m.level === 5 && (
                <span className="ml-2 text-red-400/60 text-xs">{'// FINAL'}</span>
              )}
            </button>
          ))}
        </div>

        <main className="flex flex-col lg:flex-row gap-8 px-6 py-6 max-w-6xl mx-auto">

          {/* Panel izquierdo: grid (ancho fijo = tamaño del grid) */}
          <div className="flex flex-col gap-4 shrink-0 w-[332px]">

            {/* Hint del mapa */}
            <div className="text-[10px] text-[#00FF41]/30 tracking-widest border-l border-[#00FF41]/20 pl-2">
              {currentMap.hint}
            </div>

            <div className={`border border-[#00FF41]/20 transition-all duration-300 ${boardAnim}`}>
              <GridCanvas
                key={canvasKey}
                matrix={currentMap.grid}
                path={activePath}
                enemyEvents={activeEnemyEvents}
                cellSize={64}
                stepDelay={350}
                onComplete={handleMissionComplete}
                onCollision={(c) => {
                  addLog(`> COLISION en (${c.x}, ${c.y}) — ruta bloqueada.`)
                  triggerBoardAnim('anim-shake', 500)
                }}
              />
            </div>

            {/* Leyenda */}
            <div className="flex flex-wrap gap-3">
              {LEGEND.map(({ label, cls, badge }) => (
                <div key={label} className="flex items-center gap-1.5 text-xs text-[#00FF41]/45">
                  <div className={`w-4 h-4 border ${cls} flex items-center justify-center`}>
                    {badge && (
                      <span className="text-[6px] leading-none text-red-400 font-mono">{badge}</span>
                    )}
                  </div>
                  {label}
                </div>
              ))}
            </div>
          </div>

          {/* Panel derecho: editor + consola */}
          <div className="flex-1 flex flex-col gap-4 min-w-0">
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-[#00FF41]/40 text-xs tracking-widest uppercase">
                  Codigo del dron
                </span>
                <span className="text-[#00FF41]/20 text-xs">
                  mover_* · recolectar · for · if/else
                </span>
              </div>
              <textarea
                value={code}
                onChange={(e) => setCode(e.target.value)}
                spellCheck={false}
                className="w-full h-56 bg-[#0D0D0D] border border-[#00FF41]/20 text-[#00FF41]/85 text-xs
                           leading-5 p-3 resize-none focus:outline-none focus:border-[#00FF41]/50 font-mono"
                placeholder="# Escribe los comandos del dron aqui..."
              />
            </div>

            <div className="flex gap-2">
              <motion.button whileTap={{ scale: 0.97 }} onClick={handleExecute} disabled={loading}
                className="flex-1 py-2.5 bg-[#00FF41] text-black text-xs font-black tracking-widest
                           hover:bg-[#00FF41]/85 disabled:opacity-40 disabled:cursor-not-allowed transition-colors">
                {loading ? 'SIMULANDO...' : 'EJECUTAR'}
              </motion.button>
              <motion.button whileTap={{ scale: 0.97 }} onClick={handleReset}
                className="px-5 py-2.5 border border-[#00FF41]/20 text-[#00FF41]/40 text-xs tracking-widest
                           hover:border-[#00FF41]/40 hover:text-[#00FF41]/60 transition-colors">
                REINICIAR
              </motion.button>
            </div>

            <div ref={logRef}
              className="bg-[#0D0D0D] border border-[#00FF41]/15 p-3 h-44 overflow-y-auto space-y-0.5">
              {log.map((line, i) => (
                <motion.div key={i}
                  initial={{ opacity: 0, x: -6 }} animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.15 }}
                  className={`text-xs leading-5 ${
                    line.includes('COLISION') || line.includes('[ERROR]') || line.includes('[RED]')
                      ? 'text-red-400'
                      : line.includes('COMPLETA') || line.includes('alcanzado') || line.includes('eliminado') || line.includes('destruido')
                      ? 'text-[#00FF41]'
                      : line.includes('ATAQUE') || line.includes('PRECISION')
                      ? 'text-amber-400'
                      : 'text-[#00FF41]/50'
                  }`}>
                  {line}
                </motion.div>
              ))}
            </div>

            {/* Referencia de mecánicas */}
            <div className="border border-[#00FF41]/10 p-4 text-xs text-[#00FF41]/30 leading-6">
              <div className="text-[#00FF41]/50 mb-2 tracking-widest">API DEL DRON</div>
              <div>
                <span className="text-[#00FF41]/60">mover_arriba()</span> /&nbsp;
                <span className="text-[#00FF41]/60">mover_abajo()</span> /&nbsp;
                <span className="text-[#00FF41]/60">mover_izquierda()</span> /&nbsp;
                <span className="text-[#00FF41]/60">mover_derecha()</span>
              </div>
              <div><span className="text-[#00FF41]/60">recolectar()</span> — recoge el nucleo en la posicion actual</div>
              <div className="mt-2 text-[#00FF41]/50 tracking-widest">COMBATE</div>
              <div>
                <span className="text-red-400/70">for</span> → Ataque de Area (AoE) — destruye{' '}
                <span className="text-red-400/70">Syntax Swarm</span> adyacentes
              </div>
              <div>
                <span className="text-amber-400/70">if/else</span> → Precision — rompe el escudo del{' '}
                <span className="text-amber-400/70">Logic Brute</span>
              </div>
              <div className="mt-1.5 text-[#00FF41]/20">Limite: 200 pasos · Timeout: 3s · Sin imports</div>
            </div>
          </div>
        </main>
        </div> {/* end z-10 content wrapper */}
      </div>
    </>
    </MobileGate>
  )
}
