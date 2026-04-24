'use client'

import { useState } from 'react'

const API = process.env.NEXT_PUBLIC_API_URL ?? ''

export default function NewsletterForm({ source = 'blog' }: { source?: string }) {
  const [email,   setEmail]   = useState('')
  const [status,  setStatus]  = useState<'idle' | 'loading' | 'ok' | 'error'>('idle')

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!email.trim()) return
    setStatus('loading')
    try {
      const res = await fetch(`${API}/api/v1/newsletter/subscribe`, {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify({ email: email.trim(), source }),
      })
      setStatus(res.ok ? 'ok' : 'error')
    } catch {
      setStatus('error')
    }
  }

  if (status === 'ok') {
    return (
      <div
        className="border-l-2 border-[#00FF41] pl-4 py-2 font-mono"
        style={{ background: 'rgba(0,255,65,0.03)' }}
      >
        <p className="text-[9px] tracking-[0.4em] text-[#00FF41]/40 uppercase mb-1">
          {'// SUSCRIPCIÓN CONFIRMADA'}
        </p>
        <p className="text-sm font-black text-white/75 uppercase tracking-wide">
          Bienvenido al Nexo.
        </p>
        <p className="text-[10px] text-white/35 mt-1">
          Revisá tu casilla — primer despacho en camino.
        </p>
      </div>
    )
  }

  return (
    <div
      className="border border-[#00FF41]/15 p-5 font-mono"
      style={{ background: 'rgba(0,255,65,0.02)' }}
    >
      <p className="text-[8px] tracking-[0.55em] text-[#00FF41]/30 uppercase mb-2">
        {'// TRANSMISIONES DEL NEXO'}
      </p>
      <p className="text-sm font-black text-white/70 uppercase tracking-wide leading-snug mb-1">
        Python real. Cada semana.
      </p>
      <p className="text-[10px] text-white/32 leading-relaxed mb-4">
        Artículos aplicados, movimientos del leaderboard y novedades de la plataforma.
        Sin spam. Sin teoría muerta.
      </p>

      <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-2">
        <input
          type="email"
          value={email}
          onChange={e => setEmail(e.target.value)}
          placeholder="tu@email.com"
          required
          disabled={status === 'loading'}
          className="flex-1 bg-transparent border border-[#00FF41]/20 px-4 py-2.5 text-[11px] text-white/70 placeholder-white/20 tracking-wide outline-none focus:border-[#00FF41]/45 transition-colors font-mono"
        />
        <button
          type="submit"
          disabled={status === 'loading'}
          className="border border-[#00FF41]/35 text-[9px] tracking-[0.38em] uppercase text-[#00FF41] px-5 py-2.5 transition-all duration-200 hover:border-[#00FF41]/65 disabled:opacity-40 whitespace-nowrap"
          style={{ background: 'rgba(0,255,65,0.04)' }}
        >
          {status === 'loading' ? 'ENVIANDO...' : 'UNIRSE →'}
        </button>
      </form>

      {status === 'error' && (
        <p className="text-[9px] text-[#FF6B6B]/70 tracking-wide mt-2">
          Error al suscribirse. Intentá de nuevo.
        </p>
      )}
    </div>
  )
}
