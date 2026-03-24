/**
 * BetaProtocolSection.tsx — CTA comercial de cierre · DAKI EdTech
 * ───────────────────────────────────────────────────────────────
 * Sección de conversión final. Sin inline <style> — CSS en globals.css.
 */

import Link from 'next/link'

const BENEFITS = [
  '100 niveles de Python — de cero a arquitecto de sistemas reales',
  'DAKI analiza y corrige tu código en tiempo real, sin juicios',
  'Misiones con jefes finales, duelos y leaderboard global de Operadores',
  'Certificado de Operador al completar las 3 Operaciones Clasificadas',
] as const

export default function BetaProtocolSection() {
  return (
    <section className="bg-[#060606] font-mono px-6 md:px-12 py-24 md:py-32 relative overflow-hidden">

      {/* Grid táctica de fondo */}
      <div
        className="absolute inset-0 pointer-events-none opacity-[0.025]"
        style={{
          backgroundImage: 'linear-gradient(#00FF41 1px,transparent 1px),linear-gradient(90deg,#00FF41 1px,transparent 1px)',
          backgroundSize: '48px 48px',
        }}
      />

      {/* Vignette */}
      <div
        className="absolute inset-0 pointer-events-none"
        style={{ background: 'radial-gradient(ellipse at center, transparent 40%, rgba(6,6,6,0.85) 100%)' }}
      />

      <div className="max-w-2xl mx-auto text-center relative z-10">

        {/* Pre-label */}
        <p className="text-[#00FF41]/35 text-[10px] tracking-[0.7em] uppercase mb-10">
          {'// ACCESO AL NEXO — BETA ABIERTA'}
        </p>

        {/* Headline */}
        <h2
          className="text-4xl sm:text-5xl md:text-[3.5rem] font-bold tracking-[0.06em] uppercase text-white leading-none mb-3"
          style={{ textShadow: '0 0 80px rgba(0,255,65,0.10)' }}
        >
          DOMINA PYTHON.
          <br />
          <span
            className="text-[#00FF41]"
            style={{ textShadow: '0 0 32px rgba(0,255,65,0.55), 0 0 64px rgba(0,255,65,0.2)' }}
          >
            CONSTRUYE SISTEMAS.
          </span>
        </h2>
        <p className="text-white/20 text-[10px] tracking-[0.45em] uppercase mb-4">
          {'// el lenguaje de la IA · la nube · y los sistemas reales'}
        </p>

        {/* Divisor */}
        <div className="flex items-center justify-center gap-4 my-10">
          <div className="h-px flex-1 max-w-[80px] bg-gradient-to-r from-transparent to-[#00FF41]/25" />
          <span className="text-[#00FF41]/25 text-xs">{'◆'}</span>
          <div className="h-px flex-1 max-w-[80px] bg-gradient-to-l from-transparent to-[#00FF41]/25" />
        </div>

        {/* Benefits */}
        <ul className="text-left space-y-4 mb-10">
          {BENEFITS.map((benefit, i) => (
            <li key={i} className="flex items-start gap-3">
              <span
                className="text-[#00FF41] font-bold text-sm mt-0.5 shrink-0"
                style={{ textShadow: '0 0 8px rgba(0,255,65,0.6)' }}
              >
                ✓
              </span>
              <span className="text-[#C0C0C0]/75 text-sm leading-6 tracking-wide">
                {benefit}
              </span>
            </li>
          ))}
        </ul>

        {/* Founder license highlight */}
        <div className="border border-[#FFB800]/20 bg-[#FFB800]/[0.04] px-6 py-4 mb-10">
          <p className="text-[#FFB800]/80 text-[11px] tracking-[0.3em] uppercase leading-5">
            ⚡{'  '}Licencia de Fundador gratuita para los primeros Operadores de la Beta
          </p>
        </div>

        {/* CTA Primario */}
        <Link
          href="/register"
          className="cta-primary-btn block sm:inline-block border border-[#00FF41]/25 bg-[#00FF41]/[0.06] text-[#00FF41] text-xs tracking-[0.4em] uppercase px-12 py-5 mb-5 w-full sm:w-auto"
        >
          {`[[ CREAR CUENTA — ES GRATIS ]]`}
        </Link>

        {/* CTA Secundario */}
        <div className="mb-10">
          <Link
            href="/login"
            className="text-[#00FF41]/20 text-[10px] tracking-[0.35em] uppercase hover:text-[#00FF41]/50 transition-colors duration-200"
          >
            {'[ Ya tengo cuenta → Iniciar sesión ]'}
          </Link>
        </div>

        {/* Trust signals */}
        <div className="flex flex-wrap justify-center gap-x-6 gap-y-1">
          {['Sin tarjeta de crédito', 'Sin subscripciones', 'Acceso inmediato'].map((t) => (
            <span key={t} className="text-[#00FF41]/12 text-[10px] tracking-[0.25em]">
              {t}
            </span>
          ))}
        </div>

      </div>
    </section>
  )
}
