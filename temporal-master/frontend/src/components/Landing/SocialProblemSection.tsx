/**
 * SocialProblemSection — Credenciales + El Problema · slides 3+4 fusionados
 * Layout: headline + tarjetas de fracaso + strip de stats + puente
 */

const FAILURES = [
  { label: 'Curso Online',          verdict: 'Te da un certificado.',  result: 'El mercado ignora el papel.'           },
  { label: 'Bootcamp',              verdict: 'Te da velocidad.',        result: 'Sin arquitectura, sin raíces.'         },
  { label: 'YouTube / Tutoriales',  verdict: 'Te da fragmentos.',      result: 'Código que no sobrevive producción.'   },
] as const

const STATS = [
  { value: 'Python', label: 'Misión 01',     sub: 'lenguaje de la IA y la nube'  },
  { value: '100',    label: 'Niveles',       sub: 'de combate real'               },
  { value: '∞',      label: 'Misiones',      sub: 'generadas por IA'              },
  { value: '0',      label: 'Teoría Muerta', sub: 'solo código en producción'     },
] as const

export default function SocialProblemSection() {
  return (
    <section className="bg-[#080808] font-mono px-6 md:px-12 min-h-screen flex flex-col justify-center py-10 relative overflow-hidden">

      {/* Grid rojo de fondo */}
      <div
        className="absolute inset-0 pointer-events-none opacity-[0.016]"
        style={{ backgroundImage: 'linear-gradient(#FF0033 1px,transparent 1px),linear-gradient(90deg,#FF0033 1px,transparent 1px)', backgroundSize: '48px 48px' }}
      />

      <div className="max-w-5xl mx-auto w-full relative z-10">

        {/* Pre-label */}
        <p className="text-[#FF0033]/45 text-[9px] tracking-[0.6em] uppercase mb-4">
          {'// DIAGNÓSTICO DEL SISTEMA EDUCATIVO'}
        </p>

        {/* Headline */}
        <h2 className="text-2xl sm:text-3xl md:text-4xl font-bold tracking-[0.06em] uppercase leading-tight mb-3">
          <span className="text-white">LOS CURSOS TE ENSEÑAN </span>
          <span className="text-[#FF0033]" style={{ textShadow: '0 0 18px rgba(255,0,51,0.4)' }}>SINTAXIS.</span>
          <span className="text-white"> EL MERCADO EXIGE </span>
          <span className="text-[#00FF41]" style={{ textShadow: '0 0 18px rgba(0,255,65,0.35)' }}>SISTEMAS.</span>
        </h2>

        <p className="text-[#C0C0C0]/38 text-sm leading-6 tracking-wide max-w-2xl mb-7">
          Meses estudiando, sabes escribir bucles — pero frente a un proyecto real
          la arquitectura se derrumba. No es tu culpa. Es el modelo de enseñanza.
        </p>

        {/* Tarjetas de fracaso */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 mb-7">
          {FAILURES.map(({ label, verdict, result }) => (
            <div
              key={label}
              className="prob-card p-5 flex flex-col gap-3"
            >
              <p className="text-white/18 text-[9px] tracking-[0.5em] uppercase">{label}</p>
              <p className="text-white/55 text-sm font-bold">{verdict}</p>
              <div className="h-px bg-[#FF0033]/10" />
              <p className="text-[#FF0033]/45 text-[10px] tracking-[0.15em] leading-5">
                RESULTADO: {result}
              </p>
            </div>
          ))}
        </div>

        {/* Stats strip */}
        <div
          className="grid grid-cols-4 gap-0 border border-[#00FF41]/08 mb-6"
          style={{ background: 'rgba(0,255,65,0.02)' }}
        >
          {STATS.map(({ value, label, sub }, i) => (
            <div
              key={label}
              className={`py-4 text-center ${i < 3 ? 'border-r border-[#00FF41]/06' : ''}`}
            >
              <div
                className="text-[#00FF41] text-2xl font-bold mb-0.5"
                style={{ textShadow: '0 0 14px rgba(0,255,65,0.5)' }}
              >
                {value}
              </div>
              <div className="text-white text-[9px] tracking-[0.35em] uppercase mb-0.5">{label}</div>
              <div className="text-[#00FF41]/25 text-[8px] tracking-[0.2em]">{sub}</div>
            </div>
          ))}
        </div>

        {/* Puente */}
        <div className="flex items-center gap-4">
          <div className="h-px flex-1 bg-gradient-to-r from-transparent via-[#00FF41]/12 to-transparent" />
          <span className="text-[#00FF41]/30 text-[9px] tracking-[0.5em] uppercase shrink-0">
            {'// EXISTE UN PROTOCOLO DIFERENTE'}
          </span>
          <div className="h-px flex-1 bg-gradient-to-l from-transparent via-[#00FF41]/12 to-transparent" />
        </div>

      </div>
    </section>
  )
}
