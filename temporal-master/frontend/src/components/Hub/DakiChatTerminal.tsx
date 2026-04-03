'use client'

/**
 * DakiChatTerminal.tsx — Terminal de Chat con DAKI
 * ──────────────────────────────────────────────────
 * Conecta a POST /api/v1/chat.
 * Área scrolleable de mensajes + input tipo CLI.
 */

import { useEffect, useRef, useState } from 'react'

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? ''

interface Message {
  from:   'daki' | 'operator'
  text:   string
  ts:     number
}

interface Props {
  userId:          string
  openingMessage?: string
}

export default function DakiChatTerminal({ userId, openingMessage }: Props) {
  const [messages,  setMessages]  = useState<Message[]>([
    {
      from: 'daki',
      text: 'Operador en línea. Reporte su estado o solicite asistencia táctica.',
      ts:   Date.now(),
    },
  ])
  const [input,     setInput]     = useState('')
  const [loading,   setLoading]   = useState(false)
  const [cooldown,  setCooldown]  = useState(false)
  const bottomRef    = useRef<HTMLDivElement>(null)
  const inputRef     = useRef<HTMLInputElement>(null)
  const lastSentRef  = useRef(0)
  const COOLDOWN_MS  = 2500

  // Reemplaza el mensaje inicial con el opening message personalizado de DAKI
  useEffect(() => {
    if (openingMessage) {
      setMessages([{ from: 'daki', text: openingMessage, ts: Date.now() }])
    }
  }, [openingMessage])

  // Auto-scroll al último mensaje
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  const sendMessage = async () => {
    const text = input.trim()
    if (!text || loading || cooldown) return

    // Cooldown anti-spam: 2.5s entre envíos para no quemar tokens en ráfagas
    const now = Date.now()
    if (now - lastSentRef.current < COOLDOWN_MS) return
    lastSentRef.current = now
    setCooldown(true)
    setTimeout(() => setCooldown(false), COOLDOWN_MS)

    setInput('')
    setMessages(prev => [...prev, { from: 'operator', text, ts: Date.now() }])
    setLoading(true)

    try {
      const res = await fetch(`${API_BASE}/api/v1/chat`, {
        method:      'POST',
        credentials: 'include',
        headers:     { 'Content-Type': 'application/json' },
        body:        JSON.stringify({ message: text, user_id: userId }),
      })

      const data = await res.json() as { reply?: string; detail?: string }
      const reply = data.reply ?? '[DAKI_SYS] Respuesta no procesada.'
      setMessages(prev => [...prev, { from: 'daki', text: reply, ts: Date.now() }])
    } catch {
      setMessages(prev => [
        ...prev,
        { from: 'daki', text: '[DAKI_SYS] Error de conexión con el satélite principal.', ts: Date.now() },
      ])
    } finally {
      setLoading(false)
      inputRef.current?.focus()
    }
  }

  const handleKey = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') sendMessage()
  }

  return (
    <div className="flex flex-col h-full border border-[#00FF41]/15 bg-black/60">

      {/* ── Header ──────────────────────────────────────────────────────────── */}
      <div className="shrink-0 flex items-center gap-2 px-3 py-2 border-b border-[#00FF41]/10">
        <span
          className="w-1.5 h-1.5 rounded-full bg-[#00FF41]"
          style={{ animation: 'pulse 1.5s ease-in-out infinite' }}
        />
        <span className="text-[8px] tracking-[0.5em] text-[#00FF41]/40 uppercase">
          DAKI // ENLACE TÁCTICO DIRECTO
        </span>
      </div>

      {/* ── Área de mensajes ─────────────────────────────────────────────────── */}
      <div className="flex-1 overflow-y-auto px-3 py-3 space-y-2 min-h-0">
        {messages.map(msg => (
          <div key={msg.ts + msg.from} className="flex flex-col gap-0.5">
            <span className="text-[8px] tracking-[0.4em] text-[#00FF41]/20 uppercase">
              {msg.from === 'daki' ? '> [DAKI]' : '> [OPERADOR]'}
            </span>
            <p
              className={`text-xs leading-5 ${
                msg.from === 'daki'
                  ? 'text-[#00FF41]/85'
                  : 'text-[#00FF41]/50'
              }`}
              style={{ whiteSpace: 'pre-wrap' }}
            >
              {msg.text}
            </p>
          </div>
        ))}

        {/* Indicador de procesando */}
        {loading && (
          <div className="flex flex-col gap-0.5">
            <span className="text-[8px] tracking-[0.4em] text-[#00FF41]/20">{'> [DAKI]'}</span>
            <p className="text-xs text-[#00FF41]/40">
              Procesando señal
              <span className="inline-block ml-0.5 animate-pulse">_</span>
            </p>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {/* ── Input CLI ────────────────────────────────────────────────────────── */}
      <div className="shrink-0 flex items-center gap-2 px-3 py-2.5 border-t border-[#00FF41]/10">
        <span className="text-[#00FF41]/40 text-xs select-none">{'>'}</span>
        <input
          ref={inputRef}
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKey}
          disabled={loading || cooldown}
          placeholder={cooldown ? 'Canal enfriándose...' : 'Escriba su reporte...'}
          className="flex-1 bg-transparent text-[#00FF41] text-xs outline-none border-none caret-[#00FF41] placeholder:text-[#00FF41]/15 disabled:opacity-40"
          autoComplete="off"
          spellCheck={false}
        />
        <button
          onClick={sendMessage}
          disabled={loading || cooldown || !input.trim()}
          className="text-[8px] tracking-[0.3em] text-[#00FF41]/30 hover:text-[#00FF41]/60 disabled:opacity-20 transition-colors"
        >
          {cooldown ? '[···]' : '[SEND]'}
        </button>
      </div>

    </div>
  )
}
