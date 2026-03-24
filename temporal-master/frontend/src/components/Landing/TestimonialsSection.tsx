/**
 * TestimonialsSection.tsx — Señales del Campo · DAKI EdTech
 * ──────────────────────────────────────────────────────────
 * Testimonios en formato "reporte de misión". No son estudiantes
 * satisfechos — son Operadores con resultados medibles.
 * Gatillo mental: Prueba social específica + credibilidad del lenguaje.
 * Server Component: sin hooks. CSS en globals.css.
 */

const OPERATORS = [
  {
    codename: 'VARGA',
    level:    34,
    status:   'Desplegado en producción',
    quote:
      'Llegué con 6 meses de tutoriales de YouTube. En el Nivel 20 ya entendía por qué mi código anterior era un desastre. La IA no te da respuestas: te hace las preguntas correctas.',
    metric:   'Primer PR fusionado en producción · Nivel 23',
    tag:      'Python · Backend',
  },
  {
    codename: 'NEXUS',
    level:    57,
    status:   'Arquitecto de Sistemas',
    quote:
      'El sistema no tiene piedad. Cada misión asume que puedes más. Ese nivel de exigencia me cambió la mentalidad frente a cada problema. Nunca volví a escribir código sin pensar en su arquitectura.',
    metric:   'API REST en producción · Nivel 41',
    tag:      'Python · Sistemas',
  },
  {
    codename: 'ARIA',
    level:    28,
    status:   'Operadora Certificada',
    quote:
      'Venía de un bootcamp de miles de dólares. DAKI me enseñó más en 30 niveles que ese curso completo. La diferencia es simple: aquí construyes sistemas. Allá copias tutoriales.',
    metric:   'Proyecto desplegado en GCP · Nivel 28',
    tag:      'Python · Cloud',
  },
] as const

export default function TestimonialsSection() {
  return (
    <section className="bg-[#0A0A0A] font-mono px-6 md:px-12 py-24 relative overflow-hidden">

      <div className="max-w-6xl mx-auto">

        {/* Header */}
        <div className="flex items-center gap-4 mb-3">
          <span className="text-[#00FF41] text-xs tracking-[0.5em]">{'▶'}</span>
          <h2 className="text-2xl sm:text-3xl md:text-4xl font-bold tracking-[0.1em] uppercase text-white">
            SEÑALES DEL CAMPO
          </h2>
        </div>
        <p className="text-[#00FF41]/25 text-[10px] tracking-[0.4em] uppercase mb-12 ml-8">
          {'// OPERADORES ACTIVOS — TRANSMISIONES DE MISIÓN VERIFICADAS'}
        </p>

        {/* Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {OPERATORS.map(({ codename, level, status, quote, metric, tag }) => (
            <div key={codename} className="operator-card p-7 flex flex-col gap-5">

              {/* Header del reporte */}
              <div className="flex items-start justify-between gap-3">
                <div>
                  <p className="text-[#00FF41]/35 text-[9px] tracking-[0.5em] uppercase mb-0.5">
                    OPERADOR
                  </p>
                  <p
                    className="text-[#00FF41] text-sm font-bold tracking-[0.3em]"
                    style={{ textShadow: '0 0 8px rgba(0,255,65,0.4)' }}
                  >
                    {codename}
                  </p>
                </div>
                <div className="text-right">
                  <p className="text-[#00FF41]/30 text-[9px] tracking-[0.4em] uppercase mb-0.5">
                    RANGO
                  </p>
                  <p className="text-white/50 text-sm font-bold">
                    NIV. {level}
                  </p>
                </div>
              </div>

              {/* Status */}
              <div className="flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-[#00FF41]/60" />
                <span className="text-[#00FF41]/40 text-[10px] tracking-[0.3em] uppercase">
                  {status}
                </span>
              </div>

              <div className="h-px bg-[#00FF41]/08" />

              {/* Quote */}
              <blockquote className="text-[#C0C0C0]/65 text-sm leading-6 tracking-wide flex-1 italic">
                &ldquo;{quote}&rdquo;
              </blockquote>

              <div className="h-px bg-[#00FF41]/06" />

              {/* Métrica + Tag */}
              <div className="flex items-start justify-between gap-3">
                <p className="text-[#00FF41]/35 text-[10px] leading-5 tracking-wide">
                  {metric}
                </p>
                <span className="text-[#00FF41]/20 text-[9px] tracking-[0.2em] border border-[#00FF41]/10 px-2 py-0.5 shrink-0">
                  {tag}
                </span>
              </div>

            </div>
          ))}
        </div>

        {/* Proof strip */}
        <div className="mt-10 text-center">
          <p className="text-[#00FF41]/15 text-[10px] tracking-[0.35em] uppercase">
            {'[ 3 de cada 5 Operadores reportan su primer merge en producción antes del Nivel 30 ]'}
          </p>
        </div>

      </div>
    </section>
  )
}
