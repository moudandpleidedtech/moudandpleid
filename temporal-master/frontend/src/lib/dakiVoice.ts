/**
 * dakiVoice.ts — Sintetizador de voz de DAKI (Web Speech API, sin costo)
 *
 * Usa speechSynthesis nativo del navegador.
 * La voz y características cambian según el daki_level:
 *   1 — ROBÓTICO:  voz plana, tono bajo, velocidad lenta
 *   2 — AMISTOSO:  voz neutral, tono normal, velocidad conversacional
 *   3 — COMPAÑERO: voz cálida, tono elevado, velocidad fluida
 */

export type DakiLevel = 1 | 2 | 3

interface VoiceProfile {
  pitch: number   // 0–2 (1 = normal)
  rate: number    // 0.1–10 (1 = normal)
  volume: number  // 0–1
  /** Nombres de voz preferidos, en orden de prioridad. */
  preferredVoices: string[]
  /** Locales aceptables como fallback (ej. 'es', 'es-ES', 'es-MX'). */
  localeFallback: string[]
}

const VOICE_PROFILES: Record<DakiLevel, VoiceProfile> = {
  1: {
    // Robótico — voz plana, sin entonación, lenta y mecánica
    pitch: 0.55,
    rate: 0.78,
    volume: 0.92,
    preferredVoices: ['Microsoft David', 'Daniel', 'Alex', 'Fred', 'Trinoids'],
    localeFallback: ['en-US', 'en-GB', 'en'],
  },
  2: {
    // Amistoso — voz natural en español, tono neutro, conversacional
    pitch: 0.95,
    rate: 0.9,
    volume: 0.95,
    preferredVoices: [
      'Google español',
      'Google Spanish',
      'Mónica',
      'Monica',
      'Paulina',
      'Microsoft Pablo',
      'Diego',
    ],
    localeFallback: ['es-ES', 'es-MX', 'es-US', 'es-AR', 'es'],
  },
  3: {
    // Compañero — voz española más expresiva, fluida y cálida
    pitch: 1.12,
    rate: 1.0,
    volume: 1.0,
    preferredVoices: [
      'Google español',
      'Google Spanish',
      'Mónica',
      'Monica',
      'Paulina',
      'Microsoft Sabina',
    ],
    localeFallback: ['es-ES', 'es-MX', 'es-US', 'es-AR', 'es'],
  },
}

// ─── Resolución de voces ──────────────────────────────────────────────────────

/**
 * Espera a que speechSynthesis cargue las voces disponibles.
 * En Chrome, la lista es asíncrona (evento voiceschanged).
 */
function loadVoices(): Promise<SpeechSynthesisVoice[]> {
  return new Promise((resolve) => {
    const voices = window.speechSynthesis.getVoices()
    if (voices.length > 0) {
      resolve(voices)
      return
    }
    // Chrome necesita el evento voiceschanged
    window.speechSynthesis.addEventListener(
      'voiceschanged',
      () => resolve(window.speechSynthesis.getVoices()),
      { once: true },
    )
    // Timeout de seguridad: si el evento nunca llega, resuelve vacío
    setTimeout(() => resolve(window.speechSynthesis.getVoices()), 1500)
  })
}

function pickVoice(
  voices: SpeechSynthesisVoice[],
  profile: VoiceProfile,
): SpeechSynthesisVoice | null {
  if (voices.length === 0) return null

  // 1. Coincidencia exacta de nombre (case-insensitive)
  for (const name of profile.preferredVoices) {
    const match = voices.find(
      (v) => v.name.toLowerCase() === name.toLowerCase(),
    )
    if (match) return match
  }

  // 2. Nombre que contiene la preferencia (ej. "Google español" dentro de un nombre más largo)
  for (const name of profile.preferredVoices) {
    const match = voices.find((v) =>
      v.name.toLowerCase().includes(name.toLowerCase()),
    )
    if (match) return match
  }

  // 3. Locale preferido
  for (const locale of profile.localeFallback) {
    const match = voices.find((v) => v.lang.startsWith(locale))
    if (match) return match
  }

  // 4. Cualquier voz del sistema
  return voices[0] ?? null
}

// ─── Pre-procesado del texto ──────────────────────────────────────────────────

/** Elimina caracteres de markdown y símbolos técnicos antes de hablar. */
function sanitizeForSpeech(text: string): string {
  return text
    .replace(/```[\s\S]*?```/g, ' código de ejemplo. ')  // bloques de código
    .replace(/`([^`]+)`/g, '$1')                         // inline code
    .replace(/[*_~#[\]()>|]/g, '')                       // markdown symbols
    .replace(/\s{2,}/g, ' ')
    .trim()
}

// ─── API pública ──────────────────────────────────────────────────────────────

/** Cancela cualquier síntesis en curso. Seguro de llamar aunque no haya nada activo. */
export function cancelDakiVoice(): void {
  if (typeof window === 'undefined') return
  window.speechSynthesis.cancel()
}

/** Retorna true si DAKI está hablando actualmente. */
export function isDakiSpeaking(): boolean {
  if (typeof window === 'undefined') return false
  return window.speechSynthesis.speaking
}

/**
 * Reproduce el texto con la voz apropiada para el daki_level.
 *
 * @param text       Texto a hablar (se sanitiza automáticamente).
 * @param dakiLevel  Nivel evolutivo de DAKI (1, 2 o 3).
 * @param onEnd      Callback opcional cuando termina la síntesis.
 */
export async function speakDaki(
  text: string,
  dakiLevel: DakiLevel = 1,
  onEnd?: () => void,
): Promise<void> {
  if (typeof window === 'undefined') return
  if (!('speechSynthesis' in window)) return

  // Cancela síntesis previa para no encolar
  window.speechSynthesis.cancel()

  const clean = sanitizeForSpeech(text)
  if (!clean) return

  const profile = VOICE_PROFILES[dakiLevel]
  const voices  = await loadVoices()
  const voice   = pickVoice(voices, profile)

  const utterance          = new SpeechSynthesisUtterance(clean)
  utterance.pitch          = profile.pitch
  utterance.rate           = profile.rate
  utterance.volume         = profile.volume
  if (voice) utterance.voice = voice

  if (onEnd) utterance.onend = onEnd

  // Workaround: Chrome a veces no arranca si speechSynthesis está pausado
  if (window.speechSynthesis.paused) {
    window.speechSynthesis.resume()
  }

  window.speechSynthesis.speak(utterance)
}
