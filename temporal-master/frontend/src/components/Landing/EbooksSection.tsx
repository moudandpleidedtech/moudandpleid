'use client'

import Image from 'next/image'
import { motion } from 'framer-motion'

const PACKS = [
  {
    id:    'negocio-solo',
    title: 'El Negocio Solo',
    tag:   'PACK · 4 EBOOKS',
    hook:  'Un negocio que trabaja aunque vos no estés.',
    why:   'La mayoría intercambia tiempo por dinero. Este pack te enseña a construir sistemas que generan sin que estés mirando.',
    items: [
      'El Freelancer de 3K — conseguí clientes que pagan bien',
      'Emails que Venden — secuencias que convierten',
      'La Ventaja Injusta — posicionarte diferente',
      'Notion para Humanos — organizá tu negocio sin caos',
    ],
    price: '$27 USD',
    img:   '/assets/ebook-el-negocio-solo.png',
    href:  'https://go.hotmart.com/C105461511Y',
    color: '#00FF41',
  },
  {
    id:    'automatiza-ia',
    title: 'Automatiza tu Trabajo con IA',
    tag:   'PACK · 4 EBOOKS',
    hook:  'Más output. Sin contratar a nadie más.',
    why:   'La IA no reemplaza a los que saben usarla. Este pack te da los flujos reales para multiplicar lo que producís solo.',
    items: [
      '50 Flujos con Claude — automatizaciones listas para usar',
      'IA para Creadores — contenido en escala con IA',
      'Make en 5 Días — automatizá sin saber programar',
      'Python en 7 Días — base técnica para ir más lejos',
    ],
    price: '$27 USD',
    img:   '/assets/ebook-automatiza-con-ia.png',
    href:  'https://go.hotmart.com/G105459604D',
    color: '#00CFFF',
  },
]

export default function EbooksSection() {
  return (
    <section className="h-full flex flex-col font-mono bg-[#020202] overflow-hidden relative">

      <div
        className="absolute inset-0 pointer-events-none opacity-[0.015]"
        style={{ backgroundImage: 'repeating-linear-gradient(0deg,transparent,transparent 3px,#00FF41 3px,#00FF41 4px)' }}
      />

      <div className="flex-1 flex flex-col justify-center px-5 py-4 gap-3 min-h-0">

        {/* Header compacto */}
        <motion.div
          initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.25 }}
        >
          <p className="text-[7px] tracking-[0.55em] text-[#00FF41]/35 uppercase mb-1">
            {'// BIBLIOTECA — GOLDENGEAR'}
          </p>
          <p className="text-[11px] font-black tracking-[0.04em] text-white/60 uppercase">
            Conocimiento que se aplica el mismo día.
          </p>
        </motion.div>

        {/* Cards */}
        {PACKS.map((pack, i) => (
          <motion.div
            key={pack.id}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.25, delay: 0.06 + i * 0.08 }}
            className="border flex flex-row overflow-hidden"
            style={{ borderColor: `${pack.color}20`, background: '#080808' }}
          >
            {/* Imagen lateral pequeña */}
            <div className="relative shrink-0 w-24 self-stretch overflow-hidden">
              <Image
                src={pack.img}
                alt={pack.title}
                fill
                className="object-cover"
                sizes="96px"
              />
              {/* Gradient fade derecha */}
              <div
                className="absolute inset-0"
                style={{ background: 'linear-gradient(to right, transparent 60%, #080808 100%)' }}
              />
            </div>

            {/* Contenido */}
            <div className="flex flex-col flex-1 p-3 gap-2 min-w-0">

              {/* Tag + Título */}
              <div>
                <span
                  className="text-[7px] tracking-[0.45em] font-bold uppercase"
                  style={{ color: pack.color }}
                >
                  {pack.tag}
                </span>
                <p className="text-white/85 text-[11px] font-black uppercase tracking-wide leading-tight">
                  {pack.title}
                </p>
              </div>

              {/* Hook */}
              <p className="text-white/55 text-[9px] leading-relaxed italic">
                {pack.hook}
              </p>

              {/* Por qué */}
              <p className="text-white/35 text-[8.5px] leading-relaxed">
                {pack.why}
              </p>

              {/* Divider */}
              <div className="h-px w-full" style={{ background: `${pack.color}18` }} />

              {/* Lo que obtenés */}
              <div>
                <p className="text-[7px] tracking-[0.4em] uppercase mb-1" style={{ color: `${pack.color}80` }}>
                  LO QUE OBTENÉS
                </p>
                <ul className="space-y-0.5">
                  {pack.items.map((item, j) => (
                    <li key={j} className="flex items-start gap-1.5">
                      <span className="text-[8px] shrink-0 mt-px" style={{ color: pack.color }}>▸</span>
                      <span className="text-white/40 text-[8px] leading-tight">{item}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Precio + CTA */}
              <div className="flex items-center justify-between gap-2 pt-1">
                <div>
                  <span className="text-white/90 text-base font-bold tracking-tight">{pack.price}</span>
                  <span className="text-white/25 text-[8px] ml-1">· entrega inmediata</span>
                </div>
                <a
                  href={pack.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="px-3 py-1.5 text-[8px] tracking-[0.35em] font-bold uppercase shrink-0"
                  style={{ background: pack.color, color: '#000' }}
                >
                  OBTENER →
                </a>
              </div>

            </div>
          </motion.div>
        ))}

        {/* Footer */}
        <motion.p
          initial={{ opacity: 0 }} animate={{ opacity: 1 }}
          transition={{ duration: 0.3, delay: 0.26 }}
          className="text-center text-white/15 text-[7px] tracking-[0.35em] uppercase"
        >
          {'// PAGO SEGURO VÍA HOTMART'}
        </motion.p>

      </div>
    </section>
  )
}
