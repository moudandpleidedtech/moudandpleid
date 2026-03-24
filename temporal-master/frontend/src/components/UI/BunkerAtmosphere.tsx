/**
 * BunkerAtmosphere.tsx — Filtro global CRT · DAKI EdTech
 * ───────────────────────────────────────────────────────
 * Dos capas superpuestas, pointer-events: none, z-50.
 *
 *  Capa 1 — Barrido de haz (CRT beam sweep)
 *    Banda semitransparente de fósforo verde que desciende
 *    continuamente. Simula el tubo de rayos catódicos de un
 *    monitor militar de los 90s.
 *    GPU-acelerado: solo usa transform: translateY + opacity.
 *
 *  Capa 2 — Ruido estático (SVG fractal noise grain)
 *    SVG feTurbulence 200×200 px en data URI, tiled.
 *    Opacidad ~2.5 % con parpadeo discreto (steps) — textura
 *    viva sin afectar legibilidad.
 *
 *  ✓ will-change declarado en ambas capas → zero layout thrash
 *  ✓ prefers-reduced-motion: desactiva beam, freeze grain
 *  ✓ Solo modifica opacity/transform → seguro en móviles
 */

// SVG inline: feTurbulence fractalNoise 200×200, tileable, seed fijo
// URL-encoded para backgroundImage sin dependencias externas
const GRAIN_SVG =
  "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E" +
  "%3Cfilter id='n'%3E" +
  "%3CfeTurbulence type='fractalNoise' baseFrequency='0.68' numOctaves='4' stitchTiles='stitch'/%3E" +
  "%3C/filter%3E" +
  "%3Crect width='200' height='200' filter='url(%23n)'/%3E" +
  "%3C/svg%3E"

export default function BunkerAtmosphere() {
  return (
    <>
      <style>{`
        /* ── 1. Barrido de haz CRT ──────────────────────────────────── */
        @keyframes bunker-beam-sweep {
          0%   { transform: translateY(-38vh); }
          100% { transform: translateY(120vh); }
        }
        .bunker-beam {
          animation: bunker-beam-sweep 9s linear infinite;
          will-change: transform;
        }

        /* ── 2. Grain flicker (steps = saltos discretos, no interpolación) */
        @keyframes bunker-grain-flicker {
          0%   { opacity: 0.045; }
          33%  { opacity: 0.028; }
          66%  { opacity: 0.040; }
          100% { opacity: 0.045; }
        }
        .bunker-grain {
          animation: bunker-grain-flicker 0.20s steps(3, end) infinite;
          will-change: opacity;
        }

        /* ── Accesibilidad: reducción de movimiento ──────────────────── */
        @media (prefers-reduced-motion: reduce) {
          .bunker-beam  { animation: none; opacity: 0; }
          .bunker-grain { animation: none; opacity: 0.020; }
        }
      `}</style>

      {/* ── Capa 1: Barrido de haz fósforo verde ─────────────────────────────── */}
      <div
        aria-hidden="true"
        className="bunker-beam fixed left-0 right-0 pointer-events-none z-50"
        style={{
          top: 0,
          height: '38vh',
          background: 'linear-gradient(to bottom, transparent 0%, rgba(0,255,65,0.03) 20%, rgba(0,255,65,0.07) 45%, rgba(0,255,65,0.09) 50%, rgba(0,255,65,0.07) 55%, rgba(0,255,65,0.03) 80%, transparent 100%)',
        }}
      />

      {/* ── Capa 2: Ruido estático SVG grain ─────────────────────────────────── */}
      <div
        aria-hidden="true"
        className="bunker-grain fixed inset-0 pointer-events-none z-50"
        style={{
          backgroundImage: `url("${GRAIN_SVG}")`,
          backgroundRepeat: 'repeat',
          backgroundSize: '200px 200px',
        }}
      />
    </>
  )
}
