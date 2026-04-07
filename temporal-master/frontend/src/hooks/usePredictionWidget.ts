'use client'
/**
 * usePredictionWidget — F1: Widget de predicción de output (level_order >= 30).
 *
 * El operador escribe su predicción ANTES de ejecutar.
 * Post-ejecución, se compara con el output real y se da feedback.
 *
 * Retorna:
 *   prediction        — valor actual del input de predicción
 *   setPrediction     — setter para el input
 *   predictionResult  — 'correct' | 'wrong' | null (resultado post-run)
 *   evaluatePrediction(actualOutput: string) → 'correct' | 'wrong' | null
 *     Llama internamente, compara y setea predictionResult.
 *   resetPrediction() — limpia estado (al cambiar de challenge)
 */

import { useState, useCallback } from 'react'

type PredictionResult = 'correct' | 'wrong' | null

function normalize(s: string): string {
  return s.replace(/\r\n/g, '\n').trim().toLowerCase().replace(/\s+/g, ' ')
}

export function usePredictionWidget() {
  const [prediction,       setPrediction]       = useState('')
  const [predictionResult, setPredictionResult] = useState<PredictionResult>(null)

  const evaluatePrediction = useCallback(
    (actualOutput: string): PredictionResult => {
      if (!prediction.trim()) return null
      const result = normalize(prediction) === normalize(actualOutput) ? 'correct' : 'wrong'
      setPredictionResult(result)
      return result
    },
    [prediction],
  )

  const resetPrediction = useCallback(() => {
    setPrediction('')
    setPredictionResult(null)
  }, [])

  return {
    prediction,
    setPrediction,
    predictionResult,
    evaluatePrediction,
    resetPrediction,
  }
}
