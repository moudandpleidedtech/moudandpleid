'use client'
/**
 * useRetrievalMode — detecta ?mode=retrieval en la URL.
 *
 * Cuando el operador llega desde RevisionSemanalCard vía ↺ PRACTICAR,
 * la URL incluye mode=retrieval. Este hook lo detecta una vez al montar.
 *
 * Retorna:
 *   isRetrievalMode: boolean — true si el challenge se abrió en modo recuperación
 */

import { useEffect, useState } from 'react'

export function useRetrievalMode(): boolean {
  const [isRetrievalMode, setIsRetrievalMode] = useState(false)

  useEffect(() => {
    const params = new URLSearchParams(window.location.search)
    setIsRetrievalMode(params.get('mode') === 'retrieval')
  }, [])

  return isRetrievalMode
}
