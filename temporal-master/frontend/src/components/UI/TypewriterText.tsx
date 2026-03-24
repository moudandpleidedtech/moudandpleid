'use client'

/**
 * TypewriterText.tsx — Efecto máquina de escribir · DAKI EdTech
 * ──────────────────────────────────────────────────────────────
 * SSR: renderiza el texto completo (sin efecto) para evitar hydration
 * mismatch y para que los motores de búsqueda indexen el contenido.
 * Cliente: resetea a '' en useEffect y escribe letra a letra.
 *
 * Cursor _: sólido mientras escribe, blink step-end al terminar.
 */

import { useState, useEffect } from 'react'

interface TypewriterTextProps {
  text:        string
  delayMs?:    number   // ms por carácter  (default: 55)
  startDelay?: number   // ms antes del primer carácter (default: 200)
}

export default function TypewriterText({
  text,
  delayMs    = 55,
  startDelay = 200,
}: TypewriterTextProps) {
  // SSR initial state = texto completo (sin efecto, pero legible e indexable)
  const [displayed, setDisplayed] = useState(text)
  const [isDone,    setIsDone]    = useState(true)
  const [mounted,   setMounted]   = useState(false)

  // Paso 1: marcar hydration completa
  useEffect(() => { setMounted(true) }, [])

  // Paso 2: arrancar typewriter solo en cliente, DESPUÉS de hydration
  useEffect(() => {
    if (!mounted) return

    // Reset y empieza desde cero
    setDisplayed('')
    setIsDone(false)

    let charIndex = 0
    let typeTimer: ReturnType<typeof setInterval>

    const startTimer = setTimeout(() => {
      typeTimer = setInterval(() => {
        charIndex++
        setDisplayed(text.slice(0, charIndex))
        if (charIndex >= text.length) {
          setIsDone(true)
          clearInterval(typeTimer)
        }
      }, delayMs)
    }, startDelay)

    return () => {
      clearTimeout(startTimer)
      clearInterval(typeTimer)
    }
  }, [mounted, text, delayMs, startDelay])

  return (
    <>
      <style>{`
        @keyframes tw-cursor-blink {
          0%, 100% { opacity: 1; }
          50%      { opacity: 0; }
        }
        .tw-cursor-blink { animation: tw-cursor-blink 1s step-end infinite; }
      `}</style>
      <span>
        {displayed}
        <span
          aria-hidden="true"
          className={`inline-block ml-px ${isDone && mounted ? 'tw-cursor-blink' : 'opacity-100'}`}
        >
          _
        </span>
      </span>
    </>
  )
}
