'use client'

import { useState, useCallback } from 'react'
import { useRouter } from 'next/navigation'
import { motion, AnimatePresence } from 'framer-motion'
import { useUserStore } from '@/store/userStore'

const API = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000'

// ─── Concept list ─────────────────────────────────────────────────────────────

const CONCEPTS = [
  { id: 'funciones',         label: 'Funciones',   icon: 'ƒ' },
  { id: 'recursión',         label: 'Recursión',   icon: '↻' },
  { id: 'listas',            label: 'Listas',      icon: '[ ]' },
  { id: 'diccionarios',      label: 'Diccionarios',icon: '{ }' },
  { id: 'clases',            label: 'Clases',      icon: '◈' },
  { id: 'decoradores',       label: 'Decoradores', icon: '@' },
  { id: 'generadores',       label: 'Generadores', icon: '⟳' },
  { id: 'comprensiones',     label: 'Comprensiones',icon: '⊂' },
  { id: 'manejo de errores', label: 'Errores',     icon: '⚠' },
  { id: 'strings',           label: 'Strings',     icon: '"…"' },
  { id: 'bucles',            label: 'Bucles',      icon: '∞' },
  { id: 'lambda',            label: 'Lambda',      icon: 'λ' },
]

const DIFFICULTY_LABELS: Record<number, { label: string; color: string }> = {
  1:  { label: 'TRIVIAL',  color: '#00FF41' },
  2:  { label: 'TRIVIAL',  color: '#00FF41' },
  3:  { label: 'BÁSICO',   color: '#7DF9FF' },
  4:  { label: 'BÁSICO',   color: '#7DF9FF' },
  5:  { label: 'MEDIO',    color: '#FFD700' },
  6:  { label: 'MEDIO',    color: '#FFD700' },
  7:  { label: 'DIFÍCIL',  color: '#FF8C00' },
  8:  { label: 'DIFÍCIL',  color: '#FF8C00' },
  9:  { label: 'EXTREMO',  color: '#FF4444' },
  10: { label: 'EXTREMO',  color: '#FF4444' },
}

const DDA_META: Record<string, { label: string; desc: string; color: string; icon: string }> = {
  mastery_push: {
    label: 'MODO DESAFÍO',
    desc: 'Tu dominio del concepto es alto — misión de élite con escudos cuánticos.',
    color: '#FF8C00',
    icon: '⬆',
  },
  stealth_review: {
    label: 'REPASO ENCUBIERTO',
    desc: 'Escudos enemigos bajos — calibra tu protocolo antes del asalto final.',
    color: '#7DF9FF',
    icon: '⚡',
  },
  standard: {
    label: '',
    desc: '',
    color: '#ffffff',
    icon: '',
  },
}

// ─── Types ────────────────────────────────────────────────────────────────────

interface LootOut {
  key: string
  label: string
  rarity: string
  color: string
}

interface BountyOut {
  id: string
  title: string
  description: string
  initial_code: string
  expected_output: string
  difficulty_tier: number
  base_xp_reward: number
  xp_multiplier: number
  challenge_type: string
  dda_mode: string
  dda_override: boolean
  adjusted_difficulty: number
  second_concept: string | null
  mastery_score: number
  loot: LootOut
}

type Phase = 'configure' | 'generating' | 'preview'

// ─── Animated generating screen ───────────────────────────────────────────────

function GeneratingScreen({ concept }: { concept: string }) {
  const lines = [
    `> CONECTANDO CON ENIGMA CORE…`,
    `> LEYENDO PERFIL DE MAESTRÍA…`,
    `> ANALIZANDO CONCEPTO: ${concept.toUpperCase()}`,
    `> DDA CALCULANDO DIFICULTAD ÓPTIMA…`,
    `> GENERANDO PROTOCOLO DE MISIÓN…`,
    `> COMPILANDO CÓDIGO INFECTADO…`,
  ]
  return (
    <motion.div className="flex flex-col gap-3 py-10" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
      {lines.map((line, i) => (
        <motion.p
          key={i}
          className="text-[11px] font-mono text-[#00FF41]/60 tracking-wider"
          initial={{ opacity: 0, x: -10 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: i * 0.32 }}
        >
          {line}
        </motion.p>
      ))}
      <motion.div
        className="flex items-center gap-2 mt-4"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: lines.length * 0.32 }}
      >
        <motion.span
          className="w-2 h-2 rounded-full bg-[#00FF41]"
          animate={{ opacity: [1, 0.2, 1] }}
          transition={{ duration: 0.7, repeat: Infinity }}
        />
        <span className="text-[10px] text-[#00FF41]/40 tracking-[0.3em]">CLAUDE OPUS PROCESANDO…</span>
      </motion.div>
    </motion.div>
  )
}

// ─── DDA mode badge ───────────────────────────────────────────────────────────

function DDABadge({ mode, secondConcept, masteryScore }: {
  mode: string
  secondConcept: string | null
  masteryScore: number
}) {
  const meta = DDA_META[mode]
  if (!meta || mode === 'standard') return null

  return (
    <motion.div
      className="border px-4 py-3 mb-1"
      style={{ borderColor: `${meta.color}40`, backgroundColor: `${meta.color}08` }}
      initial={{ opacity: 0, x: -8 }}
      animate={{ opacity: 1, x: 0 }}
    >
      <div className="flex items-center gap-2 mb-1">
        <span style={{ color: meta.color }} className="text-sm font-bold">{meta.icon}</span>
        <span className="text-[10px] tracking-[0.3em] font-bold" style={{ color: meta.color }}>
          {meta.label}
        </span>
        {mode === 'mastery_push' && (
          <span className="text-[9px] text-white/30 ml-auto">
            MAESTRÍA {masteryScore.toFixed(0)}/100
          </span>
        )}
      </div>
      <p className="text-[10px] text-white/45 leading-relaxed">{meta.desc}</p>
      {secondConcept && (
        <p className="text-[10px] mt-1" style={{ color: meta.color }}>
          + CONCEPTO SECUNDARIO: <strong>{secondConcept.toUpperCase()}</strong>
        </p>
      )}
    </motion.div>
  )
}

// ─── Loot display ─────────────────────────────────────────────────────────────

function LootDisplay({ loot, xpMultiplier }: { loot: LootOut; xpMultiplier: number }) {
  return (
    <div className="flex items-center gap-3 px-4 py-2.5 border border-white/8 bg-[#080808]">
      <div className="flex flex-col gap-0.5 flex-1">
        <span className="text-[9px] tracking-[0.3em] text-white/25">LOOT POSIBLE</span>
        <span className="text-[11px] font-bold tracking-wider" style={{ color: loot.color }}>
          {loot.label}
        </span>
      </div>
      <div className="flex flex-col items-end gap-0.5">
        <span
          className="text-[9px] tracking-[0.25em] px-1.5 py-0.5"
          style={{ color: loot.color, border: `1px solid ${loot.color}40` }}
        >
          {loot.rarity}
        </span>
        {xpMultiplier > 1 && (
          <span className="text-[9px] text-[#FFD700] tracking-wider font-bold">
            {xpMultiplier}× XP
          </span>
        )}
      </div>
    </div>
  )
}

// ─── Bounty preview card ──────────────────────────────────────────────────────

function BountyPreview({
  bounty, concept, difficulty, onPlay, onRegenerate,
}: {
  bounty: BountyOut
  concept: string
  difficulty: number
  onPlay: () => void
  onRegenerate: () => void
}) {
  const diffMeta = DIFFICULTY_LABELS[Math.round(bounty.adjusted_difficulty)] ?? DIFFICULTY_LABELS[difficulty]
  const tierLabel = ['', 'INICIANTE', 'INTERMEDIO', 'AVANZADO'][bounty.difficulty_tier] ?? ''
  const finalXp = Math.round(bounty.base_xp_reward)

  return (
    <motion.div className="flex flex-col gap-4" initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}>

      {/* DDA indicator */}
      <DDABadge
        mode={bounty.dda_mode}
        secondConcept={bounty.second_concept}
        masteryScore={bounty.mastery_score}
      />

      {/* Main card */}
      <div className="border border-[#FFD700]/30 bg-[#0A0A08] p-5">
        <div className="flex items-start justify-between gap-4 mb-3">
          <div className="flex flex-col gap-1">
            <span className="text-[9px] tracking-[0.4em] text-[#FFD700]/40">
              BOUNTY · {concept.toUpperCase()} · {tierLabel}
            </span>
            <h2
              className="text-lg font-black tracking-wider text-[#FFD700]"
              style={{ textShadow: '0 0 12px #FFD70040' }}
            >
              {bounty.title}
            </h2>
          </div>
          <div className="shrink-0 text-right">
            <span className="text-xl font-black" style={{ color: diffMeta.color }}>
              {bounty.adjusted_difficulty.toFixed(0)}
            </span>
            <span className="block text-[9px] tracking-widest" style={{ color: diffMeta.color }}>/10</span>
          </div>
        </div>

        <p className="text-[11px] text-white/55 leading-relaxed border-l-2 border-[#FFD700]/20 pl-3">
          {bounty.description}
        </p>

        <div className="flex items-center gap-4 mt-4 pt-3 border-t border-white/8">
          <span className="text-[10px] tracking-widest text-white/30">RECOMPENSA:</span>
          <span className="text-sm font-bold text-[#FFD700]" style={{ textShadow: '0 0 8px #FFD70060' }}>
            {finalXp} XP
          </span>
          {bounty.xp_multiplier > 1 && (
            <span className="text-[10px] text-[#FFD700]/60">({bounty.xp_multiplier}× multiplicador)</span>
          )}
          <span className="text-[10px] tracking-widest text-white/20 ml-auto">{diffMeta.label}</span>
        </div>
      </div>

      {/* Loot */}
      <LootDisplay loot={bounty.loot} xpMultiplier={bounty.xp_multiplier} />

      {/* Code preview */}
      <div className="border border-white/10 bg-[#080808]">
        <div className="flex items-center gap-2 px-3 py-1.5 border-b border-white/8">
          <span className="w-1.5 h-1.5 rounded-full bg-[#FFD700]/50" />
          <span className="text-[9px] tracking-widest text-white/25">CÓDIGO COMPROMETIDO</span>
        </div>
        <pre className="text-[11px] text-[#00FF41]/70 font-mono p-4 overflow-x-auto max-h-40 leading-relaxed">
          {bounty.initial_code}
        </pre>
      </div>

      {/* Actions */}
      <div className="flex gap-3">
        <motion.button
          onClick={onPlay}
          className="flex-1 py-3 bg-[#FFD700] hover:bg-[#FFD700]/85 text-black text-sm tracking-[0.25em] font-black transition-all"
          whileTap={{ scale: 0.98 }}
        >
          ACEPTAR BOUNTY ▶
        </motion.button>
        <button
          onClick={onRegenerate}
          className="px-4 py-3 border border-white/20 hover:border-white/40 text-white/40 hover:text-white/70 text-[11px] tracking-widest transition-all"
        >
          ↻ NUEVA
        </button>
      </div>
    </motion.div>
  )
}

// ─── Main Page ────────────────────────────────────────────────────────────────

export default function BountyPage() {
  const router = useRouter()
  const { userId, level } = useUserStore()

  const [phase, setPhase] = useState<Phase>('configure')
  const [selectedConcept, setSelectedConcept] = useState<string | null>(null)
  const [difficulty, setDifficulty] = useState(5)
  const [bounty, setBounty] = useState<BountyOut | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleGenerate = useCallback(async () => {
    if (!userId || !selectedConcept) return
    setPhase('generating')
    setError(null)

    try {
      const res = await fetch(`${API}/api/v1/bounty/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId,
          user_level: level,
          target_concept: selectedConcept,
          difficulty_modifier: difficulty,
        }),
      })
      if (!res.ok) {
        const body = await res.json().catch(() => ({}))
        throw new Error((body as { detail?: string }).detail ?? 'Error generando la misión')
      }
      const data: BountyOut = await res.json()
      setBounty(data)
      setPhase('preview')
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Error desconocido')
      setPhase('configure')
    }
  }, [userId, selectedConcept, difficulty, level])

  const handlePlay = () => { if (bounty) router.push(`/challenge/${bounty.id}`) }
  const handleRegenerate = () => { setBounty(null); setPhase('configure') }

  const diffMeta = DIFFICULTY_LABELS[difficulty]

  return (
    <div className="min-h-screen bg-[#050505] font-mono text-white flex flex-col items-center py-10 px-4">

      {/* Header */}
      <div className="w-full max-w-2xl mb-8">
        <motion.h1
          className="text-2xl font-black tracking-[0.3em] text-[#FFD700]"
          style={{ textShadow: '0 0 25px #FFD70050' }}
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
        >
          TABLERO DE BOUNTIES
        </motion.h1>
        <p className="text-[10px] tracking-[0.3em] text-white/25 mt-1">
          MISIONES GENERADAS POR IA · DIFICULTAD ADAPTATIVA · RECOMPENSAS DINÁMICAS
        </p>
      </div>

      {/* Error */}
      <AnimatePresence>
        {error && (
          <motion.div
            className="w-full max-w-2xl mb-4 border border-[#FF4444]/50 bg-[#FF4444]/10 px-4 py-3 text-[11px] tracking-wider text-[#FF4444]"
            initial={{ opacity: 0, y: -8 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}
          >
            ⚠ {error}
          </motion.div>
        )}
      </AnimatePresence>

      <div className="w-full max-w-2xl">
        <AnimatePresence mode="wait">

          {/* ── CONFIGURE ── */}
          {phase === 'configure' && (
            <motion.div key="configure" className="flex flex-col gap-7" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>

              {/* Info strip */}
              <div className="border border-white/8 bg-[#080808] px-4 py-2.5 flex gap-6 text-[9px] tracking-widest text-white/30">
                <span>◆ Maestría &gt;80 → Dificultad sube a 8 + concepto nuevo</span>
                <span>⚡ Maestría &lt;40 + 3 fallos → Repaso encubierto</span>
              </div>

              {/* Concept grid */}
              <div>
                <p className="text-[10px] tracking-[0.35em] text-white/30 mb-3">01 · SELECCIONA EL CONCEPTO</p>
                <div className="grid grid-cols-3 sm:grid-cols-4 gap-2">
                  {CONCEPTS.map(c => (
                    <button
                      key={c.id}
                      onClick={() => setSelectedConcept(c.id)}
                      className={`flex flex-col items-center gap-1 py-3 px-2 border text-center transition-all duration-150 ${
                        selectedConcept === c.id
                          ? 'border-[#FFD700] bg-[#FFD700]/10 text-[#FFD700]'
                          : 'border-white/10 text-white/40 hover:border-white/30 hover:text-white/70'
                      }`}
                    >
                      <span className="text-sm">{c.icon}</span>
                      <span className="text-[9px] tracking-[0.2em]">{c.label.toUpperCase()}</span>
                    </button>
                  ))}
                </div>
              </div>

              {/* Difficulty */}
              <div>
                <div className="flex items-center justify-between mb-3">
                  <p className="text-[10px] tracking-[0.35em] text-white/30">02 · DIFICULTAD DESEADA</p>
                  <span className="text-[11px] font-bold tracking-wider" style={{ color: diffMeta.color }}>
                    {difficulty} — {diffMeta.label}
                  </span>
                </div>
                <input
                  type="range" min={1} max={10} step={1} value={difficulty}
                  onChange={e => setDifficulty(Number(e.target.value))}
                  className="w-full h-1 appearance-none bg-white/10 outline-none cursor-pointer"
                  style={{ accentColor: diffMeta.color }}
                />
                <div className="flex justify-between mt-1">
                  <span className="text-[8px] text-white/20">TRIVIAL</span>
                  <span className="text-[8px] text-white/20">EXTREMO</span>
                </div>
              </div>

              <motion.button
                onClick={handleGenerate}
                disabled={!selectedConcept}
                className="w-full py-4 border-2 border-[#FFD700]/60 hover:border-[#FFD700] bg-[#FFD700]/5 hover:bg-[#FFD700]/12 text-[#FFD700] text-sm tracking-[0.3em] font-bold disabled:opacity-30 disabled:cursor-not-allowed transition-all duration-200"
                whileHover={selectedConcept ? { scale: 1.01 } : {}}
                whileTap={selectedConcept ? { scale: 0.99 } : {}}
              >
                GENERAR MISIÓN ◆
                {!selectedConcept && (
                  <span className="block text-[9px] tracking-[0.4em] text-[#FFD700]/40 mt-1 font-normal">
                    SELECCIONA UN CONCEPTO PRIMERO
                  </span>
                )}
              </motion.button>

              <button
                onClick={() => router.push('/misiones')}
                className="text-[10px] tracking-widest text-white/20 hover:text-white/40 transition-colors text-center"
              >
                ← VOLVER AL CENTRO DE MANDO
              </button>
            </motion.div>
          )}

          {/* ── GENERATING ── */}
          {phase === 'generating' && selectedConcept && (
            <motion.div key="generating" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
              <GeneratingScreen concept={selectedConcept} />
            </motion.div>
          )}

          {/* ── PREVIEW ── */}
          {phase === 'preview' && bounty && selectedConcept && (
            <motion.div key="preview" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
              <BountyPreview
                bounty={bounty}
                concept={selectedConcept}
                difficulty={difficulty}
                onPlay={handlePlay}
                onRegenerate={handleRegenerate}
              />
            </motion.div>
          )}

        </AnimatePresence>
      </div>
    </div>
  )
}
