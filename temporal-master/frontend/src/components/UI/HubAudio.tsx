'use client'

import { useEffect, useRef, useState } from 'react'
import { motion } from 'framer-motion'

interface Props {
  src?:         string
  fadeOut?:     boolean  // true = fade-out antes de navegar (pasado por el Hub)
  buttonClass?: string   // override de posicionamiento del botón mute (default: hub position)
}

// ─── SVG Icons ────────────────────────────────────────────────────────────────

function IconSpeakerOn() {
  return (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5" />
      <path d="M15.54 8.46a5 5 0 0 1 0 7.07" />
      <path d="M19.07 4.93a10 10 0 0 1 0 14.14" />
    </svg>
  )
}

function IconSpeakerOff() {
  return (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5" />
      <line x1="23" y1="9" x2="17" y2="15" />
      <line x1="17" y1="9" x2="23" y2="15" />
    </svg>
  )
}

// ─── HubAudio ─────────────────────────────────────────────────────────────────

export default function HubAudio({ src = '/sounds/hub-ambient.mp3', fadeOut = false, buttonClass }: Props) {
  const audioRef = useRef<HTMLAudioElement>(null)

  // Estado inicial desde localStorage (hidratación segura)
  const [muted, setMuted]     = useState(false)
  const [playing, setPlaying] = useState(false)
  const [mounted, setMounted] = useState(false)

  // ── Hidratación ──────────────────────────────────────────────────────────────
  useEffect(() => {
    const saved = localStorage.getItem('hub_bgm_muted')
    setMuted(saved === 'true')
    setMounted(true)
  }, [])

  // ── Autoplay al montar (respeta políticas de navegador) ──────────────────────
  useEffect(() => {
    if (!mounted) return
    const audio = audioRef.current
    if (!audio) return
    audio.volume = 0.14
    if (!muted) {
      audio.play()
        .then(() => setPlaying(true))
        .catch(() => setPlaying(false))  // navegador bloqueó autoplay
    }
  }, [mounted])  // solo al montar — muted viene de localStorage

  // ── Fade-out antes de navegar ─────────────────────────────────────────────────
  useEffect(() => {
    if (!fadeOut) return
    const audio = audioRef.current
    if (!audio) return
    const startVol = audio.volume
    const STEPS = 18
    let i = 0
    const iv = setInterval(() => {
      i++
      audio.volume = Math.max(0, startVol * (1 - i / STEPS))
      if (i >= STEPS) { clearInterval(iv); audio.pause() }
    }, 30)  // ~540ms total
    return () => clearInterval(iv)
  }, [fadeOut])

  // ── Toggle mute/play ─────────────────────────────────────────────────────────
  const toggle = () => {
    const audio = audioRef.current
    if (!audio) return

    if (muted || !playing) {
      audio.volume = 0.14
      audio.play()
        .then(() => { setPlaying(true); setMuted(false) })
        .catch(() => {})
      localStorage.setItem('hub_bgm_muted', 'false')
      setMuted(false)
    } else {
      audio.pause()
      setPlaying(false)
      setMuted(true)
      localStorage.setItem('hub_bgm_muted', 'true')
    }
  }

  // No renderizar en SSR para evitar mismatch
  if (!mounted) return null

  return (
    <>
      {/* eslint-disable-next-line jsx-a11y/media-has-caption */}
      <audio ref={audioRef} src={src} loop preload="auto" />

      {/* Botón toggle — esquina superior derecha */}
      <motion.button
        onClick={toggle}
        whileTap={{ scale: 0.85 }}
        title={muted || !playing ? '[ ACTIVAR BGM ]' : '[ SILENCIAR BGM ]'}
        className={`${buttonClass ?? 'fixed top-3 right-[14rem]'} z-50 w-8 h-8 flex items-center justify-center border border-[#00FF41]/18 bg-black/50 backdrop-blur-sm text-[#00FF41]/45 hover:text-[#00FF41]/80 hover:border-[#00FF41]/35 transition-colors`}
        style={{ boxShadow: playing && !muted ? '0 0 8px rgba(0,255,65,0.12)' : 'none' }}
      >
        {muted || !playing ? <IconSpeakerOff /> : <IconSpeakerOn />}
      </motion.button>
    </>
  )
}
