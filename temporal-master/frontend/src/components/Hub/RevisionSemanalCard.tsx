'use client'

/**
 * RevisionSemanalCard — Conceptos que necesitan refuerzo semanal
 *
 * Llama a GET /intel/weekly-review y muestra hasta 8 conceptos con
 * mastery_score < 70 que no se han practicado en los últimos 7 días.
 * Cada concepto tiene botón de retrieval: navega a un challenge completado
 * en modo ?mode=retrieval (sin pistas, con banner de recuperación).
 */

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
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
  const router = useRouter()
  const [concepts, setConcepts]     = useState<WeakConcept[]>([])
  const [loaded, setLoaded]         = useState(false)
  const [loading, setLoading]       = useState<string | null>(null)  // concept cargando

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

  // F7: navegar a un challenge de recuperación para el concepto dado
  const handleRetrieval = async (concept: string) => {
    if (loading) return
    setLoading(concept)
    try {
      const res = await fetch(
        `${API_BASE}/api/v1/intel/retrieval-challenge?user_id=${userId}&concept=${encodeURIComponent(concept)}`,
        { credentials: 'include' }
      )
      if (!res.ok) return
      const d = await res.json()
      if (d?.challenge_id) {
        router.push(`/challenge/${d.challenge_id}?mode=retrieval`)
      }
    } finally {
      setLoading(null)
    }
  }

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
          Conceptos sin refuerzo en 7+ días. Activá el Protocolo de Recuperación en cada uno.
        </p>

        <div className="flex flex-col gap-1.5">
          {concepts.map((c) => (
            <div
              key={c.concept}
              className="flex items-center justify-between px-2 py-1.5 border text-[9px]"
              style={{
                borderColor: c.needs_reinforcement ? 'rgba(255,80,80,0.3)' : 'rgba(255,184,0,0.2)',
                background:  c.needs_reinforcement ? 'rgba(255,80,80,0.04)' : 'rgba(255,184,0,0.04)',
              }}
            >
              <div className="flex items-center gap-2">
                <span className="font-mono tracking-wide"
                  style={{ color: c.needs_reinforcement ? 'rgba(255,80,80,0.7)' : 'rgba(255,184,0,0.6)' }}>
                  {c.concept.toUpperCase().replace(/_/g, ' ')}
                </span>
                <span style={{ color: 'rgba(255,255,255,0.2)' }}>{c.score}%</span>
                <span style={{ color: 'rgba(255,255,255,0.15)' }}>·</span>
                <span style={{ color: 'rgba(255,255,255,0.2)' }}>{daysAgo(c.last_seen)} atrás</span>
              </div>
              <button
                onClick={() => handleRetrieval(c.concept)}
                disabled={loading === c.concept}
                className="text-[7px] tracking-[0.35em] uppercase px-2 py-0.5 border transition-all disabled:opacity-40"
                style={{ borderColor: 'rgba(189,0,255,0.3)', color: 'rgba(189,0,255,0.6)', background: 'rgba(189,0,255,0.04)' }}
              >
                {loading === c.concept ? '...' : '↺ PRACTICAR'}
              </button>
            </div>
          ))}
        </div>
      </div>
    </motion.div>
  )
}
