'use client'

/**
 * TacticalPanel — Contenedor estético reutilizable D040
 *
 * Encapsula la estética "Inmersión Neón Latiendo" (Nexo-V4).
 * Úsalo como wrapper para cualquier panel, modal o sección secundaria.
 *
 * Uso mínimo:
 *   <TacticalPanel>contenido</TacticalPanel>
 *
 * Uso completo:
 *   <TacticalPanel variant="gold" label="ESTADÍSTICAS" pulse interactive>
 *     contenido
 *   </TacticalPanel>
 */

import { ReactNode } from 'react'
import { motion }   from 'framer-motion'

// ─── Variantes ────────────────────────────────────────────────────────────────

export type TacticalVariant = 'cyan' | 'emerald' | 'gold' | 'red'

const VARIANT_TOKENS: Record<TacticalVariant, {
  border:      string
  borderHover: string
  shadow:      string
  shadowHover: string
  corner:      string
  labelColor:  string
  pulseClass:  string
}> = {
  cyan: {
    border:      'rgba(6,182,212,0.40)',
    borderHover: 'rgba(6,182,212,0.75)',
    shadow:      '0 0 0 1px rgba(6,182,212,0.40), 0 0 10px rgba(6,182,212,0.25)',
    shadowHover: '0 0 0 1px rgba(6,182,212,0.75), 0 0 18px rgba(6,182,212,0.45), 0 0 36px rgba(6,182,212,0.15)',
    corner:      'rgba(6,182,212,0.55)',
    labelColor:  'rgba(6,182,212,0.55)',
    pulseClass:  'neon-pulse',
  },
  emerald: {
    border:      'rgba(16,185,129,0.40)',
    borderHover: 'rgba(16,185,129,0.75)',
    shadow:      '0 0 0 1px rgba(16,185,129,0.45), 0 0 12px rgba(16,185,129,0.28)',
    shadowHover: '0 0 0 1px rgba(16,185,129,0.75), 0 0 20px rgba(16,185,129,0.45), 0 0 40px rgba(16,185,129,0.18)',
    corner:      'rgba(16,185,129,0.55)',
    labelColor:  'rgba(16,185,129,0.55)',
    pulseClass:  'neon-pulse--emerald',
  },
  gold: {
    border:      'rgba(245,158,11,0.40)',
    borderHover: 'rgba(245,158,11,0.75)',
    shadow:      '0 0 0 1px rgba(245,158,11,0.40), 0 0 10px rgba(245,158,11,0.22)',
    shadowHover: '0 0 0 1px rgba(245,158,11,0.75), 0 0 18px rgba(245,158,11,0.40), 0 0 36px rgba(245,158,11,0.15)',
    corner:      'rgba(245,158,11,0.55)',
    labelColor:  'rgba(245,158,11,0.55)',
    pulseClass:  'neon-pulse--gold',
  },
  red: {
    border:      'rgba(255,68,68,0.40)',
    borderHover: 'rgba(255,68,68,0.75)',
    shadow:      '0 0 0 1px rgba(255,68,68,0.40), 0 0 10px rgba(255,68,68,0.22)',
    shadowHover: '0 0 0 1px rgba(255,68,68,0.75), 0 0 18px rgba(255,68,68,0.40)',
    corner:      'rgba(255,68,68,0.55)',
    labelColor:  'rgba(255,68,68,0.55)',
    pulseClass:  '',
  },
}

// ─── Props ────────────────────────────────────────────────────────────────────

export interface TacticalPanelProps {
  children:     ReactNode
  variant?:     TacticalVariant  // 'cyan' por defecto
  label?:       string           // etiqueta táctica encima del borde superior izq.
  pulse?:       boolean          // activa latido neonPulse (3s)
  interactive?: boolean          // hover effects + cursor-pointer
  padding?:     string           // clase de Tailwind, ej. 'p-4', 'px-5 py-4'
  className?:   string           // clases extra (layout, size, etc.)
  onClick?:     () => void
  corners?:     boolean          // esquinas decorativas (default true)
  animate?:     boolean          // entrada con fade + y (default true)
  delay?:       number           // delay de la animación de entrada en segundos
}

// ─── Componente ───────────────────────────────────────────────────────────────

export default function TacticalPanel({
  children,
  variant     = 'cyan',
  label,
  pulse       = false,
  interactive = false,
  padding     = 'p-5',
  className   = '',
  onClick,
  corners     = true,
  animate     = true,
  delay       = 0,
}: TacticalPanelProps) {
  const tk = VARIANT_TOKENS[variant]

  const Tag = animate ? motion.div : 'div'

  const animateProps = animate ? {
    initial:    { opacity: 0, y: 8 },
    animate:    { opacity: 1, y: 0 },
    transition: { delay, duration: 0.35, ease: 'easeOut' },
  } : {}

  return (
    <div className={`relative ${pulse ? tk.pulseClass : ''} ${className}`}>

      {/* ── Etiqueta táctica superior ── */}
      {label && (
        <p
          className="absolute -top-2.5 left-3 text-[6px] tracking-[0.55em] font-black font-mono uppercase px-1.5 z-10"
          style={{ color: tk.labelColor, background: '#020617' }}
        >
          {label}
        </p>
      )}

      {/* ── Línea de pulso superior ── */}
      <motion.div
        className="absolute top-0 left-0 right-0 h-px pointer-events-none z-10"
        style={{ background: `linear-gradient(90deg, transparent, ${tk.border.replace('0.40', '0.70')}, transparent)` }}
        animate={{ opacity: [0.25, 0.85, 0.25] }}
        transition={{ duration: 2.6, repeat: Infinity }}
      />

      {/* ── Contenedor principal ── */}
      {/* eslint-disable-next-line @typescript-eslint/no-explicit-any */}
      <Tag
        className={[
          'relative overflow-hidden font-mono',
          interactive ? 'cursor-pointer group' : '',
          padding,
        ].filter(Boolean).join(' ')}
        style={{
          background: '#020617',
          border:     `1px solid ${tk.border}`,
          boxShadow:  tk.shadow,
          transition: interactive ? 'border-color 0.18s ease, box-shadow 0.18s ease' : undefined,
        }}
        onClick={onClick}
        {...animateProps}
        {...(interactive ? {
          onMouseEnter: (e: React.MouseEvent<HTMLDivElement>) => {
            const el = e.currentTarget as HTMLDivElement
            el.style.borderColor = tk.borderHover
            el.style.boxShadow   = tk.shadowHover
          },
          onMouseLeave: (e: React.MouseEvent<HTMLDivElement>) => {
            const el = e.currentTarget as HTMLDivElement
            el.style.borderColor = tk.border
            el.style.boxShadow   = tk.shadow
          },
        } : {})}
      >
        {children}
      </Tag>

      {/* ── Esquinas decorativas ── */}
      {corners && (
        <>
          <span className="absolute top-0 left-0  w-2.5 h-2.5 border-t border-l pointer-events-none z-10" style={{ borderColor: tk.corner }} />
          <span className="absolute top-0 right-0 w-2.5 h-2.5 border-t border-r pointer-events-none z-10" style={{ borderColor: tk.corner }} />
          <span className="absolute bottom-0 left-0  w-2.5 h-2.5 border-b border-l pointer-events-none z-10" style={{ borderColor: tk.corner }} />
          <span className="absolute bottom-0 right-0 w-2.5 h-2.5 border-b border-r pointer-events-none z-10" style={{ borderColor: tk.corner }} />
        </>
      )}
    </div>
  )
}

// ─── TacticalStatusText — texto de estado táctico (nexo-tactical-green) ──────

export function TacticalStatusText({
  children,
  className = '',
  dim = false,
}: {
  children:  ReactNode
  className?: string
  dim?:       boolean      // reduce la opacidad para texto secundario
}) {
  return (
    <span
      className={`font-mono font-black tracking-widest uppercase ${className}`}
      style={{ color: dim ? 'rgba(74,222,128,0.45)' : 'rgba(74,222,128,0.85)' }}
    >
      {children}
    </span>
  )
}

// ─── TacticalButton — botón interactivo con glow según estado ─────────────────

export function TacticalButton({
  children,
  variant    = 'cyan',
  onClick,
  disabled   = false,
  size       = 'md',
  className  = '',
}: {
  children:  ReactNode
  variant?:  'cyan' | 'gold' | 'red'
  onClick?:  () => void
  disabled?: boolean
  size?:     'sm' | 'md' | 'lg'
  className?: string
}) {
  const BUTTON_TOKENS = {
    cyan: { base: 'rgba(6,182,212,0.55)',  hover: 'rgba(6,182,212,0.95)', bg: 'rgba(6,182,212,0.10)', hoverBg: 'rgba(6,182,212,0.20)', glow: '0 0 20px rgba(6,182,212,0.40)'  },
    gold: { base: 'rgba(245,158,11,0.60)', hover: 'rgba(245,158,11,0.95)', bg: 'rgba(245,158,11,0.08)', hoverBg: 'rgba(245,158,11,0.18)', glow: '0 0 20px rgba(245,158,11,0.38)'  },
    red:  { base: 'rgba(255,68,68,0.55)',  hover: 'rgba(255,68,68,0.95)',  bg: 'rgba(255,68,68,0.08)',  hoverBg: 'rgba(255,68,68,0.18)',  glow: '0 0 20px rgba(255,68,68,0.38)'   },
  }
  const tk = BUTTON_TOKENS[variant]

  const SIZE_CLS = {
    sm: 'text-[8px] tracking-[0.35em] px-3 py-1.5',
    md: 'text-[9px] tracking-[0.40em] px-4 py-2.5',
    lg: 'text-[11px] tracking-[0.35em] px-5 py-3',
  }

  return (
    <motion.button
      onClick={onClick}
      disabled={disabled}
      className={[
        SIZE_CLS[size],
        'font-black uppercase font-mono border transition-all duration-150',
        disabled ? 'opacity-40 cursor-not-allowed' : 'cursor-pointer',
        className,
      ].filter(Boolean).join(' ')}
      style={{ borderColor: tk.base, color: tk.base, background: tk.bg }}
      whileHover={disabled ? {} : {
        borderColor: tk.hover,
        color:       tk.hover,
        background:  tk.hoverBg,
        boxShadow:   tk.glow,
      }}
      whileTap={disabled ? {} : { scale: 0.97 }}
    >
      {children}
    </motion.button>
  )
}
