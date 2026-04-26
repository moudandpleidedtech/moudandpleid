/**
 * FounderLicenseSection.tsx — Distinción de Protocolo · DAKI EdTech
 * ──────────────────────────────────────────────────────────────────
 * Comparativa Modo Exploración (grises) vs Licencia de Fundador (neón).
 * Mobile-first: Fundador aparece primero en móvil (md:order-last en desktop).
 * Gatillo mental: Contraste + escasez + anclaje de valor.
 * Sin inline <style> — CSS en globals.css.
 */

import Link from 'next/link'

const EXPLORATION_FEATURES = [
  { text: 'Niveles 1 – 10 de 100',                 included: true  },
  { text: 'IA limitada · 20 consultas / día',       included: true  },
  { text: 'Misiones de calibración estándar',       included: true  },
  { text: 'Leaderboard de Operadores',              included: true  },
  { text: 'Misiones Clasificadas (proyectos reales)', included: false },
  { text: 'Mentoría directa con los creadores',    included: false },
  { text: 'Sello de Operador Certificado',          included: false },
] as const

const FOUNDER_FEATURES = [
  { text: '100 Niveles completos — de Python a sistemas' },
  { text: 'IA de grado industrial · sin límites'         },
  { text: 'Misiones Clasificadas · proyectos reales'     },
  { text: 'Leaderboard + Insignias de Rango Operativo'   },
  { text: 'Mentoría directa con los creadores'           },
  { text: 'Sello de Operador Certificado'                },
  { text: 'Cancela cuando quieras'                       },
] as const

export default function FounderLicenseSection() {
  return (
    <section
      className="font-mono px-6 md:px-12 py-24 relative overflow-hidden"
      style={{
        backgroundImage: 'url(/assets/founder-bg.png)',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundAttachment: 'fixed',
      }}
    >
      {/* Overlay oscuro — mantiene el tema DAKI sobre el fondo cálido */}
      <div
        className="absolute inset-0 pointer-events-none"
        style={{ background: 'rgba(4,4,4,0.86)' }}
      />

      {/* Vignette */}
      <div
        className="absolute inset-0 pointer-events-none"
        style={{ background: 'radial-gradient(ellipse at center,transparent 40%,rgba(6,6,6,0.9) 100%)' }}
      />

      <div className="max-w-5xl mx-auto relative z-10">

        {/* Header */}
        <div className="text-center mb-14">
          <p className="text-[#00FF41]/35 text-[10px] tracking-[0.6em] uppercase mb-4">
            {'// CHECKPOINT DE ACCESO — SELECCIONA TU PROTOCOLO'}
          </p>
          <h2
            className="text-3xl sm:text-4xl md:text-5xl font-bold tracking-[0.08em] uppercase text-white"
            style={{ textShadow: '0 0 60px rgba(0,255,65,0.08)' }}
          >
            DISTINCIÓN DE
            {' '}
            <span
              className="text-[#00FF41]"
              style={{ textShadow: '0 0 28px rgba(0,255,65,0.5)' }}
            >
              PROTOCOLO
            </span>
          </h2>
        </div>

        {/* ── Comparativa ───────────────────────────────────────────────── */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">

          {/* SUSCRIPCIÓN — primero en DOM = primero en móvil, right en desktop */}
          <div className="founder-active border bg-[#0A0A0A] p-5 md:p-8 flex flex-col gap-6 md:order-2 relative">

            {/* Header columna */}
            <div className="pt-2">
              <p
                className="text-[#00FF41] text-[10px] tracking-[0.5em] uppercase mb-1 font-bold"
                style={{ textShadow: '0 0 10px rgba(0,255,65,0.5)' }}
              >
                SUSCRIPCIÓN MENSUAL
              </p>
              <p className="text-white/40 text-[10px] tracking-[0.3em] uppercase">
                Experiencia Completa
              </p>
            </div>

            {/* Features */}
            <ul className="space-y-3 flex-1">
              {FOUNDER_FEATURES.map((f, i) => (
                <li key={i} className="flex items-start gap-3">
                  <span
                    className="text-[#00FF41] font-bold text-sm shrink-0 mt-0.5"
                    style={{ textShadow: '0 0 8px rgba(0,255,65,0.6)' }}
                  >
                    ✓
                  </span>
                  <span className="text-[#C0C0C0]/80 text-[11px] leading-5 tracking-wide">
                    {f.text}
                  </span>
                </li>
              ))}
            </ul>

            {/* Precio */}
            <div className="border-t border-[#00FF41]/15 pt-5">
              <div className="flex items-baseline gap-2 mb-1">
                <p
                  className="text-[#00FF41] text-3xl font-bold"
                  style={{ textShadow: '0 0 16px rgba(0,255,65,0.5)' }}
                >
                  $19
                </p>
                <span className="text-white/40 text-sm tracking-wide">USD/mes</span>
              </div>
              <p className="text-[#00FF41]/35 text-[9px] tracking-[0.35em] uppercase mb-4">
                cancela cuando quieras · sin permanencia
              </p>
              <Link
                href="https://go.hotmart.com/K105401308T"
                target="_blank"
                rel="noopener noreferrer"
                className="cta-primary-btn block text-center border border-[#00FF41]/25 bg-[#00FF41]/[0.07] text-[#00FF41] text-[11px] tracking-[0.4em] uppercase py-4 w-full"
              >
                {`[[ SUSCRIBIRSE — $19/MES ]]`}
              </Link>
              <p className="text-white/12 text-[9px] tracking-[0.2em] text-center mt-3">
                Sin compromisos · acceso completo desde el día 1.
              </p>
            </div>

          </div>

          {/* EXPLORACIÓN — segundo en DOM = segundo en móvil, left en desktop */}
          <div className="border border-white/[0.05] bg-[#0A0A0A] p-5 md:p-8 flex flex-col gap-6 md:order-1 opacity-70">

            {/* Header columna */}
            <div>
              <p className="text-white/30 text-[10px] tracking-[0.5em] uppercase mb-1 font-bold">
                MODO EXPLORACIÓN
              </p>
              <p className="text-white/20 text-[10px] tracking-[0.3em] uppercase">
                Prueba de Lógica
              </p>
            </div>

            {/* Features */}
            <ul className="space-y-3 flex-1">
              {EXPLORATION_FEATURES.map((f, i) => (
                <li key={i} className="flex items-start gap-3">
                  {f.included ? (
                    <span className="text-white/35 font-bold text-sm shrink-0 mt-0.5">✓</span>
                  ) : (
                    <span className="text-white/15 font-bold text-sm shrink-0 mt-0.5">—</span>
                  )}
                  <span
                    className={`text-[11px] leading-5 tracking-wide ${
                      f.included ? 'text-white/40' : 'text-white/15 line-through decoration-white/10'
                    }`}
                  >
                    {f.text}
                  </span>
                </li>
              ))}
            </ul>

            {/* Precio */}
            <div className="border-t border-white/[0.06] pt-5">
              <p className="text-white/15 text-[9px] tracking-[0.5em] uppercase mb-1">
                ACCESO BASE
              </p>
              <p className="text-white/30 text-2xl font-bold mb-4">
                GRATIS
              </p>
              <Link
                href="/register"
                className="block text-center border border-white/10 text-white/20 text-[11px] tracking-[0.35em] uppercase py-4 w-full hover:border-white/20 hover:text-white/35 transition-colors duration-200"
              >
                {`[ Explorar el Nexo → ]`}
              </Link>
              <p className="text-white/08 text-[9px] tracking-[0.2em] text-center mt-3">
                Sin tarjeta de crédito · Acceso inmediato
              </p>
            </div>

          </div>

        </div>

      </div>
    </section>
  )
}
