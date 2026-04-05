'use client'

/**
 * AlphaCodeModal — Compuerta de Acceso Alpha
 *
 * Se muestra cuando el backend devuelve 402 en niveles L10+.
 * El operador ingresa su código VANG-XXXX-XXXX (ya distribuido).
 * Llama a POST /api/v1/alpha/redeem (endpoint existente, sin cambios).
 * En éxito activa subscription_status='TRIAL' en el store y desbloquea el nivel.
 */

import { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? ''

interface Props {
  visible:   boolean
  onClose:   () => void
  onGranted: (trialEndDate: string) => void   // activa TRIAL en store
}

type RedeemState = 'idle' | 'loading' | 'success' | 'error'

// Formatea el input con guiones automáticamente: VANG-XXXX-XXXX
function formatVang(raw: string): string {
  const clean = raw.toUpperCase().replace(/[^A-Z0-9]/g, '')
  const parts: string[] = []
  if (clean.length > 0)  parts.push(clean.slice(0, 4))
  if (clean.length > 4)  parts.push(clean.slice(4, 8))
  if (clean.length > 8)  parts.push(clean.slice(8, 12))
  return parts.join('-')
}

export default function AlphaCodeModal({ visible, onClose, onGranted }: Props) {
  const [input,   setInput]   = useState('')
  const [state,   setState]   = useState<RedeemState>('idle')
  const [message, setMessage] = useState('')
  const inputRef = useRef<HTMLInputElement>(null)

  // Foco automático al abrir
  useEffect(() => {
    if (visible) {
      setTimeout(() => inputRef.current?.focus(), 120)
    } else {
      setInput('')
      setState('idle')
      setMessage('')
    }
  }, [visible])

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const formatted = formatVang(e.target.value)
    // Máximo 14 chars: VANG-XXXX-XXXX
    if (formatted.replace(/-/g, '').length <= 12) {
      setInput(formatted)
      if (state !== 'idle') setState('idle')
    }
  }

  const handleRedeem = async () => {
    const code = input.trim()
    if (!code || state === 'loading' || state === 'success') return
    if (code.length < 14) {
      setState('error')
      setMessage('Formato incompleto. Debe ser VANG-XXXX-XXXX.')
      return
    }

    setState('loading')
    setMessage('')

    try {
      const res = await fetch(`${API_BASE}/api/v1/alpha/redeem`, {
        method:      'POST',
        credentials: 'include',          // envía la cookie daki_auth
        headers:     { 'Content-Type': 'application/json' },
        body:        JSON.stringify({ code }),
      })
      const data = await res.json()

      if (!res.ok) {
        setState('error')
        setMessage(data.detail ?? 'Código inválido o ya utilizado.')
        return
      }

      setState('success')
      setMessage(data.message ?? 'Acceso concedido.')
      setTimeout(() => {
        onGranted(data.trial_end_date)
        onClose()
      }, 1400)

    } catch {
      setState('error')
      setMessage('Sin conexión con el Nexo. Verifica tu red.')
    }
  }

  const isValid    = input.length === 14   // VANG(4) + -(1) + XXXX(4) + -(1) + XXXX(4)
  const borderColor =
    state === 'error'   ? 'rgba(255,80,30,0.70)' :
    state === 'success' ? 'rgba(0,255,65,0.80)'  :
    isValid             ? 'rgba(0,255,65,0.55)'  :
                          'rgba(0,255,65,0.25)'

  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          className="fixed inset-0 z-[9100] flex items-center justify-center p-4"
          style={{ background: 'rgba(0,0,0,0.90)', backdropFilter: 'blur(8px)' }}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.20 }}
          onClick={(e) => { if (e.target === e.currentTarget) onClose() }}
        >
          <motion.div
            className="relative w-full max-w-sm font-mono overflow-hidden"
            style={{
              background:  '#06060F',
              border:      '1px solid rgba(6,182,212,0.35)',
              boxShadow:   '0 0 60px rgba(6,182,212,0.10), inset 0 0 40px rgba(6,182,212,0.03)',
            }}
            initial={{ scale: 0.86, y: 28, opacity: 0 }}
            animate={{ scale: 1,    y: 0,  opacity: 1 }}
            exit={{    scale: 0.92, y: 12, opacity: 0 }}
            transition={{ type: 'spring', stiffness: 300, damping: 26 }}
          >
            {/* Scanlines */}
            <div
              className="absolute inset-0 pointer-events-none z-0 opacity-[0.018]"
              style={{ backgroundImage: 'repeating-linear-gradient(0deg,transparent,transparent 3px,#06b6d4 3px,#06b6d4 4px)' }}
            />

            {/* Barra superior — pulso cyan */}
            <div
              className="relative z-10 flex items-center gap-2.5 px-5 py-2.5"
              style={{ background: 'rgba(6,182,212,0.06)', borderBottom: '1px solid rgba(6,182,212,0.18)' }}
            >
              <motion.span
                className="w-1.5 h-1.5 rounded-full shrink-0"
                style={{ background: '#06b6d4', boxShadow: '0 0 6px rgba(6,182,212,0.9)' }}
                animate={{ opacity: [0.4, 1, 0.4] }}
                transition={{ duration: 1.6, repeat: Infinity }}
              />
              <span className="text-[9px] tracking-[0.5em] font-bold" style={{ color: 'rgba(6,182,212,0.80)' }}>
                PROTOCOLO ALPHA — VERIFICACIÓN
              </span>
              <button
                onClick={onClose}
                className="ml-auto text-[10px] leading-none transition-colors"
                style={{ color: 'rgba(6,182,212,0.30)' }}
                onMouseEnter={(e) => (e.currentTarget.style.color = 'rgba(6,182,212,0.70)')}
                onMouseLeave={(e) => (e.currentTarget.style.color = 'rgba(6,182,212,0.30)')}
              >
                ✕
              </button>
            </div>

            {/* Body */}
            <div className="relative z-10 px-6 pt-7 pb-6">

              {/* Ícono */}
              <motion.div
                className="flex justify-center mb-5"
                animate={{ y: [0, -4, 0] }}
                transition={{ duration: 3, repeat: Infinity, ease: 'easeInOut' }}
              >
                <div
                  className="w-14 h-14 flex items-center justify-center text-2xl"
                  style={{
                    border:     '1px solid rgba(6,182,212,0.35)',
                    background: 'rgba(6,182,212,0.05)',
                    boxShadow:  '0 0 24px rgba(6,182,212,0.10)',
                  }}
                >
                  ◈
                </div>
              </motion.div>

              {/* Título */}
              <h2
                className="text-center text-sm font-black tracking-[0.14em] leading-snug mb-1"
                style={{ color: 'rgba(6,182,212,0.95)', textShadow: '0 0 18px rgba(6,182,212,0.50)' }}
              >
                CÓDIGO ALPHA REQUERIDO
              </h2>
              <p className="text-center text-[10px] tracking-[0.28em] mb-6" style={{ color: 'rgba(6,182,212,0.45)' }}>
                NIVEL 10 · ACCESO RESTRINGIDO
              </p>

              {/* Divisor */}
              <div className="h-px mb-6" style={{ background: 'linear-gradient(90deg,transparent,rgba(6,182,212,0.28),transparent)' }} />

              {/* Mensaje explicativo */}
              <p className="text-[10px] leading-relaxed mb-5" style={{ color: 'rgba(6,182,212,0.60)' }}>
                Para continuar más allá del Sector 00 necesitás tu{' '}
                <span style={{ color: 'rgba(6,182,212,0.90)', fontWeight: 700 }}>Código Alpha</span>
                {' '}de Operación Vanguardia.
                Si recibiste uno, ingrésalo a continuación.
              </p>

              {/* Input VANG */}
              <div className="mb-3">
                <div className="text-[8px] tracking-[0.5em] mb-1.5" style={{ color: 'rgba(6,182,212,0.40)' }}>
                  FORMATO: VANG-XXXX-XXXX
                </div>
                <input
                  ref={inputRef}
                  type="text"
                  value={input}
                  onChange={handleChange}
                  onKeyDown={(e) => { if (e.key === 'Enter') handleRedeem() }}
                  placeholder="VANG-____-____"
                  disabled={state === 'loading' || state === 'success'}
                  spellCheck={false}
                  autoComplete="off"
                  maxLength={14}
                  className="w-full bg-transparent text-sm font-mono tracking-[0.30em] outline-none py-3 px-3 text-center uppercase"
                  style={{
                    border:      `1px solid ${borderColor}`,
                    color:       state === 'success' ? '#00FF41' : '#06b6d4',
                    caretColor:  '#06b6d4',
                    background:  'rgba(0,0,0,0.35)',
                    transition:  'border-color 0.2s',
                    letterSpacing: '0.35em',
                  }}
                />
              </div>

              {/* Botón */}
              <button
                onClick={handleRedeem}
                disabled={!isValid || state === 'loading' || state === 'success'}
                className="w-full py-3 text-[10px] font-black tracking-[0.38em] uppercase transition-all duration-150 mb-3"
                style={{
                  background: isValid && state !== 'loading' && state !== 'success'
                    ? 'rgba(6,182,212,0.12)' : 'rgba(6,182,212,0.03)',
                  border: isValid && state !== 'loading' && state !== 'success'
                    ? '1px solid rgba(6,182,212,0.55)' : '1px solid rgba(6,182,212,0.18)',
                  color: isValid && state !== 'loading' && state !== 'success'
                    ? '#06b6d4' : 'rgba(6,182,212,0.30)',
                  cursor: (!isValid || state === 'loading' || state === 'success') ? 'not-allowed' : 'pointer',
                  textShadow: isValid ? '0 0 8px rgba(6,182,212,0.45)' : 'none',
                }}
              >
                {state === 'loading' ? '[ VERIFICANDO CÓDIGO... ]' :
                 state === 'success' ? '[ ACCESO CONCEDIDO ✓ ]'   :
                                       '[ ACTIVAR CÓDIGO ALPHA ]'}
              </button>

              {/* Feedback */}
              <AnimatePresence mode="wait">
                {(state === 'success' || state === 'error') && (
                  <motion.p
                    key={state}
                    initial={{ opacity: 0, y: 4 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0 }}
                    className="text-[10px] tracking-[0.18em] text-center"
                    style={{
                      color: state === 'success' ? '#00FF41' : 'rgba(255,100,50,0.90)',
                      textShadow: state === 'success' ? '0 0 10px rgba(0,255,65,0.5)' : 'none',
                    }}
                  >
                    {state === 'success' ? `✓ ${message}` : `✗ ${message}`}
                  </motion.p>
                )}
              </AnimatePresence>

              {/* Divisor */}
              <div className="h-px mt-5 mb-4" style={{ background: 'linear-gradient(90deg,transparent,rgba(6,182,212,0.15),transparent)' }} />

              {/* Pie */}
              <p className="text-center text-[8px] tracking-[0.3em]" style={{ color: 'rgba(6,182,212,0.28)' }}>
                ¿No tenés código? Los códigos se distribuyen en acceso anticipado.
              </p>
              <button
                onClick={onClose}
                className="block w-full text-center mt-3 text-[9px] tracking-[0.4em] transition-colors"
                style={{ color: 'rgba(6,182,212,0.22)' }}
                onMouseEnter={(e) => (e.currentTarget.style.color = 'rgba(6,182,212,0.55)')}
                onMouseLeave={(e) => (e.currentTarget.style.color = 'rgba(6,182,212,0.22)')}
              >
                VOLVER A LA TERMINAL
              </button>

            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}
