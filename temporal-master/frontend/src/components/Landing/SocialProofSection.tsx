/**
 * SocialProofSection.tsx — Strip de prueba social · DAKI EdTech
 * ──────────────────────────────────────────────────────────────
 * Stats honestos basados en el producto (no user counts fabricados).
 * Sin inline <style> — usa solo Tailwind.
 */

const STATS = [
  { value: 'Python', label: 'Misión 01',        sub: 'el lenguaje de la IA y la nube' },
  { value: '100',    label: 'Niveles',          sub: 'de combate real'                },
  { value: '∞',      label: 'Misiones',         sub: 'generadas por IA'               },
  { value: '0',      label: 'Teoría Muerta',    sub: 'solo código en producción'      },
] as const

const PILLARS = [
  'Python — de cero a arquitecto',
  'Sin videos pregrabados',
  'Código en producción real',
] as const

export default function SocialProofSection() {
  return (
    <section className="bg-[#080808] font-mono border-y border-[#00FF41]/[0.07] px-6 md:px-12 py-16">
      <div className="max-w-6xl mx-auto">

        {/* Stats grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mb-10">
          {STATS.map(({ value, label, sub }) => (
            <div key={label} className="text-center">
              <div
                className="text-[#00FF41] text-3xl md:text-4xl font-bold mb-1"
                style={{ textShadow: '0 0 16px rgba(0,255,65,0.55), 0 0 32px rgba(0,255,65,0.2)' }}
              >
                {value}
              </div>
              <div className="text-white text-[11px] tracking-[0.35em] uppercase mb-1">
                {label}
              </div>
              <div className="text-[#00FF41]/30 text-[10px] tracking-[0.2em]">
                {sub}
              </div>
            </div>
          ))}
        </div>

        {/* Divisor */}
        <div className="h-px bg-gradient-to-r from-transparent via-[#00FF41]/12 to-transparent mb-8" />

        {/* Pillars */}
        <div className="flex flex-wrap items-center justify-center gap-x-6 gap-y-2">
          {PILLARS.map((pillar, i) => (
            <span key={pillar} className="flex items-center gap-6">
              <span className="text-[#00FF41]/40 text-[10px] tracking-[0.35em] uppercase">
                {pillar}
              </span>
              {i < PILLARS.length - 1 && (
                <span className="text-[#00FF41]/15 hidden md:inline text-xs">·</span>
              )}
            </span>
          ))}
        </div>

      </div>
    </section>
  )
}
