'use client'

/**
 * SolucionSection — Slide 3 del Landing
 *
 * Rediseño D025: de tabs fragmentados a flujo continuo.
 * Objetivo: generar deseo por el ecosistema antes de pedir el registro.
 * Una sola sección scrollable — sin fricción de clicks.
 */

import { motion } from 'framer-motion'
import Link from 'next/link'

// ─── Data ─────────────────────────────────────────────────────────────────────

const FORMATIONS = [
  {
    code: '01', name: 'OPERACIÓN VANGUARDIA', sub: 'Python Core · Fundamentos de Élite',
    color: '#00FF41', icon: '⬡', status: 'ACTIVA', locked: false,
    desc: 'De print("hola") a sistemas que corren en producción. 100 niveles. 4 sectores. 1 Boss Final.',
  },
  {
    code: '02', name: 'PROTOCOLO TPM', sub: 'Technical Project Manager',
    color: '#FF6B35', icon: '◎', status: 'ENCRIPTADO', locked: true,
    desc: 'Gestión de equipos de ingeniería bajo presión real. Stakeholders imposibles. Decisiones críticas.',
  },
  {
    code: '03', name: 'PROTOCOLO ARES', sub: 'Ciberseguridad · Red Team',
    color: '#FF2D78', icon: '⬟', status: 'CLASIFICADO', locked: true,
    desc: 'Piensa como atacante, construye como defensor. CTF, CVE, kill-chain ofensivo.',
  },
  {
    code: '04', name: 'TECHNICAL SALES', sub: 'Del código a la mesa de negocios',
    color: '#FFC700', icon: '◈', status: 'CLASIFICADO', locked: true,
    desc: 'Tu expertise técnico como ventaja comercial. Para el dev que quiere cruzar al otro lado.',
  },
]

const DAKI_PROTOCOL = [
  { letter: 'D', word: 'DIAGNÓSTICO',  desc: 'Cada interacción escanea tu lógica. No qué sabés — cómo pensás.', color: '#00FF41' },
  { letter: 'A', word: 'ADAPTACIÓN',   desc: 'El sistema ajusta la dificultad en tiempo real a tu historial de errores.', color: '#00B4D8' },
  { letter: 'K', word: 'CONOCIMIENTO', desc: 'Nada es teoría sin aplicación. Cada concepto es una misión con consecuencias.', color: '#7B2FBE' },
  { letter: 'I', word: 'INTELIGENCIA', desc: 'La IA no te da la respuesta. Te interroga hasta que la construís solo.', color: '#FFB800' },
]

const PROBLEMS = [
  { icon: '⬚', label: 'CURSOS ONLINE',       verdict: 'Certificado sin arquitectura',  color: '#FF6B6B' },
  { icon: '◫', label: 'BOOTCAMPS',            verdict: 'Alcanza para entrar, no para crecer', color: '#FFB800' },
  { icon: '◪', label: 'YOUTUBE + TUTORIALES', verdict: 'Conocimiento fragmentado',      color: '#00B4D8' },
  { icon: '◆', label: 'DAKI',                 verdict: 'Sistema que piensa con vos',    color: '#00FF41' },
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
            {'// EL NEXO — ECOSISTEMA DE FORMACIONES'}
          </p>
          <h2 className="text-lg sm:text-xl font-black tracking-[0.08em] text-white/85 uppercase leading-tight mb-1">
            Cuatro formaciones.{' '}
            <span className="text-[#00FF41]" style={{ textShadow: '0 0 20px rgba(0,255,65,0.5)' }}>
              Una sola plataforma.
            </span>
          </h2>
          <p className="text-[10px] text-[#00FF41]/35 tracking-[0.3em] uppercase">
            El camino al top 1% — por disciplina, no por azar.
          </p>
        </motion.div>

        {/* ── Mapa del Ecosistema ──────────────────────────────────────────────── */}
        <motion.div
          initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.05 }}
          className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-8"
        >
          {FORMATIONS.map((f, i) => (
            <motion.div
              key={f.code}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.08 + i * 0.06, duration: 0.25 }}
              className="relative overflow-hidden p-4"
              style={{
                border:     `1px solid ${f.color}${f.locked ? '18' : '35'}`,
                background: `${f.color}${f.locked ? '03' : '05'}`,
                opacity:    f.locked ? 0.72 : 1,
              }}
            >
              {/* Pulso superior */}
              {!f.locked && (
                <motion.div
                  className="absolute top-0 left-0 right-0 h-px"
                  style={{ background: `linear-gradient(90deg,transparent,${f.color}55,transparent)` }}
                  animate={{ opacity: [0.3, 0.9, 0.3] }}
                  transition={{ duration: 2.5, repeat: Infinity }}
                />
              )}

              <div className="flex items-start justify-between gap-3 mb-2">
                <div className="flex items-center gap-2 min-w-0">
                  <span className="text-xs shrink-0" style={{ color: f.color }}>{f.icon}</span>
                  <div className="min-w-0">
                    <p className="text-[9px] font-black tracking-[0.3em] uppercase truncate" style={{ color: f.color }}>
                      {f.name}
                    </p>
                    <p className="text-[8px] tracking-wide" style={{ color: `${f.color}55` }}>{f.sub}</p>
                  </div>
                </div>
                <div className="flex items-center gap-1 shrink-0">
                  {!f.locked ? (
                    <>
                      <motion.span
                        className="w-1.5 h-1.5 rounded-full"
                        style={{ background: f.color }}
                        animate={{ opacity: [1, 0.3, 1], scale: [1, 1.3, 1] }}
                        transition={{ duration: 1.6, repeat: Infinity }}
                      />
                      <span className="text-[7px] tracking-widest" style={{ color: `${f.color}77` }}>ACTIVA</span>
                    </>
                  ) : (
                    <span className="text-[8px]" style={{ filter: `drop-shadow(0 0 3px ${f.color}55)` }}>🔒</span>
                  )}
                </div>
              </div>

              <p className="text-[9px] leading-relaxed" style={{ color: `${f.color}${f.locked ? '40' : '55'}` }}>
                {f.desc}
              </p>

              {!f.locked && (
                <div
                  className="inline-flex items-center gap-1 px-2 py-0.5 mt-2"
                  style={{ border: `1px solid ${f.color}30`, background: `${f.color}08` }}
                >
                  <span className="text-[7px] tracking-[0.35em] font-bold" style={{ color: `${f.color}80` }}>
                    DISPONIBLE AHORA
                  </span>
                </div>
              )}
            </motion.div>
          ))}
        </motion.div>

        {/* ── Por qué fallan los demás ─────────────────────────────────────────── */}
        <motion.div
          initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.2 }}
          className="mb-8"
        >
          <p className="text-[8px] tracking-[0.5em] text-[#FF0033]/35 uppercase mb-4">
            {'// EL PROBLEMA QUE NINGÚN CURSO ADMITE'}
          </p>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
            {PROBLEMS.map(({ icon, label, verdict, color }, i) => (
              <div
                key={label}
                className="p-3 text-center border"
                style={{
                  borderColor: `${color}${i === 3 ? '40' : '12'}`,
                  background:  `${color}${i === 3 ? '06' : '02'}`,
                }}
              >
                <span className="text-xl block mb-1.5" style={{ color: `${color}${i === 3 ? 'cc' : '25'}` }}>{icon}</span>
                <p className="text-[8px] font-black tracking-[0.25em] uppercase mb-1" style={{ color: `${color}${i === 3 ? '90' : '40'}` }}>
                  {label}
                </p>
                <p className="text-[7px] tracking-wide leading-4" style={{ color: `${color}${i === 3 ? '60' : '30'}` }}>
                  {verdict}
                </p>
              </div>
            ))}
          </div>
        </motion.div>

        {/* ── Protocolo D·A·K·I ────────────────────────────────────────────────── */}
        <motion.div
          initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.25 }}
          className="mb-8"
        >
          <p className="text-[8px] tracking-[0.5em] text-[#00FF41]/20 uppercase mb-4">
            {'// PROTOCOLO D·A·K·I — CÓMO FUNCIONA EL SISTEMA'}
          </p>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {DAKI_PROTOCOL.map(({ letter, word, desc, color }) => (
              <div
                key={letter}
                className="border p-4 transition-all duration-200 group"
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
                <span
                  className="text-4xl font-black leading-none block mb-2"
                  style={{ color, textShadow: `0 0 20px ${color}40` }}
                >
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

        {/* ── CTA final de sección ─────────────────────────────────────────────── */}
        <motion.div
          initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.3 }}
          className="text-center py-6 border border-[#00FF41]/10"
          style={{ background: 'rgba(0,255,65,0.02)' }}
        >
          <p className="text-[9px] tracking-[0.4em] text-[#00FF41]/35 uppercase mb-3">
            Todo esto está esperándote. Sin tarjeta de crédito.
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
