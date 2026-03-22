'use client'

import { useEffect, useMemo, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useUserStore } from '@/store/userStore'

// ─── Types ────────────────────────────────────────────────────────────────────

type Phase = 'decrypt' | 'flash' | 'reveal'

// ─── Constants ────────────────────────────────────────────────────────────────

const DECRYPT_LINES = [
  { text: '> INICIANDO PROTOCOLO DE DESENCRIPTACIÓN DEL NEXO...', gold: false, delay: 0    },
  { text: '> NEUTRALIZANDO CAPAS DE CIFRADO CUÁNTICO...',         gold: false, delay: 240  },
  { text: '> DECODIFICANDO FRAGMENTOS [████████░░░░░░░░] 48%',    gold: true,  delay: 500  },
  { text: '> VALIDANDO FIRMA BIOMÉTRICA DEL OPERADOR...',         gold: false, delay: 760  },
  { text: '> DECODIFICANDO FRAGMENTOS [████████████████] 100%',   gold: true,  delay: 1020 },
  { text: '> HAZAÑA CONFIRMADA: NIVEL 100 — NEXO VENCIDO',        gold: false, delay: 1280 },
  { text: '> GENERANDO CREDENCIALES PERMANENTES...',              gold: false, delay: 1520 },
  { text: '> NEXO DESENCRIPTADO  ◈  IDENTIDAD VALIDADA  ◈',       gold: true,  delay: 1760 },
]

const LAST_DELAY = DECRYPT_LINES[DECRYPT_LINES.length - 1].delay
const FLASH_START = LAST_DELAY + 300   // ms
const REVEAL_START = LAST_DELAY + 760  // ms

const MATRIX_CHARS = '01アイウエオカキクケコサシスセソタチツ∴∵∶∷⊕⊗⊘'

// ─── Helpers ──────────────────────────────────────────────────────────────────

function generateCertId(): string {
  const pool = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
  return (
    'GG-CERT-' +
    Array.from({ length: 5 }, () => pool[Math.floor(Math.random() * pool.length)]).join('')
  )
}

function formatDate(): string {
  const d = new Date()
  const months = ['ENE','FEB','MAR','ABR','MAY','JUN','JUL','AGO','SEP','OCT','NOV','DIC']
  return `${String(d.getDate()).padStart(2, '0')} ${months[d.getMonth()]} ${d.getFullYear()}`
}

// ─── Matrix rain ──────────────────────────────────────────────────────────────

function MatrixRain() {
  const columns = useMemo(
    () =>
      Array.from({ length: 26 }, (_, i) => ({
        id: i,
        left: `${(i / 26) * 100}%`,
        text: Array.from({ length: 32 }, () =>
          MATRIX_CHARS[Math.floor(Math.random() * MATRIX_CHARS.length)]
        ).join('\n'),
        duration: 1.5 + ((i * 0.19) % 1.2),
        delay:    (i * 0.13) % 0.9,
        opacity:  0.05 + (i % 8) * 0.025,
      })),
    []
  )

  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none select-none">
      {columns.map(col => (
        <motion.div
          key={col.id}
          className="absolute top-0 font-mono text-[10px] leading-[13px] text-[#00FF41] whitespace-pre"
          style={{ left: col.left, opacity: col.opacity }}
          initial={{ y: '-30vh' }}
          animate={{ y: '115vh' }}
          transition={{ duration: col.duration, delay: col.delay, repeat: Infinity, ease: 'linear' }}
        >
          {col.text}
        </motion.div>
      ))}
    </div>
  )
}

// ─── Certificate card ─────────────────────────────────────────────────────────

interface CardProps {
  username: string
  certId: string
  certDate: string
  rank: string
}

function CertCard({ username, certId, certDate, rank }: CardProps) {
  return (
    // Gradient border wrapper (p-[1px] trick)
    <motion.div
      className="w-full p-[1px] relative"
      style={{ background: 'linear-gradient(135deg, #FFD700, #BD00FF, #FFD70080, #00FF4140, #BD00FF)' }}
      initial={{ opacity: 0, scale: 0.9, y: 16 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      transition={{ type: 'spring', stiffness: 240, damping: 22, delay: 0.1 }}
    >
      {/* Inner card */}
      <div
        className="relative overflow-hidden font-mono"
        style={{ background: 'linear-gradient(135deg, #050510 0%, #080818 55%, #0C0A18 100%)' }}
      >
        {/* Holographic shimmer */}
        <motion.div
          className="absolute inset-0 pointer-events-none z-10"
          style={{
            background:
              'linear-gradient(108deg, transparent 25%, rgba(255,215,0,0.05) 48%, rgba(189,0,255,0.04) 52%, transparent 75%)',
          }}
          initial={{ x: '-100%' }}
          animate={{ x: '200%' }}
          transition={{ duration: 3.2, delay: 0.8, repeat: Infinity, repeatDelay: 4 }}
        />

        {/* Scanlines */}
        <div
          className="absolute inset-0 pointer-events-none z-10"
          style={{
            backgroundImage:
              'repeating-linear-gradient(0deg,transparent,transparent 3px,rgba(0,0,0,0.18) 3px,rgba(0,0,0,0.18) 4px)',
          }}
        />

        {/* Corner accents */}
        <div className="absolute top-0 left-0 w-7 h-7 border-t-2 border-l-2 border-[#FFD700]/60 z-20" />
        <div className="absolute top-0 right-0 w-7 h-7 border-t-2 border-r-2 border-[#FFD700]/60 z-20" />
        <div className="absolute bottom-0 left-0 w-7 h-7 border-b-2 border-l-2 border-[#FFD700]/60 z-20" />
        <div className="absolute bottom-0 right-0 w-7 h-7 border-b-2 border-r-2 border-[#FFD700]/60 z-20" />

        <div className="relative z-20 px-8 pt-7 pb-0">

          {/* ── HEADER ROW ─────────────────────────────────────────────────── */}
          <div className="flex items-start justify-between mb-4">
            <div>
              <p className="text-[8px] tracking-[0.55em] text-[#FFD700]/45 mb-0.5">
                GLITCH &amp; GOLD NETWORK
              </p>
              <p className="text-[7px] tracking-[0.35em] text-[#00FF41]/25">
                AUTORIDAD CENTRAL DEL NEXO — CERTIFICACIÓN OPERACIONAL
              </p>
            </div>
            <motion.span
              className="text-xl text-[#FFD700]/30"
              style={{ textShadow: '0 0 18px #FFD70060' }}
              animate={{ opacity: [0.3, 0.75, 0.3] }}
              transition={{ duration: 2.6, repeat: Infinity }}
            >
              ◈
            </motion.span>
          </div>

          {/* Divider */}
          <div className="h-px bg-gradient-to-r from-[#FFD700]/40 via-[#BD00FF]/50 to-[#FFD700]/40 mb-6" />

          {/* ── MAIN CONTENT ───────────────────────────────────────────────── */}
          <div className="flex items-stretch gap-8 mb-6">

            {/* LEFT — Identity */}
            <div className="flex-1 min-w-0">
              <p className="text-[7px] tracking-[0.5em] text-[#00FF41]/35 mb-3">
                IDENTIDAD VERIFICADA
              </p>

              {/* Username */}
              <motion.h1
                className="text-3xl font-black tracking-widest uppercase truncate mb-2"
                style={{ color: '#FFD700', textShadow: '0 0 28px rgba(255,215,0,0.55)' }}
                animate={{
                  textShadow: [
                    '0 0 28px rgba(255,215,0,0.55)',
                    '0 0 48px rgba(255,215,0,0.85)',
                    '0 0 28px rgba(255,215,0,0.55)',
                  ],
                }}
                transition={{ duration: 2.8, repeat: Infinity }}
              >
                {username}
              </motion.h1>

              <p className="text-[11px] tracking-[0.22em] text-white/55 mb-0.5">
                OPERADOR DE SISTEMAS
              </p>
              {/* Rank badge */}
              <motion.p
                className="text-[11px] tracking-[0.22em] font-bold mb-1"
                style={{ color: '#FFD700', textShadow: '0 0 12px rgba(255,215,0,0.55)' }}
                animate={{ opacity: [0.7, 1, 0.7] }}
                transition={{ duration: 2.2, repeat: Infinity }}
              >
                {rank.toUpperCase()}
              </motion.p>
              <p
                className="text-[10px] tracking-[0.22em]"
                style={{ color: 'rgba(189,0,255,0.65)' }}
              >
                NIVEL 100 · NEXO VENCIDO
              </p>
            </div>

            {/* RIGHT — Badges */}
            <div className="flex flex-col items-center gap-3 shrink-0">
              {/* DAKI validation badge */}
              <motion.div
                className="border border-[#BD00FF]/55 px-5 py-3 text-center"
                style={{ background: 'rgba(189,0,255,0.07)' }}
                animate={{
                  boxShadow: [
                    '0 0 16px rgba(189,0,255,0.18)',
                    '0 0 32px rgba(189,0,255,0.40)',
                    '0 0 16px rgba(189,0,255,0.18)',
                  ],
                }}
                transition={{ duration: 2, repeat: Infinity }}
              >
                <p className="text-[7px] tracking-[0.45em] text-[#BD00FF]/55 mb-1.5">VALIDACIÓN</p>
                <p
                  className="text-lg font-black tracking-[0.3em]"
                  style={{ color: '#BD00FF', textShadow: '0 0 14px rgba(189,0,255,0.7)' }}
                >
                  DAKI ◈
                </p>
              </motion.div>

              {/* Decorative pixel grid */}
              <div className="grid grid-cols-4 gap-[3px]">
                {Array.from({ length: 16 }).map((_, i) => (
                  <motion.div
                    key={i}
                    className="w-2.5 h-2.5 border border-[#00FF41]"
                    style={{ background: i % 3 === 0 ? 'rgba(0,255,65,0.12)' : 'transparent' }}
                    animate={{ opacity: [0.15, 0.7, 0.15] }}
                    transition={{
                      duration: 1.4,
                      delay: ((i * 0.11) % 1),
                      repeat: Infinity,
                    }}
                  />
                ))}
              </div>
            </div>
          </div>

          {/* Divider */}
          <div className="h-px bg-gradient-to-r from-transparent via-[#FFD700]/18 to-transparent mb-5" />

          {/* ── SIGNATURE ROW ─────────────────────────────────────────────── */}
          <div className="flex justify-center py-3 border-t border-b" style={{ borderColor: 'rgba(255,215,0,0.10)' }}>
            <div className="text-center">
              <p
                className="text-[12px] font-bold italic tracking-[0.18em]"
                style={{ color: '#FFD700', textShadow: '0 0 10px rgba(255,215,0,0.35)', fontStyle: 'italic' }}
              >
                DAKI Neuronal Authority
              </p>
              <p className="text-[7px] tracking-[0.4em] text-white/18 mt-0.5">
                AUTORIDAD CENTRAL DE CERTIFICACIÓN — DAKI EdTech v1.0
              </p>
            </div>
          </div>

          {/* ── FOOTER ROW ─────────────────────────────────────────────────── */}
          <div className="flex items-end justify-between pb-7 pt-4">
            <div>
              <p className="text-[7px] tracking-[0.4em] text-white/18 mb-1">
                IDENTIFICADOR DE CERTIFICADO
              </p>
              <p
                className="text-sm font-bold tracking-[0.3em]"
                style={{ color: '#00FF41', textShadow: '0 0 10px rgba(0,255,65,0.45)' }}
              >
                {certId}
              </p>
            </div>
            <div className="text-right">
              <p className="text-[7px] tracking-[0.4em] text-white/18 mb-1">FECHA DE EMISIÓN</p>
              <p className="text-sm font-bold tracking-[0.18em] text-white/45">{certDate}</p>
            </div>
          </div>
        </div>

        {/* Bottom chromatic bar */}
        <div
          className="h-[3px] w-full"
          style={{
            background:
              'linear-gradient(90deg, #FFD700, #BD00FF 33%, #00FF41 66%, #BD00FF 83%, #FFD700)',
          }}
        />
      </div>
    </motion.div>
  )
}

// ─── Main component ───────────────────────────────────────────────────────────

interface Props {
  onClose?: () => void
}

export default function CertificateReveal({ onClose }: Props) {
  const username    = useUserStore(s => s.username) || 'Operador'
  const userId      = useUserStore(s => s.userId)
  const currentRank = useUserStore(s => s.currentRank) || 'Netzach Operative'
  const [phase, setPhase]             = useState<Phase>('decrypt')
  const [visibleLines, setVisibleLines] = useState(0)
  const [certId]    = useState(generateCertId)
  const [certDate]  = useState(formatDate)
  const [downloading, setDownloading]  = useState(false)

  // ── Download handler ───────────────────────────────────────────────────────
  async function handleDownload() {
    if (downloading || !userId) return
    setDownloading(true)
    try {
      const resp = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL ?? ''}/api/v1/certificate/download?user_id=${userId}`
      )
      if (!resp.ok) {
        const err = await resp.json().catch(() => ({}))
        const msg =
          typeof err.detail === 'object' ? err.detail.message : err.detail ?? 'Error al generar el certificado.'
        alert(msg)
        return
      }
      const blob = await resp.blob()
      const certHeader = resp.headers.get('x-gg-certificate-id') ?? certId
      const url  = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href  = url
      link.download = `GG_Certificado_Nivel100_${certHeader}.pdf`
      document.body.appendChild(link)
      link.click()
      link.remove()
      URL.revokeObjectURL(url)
    } finally {
      setDownloading(false)
    }
  }

  // ── Phase orchestration ────────────────────────────────────────────────────
  useEffect(() => {
    const timers: ReturnType<typeof setTimeout>[] = []

    DECRYPT_LINES.forEach((line, i) => {
      timers.push(setTimeout(() => setVisibleLines(i + 1), line.delay))
    })

    timers.push(setTimeout(() => setPhase('flash'),  FLASH_START))
    timers.push(setTimeout(() => setPhase('reveal'), REVEAL_START))

    return () => timers.forEach(clearTimeout)
  }, [])

  return (
    <motion.div
      className="fixed inset-0 z-[100] bg-[#030308] flex items-center justify-center overflow-hidden"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.18 }}
    >
      {/* Global scanlines */}
      <div
        className="absolute inset-0 pointer-events-none z-10"
        style={{
          backgroundImage:
            'repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,255,65,0.018) 2px,rgba(0,255,65,0.018) 4px)',
        }}
      />

      {/* ── DECRYPT PHASE ───────────────────────────────────────────────────── */}
      <AnimatePresence>
        {phase === 'decrypt' && (
          <motion.div
            className="absolute inset-0 flex flex-col items-center justify-center z-20"
            exit={{ opacity: 0 }}
            transition={{ duration: 0.28 }}
          >
            <MatrixRain />

            {/* Terminal box */}
            <div
              className="relative z-10 w-full max-w-xl mx-5 border border-[#00FF41]/22 bg-black/82 px-6 py-5 font-mono"
              style={{ boxShadow: '0 0 60px rgba(0,255,65,0.07), inset 0 0 30px rgba(0,255,65,0.02)' }}
            >
              {/* Window chrome */}
              <div className="flex items-center gap-2 mb-4 pb-3 border-b border-[#00FF41]/10">
                <div className="w-2.5 h-2.5 rounded-full bg-red-500/55" />
                <div className="w-2.5 h-2.5 rounded-full bg-yellow-500/55" />
                <div className="w-2.5 h-2.5 rounded-full bg-[#00FF41]/55" />
                <span className="ml-2 text-[8px] tracking-[0.42em] text-[#00FF41]/28">
                  DAKI // NÚCLEO DE DESENCRIPTACIÓN — NIVEL 100
                </span>
              </div>

              {/* Terminal lines */}
              <div className="text-[11px] leading-[1.75] min-h-[14.5rem]">
                {DECRYPT_LINES.slice(0, visibleLines).map((line, i) => (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, x: -8 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.1 }}
                    style={{ color: line.gold ? '#FFD700' : '#00FF41' }}
                  >
                    {line.text}
                    {i === visibleLines - 1 && (
                      <motion.span
                        className="inline-block w-[7px] h-[11px] ml-1 bg-[#00FF41] align-middle"
                        animate={{ opacity: [1, 0] }}
                        transition={{ duration: 0.48, repeat: Infinity, repeatType: 'reverse' }}
                      />
                    )}
                  </motion.div>
                ))}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* ── FLASH PHASE ─────────────────────────────────────────────────────── */}
      <AnimatePresence>
        {phase === 'flash' && (
          <motion.div
            className="absolute inset-0 z-30"
            initial={{ opacity: 0 }}
            animate={{ opacity: [0, 1, 0, 0.8, 0] }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.45, times: [0, 0.12, 0.28, 0.55, 1] }}
            style={{
              background:
                'radial-gradient(ellipse at center, rgba(0,255,65,0.22) 0%, rgba(255,215,0,0.06) 60%, transparent 100%)',
            }}
          />
        )}
      </AnimatePresence>

      {/* ── REVEAL PHASE ────────────────────────────────────────────────────── */}
      <AnimatePresence>
        {phase === 'reveal' && (
          <motion.div
            className="relative z-20 w-full max-w-lg mx-5 flex flex-col items-center gap-5"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.3 }}
          >
            {/* Title */}
            <motion.div
              className="text-center"
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
            >
              <motion.p
                className="font-mono font-black text-sm tracking-[0.45em]"
                style={{ color: '#FFD700', textShadow: '0 0 22px rgba(255,215,0,0.65)' }}
                animate={{ opacity: [1, 0.55, 1] }}
                transition={{ duration: 1.8, repeat: Infinity }}
              >
                [ NEXO DESENCRIPTADO ]
              </motion.p>
              <p className="font-mono text-[8px] tracking-[0.55em] text-[#00FF41]/30 mt-1">
                CERTIFICADO PERMANENTE EMITIDO
              </p>
            </motion.div>

            {/* Certificate */}
            <CertCard username={username} certId={certId} certDate={certDate} rank={currentRank} />

            {/* Download button */}
            <motion.button
              className="w-full font-mono text-xs tracking-[0.22em] py-4 border border-[#00FF41]/48 relative overflow-hidden"
              style={{ background: 'rgba(0,255,65,0.04)', color: '#00FF41' }}
              whileHover={{
                backgroundColor: 'rgba(0,255,65,0.08)',
                borderColor: 'rgba(0,255,65,0.85)',
                boxShadow: '0 0 36px rgba(0,255,65,0.32)',
              }}
              whileTap={{ scale: 0.975 }}
              animate={{
                boxShadow: [
                  '0 0 16px rgba(0,255,65,0.10)',
                  '0 0 28px rgba(0,255,65,0.22)',
                  '0 0 16px rgba(0,255,65,0.10)',
                ],
              }}
              transition={{ duration: 2.2, repeat: Infinity }}
              initial={{ opacity: 0, y: 8 }}
              onClick={handleDownload}
              disabled={downloading}
            >
              {/* Shimmer */}
              {!downloading && (
                <motion.span
                  className="absolute inset-0 pointer-events-none"
                  style={{
                    background:
                      'linear-gradient(90deg, transparent 15%, rgba(0,255,65,0.09) 50%, transparent 85%)',
                  }}
                  initial={{ x: '-100%' }}
                  animate={{ x: '200%' }}
                  transition={{ duration: 1.8, repeat: Infinity, repeatDelay: 2 }}
                />
              )}
              <span className="relative z-10">
                {downloading
                  ? '[ GENERANDO_PDF... ]'
                  : '[ DESCARGAR_CREDENCIALES.pdf ]'}
              </span>
            </motion.button>

            {/* Back link */}
            {onClose && (
              <motion.button
                className="font-mono text-[9px] tracking-[0.35em] text-white/20 hover:text-white/50 transition-colors duration-200"
                onClick={onClose}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 1.2 }}
              >
                [ ESC · VOLVER AL NEXO ]
              </motion.button>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  )
}
