/**
 * TestimonialsSection.tsx — La Visión · DAKI EdTech
 * ───────────────────────────────────────────────────
 * No testimonios ficticios. La declaración directa de la disrupción.
 * DAKI habla en primera persona sobre lo que está rompiendo y por qué.
 * Server Component. Sin inline <style>. CSS en globals.css.
 */

const PARADIGM_SHIFTS = [
  {
    label:  'EL CONOCIMIENTO',
    before: 'Te enseñamos sintaxis hasta que la recuerdes.',
    after:  'Te hacemos necesitar la solución hasta que la descubras.',
    accent: 'La fluidez no se memoriza — se forja bajo presión real.',
  },
  {
    label:  'EL APRENDIZAJE',
    before: 'Videos pregrabados que puedes pausar, rebobinar, ignorar.',
    after:  'Un sistema adaptativo que ajusta la exigencia a tu lógica actual.',
    accent: 'La IA no te espera. Tú la alcanzas.',
  },
  {
    label:  'EL RESULTADO',
    before: 'Un certificado que valida que completaste un curso.',
    after:  'Un sistema desplegado que valida que puedes construir uno.',
    accent: 'El mercado no lee diplomas. Lee código en producción.',
  },
] as const

export default function TestimonialsSection() {
  return (
    <section className="bg-[#080808] font-mono px-6 md:px-12 py-24 relative overflow-hidden">

      {/* Grid táctica de fondo — muy sutil */}
      <div
        className="absolute inset-0 pointer-events-none opacity-[0.015]"
        style={{
          backgroundImage:
            'linear-gradient(#00FF41 1px,transparent 1px),linear-gradient(90deg,#00FF41 1px,transparent 1px)',
          backgroundSize: '48px 48px',
        }}
      />

      <div className="max-w-5xl mx-auto relative z-10">

        {/* Pre-label */}
        <p className="text-[#FF0033]/45 text-[10px] tracking-[0.6em] uppercase mb-8">
          {'// LA DISRUPCIÓN — POR QUÉ DAKI EXISTE'}
        </p>

        {/* Declaración central */}
        <div className="mb-16 max-w-3xl">
          <h2
            className="text-3xl sm:text-4xl md:text-5xl font-bold tracking-[0.06em] uppercase leading-tight text-white mb-6"
            style={{ textShadow: '0 0 60px rgba(0,255,65,0.06)' }}
          >
            EL PROBLEMA NO ES QUE
            <br />
            APRENDER SEA{' '}
            <span
              className="text-[#FF0033]"
              style={{ textShadow: '0 0 20px rgba(255,0,51,0.35)' }}
            >
              DIFÍCIL.
            </span>
          </h2>
          <p className="text-[#C0C0C0]/55 text-base leading-8 tracking-wide">
            El problema es que nos enseñaron a aprender{' '}
            <span className="text-white/70">consumiendo</span> en lugar de{' '}
            <span
              className="text-[#00FF41]"
              style={{ textShadow: '0 0 10px rgba(0,255,65,0.4)' }}
            >
              construyendo
            </span>.
            {' '}Décadas de cursos, tutoriales y bootcamps crearon ingenieros que saben
            explicar el código pero no pueden desplegarlo.
            DAKI existe para romper ese ciclo.
          </p>
        </div>

        {/* Divisor */}
        <div className="flex items-center gap-4 mb-16">
          <div className="h-px flex-1 bg-gradient-to-r from-transparent via-[#00FF41]/12 to-transparent" />
          <span className="text-[#00FF41]/20 text-[10px] tracking-[0.5em] uppercase shrink-0">
            {'// CAMBIO DE PARADIGMA'}
          </span>
          <div className="h-px flex-1 bg-gradient-to-l from-transparent via-[#00FF41]/12 to-transparent" />
        </div>

        {/* Paradigm shift cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-16">
          {PARADIGM_SHIFTS.map(({ label, before, after, accent }) => (
            <div key={label} className="operator-card p-7 flex flex-col gap-5">

              {/* Label */}
              <p className="text-[#00FF41]/30 text-[9px] tracking-[0.6em] uppercase font-bold">
                {label}
              </p>

              {/* Before */}
              <div>
                <p className="text-[#FF0033]/35 text-[9px] tracking-[0.4em] uppercase mb-2">
                  AYER
                </p>
                <p className="text-white/30 text-[12px] leading-6 tracking-wide italic">
                  &ldquo;{before}&rdquo;
                </p>
              </div>

              <div className="h-px bg-[#00FF41]/08" />

              {/* After */}
              <div>
                <p
                  className="text-[#00FF41]/50 text-[9px] tracking-[0.4em] uppercase mb-2"
                  style={{ textShadow: '0 0 6px rgba(0,255,65,0.3)' }}
                >
                  DAKI
                </p>
                <p className="text-white/75 text-[12px] leading-6 tracking-wide">
                  {after}
                </p>
              </div>

              {/* Accent */}
              <p className="text-[#00FF41]/40 text-[10px] leading-5 tracking-wide border-l-2 border-[#00FF41]/20 pl-3 mt-auto">
                {accent}
              </p>

            </div>
          ))}
        </div>

        {/* Declaración de cierre — la frase que debe quedar */}
        <div className="border border-[#00FF41]/10 bg-[#00FF41]/[0.02] p-8 md:p-12 text-center cta-section-border">
          <p className="text-[#00FF41]/25 text-[10px] tracking-[0.6em] uppercase mb-6">
            {'// NÚCLEO DEL SISTEMA'}
          </p>
          <p
            className="text-xl sm:text-2xl md:text-3xl font-bold tracking-[0.06em] uppercase text-white leading-tight"
            style={{ textShadow: '0 0 40px rgba(0,255,65,0.08)' }}
          >
            PYTHON ES EL PRIMER PROTOCOLO DE PRUEBA.
            <br />
            <span
              className="text-[#00FF41]"
              style={{ textShadow: '0 0 24px rgba(0,255,65,0.45)' }}
            >
              LA FLUIDEZ LÓGICA ES EL PRODUCTO REAL.
            </span>
          </p>
          <p className="text-[#C0C0C0]/35 text-sm leading-7 tracking-wide max-w-2xl mx-auto mt-6">
            No entrenamos programadores de Python. Entrenamos ingenieros que piensan
            en sistemas, diseñan con arquitectura y despliegan con confianza.
            El lenguaje cambia. La lógica que construimos aquí, no.
          </p>
        </div>

      </div>
    </section>
  )
}
