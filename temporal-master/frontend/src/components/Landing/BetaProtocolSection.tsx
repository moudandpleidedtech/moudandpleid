'use client'

/**
 * BetaProtocolSection + Footer fusionados — Slide 10 sin scroll
 * Dicotomía final · CTA · footer compacto todo en una pantalla
 */

import Link from 'next/link'
import { motion } from 'framer-motion'

export default function BetaProtocolSection() {
  return (
    <section className="bg-[#020202] font-mono min-h-screen flex flex-col relative overflow-hidden">

      {/* Vignette */}
      <div
        className="absolute inset-0 pointer-events-none"
        style={{ background: 'radial-gradient(ellipse at center,transparent 45%,rgba(2,2,2,0.7) 100%)' }}
      />

      {/* Scanlines muy sutiles */}
      <div
        className="absolute inset-0 pointer-events-none opacity-[0.025]"
        style={{ backgroundImage: 'repeating-linear-gradient(0deg,transparent,transparent 3px,#00FF41 3px,#00FF41 4px)' }}
      />

      {/* Contenido principal — centrado verticalmente */}
      <div className="flex-1 flex flex-col items-center justify-center px-6 md:px-12 py-12 relative z-10">

        <div className="max-w-2xl w-full text-center">

          <motion.p
            className="text-[#00FF41]/22 text-[9px] tracking-[0.7em] uppercase mb-10"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6 }}
          >
            {'// PROTOCOLO DE ACCESO — DECISIÓN FINAL'}
          </motion.p>

          <motion.h2
            className="text-3xl sm:text-4xl md:text-5xl font-bold tracking-[0.05em] uppercase leading-tight mb-4 text-white"
            style={{ textShadow: '0 0 80px rgba(0,255,65,0.06)' }}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.15 }}
          >
            ¿VAS A{' '}
            <span className="text-white/25">OBSERVAR</span>
            {' '}EL SISTEMA,
          </motion.h2>

          <motion.h2
            className="text-3xl sm:text-4xl md:text-5xl font-bold tracking-[0.05em] uppercase leading-tight mb-12"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.28 }}
          >
            O VAS A{' '}
            <span
              className="text-[#00FF41]"
              style={{ textShadow: '0 0 32px rgba(0,255,65,0.6), 0 0 64px rgba(0,255,65,0.2)' }}
            >
              CONSTRUIRLO?
            </span>
          </motion.h2>

          <motion.div
            className="flex flex-col items-center gap-3"
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.42 }}
          >
            <Link
              href="/register"
              className="cta-primary-btn block border border-[#00FF41]/25 bg-[#00FF41]/[0.06] text-[#00FF41] text-xs tracking-[0.45em] uppercase px-12 py-5 w-full sm:w-auto hover:bg-[#00FF41]/10 transition-colors duration-200"
            >
              {`[[ OBTENER LICENCIA DE FUNDADOR ]]`}
            </Link>

            <Link
              href="/register"
              className="text-[#00FF41]/20 text-[10px] tracking-[0.35em] uppercase hover:text-[#00FF41]/50 transition-colors duration-200"
            >
              {'[ Entrar al Nexo gratis → ]'}
            </Link>

            <p className="text-white/10 text-[9px] tracking-[0.3em] mt-2">
              Sin tarjeta de crédito · Sin subscripciones · Acceso inmediato
            </p>
          </motion.div>

        </div>
      </div>

      {/* Footer compacto integrado */}
      <footer className="relative z-10 border-t border-white/[0.04] px-6 md:px-12 py-5">
        <div className="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">

          <div className="flex items-center gap-6">
            <p className="text-[#00FF41] text-xs font-bold tracking-[0.4em] uppercase" style={{ textShadow: '0 0 8px rgba(0,255,65,0.35)' }}>
              DAKIedtech
            </p>
            <p className="text-[#00FF41]/15 text-[9px] tracking-[0.25em] hidden sm:block">
              Aprende Python como un Operador.
            </p>
          </div>

          <div className="flex items-center gap-6">
            {[
              { label: 'Login',      href: '/login'      },
              { label: 'Registro',   href: '/register'   },
              { label: 'Privacidad', href: '/privacidad' },
              { label: 'Términos',   href: '/terminos'   },
            ].map(({ label, href }) => (
              <Link
                key={href}
                href={href}
                className="text-[#00FF41]/18 text-[9px] tracking-[0.3em] uppercase hover:text-[#00FF41]/50 transition-colors duration-200"
              >
                {label}
              </Link>
            ))}
          </div>

          <p className="text-[#00FF41]/12 text-[9px] tracking-[0.25em]">
            © 2026 DAKIedtech
          </p>

        </div>
      </footer>

    </section>
  )
}
