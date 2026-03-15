'use client'

import { motion, useAnimation } from 'framer-motion'
import { useEffect } from 'react'

export type DroneState = 'idle' | 'moving' | 'collision' | 'complete'

interface Props {
  state: DroneState
  size?: number
}

const STATE_COLOR: Record<DroneState, string> = {
  idle:      '#00FFFF',
  moving:    '#00FF41',
  collision: '#FF3333',
  complete:  '#FFD700',
}

const STATE_GLOW: Record<DroneState, string> = {
  idle:      '0 0 10px #00FFFF, 0 0 20px #00FFFF60',
  moving:    '0 0 10px #00FF41, 0 0 20px #00FF4160',
  collision: '0 0 14px #FF3333, 0 0 28px #FF333380',
  complete:  '0 0 14px #FFD700, 0 0 28px #FFD70080',
}

export default function ByteDrone({ state, size = 56 }: Props) {
  const rotorCtrl = useAnimation()
  const bodyCtrl = useAnimation()

  const color = STATE_COLOR[state]

  // Rotores siempre girando, más rápido cuando se mueve
  useEffect(() => {
    rotorCtrl.start({
      rotate: 360,
      transition: {
        duration: state === 'moving' ? 0.4 : state === 'collision' ? 0.15 : 0.9,
        repeat: Infinity,
        ease: 'linear',
      },
    })
  }, [state, rotorCtrl])

  // Parpadeo rojo en colision
  useEffect(() => {
    if (state === 'collision') {
      bodyCtrl.start({
        opacity: [1, 0.2, 1, 0.2, 1],
        transition: { duration: 0.5, ease: 'easeInOut' },
      })
    } else if (state === 'complete') {
      bodyCtrl.start({
        scale: [1, 1.15, 1],
        transition: { duration: 0.6, repeat: 2, ease: 'easeInOut' },
      })
    } else {
      bodyCtrl.start({ opacity: 1, scale: 1 })
    }
  }, [state, bodyCtrl])

  // Bob idle (flotacion suave)
  const idleFloat = state === 'idle' || state === 'moving'
    ? {
        y: [0, -4, 0],
        transition: { duration: 1.8, repeat: Infinity, ease: 'easeInOut' },
      }
    : {}

  const half = size / 2
  const armEnd = size * 0.16  // distancia extremo del brazo desde esquina
  const rotorRx = size * 0.11
  const rotorRy = size * 0.065
  const bodyR = size * 0.22
  const eyeR = size * 0.095
  const pupilR = size * 0.05

  return (
    <motion.div animate={idleFloat} style={{ width: size, height: size }}>
      <motion.svg
        viewBox={`0 0 ${size} ${size}`}
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        animate={bodyCtrl}
        style={{ filter: `drop-shadow(${STATE_GLOW[state]})`, overflow: 'visible' }}
      >
        {/* Brazos diagonales */}
        <line x1={half} y1={half} x2={armEnd} y2={armEnd}             stroke={color} strokeWidth="2" strokeLinecap="round" />
        <line x1={half} y1={half} x2={size - armEnd} y2={armEnd}       stroke={color} strokeWidth="2" strokeLinecap="round" />
        <line x1={half} y1={half} x2={armEnd} y2={size - armEnd}       stroke={color} strokeWidth="2" strokeLinecap="round" />
        <line x1={half} y1={half} x2={size - armEnd} y2={size - armEnd} stroke={color} strokeWidth="2" strokeLinecap="round" />

        {/* Rotores (elipses giratorias) */}
        <motion.g animate={rotorCtrl} style={{ originX: `${armEnd}px`, originY: `${armEnd}px` }}>
          <ellipse cx={armEnd} cy={armEnd} rx={rotorRx} ry={rotorRy}
            fill="#0A0A0A" stroke={color} strokeWidth="1.5" />
        </motion.g>
        <motion.g animate={rotorCtrl} style={{ originX: `${size - armEnd}px`, originY: `${armEnd}px` }}>
          <ellipse cx={size - armEnd} cy={armEnd} rx={rotorRx} ry={rotorRy}
            fill="#0A0A0A" stroke={color} strokeWidth="1.5" />
        </motion.g>
        <motion.g animate={rotorCtrl} style={{ originX: `${armEnd}px`, originY: `${size - armEnd}px` }}>
          <ellipse cx={armEnd} cy={size - armEnd} rx={rotorRx} ry={rotorRy}
            fill="#0A0A0A" stroke={color} strokeWidth="1.5" />
        </motion.g>
        <motion.g animate={rotorCtrl} style={{ originX: `${size - armEnd}px`, originY: `${size - armEnd}px` }}>
          <ellipse cx={size - armEnd} cy={size - armEnd} rx={rotorRx} ry={rotorRy}
            fill="#0A0A0A" stroke={color} strokeWidth="1.5" />
        </motion.g>

        {/* Cuerpo principal */}
        <circle cx={half} cy={half} r={bodyR} fill="#0D0D0D" stroke={color} strokeWidth="1.5" />

        {/* Anillo interior */}
        <circle cx={half} cy={half} r={bodyR * 0.65}
          fill="none" stroke={color} strokeWidth="0.8" strokeDasharray="3 4" opacity="0.5" />

        {/* Ojo / sensor */}
        <circle cx={half} cy={half} r={eyeR} fill={color} />
        <circle cx={half} cy={half} r={pupilR} fill="#FFFFFF" opacity="0.9" />
        <circle cx={half - pupilR * 0.4} cy={half - pupilR * 0.4} r={pupilR * 0.35}
          fill="#000000" opacity="0.4" />
      </motion.svg>
    </motion.div>
  )
}
