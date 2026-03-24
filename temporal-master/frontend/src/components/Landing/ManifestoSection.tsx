'use client'

/**
 * ManifestoSection.tsx — La Anatomía del Nexo · DAKI EdTech
 * ────────────────────────────────────────────────────────────
 * Grid 2×2 de tarjetas con acrónimo DAKI.
 * Hover: borde verde neón + transición de opacidad en contenido.
 */

const CARDS = [
  {
    letter: 'D',
    title:  'Desarrollo',
    body:   'Construcción masiva. El código visto como una herramienta de creación, no como teoría pasiva.',
    accent: '#00FF41',
  },
  {
    letter: 'A',
    title:  'Arquitectura',
    body:   'Estructuras de élite. Diseño de sistemas preparados para escalar y resistir en producción real.',
    accent: '#00FF41',
  },
  {
    letter: 'K',
    title:  'Knowledge',
    body:   'Sabiduría táctica. El conocimiento no se memoriza, se descifra rompiendo sistemas.',
    accent: '#00FF41',
  },
  {
    letter: 'I',
    title:  'Inteligencia',
    body:   'Núcleo adaptativo. Una IA que analiza tu lógica en tiempo real para guiar tu evolución como Operador.',
    accent: '#00FF41',
  },
] as const

export default function ManifestoSection() {
  return (
    <section className="bg-[#0A0A0A] font-mono px-6 md:px-12 py-24 relative overflow-hidden">

      {/* ── Keyframes ──────────────────────────────────────────────────────────── */}
      <style>{`
        .daki-card {
          background: #0D0D0D;
          border: 1px solid rgba(0,255,65,0.12);
          transition: border-color 0.25s ease, box-shadow 0.25s ease;
        }
        .daki-card:hover {
          border-color: rgba(0,255,65,0.6);
          box-shadow: 0 0 24px rgba(0,255,65,0.08), inset 0 0 24px rgba(0,255,65,0.03);
        }
        .daki-card:hover .card-content {
          opacity: 1;
        }
        .card-content {
          opacity: 0.75;
          transition: opacity 0.25s ease;
        }
        .daki-card:hover .card-letter {
          text-shadow: 0 0 20px rgba(0,255,65,0.8), 0 0 40px rgba(0,255,65,0.4);
        }
        .card-letter {
          transition: text-shadow 0.25s ease;
          text-shadow: 0 0 8px rgba(0,255,65,0.3);
        }
      `}</style>

      {/* ── Línea decorativa superior ─────────────────────────────────────────── */}
      <div className="flex items-center gap-4 mb-16 max-w-5xl mx-auto">
        <div className="h-px flex-1 bg-gradient-to-r from-transparent via-[#00FF41]/20 to-transparent" />
        <span className="text-[#00FF41]/30 text-xs tracking-[0.5em] uppercase shrink-0">
          NEXO — SECTOR ALFA
        </span>
        <div className="h-px flex-1 bg-gradient-to-r from-transparent via-[#00FF41]/20 to-transparent" />
      </div>

      {/* ── Título de sección ─────────────────────────────────────────────────── */}
      <div className="text-center mb-16 max-w-5xl mx-auto">
        <p className="text-[#FF0033]/50 text-xs tracking-[0.6em] uppercase mb-4">
          {'// PROTOCOLO DE IDENTIFICACIÓN'}
        </p>
        <h2
          className="text-3xl sm:text-4xl md:text-5xl font-bold tracking-[0.1em] uppercase text-white"
          style={{ textShadow: '0 0 40px rgba(0,255,65,0.15), 0 0 80px rgba(0,255,65,0.06)' }}
        >
          LA ANATOMÍA DEL NEXO
        </h2>
        <div className="mt-4 flex justify-center">
          <div className="h-px w-24 bg-gradient-to-r from-transparent via-[#00FF41]/40 to-transparent" />
        </div>
      </div>

      {/* ── Grid 2×2 ──────────────────────────────────────────────────────────── */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 max-w-5xl mx-auto">
        {CARDS.map(({ letter, title, body }) => (
          <div key={letter} className="daki-card p-8 flex flex-col gap-5">

            {/* Letra DAKI */}
            <div className="flex items-baseline gap-2">
              <span className="card-letter text-[#00FF41] text-3xl font-bold tracking-widest">
                {'['}
              </span>
              <span className="card-letter text-[#00FF41] text-4xl font-bold">
                {letter}
              </span>
              <span className="card-letter text-[#00FF41] text-3xl font-bold tracking-widest">
                {']'}
              </span>
            </div>

            {/* Título de tarjeta */}
            <div className="card-content">
              <h3 className="text-[#00FF41] text-sm font-bold tracking-[0.3em] uppercase mb-3">
                {title}
              </h3>

              {/* Separador */}
              <div className="h-px bg-[#00FF41]/15 mb-4" />

              {/* Descripción */}
              <p className="text-[#C0C0C0]/80 text-sm leading-6 tracking-wide">
                {body}
              </p>
            </div>

          </div>
        ))}
      </div>

      {/* ── Footer de sección ─────────────────────────────────────────────────── */}
      <div className="flex items-center gap-4 mt-16 max-w-5xl mx-auto">
        <div className="h-px flex-1 bg-gradient-to-r from-transparent via-[#00FF41]/20 to-transparent" />
        <span className="text-[#00FF41]/20 text-xs tracking-[0.5em] uppercase shrink-0">
          {'D · A · K · I'}
        </span>
        <div className="h-px flex-1 bg-gradient-to-r from-transparent via-[#00FF41]/20 to-transparent" />
      </div>

    </section>
  )
}
