'use client'

/**
 * ActivacionSection — Slide 4 del Landing · Cierre de conversión
 *
 * Estructura: hook de identidad → tabla de precios → CTA dual (gratis / fundador).
 * El precio $97 con ancla $197 aparece aquí, antes del registro, para eliminar
 * la sorpresa del paywall y pre-calificar al visitante.
 */

import Link from 'next/link'
import { motion } from 'framer-motion'

// ─── Data ─────────────────────────────────────────────────────────────────────

const EXPLORER_FEATURES = [
  { text: 'Misiones 1 – 10 de 195',       included: true  },
  { text: 'IA DAKI · 20 consultas/día',    included: true  },
  { text: 'Leaderboard de Operadores',     included: true  },
  { text: 'Misiones Clasificadas',         included: false },
  { text: 'Certificación de Operador',     included: false },
  { text: 'Acceso de por vida',            included: false },
]

const FOUNDER_FEATURES = [
  '195 misiones · Python Core completo',
  'IA DAKI · sin límites',
  'Misiones Clasificadas',
  'Leaderboard + Insignias de Rango',
  'Certificación de Operador',
  'Acceso de por vida · precio de lanzamiento',
]

const VERIFIABLE = [
  { label: 'XP por área demostrable',               detail: 'OOP · Algoritmos · APIs · Estructuras de Datos' },
  { label: 'Rango en leaderboard nacional',          detail: 'Posición actualizada en tiempo real' },
  { label: 'Bitácora pública de errores → soluciones', detail: 'Evidencia técnica real, no presentaciones' },
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
          className="mb-6"
        >
          <p className="text-[8px] tracking-[0.6em] text-[#FF0033]/40 uppercase mb-3">
            {'// PROTOCOLO DE ACTIVACIÓN — PASO FINAL'}
          </p>

          <div
            className="relative p-5 border-l-2"
            style={{ borderColor: '#FF0033', background: 'rgba(255,0,51,0.025)' }}
          >
            <p className="text-base font-black tracking-[0.04em] text-white/80 uppercase leading-snug mb-1">
              El mercado no contrata certificados.
            </p>
            <p className="text-base font-black tracking-[0.04em] uppercase leading-snug">
              <span className="text-[#FF0033]">Contrata</span>{' '}
              <span className="text-white/80">operadores que construyen.</span>
            </p>
          </div>
        </motion.div>

        {/* ── Tabla de precios ────────────────────────────────────────────────── */}
        <motion.div
          initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.07 }}
          className="mb-6"
        >
          <p className="text-[8px] tracking-[0.5em] text-[#00FF41]/25 uppercase mb-3">
            {'// SELECCIONÁ TU PROTOCOLO DE ACCESO'}
          </p>

          <div className="grid grid-cols-2 gap-3">

            {/* Exploración — gratis */}
            <div className="border border-white/[0.06] bg-[#0A0A0A] p-4 flex flex-col opacity-70">
              <p className="text-white/30 text-[9px] tracking-[0.4em] uppercase mb-1 font-bold">
                EXPLORACIÓN
              </p>
              <p className="text-white/25 text-[9px] tracking-[0.25em] uppercase mb-3">
                Prueba de Lógica
              </p>
              <p className="text-white/30 text-2xl font-bold mb-4">
                GRATIS
              </p>
              <ul className="space-y-2 flex-1">
                {EXPLORER_FEATURES.map((f, i) => (
                  <li key={i} className="flex items-center gap-2">
                    <span className={`text-[10px] font-bold shrink-0 ${f.included ? 'text-white/35' : 'text-white/12'}`}>
                      {f.included ? '✓' : '—'}
                    </span>
                    <span className={`text-[9px] leading-4 ${f.included ? 'text-white/40' : 'text-white/15 line-through decoration-white/10'}`}>
                      {f.text}
                    </span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Fundador — $97 */}
            <div
              className="border bg-[#0A0A0A] p-4 flex flex-col relative"
              style={{ borderColor: 'rgba(0,255,65,0.30)', background: 'rgba(0,255,65,0.03)' }}
            >
              {/* Badge escasez */}
              <div className="absolute -top-2.5 left-1/2 -translate-x-1/2 bg-[#00FF41] px-3 py-0.5 whitespace-nowrap">
                <span className="text-[#0A0A0A] text-[7px] tracking-[0.35em] uppercase font-bold">
                  ⚡ CUPOS BETA
                </span>
              </div>

              <p
                className="text-[#00FF41] text-[9px] tracking-[0.4em] uppercase mb-1 font-bold mt-1"
                style={{ textShadow: '0 0 8px rgba(0,255,65,0.4)' }}
              >
                LICENCIA FUNDADOR
              </p>
              <p className="text-white/30 text-[9px] tracking-[0.25em] uppercase mb-2">
                Experiencia Completa
              </p>

              {/* Precio con ancla */}
              <div className="mb-4">
                <span className="text-white/20 text-xs line-through mr-2">$197</span>
                <span
                  className="text-[#00FF41] text-2xl font-bold"
                  style={{ textShadow: '0 0 16px rgba(0,255,65,0.5)' }}
                >
                  $97
                </span>
                <span className="text-white/30 text-[9px] ml-1 tracking-wide">USD</span>
                <p className="text-[#00FF41]/35 text-[8px] tracking-[0.3em] uppercase mt-0.5">
                  pago único · de por vida
                </p>
              </div>

              <ul className="space-y-2 flex-1">
                {FOUNDER_FEATURES.map((f, i) => (
                  <li key={i} className="flex items-center gap-2">
                    <span
                      className="text-[10px] font-bold shrink-0 text-[#00FF41]"
                      style={{ textShadow: '0 0 6px rgba(0,255,65,0.5)' }}
                    >
                      ✓
                    </span>
                    <span className="text-[9px] leading-4 text-[#C0C0C0]/70">{f}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* Comparativa de contexto */}
          <div
            className="mt-3 px-4 py-2.5 border flex flex-col sm:flex-row sm:items-center gap-1 sm:gap-4"
            style={{ borderColor: 'rgba(0,255,65,0.08)', background: 'rgba(0,255,65,0.02)' }}
          >
            <span className="text-[#00FF41]/30 text-[8px] tracking-[0.3em] uppercase shrink-0">{'// VS'}</span>
            <div className="flex flex-wrap gap-x-5 gap-y-1">
              {[
                'Platzi / Coursera: $99/año indefinidamente',
                'Bootcamp: $3.000+ USD',
                'DAKI Fundador: $97 una sola vez',
              ].map((text, i) => (
                <span
                  key={i}
                  className={`text-[8px] tracking-wide ${i === 2 ? 'text-[#00FF41]/60 font-bold' : 'text-white/18'}`}
                >
                  {text}
                </span>
              ))}
            </div>
          </div>
        </motion.div>

        {/* ── Progreso verificable (compacto) ─────────────────────────────────── */}
        <motion.div
          initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.12 }}
          className="mb-6"
        >
          <div
            className="relative px-4 py-3 border overflow-hidden"
            style={{ borderColor: 'rgba(6,182,212,0.18)', background: 'rgba(6,182,212,0.025)' }}
          >
            <motion.div
              className="absolute top-0 left-0 right-0 h-px"
              style={{ background: 'linear-gradient(90deg,transparent,rgba(6,182,212,0.45),transparent)' }}
              animate={{ opacity: [0.2, 0.8, 0.2] }}
              transition={{ duration: 2.8, repeat: Infinity }}
            />
            <p className="text-[7px] tracking-[0.5em] mb-2" style={{ color: 'rgba(6,182,212,0.40)' }}>
              {'// TU PROGRESO ES VERIFICABLE — NO SOLO UN NÚMERO'}
            </p>
            <div className="flex flex-wrap gap-x-5 gap-y-1">
              {VERIFIABLE.map(({ label, detail }) => (
                <div key={label} className="flex items-start gap-1.5">
                  <span className="text-[9px] shrink-0 mt-0.5" style={{ color: 'rgba(6,182,212,0.60)' }}>▸</span>
                  <div>
                    <p className="text-[8px] font-black tracking-[0.1em]" style={{ color: 'rgba(6,182,212,0.70)' }}>{label}</p>
                    <p className="text-[7px] tracking-wide" style={{ color: 'rgba(6,182,212,0.30)' }}>{detail}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </motion.div>

        {/* ── CTA dual ────────────────────────────────────────────────────────── */}
        <motion.div
          initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.16 }}
          className="relative py-6 text-center border border-[#00FF41]/12 mb-6"
          style={{ background: 'rgba(0,255,65,0.015)' }}
        >
          <motion.div
            className="absolute top-0 left-0 right-0 h-px"
            style={{ background: 'linear-gradient(90deg,transparent,rgba(0,255,65,0.4),transparent)' }}
            animate={{ opacity: [0.3, 1, 0.3] }}
            transition={{ duration: 2.5, repeat: Infinity }}
          />

          <p className="text-lg sm:text-xl font-black tracking-[0.04em] uppercase text-white/85 mb-1">
            ¿VAS A SEGUIR MIRANDO
          </p>
          <p className="text-lg sm:text-xl font-black tracking-[0.04em] uppercase mb-5">
            O{' '}
            <span
              className="text-[#00FF41]"
              style={{ textShadow: '0 0 24px rgba(0,255,65,0.55), 0 0 48px rgba(0,255,65,0.2)' }}
            >
              VAS A ENTRAR?
            </span>
          </p>

          <div className="flex flex-col items-center gap-3">
            {/* Primario — vitalicia */}
            <Link
              href="https://pay.hotmart.com/T105398516G"
              target="_blank"
              rel="noopener noreferrer"
              className="group inline-block border text-[10px] tracking-[0.45em] uppercase px-10 py-4 transition-all duration-200 w-full sm:w-auto"
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
              {'[[ OBTENER LICENCIA FUNDADOR — $97 ]]'}
            </Link>

            {/* Secundario — mensual */}
            <Link
              href="https://go.hotmart.com/K105401308T"
              target="_blank"
              rel="noopener noreferrer"
              className="text-[#00FF41]/40 text-[9px] tracking-[0.3em] uppercase hover:text-[#00FF41]/75 transition-colors duration-200"
            >
              {'[ Preferís suscripción mensual → ]'}
            </Link>

            {/* Terciario — gratis */}
            <Link
              href="/register"
              className="text-white/18 text-[8px] tracking-[0.25em] uppercase hover:text-white/40 transition-colors duration-200"
            >
              {'[ Explorar gratis sin tarjeta ]'}
            </Link>

            <p className="text-white/12 text-[8px] tracking-[0.3em] mt-1">
              $97 · pago único · este precio desaparece al cerrar la beta
            </p>
          </div>

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
