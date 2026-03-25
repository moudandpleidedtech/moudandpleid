'use client'

/**
 * ArchivoFallasModal — Archivo de Fallas del Operador
 * Muestra los errores más frecuentes con análisis táctico.
 * Llama a GET /api/v1/intel/error-vault
 */

import { useEffect, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000'

interface ErrorEntry {
  type: string
  count: number
}

interface VaultData {
  top_errors: ErrorEntry[]
  total_errors_logged: number
  total_attempts: number
  total_hints: number
  missions_with_data: number
  missions_failed: number
}

interface Props {
  userId: string
  onClose: () => void
}

// Traducción táctica de tipos de error
const ERROR_INTEL: Record<string, { label: string; diagnosis: string; color: string }> = {
  SyntaxError: {
    label: 'ANOMALÍA SINTÁCTICA',
    diagnosis: 'Estructura rota — sangría, paréntesis o dos puntos fuera de protocolo.',
    color: '#FF4444',
  },
  NameError: {
    label: 'REGISTRO NO DECLARADO',
    diagnosis: 'Variable utilizada antes de ser definida o con nombre incorrecto.',
    color: '#FFB800',
  },
  TypeError: {
    label: 'CONFLICTO DE TIPOS',
    diagnosis: 'Operación entre tipos incompatibles — común al mezclar str con int.',
    color: '#FF6B6B',
  },
  IndentationError: {
    label: 'FALLA DE PROTOCOLO',
    diagnosis: 'Indentación inconsistente — el canal de control se corrompió.',
    color: '#FF4444',
  },
  ValueError: {
    label: 'SEÑAL INVÁLIDA',
    diagnosis: 'Valor con formato incorrecto — conversión de tipo fallida.',
    color: '#FFB800',
  },
  AttributeError: {
    label: 'ATRIBUTO INEXISTENTE',
    diagnosis: 'Método o atributo no existe en el objeto — revisa la clase.',
    color: '#00B4D8',
  },
  IndexError: {
    label: 'DESBORDAMIENTO DE ÍNDICE',
    diagnosis: 'Acceso fuera de los límites de la lista — verifica el rango.',
    color: '#7B2FBE',
  },
  KeyError: {
    label: 'CLAVE NO ENCONTRADA',
    diagnosis: 'La clave no existe en el diccionario — usa .get() o verifica.',
    color: '#7B2FBE',
  },
}

function getErrorIntel(errorType: string) {
  return ERROR_INTEL[errorType] ?? {
    label: errorType.toUpperCase().replace('ERROR', ' ERROR'),
    diagnosis: 'Error detectado en el canal de ejecución — analiza el stacktrace.',
    color: '#00FF41',
  }
}

export default function ArchivoFallasModal({ userId, onClose }: Props) {
  const [data, setData]       = useState<VaultData | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!userId) return
    fetch(`${API_BASE}/api/v1/intel/error-vault?user_id=${userId}`)
      .then(r => r.ok ? r.json() : null)
      .then((d: VaultData | null) => { if (d) setData(d) })
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [userId])

  const maxCount = data?.top_errors[0]?.count ?? 1

  return (
    <AnimatePresence>
      <>
        <motion.div
          className="fixed inset-0 z-[90] bg-black/80"
          initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
          onClick={onClose}
        />
        <motion.div
          className="fixed inset-0 z-[91] flex items-center justify-center p-4"
          initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
        >
          <motion.div
            className="relative w-full max-w-md bg-[#060606] border border-[#FF4444]/20 font-mono overflow-hidden"
            style={{ boxShadow: '0 0 60px rgba(255,68,68,0.08)' }}
            initial={{ scale: 0.90, y: 20 }} animate={{ scale: 1, y: 0 }}
            exit={{ scale: 0.92, opacity: 0 }}
            transition={{ type: 'spring', stiffness: 320, damping: 28 }}
          >
            {/* Scanlines */}
            <div className="absolute inset-0 pointer-events-none opacity-[0.02]"
              style={{ backgroundImage: 'repeating-linear-gradient(0deg,transparent,transparent 3px,#FF4444 3px,#FF4444 4px)' }}
            />

            {/* Header */}
            <div className="flex items-center justify-between px-5 py-4 border-b border-[#FF4444]/10">
              <div>
                <p className="text-[9px] tracking-[0.5em] text-[#FF4444]/40 uppercase mb-0.5">
                  {'// DOSSIER DE FALLAS — CLASIFICADO'}
                </p>
                <h2 className="text-sm font-black tracking-[0.2em] text-[#FF4444]/80">
                  ARCHIVO DE FALLAS
                </h2>
              </div>
              <button
                onClick={onClose}
                className="text-[#FF4444]/25 hover:text-[#FF4444]/60 text-xs tracking-widest transition-colors"
              >
                [ ESC ]
              </button>
            </div>

            {/* Body */}
            <div className="px-5 py-5">
              {loading ? (
                <div className="text-center py-10">
                  <p className="text-[10px] tracking-[0.4em] text-[#FF4444]/30 animate-pulse">
                    ANALIZANDO PATRONES DE FALLA...
                  </p>
                </div>
              ) : !data || data.total_errors_logged === 0 ? (
                <div className="text-center py-10">
                  <p className="text-[10px] tracking-[0.35em] text-[#00FF41]/30">
                    SIN FALLAS REGISTRADAS
                  </p>
                  <p className="text-[9px] text-[#00FF41]/15 mt-2 tracking-wider">
                    Completa misiones para activar el análisis.
                  </p>
                </div>
              ) : (
                <>
                  {/* Top errors */}
                  <div className="space-y-3 mb-5">
                    {data.top_errors.map((err, i) => {
                      const intel = getErrorIntel(err.type)
                      const barPct = Math.round((err.count / maxCount) * 100)
                      return (
                        <div key={err.type} className="border border-white/[0.05] p-3">
                          <div className="flex items-center justify-between mb-1.5">
                            <span
                              className="text-[9px] font-black tracking-[0.3em] uppercase"
                              style={{ color: intel.color }}
                            >
                              {intel.label}
                            </span>
                            <span
                              className="text-[8px] tracking-widest font-bold"
                              style={{ color: `${intel.color}80` }}
                            >
                              ×{err.count}
                            </span>
                          </div>
                          {/* Barra de frecuencia */}
                          <div className="h-1 bg-white/[0.05] mb-2 overflow-hidden">
                            <motion.div
                              className="h-full"
                              style={{ background: intel.color, opacity: 0.6 }}
                              initial={{ width: 0 }}
                              animate={{ width: `${barPct}%` }}
                              transition={{ duration: 0.6, delay: i * 0.08 }}
                            />
                          </div>
                          <p className="text-[9px] text-white/25 leading-4 tracking-wide">
                            {intel.diagnosis}
                          </p>
                        </div>
                      )
                    })}
                  </div>

                  {/* Stats */}
                  <div className="border-t border-white/[0.05] pt-4 grid grid-cols-2 gap-2">
                    {[
                      { n: data.total_attempts,      label: 'INTENTOS TOTALES' },
                      { n: data.missions_failed,      label: 'MISIONES FALLIDAS' },
                      { n: data.total_hints,          label: 'PISTAS USADAS'    },
                      { n: data.missions_with_data,   label: 'MISIONES JUGADAS' },
                    ].map(({ n, label }) => (
                      <div key={label} className="border border-white/[0.04] p-2 text-center">
                        <p className="text-base font-black text-white/50">{n}</p>
                        <p className="text-[7px] tracking-[0.3em] text-white/20 mt-0.5">{label}</p>
                      </div>
                    ))}
                  </div>

                  <p className="text-[8px] text-[#00FF41]/18 tracking-wider text-center mt-4">
                    DAKI usa este dossier para calibrar las intervenciones tácticas.
                  </p>
                </>
              )}
            </div>
          </motion.div>
        </motion.div>
      </>
    </AnimatePresence>
  )
}
