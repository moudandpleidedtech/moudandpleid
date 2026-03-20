'use client'

import { useState, useEffect, useRef } from 'react'
import { useRouter } from 'next/navigation'
import { useUserStore } from '@/store/userStore'

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000'

const BOOT_LINES = [
  '> INICIANDO PROTOCOLO DE ACCESO ENIGMA v4.2.1...',
  '> VERIFICANDO INTEGRIDAD DE NÚCLEOS...       [OK]',
  '> CARGANDO PROTOCOLOS DE SEGURIDAD...        [OK]',
  '> ESTABLECIENDO CANAL CIFRADO...             [OK]',
  '',
]
const BOOT_DELAYS = [0, 520, 980, 1440, 1900]

type Phase = 'booting' | 'email' | 'password' | 'terms' | 'authenticating' | 'done'

// ── Modal de pago denegado ────────────────────────────────────────────────────
function UnpaidModal({ onClose }: { onClose: () => void }) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center px-6">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/80 backdrop-blur-sm"
        onClick={onClose}
      />

      {/* Panel */}
      <div className="relative z-10 w-full max-w-md border border-red-500/60 bg-[#0A0A0A] p-8 shadow-[0_0_60px_rgba(239,68,68,0.15)]">

        {/* Corner accents */}
        <span className="absolute top-0 left-0 w-3 h-3 border-t-2 border-l-2 border-red-500" />
        <span className="absolute top-0 right-0 w-3 h-3 border-t-2 border-r-2 border-red-500" />
        <span className="absolute bottom-0 left-0 w-3 h-3 border-b-2 border-l-2 border-red-500" />
        <span className="absolute bottom-0 right-0 w-3 h-3 border-b-2 border-r-2 border-red-500" />

        {/* Header */}
        <div className="flex items-center gap-3 mb-6">
          <div className="w-2 h-2 rounded-full bg-red-500 animate-pulse" />
          <span className="text-red-400 text-xs tracking-[0.4em] uppercase font-mono">
            Error 402 — Acceso Denegado
          </span>
        </div>

        {/* Message */}
        <p className="font-mono text-sm text-[#00FF41]/80 leading-7 mb-2">
          Tu enlace neuronal{' '}
          <span className="text-red-400 font-semibold">no ha sido financiado</span>.
        </p>
        <p className="font-mono text-xs text-[#00FF41]/40 leading-6 mb-8">
          El Nexo Central requiere una Licencia de Operador activa para
          establecer la conexión. Sin ella, el acceso al sistema permanece
          bloqueado.
        </p>

        {/* CTA */}
        <a
          href="https://pay.glitchandgold.com"
          target="_blank"
          rel="noopener noreferrer"
          className="group block w-full py-3 text-center font-mono text-sm tracking-[0.25em] uppercase
                     bg-[#00FF41]/10 border border-[#00FF41]/40 text-[#00FF41]
                     hover:bg-[#00FF41]/20 hover:border-[#00FF41]/80
                     hover:shadow-[0_0_20px_rgba(0,255,65,0.2)]
                     transition-all duration-200 mb-3"
        >
          [ Adquirir Licencia de Operador ]
        </a>
        <button
          onClick={onClose}
          className="w-full py-2 font-mono text-xs text-[#00FF41]/30 hover:text-[#00FF41]/60
                     tracking-[0.2em] transition-colors"
        >
          CANCELAR
        </button>
      </div>
    </div>
  )
}

// ── Checkbox TyC ──────────────────────────────────────────────────────────────
function TermsCheckbox({
  checked,
  onChange,
}: {
  checked: boolean
  onChange: (v: boolean) => void
}) {
  return (
    <label className="flex items-start gap-3 cursor-pointer group select-none mt-5">
      {/* Custom checkbox */}
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

      {/* Label */}
      <span className="text-xs text-[#00FF41]/50 leading-5 group-hover:text-[#00FF41]/70 transition-colors">
        He leído y acepto los{' '}
        <a
          href="/terminos"
          target="_blank"
          rel="noopener noreferrer"
          onClick={e => e.stopPropagation()}
          className="text-[#00FF41]/80 underline underline-offset-2 hover:text-[#00FF41] transition-colors"
        >
          Términos y Condiciones
        </a>
        {' '}y la{' '}
        <a
          href="/privacidad"
          target="_blank"
          rel="noopener noreferrer"
          onClick={e => e.stopPropagation()}
          className="text-[#00FF41]/80 underline underline-offset-2 hover:text-[#00FF41] transition-colors"
        >
          Política de Privacidad
        </a>
        {' '}de GlitchAndGold.
      </span>
    </label>
  )
}

// ── Validación de email simple ────────────────────────────────────────────────
function isValidEmail(v: string) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim())
}

// ── Página principal ──────────────────────────────────────────────────────────
export default function LoginPage() {
  const router = useRouter()
  const { setUser } = useUserStore()

  const [lines, setLines] = useState<string[]>([])
  const [phase, setPhase] = useState<Phase>('booting')
  const [emailVal, setEmailVal] = useState('')
  const [passVal, setPassVal] = useState('')
  const [termsAccepted, setTermsAccepted] = useState(false)
  const [authLine, setAuthLine] = useState('')
  const [error, setError] = useState('')
  const [showUnpaid, setShowUnpaid] = useState(false)

  const emailRef = useRef<HTMLInputElement>(null)
  const passRef  = useRef<HTMLInputElement>(null)

  // ── Boot typewriter ─────────────────────────────────────────────────────────
  useEffect(() => {
    const timers: ReturnType<typeof setTimeout>[] = []
    BOOT_LINES.forEach((line, i) => {
      timers.push(setTimeout(() => setLines(prev => [...prev, line]), BOOT_DELAYS[i] + 400))
    })
    timers.push(setTimeout(() => setPhase('email'), BOOT_DELAYS[BOOT_LINES.length - 1] + 800))
    return () => timers.forEach(clearTimeout)
  }, [])

  useEffect(() => {
    if (phase === 'email')    emailRef.current?.focus()
    if (phase === 'password') passRef.current?.focus()
  }, [phase])

  // ── Handlers ────────────────────────────────────────────────────────────────
  const handleEmailSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!emailVal.trim()) return
    if (!isValidEmail(emailVal)) {
      setError('> [ERROR] FORMATO DE CREDENCIAL INVÁLIDO.')
      return
    }
    setError('')
    setPhase('password')
  }

  const handlePasswordSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!passVal.trim()) return
    setError('')
    setPhase('terms')
  }

  const handleLogin = async () => {
    if (!termsAccepted) return
    setPhase('authenticating')
    setAuthLine('> AUTENTICANDO CREDENCIALES...')
    setError('')

    try {
      const res = await fetch(`${API_BASE}/api/v1/users/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: emailVal.trim() }),
      })
      if (!res.ok) throw new Error('auth_failed')
      const data = await res.json()

      // Pago no verificado → modal sin setUser
      if (!data.is_paid) {
        setPhase('terms')
        setAuthLine('')
        setShowUnpaid(true)
        return
      }

      setUser(data)
      document.cookie = 'enigma_user=1; path=/; max-age=604800; SameSite=Lax'
      localStorage.setItem('userId', data.id as string)

      setAuthLine(`> ACCESO CONCEDIDO. BIENVENIDO, ${(data.username as string).toUpperCase()}.`)
      setPhase('done')

      const seen = typeof window !== 'undefined' && localStorage.getItem('boot_seen')
      setTimeout(() => router.push(seen ? '/hub' : '/boot-sequence'), 900)
    } catch {
      setPhase('terms')
      setAuthLine('')
      setError('> [ERROR 403] CREDENCIAL NO RECONOCIDA. REINTENTE.')
    }
  }

  // ── Helpers ─────────────────────────────────────────────────────────────────
  const emailValid = isValidEmail(emailVal)

  // ── Render ──────────────────────────────────────────────────────────────────
  return (
    <>
      {showUnpaid && <UnpaidModal onClose={() => setShowUnpaid(false)} />}

      <div className="min-h-screen bg-[#0A0A0A] font-mono text-[#00FF41] flex flex-col justify-center px-8 md:px-24 relative overflow-hidden">

        {/* CRT scanlines */}
        <div
          className="fixed inset-0 pointer-events-none z-10"
          style={{
            backgroundImage:
              'repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,0.07) 2px,rgba(0,0,0,0.07) 4px)',
          }}
        />

        {/* Vignette */}
        <div
          className="fixed inset-0 pointer-events-none z-10"
          style={{
            background:
              'radial-gradient(ellipse at center,transparent 55%,rgba(0,0,0,0.65) 100%)',
          }}
        />

        <div className="relative z-20 w-full max-w-2xl">

          {/* Header badge */}
          <div className="text-[#00FF41]/20 text-xs tracking-[0.45em] mb-10 uppercase">
            GlitchAndGold // Canal Seguro // v4.2.1
          </div>

          {/* Boot lines */}
          <div className="space-y-1.5 mb-3">
            {lines.map((line, i) => (
              <div
                key={i}
                className={`text-sm leading-6 ${
                  line === ''            ? 'h-2'
                  : line.includes('[OK]') ? 'text-[#00FF41]/55'
                  : 'text-[#00FF41]/40'
                }`}
              >
                {line || '\u00A0'}
              </div>
            ))}
          </div>

          {/* ── EMAIL ─────────────────────────────────────────────────────── */}
          {phase === 'email' && (
            <>
              <div className="text-sm text-[#00FF41] mb-1.5">
                {'> INTRODUZCA CREDENCIAL DE OPERADOR (EMAIL):'}
              </div>
              <form onSubmit={handleEmailSubmit} className="flex items-center gap-2">
                <span className="text-[#00FF41] select-none">{'>'}</span>
                <input
                  ref={emailRef}
                  type="text"
                  value={emailVal}
                  onChange={e => { setEmailVal(e.target.value); setError('') }}
                  className="flex-1 bg-transparent text-[#00FF41] text-sm outline-none border-none caret-[#00FF41] tracking-wide"
                  autoComplete="off"
                  spellCheck={false}
                  placeholder="operador@nexo.io"
                />
                {emailVal && (
                  <span className={`text-xs ${emailValid ? 'text-[#00FF41]/60' : 'text-red-400/60'}`}>
                    {emailValid ? '[VÁLIDO]' : '[INVÁLIDO]'}
                  </span>
                )}
                <span className="text-[#00FF41] animate-pulse select-none">█</span>
              </form>
              {error && <div className="mt-2 text-red-400 text-xs">{error}</div>}
            </>
          )}

          {/* ── PASSWORD ──────────────────────────────────────────────────── */}
          {phase === 'password' && (
            <>
              <div className="text-sm text-[#00FF41]/45 mb-1.5">
                {`> CREDENCIAL: ${emailVal}`}
              </div>
              <div className="text-sm text-[#00FF41] mb-1.5">
                {'> INTRODUZCA CLAVE DE ACCESO:'}
              </div>
              <form onSubmit={handlePasswordSubmit} className="flex items-center gap-2">
                <span className="text-[#00FF41] select-none">{'>'}</span>
                <input
                  ref={passRef}
                  type="password"
                  value={passVal}
                  onChange={e => setPassVal(e.target.value)}
                  className="flex-1 bg-transparent text-[#00FF41] text-sm outline-none border-none caret-[#00FF41]"
                  autoComplete="off"
                />
                <span className="text-[#00FF41] animate-pulse select-none">█</span>
              </form>
            </>
          )}

          {/* ── TERMS + SUBMIT ────────────────────────────────────────────── */}
          {phase === 'terms' && (
            <>
              {/* Resumen de credenciales */}
              <div className="text-sm text-[#00FF41]/40 mb-0.5">
                {`> CREDENCIAL: ${emailVal}`}
              </div>
              <div className="text-sm text-[#00FF41]/40 mb-3">
                {'> CLAVE: ••••••••'}
              </div>

              {/* Bloque legal */}
              <div className="border border-[#00FF41]/12 bg-[#00FF41]/3 px-4 py-4">
                <div className="text-xs text-[#00FF41]/30 tracking-[0.3em] uppercase mb-3">
                  // Protocolo Legal — Sector 00
                </div>
                <TermsCheckbox checked={termsAccepted} onChange={setTermsAccepted} />
              </div>

              {/* Botón Ingresar */}
              <button
                onClick={handleLogin}
                disabled={!termsAccepted}
                className={`mt-5 w-full py-3 text-sm tracking-[0.3em] uppercase font-mono border
                  transition-all duration-200
                  ${
                    termsAccepted
                      ? 'border-[#00FF41]/60 text-[#00FF41] bg-[#00FF41]/8 hover:bg-[#00FF41]/15 hover:border-[#00FF41] hover:shadow-[0_0_20px_rgba(0,255,65,0.15)] cursor-pointer'
                      : 'border-[#00FF41]/15 text-[#00FF41]/25 bg-transparent cursor-not-allowed'
                  }`}
              >
                {termsAccepted ? '[ INGRESAR AL NEXO ]' : '[ ACEPTA LOS TÉRMINOS PARA CONTINUAR ]'}
              </button>

              {error && <div className="mt-2 text-red-400 text-xs">{error}</div>}
            </>
          )}

          {/* ── AUTH STATUS LINE ──────────────────────────────────────────── */}
          {authLine && (
            <div
              className={`text-sm mt-1 ${
                authLine.includes('CONCEDIDO')
                  ? 'text-[#00FF41]'
                  : 'text-[#00FF41]/50 animate-pulse'
              }`}
            >
              {authLine}
            </div>
          )}

          {/* ── ENTER HINT ────────────────────────────────────────────────── */}
          {(phase === 'email' || phase === 'password') && (
            <div className="mt-8 text-[#00FF41]/18 text-xs tracking-[0.35em]">
              PRESIONE [ENTER] PARA CONTINUAR
            </div>
          )}

          {/* ── REGISTRO HINT ─────────────────────────────────────────────── */}
          {phase === 'email' && (
            <div className="mt-12 text-[#00FF41]/15 text-xs tracking-[0.2em]">
              NUEVO OPERADOR?{' '}
              <a
                href="https://pay.glitchandgold.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-[#00FF41]/30 hover:text-[#00FF41]/60 underline underline-offset-2 transition-colors"
              >
                ADQUIRIR LICENCIA
              </a>
            </div>
          )}

        </div>
      </div>
    </>
  )
}
