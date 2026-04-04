'use client'

import { motion } from 'framer-motion'

// ─── Datos de las ramas ────────────────────────────────────────────────────────

const RAMAS = [
  {
    id:    'automatizacion',
    icon:  '⚙',
    title: 'Automatización y Scripting',
    hint:  'Scripts, tareas automáticas y CLI tools',
  },
  {
    id:    'testing',
    icon:  '⬡',
    title: 'Testing y QA',
    hint:  'Core Pytest / Playwright',
  },
  {
    id:    'apis',
    icon:  '◈',
    title: 'APIs y Backend',
    hint:  'FastAPI / Django',
  },
  {
    id:    'datascience',
    icon:  '◉',
    title: 'Data Science y Análisis',
    hint:  'Pandas, NumPy y visualización',
  },
  {
    id:    'ia',
    icon:  '◬',
    title: 'Inteligencia Artificial Básica',
    hint:  'ML fundamentals y modelos base',
  },
] as const

// ─── Tarjeta individual bloqueada ─────────────────────────────────────────────

function RamaCard({ rama, index }: { rama: typeof RAMAS[number]; index: number }) {
  return (
    <motion.div
      className="relative flex flex-col border overflow-hidden min-w-0"
      style={{
        borderColor: 'rgba(255,184,0,0.18)',
        background:  'rgba(0,0,0,0.50)',
        opacity:     0.62,
      }}
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 0.62, y: 0 }}
      transition={{ delay: 0.08 + index * 0.06, duration: 0.38 }}
      whileHover={{ opacity: 0.78, transition: { duration: 0.15 } }}
    >
      {/* Esquinas decorativas ámbar */}
      <span className="absolute top-0 left-0  w-2 h-2 border-t border-l" style={{ borderColor: 'rgba(255,184,0,0.35)' }} />
      <span className="absolute top-0 right-0 w-2 h-2 border-t border-r" style={{ borderColor: 'rgba(255,184,0,0.35)' }} />
      <span className="absolute bottom-0 left-0  w-2 h-2 border-b border-l" style={{ borderColor: 'rgba(255,184,0,0.35)' }} />
      <span className="absolute bottom-0 right-0 w-2 h-2 border-b border-r" style={{ borderColor: 'rgba(255,184,0,0.35)' }} />

      <div className="px-3.5 py-3 flex flex-col gap-2 h-full">

        {/* Fila superior: ícono de dominio + candado */}
        <div className="flex items-start justify-between gap-2">

          {/* Ícono de dominio */}
          <span
            className="text-xl leading-none select-none"
            style={{ color: 'rgba(255,184,0,0.35)', textShadow: '0 0 8px rgba(255,184,0,0.20)' }}
          >
            {rama.icon}
          </span>

          {/* Candado dorado */}
          <motion.div
            className="flex items-center gap-1 border px-1.5 py-0.5 shrink-0"
            style={{
              borderColor: 'rgba(255,184,0,0.30)',
              background:  'rgba(255,184,0,0.06)',
            }}
            animate={{ opacity: [0.55, 0.85, 0.55] }}
            transition={{ duration: 2.8, repeat: Infinity, ease: 'easeInOut', delay: index * 0.35 }}
          >
            <span style={{ fontSize: 9, lineHeight: 1 }}>🔒</span>
            <span
              className="text-[6px] font-black tracking-[0.35em] font-mono"
              style={{ color: 'rgba(255,184,0,0.65)', textShadow: '0 0 6px rgba(255,184,0,0.40)' }}
            >
              LOCKED
            </span>
          </motion.div>
        </div>

        {/* Título de la rama */}
        <div className="flex-1">
          <p
            className="text-[10px] font-black tracking-[0.18em] uppercase font-mono leading-snug"
            style={{ color: 'rgba(255,184,0,0.55)', textShadow: '0 0 8px rgba(255,184,0,0.18)' }}
          >
            {rama.title}
          </p>
          <p
            className="text-[7px] tracking-[0.15em] font-mono mt-1 leading-relaxed"
            style={{ color: 'rgba(255,184,0,0.28)' }}
          >
            {rama.hint}
          </p>
        </div>

        {/* Badge de requisito */}
        <div
          className="border px-2 py-1"
          style={{
            borderColor: 'rgba(255,184,0,0.14)',
            background:  'rgba(255,184,0,0.03)',
          }}
        >
          <p
            className="text-[6px] tracking-[0.2em] font-mono leading-relaxed"
            style={{ color: 'rgba(255,184,0,0.40)' }}
          >
            <span style={{ color: 'rgba(255,184,0,0.55)' }}>Requiere:</span>
            {' '}Python Core{' '}
            <span className="font-black">(Nivel Avanzado)</span>
          </p>
        </div>

      </div>
    </motion.div>
  )
}

// ─── Componente principal ──────────────────────────────────────────────────────

export default function EspecializacionesGrid() {
  return (
    <section
      className="shrink-0 border-t w-full"
      style={{ borderColor: 'rgba(255,184,0,0.10)', background: 'rgba(0,0,0,0.30)' }}
    >
      {/* Línea de pulso superior */}
      <motion.div
        className="h-px w-full"
        style={{ background: 'linear-gradient(90deg, transparent, rgba(255,184,0,0.35), transparent)' }}
        animate={{ opacity: [0.25, 0.70, 0.25] }}
        transition={{ duration: 3, repeat: Infinity }}
      />

      <div className="px-4 sm:px-6 lg:px-10 py-3">

        {/* Header de sección */}
        <motion.div
          className="flex flex-wrap items-center justify-between gap-2 mb-3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.05 }}
        >
          <div className="flex items-center gap-3">
            <span
              className="text-[8px] font-black tracking-[0.55em] uppercase font-mono"
              style={{ color: 'rgba(255,184,0,0.50)', textShadow: '0 0 8px rgba(255,184,0,0.25)' }}
            >
              RAMAS DE ESPECIALIZACIÓN
            </span>
            <span
              className="text-[7px] tracking-[0.3em] font-mono hidden sm:block"
              style={{ color: 'rgba(255,184,0,0.22)' }}
            >
              // Rutas avanzadas — desbloqueables
            </span>
          </div>
          <span
            className="text-[6px] tracking-[0.4em] font-mono"
            style={{ color: 'rgba(255,184,0,0.20)' }}
          >
            5 RAMAS · TODAS BLOQUEADAS
          </span>
        </motion.div>

        {/* Grid de tarjetas — Mobile-First */}
        <div className="grid gap-2 grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5">
          {RAMAS.map((rama, i) => (
            <RamaCard key={rama.id} rama={rama} index={i} />
          ))}
        </div>

      </div>
    </section>
  )
}
