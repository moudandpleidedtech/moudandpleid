/**
 * useMicroBroadcast — Hook para micro-transmisiones tácticas de DAKI
 *
 * Banco de 30 tips sobre Python y programación.
 * Cooldown: 90s entre mensajes (localStorage para persistir entre challenges).
 * Triggers:
 *   - Al iniciar un challenge: después de 30s de actividad
 *   - Al completar un challenge: inmediatamente
 *   - Al 4to fallo consecutivo: mensaje de recuperación
 */

import { useCallback, useEffect, useRef, useState } from 'react'

const TIPS: string[] = [
  'Las variables en Python no necesitan declararse con un tipo. Python lo infiere solo.',
  'range(n) genera números de 0 a n-1. range(1, n+1) los genera de 1 a n.',
  'len() funciona en strings, listas, tuplas y diccionarios.',
  'Una función sin return explícito devuelve None automáticamente.',
  'Los índices negativos en listas acceden desde el final: lista[-1] es el último elemento.',
  'f"Hola {nombre}" es más eficiente que "Hola " + nombre para concatenar strings.',
  'print() acepta múltiples argumentos separados por coma. Úsalo para depurar.',
  'El operador // realiza división entera (descarta decimales). 7 // 2 = 3.',
  '% calcula el resto de una división. 7 % 2 = 1. Útil para saber si un número es par.',
  'Las listas son mutables. Las tuplas son inmutables. Usa tuplas cuando los datos no cambian.',
  'in verifica si un elemento está en una colección: if x in lista:',
  'enumerate(lista) te da índice y valor a la vez en un for.',
  'zip(lista1, lista2) combina dos listas elemento por elemento.',
  'sorted() retorna una nueva lista ordenada. sort() ordena la lista en sitio.',
  'str.split() divide un string en partes. str.join() hace lo contrario.',
  'strip() elimina espacios y saltos de línea al inicio y fin de un string.',
  'Los diccionarios guardan pares clave:valor. Accedes por clave: d["nombre"].',
  'dict.get("clave", valor_default) no lanza KeyError si la clave no existe.',
  'Una comprensión de lista [x*2 for x in lista] es más pythónica que un for con append.',
  'try/except captura errores y evita que el programa se detenga inesperadamente.',
  'El scope de Python es LEGB: Local → Enclosing → Global → Built-in.',
  'Los parámetros con * capturan múltiples argumentos posicionales en una función.',
  'is compara identidad de objeto. == compara valor. Para None siempre usa is None.',
  'type(x) devuelve el tipo de x. isinstance(x, int) verifica si x es de tipo int.',
  'Las funciones son ciudadanos de primera clase en Python: se pueden pasar como argumentos.',
  'int("42") convierte string a entero. str(42) convierte entero a string.',
  'abs(x) retorna el valor absoluto. max(a, b) y min(a, b) son funciones incorporadas.',
  'El operador ** eleva a potencia: 2**8 = 256. pow(2, 8) hace lo mismo.',
  'round(3.14159, 2) redondea a 2 decimales: 3.14.',
  'Los comentarios con # son ignorados por Python. Úsalos para explicar lógica compleja.',
]

const COOLDOWN_KEY = 'daki_microbroadcast_last'
const COOLDOWN_MS  = 90_000  // 90 segundos

function pickTip(lastMessage: string | null): string {
  const available = lastMessage ? TIPS.filter((t) => t !== lastMessage) : TIPS
  return available[Math.floor(Math.random() * available.length)]
}

export function useMicroBroadcast(failStreak: number) {
  const [message, setMessage] = useState<string | null>(null)
  const lastMessageRef         = useRef<string | null>(null)
  const challengeTimerRef      = useRef<ReturnType<typeof setTimeout>>()

  const dismiss = useCallback(() => setMessage(null), [])

  const fire = useCallback(() => {
    // Respect cooldown
    try {
      const last = parseInt(localStorage.getItem(COOLDOWN_KEY) ?? '0', 10)
      if (Date.now() - last < COOLDOWN_MS) return
      localStorage.setItem(COOLDOWN_KEY, String(Date.now()))
    } catch { /* storage blocked */ }

    const tip = pickTip(lastMessageRef.current)
    lastMessageRef.current = tip
    setMessage(tip)
    setTimeout(() => setMessage(null), 6000)
  }, [])

  // Trigger: at 4th consecutive fail
  useEffect(() => {
    if (failStreak === 4) fire()
  }, [failStreak, fire])

  // Auto-dismiss timer handled inside fire()
  // Return fire so CodeWorkspace can call it at challenge start and on victory
  return { message, dismiss, fire }
}
