'use client'

/**
 * MissionsSection.tsx — Zonas de Operación · DAKI EdTech
 * ──────────────────────────────────────────────────────
 * CSS de .mission-active / .mission-locked / .active-btn vive en globals.css.
 * Sin inline <style> → sin hydration issues.
 */

import Link from 'next/link'

function LockIcon() {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="11"
      height="11"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      className="inline-block mr-1.5 mb-0.5 opacity-60"
    >
      <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
      <path d="M7 11V7a5 5 0 0 1 10 0v4" />
    </svg>
  )
}

export default function MissionsSection() {
  return (
    <section className="bg-[#0D0D0D] font-mono px-6 md:px-12 py-24 relative overflow-hidden">

      <div className="max-w-6xl mx-auto">

        {/* Título de sección */}
        <div className="flex items-center gap-4 mb-3">
          <span className="text-[#00FF41] text-xs tracking-[0.5em]">{'▶'}</span>
          <h2 className="text-2xl sm:text-3xl md:text-4xl font-bold tracking-[0.1em] uppercase text-white">
            ZONAS DE OPERACIÓN
          </h2>
        </div>
        <p className="text-[#00FF41]/25 text-[10px] tracking-[0.4em] uppercase mb-12 ml-8">
          {'// TU RUTA DE COMBATE — OPERACIÓN ALFA → BETA → GAMMA'}
        </p>

        {/* Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">

          {/* TARJETA 1 — ACTIVA — PYTHON */}
          <div className="mission-active p-7 flex flex-col gap-5 relative">

            {/* Fila de status + lenguaje */}
            <div className="flex items-center justify-between">
              <div className="inline-flex items-center gap-2 px-3 py-1 bg-[#00FF41]/10 border border-[#00FF41]/30">
                <span className="w-1.5 h-1.5 rounded-full bg-[#00FF41] animate-pulse" />
                <span className="text-[#00FF41] text-[10px] tracking-[0.35em] uppercase font-bold">
                  ONLINE
                </span>
              </div>
              <span
                className="text-[#00FF41]/55 text-[10px] tracking-[0.25em] border border-[#00FF41]/20 px-2 py-0.5 font-bold"
                style={{ textShadow: '0 0 10px rgba(0,255,65,0.5)' }}
              >
                PYTHON 3
              </span>
            </div>

            <div>
              <p className="text-[#00FF41]/40 text-[10px] tracking-[0.4em] uppercase mb-1">Operación 01</p>
              <h3 className="text-[#00FF41] text-sm font-bold tracking-[0.2em] uppercase leading-6">
                Python — Core<br />
                <span className="text-white/90">Lógica & Sistemas</span>
              </h3>
            </div>

            {/* Tech stack tags */}
            <div className="flex flex-wrap gap-1.5">
              {['vars', 'funciones', 'OOP', 'algoritmos', 'APIs REST'].map(tag => (
                <span
                  key={tag}
                  className="text-[#00FF41]/30 text-[9px] tracking-[0.2em] border border-[#00FF41]/10 px-1.5 py-0.5"
                >
                  {tag}
                </span>
              ))}
            </div>

            <div className="h-px bg-[#00FF41]/15" />

            <p className="text-[#C0C0C0]/70 text-sm leading-6 tracking-wide flex-1">
              Vence al Infinite Looper. Domina Python desde cero hasta APIs REST y estructuras de datos reales en 190 niveles de combate.
            </p>

            {/* Progress hint */}
            <div className="space-y-1.5">
              <div className="flex justify-between text-[10px] text-[#00FF41]/40 tracking-[0.3em]">
                <span>NIVELES 1 → 190</span>
                <span>NIVEL ACTUAL</span>
              </div>
              <div className="h-px bg-[#00FF41]/10 relative">
                <div className="absolute left-0 top-0 h-full bg-[#00FF41]/30 w-0" />
              </div>
            </div>

            <Link
              href="/login"
              className="active-btn block text-center border border-[#00FF41]/45 text-[#00FF41] text-xs tracking-[0.35em] uppercase px-4 py-3 bg-[#00FF41]/5"
            >
              {`[[ INICIAR CON PYTHON ]]`}
            </Link>

          </div>

          {/* TARJETA 2 — BLOQUEADA (Hacking Ético) */}
          <div className="mission-locked p-7 flex flex-col gap-5 opacity-70">

            <div className="inline-flex items-center gap-2 self-start px-3 py-1 border border-[#FFB800]/25">
              <span className="text-[#FFB800]/60 text-[10px] tracking-[0.35em] uppercase font-bold">
                PRÓXIMAMENTE
              </span>
            </div>

            <div>
              <p className="text-white/20 text-[10px] tracking-[0.4em] uppercase mb-1">Operación 02</p>
              <h3 className="text-white/60 text-sm font-bold tracking-[0.2em] uppercase leading-6">
                Hacking Ético<br />
                <span className="text-white/40">y Seguridad</span>
              </h3>
            </div>

            <div className="h-px bg-white/6" />

            <p className="text-[#888]/55 text-sm leading-6 tracking-wide flex-1">
              Aprende construyendo y rompiendo sistemas. Penetration testing, seguridad ofensiva y hardening en producción.
            </p>

            <button
              disabled
              className="block w-full text-center border border-[#FFB800]/20 text-[#FFB800]/35 text-[10px] tracking-[0.3em] uppercase px-4 py-3 bg-[#FFB800]/3 cursor-not-allowed"
            >
              <LockIcon />
              DESBLOQUEA EN NIVEL 10
            </button>

          </div>

          {/* TARJETA 3 — BLOQUEADA (Ciberseguridad) */}
          <div className="mission-locked p-7 flex flex-col gap-5 opacity-60">

            <div className="inline-flex items-center gap-2 self-start px-3 py-1 border border-[#FF0033]/20">
              <span className="text-[#FF0033]/50 text-[10px] tracking-[0.35em] uppercase font-bold">
                EN DESARROLLO
              </span>
            </div>

            <div>
              <p className="text-white/15 text-[10px] tracking-[0.4em] uppercase mb-1">Operación 03</p>
              <h3 className="text-white/50 text-sm font-bold tracking-[0.2em] uppercase leading-6">
                Agente de<br />
                <span className="text-white/35">Ciberseguridad</span>
              </h3>
            </div>

            <div className="h-px bg-white/5" />

            <p className="text-[#888]/45 text-sm leading-6 tracking-wide flex-1">
              Penetra sistemas antes de que otros lo hagan. Hacking ético, análisis de vulnerabilidades y hardening ofensivo — el perfil más codiciado del mercado tech.
            </p>

            <button
              disabled
              className="block w-full text-center border border-[#FF0033]/15 text-[#FF0033]/30 text-[10px] tracking-[0.3em] uppercase px-4 py-3 bg-[#FF0033]/[0.02] cursor-not-allowed"
            >
              <LockIcon />
              ZONA CLASIFICADA
            </button>

          </div>

        </div>

        {/* Nota de pie */}
        <p className="mt-10 text-[#00FF41]/15 text-[10px] tracking-[0.35em] text-center uppercase">
          {'[ Las zonas se desbloquean automáticamente al alcanzar el rango requerido ]'}
        </p>

      </div>
    </section>
  )
}
