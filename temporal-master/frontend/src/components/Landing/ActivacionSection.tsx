'use client'

/**
 * ActivacionSection — Slide 4 del Landing · Cierre de conversión
 *
 * Rediseño D025: de pricing page a máquina de registro.
 * Sin precios. Sin pricing cards. Un solo objetivo: crear cuenta.
 * El upsell a membresía sucede desde adentro del Hub — no aquí.
 */

import Link from 'next/link'
import { motion } from 'framer-motion'

const FREE_ACCESS = [
  { icon: '⬡', label: 'Operación Vanguardia',      detail: 'Python Core completo — los 100 niveles' },
  { icon: '◈', label: 'IA Simbionte DAKI',           detail: 'Tu instructor que nunca duerme ni te da respuestas gratis' },
  { icon: '◎', label: 'Mapa de Incursiones',         detail: 'Ves el ecosistema completo desde el primer login' },
  { icon: '⬟', label: 'Leaderboard de Operadores',   detail: 'Tu rango real vs el resto del Nexo' },
  { icon: '◆', label: 'Bitácora táctica',            detail: 'Tu historial de errores convertido en inteligencia' },
]

const WHAT_AWAITS = [
  { label: 'PROTOCOLO TPM',          color: '#FF6B35', status: 'Encriptado' },
  { label: 'PROTOCOLO ARES',         color: '#FF2D78', status: 'Clasificado' },
  { label: 'TECHNICAL SALES MASTERY', color: '#FFC700', status: 'Clasificado' },
]

const FOOTER_LINKS = [
  { label: 'Login',      href: '/login'      },
  { label: 'Registro',   href: '/register'   },
  { label: 'Privacidad', href: '/privacidad' },
  { label: 'Términos',   href: '/terminos'   },
]

export default function ActivacionSection() {
  return (
    <section className="h-full flex flex-col font-mono bg-[#020202] overflow-hidden relative">

      {/* Scanlines */}
      <div
        className="absolute inset-0 pointer-events-none opacity-[0.015]"
        style={{ backgroundImage: 'repeating-linear-gradient(0deg,transparent,transparent 3px,#00FF41 3px,#00FF41 4px)' }}
      />

      {/* Scrollable */}
      <div className="flex-1 overflow-y-auto px-6 pt-6 pb-4 min-h-0" style={{ scrollbarWidth: 'none' }}>

        {/* ── Gancho de identidad ─────────────────────────────────────────────── */}
        <motion.div
          initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
          className="mb-8"
        >
          <p className="text-[8px] tracking-[0.6em] text-[#FF0033]/40 uppercase mb-4">
            {'// PROTOCOLO DE ACTIVACIÓN — PASO FINAL'}
          </p>

          <div
            className="relative p-6 border-l-2 mb-4"
            style={{ borderColor: '#FF0033', background: 'rgba(255,0,51,0.025)' }}
          >
            <p className="text-base sm:text-lg font-black tracking-[0.05em] text-white/80 uppercase leading-snug mb-2">
              La mayoría termina el curso.
            </p>
            <p className="text-base sm:text-lg font-black tracking-[0.05em] uppercase leading-snug">
              <span className="text-[#FF0033]">Muy pocos</span>{' '}
              <span className="text-white/80">aprenden a construir sistemas.</span>
            </p>
            <p className="text-[10px] text-[#00FF41]/40 tracking-[0.25em] mt-3 uppercase">
              DAKI no te enseña a completar ejercicios. Te forja hasta que no los necesitás.
            </p>
          </div>
        </motion.div>

        {/* ── Lo que obtenés gratis ────────────────────────────────────────────── */}
        <motion.div
          initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.06 }}
          className="mb-8"
        >
          <p className="text-[8px] tracking-[0.5em] text-[#00FF41]/25 uppercase mb-4">
            {'// ACCESO INMEDIATO — SIN TARJETA DE CRÉDITO'}
          </p>

          <div className="flex flex-col gap-2 mb-5">
            {FREE_ACCESS.map(({ icon, label, detail }, i) => (
              <motion.div
                key={label}
                initial={{ opacity: 0, x: -8 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.1 + i * 0.05, duration: 0.2 }}
                className="flex items-start gap-3 px-4 py-3 border border-[#00FF41]/10 bg-[#00FF41]/[0.025] transition-all duration-150"
                onMouseEnter={e => {
                  ;(e.currentTarget as HTMLDivElement).style.borderColor = 'rgba(0,255,65,0.25)'
                  ;(e.currentTarget as HTMLDivElement).style.background   = 'rgba(0,255,65,0.05)'
                }}
                onMouseLeave={e => {
                  ;(e.currentTarget as HTMLDivElement).style.borderColor = 'rgba(0,255,65,0.10)'
                  ;(e.currentTarget as HTMLDivElement).style.background   = 'rgba(0,255,65,0.025)'
                }}
              >
                <span className="text-[#00FF41] font-black text-xs shrink-0 mt-0.5"
                  style={{ textShadow: '0 0 8px rgba(0,255,65,0.5)' }}>
                  ✓
                </span>
                <div className="min-w-0">
                  <span className="text-[10px] font-black tracking-[0.2em] text-[#00FF41]/80 uppercase">{icon} {label}</span>
                  <p className="text-[9px] text-[#00FF41]/40 tracking-wide mt-0.5">{detail}</p>
                </div>
              </motion.div>
            ))}
          </div>

          {/* Lo que te espera adentro (tease de membresía — sin precio) */}
          <div
            className="relative px-4 py-4 border border-dashed overflow-hidden"
            style={{ borderColor: 'rgba(255,255,255,0.07)', background: 'rgba(0,0,0,0.4)' }}
          >
            <div
              className="absolute inset-0 pointer-events-none"
              style={{ background: 'repeating-linear-gradient(90deg, transparent, transparent 8px, rgba(255,255,255,0.005) 8px, rgba(255,255,255,0.005) 9px)' }}
            />
            <p className="text-[8px] tracking-[0.5em] text-white/20 uppercase mb-3">
              {'// UNA VEZ DENTRO — PRÓXIMAS FORMACIONES'}
            </p>
            <div className="flex flex-col gap-2">
              {WHAT_AWAITS.map(({ label, color, status }) => (
                <div key={label} className="flex items-center justify-between gap-2">
                  <div className="flex items-center gap-2">
                    <span className="text-[10px]">🔒</span>
                    <span className="text-[9px] font-black tracking-[0.2em] uppercase" style={{ color: `${color}55` }}>
                      {label}
                    </span>
                  </div>
                  <span
                    className="text-[7px] tracking-[0.3em] px-2 py-0.5 border"
                    style={{ color: `${color}55`, borderColor: `${color}20`, background: `${color}05` }}
                  >
                    {status}
                  </span>
                </div>
              ))}
            </div>
            <p className="text-[8px] text-white/15 tracking-[0.25em] mt-3 italic">
              Los verás en el Hub. Cuando quieras acceder, sabés dónde encontrarnos.
            </p>
          </div>
        </motion.div>

        {/* ── CTA Principal ────────────────────────────────────────────────────── */}
        <motion.div
          initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.15 }}
          className="relative py-8 text-center border border-[#00FF41]/12 mb-6"
          style={{ background: 'rgba(0,255,65,0.015)' }}
        >
          {/* Línea de pulso */}
          <motion.div
            className="absolute top-0 left-0 right-0 h-px"
            style={{ background: 'linear-gradient(90deg,transparent,rgba(0,255,65,0.4),transparent)' }}
            animate={{ opacity: [0.3, 1, 0.3] }}
            transition={{ duration: 2.5, repeat: Infinity }}
          />

          <p className="text-xl sm:text-2xl font-black tracking-[0.04em] uppercase text-white/85 mb-1">
            ¿VAS A SEGUIR MIRANDO
          </p>
          <p className="text-xl sm:text-2xl font-black tracking-[0.04em] uppercase mb-5">
            O{' '}
            <span
              className="text-[#00FF41]"
              style={{ textShadow: '0 0 24px rgba(0,255,65,0.55), 0 0 48px rgba(0,255,65,0.2)' }}
            >
              VAS A ENTRAR?
            </span>
          </p>

          <div className="flex flex-col items-center gap-3">
            <Link
              href="/register"
              className="group inline-block border text-[10px] tracking-[0.45em] uppercase px-10 py-4 transition-all duration-200"
              style={{
                borderColor: 'rgba(0,255,65,0.50)',
                color:       '#00FF41',
                background:  'rgba(0,255,65,0.07)',
                boxShadow:   '0 0 20px rgba(0,255,65,0.08)',
              }}
              onMouseEnter={e => {
                const el = e.currentTarget as HTMLAnchorElement
                el.style.background  = 'rgba(0,255,65,0.14)'
                el.style.borderColor = '#00FF41'
                el.style.boxShadow   = '0 0 32px rgba(0,255,65,0.22)'
              }}
              onMouseLeave={e => {
                const el = e.currentTarget as HTMLAnchorElement
                el.style.background  = 'rgba(0,255,65,0.07)'
                el.style.borderColor = 'rgba(0,255,65,0.50)'
                el.style.boxShadow   = '0 0 20px rgba(0,255,65,0.08)'
              }}
            >
              {'[[ CREAR CREDENCIALES — ACCESO INMEDIATO ]]'}
            </Link>

            <Link
              href="/login"
              className="text-[#00FF41]/22 text-[9px] tracking-[0.35em] uppercase hover:text-[#00FF41]/50 transition-colors duration-200"
            >
              {'[ Ya tengo credenciales → Ingresar ]'}
            </Link>

            <p className="text-white/12 text-[8px] tracking-[0.3em] mt-1">
              Sin tarjeta de crédito · Sin subscripción · Sin excusas
            </p>
          </div>

          {/* Línea de pulso inferior */}
          <motion.div
            className="absolute bottom-0 left-0 right-0 h-px"
            style={{ background: 'linear-gradient(90deg,transparent,rgba(0,255,65,0.25),transparent)' }}
            animate={{ opacity: [0.2, 0.7, 0.2] }}
            transition={{ duration: 3, repeat: Infinity, delay: 1 }}
          />
        </motion.div>

        {/* ── Footer ──────────────────────────────────────────────────────────── */}
        <div className="border-t border-white/[0.04] pt-4 pb-2">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-3">
            <div className="flex items-center gap-4">
              <p
                className="text-[#00FF41] text-xs font-black tracking-[0.4em] uppercase"
                style={{ textShadow: '0 0 8px rgba(0,255,65,0.3)' }}
              >
                DAKIedtech
              </p>
              <p className="text-[#00FF41]/15 text-[9px] tracking-[0.25em] hidden sm:block">
                Entrena. Despliega. Domina el ecosistema.
              </p>
            </div>
            <div className="flex items-center gap-5">
              {FOOTER_LINKS.map(({ label, href }) => (
                <Link
                  key={href}
                  href={href}
                  className="text-[#00FF41]/18 text-[9px] tracking-[0.3em] uppercase hover:text-[#00FF41]/50 transition-colors duration-200"
                >
                  {label}
                </Link>
              ))}
            </div>
            <p className="text-[#00FF41]/12 text-[9px] tracking-[0.25em]">© 2026 DAKIedtech</p>
          </div>
        </div>

      </div>
    </section>
  )
}
