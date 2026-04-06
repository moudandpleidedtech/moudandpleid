'use client'

/**
 * FlashRecallModal — Retrieval Practice entre misiones (Roediger & Butler, 2011)
 *
 * Aparece entre misiones con una pregunta de opción múltiple sobre conceptos ya vistos.
 * 15s de tiempo. 4 opciones. Nunca bloquea la navegación — el botón "Saltar" siempre visible.
 * El feedback es inmediato: verde/rojo con la respuesta correcta.
 */

import { useEffect, useRef, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

interface Question {
  id: string
  concept: string
  question: string
  options: string[]
  correct: number   // índice de la opción correcta
  explanation: string
}

const QUESTION_BANK: Question[] = [
  {
    id: 'q1', concept: 'variable',
    question: '¿Qué imprime este código?\nx = 5\nx = x + 3\nprint(x)',
    options: ['5', '3', '8', 'Error'],
    correct: 2,
    explanation: 'x se reasigna a 5+3=8. Las variables pueden cambiar de valor.',
  },
  {
    id: 'q2', concept: 'for_loop',
    question: '¿Cuántas veces itera este bucle?\nfor i in range(3):',
    options: ['2', '3', '4', '1'],
    correct: 1,
    explanation: 'range(3) genera [0, 1, 2] — tres valores, tres iteraciones.',
  },
  {
    id: 'q3', concept: 'string',
    question: '¿Cuál es el resultado de "nexo"[0]?',
    options: ['"nexo"', '"n"', '"o"', 'Error'],
    correct: 1,
    explanation: 'Los índices comienzan en 0. El primer carácter es "n".',
  },
  {
    id: 'q4', concept: 'function',
    question: 'Una función sin return explícito devuelve:',
    options: ['0', '""', 'None', 'Error'],
    correct: 2,
    explanation: 'Python retorna None implícitamente cuando no hay return.',
  },
  {
    id: 'q5', concept: 'if_else',
    question: '¿Qué imprime?\nx = 10\nif x > 5:\n    print("A")\nelse:\n    print("B")',
    options: ['B', 'A', 'AB', 'Error'],
    correct: 1,
    explanation: '10 > 5 es True, entonces ejecuta el bloque if: imprime "A".',
  },
  {
    id: 'q6', concept: 'list',
    question: '¿Qué hace lista.append(42)?',
    options: ['Crea una nueva lista', 'Inserta 42 al inicio', 'Agrega 42 al final', 'Elimina el último'],
    correct: 2,
    explanation: 'append() agrega el elemento al final de la lista.',
  },
  {
    id: 'q7', concept: 'number',
    question: '¿Cuál es el resultado de 7 % 3?',
    options: ['2', '1', '0', '3'],
    correct: 1,
    explanation: '7 dividido por 3 da cociente 2 y resto 1. 7 % 3 = 1.',
  },
  {
    id: 'q8', concept: 'while_loop',
    question: '¿Qué condición detiene un while?',
    options: ['Cuando la condición es True', 'Cuando la condición es False', 'Después de 10 veces', 'Nunca'],
    correct: 1,
    explanation: 'El while continúa mientras la condición sea True. Se detiene cuando es False.',
  },
  {
    id: 'q9', concept: 'dict',
    question: '¿Cómo accedo al valor "Python" en {"lang": "Python"}?',
    options: ['d[0]', 'd.lang', 'd["lang"]', 'd.get[0]'],
    correct: 2,
    explanation: 'Los diccionarios se acceden por clave: d["lang"] retorna "Python".',
  },
  {
    id: 'q10', concept: 'print_fn',
    question: '¿Cuál es la salida de print(2 + 3)?',
    options: ['"2 + 3"', '5', '"5"', 'Error'],
    correct: 1,
    explanation: 'Python evalúa 2+3=5 primero, luego print muestra el número 5.',
  },
  {
    id: 'q11', concept: 'input_fn',
    question: 'input() siempre retorna un valor de tipo:',
    options: ['int', 'float', 'str', 'bool'],
    correct: 2,
    explanation: 'input() siempre retorna string. Usa int() o float() para convertir.',
  },
  {
    id: 'q12', concept: 'range_fn',
    question: '¿Qué genera range(2, 5)?',
    options: ['[2, 3, 4, 5]', '[2, 3, 4]', '[1, 2, 3, 4]', '[2, 5]'],
    correct: 1,
    explanation: 'range(start, stop) genera desde start hasta stop-1: [2, 3, 4].',
  },
  {
    id: 'q13', concept: 'boolean',
    question: '¿Cuál es el resultado de not True?',
    options: ['True', 'False', '1', '0'],
    correct: 1,
    explanation: 'not invierte el booleano. not True = False.',
  },
  {
    id: 'q14', concept: 'return_stmt',
    question: '¿Qué hace return en una función?',
    options: ['Detiene el programa', 'Imprime un valor', 'Devuelve un valor y termina la función', 'Crea una variable'],
    correct: 2,
    explanation: 'return devuelve el valor al llamador y termina la ejecución de la función.',
  },
  {
    id: 'q15', concept: 'variable',
    question: '¿Cuál de estos es un nombre de variable válido en Python?',
    options: ['2nombre', 'mi-variable', '_dato', 'class'],
    correct: 2,
    explanation: '_dato es válido. Los nombres no pueden empezar con número, tener guiones o ser palabras reservadas.',
  },
]

const TIME_LIMIT   = 15   // segundos
const HISTORY_KEY  = 'daki-flash-history'  // Record<questionId, {correct: number, wrong: number}>

type QuestionHistory = Record<string, { correct: number; wrong: number }>

function loadHistory(): QuestionHistory {
  try {
    const raw = localStorage.getItem(HISTORY_KEY)
    return raw ? JSON.parse(raw) : {}
  } catch { return {} }
}

function saveResult(questionId: string, wasCorrect: boolean): void {
  try {
    const h = loadHistory()
    if (!h[questionId]) h[questionId] = { correct: 0, wrong: 0 }
    if (wasCorrect) h[questionId].correct += 1
    else            h[questionId].wrong   += 1
    localStorage.setItem(HISTORY_KEY, JSON.stringify(h))
  } catch {}
}

function pickQuestion(concepts: string[], lastId: string | null): Question {
  const history = loadHistory()

  // Peso de cada pregunta: preguntas con más errores tienen mayor probabilidad
  // Nunca vistas → peso base 2. Incorrectas anteriores → peso proporcional.
  const scored = QUESTION_BANK
    .filter((q) => q.id !== lastId)
    .map((q) => {
      const h = history[q.id]
      const wrong   = h?.wrong   ?? 0
      const correct = h?.correct ?? 0
      // Prioridad 1: conceptos del challenge actual + errores previos
      const conceptMatch = concepts.includes(q.concept) ? 3 : 1
      const errorBonus   = wrong > 0 ? wrong * 2 : 0
      const masteryPenalty = correct >= 3 ? -1 : 0  // deprioritizar preguntas ya dominadas
      const weight = Math.max(1, conceptMatch + errorBonus + masteryPenalty)
      return { q, weight }
    })

  // Selección ponderada
  const totalWeight = scored.reduce((sum, s) => sum + s.weight, 0)
  let rand = Math.random() * totalWeight
  for (const { q, weight } of scored) {
    rand -= weight
    if (rand <= 0) return q
  }
  return scored[scored.length - 1].q
}

interface Props {
  visible: boolean
  conceptsTaught?: string[]
  onClose: () => void
}

export default function FlashRecallModal({ visible, conceptsTaught = [], onClose }: Props) {
  const [question, setQuestion]       = useState<Question | null>(null)
  const [selected, setSelected]       = useState<number | null>(null)
  const [revealed, setRevealed]       = useState(false)
  const [timeLeft, setTimeLeft]       = useState(TIME_LIMIT)
  const lastIdRef                      = useRef<string | null>(null)
  const timerRef                       = useRef<ReturnType<typeof setInterval>>()

  // Pick question on open
  useEffect(() => {
    if (!visible) return
    const q = pickQuestion(conceptsTaught, lastIdRef.current)
    setQuestion(q)
    setSelected(null)
    setRevealed(false)
    setTimeLeft(TIME_LIMIT)
    lastIdRef.current = q.id

    timerRef.current = setInterval(() => {
      setTimeLeft((t) => {
        if (t <= 1) {
          clearInterval(timerRef.current)
          setRevealed(true)
          // Timeout cuenta como respuesta incorrecta para el historial
          setQuestion((q) => { if (q) saveResult(q.id, false); return q })
          return 0
        }
        return t - 1
      })
    }, 1000)

    return () => clearInterval(timerRef.current)
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [visible])

  const handleSelect = (idx: number) => {
    if (revealed || !question) return
    clearInterval(timerRef.current)
    setSelected(idx)
    setRevealed(true)
    saveResult(question.id, idx === question.correct)
  }

  if (!question) return null

  const isCorrect = selected === question.correct
  const timerPct  = (timeLeft / TIME_LIMIT) * 100

  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 z-[200] flex items-center justify-center"
          style={{ background: 'rgba(0,4,0,0.85)' }}
        >
          <motion.div
            initial={{ scale: 0.88, y: 24 }}
            animate={{ scale: 1, y: 0 }}
            exit={{ scale: 0.92, opacity: 0 }}
            transition={{ type: 'spring', stiffness: 300, damping: 26 }}
            className="w-full max-w-md font-mono border"
            style={{
              background: '#030A03',
              borderColor: '#00FF4130',
              boxShadow: '0 0 40px #00FF4115',
            }}
          >
            {/* Header */}
            <div
              className="flex items-center justify-between px-4 py-2 border-b"
              style={{ borderColor: '#00FF4118' }}
            >
              <div>
                <span className="text-[8px] tracking-[0.5em] text-[#00FF41]/40">FLASH RECALL</span>
                <span className="ml-3 text-[8px] tracking-widest text-[#00FF41]/25">◆ {question.concept.toUpperCase()}</span>
              </div>
              <button
                onClick={onClose}
                className="text-[10px] text-[#00FF41]/25 hover:text-[#00FF41]/60 tracking-widest"
              >
                SALTAR
              </button>
            </div>

            {/* Timer bar */}
            <div className="h-0.5 bg-[#00FF41]/10">
              <motion.div
                className="h-full"
                style={{ width: `${timerPct}%`, background: timeLeft > 5 ? '#00FF41' : '#FF4444' }}
                animate={{ width: `${timerPct}%` }}
                transition={{ duration: 0.9, ease: 'linear' }}
              />
            </div>

            {/* Question */}
            <div className="px-5 py-4">
              <pre className="text-[11px] text-[#C0FFC0]/80 leading-relaxed whitespace-pre-wrap mb-4">
                {question.question}
              </pre>

              {/* Options */}
              <div className="grid grid-cols-1 gap-2">
                {question.options.map((opt, idx) => {
                  let borderColor = '#00FF4118'
                  let textColor   = '#C0FFC0CC'
                  let bg          = 'transparent'
                  if (revealed) {
                    if (idx === question.correct) {
                      borderColor = '#00FF41'; textColor = '#00FF41'; bg = '#00FF4110'
                    } else if (idx === selected && !isCorrect) {
                      borderColor = '#FF4444'; textColor = '#FF4444'; bg = '#FF444410'
                    } else {
                      textColor = '#C0FFC040'
                    }
                  }
                  return (
                    <button
                      key={idx}
                      onClick={() => handleSelect(idx)}
                      disabled={revealed}
                      className="text-left px-3 py-2 text-[10px] tracking-wide border transition-all"
                      style={{ borderColor, color: textColor, background: bg }}
                    >
                      {String.fromCharCode(65 + idx)}. {opt}
                    </button>
                  )
                })}
              </div>

              {/* Explanation */}
              {revealed && (
                <motion.div
                  initial={{ opacity: 0, y: 6 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="mt-4 px-3 py-2 text-[9px] leading-relaxed border"
                  style={{
                    borderColor: isCorrect ? '#00FF4130' : '#FF444430',
                    color: isCorrect ? '#00FF4180' : '#FF444480',
                    background: isCorrect ? '#00FF4108' : '#FF444408',
                  }}
                >
                  {isCorrect ? '✓ CORRECTO — ' : '✗ INCORRECTO — '}{question.explanation}
                </motion.div>
              )}
            </div>

            {/* Footer */}
            {revealed && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="px-4 pb-3 flex justify-end"
              >
                <button
                  onClick={onClose}
                  className="text-[9px] tracking-[0.4em] px-3 py-1.5 border text-[#00FF41] border-[#00FF4140] hover:bg-[#00FF4110]"
                >
                  CONTINUAR →
                </button>
              </motion.div>
            )}
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}
