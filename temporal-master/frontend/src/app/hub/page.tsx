'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { motion, AnimatePresence } from 'framer-motion'
import { useUserStore } from '@/store/userStore'
import BitacoraModal, { countNewArchives } from '@/components/Game/BitacoraModal'
import HubAudio from '@/components/UI/HubAudio'

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
  onClick, label, sublabel, icon, primary = false,
}: {
  onClick: () => void
  label: string
  sublabel: string
  icon: string
  primary?: boolean
}) {
  return (
    <motion.button
      onClick={onClick}
      className="w-full text-left px-5 py-4 border font-mono transition-all duration-150 group relative overflow-hidden cursor-pointer z-10"
      style={primary
        ? { borderColor: 'rgba(0,255,65,0.5)', background: 'rgba(0,255,65,0.06)' }
        : { borderColor: 'rgba(0,255,65,0.2)', background: 'transparent' }
      }
      whileHover={{ x: 3 }}
      whileTap={{ scale: 0.98 }}
      onMouseEnter={e => {
        const el = e.currentTarget
        el.style.background = 'rgba(0,255,65,0.12)'
        el.style.borderColor = 'rgba(0,255,65,0.7)'
        el.style.boxShadow = '0 0 20px rgba(0,255,65,0.15)'
      }}
      onMouseLeave={e => {
        const el = e.currentTarget
        el.style.background = primary ? 'rgba(0,255,65,0.06)' : 'transparent'
        el.style.borderColor = primary ? 'rgba(0,255,65,0.5)' : 'rgba(0,255,65,0.2)'
        el.style.boxShadow = 'none'
      }}
    >
      <div className="flex items-center justify-between gap-4">
        <div className="flex flex-col gap-0.5 min-w-0">
          <span
            className="text-sm font-black tracking-widest uppercase text-[#00FF41]"
            style={primary ? { textShadow: '0 0 8px rgba(0,255,65,0.6)' } : undefined}
          >
            {label}
          </span>
          <span className="text-[10px] tracking-wider text-[#00FF41]/40 truncate">
            {sublabel}
          </span>
        </div>
        <motion.span
          className="text-xl shrink-0 text-[#00FF41]/60"
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
  const { userId, username, level, totalXp, streakDays, badges, clearUser } = useUserStore()

  const handleLogout = () => {
    clearUser()
    document.cookie = 'enigma_user=; path=/; max-age=0; SameSite=Lax'
    router.push('/')
  }
  const [quote] = useState(() => DAKI_QUOTES[Math.floor(Math.random() * DAKI_QUOTES.length)])
  const { displayed, done } = useTypewriter(quote)
  const [isBitacoraOpen, setIsBitacoraOpen] = useState(false)
  const [completedOrders, setCompletedOrders] = useState<number[]>([])
  const [bgmFadeOut, setBgmFadeOut] = useState(false)

  const navigateWithFade = (path: string) => {
    setBgmFadeOut(true)
    setTimeout(() => router.push(path), 580)
  }

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

  return (
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
      <BitacoraModal isOpen={isBitacoraOpen} onClose={() => setIsBitacoraOpen(false)} completedOrders={completedOrders} />

      {/* ── Header ── */}
      <header className="relative z-20 shrink-0 flex items-center justify-between px-6 py-2.5 border-b border-[#00FF41]/12 bg-black/40 backdrop-blur-sm">
        <div className="flex items-center gap-4">
          <span className="font-black tracking-widest text-sm" style={{ textShadow: '0 0 8px #00FF41' }}>
            PYTHON QUEST
          </span>
          <span className="text-[8px] tracking-[0.5em] text-[#00FF41]/25 hidden sm:block">
            // CENTRO DE MANDO ACTIVO
          </span>
        </div>
        <div className="flex items-center gap-5 text-xs text-[#00FF41]/45">
          <span className="text-[#00FF41]/30 hidden sm:block">{username}</span>
          <span>NVL <strong className="text-[#00FF41]">{level}</strong></span>
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

          {/* Caja de diálogo */}
          <motion.div
            className="w-full max-w-sm"
            initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6, duration: 0.4 }}
          >
            <div className="relative border border-[#00FF41]/25 bg-black/60 px-5 py-4 backdrop-blur-sm">
              {/* Esquinas */}
              <span className="absolute top-0 left-0 w-2.5 h-2.5 border-t-2 border-l-2 border-[#00FF41]/60" />
              <span className="absolute top-0 right-0 w-2.5 h-2.5 border-t-2 border-r-2 border-[#00FF41]/60" />
              <span className="absolute bottom-0 left-0 w-2.5 h-2.5 border-b-2 border-l-2 border-[#00FF41]/60" />
              <span className="absolute bottom-0 right-0 w-2.5 h-2.5 border-b-2 border-r-2 border-[#00FF41]/60" />

              <div className="flex items-center gap-2 mb-2">
                <motion.span
                  className="w-1.5 h-1.5 rounded-full bg-[#00FF41]"
                  animate={{ opacity: [1, 0.15, 1] }}
                  transition={{ duration: 1, repeat: Infinity }}
                />
                <span className="text-[8px] tracking-[0.5em] text-[#00FF41]/35">DAKI // CANAL CIFRADO</span>
              </div>

              <p
                className="text-[12px] leading-relaxed text-[#00FF41] min-h-[4rem]"
                style={{ textShadow: '0 0 6px rgba(0,255,65,0.35)' }}
              >
                {displayed}
                {!done && (
                  <motion.span
                    className="inline-block w-[8px] h-[14px] ml-0.5 align-middle bg-[#00FF41]"
                    animate={{ opacity: [1, 0] }}
                    transition={{ duration: 0.5, repeat: Infinity, repeatType: 'reverse' }}
                    style={{ boxShadow: '0 0 6px #00FF41' }}
                  />
                )}
              </p>
            </div>
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

          {/* Separador */}
          <div className="h-px bg-[#00FF41]/8 w-full" />

          {/* Accesos secundarios */}
          <div className="flex flex-col gap-2">
            <p className="text-[8px] tracking-[0.5em] text-[#00FF41]/15 mb-1">ACCESOS SECUNDARIOS</p>
            {[
              { label: 'BOUNTIES IA', path: '/bounty', color: '#FFD700' },
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
                { label: 'BOUNTY AI',     ok: false },
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
    </div>
  )
}
