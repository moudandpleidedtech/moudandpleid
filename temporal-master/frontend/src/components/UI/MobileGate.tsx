/**
 * MobileGate.tsx — Bloqueo elegante en móvil · DAKI EdTech
 * ──────────────────────────────────────────────────────────
 * CSS-only: no hooks, no useEffect, sin hydration mismatch.
 * En <768px muestra el mensaje táctico y oculta el contenido.
 * En ≥768px renderiza los children con normalidad.
 *
 * Aplicar en páginas con editor de código o mecánicas de juego
 * que requieren viewport amplio (arena, enigma, boss, sector, etc.)
 */

export default function MobileGate({ children }: { children: React.ReactNode }) {
  return (
    <>
      {/* ── Bloqueo móvil (<768px) ──────────────────────────────────── */}
      <div className="md:hidden min-h-screen bg-[#0A0A0A] font-mono flex flex-col items-center justify-center px-8 relative overflow-hidden">

        {/* Grid táctica de fondo */}
        <div
          className="absolute inset-0 pointer-events-none opacity-[0.025]"
          style={{
            backgroundImage:
              'linear-gradient(#00FF41 1px,transparent 1px),linear-gradient(90deg,#00FF41 1px,transparent 1px)',
            backgroundSize: '48px 48px',
          }}
        />

        {/* Vignette */}
        <div
          className="absolute inset-0 pointer-events-none"
          style={{ background: 'radial-gradient(ellipse at center,transparent 40%,rgba(10,10,10,0.9) 100%)' }}
        />

        <div className="relative z-10 text-center max-w-xs">

          {/* Logo */}
          <p className="text-[#00FF41] text-xs font-bold tracking-[0.5em] uppercase mb-12 opacity-60">
            DAKIedtech
          </p>

          {/* Icono — monitor */}
          <div className="flex justify-center mb-8">
            <svg
              width="48" height="48"
              viewBox="0 0 24 24"
              fill="none"
              stroke="#00FF41"
              strokeWidth="1"
              strokeLinecap="round"
              strokeLinejoin="round"
              opacity="0.45"
            >
              <rect x="2" y="3" width="20" height="14" rx="2" />
              <line x1="8" y1="21" x2="16" y2="21" />
              <line x1="12" y1="17" x2="12" y2="21" />
            </svg>
          </div>

          {/* Código de error */}
          <p className="text-[#FF0033]/50 text-[10px] tracking-[0.6em] uppercase mb-5">
            {'// ERROR — RESOLUCIÓN INSUFICIENTE'}
          </p>

          {/* Mensaje principal */}
          <h1 className="text-2xl font-bold tracking-[0.08em] uppercase text-white leading-tight mb-5">
            ESTA OPERACIÓN
            <br />
            <span
              className="text-[#00FF41]"
              style={{ textShadow: '0 0 20px rgba(0,255,65,0.4)' }}
            >
              REQUIERE ESCRITORIO.
            </span>
          </h1>

          <p className="text-[#C0C0C0]/45 text-sm leading-6 mb-10">
            El Nexo Neural está optimizado para pantallas de 768px o más.
            El entrenamiento de élite no admite resoluciones reducidas.
          </p>

          {/* CTA */}
          <p className="text-[#00FF41]/25 text-[10px] tracking-[0.4em] uppercase leading-6">
            {'[ Accede desde un equipo de escritorio para continuar tu misión ]'}
          </p>

        </div>
      </div>

      {/* ── Contenido real (≥768px) ──────────────────────────────────── */}
      <div className="hidden md:contents">
        {children}
      </div>
    </>
  )
}
