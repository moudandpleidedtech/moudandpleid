/**
 * Footer.tsx — Pie de Página del Búnker · DAKI EdTech
 * ──────────────────────────────────────────────────────
 * Minimalista. Borde superior gris oscuro.
 * Derecha: texto casi invisible → verde neón en hover.
 */

export default function Footer() {
  return (
    <footer className="bg-[#0A0A0A] font-mono border-t border-white/[0.06] px-6 md:px-12 py-8">
      <div className="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">

        {/* Izquierda */}
        <p className="text-[#00FF41]/20 text-xs tracking-[0.3em]">
          © 2026 DAKIedtech. Todos los sistemas operativos.
        </p>

        {/* Derecha — casi invisible, verde en hover */}
        <p className="text-white/10 text-xs tracking-[0.3em] transition-colors duration-300 hover:text-[#00FF41] hover:[text-shadow:0_0_8px_rgba(0,255,65,0.6)]">
          Construido con precisión. Desarrollado por QA.
        </p>

      </div>
    </footer>
  )
}
