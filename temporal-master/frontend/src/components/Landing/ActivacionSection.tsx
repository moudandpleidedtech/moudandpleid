'use client'

/**
 * ActivacionSection — Slide 4 del Landing (reemplaza slides 7, 8, 9)
 *
 * Fusiona en una sola pantalla scrolleable:
 *   1. Paradigm shifts (condensado de TestimonialsSection)
 *   2. Pricing: Modo Exploración vs Licencia de Fundador
 *   3. CTA final + footer
 */

import Link from 'next/link'

const SHIFTS = [
  {
    label: 'EL CONOCIMIENTO',
    before: 'Copias sintaxis hasta que la recuerdas.',
    after:  'Necesitas la solución hasta que la descubres.',
    color:  '#00FF41',
  },
  {
    label: 'EL APRENDIZAJE',
    before: 'Videos que puedes pausar, rebobinar, ignorar.',
    after:  'Un sistema que ajusta la exigencia a tu lógica.',
    color:  '#00B4D8',
  },
  {
    label: 'EL RESULTADO',
    before: 'Un certificado que valida que completaste un curso.',
    after:  'Un sistema desplegado que valida que puedes construir uno.',
    color:  '#FFB800',
  },
]

const FOUNDER_FEATURES = [
  '100 Niveles completos — de Python a sistemas',
  'IA de grado industrial · sin límites',
  'Misiones Clasificadas · proyectos reales',
  'Leaderboard + Insignias de Rango Operativo',
  'Mentoría directa con los creadores',
  'Sello de Operador Certificado',
  'Acceso de por vida · precio de lanzamiento',
]

const FREE_FEATURES = [
  { text: 'Niveles 1 – 10 de 100',               ok: true  },
  { text: 'IA limitada · 20 consultas / día',     ok: true  },
  { text: 'Misiones de calibración estándar',     ok: true  },
  { text: 'Leaderboard de Operadores',            ok: true  },
  { text: 'Misiones Clasificadas',                ok: false },
  { text: 'Mentoría directa con creadores',       ok: false },
  { text: 'Sello de Operador Certificado',        ok: false },
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
        className="absolute inset-0 pointer-events-none opacity-[0.02]"
        style={{ backgroundImage: 'repeating-linear-gradient(0deg,transparent,transparent 3px,#00FF41 3px,#00FF41 4px)' }}
      />

      {/* Scrollable body */}
      <div className="flex-1 overflow-y-auto px-6 pb-4 pt-6 min-h-0" style={{ scrollbarWidth: 'none' }}>

        {/* ── Paradigm shifts ────────────────────────────────────────────────── */}
        <p className="text-[8px] tracking-[0.6em] text-[#FF0033]/40 uppercase mb-4">
          {'// LA DISRUPCIÓN — POR QUÉ DAKI EXISTE'}
        </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mb-8">
          {SHIFTS.map(({ label, before, after, color }) => (
            <div
              key={label}
              className="p-4 relative overflow-hidden"
              style={{ border: `1px solid ${color}20`, background: `${color}03` }}
            >
              <div className="absolute top-0 left-0 right-0 h-px" style={{ background: `linear-gradient(90deg,transparent,${color}50,transparent)` }} />
              <p className="text-[8px] tracking-[0.45em] font-bold uppercase mb-3" style={{ color: `${color}45` }}>
                {label}
              </p>
              <p className="text-white/22 text-[10px] leading-5 italic mb-2">
                &ldquo;{before}&rdquo;
              </p>
              <div className="h-px mb-2" style={{ background: `${color}14` }} />
              <p className="text-[11px] leading-5 font-bold text-white/85">
                {after}
              </p>
            </div>
          ))}
        </div>

        {/* ── Pricing ────────────────────────────────────────────────────────── */}
        <p className="text-[8px] tracking-[0.6em] text-[#00FF41]/22 uppercase mb-4">
          {'// CHECKPOINT DE ACCESO — SELECCIONA TU PROTOCOLO'}
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-8">

          {/* Fundador */}
          <div
            className="relative p-5 flex flex-col gap-4"
            style={{ border: '1px solid rgba(0,255,65,0.30)', background: 'rgba(0,255,65,0.03)' }}
          >
            <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-[#00FF41] px-3 py-0.5">
              <span className="text-[#0A0A0A] text-[8px] tracking-[0.4em] uppercase font-bold">
                ⚡ CUPOS BETA LIMITADOS
              </span>
            </div>
            <div className="pt-1">
              <p className="text-[#00FF41] text-[10px] tracking-[0.5em] uppercase font-bold mb-0.5"
                style={{ textShadow: '0 0 10px rgba(0,255,65,0.4)' }}>
                LICENCIA DE FUNDADOR
              </p>
              <p className="text-white/30 text-[9px] tracking-[0.3em] uppercase">Experiencia Completa</p>
            </div>
            <ul className="space-y-2 flex-1">
              {FOUNDER_FEATURES.map((f, i) => (
                <li key={i} className="flex items-start gap-2">
                  <span className="text-[#00FF41] font-bold text-xs shrink-0 mt-0.5"
                    style={{ textShadow: '0 0 8px rgba(0,255,65,0.5)' }}>✓</span>
                  <span className="text-[#C0C0C0]/75 text-[10px] leading-5 tracking-wide">{f}</span>
                </li>
              ))}
            </ul>
            <div className="border-t border-[#00FF41]/12 pt-4">
              <p className="text-[#00FF41]/30 text-[8px] tracking-[0.5em] uppercase mb-1">PRECIO BETA</p>
              <p className="text-[#00FF41] text-xl font-bold mb-3"
                style={{ textShadow: '0 0 16px rgba(0,255,65,0.4)' }}>
                ACCESO DE POR VIDA
              </p>
              <Link
                href="/register"
                className="block text-center border border-[#00FF41]/25 bg-[#00FF41]/[0.07] text-[#00FF41] text-[10px] tracking-[0.4em] uppercase py-3 w-full hover:bg-[#00FF41]/12 transition-colors duration-200"
              >
                {'[[ OBTENER LICENCIA DE FUNDADOR ]]'}
              </Link>
              <p className="text-white/10 text-[8px] tracking-[0.2em] text-center mt-2">
                Este precio no vuelve una vez termine la Beta.
              </p>
            </div>
          </div>

          {/* Free */}
          <div
            className="p-5 flex flex-col gap-4 opacity-60"
            style={{ border: '1px solid rgba(255,255,255,0.06)', background: 'rgba(10,10,10,0.6)' }}
          >
            <div>
              <p className="text-white/30 text-[10px] tracking-[0.5em] uppercase font-bold mb-0.5">MODO EXPLORACIÓN</p>
              <p className="text-white/18 text-[9px] tracking-[0.3em] uppercase">Prueba de Lógica</p>
            </div>
            <ul className="space-y-2 flex-1">
              {FREE_FEATURES.map((f, i) => (
                <li key={i} className="flex items-start gap-2">
                  <span className={`font-bold text-xs shrink-0 mt-0.5 ${f.ok ? 'text-white/30' : 'text-white/12'}`}>
                    {f.ok ? '✓' : '—'}
                  </span>
                  <span className={`text-[10px] leading-5 tracking-wide ${f.ok ? 'text-white/38' : 'text-white/14 line-through decoration-white/10'}`}>
                    {f.text}
                  </span>
                </li>
              ))}
            </ul>
            <div className="border-t border-white/[0.05] pt-4">
              <p className="text-white/15 text-[8px] tracking-[0.5em] uppercase mb-1">ACCESO BASE</p>
              <p className="text-white/28 text-xl font-bold mb-3">GRATIS</p>
              <Link
                href="/register"
                className="block text-center border border-white/10 text-white/20 text-[10px] tracking-[0.35em] uppercase py-3 w-full hover:border-white/20 hover:text-white/35 transition-colors duration-200"
              >
                {'[ Explorar el Nexo → ]'}
              </Link>
              <p className="text-white/08 text-[8px] tracking-[0.2em] text-center mt-2">
                Sin tarjeta de crédito · Acceso inmediato
              </p>
            </div>
          </div>

        </div>

        {/* ── CTA final ─────────────────────────────────────────────────────── */}
        <div className="text-center py-6 border border-[#00FF41]/08 mb-6" style={{ background: 'rgba(0,255,65,0.01)' }}>
          <div className="absolute top-0 left-0 right-0 h-px" style={{ background: 'linear-gradient(90deg,transparent,rgba(0,255,65,0.25),transparent)' }} />
          <h2
            className="text-2xl sm:text-3xl font-bold tracking-[0.05em] uppercase leading-tight mb-2 text-white"
            style={{ textShadow: '0 0 60px rgba(0,255,65,0.06)' }}
          >
            ¿VAS A <span className="text-white/22">OBSERVAR</span> EL SISTEMA,
          </h2>
          <h2
            className="text-2xl sm:text-3xl font-bold tracking-[0.05em] uppercase leading-tight mb-6"
          >
            O VAS A{' '}
            <span
              className="text-[#00FF41]"
              style={{ textShadow: '0 0 28px rgba(0,255,65,0.55), 0 0 56px rgba(0,255,65,0.18)' }}
            >
              CONSTRUIRLO?
            </span>
          </h2>
          <div className="flex flex-col items-center gap-2">
            <Link
              href="/register"
              className="border border-[#00FF41]/25 bg-[#00FF41]/[0.06] text-[#00FF41] text-[10px] tracking-[0.45em] uppercase px-10 py-4 hover:bg-[#00FF41]/10 transition-colors duration-200 inline-block"
            >
              {'[[ OBTENER LICENCIA DE FUNDADOR ]]'}
            </Link>
            <Link
              href="/register"
              className="text-[#00FF41]/20 text-[9px] tracking-[0.35em] uppercase hover:text-[#00FF41]/50 transition-colors duration-200"
            >
              {'[ Entrar al Nexo gratis → ]'}
            </Link>
            <p className="text-white/10 text-[8px] tracking-[0.3em] mt-1">
              Sin tarjeta de crédito · Sin subscripciones · Acceso inmediato
            </p>
          </div>
        </div>

        {/* ── Footer ────────────────────────────────────────────────────────── */}
        <div className="border-t border-white/[0.04] pt-4 pb-2">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-3">
            <div className="flex items-center gap-5">
              <p className="text-[#00FF41] text-xs font-bold tracking-[0.4em] uppercase"
                style={{ textShadow: '0 0 8px rgba(0,255,65,0.3)' }}>
                DAKIedtech
              </p>
              <p className="text-[#00FF41]/15 text-[9px] tracking-[0.25em] hidden sm:block">
                Aprende Python como un Operador.
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
