'use client'

/**
 * TypewriterText.tsx — Efecto máquina de escribir · DAKI EdTech
 * ──────────────────────────────────────────────────────────────
 * Escribe el texto carácter a carácter con un intervalo configurable.
 * Cursor _ verde: sólido mientras escribe, parpadeante (step-end) al
 * terminar — simula el cursor de terminal táctico.
 *
 * Uso:
 *   <h2 className="text-xl ... text-[#00FF41]/90 neon-glow">
 *     <TypewriterText text="TÚ ERES LA CORRECCIÓN." />
 *   </h2>
 *
 * Props:
 *   text        — cadena a escribir
 *   delayMs     — ms por carácter          (default: 50)
 *   startDelay  — ms de espera antes de   (default: 500)
 *                 empezar a escribir
 */

import { useState, useEffect } from 'react'

interface TypewriterTextProps {
  text:        string
  delayMs?:    number
  startDelay?: number
}

export default function TypewriterText({
  text,
  delayMs    = 50,
  startDelay = 500,
}: TypewriterTextProps) {
  const [displayed, setDisplayed] = useState('')
  const [isDone,    setIsDone]    = useState(false)

  useEffect(() => {
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
  }, [text, delayMs, startDelay])

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
          className={`inline-block ml-px ${isDone ? 'tw-cursor-blink' : 'opacity-100'}`}
        >
          _
        </span>
      </span>
    </>
  )
}
