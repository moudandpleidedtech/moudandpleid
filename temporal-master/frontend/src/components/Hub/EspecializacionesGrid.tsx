'use client'

import { motion } from 'framer-motion'

// ─── Datos de las ramas ────────────────────────────────────────────────────────

const RAMAS = [
  {
    id:        'automatizacion',
    icon:      '⚙',
    title:     'Automatización y Scripting',
    hint:      'Scripts, tareas automáticas y CLI tools',
    jobs:      ['DevOps Engineer', 'SRE', 'Backend Dev'],
    unlockAt:  60,
  },
  {
    id:        'testing',
    icon:      '⬡',
    title:     'Testing y QA',
    hint:      'Pytest · Playwright · CI pipelines',
    jobs:      ['QA Engineer', 'SDET', 'Test Automation'],
    unlockAt:  70,
  },
  {
    id:        'apis',
    icon:      '◈',
    title:     'APIs y Backend',
    hint:      'FastAPI · Django · REST',
    jobs:      ['Backend Developer', 'API Engineer', 'Full Stack'],
    unlockAt:  75,
  },
  {
    id:        'datascience',
    icon:      '◉',
    title:     'Data Science y Análisis',
    hint:      'Pandas · NumPy · visualización',
    jobs:      ['Data Analyst', 'Data Scientist', 'BI Developer'],
    unlockAt:  80,
  },
  {
    id:        'ia',
    icon:      '◬',
    title:     'Inteligencia Artificial',
    hint:      'ML fundamentals · modelos base',
    jobs:      ['ML Engineer', 'AI Developer', 'Data Scientist'],
    unlockAt:  90,
  },
] as const

// ─── Tarjeta individual bloqueada ─────────────────────────────────────────────

function RamaCard({ rama, index, completedCount }: { rama: typeof RAMAS[number]; index: number; completedCount: number }) {
  const pct = Math.min(100, Math.round((completedCount / rama.unlockAt) * 100))
  const remaining = Math.max(0, rama.unlockAt - completedCount)
  return (
    <motion.div
      className="relative flex flex-col border overflow-hidden min-w-0"
      style={{
        borderColor: 'rgba(255,184,0,0.22)',
        background:  'rgba(0,0,0,0.50)',
        opacity:     0.70,
      }}
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 0.70, y: 0 }}
      transition={{ delay: 0.08 + index * 0.06, duration: 0.38 }}
      whileHover={{ opacity: 0.88, transition: { duration: 0.15 } }}
    >
      {/* Esquinas decorativas ámbar */}
      <span className="absolute top-0 left-0  w-2 h-2 border-t border-l" style={{ borderColor: 'rgba(255,184,0,0.40)' }} />
      <span className="absolute top-0 right-0 w-2 h-2 border-t border-r" style={{ borderColor: 'rgba(255,184,0,0.40)' }} />
      <span className="absolute bottom-0 left-0  w-2 h-2 border-b border-l" style={{ borderColor: 'rgba(255,184,0,0.40)' }} />
      <span className="absolute bottom-0 right-0 w-2 h-2 border-b border-r" style={{ borderColor: 'rgba(255,184,0,0.40)' }} />

      <div className="px-3.5 py-3 flex flex-col gap-2 h-full">

        {/* Fila superior: ícono de dominio + candado */}
        <div className="flex items-start justify-between gap-2">

          {/* Ícono de dominio */}
          <span
            className="text-xl leading-none select-none"
            style={{ color: 'rgba(255,184,0,0.50)', textShadow: '0 0 8px rgba(255,184,0,0.25)' }}
          >
            {rama.icon}
          </span>

          {/* Candado dorado */}
          <motion.div
            className="flex items-center gap-1 border px-1.5 py-0.5 shrink-0"
            style={{
              borderColor: 'rgba(255,184,0,0.35)',
              background:  'rgba(255,184,0,0.08)',
            }}
            animate={{ opacity: [0.60, 0.90, 0.60] }}
            transition={{ duration: 2.8, repeat: Infinity, ease: 'easeInOut', delay: index * 0.35 }}
          >
            <span style={{ fontSize: 9, lineHeight: 1 }}>🔒</span>
            <span
              className="text-[10px] font-black tracking-[0.3em] font-mono"
              style={{ color: 'rgba(255,184,0,0.80)', textShadow: '0 0 6px rgba(255,184,0,0.40)' }}
            >
              LOCKED
            </span>
          </motion.div>
        </div>

        {/* Título de la rama */}
        <div className="flex-1">
          <p
            className="text-xs font-black tracking-[0.15em] uppercase font-mono leading-snug"
            style={{ color: 'rgba(255,184,0,0.75)', textShadow: '0 0 8px rgba(255,184,0,0.20)' }}
          >
            {rama.title}
          </p>
          <p
            className="text-[10px] tracking-[0.10em] font-mono mt-1 leading-relaxed"
            style={{ color: 'rgba(255,184,0,0.45)' }}
          >
            {rama.hint}
          </p>
        </div>

        {/* Roles de mercado */}
        <div
          className="border px-2 py-1.5"
          style={{
            borderColor: 'rgba(255,184,0,0.18)',
            background:  'rgba(255,184,0,0.04)',
          }}
        >
          <p
            className="text-[9px] tracking-[0.25em] font-mono mb-1"
            style={{ color: 'rgba(255,184,0,0.45)' }}
          >
            SALIDAS LABORALES
          </p>
          <div className="flex flex-wrap gap-1 mb-2">
            {rama.jobs.map(job => (
              <span
                key={job}
                className="text-[10px] font-mono px-1.5 py-0.5 border"
                style={{
                  color:       'rgba(255,184,0,0.70)',
                  borderColor: 'rgba(255,184,0,0.22)',
                  background:  'rgba(255,184,0,0.06)',
                }}
              >
                {job}
              </span>
            ))}
          </div>
          {/* Barra de desbloqueo */}
          <div className="flex items-center gap-2 mt-1.5">
            <div className="flex-1 h-[3px] rounded-full overflow-hidden" style={{ background: 'rgba(255,184,0,0.10)' }}>
              <motion.div
                className="h-full rounded-full"
                initial={{ width: 0 }}
                animate={{ width: `${pct}%` }}
                transition={{ duration: 0.8, ease: 'easeOut', delay: 0.1 + index * 0.08 }}
                style={{ background: pct >= 100 ? 'rgba(255,184,0,0.90)' : 'rgba(255,184,0,0.45)' }}
              />
            </div>
            <span className="text-[9px] font-mono shrink-0" style={{ color: 'rgba(255,184,0,0.50)' }}>
              {remaining > 0 ? `−${remaining} niveles` : 'LISTO'}
            </span>
          </div>
        </div>

      </div>
    </motion.div>
  )
}

// ─── Componente principal ──────────────────────────────────────────────────────

export default function EspecializacionesGrid({ completedCount = 0 }: { completedCount?: number }) {
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
              className="text-[11px] font-black tracking-[0.45em] uppercase font-mono"
              style={{ color: 'rgba(255,184,0,0.70)', textShadow: '0 0 8px rgba(255,184,0,0.25)' }}
            >
              RAMAS DE ESPECIALIZACIÓN
            </span>
            <span
              className="text-[10px] tracking-[0.25em] font-mono hidden sm:block"
              style={{ color: 'rgba(255,184,0,0.35)' }}
            >
              // Rutas avanzadas — desbloqueables
            </span>
          </div>
          <span
            className="text-[10px] tracking-[0.35em] font-mono"
            style={{ color: 'rgba(255,184,0,0.40)' }}
          >
            5 RAMAS · TODAS BLOQUEADAS
          </span>
        </motion.div>

        {/* Grid de tarjetas — Mobile-First */}
        <div className="grid gap-2 grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5">
          {RAMAS.map((rama, i) => (
            <RamaCard key={rama.id} rama={rama} index={i} completedCount={completedCount} />
          ))}
        </div>

      </div>
    </section>
  )
}
