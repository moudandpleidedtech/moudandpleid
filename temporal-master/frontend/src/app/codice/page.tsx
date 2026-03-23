'use client'

import { useEffect, useState, useCallback } from 'react'
import { useRouter } from 'next/navigation'
import { motion, AnimatePresence } from 'framer-motion'
import { useUserStore } from '@/store/userStore'
import MissionBriefing from '@/components/Game/MissionBriefing'

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000'

interface KnowledgeEntry {
  id: string
  title: string
  difficulty_tier: number
  phase: string | null
  level_order: number | null
  theory_content: string | null
  completed: boolean
}

const TIER_LABEL: Record<number, string> = {
  1: 'INICIANTE',
  2: 'INTERMEDIO',
  3: 'AVANZADO',
}

const TIER_COLOR: Record<number, string> = {
  1: '#00FF41',
  2: '#FFD700',
  3: '#FF4444',
}

export default function CodicePage() {
  const router = useRouter()
  const { userId, username, level } = useUserStore()

  const [entries, setEntries] = useState<KnowledgeEntry[]>([])
  const [loading, setLoading] = useState(true)
  const [selected, setSelected] = useState<KnowledgeEntry | null>(null)

  useEffect(() => {
    if (!userId) {
      router.replace('/')
      return
    }
    fetch(`${API_BASE}/api/v1/challenges?user_id=${userId}`)
      .then((r) => r.json())
      .then((data: KnowledgeEntry[]) => {
        // Solo muestra entradas con theory_content
        setEntries(data.filter((e) => e.theory_content))
      })
      .finally(() => setLoading(false))
  }, [userId, router])

  const completedEntries = entries.filter((e) => e.completed)
  const lockedEntries = entries.filter((e) => !e.completed)

  const handleClose = useCallback(() => setSelected(null), [])

  return (
    <div className="min-h-screen bg-[#050A05] font-mono text-[#00FF41]">

      {/* Scanlines */}
      <div
        className="fixed inset-0 pointer-events-none z-0 opacity-[0.025]"
        style={{
          backgroundImage:
            'repeating-linear-gradient(0deg,transparent,transparent 3px,#00FF41 3px,#00FF41 4px)',
        }}
      />

      {/* Cabecera */}
      <header className="relative z-10 flex items-center justify-between px-6 py-3 bg-[#030803] border-b border-[#00FF41]/15">
        <div className="flex items-center gap-4">
          <button
            onClick={() => router.push('/misiones')}
            className="text-[#00FF41]/35 hover:text-[#00FF41]/70 text-xs tracking-widest transition-colors"
          >
            ← MISIONES
          </button>
          <span className="text-[#00FF41]/15">|</span>
          <span
            className="font-black tracking-[0.2em] text-sm text-[#00FF41]"
            style={{ textShadow: '0 0 10px #00FF4150' }}
          >
            CÓDICE
          </span>
          <span className="text-[#00FF41]/20 text-xs tracking-widest">{'// BÓVEDA DE CONOCIMIENTO'}</span>
        </div>
        <div className="flex items-center gap-5 text-xs text-[#00FF41]/50">
          <span>{username}</span>
          <span>RANGO <strong className="text-[#00FF41]">{level}</strong></span>
        </div>
      </header>

      <main className="relative z-10 max-w-2xl mx-auto px-6 py-10">

        {/* Título */}
        <div className="mb-8">
          <h1 className="text-2xl font-black tracking-[0.15em] mb-1">BÓVEDA DE CONOCIMIENTO</h1>
          <p className="text-[#00FF41]/35 text-xs tracking-widest leading-relaxed">
            Consulta libremente la teoría de los módulos que has superado.<br />
            Los registros bloqueados se desbloquean al completar su misión.
          </p>
          {/* Barra de progreso */}
          <div className="mt-4 h-px bg-[#00FF41]/10 relative overflow-hidden">
            <motion.div
              className="absolute left-0 top-0 h-full bg-[#00FF41]"
              initial={{ width: 0 }}
              animate={{
                width: entries.length
                  ? `${(completedEntries.length / entries.length) * 100}%`
                  : '0%',
              }}
              transition={{ duration: 0.9, ease: 'easeOut' }}
            />
          </div>
          <div className="mt-1 text-[10px] text-[#00FF41]/25 tracking-widest">
            {completedEntries.length}/{entries.length} REGISTROS DESBLOQUEADOS
          </div>
        </div>

        {loading ? (
          <p className="text-[#00FF41]/30 text-xs tracking-widest animate-pulse">
            CARGANDO BÓVEDA...
          </p>
        ) : (
          <div className="flex flex-col gap-3">

            {/* Entradas desbloqueadas */}
            {completedEntries.map((entry, idx) => (
              <motion.button
                key={entry.id}
                initial={{ opacity: 0, x: -16 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: idx * 0.06 }}
                onClick={() => setSelected(entry)}
                className="w-full text-left px-5 py-4 border border-[#00FF41]/30 bg-[#030D05] hover:border-[#00FF41]/70 hover:bg-[#00FF41]/5 transition-all duration-150 group"
              >
                <div className="flex items-center justify-between gap-4">
                  <div className="flex items-center gap-3 min-w-0">
                    <span className="text-[#00FF41]/25 text-xs w-5 shrink-0">
                      {String(entry.level_order ?? idx + 1).padStart(2, '0')}
                    </span>
                    <div className="min-w-0">
                      <div className="text-sm font-bold truncate group-hover:text-[#00FF41] transition-colors">
                        {entry.title}
                      </div>
                      <div className="text-[10px] text-[#00FF41]/35 tracking-widest mt-0.5"
                        style={{ color: `${TIER_COLOR[entry.difficulty_tier]}50` }}>
                        {TIER_LABEL[entry.difficulty_tier]}
                      </div>
                    </div>
                  </div>
                  <div className="shrink-0 flex items-center gap-2">
                    <span
                      className="text-[#00FF41] text-xs"
                      style={{ textShadow: '0 0 6px #00FF41' }}
                    >
                      ✓ DESBLOQUEADO
                    </span>
                    <span className="text-[#00FF41]/40 text-xs group-hover:text-[#00FF41] transition-colors">▶</span>
                  </div>
                </div>
              </motion.button>
            ))}

            {/* Separador si hay entradas bloqueadas */}
            {lockedEntries.length > 0 && completedEntries.length > 0 && (
              <div className="flex items-center gap-3 my-3">
                <div className="h-px flex-1 bg-[#00FF41]/10" />
                <span className="text-[#00FF41]/20 text-[10px] tracking-[0.3em]">REGISTROS BLOQUEADOS</span>
                <div className="h-px flex-1 bg-[#00FF41]/10" />
              </div>
            )}

            {/* Entradas bloqueadas */}
            {lockedEntries.map((entry, idx) => (
              <motion.div
                key={entry.id}
                initial={{ opacity: 0, x: -16 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: (completedEntries.length + idx) * 0.06 }}
                className="px-5 py-4 border border-[#00FF41]/8 opacity-30 cursor-not-allowed select-none"
              >
                <div className="flex items-center justify-between gap-4">
                  <div className="flex items-center gap-3 min-w-0">
                    <span className="text-[#00FF41]/25 text-xs w-5 shrink-0">
                      {String(entry.level_order ?? completedEntries.length + idx + 1).padStart(2, '0')}
                    </span>
                    <div className="min-w-0">
                      <div className="text-sm font-bold truncate text-[#00FF41]/50">
                        ████ ██████ ████████
                      </div>
                      <div className="text-[10px] text-[#00FF41]/20 tracking-widest mt-0.5">
                        CLASIFICADO
                      </div>
                    </div>
                  </div>
                  <span className="text-[#00FF41]/25 text-xs tracking-widest shrink-0">
                    BLOQUEADO
                  </span>
                </div>
              </motion.div>
            ))}

          </div>
        )}
      </main>

      {/* Modal de lectura de teoría */}
      <AnimatePresence>
        {selected && (
          <motion.div
            className="fixed inset-0 z-[200] flex flex-col"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <div
              className="absolute inset-0 bg-black/80"
              onClick={handleClose}
            />
            <motion.div
              className="relative z-10 m-auto w-full max-w-2xl h-[80vh] flex flex-col bg-[#050A05] border border-[#00FF41]/30 overflow-hidden"
              style={{ boxShadow: '0 0 60px #00FF4115' }}
              initial={{ scale: 0.94, y: 20 }}
              animate={{ scale: 1, y: 0 }}
              exit={{ scale: 0.94, y: 20 }}
              transition={{ type: 'spring', stiffness: 300, damping: 28 }}
            >
              {/* Botón cerrar */}
              <button
                onClick={handleClose}
                className="absolute top-3 right-4 z-20 text-[#00FF41]/35 hover:text-[#00FF41] text-xs tracking-widest transition-colors"
              >
                [ESC] CERRAR
              </button>

              <MissionBriefing
                title={selected.title}
                theoryContent={selected.theory_content!}
                challengeId={selected.id}
                onInitialize={handleClose}
              />
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

    </div>
  )
}
