'use client'
/**
 * useRubberDuck — F3: Rubber Duck Gate antes de pedir ENIGMA.
 *
 * Cuando el operador lleva failStreak >= 3 en level_order >= 30,
 * antes de pedir pista se le pide que articule su razonamiento (mín. 15 chars).
 *
 * Retorna:
 *   showRubberDuck    — boolean: muestra el modal
 *   rubberDuckText    — texto explicativo del operador
 *   setRubberDuckText
 *   openRubberDuck()  — abre el gate (llamar desde requestHint)
 *   closeRubberDuck() — cierra el modal sin pedir pista
 *   confirmRubberDuck(onConfirm: () => void)
 *     — valida mín. 15 chars y llama onConfirm() (que debe llamar requestHint)
 *   shouldGate(failStreak, levelOrder, isIronman, isRetrieval) → boolean
 *     — retorna true si el gate debe activarse
 */

import { useState, useCallback } from 'react'

const MIN_CHARS = 15

export function useRubberDuck() {
  const [showRubberDuck,  setShowRubberDuck]  = useState(false)
  const [rubberDuckText,  setRubberDuckText]  = useState('')

  const shouldGate = useCallback(
    (
      failStreak:    number,
      levelOrder:    number | null | undefined,
      isIronman:     boolean | undefined,
      isRetrieval:   boolean,
      pendingHint:   boolean,
    ): boolean => {
      if (isIronman || isRetrieval || pendingHint) return false
      const earlyLevel = (levelOrder ?? 0) < 30
      return !earlyLevel && failStreak >= 3
    },
    [],
  )

  const openRubberDuck = useCallback(() => {
    setRubberDuckText('')
    setShowRubberDuck(true)
  }, [])

  const closeRubberDuck = useCallback(() => {
    setShowRubberDuck(false)
    setRubberDuckText('')
  }, [])

  const confirmRubberDuck = useCallback(
    (onConfirm: () => void): boolean => {
      if (rubberDuckText.trim().length < MIN_CHARS) return false
      setShowRubberDuck(false)
      setRubberDuckText('')
      onConfirm()
      return true
    },
    [rubberDuckText],
  )

  return {
    showRubberDuck,
    rubberDuckText,
    setRubberDuckText,
    openRubberDuck,
    closeRubberDuck,
    confirmRubberDuck,
    shouldGate,
    MIN_CHARS,
  }
}
