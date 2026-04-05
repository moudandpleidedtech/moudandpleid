'use client'

/**
 * Onboarding — Tour guiado por DAKI para nuevos Operadores.
 *
 * Modo estándar (7 pasos): conoce la plataforma, Python y el IDE.
 * Modo principiante (11 pasos): explicación desde cero, analogías simples,
 *   lenguaje coloquial para alguien que nunca escribió una línea de código.
 *
 * Flujo:
 *   Pantalla de elección → modo elegido → pasos → /hub
 */

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { motion, AnimatePresence } from 'framer-motion'

// ─── Mini terminal con typewriter ────────────────────────────────────────────

type LT = 'code' | 'output' | 'comment' | 'blank'
interface CodeLine { text: string; type: LT }

function MiniTerminal({ lines, color }: { lines: CodeLine[]; color: string }) {
  const [visible, setVisible] = useState(0)
  useEffect(() => { setVisible(0) }, [lines])
  useEffect(() => {
    if (visible >= lines.length) return
    const ms = lines[visible]?.type === 'blank' ? 60 : 200
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
    <div className="w-full font-mono text-[12px] leading-[1.85] p-3 mt-3 overflow-hidden"
      style={{ background: 'rgba(0,0,0,0.55)', border: `1px solid ${color}25` }}>
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

function DakiEye({ color }: { color: string }) {
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

// ─── Caja de analogía (solo modo principiante) ────────────────────────────────

function AnalogyBox({ emoji, title, text, color }: { emoji: string; title: string; text: string; color: string }) {
  return (
    <div className="mt-4 px-4 py-3 font-mono border text-left"
      style={{ borderColor: `${color}25`, background: `${color}06` }}>
      <div className="flex items-center gap-2 mb-1.5">
        <span className="text-xl leading-none">{emoji}</span>
        <span className="text-[10px] tracking-[0.3em] font-bold" style={{ color: `${color}90` }}>{title}</span>
      </div>
      <p className="text-[11px] leading-relaxed text-white/50">{text}</p>
    </div>
  )
}

// ─── Pasos — Modo Estándar ────────────────────────────────────────────────────

const STANDARD_STEPS = [
  {
    tag:   'PROTOCOLO 00 · BIENVENIDA',
    color: '#00FF41',
    title: 'Bienvenido al Nexo, Operador.',
    body:  'Soy DAKI — tu instructora táctica. Este sistema te va a enseñar Python desde cero. No con videos. No con textos. Con código real que vos escribís y ejecutás.\n\nCada misión tiene un objetivo concreto. Yo te observo, te pregunto, te señalo cuando algo falla. Nunca te doy la respuesta. Te hago llegar a ella.',
    code:  null,
    analogy: null,
  },
  {
    tag:   'MÓDULO 01 · CONCEPTOS BÁSICOS',
    color: '#00FF41',
    title: '¿Qué es programar?',
    body:  'Programar es escribir instrucciones precisas que una computadora puede ejecutar. Igual que una receta de cocina, pero sin margen de error: si decís "ponelo" en vez de "poné 200 gramos de harina", la receta falla.\n\nUna computadora hace exactamente lo que le decís — ni más, ni menos.',
    code:  [
      { text: '# Esto es una instrucción para la computadora', type: 'comment' as LT },
      { text: 'print("Hola, Operador")', type: 'code' as LT },
      { text: '', type: 'blank' as LT },
      { text: 'Hola, Operador', type: 'output' as LT },
    ],
    analogy: null,
  },
  {
    tag:   'MÓDULO 02 · PYTHON',
    color: '#00CFFF',
    title: 'Python: el idioma del Nexo.',
    body:  'Python es un lenguaje de programación. Es el idioma que usás para darle instrucciones a la máquina. Fue diseñado para ser legible — casi parece inglés.\n\nEs el lenguaje más usado en IA, ciencia de datos y automatización. Elegimos Python porque abre más puertas que cualquier otro lenguaje para empezar.',
    code:  [
      { text: '# Python es legible. Esto calcula y muestra el resultado:', type: 'comment' as LT },
      { text: 'resultado = 15 * 4 + 2', type: 'code' as LT },
      { text: 'print(resultado)', type: 'code' as LT },
      { text: '', type: 'blank' as LT },
      { text: '62', type: 'output' as LT },
    ],
    analogy: null,
  },
  {
    tag:   'MÓDULO 03 · VARIABLES',
    color: '#FFB800',
    title: 'Variables: cajas con nombre.',
    body:  'Una variable es como una caja etiquetada donde guardás un valor. La etiqueta es el nombre. Podés guardar números, texto, listas — lo que necesités.\n\nCuando necesitás ese valor más tarde, usás el nombre de la caja y Python recuerda qué había adentro.',
    code:  [
      { text: 'nombre = "Operador"', type: 'code' as LT },
      { text: 'nivel  = 1', type: 'code' as LT },
      { text: 'print(f"{nombre} · Nivel {nivel}")', type: 'code' as LT },
      { text: '', type: 'blank' as LT },
      { text: 'Operador · Nivel 1', type: 'output' as LT },
    ],
    analogy: null,
  },
  {
    tag:   'MÓDULO 04 · FUNCIONES',
    color: '#00CFFF',
    title: 'Funciones: instrucciones reutilizables.',
    body:  'Una función es un bloque de instrucciones con nombre. La definís una vez y la usás cuantas veces quieras. `def` le dice a Python: "voy a definir una función".',
    code:  [
      { text: 'def saludar(nombre):', type: 'code' as LT },
      { text: '    print(f"Acceso concedido, {nombre}")', type: 'code' as LT },
      { text: '', type: 'blank' as LT },
      { text: 'saludar("Operador")', type: 'code' as LT },
      { text: '', type: 'blank' as LT },
      { text: 'Acceso concedido, Operador', type: 'output' as LT },
    ],
    analogy: null,
  },
  {
    tag:   'MÓDULO 05 · EL EDITOR',
    color: '#00FF41',
    title: 'El IDE: donde escribís el código.',
    body:  'El editor (IDE) es tu espacio de trabajo. A la izquierda escribís el código Python. A la derecha ves la misión y los mensajes de DAKI.\n\nHacé clic en EJECUTAR (o Ctrl+Enter) para correr tu código. Si hay un error, yo te señalo exactamente la línea y te hago una pregunta para que lo resuelvas vos.',
    code:  [
      { text: '# Escribís esto en el editor...', type: 'comment' as LT },
      { text: 'print(10 + 5)', type: 'code' as LT },
      { text: '', type: 'blank' as LT },
      { text: '15   ✓', type: 'output' as LT },
    ],
    analogy: null,
  },
  {
    tag:   'PROTOCOLO COMPLETADO',
    color: '#00FF41',
    title: '¡Sistema listo, Operador!',
    body:  'Tenés todo lo que necesitás para empezar. Las primeras misiones son cortas y guiadas — yo voy a estar presente en todo momento.\n\nRecordá: el error no es el fracaso. El error es la información. Cada vez que algo falla, hay una razón precisa. Encontrarla es el ejercicio real.',
    code:  null,
    analogy: null,
  },
]

// ─── Pasos — Modo Principiante ────────────────────────────────────────────────

const BEGINNER_STEPS = [
  {
    tag:   '◈ PRIMERA TRANSMISIÓN',
    color: '#00FF41',
    title: 'Hola. Empecemos desde el principio.',
    body:  'Soy DAKI. Voy a guiarte paso a paso, sin apuros y sin palabras raras.\n\nSi en algún momento no entendés algo, está bien — eso es exactamente normal. No pasa nada. Yo estoy acá para explicarlo de la manera más simple posible.',
    code:  null,
    analogy: { emoji: '🤝', title: 'TE LO PROMETO', text: 'No voy a usar palabras técnicas sin explicarlas antes. Si lo hago, podés volver a leer.' },
  },
  {
    tag:   'PASO 1 · LA COMPUTADORA',
    color: '#00CFFF',
    title: 'La computadora no piensa. Obedece.',
    body:  'Una computadora es una máquina muy, muy rápida que solo hace lo que le decís. No improvisa. No adivina. Si le decís "sumá 2 + 2", lo hace. Si le decís "sumá 2 + pepino", te devuelve un error — porque pepino no es un número.\n\nNo tiene opinión propia. Necesita instrucciones exactas y sin errores.',
    code:  null,
    analogy: { emoji: '🤖', title: 'PENSALO ASÍ', text: 'La computadora es como un robot de cocina: superpoderoso, pero solo hace lo que le programás. Si le cargás mal los ingredientes, el plato sale mal.' },
  },
  {
    tag:   'PASO 2 · ¿QUÉ ES UN PROGRAMA?',
    color: '#FFB800',
    title: 'Un programa es una lista de instrucciones.',
    body:  'Un programa es simplemente una lista de instrucciones escritas en un idioma que la computadora entiende. Igual que una receta de cocina, pero para la máquina.\n\nCuando abrís WhatsApp, estás ejecutando un programa. Cuando jugás un videojuego, estás ejecutando un programa. Alguien los escribió.',
    code:  null,
    analogy: { emoji: '📋', title: 'COMO UNA RECETA', text: '"Calentar el horno. Mezclar la harina con los huevos. Poner en el molde 30 minutos." — Eso es exactamente lo que es un programa: pasos en orden.' },
  },
  {
    tag:   'PASO 3 · ¿QUÉ ES PYTHON?',
    color: '#00FF41',
    title: 'Python es el idioma que usamos para hablarle a la computadora.',
    body:  'Así como vos hablás español para comunicarte con personas, los programadores usan lenguajes especiales para comunicarse con las computadoras.\n\nPython es uno de esos lenguajes. Fue creado para que sea fácil de leer y escribir — parece casi inglés normal. Es el lenguaje más popular del mundo para aprender a programar.',
    code:  [
      { text: '# Esto es Python. Parece casi inglés, ¿no?', type: 'comment' as LT },
      { text: 'print("Hola, mundo")', type: 'code' as LT },
      { text: '', type: 'blank' as LT },
      { text: 'Hola, mundo', type: 'output' as LT },
    ],
    analogy: { emoji: '🌍', title: 'COMO UN IDIOMA', text: '"print" significa "mostrar en pantalla". Lo escribís, la computadora lo hace. Así de directo.' },
  },
  {
    tag:   'PASO 4 · TU PRIMERA INSTRUCCIÓN',
    color: '#00FF41',
    title: 'print() — mostrar algo en pantalla.',
    body:  'La instrucción más básica se llama print(). Lo que ponés adentro de los paréntesis aparece en la pantalla.\n\nCon las comillas le decís a Python: "esto es texto, no es código". Sin comillas piensa que es el nombre de algo que definiste antes.',
    code:  [
      { text: 'print("Soy nuevo en esto")', type: 'code' as LT },
      { text: '', type: 'blank' as LT },
      { text: 'Soy nuevo en esto', type: 'output' as LT },
      { text: '', type: 'blank' as LT },
      { text: 'print(2 + 2)', type: 'code' as LT },
      { text: '', type: 'blank' as LT },
      { text: '4', type: 'output' as LT },
    ],
    analogy: { emoji: '📺', title: 'COMO UN PROYECTOR', text: 'print() es tu forma de ver qué está pasando adentro del programa. Si querés saber un resultado, lo mostrás con print().' },
  },
  {
    tag:   'PASO 5 · VARIABLES',
    color: '#FFB800',
    title: 'Variables: guardá cosas con un nombre.',
    body:  'Una variable es como una caja con una etiqueta. En la etiqueta escribís el nombre. Adentro guardás un valor.\n\nDespués, cada vez que usás ese nombre, Python busca la caja y usa lo que hay adentro. Podés cambiar el contenido en cualquier momento.',
    code:  [
      { text: 'edad = 25         # caja llamada "edad", guarda 25', type: 'code' as LT },
      { text: 'ciudad = "Buenos Aires"', type: 'code' as LT },
      { text: '', type: 'blank' as LT },
      { text: 'print(edad)', type: 'code' as LT },
      { text: 'print(ciudad)', type: 'code' as LT },
      { text: '', type: 'blank' as LT },
      { text: '25', type: 'output' as LT },
      { text: 'Buenos Aires', type: 'output' as LT },
    ],
    analogy: { emoji: '📦', title: 'COMO UNA CAJA', text: 'edad = 25 significa: "creá una caja llamada edad y metele el número 25 adentro". El signo = no es "igual" — es "guardá esto acá".' },
  },
  {
    tag:   'PASO 6 · CÓMO SE CALCULAN COSAS',
    color: '#00CFFF',
    title: 'Python puede hacer cálculos.',
    body:  'Python hace matemática básica con los símbolos que ya conocés. Solo hay uno raro: el * para multiplicar (en vez de ×) y el / para dividir.\n\nPodés guardar resultados en variables y mostrarlos después.',
    code:  [
      { text: 'precio = 100', type: 'code' as LT },
      { text: 'descuento = 20', type: 'code' as LT },
      { text: 'final = precio - descuento', type: 'code' as LT },
      { text: '', type: 'blank' as LT },
      { text: 'print("Precio final:", final)', type: 'code' as LT },
      { text: '', type: 'blank' as LT },
      { text: 'Precio final: 80', type: 'output' as LT },
    ],
    analogy: { emoji: '🧮', title: 'COMO UNA CALCULADORA CON MEMORIA', text: 'Calculás, guardás el resultado en una variable, y después lo mostrás. En vez de anotar en papel, lo guardás en código.' },
  },
  {
    tag:   'PASO 7 · FUNCIONES',
    color: '#00FF41',
    title: 'Funciones: instrucciones con nombre propio.',
    body:  'Cuando tenés varias instrucciones que vas a necesitar usar varias veces, las metés en una función. Le ponés un nombre y la llamás cuando la necesitás.\n\n"def" es la palabra que usás para crearla. La indentación (los espacios al inicio) le dice a Python qué líneas están adentro de la función.',
    code:  [
      { text: 'def bienvenida(nombre):', type: 'code' as LT },
      { text: '    print("Hola,", nombre)', type: 'code' as LT },
      { text: '    print("Bienvenido al sistema")', type: 'code' as LT },
      { text: '', type: 'blank' as LT },
      { text: 'bienvenida("Ana")', type: 'code' as LT },
      { text: '', type: 'blank' as LT },
      { text: 'Hola, Ana', type: 'output' as LT },
      { text: 'Bienvenido al sistema', type: 'output' as LT },
    ],
    analogy: { emoji: '🎯', title: 'COMO UN BOTÓN', text: 'Definís la función una vez. Después la "llamás" por su nombre y hace todo lo que programaste. Como apretar un botón.' },
  },
  {
    tag:   'PASO 8 · LOS ERRORES SON NORMALES',
    color: '#FF4444',
    title: 'Los errores no son un fracaso.',
    body:  'Todos los programadores del mundo cometen errores todo el tiempo — incluso los más experimentados. La diferencia es que saben leer el mensaje de error para entender qué falló.\n\nPython te dice exactamente en qué línea hay un problema. Yo también voy a ayudarte a interpretarlo. Un error es información, no un castigo.',
    code:  [
      { text: '# Ejemplo de error — falta cerrar la comilla:', type: 'comment' as LT },
      { text: 'print("Hola)', type: 'code' as LT },
      { text: '', type: 'blank' as LT },
      { text: 'SyntaxError: EOL while scanning string literal', type: 'output' as LT },
      { text: '', type: 'blank' as LT },
      { text: '# Versión corregida:', type: 'comment' as LT },
      { text: 'print("Hola")', type: 'code' as LT },
      { text: '', type: 'blank' as LT },
      { text: 'Hola   ✓', type: 'output' as LT },
    ],
    analogy: { emoji: '🔧', title: 'COMO ARMAR UN MUEBLE', text: 'Si metés una pieza al revés, las instrucciones te dicen en qué paso fallaste. No tirás todo. Volvés a ese paso y lo corregís.' },
  },
  {
    tag:   'PASO 9 · EL EDITOR (IDE)',
    color: '#00FF41',
    title: 'El editor es tu taller.',
    body:  'Dentro de la plataforma vas a tener un editor de código — como un bloc de notas inteligente. Ahí escribís tu Python, apretás EJECUTAR, y la computadora corre lo que escribiste.\n\nSi algo falla, el editor te marca la línea con el problema. Yo te voy a dar una pista para que lo descubras vos.',
    code:  [
      { text: '# Escribís en el editor:', type: 'comment' as LT },
      { text: 'nombre = "Operador"', type: 'code' as LT },
      { text: 'print("Bienvenido,", nombre)', type: 'code' as LT },
      { text: '', type: 'blank' as LT },
      { text: '# Apretás EJECUTAR →', type: 'comment' as LT },
      { text: 'Bienvenido, Operador   ✓', type: 'output' as LT },
    ],
    analogy: null,
  },
  {
    tag:   'PROTOCOLO COMPLETADO ✓',
    color: '#00FF41',
    title: 'Ya tenés todo lo que necesitás para empezar.',
    body:  'Aprendiste qué es una computadora, qué es un programa, qué es Python, cómo funciona print(), qué son las variables, las funciones y los errores.\n\nLas primeras misiones son cortas y con mucho apoyo mío. No hay apuro. No hay nota. Hay progreso.\n\n¿Listo, Operador?',
    code:  null,
    analogy: { emoji: '🚀', title: 'LO QUE VIENE', text: 'Las primeras misiones te van a pedir hacer cosas muy simples. Cada misión enseña un concepto nuevo. Yo te acompaño en cada una.' },
  },
]

// ─── Pantalla de selección de camino ─────────────────────────────────────────

function PathSelector({ onStandard, onBeginner }: { onStandard: () => void; onBeginner: () => void }) {
  return (
    <div className="w-full max-w-xl relative z-10">
      <motion.div
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        className="border p-6 sm:p-8 text-center"
        style={{ borderColor: '#00FF4130', background: 'linear-gradient(160deg, #00FF4106 0%, rgba(0,0,0,0.7) 100%)' }}
      >
        <div className="absolute top-0 left-0 right-0 h-px"
          style={{ background: 'linear-gradient(90deg,transparent,#00FF4160,transparent)' }} />

        {/* DAKI */}
        <div className="flex justify-center mb-5">
          <DakiEye color="#00FF41" />
        </div>

        <p className="text-[9px] tracking-[0.5em] text-[#00FF41]/40 mb-3 font-mono">INICIANDO PROTOCOLO</p>
        <h1 className="text-2xl sm:text-3xl font-black text-white/90 leading-tight mb-2 font-mono">
          Bienvenido al Nexo.
        </h1>
        <p className="text-[12px] text-white/40 font-mono leading-relaxed mb-8">
          Soy DAKI. Antes de empezar, decime cuál es tu punto de partida.
        </p>

        {/* Opciones */}
        <div className="flex flex-col gap-3">

          {/* Opción principiante */}
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={onBeginner}
            className="w-full text-left px-5 py-4 border font-mono transition-all"
            style={{ borderColor: '#00CFFF40', background: '#00CFFF06', boxShadow: '0 0 20px #00CFFF08' }}
          >
            <div className="flex items-center gap-3">
              <span className="text-2xl">🐣</span>
              <div>
                <div className="text-[13px] font-black tracking-wide text-[#00CFFF]">
                  Es mi primera vez con código
                </div>
                <div className="text-[10px] text-white/30 mt-0.5">
                  Nunca escribí código. Quiero que me expliques todo desde cero.
                </div>
              </div>
              <span className="ml-auto text-[#00CFFF]/40 text-lg">→</span>
            </div>
          </motion.button>

          {/* Opción estándar */}
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={onStandard}
            className="w-full text-left px-5 py-4 border font-mono transition-all"
            style={{ borderColor: '#00FF4130', background: '#00FF4106' }}
          >
            <div className="flex items-center gap-3">
              <span className="text-2xl">⚡</span>
              <div>
                <div className="text-[13px] font-black tracking-wide text-[#00FF41]">
                  Sé algo de programación
                </div>
                <div className="text-[10px] text-white/30 mt-0.5">
                  Conozco lo básico. Quiero ver cómo funciona la plataforma.
                </div>
              </div>
              <span className="ml-auto text-[#00FF41]/40 text-lg">→</span>
            </div>
          </motion.button>

        </div>

        <p className="mt-5 text-[9px] text-white/20 font-mono tracking-widest">
          Podés saltar el tour en cualquier momento
        </p>
      </motion.div>
    </div>
  )
}

// ─── Componente de pasos ──────────────────────────────────────────────────────

function Steps({
  steps,
  onFinish,
}: {
  steps: typeof STANDARD_STEPS
  onFinish: () => void
}) {
  const [step, setStep] = useState(0)
  const total = steps.length
  const s     = steps[step]
  const isLast = step === total - 1

  return (
    <>
      {/* Header: progreso + skip */}
      <div className="w-full max-w-xl flex items-center justify-between mb-6 relative z-10">
        <div className="flex items-center gap-1.5 flex-wrap">
          {steps.map((_, i) => (
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
          onClick={onFinish}
          className="text-[10px] tracking-[0.35em] uppercase border px-4 py-1.5 transition-all duration-150 hover:opacity-80"
          style={{ borderColor: 'rgba(255,255,255,0.15)', color: 'rgba(255,255,255,0.35)' }}
        >
          SALTAR
        </button>
      </div>

      {/* Tarjeta */}
      <div className="w-full max-w-xl relative z-10">
        <AnimatePresence mode="wait">
          <motion.div
            key={step}
            initial={{ opacity: 0, x: 32 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -32 }}
            transition={{ duration: 0.22, ease: 'easeOut' }}
            className="border p-6 sm:p-8 relative"
            style={{
              borderColor: `${s.color}30`,
              background:  `linear-gradient(160deg, ${s.color}06 0%, rgba(0,0,0,0.7) 100%)`,
              boxShadow:   `0 0 40px ${s.color}08`,
            }}
          >
            <div className="absolute top-0 left-0 right-0 h-px"
              style={{ background: `linear-gradient(90deg,transparent,${s.color}60,transparent)` }} />

            <p className="text-[9px] tracking-[0.5em] mb-4 font-mono" style={{ color: `${s.color}50` }}>
              {s.tag}
            </p>

            <div className="flex items-start gap-5 mb-4">
              <DakiEye color={s.color} />
              <div className="flex-1 min-w-0 pt-1">
                <h1 className="text-xl sm:text-2xl font-black text-white/90 leading-tight mb-1 font-mono">
                  {s.title}
                </h1>
                <p className="text-[9px] tracking-[0.35em] font-mono" style={{ color: `${s.color}55` }}>
                  DAKI · TRANSMISIÓN ACTIVA
                </p>
              </div>
            </div>

            <p className="text-[12px] sm:text-[13px] leading-relaxed text-white/55 whitespace-pre-line font-mono">
              {s.body}
            </p>

            {s.code && <MiniTerminal lines={s.code} color={s.color} />}

            {s.analogy && (
              <AnalogyBox
                emoji={s.analogy.emoji}
                title={s.analogy.title}
                text={s.analogy.text}
                color={s.color}
              />
            )}
          </motion.div>
        </AnimatePresence>
      </div>

      {/* Navegación */}
      <div className="w-full max-w-xl flex items-center justify-between mt-5 relative z-10">
        <button
          onClick={() => setStep(s => Math.max(0, s - 1))}
          disabled={step === 0}
          className="text-[10px] tracking-[0.3em] uppercase px-5 py-2 border transition-all duration-150 disabled:opacity-20 disabled:cursor-not-allowed font-mono"
          style={{ borderColor: 'rgba(255,255,255,0.15)', color: 'rgba(255,255,255,0.4)' }}
        >
          ← ANTERIOR
        </button>

        <span className="text-[9px] tracking-[0.4em] font-mono" style={{ color: 'rgba(255,255,255,0.2)' }}>
          {step + 1} / {total}
        </span>

        <motion.button
          onClick={() => { if (isLast) onFinish(); else setStep(s => s + 1) }}
          whileHover={{ scale: 1.03 }}
          whileTap={{ scale: 0.97 }}
          className="text-[11px] tracking-[0.35em] uppercase px-6 py-2.5 font-black transition-all duration-150 font-mono"
          style={{ background: s.color, color: '#000', boxShadow: `0 0 20px ${s.color}40` }}
        >
          {isLast ? '[ INICIAR MISIÓN ]' : 'SIGUIENTE →'}
        </motion.button>
      </div>
    </>
  )
}

// ─── Página principal ─────────────────────────────────────────────────────────

type Mode = 'choose' | 'standard' | 'beginner'

export default function OnboardingPage() {
  const router = useRouter()
  const [mode, setMode] = useState<Mode>('choose')

  const finish = () => {
    try { localStorage.setItem('onboarding_done', 'true') } catch { /* */ }
    router.push('/hub')
  }

  useEffect(() => {
    try {
      if (localStorage.getItem('onboarding_done') === 'true') router.replace('/hub')
    } catch { /* */ }
  }, [router])

  return (
    <div className="min-h-screen bg-[#020202] font-mono flex flex-col items-center justify-center px-4 py-8 relative overflow-hidden">

      <style>{`
        @keyframes ob-blink { 0%,100%{opacity:1} 50%{opacity:0} }
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

      <AnimatePresence mode="wait">
        {mode === 'choose' && (
          <motion.div key="choose" className="w-full flex justify-center"
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
            <PathSelector
              onStandard={() => setMode('standard')}
              onBeginner={() => setMode('beginner')}
            />
          </motion.div>
        )}

        {mode === 'standard' && (
          <motion.div key="standard" className="w-full flex flex-col items-center"
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
            <Steps steps={STANDARD_STEPS} onFinish={finish} />
          </motion.div>
        )}

        {mode === 'beginner' && (
          <motion.div key="beginner" className="w-full flex flex-col items-center"
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
            <Steps steps={BEGINNER_STEPS} onFinish={finish} />
          </motion.div>
        )}
      </AnimatePresence>

    </div>
  )
}
