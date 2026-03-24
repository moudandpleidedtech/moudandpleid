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
        /* ── Phosphor title flicker (8 s) ───────────────────────────── */
        @keyframes title-flicker {
          0%, 90%, 100% { opacity: 1;    }
          93%           { opacity: 0.80; }
          96%           { opacity: 1;    }
          98%           { opacity: 0.60; }
        }
        .hero-title { animation: title-flicker 6s ease-in-out infinite; }

        /* ── Canal rojo: ciclo 2.8 s, glitch en 70-82 % ────────────── */
        @keyframes hero-glitch-r {
          0%,   69.9% { clip-path: inset(100% 0 0 0); opacity: 0;   transform: translate(0);         }
          70%         { clip-path: inset(38% 0 48% 0); opacity: 1;   transform: translate(-6px, 0);   }
          72%         { clip-path: inset(5%  0 78% 0); opacity: 1;   transform: translate( 7px, 2px); }
          74%         { clip-path: inset(65% 0 12% 0); opacity: 1;   transform: translate(-5px,-2px); }
          76%         { clip-path: inset(22% 0 58% 0); opacity: 1;   transform: translate( 8px, 0);   }
          78%         { clip-path: inset(50% 0 28% 0); opacity: 1;   transform: translate(-6px, 3px); }
          80%         { clip-path: inset(30% 0 45% 0); opacity: 1;   transform: translate( 5px,-1px); }
          82%, 100%   { clip-path: inset(100% 0 0 0); opacity: 0;   transform: translate(0);         }
        }

        /* ── Canal verde: 2 frames detrás ──────────────────────────── */
        @keyframes hero-glitch-g {
          0%,   73.9% { clip-path: inset(100% 0 0 0); opacity: 0;   transform: translate(0);         }
          74%         { clip-path: inset(18% 0 60% 0); opacity: 0.9; transform: translate( 6px, 0);   }
          76%         { clip-path: inset(62% 0 15% 0); opacity: 0.9; transform: translate(-7px, 2px); }
          78%         { clip-path: inset(35% 0 40% 0); opacity: 0.9; transform: translate( 5px,-3px); }
          80%         { clip-path: inset(78% 0 8%  0); opacity: 0.9; transform: translate(-6px, 0);   }
          83%, 100%   { clip-path: inset(100% 0 0 0); opacity: 0;   transform: translate(0);         }
        }

        .hero-glitch-r {
          color: #FF0033;
          text-shadow: 0 0 12px rgba(255,0,51,0.8), 0 0 24px rgba(255,0,51,0.4);
          animation: hero-glitch-r 2.8s linear infinite;
          will-change: transform, clip-path, opacity;
        }
        .hero-glitch-g {
          color: #00FF41;
          text-shadow: 0 0 12px rgba(0,255,65,0.7), 0 0 24px rgba(0,255,65,0.3);
          animation: hero-glitch-g 2.8s linear infinite;
          will-change: transform, clip-path, opacity;
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
