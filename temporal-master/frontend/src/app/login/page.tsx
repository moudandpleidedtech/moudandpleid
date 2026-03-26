'use client'

/**
 * /login — Terminal de Acceso · DAKI EdTech
 * ──────────────────────────────────────────
 * POST /api/v1/auth/login  { email, password }  → JWT → /hub
 * Para crear cuenta → /register
 */

import { useState, useEffect, useRef } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? ''

const BOOT_LINES = [
  '> INICIANDO PROTOCOLO DE AUTENTICACIÓN...',
  '> VERIFICANDO INTEGRIDAD DE NÚCLEOS...       [OK]',
  '> CARGANDO PROTOCOLOS DE SEGURIDAD...        [OK]',
  '> ESTABLECIENDO CANAL CIFRADO...             [OK]',
  '> TERMINAL LISTA. INGRESE CREDENCIALES.',
]
const BOOT_DELAYS = [0, 480, 920, 1360, 1800]

type ConsoleState = 'idle' | 'loading' | 'success' | 'error'
interface ConsoleLine { text: string; state: ConsoleState }

export default function LoginPage() {
  const router = useRouter()

  const [bootLines,    setBootLines]    = useState<string[]>([])
  const [bootDone,     setBootDone]     = useState(false)
  const [email,        setEmail]        = useState('')
  const [password,     setPassword]     = useState('')
  const [isLoading,    setIsLoading]    = useState(false)
  const [focusedField, setFocusedField] = useState<string | null>(null)
  const [console_,     setConsole]      = useState<ConsoleLine>({
    text: 'Esperando credenciales', state: 'idle',
  })

  const emailRef    = useRef<HTMLInputElement>(null)
  const passwordRef = useRef<HTMLInputElement>(null)

  // ── Boot typewriter ────────────────────────────────────────────────────────
  useEffect(() => {
    const timers: ReturnType<typeof setTimeout>[] = []
    BOOT_LINES.forEach((line, i) =>
      timers.push(setTimeout(() => setBootLines(prev => [...prev, line]), BOOT_DELAYS[i] + 300))
    )
    timers.push(setTimeout(() => {
      setBootDone(true)
      emailRef.current?.focus()
    }, BOOT_DELAYS[BOOT_LINES.length - 1] + 600))
    return () => timers.forEach(clearTimeout)
  }, [])

  // ── Login ──────────────────────────────────────────────────────────────────
  const ejecutarLogin = async () => {
    if (!email.trim() || !password.trim() || isLoading) return

    setIsLoading(true)
    setConsole({ text: 'Autenticando credenciales...', state: 'loading' })

    try {
      const res = await fetch(`${API_BASE}/api/v1/auth/login`, {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify({ email: email.trim(), password }),
      })

      if (res.ok) {
        const data = await res.json() as {
          access_token: string; user_id: string; callsign: string
          level: number; is_licensed: boolean
        }
        localStorage.setItem('daki_token',    data.access_token)
        localStorage.setItem('daki_user_id',  data.user_id)
        localStorage.setItem('daki_callsign', data.callsign)
        localStorage.setItem('daki_level',    String(data.level))
        localStorage.setItem('daki_licensed', String(data.is_licensed))
        document.cookie = 'enigma_user=1; path=/; max-age=604800; SameSite=Lax'
        setConsole({ text: `ACCESO CONCEDIDO. BIENVENIDO, ${data.callsign}.`, state: 'success' })
        setTimeout(() => router.push('/hub'), 1000)
        return
      }

      if (res.status === 401) {
        setConsole({ text: 'ERROR 401: CREDENCIALES INVÁLIDAS', state: 'error' })
      } else {
        setConsole({ text: `ERROR ${res.status}: RESPUESTA INESPERADA DEL NEXO`, state: 'error' })
      }
    } catch {
      setConsole({ text: 'ERROR CRÍTICO: FALLO DE CONEXIÓN CON EL NEXO', state: 'error' })
    } finally {
      setIsLoading(false)
    }
  }

  const handleSubmit = (e: React.FormEvent) => { e.preventDefault(); ejecutarLogin() }

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

      <style>{`
        @keyframes cursor-blink { 0%,100%{opacity:1} 50%{opacity:0} }
        @keyframes error-blink  { 0%,100%{opacity:1} 25%,75%{opacity:0.3} }
        .blink       { animation: cursor-blink 1s step-end infinite; }
        .error-blink { animation: error-blink 0.4s ease-in-out 2; }
        .exec-btn {
          border: 1px solid rgba(0,255,65,0.55); color: #00FF41; background: transparent;
          transition: background 0.15s, color 0.15s, box-shadow 0.15s;
        }
        .exec-btn:hover:not(:disabled) {
          background: #00FF41; color: #0A0A0A;
          box-shadow: 0 0 24px rgba(0,255,65,0.4);
        }
        .exec-btn:disabled { border-color:rgba(0,255,65,0.15); color:rgba(0,255,65,0.25); cursor:not-allowed; }
        .input-line { border-bottom: 1px solid rgba(0,255,65,0.2); transition: border-color 0.2s, box-shadow 0.2s; }
        .input-line.focused { border-color: #00FF41; box-shadow: 0 2px 12px rgba(0,255,65,0.2); }
      `}</style>

      <div className="fixed inset-0 pointer-events-none z-10"
        style={{ backgroundImage: 'repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,0.07) 2px,rgba(0,0,0,0.07) 4px)' }}
      />
      <div className="fixed inset-0 pointer-events-none z-10"
        style={{ background: 'radial-gradient(ellipse at center,transparent 50%,rgba(0,0,0,0.75) 100%)' }}
      />

      <div className="relative z-20 w-full max-w-lg px-6 py-10 pb-16">

        {/* Header */}
        <div className="border-b border-[#00FF41]/15 pb-4 mb-8">
          <p className="text-[#00FF41]/25 text-xs tracking-[0.5em] uppercase mb-1">
            {'// ACCESO RESTRINGIDO'}
          </p>
          <h1 className="text-[#00FF41] text-sm md:text-base font-bold tracking-[0.3em] uppercase neon-glow">
            DAKIedtech {'//'}  TERMINAL DE ACCESO
          </h1>
        </div>

        {/* Boot log */}
        {bootLines.length > 0 && (
          <div className="space-y-1 mb-8">
            {bootLines.map((line, i) => (
              <div key={i} className={`text-xs leading-5 ${
                line.includes('[OK]')   ? 'text-[#00FF41]/50'
                : line.includes('LISTA') ? 'text-[#00FF41]/80'
                : 'text-[#00FF41]/30'
              }`}>{line}</div>
            ))}
          </div>
        )}

        {/* Form */}
        {bootDone && (
          <div className="mb-6">
            <p className="text-xs text-[#00FF41]/50 tracking-[0.3em] uppercase mb-5">
              {'> INTRODUZCA CREDENCIALES DE OPERADOR'}
            </p>

            <form onSubmit={handleSubmit}>
              {/* Email */}
              <div className={`input-line pb-2 mb-5 flex items-center gap-2 ${focusedField === 'email' ? 'focused' : ''}`}>
                <span className="text-[#00FF41]/35 select-none text-[10px] tracking-[0.3em] w-24 shrink-0">EMAIL</span>
                <input
                  ref={emailRef}
                  type="email"
                  value={email}
                  onChange={e => setEmail(e.target.value)}
                  onFocus={() => setFocusedField('email')}
                  onBlur={() => setFocusedField(null)}
                  onKeyDown={e => { if (e.key === 'Enter') { e.preventDefault(); passwordRef.current?.focus() } }}
                  placeholder="operador@nexo.io"
                  disabled={isLoading}
                  className="flex-1 bg-transparent text-[#00FF41] text-sm outline-none border-none caret-[#00FF41] tracking-wide placeholder:text-[#00FF41]/15 placeholder:normal-case disabled:opacity-40"
                  autoComplete="email"
                  spellCheck={false}
                />
              </div>

              {/* Password */}
              <div className={`input-line pb-2 mb-6 flex items-center gap-2 ${focusedField === 'password' ? 'focused' : ''}`}>
                <span className="text-[#00FF41]/35 select-none text-[10px] tracking-[0.3em] w-24 shrink-0">CLAVE</span>
                <input
                  ref={passwordRef}
                  type="password"
                  value={password}
                  onChange={e => setPassword(e.target.value)}
                  onFocus={() => setFocusedField('password')}
                  onBlur={() => setFocusedField(null)}
                  placeholder="tu contraseña"
                  disabled={isLoading}
                  className="flex-1 bg-transparent text-[#00FF41] text-sm outline-none border-none caret-[#00FF41] tracking-widest placeholder:text-[#00FF41]/15 placeholder:normal-case placeholder:tracking-wide disabled:opacity-40"
                  autoComplete="current-password"
                />
              </div>

              <button
                type="submit"
                disabled={isLoading || !email.trim() || !password.trim()}
                className="exec-btn w-full py-3 text-xs tracking-[0.4em] uppercase"
              >
                {isLoading ? '[ PROCESANDO... ]' : '[[ EJECUTAR SECUENCIA ]]'}
              </button>
            </form>
          </div>
        )}

        {/* Consola */}
        <div className="border-t border-[#00FF41]/10 pt-4 mt-2 mb-8 min-h-[50px]">
          <p className={`text-xs tracking-wide ${consoleColor} ${consoleGlow} ${console_.state === 'error' ? 'error-blink' : ''}`}>
            {'> Status: '}{console_.text}
            <span className="blink ml-0.5">_</span>
          </p>
        </div>

        {/* Links */}
        <div className="flex flex-col items-center gap-3 text-center">
          <Link
            href="/register"
            className="text-[#00FF41]/20 text-[10px] tracking-[0.3em] hover:text-[#00FF41]/50 transition-colors uppercase"
          >
            {'[ ¿Primera vez? → Crear cuenta de Operador ]'}
          </Link>
          <Link
            href="/"
            className="text-[#00FF41]/10 text-[9px] tracking-[0.25em] hover:text-[#00FF41]/30 transition-colors"
          >
            {'[ Abortar y volver al portal principal ]'}
          </Link>
        </div>

      </div>
    </div>
  )
}
