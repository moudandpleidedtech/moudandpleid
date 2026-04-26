'use client'

import { useState, useEffect, useRef } from 'react'
import Link from 'next/link'
import { motion } from 'framer-motion'
import GlitchTitle from '@/components/UI/GlitchTitle'
import TypewriterText from '@/components/UI/TypewriterText'

/* ── Datos ──────────────────────────────────────────────────────────────── */

const NEXO_FEED = [
  { type: 'rank',  text: 'vectorial_mx subió a Diamante · +850 XP'              },
  { type: 'log',   text: '31 misiones completadas en la última hora'             },
  { type: 'nexo',  text: 'nueva transmisión: "Closures en Python real"'          },
  { type: 'rank',  text: 'k4rl0s_arg alcanzó Nivel 15 · Racha 23 días'          },
  { type: 'log',   text: '1.204 Operadores activos este mes'                     },
  { type: 'nexo',  text: 'zero_day_pe completó el Boss Final ⚡'                 },
  { type: 'rank',  text: 'nullbyte_cl · racha de 30 días confirmada 🔥'         },
  { type: 'log',   text: 'leaderboard actualizado · semana 17'                   },
  { type: 'nexo',  text: 'devjuana desbloqueó Misión Clasificada #7'             },
  { type: 'rank',  text: 'syntax_co subió a Arquitecto Supremo ◆'               },
  { type: 'log',   text: '3 nuevos Operadores registrados hoy'                   },
  { type: 'nexo',  text: 'bytehunter_uy completó OOP · 100% de acierto'        },
  { type: 'rank',  text: 'mari_dev_ar completó Misión 47 · +200 XP'             },
  { type: 'log',   text: 'transmisión nueva: "Python en producción"'             },
  { type: 'nexo',  text: 'top3 esta semana: vectorial_mx · syntax_co · k4rl0s_arg' },
]

type LineType = 'cmd' | 'info' | 'ok' | 'daki' | 'prog' | 'done' | 'sep'
interface TermLine { t: number; type: LineType; text: string }

const TERMINAL: TermLine[] = [
  { t: 0,     type: 'cmd',  text: '$ nexo run --mission=18 --op=syntax_co'    },
  { t: 500,   type: 'info', text: '  Misión 18: Recursión con Memoización'    },
  { t: 900,   type: 'info', text: '  Cargando suite de tests...'              },
  { t: 1300,  type: 'ok',   text: '  test_base_case       → PASS ✓'          },
  { t: 1650,  type: 'ok',   text: '  test_recursion_deep  → PASS ✓'          },
  { t: 2000,  type: 'ok',   text: '  test_memo_cache      → PASS ✓'          },
  { t: 2350,  type: 'ok',   text: '  test_edge_case_zero  → PASS ✓'          },
  { t: 2800,  type: 'sep',  text: '  ──────────────────────────────────────'  },
  { t: 3100,  type: 'daki', text: '  DAKI INTELLIGENCE → ANÁLISIS ACTIVADO'   },
  { t: 3500,  type: 'sep',  text: '  ──────────────────────────────────────'  },
  { t: 3900,  type: 'daki', text: '  [DAKI] Solución correcta y eficiente ✓' },
  { t: 4400,  type: 'daki', text: '  [DAKI] Complejidad O(n) · Memo: O(n)'   },
  { t: 4900,  type: 'daki', text: '  [DAKI] ¿Por qué funciona el cache?'     },
  { t: 5500,  type: 'daki', text: '  [DAKI] Misión 19 desbloqueada ⚡'       },
  { t: 6100,  type: 'info', text: '  +150 XP · Racha: 12 días 🔥'            },
  { t: 6700,  type: 'prog', text: '  [███████████████████░] Nivel 7 → 8'    },
  { t: 7400,  type: 'done', text: '  OPERADOR VERIFICADO · MISIÓN COMPLETA ✓'},
]
const CYCLE_MS = 10000

const LINE_COLOR: Record<LineType, string> = {
  cmd:  '#00FF41',
  info: 'rgba(192,192,192,0.45)',
  ok:   '#00FF41',
  daki: 'rgba(0,255,65,0.8)',
  prog: '#00FF41',
  done: '#00FF41',
  sep:  'rgba(0,255,65,0.1)',
}

/* ── Componente ──────────────────────────────────────────────────────────── */

export default function HeroSection() {
  const [feedTail,  setFeedTail]  = useState(4)
  const [termLines, setTermLines] = useState(0)
  const timers = useRef<ReturnType<typeof setTimeout>[]>([])

  useEffect(() => {
    const t = setInterval(() => setFeedTail(i => (i + 1) % NEXO_FEED.length), 1800)
    return () => clearInterval(t)
  }, [])

  useEffect(() => {
    const run = () => {
      setTermLines(0)
      timers.current.forEach(clearTimeout)
      timers.current = []
      TERMINAL.forEach((line, i) => {
        const id = setTimeout(() => setTermLines(i + 1), line.t)
        timers.current.push(id)
      })
      const restart = setTimeout(run, CYCLE_MS)
      timers.current.push(restart)
    }
    run()
    return () => timers.current.forEach(clearTimeout)
  }, [])

  const visibleFeed  = Array.from({ length: 5 }, (_, i) =>
    NEXO_FEED[(feedTail - 4 + i + NEXO_FEED.length) % NEXO_FEED.length]
  )
  const visibleLines = TERMINAL.slice(0, termLines)

  const feedColor = (type: string) => {
    if (type === 'rank') return '#00FF41'
    if (type === 'nexo') return 'rgba(6,182,212,0.8)'
    return 'rgba(0,255,65,0.4)'
  }
  const feedTag = (type: string) => {
    if (type === 'rank') return 'RANK'
    if (type === 'nexo') return 'NEXO'
    return 'LOG'
  }

  return (
    <section
      className="min-h-screen font-mono text-[#00FF41] flex flex-col relative overflow-hidden"
      style={{
        backgroundImage: 'url(/assets/daki-bg.jpg)',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundAttachment: 'fixed',
      }}
    >
      <style>{`
        @keyframes scanline-sweep {
          0%  { top:-4px; opacity:.4; }
          100%{ top:100%; opacity:0; }
        }
        .scanline-sweep{ animation:scanline-sweep 4s linear infinite; }

        @keyframes cursor-blink {
          0%,100%{ opacity:1; } 50%{ opacity:0; }
        }
        .cursor-blink{ animation:cursor-blink .8s step-end infinite; }
      `}</style>

      {/* Overlay */}
      <div className="absolute inset-0 z-0 pointer-events-none" style={{ background: 'rgba(4,5,4,0.84)' }} />

      {/* CRT scanlines */}
      <div
        className="fixed inset-0 pointer-events-none z-10"
        style={{ backgroundImage:'repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,0.07) 2px,rgba(0,0,0,0.07) 4px)' }}
      />

      {/* Vignette */}
      <div
        className="fixed inset-0 pointer-events-none z-10"
        style={{ background:'radial-gradient(ellipse at center,transparent 50%,rgba(0,0,0,0.75) 100%)' }}
      />

      {/* Grid */}
      <div
        className="fixed inset-0 pointer-events-none z-0 opacity-[0.03]"
        style={{ backgroundImage:'linear-gradient(#00FF41 1px,transparent 1px),linear-gradient(90deg,#00FF41 1px,transparent 1px)', backgroundSize:'48px 48px' }}
      />

      {/* ── Main split ─────────────────────────────────────────────────────── */}
      <div className="relative z-20 flex-1 flex items-center px-6 md:px-12 pt-24 pb-8 gap-8">

        {/* ─── LEFT: copy ─────────────────────────────────────────────────── */}
        <div className="flex-1 min-w-0 flex flex-col justify-center">

          {/* Status pulse bar */}
          <div className="flex items-center gap-3 mb-5">
            <span className="w-1.5 h-1.5 rounded-full bg-[#00FF41] animate-pulse shrink-0" style={{ boxShadow: '0 0 6px #00FF41' }} />
            <span className="text-[8px] tracking-[0.4em] text-[#00FF41]/55 uppercase">NEXO EN LÍNEA</span>
            <span className="text-[#00FF41]/15 text-[8px]">·</span>
            <span className="text-[8px] tracking-[0.35em] text-[#00FF41]/40 uppercase">13 TRANSMISIONES</span>
            <span className="text-[#00FF41]/15 text-[8px]">·</span>
            <span className="text-[8px] tracking-[0.35em] text-[#00FF41]/40 uppercase">DAKI ACTIVO</span>
          </div>

          {/* Pre-label */}
          <div className="flex items-center gap-4 mb-6">
            <div className="h-px bg-gradient-to-r from-transparent to-[#00FF41]/30 w-14" />
            <span className="text-[#00FF41]/55 text-[10px] tracking-[0.5em] uppercase">COMUNIDAD — NEXO CENTRAL — v4.2</span>
          </div>

          <GlitchTitle />

          <h2 className="text-xl sm:text-2xl md:text-3xl font-bold tracking-[0.15em] uppercase mb-8 text-[#00FF41]/90 neon-glow">
            <TypewriterText text="CONSTRUÍS O MIRÁS." delayMs={50} startDelay={500} />
          </h2>

          <p className="text-sm text-[#00FF41]/55 leading-7 tracking-wide max-w-lg mb-7">
            <span className="text-[#00FF41]/90 font-bold">El Nexo</span>
            {' '}es la comunidad de Operadores de Python en Latinoamérica.
            Transmisiones semanales. Código ejecutable. IA táctica.
            El lugar donde los que van en serio con Python se encuentran.
          </p>

          {/* CTA Principal — sólido */}
          <Link
            href="/register"
            className="inline-block bg-[#00FF41] text-[#020202] text-sm font-black tracking-[0.2em] uppercase px-10 py-4 w-full sm:w-auto text-center hover:bg-[#00FF41]/90 transition-colors duration-150 mb-3"
          >
            PROBAR UNA MISIÓN GRATIS
          </Link>

          {/* CTA Secundario */}
          <div className="flex items-center gap-4 mb-3">
            <Link
              href="/blog"
              className="text-[#00FF41]/55 text-[9px] tracking-[0.3em] uppercase hover:text-[#00FF41]/85 transition-colors duration-200 border border-[#00FF41]/25 px-5 py-2.5 hover:border-[#00FF41]/55"
            >
              Ver las transmisiones →
            </Link>
            <Link
              href="/comunidad"
              className="text-white/30 text-[9px] tracking-[0.25em] uppercase hover:text-white/55 transition-colors duration-200"
            >
              El Nexo →
            </Link>
          </div>

          <p className="text-[#00FF41]/22 text-[9px] tracking-[0.2em]">
            Sin tarjeta · 10 misiones gratis · entrás en 60 segundos
          </p>

          {/* ── Canales de transmisión ───────────────────────────────────── */}
          <div className="flex items-center gap-3 mt-5">
            <span className="text-[8px] tracking-[0.45em] text-[#00FF41]/25 uppercase shrink-0">TRANSMISIONES</span>
            <div className="h-px flex-1 bg-[#00FF41]/8" />
            {[
              {
                href:  'https://www.instagram.com/dakiedtech',
                label: 'IG',
                lore:  'REELS',
                hoverBorder: 'hover:border-[#E1306C]/50',
                hoverBg:     'hover:bg-[#E1306C]/5',
                hoverText:   'group-hover:text-[#E1306C]/70',
                icon: (
                  <svg viewBox="0 0 24 24" fill="currentColor" className="w-3 h-3">
                    <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
                  </svg>
                ),
              },
              {
                href:  'https://www.tiktok.com/@dakiedtech',
                label: 'TT',
                lore:  'SEÑAL',
                hoverBorder: 'hover:border-white/30',
                hoverBg:     'hover:bg-white/5',
                hoverText:   'group-hover:text-white/60',
                icon: (
                  <svg viewBox="0 0 24 24" fill="currentColor" className="w-3 h-3">
                    <path d="M19.59 6.69a4.83 4.83 0 01-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 01-2.88 2.5 2.89 2.89 0 01-2.89-2.89 2.89 2.89 0 012.89-2.89c.28 0 .54.04.79.1V9.01a6.27 6.27 0 00-.79-.05 6.34 6.34 0 00-6.34 6.34 6.34 6.34 0 006.34 6.34 6.34 6.34 0 006.33-6.34l-.01-8.41a8.15 8.15 0 004.78 1.52V5.06a4.85 4.85 0 01-1-.37z"/>
                  </svg>
                ),
              },
              {
                href:  'https://www.youtube.com/@dakiedtech',
                label: 'YT',
                lore:  'CODEX',
                hoverBorder: 'hover:border-[#FF0000]/50',
                hoverBg:     'hover:bg-[#FF0000]/5',
                hoverText:   'group-hover:text-[#FF0000]/70',
                icon: (
                  <svg viewBox="0 0 24 24" fill="currentColor" className="w-3 h-3">
                    <path d="M23.498 6.186a3.016 3.016 0 00-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 00.502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 002.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 002.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
                  </svg>
                ),
              },
            ].map(({ href, label, lore, hoverBorder, hoverBg, hoverText, icon }) => (
              <a
                key={label}
                href={href}
                target="_blank"
                rel="noopener noreferrer"
                className={`group flex items-center gap-1.5 border border-[#00FF41]/15 bg-[#00FF41]/3 px-2.5 py-1.5 transition-all duration-200 ${hoverBorder} ${hoverBg}`}
              >
                <span className={`text-[#00FF41]/35 transition-colors duration-200 ${hoverText}`}>
                  {icon}
                </span>
                <span className={`text-[7px] tracking-[0.4em] text-[#00FF41]/30 transition-colors duration-200 uppercase ${hoverText}`}>
                  {lore}
                </span>
              </a>
            ))}
          </div>

          {/* Stats */}
          <div className="mt-8 pt-5 border-t border-[#00FF41]/8 flex items-center gap-8">
            {[
              { valor: '195', label: 'MISIONES' },
              { valor: '5',   label: 'LIGAS'    },
              { valor: 'IA',  label: 'TÁCTICA'  },
            ].map(({ valor, label }) => (
              <div key={label} className="flex items-center gap-2">
                <span className="text-base font-bold text-[#00FF41] neon-glow">{valor}</span>
                <span className="text-[9px] tracking-[0.4em] text-[#00FF41]/38 uppercase">{label}</span>
              </div>
            ))}
          </div>
        </div>

        {/* ─── RIGHT: terminal panels (solo lg+) ──────────────────────────── */}
        <div className="hidden lg:flex flex-col gap-3 w-[420px] xl:w-[460px] shrink-0 h-full max-h-[calc(100vh-130px)]">

          {/* ── Nexo activity feed ── */}
          <motion.div
            className="border overflow-hidden shrink-0"
            style={{ borderColor:'rgba(0,255,65,0.15)', background:'rgba(3,2,2,0.92)' }}
            initial={{ opacity:0, x:30 }}
            animate={{ opacity:1, x:0 }}
            transition={{ delay:0.4, duration:0.5 }}
          >
            <div
              className="flex items-center justify-between px-3 py-1.5 border-b"
              style={{ borderColor:'rgba(0,255,65,0.10)', background:'rgba(0,255,65,0.04)' }}
            >
              <div className="flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-[#00FF41]/70 animate-pulse" />
                <span className="text-[8px] tracking-[0.45em] text-[#00FF41]/50 uppercase">NEXO · ACTIVIDAD EN VIVO</span>
              </div>
              <span className="text-[8px] text-[#00FF41]/25 tracking-widest">LIVE</span>
            </div>

            <div className="px-3 py-2 space-y-1">
              {visibleFeed.map((entry, i) => {
                const isLatest = i === visibleFeed.length - 1
                const color = feedColor(entry.type)
                return (
                  <motion.div
                    key={`${feedTail}-${i}`}
                    className="flex items-start gap-2"
                    initial={isLatest ? { opacity:0, x:6 } : {}}
                    animate={{ opacity: isLatest ? 1 : (0.25 + i * 0.15), x:0 }}
                    transition={{ duration:0.3 }}
                  >
                    <span
                      className="text-[7px] tracking-[0.3em] shrink-0 mt-0.5 font-bold"
                      style={{ color, minWidth:'34px' }}
                    >
                      [{feedTag(entry.type)}]
                    </span>
                    <span className="text-[8px] leading-4" style={{ color: isLatest ? 'rgba(192,192,192,0.55)' : 'rgba(192,192,192,0.22)' }}>
                      {entry.text}
                    </span>
                  </motion.div>
                )
              })}
            </div>
          </motion.div>

          {/* ── Live terminal ── */}
          <motion.div
            className="border flex-1 flex flex-col overflow-hidden"
            style={{ borderColor:'rgba(0,255,65,0.15)', background:'rgba(2,4,2,0.94)' }}
            initial={{ opacity:0, x:30 }}
            animate={{ opacity:1, x:0 }}
            transition={{ delay:0.65, duration:0.5 }}
          >
            <div
              className="flex items-center justify-between px-3 py-1.5 border-b shrink-0"
              style={{ borderColor:'rgba(0,255,65,0.10)', background:'rgba(0,255,65,0.03)' }}
            >
              <div className="flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-[#00FF41]/60 animate-pulse" />
                <span className="text-[8px] tracking-[0.45em] text-[#00FF41]/40 uppercase">NEXO · ENTORNO DE EJECUCIÓN</span>
              </div>
              <div className="flex gap-1">
                <span className="w-2 h-2 rounded-full bg-[#FF0033]/30" />
                <span className="w-2 h-2 rounded-full bg-[#FFB800]/25" />
                <span className="w-2 h-2 rounded-full bg-[#00FF41]/20" />
              </div>
            </div>

            <div className="relative flex-1 overflow-hidden">
              <div
                className="scanline-sweep absolute left-0 right-0 h-px pointer-events-none z-10"
                style={{ background:'rgba(0,255,65,0.12)' }}
              />
              <div className="px-3 py-2.5 space-y-0.5 h-full overflow-y-auto" style={{ scrollbarWidth:'none' }}>
                {visibleLines.map((line, i) => {
                  const isLast = i === visibleLines.length - 1
                  const bold   = line.type === 'done' || line.type === 'daki'
                  return (
                    <motion.div
                      key={i}
                      initial={{ opacity:0, x:4 }}
                      animate={{ opacity:1, x:0 }}
                      transition={{ duration:0.15 }}
                      className={`text-[9px] leading-5 font-mono ${bold ? 'font-bold' : ''}`}
                      style={{ color: LINE_COLOR[line.type] }}
                    >
                      {line.text}
                      {isLast && line.type !== 'sep' && (
                        <span className="cursor-blink ml-0.5">█</span>
                      )}
                    </motion.div>
                  )
                })}
              </div>
            </div>
          </motion.div>

        </div>
      </div>

    </section>
  )
}
