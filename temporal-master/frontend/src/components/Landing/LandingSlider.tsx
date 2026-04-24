'use client'

/**
 * LandingSlider — Navegación full-page entre secciones
 * Implementación: CSS scroll-snap vertical — todos los slides están en el DOM
 * simultáneamente para que Google los indexe.
 * Flechas neon laterales + dots + teclado + swipe nativo mobile.
 */

import { useState, useCallback, useEffect, useRef } from 'react'
import { motion } from 'framer-motion'

export interface Slide {
  name: string
  content: React.ReactNode
}

interface Props {
  slides: Slide[]
}

export default function LandingSlider({ slides }: Props) {
  const [idx, setIdx]   = useState(0)
  const slideRefs       = useRef<(HTMLDivElement | null)[]>([])

  // Trackear slide activo con IntersectionObserver
  useEffect(() => {
    const observers: IntersectionObserver[] = []
    slideRefs.current.forEach((el, i) => {
      if (!el) return
      const obs = new IntersectionObserver(
        ([entry]) => {
          if (entry.isIntersecting && entry.intersectionRatio >= 0.5) setIdx(i)
        },
        { threshold: 0.5 },
      )
      obs.observe(el)
      observers.push(obs)
    })
    return () => observers.forEach(o => o.disconnect())
  }, [])

  const go = useCallback((next: number) => {
    if (next < 0 || next >= slides.length) return
    slideRefs.current[next]?.scrollIntoView({ behavior: 'smooth' })
  }, [slides.length])

  // Teclado
  useEffect(() => {
    const h = (e: KeyboardEvent) => {
      if (e.key === 'ArrowDown' || e.key === 'ArrowRight') go(idx + 1)
      if (e.key === 'ArrowUp'   || e.key === 'ArrowLeft')  go(idx - 1)
    }
    window.addEventListener('keydown', h)
    return () => window.removeEventListener('keydown', h)
  }, [idx, go])

  return (
    <div
      className="relative w-full font-mono"
      style={{
        height: '100dvh',
        overflowY: 'scroll',
        scrollSnapType: 'y mandatory',
        scrollbarWidth: 'none',
      }}
    >
      {/* Todos los slides en el DOM — clave para indexación por Google */}
      {slides.map((slide, i) => (
        <div
          key={i}
          ref={el => { slideRefs.current[i] = el }}
          style={{
            height: '100dvh',
            scrollSnapAlign: 'start',
            scrollSnapStop: 'always',
            overflow: 'hidden',
            position: 'relative',
          }}
        >
          {slide.content}
        </div>
      ))}

      {/* Flecha — anterior */}
      {idx > 0 && (
        <motion.button
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.2 }}
          onClick={() => go(idx - 1)}
          className="fixed left-2 md:left-4 top-1/2 -translate-y-1/2 z-[200] flex items-center justify-center w-9 h-14 md:w-11 md:h-18 select-none"
          style={{
            border: '1px solid rgba(0,255,65,0.18)',
            background: 'rgba(2,4,2,0.75)',
            backdropFilter: 'blur(4px)',
          }}
          aria-label="Anterior"
          whileHover={{
            borderColor: 'rgba(0,255,65,0.7)',
            boxShadow: '0 0 18px rgba(0,255,65,0.3)',
          }}
        >
          <span
            className="font-mono font-thin select-none"
            style={{ fontSize: '28px', lineHeight: 1, color: 'rgba(0,255,65,0.45)' }}
          >
            ‹
          </span>
        </motion.button>
      )}

      {/* Flecha — siguiente */}
      {idx < slides.length - 1 && (
        <motion.button
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.2 }}
          onClick={() => go(idx + 1)}
          className="fixed right-2 md:right-4 top-1/2 -translate-y-1/2 z-[200] flex items-center justify-center w-9 h-14 md:w-11 md:h-18 select-none"
          style={{
            border: '1px solid rgba(0,255,65,0.18)',
            background: 'rgba(2,4,2,0.75)',
            backdropFilter: 'blur(4px)',
          }}
          aria-label="Siguiente"
          whileHover={{
            borderColor: 'rgba(0,255,65,0.7)',
            boxShadow: '0 0 18px rgba(0,255,65,0.3)',
          }}
        >
          <span
            className="font-mono font-thin select-none"
            style={{ fontSize: '28px', lineHeight: 1, color: 'rgba(0,255,65,0.45)' }}
          >
            ›
          </span>
        </motion.button>
      )}

      {/* Indicador inferior */}
      <div className="fixed bottom-4 left-0 right-0 z-[200] flex flex-col items-center gap-2 pointer-events-none">
        <span
          className="text-[7px] tracking-[0.55em] uppercase"
          style={{ color: 'rgba(0,255,65,0.22)' }}
        >
          {String(idx + 1).padStart(2, '0')} · {slides[idx].name}
        </span>

        <div className="flex items-center gap-1.5 pointer-events-auto">
          {slides.map((_, i) => (
            <button
              key={i}
              onClick={() => go(i)}
              className="block transition-all duration-300"
              aria-label={`Ir a sección ${i + 1}`}
              style={{
                width:     i === idx ? '18px' : '4px',
                height:    '3px',
                background: i === idx ? '#00FF41' : 'rgba(0,255,65,0.14)',
                boxShadow:  i === idx ? '0 0 7px rgba(0,255,65,0.55)' : 'none',
              }}
            />
          ))}
        </div>
      </div>
    </div>
  )
}
