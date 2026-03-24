'use client'

/**
 * /login — Terminal de Acceso Restringido · DAKI EdTech
 * ──────────────────────────────────────────────────────
 * Flujo: boot typewriter → input código Beta → fetch verify-beta-code → hub
 */

import { useState, useEffect, useRef } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000'

const BOOT_LINES = [
  '> INICIANDO PROTOCOLO DE AUTENTICACIÓN...',
  '> VERIFICANDO INTEGRIDAD DE NÚCLEOS...       [OK]',
  '> CARGANDO PROTOCOLOS DE SEGURIDAD...        [OK]',
  '> ESTABLECIENDO CANAL CIFRADO...             [OK]',
  '> TERMINAL LISTA. INGRESE CÓDIGO DE OPERADOR.',
]
const BOOT_DELAYS = [0, 480, 920, 1360, 1800]

type ConsoleState = 'idle' | 'loading' | 'success' | 'error'

interface ConsoleLine {
  text:  string
  state: ConsoleState
}

export default function LoginPage() {
  const router = useRouter()

  const [bootLines,    setBootLines]    = useState<string[]>([])
  const [bootDone,     setBootDone]     = useState(false)
  const [inputCode,    setInputCode]    = useState('')
  const [isLoading,    setIsLoading]    = useState(false)
  const [inputFocused, setInputFocused] = useState(false)
  const [console_,     setConsole]      = useState<ConsoleLine>({
    text:  'Esperando credenciales',
    state: 'idle',
  })

  const inputRef = useRef<HTMLInputElement>(null)

  // ── Boot typewriter ──────────────────────────────────────────────────────────
  useEffect(() => {
    const timers: ReturnType<typeof setTimeout>[] = []
    BOOT_LINES.forEach((line, i) =>
      timers.push(setTimeout(() => setBootLines(prev => [...prev, line]), BOOT_DELAYS[i] + 300))
    )
    timers.push(setTimeout(() => {
      setBootDone(true)
      inputRef.current?.focus()
    }, BOOT_DELAYS[BOOT_LINES.length - 1] + 600))
    return () => timers.forEach(clearTimeout)
  }, [])

  // ── Ejecutar secuencia ───────────────────────────────────────────────────────
  const ejecutarSecuencia = async () => {
    if (!inputCode.trim() || isLoading) return

    setIsLoading(true)
    setConsole({ text: 'Autenticando credenciales...', state: 'loading' })

    try {
      const res = await fetch(`${API_BASE}/api/v1/auth/verify-beta-code`, {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify({ code: inputCode.trim() }),
      })

      if (res.ok) {
        const data = await res.json() as { token: string; message: string }
        localStorage.setItem('beta_token', data.token)
        document.cookie = 'enigma_user=1; path=/; max-age=604800; SameSite=Lax'
        setConsole({ text: 'ACCESO CONCEDIDO. Abriendo el Nexo...', state: 'success' })
        setTimeout(() => router.push('/hub'), 1000)
        return
      }

      if (res.status === 404) {
        setConsole({ text: 'ERROR 404: CREDENCIAL INVÁLIDA O INACTIVA', state: 'error' })
      } else if (res.status === 403) {
        setConsole({ text: 'ERROR 403: CÓDIGO AGOTADO. LÍMITE DE USOS ALCANZADO', state: 'error' })
      } else {
        setConsole({ text: `ERROR ${res.status}: RESPUESTA INESPERADA DEL NEXO`, state: 'error' })
      }
    } catch {
      setConsole({ text: 'ERROR CRÍTICO: FALLO DE CONEXIÓN CON EL NEXO', state: 'error' })
    } finally {
      setIsLoading(false)
    }
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    ejecutarSecuencia()
  }

  // ── Color de la consola según estado ─────────────────────────────────────────
  const consoleColor = {
    idle:    'text-[#00FF41]/35',
    loading: 'text-[#FFB800]/70',
    success: 'text-[#00FF41]',
    error:   'text-[#FF3333]',
  }[console_.state]

  const consoleGlow = console_.state === 'success'
    ? '[text-shadow:0_0_8px_rgba(0,255,65,0.6)]'
    : console_.state === 'error'
      ? '[text-shadow:0_0_8px_rgba(255,51,51,0.5)]'
      : ''

  return (
    <div className="min-h-screen bg-[#0A0A0A] font-mono text-[#00FF41] flex flex-col items-center justify-center relative overflow-y-auto">

      {/* ── Keyframes ──────────────────────────────────────────────────────────── */}
      <style>{`
        @keyframes cursor-blink {
          0%, 100% { opacity: 1; }
          50%       { opacity: 0; }
        }
        @keyframes error-blink {
          0%, 100% { opacity: 1; }
          25%, 75% { opacity: 0.3; }
        }
        .blink        { animation: cursor-blink 1s step-end infinite; }
        .error-blink  { animation: error-blink 0.4s ease-in-out 2; }

        .exec-btn {
          border: 1px solid rgba(0,255,65,0.55);
          color: #00FF41;
          background: transparent;
          transition: background 0.15s ease, color 0.15s ease, box-shadow 0.15s ease;
        }
        .exec-btn:hover:not(:disabled) {
          background: #00FF41;
          color: #0A0A0A;
          box-shadow: 0 0 24px rgba(0,255,65,0.4);
        }
        .exec-btn:disabled {
          border-color: rgba(0,255,65,0.15);
          color: rgba(0,255,65,0.25);
          cursor: not-allowed;
        }
        .input-line {
          border-bottom: 1px solid rgba(0,255,65,0.2);
          transition: border-color 0.2s ease, box-shadow 0.2s ease;
        }
        .input-line.focused {
          border-color: #00FF41;
          box-shadow: 0 2px 12px rgba(0,255,65,0.2);
        }
      `}</style>

      {/* CRT overlay */}
      <div className="fixed inset-0 pointer-events-none z-10"
        style={{ backgroundImage: 'repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,0.07) 2px,rgba(0,0,0,0.07) 4px)' }}
      />
      {/* Vignette */}
      <div className="fixed inset-0 pointer-events-none z-10"
        style={{ background: 'radial-gradient(ellipse at center,transparent 50%,rgba(0,0,0,0.75) 100%)' }}
      />

      {/* ── Terminal box ───────────────────────────────────────────────────────── */}
      <div className="relative z-20 w-full max-w-lg px-6 py-10 pb-16">

        {/* ── Header ─────────────────────────────────────────────────────────── */}
        <div className="border-b border-[#00FF41]/15 pb-4 mb-8">
          <p className="text-[#00FF41]/25 text-xs tracking-[0.5em] uppercase mb-1">
            {'// ACCESO RESTRINGIDO — FASE BETA'}
          </p>
          <h1 className="text-[#00FF41] text-sm md:text-base font-bold tracking-[0.3em] uppercase neon-glow">
            DAKIedtech {'//'}  PROTOCOLO DE AUTENTICACIÓN
          </h1>
        </div>

        {/* ── Boot log ───────────────────────────────────────────────────────── */}
        {bootLines.length > 0 && (
          <div className="space-y-1 mb-8">
            {bootLines.map((line, i) => (
              <div key={i} className={`text-xs leading-5 ${
                line.includes('[OK]')   ? 'text-[#00FF41]/50'
                : line.includes('LISTA') ? 'text-[#00FF41]/80'
                : 'text-[#00FF41]/30'
              }`}>
                {line}
              </div>
            ))}
          </div>
        )}

        {/* ── Input de código Beta ────────────────────────────────────────────── */}
        {bootDone && (
          <div className="mb-6">
            <p className="text-xs text-[#00FF41]/50 tracking-[0.3em] uppercase mb-4">
              {'> INTRODUZCA CÓDIGO DE OPERADOR'}
            </p>

            <form onSubmit={handleSubmit}>
              <div className={`input-line pb-2 mb-5 flex items-center gap-2 ${inputFocused ? 'focused' : ''}`}>
                <span className="text-[#00FF41]/50 select-none text-xs">{'>'}</span>
                <input
                  ref={inputRef}
                  type="text"
                  value={inputCode}
                  onChange={e => setInputCode(e.target.value)}
                  onFocus={() => setInputFocused(true)}
                  onBlur={() => setInputFocused(false)}
                  placeholder="[ INGRESE CÓDIGO DE OPERADOR ]"
                  disabled={isLoading}
                  className="flex-1 bg-transparent text-[#00FF41] text-sm outline-none border-none caret-[#00FF41] tracking-widest uppercase placeholder:text-[#00FF41]/20 placeholder:normal-case placeholder:tracking-wide disabled:opacity-40"
                  autoComplete="off"
                  spellCheck={false}
                />
              </div>

              <button
                type="submit"
                disabled={isLoading || !inputCode.trim()}
                className="exec-btn w-full py-3 text-xs tracking-[0.4em] uppercase"
              >
                {isLoading ? '[ PROCESANDO... ]' : '[[ EJECUTAR SECUENCIA ]]'}
              </button>
            </form>
          </div>
        )}

        {/* ── Consola de estado ──────────────────────────────────────────────── */}
        <div className="border-t border-[#00FF41]/10 pt-4 mt-2 mb-8 min-h-[50px]">
          <p className={`text-xs tracking-wide ${consoleColor} ${consoleGlow} ${console_.state === 'error' ? 'error-blink' : ''}`}>
            {'> Status: '}{console_.text}
            <span className="blink ml-0.5">_</span>
          </p>
        </div>

        {/* ── Salida de emergencia ───────────────────────────────────────────── */}
        <div className="text-center">
          <Link
            href="/"
            className="text-[#00FF41]/15 text-[10px] tracking-[0.3em] hover:text-[#00FF41]/40 transition-colors"
          >
            {'[ Abortar y volver al portal principal ]'}
          </Link>
        </div>

      </div>
    </div>
  )
}
