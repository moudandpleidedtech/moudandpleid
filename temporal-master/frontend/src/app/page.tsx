'use client'

import { useState, useEffect, useRef } from 'react'
import { useRouter } from 'next/navigation'
import { useUserStore } from '@/store/userStore'

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000'

const BOOT_LINES = [
  '> INICIANDO SISTEMA ENIGMA v4.2.1...',
  '> VERIFICANDO INTEGRIDAD DE NUCLEOS...       [OK]',
  '> CARGANDO PROTOCOLOS DE SEGURIDAD...        [OK]',
  '> ESTABLECIENDO CANAL CIFRADO...             [OK]',
  '',
]

const BOOT_DELAYS = [0, 520, 980, 1440, 1900]

type Phase = 'booting' | 'email' | 'password' | 'authenticating' | 'done'

export default function LoginPage() {
  const router = useRouter()
  const { setUser } = useUserStore()

  const [lines, setLines] = useState<string[]>([])
  const [phase, setPhase] = useState<Phase>('booting')
  const [emailVal, setEmailVal] = useState('')
  const [passVal, setPassVal] = useState('')
  const [authLine, setAuthLine] = useState('')
  const [error, setError] = useState('')

  const emailRef = useRef<HTMLInputElement>(null)
  const passRef = useRef<HTMLInputElement>(null)

  // ── Typewriter boot sequence ─────────────────────────────────────────────
  useEffect(() => {
    const timers: ReturnType<typeof setTimeout>[] = []

    BOOT_LINES.forEach((line, i) => {
      timers.push(setTimeout(() => setLines(prev => [...prev, line]), BOOT_DELAYS[i] + 400))
    })

    timers.push(setTimeout(() => setPhase('email'), BOOT_DELAYS[BOOT_LINES.length - 1] + 800))

    return () => timers.forEach(clearTimeout)
  }, [])

  useEffect(() => {
    if (phase === 'email') emailRef.current?.focus()
    if (phase === 'password') passRef.current?.focus()
  }, [phase])

  // ── Handlers ─────────────────────────────────────────────────────────────
  const handleEmailSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!emailVal.trim()) return
    setError('')
    setPhase('password')
  }

  const handlePassSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (phase !== 'password') return
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
      setUser(data)

      // Cookie para que middleware.ts pueda redirigir si ya está autenticado
      document.cookie = 'enigma_user=1; path=/; max-age=604800; SameSite=Lax'
      // Persist userId para páginas que leen de localStorage (boss page)
      localStorage.setItem('userId', data.id as string)

      setAuthLine(`> ACCESO CONCEDIDO. BIENVENIDO, ${(data.username as string).toUpperCase()}.`)
      setPhase('done')

      const seen = typeof window !== 'undefined' && localStorage.getItem('boot_seen')
      setTimeout(() => router.push(seen ? '/misiones' : '/boot-sequence'), 900)
    } catch {
      setPhase('password')
      setAuthLine('')
      setError('> [ERROR 403] CREDENCIAL NO RECONOCIDA. REINTENTE.')
      setTimeout(() => passRef.current?.focus(), 50)
    }
  }

  // ── Render ────────────────────────────────────────────────────────────────
  return (
    <div className="min-h-screen bg-[#0A0A0A] font-mono text-[#00FF41] flex flex-col justify-center px-8 md:px-24 relative overflow-hidden">

      {/* CRT scanlines */}
      <div className="fixed inset-0 pointer-events-none z-10"
        style={{ backgroundImage: 'repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,0.07) 2px,rgba(0,0,0,0.07) 4px)' }} />

      {/* Vignette */}
      <div className="fixed inset-0 pointer-events-none z-10"
        style={{ background: 'radial-gradient(ellipse at center,transparent 55%,rgba(0,0,0,0.65) 100%)' }} />

      <div className="relative z-20 w-full max-w-2xl">

        {/* Header badge */}
        <div className="text-[#00FF41]/20 text-xs tracking-[0.45em] mb-10 uppercase">
          Enigma Terminal // Canal Seguro // v4.2.1
        </div>

        {/* Boot lines */}
        <div className="space-y-1.5 mb-3">
          {lines.map((line, i) => (
            <div key={i} className={`text-sm leading-6 ${
              line === ''           ? 'h-2' :
              line.includes('[OK]') ? 'text-[#00FF41]/55' :
              'text-[#00FF41]/40'
            }`}>
              {line || '\u00A0'}
            </div>
          ))}
        </div>

        {/* EMAIL prompt */}
        {phase === 'email' && (
          <>
            <div className="text-sm text-[#00FF41] mb-1.5">
              {'> INTRODUZCA CREDENCIAL DE ARQUITECTO (EMAIL):'}
            </div>
            <form onSubmit={handleEmailSubmit} className="flex items-center gap-2">
              <span className="text-[#00FF41] select-none">{'>'}</span>
              <input
                ref={emailRef}
                type="text"
                value={emailVal}
                onChange={e => setEmailVal(e.target.value)}
                className="flex-1 bg-transparent text-[#00FF41] text-sm outline-none border-none caret-[#00FF41] tracking-wide"
                autoComplete="off"
                spellCheck={false}
              />
              <span className="text-[#00FF41] animate-pulse select-none">█</span>
            </form>
          </>
        )}

        {/* PASSWORD prompt */}
        {phase === 'password' && (
          <>
            <div className="text-sm text-[#00FF41]/45 mb-1.5">
              {`> CREDENCIAL: ${emailVal}`}
            </div>
            <div className="text-sm text-[#00FF41] mb-1.5">
              {'> INTRODUZCA CLAVE DE ACCESO (PASSWORD):'}
            </div>
            <form onSubmit={handlePassSubmit} className="flex items-center gap-2">
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
            {error && <div className="mt-2 text-red-400 text-xs">{error}</div>}
          </>
        )}

        {/* Auth / done status line */}
        {authLine && (
          <div className={`text-sm mt-1 ${
            authLine.includes('CONCEDIDO')
              ? 'text-[#00FF41]'
              : 'text-[#00FF41]/50 animate-pulse'
          }`}>
            {authLine}
          </div>
        )}

        {/* Enter hint */}
        {(phase === 'email' || phase === 'password') && (
          <div className="mt-8 text-[#00FF41]/18 text-xs tracking-[0.35em]">
            PRESIONE [ENTER] PARA CONTINUAR
          </div>
        )}

      </div>
    </div>
  )
}
