'use client'

import { useEffect, useRef, useState, useCallback } from 'react'
import { motion, useAnimation } from 'framer-motion'
import ByteDrone, { type DroneState } from './ByteDrone'
import { SyntaxSwarm, LogicBrute, PixelExplosion } from './EnemyCell'

// ─── Tipos ────────────────────────────────────────────────────────────────────

/**
 * 0 = suelo · 1 = muro/corrupcion · 2 = nucleo (meta) · 3 = inicio
 * 4 = Syntax Swarm (enemigo AoE) · 5 = Logic Brute (enemigo blindado)
 */
export type CellType = 0 | 1 | 2 | 3 | 4 | 5

export interface Coord {
  x: number
  y: number
}

export interface EnemyEvent {
  x: number
  y: number
  enemy_type: number
  event: string
  attack_type: string
}

interface Props {
  matrix: CellType[][]
  path?: Coord[]
  cellSize?: number
  stepDelay?: number
  onComplete?: () => void
  onCollision?: (_coord: Coord) => void
  enemyEvents?: EnemyEvent[]
}

// ─── Constantes de estilo (tipos base 0-3) ────────────────────────────────────

const CELL_STYLE: Record<0 | 1 | 2 | 3, string> = {
  0: 'bg-[#0D0D0D] border border-[#1A1A1A]',
  1: 'bg-[#1A0000] border border-red-600/70',
  2: 'bg-[#000D1A] border border-blue-400',
  3: 'bg-[#001A00] border border-[#00FF41]/40',
}

const GAP = 3  // px entre celdas

// ─── Celda base (tipos 0–3) ───────────────────────────────────────────────────

function GridCell({ type, size }: { type: 0 | 1 | 2 | 3; size: number }) {
  return (
    <motion.div
      className={`relative flex items-center justify-center ${CELL_STYLE[type]}`}
      style={{ width: size, height: size }}
      animate={
        type === 2
          ? { boxShadow: ['0 0 6px #0080FF60', '0 0 18px #0080FF', '0 0 6px #0080FF60'] }
          : type === 1
          ? { boxShadow: ['0 0 3px #FF000040', '0 0 8px #FF000070', '0 0 3px #FF000040'] }
          : {}
      }
      transition={
        type === 2 || type === 1
          ? { duration: 1.6, repeat: Infinity, ease: 'easeInOut' }
          : undefined
      }
    >
      {type === 2 && (
        <svg viewBox="0 0 24 24" fill="none" className="w-5 h-5 opacity-80">
          <polygon points="12,2 22,19 2,19"
            fill="none" stroke="#60A5FA" strokeWidth="1.5" />
          <circle cx="12" cy="12" r="3" fill="#60A5FA" />
        </svg>
      )}
      {type === 1 && (
        <div className="w-full h-full opacity-10 absolute inset-0"
          style={{ background: 'repeating-linear-gradient(45deg, #FF3333 0px, #FF3333 1px, transparent 1px, transparent 8px)' }}
        />
      )}
    </motion.div>
  )
}

// ─── GridCanvas ───────────────────────────────────────────────────────────────

export default function GridCanvas({
  matrix,
  path,
  cellSize = 64,
  stepDelay = 380,
  onComplete,
  onCollision,
  enemyEvents,
}: Props) {
  const rows = matrix.length
  const cols = matrix[0]?.length ?? 0

  const startPos = useCallback((): Coord => {
    for (let y = 0; y < rows; y++)
      for (let x = 0; x < cols; x++)
        if (matrix[y][x] === 3) return { x, y }
    return { x: 0, y: 0 }
  }, [matrix, rows, cols])

  const [dronePos, setDronePos]     = useState<Coord>(startPos)
  const [droneState, setDroneState] = useState<DroneState>('idle')
  const [explodingEnemies, setExplodingEnemies] = useState<Set<string>>(new Set())
  const [destroyedEnemies, setDestroyedEnemies] = useState<Set<string>>(new Set())

  const containerCtrl = useAnimation()
  const animRunning   = useRef(false)

  useEffect(() => {
    setDronePos(startPos())
    setDroneState('idle')
    setExplodingEnemies(new Set())
    setDestroyedEnemies(new Set())
  }, [matrix, startPos])

  const triggerShake = useCallback(async () => {
    await containerCtrl.start({
      x: [0, -12, 12, -8, 8, -4, 4, 0],
      transition: { duration: 0.45, ease: 'easeInOut' },
    })
    containerCtrl.set({ x: 0 })
  }, [containerCtrl])

  // ── Animación de recorrido ────────────────────────────────────────────────────

  useEffect(() => {
    if (!path || path.length === 0) return
    if (animRunning.current) return

    animRunning.current = true
    setDroneState('moving')

    let step = 0
    const advance = async () => {
      if (step >= path.length) {
        animRunning.current = false
        return
      }

      const coord    = path[step]
      const cellType = matrix[coord.y]?.[coord.x]

      setDronePos(coord)

      if (cellType === 1) {
        setDroneState('collision')
        triggerShake()
        onCollision?.(coord)
        animRunning.current = false
        return
      }

      if (cellType === 2) {
        setDroneState('complete')
        onComplete?.()
        animRunning.current = false
        return
      }

      step++
      setTimeout(advance, stepDelay)
    }

    const timer = setTimeout(advance, 100)
    return () => {
      clearTimeout(timer)
      animRunning.current = false
    }
  }, [path]) // eslint-disable-line react-hooks/exhaustive-deps

  // ── Explosiones de enemigos (disparan tras el fin de la animación del dron) ──

  useEffect(() => {
    if (!enemyEvents?.length) return

    const pathDelay = (path?.length ?? 0) * stepDelay + 700
    const timers: ReturnType<typeof setTimeout>[] = []

    const outer = setTimeout(() => {
      enemyEvents.forEach((evt, i) => {
        const t = setTimeout(() => {
          const key = `${evt.x}-${evt.y}`
          setExplodingEnemies((prev) => new Set([...prev, key]))
          // Screen shake suave por cada enemigo destruido
          containerCtrl.start({
            x: [0, -6, 6, -4, 4, -2, 2, 0],
            transition: { duration: 0.3, ease: 'easeInOut' },
          }).then(() => containerCtrl.set({ x: 0 }))
          const t2 = setTimeout(() => {
            setExplodingEnemies((prev) => {
              const next = new Set(prev)
              next.delete(key)
              return next
            })
            setDestroyedEnemies((prev) => new Set([...prev, key]))
          }, 900)
          timers.push(t2)
        }, i * 280)
        timers.push(t)
      })
    }, pathDelay)

    return () => {
      clearTimeout(outer)
      timers.forEach(clearTimeout)
    }
  }, [enemyEvents]) // eslint-disable-line react-hooks/exhaustive-deps

  // ── Dimensiones ───────────────────────────────────────────────────────────────

  const stride      = cellSize + GAP
  const dronePixelX = dronePos.x * stride + cellSize / 2
  const dronePixelY = dronePos.y * stride + cellSize / 2
  const droneSize   = Math.round(cellSize * 0.75)
  const gridW = cols * cellSize + (cols - 1) * GAP
  const gridH = rows * cellSize + (rows - 1) * GAP

  // ── Render ────────────────────────────────────────────────────────────────────

  return (
    <motion.div
      animate={containerCtrl}
      className="relative inline-block"
      style={{ width: gridW, height: gridH }}
    >
      {/* Matriz de celdas */}
      <div
        className="absolute inset-0"
        style={{
          display: 'grid',
          gridTemplateColumns: `repeat(${cols}, ${cellSize}px)`,
          gridTemplateRows: `repeat(${rows}, ${cellSize}px)`,
          gap: GAP,
        }}
      >
        {matrix.flatMap((row, y) =>
          row.map((cell, x) => {
            const key = `${x}-${y}`

            if (explodingEnemies.has(key)) {
              return <PixelExplosion key={key} cellSize={cellSize} enemyType={cell} />
            }
            if (destroyedEnemies.has(key)) {
              return <GridCell key={key} type={0} size={cellSize} />
            }
            if (cell === 4) return <SyntaxSwarm key={key} size={cellSize} />
            if (cell === 5) return <LogicBrute  key={key} size={cellSize} />

            return <GridCell key={key} type={cell as 0 | 1 | 2 | 3} size={cellSize} />
          })
        )}
      </div>

      {/* Dron */}
      <motion.div
        className="absolute pointer-events-none"
        style={{ zIndex: 10 }}
        animate={{
          x: dronePixelX - droneSize / 2,
          y: dronePixelY - droneSize / 2,
        }}
        transition={{ type: 'spring', stiffness: 260, damping: 22, mass: 0.8 }}
      >
        <ByteDrone state={droneState} size={droneSize} />
      </motion.div>

      {/* Flash rojo en colisión */}
      {droneState === 'collision' && (
        <motion.div
          className="absolute inset-0 pointer-events-none"
          style={{ background: '#FF000015', zIndex: 20 }}
          initial={{ opacity: 1 }}
          animate={{ opacity: 0 }}
          transition={{ duration: 0.8 }}
        />
      )}

      {/* Overlay de victoria */}
      {droneState === 'complete' && (
        <motion.div
          className="absolute inset-0 flex items-center justify-center pointer-events-none"
          style={{ zIndex: 20 }}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
        >
          <motion.div
            className="font-mono font-black text-yellow-400 text-2xl tracking-widest"
            style={{ textShadow: '0 0 16px #FFD700, 0 0 32px #FFD700' }}
            animate={{ scale: [0.8, 1.1, 1] }}
            transition={{ duration: 0.5 }}
          >
            NUCLEO ALCANZADO
          </motion.div>
        </motion.div>
      )}
    </motion.div>
  )
}
