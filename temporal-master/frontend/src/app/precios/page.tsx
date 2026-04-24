import Link from 'next/link'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Precios | DAKI EdTech — Aprende Python desde $0',
  description: 'Empieza gratis con 10 misiones reales. Suscribite por $19/mes para acceso completo: 195 misiones, IA sin límites y certificación de Operador.',
  alternates: { canonical: 'https://dakiedtech.com/precios' },
}

const EXPLORER = [
  { text: 'Misiones 1 – 10 de 195',        included: true  },
  { text: 'IA DAKI · 20 consultas/día',     included: true  },
  { text: 'Leaderboard de Operadores',      included: true  },
  { text: 'Misiones Clasificadas',          included: false },
  { text: 'Certificación de Operador',      included: false },
  { text: 'Acceso de por vida',             included: false },
]

const FULL = [
  '195 misiones · Python Core completo',
  'IA DAKI · sin límites',
  'Misiones Clasificadas',
  'Leaderboard + Insignias de Rango',
  'Certificación de Operador',
  'Cancela cuando quieras',
]

const FAQ = [
  {
    q: '¿Puedo cancelar cuando quiera?',
    a: 'Sí. La suscripción es mensual, sin permanencia. Cancelás desde tu cuenta de Hotmart en cualquier momento.',
  },
  {
    q: '¿Qué pasa con mi progreso si cancelo?',
    a: 'Tu XP y progreso quedan guardados. Si volvés a suscribirte, retomás exactamente donde dejaste.',
  },
  {
    q: '¿Es realmente gratis el plan Exploración?',
    a: 'Sí. Las primeras 10 misiones son completamente gratis, sin tarjeta de crédito.',
  },
  {
    q: '¿La plataforma está en español?',
    a: 'Sí. Todo el contenido, la IA DAKI y la interfaz están en español latinoamericano.',
  },
]

export default function PreciosPage() {
  return (
    <main className="min-h-screen bg-[#020202] font-mono text-[#00FF41] pt-14">

      {/* Scanlines */}
      <div
        className="fixed inset-0 pointer-events-none z-0 opacity-[0.015]"
        style={{ backgroundImage: 'repeating-linear-gradient(0deg,transparent,transparent 3px,#00FF41 3px,#00FF41 4px)' }}
      />

      <div className="relative z-10 max-w-3xl mx-auto px-6 py-16">

        {/* Breadcrumb */}
        <div className="flex items-center gap-2 mb-10 text-[8px] tracking-[0.35em] uppercase">
          <Link href="/" className="text-[#00FF41]/28 hover:text-[#00FF41]/55 transition-colors">NEXO</Link>
          <span className="text-[#00FF41]/15">›</span>
          <span className="text-[#00FF41]/45">PRECIOS</span>
        </div>

        {/* Header */}
        <header className="mb-12">
          <p className="text-[8px] tracking-[0.6em] text-[#00FF41]/25 uppercase mb-3">
            {'// PROTOCOLO DE ACCESO — SELECCIONÁ TU NIVEL'}
          </p>
          <h1 className="text-3xl sm:text-4xl font-black tracking-[0.05em] uppercase text-white/85 mb-4">
            Empieza{' '}
            <span className="text-[#00FF41]" style={{ textShadow: '0 0 28px rgba(0,255,65,0.4)' }}>
              gratis.
            </span>
          </h1>
          <p className="text-sm text-white/40 leading-relaxed">
            Las primeras 10 misiones son sin costo. Cuando quieras ir más profundo, suscribite por $19/mes.
          </p>
          <div className="mt-6 h-px bg-gradient-to-r from-[#00FF41]/20 via-transparent to-transparent" />
        </header>

        {/* Pricing grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-12">

          {/* Free */}
          <div className="border border-white/[0.06] bg-[#0A0A0A] p-6 flex flex-col">
            <p className="text-white/30 text-[9px] tracking-[0.4em] uppercase mb-1 font-bold">EXPLORACIÓN</p>
            <p className="text-white/20 text-[9px] tracking-[0.25em] uppercase mb-4">Prueba de Lógica</p>
            <p className="text-white/40 text-3xl font-bold mb-6">GRATIS</p>
            <ul className="space-y-3 flex-1 mb-6">
              {EXPLORER.map((f, i) => (
                <li key={i} className="flex items-center gap-2">
                  <span className={`text-[10px] font-bold shrink-0 ${f.included ? 'text-white/35' : 'text-white/12'}`}>
                    {f.included ? '✓' : '—'}
                  </span>
                  <span className={`text-[9px] leading-4 ${f.included ? 'text-white/40' : 'text-white/15 line-through'}`}>
                    {f.text}
                  </span>
                </li>
              ))}
            </ul>
            <Link
              href="/register"
              className="block text-center border border-white/15 text-[9px] tracking-[0.4em] uppercase px-5 py-3 text-white/35 hover:border-white/30 hover:text-white/55 transition-all duration-200"
            >
              EMPEZAR GRATIS →
            </Link>
          </div>

          {/* Subscription */}
          <div
            className="border p-6 flex flex-col relative"
            style={{ borderColor: 'rgba(0,255,65,0.30)', background: 'rgba(0,255,65,0.03)' }}
          >
            <div
              className="absolute top-0 left-0 right-0 h-px"
              style={{ background: 'linear-gradient(90deg,transparent,rgba(0,255,65,0.55),transparent)' }}
            />
            <p className="text-[#00FF41] text-[9px] tracking-[0.4em] uppercase mb-1 font-bold"
              style={{ textShadow: '0 0 8px rgba(0,255,65,0.4)' }}>
              SUSCRIPCIÓN
            </p>
            <p className="text-white/30 text-[9px] tracking-[0.25em] uppercase mb-4">Experiencia Completa</p>
            <div className="mb-6">
              <span className="text-[#00FF41] text-3xl font-bold" style={{ textShadow: '0 0 16px rgba(0,255,65,0.5)' }}>
                $19
              </span>
              <span className="text-white/35 text-sm ml-1">USD/mes</span>
              <p className="text-[#00FF41]/35 text-[8px] tracking-[0.3em] uppercase mt-1">cancela cuando quieras</p>
            </div>
            <ul className="space-y-3 flex-1 mb-6">
              {FULL.map((f, i) => (
                <li key={i} className="flex items-center gap-2">
                  <span className="text-[10px] font-bold shrink-0 text-[#00FF41]" style={{ textShadow: '0 0 6px rgba(0,255,65,0.5)' }}>
                    ✓
                  </span>
                  <span className="text-[9px] leading-4 text-white/65">{f}</span>
                </li>
              ))}
            </ul>
            <Link
              href="https://go.hotmart.com/K105401308T"
              target="_blank"
              rel="noopener noreferrer"
              className="block text-center border border-[#00FF41]/50 text-[9px] tracking-[0.4em] uppercase px-5 py-3 text-[#00FF41] hover:border-[#00FF41] hover:bg-[#00FF41]/08 transition-all duration-200"
            >
              {'[[ SUSCRIBIRSE — $19/MES ]]'}
            </Link>
          </div>
        </div>

        {/* FAQ */}
        <section className="mb-12">
          <p className="text-[8px] tracking-[0.55em] text-[#00FF41]/25 uppercase mb-6">
            {'// PREGUNTAS FRECUENTES'}
          </p>
          <div className="space-y-4">
            {FAQ.map(({ q, a }) => (
              <div key={q} className="border-l-2 border-[#00FF41]/20 pl-4">
                <p className="text-[11px] font-black tracking-[0.08em] uppercase text-white/70 mb-1">{q}</p>
                <p className="text-[10px] text-white/38 leading-relaxed">{a}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Footer nav */}
        <div className="pt-6 border-t border-[#00FF41]/8 flex items-center justify-between">
          <Link href="/" className="text-[#00FF41]/30 text-[9px] tracking-[0.3em] uppercase hover:text-[#00FF41]/60 transition-colors">
            ← NEXO CENTRAL
          </Link>
          <Link href="/register" className="text-[#00FF41]/30 text-[9px] tracking-[0.3em] uppercase hover:text-[#00FF41]/60 transition-colors">
            CREAR CUENTA →
          </Link>
        </div>
      </div>
    </main>
  )
}
