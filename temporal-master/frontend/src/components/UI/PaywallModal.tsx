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
 *   paymentUrl  — URL del flujo de pago (default: https://pay.dakiedtech.com)
 */

import { motion, AnimatePresence } from 'framer-motion'

interface Props {
  visible: boolean
  onClose: () => void
  paymentUrl?: string
}

const FEATURES = [
  'Acceso completo a los 90 niveles del Nexo (L11–L100)',
  'Sistema de Duelos PvP contra operadores globales',
  'Certificado de Operador al completar el 100%',
  'DAKI Compañero — nivel evolutivo máximo desbloqueado',
  'Soporte prioritario y actualizaciones de por vida',
]

export default function PaywallModal({
  visible,
  onClose,
  paymentUrl = 'https://pay.dakiedtech.com',
}: Props) {
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

              {/* Price + CTA */}
              <div className="flex items-center justify-between mb-4">
                <div>
                  <div className="text-[9px] tracking-[0.4em]" style={{ color: 'rgba(255,150,80,0.5)' }}>
                    LICENCIA DE FUNDADOR
                  </div>
                  <div
                    className="text-2xl font-black tracking-wide mt-0.5"
                    style={{ color: '#00FF41', textShadow: '0 0 12px rgba(0,255,65,0.5)' }}
                  >
                    $24.90
                    <span className="text-sm font-normal ml-1" style={{ color: 'rgba(0,255,65,0.5)' }}>USD</span>
                  </div>
                  <div className="text-[8px] tracking-widest mt-0.5" style={{ color: 'rgba(0,255,65,0.3)' }}>
                    PAGO ÚNICO · ACCESO DE POR VIDA
                  </div>
                </div>

                {/* Glitch chip */}
                <div
                  className="px-3 py-1.5 text-[9px] tracking-[0.3em] font-bold"
                  style={{
                    border:     '1px solid rgba(0,255,65,0.25)',
                    color:      'rgba(0,255,65,0.45)',
                    background: 'rgba(0,255,65,0.04)',
                  }}
                >
                  PAGO ÚNICO
                </div>
              </div>

              {/* Main CTA */}
              <motion.a
                href={paymentUrl}
                rel="noopener noreferrer"
                className="block w-full text-center py-3.5 text-xs font-black tracking-[0.3em] transition-all duration-150"
                style={{
                  background: 'linear-gradient(135deg, rgba(255,80,30,0.85), rgba(255,40,10,0.75))',
                  border:     '1px solid rgba(255,100,40,0.5)',
                  color:      '#fff',
                  textShadow: '0 1px 4px rgba(0,0,0,0.5)',
                  boxShadow:  '0 0 20px rgba(255,50,10,0.25)',
                }}
                whileHover={{ scale: 1.02, boxShadow: '0 0 30px rgba(255,60,10,0.40)' }}
                whileTap={{ scale: 0.98 }}
              >
                ADQUIRIR LICENCIA DE FUNDADOR →
              </motion.a>

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
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}
