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
import IntelReportModal from '@/components/Hub/IntelReportModal'
import DistincionesPanel from '@/components/Hub/DistincionesPanel'
import SkillTreePanel from '@/components/Hub/SkillTreePanel'
import DailyAnomalyCard from '@/components/Hub/DailyAnomalyCard'
import DakiMemoriaCard from '@/components/Hub/DakiMemoriaCard'
import RevisionSemanalCard from '@/components/Hub/RevisionSemanalCard'
import FinDeTurnoModal from '@/components/Game/FinDeTurnoModal'
import { getSessionLog, clearSessionLog } from '@/hooks/useSessionLog'
import type { SessionMission } from '@/hooks/useSessionLog'

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

// ─── Python Core Status ───────────────────────────────────────────────────────

const CORE_THRESHOLDS = { BASICO: 45, MEDIO: 95, AVANZADO: 140 }
const CORE_NODES = [
  { label: 'BÁSICO',   sub: 'Fundamentos'           },
  { label: 'MEDIO',    sub: 'Estructuras y Lógica'  },
  { label: 'AVANZADO', sub: 'Algoritmos y OOP'      },
  { label: 'EXPERT',   sub: 'Patrones y Producción' },
]

function PythonCoreStatus({ completedCount }: { completedCount: number }) {
  // Determinar nodo activo y progreso hacia el siguiente umbral
  let activeIdx   = 0
  let rangeStart  = 0
  let rangeEnd    = CORE_THRESHOLDS.BASICO

  if (completedCount >= CORE_THRESHOLDS.AVANZADO) {
    activeIdx  = 3; rangeStart = CORE_THRESHOLDS.AVANZADO; rangeEnd = CORE_THRESHOLDS.AVANZADO
  } else if (completedCount >= CORE_THRESHOLDS.MEDIO) {
    activeIdx  = 2; rangeStart = CORE_THRESHOLDS.MEDIO;    rangeEnd = CORE_THRESHOLDS.AVANZADO
  } else if (completedCount >= CORE_THRESHOLDS.BASICO) {
    activeIdx  = 1; rangeStart = CORE_THRESHOLDS.BASICO;   rangeEnd = CORE_THRESHOLDS.MEDIO
  }

  const pct          = rangeEnd > rangeStart
    ? Math.round(((completedCount - rangeStart) / (rangeEnd - rangeStart)) * 100)
    : 100
  const missionsLeft = Math.max(0, rangeEnd - completedCount)
  const nextLabel    = activeIdx < 3 ? CORE_NODES[activeIdx + 1].label : null

  return (
    <div className="flex flex-col gap-3">
      {/* Header */}
      <div className="flex items-center justify-between">
        <p className="text-[8px] tracking-[0.5em] text-[#00FF41]/20 font-mono uppercase">
          Operación Activa
        </p>
        <span className="text-[7px] tracking-[0.3em] text-[#00FF41]/15 font-mono">
          {completedCount} MIS.
        </span>
      </div>

      {/* Card del nodo activo */}
      <div
        className="relative overflow-hidden border px-4 py-3.5"
        style={{ borderColor: 'rgba(0,255,65,0.15)', background: 'rgba(0,255,65,0.025)' }}
      >
        <motion.div
          className="absolute top-0 left-0 right-0 h-px pointer-events-none"
          style={{ background: 'linear-gradient(90deg, transparent, rgba(0,255,65,0.45), transparent)' }}
          animate={{ opacity: [0.2, 0.8, 0.2] }}
          transition={{ duration: 2.2, repeat: Infinity }}
        />

        <div className="flex items-start justify-between mb-3">
          <div>
            <p className="text-[7px] tracking-[0.5em] text-[#00FF41]/30 font-mono mb-0.5">PYTHON CORE</p>
            <p
              className="text-base font-black tracking-[0.3em] font-mono leading-none"
              style={{ color: '#00FF41', textShadow: '0 0 10px rgba(0,255,65,0.5)' }}
            >
              {CORE_NODES[activeIdx].label}
            </p>
            <p className="text-[8px] tracking-[0.2em] text-[#00FF41]/35 font-mono mt-0.5">
              {CORE_NODES[activeIdx].sub}
            </p>
          </div>
          <motion.span
            className="text-[6px] tracking-[0.45em] font-black font-mono px-2 py-1 border border-[#00FF41]/25 text-[#00FF41]/55 bg-[#00FF41]/5 shrink-0"
            animate={{ opacity: [0.45, 1, 0.45] }}
            transition={{ duration: 1.4, repeat: Infinity }}
          >
            EN CURSO
          </motion.span>
        </div>

        {/* Barra de progreso */}
        <div className="h-[2px] w-full bg-white/5 overflow-hidden rounded-full mb-1.5">
          <motion.div
            className="h-full rounded-full"
            style={{ background: '#00FF41', boxShadow: '0 0 6px rgba(0,255,65,0.6)' }}
            initial={{ width: 0 }}
            animate={{ width: `${Math.min(pct, 100)}%` }}
            transition={{ delay: 0.8, duration: 0.9, ease: 'easeOut' }}
          />
        </div>
        <div className="flex justify-between">
          <span className="text-[6px] tracking-widest text-[#00FF41]/20 font-mono">
            {completedCount}/{rangeEnd} COMPLETADAS
          </span>
          {missionsLeft > 0 && nextLabel && (
            <span className="text-[6px] tracking-widest font-mono" style={{ color: 'rgba(245,158,11,0.45)' }}>
              {missionsLeft} → {nextLabel}
            </span>
          )}
        </div>
      </div>

      {/* Mini track — 4 nodos */}
      <div className="flex items-center justify-between px-1">
        {CORE_NODES.map((n, i) => {
          const done   = i < activeIdx
          const active = i === activeIdx
          const dotColor = done ? '#06b6d4' : active ? '#10b981' : 'rgba(255,255,255,0.1)'
          const lblColor = done ? 'rgba(6,182,212,0.55)' : active ? 'rgba(16,185,129,0.75)' : 'rgba(255,255,255,0.12)'
          return (
            <div key={n.label} className="flex items-center flex-1">
              <div className="flex flex-col items-center gap-1">
                <div
                  className="w-2 h-2 rounded-full"
                  style={{
                    background: dotColor,
                    boxShadow:  done ? '0 0 4px rgba(6,182,212,0.55)' : active ? '0 0 6px rgba(16,185,129,0.7)' : 'none',
                  }}
                />
                <span className="text-[5px] tracking-widest font-black font-mono" style={{ color: lblColor }}>
                  {n.label}
                </span>
              </div>
              {i < CORE_NODES.length - 1 && (
                <div
                  className="h-px flex-1 mx-1 mb-3.5"
                  style={{ background: i < activeIdx ? 'rgba(6,182,212,0.25)' : 'rgba(255,255,255,0.05)' }}
                />
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}

// ─── Barra de Progreso Global ─────────────────────────────────────────────────

const MILESTONES = [
  { at:  45, label: 'BÁSICO completado'    },
  { at:  95, label: 'MEDIO completado'     },
  { at: 140, label: 'AVANZADO completado'  },
  { at: 190, label: 'PYTHON CORE COMPLETO' },
]

function GlobalProgressBar({ completedCount }: { completedCount: number }) {
  const TOTAL = 190
  const pct   = Math.min(100, Math.round((completedCount / TOTAL) * 100))
  const next  = MILESTONES.find(m => m.at > completedCount)
  const toNext = next ? next.at - completedCount : 0

  return (
    <div className="relative z-20 shrink-0 px-6 py-1.5 border-b border-[#06b6d4]/10 bg-black/30"
      style={{ backdropFilter: 'blur(4px)' }}>
      <div className="flex items-center gap-3">
        <span className="text-[9px] font-mono tracking-[0.3em] shrink-0"
          style={{ color: 'rgba(6,182,212,0.55)' }}>
          PYTHON CORE
        </span>
        <div className="flex-1 h-[3px] rounded-full overflow-hidden" style={{ background: 'rgba(6,182,212,0.08)' }}>
          <motion.div
            className="h-full rounded-full"
            initial={{ width: 0 }}
            animate={{ width: `${pct}%` }}
            transition={{ duration: 1.0, ease: 'easeOut', delay: 0.5 }}
            style={{
              background: pct >= 100
                ? 'linear-gradient(90deg, rgba(6,182,212,0.9), rgba(16,185,129,0.9))'
                : 'rgba(6,182,212,0.65)',
              boxShadow: '0 0 8px rgba(6,182,212,0.50)',
            }}
          />
        </div>
        <span className="text-[9px] font-black font-mono shrink-0"
          style={{ color: 'rgba(6,182,212,0.80)' }}>
          {completedCount}/{TOTAL}
        </span>
        {next && (
          <span className="text-[8px] font-mono shrink-0 hidden sm:block"
            style={{ color: 'rgba(6,182,212,0.35)' }}>
            · {next.label} en {toNext} misión{toNext !== 1 ? 'es' : ''}
          </span>
        )}
      </div>
    </div>
  )
}

// ─── Onboarding — modal de primera visita ─────────────────────────────────────

function OnboardingModal({ onClose, onStart }: { onClose: () => void; onStart: () => void }) {
  const [step, setStep] = useState(0)

  const steps = [
    {
      icon:  '◈',
      title: 'Bienvenido al Nexo',
      body:  'El Nexo es la plataforma de entrenamiento operacional de DAKI EdTech. Aquí convertirás conocimiento en habilidades reales mediante misiones progresivas.',
      cta:   'CONTINUAR',
    },
    {
      icon:  '⬡',
      title: 'Python Core — Tu primera formación',
      body:  '100 misiones. 4 sectores de dificultad creciente. 1 Boss Final. Python Core es la base de todo lo que vendrá después en el Nexo.',
      cta:   'CONTINUAR',
    },
    {
      icon:  '▶',
      title: 'Primera misión disponible',
      body:  'Tu primer desafío ya está desbloqueado. Comienza por el Sector 00 — Calibración Sináptica. DAKI te guiará en cada paso.',
      cta:   'INICIAR OPERACIÓN',
    },
  ]

  const current = steps[step]
  const isLast  = step === steps.length - 1

  return (
    <motion.div
      className="fixed inset-0 z-[500] flex items-center justify-center px-4"
      style={{ background: 'rgba(0,0,0,0.85)', backdropFilter: 'blur(8px)' }}
      initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
    >
      <motion.div
        className="relative w-full max-w-sm border font-mono overflow-hidden"
        style={{ background: '#020617', borderColor: 'rgba(6,182,212,0.40)', boxShadow: '0 0 60px rgba(6,182,212,0.15)' }}
        initial={{ scale: 0.90, y: 20 }} animate={{ scale: 1, y: 0 }} exit={{ scale: 0.90, y: 20 }}
        transition={{ duration: 0.25, ease: 'easeOut' }}
      >
        {/* Línea pulso superior */}
        <motion.div className="h-px w-full"
          style={{ background: 'linear-gradient(90deg, transparent, rgba(6,182,212,0.70), transparent)' }}
          animate={{ opacity: [0.4, 1, 0.4] }} transition={{ duration: 1.8, repeat: Infinity }} />

        {/* Esquinas */}
        {['top-0 left-0 border-t border-l', 'top-0 right-0 border-t border-r', 'bottom-0 left-0 border-b border-l', 'bottom-0 right-0 border-b border-r'].map(cls => (
          <span key={cls} className={`absolute w-3 h-3 ${cls}`} style={{ borderColor: 'rgba(6,182,212,0.55)' }} />
        ))}

        <div className="px-8 py-8">
          {/* Indicadores de paso */}
          <div className="flex gap-1.5 mb-6">
            {steps.map((_, i) => (
              <div key={i} className="flex-1 h-[2px] rounded-full"
                style={{ background: i <= step ? 'rgba(6,182,212,0.80)' : 'rgba(6,182,212,0.15)' }} />
            ))}
          </div>

          <AnimatePresence mode="wait">
            <motion.div key={step}
              initial={{ opacity: 0, x: 16 }} animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -16 }} transition={{ duration: 0.20 }}>
              <div className="text-4xl mb-4 text-center"
                style={{ color: 'rgba(6,182,212,0.80)', textShadow: '0 0 20px rgba(6,182,212,0.50)' }}>
                {current.icon}
              </div>
              <h2 className="text-base font-black tracking-[0.25em] uppercase mb-3 text-center"
                style={{ color: 'rgba(6,182,212,0.95)' }}>
                {current.title}
              </h2>
              <p className="text-xs leading-relaxed text-center mb-6"
                style={{ color: 'rgba(255,255,255,0.55)' }}>
                {current.body}
              </p>
            </motion.div>
          </AnimatePresence>

          <motion.button
            onClick={() => isLast ? onStart() : setStep(s => s + 1)}
            className="w-full py-2.5 font-black tracking-[0.35em] text-[11px] border mb-2"
            style={{ borderColor: 'rgba(6,182,212,0.50)', color: 'rgba(6,182,212,1)', background: 'rgba(6,182,212,0.08)' }}
            whileHover={{ background: 'rgba(6,182,212,0.16)', boxShadow: '0 0 20px rgba(6,182,212,0.20)' }}
            whileTap={{ scale: 0.98 }}>
            {current.cta}
          </motion.button>
          <button onClick={onClose}
            className="w-full text-[9px] tracking-[0.3em] text-center py-1.5 transition-colors"
            style={{ color: 'rgba(255,255,255,0.20)' }}
            onMouseEnter={e => (e.currentTarget.style.color = 'rgba(255,255,255,0.45)')}
            onMouseLeave={e => (e.currentTarget.style.color = 'rgba(255,255,255,0.20)')}>
            EXPLORAR PRIMERO
          </button>
        </div>
      </motion.div>
    </motion.div>
  )
}

// ─── Trial Countdown Banner ───────────────────────────────────────────────────

function TrialCountdownBanner({
  subscriptionStatus,
  trialEndDate,
  onSubscribe,
}: {
  subscriptionStatus: string
  trialEndDate: string | null
  onSubscribe: () => void
}) {
  if (subscriptionStatus !== 'TRIAL') return null

  const daysLeft = trialEndDate
    ? Math.max(0, Math.ceil((new Date(trialEndDate).getTime() - Date.now()) / 86400000))
    : null

  const urgent  = daysLeft !== null && daysLeft <= 2
  const warning = daysLeft !== null && daysLeft <= 5

  const color     = urgent ? '#FF4040' : warning ? '#FFB800' : '#00E5FF'
  const colorDim  = urgent ? 'rgba(255,64,64,0.15)' : warning ? 'rgba(255,184,0,0.10)' : 'rgba(0,229,255,0.08)'
  const colorBdr  = urgent ? 'rgba(255,64,64,0.40)' : warning ? 'rgba(255,184,0,0.35)' : 'rgba(0,229,255,0.25)'

  return (
    <motion.div
      initial={{ opacity: 0, y: -8 }}
      animate={{ opacity: 1, y: 0 }}
      className="w-full font-mono border-b flex items-center justify-between px-6 py-2 gap-4"
      style={{ background: colorDim, borderColor: colorBdr }}
    >
      <div className="flex items-center gap-3">
        <motion.span
          style={{ color }}
          animate={{ opacity: [0.6, 1, 0.6] }}
          transition={{ duration: 1.6, repeat: Infinity }}
          className="text-sm"
        >
          {urgent ? '⚠' : '◉'}
        </motion.span>
        <span className="text-[10px] tracking-[0.3em] uppercase" style={{ color }}>
          {urgent
            ? `TRIAL EXPIRA EN ${daysLeft === 0 ? 'HOY' : `${daysLeft}D`} — ACCESO EN RIESGO`
            : daysLeft !== null
              ? `TRIAL ACTIVO — ${daysLeft} DÍAS RESTANTES`
              : 'PERÍODO DE PRUEBA ACTIVO'}
        </span>
      </div>
      <motion.button
        onClick={onSubscribe}
        className="text-[9px] tracking-[0.35em] uppercase px-3 py-1 border shrink-0"
        style={{ borderColor: colorBdr, color, background: colorDim }}
        whileHover={{ scale: 1.04 }}
        whileTap={{ scale: 0.97 }}
      >
        ACTIVAR LICENCIA →
      </motion.button>
    </motion.div>
  )
}

// ─── Página Hub ────────────────────────────────────────────────────────────────

export default function HubPage() {
  const router = useRouter()
  const {
    _hasHydrated,
    userId, username, level, totalXp, streakDays, badges,
    subscriptionStatus, isPaid, role,
    clearUser, setSubscription, setIsPaid, setRole,
  } = useUserStore()

  const handleLogout = () => {
    ;['daki_user_id', 'daki_callsign', 'daki_level', 'daki_licensed'].forEach(k => localStorage.removeItem(k))
    clearUser()
    document.cookie = 'enigma_user=; path=/; max-age=0; SameSite=Lax'
    // Eliminar cookie httpOnly desde el servidor
    const API_BASE_LOGOUT = process.env.NEXT_PUBLIC_API_URL ?? ''
    fetch(`${API_BASE_LOGOUT}/api/v1/auth/logout`, { method: 'POST', credentials: 'include' }).catch(() => {})
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
  const [showOnboarding,     setShowOnboarding]     = useState(false)
  const [showDakiGreeting,   setShowDakiGreeting]   = useState(false)
  const [sessionLog,         setSessionLog]         = useState<SessionMission[]>([])
  const [showFinDeTurno,     setShowFinDeTurno]     = useState(false)

  // ── Saludo de DAKI — una vez por sesión de navegador ──────────────────────
  useEffect(() => {
    if (!username) return
    try {
      if (sessionStorage.getItem('daki_greeted')) return
      sessionStorage.setItem('daki_greeted', '1')
    } catch { /* */ }
    const t = setTimeout(() => {
      setShowDakiGreeting(true)
      setTimeout(() => setShowDakiGreeting(false), 5000)
    }, 900)
    return () => clearTimeout(t)
  }, [username])

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

  // ── Onboarding — primera visita ───────────────────────────────────────────
  useEffect(() => {
    if (!_hasHydrated || !userId) return
    if (!localStorage.getItem('nexo_onboarded')) {
      setTimeout(() => setShowOnboarding(true), 900)
    }
  }, [_hasHydrated, userId])

  // ── Cargar log de sesión al montar ────────────────────────────────────────
  useEffect(() => {
    setSessionLog(getSessionLog())
  }, [])

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
    const API_BASE_LOCAL = process.env.NEXT_PUBLIC_API_URL ?? ''
    fetch(`${API_BASE_LOCAL}/api/v1/session/open`, {
      method:      'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
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
    // Sellar boot_seen para usuarios con progreso previo (evita que vean la secuencia de arranque retroactivamente)
    if (level > 1) { try { localStorage.setItem('boot_seen', '1') } catch { /* */ } }
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

  const [leagueTier, setLeagueTier] = useState<string>('')

  // ── Sincronizar subscription_status y liga desde backend al montar ───────────
  useEffect(() => {
    if (!userId) return
    const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? ''
    fetch(`${API_BASE}/api/v1/user/me`, { credentials: 'include' })
      .then(r => r.ok ? r.json() : null)
      .then((data: { subscription_status?: string; trial_end_date?: string | null; role?: string; league_tier?: string } | null) => {
        if (!data) return
        if (data.subscription_status && data.subscription_status !== 'INACTIVE') {
          setSubscription(data.subscription_status, data.trial_end_date ?? null)
          if (data.subscription_status === 'ACTIVE') setIsPaid(true)
        }
        if (data.role) setRole(data.role)
        if (data.role === 'FOUNDER') {
          setSubscription(data.subscription_status ?? 'ACTIVE', null)
          setIsPaid(true)
        }
        if (data.league_tier) setLeagueTier(data.league_tier)
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
    const API_BASE_LOCAL = process.env.NEXT_PUBLIC_API_URL ?? ''
    try {
      const res = await fetch(`${API_BASE_LOCAL}/api/v1/payments/create-checkout-session`, {
        method:      'POST',
        credentials: 'include',
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
      style={{ background: 'radial-gradient(circle at 50% 30%, #030d1f 0%, #020617 55%, #010410 100%)' }}
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

      {/* ── Onboarding — primera visita ── */}
      <AnimatePresence>
        {showOnboarding && (
          <OnboardingModal onClose={() => {
            localStorage.setItem('nexo_onboarded', '1')
            setShowOnboarding(false)
          }} onStart={() => {
            localStorage.setItem('nexo_onboarded', '1')
            setShowOnboarding(false)
            navigateWithFade('/misiones')
          }} />
        )}
      </AnimatePresence>

      {/* ── Header ── */}
      <header className="relative z-20 shrink-0 flex flex-wrap items-center justify-between px-6 py-2.5 border-b border-[#00FF41]/12 bg-black/40 backdrop-blur-sm gap-4">
        <div className="flex items-center gap-4 shrink-0">
          <span className="font-black tracking-widest text-sm" style={{ textShadow: '0 0 8px #00FF41' }}>
            NEXO CENTRAL
          </span>
          <span className="text-[8px] tracking-[0.5em] text-[#00FF41]/25 hidden md:block">
            {'// OPERADORES PYTHON · ECOSISTEMA ACTIVO'}
          </span>
        </div>
        
        {/* Panel de Controles & Rango (CSS Flex con wrapping y gaps fijos) */}
        <div className="flex flex-wrap items-center justify-end gap-3 sm:gap-5 text-xs text-[#00FF41]/45">
          <span className="text-[#00FF41]/30 hidden lg:block truncate max-w-[120px]" title={username}>{username}</span>
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
          
          {role === 'FOUNDER' && (
            <motion.button
              onClick={() => navigateWithFade('/founder')}
              className="border px-3 py-1 text-[9px] font-mono tracking-widest cursor-pointer transition-all duration-150 shrink-0"
              style={{ borderColor: 'rgba(255,199,0,0.30)', color: 'rgba(255,199,0,0.55)' }}
              whileHover={{ borderColor: 'rgba(255,199,0,0.75)', color: 'rgba(255,199,0,1)' }}
              whileTap={{ scale: 0.96 }}
              title="Panel de datos — progreso de usuarios"
            >
              ◈ DATOS
            </motion.button>
          )}

          <button
            onClick={handleLogout}
            className="text-red-500 hover:text-red-400 hover:bg-red-950/30 border border-red-800 px-3 py-1 text-xs font-mono tracking-widest cursor-pointer transition-all shrink-0"
          >
            [ ABORTAR CONEXIÓN ]
          </button>
        </div>
      </header>

      {/* ── Trial Countdown Banner ── */}
      <TrialCountdownBanner
        subscriptionStatus={subscriptionStatus}
        trialEndDate={useUserStore.getState().trialEndDate}
        onSubscribe={handleStripeCheckout}
      />

      {/* ── Boss Warning Banner ── */}
      <BossWarningBanner level={level} />

      {/* ── Barra de progreso global ── */}
      <GlobalProgressBar completedCount={completedOrders.length} />

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
                color:      '#4ade80',
                textShadow: '0 0 20px rgba(74,222,128,0.65), 0 0 50px rgba(74,222,128,0.25)',
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
                style={{ borderColor: 'rgba(74,222,128,0.30)', background: 'rgba(74,222,128,0.05)' }}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.35 }}
              >
                <span className="text-[10px] font-black tracking-[0.5em] font-mono"
                  style={{ color: '#4ade80', textShadow: '0 0 8px rgba(74,222,128,0.50)' }}>
                  OPERADOR
                </span>
                <span className="text-[8px] font-mono" style={{ color: 'rgba(74,222,128,0.45)' }}>// NIV. {level}</span>
              </motion.div>
            )}
            {/* Espacio base — sin CTA aquí */}
            <div className="mb-1" />

          </motion.div>

          {/* Divisor */}
          <div className="w-full max-w-sm h-px bg-[#00FF41]/8 mb-6" />

          {/* ── DAKI — compacto ── */}
          <motion.div
            className="text-[7px] tracking-[0.6em] mb-4 text-center font-mono"
            style={{ color: 'rgba(74,222,128,0.35)' }}
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.5 }}
          >
            SIMBIONTE // UNIDAD DAKI // CONEXIÓN ACTIVA
          </motion.div>

          {/* Envoltorio DAKI con aura verde pulsante */}
          <motion.div
            className="relative transform scale-75 origin-center mb-1"
            initial={{ opacity: 0, scale: 0.5 }}
            animate={{ opacity: 1, scale: 0.75 }}
            transition={{ duration: 0.7, ease: [0.16, 1, 0.3, 1], delay: 0.3 }}
          >
            <div className="neon-pulse--emerald rounded-full absolute inset-0 -m-4 pointer-events-none" />
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
            PANEL CENTRAL — Skill Tree Python Core
        ══════════════════════════════════════════════ */}
        <motion.div
          className="flex-1 min-w-0 border-r border-[#00FF41]/8 overflow-hidden"
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.35, duration: 0.45 }}
        >
          <SkillTreePanel
            completedCount={completedOrders.length}
            onNavigate={navigateWithFade}
          />
        </motion.div>

        {/* ══════════════════════════════════════════════
            PANEL DERECHO — Navegación Táctica
        ══════════════════════════════════════════════ */}
        <motion.div
          className="w-[320px] shrink-0 flex flex-col justify-start gap-5 px-8 py-6 overflow-y-auto [&::-webkit-scrollbar]:hidden [-ms-overflow-style:none] [scrollbar-width:none]"
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
                {leagueTier && (
                  <p
                    className="text-[7px] tracking-widest mt-0.5 font-black cursor-pointer"
                    style={{ color: leagueTier === 'Arquitecto Supremo' ? '#FF6B9D' : leagueTier === 'Diamante' ? '#7DF9FF' : leagueTier === 'Oro' ? '#FFD700' : leagueTier === 'Plata' ? '#C0C0C0' : '#CD7F32' }}
                    onClick={() => navigateWithFade('/leaderboard')}
                    title="Ver clasificación"
                  >
                    ◆ {leagueTier.toUpperCase()}
                  </p>
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
            className="neon-pulse rounded-sm"
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

          {/* ── ARENA — Modo PvP ── */}
          <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.28 }}
          >
            <motion.button
              onClick={() => navigateWithFade('/arena')}
              className="w-full py-3 font-black text-sm tracking-[0.25em] uppercase font-mono border-2 transition-all duration-200 cursor-pointer flex items-center justify-center gap-3"
              style={{
                borderColor: 'rgba(255,107,107,0.45)',
                color:       'rgba(255,107,107,0.85)',
                background:  'rgba(255,107,107,0.05)',
                textShadow:  '0 0 8px rgba(255,107,107,0.5)',
              }}
              whileHover={{
                background:  'rgba(255,107,107,0.12)',
                boxShadow:   '0 0 24px rgba(255,107,107,0.2)',
              }}
              whileTap={{ scale: 0.98 }}
            >
              <span style={{ opacity: 0.6 }}>⚔</span>
              <span>MODO ARENA</span>
              <span className="text-[9px] font-normal tracking-widest" style={{ color: 'rgba(255,107,107,0.45)' }}>PvP</span>
            </motion.button>
          </motion.div>

          {/* ── Progreso Python Core ── */}
          <motion.div
            initial={{ opacity: 0, x: 16 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
          >
            <PythonCoreStatus completedCount={completedOrders.length} />
          </motion.div>

          {/* F3: Anomalía Diaria */}
          <DailyAnomalyCard />

          {/* F4: DAKI Memoria — resumen de sesión activa */}
          <DakiMemoriaCard />

          {/* Block 4: Revisión Semanal — conceptos con maestría incompleta sin practicar */}
          {userId && <RevisionSemanalCard userId={userId} />}

          {/* F4: Fin de Turno — aparece con 2+ misiones completadas */}
          {sessionLog.length >= 2 && (
            <TacticButton
              onClick={() => setShowFinDeTurno(true)}
              label="VER INFORME DE TURNO"
              sublabel={`${sessionLog.length} misiones ejecutadas esta sesión`}
              icon="◎"
              primary
            />
          )}

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
                  label: 'LIGAS', icon: '◆', color: '#FFD700',
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

      {/* ── Fin de Turno — resumen de sesión con DAKI ───────────────────────── */}
      <FinDeTurnoModal
        visible={showFinDeTurno}
        userId={userId ?? ''}
        operatorLevel={level}
        missions={sessionLog}
        onClose={() => {
          setShowFinDeTurno(false)
          clearSessionLog()
          setSessionLog([])
        }}
      />

      {/* ── Saludo de DAKI ───────────────────────────────────────────────────── */}
      <AnimatePresence>
        {showDakiGreeting && (
          <motion.div
            initial={{ opacity: 0, y: -16, scale: 0.97 }}
            animate={{ opacity: 1, y: 0,   scale: 1 }}
            exit={{    opacity: 0, y: -10,  scale: 0.97 }}
            transition={{ duration: 0.28, ease: 'easeOut' }}
            className="fixed top-14 left-1/2 z-[90] -translate-x-1/2 pointer-events-none"
          >
            <div
              className="flex items-center gap-3 px-5 py-3 font-mono backdrop-blur-sm"
              style={{
                border:     '1px solid rgba(0,207,255,0.35)',
                background: 'rgba(0,0,0,0.88)',
                boxShadow:  '0 0 28px rgba(0,207,255,0.15), 0 4px 24px rgba(0,0,0,0.6)',
              }}
            >
              {/* Ojo de DAKI */}
              <motion.span
                className="text-xl leading-none shrink-0"
                style={{ color: '#00CFFF', textShadow: '0 0 12px rgba(0,207,255,0.8)' }}
                animate={{ opacity: [0.6, 1, 0.6], scale: [1, 1.12, 1] }}
                transition={{ duration: 1.4, repeat: Infinity, ease: 'easeInOut' }}
              >◈</motion.span>

              {/* Texto */}
              <div>
                <span className="text-[8px] tracking-[0.45em] block mb-0.5"
                  style={{ color: 'rgba(0,207,255,0.45)' }}>
                  DAKI · TRANSMISIÓN
                </span>
                <span className="text-[12px] font-bold tracking-[0.1em]"
                  style={{ color: 'rgba(255,255,255,0.85)' }}>
                  {(() => {
                    const h = new Date().getHours()
                    const saludo = h < 12 ? 'Buenos días' : h < 19 ? 'Buenas tardes' : 'Buenas noches'
                    return `${saludo}, `
                  })()}
                  <span style={{ color: '#00CFFF', textShadow: '0 0 8px rgba(0,207,255,0.6)' }}>
                    {username?.toUpperCase()}
                  </span>
                  <span style={{ color: 'rgba(255,255,255,0.4)' }}>.</span>
                </span>
              </div>

              {/* Waveform decorativa */}
              <div className="flex items-end gap-0.5 h-4 shrink-0">
                {[5,9,14,8,12,6,10,7,13,5].map((h, i) => (
                  <motion.span key={i}
                    className="block w-0.5 rounded-full"
                    style={{ background: '#00CFFF', opacity: 0.5 }}
                    animate={{ height: [h * 0.5, h, h * 0.3, h * 0.8, h * 0.5] }}
                    transition={{ duration: 0.6 + i * 0.04, repeat: Infinity, ease: 'easeInOut', delay: i * 0.05 }}
                  />
                ))}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

    </div>
    </MobileGate>
  )
}
