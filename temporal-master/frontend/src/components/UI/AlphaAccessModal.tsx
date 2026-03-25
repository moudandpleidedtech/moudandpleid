'use client'

/**
 * AlphaAccessModal — Puerta de Acceso Vanguardia
 *
 * Permite al Operador canjear su Pase Alpha (código VANG-XXXX-XXXX)
 * para activar 30 días de acceso TRIAL al Nexo.
 *
 * Endpoint: POST /api/v1/alpha/redeem
 * Auth:     Bearer JWT (extraído de localStorage — el user_id viene del token, no del body)
 *
 * Estados:
 *   idle     → formulario activo
 *   loading  → [ VERIFICANDO CREDENCIALES... ]
 *   success  → ✓ mensaje de éxito → llama onGranted() tras 1.6s
 *   error    → mensaje de error específico según código HTTP
 */

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000'

interface Props {
  visible:   boolean
  onClose:   () => void
  onGranted: (trialEndDate: string) => void  // activa subscriptionStatus='TRIAL' en store
}

type RedeemState = 'idle' | 'loading' | 'success' | 'error'

// Mapeo de códigos HTTP a mensajes tácticos
const ERROR_MESSAGES: Record<number, string> = {
  401: 'Token de Operador inválido. Inicia sesión de nuevo.',
  404: 'Código no encontrado en la Bóveda Alpha. Verifica el formato.',
  409: 'Código ya utilizado. Este pase fue consumido por otro Operador.',
  429: 'Demasiados intentos. Espera 60 segundos e intenta de nuevo.',
}

export default function AlphaAccessModal({ visible, onClose, onGranted }: Props) {
  const [codeInput,    setCodeInput]    = useState('')
  const [redeemState,  setRedeemState]  = useState<RedeemState>('idle')
  const [feedbackMsg,  setFeedbackMsg]  = useState('')
  const [trialEndDate, setTrialEndDate] = useState('')

  const handleRedeem = async () => {
    const code = codeInput.trim().toUpperCase()
    if (!code || redeemState === 'loading' || redeemState === 'success') return

    setRedeemState('loading')
    setFeedbackMsg('')

    const token = typeof window !== 'undefined'
      ? localStorage.getItem('daki_token')
      : null

    if (!token) {
      setRedeemState('error')
      setFeedbackMsg(ERROR_MESSAGES[401])
      return
    }

    try {
      const res = await fetch(`${API_BASE}/api/v1/alpha/redeem`, {
        method:  'POST',
        headers: {
          'Content-Type':  'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ code }),
      })

      const data = await res.json()

      if (!res.ok) {
        setRedeemState('error')
        setFeedbackMsg(
          ERROR_MESSAGES[res.status] ?? data.detail ?? 'Error desconocido. Intenta de nuevo.'
        )
        return
      }

      // Éxito
      setTrialEndDate(data.trial_end_date ?? '')
      setRedeemState('success')
      setFeedbackMsg(data.message ?? 'Acceso Nivel Vanguardia Concedido. Bienvenido al Nexo.')

      setTimeout(() => {
        onGranted(data.trial_end_date ?? '')
        onClose()
      }, 1800)

    } catch {
      setRedeemState('error')
      setFeedbackMsg('Sin señal con el Nexo. Verifica tu conexión.')
    }
  }

  const handleInput = (val: string) => {
    setCodeInput(val.toUpperCase())
    if (redeemState === 'error') {
      setRedeemState('idle')
      setFeedbackMsg('')
    }
  }

  return (
    <AnimatePresence>
      {visible && (
        /* Backdrop */
        <motion.div
          className="fixed inset-0 z-[9100] flex items-center justify-center p-4"
          style={{ background: 'rgba(0,0,0,0.92)', backdropFilter: 'blur(8px)' }}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.2 }}
          onClick={(e) => { if (e.target === e.currentTarget && redeemState !== 'loading') onClose() }}
        >
          {/* Card */}
          <motion.div
            className="relative w-full max-w-sm font-mono overflow-hidden"
            style={{
              background:  '#040A06',
              border:      '1px solid rgba(0,255,65,0.30)',
              boxShadow:   '0 0 80px rgba(0,255,65,0.10), inset 0 0 40px rgba(0,255,65,0.03)',
            }}
            initial={{ scale: 0.88, y: 20, opacity: 0 }}
            animate={{ scale: 1,    y: 0,  opacity: 1 }}
            exit={{    scale: 0.92, y: 10, opacity: 0 }}
            transition={{ type: 'spring', stiffness: 340, damping: 30 }}
          >
            {/* Scanlines */}
            <div
              className="absolute inset-0 pointer-events-none z-0"
              style={{
                background: 'repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,0.04) 2px,rgba(0,0,0,0.04) 4px)',
              }}
            />

            {/* Top bar */}
            <div
              className="relative z-10 flex items-center gap-2 px-5 py-2.5"
              style={{
                background:   'rgba(0,255,65,0.06)',
                borderBottom: '1px solid rgba(0,255,65,0.15)',
              }}
            >
              <motion.span
                className="w-1.5 h-1.5 rounded-full bg-[#00FF41] shrink-0"
                animate={{ opacity: [0.4, 1, 0.4] }}
                transition={{ duration: 1.6, repeat: Infinity }}
                style={{ boxShadow: '0 0 6px rgba(0,255,65,0.8)' }}
              />
              <span
                className="text-[9px] tracking-[0.45em] font-bold"
                style={{ color: 'rgba(0,255,65,0.70)' }}
              >
                BÓVEDA ALPHA // OPERACIÓN VANGUARDIA
              </span>
              <button
                onClick={() => { if (redeemState !== 'loading') onClose() }}
                className="ml-auto text-[#00FF41]/25 hover:text-[#00FF41]/60 transition-colors text-sm leading-none"
                aria-label="Cerrar"
              >
                ✕
              </button>
            </div>

            {/* Body */}
            <div className="relative z-10 px-6 pt-7 pb-6">

              {/* Icono central */}
              <motion.div
                className="flex justify-center mb-6"
                animate={redeemState === 'success'
                  ? { scale: [1, 1.15, 1] }
                  : { y: [0, -4, 0] }
                }
                transition={{ duration: redeemState === 'success' ? 0.4 : 3, repeat: redeemState === 'success' ? 0 : Infinity, ease: 'easeInOut' }}
              >
                <div
                  className="w-16 h-16 flex items-center justify-center text-3xl"
                  style={{
                    border:     `1px solid ${redeemState === 'success' ? 'rgba(0,255,65,0.6)' : 'rgba(0,255,65,0.25)'}`,
                    background: `${redeemState === 'success' ? 'rgba(0,255,65,0.12)' : 'rgba(0,255,65,0.04)'}`,
                    boxShadow:  `0 0 ${redeemState === 'success' ? '30px' : '15px'} rgba(0,255,65,${redeemState === 'success' ? '0.25' : '0.08'})`,
                    transition: 'all 0.4s ease',
                  }}
                >
                  {redeemState === 'success' ? '◈' : '🔑'}
                </div>
              </motion.div>

              {/* Title */}
              <h2
                className="text-center text-sm font-black tracking-[0.15em] mb-1"
                style={{ color: '#00FF41', textShadow: '0 0 12px rgba(0,255,65,0.45)' }}
              >
                ACTIVAR PASE ALPHA
              </h2>
              <p
                className="text-center text-[10px] tracking-[0.3em] mb-6"
                style={{ color: 'rgba(0,255,65,0.45)' }}
              >
                30 DÍAS DE ACCESO AL NEXO
              </p>

              {/* Divider */}
              <div
                className="h-px mb-5"
                style={{ background: 'linear-gradient(90deg,transparent,rgba(0,255,65,0.25),transparent)' }}
              />

              {/* Instrucciones */}
              <p
                className="text-[10px] leading-relaxed mb-4 text-center"
                style={{ color: 'rgba(0,255,65,0.55)' }}
              >
                Ingresa tu Pase Alpha en formato{' '}
                <span style={{ color: '#00FF41', fontWeight: 'bold' }}>VANG-XXXX-XXXX</span>
                {' '}para activar tu acceso TRIAL.
              </p>

              {/* Input */}
              <input
                type="text"
                value={codeInput}
                onChange={(e) => handleInput(e.target.value)}
                onKeyDown={(e) => { if (e.key === 'Enter') handleRedeem() }}
                placeholder="VANG-XXXX-XXXX"
                disabled={redeemState === 'loading' || redeemState === 'success'}
                maxLength={24}
                className="w-full bg-transparent text-sm font-mono font-bold tracking-[0.25em] outline-none py-3 px-4 mb-3 text-center"
                style={{
                  border:     `1px solid ${redeemState === 'error' ? 'rgba(255,80,30,0.6)' : 'rgba(0,255,65,0.40)'}`,
                  color:      redeemState === 'error' ? 'rgba(255,120,60,0.9)' : '#00FF41',
                  caretColor: '#00FF41',
                  background: 'rgba(0,0,0,0.4)',
                  letterSpacing: '0.2em',
                  transition: 'border-color 0.2s',
                }}
                spellCheck={false}
                autoComplete="off"
                autoFocus
              />

              {/* CTA Button */}
              <motion.button
                onClick={handleRedeem}
                disabled={!codeInput.trim() || redeemState === 'loading' || redeemState === 'success'}
                className="w-full py-3 text-[11px] font-black tracking-[0.4em] uppercase transition-all duration-150"
                style={{
                  background: codeInput.trim() && redeemState !== 'loading' && redeemState !== 'success'
                    ? 'rgba(0,255,65,0.14)'
                    : 'rgba(0,255,65,0.03)',
                  border: codeInput.trim() && redeemState !== 'loading' && redeemState !== 'success'
                    ? '1px solid rgba(0,255,65,0.60)'
                    : '1px solid rgba(0,255,65,0.18)',
                  color: codeInput.trim() && redeemState !== 'loading' && redeemState !== 'success'
                    ? '#00FF41'
                    : 'rgba(0,255,65,0.30)',
                  cursor: !codeInput.trim() || redeemState === 'loading' || redeemState === 'success'
                    ? 'not-allowed'
                    : 'pointer',
                  textShadow: codeInput.trim() ? '0 0 10px rgba(0,255,65,0.4)' : 'none',
                  boxShadow: codeInput.trim() && redeemState !== 'loading' && redeemState !== 'success'
                    ? '0 0 20px rgba(0,255,65,0.08)'
                    : 'none',
                }}
                whileTap={codeInput.trim() ? { scale: 0.97 } : {}}
              >
                {redeemState === 'loading'
                  ? '[ VERIFICANDO CREDENCIALES... ]'
                  : redeemState === 'success'
                  ? '[ ACCESO CONCEDIDO ]'
                  : '[ ACTIVAR PASE ALPHA ]'
                }
              </motion.button>

              {/* Feedback */}
              <AnimatePresence mode="wait">
                {(redeemState === 'success' || redeemState === 'error') && feedbackMsg && (
                  <motion.div
                    key={redeemState}
                    initial={{ opacity: 0, y: 6 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0 }}
                    transition={{ duration: 0.25 }}
                    className="mt-4 text-center"
                  >
                    {redeemState === 'success' ? (
                      <>
                        <p
                          className="text-[11px] font-bold tracking-[0.2em]"
                          style={{ color: '#00FF41', textShadow: '0 0 12px rgba(0,255,65,0.6)' }}
                        >
                          ✓ {feedbackMsg}
                        </p>
                        {trialEndDate && (
                          <p className="mt-1 text-[9px] tracking-[0.25em]" style={{ color: 'rgba(0,255,65,0.4)' }}>
                            TRIAL ACTIVO HASTA: {new Date(trialEndDate).toLocaleDateString('es-ES', { day: '2-digit', month: 'short', year: 'numeric' }).toUpperCase()}
                          </p>
                        )}
                      </>
                    ) : (
                      <p
                        className="text-[10px] tracking-[0.15em]"
                        style={{ color: 'rgba(255,100,50,0.90)' }}
                      >
                        ✗ {feedbackMsg}
                      </p>
                    )}
                  </motion.div>
                )}
              </AnimatePresence>

              {/* Dismiss */}
              {redeemState !== 'loading' && redeemState !== 'success' && (
                <button
                  onClick={onClose}
                  className="block w-full text-center mt-4 text-[9px] tracking-[0.4em] transition-colors"
                  style={{ color: 'rgba(0,255,65,0.20)' }}
                  onMouseEnter={(e) => (e.currentTarget.style.color = 'rgba(0,255,65,0.45)')}
                  onMouseLeave={(e) => (e.currentTarget.style.color = 'rgba(0,255,65,0.20)')}
                >
                  CANCELAR OPERACIÓN
                </button>
              )}

            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}
