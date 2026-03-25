'use client'

import { useEffect, useRef, useState } from 'react'
import { useRouter } from 'next/navigation'
import { motion } from 'framer-motion'
import { useUserStore } from '@/store/userStore'
import BitacoraModal, { countNewArchives } from '@/components/Game/BitacoraModal'
import HubAudio from '@/components/UI/HubAudio'
import DakiChatTerminal from '@/components/Hub/DakiChatTerminal'
import RadarMaestriaModal from '@/components/Hub/RadarMaestriaModal'
import ArchivoFallasModal from '@/components/Hub/ArchivoFallasModal'
import MobileGate from '@/components/UI/MobileGate'
import AlphaAccessModal from '@/components/UI/AlphaAccessModal'
import BossWarningBanner from '@/components/UI/BossWarningBanner'
import IncursionSelector from '@/components/Hub/IncursionSelector'

// ─── Frases de DAKI ───────────────────────────────────────────────────────────

const DAKI_QUOTES = [
  'Alineación neuronal completada. El Nexo ha reforzado sus protocolos. Necesitaremos bucles más eficientes, Operador.',
  'Recuerda: un nodo sin condicionales es un nodo ciego. Usa if/else para escanear la Matriz Neuronal.',
  'He interceptado pulsos de los Syntax Swarms. Su capa sináptica es vulnerable a ataques de área — for loops.',
  'La sintaxis es tu señal neural. Un error de indentación colapsa el canal. Precisión absoluta, Operador.',
]

// ─── Typewriter ────────────────────────────────────────────────────────────────

function useTypewriter(text: string, speed = 22, startDelay = 600) {
  const [displayed, setDisplayed] = useState('')
  const [done, setDone] = useState(false)
  useEffect(() => {
    setDisplayed(''); setDone(false)
    let i = 0
    const start = setTimeout(() => {
      const iv = setInterval(() => {
        i++; setDisplayed(text.slice(0, i))
        if (i >= text.length) { clearInterval(iv); setDone(true) }
      }, speed)
      return () => clearInterval(iv)
    }, startDelay)
    return () => clearTimeout(start)
  }, [text, speed, startDelay])
  return { displayed, done }
}

// ─── Núcleo de DAKI ────────────────────────────────────────────────────────────

function AdriCore() {
  return (
    <div className="relative flex items-center justify-center w-44 h-44 mx-auto">

      {/* Halo de energía */}
      <motion.div
        className="absolute inset-0 rounded-full"
        style={{ background: 'radial-gradient(circle, rgba(0,255,65,0.1) 0%, transparent 70%)' }}
        animate={{ scale: [1, 1.2, 1], opacity: [0.5, 1, 0.5] }}
        transition={{ duration: 3, repeat: Infinity, ease: 'easeInOut' }}
      />

      {/* Anillo exterior — rota */}
      <motion.div
        className="absolute inset-3 rounded-full border border-[#00FF41]/15"
        animate={{ rotate: 360 }}
        transition={{ duration: 20, repeat: Infinity, ease: 'linear' }}
      />

      {/* Anillo medio — contra-rota */}
      <motion.div
        className="absolute inset-7 rounded-full border border-[#00FF41]/25"
        animate={{ rotate: -360 }}
        transition={{ duration: 14, repeat: Infinity, ease: 'linear' }}
      />

      {/* Núcleo pulsante */}
      <motion.div
        className="w-20 h-20 rounded-full flex items-center justify-center"
        style={{
          background: 'radial-gradient(circle at 38% 38%, rgba(0,255,65,0.18), rgba(0,10,5,0.9))',
          border: '1.5px solid rgba(0,255,65,0.6)',
        }}
        animate={{
          boxShadow: [
            '0 0 20px rgba(0,255,65,0.4), 0 0 40px rgba(0,255,65,0.15)',
            '0 0 40px rgba(0,255,65,0.7), 0 0 80px rgba(0,255,65,0.3)',
            '0 0 20px rgba(0,255,65,0.4), 0 0 40px rgba(0,255,65,0.15)',
          ],
          scale: [1, 1.05, 1],
        }}
        transition={{ duration: 2.8, repeat: Infinity, ease: 'easeInOut' }}
      >
        <motion.span
          className="text-3xl select-none"
          style={{ color: '#00FF41', textShadow: '0 0 16px #00FF41, 0 0 32px rgba(0,255,65,0.6)' }}
          animate={{ opacity: [0.7, 1, 0.7] }}
          transition={{ duration: 2.8, repeat: Infinity }}
        >
          ◈
        </motion.span>
      </motion.div>

      {/* Partículas orbitantes */}
      {[0, 72, 144, 216, 288].map((deg, i) => (
        <motion.div
          key={i}
          className="absolute w-1.5 h-1.5 rounded-full bg-[#00FF41]"
          style={{
            top: `${50 + 44 * Math.sin((deg * Math.PI) / 180)}%`,
            left: `${50 + 44 * Math.cos((deg * Math.PI) / 180)}%`,
            transform: 'translate(-50%,-50%)',
          }}
          animate={{ opacity: [0.2, 0.9, 0.2], scale: [0.6, 1.3, 0.6] }}
          transition={{ duration: 2.5, repeat: Infinity, delay: i * 0.5, ease: 'easeInOut' }}
        />
      ))}
    </div>
  )
}

// ─── Botón táctico ─────────────────────────────────────────────────────────────

function TacticButton({
  onClick, label, sublabel, icon, primary = false, color = '#00FF41',
}: {
  onClick: () => void
  label: string
  sublabel: string
  icon: string
  primary?: boolean
  color?: string
}) {
  const hex = color
  return (
    <motion.button
      onClick={onClick}
      className="w-full text-left px-5 py-4 border font-mono transition-all duration-150 group relative overflow-hidden cursor-pointer z-10"
      style={primary
        ? { borderColor: `${hex}80`, background: `${hex}10` }
        : { borderColor: `${hex}33`, background: 'transparent' }
      }
      whileHover={{ x: 3 }}
      whileTap={{ scale: 0.98 }}
      onMouseEnter={e => {
        const el = e.currentTarget
        el.style.background = `${hex}20`
        el.style.borderColor = `${hex}b3`
        el.style.boxShadow = `0 0 20px ${hex}26`
      }}
      onMouseLeave={e => {
        const el = e.currentTarget
        el.style.background = primary ? `${hex}10` : 'transparent'
        el.style.borderColor = primary ? `${hex}80` : `${hex}33`
        el.style.boxShadow = 'none'
      }}
    >
      <div className="flex items-center justify-between gap-4">
        <div className="flex flex-col gap-0.5 min-w-0">
          <span
            className="text-sm font-black tracking-widest uppercase"
            style={{ color: hex, ...(primary ? { textShadow: `0 0 8px ${hex}99` } : {}) }}
          >
            {label}
          </span>
          <span className="text-[10px] tracking-wider truncate" style={{ color: `${hex}66` }}>
            {sublabel}
          </span>
        </div>
        <motion.span
          className="text-xl shrink-0"
          style={{ color: `${hex}99` }}
          animate={{ x: [0, 5, 0] }}
          transition={{ duration: 1.8, repeat: Infinity, ease: 'easeInOut' }}
        >
          {icon}
        </motion.span>
      </div>
    </motion.button>
  )
}

// ─── Página Hub ────────────────────────────────────────────────────────────────

export default function HubPage() {
  const router = useRouter()
  const {
    userId, username, level, totalXp, streakDays, badges,
    subscriptionStatus, isPaid, role,
    clearUser, setSubscription, setIsPaid,
  } = useUserStore()

  const handleLogout = () => {
    clearUser()
    document.cookie = 'enigma_user=; path=/; max-age=0; SameSite=Lax'
    router.push('/')
  }
  const [isBitacoraOpen,     setIsBitacoraOpen]     = useState(false)
  const [completedOrders,    setCompletedOrders]    = useState<number[]>([])
  const [bgmFadeOut,         setBgmFadeOut]         = useState(false)
  const [showReenganche,     setShowReenganche]     = useState(false)
  const [showAlphaModal,     setShowAlphaModal]     = useState(false)
  const [dakiOpeningMessage, setDakiOpeningMessage] = useState('')
  const [, setSessionId]                            = useState<string | null>(null)
  const sessionOpenedRef                            = useRef(false)
  const [checkoutLoading,   setCheckoutLoading]    = useState(false)
  const [showRadar,          setShowRadar]          = useState(false)
  const [showFallas,         setShowFallas]         = useState(false)

  // ── XP progress hacia próximo nivel ────────────────────────────────────────
  // Fórmula: level = floor(0.1 * sqrt(XP)) + 1  →  XP en nivel N = ((N-1)*10)²
  const xpAtCurrentLevel = Math.pow((level - 1) * 10, 2)
  const xpAtNextLevel    = Math.pow(level * 10, 2)
  const xpProgress = xpAtNextLevel > xpAtCurrentLevel
    ? Math.min((totalXp - xpAtCurrentLevel) / (xpAtNextLevel - xpAtCurrentLevel), 1)
    : 1
  const xpToNext = Math.max(0, xpAtNextLevel - totalXp)

  const navigateWithFade = (path: string) => {
    setBgmFadeOut(true)
    setTimeout(() => router.push(path), 580)
  }

  // ── Reenganche — detecta inactividad > 24h ─────────────────────────────────
  useEffect(() => {
    const LAST_VISIT_KEY = 'daki_last_hub_visit'
    const now = Date.now()
    const last = parseInt(localStorage.getItem(LAST_VISIT_KEY) ?? '0', 10)
    if (last && now - last > 24 * 60 * 60 * 1000) {
      setTimeout(() => setShowReenganche(true), 1800)
    }
    localStorage.setItem(LAST_VISIT_KEY, String(now))
  }, [])

  // ── Apertura de sesión DAKI — opening message personalizado ───────────────
  useEffect(() => {
    if (!userId || sessionOpenedRef.current) return
    sessionOpenedRef.current = true
    const token = typeof window !== 'undefined' ? localStorage.getItem('daki_token') : null
    if (!token) return
    const API_BASE_LOCAL = process.env.NEXT_PUBLIC_API_URL ?? ''
    fetch(`${API_BASE_LOCAL}/api/v1/session/open`, {
      method:  'POST',
      headers: {
        'Content-Type':  'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({
        operator_level: level,
        streak_days:    streakDays,
        callsign:       username,
        hour:           new Date().getHours(),
      }),
    })
      .then(r => r.ok ? r.json() : null)
      .then((data: { session_id: string; opening_message: string; weak_concept: string | null } | null) => {
        if (data?.session_id) {
          setSessionId(data.session_id)
          if (data.opening_message) setDakiOpeningMessage(data.opening_message)
        }
      })
      .catch(() => {})
  }, [userId]) // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    if (!userId) { router.replace('/'); return }
    // Fetch completed missions to drive Bitácora unlock + ping
    const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? ''
    fetch(`${API_BASE}/api/v1/challenges?user_id=${userId}`)
      .then(r => r.ok ? r.json() : [])
      .then((data: { level_order: number | null; completed: boolean }[]) => {
        const orders = data
          .filter(m => m.completed && m.level_order != null)
          .map(m => m.level_order as number)
        setCompletedOrders(orders)
      })
      .catch(() => {})
  }, [userId, router])

  const newArchiveCount = countNewArchives(completedOrders)

  // ── Retorno desde Stripe Checkout exitoso ───────────────────────────────────
  useEffect(() => {
    if (typeof window === 'undefined') return
    const params = new URLSearchParams(window.location.search)
    if (params.get('checkout') === 'success') {
      // Actualización optimista: el webhook de Stripe confirma async,
      // pero Stripe solo genera este redirect tras pago confirmado.
      setSubscription('ACTIVE', null)
      setIsPaid(true)
      window.history.replaceState({}, '', '/hub')
    }
  }, []) // eslint-disable-line react-hooks/exhaustive-deps

  // ── Redirección a Stripe Checkout ───────────────────────────────────────────
  const handleStripeCheckout = async () => {
    if (checkoutLoading) return
    setCheckoutLoading(true)
    const token = typeof window !== 'undefined' ? localStorage.getItem('daki_token') : null
    if (!token) { setCheckoutLoading(false); return }
    const API_BASE_LOCAL = process.env.NEXT_PUBLIC_API_URL ?? ''
    try {
      const res = await fetch(`${API_BASE_LOCAL}/api/v1/payments/create-checkout-session`, {
        method:  'POST',
        headers: { 'Authorization': `Bearer ${token}` },
      })
      if (!res.ok) throw new Error('checkout_failed')
      const data = await res.json() as { checkout_url: string }
      window.location.href = data.checkout_url
    } catch {
      setCheckoutLoading(false)
    }
  }

  return (
    <MobileGate>
    <div
      className="h-screen flex flex-col font-mono text-[#00FF41] overflow-hidden relative"
      style={{ background: 'radial-gradient(circle at 50% 45%, #001a0d 0%, #000000 65%)' }}
    >
      {/* ── Scanlines CSS ── */}
      <div
        className="fixed inset-0 pointer-events-none z-10"
        style={{
          backgroundImage: 'repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.08) 2px, rgba(0,0,0,0.08) 4px)',
        }}
      />
      {/* Viñeta */}
      <div
        className="fixed inset-0 pointer-events-none z-10"
        style={{ background: 'radial-gradient(ellipse at center, transparent 40%, rgba(0,0,0,0.8) 100%)' }}
      />

      {/* BGM ambiental del Hub */}
      <HubAudio fadeOut={bgmFadeOut} />

      {/* Bitácora — Códice de Infiltración */}
      <BitacoraModal isOpen={isBitacoraOpen} onClose={() => setIsBitacoraOpen(false)} userId={userId ?? ''} completedOrders={completedOrders} />

      {/* Intel Modals */}
      {showRadar  && <RadarMaestriaModal userId={userId ?? ''} onClose={() => setShowRadar(false)} />}
      {showFallas && <ArchivoFallasModal userId={userId ?? ''} onClose={() => setShowFallas(false)} />}

      {/* ── Header ── */}
      <header className="relative z-20 shrink-0 flex items-center justify-between px-6 py-2.5 border-b border-[#00FF41]/12 bg-black/40 backdrop-blur-sm">
        <div className="flex items-center gap-4">
          <span className="font-black tracking-widest text-sm" style={{ textShadow: '0 0 8px #00FF41' }}>
            PYTHON QUEST
          </span>
          <span className="text-[8px] tracking-[0.5em] text-[#00FF41]/25 hidden sm:block">
            {'// CENTRO DE MANDO ACTIVO'}
          </span>
        </div>
        <div className="flex items-center gap-5 text-xs text-[#00FF41]/45">
          <span className="text-[#00FF41]/30 hidden sm:block">{username}</span>
          <span>RANGO <strong className="text-[#00FF41]">{level}</strong></span>
          <span>XP <strong className="text-[#00FF41]">{totalXp.toLocaleString()}</strong></span>
          {streakDays > 0 && <span>🔥 <strong className="text-[#00FF41]">{streakDays}d</strong></span>}
          <button
            onClick={handleLogout}
            className="ml-4 text-red-500 hover:text-red-400 hover:bg-red-950/30 border border-red-800 px-3 py-1 text-xs font-mono tracking-widest cursor-pointer transition-all"
          >
            [ ABORTAR CONEXIÓN ]
          </button>
        </div>
      </header>

      {/* ── Boss Warning Banner ── */}
      <BossWarningBanner level={level} />

      {/* ── Contenido principal ── */}
      <main className="relative z-20 flex-1 flex overflow-hidden">

        {/* ══════════════════════════════════════════════
            PANEL IZQUIERDO — DAKI el Simbionte
        ══════════════════════════════════════════════ */}
        <div className="flex-1 flex flex-col items-center justify-center px-8 py-6 border-r border-[#00FF41]/8">

          {/* Etiqueta superior */}
          <motion.div
            className="text-[8px] tracking-[0.6em] text-[#00FF41]/20 mb-6 text-center"
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.2 }}
          >
            SIMBIONTE // UNIDAD DAKI // CONEXIÓN ACTIVA
          </motion.div>

          {/* Núcleo de DAKI */}
          <motion.div
            initial={{ opacity: 0, scale: 0.7 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.7, ease: [0.16, 1, 0.3, 1] }}
          >
            <AdriCore />
          </motion.div>

          {/* Nombre */}
          <motion.div
            className="mt-3 mb-5 text-center"
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.5 }}
          >
            <span
              className="text-xs font-black tracking-[0.5em] text-[#00FF41]"
              style={{ textShadow: '0 0 10px rgba(0,255,65,0.5)' }}
            >
              D A K I
            </span>
            <p className="text-[8px] tracking-[0.4em] text-[#00FF41]/30 mt-0.5">IA SIMBIONTE // v2.7.1</p>
          </motion.div>

          {/* Terminal de chat con DAKI */}
          <motion.div
            className="w-full max-w-sm h-52"
            initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6, duration: 0.4 }}
          >
            <DakiChatTerminal userId={userId ?? ''} openingMessage={dakiOpeningMessage || undefined} />
          </motion.div>

        </div>

        {/* ══════════════════════════════════════════════
            PANEL DERECHO — Navegación Táctica
        ══════════════════════════════════════════════ */}
        <motion.div
          className="w-80 shrink-0 flex flex-col justify-center gap-5 px-8 py-8"
          initial={{ opacity: 0, x: 24 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.4, duration: 0.45 }}
        >
          {/* Label */}
          <div className="mb-2">
            <p className="text-[8px] tracking-[0.6em] text-[#00FF41]/20 mb-1">
              NAVEGACIÓN TÁCTICA
            </p>
            <div className="h-px bg-[#00FF41]/10 w-full" />
          </div>

          {/* ── XP Progress Bar ── */}
          <motion.div
            className="border border-[#00FF41]/10 px-4 py-3"
            initial={{ opacity: 0, x: 16 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.44 }}
          >
            <div className="flex items-center justify-between mb-2">
              <div>
                <span className="text-[8px] tracking-[0.4em] text-[#00FF41]/30 uppercase">Nivel</span>
                <span className="text-sm font-black text-[#00FF41] ml-2">{level}</span>
              </div>
              <div className="text-right">
                <span className="text-[8px] text-[#00FF41]/25 tracking-wider">{xpToNext.toLocaleString()} XP para N.{level + 1}</span>
              </div>
            </div>
            <div className="h-1 bg-[#00FF41]/8 w-full overflow-hidden">
              <motion.div
                className="h-full bg-[#00FF41]"
                initial={{ width: 0 }}
                animate={{ width: `${xpProgress * 100}%` }}
                transition={{ delay: 0.9, duration: 0.8, ease: 'easeOut' }}
                style={{ boxShadow: '0 0 8px rgba(0,255,65,0.6)' }}
              />
            </div>
            <div className="flex justify-between mt-1.5">
              <span className="text-[7px] text-[#00FF41]/20 tracking-widest">{totalXp.toLocaleString()} XP</span>
              {streakDays > 0 && (
                <span className="text-[7px] text-[#FFB800]/60 tracking-widest">🔥 {streakDays}d racha</span>
              )}
            </div>
          </motion.div>

          {/* ── Tarjeta de misión activa ── */}
          <motion.div
            className="border border-[#00FF41]/25 bg-[#00FF41]/3 px-4 py-4"
            initial={{ opacity: 0, x: 16 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.48 }}
            style={{ boxShadow: '0 0 20px rgba(0,255,65,0.05)' }}
          >
            <div className="flex items-center gap-2 mb-3">
              <span className="w-1.5 h-1.5 rounded-full bg-[#00FF41] animate-pulse" />
              <span className="text-[8px] tracking-[0.5em] text-[#00FF41]/40 uppercase">MISIÓN ACTIVA</span>
            </div>
            <p className="text-[10px] font-bold tracking-[0.25em] text-[#00FF41] uppercase mb-1">
              OPERACIÓN ALFA
            </p>
            <p className="text-[9px] text-[#00FF41]/50 tracking-wide mb-3">
              Lógica y Sintaxis Core
            </p>
            {/* Barra de progreso */}
            <div className="mb-3">
              <div className="flex justify-between text-[8px] text-[#00FF41]/30 tracking-widest mb-1">
                <span>PROGRESO</span>
                <span>{Math.round((completedOrders.length / 10) * 100)}%</span>
              </div>
              <div className="h-1.5 bg-[#00FF41]/8 w-full">
                <motion.div
                  className="h-full bg-[#00FF41]"
                  initial={{ width: 0 }}
                  animate={{ width: `${Math.min((completedOrders.length / 10) * 100, 100)}%` }}
                  transition={{ delay: 0.8, duration: 0.6, ease: 'easeOut' }}
                  style={{ boxShadow: '0 0 8px rgba(0,255,65,0.5)' }}
                />
              </div>
            </div>
            {/* Objetivos */}
            <div className="space-y-1 mb-3">
              <p className="text-[8px] tracking-[0.4em] text-[#00FF41]/20 uppercase mb-1.5">Objetivos</p>
              {['Vulnerar el bucle For', 'Declarar variables seguras'].map((obj, i) => (
                <div key={i} className="flex items-center gap-2">
                  <span className={`w-1 h-1 rounded-full ${completedOrders.length > i ? 'bg-[#00FF41]' : 'bg-[#00FF41]/20'}`} />
                  <span className={`text-[9px] tracking-wide ${completedOrders.length > i ? 'text-[#00FF41]/60 line-through' : 'text-[#00FF41]/35'}`}>
                    {obj}
                  </span>
                </div>
              ))}
            </div>
            <button
              onClick={() => navigateWithFade('/mission/alfa')}
              className="w-full text-center text-[9px] tracking-[0.35em] uppercase border border-[#00FF41]/40 text-[#00FF41]/70 py-2 hover:bg-[#00FF41]/8 hover:border-[#00FF41]/70 transition-all duration-150"
            >
              {'[[ RETOMAR INFILTRACIÓN ]]'}
            </button>
          </motion.div>

          {/* Botones principales */}
          <div className="flex flex-col gap-3">
            <motion.div
              initial={{ opacity: 0, x: 16 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.55 }}
            >
              <TacticButton
                onClick={() => navigateWithFade('/misiones')}
                label="INICIAR AUDITORÍA"
                sublabel="Desplegar dron · Ir a misiones"
                icon="▶"
                primary
              />
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 16 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.68 }}
              className="relative"
            >
              <TacticButton
                onClick={() => setIsBitacoraOpen(true)}
                label="BASE DE DATOS TÁCTICA"
                sublabel="Códice de infiltración · Archivos DAKI"
                icon="◎"
              />
              {/* Ping dot — nuevo archivo desbloqueado */}
              {newArchiveCount > 0 && (
                <span className="absolute -top-1 -right-1 flex h-3 w-3 z-20 pointer-events-none">
                  <motion.span
                    className="absolute inline-flex h-full w-full rounded-full bg-[#00FF41] opacity-75"
                    animate={{ scale: [1, 1.8, 1], opacity: [0.75, 0, 0.75] }}
                    transition={{ duration: 1.4, repeat: Infinity, ease: 'easeOut' }}
                  />
                  <span className="relative inline-flex rounded-full h-3 w-3 bg-[#00FF41]" />
                </span>
              )}
            </motion.div>
          </div>

          {/* SALA DE CONTRATOS */}
          <motion.div
            initial={{ opacity: 0, x: 16 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.72 }}
          >
            <TacticButton
              onClick={() => navigateWithFade('/contratos')}
              label="SALA DE CONTRATOS"
              sublabel="Proyectos · Revisión DAKI · GitHub"
              icon="⬡"
              color="#FFB800"
            />
          </motion.div>

          {/* ── Intel Operacional ── */}
          <motion.div
            initial={{ opacity: 0, x: 16 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.75 }}
          >
            <p className="text-[8px] tracking-[0.5em] text-[#00FF41]/15 mb-2 uppercase">Intel Operacional</p>
            <div className="grid grid-cols-2 gap-2">
              {[
                { label: 'RADAR', sublabel: 'Maestría por concepto', onClick: () => setShowRadar(true), color: '#00FF41' },
                { label: 'FALLAS', sublabel: 'Archivo de errores', onClick: () => setShowFallas(true), color: '#FF4444' },
              ].map(({ label, sublabel, onClick, color }) => (
                <button
                  key={label}
                  onClick={onClick}
                  className="px-3 py-2.5 border text-left transition-all duration-150 font-mono"
                  style={{ borderColor: `${color}20` }}
                  onMouseEnter={e => {
                    const el = e.currentTarget as HTMLButtonElement
                    el.style.borderColor = `${color}45`
                    el.style.background  = `${color}08`
                  }}
                  onMouseLeave={e => {
                    const el = e.currentTarget as HTMLButtonElement
                    el.style.borderColor = `${color}20`
                    el.style.background  = 'transparent'
                  }}
                >
                  <p className="text-[9px] font-black tracking-[0.3em]" style={{ color: `${color}70` }}>{label}</p>
                  <p className="text-[8px] tracking-wide mt-0.5" style={{ color: `${color}35` }}>{sublabel}</p>
                </button>
              ))}
            </div>
          </motion.div>

          {/* Separador */}
          <div className="h-px bg-[#00FF41]/8 w-full" />

          {/* Mapa de Niebla — Incursiones del Nexo (D021/D022) */}
          <IncursionSelector onNavigate={navigateWithFade} isFounder={role === 'FOUNDER'} />

          {/* ── Pase Alpha — visible solo si no tiene acceso activo ── */}
          {!isPaid && subscriptionStatus === 'INACTIVE' && (
            <motion.div
              initial={{ opacity: 0, x: 16 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.78 }}
            >
              <motion.button
                onClick={() => setShowAlphaModal(true)}
                className="w-full text-left px-5 py-3.5 border font-mono transition-all duration-150 relative overflow-hidden"
                style={{
                  borderColor: 'rgba(0,255,65,0.45)',
                  background:  'rgba(0,255,65,0.06)',
                  boxShadow:   '0 0 16px rgba(0,255,65,0.06)',
                }}
                whileHover={{ x: 3 }}
                whileTap={{ scale: 0.98 }}
                onMouseEnter={e => {
                  e.currentTarget.style.background   = 'rgba(0,255,65,0.12)'
                  e.currentTarget.style.borderColor  = 'rgba(0,255,65,0.75)'
                  e.currentTarget.style.boxShadow    = '0 0 24px rgba(0,255,65,0.14)'
                }}
                onMouseLeave={e => {
                  e.currentTarget.style.background   = 'rgba(0,255,65,0.06)'
                  e.currentTarget.style.borderColor  = 'rgba(0,255,65,0.45)'
                  e.currentTarget.style.boxShadow    = '0 0 16px rgba(0,255,65,0.06)'
                }}
              >
                {/* Pulso superior */}
                <motion.div
                  className="absolute top-0 left-0 right-0 h-px"
                  style={{ background: 'linear-gradient(90deg,transparent,rgba(0,255,65,0.6),transparent)' }}
                  animate={{ opacity: [0.3, 1, 0.3] }}
                  transition={{ duration: 2, repeat: Infinity }}
                />
                <div className="flex items-center justify-between gap-3">
                  <div className="flex flex-col gap-0.5">
                    <span
                      className="text-sm font-black tracking-widest uppercase"
                      style={{ color: '#00FF41', textShadow: '0 0 8px rgba(0,255,65,0.6)' }}
                    >
                      ACTIVAR PASE ALPHA
                    </span>
                    <span className="text-[10px] tracking-wider" style={{ color: 'rgba(0,255,65,0.50)' }}>
                      Canjea tu código VANG · 30 días de acceso
                    </span>
                  </div>
                  <motion.span
                    className="text-xl shrink-0"
                    style={{ color: 'rgba(0,255,65,0.70)' }}
                    animate={{ x: [0, 5, 0] }}
                    transition={{ duration: 1.6, repeat: Infinity, ease: 'easeInOut' }}
                  >
                    🔑
                  </motion.span>
                </div>
              </motion.button>
            </motion.div>
          )}

          {/* ── Suscripción Stripe — visible si no tiene acceso activo ── */}
          {!isPaid && subscriptionStatus !== 'ACTIVE' && (
            <motion.div
              initial={{ opacity: 0, x: 16 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.82 }}
            >
              <motion.button
                onClick={handleStripeCheckout}
                disabled={checkoutLoading}
                className="w-full text-left px-5 py-3.5 border font-mono transition-all duration-150 relative overflow-hidden disabled:opacity-60 disabled:cursor-not-allowed"
                style={{
                  borderColor: 'rgba(255,215,0,0.40)',
                  background:  'rgba(255,215,0,0.05)',
                  boxShadow:   '0 0 16px rgba(255,215,0,0.05)',
                }}
                whileHover={!checkoutLoading ? { x: 3 } : {}}
                whileTap={!checkoutLoading ? { scale: 0.98 } : {}}
                onMouseEnter={e => {
                  if (!checkoutLoading) {
                    e.currentTarget.style.background   = 'rgba(255,215,0,0.10)'
                    e.currentTarget.style.borderColor  = 'rgba(255,215,0,0.70)'
                    e.currentTarget.style.boxShadow    = '0 0 24px rgba(255,215,0,0.12)'
                  }
                }}
                onMouseLeave={e => {
                  e.currentTarget.style.background   = 'rgba(255,215,0,0.05)'
                  e.currentTarget.style.borderColor  = 'rgba(255,215,0,0.40)'
                  e.currentTarget.style.boxShadow    = '0 0 16px rgba(255,215,0,0.05)'
                }}
              >
                {/* Pulso superior */}
                <motion.div
                  className="absolute top-0 left-0 right-0 h-px"
                  style={{ background: 'linear-gradient(90deg,transparent,rgba(255,215,0,0.55),transparent)' }}
                  animate={{ opacity: [0.3, 1, 0.3] }}
                  transition={{ duration: 2.4, repeat: Infinity }}
                />
                <div className="flex items-center justify-between gap-3">
                  <div className="flex flex-col gap-0.5">
                    <span
                      className="text-sm font-black tracking-widest uppercase"
                      style={{ color: 'rgba(255,215,0,0.95)', textShadow: '0 0 8px rgba(255,215,0,0.5)' }}
                    >
                      {checkoutLoading ? 'CONECTANDO...' : 'SUSCRIBIRSE AL NEXO'}
                    </span>
                    <span className="text-[10px] tracking-wider" style={{ color: 'rgba(255,215,0,0.45)' }}>
                      {subscriptionStatus === 'TRIAL'
                        ? 'Convierte tu TRIAL a acceso pleno · $25/mes'
                        : 'Acceso total · $25 USD/mes · Cancela cuando quieras'}
                    </span>
                  </div>
                  <motion.span
                    className="text-xl shrink-0"
                    style={{ color: 'rgba(255,215,0,0.65)' }}
                    animate={checkoutLoading ? { rotate: 360 } : { x: [0, 5, 0] }}
                    transition={checkoutLoading
                      ? { duration: 1, repeat: Infinity, ease: 'linear' }
                      : { duration: 1.6, repeat: Infinity, ease: 'easeInOut' }
                    }
                  >
                    {checkoutLoading ? '◌' : '◈'}
                  </motion.span>
                </div>
              </motion.button>
            </motion.div>
          )}

          {/* Separador */}
          <div className="h-px bg-[#00FF41]/8 w-full" />

          {/* Accesos secundarios */}
          <div className="flex flex-col gap-2">
            <p className="text-[8px] tracking-[0.5em] text-[#00FF41]/15 mb-1">ACCESOS SECUNDARIOS</p>
            {[
              { label: 'LEADERBOARD', path: '/leaderboard', color: '#FF6B6B' },
            ].map(({ label, path, color }) => (
              <button
                key={path}
                onClick={() => navigateWithFade(path)}
                className="text-left px-4 py-2 border transition-all duration-150 text-[10px] tracking-widest font-bold"
                style={{ borderColor: `${color}20`, color: `${color}50` }}
                onMouseEnter={e => {
                  const el = e.currentTarget
                  el.style.borderColor = `${color}50`
                  el.style.color = `${color}90`
                  el.style.background = `${color}08`
                }}
                onMouseLeave={e => {
                  const el = e.currentTarget
                  el.style.borderColor = `${color}20`
                  el.style.color = `${color}50`
                  el.style.background = 'transparent'
                }}
              >
                ↳ {label}
              </button>
            ))}
          </div>

          {/* ── Registro de Conquistas ── */}
          {badges.length > 0 && (
            <motion.div
              className="relative"
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.9 }}
              style={{
                border: '1px solid rgba(0,229,255,0.28)',
                background: 'rgba(0,10,20,0.7)',
                boxShadow: '0 0 24px rgba(0,229,255,0.08), inset 0 0 20px rgba(0,229,255,0.03)',
              }}
            >
              {/* Esquinas decorativas */}
              <span className="absolute top-0 left-0 w-3 h-3 border-t-2 border-l-2 border-cyan-400/60" />
              <span className="absolute top-0 right-0 w-3 h-3 border-t-2 border-r-2 border-cyan-400/60" />
              <span className="absolute bottom-0 left-0 w-3 h-3 border-b-2 border-l-2 border-cyan-400/60" />
              <span className="absolute bottom-0 right-0 w-3 h-3 border-b-2 border-r-2 border-cyan-400/60" />

              <div className="px-5 py-4">
                {/* Header */}
                <div className="flex items-center justify-between mb-3">
                  <p className="text-[9px] tracking-[0.55em] text-cyan-400/50 font-bold">
                    REGISTRO DE CONQUISTAS
                  </p>
                  <span className="text-[8px] tracking-widest text-cyan-400/25">
                    {badges.length}/∞
                  </span>
                </div>

                {/* Lista de medallas */}
                <div className="flex flex-col gap-2">
                  {badges.includes('SYSTEM_KILLER') && (
                    <motion.div
                      className="flex items-center gap-3 px-3 py-2.5"
                      style={{ background: 'rgba(0,229,255,0.06)', border: '1px solid rgba(0,229,255,0.22)' }}
                      animate={{ boxShadow: ['0 0 0px rgba(0,229,255,0)', '0 0 16px rgba(0,229,255,0.18)', '0 0 0px rgba(0,229,255,0)'] }}
                      transition={{ duration: 2.5, repeat: Infinity }}
                    >
                      <motion.span
                        className="text-2xl shrink-0 select-none"
                        style={{ filter: 'drop-shadow(0 0 8px rgba(0,229,255,0.9))' }}
                        animate={{ rotate: [0, 8, -8, 0] }}
                        transition={{ duration: 4, repeat: Infinity, ease: 'easeInOut' }}
                      >
                        ⬡
                      </motion.span>
                      <div className="flex flex-col min-w-0 gap-0.5">
                        <span
                          className="text-xs font-black tracking-[0.25em]"
                          style={{ color: '#00E5FF', textShadow: '0 0 10px rgba(0,229,255,0.6)' }}
                        >
                          SYSTEM_KILLER
                        </span>
                        <span className="text-[8px] tracking-wider text-cyan-400/40 truncate">
                          ARCHITECT OF VOID · LOOP MASTERY
                        </span>
                      </div>
                      <motion.span
                        className="ml-auto text-[8px] tracking-widest text-cyan-400/30 shrink-0"
                        animate={{ opacity: [0.3, 0.8, 0.3] }}
                        transition={{ duration: 2, repeat: Infinity }}
                      >
                        ✦
                      </motion.span>
                    </motion.div>
                  )}
                </div>
              </div>
            </motion.div>
          )}

          {/* Estado del sistema */}
          <div className="mt-auto border border-[#00FF41]/8 px-4 py-3 bg-black/30">
            <p className="text-[7px] tracking-[0.5em] text-[#00FF41]/20 mb-2">ESTADO DEL SISTEMA</p>
            <div className="flex flex-col gap-1.5">
              {[
                { label: 'NÚCLEO ENIGMA', ok: true },
                { label: 'COMPILADOR',    ok: true },
                { label: 'DDA ENGINE',    ok: true },
              ].map(({ label, ok }) => (
                <div key={label} className="flex items-center justify-between">
                  <span className="text-[8px] tracking-wider text-[#00FF41]/20">{label}</span>
                  <div className="flex items-center gap-1.5">
                    <motion.span
                      className={`w-1 h-1 rounded-full ${ok ? 'bg-[#00FF41]' : 'bg-yellow-500'}`}
                      animate={{ opacity: [1, 0.3, 1] }}
                      transition={{ duration: 2, repeat: Infinity, delay: Math.random() * 2 }}
                    />
                    <span className={`text-[7px] tracking-widest ${ok ? 'text-[#00FF41]/35' : 'text-yellow-500/40'}`}>
                      {ok ? 'ONLINE' : 'STANDBY'}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>

        </motion.div>
      </main>

      {/* ── Modal de Alpha Access ────────────────────────────────────────────── */}
      <AlphaAccessModal
        visible={showAlphaModal}
        onClose={() => setShowAlphaModal(false)}
        onGranted={(endDate) => {
          setSubscription('TRIAL', endDate)
          setIsPaid(true)
          setShowAlphaModal(false)
        }}
      />

      {/* ── Modal de Reenganche DAKI ─────────────────────────────────────────── */}
      {showReenganche && (
        <div className="fixed inset-0 z-[200] flex items-end justify-center pb-8 px-4 pointer-events-none">
          <motion.div
            className="pointer-events-auto w-full max-w-md border border-[#00FF41]/25 bg-[#050A05] font-mono overflow-hidden"
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ type: 'spring', stiffness: 260, damping: 24 }}
            style={{ boxShadow: '0 0 40px rgba(0,255,65,0.08)' }}
          >
            <div className="h-px bg-gradient-to-r from-transparent via-[#00FF41]/50 to-transparent" />
            <div className="px-5 py-4 flex items-start gap-4">
              <div className="text-2xl shrink-0 mt-0.5">⚡</div>
              <div className="flex-1">
                <div className="text-[8px] tracking-[0.5em] text-[#00FF41]/30 mb-1.5">DAKI // REACTIVACIÓN</div>
                <p className="text-[11px] text-[#C0C0C0]/70 leading-5">
                  Operador <span className="text-[#00FF41] font-bold">{username}</span>. Tu sector lleva más de 24h sin señal. El Nexo te esperaba — 3 minutos es todo lo que necesita.
                </p>
                <button
                  onClick={() => { setShowReenganche(false); navigateWithFade('/misiones') }}
                  className="mt-3 text-[9px] tracking-[0.4em] border border-[#00FF41]/40 text-[#00FF41] px-4 py-1.5 hover:bg-[#00FF41]/10 transition-colors"
                >
                  [[ REANUDAR PROTOCOLO ]]
                </button>
              </div>
              <button
                onClick={() => setShowReenganche(false)}
                className="shrink-0 text-xs text-[#00FF41]/20 hover:text-[#00FF41]/50 transition-colors"
              >
                ×
              </button>
            </div>
          </motion.div>
        </div>
      )}
    </div>
    </MobileGate>
  )
}
