'use client'

import { useEffect, useRef, useState } from 'react'
import { useRouter } from 'next/navigation'
import { motion, AnimatePresence } from 'framer-motion'
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
import IntelReportModal from '@/components/Hub/IntelReportModal'
import DistincionesPanel from '@/components/Hub/DistincionesPanel'

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

// ─── Glitch CTA ────────────────────────────────────────────────────────────────

function GlitchCTA({ onClick }: { onClick: () => void }) {
  const [flash, setFlash] = useState(false)
  return (
    <motion.button
      onClick={onClick}
      onHoverStart={() => { setFlash(true); setTimeout(() => setFlash(false), 380) }}
      className="relative w-full max-w-xs px-6 py-4 border font-mono overflow-hidden mx-auto block"
      style={{
        borderColor: 'rgba(0,255,65,0.55)',
        background:  'rgba(0,255,65,0.07)',
        boxShadow:   '0 0 24px rgba(0,255,65,0.08)',
      }}
      whileHover={{
        borderColor: 'rgba(0,255,65,0.95)',
        boxShadow:   '0 0 36px rgba(0,255,65,0.22)',
      }}
      whileTap={{ scale: 0.97 }}
    >
      {/* Línea pulso superior */}
      <motion.div
        className="absolute top-0 left-0 right-0 h-[2px]"
        style={{ background: 'linear-gradient(90deg, transparent, #00FF41cc, transparent)' }}
        animate={{ opacity: [0.3, 1, 0.3] }}
        transition={{ duration: 1.8, repeat: Infinity }}
      />
      {/* Flash glitch al hover */}
      <AnimatePresence>
        {flash && (
          <motion.div
            className="absolute inset-0 pointer-events-none"
            style={{ background: 'rgba(0,255,65,0.18)' }}
            initial={{ opacity: 0 }}
            animate={{ opacity: [0, 1, 0.5, 0] }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.35 }}
          />
        )}
      </AnimatePresence>
      <span
        className="relative text-[11px] font-black tracking-[0.4em] uppercase"
        style={{ color: '#00FF41', textShadow: '0 0 10px rgba(0,255,65,0.8)' }}
      >
        [[ CONTINUAR MISIÓN ACTUAL ]]
      </span>
      {/* Línea pulso inferior */}
      <motion.div
        className="absolute bottom-0 left-0 right-0 h-px"
        style={{ background: 'linear-gradient(90deg, transparent, rgba(0,255,65,0.5), transparent)' }}
        animate={{ opacity: [0.2, 0.8, 0.2] }}
        transition={{ duration: 2.2, repeat: Infinity, delay: 0.6 }}
      />
    </motion.button>
  )
}

// ─── Página Hub ────────────────────────────────────────────────────────────────

export default function HubPage() {
  const router = useRouter()
  const {
    _hasHydrated,
    userId, username, level, totalXp, streakDays, badges,
    subscriptionStatus, isPaid, role,
    clearUser, setSubscription, setIsPaid,
  } = useUserStore()

  const handleLogout = () => {
    ;['daki_token', 'daki_user_id', 'daki_callsign', 'daki_level', 'daki_licensed'].forEach(k => localStorage.removeItem(k))
    clearUser()
    document.cookie = 'enigma_user=; path=/; max-age=0; SameSite=Lax'
    router.replace('/login')
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
  const [showIntelReport,    setShowIntelReport]    = useState(false)

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
    if (!_hasHydrated) return
    if (!userId) { router.replace('/login'); return }
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
  }, [_hasHydrated, userId, router])

  const newArchiveCount = countNewArchives(completedOrders)

  // ── Sincronizar subscription_status desde backend al montar ─────────────────
  // Evita que Zustand muestre 'INACTIVE' cuando el usuario ya tiene TRIAL/ACTIVE.
  useEffect(() => {
    if (!userId) return
    const token = typeof window !== 'undefined' ? localStorage.getItem('daki_token') : null
    if (!token) return
    const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? ''
    fetch(`${API_BASE}/api/v1/user/me`, {
      headers: { 'Authorization': `Bearer ${token}` },
    })
      .then(r => r.ok ? r.json() : null)
      .then((data: { subscription_status?: string; trial_end_date?: string | null; role?: string } | null) => {
        if (!data) return
        if (data.subscription_status && data.subscription_status !== 'INACTIVE') {
          setSubscription(data.subscription_status, data.trial_end_date ?? null)
          if (data.subscription_status === 'ACTIVE') setIsPaid(true)
        }
        // Sync FOUNDER role so hasAccess check also covers role-based bypass
        if (data.role === 'FOUNDER') {
          setSubscription(data.subscription_status ?? 'ACTIVE', null)
          setIsPaid(true)
        }
      })
      .catch(() => {})
  }, [userId]) // eslint-disable-line react-hooks/exhaustive-deps

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

      {/* BGM ambiental del Hub (audio manager) */}


      {/* Bitácora — Códice de Infiltración */}
      <BitacoraModal isOpen={isBitacoraOpen} onClose={() => setIsBitacoraOpen(false)} userId={userId ?? ''} completedOrders={completedOrders} />

      {/* Intel Modals */}
      {showRadar  && <RadarMaestriaModal userId={userId ?? ''} onClose={() => setShowRadar(false)} />}
      {showFallas && <ArchivoFallasModal userId={userId ?? ''} onClose={() => setShowFallas(false)} />}
      <IntelReportModal isOpen={showIntelReport} onClose={() => setShowIntelReport(false)} userId={userId ?? ''} />

      {/* ── Header ── */}
      <header className="relative z-20 shrink-0 flex flex-wrap items-center justify-between px-6 py-2.5 border-b border-[#00FF41]/12 bg-black/40 backdrop-blur-sm gap-4">
        <div className="flex items-center gap-4 shrink-0">
          <span className="font-black tracking-widest text-sm" style={{ textShadow: '0 0 8px #00FF41' }}>
            NEXO CENTRAL
          </span>
          <span className="text-[8px] tracking-[0.5em] text-[#00FF41]/25 hidden md:block">
            {'// ECOSISTEMA DE FORMACIONES ACTIVO'}
          </span>
        </div>
        
        {/* Panel de Controles & Rango (CSS Flex con wrapping y gaps fijos) */}
        <div className="flex flex-wrap items-center justify-end gap-3 sm:gap-5 text-xs text-[#00FF41]/45">
          <span className="text-[#00FF41]/30 hidden lg:block whitespace-nowrap">{username}</span>
          <span className="whitespace-nowrap">RANGO <strong className="text-[#00FF41]">{level}</strong></span>
          <span className="whitespace-nowrap">XP <strong className="text-[#00FF41]">{totalXp.toLocaleString()}</strong></span>
          {streakDays > 0 && <span className="whitespace-nowrap">🔥 <strong className="text-[#00FF41]">{streakDays}d</strong></span>}
          
          {/* Componente de Audio (reubicado dentro del flujo flex) */}
          <div className="flex items-center justify-center shrink-0">
            <HubAudio fadeOut={bgmFadeOut} buttonClass="relative" />
          </div>

          <motion.button
            onClick={() => setShowIntelReport(true)}
            className="border px-3 py-1 text-[9px] font-mono tracking-widest cursor-pointer transition-all duration-150 shrink-0"
            style={{ borderColor: 'rgba(255,184,0,0.35)', color: 'rgba(255,184,0,0.65)' }}
            whileHover={{ borderColor: 'rgba(255,184,0,0.70)', color: 'rgba(255,184,0,0.95)' }}
            whileTap={{ scale: 0.96 }}
            title="Reporte de Inteligencia — reportar bug o sugerencia"
          >
            ⚑ INTEL
          </motion.button>
          
          <button
            onClick={handleLogout}
            className="text-red-500 hover:text-red-400 hover:bg-red-950/30 border border-red-800 px-3 py-1 text-xs font-mono tracking-widest cursor-pointer transition-all shrink-0"
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
            PANEL IZQUIERDO — Bienvenida + DAKI
        ══════════════════════════════════════════════ */}
        <div className="w-[300px] shrink-0 flex flex-col items-center justify-center px-6 py-6 border-r border-[#00FF41]/8 gap-0">

          {/* ── WELCOME SECTION ── */}
          <motion.div
            className="w-full max-w-sm mb-7 text-center"
            initial={{ opacity: 0, y: -12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1, duration: 0.5, ease: 'easeOut' }}
          >
            <p className="text-[8px] tracking-[0.7em] text-[#00FF41]/30 mb-2 font-mono">
              BIENVENIDO, OPERADOR
            </p>
            <h2
              className="text-3xl font-black tracking-[0.15em] mb-3 font-mono"
              style={{
                color:      '#00FF41',
                textShadow: '0 0 20px rgba(0,255,65,0.55), 0 0 50px rgba(0,255,65,0.18)',
              }}
            >
              {username?.toUpperCase() ?? '—'}
            </h2>

            {/* Rol / Rango */}
            {role === 'FOUNDER' ? (
              <motion.div
                className="inline-flex items-center gap-2 px-4 py-1.5 border mb-5 mx-auto"
                style={{
                  borderColor: 'rgba(255,199,0,0.40)',
                  background:  'rgba(255,199,0,0.06)',
                  boxShadow:   '0 0 16px rgba(255,199,0,0.08)',
                }}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.35 }}
              >
                <motion.span
                  className="text-sm leading-none"
                  style={{ color: '#FFC700', textShadow: '0 0 10px rgba(255,199,0,0.9)' }}
                  animate={{ opacity: [0.7, 1, 0.7] }}
                  transition={{ duration: 1.8, repeat: Infinity }}
                >
                  ◈
                </motion.span>
                <span
                  className="text-[10px] font-black tracking-[0.5em] font-mono"
                  style={{ color: '#FFC700', textShadow: '0 0 8px rgba(255,199,0,0.5)' }}
                >
                  FOUNDER
                </span>
                <span className="text-[8px] font-mono" style={{ color: 'rgba(255,199,0,0.40)' }}>
                  // ACCESO TOTAL
                </span>
              </motion.div>
            ) : (
              <motion.div
                className="inline-flex items-center gap-2 px-4 py-1.5 border mb-5 mx-auto"
                style={{ borderColor: 'rgba(0,255,65,0.22)', background: 'rgba(0,255,65,0.04)' }}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.35 }}
              >
                <span className="text-[10px] font-black tracking-[0.5em] text-[#00FF41]/70 font-mono">
                  OPERADOR
                </span>
                <span className="text-[8px] text-[#00FF41]/35 font-mono">// NIV. {level}</span>
              </motion.div>
            )}
            {/* Espacio base — sin CTA aquí */}
            <div className="mb-1" />

          </motion.div>

          {/* Divisor */}
          <div className="w-full max-w-sm h-px bg-[#00FF41]/8 mb-6" />

          {/* ── DAKI — compacto ── */}
          <motion.div
            className="text-[7px] tracking-[0.6em] text-[#00FF41]/18 mb-4 text-center font-mono"
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.5 }}
          >
            SIMBIONTE // UNIDAD DAKI // CONEXIÓN ACTIVA
          </motion.div>

          <motion.div
            className="transform scale-75 origin-center mb-1"
            initial={{ opacity: 0, scale: 0.5 }}
            animate={{ opacity: 1, scale: 0.75 }}
            transition={{ duration: 0.7, ease: [0.16, 1, 0.3, 1], delay: 0.3 }}
          >
            <AdriCore />
          </motion.div>

          <motion.div
            className="mb-4 text-center"
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.55 }}
          >
            <span
              className="text-[10px] font-black tracking-[0.5em] text-[#00FF41]"
              style={{ textShadow: '0 0 8px rgba(0,255,65,0.4)' }}
            >
              D A K I
            </span>
            <p className="text-[7px] tracking-[0.4em] text-[#00FF41]/25 mt-0.5 font-mono">IA SIMBIONTE // v2.7.1</p>
          </motion.div>

          <motion.div
            className="w-full max-w-sm h-48"
            initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.65, duration: 0.4 }}
          >
            <DakiChatTerminal userId={userId ?? ''} openingMessage={dakiOpeningMessage || undefined} />
          </motion.div>

        </div>

        {/* ══════════════════════════════════════════════
            PANEL DERECHO — Navegación Táctica
        ══════════════════════════════════════════════ */}
        <motion.div
          className="flex-1 flex flex-col justify-start gap-5 px-10 py-6 overflow-y-auto [&::-webkit-scrollbar]:hidden [-ms-overflow-style:none] [scrollbar-width:none]"
          initial={{ opacity: 0, x: 24 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.4, duration: 0.45 }}
        >
          {/* ── Badge de Rango ── */}
          <motion.div
            className="border px-4 py-3.5 relative overflow-hidden"
            style={{
              borderColor: role === 'FOUNDER' ? 'rgba(255,199,0,0.30)' : 'rgba(0,255,65,0.18)',
              background:  role === 'FOUNDER' ? 'rgba(255,199,0,0.04)' : 'rgba(0,255,65,0.03)',
              boxShadow:   role === 'FOUNDER' ? '0 0 20px rgba(255,199,0,0.06)' : '0 0 16px rgba(0,255,65,0.04)',
            }}
            initial={{ opacity: 0, x: 16 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
          >
            {/* Esquinas decorativas */}
            <span className="absolute top-0 left-0 w-2.5 h-2.5 border-t border-l" style={{ borderColor: role === 'FOUNDER' ? 'rgba(255,199,0,0.5)' : 'rgba(0,255,65,0.3)' }} />
            <span className="absolute top-0 right-0 w-2.5 h-2.5 border-t border-r" style={{ borderColor: role === 'FOUNDER' ? 'rgba(255,199,0,0.5)' : 'rgba(0,255,65,0.3)' }} />
            <span className="absolute bottom-0 left-0 w-2.5 h-2.5 border-b border-l" style={{ borderColor: role === 'FOUNDER' ? 'rgba(255,199,0,0.5)' : 'rgba(0,255,65,0.3)' }} />
            <span className="absolute bottom-0 right-0 w-2.5 h-2.5 border-b border-r" style={{ borderColor: role === 'FOUNDER' ? 'rgba(255,199,0,0.5)' : 'rgba(0,255,65,0.3)' }} />

            <p className="text-[9px] tracking-[0.5em] font-mono mb-3"
              style={{ color: role === 'FOUNDER' ? 'rgba(255,199,0,0.45)' : 'rgba(0,255,65,0.35)' }}>
              RANGO OPERACIONAL
            </p>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <motion.span
                  className="text-3xl leading-none"
                  style={{
                    color:      role === 'FOUNDER' ? '#FFC700' : '#00FF41',
                    textShadow: role === 'FOUNDER' ? '0 0 18px rgba(255,199,0,0.9)' : '0 0 12px rgba(0,255,65,0.7)',
                  }}
                  animate={{ opacity: [0.7, 1, 0.7] }}
                  transition={{ duration: 2.2, repeat: Infinity }}
                >
                  {role === 'FOUNDER' ? '◈' : '◇'}
                </motion.span>
                <div>
                  <p
                    className="text-xl font-black tracking-[0.35em] leading-none font-mono"
                    style={{
                      color:      role === 'FOUNDER' ? '#FFC700' : '#00FF41',
                      textShadow: role === 'FOUNDER' ? '0 0 12px rgba(255,199,0,0.6)' : '0 0 10px rgba(0,255,65,0.5)',
                    }}
                  >
                    {role === 'FOUNDER' ? 'FOUNDER' : 'OPERADOR'}
                  </p>
                  <p className="text-[10px] tracking-[0.3em] mt-1 font-mono"
                    style={{ color: role === 'FOUNDER' ? 'rgba(255,199,0,0.55)' : 'rgba(0,255,65,0.45)' }}>
                    {role === 'FOUNDER' ? 'ACCESO ILIMITADO' : `NIVEL ${level}`}
                  </p>
                </div>
              </div>
              <div className="text-right">
                <p className="text-lg font-black font-mono" style={{ color: role === 'FOUNDER' ? 'rgba(255,199,0,0.85)' : 'rgba(0,255,65,0.75)' }}>
                  {totalXp.toLocaleString()}
                </p>
                <p className="text-[9px] tracking-[0.3em] font-mono" style={{ color: role === 'FOUNDER' ? 'rgba(255,199,0,0.35)' : 'rgba(0,255,65,0.30)' }}>
                  XP TOTAL
                </p>
                {streakDays > 0 && (
                  <p className="text-[7px] text-[#FFB800]/60 tracking-widest mt-0.5">🔥 {streakDays}d</p>
                )}
              </div>
            </div>
            {/* XP bar */}
            <div className="mt-3 h-0.5 w-full overflow-hidden" style={{ background: role === 'FOUNDER' ? 'rgba(255,199,0,0.08)' : 'rgba(0,255,65,0.08)' }}>
              <motion.div
                className="h-full"
                initial={{ width: 0 }}
                animate={{ width: `${xpProgress * 100}%` }}
                transition={{ delay: 1, duration: 0.9, ease: 'easeOut' }}
                style={{
                  background: role === 'FOUNDER' ? '#FFC700' : '#00FF41',
                  boxShadow:  role === 'FOUNDER' ? '0 0 8px rgba(255,199,0,0.7)' : '0 0 8px rgba(0,255,65,0.6)',
                }}
              />
            </div>
            <div className="flex justify-between mt-1">
              <span className="text-[7px] font-mono tracking-widest" style={{ color: role === 'FOUNDER' ? 'rgba(255,199,0,0.25)' : 'rgba(0,255,65,0.20)' }}>
                NIV. {level}
              </span>
              <span className="text-[7px] font-mono tracking-widest" style={{ color: role === 'FOUNDER' ? 'rgba(255,199,0,0.25)' : 'rgba(0,255,65,0.20)' }}>
                {xpToNext.toLocaleString()} XP → N.{level + 1}
              </span>
            </div>
          </motion.div>

          {/* ── CTA Primario único ── */}
          <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.25 }}
          >
            <motion.button
              onClick={() => {
                const access = isPaid || subscriptionStatus === 'TRIAL' || subscriptionStatus === 'ACTIVE' || role === 'FOUNDER'
                if (!access) { setShowAlphaModal(true); return }
                navigateWithFade('/misiones')
              }}
              className="w-full py-4 font-black text-base tracking-[0.2em] uppercase font-mono relative overflow-hidden focus:outline-none focus-visible:ring-2 focus-visible:ring-[#00FF41]/50"
              style={{
                background:  'rgba(0,255,65,0.10)',
                border:      '2px solid rgba(0,255,65,0.65)',
                color:       '#00FF41',
                textShadow:  '0 0 12px rgba(0,255,65,0.8)',
                boxShadow:   '0 0 32px rgba(0,255,65,0.12)',
              }}
              whileHover={{
                background:  'rgba(0,255,65,0.18)',
                borderColor: 'rgba(0,255,65,0.95)',
                boxShadow:   '0 0 40px rgba(0,255,65,0.25)',
              }}
              whileTap={{ scale: 0.98 }}
            >
              <motion.div
                className="absolute top-0 left-0 right-0 h-[2px]"
                style={{ background: 'linear-gradient(90deg,transparent,#00FF41,transparent)' }}
                animate={{ opacity: [0.4, 1, 0.4] }}
                transition={{ duration: 1.8, repeat: Infinity }}
              />
              <span className="flex items-center justify-center gap-3">
                <span>▶</span>
                <span>CONTINUAR MISIÓN</span>
                <span className="text-[10px] text-[#00FF41]/50 font-normal tracking-widest">
                  {Math.min(Math.round((completedOrders.length / 10) * 100), 100)}% completado
                </span>
              </span>
              <motion.div
                className="absolute bottom-0 left-0 right-0 h-px"
                style={{ background: 'linear-gradient(90deg,transparent,rgba(0,255,65,0.4),transparent)' }}
                animate={{ opacity: [0.2, 0.8, 0.2] }}
                transition={{ duration: 2.2, repeat: Infinity, delay: 0.5 }}
              />
            </motion.button>
          </motion.div>

          {/* ── Formaciones — Tabs + Grid ── */}
          <motion.div
            initial={{ opacity: 0, x: 16 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
          >
            <IncursionSelector
              onNavigate={navigateWithFade}
              isFounder={role === 'FOUNDER'}
              hasAccess={isPaid || subscriptionStatus === 'TRIAL' || subscriptionStatus === 'ACTIVE' || role === 'FOUNDER'}
              onAccessDenied={() => setShowAlphaModal(true)}
            />
          </motion.div>

          {/* Separador */}
          <div className="h-px bg-[#00FF41]/8 w-full" />

          {/* ── Accesos Rápidos — barra compacta 3×2 ── */}
          <motion.div
            initial={{ opacity: 0, x: 16 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.45 }}
          >
            <p className="text-[8px] tracking-[0.5em] text-[#00FF41]/18 mb-3 font-mono uppercase">Accesos Rápidos</p>
            <div className="grid grid-cols-3 gap-2">
              {[
                {
                  label: 'BITÁCORA', icon: '◎', color: '#00FF41',
                  onClick: () => setIsBitacoraOpen(true),
                  ping: newArchiveCount > 0,
                },
                {
                  label: 'CONTRATOS', icon: '⬡', color: '#FFB800',
                  onClick: () => navigateWithFade('/contratos'),
                  ping: false,
                },
                {
                  label: 'LEADERBOARD', icon: '▲', color: '#FF6B6B',
                  onClick: () => navigateWithFade('/leaderboard'),
                  ping: false,
                },
                {
                  label: 'RADAR', icon: '◉', color: '#00FF41',
                  onClick: () => setShowRadar(true),
                  ping: false,
                },
                {
                  label: 'FALLAS', icon: '⚠', color: '#FF4444',
                  onClick: () => setShowFallas(true),
                  ping: false,
                },
                {
                  label: 'INTEL', icon: '⚑', color: '#FFB800',
                  onClick: () => setShowIntelReport(true),
                  ping: false,
                },
              ].map(({ label, icon, color, onClick, ping }) => (
                <button
                  key={label}
                  onClick={onClick}
                  className="relative flex flex-col items-center gap-1.5 py-3 border transition-all duration-150 font-mono focus:outline-none focus-visible:ring-2 group"
                  style={{
                    borderColor: `${color}22`,
                    color:       `${color}55`,
                  }}
                  onMouseEnter={e => {
                    const el = e.currentTarget
                    el.style.borderColor = `${color}55`
                    el.style.background  = `${color}08`
                    el.style.color       = `${color}99`
                  }}
                  onMouseLeave={e => {
                    const el = e.currentTarget
                    el.style.borderColor = `${color}22`
                    el.style.background  = 'transparent'
                    el.style.color       = `${color}55`
                  }}
                >
                  {ping && (
                    <span className="absolute -top-1 -right-1 flex h-2.5 w-2.5 z-10 pointer-events-none">
                      <motion.span
                        className="absolute inline-flex h-full w-full rounded-full opacity-75"
                        style={{ background: color }}
                        animate={{ scale: [1, 1.8, 1], opacity: [0.75, 0, 0.75] }}
                        transition={{ duration: 1.4, repeat: Infinity }}
                      />
                      <span className="relative inline-flex rounded-full h-2.5 w-2.5" style={{ background: color }} />
                    </span>
                  )}
                  <span className="text-base leading-none">{icon}</span>
                  <span className="text-[7px] tracking-[0.3em] uppercase">{label}</span>
                </button>
              ))}
            </div>
          </motion.div>

          {/* ── Distinciones — logros desbloqueados ── */}
          {userId && (
            <motion.div
              initial={{ opacity: 0, x: 16 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.55 }}
            >
              <DistincionesPanel userId={userId} />
            </motion.div>
          )}

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
