'use client'

import { useParams } from 'next/navigation'
import Image from 'next/image'
import Link  from 'next/link'
import { motion } from 'framer-motion'

const PACKS = {
  'el-negocio-solo': {
    title: 'El Negocio Solo',
    tag:   'PACK · 4 EBOOKS',
    hook:  'Un negocio que trabaja aunque vos no estés.',
    why: [
      'La mayoría intercambia horas por dinero y llama a eso un negocio. No lo es.',
      'Un negocio real tiene sistemas: atrae clientes, los convierte, los retiene — sin que vos estés presente en cada paso.',
      'Este pack te da las piezas para construir eso desde cero.',
    ],
    para:  'Freelancers, consultores y creadores que quieren escalar sin trabajar más horas.',
    items: [
      { name: 'El Freelancer de 3K',  desc: 'Cómo posicionarte para cobrar lo que vale tu trabajo y atraer clientes que pagan sin regatear.' },
      { name: 'Emails que Venden',     desc: 'Secuencias de email reales para nutrir leads y convertirlos sin llamadas de ventas.' },
      { name: 'La Ventaja Injusta',    desc: 'Diferenciarte cuando todos ofrecen lo mismo. Estrategia de posicionamiento para mercados saturados.' },
      { name: 'Notion para Humanos',   desc: 'Organizá tu negocio, clientes y proyectos sin perder tiempo en sistemas complicados.' },
    ],
    bonus: [
      'Plantillas editables para cada sistema',
      'Entrega inmediata — acceso en minutos',
      'Acceso de por vida al material',
    ],
    price: '$27 USD',
    img:   '/assets/ebook-el-negocio-solo.png',
    href:  'https://go.hotmart.com/C105461511Y',
    color: '#00FF41',
  },
  'automatiza-con-ia': {
    title: 'Automatiza tu Trabajo con IA',
    tag:   'PACK · 4 EBOOKS',
    hook:  'Más output. Sin contratar a nadie más.',
    why: [
      'La IA no reemplaza a los que saben usarla — los hace inalcanzables.',
      'Mientras otros experimentan con prompts sueltos, este pack te da flujos completos probados en producción.',
      'Aplicables desde el día uno, sin necesitar saber programar.',
    ],
    para:  'Creadores, emprendedores y profesionales que quieren hacer más en menos tiempo usando IA.',
    items: [
      { name: '50 Flujos con Claude',  desc: '50 automatizaciones reales con Claude AI organizadas por caso de uso: marketing, ops, atención, contenido.' },
      { name: 'IA para Creadores',     desc: 'Cómo usar IA para producir contenido en escala sin perder tu voz ni tu estilo.' },
      { name: 'Make en 5 Días',        desc: 'Construí tus primeras automatizaciones reales con Make (ex-Integromat) en una semana.' },
      { name: 'Python en 7 Días',      desc: 'Base técnica para entender y modificar scripts de IA sin depender de nadie.' },
    ],
    bonus: [
      'Flujos listos para copiar y adaptar',
      'Entrega inmediata — acceso en minutos',
      'Acceso de por vida al material',
    ],
    price: '$27 USD',
    img:   '/assets/ebook-automatiza-con-ia.png',
    href:  'https://go.hotmart.com/G105459604D',
    color: '#00CFFF',
  },
} as const

type PackId = keyof typeof PACKS

export default function BibliotecaPackPage() {
  const { id } = useParams<{ id: string }>()
  const pack = PACKS[id as PackId]

  if (!pack) {
    return (
      <main className="min-h-screen flex items-center justify-center bg-[#020202] font-mono">
        <div className="text-center">
          <p className="text-[#FF0033] text-sm mb-4">[ PACK NO ENCONTRADO ]</p>
          <Link href="/" className="text-[#00FF41]/60 text-[9px] tracking-[0.4em] uppercase">← VOLVER</Link>
        </div>
      </main>
    )
  }

  return (
    <main
      className="min-h-screen font-mono bg-[#020202] relative"
      style={{
        backgroundImage:      'url(/assets/daki-bg.jpg)',
        backgroundAttachment: 'fixed',
        backgroundSize:       'cover',
        backgroundPosition:   'center',
      }}
    >
      <div className="fixed inset-0 pointer-events-none" style={{ background: 'rgba(4,6,4,0.92)' }} />
      <div
        className="fixed inset-0 pointer-events-none opacity-[0.015]"
        style={{ backgroundImage: 'repeating-linear-gradient(0deg,transparent,transparent 3px,#00FF41 3px,#00FF41 4px)' }}
      />

      <div className="relative z-10 max-w-xl mx-auto px-5 py-8">

        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.2 }}>
          <Link
            href="/"
            className="text-[8px] tracking-[0.5em] uppercase mb-6 inline-block"
            style={{ color: `${pack.color}60` }}
          >
            ← VOLVER AL NEXO
          </Link>
        </motion.div>

        {/* Imagen */}
        <motion.div
          initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.05 }}
          className="relative w-full aspect-[16/7] overflow-hidden mb-5"
          style={{ border: `1px solid ${pack.color}20` }}
        >
          <Image src={pack.img} alt={pack.title} fill className="object-cover" sizes="580px" />
          <div className="absolute inset-0" style={{ background: 'linear-gradient(to top, #020202 0%, transparent 60%)' }} />
          <div
            className="absolute top-3 left-3 px-2 py-0.5 text-[7px] tracking-[0.45em] font-bold uppercase"
            style={{ background: pack.color, color: '#000' }}
          >
            {pack.tag}
          </div>
        </motion.div>

        {/* Título + Hook */}
        <motion.div
          initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.1 }}
          className="mb-5"
        >
          <p className="text-white/90 text-lg font-black uppercase tracking-wide leading-tight mb-1">
            {pack.title}
          </p>
          <p className="text-[11px] italic leading-relaxed" style={{ color: pack.color }}>
            {pack.hook}
          </p>
        </motion.div>

        {/* Por qué */}
        <motion.div
          initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.14 }}
          className="mb-5 p-4 border-l-2"
          style={{ borderColor: pack.color, background: `${pack.color}08` }}
        >
          <p className="text-[7px] tracking-[0.5em] uppercase mb-3" style={{ color: `${pack.color}70` }}>
            POR QUÉ ESTE PACK
          </p>
          {pack.why.map((p, i) => (
            <p key={i} className="text-white/55 text-[10px] leading-relaxed mb-2 last:mb-0">{p}</p>
          ))}
          <p className="text-[8px] mt-3 pt-3 border-t" style={{ borderColor: `${pack.color}20`, color: `${pack.color}60` }}>
            Para quién: {pack.para}
          </p>
        </motion.div>

        {/* Qué incluye */}
        <motion.div
          initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.18 }}
          className="mb-5"
        >
          <p className="text-[7px] tracking-[0.5em] uppercase mb-3" style={{ color: `${pack.color}70` }}>
            LO QUE OBTENÉS
          </p>
          <div className="space-y-2">
            {pack.items.map((item, i) => (
              <div key={i} className="p-3 border-l" style={{ borderColor: `${pack.color}30`, background: '#0A0A0A' }}>
                <p className="text-white/80 text-[10px] font-bold mb-0.5">{item.name}</p>
                <p className="text-white/35 text-[9px] leading-relaxed">{item.desc}</p>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Bonus */}
        <motion.div
          initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.22 }}
          className="mb-6"
        >
          <p className="text-[7px] tracking-[0.5em] uppercase mb-2" style={{ color: `${pack.color}70` }}>
            ADEMÁS
          </p>
          <ul className="space-y-1">
            {pack.bonus.map((b, i) => (
              <li key={i} className="flex items-center gap-2">
                <span className="text-[9px]" style={{ color: pack.color }}>✓</span>
                <span className="text-white/40 text-[9px]">{b}</span>
              </li>
            ))}
          </ul>
        </motion.div>

        {/* CTA */}
        <motion.div
          initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.26 }}
          className="flex items-center justify-between gap-4 p-4 border"
          style={{ borderColor: `${pack.color}30`, background: '#0A0A0A' }}
        >
          <div>
            <p className="text-white/90 text-2xl font-bold tracking-tight">{pack.price}</p>
            <p className="text-white/25 text-[8px]">pago único · acceso de por vida</p>
          </div>
          <a
            href={pack.href}
            target="_blank"
            rel="noopener noreferrer"
            className="px-5 py-3 text-[9px] tracking-[0.4em] font-bold uppercase"
            style={{ background: pack.color, color: '#000' }}
          >
            OBTENER AHORA →
          </a>
        </motion.div>

        <p className="text-center text-white/15 text-[7px] tracking-[0.35em] uppercase mt-4">
          {'// PAGO SEGURO VÍA HOTMART · ENTREGA INMEDIATA'}
        </p>

      </div>
    </main>
  )
}
