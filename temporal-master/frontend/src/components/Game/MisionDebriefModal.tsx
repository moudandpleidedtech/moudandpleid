'use client'

/**
 * MisionDebriefModal — Bucle metacognitivo post-misión
 *
 * Aparece inmediatamente después de completar una misión.
 * DAKI formula una pregunta de reflexión táctica.
 * El Operador responde en 2-3 líneas → activa retención a largo plazo.
 */

import { useEffect, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? ''

interface Props {
  visible: boolean
  userId: string
  challengeId: string
  attemptCount: number
  operatorLevel?: number    // nivel del operador — calibra dificultad de la pregunta
  difficultyTier?: number   // tier del challenge — 1=básico, 2=intermedio, 3=avanzado
  onClose: () => void
}

export default function MisionDebriefModal({
  visible,
  userId,
  challengeId,
  attemptCount,
  operatorLevel = 1,
  difficultyTier = 1,
  onClose,
}: Props) {
  const [question, setQuestion] = useState('')
  const [answer,   setAnswer]   = useState('')
  const [loading,  setLoading]  = useState(true)
  const [submitted, setSubmitted] = useState(false)

  useEffect(() => {
    if (!visible || !challengeId) return
    setLoading(true)
    setAnswer('')
    setSubmitted(false)

    fetch(`${API_BASE}/api/v1/daki/debrief`, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id:        userId,
        challenge_id:   challengeId,
        attempt_count:  attemptCount,
        operator_level: operatorLevel,
        difficulty_tier: difficultyTier,
      }),
    })
      .then(r => r.ok ? r.json() : null)
      .then((d: { question: string } | null) => {
        const fallback = operatorLevel <= 5 || difficultyTier <= 1
          ? '¿Con tus palabras, qué hizo el código que escribiste?'
          : operatorLevel <= 15 || difficultyTier <= 2
          ? '¿Qué cambiarías si el valor de entrada fuera diferente?'
          : '¿Cómo aplicarías este patrón si los datos de entrada cambiaran de tipo?'
        setQuestion(d?.question ?? fallback)
      })
      .catch(() => {
        setQuestion(operatorLevel <= 5 || difficultyTier <= 1
          ? '¿Con tus palabras, qué hizo el código que escribiste?'
          : '¿Qué modificarías en tu solución si el tipo de dato cambiara?')
      })
      .finally(() => setLoading(false))
  }, [visible, challengeId]) // eslint-disable-line react-hooks/exhaustive-deps

  const handleSubmit = () => {
    if (!answer.trim()) return
    setSubmitted(true)
    setTimeout(onClose, 1600)
  }

  const handleSkip = () => onClose()

  return (
    <AnimatePresence>
      {visible && (
        <>
          {/* Backdrop */}
          <motion.div
            key="bd"
            className="fixed inset-0 z-[95] bg-black/85"
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
          />

          {/* Modal */}
          <motion.div
            key="modal"
            className="fixed inset-0 z-[96] flex items-center justify-center p-4"
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
          >
            <motion.div
              className="relative w-full max-w-md bg-[#060D06] border border-[#00FF41]/30 font-mono overflow-hidden"
              style={{ boxShadow: '0 0 80px rgba(0,255,65,0.12)' }}
              initial={{ scale: 0.88, y: 24 }}
              animate={{ scale: 1, y: 0 }}
              exit={{ scale: 0.92, y: 16, opacity: 0 }}
              transition={{ type: 'spring', stiffness: 300, damping: 28 }}
            >
              {/* Top accent line */}
              <div className="h-px w-full"
                style={{ background: 'linear-gradient(90deg,transparent,rgba(0,255,65,0.6),transparent)' }}
              />

              {/* Scanlines */}
              <div className="absolute inset-0 pointer-events-none opacity-[0.025]"
                style={{ backgroundImage: 'repeating-linear-gradient(0deg,transparent,transparent 3px,#00FF41 3px,#00FF41 4px)' }}
              />

              {/* Header */}
              <div className="px-6 pt-5 pb-4 border-b border-[#00FF41]/12">
                <div className="flex items-center gap-2 mb-2">
                  <motion.span
                    className="text-[10px] tracking-[0.35em] text-[#00FF41]/60 border border-[#00FF41]/25 px-2 py-0.5"
                    animate={{ opacity: [0.5, 1, 0.5] }}
                    transition={{ duration: 2, repeat: Infinity }}
                  >
                    MISIÓN COMPLETADA
                  </motion.span>
                </div>
                <h2 className="text-[13px] font-black tracking-[0.15em] text-[#00FF41]"
                  style={{ textShadow: '0 0 12px rgba(0,255,65,0.4)' }}>
                  DEBRIEF TÁCTICO — DAKI
                </h2>
              </div>

              {/* DAKI question */}
              <div className="px-6 py-5 border-b border-[#00FF41]/08">
                <p className="text-[9px] tracking-[0.4em] text-[#00FF41]/30 uppercase mb-3">
                  {'> [DAKI] PROTOCOLO DE REFLEXIÓN ACTIVADO'}
                </p>
                {loading ? (
                  <p className="text-xs text-[#00FF41]/35 animate-pulse tracking-wide">
                    Analizando misión_
                  </p>
                ) : submitted ? (
                  <motion.p
                    className="text-xs text-[#00FF41]/70 leading-5 tracking-wide"
                    initial={{ opacity: 0 }} animate={{ opacity: 1 }}
                  >
                    Respuesta registrada. El conocimiento que articulas se ancla más profundo
                    que el que solo ejecutas.
                  </motion.p>
                ) : (
                  <p className="text-xs text-[#00FF41]/80 leading-6 tracking-wide"
                    style={{ whiteSpace: 'pre-wrap' }}>
                    {question}
                  </p>
                )}
              </div>

              {/* Input */}
              {!loading && !submitted && (
                <div className="px-6 py-4 bg-[#030803]">
                  <p className="text-[8px] tracking-[0.4em] text-[#00FF41]/25 uppercase mb-2">
                    REPORTE DEL OPERADOR
                  </p>
                  <textarea
                    value={answer}
                    onChange={e => setAnswer(e.target.value)}
                    rows={3}
                    placeholder="Escribe tu análisis..."
                    className="w-full bg-transparent border border-[#00FF41]/15 text-[#00FF41]/75 text-xs leading-5 p-3 outline-none resize-none placeholder:text-[#00FF41]/15 focus:border-[#00FF41]/35 transition-colors"
                    style={{ fontFamily: 'monospace' }}
                  />
                  <div className="flex items-center justify-between mt-3">
                    <button
                      onClick={handleSkip}
                      className="text-[9px] tracking-[0.3em] text-[#00FF41]/20 hover:text-[#00FF41]/45 transition-colors uppercase"
                    >
                      [ Omitir ]
                    </button>
                    <motion.button
                      onClick={handleSubmit}
                      disabled={!answer.trim()}
                      className="border border-[#00FF41]/25 bg-[#00FF41]/[0.06] text-[#00FF41] text-[10px] tracking-[0.35em] uppercase px-5 py-2.5 disabled:opacity-25 hover:bg-[#00FF41]/10 hover:border-[#00FF41]/45 transition-all duration-150"
                      whileTap={{ scale: 0.97 }}
                    >
                      REGISTRAR ANÁLISIS
                    </motion.button>
                  </div>
                </div>
              )}

              {submitted && (
                <div className="px-6 py-4">
                  <motion.p
                    className="text-[9px] tracking-[0.3em] text-[#00FF41]/40 text-center"
                    initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.3 }}
                  >
                    CERRANDO DEBRIEF...
                  </motion.p>
                </div>
              )}
            </motion.div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}
