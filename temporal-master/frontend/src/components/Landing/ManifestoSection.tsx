'use client'

/**
 * ManifestoSection.tsx — La Anatomía del Nexo · DAKI EdTech
 * ──────────────────────────────────────────────────────────
 * Grid 2×2 con efecto "Iluminación Táctica" (Mouse Spotlight).
 *
 * Mecánica:
 *   • Desktop (pointer: fine): radial-gradient sigue al cursor en tiempo
 *     real usando CSS custom props --gx/--gy. Sin React state → cero
 *     re-renders durante el mousemove. Solo se usa el atributo data-lit
 *     para activar/desactivar las transiciones de borde vía CSS.
 *
 *   • Mobile (pointer: coarse): spotlight desactivado completamente.
 *     El panel tiene un borde estático muy tenue que se activa con :active
 *     (touch) para dar feedback táctil.
 *
 * Stack de capas dentro de cada tarjeta (bottom → top):
 *   1. Fondo #0D0D0D (background de .daki-card)
 *   2. ::before con radial-gradient (z-index: -1, dentro del isolate)
 *   3. Contenido de texto (non-positioned → encima por defecto)
 */

import { useRef, useEffect, useCallback } from 'react'

// ─── Data ──────────────────────────────────────────────────────────────────────

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

/**
 * TacticalCard — Panel de metal con iluminación táctica.
 *
 * Implementación sin estado React para el seguimiento del cursor:
 *   1. onMouseMove → style.setProperty('--gx'/'--gy') en el elemento DOM
 *   2. setAttribute('data-lit', '1') activa las transiciones CSS
 *   3. onMouseLeave → removeAttribute('data-lit')
 *
 * pointer: fine se verifica en useEffect (client-only). En pointer: coarse
 * el handler regresa inmediatamente sin tocar el DOM → CSS se encarga.
 */
function TacticalCard({ letter, title, body }: CardData) {
  const cardRef  = useRef<HTMLDivElement>(null)
  const finePtr  = useRef(false)  // true solo en mouse desktop

  useEffect(() => {
    finePtr.current = window.matchMedia('(pointer: fine)').matches
  }, [])

  const handleMouseMove = useCallback((e: React.MouseEvent<HTMLDivElement>) => {
    if (!finePtr.current) return
    const el = cardRef.current
    if (!el) return
    const r = el.getBoundingClientRect()
    // Actualiza coordenadas Y activa spotlight en una sola pasada
    el.style.setProperty('--gx', `${e.clientX - r.left}px`)
    el.style.setProperty('--gy', `${e.clientY - r.top}px`)
    el.setAttribute('data-lit', '1')
  }, [])

  const handleMouseLeave = useCallback(() => {
    cardRef.current?.removeAttribute('data-lit')
  }, [])

  return (
    <div
      ref={cardRef}
      className="daki-card p-8 flex flex-col gap-5"
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

      <style>{`
        /* ── Panel base ────────────────────────────────────────────── */
        .daki-card {
          position: relative;
          isolation: isolate;           /* contiene el z-index del ::before */
          background: #0D0D0D;
          border: 1px solid rgba(0, 255, 65, 0.12);
          transition: border-color 0.30s ease, box-shadow 0.30s ease;
        }

        /* ── Capa de spotlight (::before, z-index: -1) ─────────────── */
        /* Con isolation: isolate, z-index: -1 queda ENTRE el fondo del
           panel y el contenido de texto — nunca cubre el texto. */
        .daki-card::before {
          content: "";
          position: absolute;
          inset: 0;
          z-index: -1;
          background: radial-gradient(
            520px circle at var(--gx, -999px) var(--gy, -999px),
            rgba(0, 255, 65, 0.09),
            transparent 42%
          );
          opacity: 0;
          transition: opacity 0.18s ease;
          will-change: opacity;
          pointer-events: none;
        }

        /* ── Estado iluminado (data-lit presente) ──────────────────── */
        .daki-card[data-lit] {
          border-color: rgba(0, 255, 65, 0.52);
          box-shadow:
            0 0 32px rgba(0, 255, 65, 0.06),
            inset 0 0 40px rgba(0, 255, 65, 0.025);
        }
        .daki-card[data-lit]::before       { opacity: 1; }
        .daki-card[data-lit] .card-content { opacity: 1; }
        .daki-card[data-lit] .card-letter  {
          text-shadow:
            0 0 20px rgba(0, 255, 65, 0.85),
            0 0 42px rgba(0, 255, 65, 0.45);
        }

        /* ── Estado por defecto del contenido ──────────────────────── */
        .card-content {
          opacity: 0.72;
          transition: opacity 0.30s ease;
        }
        .card-letter {
          transition: text-shadow 0.30s ease;
          text-shadow: 0 0 8px rgba(0, 255, 65, 0.28);
        }

        /* ── Mobile: pointer: coarse — spotlight OFF ───────────────── */
        /* Sin rastreo JS. El borde se activa con :active (toque). */
        @media (pointer: coarse) {
          .daki-card::before { display: none; }

          .daki-card {
            border-color: rgba(0, 255, 65, 0.10);
            transition: border-color 0.12s ease, box-shadow 0.12s ease;
          }
          .daki-card:active {
            border-color: rgba(0, 255, 65, 0.46);
            box-shadow:
              0 0 20px rgba(0, 255, 65, 0.08),
              inset 0 0 20px rgba(0, 255, 65, 0.03);
          }
          .daki-card:active .card-content { opacity: 1; }
          .daki-card:active .card-letter  {
            text-shadow:
              0 0 18px rgba(0, 255, 65, 0.75),
              0 0 36px rgba(0, 255, 65, 0.38);
          }
          /* Visible por defecto en mobile — sin hover */
          .card-content { opacity: 0.85; }
        }
      `}</style>

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
