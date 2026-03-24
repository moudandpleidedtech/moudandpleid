'use client'

/**
 * ManifestoSection.tsx — La Anatomía del Nexo · DAKI EdTech
 * ──────────────────────────────────────────────────────────
 * Grid 2×2 con efecto "Iluminación Táctica" (Mouse Spotlight).
 *
 * El spotlight se aplica directamente sobre el background del elemento
 * via el.style.background en mousemove — sin ::before, sin content:"",
 * sin hydration mismatch. El CSS de las clases vive en globals.css.
 *
 * Desktop (pointer: fine): gradiente radial sigue al cursor sin
 * re-renders React (manipulación DOM directa vía useRef).
 * Mobile  (pointer: coarse): sin spotlight; :active en globals.css
 * activa borde + glow para feedback táctil.
 */

import { useRef, useEffect, useCallback } from 'react'

const CARDS = [
  {
    letter: 'D',
    title:  'Desarrollo',
    body:   'Construcción masiva. El código visto como una herramienta de creación, no como teoría pasiva.',
  },
  {
    letter: 'A',
    title:  'Arquitectura',
    body:   'Estructuras de élite. Diseño de sistemas preparados para escalar y resistir en producción real.',
  },
  {
    letter: 'K',
    title:  'Knowledge',
    body:   'Sabiduría táctica. El conocimiento no se memoriza, se descifra rompiendo sistemas.',
  },
  {
    letter: 'I',
    title:  'Inteligencia',
    body:   'Núcleo adaptativo. Una IA que analiza tu lógica en tiempo real para guiar tu evolución como Operador.',
  },
] as const

type CardData = (typeof CARDS)[number]

// ─── TacticalCard ──────────────────────────────────────────────────────────────

function TacticalCard({ letter, title, body }: CardData) {
  const cardRef = useRef<HTMLDivElement>(null)
  const finePtr = useRef(false)

  useEffect(() => {
    finePtr.current = window.matchMedia('(pointer: fine)').matches
  }, [])

  const handleMouseMove = useCallback((e: React.MouseEvent<HTMLDivElement>) => {
    if (!finePtr.current) return
    const el = cardRef.current
    if (!el) return
    const r = el.getBoundingClientRect()
    const x = e.clientX - r.left
    const y = e.clientY - r.top
    // El background del elemento ES el spotlight — no necesita ::before ni content
    el.style.background = `radial-gradient(520px circle at ${x}px ${y}px, rgba(0,255,65,0.09), transparent 42%), #0D0D0D`
    el.setAttribute('data-lit', '1')
  }, [])

  const handleMouseLeave = useCallback(() => {
    const el = cardRef.current
    if (!el) return
    el.removeAttribute('data-lit')
    el.style.background = '#0D0D0D'
  }, [])

  return (
    <div
      ref={cardRef}
      className="daki-card p-5 md:p-8 flex flex-col gap-5"
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
    >
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

      {/* Contenido */}
      <div className="card-content">
        <h3 className="text-[#00FF41] text-sm font-bold tracking-[0.3em] uppercase mb-3">
          {title}
        </h3>
        <div className="h-px bg-[#00FF41]/15 mb-4" />
        <p className="text-[#C0C0C0]/80 text-sm leading-6 tracking-wide">
          {body}
        </p>
      </div>
    </div>
  )
}

// ─── ManifestoSection ──────────────────────────────────────────────────────────

export default function ManifestoSection() {
  return (
    <section className="bg-[#0A0A0A] font-mono px-6 md:px-12 py-24 relative overflow-hidden">

      {/* ── Línea decorativa superior ────────────────────────────────────────── */}
      <div className="flex items-center gap-4 mb-16 max-w-5xl mx-auto">
        <div className="h-px flex-1 bg-gradient-to-r from-transparent via-[#00FF41]/20 to-transparent" />
        <span className="text-[#00FF41]/30 text-xs tracking-[0.5em] uppercase shrink-0">
          NEXO — SECTOR ALFA
        </span>
        <div className="h-px flex-1 bg-gradient-to-r from-transparent via-[#00FF41]/20 to-transparent" />
      </div>

      {/* ── Título de sección ────────────────────────────────────────────────── */}
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

      {/* ── Grid 2×2 ─────────────────────────────────────────────────────────── */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 max-w-5xl mx-auto">
        {CARDS.map(card => (
          <TacticalCard key={card.letter} {...card} />
        ))}
      </div>

      {/* ── Footer de sección ────────────────────────────────────────────────── */}
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
