import Link from 'next/link'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'La Plataforma | DAKI EdTech — 195 Misiones de Python',
  description: '195 misiones de Python ejecutables en vivo. IA que detecta tus errores. Dificultad adaptativa. Sin teoría muerta — código real desde el día 1.',
  alternates: { canonical: 'https://dakiedtech.com/plataforma' },
}

const PILARES = [
  {
    glyph: '◈',
    color: '#00FF41',
    title: 'IA Que Interroga',
    tagline: 'No te da la respuesta. Te hace la pregunta correcta.',
    body: 'DAKI detecta dónde falla tu lógica y construye la pregunta exacta que te fuerza a resolver el problema vos mismo.',
    stat: '3 niveles de escalación cognitiva',
  },
  {
    glyph: '▶',
    color: '#06b6d4',
    title: 'Código Que Corre',
    tagline: 'Sandbox real. Output real.',
    body: 'Cada misión evalúa lo que hace tu código. Sin múltiple choice. Si falla, falla. Si pasa, pasó.',
    stat: '195 misiones ejecutables en vivo',
  },
  {
    glyph: '⬡',
    color: '#f59e0b',
    title: 'Dificultad Adaptativa',
    tagline: 'Nunca aburrido. Nunca injusto.',
    body: 'El sistema lee tus patrones de error y calibra la próxima misión siempre en el borde de tu límite. Adaptación en tiempo real.',
    stat: 'DDA — sin techo artificial',
  },
]

const AREAS = [
  { name: 'Python Core',              count: '45 misiones' },
  { name: 'Estructuras de Datos',     count: '28 misiones' },
  { name: 'POO — Clases y Objetos',   count: '22 misiones' },
  { name: 'APIs y HTTP',              count: '18 misiones' },
  { name: 'Manejo de Errores',        count: '15 misiones' },
  { name: 'Archivos y JSON',          count: '12 misiones' },
  { name: 'Algoritmos y Eficiencia',  count: '20 misiones' },
  { name: 'Testing Unitario',         count: '15 misiones' },
  { name: 'Boss Final',               count: '1 misión'    },
]

export default function PlataformaPage() {
  return (
    <main className="min-h-screen bg-[#020202] font-mono text-[#00FF41] pt-14">

      <div
        className="fixed inset-0 pointer-events-none z-0 opacity-[0.015]"
        style={{ backgroundImage: 'repeating-linear-gradient(0deg,transparent,transparent 3px,#00FF41 3px,#00FF41 4px)' }}
      />

      <div className="relative z-10 max-w-4xl mx-auto px-6 py-16">

        {/* Breadcrumb */}
        <div className="flex items-center gap-2 mb-10 text-[8px] tracking-[0.35em] uppercase">
          <Link href="/" className="text-[#00FF41]/28 hover:text-[#00FF41]/55 transition-colors">NEXO</Link>
          <span className="text-[#00FF41]/15">›</span>
          <span className="text-[#00FF41]/45">PLATAFORMA</span>
        </div>

        {/* Header */}
        <header className="mb-14">
          <p className="text-[8px] tracking-[0.6em] text-[#00FF41]/25 uppercase mb-3">
            {'// SISTEMA — 195 MISIONES EJECUTABLES'}
          </p>
          <h1 className="text-3xl sm:text-4xl font-black tracking-[0.05em] uppercase text-white/85 mb-4 leading-tight">
            No memorizás.{' '}
            <span className="text-[#00FF41]" style={{ textShadow: '0 0 28px rgba(0,255,65,0.4)' }}>
              Entrenás de verdad.
            </span>
          </h1>
          <p className="text-sm text-white/40 leading-relaxed max-w-xl">
            Cada misión ejecuta tu código en un sandbox real. DAKI detecta tus errores y te guía al siguiente nivel con IA táctica en español.
          </p>
          <div className="mt-6 h-px bg-gradient-to-r from-[#00FF41]/20 via-transparent to-transparent" />
        </header>

        {/* 3 Pilares */}
        <section className="mb-14">
          <p className="text-[8px] tracking-[0.55em] text-[#00FF41]/25 uppercase mb-6">
            {'// LO QUE NOS HACE DIFERENTES'}
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            {PILARES.map(({ glyph, color, title, tagline, body, stat }) => (
              <div
                key={title}
                className="relative border p-5 flex flex-col"
                style={{ borderColor: `${color}22`, background: `${color}04` }}
              >
                <div
                  className="absolute top-0 left-0 right-0 h-px"
                  style={{ background: `linear-gradient(90deg,transparent,${color}50,transparent)` }}
                />
                <div className="flex items-center gap-3 mb-3">
                  <span className="text-3xl font-black" style={{ color, textShadow: `0 0 20px ${color}40` }}>
                    {glyph}
                  </span>
                  <div>
                    <h3 className="text-sm font-black tracking-[0.1em] uppercase" style={{ color }}>{title}</h3>
                    <p className="text-[10px] font-bold" style={{ color: `${color}80` }}>{tagline}</p>
                  </div>
                </div>
                <p className="text-[11px] leading-relaxed text-white/38 flex-1 mb-3">{body}</p>
                <div
                  className="pt-2.5 border-t text-[9px] tracking-[0.3em] uppercase"
                  style={{ borderColor: `${color}15`, color: `${color}40` }}
                >
                  ▸ {stat}
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Áreas */}
        <section className="mb-14">
          <p className="text-[8px] tracking-[0.55em] text-[#00FF41]/25 uppercase mb-6">
            {'// ÁREAS DE ENTRENAMIENTO'}
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
            {AREAS.map(({ name, count }) => (
              <div
                key={name}
                className="border border-[#00FF41]/10 px-4 py-3 flex items-center justify-between"
                style={{ background: 'rgba(0,255,65,0.02)' }}
              >
                <span className="text-[10px] tracking-wide text-white/55">{name}</span>
                <span className="text-[9px] tracking-[0.3em] text-[#00FF41]/40 shrink-0 ml-2">{count}</span>
              </div>
            ))}
          </div>
          <div
            className="mt-3 px-4 py-3 border border-[#00FF41]/10 text-center"
            style={{ background: 'rgba(0,255,65,0.02)' }}
          >
            <span className="text-[10px] tracking-[0.3em] text-[#00FF41]/35 uppercase">
              Total: 195 misiones · 1 Boss Final · Certificación de Operador
            </span>
          </div>
        </section>

        {/* CTA */}
        <div
          className="p-6 border-l-2 mb-10"
          style={{ borderColor: '#00FF41', background: 'rgba(0,255,65,0.03)' }}
        >
          <p className="text-[8px] tracking-[0.5em] text-[#00FF41]/30 uppercase mb-3">{'// SIGUIENTE PASO'}</p>
          <p className="text-base font-black text-white/80 uppercase tracking-wide mb-4">
            Las primeras 10 misiones son gratis.
          </p>
          <div className="flex flex-col sm:flex-row gap-3">
            <Link
              href="/register"
              className="text-[9px] tracking-[0.4em] uppercase border border-[#00FF41]/40 px-6 py-3 text-[#00FF41] hover:bg-[#00FF41]/08 hover:border-[#00FF41]/70 transition-all duration-200 text-center"
            >
              {'[[ EMPEZAR GRATIS ]]'}
            </Link>
            <Link
              href="/precios"
              className="text-[9px] tracking-[0.35em] uppercase text-[#00FF41]/35 hover:text-[#00FF41]/65 transition-colors py-3 text-center"
            >
              Ver planes →
            </Link>
          </div>
        </div>

        {/* Footer nav */}
        <div className="pt-6 border-t border-[#00FF41]/8 flex items-center justify-between">
          <Link href="/" className="text-[#00FF41]/30 text-[9px] tracking-[0.3em] uppercase hover:text-[#00FF41]/60 transition-colors">
            ← NEXO CENTRAL
          </Link>
          <Link href="/blog" className="text-[#00FF41]/30 text-[9px] tracking-[0.3em] uppercase hover:text-[#00FF41]/60 transition-colors">
            INTEL CODEX →
          </Link>
        </div>
      </div>
    </main>
  )
}
