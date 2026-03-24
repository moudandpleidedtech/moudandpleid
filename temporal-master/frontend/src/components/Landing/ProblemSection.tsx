/**
 * ProblemSection.tsx — El Sistema Caduco · DAKI EdTech
 * ─────────────────────────────────────────────────────
 * Activa el dolor. Valida la frustración del usuario con el modelo
 * educativo tradicional. Ningún nombre propio es atacado — solo el modelo.
 * Gatillo mental: Agitación del problema + alivio de reconocimiento.
 */

const FAILURES = [
  {
    label:   'Curso Online',
    verdict: 'Te da un certificado.',
    result:  'El mercado ignora el papel.',
  },
  {
    label:   'Bootcamp',
    verdict: 'Te da velocidad.',
    result:  'Sin arquitectura, sin raíces.',
  },
  {
    label:   'Tutoriales de YouTube',
    verdict: 'Te da fragmentos.',
    result:  'Código que no sobrevive producción.',
  },
] as const

export default function ProblemSection() {
  return (
    <section className="bg-[#080808] font-mono px-6 md:px-12 py-24 relative overflow-hidden">

      {/* Grid táctica de fondo */}
      <div
        className="absolute inset-0 pointer-events-none opacity-[0.018]"
        style={{
          backgroundImage:
            'linear-gradient(#FF0033 1px,transparent 1px),linear-gradient(90deg,#FF0033 1px,transparent 1px)',
          backgroundSize: '48px 48px',
        }}
      />

      <div className="max-w-5xl mx-auto relative z-10">

        {/* Pre-label */}
        <p className="text-[#FF0033]/50 text-[10px] tracking-[0.6em] uppercase mb-8">
          {'// DIAGNÓSTICO DEL SISTEMA EDUCATIVO'}
        </p>

        {/* Headline */}
        <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold tracking-[0.06em] uppercase leading-tight mb-6">
          <span className="text-white">LOS CURSOS TE ENSEÑAN </span>
          <span
            className="text-[#FF0033]"
            style={{ textShadow: '0 0 20px rgba(255,0,51,0.4)' }}
          >
            SINTAXIS.
          </span>
          <br />
          <span className="text-white">EL MERCADO EXIGE </span>
          <span
            className="text-[#00FF41]"
            style={{ textShadow: '0 0 20px rgba(0,255,65,0.35)' }}
          >
            SISTEMAS.
          </span>
        </h2>

        {/* Sub-copy */}
        <p className="text-[#C0C0C0]/45 text-sm leading-7 tracking-wide max-w-2xl mb-16">
          Llevas meses estudiando. Sabes escribir bucles. Pero cuando te sientas
          frente a un proyecto real, la arquitectura se derrumba y el código no
          escala. No es tu culpa — es el modelo de enseñanza.
        </p>

        {/* Failure cards */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 mb-14">
          {FAILURES.map(({ label, verdict, result }) => (
            <div key={label} className="prob-card p-6">
              <p className="text-white/20 text-[10px] tracking-[0.5em] uppercase mb-5">
                {label}
              </p>
              <p className="text-white/55 text-sm font-bold mb-3">
                {verdict}
              </p>
              <div className="h-px bg-[#FF0033]/12 mb-3" />
              <p className="text-[#FF0033]/50 text-[11px] tracking-[0.15em] leading-5">
                RESULTADO: {result}
              </p>
            </div>
          ))}
        </div>

        {/* Bridge to solution */}
        <div className="flex items-center gap-4">
          <div className="h-px flex-1 bg-gradient-to-r from-transparent via-[#00FF41]/15 to-transparent" />
          <span className="text-[#00FF41]/35 text-[10px] tracking-[0.5em] uppercase shrink-0">
            {'// EXISTE UN PROTOCOLO DIFERENTE'}
          </span>
          <div className="h-px flex-1 bg-gradient-to-l from-transparent via-[#00FF41]/15 to-transparent" />
        </div>

      </div>
    </section>
  )
}
