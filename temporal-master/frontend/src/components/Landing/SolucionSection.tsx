'use client'

/**
 * SolucionSection — Slide 3 del Landing
 * Rediseño: 3 pilares visuales grandes. Sin scroll. Sin texto chico.
 * Enfocado en los 3 diferenciadores reales de DAKI.
 */

import { motion } from 'framer-motion'
import Link from 'next/link'

const PILARES = [
  {
    glyph:   '◈',
    color:   '#00FF41',
    title:   'IA QUE INTERROGA',
    tagline: 'No te da la respuesta.',
    body:    'DAKI detecta exactamente dónde falla tu lógica y construye la pregunta que te fuerza a resolverlo vos. Sin spoilers. Sin atajos.',
    stat:    '3 niveles de escalación cognitiva',
  },
  {
    glyph:   '▶',
    color:   '#06b6d4',
    title:   'CÓDIGO QUE CORRE',
    tagline: 'Sandbox real. Output real.',
    body:    'Cada misión evalúa lo que hace tu código — no lo que decís que hace. Sin múltiple choice. Si falla, falla. Si pasa, pasó.',
    stat:    '100 misiones ejecutables en vivo',
  },
  {
    glyph:   '⬡',
    color:   '#f59e0b',
    title:   'DIFICULTAD ADAPTATIVA',
    tagline: 'Nunca aburrido. Nunca injusto.',
    body:    'El sistema lee tus patrones de error y calibra la próxima misión en tiempo real. Siempre en el borde exacto de tu límite.',
    stat:    'DDA — sin techo artificial',
  },
]

export default function SolucionSection() {
  return (
    <section className="h-full flex flex-col font-mono bg-[#020202] relative overflow-hidden">

      {/* Scanlines sutiles */}
      <div
        className="absolute inset-0 pointer-events-none opacity-[0.012]"
        style={{ backgroundImage: 'repeating-linear-gradient(0deg,transparent,transparent 3px,#00FF41 3px,#00FF41 4px)' }}
      />

      {/* Grid de fondo */}
      <div
        className="absolute inset-0 pointer-events-none"
        style={{
          backgroundImage:
            'linear-gradient(rgba(0,255,65,0.04) 1px, transparent 1px), linear-gradient(90deg, rgba(0,255,65,0.04) 1px, transparent 1px)',
          backgroundSize: '72px 72px',
        }}
      />

      <div className="relative z-10 flex flex-col h-full px-6 sm:px-10 py-7 gap-5">

        {/* ── Header ────────────────────────────────────────────────────────────── */}
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1,  y: 0   }}
          transition={{ duration: 0.35 }}
        >
          <p className="text-[9px] tracking-[0.55em] text-[#00FF41]/25 uppercase mb-3">
            {'// SISTEMA — LO QUE NOS HACE DIFERENTES'}
          </p>
          <h2 className="text-2xl sm:text-3xl font-black text-white/85 uppercase leading-tight tracking-wide">
            No memorizás.
            <br />
            <span
              className="text-[#00FF41]"
              style={{ textShadow: '0 0 28px rgba(0,255,65,0.45)' }}
            >
              Entrenás de verdad.
            </span>
          </h2>
          <p className="mt-2 text-[11px] text-white/25 tracking-[0.25em]">
            Python. Un lenguaje. Llevado hasta el límite.
          </p>
        </motion.div>

        {/* ── 3 Pilares — ocupan el alto restante ─────────────────────────────── */}
        <div className="flex-1 grid grid-cols-1 sm:grid-cols-3 gap-3 min-h-0">
          {PILARES.map(({ glyph, color, title, tagline, body, stat }, i) => (
            <motion.div
              key={title}
              initial={{ opacity: 0, y: 24 }}
              animate={{ opacity: 1,  y: 0  }}
              transition={{ duration: 0.38, delay: 0.10 + i * 0.09 }}
              className="flex flex-col border p-5 sm:p-6 relative overflow-hidden cursor-default transition-all duration-300"
              style={{ borderColor: `${color}22`, background: `${color}04` }}
              onMouseEnter={e => {
                const el = e.currentTarget as HTMLDivElement
                el.style.borderColor = `${color}55`
                el.style.background  = `${color}09`
              }}
              onMouseLeave={e => {
                const el = e.currentTarget as HTMLDivElement
                el.style.borderColor = `${color}22`
                el.style.background  = `${color}04`
              }}
            >
              {/* Línea de acento superior */}
              <div
                className="absolute top-0 left-0 right-0 h-px"
                style={{ background: `linear-gradient(90deg,transparent,${color}55,transparent)` }}
              />

              {/* Glifo grande */}
              <span
                className="text-[56px] sm:text-[64px] font-black leading-none mb-4 block select-none"
                style={{ color, textShadow: `0 0 32px ${color}45` }}
              >
                {glyph}
              </span>

              {/* Título */}
              <h3
                className="text-base sm:text-lg font-black tracking-[0.12em] uppercase leading-tight mb-2"
                style={{ color }}
              >
                {title}
              </h3>

              {/* Tagline */}
              <p
                className="text-[11px] font-bold mb-3 tracking-wide"
                style={{ color: `${color}95` }}
              >
                {tagline}
              </p>

              {/* Cuerpo */}
              <p className="text-[11px] leading-relaxed text-white/40 flex-1">
                {body}
              </p>

              {/* Stat badge */}
              <div
                className="mt-4 pt-3 border-t text-[9px] tracking-[0.3em] uppercase"
                style={{ borderColor: `${color}15`, color: `${color}45` }}
              >
                ▸ {stat}
              </div>
            </motion.div>
          ))}
        </div>

        {/* ── CTA strip ─────────────────────────────────────────────────────────── */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.4, delay: 0.38 }}
          className="flex flex-col sm:flex-row items-center justify-between gap-4 border-t border-[#00FF41]/10 pt-4"
        >
          <p className="text-[11px] text-white/30 tracking-[0.18em] text-center sm:text-left leading-relaxed">
            <span style={{ color: 'rgba(0,255,65,0.65)' }}>100 misiones reales.</span>
            {' · '}
            <span style={{ color: 'rgba(245,158,11,0.65)' }}>1 Boss Final.</span>
            {' · '}
            <span className="text-white/40">Rango que se gana — no se compra.</span>
          </p>
          <Link
            href="/register"
            className="border text-[10px] tracking-[0.4em] uppercase px-8 py-3 whitespace-nowrap transition-all duration-200"
            style={{
              borderColor: 'rgba(0,255,65,0.40)',
              color:       '#00FF41',
              background:  'rgba(0,255,65,0.05)',
            }}
            onMouseEnter={e => {
              const el = e.currentTarget as HTMLAnchorElement
              el.style.background   = 'rgba(0,255,65,0.12)'
              el.style.borderColor  = 'rgba(0,255,65,0.70)'
              el.style.boxShadow    = '0 0 20px rgba(0,255,65,0.15)'
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
