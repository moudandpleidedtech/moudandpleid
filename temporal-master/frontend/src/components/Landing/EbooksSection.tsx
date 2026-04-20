'use client'

import { useState } from 'react'
import Image from 'next/image'
import { motion, AnimatePresence } from 'framer-motion'

const PACKS = [
  {
    id:    'negocio-solo',
    title: 'El Negocio Solo',
    tag:   'PACK · 3 EBOOKS',
    hook:  'Un negocio que trabaja aunque vos no estés.',
    why:   'La mayoría intercambia horas por dinero. Este pack te da los sistemas para atraer clientes, convertirlos y cobrar bien — sin depender de tu presencia constante.',
    para:  'Para freelancers y creadores que quieren escalar sin trabajar más horas.',
    items: [
      { name: 'El Freelancer de 3K',  desc: 'Posicionarte para cobrar lo que vale tu trabajo y atraer clientes que pagan sin regatear.' },
      { name: 'IA para Creadores',    desc: 'Producir contenido en escala usando IA sin perder tu voz ni tu estilo.' },
      { name: 'Emails que Venden',    desc: 'Secuencias de email reales para nutrir leads y convertirlos sin llamadas de ventas.' },
    ],
    price: '$27 USD',
    img:   '/assets/ebook-el-negocio-solo.png',
    href:  'https://go.hotmart.com/C105461511Y',
    color: '#00FF41',
  },
  {
    id:    'automatiza-ia',
    title: 'Automatiza tu Trabajo con IA',
    tag:   'PACK · 3 EBOOKS',
    hook:  'Más output. Sin contratar a nadie más.',
    why:   'La IA no reemplaza a los que saben usarla — los hace inalcanzables. Este pack te da flujos reales y base técnica para multiplicar lo que producís solo.',
    para:  'Para emprendedores y profesionales que quieren hacer más en menos tiempo.',
    items: [
      { name: 'La Ventaja Injusta',   desc: 'Diferenciarte cuando todos ofrecen lo mismo. Posicionamiento para mercados saturados.' },
      { name: '50 Flujos con Claude', desc: '50 automatizaciones reales con Claude AI listas para copiar y adaptar a tu negocio.' },
      { name: 'Python en 7 Días',     desc: 'Base técnica para entender y modificar scripts de IA sin depender de nadie.' },
    ],
    price: '$27 USD',
    img:   '/assets/ebook-automatiza-con-ia.png',
    href:  'https://go.hotmart.com/G105459604D',
    color: '#00CFFF',
  },
]

export default function EbooksSection() {
  const [expanded, setExpanded] = useState<string | null>(null)

  return (
    <section className="h-full flex flex-col font-mono bg-[#020202] overflow-hidden relative">
      <div
        className="absolute inset-0 pointer-events-none opacity-[0.015]"
        style={{ backgroundImage: 'repeating-linear-gradient(0deg,transparent,transparent 3px,#00FF41 3px,#00FF41 4px)' }}
      />

      <div className="flex-1 overflow-y-auto px-5 pt-5 pb-4 min-h-0" style={{ scrollbarWidth: 'none' }}>

        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.25 }}
          className="mb-4"
        >
          <p className="text-[7px] tracking-[0.55em] text-[#00FF41]/35 uppercase mb-1">
            {'// BIBLIOTECA — GOLDENGEAR'}
          </p>
          <p className="text-[11px] font-black tracking-[0.04em] text-white/60 uppercase">
            Conocimiento que se aplica el mismo día.
          </p>
        </motion.div>

        {/* Cards */}
        <div className="flex flex-col gap-3">
          {PACKS.map((pack, i) => {
            const isOpen = expanded === pack.id
            return (
              <motion.div
                key={pack.id}
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.25, delay: 0.06 + i * 0.08 }}
                className="border overflow-hidden"
                style={{ borderColor: `${pack.color}20`, background: '#080808' }}
              >
                {/* Fila principal — siempre visible */}
                <div className="flex flex-row">
                  {/* Imagen */}
                  <div className="relative shrink-0 w-20 self-stretch overflow-hidden">
                    <Image
                      src={pack.img}
                      alt={pack.title}
                      fill
                      className="object-cover"
                      sizes="80px"
                    />
                    <div
                      className="absolute inset-0"
                      style={{ background: 'linear-gradient(to right, transparent 50%, #080808 100%)' }}
                    />
                  </div>

                  {/* Contenido compacto */}
                  <div className="flex flex-col flex-1 p-3 gap-1.5 min-w-0">
                    <div>
                      <span className="text-[7px] tracking-[0.4em] font-bold uppercase" style={{ color: pack.color }}>
                        {pack.tag}
                      </span>
                      <p className="text-white/85 text-[11px] font-black uppercase tracking-wide leading-tight">
                        {pack.title}
                      </p>
                    </div>
                    <p className="text-white/40 text-[8.5px] italic leading-snug">{pack.hook}</p>

                    {/* Precio + CTAs */}
                    <div className="flex items-center justify-between gap-2 pt-1">
                      <span className="text-white/90 text-sm font-bold">{pack.price}</span>
                      <div className="flex gap-1.5">
                        <button
                          onClick={() => setExpanded(isOpen ? null : pack.id)}
                          className="px-2.5 py-1 text-[7px] tracking-[0.3em] font-bold uppercase border transition-colors"
                          style={{ borderColor: `${pack.color}40`, color: `${pack.color}90` }}
                        >
                          {isOpen ? 'CERRAR ↑' : 'VER MÁS ↓'}
                        </button>
                        <a
                          href={pack.href}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="px-2.5 py-1 text-[7px] tracking-[0.3em] font-bold uppercase"
                          style={{ background: pack.color, color: '#000' }}
                        >
                          OBTENER →
                        </a>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Panel expandible */}
                <AnimatePresence initial={false}>
                  {isOpen && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: 'auto', opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      transition={{ duration: 0.22 }}
                      className="overflow-hidden"
                    >
                      <div
                        className="px-4 pt-3 pb-4 border-t flex flex-col gap-3"
                        style={{ borderColor: `${pack.color}15` }}
                      >
                        {/* Por qué */}
                        <div className="border-l-2 pl-3" style={{ borderColor: pack.color }}>
                          <p className="text-[7px] tracking-[0.4em] uppercase mb-1" style={{ color: `${pack.color}70` }}>
                            POR QUÉ ESTE PACK
                          </p>
                          <p className="text-white/50 text-[9px] leading-relaxed">{pack.why}</p>
                          <p className="text-[8px] mt-1.5" style={{ color: `${pack.color}50` }}>{pack.para}</p>
                        </div>

                        {/* 3 ebooks */}
                        <div>
                          <p className="text-[7px] tracking-[0.4em] uppercase mb-2" style={{ color: `${pack.color}70` }}>
                            LO QUE OBTENÉS
                          </p>
                          <div className="space-y-1.5">
                            {pack.items.map((item, j) => (
                              <div key={j} className="flex gap-2">
                                <span className="text-[8px] shrink-0 mt-px" style={{ color: pack.color }}>▸</span>
                                <div>
                                  <span className="text-white/75 text-[9px] font-bold">{item.name} — </span>
                                  <span className="text-white/35 text-[9px]">{item.desc}</span>
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>

                        {/* CTA final */}
                        <a
                          href={pack.href}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="w-full py-2 text-center text-[8px] tracking-[0.4em] font-bold uppercase"
                          style={{ background: pack.color, color: '#000' }}
                        >
                          OBTENER AHORA POR {pack.price} →
                        </a>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </motion.div>
            )
          })}
        </div>

        <motion.p
          initial={{ opacity: 0 }} animate={{ opacity: 1 }}
          transition={{ duration: 0.3, delay: 0.28 }}
          className="text-center text-white/15 text-[7px] tracking-[0.35em] uppercase mt-4"
        >
          {'// PAGO SEGURO VÍA HOTMART · ENTREGA INMEDIATA'}
        </motion.p>

      </div>
    </section>
  )
}
