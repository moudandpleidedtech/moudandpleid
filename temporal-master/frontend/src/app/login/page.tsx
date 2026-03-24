'use client'

/**
 * /login — Terminal de Acceso Restringido · DAKI EdTech
 * ──────────────────────────────────────────────────────
 * UI centrada absolutamente. Estética terminal/hacker.
 * Lógica de auth: boot typewriter → email → password → terms → JWT.
 */

import { useState, useEffect, useRef } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { useUserStore } from '@/store/userStore'

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000'

const BOOT_LINES = [
  '> INICIANDO PROTOCOLO DE AUTENTICACIÓN...',
  '> VERIFICANDO INTEGRIDAD DE NÚCLEOS...       [OK]',
  '> CARGANDO PROTOCOLOS DE SEGURIDAD...        [OK]',
  '> ESTABLECIENDO CANAL CIFRADO...             [OK]',
  '> TERMINAL LISTA.',
]
const BOOT_DELAYS = [0, 480, 920, 1360, 1800]

type Phase = 'booting' | 'email' | 'password' | 'terms' | 'authenticating' | 'done'

// ── Checkbox TyC ──────────────────────────────────────────────────────────────
function TermsCheckbox({
  checked,
  onChange,
}: {
  checked: boolean
  onChange: (_v: boolean) => void
}) {
  return (
    <label className="flex items-start gap-3 cursor-pointer group select-none">
      <div
        onClick={() => onChange(!checked)}
        className={`mt-0.5 w-4 h-4 flex-shrink-0 border transition-all duration-150 ${
          checked
            ? 'border-[#00FF41] bg-[#00FF41]/20 shadow-[0_0_8px_rgba(0,255,65,0.4)]'
            : 'border-[#00FF41]/30 bg-transparent group-hover:border-[#00FF41]/60'
        }`}
      >
        {checked && (
          <svg viewBox="0 0 12 12" className="w-full h-full p-0.5 text-[#00FF41]" fill="none">
            <path d="M2 6l3 3 5-5" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        )}
      </div>
      <span className="text-xs text-[#00FF41]/50 leading-5 group-hover:text-[#00FF41]/70 transition-colors">
        He leído y acepto los{' '}
        <a href="/terminos" target="_blank" rel="noopener noreferrer"
          onClick={e => e.stopPropagation()}
          className="text-[#00FF41]/80 underline underline-offset-2 hover:text-[#00FF41] transition-colors">
          Términos y Condiciones
        </a>
        {' '}y la{' '}
        <a href="/privacidad" target="_blank" rel="noopener noreferrer"
          onClick={e => e.stopPropagation()}
          className="text-[#00FF41]/80 underline underline-offset-2 hover:text-[#00FF41] transition-colors">
          Política de Privacidad
        </a>
        {' '}de DAKI EdTech.
      </span>
    </label>
  )
}

function isValidEmail(v: string) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim())
}

// ── Página ────────────────────────────────────────────────────────────────────
export default function LoginPage() {
  const router = useRouter()
  const { setUser } = useUserStore()

  const [lines,         setLines]         = useState<string[]>([])
  const [phase,         setPhase]         = useState<Phase>('booting')
  const [emailVal,      setEmailVal]      = useState('')
  const [passVal,       setPassVal]       = useState('')
  const [termsAccepted, setTermsAccepted] = useState(false)
  const [statusLine,    setStatusLine]    = useState('Esperando credenciales')
  const [error,         setError]         = useState('')
  const [inputFocused,  setInputFocused]  = useState(false)

  const emailRef = useRef<HTMLInputElement>(null)
  const passRef  = useRef<HTMLInputElement>(null)

  // ── Boot typewriter ──────────────────────────────────────────────────────────
  useEffect(() => {
    const timers: ReturnType<typeof setTimeout>[] = []
    BOOT_LINES.forEach((line, i) => {
      timers.push(setTimeout(() => setLines(prev => [...prev, line]), BOOT_DELAYS[i] + 300))
    })
    timers.push(setTimeout(() => {
      setPhase('email')
      setStatusLine('Esperando credenciales')
    }, BOOT_DELAYS[BOOT_LINES.length - 1] + 600))
    return () => timers.forEach(clearTimeout)
  }, [])

  useEffect(() => {
    if (phase === 'email')    emailRef.current?.focus()
    if (phase === 'password') passRef.current?.focus()
  }, [phase])

  // ── Handlers ─────────────────────────────────────────────────────────────────
  const handleEmailSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!emailVal.trim()) return
    if (!isValidEmail(emailVal)) {
      setError('> [ERROR] FORMATO DE CREDENCIAL INVÁLIDO.')
      setStatusLine('Error de validación')
      return
    }
    setError('')
    setStatusLine('Credencial aceptada — ingrese clave')
    setPhase('password')
  }

  const handlePasswordSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!passVal.trim()) return
    setError('')
    setStatusLine('Clave recibida — confirme protocolo legal')
    setPhase('terms')
  }

  const handleLogin = async () => {
    if (!termsAccepted) return
    setPhase('authenticating')
    setStatusLine('Autenticando credenciales...')
    setError('')

    const controller = new AbortController()
    const timeoutId  = setTimeout(() => controller.abort(), 10_000)

    try {
      const res = await fetch(`${API_BASE}/api/v1/users/login`, {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify({ username: emailVal.trim() }),
        signal:  controller.signal,
      })
      clearTimeout(timeoutId)
      if (!res.ok) throw new Error('auth_failed')
      const data = await res.json()

      setUser(data)
      document.cookie = 'enigma_user=1; path=/; max-age=604800; SameSite=Lax'
      localStorage.setItem('userId', data.id as string)

      setStatusLine(`Acceso concedido — ${(data.username as string).toUpperCase()}`)
      setPhase('done')

      const seen = typeof window !== 'undefined' && localStorage.getItem('boot_seen')
      setTimeout(() => router.push(seen ? '/hub' : '/boot-sequence'), 900)
    } catch (err) {
      clearTimeout(timeoutId)
      setPhase('terms')
      const isTimeout = err instanceof DOMException && err.name === 'AbortError'
      setError(
        isTimeout
          ? '> [ERROR 503] NEXO CENTRAL SIN RESPUESTA.'
          : '> [ERROR 403] CREDENCIAL NO RECONOCIDA.',
      )
      setStatusLine('Autenticación fallida')
    }
  }

  const emailValid = isValidEmail(emailVal)
  const isSuccess  = phase === 'done'

  // ── Render ───────────────────────────────────────────────────────────────────
  return (
    <div className="min-h-screen bg-[#0A0A0A] font-mono text-[#00FF41] flex flex-col items-center justify-center relative overflow-hidden">

      {/* Keyframes */}
      <style>{`
        @keyframes cursor-blink {
          0%, 100% { opacity: 1; }
          50%       { opacity: 0; }
        }
        .blink { animation: cursor-blink 1s step-end infinite; }

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
      <div className="relative z-20 w-full max-w-lg px-6">

        {/* ── Header ─────────────────────────────────────────────────────────── */}
        <div className="border-b border-[#00FF41]/15 pb-4 mb-8">
          <p className="text-[#00FF41]/25 text-xs tracking-[0.5em] uppercase mb-1">
            {'// ACCESO RESTRINGIDO'}
          </p>
          <h1 className="text-[#00FF41] text-sm md:text-base font-bold tracking-[0.3em] uppercase neon-glow">
            DAKIedtech {'//'}  PROTOCOLO DE AUTENTICACIÓN
          </h1>
        </div>

        {/* ── Boot log ───────────────────────────────────────────────────────── */}
        {lines.length > 0 && (
          <div className="space-y-1 mb-8">
            {lines.map((line, i) => (
              <div key={i} className={`text-xs leading-5 ${
                line.includes('[OK]')    ? 'text-[#00FF41]/50'
                : line.includes('LISTA') ? 'text-[#00FF41]/80'
                : 'text-[#00FF41]/30'
              }`}>
                {line}
              </div>
            ))}
          </div>
        )}

        {/* ── EMAIL ──────────────────────────────────────────────────────────── */}
        {phase === 'email' && (
          <div className="mb-6">
            <p className="text-xs text-[#00FF41]/50 tracking-[0.3em] uppercase mb-4">
              {'> INTRODUZCA CÓDIGO DE OPERADOR'}
            </p>
            <form onSubmit={handleEmailSubmit}>
              <div className={`input-line pb-2 mb-5 flex items-center gap-2 ${inputFocused ? 'focused' : ''}`}>
                <span className="text-[#00FF41]/50 select-none text-xs">{'>'}</span>
                <input
                  ref={emailRef}
                  type="text"
                  value={emailVal}
                  onChange={e => { setEmailVal(e.target.value); setError('') }}
                  onFocus={() => setInputFocused(true)}
                  onBlur={() => setInputFocused(false)}
                  placeholder="[ INGRESE CÓDIGO DE OPERADOR ]"
                  className="flex-1 bg-transparent text-[#00FF41] text-sm outline-none border-none caret-[#00FF41] tracking-wide placeholder:text-[#00FF41]/20"
                  autoComplete="off"
                  spellCheck={false}
                />
                {emailVal && (
                  <span className={`text-[10px] tracking-widest ${emailValid ? 'text-[#00FF41]/60' : 'text-red-400/60'}`}>
                    {emailValid ? '[OK]' : '[ERR]'}
                  </span>
                )}
              </div>
              <button type="submit" disabled={!emailValid} className="exec-btn w-full py-3 text-xs tracking-[0.4em] uppercase">
                {'[ EJECUTAR SECUENCIA ]'}
              </button>
            </form>
            {error && <p className="mt-3 text-red-400 text-xs">{error}</p>}
          </div>
        )}

        {/* ── PASSWORD ───────────────────────────────────────────────────────── */}
        {phase === 'password' && (
          <div className="mb-6">
            <p className="text-xs text-[#00FF41]/40 tracking-wide mb-1">
              {`> OPERADOR: ${emailVal}`}
            </p>
            <p className="text-xs text-[#00FF41]/50 tracking-[0.3em] uppercase mb-4">
              {'> INTRODUZCA CLAVE DE ACCESO'}
            </p>
            <form onSubmit={handlePasswordSubmit}>
              <div className={`input-line pb-2 mb-5 flex items-center gap-2 ${inputFocused ? 'focused' : ''}`}>
                <span className="text-[#00FF41]/50 select-none text-xs">{'>'}</span>
                <input
                  ref={passRef}
                  type="password"
                  value={passVal}
                  onChange={e => setPassVal(e.target.value)}
                  onFocus={() => setInputFocused(true)}
                  onBlur={() => setInputFocused(false)}
                  placeholder="[ ••••••••••••• ]"
                  className="flex-1 bg-transparent text-[#00FF41] text-sm outline-none border-none caret-[#00FF41] placeholder:text-[#00FF41]/20"
                  autoComplete="off"
                />
              </div>
              <button type="submit" disabled={!passVal.trim()} className="exec-btn w-full py-3 text-xs tracking-[0.4em] uppercase">
                {'[ EJECUTAR SECUENCIA ]'}
              </button>
            </form>
          </div>
        )}

        {/* ── TERMS + CONFIRM ────────────────────────────────────────────────── */}
        {phase === 'terms' && (
          <div className="mb-6">
            <p className="text-xs text-[#00FF41]/40 tracking-wide mb-0.5">{`> OPERADOR: ${emailVal}`}</p>
            <p className="text-xs text-[#00FF41]/40 tracking-wide mb-5">{'> CLAVE: ••••••••'}</p>
            <div className="border border-[#00FF41]/10 bg-[#00FF41]/3 px-4 py-4 mb-5">
              <p className="text-[10px] text-[#00FF41]/30 tracking-[0.3em] uppercase mb-3">
                {'// Protocolo Legal — Sector 00'}
              </p>
              <TermsCheckbox checked={termsAccepted} onChange={setTermsAccepted} />
            </div>
            <button
              onClick={handleLogin}
              disabled={!termsAccepted}
              className="exec-btn w-full py-3 text-xs tracking-[0.4em] uppercase"
            >
              {termsAccepted ? '[ EJECUTAR SECUENCIA ]' : '[ ACEPTE EL PROTOCOLO PARA CONTINUAR ]'}
            </button>
            {error && <p className="mt-3 text-red-400 text-xs">{error}</p>}
          </div>
        )}

        {/* ── AUTHENTICATING ─────────────────────────────────────────────────── */}
        {phase === 'authenticating' && (
          <div className="mb-6">
            <p className="text-xs text-[#00FF41]/60 animate-pulse tracking-[0.3em]">
              {'> AUTENTICANDO... ESPERE'}
            </p>
          </div>
        )}

        {/* ── DONE ───────────────────────────────────────────────────────────── */}
        {phase === 'done' && (
          <div className="mb-6">
            <p className="text-sm text-[#00FF41] neon-glow tracking-[0.2em]">
              {'> ACCESO CONCEDIDO. REDIRIGIENDO...'}
            </p>
          </div>
        )}

        {/* ── Consola de estado ──────────────────────────────────────────────── */}
        <div className="border-t border-[#00FF41]/10 pt-4 mt-2 mb-8">
          <p className={`text-xs tracking-wide ${isSuccess ? 'text-[#00FF41]' : 'text-[#00FF41]/35'}`}>
            {'> Status: '}{statusLine}
            <span className="blink ml-0.5">_</span>
          </p>
          {(phase === 'email' || phase === 'password') && (
            <p className="mt-1 text-[#00FF41]/15 text-[10px] tracking-[0.3em]">
              PRESIONE [ENTER] PARA CONTINUAR
            </p>
          )}
        </div>

        {/* ── NUEVO OPERADOR ─────────────────────────────────────────────────── */}
        {phase === 'email' && (
          <p className="text-[#00FF41]/15 text-xs tracking-[0.2em] mb-6">
            NUEVO OPERADOR?{' '}
            <a href="https://pay.dakiedtech.com" target="_blank" rel="noopener noreferrer"
              className="text-[#00FF41]/30 hover:text-[#00FF41]/60 underline underline-offset-2 transition-colors">
              ADQUIRIR LICENCIA
            </a>
          </p>
        )}

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
