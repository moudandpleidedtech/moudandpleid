'use client'
/**
 * usePatternCallout — detecta overlap de conceptos con challenges anteriores.
 *
 * F5: 1.5s después de cargar el challenge (level_order >= 20), llama a
 * GET /intel/pattern-callout y si hay match agrega una línea a la consola.
 *
 * Props:
 *   challengeId — ID del challenge actual (string | null)
 *   userId      — ID del operador (string | null)
 *   levelOrder  — level_order del challenge (number | null)
 *   onMatch     — callback (line: string) → void; agrega línea a consola
 */

import { useEffect } from 'react'

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? ''

interface PatternCalloutResult {
  previous_title?: string
  previous_level?: number
  concept?: string
}

export function usePatternCallout({
  challengeId,
  userId,
  levelOrder,
  onMatch,
}: {
  challengeId: string | null
  userId: string | null
  levelOrder: number | null
  onMatch: (line: string) => void
}): void {
  useEffect(() => {
    if (!challengeId || !userId || (levelOrder ?? 0) < 20) return

    const timer = setTimeout(async () => {
      try {
        const r = await fetch(
          `${API_BASE}/api/v1/intel/pattern-callout` +
          `?user_id=${userId}&challenge_id=${challengeId}`,
        )
        if (!r.ok) return
        const d: PatternCalloutResult = await r.json()
        if (d.concept && d.previous_title) {
          onMatch(
            `[DAKI] Ya trabajaste '${d.concept}' en '${d.previous_title}' (L${d.previous_level ?? '?'}). ` +
            `Conectá ese conocimiento previo.`,
          )
        }
      } catch {
        // silencioso — no es crítico
      }
    }, 1500)

    return () => clearTimeout(timer)
  }, [challengeId, userId, levelOrder, onMatch])
}
