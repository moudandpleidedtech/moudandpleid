'use client'

/**
 * ActivacionSection — Slide 4 del Landing · Cierre de conversión
 *
 * Propuesta: El mercado no contrata certificados. Contrata operadores.
 * Diferenciador: experiencia Python real + verificable + gamificada.
 */

import Link from 'next/link'
import { motion } from 'framer-motion'

// ─── Data ─────────────────────────────────────────────────────────────────────

const FREE_ACCESS = [
  {
    icon: '⬡',
    label: 'Python Core — 190 misiones',
    detail: 'De variables a sistemas en producción. Sin atajos. Sin relleno.',
  },
  {
    icon: '◈',
    label: 'IA adaptativa DAKI',
    detail: 'Ajusta la dificultad a tus errores — no al promedio del grupo.',
  },
  {
    icon: '◎',
    label: 'Boss Fights de integración',
    detail: 'Al final de cada sector: pruebas reales que obligan a integrar todo lo aprendido.',
  },
  {
    icon: '⬟',
    label: 'Leaderboard de Operadores',
    detail: 'Tu rango verificable frente al resto del Nexo en tiempo real.',
  },
  {
    icon: '◆',
    label: 'Bitácora táctica',
    detail: 'Tu historial de errores y cómo los resolviste — evidencia técnica real.',
  },
]

const VERIFIABLE = [
  { label: 'XP por área demostrable',                          detail: '(OOP, Algoritmos, APIs, Estructuras de Datos)' },
  { label: 'Rango en el leaderboard nacional',                  detail: 'Posición actualizada en tiempo real' },
  { label: 'Sectores completados con código que funciona',       detail: 'No presentaciones — misiones con output real' },
  { label: 'Bitácora pública de errores → soluciones',          detail: 'La diferencia entre alguien que aprendió y alguien que lo dice' },
]

const FOOTER_LINKS = [
  { label: 'Login',      href: '/login'      },
  { label: 'Registro',   href: '/register'   },
  { label: 'Privacidad', href: '/privacidad' },
  { label: 'Términos',   href: '/terminos'   },
]

// ─── Componente ───────────────────────────────────────────────────────────────

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
            <p className="text-base sm:text-lg font-black tracking-[0.04em] text-white/80 uppercase leading-snug mb-2">
              El mercado no contrata certificados.
            </p>
            <p className="text-base sm:text-lg font-black tracking-[0.04em] uppercase leading-snug">
              <span className="text-[#FF0033]">Contrata</span>{' '}
              <span className="text-white/80">operadores que construyen.</span>
            </p>
            <p className="text-[10px] text-[#00FF41]/40 tracking-[0.25em] mt-3 uppercase">
              DAKI no te enseña a completar ejercicios. Te forja hasta que construís sin red de contención.
            </p>
          </div>
        </motion.div>

        {/* ── Acceso inmediato ─────────────────────────────────────────────────── */}
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
                transition={{ delay: 0.10 + i * 0.05, duration: 0.20 }}
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
                  <span className="text-[10px] font-black tracking-[0.2em] text-[#00FF41]/80 uppercase">
                    {icon} {label}
                  </span>
                  <p className="text-[9px] text-[#00FF41]/40 tracking-wide mt-0.5">{detail}</p>
                </div>
              </motion.div>
            ))}
          </div>

          {/* Tu progreso es verificable */}
          <div
            className="relative px-4 py-4 border overflow-hidden"
            style={{ borderColor: 'rgba(6,182,212,0.20)', background: 'rgba(6,182,212,0.03)' }}
          >
            <motion.div
              className="absolute top-0 left-0 right-0 h-px"
              style={{ background: 'linear-gradient(90deg,transparent,rgba(6,182,212,0.50),transparent)' }}
              animate={{ opacity: [0.2, 0.8, 0.2] }}
              transition={{ duration: 2.8, repeat: Infinity }}
            />
            <p className="text-[8px] tracking-[0.5em] mb-3"
              style={{ color: 'rgba(6,182,212,0.45)' }}>
              {'// TU PROGRESO ES VERIFICABLE — NO SOLO UN NÚMERO'}
            </p>
            <div className="flex flex-col gap-2">
              {VERIFIABLE.map(({ label, detail }) => (
                <div key={label} className="flex items-start gap-2">
                  <span className="text-[10px] shrink-0 mt-0.5"
                    style={{ color: 'rgba(6,182,212,0.70)' }}>▸</span>
                  <div>
                    <p className="text-[9px] font-black tracking-[0.15em]"
                      style={{ color: 'rgba(6,182,212,0.75)' }}>
                      {label}
                    </p>
                    <p className="text-[8px] tracking-wide"
                      style={{ color: 'rgba(6,182,212,0.35)' }}>
                      {detail}
                    </p>
                  </div>
                </div>
              ))}
            </div>
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
                Python. Gamificado. Verificable.
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
