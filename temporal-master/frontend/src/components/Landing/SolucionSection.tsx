'use client'

/**
 * SolucionSection — Slide 3 del Landing
 *
 * Propuesta: Un lenguaje. Dominado de verdad.
 * Diferenciadores: Python-only + gamificación + experiencia verificable.
 */

import { motion } from 'framer-motion'
import Link from 'next/link'

// ─── Data ─────────────────────────────────────────────────────────────────────

const CORE_STATS = [
  { value: '100', label: 'Misiones reales',              icon: '⬡', color: '#00FF41' },
  { value: '4',   label: 'Sectores de dificultad',       icon: '◎', color: '#06b6d4' },
  { value: '1',   label: 'Boss Final de integración',    icon: '◆', color: '#f59e0b' },
  { value: 'DDA', label: 'Dificultad que se adapta',     icon: '◈', color: '#a78bfa' },
]

const BRANCHES = [
  { icon: '⚙', title: 'Automatización',  jobs: 'DevOps · SRE · Scripting',       unlockAt: 60 },
  { icon: '⬡', title: 'Testing y QA',    jobs: 'QA Engineer · SDET',              unlockAt: 70 },
  { icon: '◈', title: 'APIs y Backend',  jobs: 'Backend Dev · API Engineer',      unlockAt: 75 },
  { icon: '◉', title: 'Data Science',    jobs: 'Data Analyst · BI Developer',     unlockAt: 80 },
  { icon: '◬', title: 'IA Aplicada',     jobs: 'ML Engineer · AI Developer',      unlockAt: 90 },
]

const PROBLEMS = [
  { icon: '⬚', label: 'YOUTUBE / TUTORIALES', verdict: 'Sintaxis sin criterio de arquitectura',           color: '#FF6B6B' },
  { icon: '◫', label: 'BOOTCAMPS',            verdict: 'Te da el primer empleo, no los siguientes',        color: '#FFB800' },
  { icon: '◪', label: 'CERTIFICADOS ONLINE',  verdict: 'Acredita que cursaste, no que podés construir',    color: '#00B4D8' },
  { icon: '◆', label: 'NEXO — DAKI',          verdict: 'Código que corre. Errores documentados. Rango real.', color: '#00FF41' },
]

const DAKI_PROTOCOL = [
  {
    letter: 'D', word: 'DIAGNÓSTICO', color: '#00FF41',
    desc: 'Cada misión escanea tu lógica en tiempo real. No qué sabés — cómo pensás bajo presión.',
  },
  {
    letter: 'A', word: 'ADAPTACIÓN', color: '#00B4D8',
    desc: 'DDA ajusta la dificultad a tu historial de errores. Nunca demasiado fácil. Nunca injusto.',
  },
  {
    letter: 'K', word: 'CONOCIMIENTO', color: '#7B2FBE',
    desc: 'Cada concepto es una misión con consecuencias reales. La teoría sin aplicación no existe aquí.',
  },
  {
    letter: 'I', word: 'INTELIGENCIA', color: '#FFB800',
    desc: 'La IA no te da la respuesta. Te interroga hasta que la construís solo — y la recordás.',
  },
]

// ─── Componente ────────────────────────────────────────────────────────────────

export default function SolucionSection() {
  return (
    <section className="h-full flex flex-col font-mono bg-[#020202] overflow-hidden relative">

      {/* Scanlines */}
      <div
        className="absolute inset-0 pointer-events-none opacity-[0.015]"
        style={{ backgroundImage: 'repeating-linear-gradient(0deg,transparent,transparent 3px,#00FF41 3px,#00FF41 4px)' }}
      />

      {/* Contenido scrollable */}
      <div className="flex-1 overflow-y-auto px-6 pt-6 pb-8 min-h-0" style={{ scrollbarWidth: 'none' }}>

        {/* ── Header ──────────────────────────────────────────────────────────── */}
        <motion.div
          initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
          className="mb-7"
        >
          <p className="text-[8px] tracking-[0.6em] text-[#00FF41]/20 mb-2">
            {'// EL NEXO — FORMACIÓN PYTHON INTENSIVA'}
          </p>
          <h2 className="text-lg sm:text-xl font-black tracking-[0.06em] text-white/85 uppercase leading-tight mb-1">
            Un lenguaje.{' '}
            <span className="text-[#00FF41]" style={{ textShadow: '0 0 20px rgba(0,255,65,0.5)' }}>
              Dominado de verdad.
            </span>
          </h2>
          <p className="text-[10px] text-[#00FF41]/35 tracking-[0.3em] uppercase">
            No diez lenguajes a medias. Python al nivel que el mercado exige.
          </p>
        </motion.div>

        {/* ── Python Core — showcase ─────────────────────────────────────────── */}
        <motion.div
          initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.05 }}
          className="relative mb-5 p-5 overflow-hidden"
          style={{ border: '1px solid rgba(0,255,65,0.30)', background: 'rgba(0,255,65,0.03)' }}
        >
          {/* Pulso superior activo */}
          <motion.div
            className="absolute top-0 left-0 right-0 h-px"
            style={{ background: 'linear-gradient(90deg,transparent,rgba(0,255,65,0.60),transparent)' }}
            animate={{ opacity: [0.3, 1, 0.3] }}
            transition={{ duration: 2.2, repeat: Infinity }}
          />

          <div className="flex items-start justify-between gap-3 mb-4">
            <div>
              <div className="flex items-center gap-2 mb-1">
                <motion.span
                  className="w-2 h-2 rounded-full bg-[#00FF41]"
                  animate={{ opacity: [1, 0.3, 1], scale: [1, 1.4, 1] }}
                  transition={{ duration: 1.5, repeat: Infinity }}
                />
                <span className="text-[7px] tracking-[0.5em] text-[#00FF41]/60">FORMACIÓN ACTIVA</span>
              </div>
              <h3 className="text-sm font-black tracking-[0.20em] text-[#00FF41] uppercase"
                style={{ textShadow: '0 0 12px rgba(0,255,65,0.40)' }}>
                OPERACIÓN VANGUARDIA
              </h3>
              <p className="text-[9px] text-[#00FF41]/45 tracking-wider">Python Core · Fundamentos de Élite</p>
            </div>
            <span className="text-2xl" style={{ color: 'rgba(0,255,65,0.50)' }}>⬡</span>
          </div>

          {/* Stats grid */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 mb-4">
            {CORE_STATS.map(({ value, label, icon, color }) => (
              <div key={label} className="border px-3 py-2.5 text-center"
                style={{ borderColor: `${color}18`, background: `${color}04` }}>
                <p className="text-lg font-black font-mono mb-0.5" style={{ color, textShadow: `0 0 10px ${color}55` }}>
                  {value}
                </p>
                <p className="text-[7px] tracking-wider leading-tight" style={{ color: `${color}55` }}>
                  {icon} {label}
                </p>
              </div>
            ))}
          </div>

          <p className="text-[9px] leading-relaxed text-[#00FF41]/50">
            De{' '}
            <span className="text-[#00FF41]/80 font-mono">print(&quot;hola&quot;)</span>
            {' '}a sistemas que corren en producción. Cada sector escala la complejidad.
            El Boss Final valida que podés integrar todo lo aprendido bajo presión.
          </p>
        </motion.div>

        {/* ── Ramas de especialización — post Python Core ──────────────────────── */}
        <motion.div
          initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.10 }}
          className="mb-8"
        >
          <p className="text-[8px] tracking-[0.5em] text-[#f59e0b]/30 uppercase mb-3">
            {'// TRAS COMPLETAR PYTHON CORE — RAMAS DE ESPECIALIZACIÓN'}
          </p>
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-2">
            {BRANCHES.map(({ icon, title, jobs, unlockAt }, i) => (
              <motion.div
                key={title}
                initial={{ opacity: 0, y: 6 }}
                animate={{ opacity: 0.65, y: 0 }}
                transition={{ delay: 0.12 + i * 0.04, duration: 0.22 }}
                className="border px-3 py-3 relative overflow-hidden"
                style={{ borderColor: 'rgba(245,158,11,0.18)', background: 'rgba(245,158,11,0.03)' }}
              >
                <span className="absolute top-1.5 right-1.5 text-[8px]">🔒</span>
                <p className="text-base mb-1" style={{ color: 'rgba(245,158,11,0.40)' }}>{icon}</p>
                <p className="text-[8px] font-black tracking-[0.15em] uppercase leading-snug mb-1"
                  style={{ color: 'rgba(245,158,11,0.55)' }}>
                  {title}
                </p>
                <p className="text-[7px] leading-relaxed" style={{ color: 'rgba(245,158,11,0.30)' }}>{jobs}</p>
                <p className="text-[6px] tracking-[0.3em] mt-1.5" style={{ color: 'rgba(245,158,11,0.25)' }}>
                  desde nivel {unlockAt}
                </p>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* ── Por qué fallan los demás ─────────────────────────────────────────── */}
        <motion.div
          initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.18 }}
          className="mb-8"
        >
          <p className="text-[8px] tracking-[0.5em] text-[#FF0033]/35 uppercase mb-4">
            {'// EL PROBLEMA QUE NINGÚN CURSO ADMITE'}
          </p>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
            {PROBLEMS.map(({ icon, label, verdict, color }, i) => (
              <div
                key={label}
                className="p-3 text-center border transition-all duration-200"
                style={{
                  borderColor: `${color}${i === 3 ? '40' : '12'}`,
                  background:  `${color}${i === 3 ? '06' : '02'}`,
                }}
              >
                <span className="text-xl block mb-1.5" style={{ color: `${color}${i === 3 ? 'cc' : '25'}` }}>
                  {icon}
                </span>
                <p className="text-[8px] font-black tracking-[0.2em] uppercase mb-1"
                  style={{ color: `${color}${i === 3 ? '90' : '40'}` }}>
                  {label}
                </p>
                <p className="text-[7px] tracking-wide leading-4"
                  style={{ color: `${color}${i === 3 ? '65' : '30'}` }}>
                  {verdict}
                </p>
              </div>
            ))}
          </div>
        </motion.div>

        {/* ── Protocolo D·A·K·I ────────────────────────────────────────────────── */}
        <motion.div
          initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.24 }}
          className="mb-8"
        >
          <p className="text-[8px] tracking-[0.5em] text-[#00FF41]/20 uppercase mb-4">
            {'// PROTOCOLO D·A·K·I — POR QUÉ FUNCIONA LA GAMIFICACIÓN'}
          </p>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {DAKI_PROTOCOL.map(({ letter, word, desc, color }) => (
              <div
                key={letter}
                className="border p-4 transition-all duration-200"
                style={{ borderColor: `${color}15`, background: `${color}03` }}
                onMouseEnter={e => {
                  ;(e.currentTarget as HTMLDivElement).style.borderColor = `${color}40`
                  ;(e.currentTarget as HTMLDivElement).style.background  = `${color}07`
                }}
                onMouseLeave={e => {
                  ;(e.currentTarget as HTMLDivElement).style.borderColor = `${color}15`
                  ;(e.currentTarget as HTMLDivElement).style.background  = `${color}03`
                }}
              >
                <span className="text-4xl font-black leading-none block mb-2"
                  style={{ color, textShadow: `0 0 20px ${color}40` }}>
                  {letter}
                </span>
                <p className="text-[8px] font-black tracking-[0.35em] mb-1.5 uppercase" style={{ color }}>
                  {word}
                </p>
                <p className="text-[8px] leading-relaxed" style={{ color: `${color}50` }}>
                  {desc}
                </p>
              </div>
            ))}
          </div>
        </motion.div>

        {/* ── CTA final ────────────────────────────────────────────────────────── */}
        <motion.div
          initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.30 }}
          className="text-center py-6 border border-[#00FF41]/10"
          style={{ background: 'rgba(0,255,65,0.02)' }}
        >
          <p className="text-[9px] tracking-[0.4em] text-[#00FF41]/35 uppercase mb-3">
            Sin tarjeta de crédito. Sin excusas.
          </p>
          <Link
            href="/register"
            className="inline-block border border-[#00FF41]/40 bg-[#00FF41]/[0.07] text-[#00FF41] text-[10px] tracking-[0.4em] uppercase px-8 py-3 transition-all duration-200 hover:bg-[#00FF41]/12 hover:border-[#00FF41]/70"
          >
            {'[[ INGRESAR AL NEXO — ES GRATIS ]]'}
          </Link>
        </motion.div>

      </div>
    </section>
  )
}
