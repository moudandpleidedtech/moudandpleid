'use client'

/**
 * useIdleDetection — Detecta inactividad semántica en el editor de código.
 *
 * A diferencia de los listeners genéricos (mousemove, keydown), este hook
 * mide inactividad táctica: ausencia de cambios en el código O de envíos
 * de solución. El componente llama `resetTimer()` manualmente cuando ocurre
 * cualquiera de esas acciones.
 *
 * Uso:
 *   const { resetTimer } = useIdleDetection({
 *     timeoutMs: 120_000,
 *     onStuck: handleStuck,
 *     enabled: hydrated && !!userId,
 *   })
 *
 *   // En handleCodeChange:
 *   resetTimer()
 *   // En handleEjecutar (inicio):
 *   resetTimer()
 */

import { useCallback, useEffect, useRef } from 'react'

interface UseIdleDetectionOptions {
  /** Milisegundos sin actividad antes de disparar `onStuck`. Default: 120 000 (2 min). */
  timeoutMs?: number
  /** Callback que se invoca cuando se detecta estancamiento. */
  onStuck: () => void | Promise<void>
  /** Si false, el timer no corre. Útil para esperar hidratación. Default: true. */
  enabled?: boolean
}

interface UseIdleDetectionReturn {
  /** Reinicia el temporizador. Llámala cuando el usuario cambia código o envía. */
  resetTimer: () => void
  /** Detiene el temporizador sin disparar onStuck. */
  clearTimer: () => void
}

export function useIdleDetection({
  timeoutMs = 120_000,
  onStuck,
  enabled = true,
}: UseIdleDetectionOptions): UseIdleDetectionReturn {
  const timerRef   = useRef<ReturnType<typeof setTimeout>>()
  // onStuckRef mantiene la versión más reciente del callback sin re-suscribir el effect
  const onStuckRef = useRef(onStuck)
  onStuckRef.current = onStuck

  const clearTimer = useCallback(() => {
    if (timerRef.current) clearTimeout(timerRef.current)
  }, [])

  const resetTimer = useCallback(() => {
    if (!enabled) return
    if (timerRef.current) clearTimeout(timerRef.current)
    timerRef.current = setTimeout(() => {
      onStuckRef.current()
    }, timeoutMs)
  }, [enabled, timeoutMs])

  // Arranca el timer al montar (o cuando enabled cambia a true)
  useEffect(() => {
    if (!enabled) return
    resetTimer()
    return () => clearTimer()
  }, [enabled, resetTimer, clearTimer])

  return { resetTimer, clearTimer }
}
