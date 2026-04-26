'use client'

import Link from 'next/link'
import { motion } from 'framer-motion'

const STEPS = [
  {
    num:   '01',
    label: 'RECIBÍS EL DESAFÍO',
    color: '#00FF41',
    panel: [
      { t: 'tag',  c: '// MISIÓN 18 · RECURSIÓN'                   },
      { t: 'dim',  c: ''                                            },
      { t: 'text', c: 'Implementá factorial(n) sin usar'            },
      { t: 'text', c: 'bucles. Solo recursión.'                     },
      { t: 'dim',  c: ''                                            },
      { t: 'text', c: 'factorial(5)  →  120'                        },
      { t: 'text', c: 'factorial(0)  →  1'                          },
      { t: 'dim',  c: ''                                            },
      { t: 'warn', c: 'Sin múltiple choice.'                        },
      { t: 'warn', c: 'Tu código corre de verdad.'                  },
    ],
  },
  {
    num:   '02',
    label: 'ESCRIBÍS EL CÓDIGO',
    color: '#06b6d4',
    panel: [
      { t: 'tag',  c: '$ python3 mision_18.py'                      },
      { t: 'dim',  c: ''                                            },
      { t: 'code', c: 'def factorial(n: int) -> int:'              },
      { t: 'code', c: '    if n <= 1:'                              },
      { t: 'code', c: '        return 1'                            },
      { t: 'code', c: '    return n * factorial(n - 1)'             },
      { t: 'dim',  c: ''                                            },
      { t: 'run',  c: '▸ ejecutando tests...'                       },
      { t: 'ok',   c: '✓ 8/8 casos pasaron'                        },
    ],
  },
  {
    num:   '03',
    label: 'DAKI ANALIZA',
    color: '#f59e0b',
    panel: [
      { t: 'tag',  c: '◈ DAKI INTELLIGENCE'                        },
      { t: 'dim',  c: ''                                            },
      { t: 'daki', c: '"Tu caso base maneja n=0'                   },
      { t: 'daki', c: ' correctamente. Bien."'                      },
      { t: 'dim',  c: ''                                            },
      { t: 'daki', c: '"¿Qué pasa si n es'                         },
      { t: 'daki', c: ' negativo? ¿Tu función'                      },
      { t: 'daki', c: ' entra en loop infinito?"'                   },
      { t: 'dim',  c: ''                                            },
      { t: 'ok',   c: '⚡ Misión 19 desbloqueada'                  },
    ],
  },
]

const LINE_COLOR: Record<string, string> = {
  tag:  'rgba(0,255,65,0.40)',
  dim:  'transparent',
  text: 'rgba(255,255,255,0.55)',
  warn: 'rgba(255,184,0,0.70)',
  code: '#00FF41',
  run:  'rgba(192,192,192,0.40)',
  ok:   '#00FF41',
  daki: 'rgba(245,158,11,0.80)',
}

export default function MisionPreviewSection() {
  return (
    <section className="font-mono bg-[#020202] relative border-t border-[#00FF41]/08">

      <div
        className="absolute inset-0 pointer-events-none opacity-[0.008]"
        style={{ backgroundImage: 'linear-gradient(rgba(0,255,65,0.05) 1px,transparent 1px),linear-gradient(90deg,rgba(0,255,65,0.05) 1px,transparent 1px)', backgroundSize: '60px 60px' }}
      />

      <div className="relative z-10 px-6 sm:px-10 py-14">

        {/* Header */}
        <div className="mb-10">
          <p className="text-[7px] tracking-[0.6em] text-[#00FF41]/25 uppercase mb-3">
            {'// ASÍ FUNCIONA UNA MISIÓN — TOMÁ 90 SEGUNDOS Y MIRÁ'}
          </p>
          <h2 className="text-2xl sm:text-3xl font-black tracking-[0.06em] uppercase text-white/85 leading-tight">
            No hay teoría.{' '}
            <span className="text-[#00FF41]" style={{ textShadow: '0 0 24px rgba(0,255,65,0.4)' }}>
              Solo código real.
            </span>
          </h2>
        </div>

        {/* 3 steps */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-10">
          {STEPS.map(({ num, label, color, panel }, si) => (
            <motion.div
              key={num}
              initial={{ opacity: 0, y: 12 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.3, delay: si * 0.1 }}
              className="relative border flex flex-col overflow-hidden"
              style={{ borderColor: `${color}20`, background: `${color}03` }}
            >
              {/* Top accent */}
              <div className="absolute top-0 left-0 right-0 h-px"
                style={{ background: `linear-gradient(90deg,transparent,${color}60,transparent)` }} />

              {/* Step header */}
              <div
                className="flex items-center gap-3 px-4 py-2.5 border-b"
                style={{ borderColor: `${color}15`, background: `${color}05` }}
              >
                <span className="text-[9px] font-black tracking-[0.3em]" style={{ color: `${color}50` }}>
                  PASO {num}
                </span>
                <span className="text-[8px] tracking-[0.3em] uppercase font-bold" style={{ color }}>
                  {label}
                </span>
              </div>

              {/* Code panel */}
              <div className="px-4 py-3 flex-1 space-y-0.5" style={{ fontFamily: 'monospace' }}>
                {panel.map((line, li) => (
                  <div
                    key={li}
                    className="text-[9px] leading-[1.7]"
                    style={{ color: LINE_COLOR[line.t] ?? 'rgba(255,255,255,0.4)', minHeight: line.c ? undefined : '8px' }}
                  >
                    {line.c}
                  </div>
                ))}
              </div>
            </motion.div>
          ))}
        </div>

        {/* CTA — solid */}
        <div className="flex flex-col sm:flex-row items-center gap-4">
          <Link
            href="/register"
            className="bg-[#00FF41] text-[#020202] text-sm font-black tracking-[0.2em] uppercase px-10 py-4 hover:bg-[#00FF41]/90 transition-colors duration-150 text-center w-full sm:w-auto"
          >
            PROBAR ESTA MISIÓN GRATIS
          </Link>
          <div>
            <p className="text-[9px] text-white/30 tracking-[0.2em]">Sin tarjeta · en línea en 60 segundos</p>
            <p className="text-[8px] text-[#00FF41]/30 tracking-[0.2em]">Las primeras 10 misiones son completamente gratis.</p>
          </div>
        </div>

      </div>
    </section>
  )
}
