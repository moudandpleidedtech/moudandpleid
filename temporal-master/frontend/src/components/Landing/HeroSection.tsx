'use client'

/**
 * HeroSection.tsx — Landing Page · DAKI EdTech
 * ─────────────────────────────────────────────
 * Layout split: izquierda (copy) · derecha (terminal vivo + feed de intrusiones)
 * Efectos: CRT scanlines · vignette · glitch · terminal animado · intrusion log
 */

import { useState, useEffect, useRef } from 'react'
import Link from 'next/link'
import { motion, AnimatePresence } from 'framer-motion'
import GlitchTitle from '@/components/UI/GlitchTitle'
import TypewriterText from '@/components/UI/TypewriterText'

/* ── Datos ──────────────────────────────────────────────────────────────── */

const ROLES = [
  { title: 'Python Backend Dev',  salary: '$90k – $130k',  yoy: '+34%' },
  { title: 'Data Engineer',       salary: '$110k – $160k', yoy: '+41%' },
  { title: 'ML Engineer',         salary: '$130k – $180k', yoy: '+52%' },
  { title: 'DevOps / Platform',   salary: '$100k – $150k', yoy: '+38%' },
  { title: 'Software Architect',  salary: '$140k – $200k', yoy: '+29%' },
]

const INTRUSION_LOG = [
  { type: 'alert', text: '203.45.67.89 → intento de acceso bloqueado'     },
  { type: 'scan',  text: 'escaneando vectores de ataque activos...'        },
  { type: 'warn',  text: 'JWT malformado detectado · origen: desconocido'  },
  { type: 'alert', text: 'bot_crawler_v7 → IP baneada automáticamente'    },
  { type: 'info',  text: '1.204 amenazas/hora · firewall activo'           },
  { type: 'warn',  text: 'SQL injection probe → rechazado · ln 89'        },
  { type: 'alert', text: '178.92.14.55 → acceso denegado · 3er intento'   },
  { type: 'scan',  text: 'análisis de dependencias en curso...'            },
  { type: 'warn',  text: 'XSS vector detectado en form público'            },
  { type: 'alert', text: 'fuerza bruta: 847 intentos/min · bloqueado'     },
  { type: 'info',  text: 'DAKI shield activo · 0 brechas confirmadas'     },
  { type: 'warn',  text: 'path traversal attempt → bloqueado'             },
  { type: 'alert', text: '45.33.32.156 → reconocimiento detectado'        },
  { type: 'scan',  text: 'verificando integridad de sesiones activas...'  },
  { type: 'info',  text: 'protocolo DAKI: sistema asegurado ✓'            },
]

type LineType = 'cmd' | 'info' | 'warn' | 'crit' | 'sub' | 'fail' | 'sep' | 'daki' | 'ok' | 'prog' | 'done'
interface TermLine { t: number; type: LineType; text: string }

const TERMINAL: TermLine[] = [
  { t: 0,     type: 'cmd',  text: '$ python deploy/app.py --env=production'          },
  { t: 600,   type: 'info', text: '  Cargando módulos: auth, db, api...'             },
  { t: 1100,  type: 'info', text: '  Ejecutando 24 tests unitarios...'               },
  { t: 1700,  type: 'warn', text: '⚠  sesión sin validación de tipo'                 },
  { t: 2100,  type: 'warn', text: '⚠  query sin parametrizar detectada'              },
  { t: 2550,  type: 'crit', text: '✗  ERROR CRÍTICO — línea 89'                     },
  { t: 2750,  type: 'sub',  text: '   TypeError: "NoneType" no tiene atributo get'   },
  { t: 3150,  type: 'crit', text: '✗  VULNERABILIDAD SQL — línea 134'               },
  { t: 3350,  type: 'sub',  text: '   user_input sin sanitizar → injection posible' },
  { t: 3850,  type: 'crit', text: '✗  BRECHA DE AUTENTICACIÓN — línea 203'          },
  { t: 4050,  type: 'sub',  text: '   token JWT no verificado antes de uso'          },
  { t: 4700,  type: 'fail', text: '  DEPLOY RECHAZADO · Code Review: FALLIDO ✗'    },
  { t: 5100,  type: 'sub',  text: '  3 vulnerabilidades críticas · 2 advertencias'  },
  { t: 5900,  type: 'sep',  text: '  ──────────────────────────────────────────'    },
  { t: 6200,  type: 'daki', text: '  DAKI INTELLIGENCE PROTOCOL → ACTIVADO'         },
  { t: 6600,  type: 'sep',  text: '  ──────────────────────────────────────────'    },
  { t: 7100,  type: 'daki', text: '  [DAKI] Analizando gaps cognitivos del dev...'  },
  { t: 7600,  type: 'daki', text: '  [DAKI] Gap detectado → manejo de errores'      },
  { t: 8100,  type: 'daki', text: '  [DAKI] Gap detectado → SQL y seguridad'        },
  { t: 8600,  type: 'daki', text: '  [DAKI] Gap detectado → autenticación JWT'      },
  { t: 9200,  type: 'ok',   text: '  [DAKI] Misión 18 desbloqueada ⚡'              },
  { t: 9700,  type: 'ok',   text: '  [DAKI] Misión 31 desbloqueada ⚡'              },
  { t: 10200, type: 'ok',   text: '  [DAKI] Misión 47 desbloqueada ⚡'              },
  { t: 10800, type: 'info', text: '  Entrenamiento personalizado iniciado...'        },
  { t: 11400, type: 'prog', text: '  [████████████████████] 100%'                  },
  { t: 12200, type: 'done', text: '  OPERADOR CERTIFICADO · DEPLOY APROBADO ✓'     },
]
const CYCLE_MS = 15000

const LINE_COLOR: Record<LineType, string> = {
  cmd:  '#00FF41',
  info: 'rgba(192,192,192,0.45)',
  warn: 'rgba(255,184,0,0.7)',
  crit: '#FF0033',
  sub:  'rgba(192,192,192,0.25)',
  fail: '#FF0033',
  sep:  'rgba(0,255,65,0.1)',
  daki: 'rgba(0,255,65,0.8)',
  ok:   '#00FF41',
  prog: '#00FF41',
  done: '#00FF41',
}

/* ── Componente ──────────────────────────────────────────────────────────── */

export default function HeroSection() {
  const [roleIdx,    setRoleIdx]    = useState(0)
  const [feedTail,   setFeedTail]   = useState(4)
  const [termLines,  setTermLines]  = useState(0)
  const timers = useRef<ReturnType<typeof setTimeout>[]>([])

  /* Role ticker */
  useEffect(() => {
    const t = setInterval(() => setRoleIdx(i => (i + 1) % ROLES.length), 2800)
    return () => clearInterval(t)
  }, [])

  /* Intrusion feed */
  useEffect(() => {
    const t = setInterval(() => setFeedTail(i => (i + 1) % INTRUSION_LOG.length), 1600)
    return () => clearInterval(t)
  }, [])

  /* Terminal animation — loop */
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

  const role         = ROLES[roleIdx]
  const visibleFeed  = Array.from({ length: 5 }, (_, i) =>
    INTRUSION_LOG[(feedTail - 4 + i + INTRUSION_LOG.length) % INTRUSION_LOG.length]
  )
  const visibleLines = TERMINAL.slice(0, termLines)

  /* Feed label colors */
  const feedColor = (type: string) => {
    if (type === 'alert') return '#FF0033'
    if (type === 'warn')  return '#FFB800'
    if (type === 'scan')  return 'rgba(0,255,65,0.5)'
    return 'rgba(192,192,192,0.35)'
  }
  const feedTag = (type: string) => {
    if (type === 'alert') return 'ALERT'
    if (type === 'warn')  return 'WARN'
    if (type === 'scan')  return 'SCAN'
    return 'INFO'
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
      {/* ── Keyframes ──────────────────────────────────────────────────────── */}
      <style>{`
        @keyframes btn-pulse {
          0%,100%{ box-shadow:0 0 8px rgba(0,255,65,.3),0 0 20px rgba(0,255,65,.1); border-color:rgba(0,255,65,.5); }
          50%    { box-shadow:0 0 24px rgba(0,255,65,.7),0 0 48px rgba(0,255,65,.3); border-color:#00FF41; }
        }
        .hero-btn-pulse{ animation:btn-pulse 2.4s ease-in-out infinite; }
        .hero-btn-pulse:hover{ animation:none; box-shadow:0 0 32px rgba(0,255,65,.8),0 0 64px rgba(0,255,65,.4); border-color:#00FF41; background-color:rgba(0,255,65,.12); }

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

      {/* ── Header ─────────────────────────────────────────────────────────── */}
      <header className="relative z-20 flex items-center justify-between px-6 md:px-12 py-5 border-b border-[#00FF41]/10 shrink-0">
        <div className="flex items-center gap-3">
          <span className="text-[#FF0033] text-xs tracking-[0.3em] opacity-60 hidden sm:block">{'//'}</span>
          <span className="text-[#00FF41] text-sm md:text-base font-bold tracking-[0.35em] uppercase neon-glow">DAKIedtech</span>
        </div>
        <div className="flex items-center gap-2 border border-[#00FF41]/30 px-3 py-1.5 bg-[#00FF41]/5">
          <span className="w-1.5 h-1.5 rounded-full bg-[#00FF41] animate-pulse" />
          <span className="text-[#00FF41] text-xs tracking-[0.3em] uppercase">STATUS: OPERATIVO</span>
        </div>
      </header>

      {/* ── Main split ─────────────────────────────────────────────────────── */}
      <div className="relative z-20 flex-1 flex items-center px-6 md:px-12 py-6 gap-8 min-h-0">

        {/* ─── LEFT: copy ─────────────────────────────────────────────────── */}
        <div className="flex-1 min-w-0 flex flex-col justify-center">

          {/* Role ticker */}
          <div className="flex items-center gap-3 mb-6 h-6 overflow-hidden">
            <span className="text-[8px] tracking-[0.45em] text-[#FF0033]/35 uppercase shrink-0">MERCADO HOY</span>
            <div className="h-px w-8 bg-[#FF0033]/12" />
            <AnimatePresence mode="wait">
              <motion.div
                key={roleIdx}
                className="flex items-center gap-3"
                initial={{ opacity: 0, y: -7 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: 7 }}
                transition={{ duration: 0.25 }}
              >
                <span className="text-[9px] tracking-[0.3em] text-white/38 uppercase">{role.title}</span>
                <span className="text-[9px] text-[#00FF41]/55 font-bold tracking-wider">{role.salary}</span>
                <span
                  className="text-[8px] px-1.5 py-0.5 font-black tracking-widest"
                  style={{ background:'rgba(0,255,65,0.07)', color:'#00FF41', border:'1px solid rgba(0,255,65,0.18)' }}
                >
                  {role.yoy}
                </span>
              </motion.div>
            </AnimatePresence>
          </div>

          {/* Pre-label */}
          <div className="flex items-center gap-4 mb-6">
            <div className="h-px bg-gradient-to-r from-transparent to-[#FF0033]/40 w-14" />
            <span className="text-[#FF0033]/70 text-[10px] tracking-[0.5em] uppercase">SISTEMA — NEXO CENTRAL — v4.2</span>
          </div>

          <GlitchTitle />

          <h2 className="text-xl sm:text-2xl md:text-3xl font-bold tracking-[0.15em] uppercase mb-8 text-[#00FF41]/90 neon-glow">
            <TypewriterText text="TÚ ERES LA CORRECCIÓN." delayMs={50} startDelay={500} />
          </h2>

          <p className="text-sm text-[#00FF41]/55 leading-7 tracking-wide max-w-lg mb-7">
            <span className="text-[#00FF41]/90 font-bold">DAKIedtech:</span>
            {' '}No somos un curso. Somos tu entorno de despliegue.
            IA de grado industrial que analiza tu lógica en tiempo real.
          </p>

          {/* Stat disruptivo */}
          <motion.div
            className="flex items-center gap-4 mb-8 px-4 py-3 border-l-2"
            style={{ borderColor:'#FF0033', background:'rgba(255,0,51,0.04)' }}
            initial={{ opacity:0, x:-12 }}
            animate={{ opacity:1, x:0 }}
            transition={{ delay:2.6, duration:0.5 }}
          >
            <span className="text-[#FF0033] text-2xl font-black shrink-0" style={{ textShadow:'0 0 20px rgba(255,0,51,0.4)' }}>
              73%
            </span>
            <div>
              <p className="text-[9px] text-[#C0C0C0]/38 leading-4 tracking-wide uppercase">
                de los devs junior fallan su primer code review real.
              </p>
              <p className="text-[9px] text-[#00FF41]/42 leading-4 tracking-wide uppercase mt-0.5">
                DAKI entrena exactamente ese gap.
              </p>
            </div>
          </motion.div>

          {/* CTA */}
          <Link
            href="/register"
            className="hero-btn-pulse inline-block border border-[#00FF41]/50 bg-[#00FF41]/5 text-[#00FF41] text-xs tracking-[0.35em] uppercase px-8 py-4 w-full sm:w-auto text-center mb-3"
          >
            {`[[ INICIAR SECUENCIA DE ACCESO ]]`}
          </Link>
          <p className="text-[#00FF41]/28 text-[10px] tracking-[0.2em]">
            {'[ Sin tarjeta de crédito · Acceso inmediato · Beta abierta ]'}
          </p>

          {/* Stats */}
          <div className="mt-8 pt-5 border-t border-[#00FF41]/8 flex items-center gap-8">
            {[
              { valor: '100', label: 'NIVELES' },
              { valor: 'IA',  label: 'INSTRUCTORA' },
              { valor: '∞',   label: 'DESAFÍOS' },
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

          {/* ── Intrusion feed ── */}
          <motion.div
            className="border overflow-hidden shrink-0"
            style={{ borderColor:'rgba(255,0,51,0.18)', background:'rgba(3,2,2,0.92)' }}
            initial={{ opacity:0, x:30 }}
            animate={{ opacity:1, x:0 }}
            transition={{ delay:0.4, duration:0.5 }}
          >
            {/* Titlebar */}
            <div
              className="flex items-center justify-between px-3 py-1.5 border-b"
              style={{ borderColor:'rgba(255,0,51,0.12)', background:'rgba(255,0,51,0.05)' }}
            >
              <div className="flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-[#FF0033] animate-pulse" />
                <span className="text-[8px] tracking-[0.45em] text-[#FF0033]/50 uppercase">DAKI THREAT MONITOR</span>
              </div>
              <span className="text-[8px] text-[#FF0033]/25 tracking-widest">LIVE</span>
            </div>

            {/* Log lines */}
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
            {/* Titlebar */}
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

            {/* Terminal body — scrollable */}
            <div className="relative flex-1 overflow-hidden">
              {/* Scanline sweep */}
              <div
                className="scanline-sweep absolute left-0 right-0 h-px pointer-events-none z-10"
                style={{ background:'rgba(0,255,65,0.12)' }}
              />

              <div className="px-3 py-2.5 space-y-0.5 h-full overflow-y-auto" style={{ scrollbarWidth:'none' }}>
                {visibleLines.map((line, i) => {
                  const isLast = i === visibleLines.length - 1
                  const bold   = line.type === 'done' || line.type === 'fail' || line.type === 'daki'
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

      {/* ── Footer ─────────────────────────────────────────────────────────── */}
      <footer className="relative z-20 px-6 md:px-12 py-3 border-t border-[#00FF41]/8 flex items-center justify-between shrink-0">
        <span className="text-[#00FF41]/18 text-[9px] tracking-[0.4em]">{'DAKI EdTech // CANAL SEGURO // CIFRADO AES-256'}</span>
        <span className="text-[#FF0033]/28 text-[9px] tracking-[0.3em] hidden md:block">{'[ ACCESO RESTRINGIDO — SOLO OPERADORES AUTORIZADOS ]'}</span>
      </footer>
    </section>
  )
}
