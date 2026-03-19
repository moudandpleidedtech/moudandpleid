'use client'

/**
 * useDakiVoice — Hook que activa la voz de DAKI cuando cambia el texto.
 *
 * Uso:
 *   const { speak, cancel, isSpeaking } = useDakiVoice(dakiLevel)
 *   speak("Operador, revisa la sintaxis.")
 *
 * También puede activarse automáticamente al montar:
 *   useDakiVoice(dakiLevel, { text: hint, autoPlay: true })
 */

import { useCallback, useEffect, useRef, useState } from 'react'
import {
  cancelDakiVoice,
  isDakiSpeaking,
  speakDaki,
  type DakiLevel,
} from '@/lib/dakiVoice'

interface UseDakiVoiceOptions {
  /** Si se provee junto con autoPlay=true, se habla al montar el hook. */
  text?: string
  /** Reproduce automáticamente cuando `text` cambia. Default: false. */
  autoPlay?: boolean
  /** Si false, la síntesis nunca se activa (ej. usuario silencia DAKI). Default: true. */
  enabled?: boolean
}

interface UseDakiVoiceReturn {
  /** Reproduce el texto manualmente. */
  speak: (text: string) => void
  /** Detiene la síntesis en curso. */
  cancel: () => void
  /** True mientras DAKI está hablando. */
  isSpeaking: boolean
}

export function useDakiVoice(
  dakiLevel: DakiLevel = 1,
  options: UseDakiVoiceOptions = {},
): UseDakiVoiceReturn {
  const { text, autoPlay = false, enabled = true } = options
  const [isSpeaking, setIsSpeaking] = useState(false)
  const prevTextRef = useRef<string | undefined>(undefined)

  const speak = useCallback(
    (input: string) => {
      if (!enabled) return
      speakDaki(input, dakiLevel, () => setIsSpeaking(false))
      setIsSpeaking(true)
    },
    [dakiLevel, enabled],
  )

  const cancel = useCallback(() => {
    cancelDakiVoice()
    setIsSpeaking(false)
  }, [])

  // Auto-play cuando `text` cambia (y autoPlay está activo)
  useEffect(() => {
    if (!autoPlay || !enabled || !text) return
    if (text === prevTextRef.current) return   // mismo texto, no repetir
    prevTextRef.current = text
    speak(text)
  }, [text, autoPlay, enabled, speak])

  // Cancelar al desmontar el componente
  useEffect(() => {
    return () => {
      if (isDakiSpeaking()) cancelDakiVoice()
    }
  }, [])

  // Actualizar isSpeaking desde el estado real del navegador
  useEffect(() => {
    const interval = setInterval(() => {
      setIsSpeaking(isDakiSpeaking())
    }, 300)
    return () => clearInterval(interval)
  }, [])

  return { speak, cancel, isSpeaking }
}
