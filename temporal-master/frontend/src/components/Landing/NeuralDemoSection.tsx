/**
 * NeuralDemoSection.tsx — Preview de la Interfaz Neural · DAKI EdTech
 * ────────────────────────────────────────────────────────────────────
 * Mock estático de la interfaz Monaco + panel DAKI IA.
 * Sintaxis Python coloreada con <span> (sin librerías externas).
 * Gatillo mental: Prueba tangible + FOMO. El usuario VE antes de registrarse.
 * Server Component: sin hooks, sin APIs del browser.
 */

export default function NeuralDemoSection() {
  return (
    <section className="bg-[#0A0A0A] font-mono px-6 md:px-12 py-24 relative overflow-hidden">

      <div className="max-w-5xl mx-auto">

        {/* Header de sección */}
        <div className="flex items-center gap-4 mb-4">
          <span className="text-[#00FF41] text-xs tracking-[0.5em]">{'▶'}</span>
          <h2 className="text-2xl sm:text-3xl md:text-4xl font-bold tracking-[0.08em] uppercase text-white">
            INTERFAZ NEURAL
          </h2>
          <div className="h-px flex-1 bg-gradient-to-r from-[#00FF41]/15 to-transparent hidden md:block" />
        </div>
        <p className="text-[#00FF41]/25 text-[10px] tracking-[0.4em] uppercase mb-12 ml-8">
          {'// ESTO NO ES UN VIDEO DE YOUTUBE — ES TU ENTORNO DE DESPLIEGUE'}
        </p>

        {/* ── Mock de la interfaz ──────────────────────────────────────────── */}
        <div className="border border-[#00FF41]/18 overflow-hidden relative">

          {/* Scanline overlay sobre el mock */}
          <div
            className="absolute inset-0 pointer-events-none z-10 opacity-40"
            style={{
              backgroundImage:
                'repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,0.06) 2px,rgba(0,0,0,0.06) 4px)',
            }}
          />

          {/* ── Tab bar (estilo Monaco) ─────────────────────────────── */}
          <div className="bg-[#111111] border-b border-[#00FF41]/10 px-4 py-2.5 flex items-center justify-between">
            <div className="flex items-center gap-4">
              {/* Dots */}
              <div className="flex items-center gap-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-[#FF0033]/50" />
                <span className="w-2.5 h-2.5 rounded-full bg-[#FFB800]/30" />
                <span className="w-2.5 h-2.5 rounded-full bg-[#00FF41]/20" />
              </div>
              {/* Tab activo */}
              <div className="flex items-center gap-2 border-b-2 border-[#00FF41]/50 pb-0.5">
                <span className="text-[#00FF41]/60 text-[10px] tracking-[0.2em]">
                  operacion_01.py
                </span>
              </div>
              <span className="text-white/10 text-[10px] tracking-[0.2em] hidden sm:block">
                nexo_core.py
              </span>
            </div>
            {/* Status badge */}
            <div className="flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-[#00FF41] animate-pulse" />
              <span className="text-[#00FF41]/50 text-[9px] tracking-[0.3em] uppercase">
                NEXO ACTIVO
              </span>
            </div>
          </div>

          {/* ── Área del editor ────────────────────────────────────── */}
          <div className="bg-[#0D0D0D] p-4 md:p-6 overflow-x-auto">
            <table className="text-xs md:text-sm leading-7" style={{ borderCollapse: 'collapse', minWidth: '100%' }}>
              <tbody>

                {/* Línea 1 — comentario */}
                <tr>
                  <td className="text-white/15 text-[9px] md:text-[10px] pr-4 md:pr-6 select-none w-6 md:w-8 text-right whitespace-nowrap">1</td>
                  <td>
                    <span className="text-[#6A9955]"># Operación 01 · Misión: El Loop Infinito</span>
                  </td>
                </tr>

                {/* Línea 2 — blank */}
                <tr>
                  <td className="text-white/15 text-[9px] md:text-[10px] pr-4 md:pr-6 select-none w-6 md:w-8 text-right whitespace-nowrap">2</td>
                  <td>&nbsp;</td>
                </tr>

                {/* Línea 3 — def */}
                <tr>
                  <td className="text-white/15 text-[9px] md:text-[10px] pr-4 md:pr-6 select-none w-6 md:w-8 text-right whitespace-nowrap">3</td>
                  <td>
                    <span className="text-[#569CD6]">def </span>
                    <span className="text-[#DCDCAA]">hunt_duplicates</span>
                    <span className="text-white/70">(</span>
                    <span className="text-[#9CDCFE]">data</span>
                    <span className="text-[#4EC9B0]">: list</span>
                    <span className="text-white/70">) </span>
                    <span className="text-[#569CD6]">-{'>'} </span>
                    <span className="text-[#4EC9B0]">list</span>
                    <span className="text-white/70">:</span>
                  </td>
                </tr>

                {/* Línea 4 — seen = set() */}
                <tr>
                  <td className="text-white/15 text-[9px] md:text-[10px] pr-4 md:pr-6 select-none w-6 md:w-8 text-right whitespace-nowrap">4</td>
                  <td className="pl-4 md:pl-8 whitespace-nowrap">
                    <span className="text-[#9CDCFE]">seen </span>
                    <span className="text-white/70">= </span>
                    <span className="text-[#4EC9B0]">set</span>
                    <span className="text-white/70">()</span>
                  </td>
                </tr>

                {/* Línea 5 — result = [] */}
                <tr>
                  <td className="text-white/15 text-[9px] md:text-[10px] pr-4 md:pr-6 select-none w-6 md:w-8 text-right whitespace-nowrap">5</td>
                  <td className="pl-4 md:pl-8 whitespace-nowrap">
                    <span className="text-[#9CDCFE]">result </span>
                    <span className="text-white/70">= []</span>
                  </td>
                </tr>

                {/* Línea 6 — for loop */}
                <tr>
                  <td className="text-white/15 text-[9px] md:text-[10px] pr-4 md:pr-6 select-none w-6 md:w-8 text-right whitespace-nowrap">6</td>
                  <td className="pl-4 md:pl-8 whitespace-nowrap">
                    <span className="text-[#569CD6]">for </span>
                    <span className="text-[#9CDCFE]">item </span>
                    <span className="text-[#569CD6]">in </span>
                    <span className="text-[#9CDCFE]">data</span>
                    <span className="text-white/70">:</span>
                    <span className="text-[#6A9955] text-[11px] ml-4">  # ← DAKI: O(n) detectado</span>
                  </td>
                </tr>

                {/* Línea 7 — if */}
                <tr>
                  <td className="text-white/15 text-[9px] md:text-[10px] pr-4 md:pr-6 select-none w-6 md:w-8 text-right whitespace-nowrap">7</td>
                  <td className="pl-8 md:pl-16 whitespace-nowrap">
                    <span className="text-[#569CD6]">if </span>
                    <span className="text-[#9CDCFE]">item </span>
                    <span className="text-[#569CD6]">not in </span>
                    <span className="text-[#9CDCFE]">seen</span>
                    <span className="text-white/70">:</span>
                  </td>
                </tr>

                {/* Línea 8 — seen.add */}
                <tr>
                  <td className="text-white/15 text-[9px] md:text-[10px] pr-4 md:pr-6 select-none w-6 md:w-8 text-right whitespace-nowrap">8</td>
                  <td className="pl-12 md:pl-24 whitespace-nowrap">
                    <span className="text-[#9CDCFE]">seen</span>
                    <span className="text-white/70">.</span>
                    <span className="text-[#DCDCAA]">add</span>
                    <span className="text-white/70">(</span>
                    <span className="text-[#9CDCFE]">item</span>
                    <span className="text-white/70">)</span>
                  </td>
                </tr>

                {/* Línea 9 — result.append */}
                <tr>
                  <td className="text-white/15 text-[9px] md:text-[10px] pr-4 md:pr-6 select-none w-6 md:w-8 text-right whitespace-nowrap">9</td>
                  <td className="pl-12 md:pl-24 whitespace-nowrap">
                    <span className="text-[#9CDCFE]">result</span>
                    <span className="text-white/70">.</span>
                    <span className="text-[#DCDCAA]">append</span>
                    <span className="text-white/70">(</span>
                    <span className="text-[#9CDCFE]">item</span>
                    <span className="text-white/70">)</span>
                  </td>
                </tr>

                {/* Línea 10 — return */}
                <tr>
                  <td className="text-white/15 text-[9px] md:text-[10px] pr-4 md:pr-6 select-none w-6 md:w-8 text-right whitespace-nowrap">10</td>
                  <td className="pl-4 md:pl-8 whitespace-nowrap">
                    <span className="text-[#569CD6]">return </span>
                    <span className="text-[#9CDCFE]">result</span>
                  </td>
                </tr>

                {/* Línea 11 — cursor */}
                <tr>
                  <td className="text-white/15 text-[9px] md:text-[10px] pr-4 md:pr-6 select-none w-6 md:w-8 text-right whitespace-nowrap">11</td>
                  <td>
                    <span className="inline-block w-2 h-4 bg-[#00FF41]/70 align-middle" />
                  </td>
                </tr>

              </tbody>
            </table>
          </div>

          {/* ── Panel DAKI IA ───────────────────────────────────────── */}
          <div className="bg-[#080808] border-t border-[#00FF41]/12 p-5">
            <div className="flex items-center gap-2 mb-4">
              <span
                className="text-[#00FF41] text-[9px] tracking-[0.5em] uppercase font-bold"
                style={{ textShadow: '0 0 8px rgba(0,255,65,0.6)' }}
              >
                DAKI IA
              </span>
              <span className="text-[#00FF41]/20 text-[9px]">—</span>
              <span className="text-[#00FF41]/30 text-[9px] tracking-[0.3em] uppercase">
                ANÁLISIS EN TIEMPO REAL
              </span>
              <span className="ml-auto flex items-center gap-1.5">
                <span className="w-1 h-1 rounded-full bg-[#00FF41] animate-pulse" />
                <span className="text-[#00FF41]/25 text-[9px] tracking-widest">PROCESANDO</span>
              </span>
            </div>

            <div className="space-y-2.5">
              <div className="flex items-start gap-3">
                <span className="text-[#00FF41]/50 text-[10px] shrink-0 mt-0.5">▶</span>
                <span className="text-[#00FF41]/70 text-[11px] leading-5 tracking-wide">
                  Complejidad detectada: <span className="text-[#00FF41] font-bold">O(n)</span> — uso de
                  {' '}<code className="text-[#4EC9B0]">set</code> para lookup constante. Estructura eficiente.
                </span>
              </div>
              <div className="flex items-start gap-3">
                <span className="text-[#FFB800]/50 text-[10px] shrink-0 mt-0.5">▶</span>
                <span className="text-[#C0C0C0]/55 text-[11px] leading-5 tracking-wide">
                  Patrón identificado: lógica de deduplicación manual.
                  Nivel 12 desbloquea: <span className="text-[#FFB800]/70">optimización con list comprehension</span>.
                </span>
              </div>
              <div className="flex items-start gap-3">
                <span className="text-[#00FF41]/50 text-[10px] shrink-0 mt-0.5">▶</span>
                <span className="text-[#C0C0C0]/40 text-[11px] leading-5 tracking-wide">
                  Misión completada al 93% —
                  próxima: <span className="text-[#00FF41]/60">Recursividad Táctica → Nivel 08</span>
                </span>
              </div>
            </div>

            {/* Barra de progreso */}
            <div className="mt-5 flex items-center gap-4">
              <span className="text-[#00FF41]/30 text-[9px] tracking-[0.4em] uppercase shrink-0">
                NIVEL 07
              </span>
              <div className="flex-1 h-px bg-[#00FF41]/08 relative">
                <div
                  className="absolute left-0 top-0 h-full bg-[#00FF41]/35"
                  style={{ width: '93%' }}
                />
              </div>
              <span className="text-[#00FF41]/30 text-[9px] tracking-[0.3em] shrink-0">93%</span>
            </div>
          </div>

        </div>

        {/* Footer */}
        <p className="mt-8 text-center text-[#00FF41]/18 text-[10px] tracking-[0.4em] uppercase">
          {'[ La IA no te corrige — te analiza. Detecta patrones de error antes de que los cometas ]'}
        </p>

      </div>
    </section>
  )
}
