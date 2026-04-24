'use client'

import { useState } from 'react'
import Image from 'next/image'
import { motion, AnimatePresence } from 'framer-motion'

const PACKS = [
  {
    id:    'el-negocio-solo',
    title: 'El Negocio Solo',
    desc:  'Construí un negocio digital que funciona sin que estés mirando. Sistemas, automatizaciones y flujos que trabajan por vos.',
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
    id:    'automatiza-con-ia',
    title: 'Automatiza tu Trabajo con IA',
    desc:  'Flujos reales con Claude, Make y herramientas de IA para multiplicar tu output sin contratar a nadie.',
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

type Pack = typeof PACKS[number]

function PackModal({ pack, onClose }: { pack: Pack; onClose: () => void }) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.18 }}
      className="fixed inset-0 z-50 flex flex-col font-mono"
      style={{ background: 'rgba(2,2,2,0.97)' }}
      onClick={onClose}
    >
      <div
        className="flex-1 overflow-y-auto px-5 py-6 max-w-xl mx-auto w-full"
        onClick={e => e.stopPropagation()}
      >
        {/* Cerrar */}
        <button
          onClick={onClose}
          className="text-xs tracking-[0.4em] uppercase mb-6 inline-block"
          style={{ color: `${pack.color}70` }}
        >
          ← CERRAR
        </button>

        {/* Título + Hook */}
        <div className="mb-6 border-l-2 pl-4" style={{ borderColor: pack.color }}>
          <p className="text-[10px] tracking-[0.5em] uppercase mb-2" style={{ color: pack.color }}>
            {pack.tag}
          </p>
          <p className="text-white/95 text-2xl font-black uppercase tracking-wide leading-tight mb-2">
            {pack.title}
          </p>
          <p className="text-base italic leading-relaxed text-white/60">
            {pack.hook}
          </p>
        </div>

        {/* Por qué */}
        <div
          className="mb-6 p-5"
          style={{ background: `${pack.color}08`, border: `1px solid ${pack.color}20` }}
        >
          <p className="text-xs tracking-[0.4em] uppercase mb-3" style={{ color: `${pack.color}80` }}>
            POR QUÉ ESTE PACK
          </p>
          <p className="text-white/65 text-sm leading-relaxed mb-3">{pack.why}</p>
          <p className="text-xs pt-3 border-t" style={{ borderColor: `${pack.color}20`, color: `${pack.color}70` }}>
            Para quién: {pack.para}
          </p>
        </div>

        {/* 3 ebooks */}
        <div className="mb-6">
          <p className="text-xs tracking-[0.4em] uppercase mb-3" style={{ color: `${pack.color}80` }}>
            LO QUE OBTENÉS
          </p>
          <div className="space-y-3">
            {pack.items.map((item, i) => (
              <div key={i} className="p-4 border-l-2" style={{ borderColor: `${pack.color}40`, background: '#0A0A0A' }}>
                <p className="text-white/90 text-sm font-bold mb-1">{item.name}</p>
                <p className="text-white/50 text-xs leading-relaxed">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>

        {/* CTA */}
        <div
          className="flex items-center justify-between gap-4 p-5 border"
          style={{ borderColor: `${pack.color}30`, background: '#0A0A0A' }}
        >
          <div>
            <p className="text-white/95 text-3xl font-bold tracking-tight">{pack.price}</p>
            <p className="text-white/35 text-xs mt-0.5">pago único · acceso de por vida</p>
          </div>
          <a
            href={pack.href}
            target="_blank"
            rel="noopener noreferrer"
            className="px-6 py-3 text-xs tracking-[0.4em] font-bold uppercase"
            style={{ background: pack.color, color: '#000' }}
          >
            OBTENER →
          </a>
        </div>

        <p className="text-center text-white/20 text-xs tracking-[0.3em] uppercase mt-5">
          {'// PAGO SEGURO VÍA HOTMART · ENTREGA INMEDIATA'}
        </p>
      </div>
    </motion.div>
  )
}

export default function EbooksSection() {
  const [activePack, setActivePack] = useState<Pack | null>(null)

  return (
    <section className="min-h-screen font-mono bg-[#020202] relative">

      <div
        className="absolute inset-0 pointer-events-none opacity-[0.015]"
        style={{ backgroundImage: 'repeating-linear-gradient(0deg,transparent,transparent 3px,#00FF41 3px,#00FF41 4px)' }}
      />

      <div className="px-6 sm:px-10 pt-16 pb-10">

        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 8 }} whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }} transition={{ duration: 0.3 }}
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
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.3, delay: 0.08 + i * 0.08 }}
              className="border flex flex-col"
              style={{ borderColor: `${pack.color}22`, background: '#0A0A0A' }}
            >
              {/* Imagen */}
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
                    <button
                      onClick={() => setActivePack(pack)}
                      className="px-3 py-2 text-[9px] tracking-[0.35em] font-bold uppercase border transition-colors"
                      style={{ borderColor: `${pack.color}55`, color: pack.color }}
                    >
                      VER INFO
                    </button>
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

        <motion.p
          initial={{ opacity: 0 }} whileInView={{ opacity: 1 }}
          viewport={{ once: true }} transition={{ duration: 0.4, delay: 0.15 }}
          className="text-center text-white/20 text-[9px] tracking-[0.3em] uppercase mt-6"
        >
          {'// ENTREGA INMEDIATA VÍA HOTMART · PAGO SEGURO'}
        </motion.p>

      </div>

      {/* Modal */}
      <AnimatePresence>
        {activePack && (
          <PackModal pack={activePack} onClose={() => setActivePack(null)} />
        )}
      </AnimatePresence>
    </section>
  )
}
