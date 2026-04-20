'use client'

import Image from 'next/image'
import Link  from 'next/link'
import { motion } from 'framer-motion'

const PACKS = [
  {
    id:    'el-negocio-solo',
    title: 'El Negocio Solo',
    desc:  'Construí un negocio digital que funciona sin que estés mirando. Sistemas, automatizaciones y flujos que trabajan por vos.',
    price: '$27 USD',
    img:   '/assets/ebook-el-negocio-solo.png',
    href:  'https://go.hotmart.com/C105461511Y',
    tag:   'PACK · 4 EBOOKS',
    color: '#00FF41',
  },
  {
    id:    'automatiza-con-ia',
    title: 'Automatiza tu Trabajo con IA',
    desc:  'Flujos reales con Claude, Make y herramientas de IA para multiplicar tu output sin contratar a nadie.',
    price: '$27 USD',
    img:   '/assets/ebook-automatiza-con-ia.png',
    href:  'https://go.hotmart.com/G105459604D',
    tag:   'PACK · 4 EBOOKS',
    color: '#00CFFF',
  },
]

export default function EbooksSection() {
  return (
    <section className="h-full flex flex-col font-mono bg-[#020202] overflow-hidden relative">

      {/* Scanlines */}
      <div
        className="absolute inset-0 pointer-events-none opacity-[0.015]"
        style={{ backgroundImage: 'repeating-linear-gradient(0deg,transparent,transparent 3px,#00FF41 3px,#00FF41 4px)' }}
      />

      <div className="flex-1 overflow-y-auto px-6 pt-6 pb-4 min-h-0" style={{ scrollbarWidth: 'none' }}>

        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
          className="mb-6"
        >
          <p className="text-[8px] tracking-[0.6em] text-[#00FF41]/40 uppercase mb-3">
            {'// BIBLIOTECA DE OPERACIONES — GOLDENGEAR'}
          </p>
          <div
            className="relative p-5 border-l-2"
            style={{ borderColor: '#00FF41', background: 'rgba(0,255,65,0.025)' }}
          >
            <p className="text-base font-black tracking-[0.04em] text-white/80 uppercase leading-snug mb-1">
              Conocimiento que se aplica el mismo día.
            </p>
            <p className="text-base font-black tracking-[0.04em] uppercase leading-snug">
              <span className="text-[#00FF41]">Ebooks</span>{' '}
              <span className="text-white/80">diseñados para ejecutar, no para guardar.</span>
            </p>
          </div>
        </motion.div>

        {/* Cards */}
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          {PACKS.map((pack, i) => (
            <motion.div
              key={pack.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: 0.08 + i * 0.08 }}
              className="border flex flex-col"
              style={{ borderColor: `${pack.color}22`, background: '#0A0A0A' }}
            >
              {/* Cover image — 20% más chica: aspect-[5/3] vs [4/3] original */}
              <div className="relative w-full aspect-[5/3] overflow-hidden">
                <Image
                  src={pack.img}
                  alt={pack.title}
                  fill
                  className="object-cover"
                  sizes="(max-width: 640px) 100vw, 50vw"
                />
                <div
                  className="absolute top-2 left-2 px-2 py-0.5 text-[8px] tracking-[0.4em] font-bold uppercase"
                  style={{ background: pack.color, color: '#000' }}
                >
                  {pack.tag}
                </div>
              </div>

              {/* Body */}
              <div className="p-4 flex flex-col flex-1">
                <p
                  className="text-[9px] tracking-[0.5em] uppercase mb-1 font-bold"
                  style={{ color: pack.color }}
                >
                  {pack.title}
                </p>
                <p className="text-white/45 text-[10px] leading-relaxed mb-4 flex-1">
                  {pack.desc}
                </p>

                {/* Precio + CTAs */}
                <div className="flex items-center justify-between gap-2 flex-wrap">
                  <span className="text-white/90 text-xl font-bold tracking-tight shrink-0">
                    {pack.price}
                  </span>
                  <div className="flex gap-2">
                    <Link
                      href={`/biblioteca/${pack.id}`}
                      className="px-3 py-2 text-[9px] tracking-[0.35em] font-bold uppercase border transition-colors"
                      style={{ borderColor: `${pack.color}55`, color: pack.color }}
                    >
                      VER INFO
                    </Link>
                    <a
                      href={pack.href}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="px-3 py-2 text-[9px] tracking-[0.35em] font-bold uppercase transition-opacity hover:opacity-80"
                      style={{ background: pack.color, color: '#000' }}
                    >
                      OBTENER →
                    </a>
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Footer note */}
        <motion.p
          initial={{ opacity: 0 }} animate={{ opacity: 1 }}
          transition={{ duration: 0.4, delay: 0.28 }}
          className="text-center text-white/20 text-[9px] tracking-[0.3em] uppercase mt-6"
        >
          {'// ENTREGA INMEDIATA VÍA HOTMART · PAGO SEGURO'}
        </motion.p>

      </div>
    </section>
  )
}
