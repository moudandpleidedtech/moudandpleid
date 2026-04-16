'use client'

/**
 * PaywallModal — "El Muro"
 *
 * Aparece cuando el backend devuelve 402 Payment Required.
 * Estética dark cyberpunk con acento rojo-naranja (BLOCKED state).
 *
 * Props:
 *   visible     — controla AnimatePresence
 *   onClose     — callback para cerrar sin pagar
 *   onGranted   — callback cuando el override táctico tiene éxito (activa isPaid en store)
 *   paymentUrl  — URL del flujo de pago (default: https://pay.dakiedtech.com)
 *   userId      — UUID del operador (requerido para el override táctico)
 */

import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? ''

interface Props {
  visible: boolean
  onClose: () => void
  onGranted: () => void   // activa isPaid en el store y cierra el modal
  userId?: string
}

const FEATURES = [
  'Acceso completo a los 195 desafíos del Nexo (todos los sectores)',
  'Sistema de Duelos PvP — Arena contra operadores globales',
  'Certificados descargables por sector completado',
  'DAKI IA ilimitada — hints, debrief y mentoría sin restricciones',
  '1 sesión de coaching individual con el Arquitecto del Sistema',
]

type OverrideState = 'idle' | 'loading' | 'success' | 'error'
type CheckoutState = 'idle' | 'loading' | 'error'


export default function PaywallModal({
  visible,
  onClose,
  onGranted,
  userId,
}: Props) {
  const [codeInput,      setCodeInput]      = useState('')
  const [overrideState,  setOverrideState]  = useState<OverrideState>('idle')
  const [overrideMsg,    setOverrideMsg]    = useState('')
  const [checkoutState,  setCheckoutState]  = useState<CheckoutState>('idle')
  const [checkoutError,  setCheckoutError]  = useState('')
  const [personalMsg,    setPersonalMsg]    = useState<string | null>(null)

  // Feature 2: Personalización — leer patrones de errores del operador en localStorage
  useEffect(() => {
    if (!visible) return
    try {
      const errorMap: Record<string, string> = {
        SyntaxError:      'Tuviste dificultad con SyntaxError. En el Sector 02 la estructura de Python se vuelve tan natural que ese error desaparece.',
        TypeError:        'TypeError apareció en tus incursiones. En el Sector 02 dominarás la conversión de tipos — ese error deja de existir.',
        NameError:        'El NameError te visitó más de una vez. En el Sector 02 entenderás el scope de variables de forma definitiva.',
        IndentationError: 'La indentación te costó en el Sector 01. Los bucles del Sector 02 la convierten en segunda naturaleza.',
        ValueError:       'Tuviste ValueError con conversiones. En el Sector 02 aprenderás a validar datos antes de operar con ellos.',
      }
      const topError = Object.keys(errorMap)
        .map((t) => ({ type: t, count: parseInt(localStorage.getItem(`daki_pattern_${t}`) ?? '0', 10) }))
        .filter((e) => e.count > 0)
        .sort((a, b) => b.count - a.count)[0]
      if (topError) setPersonalMsg(errorMap[topError.type])
    } catch { /* localStorage bloqueado */ }
  }, [visible])

  const handleCheckout = async () => {
    if (checkoutState === 'loading') return
    setCheckoutState('loading')
    setCheckoutError('')
    try {
      // Leer cookie de afiliado si existe (seteada por AffiliateTracker vía ?ref=)
      const refMatch = document.cookie.match(/(?:^|; )daki_ref=([^;]*)/)
      const ref = refMatch ? decodeURIComponent(refMatch[1]) : undefined

      const res = await fetch(`${API_BASE}/api/v1/hotmart/checkout`, {
        method:      'POST',
        headers:     { 'Content-Type': 'application/json' },
        credentials: 'include',
        body:        JSON.stringify({ plan: 'lifetime', ...(ref ? { ref } : {}) }),
      })
      const data = await res.json()
      if (!res.ok) {
        setCheckoutState('error')
        setCheckoutError(data.detail ?? 'Error al generar el enlace de pago.')
        return
      }
      setCheckoutState('idle')
      window.location.href = data.checkout_url   // misma pestaña, flujo limpio
    } catch {
      setCheckoutState('error')
      setCheckoutError('Sin conexión con el Nexo. Intentá de nuevo.')
    }
  }

  const handleRedeem = async () => {
    if (!codeInput.trim() || !userId || overrideState === 'loading') return
    setOverrideState('loading')
    setOverrideMsg('')

    try {
      const res = await fetch(`${API_BASE}/api/v1/checkout/redeem`, {
        method:      'POST',
        headers:     { 'Content-Type': 'application/json' },
        credentials: 'include',
        body:        JSON.stringify({ code_string: codeInput.trim() }),
      })
      const data = await res.json()

      if (!res.ok) {
        setOverrideState('error')
        setOverrideMsg(data.detail ?? 'Código inválido o agotado.')
        return
      }

      setOverrideState('success')
      setOverrideMsg(data.message)
      // Esperar 1.2s para que el Operador lea el mensaje, luego activar acceso
      setTimeout(() => {
        onGranted()
        onClose()
      }, 1200)
    } catch {
      setOverrideState('error')
      setOverrideMsg('Sin conexión con el Nexo. Verifica tu red e intenta de nuevo.')
    }
  }

  return (
    <AnimatePresence>
      {visible && (
        /* Backdrop */
        <motion.div
          className="fixed inset-0 z-[9000] flex items-center justify-center p-4"
          style={{ background: 'rgba(0,0,0,0.88)', backdropFilter: 'blur(6px)' }}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.22 }}
          onClick={(e) => { if (e.target === e.currentTarget) onClose() }}
        >
          {/* Card */}
          <motion.div
            className="relative w-full max-w-md font-mono overflow-hidden"
            style={{
              background:   '#06060A',
              border:       '1px solid rgba(255,80,30,0.35)',
              boxShadow:    '0 0 60px rgba(255,50,10,0.12), inset 0 0 40px rgba(255,30,0,0.04)',
            }}
            initial={{ scale: 0.88, y: 24, opacity: 0 }}
            animate={{ scale: 1,    y: 0,  opacity: 1 }}
            exit={{    scale: 0.92, y: 12, opacity: 0 }}
            transition={{ type: 'spring', stiffness: 320, damping: 28 }}
          >
            {/* Scanline overlay */}
            <div
              className="absolute inset-0 pointer-events-none z-0"
              style={{
                background: 'repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,0.03) 2px,rgba(0,0,0,0.03) 4px)',
              }}
            />

            {/* Top warning stripe */}
            <div
              className="relative z-10 flex items-center gap-2 px-5 py-2.5"
              style={{
                background:   'rgba(255,50,10,0.08)',
                borderBottom: '1px solid rgba(255,80,30,0.20)',
              }}
            >
              <motion.span
                className="text-xs font-black tracking-[0.35em]"
                style={{ color: 'rgba(255,80,30,0.9)', textShadow: '0 0 12px rgba(255,80,10,0.6)' }}
                animate={{ opacity: [0.6, 1, 0.6] }}
                transition={{ duration: 1.8, repeat: Infinity }}
              >
                ⚠ ACCESO DENEGADO
              </motion.span>
              <span className="text-[9px] tracking-[0.3em]" style={{ color: 'rgba(255,80,30,0.4)' }}>
                · CÓDIGO 402
              </span>

              {/* Close button */}
              <button
                onClick={onClose}
                className="ml-auto text-[#00FF41]/30 hover:text-[#00FF41]/70 transition-colors text-sm leading-none"
                aria-label="Cerrar"
              >
                ✕
              </button>
            </div>

            {/* Body */}
            <div className="relative z-10 px-6 pt-6 pb-5">

              {/* Lock icon */}
              <motion.div
                className="flex justify-center mb-5"
                animate={{ y: [0, -3, 0] }}
                transition={{ duration: 2.5, repeat: Infinity, ease: 'easeInOut' }}
              >
                <div
                  className="w-14 h-14 flex items-center justify-center text-2xl"
                  style={{
                    border:     '1px solid rgba(255,80,30,0.3)',
                    background: 'rgba(255,50,10,0.06)',
                    boxShadow:  '0 0 20px rgba(255,50,10,0.10)',
                  }}
                >
                  🔒
                </div>
              </motion.div>

              {/* Title */}
              <h2
                className="text-center text-sm font-black tracking-[0.12em] leading-snug mb-1"
                style={{ color: 'rgba(255,80,30,0.95)', textShadow: '0 0 16px rgba(255,60,10,0.45)' }}
              >
                INCURSIÓN BLOQUEADA
              </h2>
              <p
                className="text-center text-[10px] tracking-[0.25em] mb-5"
                style={{ color: 'rgba(255,150,80,0.7)' }}
              >
                REQUIERE LICENCIA DE FUNDADOR
              </p>

              {/* Feature 2: Mensaje personalizado DAKI basado en historial del operador */}
              {personalMsg && (
                <motion.div
                  className="mb-4 px-4 py-3 border-l-2"
                  style={{ borderColor: 'rgba(0,255,65,0.35)', background: 'rgba(0,255,65,0.03)' }}
                  initial={{ opacity: 0, x: -6 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.15 }}
                >
                  <div className="text-[8px] tracking-[0.45em] mb-1.5" style={{ color: 'rgba(0,255,65,0.35)' }}>
                    DAKI ANALIZÓ TUS INCURSIONES
                  </div>
                  <p className="text-[10px] leading-relaxed" style={{ color: 'rgba(0,255,65,0.70)' }}>
                    {personalMsg}
                  </p>
                </motion.div>
              )}

              {/* Divider */}
              <div className="h-px mb-5" style={{ background: 'linear-gradient(90deg,transparent,rgba(255,80,30,0.25),transparent)' }} />

              {/* Features */}
              <ul className="space-y-2 mb-6">
                {FEATURES.map((f, i) => (
                  <motion.li
                    key={i}
                    className="flex items-start gap-2.5 text-[10px] leading-relaxed"
                    style={{ color: 'rgba(0,255,65,0.65)' }}
                    initial={{ opacity: 0, x: -8 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.08 + i * 0.06 }}
                  >
                    <span style={{ color: '#00FF41', marginTop: 1 }}>◈</span>
                    {f}
                  </motion.li>
                ))}
              </ul>

              {/* Divider */}
              <div className="h-px mb-5" style={{ background: 'linear-gradient(90deg,transparent,rgba(255,80,30,0.25),transparent)' }} />

              {/* Precio */}
              <div className="mb-4 p-4 text-center relative" style={{ border: '1px solid rgba(255,80,30,0.45)', background: 'rgba(255,50,10,0.06)' }}>
                <div className="absolute -top-2 left-1/2 -translate-x-1/2 text-[7px] tracking-[0.3em] px-2 py-0.5 font-black"
                  style={{ background: 'rgba(255,80,30,0.85)', color: '#fff' }}>
                  PRECIO FUNDADOR
                </div>
                <div className="text-[9px] line-through mb-1" style={{ color: 'rgba(255,150,80,0.35)' }}>$197 USD</div>
                <div className="text-3xl font-black" style={{ color: '#FF5020', textShadow: '0 0 12px rgba(255,80,30,0.4)' }}>
                  $97 <span className="text-sm font-normal">USD</span>
                </div>
                <div className="text-[8px] tracking-wider mt-1" style={{ color: 'rgba(255,150,80,0.50)' }}>PAGO ÚNICO · ACCESO DE POR VIDA</div>
              </div>

              {/* CTA único */}
              <div className="mb-1">
                <motion.button
                  onClick={handleCheckout}
                  disabled={checkoutState === 'loading'}
                  className="w-full py-4 text-sm font-black tracking-[0.25em] transition-all duration-150"
                  style={{
                    background: checkoutState === 'loading' ? 'rgba(255,50,10,0.30)' : 'linear-gradient(135deg, rgba(255,80,30,0.90), rgba(255,40,10,0.80))',
                    border:     '1px solid rgba(255,100,40,0.5)',
                    color:      '#fff',
                    textShadow: '0 1px 4px rgba(0,0,0,0.5)',
                    boxShadow:  '0 0 24px rgba(255,50,10,0.30)',
                    cursor:     checkoutState === 'loading' ? 'wait' : 'pointer',
                  }}
                  whileHover={checkoutState !== 'loading' ? { scale: 1.02, boxShadow: '0 0 36px rgba(255,60,10,0.45)' } : {}}
                  whileTap={{ scale: 0.98 }}
                >
                  {checkoutState === 'loading' ? '[ CONECTANDO CON HOTMART... ]' : 'OBTENER LICENCIA VITALICIA →'}
                </motion.button>
              </div>

              {checkoutError && (
                <p className="text-[9px] text-center tracking-wide mt-1" style={{ color: 'rgba(255,100,50,0.9)' }}>
                  ✗ {checkoutError}
                </p>
              )}

              {/* Feature 3: Framing emocional — comparación de valor */}
              <div className="mt-3 mb-1 space-y-1">
                {[
                  '▸ Un libro de Python cuesta más y no te da práctica real.',
                  '▸ Platzi / Coursera cobran mensual. Acá pagás una sola vez.',
                  '▸ Un bootcamp: $3.000 USD. Nexo: $97 con acceso de por vida.',
                ].map((line, i) => (
                  <p key={i} className="text-[8px] tracking-wider" style={{ color: 'rgba(0,255,65,0.28)' }}>
                    {line}
                  </p>
                ))}
              </div>

              {/* Dismiss link */}
              <button
                onClick={onClose}
                className="block w-full text-center mt-3 text-[9px] tracking-[0.4em] transition-colors"
                style={{ color: 'rgba(0,255,65,0.25)' }}
                onMouseEnter={(e) => (e.currentTarget.style.color = 'rgba(0,255,65,0.5)')}
                onMouseLeave={(e) => (e.currentTarget.style.color = 'rgba(0,255,65,0.25)')}
              >
                VOLVER A LA TERMINAL
              </button>

              {/* ══════════════════════════════════════════════════════════════
                  SECCIÓN DE OVERRIDE TÁCTICO
              ══════════════════════════════════════════════════════════════ */}
              <div
                className="mt-5 pt-4 px-3 pb-3"
                style={{
                  border:       '1px solid rgba(0,255,65,0.18)',
                  borderTop:    '1px solid rgba(0,255,65,0.22)',
                  background:   'rgba(0,255,65,0.03)',
                }}
              >
                {/* Header */}
                <div className="flex items-center gap-2 mb-2.5">
                  <motion.span
                    className="w-1.5 h-1.5 rounded-full shrink-0"
                    style={{ background: '#00FF41', boxShadow: '0 0 5px rgba(0,255,65,0.8)' }}
                    animate={{ opacity: [0.4, 1, 0.4] }}
                    transition={{ duration: 2, repeat: Infinity }}
                  />
                  <span
                    className="text-[9px] tracking-[0.4em] font-bold uppercase"
                    style={{ color: 'rgba(0,255,65,0.70)' }}
                  >
                    Llave de Acceso Táctico
                  </span>
                </div>

                <p
                  className="text-[10px] leading-relaxed mb-3"
                  style={{ color: 'rgba(0,255,65,0.55)' }}
                >
                  ¿Tienes un código de beta tester o invitado especial?
                </p>

                {/* Input */}
                <input
                  type="text"
                  value={codeInput}
                  onChange={(e) => {
                    setCodeInput(e.target.value.toUpperCase())
                    if (overrideState !== 'idle') setOverrideState('idle')
                  }}
                  onKeyDown={(e) => { if (e.key === 'Enter') handleRedeem() }}
                  placeholder="INGRESA TU CÓDIGO AQUÍ..."
                  disabled={overrideState === 'loading' || overrideState === 'success'}
                  className="w-full bg-transparent text-xs font-mono tracking-widest outline-none py-2.5 px-3 mb-2"
                  style={{
                    border:     `1px solid ${overrideState === 'error' ? 'rgba(255,80,30,0.6)' : 'rgba(0,255,65,0.40)'}`,
                    color:      '#00FF41',
                    caretColor: '#00FF41',
                    background: 'rgba(0,0,0,0.3)',
                  }}
                  spellCheck={false}
                  autoComplete="off"
                />

                {/* Button */}
                <button
                  onClick={handleRedeem}
                  disabled={!codeInput.trim() || overrideState === 'loading' || overrideState === 'success'}
                  className="w-full py-2.5 text-[10px] font-black tracking-[0.35em] uppercase transition-all duration-150"
                  style={{
                    background: codeInput.trim() && overrideState !== 'loading' && overrideState !== 'success'
                      ? 'rgba(0,255,65,0.12)'
                      : 'rgba(0,255,65,0.03)',
                    border: codeInput.trim() && overrideState !== 'loading' && overrideState !== 'success'
                      ? '1px solid rgba(0,255,65,0.55)'
                      : '1px solid rgba(0,255,65,0.18)',
                    color: codeInput.trim() && overrideState !== 'loading' && overrideState !== 'success'
                      ? '#00FF41'
                      : 'rgba(0,255,65,0.35)',
                    cursor: !codeInput.trim() || overrideState === 'loading' || overrideState === 'success'
                      ? 'not-allowed'
                      : 'pointer',
                    textShadow: codeInput.trim() ? '0 0 8px rgba(0,255,65,0.4)' : 'none',
                  }}
                >
                  {overrideState === 'loading' ? '[ VERIFICANDO... ]' : '[ EJECUTAR OVERRIDE ]'}
                </button>

                {/* Feedback */}
                <AnimatePresence mode="wait">
                  {overrideState === 'success' && (
                    <motion.p
                      key="ok"
                      initial={{ opacity: 0, y: 4 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0 }}
                      className="mt-2.5 text-[10px] tracking-[0.2em] font-bold text-center"
                      style={{ color: '#00FF41', textShadow: '0 0 10px rgba(0,255,65,0.6)' }}
                    >
                      ✓ {overrideMsg}
                    </motion.p>
                  )}
                  {overrideState === 'error' && (
                    <motion.p
                      key="err"
                      initial={{ opacity: 0, y: 4 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0 }}
                      className="mt-2.5 text-[10px] tracking-[0.15em] text-center"
                      style={{ color: 'rgba(255,100,50,0.9)' }}
                    >
                      ✗ {overrideMsg}
                    </motion.p>
                  )}
                </AnimatePresence>
              </div>
              {/* ── FIN OVERRIDE TÁCTICO ─────────────────────────────────── */}

            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}
