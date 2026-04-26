'use client'

export default function GlitchTitle() {
  const layerBase =
    'absolute inset-0 text-4xl sm:text-5xl md:text-7xl font-bold ' +
    'tracking-[0.08em] uppercase leading-none pointer-events-none select-none'

  return (
    <div className="relative overflow-x-hidden mb-4">
      <style>{`
        @keyframes title-flicker {
          0%, 90%, 100% { opacity: 1;    }
          93%           { opacity: 0.80; }
          96%           { opacity: 1;    }
          98%           { opacity: 0.60; }
        }
        .hero-title { animation: title-flicker 6s ease-in-out infinite; }

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

        @media (prefers-reduced-motion: reduce) {
          .hero-glitch-r,
          .hero-glitch-g { animation: none; opacity: 0; }
          .hero-title     { animation: none; }
        }
      `}</style>

      <h1 aria-hidden="true" className={`hero-glitch-r ${layerBase}`}>
        EL NEXO<br />ESTÁ EN LÍNEA.
      </h1>

      <h1 aria-hidden="true" className={`hero-glitch-g ${layerBase}`}>
        EL NEXO<br />ESTÁ EN LÍNEA.
      </h1>

      <h1 className="hero-title text-4xl sm:text-5xl md:text-7xl font-bold tracking-[0.08em] uppercase leading-none text-[#00FF41]">
        EL NEXO
        <br />
        <span
          className="text-[#00FF41]"
          style={{ textShadow: '0 0 28px rgba(0,255,65,0.5), 0 0 56px rgba(0,255,65,0.2)' }}
        >
          ESTÁ EN LÍNEA.
        </span>
      </h1>
    </div>
  )
}
