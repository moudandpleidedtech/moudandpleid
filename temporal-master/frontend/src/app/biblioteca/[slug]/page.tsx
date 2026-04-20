'use client'

import { use, useEffect, useState, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import Link from 'next/link'

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? ''

// ─── Data ─────────────────────────────────────────────────────────────────────

const PACKS: Record<string, {
  title: string
  subtitle: string
  color: string
  hotmart: string
  price: string
  ebooks: { title: string; desc: string; chapters: string[] }[]
}> = {
  'el-negocio-solo': {
    title:    'El Negocio Solo',
    subtitle: '4 ebooks para construir un negocio digital que funciona sin que estés mirando',
    color:    '#00FF41',
    hotmart:  'https://go.hotmart.com/C105461511Y',
    price:    '$27 USD',
    ebooks: [
      {
        title: 'El Freelancer de $3K',
        desc:  'De cero a tus primeros clientes cobrando lo que valés — con IA como ventaja',
        chapters: [
          'Capítulo 1 — El modelo que cambia todo: servicio + IA',
          'Capítulo 2 — Tu propuesta de valor irrechazable',
          'Capítulo 3 — Cómo conseguir los primeros clientes',
          'Capítulo 4 — Cerrar, cobrar y escalar',
        ],
      },
      {
        title: 'Emails que Venden',
        desc:  'El sistema completo de email marketing con IA para convertir suscriptores en compradores',
        chapters: [
          'Capítulo 1 — Por qué el email sigue siendo el canal más rentable',
          'Capítulo 2 — La lista que vale más que tus seguidores',
          'Capítulo 3 — Secuencias que venden solas',
          'Capítulo 4 — Automatización y métricas que importan',
        ],
      },
      {
        title: 'La Ventaja Injusta',
        desc:  'Automatiza tu trabajo con IA en 48 horas, sin código, sin excusas',
        chapters: [
          'Capítulo 1 — Qué es automatizar en serio (y qué no lo es)',
          'Capítulo 2 — Las 3 herramientas que necesitás (y nada más)',
          'Capítulo 3 — Tus primeros 5 flujos de trabajo',
          'Capítulo 4 — Escalá sin contratar',
        ],
      },
      {
        title: 'Python en 7 Días',
        desc:  'Para automatizar lo que odiás hacer — sin haber programado nunca',
        chapters: [
          'Día 1 — Setup: tu computadora lista en 30 minutos',
          'Día 2-3 — Variables, funciones y lógica básica',
          'Día 4-5 — Automatizaciones reales con archivos y web',
          'Día 6-7 — Tu primer script productivo deployado',
        ],
      },
    ],
  },
  'automatiza-con-ia': {
    title:    'Automatiza tu Trabajo con IA',
    subtitle: '4 ebooks para multiplicar tu output con herramientas de IA sin contratar a nadie',
    color:    '#00CFFF',
    hotmart:  'https://go.hotmart.com/G105459604D',
    price:    '$27 USD',
    ebooks: [
      {
        title: 'IA para Creadores',
        desc:  'Cómo producir 30 días de contenido en 3 horas con Claude',
        chapters: [
          'Capítulo 1 — El problema real con el contenido',
          'Capítulo 2 — La mentalidad correcta con IA',
          'Capítulo 3 — Tu voz, no la de la IA',
          'Capítulo 4 — El sistema de producción en 3 horas',
        ],
      },
      {
        title: '50 Flujos con Claude',
        desc:  'Para duplicar tu productividad sin saber programar',
        chapters: [
          'Categoría 1 — Emails y Comunicación (flujos 1-10)',
          'Categoría 2 — Investigación y Análisis (flujos 11-20)',
          'Categoría 3 — Creación de Contenido (flujos 21-35)',
          'Categoría 4 — Operaciones y Negocios (flujos 36-50)',
        ],
      },
      {
        title: 'Make en 5 Días',
        desc:  'Cómo automatizar tu trabajo sin escribir una sola línea de código',
        chapters: [
          'Día 1 — Cómo piensa Make (y cómo empezar a pensar como Make)',
          'Día 2 — Tu primera automatización real',
          'Día 3 — Conectar apps y manejar datos',
          'Día 4-5 — Flujos avanzados y casos de uso de negocio',
        ],
      },
      {
        title: 'Notion para Humanos',
        desc:  '7 templates listos para usar y dejar de perder el hilo',
        chapters: [
          'Capítulo 1 — Por qué tu sistema actual no funciona',
          'Capítulo 2 — Notion 101: lo único que necesitás saber',
          'Capítulo 3 — Los 7 Templates (Dashboard, Proyectos, CRM, y más)',
          'Capítulo 4 — Automatizaciones con Notion y otras apps',
        ],
      },
    ],
  },
}

// ─── Votes component ──────────────────────────────────────────────────────────

function VotingPanel() {
  const [votes, setVotes]     = useState<{ negocios: number; tecnologia: number } | null>(null)
  const [voted, setVoted]     = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const fetchVotes = useCallback(async () => {
    try {
      const r = await fetch(`${API_BASE}/api/v1/votes`)
      if (r.ok) setVotes(await r.json())
    } catch { /* silent */ }
  }, [])

  useEffect(() => {
    fetchVotes()
    const id = setInterval(fetchVotes, 8000)
    return () => clearInterval(id)
  }, [fetchVotes])

  async function castVote(cat: string) {
    if (voted || loading) return
    setLoading(true)
    try {
      const r = await fetch(`${API_BASE}/api/v1/votes/${cat}`, { method: 'POST' })
      if (r.ok) {
        setVotes(await r.json())
        setVoted(cat)
      }
    } finally {
      setLoading(false)
    }
  }

  const total = votes ? votes.negocios + votes.tecnologia : 0
  const pctN  = total > 0 ? Math.round((votes!.negocios   / total) * 100) : 50
  const pctT  = total > 0 ? Math.round((votes!.tecnologia / total) * 100) : 50

  return (
    <div className="border border-white/[0.06] bg-[#0A0A0A] p-6 mt-8">
      <p className="text-[8px] tracking-[0.6em] text-white/30 uppercase mb-2">
        {'// PROTOCOLO DE VOTACIÓN — PRÓXIMOS EBOOKS'}
      </p>
      <p className="text-white/70 text-sm font-bold tracking-wide mb-1">
        ¿Sobre qué querés que sean los próximos libros?
      </p>
      <p className="text-white/30 text-[10px] mb-6">
        Tu voto define el contenido que viene. Resultados en tiempo real.
      </p>

      <div className="grid grid-cols-2 gap-4 mb-6">
        {[
          { cat: 'negocios',   label: 'NEGOCIOS',    emoji: '💼', color: '#00FF41', pct: pctN },
          { cat: 'tecnologia', label: 'TECNOLOGÍA',  emoji: '⚡', color: '#00CFFF', pct: pctT },
        ].map(({ cat, label, emoji, color, pct }) => (
          <button
            key={cat}
            onClick={() => castVote(cat)}
            disabled={!!voted || loading}
            className="relative p-4 border text-left transition-all disabled:cursor-not-allowed overflow-hidden"
            style={{
              borderColor: voted === cat ? color : 'rgba(255,255,255,0.08)',
              background:  voted === cat ? `${color}11` : '#0A0A0A',
            }}
          >
            {/* barra de progreso */}
            <div
              className="absolute bottom-0 left-0 h-[2px] transition-all duration-700"
              style={{ width: votes ? `${pct}%` : '50%', background: color }}
            />

            <div className="text-2xl mb-2">{emoji}</div>
            <p className="text-[10px] tracking-[0.4em] font-bold uppercase mb-1" style={{ color }}>
              {label}
            </p>
            <AnimatePresence mode="wait">
              {votes ? (
                <motion.p
                  key={pct}
                  initial={{ opacity: 0, y: 4 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="text-white/50 text-xs font-mono"
                >
                  {pct}% · {cat === 'negocios' ? votes.negocios : votes.tecnologia} votos
                </motion.p>
              ) : (
                <p className="text-white/20 text-xs">cargando...</p>
              )}
            </AnimatePresence>

            {voted === cat && (
              <span className="absolute top-2 right-2 text-[8px] tracking-[0.3em] font-bold" style={{ color }}>
                ✓ VOTASTE
              </span>
            )}
          </button>
        ))}
      </div>

      {votes && (
        <p className="text-white/20 text-[9px] tracking-[0.3em] text-center">
          {total} operadores votaron · se actualiza cada 8s
        </p>
      )}
    </div>
  )
}

// ─── Página principal ─────────────────────────────────────────────────────────

export default function BibliotecaPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = use(params)
  const pack = PACKS[slug]

  if (!pack) {
    return (
      <main className="min-h-screen bg-[#020202] font-mono flex items-center justify-center">
        <div className="text-center">
          <p className="text-white/30 text-sm mb-4">Pack no encontrado.</p>
          <Link href="/" className="text-[#00FF41] text-xs tracking-widest hover:underline">← VOLVER</Link>
        </div>
      </main>
    )
  }

  return (
    <main
      className="min-h-screen bg-[#020202] font-mono"
      style={{
        backgroundImage: 'repeating-linear-gradient(0deg,transparent,transparent 3px,rgba(0,255,65,0.012) 3px,rgba(0,255,65,0.012) 4px)',
      }}
    >
      <div className="max-w-3xl mx-auto px-6 py-10">

        {/* Nav */}
        <motion.div
          initial={{ opacity: 0 }} animate={{ opacity: 1 }}
          className="mb-8 flex items-center gap-4"
        >
          <Link href="/" className="text-white/25 text-[9px] tracking-[0.4em] uppercase hover:text-white/50 transition-colors">
            ← DAKI
          </Link>
          <span className="text-white/15 text-[9px]">/</span>
          <span className="text-[9px] tracking-[0.4em] uppercase" style={{ color: pack.color }}>
            BIBLIOTECA
          </span>
        </motion.div>

        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
          className="mb-8 border-l-2 pl-5"
          style={{ borderColor: pack.color }}
        >
          <p className="text-[8px] tracking-[0.5em] uppercase mb-2" style={{ color: `${pack.color}88` }}>
            PACK · 4 EBOOKS
          </p>
          <h1 className="text-2xl font-black uppercase tracking-tight text-white/90 mb-2">
            {pack.title}
          </h1>
          <p className="text-white/40 text-sm leading-relaxed">
            {pack.subtitle}
          </p>
        </motion.div>

        {/* Ebooks */}
        <div className="space-y-4 mb-6">
          {pack.ebooks.map((eb, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: 0.06 * i }}
              className="border border-white/[0.06] bg-[#0A0A0A] p-5"
            >
              <div className="flex items-start gap-3 mb-3">
                <span
                  className="text-[9px] font-bold w-6 h-6 flex items-center justify-center shrink-0 mt-0.5"
                  style={{ background: `${pack.color}22`, color: pack.color }}
                >
                  {i + 1}
                </span>
                <div>
                  <p className="text-white/85 text-sm font-bold tracking-tight mb-1">{eb.title}</p>
                  <p className="text-white/35 text-[10px] leading-relaxed">{eb.desc}</p>
                </div>
              </div>
              <div className="pl-9 space-y-1.5">
                {eb.chapters.map((ch, j) => (
                  <p key={j} className="text-white/25 text-[9px] flex gap-2">
                    <span style={{ color: `${pack.color}55` }}>›</span>
                    {ch}
                  </p>
                ))}
              </div>
            </motion.div>
          ))}
        </div>

        {/* CTA */}
        <motion.div
          initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.28 }}
          className="flex items-center justify-between border border-white/[0.06] bg-[#0A0A0A] p-5"
        >
          <div>
            <p className="text-white/40 text-[9px] tracking-[0.3em] uppercase mb-1">Precio del pack</p>
            <p className="text-white/90 text-2xl font-bold">{pack.price}</p>
          </div>
          <a
            href={pack.hotmart}
            target="_blank"
            rel="noopener noreferrer"
            className="px-6 py-3 text-[10px] tracking-[0.4em] font-bold uppercase transition-opacity hover:opacity-80"
            style={{ background: pack.color, color: '#000' }}
          >
            OBTENER PACK →
          </a>
        </motion.div>

        {/* Voting */}
        <VotingPanel />

      </div>
    </main>
  )
}
