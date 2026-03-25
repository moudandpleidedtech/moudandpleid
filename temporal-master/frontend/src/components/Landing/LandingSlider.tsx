'use client'

/**
 * LandingSlider — Navegación full-page entre secciones
 * Flechas neon laterales + dots + teclado + swipe mobile
 */

import { useState, useCallback, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

export interface Slide {
  name: string
  content: React.ReactNode
}

interface Props {
  slides: Slide[]
}

export default function LandingSlider({ slides }: Props) {
  const [idx, setIdx]   = useState(0)
  const [dir, setDir]   = useState(1)
  const touchX          = useRef(0)
  const canNav          = useRef(true)

  const go = useCallback((next: number) => {
    if (!canNav.current) return
    if (next < 0 || next >= slides.length) return
    canNav.current = false
    setDir(next > idx ? 1 : -1)
    setIdx(next)
    setTimeout(() => { canNav.current = true }, 600)
  }, [idx, slides.length])

  // Teclado
  useEffect(() => {
    const h = (e: KeyboardEvent) => {
      if (e.key === 'ArrowRight' || e.key === 'ArrowDown') go(idx + 1)
      if (e.key === 'ArrowLeft'  || e.key === 'ArrowUp')   go(idx - 1)
    }
    window.addEventListener('keydown', h)
    return () => window.removeEventListener('keydown', h)
  }, [idx, go])

  const variants = {
    enter:  (d: number) => ({ x: d > 0 ? '100%' : '-100%', opacity: 0 }),
    center:              ({ x: 0, opacity: 1 }),
    exit:   (d: number) => ({ x: d > 0 ? '-100%' : '100%', opacity: 0 }),
  }

  const ArrowBtn = ({ side }: { side: 'left' | 'right' }) => {
    const target = side === 'left' ? idx - 1 : idx + 1
    const visible = side === 'left' ? idx > 0 : idx < slides.length - 1
    if (!visible) return null
    return (
      <motion.button
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        onClick={() => go(target)}
        className={`absolute ${side === 'left' ? 'left-2 md:left-4' : 'right-2 md:right-4'} top-1/2 -translate-y-1/2 z-[200] flex items-center justify-center w-9 h-14 md:w-11 md:h-18 select-none`}
        style={{
          border: '1px solid rgba(0,255,65,0.18)',
          background: 'rgba(2,4,2,0.75)',
          backdropFilter: 'blur(4px)',
        }}
        aria-label={side === 'left' ? 'Anterior' : 'Siguiente'}
        whileHover={{
          borderColor: 'rgba(0,255,65,0.7)',
          boxShadow: '0 0 18px rgba(0,255,65,0.3)',
        }}
      >
        <span
          className="font-mono font-thin select-none"
          style={{
            fontSize: '28px',
            lineHeight: 1,
            color: 'rgba(0,255,65,0.45)',
          }}
        >
          {side === 'left' ? '‹' : '›'}
        </span>
      </motion.button>
    )
  }

  return (
    <div
      className="relative w-full font-mono"
      style={{ height: '100dvh', overflow: 'hidden' }}
      onTouchStart={(e) => { touchX.current = e.touches[0].clientX }}
      onTouchEnd={(e) => {
        const d = touchX.current - e.changedTouches[0].clientX
        if (Math.abs(d) > 55) go(d > 0 ? idx + 1 : idx - 1)
      }}
    >
      {/* Slide activo */}
      <AnimatePresence custom={dir} mode="wait">
        <motion.div
          key={idx}
          custom={dir}
          variants={variants}
          initial="enter"
          animate="center"
          exit="exit"
          transition={{ type: 'tween', ease: [0.22, 1, 0.36, 1], duration: 0.52 }}
          className="absolute inset-0 overflow-y-auto"
          style={{ scrollbarWidth: 'none' }}
        >
          {slides[idx].content}
        </motion.div>
      </AnimatePresence>

      {/* Flechas */}
      <ArrowBtn side="left" />
      <ArrowBtn side="right" />

      {/* Indicador inferior */}
      <div className="absolute bottom-4 left-0 right-0 z-[200] flex flex-col items-center gap-2 pointer-events-none">
        <AnimatePresence mode="wait">
          <motion.span
            key={idx}
            initial={{ opacity: 0, y: 4 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -4 }}
            transition={{ duration: 0.2 }}
            className="text-[7px] tracking-[0.55em] uppercase"
            style={{ color: 'rgba(0,255,65,0.22)' }}
          >
            {String(idx + 1).padStart(2, '0')} · {slides[idx].name}
          </motion.span>
        </AnimatePresence>

        <div className="flex items-center gap-1.5 pointer-events-auto">
          {slides.map((_, i) => (
            <button
              key={i}
              onClick={() => go(i)}
              className="block transition-all duration-300"
              style={{
                width:      i === idx ? '18px' : '4px',
                height:     '3px',
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
