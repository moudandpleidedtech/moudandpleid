'use client'

/**
 * IntelReportModal — D026 Reporte de Inteligencia
 *
 * Modal táctico para que los Alpha Testers reporten bugs, UX y sugerencias
 * directamente desde el Hub sin salir del Nexo.
 *
 * POST /api/v1/reports
 */

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? ''

// ─── Types ────────────────────────────────────────────────────────────────────

type ReportType     = 'BUG' | 'UX_UI' | 'TACTICAL_IDEA'
type ReportSeverity = 'LOW' | 'HIGH' | 'CRITICAL'
type SubmitState    = 'idle' | 'loading' | 'success' | 'error'

interface Props {
  isOpen:  boolean
  onClose: () => void
  userId:  string
}

// ─── Config ───────────────────────────────────────────────────────────────────

const TYPE_OPTIONS: { value: ReportType; label: string; icon: string; color: string; desc: string }[] = [
  { value: 'BUG',           label: 'FALLA DE SISTEMA',    icon: '⬟', color: '#FF2D78', desc: 'Algo está roto o no funciona como debería' },
  { value: 'UX_UI',         label: 'INTERFAZ TÁCTICA',    icon: '◎', color: '#00B4D8', desc: 'El diseño o la experiencia puede mejorar' },
  { value: 'TACTICAL_IDEA', label: 'PROPUESTA DE INTEL',  icon: '◈', color: '#FFC700', desc: 'Una idea o feature para el Nexo' },
]

const SEVERITY_OPTIONS: { value: ReportSeverity; label: string; color: string; desc: string }[] = [
  { value: 'LOW',      label: 'BAJA',     color: '#00FF41', desc: 'No bloquea operaciones' },
  { value: 'HIGH',     label: 'ALTA',     color: '#FFB800', desc: 'Afecta la experiencia significativamente' },
  { value: 'CRITICAL', label: 'CRÍTICA',  color: '#FF2D78', desc: 'El sistema está comprometido' },
]

// ─── Componente ───────────────────────────────────────────────────────────────

export default function IntelReportModal({ isOpen, onClose, userId }: Props) {
  const [type,               setType]              = useState<ReportType>('BUG')
  const [severity,           setSeverity]          = useState<ReportSeverity>('LOW')
  const [description,        setDescription]       = useState('')
  const [stepsToReproduce,   setStepsToReproduce]  = useState('')
  const [submitState,        setSubmitState]       = useState<SubmitState>('idle')
  const [charCount,          setCharCount]         = useState(0)

  const selectedType     = TYPE_OPTIONS.find(t => t.value === type)!
  const selectedSeverity = SEVERITY_OPTIONS.find(s => s.value === severity)!

  const handleClose = () => {
    if (submitState === 'loading') return
    // Reset si no está en éxito (el éxito se auto-cierra)
    setType('BUG')
    setSeverity('LOW')
    setDescription('')
    setStepsToReproduce('')
    setSubmitState('idle')
    setCharCount(0)
    onClose()
  }

  const handleSubmit = async () => {
    if (submitState === 'loading' || description.trim().length < 10) return
    setSubmitState('loading')

    try {
      const res = await fetch(`${API_BASE}/api/v1/reports`, {
        method:      'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          type,
          severity,
          description:        description.trim(),
          steps_to_reproduce: stepsToReproduce.trim() || null,
        }),
      })

      if (!res.ok) throw new Error('submit_failed')
      setSubmitState('success')

      // Auto-cierre después del toast
      setTimeout(() => {
        handleClose()
      }, 3200)
    } catch {
      setSubmitState('error')
      setTimeout(() => setSubmitState('idle'), 3000)
    }
  }

  const accentColor = selectedType.color

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={handleClose}
          />

          {/* Modal */}
          <motion.div
            className="fixed inset-0 z-50 flex items-center justify-center p-4"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <motion.div
              className="relative w-full max-w-lg font-mono overflow-hidden"
              style={{
                background: 'rgba(4,6,4,0.97)',
                border:     `1px solid ${accentColor}30`,
                boxShadow:  `0 0 40px ${accentColor}10, 0 0 80px rgba(0,0,0,0.8)`,
              }}
              initial={{ scale: 0.93, y: 16 }}
              animate={{ scale: 1,    y: 0  }}
              exit={{    scale: 0.93, y: 16 }}
              transition={{ duration: 0.2, ease: [0.16, 1, 0.3, 1] }}
              onClick={e => e.stopPropagation()}
            >
              {/* Línea de pulso superior */}
              <motion.div
                className="absolute top-0 left-0 right-0 h-px"
                style={{ background: `linear-gradient(90deg,transparent,${accentColor}60,transparent)` }}
                animate={{ opacity: [0.3, 0.9, 0.3] }}
                transition={{ duration: 2.5, repeat: Infinity }}
              />

              {/* ── Header ── */}
              <div
                className="flex items-center justify-between px-5 py-3.5 border-b"
                style={{ borderColor: `${accentColor}15`, background: `${accentColor}05` }}
              >
                <div className="flex items-center gap-2.5">
                  <motion.div
                    className="w-2 h-2 rounded-full"
                    style={{ background: accentColor }}
                    animate={{ opacity: [1, 0.3, 1], scale: [1, 1.4, 1] }}
                    transition={{ duration: 1.4, repeat: Infinity }}
                  />
                  <div>
                    <p className="text-[10px] font-black tracking-[0.45em] uppercase" style={{ color: accentColor }}>
                      REPORTE DE INTELIGENCIA
                    </p>
                    <p className="text-[8px] tracking-[0.3em]" style={{ color: `${accentColor}50` }}>
                      CANAL CIFRADO — ALTO MANDO
                    </p>
                  </div>
                </div>
                <button
                  onClick={handleClose}
                  className="text-[#00FF41]/25 hover:text-[#00FF41]/70 transition-colors text-sm font-mono tracking-widest"
                >
                  [×]
                </button>
              </div>

              {/* ── Body ── */}
              <div className="px-5 py-5 flex flex-col gap-4 max-h-[70vh] overflow-y-auto" style={{ scrollbarWidth: 'none' }}>

                {/* Tipo de reporte */}
                <div>
                  <label className="text-[8px] tracking-[0.5em] text-[#00FF41]/30 uppercase block mb-2">
                    // CLASIFICACIÓN DEL INCIDENTE
                  </label>
                  <div className="grid grid-cols-3 gap-2">
                    {TYPE_OPTIONS.map(opt => (
                      <button
                        key={opt.value}
                        onClick={() => setType(opt.value)}
                        className="relative p-3 border text-left transition-all duration-150"
                        style={{
                          borderColor: type === opt.value ? `${opt.color}55` : `${opt.color}15`,
                          background:  type === opt.value ? `${opt.color}08` : 'transparent',
                        }}
                      >
                        {type === opt.value && (
                          <motion.div
                            className="absolute top-0 left-0 right-0 h-px"
                            style={{ background: `linear-gradient(90deg,transparent,${opt.color}70,transparent)` }}
                            layoutId="type-indicator"
                          />
                        )}
                        <span className="text-sm block mb-1" style={{ color: opt.color }}>{opt.icon}</span>
                        <p className="text-[8px] font-black tracking-[0.2em] uppercase leading-tight" style={{ color: `${opt.color}${type === opt.value ? 'cc' : '50'}` }}>
                          {opt.label}
                        </p>
                      </button>
                    ))}
                  </div>
                  <p className="text-[8px] mt-1.5 tracking-wide" style={{ color: `${accentColor}45` }}>
                    {selectedType.desc}
                  </p>
                </div>

                {/* Severidad */}
                <div>
                  <label className="text-[8px] tracking-[0.5em] text-[#00FF41]/30 uppercase block mb-2">
                    // NIVEL DE AMENAZA
                  </label>
                  <div className="flex gap-2">
                    {SEVERITY_OPTIONS.map(opt => (
                      <button
                        key={opt.value}
                        onClick={() => setSeverity(opt.value)}
                        className="flex-1 py-2 px-3 border text-center transition-all duration-150"
                        style={{
                          borderColor: severity === opt.value ? `${opt.color}60` : `${opt.color}18`,
                          background:  severity === opt.value ? `${opt.color}10` : 'transparent',
                          color:       severity === opt.value ? opt.color : `${opt.color}45`,
                        }}
                      >
                        <p className="text-[8px] font-black tracking-[0.3em]">{opt.label}</p>
                      </button>
                    ))}
                  </div>
                  <p className="text-[8px] mt-1.5 tracking-wide" style={{ color: `${selectedSeverity.color}40` }}>
                    {selectedSeverity.desc}
                  </p>
                </div>

                {/* Descripción */}
                <div>
                  <label className="text-[8px] tracking-[0.5em] text-[#00FF41]/30 uppercase block mb-2">
                    // DESCRIPCIÓN DEL INCIDENTE
                    <span className="ml-2 text-[#00FF41]/20 normal-case tracking-normal">
                      ({charCount}/2000)
                    </span>
                  </label>
                  <textarea
                    value={description}
                    onChange={e => { setDescription(e.target.value); setCharCount(e.target.value.length) }}
                    placeholder="Describe el problema con precisión táctica. ¿Qué esperabas? ¿Qué ocurrió?"
                    rows={4}
                    maxLength={2000}
                    className="w-full bg-transparent text-[10px] text-[#00FF41]/80 placeholder:text-[#00FF41]/18 outline-none resize-none p-3 border transition-all duration-150"
                    style={{
                      borderColor: description.length >= 10 ? `${accentColor}30` : 'rgba(0,255,65,0.12)',
                      fontFamily: 'monospace',
                    }}
                    onFocus={e => e.target.style.borderColor = `${accentColor}55`}
                    onBlur={e  => e.target.style.borderColor = description.length >= 10 ? `${accentColor}30` : 'rgba(0,255,65,0.12)'}
                  />
                  {description.trim().length > 0 && description.trim().length < 10 && (
                    <p className="text-[8px] text-[#FF2D78]/70 mt-1 tracking-wide">
                      Mínimo 10 caracteres para transmitir el reporte.
                    </p>
                  )}
                </div>

                {/* Pasos para reproducir — solo para BUG */}
                <AnimatePresence>
                  {type === 'BUG' && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      exit={{    opacity: 0, height: 0 }}
                      transition={{ duration: 0.2 }}
                    >
                      <label className="text-[8px] tracking-[0.5em] text-[#FF2D78]/40 uppercase block mb-2">
                        // PASOS PARA REPRODUCIR
                        <span className="ml-2 text-[#00FF41]/20 normal-case tracking-normal">(opcional)</span>
                      </label>
                      <textarea
                        value={stepsToReproduce}
                        onChange={e => setStepsToReproduce(e.target.value)}
                        placeholder={"1. Ir a /hub\n2. Hacer clic en...\n3. Observar que..."}
                        rows={3}
                        maxLength={2000}
                        className="w-full bg-transparent text-[10px] text-[#00FF41]/70 placeholder:text-[#00FF41]/15 outline-none resize-none p-3 border border-[#FF2D78]/15 transition-all duration-150"
                        style={{ fontFamily: 'monospace' }}
                        onFocus={e => e.target.style.borderColor = 'rgba(255,45,120,0.35)'}
                        onBlur={e  => e.target.style.borderColor = 'rgba(255,45,120,0.15)'}
                      />
                    </motion.div>
                  )}
                </AnimatePresence>

              </div>

              {/* ── Footer / Submit ── */}
              <div
                className="px-5 py-4 border-t"
                style={{ borderColor: `${accentColor}10`, background: `${accentColor}03` }}
              >
                <AnimatePresence mode="wait">

                  {/* Success toast */}
                  {submitState === 'success' && (
                    <motion.div
                      key="success"
                      initial={{ opacity: 0, y: 6 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -6 }}
                      className="flex items-center gap-3 py-2"
                      style={{
                        border:     '1px solid rgba(0,255,65,0.35)',
                        background: 'rgba(0,255,65,0.06)',
                        padding:    '12px 16px',
                      }}
                    >
                      <motion.span
                        className="text-lg"
                        animate={{ scale: [1, 1.3, 1] }}
                        transition={{ duration: 0.4 }}
                      >
                        ✓
                      </motion.span>
                      <div>
                        <p className="text-[9px] font-black tracking-[0.3em] text-[#00FF41] uppercase">
                          Reporte encriptado enviado al Alto Mando.
                        </p>
                        <p className="text-[8px] text-[#00FF41]/50 tracking-wider mt-0.5">
                          Buen trabajo, Operador.
                        </p>
                      </div>
                    </motion.div>
                  )}

                  {/* Error */}
                  {submitState === 'error' && (
                    <motion.div
                      key="error"
                      initial={{ opacity: 0, y: 6 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -6 }}
                      className="py-3 px-4 border border-[#FF2D78]/30 bg-[#FF2D78]/06"
                    >
                      <p className="text-[9px] text-[#FF2D78]/80 tracking-[0.25em] uppercase">
                        Error en la transmisión. Reintentá en unos segundos.
                      </p>
                    </motion.div>
                  )}

                  {/* Idle / Loading */}
                  {(submitState === 'idle' || submitState === 'loading') && (
                    <motion.div
                      key="actions"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      exit={{ opacity: 0 }}
                      className="flex items-center justify-between gap-3"
                    >
                      <button
                        onClick={handleClose}
                        className="text-[9px] tracking-[0.3em] uppercase text-[#00FF41]/25 hover:text-[#00FF41]/55 transition-colors font-mono"
                      >
                        [ ABORTAR ]
                      </button>

                      <motion.button
                        onClick={handleSubmit}
                        disabled={submitState === 'loading' || description.trim().length < 10}
                        className="px-6 py-2.5 border text-[9px] tracking-[0.35em] uppercase font-mono transition-all duration-150 disabled:opacity-35 disabled:cursor-not-allowed"
                        style={{
                          borderColor: accentColor + '55',
                          color:       accentColor,
                          background:  accentColor + '08',
                        }}
                        whileHover={description.trim().length >= 10 ? {
                          background:  accentColor + '18',
                          borderColor: accentColor + '99',
                          boxShadow:   `0 0 16px ${accentColor}20`,
                        } : {}}
                        whileTap={description.trim().length >= 10 ? { scale: 0.97 } : {}}
                      >
                        {submitState === 'loading' ? (
                          <span className="flex items-center gap-2">
                            <motion.span
                              animate={{ rotate: 360 }}
                              transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
                              className="inline-block"
                            >
                              ◌
                            </motion.span>
                            TRANSMITIENDO...
                          </span>
                        ) : (
                          '▶ TRANSMITIR REPORTE'
                        )}
                      </motion.button>
                    </motion.div>
                  )}

                </AnimatePresence>
              </div>

              {/* Línea de pulso inferior */}
              <motion.div
                className="absolute bottom-0 left-0 right-0 h-px"
                style={{ background: `linear-gradient(90deg,transparent,${accentColor}30,transparent)` }}
                animate={{ opacity: [0.2, 0.6, 0.2] }}
                transition={{ duration: 3, repeat: Infinity, delay: 1.2 }}
              />
            </motion.div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}
