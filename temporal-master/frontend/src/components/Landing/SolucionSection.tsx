'use client'

/**
 * SolucionSection — Slide 3 del Landing
 * 3 pilares + terminal animada por tarjeta (typewriter Python en vivo).
 */

import { motion } from 'framer-motion'
import { useState, useEffect } from 'react'
import Link from 'next/link'

// ─── Tipos ────────────────────────────────────────────────────────────────────

type LT = 'code' | 'error' | 'ok' | 'daki' | 'dim' | 'blank'
interface CodeLine { code: string; type: LT }

// ─── Data ─────────────────────────────────────────────────────────────────────

const PILARES = [
  {
    glyph:   '◈',
    color:   '#00FF41',
    title:   'IA QUE INTERROGA',
    tagline: 'No te da la respuesta.',
    body:    'DAKI detecta dónde falla tu lógica y construye la pregunta exacta que te fuerza a resolverlo vos.',
    stat:    '3 niveles de escalación cognitiva',
    termTitle: 'MISIÓN 23 · DAKI ACTIVO',
    delay:   400,
    lines: [
      { code: 'def suma_lista(nums):', type: 'code' },
      { code: '    total = 0',         type: 'code' },
      { code: '    for n in nums',     type: 'error' },
      { code: '        total += n',    type: 'dim'  },
      { code: '    return total',      type: 'dim'  },
      { code: '',                      type: 'blank' },
      { code: '✗  SyntaxError — línea 3', type: 'error' },
      { code: '',                         type: 'blank' },
      { code: '◈  "¿Qué necesita el for',  type: 'daki' },
      { code: '    para funcionar?"',       type: 'daki' },
    ] as CodeLine[],
  },
  {
    glyph:   '▶',
    color:   '#06b6d4',
    title:   'CÓDIGO QUE CORRE',
    tagline: 'Sandbox real. Output real.',
    body:    'Cada misión evalúa lo que hace tu código. Sin múltiple choice. Si falla, falla. Si pasa, pasó.',
    stat:    '195 misiones ejecutables en vivo',
    termTitle: 'SANDBOX · EJECUCIÓN EN VIVO',
    delay:   900,
    lines: [
      { code: 'nums = [3, 7, 2, 9, 1, 5]', type: 'code' },
      { code: '',                            type: 'blank' },
      { code: 'top3 = sorted(nums,',         type: 'code' },
      { code: '    reverse=True)[:3]',        type: 'code' },
      { code: 'print(f"Top 3: {top3}")',      type: 'code' },
      { code: '',                             type: 'blank' },
      { code: '$ ejecutando...',              type: 'dim'  },
      { code: 'Top 3: [9, 7, 5]',            type: 'code' },
      { code: '',                             type: 'blank' },
      { code: '✓  MISIÓN COMPLETADA +120 XP', type: 'ok'  },
    ] as CodeLine[],
  },
  {
    glyph:   '⬡',
    color:   '#f59e0b',
    title:   'DIFICULTAD ADAPTATIVA',
    tagline: 'Nunca aburrido. Nunca injusto.',
    body:    'El sistema lee tus patrones de error y calibra la próxima misión siempre en el borde de tu límite.',
    stat:    'DDA — sin techo artificial',
    termTitle: 'DDA · CALIBRACIÓN EN TIEMPO REAL',
    delay:   1400,
    lines: [
      { code: '# análisis de sesión',        type: 'dim'   },
      { code: 'errores_indent  : 4',          type: 'error' },
      { code: 'errores_sintaxis: 1',          type: 'code'  },
      { code: 'tiempo_promedio : 4.2 min',    type: 'code'  },
      { code: 'tasa_éxito      : 68%',        type: 'code'  },
      { code: '',                             type: 'blank'  },
      { code: '⬡  DDA calibrando...',         type: 'daki'  },
      { code: '   foco      → indentación',   type: 'daki'  },
      { code: '   siguiente → nivel 2',       type: 'daki'  },
      { code: '   misión lista ✓',            type: 'ok'    },
    ] as CodeLine[],
  },
]

// ─── Terminal animada ─────────────────────────────────────────────────────────

function Terminal({
  lines, color, title, startDelay,
}: {
  lines: CodeLine[]; color: string; title: string; startDelay: number
}) {
  const [visible, setVisible] = useState(0)
  const [active,  setActive]  = useState(false)

  useEffect(() => {
    const t = setTimeout(() => setActive(true), startDelay)
    return () => clearTimeout(t)
  }, [startDelay])

  useEffect(() => {
    if (!active) return
    if (visible < lines.length) {
      const ms = lines[visible]?.type === 'blank' ? 80 : 310
      const t = setTimeout(() => setVisible(v => v + 1), ms)
      return () => clearTimeout(t)
    }
    const t = setTimeout(() => setVisible(0), 3800)
    return () => clearTimeout(t)
  }, [active, visible, lines])

  const lineColor = (type: LT): string => {
    switch (type) {
      case 'error': return '#FF6B6B'
      case 'ok':    return '#00FF41'
      case 'daki':  return color
      case 'dim':   return 'rgba(255,255,255,0.22)'
      case 'blank': return 'transparent'
      default:      return 'rgba(255,255,255,0.60)'
    }
  }

  return (
    <div
      className="flex-1 min-h-0 flex flex-col overflow-hidden mt-3"
      style={{ border: `1px solid ${color}20`, background: 'rgba(0,0,0,0.45)' }}
    >
      {/* Barra del terminal */}
      <div
        className="flex items-center gap-2 px-3 py-1.5 border-b shrink-0"
        style={{ borderColor: `${color}15`, background: `${color}07` }}
      >
        <div className="flex gap-1">
          {[0.45, 0.25, 0.12].map((o, i) => (
            <span key={i} className="w-2 h-2 rounded-full" style={{ background: `${color}`, opacity: o }} />
          ))}
        </div>
        <span className="text-[8px] tracking-[0.3em] uppercase truncate" style={{ color: `${color}50` }}>
          {title}
        </span>
      </div>

      {/* Código */}
      <div className="flex-1 px-3 py-2.5 font-mono text-[11px] leading-[1.75] overflow-hidden">
        {lines.slice(0, visible).map((line, i) => (
          <div key={i}>
            {line.type === 'blank' ? (
              <span>&nbsp;</span>
            ) : (
              <span style={{ color: lineColor(line.type) }}>
                {line.code}
                {i === visible - 1 && (
                  <span
                    className="inline-block w-[6px] h-[12px] ml-0.5 align-middle"
                    style={{ background: color, animation: 'tw-blink 0.75s step-end infinite' }}
                  />
                )}
              </span>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

// ─── Componente principal ─────────────────────────────────────────────────────

export default function SolucionSection() {
  return (
    <section className="h-full flex flex-col font-mono bg-[#020202] relative overflow-hidden">

      <style>{`
        @keyframes tw-blink { 0%,100%{opacity:1} 50%{opacity:0} }
      `}</style>

      {/* Scanlines */}
      <div
        className="absolute inset-0 pointer-events-none opacity-[0.012]"
        style={{ backgroundImage: 'repeating-linear-gradient(0deg,transparent,transparent 3px,#00FF41 3px,#00FF41 4px)' }}
      />
      {/* Grid */}
      <div
        className="absolute inset-0 pointer-events-none"
        style={{
          backgroundImage: 'linear-gradient(rgba(0,255,65,0.04) 1px,transparent 1px),linear-gradient(90deg,rgba(0,255,65,0.04) 1px,transparent 1px)',
          backgroundSize:  '72px 72px',
        }}
      />

      <div className="relative z-10 flex flex-col h-full px-6 sm:px-10 py-7 gap-4">

        {/* ── Header ──────────────────────────────────────────────────────────── */}
        <motion.div
          initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.35 }}
        >
          <p className="text-[9px] tracking-[0.55em] text-[#00FF41]/25 uppercase mb-2">
            {'// SISTEMA — LO QUE NOS HACE DIFERENTES'}
          </p>
          <h2 className="text-2xl sm:text-3xl font-black text-white/85 uppercase leading-tight tracking-wide">
            No memorizás.{' '}
            <span className="text-[#00FF41]" style={{ textShadow: '0 0 28px rgba(0,255,65,0.45)' }}>
              Entrenás de verdad.
            </span>
          </h2>
        </motion.div>

        {/* ── 3 Pilares ───────────────────────────────────────────────────────── */}
        <div className="flex-1 grid grid-cols-1 sm:grid-cols-3 gap-3 min-h-0">
          {PILARES.map(({ glyph, color, title, tagline, body, stat, termTitle, delay, lines }, i) => (
            <motion.div
              key={title}
              initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.38, delay: 0.10 + i * 0.09 }}
              className="flex flex-col border p-4 sm:p-5 relative overflow-hidden cursor-default transition-all duration-300"
              style={{ borderColor: `${color}22`, background: `${color}04` }}
              onMouseEnter={e => {
                const el = e.currentTarget as HTMLDivElement
                el.style.borderColor = `${color}50`
                el.style.background  = `${color}08`
              }}
              onMouseLeave={e => {
                const el = e.currentTarget as HTMLDivElement
                el.style.borderColor = `${color}22`
                el.style.background  = `${color}04`
              }}
            >
              {/* Acento superior */}
              <div className="absolute top-0 left-0 right-0 h-px"
                style={{ background: `linear-gradient(90deg,transparent,${color}55,transparent)` }} />

              {/* Encabezado de tarjeta */}
              <div className="flex items-center gap-3 mb-3">
                <span
                  className="text-4xl font-black leading-none select-none shrink-0"
                  style={{ color, textShadow: `0 0 20px ${color}45` }}
                >
                  {glyph}
                </span>
                <div>
                  <h3 className="text-sm font-black tracking-[0.12em] uppercase leading-tight" style={{ color }}>
                    {title}
                  </h3>
                  <p className="text-[10px] font-bold tracking-wide" style={{ color: `${color}90` }}>
                    {tagline}
                  </p>
                </div>
              </div>

              {/* Cuerpo */}
              <p className="text-[11px] leading-relaxed text-white/38 shrink-0">
                {body}
              </p>

              {/* Terminal animada — ocupa el espacio restante */}
              <Terminal lines={lines} color={color} title={termTitle} startDelay={delay} />

              {/* Stat */}
              <div
                className="mt-3 pt-2.5 border-t text-[9px] tracking-[0.3em] uppercase shrink-0"
                style={{ borderColor: `${color}15`, color: `${color}40` }}
              >
                ▸ {stat}
              </div>
            </motion.div>
          ))}
        </div>

        {/* ── CTA strip ───────────────────────────────────────────────────────── */}
        <motion.div
          initial={{ opacity: 0 }} animate={{ opacity: 1 }}
          transition={{ duration: 0.4, delay: 0.38 }}
          className="flex flex-col sm:flex-row items-center justify-between gap-3 border-t border-[#00FF41]/10 pt-3"
        >
          <p className="text-[11px] text-white/30 tracking-[0.18em] text-center sm:text-left">
            <span style={{ color: 'rgba(0,255,65,0.65)' }}>195 misiones reales.</span>
            {' · '}
            <span style={{ color: 'rgba(245,158,11,0.65)' }}>1 Boss Final.</span>
            {' · '}
            <span className="text-white/40">Rango que se gana — no se compra.</span>
          </p>
          <Link
            href="/register"
            className="border text-[10px] tracking-[0.4em] uppercase px-8 py-3 whitespace-nowrap transition-all duration-200"
            style={{ borderColor: 'rgba(0,255,65,0.40)', color: '#00FF41', background: 'rgba(0,255,65,0.05)' }}
            onMouseEnter={e => {
              const el = e.currentTarget as HTMLAnchorElement
              el.style.background  = 'rgba(0,255,65,0.12)'
              el.style.borderColor = 'rgba(0,255,65,0.70)'
              el.style.boxShadow   = '0 0 20px rgba(0,255,65,0.15)'
            }}
            onMouseLeave={e => {
              const el = e.currentTarget as HTMLAnchorElement
              el.style.background  = 'rgba(0,255,65,0.05)'
              el.style.borderColor = 'rgba(0,255,65,0.40)'
              el.style.boxShadow   = 'none'
            }}
          >
            {'[[ ACCEDER — ES GRATIS ]]'}
          </Link>
        </motion.div>

      </div>
    </section>
  )
}
