'use client'

/**
 * GlitchTitle.tsx — Aberración cromática sobre el titular · DAKI EdTech
 * ───────────────────────────────────────────────────────────────────────
 * Renderiza el h1 "EL SISTEMA / TIENE FALLOS." con tres capas superpuestas:
 *
 *   Layer R (aria-hidden) — copia del texto en #FF0033, animada con
 *                           clip-path + translateX, mezclada con screen
 *   Layer G (aria-hidden) — copia en #00FF41, desfasada 2 frames
 *                           respecto al canal rojo → aberración real
 *   Main h1               — siempre legible, con flicker de fósforo sutil
 *
 * ── Timing del glitch (ciclo 4 s) ────────────────────────────────────────
 *   0 – 87.9 %  → capas ocultas (clip-path: inset(100% 0 0 0))
 *   88 – 93 %   → burst: 6 frames × 40 ms (1 % × 4 000 ms)
 *   93 – 100 %  → ocultas de nuevo
 *
 *   El truco del 87.9 %: interpolar 0.1 % × 4 s = 4 ms desde oculto
 *   hasta el primer frame de glitch es < 1 frame @ 60 fps → INSTANTE.
 *   La capa verde empieza en 89.9 % → 2 frames de desfase → chromatic.
 *
 * ✓ overflow-x: hidden en wrapper — sin desbordamiento horizontal en móvil
 * ✓ will-change: transform, clip-path, opacity — GPU-accelerated
 * ✓ prefers-reduced-motion: glitch off, flicker off
 */

export default function GlitchTitle() {
  const layerBase =
    'absolute inset-0 text-4xl sm:text-5xl md:text-7xl font-bold ' +
    'tracking-[0.08em] uppercase leading-none pointer-events-none select-none'

  return (
    <div className="relative overflow-x-hidden mb-4">
      <style>{`
        /* ── Phosphor title flicker (8 s, muy sutil) ────────────────── */
        @keyframes title-flicker {
          0%, 96%, 100% { opacity: 1;    }
          97%           { opacity: 0.85; }
          98%           { opacity: 1;    }
          99%           { opacity: 0.70; }
        }
        .hero-title { animation: title-flicker 8s ease-in-out infinite; }

        /* ── Canal rojo ─────────────────────────────────────────────── */
        @keyframes hero-glitch-r {
          0%,  87.9% { clip-path: inset(100% 0 0 0); opacity: 0;    transform: translate(0);        }
          88%        { clip-path: inset(42% 0 44% 0); opacity: 0.85; transform: translate(-4px, 0);  }
          89%        { clip-path: inset(8%  0 80% 0); opacity: 0.85; transform: translate( 5px, 1px);}
          90%        { clip-path: inset(70% 0 15% 0); opacity: 0.85; transform: translate(-3px,-1px);}
          91%        { clip-path: inset(25% 0 55% 0); opacity: 0.85; transform: translate( 4px, 0);  }
          92%        { clip-path: inset(56% 0 30% 0); opacity: 0.85; transform: translate(-5px, 2px);}
          93%, 100%  { clip-path: inset(100% 0 0 0); opacity: 0;    transform: translate(0);        }
        }

        /* ── Canal verde (2 frames de retraso → aberración cromática) ─ */
        @keyframes hero-glitch-g {
          0%,  89.9% { clip-path: inset(100% 0 0 0); opacity: 0;    transform: translate(0);        }
          90%        { clip-path: inset(20% 0 62% 0); opacity: 0.70; transform: translate( 4px, 0);  }
          91%        { clip-path: inset(65% 0 18% 0); opacity: 0.70; transform: translate(-5px, 1px);}
          92%        { clip-path: inset(38% 0 38% 0); opacity: 0.70; transform: translate( 3px,-2px);}
          93%        { clip-path: inset(80% 0 5%  0); opacity: 0.70; transform: translate(-4px, 0);  }
          95%, 100%  { clip-path: inset(100% 0 0 0); opacity: 0;    transform: translate(0);        }
        }

        .hero-glitch-r {
          color: #FF0033;
          text-shadow: 0 0 8px rgba(255,0,51,0.5);
          animation: hero-glitch-r 4s linear infinite;
          will-change: transform, clip-path, opacity;
          mix-blend-mode: screen;
        }
        .hero-glitch-g {
          color: #00FF41;
          text-shadow: 0 0 8px rgba(0,255,65,0.4);
          animation: hero-glitch-g 4s linear infinite;
          will-change: transform, clip-path, opacity;
          mix-blend-mode: screen;
        }

        /* ── Accesibilidad ───────────────────────────────────────────── */
        @media (prefers-reduced-motion: reduce) {
          .hero-glitch-r,
          .hero-glitch-g { animation: none; opacity: 0; }
          .hero-title     { animation: none; }
        }
      `}</style>

      {/* Capa roja — canal de aberración */}
      <h1 aria-hidden="true" className={`hero-glitch-r ${layerBase}`}>
        EL SISTEMA<br />TIENE FALLOS.
      </h1>

      {/* Capa verde — canal de aberración desfasado */}
      <h1 aria-hidden="true" className={`hero-glitch-g ${layerBase}`}>
        EL SISTEMA<br />TIENE FALLOS.
      </h1>

      {/* Texto principal — siempre encima y legible */}
      <h1 className="hero-title text-4xl sm:text-5xl md:text-7xl font-bold tracking-[0.08em] uppercase leading-none text-[#00FF41]">
        EL SISTEMA
        <br />
        <span
          className="text-[#FF0033]"
          style={{ textShadow: '0 0 20px rgba(255,0,51,0.5)' }}
        >
          TIENE FALLOS.
        </span>
      </h1>
    </div>
  )
}
