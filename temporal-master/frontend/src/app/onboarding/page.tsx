'use client'

/**
 * Onboarding — Tour guiado por DAKI para nuevos Operadores.
 *
 * 7 pasos: bienvenida → programación → Python → variables →
 *          funciones → el IDE → listo.
 * Siempre visible: botón SALTAR.
 * Al terminar o saltar → localStorage 'onboarding_done' = true → /hub
 */

import { useState, useEffect, useId } from 'react'
import { useRouter } from 'next/navigation'
import { motion, AnimatePresence } from 'framer-motion'

// ─── Mini terminal con typewriter ────────────────────────────────────────────

type LT = 'code' | 'output' | 'comment' | 'blank'
interface CodeLine { text: string; type: LT }

function MiniTerminal({ lines, color }: { lines: CodeLine[]; color: string }) {
  const [visible, setVisible] = useState(0)

  // Reiniciar al cambiar líneas
  useEffect(() => { setVisible(0) }, [lines])

  useEffect(() => {
    if (visible >= lines.length) return
    const ms = lines[visible]?.type === 'blank' ? 60 : 220
    const t = setTimeout(() => setVisible(v => v + 1), ms)
    return () => clearTimeout(t)
  }, [visible, lines])

  const lineColor = (type: LT) => {
    switch (type) {
      case 'output':  return 'rgba(0,255,65,0.9)'
      case 'comment': return 'rgba(255,255,255,0.28)'
      case 'blank':   return 'transparent'
      default:        return 'rgba(255,255,255,0.72)'
    }
  }

  return (
    <div
      className="w-full font-mono text-[12px] leading-[1.85] p-3 mt-3 overflow-hidden"
      style={{ background: 'rgba(0,0,0,0.55)', border: `1px solid ${color}25` }}
    >
      {/* Barra del terminal */}
      <div className="flex gap-1.5 mb-2.5">
        {[0.5, 0.28, 0.14].map((o, i) => (
          <span key={i} className="w-2 h-2 rounded-full" style={{ background: color, opacity: o }} />
        ))}
      </div>
      {lines.slice(0, visible).map((line, i) => (
        <div key={i}>
          {line.type === 'blank' ? <span>&nbsp;</span> : (
            <span style={{ color: lineColor(line.type) }}>
              {line.text}
              {i === visible - 1 && (
                <span className="inline-block w-[5px] h-[11px] ml-0.5 align-middle"
                  style={{ background: color, animation: 'ob-blink 0.75s step-end infinite' }} />
              )}
            </span>
          )}
        </div>
      ))}
    </div>
  )
}

// ─── Ojo de DAKI ─────────────────────────────────────────────────────────────

function DakiEye({ step }: { step: number }) {
  const colors = ['#00FF41', '#00CFFF', '#00FF41', '#FFB800', '#00CFFF', '#00FF41', '#00FF41']
  const color = colors[step % colors.length]
  return (
    <div className="relative flex items-center justify-center w-20 h-20 shrink-0">
      <motion.div className="absolute w-20 h-20 rounded-full"
        style={{ background: `radial-gradient(circle, ${color}20 0%, transparent 70%)` }}
        animate={{ scale: [1, 1.3, 1], opacity: [0.5, 1, 0.5] }}
        transition={{ duration: 2.5, repeat: Infinity, ease: 'easeInOut' }}
      />
      <motion.div className="absolute w-14 h-14 rounded-full border"
        style={{ borderColor: `${color}35` }}
        animate={{ scale: [1, 1.12, 1], opacity: [0.25, 0.55, 0.25] }}
        transition={{ duration: 2.2, repeat: Infinity, ease: 'easeInOut', delay: 0.15 }}
      />
      <motion.span className="text-5xl leading-none"
        style={{ color, textShadow: `0 0 22px ${color}80, 0 0 50px ${color}30` }}
        animate={{ scale: [1, 1.08, 1], opacity: [0.8, 1, 0.8] }}
        transition={{ duration: 2, repeat: Infinity, ease: 'easeInOut' }}
      >◈</motion.span>
    </div>
  )
}

// ─── Datos de los pasos ───────────────────────────────────────────────────────

const STEPS = [
  {
    tag:     'PROTOCOLO 00 · BIENVENIDA',
    color:   '#00FF41',
    title:   'Bienvenido al Nexo, Operador.',
    body:    'Soy DAKI — tu instructora táctica. Este sistema te va a enseñar Python desde cero. No con videos. No con textos. Con código real que vos escribís y ejecutás.\n\nCada misión tiene un objetivo concreto. Yo te observo, te pregunto, te señalo cuando algo falla. Nunca te doy la respuesta. Te hago llegar a ella.',
    code:    null,
  },
  {
    tag:     'MÓDULO 01 · CONCEPTOS BÁSICOS',
    color:   '#00FF41',
    title:   '¿Qué es programar?',
    body:    'Programar es escribir instrucciones precisas que una computadora puede ejecutar. Igual que una receta de cocina, pero sin margen de error: si decís "ponelo" en vez de "poné 200 gramos de harina", la receta falla.\n\nUna computadora hace exactamente lo que le decís — ni más, ni menos.',
    code: [
      { text: '# Esto es una instrucción para la computadora', type: 'comment' as LT },
      { text: 'print("Hola, Operador")', type: 'code' as LT },
      { text: '', type: 'blank' as LT },
      { text: 'Hola, Operador', type: 'output' as LT },
    ],
  },
  {
    tag:     'MÓDULO 02 · PYTHON',
    color:   '#00CFFF',
    title:   'Python: el idioma del Nexo.',
    body:    'Python es un lenguaje de programación. Es el idioma que usás para darle instrucciones a la máquina. Fue diseñado para ser legible — casi parece inglés.\n\nEs el lenguaje más usado en IA, ciencia de datos y automatización. Elegimos Python porque abre más puertas que cualquier otro lenguaje para empezar.',
    code: [
      { text: '# Python es legible. Esto calcula y muestra el resultado:', type: 'comment' as LT },
      { text: 'resultado = 15 * 4 + 2', type: 'code' as LT },
      { text: 'print(resultado)', type: 'code' as LT },
      { text: '', type: 'blank' as LT },
      { text: '62', type: 'output' as LT },
    ],
  },
  {
    tag:     'MÓDULO 03 · VARIABLES',
    color:   '#FFB800',
    title:   'Variables: cajas con nombre.',
    body:    'Una variable es como una caja etiquetada donde guardás un valor. La etiqueta es el nombre. Podés guardar números, texto, listas — lo que necesites.\n\nCuando necesitás ese valor más tarde, usás el nombre de la caja y Python recuerda qué había adentro.',
    code: [
      { text: 'nombre = "Operador"       # caja llamada "nombre"', type: 'code' as LT },
      { text: 'nivel  = 1                # caja llamada "nivel"', type: 'code' as LT },
      { text: 'xp     = 0', type: 'code' as LT },
      { text: '', type: 'blank' as LT },
      { text: 'print(f"{nombre} · Nivel {nivel} · XP: {xp}")', type: 'code' as LT },
      { text: '', type: 'blank' as LT },
      { text: 'Operador · Nivel 1 · XP: 0', type: 'output' as LT },
    ],
  },
  {
    tag:     'MÓDULO 04 · FUNCIONES',
    color:   '#00CFFF',
    title:   'Funciones: instrucciones reutilizables.',
    body:    'Una función es un bloque de instrucciones con nombre. La definís una vez y la usás cuantas veces quieras. Como un comando guardado.\n\n`def` le dice a Python: "voy a definir una función". Los dos puntos y la indentación (el espacio al inicio) son obligatorios — Python los usa para saber qué está adentro de la función.',
    code: [
      { text: 'def saludar(nombre):', type: 'code' as LT },
      { text: '    print(f"Acceso concedido, {nombre}")', type: 'code' as LT },
      { text: '', type: 'blank' as LT },
      { text: 'saludar("Operador")   # llamar la función', type: 'code' as LT },
      { text: 'saludar("DAKI")', type: 'code' as LT },
      { text: '', type: 'blank' as LT },
      { text: 'Acceso concedido, Operador', type: 'output' as LT },
      { text: 'Acceso concedido, DAKI', type: 'output' as LT },
    ],
  },
  {
    tag:     'MÓDULO 05 · EL EDITOR',
    color:   '#00FF41',
    title:   'El IDE: donde escribís el código.',
    body:    'El editor (IDE) es tu espacio de trabajo. A la izquierda escribís el código Python. A la derecha ves la misión y los mensajes de DAKI.\n\nHacé clic en EJECUTAR (o Ctrl+Enter) para correr tu código. Si hay un error, yo te señalo exactamente la línea y te hago una pregunta para que lo resuelvas vos.',
    code: [
      { text: '# Escribís esto en el editor...', type: 'comment' as LT },
      { text: 'x = 10', type: 'code' as LT },
      { text: 'y = 5', type: 'code' as LT },
      { text: 'print(x + y)', type: 'code' as LT },
      { text: '', type: 'blank' as LT },
      { text: '# ...presionás EJECUTAR...', type: 'comment' as LT },
      { text: '15                         ✓', type: 'output' as LT },
    ],
  },
  {
    tag:     'PROTOCOLO COMPLETADO',
    color:   '#00FF41',
    title:   '¡Sistema listo, Operador!',
    body:    'Tenés todo lo que necesitás para empezar. Las primeras misiones son cortas y guiadas — yo voy a estar presente en todo momento.\n\nRecordá: el error no es el fracaso. El error es la información. Cada vez que algo falla, hay una razón precisa. Encontrarla es el ejercicio real.',
    code: null,
  },
]

// ─── Página principal ─────────────────────────────────────────────────────────

export default function OnboardingPage() {
  const router  = useRouter()
  const [step,  setStep]  = useState(0)
  const [done,  setDone]  = useState(false)

  const total = STEPS.length
  const s     = STEPS[step]

  const finish = () => {
    try { localStorage.setItem('onboarding_done', 'true') } catch { /* */ }
    router.push('/hub')
  }

  const next = () => {
    if (step < total - 1) setStep(s => s + 1)
    else finish()
  }

  const prev = () => { if (step > 0) setStep(s => s - 1) }

  // Nunca mostrar si ya completó (por si accede directo a la URL)
  useEffect(() => {
    try {
      if (localStorage.getItem('onboarding_done') === 'true') router.replace('/hub')
    } catch { /* */ }
  }, [router])

  const isLast = step === total - 1

  return (
    <div className="min-h-screen bg-[#020202] font-mono flex flex-col items-center justify-center px-4 py-8 relative overflow-hidden">

      <style>{`
        @keyframes ob-blink { 0%,100%{opacity:1} 50%{opacity:0} }
        @keyframes ob-scan  { 0%{transform:translateY(-100%)} 100%{transform:translateY(100vh)} }
      `}</style>

      {/* Scanlines */}
      <div className="absolute inset-0 pointer-events-none opacity-[0.015]"
        style={{ backgroundImage: 'repeating-linear-gradient(0deg,transparent,transparent 3px,#00FF41 3px,#00FF41 4px)' }} />

      {/* Grid */}
      <div className="absolute inset-0 pointer-events-none"
        style={{
          backgroundImage: 'linear-gradient(rgba(0,255,65,0.03) 1px,transparent 1px),linear-gradient(90deg,rgba(0,255,65,0.03) 1px,transparent 1px)',
          backgroundSize: '72px 72px',
        }} />

      {/* Header: progreso + skip */}
      <div className="w-full max-w-xl flex items-center justify-between mb-6 relative z-10">
        <div className="flex items-center gap-1.5">
          {STEPS.map((_, i) => (
            <motion.div key={i}
              className="h-1 rounded-full transition-all duration-300"
              style={{
                width:      i === step ? 28 : 8,
                background: i <= step ? s.color : 'rgba(255,255,255,0.12)',
              }}
            />
          ))}
        </div>
        <button
          onClick={finish}
          className="text-[10px] tracking-[0.35em] uppercase border px-4 py-1.5 transition-all duration-150 hover:opacity-80"
          style={{ borderColor: 'rgba(255,255,255,0.15)', color: 'rgba(255,255,255,0.35)' }}
        >
          SALTAR
        </button>
      </div>

      {/* Tarjeta principal */}
      <div className="w-full max-w-xl relative z-10">
        <AnimatePresence mode="wait">
          <motion.div
            key={step}
            initial={{ opacity: 0, x: 32 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -32 }}
            transition={{ duration: 0.22, ease: 'easeOut' }}
            className="border p-6 sm:p-8"
            style={{
              borderColor: `${s.color}30`,
              background:  `linear-gradient(160deg, ${s.color}06 0%, rgba(0,0,0,0.7) 100%)`,
              boxShadow:   `0 0 40px ${s.color}08`,
            }}
          >
            {/* Acento superior */}
            <div className="absolute top-0 left-0 right-0 h-px"
              style={{ background: `linear-gradient(90deg,transparent,${s.color}60,transparent)` }} />

            {/* Tag */}
            <p className="text-[9px] tracking-[0.5em] mb-4" style={{ color: `${s.color}50` }}>
              {s.tag}
            </p>

            {/* Avatar + título */}
            <div className="flex items-start gap-5 mb-4">
              <DakiEye step={step} />
              <div className="flex-1 min-w-0 pt-1">
                <h1 className="text-xl sm:text-2xl font-black text-white/90 leading-tight mb-1">
                  {s.title}
                </h1>
                <p className="text-[9px] tracking-[0.35em]" style={{ color: `${s.color}55` }}>
                  DAKI · TRANSMISIÓN ACTIVA
                </p>
              </div>
            </div>

            {/* Cuerpo */}
            <p className="text-[12px] sm:text-[13px] leading-relaxed text-white/55 whitespace-pre-line">
              {s.body}
            </p>

            {/* Terminal de código */}
            {s.code && <MiniTerminal lines={s.code} color={s.color} />}

          </motion.div>
        </AnimatePresence>
      </div>

      {/* Navegación */}
      <div className="w-full max-w-xl flex items-center justify-between mt-5 relative z-10">
        <button
          onClick={prev}
          disabled={step === 0}
          className="text-[10px] tracking-[0.3em] uppercase px-5 py-2 border transition-all duration-150 disabled:opacity-20 disabled:cursor-not-allowed"
          style={{ borderColor: 'rgba(255,255,255,0.15)', color: 'rgba(255,255,255,0.4)' }}
        >
          ← ANTERIOR
        </button>

        <span className="text-[9px] tracking-[0.4em]" style={{ color: 'rgba(255,255,255,0.2)' }}>
          {step + 1} / {total}
        </span>

        <motion.button
          onClick={next}
          whileHover={{ scale: 1.03 }}
          whileTap={{ scale: 0.97 }}
          className="text-[11px] tracking-[0.35em] uppercase px-6 py-2.5 font-black transition-all duration-150"
          style={{
            background:  s.color,
            color:       '#000',
            boxShadow:   `0 0 20px ${s.color}40`,
          }}
        >
          {isLast ? '[ INICIAR MISIÓN ]' : 'SIGUIENTE →'}
        </motion.button>
      </div>

    </div>
  )
}
