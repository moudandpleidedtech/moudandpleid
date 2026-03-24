'use client'

/**
 * /mission/alfa — Campo de Batalla · DAKI EdTech
 * ─────────────────────────────────────────────────
 * Split-screen: Briefing + chat DAKI (30%) | Monaco + consola (70%)
 * Ejecución simulada para maqueta — sin challenge_id real.
 */

import { useRef, useState } from 'react'
import { useRouter } from 'next/navigation'
import dynamic from 'next/dynamic'
import DakiChatTerminal from '@/components/Hub/DakiChatTerminal'

// Monaco se carga solo en cliente (SSR no compatible)
const MonacoEditor = dynamic(() => import('@monaco-editor/react'), { ssr: false })

const INITIAL_CODE = `# MISIÓN: Eliminar al Infinite Looper
# El servidor está atrapado en un bucle sin fin.
# Corrige la condición de salida sin romper la lógica.

contador = 0

while True:  # <- ANOMALÍA: bucle infinito
    print(f"Ciclo {contador}")
    contador += 1

print("Sistema liberado")
`

// ── Simulador de ejecución (maqueta) ─────────────────────────────────────────
function simularEjecucion(code: string): string[] {
  const hasInfiniteLoop = /while\s+True\s*:/i.test(code) && !/break/.test(code)
  const hasFixedCondition = /while\s+contador\s*[<>!]=?\s*\d+/i.test(code) || /break/.test(code)

  if (hasInfiniteLoop) {
    return [
      '> Iniciando compilación...',
      '> Ejecutando secuencia...',
      '',
      'Ciclo 0',
      'Ciclo 1',
      'Ciclo 2',
      '...',
      '',
      '[ERROR] TimeoutError: CPU limit exceeded (2000ms)',
      '[DAKI_SYS] Bucle infinito detectado. La anomalía persiste, Operador.',
    ]
  }

  if (hasFixedCondition) {
    const lines = ['> Iniciando compilación...', '> Ejecutando secuencia...', '']
    for (let i = 0; i < 5; i++) lines.push(`Ciclo ${i}`)
    lines.push('', 'Sistema liberado', '', '[OK] Misión completada. Anomalía neutralizada.')
    return lines
  }

  return [
    '> Iniciando compilación...',
    '> Analizando secuencia...',
    '',
    '[WARN] Código modificado. Ejecutando validación...',
    '[OK] Sin errores de sintaxis detectados.',
  ]
}

// ── Página ────────────────────────────────────────────────────────────────────
export default function MissionAlfaPage() {
  const router  = useRouter()
  const [code,  setCode]  = useState(INITIAL_CODE)
  const [logs,  setLogs]  = useState<string[]>(['> Consola en espera. Sistema listo para compilar_'])
  const [running, setRunning] = useState(false)
  const consoleRef = useRef<HTMLDivElement>(null)

  const ejecutar = async () => {
    if (running) return
    setRunning(true)
    setLogs(['> Autorizando secuencia de compilación...'])

    // Simula delay de ejecución
    await new Promise(r => setTimeout(r, 900))
    const output = simularEjecucion(code)
    setLogs(output)
    setRunning(false)

    setTimeout(() => {
      consoleRef.current?.scrollTo({ top: consoleRef.current.scrollHeight, behavior: 'smooth' })
    }, 50)
  }

  const abortar = () => {
    if (!running) return
    setRunning(false)
    setLogs(prev => [...prev, '', '> [ABORT] Secuencia interrumpida por el Operador.'])
  }

  return (
    <div className="h-screen bg-[#0A0A0A] font-mono text-[#00FF41] flex flex-col overflow-hidden">

      {/* ── CRT overlay ──────────────────────────────────────────────────────── */}
      <div className="fixed inset-0 pointer-events-none z-10"
        style={{ backgroundImage: 'repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,0.07) 2px,rgba(0,0,0,0.07) 4px)' }}
      />

      {/* ── Header ───────────────────────────────────────────────────────────── */}
      <header className="relative z-20 shrink-0 flex items-center justify-between px-6 py-3 border-b border-[#00FF41]/12 bg-black/60">
        <div className="flex items-center gap-3">
          <span className="w-1.5 h-1.5 rounded-full bg-[#00FF41] animate-pulse" />
          <span className="text-xs font-bold tracking-[0.35em] uppercase neon-glow">
            DAKI {'//'}  ENTORNO DE EJECUCIÓN AIS_01
          </span>
        </div>
        <button
          onClick={() => router.push('/hub')}
          className="text-[10px] tracking-[0.35em] uppercase border border-[#00FF41]/25 text-[#00FF41]/50 px-3 py-1.5 hover:border-[#00FF41]/50 hover:text-[#00FF41]/80 transition-all duration-150"
        >
          {'[ VOLVER AL HUB ]'}
        </button>
      </header>

      {/* ── Split layout ─────────────────────────────────────────────────────── */}
      <main className="relative z-20 flex-1 flex overflow-hidden">

        {/* ══ PANEL IZQUIERDO — Briefing 30% ══════════════════════════════════ */}
        <div className="w-[30%] shrink-0 flex flex-col border-r border-[#FF4444]/20 overflow-hidden">

          {/* Briefing */}
          <div className="shrink-0 px-5 py-5 border-b border-[#FF4444]/15">

            {/* Badge */}
            <div className="flex items-center gap-2 mb-4">
              <span className="text-[#FF4444] text-xs">{'▶'}</span>
              <span className="text-[8px] tracking-[0.5em] text-[#FF4444]/60 uppercase">ZONA DE COMBATE ACTIVA</span>
            </div>

            {/* Título objetivo */}
            <h1 className="text-[11px] font-bold tracking-[0.25em] uppercase text-white mb-3 leading-5">
              OBJETIVO:<br />
              <span className="text-[#FF4444]">Eliminar al Infinite Looper</span>
            </h1>

            {/* Separador */}
            <div className="h-px bg-[#FF4444]/15 mb-4" />

            {/* Descripción */}
            <p className="text-[10px] text-[#C0C0C0]/65 leading-5 mb-4">
              Un bucle <span className="text-[#00FF41]">while</span> malicioso está consumiendo
              la memoria del servidor. Tu misión es inyectar un freno de emergencia{' '}
              <span className="text-[#00FF41]">(break)</span> o corregir la condición
              de salida sin romper la lógica principal.
            </p>

            {/* Restricción */}
            <div className="border border-[#FF4444]/25 bg-[#FF4444]/5 px-3 py-2.5">
              <p className="text-[9px] text-[#FF4444]/70 tracking-[0.25em]">
                <span className="font-bold">[!]</span> Tiempo límite de CPU:{' '}
                <span className="text-[#FF4444]">2 000 ms</span>
              </p>
            </div>
          </div>

          {/* Chat DAKI para pistas */}
          <div className="flex-1 flex flex-col min-h-0">
            <div className="shrink-0 px-4 py-2 border-b border-[#00FF41]/8">
              <p className="text-[8px] tracking-[0.5em] text-[#00FF41]/30 uppercase">
                {'// ENLACE DAKI — SOLICITAR PISTA'}
              </p>
            </div>
            <div className="flex-1 min-h-0">
              <DakiChatTerminal userId="" />
            </div>
          </div>
        </div>

        {/* ══ PANEL DERECHO — Editor + Consola 70% ════════════════════════════ */}
        <div className="flex-1 flex flex-col overflow-hidden">

          {/* Editor Monaco */}
          <div className="flex-1 min-h-0">
            <MonacoEditor
              height="100%"
              language="python"
              theme="vs-dark"
              value={code}
              onChange={v => setCode(v ?? '')}
              options={{
                fontSize:        13,
                fontFamily:      "'Fira Code', 'Cascadia Code', Consolas, monospace",
                minimap:         { enabled: false },
                scrollBeyondLastLine: false,
                lineNumbers:     'on',
                renderLineHighlight: 'line',
                tabSize:         4,
                wordWrap:        'on',
                padding:         { top: 12 },
              }}
            />
          </div>

          {/* Controles */}
          <div className="shrink-0 flex items-center gap-3 px-4 py-2.5 border-t border-b border-[#00FF41]/10 bg-black/40">
            <button
              onClick={ejecutar}
              disabled={running}
              className="text-[10px] tracking-[0.35em] uppercase border border-[#00FF41]/55 text-[#00FF41] px-5 py-2 bg-[#00FF41]/5 hover:bg-[#00FF41]/12 hover:border-[#00FF41] hover:shadow-[0_0_16px_rgba(0,255,65,0.3)] disabled:opacity-30 disabled:cursor-not-allowed transition-all duration-150"
            >
              {running ? '[ EJECUTANDO... ]' : '[[ COMPILAR Y EJECUTAR ]]'}
            </button>
            <button
              onClick={abortar}
              disabled={!running}
              className="text-[10px] tracking-[0.35em] uppercase border border-[#FF4444]/40 text-[#FF4444]/70 px-4 py-2 hover:bg-[#FF4444]/8 hover:border-[#FF4444]/70 disabled:opacity-20 disabled:cursor-not-allowed transition-all duration-150"
            >
              {'[ ABORTAR SECUENCIA ]'}
            </button>
            <span className="ml-auto text-[8px] tracking-[0.4em] text-[#00FF41]/20 uppercase">
              Python 3.12 · AIS_01
            </span>
          </div>

          {/* Consola de salida */}
          <div
            ref={consoleRef}
            className="shrink-0 h-[28%] bg-black border-t border-[#00FF41]/8 px-4 py-3 overflow-y-auto"
          >
            <div className="text-[8px] tracking-[0.5em] text-[#00FF41]/20 uppercase mb-3">
              {'// TERMINAL DE SALIDA'}
            </div>
            {logs.map((line, i) => (
              <div key={i} className={`text-[11px] leading-5 font-mono ${
                line.startsWith('[ERROR]') || line.startsWith('[ABORT]') ? 'text-[#FF4444]/80'
                : line.startsWith('[OK]')    ? 'text-[#00FF41]'
                : line.startsWith('[WARN]')  ? 'text-[#FFB800]/70'
                : line.startsWith('[DAKI')   ? 'text-[#00FF41]/50'
                : line.startsWith('>')       ? 'text-[#00FF41]/35'
                : line === ''               ? 'h-2'
                : 'text-[#C0C0C0]/60'
              }`}>
                {line || '\u00A0'}
              </div>
            ))}
            {running && (
              <span className="text-[#00FF41]/40 text-[11px] animate-pulse">_</span>
            )}
          </div>

        </div>
      </main>
    </div>
  )
}
