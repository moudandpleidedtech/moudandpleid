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
import { useUserStore } from '@/store/userStore'

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
  const { _hasHydrated, userId, setUser } = useUserStore()

  // Guard inverso: sesión activa en el store → no mostrar login
  useEffect(() => {
    if (_hasHydrated && userId) router.replace('/hub')
  }, [_hasHydrated, userId, router])

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
          level: number; is_licensed: boolean; role?: string
        }
        localStorage.setItem('daki_user_id',  data.user_id)
        localStorage.setItem('daki_callsign', data.callsign)
        localStorage.setItem('daki_level',    String(data.level))
        localStorage.setItem('daki_licensed', String(data.is_licensed))
        setUser({
          id:           data.user_id,
          username:     data.callsign,
          current_level: data.level,
          total_xp:     0,
          streak_days:  0,
          is_paid:      data.is_licensed,
          role:         data.role,
        })
        document.cookie = 'enigma_user=1; path=/; max-age=604800; SameSite=Lax'
        setConsole({ text: `ACCESO CONCEDIDO. BIENVENIDO, ${data.callsign}.`, state: 'success' })
        const destination = localStorage.getItem('boot_seen') ? '/hub' : '/boot-sequence'
        setTimeout(() => router.push(destination), 1000)
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

            {/* ── Divisor ── */}
            <div className="flex items-center gap-3 my-5">
              <div className="flex-1 h-px" style={{ background: 'rgba(0,255,65,0.08)' }} />
              <span className="text-[9px] tracking-[0.4em] uppercase" style={{ color: 'rgba(0,255,65,0.22)' }}>
                O CONTINUAR CON
              </span>
              <div className="flex-1 h-px" style={{ background: 'rgba(0,255,65,0.08)' }} />
            </div>

            {/* ── Google OAuth — deshabilitado durante revisión de Google ── */}
            <div
              className="flex items-center justify-center gap-3 w-full py-3 border cursor-not-allowed relative"
              style={{
                borderColor: 'rgba(0,255,65,0.08)',
                background:  'rgba(0,255,65,0.01)',
                color:       'rgba(0,255,65,0.20)',
              }}
              title="Verificación de Google en progreso — disponible próximamente"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" style={{ opacity: 0.25 }}>
                <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
                <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
                <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.84z" fill="#FBBC05"/>
                <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
              </svg>
              <span className="text-[10px] tracking-[0.3em] font-bold uppercase">
                Google — Verificación en progreso
              </span>
            </div>
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
