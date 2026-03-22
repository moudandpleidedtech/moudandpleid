'use client'

/**
 * DakiWaveform — forma de onda de audio abstracta para el avatar de DAKI.
 *
 * - isActive=false → barras planas, sin glow, estáticas
 * - isActive=true  → barras oscilan con alturas y tiempos escalonados (Framer Motion)
 *
 * Props:
 *   isActive  — true cuando DAKI está "hablando" (mostrando texto / voz activa)
 *   color     — color base de las barras (hereda del nivel evolutivo: verde/cian/magenta)
 *   size      — "sm" = 7 barras 2px, "md" = 9 barras 3px (default)
 */

import { motion } from 'framer-motion'

interface Props {
  isActive: boolean
  color?: string
  size?: 'sm' | 'md'
}

// Alturas en reposo (px) para cada barra — asimetría intencional para aspecto orgánico
const IDLE_SM: number[] = [4, 7, 5, 9, 6, 7, 4]
const IDLE_MD: number[] = [4, 7, 5, 11, 8, 12, 6, 9, 4]

// Amplitudes de pico adicionales al oscilar (peak = idle + amp)
const AMP_SM:  number[] = [9, 6, 13, 5, 10, 6, 9]
const AMP_MD:  number[] = [10, 7, 15, 5, 12, 4, 13, 6, 10]

export default function DakiWaveform({
  isActive,
  color = '#BD00FF',
  size = 'md',
}: Props) {
  const idle = size === 'sm' ? IDLE_SM : IDLE_MD
  const amp  = size === 'sm' ? AMP_SM  : AMP_MD
  const w    = size === 'sm' ? 2 : 3
  const gap  = size === 'sm' ? 2 : 3
  const maxH = size === 'sm' ? 20 : 26

  return (
    <div
      className="flex items-end"
      style={{ gap, height: maxH, userSelect: 'none', pointerEvents: 'none' }}
      aria-hidden="true"
    >
      {idle.map((h, i) => (
        <motion.span
          key={i}
          style={{
            width:         w,
            borderRadius:  1,
            background:    color,
            display:       'block',
            boxShadow:     isActive ? `0 0 ${w * 3}px ${color}80` : 'none',
            transformOrigin: 'bottom',
          }}
          animate={{
            height: isActive
              ? [h, h + amp[i], h + amp[i] * 0.35, h + amp[i] * 0.85, h]
              : [h, h * 0.7, h],
          }}
          transition={
            isActive
              ? {
                  duration:  0.55 + i * 0.045,
                  repeat:    Infinity,
                  ease:      'easeInOut',
                  delay:     i * 0.055,
                }
              : {
                  duration: 0.4,
                  ease:     'easeOut',
                }
          }
        />
      ))}
    </div>
  )
}
