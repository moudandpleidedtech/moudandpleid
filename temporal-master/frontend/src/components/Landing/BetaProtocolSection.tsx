'use client'

/**
 * BetaProtocolSection.tsx — Canal de Feedback · DAKI EdTech
 * ──────────────────────────────────────────────────────────
 * Fondo negro con borde rojo alerta. Layout centrado tipo terminal.
 * Botón con glow pulsante rojo → mailto de reporte.
 */

export default function BetaProtocolSection() {
  return (
    <section className="bg-[#0A0A0A] font-mono px-6 md:px-12 py-24">

      <style>{`
        @keyframes red-pulse {
          0%, 100% {
            box-shadow: 0 0 8px rgba(255,51,51,0.2), 0 0 20px rgba(255,51,51,0.08);
            border-color: rgba(255,51,51,0.4);
          }
          50% {
            box-shadow: 0 0 24px rgba(255,51,51,0.6), 0 0 48px rgba(255,51,51,0.2);
            border-color: rgba(255,51,51,0.9);
          }
        }
        @keyframes border-blink {
          0%, 90%, 100% { border-color: rgba(255,51,51,0.25); }
          95%            { border-color: rgba(255,51,51,0.7); }
        }
        .beta-wrapper {
          border: 1px solid rgba(255,51,51,0.25);
          animation: border-blink 4s ease-in-out infinite;
        }
        .report-btn {
          animation: red-pulse 2.6s ease-in-out infinite;
          transition: background 0.2s ease;
        }
        .report-btn:hover {
          animation: none;
          box-shadow: 0 0 32px rgba(255,51,51,0.7), 0 0 64px rgba(255,51,51,0.3);
          border-color: #ff3333;
          background: rgba(255,51,51,0.1);
        }
      `}</style>

      <div className="max-w-3xl mx-auto">
        <div className="beta-wrapper p-10 md:p-14 flex flex-col items-center gap-8 text-center bg-[#0D0D0D]">

          {/* Pre-label */}
          <span className="text-[#ff3333]/50 text-xs tracking-[0.6em] uppercase">
            {'// CANAL SEGURO — FASE ALPHA'}
          </span>

          {/* Título */}
          <h2
            className="text-2xl sm:text-3xl md:text-4xl font-bold tracking-[0.1em] uppercase text-white"
            style={{ textShadow: '0 0 30px rgba(255,51,51,0.4), 0 0 60px rgba(255,51,51,0.15)' }}
          >
            PROTOCOLO DE<br />
            <span className="text-[#ff3333]">REPORTE BETA</span>
          </h2>

          {/* Separador */}
          <div className="h-px w-24 bg-gradient-to-r from-transparent via-[#ff3333]/40 to-transparent" />

          {/* Descripción */}
          <p className="text-[#C0C0C0]/65 text-sm leading-7 tracking-wide max-w-xl">
            A los Operadores de la Fase Alpha: El sistema está vivo.
            Si encuentran una fisura, no la ignoren.{' '}
            <span className="text-white/80">Documenten el fallo.</span>{' '}
            Su feedback es el blindaje de las futuras generaciones.
          </p>

          {/* CTA */}
          <a
            href="mailto:reporte@dakiedtech.com?subject=[ANOMALIA]%20Reporte%20de%20Operador"
            className="report-btn border border-[#ff3333]/40 text-[#ff3333] text-xs tracking-[0.4em] uppercase px-10 py-4 bg-[#ff3333]/5 w-full sm:w-auto text-center"
          >
            {`[[ REPORTAR ANOMALÍA ]]`}
          </a>

          {/* Micro-copy */}
          <p className="text-[#ff3333]/25 text-xs tracking-[0.25em]">
            {'[ TODOS LOS REPORTES SON ANALIZADOS POR EL NÚCLEO ]'}
          </p>

        </div>
      </div>

    </section>
  )
}
