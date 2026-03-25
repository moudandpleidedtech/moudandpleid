'use client'

/**
 * SolucionSection — Slide 3 del Landing (reemplaza slides 3, 4, 5, 6)
 *
 * Tres tabs navegables sin cambio de slide:
 *   DIAGNÓSTICO  — por qué fallan los métodos tradicionales
 *   D·A·K·I      — el protocolo de aprendizaje
 *   MISIONES     — las zonas de operación disponibles
 *
 * Reduce 4 slides a 1 con botones de despliegue de información.
 */

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import Link from 'next/link'

type Tab = 'diagnostico' | 'protocolo' | 'misiones'

const TABS: { id: Tab; label: string }[] = [
  { id: 'diagnostico', label: 'DIAGNÓSTICO' },
  { id: 'protocolo',   label: 'D·A·K·I'     },
  { id: 'misiones',    label: 'MISIONES'     },
]

const PROBLEMS = [
  {
    icon: '⬚', title: 'CURSOS ONLINE', badge: 'CERTIFICADO SIN ARQUITECTURA', badgeColor: '#FF6B6B',
    lines: ['Copias código, no diseñas sistemas.', 'El certificado no reemplaza el criterio de ingeniería.'],
  },
  {
    icon: '◫', title: 'BOOTCAMPS', badge: 'PROFUNDIDAD INSUFICIENTE', badgeColor: '#FFB800',
    lines: ['12 semanas alcanzan para el primer trabajo.', 'No alcanzan para crecer ni para escalar.'],
  },
  {
    icon: '◪', title: 'YOUTUBE + TUTORIALES', badge: 'FRAGMENTADO', badgeColor: '#00B4D8',
    lines: ['100 videos desconectados entre sí.', 'Sin criterio de diseño. Sin visión de sistema.'],
  },
]

const PROTOCOL = [
  { letter: 'D', word: 'DESARROLLO',  desc: 'Python profesional desde el primer commit. Sin teoría vacía, sin sandboxes eternos.',      color: '#00FF41' },
  { letter: 'A', word: 'ARQUITECTURA', desc: 'Sistemas reales que corren en producción. No ejercicios. No proyectos que nadie usa.',      color: '#00B4D8' },
  { letter: 'K', word: 'KNOWLEDGE',   desc: 'DAKI recuerda tu historial de errores y adapta cada misión a tu gap de conocimiento.',      color: '#7B2FBE' },
  { letter: 'I', word: 'INTELIGENCIA', desc: 'Tu instructor IA te interroga hasta que demuestres dominio. No basta con copiar la respuesta.', color: '#FFB800' },
]

const MISSIONS = [
  {
    code: 'OP-01', name: 'Python Core', status: 'ONLINE', statusColor: '#00FF41',
    levels: '100 niveles', desc: 'Fundamentos → OOP → APIs → Arquitectura. La trayectoria completa de Junior a Senior.',
    tags: ['Python', 'OOP', 'APIs', 'Algoritmos', 'Arquitectura'], locked: false,
  },
  {
    code: 'OP-02', name: 'Hacking Ético', status: 'PRÓXIMAMENTE', statusColor: '#FFB800',
    levels: 'Nivel 10+', desc: 'La mentalidad del atacante para entender y defender sistemas reales.',
    tags: ['Pentesting', 'Scripts', 'Redes', 'CVE'], locked: true,
  },
  {
    code: 'OP-03', name: 'Agente de IA', status: 'EN DESARROLLO', statusColor: '#7B2FBE',
    levels: 'Clasificado', desc: 'Construye sistemas de IA con Python. Agentes autónomos, pipelines, LLMs.',
    tags: ['LLMs', 'Agentes', 'Pipelines', 'Anthropic'], locked: true,
  },
]

const STATS = [
  { n: '#1', label: 'LENGUAJE EN IA Y DATOS' },
  { n: '100', label: 'NIVELES DE OPERACIÓN' },
  { n: '∞', label: 'MISIONES GENERADAS POR IA' },
  { n: '0', label: 'TEORÍA SIN APLICACIÓN' },
]

export default function SolucionSection() {
  const [tab, setTab] = useState<Tab>('diagnostico')

  return (
    <section className="h-full flex flex-col font-mono bg-[#020202] overflow-hidden relative">

      {/* Scanlines */}
      <div className="absolute inset-0 pointer-events-none opacity-[0.02]"
        style={{ backgroundImage: 'repeating-linear-gradient(0deg,transparent,transparent 3px,#00FF41 3px,#00FF41 4px)' }}
      />

      {/* Tab bar */}
      <div className="shrink-0 px-6 pt-6 z-10">
        <p className="text-[8px] tracking-[0.6em] text-[#00FF41]/18 mb-4">
          {'// MÓDULO DE ANÁLISIS — SELECCIONA UNA SECCIÓN'}
        </p>
        <div className="flex items-end gap-0 border-b border-[#00FF41]/10">
          {TABS.map(t => (
            <button
              key={t.id}
              onClick={() => setTab(t.id)}
              className="relative px-5 py-2.5 text-[9px] tracking-[0.4em] uppercase font-bold transition-all duration-200 font-mono"
              style={{
                color:        tab === t.id ? '#00FF41' : 'rgba(0,255,65,0.22)',
                borderBottom: tab === t.id ? '1px solid #00FF41' : '1px solid transparent',
                marginBottom: '-1px',
                background:   tab === t.id ? 'rgba(0,255,65,0.04)' : 'transparent',
              }}
            >
              {t.label}
            </button>
          ))}
        </div>
      </div>

      {/* Content area */}
      <div
        className="flex-1 overflow-y-auto px-6 pb-8 min-h-0"
        style={{ scrollbarWidth: 'none' }}
      >
        <AnimatePresence mode="wait">

          {/* ── DIAGNÓSTICO ────────────────────────────────────────────────── */}
          {tab === 'diagnostico' && (
            <motion.div key="diag"
              initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -8 }} transition={{ duration: 0.18 }}
            >
              <p className="text-[9px] tracking-[0.4em] text-[#00FF41]/22 uppercase mt-5 mb-6">
                Los cursos te enseñan sintaxis. El mercado exige sistemas.
              </p>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
                {PROBLEMS.map(p => (
                  <div key={p.title} className="border border-[#00FF41]/10 p-5">
                    <div className="flex items-start justify-between mb-4">
                      <span className="text-2xl text-[#00FF41]/20 leading-none">{p.icon}</span>
                      <span
                        className="text-[7px] tracking-[0.3em] font-bold px-2 py-1 border"
                        style={{ color: p.badgeColor, borderColor: `${p.badgeColor}30`, background: `${p.badgeColor}08` }}
                      >
                        {p.badge}
                      </span>
                    </div>
                    <h3 className="text-[11px] font-black tracking-[0.3em] text-[#00FF41]/60 mb-3">{p.title}</h3>
                    {p.lines.map((line, i) => (
                      <p key={i} className="text-[10px] text-[#00FF41]/38 leading-relaxed tracking-wide mb-1.5">
                        — {line}
                      </p>
                    ))}
                  </div>
                ))}
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                {STATS.map(({ n, label }) => (
                  <div key={label} className="border border-[#00FF41]/8 p-3 text-center">
                    <p className="text-xl font-black text-[#00FF41]"
                      style={{ textShadow: '0 0 12px rgba(0,255,65,0.4)' }}>
                      {n}
                    </p>
                    <p className="text-[7px] tracking-[0.3em] text-[#00FF41]/22 mt-1">{label}</p>
                  </div>
                ))}
              </div>
            </motion.div>
          )}

          {/* ── PROTOCOLO D·A·K·I ──────────────────────────────────────────── */}
          {tab === 'protocolo' && (
            <motion.div key="proto"
              initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -8 }} transition={{ duration: 0.18 }}
            >
              <p className="text-[9px] tracking-[0.4em] text-[#00FF41]/22 uppercase mt-5 mb-6">
                Un sistema de aprendizaje diseñado para producción real, no para exámenes.
              </p>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {PROTOCOL.map(({ letter, word, desc, color }) => (
                  <div
                    key={letter}
                    className="border p-6 flex gap-5 items-start transition-all duration-200"
                    style={{ borderColor: `${color}18`, background: `${color}03` }}
                    onMouseEnter={e => {
                      ;(e.currentTarget as HTMLDivElement).style.borderColor = `${color}40`
                      ;(e.currentTarget as HTMLDivElement).style.background  = `${color}07`
                    }}
                    onMouseLeave={e => {
                      ;(e.currentTarget as HTMLDivElement).style.borderColor = `${color}18`
                      ;(e.currentTarget as HTMLDivElement).style.background  = `${color}03`
                    }}
                  >
                    <span
                      className="text-5xl font-black leading-none shrink-0"
                      style={{ color, textShadow: `0 0 30px ${color}50` }}
                    >
                      {letter}
                    </span>
                    <div>
                      <h3 className="text-xs font-black tracking-[0.35em] mb-2" style={{ color }}>
                        {word}
                      </h3>
                      <p className="text-[10px] leading-relaxed tracking-wide" style={{ color: `${color}50` }}>
                        {desc}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </motion.div>
          )}

          {/* ── MISIONES ────────────────────────────────────────────────────── */}
          {tab === 'misiones' && (
            <motion.div key="mis"
              initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -8 }} transition={{ duration: 0.18 }}
            >
              <p className="text-[9px] tracking-[0.4em] text-[#00FF41]/22 uppercase mt-5 mb-6">
                Tres zonas de operación. Una trayectoria hacia el top 1%.
              </p>

              <div className="flex flex-col gap-3 mb-6">
                {MISSIONS.map(m => (
                  <div
                    key={m.code}
                    className={`border p-5 transition-all duration-200 ${m.locked ? 'opacity-50' : ''}`}
                    style={{ borderColor: m.locked ? 'rgba(0,255,65,0.07)' : 'rgba(0,255,65,0.22)' }}
                    onMouseEnter={e => {
                      if (!m.locked) (e.currentTarget as HTMLDivElement).style.borderColor = 'rgba(0,255,65,0.45)'
                    }}
                    onMouseLeave={e => {
                      if (!m.locked) (e.currentTarget as HTMLDivElement).style.borderColor = 'rgba(0,255,65,0.22)'
                    }}
                  >
                    <div className="flex items-start justify-between gap-4">
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-3 mb-2">
                          <span className="text-[8px] tracking-[0.45em] text-[#00FF41]/20">{m.code}</span>
                          <span
                            className="text-[7px] tracking-[0.3em] font-black px-2 py-0.5 border"
                            style={{ color: m.statusColor, borderColor: `${m.statusColor}30`, background: `${m.statusColor}08` }}
                          >
                            {m.status}
                          </span>
                        </div>
                        <h3 className="text-sm font-black tracking-[0.2em] text-[#00FF41] mb-1.5">{m.name}</h3>
                        <p className="text-[10px] text-[#00FF41]/40 leading-relaxed mb-3">{m.desc}</p>
                        <div className="flex flex-wrap gap-1.5">
                          {m.tags.map(tag => (
                            <span
                              key={tag}
                              className="text-[7px] px-2 py-0.5 border border-[#00FF41]/12 text-[#00FF41]/28 tracking-wider"
                            >
                              {tag}
                            </span>
                          ))}
                        </div>
                      </div>
                      <div className="text-right shrink-0">
                        <p className="text-[8px] text-[#00FF41]/25 tracking-wider whitespace-nowrap">{m.levels}</p>
                        {m.locked && <span className="block mt-2 text-lg opacity-25">🔒</span>}
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              <div className="text-center">
                <Link
                  href="/register"
                  className="inline-block border border-[#00FF41]/30 text-[#00FF41]/65 text-[10px] tracking-[0.4em] uppercase px-8 py-3 transition-all duration-200"
                  style={{ fontFamily: 'monospace' }}
                  onMouseEnter={e => {
                    ;(e.currentTarget as HTMLAnchorElement).style.borderColor = 'rgba(0,255,65,0.60)'
                    ;(e.currentTarget as HTMLAnchorElement).style.color       = '#00FF41'
                    ;(e.currentTarget as HTMLAnchorElement).style.background  = 'rgba(0,255,65,0.06)'
                  }}
                  onMouseLeave={e => {
                    ;(e.currentTarget as HTMLAnchorElement).style.borderColor = 'rgba(0,255,65,0.30)'
                    ;(e.currentTarget as HTMLAnchorElement).style.color       = 'rgba(0,255,65,0.65)'
                    ;(e.currentTarget as HTMLAnchorElement).style.background  = 'transparent'
                  }}
                >
                  {'[ INICIAR OPERACIÓN PYTHON CORE ]'}
                </Link>
              </div>
            </motion.div>
          )}

        </AnimatePresence>
      </div>
    </section>
  )
}
