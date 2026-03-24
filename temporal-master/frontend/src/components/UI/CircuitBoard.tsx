/**
 * CircuitBoard.tsx — Overlay de circuito eléctrico · DAKI EdTech
 * ───────────────────────────────────────────────────────────────
 * Fixed, pointer-events-none, z-[5].
 * Trazos SVG en bordes laterales + pulsos eléctricos animados.
 * Server Component: sin hooks, sin APIs del browser.
 *
 * Layout (viewBox 0 0 1440 900):
 *   Izquierda: columna x=60, horizontales, L-connections
 *   Derecha:   columna x=1380, horizontales, L-connections
 *   Fondo:     trazo horizontal inferior + drops
 *   Esquinas:  brackets decorativos en los 4 vértices
 */

export default function CircuitBoard() {
  return (
    <div aria-hidden="true" className="fixed inset-0 pointer-events-none z-[5]">
      <svg
        className="w-full h-full"
        viewBox="0 0 1440 900"
        preserveAspectRatio="xMidYMid slice"
        xmlns="http://www.w3.org/2000/svg"
      >
        <defs>
          {/* Glow filter para los pulsos */}
          <filter id="cg" x="-300%" y="-300%" width="700%" height="700%">
            <feGaussianBlur stdDeviation="5" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
          {/* Glow suave para los nodos */}
          <filter id="ng" x="-200%" y="-200%" width="500%" height="500%">
            <feGaussianBlur stdDeviation="2.5" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>

        {/* ── Trazos de circuito ─────────────────────────────────────── */}
        <g stroke="#00FF41" strokeWidth="0.7" fill="none" opacity="0.18">
          {/* Columna izquierda — trazo vertical completo */}
          <line id="p-lv" x1="60" y1="0" x2="60" y2="900" />
          {/* Horizontales izquierda */}
          <line id="p-lh1" x1="0" y1="220" x2="260" y2="220" />
          <line id="p-lh2" x1="0" y1="520" x2="160" y2="520" />
          {/* Conector L izquierda */}
          <path id="p-ll1" d="M 160 220 L 160 520" />
          {/* Rama izquierda baja */}
          <path id="p-ll2" d="M 60 680 L 60 900" />

          {/* Columna derecha — trazo vertical completo */}
          <line id="p-rv" x1="1380" y1="0" x2="1380" y2="900" />
          {/* Horizontales derecha */}
          <line id="p-rh1" x1="1180" y1="310" x2="1440" y2="310" />
          <line id="p-rh2" x1="1280" y1="620" x2="1440" y2="620" />
          {/* Conector vertical derecha */}
          <path id="p-rl1" d="M 1280 0 L 1280 310" />
          <path id="p-rl2" d="M 1280 620 L 1280 900" />

          {/* Trazo inferior */}
          <path id="p-bh" d="M 200 850 L 1240 850" />
          <line x1="200" y1="850" x2="200" y2="900" />
          <line x1="1240" y1="850" x2="1240" y2="900" />
        </g>

        {/* ── Brackets de esquina ────────────────────────────────────── */}
        <g stroke="#00FF41" strokeWidth="1" fill="none" opacity="0.22">
          {/* Top-left */}
          <path d="M 0 36 L 36 36 L 36 0" />
          {/* Top-right */}
          <path d="M 1404 0 L 1404 36 L 1440 36" />
          {/* Bottom-left */}
          <path d="M 0 864 L 36 864 L 36 900" />
          {/* Bottom-right */}
          <path d="M 1440 864 L 1404 864 L 1404 900" />
        </g>

        {/* ── Micro-chips (rectángulos en nodos clave) ───────────────── */}
        <g stroke="#00FF41" strokeWidth="0.6" fill="#00FF41" fillOpacity="0.04" opacity="0.30">
          <rect x="52"   y="212" width="16" height="16" />
          <rect x="152"  y="212" width="16" height="16" />
          <rect x="152"  y="512" width="16" height="16" />
          <rect x="1372" y="302" width="16" height="16" />
          <rect x="1272" y="302" width="16" height="16" />
          <rect x="1272" y="612" width="16" height="16" />
        </g>

        {/* ── Nodos de conexión ──────────────────────────────────────── */}
        <g filter="url(#ng)" fill="#00FF41" opacity="0.40">
          <circle cx="60"   cy="220" r="3" />
          <circle cx="160"  cy="220" r="3" />
          <circle cx="160"  cy="520" r="3" />
          <circle cx="60"   cy="520" r="2.5" />
          <circle cx="1380" cy="310" r="3" />
          <circle cx="1280" cy="310" r="3" />
          <circle cx="1280" cy="620" r="3" />
          <circle cx="1380" cy="620" r="2.5" />
          <circle cx="200"  cy="850" r="2.5" />
          <circle cx="1240" cy="850" r="2.5" />
        </g>

        {/* ── Pulsos eléctricos animados ─────────────────────────────── */}
        <g filter="url(#cg)" className="circuit-pulse">
          {/* Pulso: columna izquierda ↓ */}
          <circle r="3.5" fill="#00FF41" opacity="0.88">
            <animateMotion dur="9s" repeatCount="indefinite" calcMode="linear">
              <mpath href="#p-lv" />
            </animateMotion>
          </circle>

          {/* Pulso: horizontal izquierda → */}
          <circle r="3" fill="#00FF41" opacity="0.80">
            <animateMotion dur="2.8s" repeatCount="indefinite" calcMode="linear" begin="1s">
              <mpath href="#p-lh1" />
            </animateMotion>
          </circle>

          {/* Pulso: L-connector izquierda ↓ */}
          <circle r="2.5" fill="#00FF41" opacity="0.75">
            <animateMotion dur="3.2s" repeatCount="indefinite" calcMode="linear" begin="2.5s">
              <mpath href="#p-ll1" />
            </animateMotion>
          </circle>

          {/* Pulso: columna derecha ↓ */}
          <circle r="3.5" fill="#00FF41" opacity="0.85">
            <animateMotion dur="8s" repeatCount="indefinite" calcMode="linear" begin="0.5s">
              <mpath href="#p-rv" />
            </animateMotion>
          </circle>

          {/* Pulso: horizontal derecha → */}
          <circle r="3" fill="#00FF41" opacity="0.80">
            <animateMotion dur="3s" repeatCount="indefinite" calcMode="linear" begin="2s">
              <mpath href="#p-rh1" />
            </animateMotion>
          </circle>

          {/* Pulso: trazo inferior → */}
          <circle r="3" fill="#00FF41" opacity="0.72">
            <animateMotion dur="6s" repeatCount="indefinite" calcMode="linear" begin="1.5s">
              <mpath href="#p-bh" />
            </animateMotion>
          </circle>

          {/* Pulso: columna derecha corta (arriba) ↓ */}
          <circle r="2.5" fill="#00FF41" opacity="0.70">
            <animateMotion dur="3.5s" repeatCount="indefinite" calcMode="linear" begin="3.5s">
              <mpath href="#p-rl1" />
            </animateMotion>
          </circle>
        </g>
      </svg>
    </div>
  )
}
