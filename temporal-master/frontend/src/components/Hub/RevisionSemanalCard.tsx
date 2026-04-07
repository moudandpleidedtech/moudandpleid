'use client'

/**
 * RevisionSemanalCard — Conceptos que necesitan refuerzo semanal
 *
 * Llama a GET /intel/weekly-review y muestra hasta 8 conceptos con
 * mastery_score < 70 que no se han practicado en los últimos 7 días.
 * Solo aparece si hay conceptos pendientes.
 */

import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? ''

interface WeakConcept {
  concept: string
  score: number
  last_seen: string | null
  needs_reinforcement: boolean
}

function daysAgo(iso: string | null): string {
  if (!iso) return '?d'
  const diff = Date.now() - new Date(iso).getTime()
  const days = Math.floor(diff / 86400000)
  return days === 0 ? 'hoy' : `${days}d`
}

export default function RevisionSemanalCard({ userId }: { userId: string }) {
  const [concepts, setConcepts] = useState<WeakConcept[]>([])
  const [loaded, setLoaded] = useState(false)

  useEffect(() => {
    if (!userId) return
    fetch(`${API_BASE}/api/v1/intel/weekly-review?user_id=${userId}`)
      .then((r) => r.ok ? r.json() : null)
      .then((data) => {
        if (data?.concepts?.length) setConcepts(data.concepts)
        setLoaded(true)
      })
      .catch(() => setLoaded(true))
  }, [userId])

  if (!loaded || concepts.length === 0) return null

  return (
    <motion.div
      initial={{ opacity: 0, y: -6 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.6 }}
      className="font-mono border"
      style={{
        borderColor: 'rgba(255,184,0,0.2)',
        background:  '#0A0800',
        boxShadow:   '0 0 16px rgba(255,184,0,0.05)',
      }}
    >
      <div className="h-px" style={{ background: 'linear-gradient(90deg, #FFB800, transparent)' }} />

      <div className="px-4 py-3">
        <div className="flex items-center gap-2 mb-2">
          <motion.span
            className="text-sm"
            animate={{ opacity: [0.5, 1, 0.5] }}
            transition={{ duration: 2.4, repeat: Infinity }}
            style={{ color: '#FFB800' }}
          >⚠</motion.span>
          <span className="text-[7px] tracking-[0.5em]" style={{ color: 'rgba(255,184,0,0.5)' }}>
            REVISIÓN SEMANAL
          </span>
          <span className="text-[7px] tracking-widest px-1 border" style={{ borderColor: 'rgba(255,184,0,0.2)', color: 'rgba(255,184,0,0.4)' }}>
            {concepts.length} NODO{concepts.length > 1 ? 'S' : ''}
          </span>
        </div>

        <p className="text-[9px] mb-3" style={{ color: 'rgba(255,184,0,0.4)' }}>
          Estos conceptos no se han reforzado en 7+ días y tienen maestría incompleta.
        </p>

        <div className="flex flex-wrap gap-1.5">
          {concepts.map((c) => (
            <div
              key={c.concept}
              className="flex items-center gap-1.5 px-2 py-1 border text-[9px]"
              style={{
                borderColor: c.needs_reinforcement ? 'rgba(255,80,80,0.3)' : 'rgba(255,184,0,0.2)',
                background:  c.needs_reinforcement ? 'rgba(255,80,80,0.04)' : 'rgba(255,184,0,0.04)',
                color:       c.needs_reinforcement ? 'rgba(255,80,80,0.7)' : 'rgba(255,184,0,0.6)',
              }}
              title={`Maestría: ${c.score}% | Última vez: ${daysAgo(c.last_seen)} atrás`}
            >
              <span className="font-mono tracking-wide">
                {c.concept.toUpperCase().replace(/_/g, ' ')}
              </span>
              <span style={{ opacity: 0.5 }}>{c.score}%</span>
            </div>
          ))}
        </div>
      </div>
    </motion.div>
  )
}
