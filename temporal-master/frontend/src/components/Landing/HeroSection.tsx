'use client'

/**
 * HeroSection.tsx — Landing Page · DAKI EdTech
 * ─────────────────────────────────────────────
 * Design system: fondo #0A0A0A · verde #00FF41 · rojo #FF0033 · font-mono
 * Efectos: CRT scanlines · vignette · glitch en título · pulse en botón CTA
 */

import Link from 'next/link'

export default function HeroSection() {

  return (
    <section className="min-h-screen bg-[#0A0A0A] font-mono text-[#00FF41] flex flex-col relative overflow-hidden">

      {/* ── Keyframes inline ─────────────────────────────────────────────────── */}
      <style>{`
        @keyframes btn-pulse {
          0%, 100% {
            box-shadow: 0 0 8px rgba(0,255,65,0.3), 0 0 20px rgba(0,255,65,0.1);
            border-color: rgba(0,255,65,0.5);
          }
          50% {
            box-shadow: 0 0 24px rgba(0,255,65,0.7), 0 0 48px rgba(0,255,65,0.3), 0 0 80px rgba(0,255,65,0.12);
            border-color: #00FF41;
          }
        }
        @keyframes title-flicker {
          0%, 96%, 100% { opacity: 1; }
          97%           { opacity: 0.85; }
          98%           { opacity: 1; }
          99%           { opacity: 0.7; }
        }
        @keyframes scanline-drift {
          0%   { transform: translateY(0); }
          100% { transform: translateY(4px); }
        }
        .hero-btn-pulse {
          animation: btn-pulse 2.4s ease-in-out infinite;
        }
        .hero-btn-pulse:hover {
          animation: none;
          box-shadow: 0 0 32px rgba(0,255,65,0.8), 0 0 64px rgba(0,255,65,0.4);
          border-color: #00FF41;
          background-color: rgba(0,255,65,0.12);
        }
        .hero-title {
          animation: title-flicker 8s ease-in-out infinite;
        }
      `}</style>

      {/* ── CRT scanlines ────────────────────────────────────────────────────── */}
      <div
        className="fixed inset-0 pointer-events-none z-10"
        style={{
          backgroundImage:
            'repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,0.07) 2px,rgba(0,0,0,0.07) 4px)',
        }}
      />

      {/* ── Vignette ─────────────────────────────────────────────────────────── */}
      <div
        className="fixed inset-0 pointer-events-none z-10"
        style={{
          background: 'radial-gradient(ellipse at center,transparent 50%,rgba(0,0,0,0.75) 100%)',
        }}
      />

      {/* ── Ruido de fondo (grid táctica) ────────────────────────────────────── */}
      <div
        className="fixed inset-0 pointer-events-none z-0 opacity-[0.03]"
        style={{
          backgroundImage:
            'linear-gradient(#00FF41 1px,transparent 1px),linear-gradient(90deg,#00FF41 1px,transparent 1px)',
          backgroundSize: '48px 48px',
        }}
      />

      {/* ── Header ───────────────────────────────────────────────────────────── */}
      <header className="relative z-20 flex items-center justify-between px-6 md:px-12 py-6 border-b border-[#00FF41]/10">

        {/* Logo */}
        <div className="flex items-center gap-3">
          <span className="text-[#FF0033] text-xs tracking-[0.3em] opacity-60 hidden sm:block">
            {'//'}
          </span>
          <span className="text-[#00FF41] text-sm md:text-base font-bold tracking-[0.35em] uppercase neon-glow">
            DAKIedtech
          </span>
        </div>

        {/* Status badge */}
        <div className="flex items-center gap-2 border border-[#00FF41]/30 px-3 py-1.5 bg-[#00FF41]/5">
          <span className="w-1.5 h-1.5 rounded-full bg-[#00FF41] animate-pulse" />
          <span className="text-[#00FF41] text-xs tracking-[0.3em] uppercase">
            STATUS: OPERATIVO
          </span>
        </div>
      </header>

      {/* ── Hero content ─────────────────────────────────────────────────────── */}
      <div className="relative z-20 flex-1 flex items-center justify-center px-6 md:px-12 py-16 md:py-0">
        <div className="w-full max-w-4xl">

          {/* Pre-label */}
          <div className="flex items-center gap-4 mb-8">
            <div className="h-px flex-1 bg-gradient-to-r from-transparent to-[#FF0033]/40 max-w-[60px]" />
            <span className="text-[#FF0033]/70 text-xs tracking-[0.5em] uppercase">
              SISTEMA — NEXO CENTRAL — v4.2
            </span>
          </div>

          {/* Título principal */}
          <h1 className="hero-title text-4xl sm:text-5xl md:text-7xl font-bold tracking-[0.08em] uppercase leading-none mb-4 text-[#00FF41]">
            EL SISTEMA
            <br />
            <span className="text-[#FF0033]" style={{ textShadow: '0 0 20px rgba(255,0,51,0.5)' }}>
              TIENE FALLOS.
            </span>
          </h1>

          {/* Subtítulo */}
          <h2 className="text-xl sm:text-2xl md:text-4xl font-bold tracking-[0.15em] uppercase mb-10 text-[#00FF41]/90 neon-glow">
            TÚ ERES LA CORRECCIÓN.
          </h2>

          {/* Separador */}
          <div className="flex items-center gap-4 mb-10">
            <div className="h-px bg-[#00FF41]/20 flex-1 max-w-xs" />
            <span className="text-[#00FF41]/30 text-xs">{'◆'}</span>
          </div>

          {/* Descripción */}
          <p className="text-sm md:text-base text-[#00FF41]/60 leading-7 tracking-wide max-w-2xl mb-12">
            <span className="text-[#00FF41]/90 font-bold">DAKIedtech:</span>
            {' '}No somos un curso. Somos tu entorno de despliegue.
            Entrena con una IA que analiza tu código, desafía tu lógica
            y te otorga el sello de calidad definitivo.
          </p>

          {/* CTA Button */}
          <div className="flex flex-col items-start gap-4">
            <Link
              href="/login"
              className="hero-btn-pulse inline-block border border-[#00FF41]/50 bg-[#00FF41]/5 text-[#00FF41] text-xs md:text-sm tracking-[0.35em] uppercase px-8 py-4 transition-colors duration-150 w-full sm:w-auto text-center"
            >
              {`[[ INICIAR SECUENCIA DE ACCESO ]]`}
            </Link>

            {/* Micro-copy */}
            <p className="text-[#00FF41]/30 text-xs tracking-[0.2em]">
              {'[ Beta Testers: Ingresen su código de operador en el siguiente paso ]'}
            </p>
          </div>

          {/* Footer de sección */}
          <div className="mt-20 pt-6 border-t border-[#00FF41]/8 flex flex-col sm:flex-row items-start sm:items-center gap-4 sm:gap-8">
            {[
              { valor: '100', label: 'NIVELES' },
              { valor: 'IA', label: 'INSTRUCTORA' },
              { valor: '∞', label: 'DESAFÍOS' },
            ].map(({ valor, label }) => (
              <div key={label} className="flex items-center gap-3">
                <span className="text-lg font-bold text-[#00FF41] neon-glow">{valor}</span>
                <span className="text-[10px] tracking-[0.4em] text-[#00FF41]/40 uppercase">{label}</span>
              </div>
            ))}
          </div>

        </div>
      </div>

      {/* ── Línea inferior de estado ──────────────────────────────────────────── */}
      <footer className="relative z-20 px-6 md:px-12 py-4 border-t border-[#00FF41]/8 flex items-center justify-between">
        <span className="text-[#00FF41]/20 text-xs tracking-[0.4em]">
          {'DAKI EdTech // CANAL SEGURO // CIFRADO AES-256'}
        </span>
        <span className="text-[#FF0033]/30 text-xs tracking-[0.3em] hidden md:block">
          {'[ ACCESO RESTRINGIDO — SOLO OPERADORES AUTORIZADOS ]'}
        </span>
      </footer>

    </section>
  )
}
