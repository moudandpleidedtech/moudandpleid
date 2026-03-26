'use client'

import { useEffect, useRef, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

const API = process.env.NEXT_PUBLIC_API_URL ?? ''
const POLL_INTERVAL = 30_000

// ─── Types ───────────────────────────────────────────────────────────────────

type EventType =
  | 'challenge_complete'
  | 'level_up'
  | 'boss_defeated'
  | 'duel_result'
  | 'league_rank_up'

interface ActivityEvent {
  id: string
  type: EventType
  message: string
  actor: string | null
  target: string | null
  value: number | null
  ts: number
}

// ─── Event type metadata ──────────────────────────────────────────────────────

const EVENT_META: Record<EventType, { icon: string; color: string }> = {
  challenge_complete: { icon: '✓', color: '#00FF41' },
  level_up:          { icon: '↑', color: '#FFD700' },
  boss_defeated:     { icon: '∞', color: '#FF4444' },
  duel_result:       { icon: '⚔', color: '#7DF9FF' },
  league_rank_up:    { icon: '◆', color: '#FF8C00' },
}

function formatRelative(ts: number): string {
  const diff = Math.floor((Date.now() - ts) / 1000)
  if (diff < 5)   return 'ahora'
  if (diff < 60)  return `${diff}s`
  if (diff < 3600) return `${Math.floor(diff / 60)}m`
  return `${Math.floor(diff / 3600)}h`
}

// ─── Single log line ──────────────────────────────────────────────────────────

function EventLine({ event }: { event: ActivityEvent }) {
  const meta = EVENT_META[event.type] ?? { icon: '·', color: '#ffffff' }
  const [, setTick] = useState(0)

  // re-render every 30s so timestamps stay fresh
  useEffect(() => {
    const id = setInterval(() => setTick(t => t + 1), 30_000)
    return () => clearInterval(id)
  }, [])

  return (
    <motion.div
      className="flex items-start gap-2 py-1 border-b border-white/5 last:border-0"
      initial={{ opacity: 0, x: 8 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.25 }}
    >
      {/* Icon */}
      <span
        className="text-[11px] shrink-0 mt-px w-3 text-center"
        style={{ color: meta.color }}
      >
        {meta.icon}
      </span>

      {/* Message */}
      <span className="text-[10px] leading-relaxed text-white/45 flex-1 min-w-0 break-words">
        {event.message}
      </span>

      {/* Timestamp */}
      <span className="text-[9px] text-white/20 shrink-0 mt-px tabular-nums">
        {formatRelative(event.ts)}
      </span>
    </motion.div>
  )
}

// ─── Main component ───────────────────────────────────────────────────────────

export default function LiveActivityFeed() {
  const [events, setEvents] = useState<ActivityEvent[]>([])
  const [connected, setConnected] = useState(false)
  const [blink, setBlink] = useState(true)
  const esRef = useRef<EventSource | null>(null)
  const pollRef = useRef<NodeJS.Timeout | null>(null)
  const seenIds = useRef<Set<string>>(new Set())

  const mergeEvents = (incoming: ActivityEvent[]) => {
    const fresh = incoming.filter(e => !seenIds.current.has(e.id))
    fresh.forEach(e => seenIds.current.add(e.id))
    if (fresh.length === 0) return
    setEvents(prev => {
      const combined = [...fresh, ...prev].slice(0, 40) // keep latest 40
      return combined
    })
  }

  // SSE connection
  useEffect(() => {
    const trySSE = () => {
      const es = new EventSource(`${API}/api/v1/activity/stream`)
      esRef.current = es

      es.onopen = () => setConnected(true)

      es.onmessage = (e) => {
        try {
          const event: ActivityEvent = JSON.parse(e.data)
          mergeEvents([event])
        } catch {
          // ignore malformed messages
        }
      }

      es.onerror = () => {
        setConnected(false)
        es.close()
        esRef.current = null
        // Fallback to polling
        startPolling()
      }
    }

    const startPolling = () => {
      if (pollRef.current) return // already polling
      const poll = async () => {
        try {
          const res = await fetch(`${API}/api/v1/activity/recent?limit=20`)
          if (res.ok) {
            const data: ActivityEvent[] = await res.json()
            mergeEvents(data)
            setConnected(true)
          }
        } catch {
          setConnected(false)
        }
      }
      poll()
      pollRef.current = setInterval(poll, POLL_INTERVAL)
    }

    trySSE()

    return () => {
      esRef.current?.close()
      if (pollRef.current) clearInterval(pollRef.current)
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  // Blink dot
  useEffect(() => {
    const id = setInterval(() => setBlink(b => !b), 1200)
    return () => clearInterval(id)
  }, [])

  return (
    <div className="flex flex-col h-full font-mono">
      {/* Header */}
      <div className="flex items-center gap-2 px-3 py-2 border-b border-white/8 shrink-0">
        <span
          className="w-1.5 h-1.5 rounded-full transition-opacity duration-300"
          style={{
            backgroundColor: connected ? '#00FF41' : '#FF4444',
            opacity: connected ? (blink ? 1 : 0.3) : 0.5,
          }}
        />
        <span className="text-[9px] tracking-[0.3em] text-white/25 uppercase">
          Feed de Actividad
        </span>
        <span className="ml-auto text-[8px] text-white/15 tracking-wider">
          {connected ? 'EN VIVO' : 'OFFLINE'}
        </span>
      </div>

      {/* Event list */}
      <div className="flex-1 overflow-y-auto px-3 py-1 scrollbar-thin scrollbar-track-transparent scrollbar-thumb-white/10">
        {events.length === 0 ? (
          <p className="text-[9px] text-white/15 tracking-widest py-3 text-center">
            — sin actividad reciente —
          </p>
        ) : (
          <AnimatePresence initial={false}>
            {events.map(ev => (
              <EventLine key={ev.id} event={ev} />
            ))}
          </AnimatePresence>
        )}
      </div>

      {/* Footer */}
      <div className="px-3 py-1.5 border-t border-white/8 shrink-0">
        <span className="text-[8px] tracking-widest text-white/12">
          {events.length > 0 ? `${events.length} ENTRADAS` : 'SISTEMA EN ESPERA'}
        </span>
      </div>
    </div>
  )
}
