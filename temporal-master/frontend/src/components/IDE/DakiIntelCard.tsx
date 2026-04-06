'use client'

/**
 * DakiIntelCard — Briefing de concepto para challenges sin theory_content
 *
 * Aparece antes del editor cuando el challenge no tiene teoría en la DB.
 * Usa el conceptGlossary para mostrar una mini-lección DAKI instantánea
 * (sin llamada a LLM — respuesta inmediata).
 *
 * Props:
 *   concepts     — array de conceptos del challenge (de concepts_taught_json)
 *   challengeTitle — para el header contextual
 *   onStart      — callback para entrar al editor
 */

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { getConceptTheory } from '@/lib/conceptGlossary'

interface Props {
  concepts:       string[]
  challengeTitle: string
  onStart:        () => void
}

export default function DakiIntelCard({ concepts, challengeTitle, onStart }: Props) {
  const [revealed, setReveal] = useState(false)
  const entry = getConceptTheory(concepts)

  // Si no hay entrada en el glossary para ningún concepto, ir directo al editor
  if (!entry) {
    onStart()
    return null
  }

  return (
    <motion.div
      className="flex-1 flex flex-col items-center justify-center px-6 py-8 font-mono overflow-y-auto"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
    >
      <div
        className="w-full max-w-xl"
        style={{
          border:     '1px solid rgba(0,255,65,0.20)',
          background: '#030A03',
          boxShadow:  '0 0 30px rgba(0,255,65,0.06)',
        }}
      >
        <div className="h-px" style={{ background: 'linear-gradient(90deg, transparent, #00FF41, transparent)' }} />

        {/* Header */}
        <div className="px-5 py-4 border-b border-[#00FF41]/08">
          <p className="text-[7px] tracking-[0.7em] text-[#00FF41]/30 mb-0.5">
            // DAKI INTEL — PRE-INCURSIÓN
          </p>
          <h2 className="text-xs font-black tracking-[0.2em] text-[#00FF41]"
            style={{ textShadow: '0 0 10px rgba(0,255,65,0.30)' }}>
            {entry.title}
          </h2>
          <p className="text-[8px] tracking-wider text-[#00FF41]/30 mt-0.5">
            MISIÓN: {challengeTitle.toUpperCase()}
          </p>
        </div>

        {/* Theory */}
        <div className="px-5 py-4 space-y-4">
          <p className="text-[10px] leading-relaxed text-[#00FF41]/70">
            {entry.theory}
          </p>

          {/* Code example */}
          <div>
            <p className="text-[7px] tracking-[0.5em] text-[#00FF41]/25 mb-2">EJEMPLO TÁCTICO</p>
            <pre
              className="text-[10px] leading-relaxed p-3 overflow-x-auto"
              style={{
                background:  'rgba(0,255,65,0.04)',
                border:      '1px solid rgba(0,255,65,0.12)',
                color:       'rgba(0,255,65,0.80)',
                fontFamily:  'monospace',
              }}
            >
              {entry.example}
            </pre>
          </div>

          {/* Real world */}
          <AnimatePresence>
            {revealed && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                className="border-l-2 pl-3"
                style={{ borderColor: 'rgba(0,255,65,0.25)' }}
              >
                <p className="text-[7px] tracking-[0.5em] text-[#00FF41]/25 mb-1">CONEXIÓN MUNDO REAL</p>
                <p className="text-[9px] leading-relaxed text-[#00FF41]/50 italic">
                  {entry.realWorld}
                </p>
              </motion.div>
            )}
          </AnimatePresence>

          {!revealed && (
            <button
              onClick={() => setReveal(true)}
              className="text-[8px] tracking-[0.4em] text-[#00FF41]/25 hover:text-[#00FF41]/60 transition-colors"
            >
              {'▸ VER APLICACIÓN REAL'}
            </button>
          )}
        </div>

        {/* CTA */}
        <div className="px-5 pb-5 flex justify-between items-center border-t border-[#00FF41]/08 pt-4">
          <p className="text-[8px] tracking-wider text-[#00FF41]/20">
            Conceptos: {concepts.slice(0, 3).join(' · ').toUpperCase()}
          </p>
          <button
            onClick={onStart}
            className="text-[10px] tracking-[0.4em] px-5 py-2 border font-bold transition-all duration-150"
            style={{ borderColor: 'rgba(0,255,65,0.50)', color: '#00FF41' }}
            onMouseEnter={e => {
              e.currentTarget.style.background   = 'rgba(0,255,65,0.08)'
              e.currentTarget.style.boxShadow    = '0 0 16px rgba(0,255,65,0.20)'
            }}
            onMouseLeave={e => {
              e.currentTarget.style.background   = 'transparent'
              e.currentTarget.style.boxShadow    = 'none'
            }}
          >
            INICIAR INCURSIÓN →
          </button>
        </div>

        <div className="h-px" style={{ background: 'linear-gradient(90deg, transparent, rgba(0,255,65,0.40), transparent)' }} />
      </div>
    </motion.div>
  )
}
