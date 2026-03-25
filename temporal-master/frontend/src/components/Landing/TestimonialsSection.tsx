'use client'

/**
 * TestimonialsSection — La Visión · DAKI EdTech
 * Diseño: tarjetas neon con texto blanco brillante, cambio de paradigma
 */

import { motion } from 'framer-motion'

const SHIFTS = [
  {
    label:  'EL CONOCIMIENTO',
    before: 'Te enseñamos sintaxis hasta que la recuerdes.',
    after:  'Te hacemos necesitar la solución hasta que la descubras.',
    accent: 'La fluidez no se memoriza — se forja bajo presión real.',
    color:  '#00FF41',
  },
  {
    label:  'EL APRENDIZAJE',
    before: 'Videos pregrabados que puedes pausar, rebobinar, ignorar.',
    after:  'Un sistema que ajusta la exigencia a tu lógica en tiempo real.',
    accent: 'La IA no te espera. Tú la alcanzas.',
    color:  '#00B4D8',
  },
  {
    label:  'EL RESULTADO',
    before: 'Un certificado que valida que completaste un curso.',
    after:  'Un sistema desplegado que valida que puedes construir uno.',
    accent: 'El mercado no lee diplomas. Lee código en producción.',
    color:  '#FFB800',
  },
] as const

export default function TestimonialsSection() {
  return (
    <section className="bg-[#060606] font-mono px-6 md:px-12 min-h-screen flex flex-col justify-center py-10 relative overflow-hidden">

      <div
        className="absolute inset-0 pointer-events-none opacity-[0.014]"
        style={{ backgroundImage: 'linear-gradient(#00FF41 1px,transparent 1px),linear-gradient(90deg,#00FF41 1px,transparent 1px)', backgroundSize: '48px 48px' }}
      />

      <div className="max-w-5xl mx-auto w-full relative z-10">

        {/* Header */}
        <motion.div
          className="mb-8"
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <p className="text-[#FF0033]/40 text-[9px] tracking-[0.6em] uppercase mb-4">
            {'// LA DISRUPCIÓN — POR QUÉ DAKI EXISTE'}
          </p>
          <h2 className="text-2xl sm:text-3xl md:text-4xl font-bold tracking-[0.05em] uppercase leading-tight">
            <span className="text-white" style={{ textShadow: '0 0 40px rgba(255,255,255,0.08)' }}>
              EL PROBLEMA NO ES QUE APRENDER SEA{' '}
            </span>
            <span className="text-[#FF0033]" style={{ textShadow: '0 0 24px rgba(255,0,51,0.5)' }}>
              DIFÍCIL.
            </span>
          </h2>
          <p className="text-[#C0C0C0]/45 text-sm leading-6 tracking-wide max-w-2xl mt-3">
            Décadas de cursos crearon ingenieros que saben explicar el código pero no pueden desplegarlo.
            DAKI existe para romper ese ciclo.
          </p>
        </motion.div>

        {/* Tarjetas neon */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-7">
          {SHIFTS.map(({ label, before, after, accent, color }, i) => (
            <motion.div
              key={label}
              className="flex flex-col gap-4 p-6 relative overflow-hidden"
              style={{
                border: `1px solid ${color}28`,
                background: 'rgba(4,6,4,0.7)',
                boxShadow: `0 0 30px ${color}08, inset 0 0 40px rgba(0,0,0,0.5)`,
              }}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.45, delay: i * 0.1 }}
            >
              {/* Línea superior de color */}
              <div className="absolute top-0 left-0 right-0 h-px" style={{ background: `linear-gradient(90deg, transparent, ${color}60, transparent)` }} />

              {/* Label */}
              <p className="text-[9px] tracking-[0.55em] font-bold uppercase" style={{ color: `${color}55` }}>
                {label}
              </p>

              {/* AYER */}
              <div>
                <p className="text-[#FF0033]/35 text-[8px] tracking-[0.4em] uppercase mb-1.5">ANTES</p>
                <p className="text-white/28 text-[11px] leading-5 italic tracking-wide">
                  &ldquo;{before}&rdquo;
                </p>
              </div>

              <div className="h-px" style={{ background: `${color}14` }} />

              {/* DAKI */}
              <div>
                <p className="text-[8px] tracking-[0.4em] uppercase mb-1.5 font-bold" style={{ color: `${color}60` }}>
                  DAKI
                </p>
                <p
                  className="text-[13px] leading-6 font-bold tracking-wide"
                  style={{
                    color: 'rgba(255,255,255,0.92)',
                    textShadow: '0 0 20px rgba(255,255,255,0.25)',
                  }}
                >
                  {after}
                </p>
              </div>

              {/* Accent */}
              <p
                className="text-[10px] leading-5 tracking-wide border-l-2 pl-3 mt-auto"
                style={{ color: `${color}55`, borderColor: `${color}30` }}
              >
                {accent}
              </p>
            </motion.div>
          ))}
        </div>

        {/* Cierre */}
        <motion.div
          className="border border-[#00FF41]/10 p-6 text-center relative overflow-hidden"
          style={{ background: 'rgba(0,255,65,0.02)' }}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.4 }}
        >
          <div className="absolute top-0 left-0 right-0 h-px" style={{ background: 'linear-gradient(90deg,transparent,rgba(0,255,65,0.3),transparent)' }} />
          <p
            className="text-lg sm:text-xl md:text-2xl font-bold tracking-[0.06em] uppercase leading-tight"
            style={{ color: 'rgba(255,255,255,0.88)', textShadow: '0 0 30px rgba(255,255,255,0.15)' }}
          >
            PYTHON ES EL PRIMER PROTOCOLO.{' '}
            <span className="text-[#00FF41]" style={{ textShadow: '0 0 20px rgba(0,255,65,0.5)' }}>
              LA LÓGICA ES EL PRODUCTO REAL.
            </span>
          </p>
          <p className="text-[#C0C0C0]/32 text-[11px] leading-6 tracking-wide max-w-xl mx-auto mt-3">
            No entrenamos programadores de Python. Entrenamos ingenieros que piensan en sistemas,
            diseñan con arquitectura y despliegan con confianza.
          </p>
        </motion.div>

      </div>
    </section>
  )
}
