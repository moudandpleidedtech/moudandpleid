/**
 * BetaProtocolSection.tsx — Final CTA · Protocolo de Acceso · DAKI EdTech
 * ──────────────────────────────────────────────────────────────────────────
 * Última oportunidad de conversión. Negro puro, sin grilla, sin distracciones.
 * Contraste máximo con el resto de la página — solo la decisión importa.
 * Gatillo mental: Dicotomía de identidad.
 * Sin inline <style> — CSS en globals.css.
 */

import Link from 'next/link'

export default function BetaProtocolSection() {
  return (
    <section className="bg-[#020202] font-mono px-6 md:px-12 py-32 md:py-40 relative">

      {/* Vignette mínima */}
      <div
        className="absolute inset-0 pointer-events-none"
        style={{ background: 'radial-gradient(ellipse at center,transparent 50%,rgba(2,2,2,0.6) 100%)' }}
      />

      <div className="max-w-2xl mx-auto text-center relative z-10">

        {/* Pre-label */}
        <p className="text-[#00FF41]/25 text-[10px] tracking-[0.7em] uppercase mb-12">
          {'// PROTOCOLO DE ACCESO — DECISIÓN FINAL'}
        </p>

        {/* Dicotomía */}
        <h2
          className="text-3xl sm:text-4xl md:text-5xl font-bold tracking-[0.06em] uppercase leading-tight mb-16 text-white"
          style={{ textShadow: '0 0 80px rgba(0,255,65,0.06)' }}
        >
          ¿VAS A
          {' '}
          <span className="text-white/30">OBSERVAR</span>
          {' '}
          EL SISTEMA,
          <br />
          O VAS A
          {' '}
          <span
            className="text-[#00FF41]"
            style={{ textShadow: '0 0 32px rgba(0,255,65,0.55), 0 0 64px rgba(0,255,65,0.2)' }}
          >
            CONSTRUIRLO?
          </span>
        </h2>

        {/* CTAs */}
        <div className="flex flex-col items-center gap-4">
          <Link
            href="/register"
            className="cta-primary-btn block border border-[#00FF41]/25 bg-[#00FF41]/[0.06] text-[#00FF41] text-xs tracking-[0.45em] uppercase px-12 py-5 w-full sm:w-auto"
          >
            {`[[ OBTENER LICENCIA DE FUNDADOR ]]`}
          </Link>

          <Link
            href="/register"
            className="text-[#00FF41]/18 text-[10px] tracking-[0.35em] uppercase hover:text-[#00FF41]/45 transition-colors duration-200"
          >
            {'[ Entrar al Nexo gratis → ]'}
          </Link>
        </div>

        {/* Trust */}
        <p className="mt-10 text-white/08 text-[9px] tracking-[0.3em]">
          Sin tarjeta de crédito · Sin subscripciones · Acceso inmediato
        </p>

      </div>
    </section>
  )
}
