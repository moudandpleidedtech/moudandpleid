'use client'

/**
 * MissionsSection.tsx — Zonas de Operación · DAKI EdTech
 * ─────────────────────────────────────────────────────────
 * Grid 3 cols (desktop) / 1 col (mobile).
 * Tarjeta 1: activa con glow verde.
 * Tarjetas 2–3: bloqueadas, opacidad 60%, cursor-not-allowed en botón.
 */

import Link from 'next/link'

// ── Ícono de candado (SVG inline — sin dependencia externa) ───────────────────
function LockIcon() {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="12"
      height="12"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      className="inline-block mr-1.5 mb-0.5"
    >
      <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
      <path d="M7 11V7a5 5 0 0 1 10 0v4" />
    </svg>
  )
}

export default function MissionsSection() {
  return (
    <section className="bg-[#0A0A0A] font-mono px-6 md:px-12 py-24 relative overflow-hidden">

      <style>{`
        .mission-active {
          border: 1px solid rgba(0,255,65,0.35);
          background: #0D0D0D;
          transition: border-color 0.25s ease, box-shadow 0.25s ease;
        }
        .mission-active:hover {
          border-color: rgba(0,255,65,0.8);
          box-shadow: 0 0 32px rgba(0,255,65,0.1), 0 0 2px rgba(0,255,65,0.4);
        }
        .mission-active:hover .active-btn {
          border-color: #00FF41;
          box-shadow: 0 0 16px rgba(0,255,65,0.4);
          background: rgba(0,255,65,0.12);
        }
        .active-btn {
          transition: border-color 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
        }
        .mission-locked {
          border: 1px solid rgba(255,255,255,0.06);
          background: #0D0D0D;
          opacity: 0.6;
        }
      `}</style>

      <div className="max-w-6xl mx-auto">

        {/* ── Título de sección ───────────────────────────────────────────────── */}
        <div className="flex items-center gap-4 mb-12">
          <span className="text-[#00FF41] text-xs tracking-[0.5em]">{'▶'}</span>
          <h2 className="text-2xl sm:text-3xl md:text-4xl font-bold tracking-[0.1em] uppercase text-white">
            ZONAS DE OPERACIÓN
          </h2>
        </div>

        {/* Sub-label */}
        <p className="text-[#00FF41]/30 text-xs tracking-[0.4em] uppercase mb-10 -mt-8">
          {'// MÓDULOS DE ENTRENAMIENTO ACTIVOS Y CLASIFICADOS'}
        </p>

        {/* ── Grid ────────────────────────────────────────────────────────────── */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">

          {/* ── TARJETA 1 — ACTIVA ────────────────────────────────────────────── */}
          <div className="mission-active p-7 flex flex-col gap-5">

            {/* Badge */}
            <div className="inline-flex items-center gap-2 self-start px-3 py-1 bg-[#00FF41]/10 border border-[#00FF41]/30">
              <span className="w-1.5 h-1.5 rounded-full bg-[#00FF41] animate-pulse" />
              <span className="text-[#00FF41] text-[10px] tracking-[0.35em] uppercase font-bold">
                STATUS: ONLINE
              </span>
            </div>

            {/* Título */}
            <h3 className="text-[#00FF41] text-sm font-bold tracking-[0.2em] uppercase leading-6">
              OPERACIÓN ALFA:<br />
              <span className="text-white/90">Lógica y Sintaxis Core</span>
            </h3>

            {/* Separador */}
            <div className="h-px bg-[#00FF41]/15" />

            {/* Descripción */}
            <p className="text-[#C0C0C0]/70 text-sm leading-6 tracking-wide flex-1">
              Vence al Infinite Looper y domina las bases del código bajo fuego real.
            </p>

            {/* CTA */}
            <Link
              href="/login"
              className="active-btn block text-center border border-[#00FF41]/50 text-[#00FF41] text-xs tracking-[0.35em] uppercase px-4 py-3 bg-[#00FF41]/5"
            >
              {`[[ INICIAR MISIÓN ]]`}
            </Link>

          </div>

          {/* ── TARJETA 2 — BLOQUEADA (Hacking Ético) ────────────────────────── */}
          <div className="mission-locked p-7 flex flex-col gap-5">

            {/* Badge */}
            <div className="inline-flex items-center gap-2 self-start px-3 py-1 border border-[#FF0033]/25">
              <span className="text-[#FF0033]/60 text-[10px] tracking-[0.35em] uppercase font-bold">
                STATUS: CLASIFICADO
              </span>
            </div>

            {/* Título */}
            <h3 className="text-[#888]/80 text-sm font-bold tracking-[0.2em] uppercase leading-6">
              OPERACIÓN BETA:<br />
              <span className="text-white/50">Hacking Ético</span>
            </h3>

            {/* Separador */}
            <div className="h-px bg-white/6" />

            {/* Descripción */}
            <p className="text-[#888]/60 text-sm leading-6 tracking-wide flex-1">
              Aprende a construir sistemas rompiéndolos. Infiltración y seguridad ofensiva.
            </p>

            {/* Botón deshabilitado */}
            <button
              disabled
              className="block w-full text-center border border-white/10 text-white/25 text-xs tracking-[0.3em] uppercase px-4 py-3 bg-white/3 cursor-not-allowed"
            >
              <LockIcon />
              REQUIERE NIVEL 10
            </button>

          </div>

          {/* ── TARJETA 3 — BLOQUEADA (QA Senior) ───────────────────────────── */}
          <div className="mission-locked p-7 flex flex-col gap-5">

            {/* Badge */}
            <div className="inline-flex items-center gap-2 self-start px-3 py-1 border border-[#FFB800]/20">
              <span className="text-[#FFB800]/50 text-[10px] tracking-[0.35em] uppercase font-bold">
                STATUS: EN DESARROLLO
              </span>
            </div>

            {/* Título */}
            <h3 className="text-[#888]/80 text-sm font-bold tracking-[0.2em] uppercase leading-6">
              OPERACIÓN GAMMA:<br />
              <span className="text-white/50">Resiliencia QA Senior</span>
            </h3>

            {/* Separador */}
            <div className="h-px bg-white/6" />

            {/* Descripción */}
            <p className="text-[#888]/60 text-sm leading-6 tracking-wide flex-1">
              Simulación de caos en producción. Blindaje de despliegues y detección de fallos críticos.
            </p>

            {/* Botón deshabilitado */}
            <button
              disabled
              className="block w-full text-center border border-white/10 text-white/25 text-xs tracking-[0.3em] uppercase px-4 py-3 bg-white/3 cursor-not-allowed"
            >
              <LockIcon />
              ZONA BLOQUEADA
            </button>

          </div>

        </div>

        {/* ── Nota de pie ─────────────────────────────────────────────────────── */}
        <p className="mt-8 text-[#00FF41]/20 text-xs tracking-[0.3em] text-center">
          {'[ NUEVAS ZONAS SE DESBLOQUEAN SEGÚN TU RANGO OPERATIVO ]'}
        </p>

      </div>
    </section>
  )
}
