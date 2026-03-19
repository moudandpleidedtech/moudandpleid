/**
 * dakiVoice.ts — DAKI Audio Engine V3
 * =====================================
 *
 * Secuencia garantizada:
 *   1. Reproduce /public/sounds/daki_alert.mp3 (SFX corto)
 *   2. Solo cuando el SFX termina → inicia TTS con prefijo conversacional
 *
 * Calibración v3.1 — Guardiana Cálida (voz confirmada):
 *   • Voz principal: "Microsoft Elvira Online (Natural)" — es-ES, Neural femenina
 *   • pitch  = 1.0  → sin corrección; Elvira ya es genuinamente femenina
 *   • rate   = 0.9  → dicción pausada y calmada
 *   • volume = 0.9  → nítida por encima del SFX atenuado (0.25)
 *   • Prefijo "Operador, un pequeño ajuste táctico para ti." → cálido y personal
 *   • cancelDakiVoice() detiene también el SFX en curso
 */

// ─── Tipos ────────────────────────────────────────────────────────────────────

export type DakiLevel = 1 | 2 | 3

interface VoiceProfile {
  pitch: number
  rate: number
  volume: number
  /** Nombres de voz preferidos para coincidencia exacta. */
  preferredVoices: string[]
  /** Locales aceptables como fallback (es-ES, es-AR, etc.). */
  localeFallback: string[]
  /**
   * Si es true, reproduce daki_alert.mp3 antes de comenzar a hablar.
   * Solo para niveles con personalidad (2 y 3); el nivel 1 es puro texto.
   */
  withAlert: boolean
  /**
   * Si es true, antepone "Aviso. ... " al texto para crear una micro-pausa
   * que separa el SFX de la información real y refuerza la atención.
   */
  withPrefix: boolean
}

// ─── Perfiles de voz ─────────────────────────────────────────────────────────

const VOICE_PROFILES: Record<DakiLevel, VoiceProfile> = {
  1: {
    // Robótico — mecánico, plano, sin entonación. Sin SFX ni prefijo.
    pitch:  0.55,
    rate:   0.78,
    volume: 0.92,
    preferredVoices: ['Microsoft David', 'Daniel', 'Alex', 'Fred', 'Trinoids'],
    localeFallback:  ['en-US', 'en-GB', 'en'],
    withAlert:  false,
    withPrefix: false,
  },
  2: {
    // Amistoso — Guardiana cálida. Voz principal: Elvira Neural (es-ES).
    pitch:  1.0,
    rate:   0.9,
    volume: 0.9,
    preferredVoices: [
      // ── Voz confirmada ───────────────────────────────────────────────────
      'Microsoft Elvira Online (Natural)',   // es-ES ★ primera opción
      // ── Fallbacks femeninas (por si Elvira no está disponible) ───────────
      'Microsoft Laura Online (Natural)',    // es-ES, Neural femenina
      'Microsoft Dalia Online (Natural)',    // es-MX, Neural femenina
      'Microsoft Sabina Online (Natural)',   // es-MX, Neural femenina
      'Microsoft Helena',                   // es-ES, estándar femenina
      'Paulina',                            // macOS es-MX femenina
      'Mónica', 'Monica',                   // macOS es-ES femenina
    ],
    localeFallback: ['es-ES', 'es-MX', 'es-AR', 'es-US', 'es'],
    withAlert:  true,
    withPrefix: true,
  },
  3: {
    // Compañero — misma voz, rate ligeramente más pausado.
    pitch:  1.0,
    rate:   0.85,
    volume: 0.9,
    preferredVoices: [
      'Microsoft Elvira Online (Natural)',
      'Microsoft Laura Online (Natural)',
      'Microsoft Dalia Online (Natural)',
      'Microsoft Sabina Online (Natural)',
      'Microsoft Helena',
      'Paulina',
      'Mónica', 'Monica',
    ],
    localeFallback: ['es-ES', 'es-MX', 'es-AR', 'es-US', 'es'],
    withAlert:  true,
    withPrefix: true,
  },
}

// ─── Keywords premium (Tier-1 del selector de voz) ───────────────────────────

/**
 * Keywords para el Tier-2 del selector de voz (coincidencia parcial de nombre).
 * Se usan cuando no hay coincidencia exacta en `preferredVoices`.
 *
 * Incluimos voces Neural femeninas de Microsoft porque son genuinamente
 * femeninas sin distorsión de pitch. El Uncanny Valley previo era causado
 * por aplicar pitch alto a voces masculinas/neutras, no por las Neural en sí.
 */
const PREFERRED_KEYWORDS = [
  'elvira',   // Microsoft Elvira Online (Natural) — voz principal confirmada
  'laura',    // Microsoft Laura Online (Natural)
  'dalia',    // Microsoft Dalia Online (Natural)
  'sabina',   // Microsoft Sabina Online (Natural)
  'helena',   // Microsoft Helena
  'monica',   // macOS Monica / Mónica
  'paulina',  // macOS Paulina
] as const

// ─── Estado interno ───────────────────────────────────────────────────────────

/** Referencia al <audio> del SFX en curso, para poder cancelarlo. */
let _currentSfx: HTMLAudioElement | null = null

// ─── Reproducción del SFX de alerta ─────────────────────────────────────────

/**
 * Reproduce /sounds/daki_alert.mp3 y resuelve la promesa cuando termina.
 * Si el archivo falla (error 404, autoplay policy, etc.), resuelve igualmente
 * para que el TTS nunca quede bloqueado.
 */
function playAlertSfx(): Promise<void> {
  return new Promise((resolve) => {
    // Detiene un SFX previo si lo hubiera
    if (_currentSfx) {
      _currentSfx.pause()
      _currentSfx.currentTime = 0
    }

    const audio = new Audio('/sounds/daki_alert.mp3')
    audio.volume = 0.25  // Atenuado: SFX de fondo, no opaca la voz
    _currentSfx = audio

    const cleanup = () => {
      _currentSfx = null
      resolve()
    }

    audio.onended = cleanup
    audio.onerror = cleanup  // Fallback: no bloquear el TTS si el SFX falla

    audio.play().catch(cleanup)  // Autoplay policy: resuelve en vez de lanzar
  })
}

// ─── Diagnóstico de voces disponibles ────────────────────────────────────────

/**
 * Imprime en consola todas las voces del sistema agrupadas por idioma.
 * Útil para calibrar `preferredVoices` en distintos navegadores/SO.
 *
 * Uso desde DevTools:
 *   import('@/lib/dakiVoice').then(m => m.logAvailableVoices())
 *
 * O temporalmente en un componente:
 *   useEffect(() => { logAvailableVoices() }, [])
 */
export async function logAvailableVoices(): Promise<void> {
  const voices = await loadVoices()
  const spanish = voices.filter(v => v.lang.startsWith('es'))
  const others  = voices.filter(v => !v.lang.startsWith('es'))

  console.group('🎙️ DAKI — Voces disponibles')
  console.group(`Español (${spanish.length} voces)`)
  spanish.forEach(v =>
    console.log(`  [${v.lang}] "${v.name}" | local=${v.localService} | default=${v.default}`)
  )
  console.groupEnd()
  console.group(`Otros idiomas (${others.length} voces)`)
  others.forEach(v =>
    console.log(`  [${v.lang}] "${v.name}"`)
  )
  console.groupEnd()
  console.groupEnd()
}

// ─── Carga de voces ───────────────────────────────────────────────────────────

/**
 * Espera a que speechSynthesis tenga voces disponibles.
 * Chrome las carga de forma asíncrona via el evento `voiceschanged`.
 */
function loadVoices(): Promise<SpeechSynthesisVoice[]> {
  return new Promise((resolve) => {
    const voices = window.speechSynthesis.getVoices()
    if (voices.length > 0) {
      resolve(voices)
      return
    }
    window.speechSynthesis.addEventListener(
      'voiceschanged',
      () => resolve(window.speechSynthesis.getVoices()),
      { once: true },
    )
    // Timeout de seguridad por si el evento nunca llega
    setTimeout(() => resolve(window.speechSynthesis.getVoices()), 1500)
  })
}

// ─── Selector de voz premium ──────────────────────────────────────────────────

/**
 * Selecciona la mejor voz disponible para el perfil dado.
 *
 * Orden de prioridad:
 *   1. Coincidencia exacta de nombre (preferredVoices)
 *   2. Tier-1 premium: nombre contiene "Google Español", "Natural", "Sabina" o "Monica"
 *   3. Coincidencia parcial de nombre (preferredVoices)
 *   4. Locale preferido (es-ES, es-AR…)
 *   5. Primera voz del sistema como último recurso
 */
function pickVoice(
  voices: SpeechSynthesisVoice[],
  profile: VoiceProfile,
): SpeechSynthesisVoice | null {
  if (voices.length === 0) return null

  const lc = (s: string) => s.toLowerCase()

  // 1. Coincidencia exacta de nombre
  for (const name of profile.preferredVoices) {
    const match = voices.find((v) => lc(v.name) === lc(name))
    if (match) return match
  }

  // 2. Keyword preferida (Google español estándar, Paulina, Monica — sin Neurales)
  for (const keyword of PREFERRED_KEYWORDS) {
    const match = voices.find((v) => lc(v.name).includes(keyword))
    if (match) return match
  }

  // 3. Coincidencia parcial de nombre preferido
  for (const name of profile.preferredVoices) {
    const match = voices.find((v) => lc(v.name).includes(lc(name)))
    if (match) return match
  }

  // 4. Locale preferido
  for (const locale of profile.localeFallback) {
    const match = voices.find((v) => v.lang.startsWith(locale))
    if (match) return match
  }

  // 5. Cualquier voz disponible
  return voices[0] ?? null
}

// ─── Pre-procesado del texto ──────────────────────────────────────────────────

/**
 * Elimina markdown y símbolos técnicos antes de la síntesis de voz.
 * Reemplaza bloques de código por un aviso hablable y limpia el resto.
 */
function sanitizeForSpeech(text: string): string {
  return text
    .replace(/```[\s\S]*?```/g, ' código de ejemplo. ')
    .replace(/`([^`]+)`/g, '$1')
    .replace(/[*_~#[\]()>|]/g, '')
    .replace(/\s{2,}/g, ' ')
    .trim()
}

/**
 * Construye el texto final que se enviará al sintetizador.
 *
 * Con prefijo (niveles 2 y 3):
 *   "Operador, un pequeño ajuste táctico para ti. [texto real]"
 *   La coma tras "Operador" crea una pausa natural en cualquier motor TTS.
 *   Suena cálido y personal en vez del "Atención, operador." anterior.
 *
 * Sin prefijo (nivel 1):
 *   "[texto real]"
 */
function buildUtteranceText(clean: string, profile: VoiceProfile): string {
  if (!profile.withPrefix) return clean
  return `Operador, un pequeño ajuste táctico para ti. ${clean}`
}

// ─── API pública ──────────────────────────────────────────────────────────────

/**
 * Detiene inmediatamente el SFX en curso y cualquier síntesis de voz activa.
 * Seguro de llamar aunque no haya nada reproduciéndose.
 */
export function cancelDakiVoice(): void {
  if (typeof window === 'undefined') return

  // Cancela el SFX si estaba sonando
  if (_currentSfx) {
    _currentSfx.pause()
    _currentSfx.currentTime = 0
    _currentSfx = null
  }

  window.speechSynthesis.cancel()
}

/** Retorna true si DAKI está hablando actualmente (no incluye el SFX previo). */
export function isDakiSpeaking(): boolean {
  if (typeof window === 'undefined') return false
  return window.speechSynthesis.speaking
}

/**
 * Secuencia completa DAKI Audio Engine V3:
 *
 *   [SFX daki_alert.mp3]  →  onended  →  [TTS: "Operador... {text}"]
 *
 * El SFX y el TTS se ejecutan siempre en serie, nunca en paralelo.
 * Si el nivel no tiene `withAlert`, salta directamente al TTS.
 *
 * @param text        Texto a hablar (se sanitiza automáticamente).
 * @param dakiLevel   Nivel evolutivo de DAKI: 1 Robótico | 2 Amistoso | 3 Compañero.
 * @param onEnd       Callback opcional invocado cuando el TTS termina.
 * @param skipPrefix  Si true, omite el prefijo conversacional (útil para narrativa cinemática).
 */
export async function speakDaki(
  text: string,
  dakiLevel: DakiLevel = 1,
  onEnd?: () => void,
  skipPrefix = false,
): Promise<void> {
  if (typeof window === 'undefined') return
  if (!('speechSynthesis' in window)) return

  // Cancela cualquier secuencia previa (SFX + TTS)
  cancelDakiVoice()

  const clean = sanitizeForSpeech(text)
  if (!clean) return

  const profile = VOICE_PROFILES[dakiLevel]

  // ── Paso 1: SFX (solo si el perfil lo requiere) ───────────────────────────
  if (profile.withAlert) {
    await playAlertSfx()
  }

  // ── Paso 2: Resolución de voces ───────────────────────────────────────────
  const voices = await loadVoices()
  const voice  = pickVoice(voices, profile)

  // ── Paso 3: Construcción del utterance ────────────────────────────────────
  const utteranceText = skipPrefix ? clean : buildUtteranceText(clean, profile)
  const utterance     = new SpeechSynthesisUtterance(utteranceText)

  utterance.pitch  = profile.pitch
  utterance.rate   = profile.rate
  utterance.volume = profile.volume
  if (voice) utterance.voice = voice
  if (onEnd) utterance.onend = onEnd

  // ── Paso 4: Reproducción ──────────────────────────────────────────────────
  // Workaround Chrome: a veces speechSynthesis queda pausado entre llamadas
  if (window.speechSynthesis.paused) {
    window.speechSynthesis.resume()
  }

  window.speechSynthesis.speak(utterance)
}
