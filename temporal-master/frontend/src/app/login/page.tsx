'use client'

/**
 * /login — Terminal de Acceso Restringido · DAKI EdTech
 * ──────────────────────────────────────────────────────
 * Modo ACCEDER  → POST /api/v1/auth/login     { email, password }
 * Modo REGISTRAR → POST /api/v1/auth/register { email, password }
 * En ambos casos: guarda JWT + cookie → redirige a /hub
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
  '> TERMINAL LISTA. INGRESE CREDENCIALES DE OPERADOR.',
]
const BOOT_DELAYS = [0, 480, 920, 1360, 1800]

type Mode        = 'login' | 'register'
type ConsoleState = 'idle' | 'loading' | 'success' | 'error'

interface ConsoleLine {
  text:  string
  state: ConsoleState
}

export default function LoginPage() {
  const router = useRouter()

  const [bootLines,    setBootLines]    = useState<string[]>([])
  const [bootDone,     setBootDone]     = useState(false)
  const [mode,         setMode]         = useState<Mode>('login')
  const [email,        setEmail]        = useState('')
  const [callsign,     setCallsign]     = useState('')
  const [password,     setPassword]     = useState('')
  const [founderCode,  setFounderCode]  = useState('')
  const [showAlpha,    setShowAlpha]    = useState(false)
  const [isLoading,    setIsLoading]    = useState(false)
  const [focusedField, setFocusedField] = useState<string | null>(null)
  const [console_,     setConsole]      = useState<ConsoleLine>({
    text:  'Esperando credenciales',
    state: 'idle',
  })

  const emailRef    = useRef<HTMLInputElement>(null)
  const callsignRef = useRef<HTMLInputElement>(null)
  const passwordRef = useRef<HTMLInputElement>(null)

  // ── Boot typewriter ──────────────────────────────────────────────────────────
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

  // ── Reset consola al cambiar de modo ────────────────────────────────────────
  useEffect(() => {
    setConsole({ text: 'Esperando credenciales', state: 'idle' })
    setCallsign('')
    setFounderCode('')
    setShowAlpha(false)
  }, [mode])

  // ── Enviar ───────────────────────────────────────────────────────────────────
  const ejecutarSecuencia = async () => {
    if (!email.trim() || !password.trim() || isLoading) return
    if (mode === 'register' && !callsign.trim()) return

    setIsLoading(true)
    setConsole({ text: 'Autenticando credenciales...', state: 'loading' })

    const endpoint = mode === 'login'
      ? `${API_BASE}/api/v1/auth/login`
      : `${API_BASE}/api/v1/auth/register`

    try {
      const res = await fetch(endpoint, {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify(
          mode === 'register'
            ? {
                email:    email.trim(),
                callsign: callsign.trim(),
                password,
                ...(founderCode.trim() ? { founder_code: founderCode.trim() } : {}),
              }
            : { email: email.trim(), password }
        ),
      })

      if (res.ok) {
        const data = await res.json() as {
          access_token: string; user_id: string; callsign: string
          level: number; is_licensed: boolean; founder_code_applied?: boolean
        }
        localStorage.setItem('daki_token',    data.access_token)
        localStorage.setItem('daki_user_id',  data.user_id)
        localStorage.setItem('daki_callsign', data.callsign)
        localStorage.setItem('daki_level',    String(data.level))
        localStorage.setItem('daki_licensed', String(data.is_licensed))
        // Cookie para middleware de Next.js
        document.cookie = 'enigma_user=1; path=/; max-age=604800; SameSite=Lax'
        const msg = data.founder_code_applied
          ? `LICENCIA DE FUNDADOR ACTIVADA. Bienvenido, ${data.callsign}.`
          : 'ACCESO CONCEDIDO. Abriendo el Nexo...'
        setConsole({ text: msg, state: 'success' })
        setTimeout(() => router.push('/hub'), 1200)
        return
      }

      const err = await res.json().catch(() => ({})) as { detail?: string }
      if (res.status === 401) {
        setConsole({ text: 'ERROR 401: CREDENCIALES INVÁLIDAS', state: 'error' })
      } else if (res.status === 409) {
        setConsole({ text: 'ERROR 409: EMAIL YA REGISTRADO EN EL SISTEMA', state: 'error' })
      } else if (res.status === 422) {
        const msg = err.detail ?? 'DATOS INVÁLIDOS'
        setConsole({ text: `ERROR 422: ${String(msg).toUpperCase()}`, state: 'error' })
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

  const switchMode = (m: Mode) => {
    if (isLoading) return
    setMode(m)
    setEmail('')
    setCallsign('')
    setPassword('')
    setTimeout(() => emailRef.current?.focus(), 50)
  }

  // ── Color de consola ─────────────────────────────────────────────────────────
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

        .mode-btn {
          border: 1px solid transparent;
          background: transparent;
          color: rgba(0,255,65,0.25);
          transition: all 0.15s ease;
          letter-spacing: 0.25em;
          font-size: 9px;
          text-transform: uppercase;
          padding: 5px 12px;
        }
        .mode-btn.active {
          border-color: rgba(0,255,65,0.5);
          color: #00FF41;
          background: rgba(0,255,65,0.05);
        }
        .mode-btn:not(.active):hover {
          color: rgba(0,255,65,0.55);
          border-color: rgba(0,255,65,0.2);
        }
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

        {/* ── Formulario ───────────────────────────────────────────────────── */}
        {bootDone && (
          <div className="mb-6">

            {/* Selector de modo */}
            <div className="flex gap-2 mb-6">
              <button
                type="button"
                onClick={() => switchMode('login')}
                className={`mode-btn ${mode === 'login' ? 'active' : ''}`}
              >
                [[ ACCEDER ]]
              </button>
              <button
                type="button"
                onClick={() => switchMode('register')}
                className={`mode-btn ${mode === 'register' ? 'active' : ''}`}
              >
                [[ REGISTRAR ]]
              </button>
            </div>

            <p className="text-xs text-[#00FF41]/50 tracking-[0.3em] uppercase mb-5">
              {mode === 'login'
                ? '> INTRODUZCA CREDENCIALES DE OPERADOR'
                : '> CREAR NUEVA CUENTA DE OPERADOR'}
            </p>

            <form onSubmit={handleSubmit}>

              {/* Email */}
              <div className={`input-line pb-2 mb-5 flex items-center gap-2 ${focusedField === 'email' ? 'focused' : ''}`}>
                <span className="text-[#00FF41]/35 select-none text-[10px] tracking-[0.3em] w-20 shrink-0">EMAIL</span>
                <input
                  ref={emailRef}
                  type="email"
                  value={email}
                  onChange={e => setEmail(e.target.value)}
                  onFocus={() => setFocusedField('email')}
                  onBlur={() => setFocusedField(null)}
                  onKeyDown={e => {
                    if (e.key === 'Enter') {
                      e.preventDefault()
                      mode === 'register' ? callsignRef.current?.focus() : passwordRef.current?.focus()
                    }
                  }}
                  placeholder="operador@nexo.io"
                  disabled={isLoading}
                  className="flex-1 bg-transparent text-[#00FF41] text-sm outline-none border-none caret-[#00FF41] tracking-wide placeholder:text-[#00FF41]/15 placeholder:normal-case disabled:opacity-40"
                  autoComplete="email"
                  spellCheck={false}
                />
              </div>

              {/* Callsign — solo en modo register */}
              {mode === 'register' && (
                <div className={`input-line pb-2 mb-5 flex items-center gap-2 ${focusedField === 'callsign' ? 'focused' : ''}`}>
                  <span className="text-[#00FF41]/35 select-none text-[10px] tracking-[0.3em] w-20 shrink-0">CALLSIGN</span>
                  <input
                    ref={callsignRef}
                    type="text"
                    value={callsign}
                    onChange={e => setCallsign(e.target.value.replace(/\s/g, ''))}
                    onFocus={() => setFocusedField('callsign')}
                    onBlur={() => setFocusedField(null)}
                    onKeyDown={e => { if (e.key === 'Enter') { e.preventDefault(); passwordRef.current?.focus() } }}
                    placeholder="Ej: Ghost-Zero"
                    disabled={isLoading}
                    maxLength={20}
                    className="flex-1 bg-transparent text-[#00FF41] text-sm outline-none border-none caret-[#00FF41] tracking-widest uppercase placeholder:text-[#00FF41]/15 placeholder:normal-case placeholder:tracking-wide disabled:opacity-40"
                    autoComplete="off"
                    spellCheck={false}
                  />
                </div>
              )}

              {/* Password */}
              <div className={`input-line pb-2 mb-6 flex items-center gap-2 ${focusedField === 'password' ? 'focused' : ''}`}>
                <span className="text-[#00FF41]/35 select-none text-[10px] tracking-[0.3em] w-20 shrink-0">CLAVE</span>
                <input
                  ref={passwordRef}
                  type="password"
                  value={password}
                  onChange={e => setPassword(e.target.value)}
                  onFocus={() => setFocusedField('password')}
                  onBlur={() => setFocusedField(null)}
                  placeholder="mínimo 8 caracteres"
                  disabled={isLoading}
                  className="flex-1 bg-transparent text-[#00FF41] text-sm outline-none border-none caret-[#00FF41] tracking-widest placeholder:text-[#00FF41]/15 placeholder:normal-case placeholder:tracking-wide disabled:opacity-40"
                  autoComplete={mode === 'register' ? 'new-password' : 'current-password'}
                />
              </div>

              {/* Alpha Tester section — solo en registro */}
              {mode === 'register' && (
                <div className="mb-5">
                  <button
                    type="button"
                    onClick={() => setShowAlpha(v => !v)}
                    className="text-[9px] tracking-[0.35em] text-[#00FF41]/25 hover:text-[#00FF41]/50 transition-colors uppercase"
                  >
                    {showAlpha ? '[-]' : '[+]'} ¿Eres Alpha Tester? Ingresa tu código de Fundador
                  </button>

                  {showAlpha && (
                    <div className={`input-line pb-2 mt-3 flex items-center gap-2 ${focusedField === 'founder' ? 'focused' : ''}`}>
                      <span className="text-[#FFB800]/40 select-none text-[10px] tracking-[0.25em] w-20 shrink-0">CÓDIGO</span>
                      <input
                        type="text"
                        value={founderCode}
                        onChange={e => setFounderCode(e.target.value.toUpperCase())}
                        onFocus={() => setFocusedField('founder')}
                        onBlur={() => setFocusedField(null)}
                        placeholder="GLITCH-GOLD-INIT"
                        disabled={isLoading}
                        className="flex-1 bg-transparent text-[#FFB800] text-xs outline-none border-none caret-[#FFB800] tracking-widest uppercase placeholder:text-[#FFB800]/20 placeholder:tracking-wide disabled:opacity-40"
                        style={{ borderBottom: '1px solid rgba(255,184,0,0.25)' }}
                        autoComplete="off"
                        spellCheck={false}
                      />
                    </div>
                  )}
                </div>
              )}

              <button
                type="submit"
                disabled={isLoading || !email.trim() || !password.trim() || (mode === 'register' && !callsign.trim())}
                className="exec-btn w-full py-3 text-xs tracking-[0.4em] uppercase"
              >
                {isLoading
                  ? '[ PROCESANDO... ]'
                  : mode === 'login'
                    ? '[[ EJECUTAR SECUENCIA ]]'
                    : '[[ CREAR CUENTA ]]'}
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
