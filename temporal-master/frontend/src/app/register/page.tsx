'use client'

/**
 * /register — Protocolo de Reclutamiento · DAKI EdTech
 * ──────────────────────────────────────────────────────
 * Flujo:
 *  1. Boot sequence con escaneo silencioso del localStorage
 *  2. Si detecta sesión anterior → muestra panel de migración en amber
 *  3. Formulario: EMAIL + CALLSIGN + CLAVE + [opcional] Código de Fundador
 *  4. POST /api/v1/auth/register con campos de migración inyectados
 *  5. Éxito → limpia keys legacy, guarda nuevo JWT, redirige a /hub
 */

import { useState, useEffect, useRef } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { useUserStore } from '@/store/userStore'

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? ''

// Keys legacy a limpiar tras migración exitosa
const LEGACY_KEYS = [
  'beta_token', 'daki_token', 'daki_user_id',
  'daki_callsign', 'daki_level', 'daki_licensed', 'daki_mission_state',
]

const BOOT_LINES = [
  '> INICIANDO PROTOCOLO DE RECLUTAMIENTO...',
  '> ESCANEANDO SESIÓN LOCAL...',
  '> ANÁLISIS DE PERFIL COMPLETADO.          [OK]',
  '> CANAL CIFRADO ESTABLECIDO.              [OK]',
  '> FORMULARIO DE IDENTIDAD LISTO.',
]
const BOOT_DELAYS = [0, 500, 1050, 1550, 2050]

type ConsoleState = 'idle' | 'loading' | 'success' | 'error'

interface ConsoleLine { text: string; state: ConsoleState }

interface DetectedSession {
  level:         number | null
  callsign:      string | null
  hasBetaSession: boolean
  missionState:  Record<string, unknown> | null
}

// ── Escaneo silencioso del localStorage ──────────────────────────────────────
function scanLocalSession(): DetectedSession {
  if (typeof window === 'undefined') {
    return { level: null, callsign: null, hasBetaSession: false, missionState: null }
  }
  const rawLevel    = localStorage.getItem('daki_level')
  const callsign    = localStorage.getItem('daki_callsign') ?? null
  const betaToken   = localStorage.getItem('beta_token')
  const dakiToken   = localStorage.getItem('daki_token')
  const rawMission  = localStorage.getItem('daki_mission_state')

  const level = rawLevel ? parseInt(rawLevel, 10) : null

  let missionState: Record<string, unknown> | null = null
  if (rawMission) {
    try { missionState = JSON.parse(rawMission) } catch { /* ignore */ }
  }

  return {
    level:          level && level > 1 ? level : null,
    callsign:       callsign && callsign.length >= 3 ? callsign : null,
    hasBetaSession: !!(betaToken || dakiToken),
    missionState,
  }
}

// ─────────────────────────────────────────────────────────────────────────────

export default function RegisterPage() {
  const router = useRouter()
  const { setUser } = useUserStore()

  const [bootLines,    setBootLines]    = useState<string[]>([])
  const [bootDone,     setBootDone]     = useState(false)
  const [detected,     setDetected]     = useState<DetectedSession | null>(null)
  const [email,        setEmail]        = useState('')
  const [callsign,     setCallsign]     = useState('')
  const [password,     setPassword]     = useState('')
  const [founderCode,  setFounderCode]  = useState('')
  const [showFounder,  setShowFounder]  = useState(false)
  const [isLoading,    setIsLoading]    = useState(false)
  const [focusedField, setFocusedField] = useState<string | null>(null)
  const [console_,     setConsole]      = useState<ConsoleLine>({
    text: 'Esperando datos de Operador', state: 'idle',
  })

  const emailRef    = useRef<HTMLInputElement>(null)
  const callsignRef = useRef<HTMLInputElement>(null)
  const passwordRef = useRef<HTMLInputElement>(null)

  // ── Boot + escaneo ──────────────────────────────────────────────────────────
  useEffect(() => {
    const session = scanLocalSession()

    const timers: ReturnType<typeof setTimeout>[] = []
    BOOT_LINES.forEach((line, i) =>
      timers.push(setTimeout(() => setBootLines(prev => [...prev, line]), BOOT_DELAYS[i] + 200))
    )

    // Después del último boot line, revelar datos detectados y formulario
    timers.push(setTimeout(() => {
      setDetected(session)
      if (session.callsign) setCallsign(session.callsign)
      setBootDone(true)
      emailRef.current?.focus()
    }, BOOT_DELAYS[BOOT_LINES.length - 1] + 500))

    return () => timers.forEach(clearTimeout)
  }, [])

  // ── Enviar registro ─────────────────────────────────────────────────────────
  const ejecutarRegistro = async () => {
    if (!email.trim() || !callsign.trim() || !password.trim() || isLoading) return

    setIsLoading(true)
    setConsole({ text: 'Transmitiendo datos al Nexo...', state: 'loading' })

    // ── Construir cuerpo con campos de migración ───────────────────────────
    const body: Record<string, unknown> = {
      email:    email.trim(),
      callsign: callsign.trim(),
      password,
    }

    // Inyección silenciosa de progreso detectado
    if (detected?.level) {
      body.migrated_level = detected.level
    }
    if (detected?.missionState && Object.keys(detected.missionState).length > 0) {
      body.migrated_mission_state = detected.missionState
    }
    if (founderCode.trim()) {
      body.founder_code = founderCode.trim().toUpperCase()
    }

    try {
      const res = await fetch(`${API_BASE}/api/v1/auth/register`, {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify(body),
      })

      if (res.ok) {
        const data = await res.json() as {
          access_token: string; user_id: string; callsign: string
          level: number; is_licensed: boolean; founder_code_applied?: boolean; role?: string
        }

        // ── Limpiar keys legacy antes de guardar las nuevas ────────────────
        LEGACY_KEYS.forEach(k => localStorage.removeItem(k))

        // ── Guardar nuevo JWT y perfil ─────────────────────────────────────
        localStorage.setItem('daki_token',    data.access_token)
        localStorage.setItem('daki_user_id',  data.user_id)
        localStorage.setItem('daki_callsign', data.callsign)
        localStorage.setItem('daki_level',    String(data.level))
        localStorage.setItem('daki_licensed', String(data.is_licensed))
        setUser({
          id:            data.user_id,
          username:      data.callsign,
          current_level: data.level,
          total_xp:      0,
          streak_days:   0,
          is_paid:       data.is_licensed,
          role:          data.role,
        })

        // Cookie para middleware de Next.js
        document.cookie = 'enigma_user=1; path=/; max-age=604800; SameSite=Lax'

        const msg = data.founder_code_applied
          ? `LICENCIA DE FUNDADOR ACTIVADA — BIENVENIDO, ${data.callsign}.`
          : `OPERADOR ${data.callsign} REGISTRADO. ABRIENDO EL NEXO...`

        setConsole({ text: msg, state: 'success' })
        setTimeout(() => router.push('/hub'), 1400)
        return
      }

      // ── Errores ────────────────────────────────────────────────────────────
      const err = await res.json().catch(() => ({})) as { detail?: string }
      if (res.status === 409) {
        const detail = typeof err.detail === 'string' ? err.detail : 'CONFLICTO DE IDENTIDAD'
        setConsole({ text: `ERROR 409: ${detail.toUpperCase()}`, state: 'error' })
      } else if (res.status === 422) {
        const detail = Array.isArray(err.detail)
          ? (err.detail[0]?.msg ?? 'DATOS INVÁLIDOS')
          : (err.detail ?? 'DATOS INVÁLIDOS')
        setConsole({ text: `ERROR 422: ${String(detail).toUpperCase()}`, state: 'error' })
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
    ejecutarRegistro()
  }

  // ── Colores de consola ───────────────────────────────────────────────────────
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

  const hasMigrationData = detected && (
    detected.level || detected.hasBetaSession || detected.callsign
  )

  return (
    <div className="min-h-screen bg-[#0A0A0A] font-mono text-[#00FF41] flex flex-col items-center justify-center relative overflow-y-auto">

      <style>{`
        @keyframes cursor-blink  { 0%,100%{opacity:1} 50%{opacity:0} }
        @keyframes error-blink   { 0%,100%{opacity:1} 25%,75%{opacity:0.3} }
        @keyframes amber-pulse   { 0%,100%{opacity:1} 50%{opacity:0.6} }
        .blink       { animation: cursor-blink 1s step-end infinite; }
        .error-blink { animation: error-blink 0.4s ease-in-out 2; }
        .amber-pulse { animation: amber-pulse 2s ease-in-out infinite; }

        .exec-btn {
          border: 1px solid rgba(0,255,65,0.55);
          color: #00FF41;
          background: transparent;
          transition: background 0.15s, color 0.15s, box-shadow 0.15s;
        }
        .exec-btn:hover:not(:disabled) {
          background: #00FF41; color: #0A0A0A;
          box-shadow: 0 0 24px rgba(0,255,65,0.4);
        }
        .exec-btn:disabled {
          border-color: rgba(0,255,65,0.15);
          color: rgba(0,255,65,0.25); cursor: not-allowed;
        }
        .input-line {
          border-bottom: 1px solid rgba(0,255,65,0.2);
          transition: border-color 0.2s, box-shadow 0.2s;
        }
        .input-line.focused {
          border-color: #00FF41;
          box-shadow: 0 2px 12px rgba(0,255,65,0.2);
        }
        .input-line.amber {
          border-bottom-color: rgba(255,184,0,0.3);
        }
        .input-line.amber.focused {
          border-bottom-color: #FFB800;
          box-shadow: 0 2px 12px rgba(255,184,0,0.2);
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

      {/* ── Terminal box ─────────────────────────────────────────────────────── */}
      <div className="relative z-20 w-full max-w-lg px-6 py-10 pb-16">

        {/* Header */}
        <div className="border-b border-[#00FF41]/15 pb-4 mb-8">
          <p className="text-[#00FF41]/25 text-xs tracking-[0.5em] uppercase mb-1">
            {'// NUEVO OPERADOR — PROTOCOLO DE RECLUTAMIENTO'}
          </p>
          <h1 className="text-[#00FF41] text-sm md:text-base font-bold tracking-[0.3em] uppercase neon-glow">
            DAKIedtech {'//'}  CREAR CUENTA DE OPERADOR
          </h1>
        </div>

        {/* Boot log */}
        {bootLines.length > 0 && (
          <div className="space-y-1 mb-6">
            {bootLines.map((line, i) => (
              <div key={i} className={`text-xs leading-5 ${
                line.includes('[OK]')          ? 'text-[#00FF41]/50'
                : line.includes('LISTO')       ? 'text-[#00FF41]/80'
                : line.includes('ESCANEANDO')  ? 'text-[#FFB800]/60'
                : 'text-[#00FF41]/30'
              }`}>
                {line}
              </div>
            ))}
          </div>
        )}

        {/* ── Panel de sesión detectada ──────────────────────────────────────── */}
        {bootDone && hasMigrationData && (
          <div className="border border-[#FFB800]/30 bg-[#FFB800]/5 px-4 py-3 mb-6">
            <div className="flex items-center gap-2 mb-2">
              <span className="amber-pulse text-[#FFB800] text-xs">{'[!]'}</span>
              <span className="text-[8px] tracking-[0.5em] text-[#FFB800]/70 uppercase">
                SESIÓN ANTERIOR DETECTADA — MIGRACIÓN AUTOMÁTICA
              </span>
            </div>
            <div className="space-y-1">
              {detected?.level && (
                <div className="flex gap-3 text-[10px]">
                  <span className="text-[#FFB800]/40 w-24 shrink-0">NIVEL</span>
                  <span className="text-[#FFB800]/80">{detected.level}</span>
                </div>
              )}
              {detected?.callsign && (
                <div className="flex gap-3 text-[10px]">
                  <span className="text-[#FFB800]/40 w-24 shrink-0">CALLSIGN</span>
                  <span className="text-[#FFB800]/80">{detected.callsign} → pre-cargado</span>
                </div>
              )}
              {detected?.hasBetaSession && (
                <div className="flex gap-3 text-[10px]">
                  <span className="text-[#FFB800]/40 w-24 shrink-0">SESIÓN BETA</span>
                  <span className="text-[#FFB800]/80">ACTIVA → será migrada</span>
                </div>
              )}
              {detected?.missionState && Object.keys(detected.missionState).length > 0 && (
                <div className="flex gap-3 text-[10px]">
                  <span className="text-[#FFB800]/40 w-24 shrink-0">MISIONES</span>
                  <span className="text-[#FFB800]/80">
                    {Object.keys(detected.missionState).length} sector(es) guardados
                  </span>
                </div>
              )}
            </div>
            <p className="text-[9px] text-[#FFB800]/35 tracking-wide mt-2">
              → Tu progreso será transferido automáticamente al crear la cuenta.
            </p>
          </div>
        )}

        {/* ── Formulario ──────────────────────────────────────────────────────── */}
        {bootDone && (
          <div className="mb-6">
            <p className="text-xs text-[#00FF41]/50 tracking-[0.3em] uppercase mb-5">
              {'> INGRESE DATOS DE IDENTIDAD'}
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
                  onKeyDown={e => { if (e.key === 'Enter') { e.preventDefault(); callsignRef.current?.focus() } }}
                  placeholder="operador@nexo.io"
                  disabled={isLoading}
                  className="flex-1 bg-transparent text-[#00FF41] text-sm outline-none border-none caret-[#00FF41] tracking-wide placeholder:text-[#00FF41]/15 placeholder:normal-case disabled:opacity-40"
                  autoComplete="email"
                  spellCheck={false}
                />
              </div>

              {/* Callsign */}
              <div className={`input-line pb-2 mb-5 flex items-center gap-2 ${focusedField === 'callsign' ? 'focused' : ''}`}>
                <span className="text-[#00FF41]/35 select-none text-[10px] tracking-[0.3em] w-24 shrink-0">CALLSIGN</span>
                <input
                  ref={callsignRef}
                  type="text"
                  value={callsign}
                  onChange={e => setCallsign(e.target.value.replace(/\s/g, ''))}
                  onFocus={() => setFocusedField('callsign')}
                  onBlur={() => setFocusedField(null)}
                  onKeyDown={e => { if (e.key === 'Enter') { e.preventDefault(); passwordRef.current?.focus() } }}
                  placeholder="Ej: Ghost-Zero (3-20 chars)"
                  disabled={isLoading}
                  maxLength={20}
                  className="flex-1 bg-transparent text-[#00FF41] text-sm outline-none border-none caret-[#00FF41] tracking-widest uppercase placeholder:text-[#00FF41]/15 placeholder:normal-case placeholder:tracking-wide disabled:opacity-40"
                  autoComplete="off"
                  spellCheck={false}
                />
                {detected?.callsign && callsign === detected.callsign && (
                  <span className="text-[#FFB800]/50 text-[9px] shrink-0 tracking-widest">← PREVIO</span>
                )}
              </div>

              {/* Password */}
              <div className={`input-line pb-2 mb-5 flex items-center gap-2 ${focusedField === 'password' ? 'focused' : ''}`}>
                <span className="text-[#00FF41]/35 select-none text-[10px] tracking-[0.3em] w-24 shrink-0">CLAVE</span>
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
                  autoComplete="new-password"
                />
              </div>

              {/* ── Founder Code toggle ──────────────────────────────────────── */}
              <div className="mb-6">
                <button
                  type="button"
                  onClick={() => setShowFounder(v => !v)}
                  className="text-[9px] tracking-[0.35em] text-[#FFB800]/30 hover:text-[#FFB800]/60 transition-colors uppercase"
                >
                  {showFounder ? '[-]' : '[+]'} ¿Tienes Licencia de Fundador? (código distinto al VANG)
                </button>

                {showFounder && (
                  <div className={`input-line amber pb-2 mt-3 flex items-center gap-2 ${focusedField === 'founder' ? 'focused amber' : ''}`}>
                    <span className="text-[#FFB800]/40 select-none text-[10px] tracking-[0.25em] w-24 shrink-0">CÓDIGO</span>
                    <input
                      type="text"
                      value={founderCode}
                      onChange={e => setFounderCode(e.target.value.toUpperCase().replace(/\s/g, ''))}
                      onFocus={() => setFocusedField('founder')}
                      onBlur={() => setFocusedField(null)}
                      placeholder="GLITCH-GOLD-INIT"
                      disabled={isLoading}
                      className="flex-1 bg-transparent text-[#FFB800] text-xs outline-none border-none caret-[#FFB800] tracking-widest uppercase placeholder:text-[#FFB800]/20 placeholder:tracking-wide disabled:opacity-40"
                      autoComplete="off"
                      spellCheck={false}
                    />
                  </div>
                )}
              </div>


              <button
                type="submit"
                disabled={isLoading || !email.trim() || !callsign.trim() || !password.trim()}
                className="exec-btn w-full py-3 text-xs tracking-[0.4em] uppercase"
              >
                {isLoading ? '[ PROCESANDO... ]' : '[[ EJECUTAR PROTOCOLO DE REGISTRO ]]'}
              </button>
            </form>
          </div>
        )}

        {/* ── Consola de estado ───────────────────────────────────────────────── */}
        <div className="border-t border-[#00FF41]/10 pt-4 mt-2 mb-8 min-h-[50px]">
          <p className={`text-xs tracking-wide ${consoleColor} ${consoleGlow} ${console_.state === 'error' ? 'error-blink' : ''}`}>
            {'> Status: '}{console_.text}
            <span className="blink ml-0.5">_</span>
          </p>
        </div>

        {/* ── Links de navegación ─────────────────────────────────────────────── */}
        <div className="flex flex-col items-center gap-3 text-center">
          <Link
            href="/login"
            className="text-[#00FF41]/20 text-[10px] tracking-[0.3em] hover:text-[#00FF41]/50 transition-colors uppercase"
          >
            {'[ ¿Ya tienes acceso? → Ingresar al sistema ]'}
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
