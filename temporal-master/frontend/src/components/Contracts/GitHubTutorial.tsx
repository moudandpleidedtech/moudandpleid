'use client'

/**
 * GitHubTutorial — Modal post-contrato
 * ─────────────────────────────────────
 * Tutorial de 5 pasos para publicar el proyecto en GitHub.
 * Se activa cuando DAKI valida un contrato (listo_para_github = true).
 * Incluye comandos listos para copiar con terminología DAKI.
 */

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

interface Props {
  contractTitle: string
  code: string
  onClose: () => void
}

interface Step {
  id: number
  title: string
  instruction: string
  command?: string
  note?: string
  isExternal?: boolean
  externalLabel?: string
  externalUrl?: string
}

function buildRepoName(title: string): string {
  return title.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '')
}

export default function GitHubTutorial({ contractTitle, code, onClose }: Props) {
  const [activeStep, setActiveStep] = useState(0)
  const [completedSteps, setCompletedSteps] = useState<Set<number>>(new Set())
  const [copied, setCopied] = useState<string | null>(null)

  const repoName = buildRepoName(contractTitle)
  const fileName = `${repoName}.py`

  const steps: Step[] = [
    {
      id: 0,
      title: 'Crear cuenta en GitHub',
      instruction:
        'GitHub es el sistema de control de versiones donde los operadores almacenan y comparten su código. Si ya tienes cuenta, salta al paso 2.',
      isExternal: true,
      externalLabel: '[ ABRIR GITHUB.COM ]',
      externalUrl: 'https://github.com/signup',
      note: 'Elige un nombre de usuario profesional — será tu identidad en la industria.',
    },
    {
      id: 1,
      title: 'Crear repositorio',
      instruction:
        'Un repositorio es el contenedor de tu proyecto. Crea uno nuevo con el nombre sugerido.',
      isExternal: true,
      externalLabel: '[ CREAR REPOSITORIO ]',
      externalUrl: 'https://github.com/new',
      note: `Nombre sugerido: "${repoName}" · Marca "Add a README file" · Visibilidad: Public`,
    },
    {
      id: 2,
      title: 'Guardar tu código localmente',
      instruction: `Crea un archivo llamado "${fileName}" en tu computadora y pega el código del contrato.`,
      command: `# Crea el archivo con tu código\n# Nombre: ${fileName}`,
      note: 'Abre cualquier editor de texto (VS Code recomendado), pega el código y guarda con ese nombre.',
    },
    {
      id: 3,
      title: 'Inicializar Git y subir el código',
      instruction:
        'Desde la terminal (PowerShell o CMD en Windows, Terminal en Mac/Linux), navega a la carpeta donde guardaste el archivo y ejecuta estos comandos:',
      command: `cd ruta/a/tu/carpeta\ngit init\ngit add ${fileName}\ngit commit -m "CONTRATO DAKI: ${contractTitle}"\ngit branch -M main\ngit remote add origin https://github.com/TU_USUARIO/${repoName}.git\ngit push -u origin main`,
      note: 'Reemplaza "TU_USUARIO" con tu nombre de usuario de GitHub y "ruta/a/tu/carpeta" con la ruta real.',
    },
    {
      id: 4,
      title: 'Verificar en GitHub',
      instruction:
        'Visita tu repositorio en GitHub. Deberías ver el archivo con tu código. Tu primer proyecto está publicado.',
      isExternal: true,
      externalLabel: '[ VER EN GITHUB ]',
      externalUrl: `https://github.com`,
      note: 'Comparte el link del repositorio en tu LinkedIn o CV — es evidencia real de tu skill.',
    },
  ]

  const handleCopy = (text: string, id: string) => {
    navigator.clipboard.writeText(text)
    setCopied(id)
    setTimeout(() => setCopied(null), 2000)
  }

  const markComplete = (stepId: number) => {
    setCompletedSteps(prev => new Set([...prev, stepId]))
    if (stepId < steps.length - 1) setActiveStep(stepId + 1)
  }

  const allDone = completedSteps.size === steps.length

  return (
    <div className="fixed inset-0 z-[300] flex items-center justify-center">
      {/* Backdrop */}
      <motion.div
        className="absolute inset-0 bg-black/85"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        onClick={onClose}
      />

      {/* Modal */}
      <motion.div
        className="relative z-10 w-full max-w-2xl h-[85vh] flex flex-col bg-[#050A05] border border-[#00FF41]/30 overflow-hidden font-mono"
        style={{ boxShadow: '0 0 60px rgba(0,255,65,0.1)' }}
        initial={{ scale: 0.94, y: 20 }}
        animate={{ scale: 1, y: 0 }}
        exit={{ scale: 0.94, y: 20 }}
        transition={{ type: 'spring', stiffness: 300, damping: 28 }}
      >
        {/* Header */}
        <div className="shrink-0 flex items-center justify-between px-6 py-4 border-b border-[#00FF41]/15 bg-[#030803]">
          <div>
            <div className="text-[9px] tracking-[0.5em] text-[#00FF41]/30 uppercase mb-0.5">
              PROTOCOLO DE DESPLIEGUE
            </div>
            <div className="text-sm font-bold tracking-[0.15em] text-[#00FF41]">
              TUTORIAL GITHUB — {contractTitle.toUpperCase()}
            </div>
          </div>
          <button onClick={onClose}
            className="text-[#00FF41]/35 hover:text-[#00FF41] text-xs tracking-widest transition-colors">
            [ESC] CERRAR
          </button>
        </div>

        {/* Completado */}
        <AnimatePresence>
          {allDone && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              className="shrink-0 border-b border-[#00FF41]/30 bg-[#00FF41]/5 px-6 py-3"
            >
              <p className="text-[10px] font-bold tracking-[0.3em] text-[#00FF41]">
                ✓ PROTOCOLO DE DESPLIEGUE COMPLETADO — Tu código está en el mundo.
              </p>
              <p className="text-[9px] text-[#00FF41]/50 tracking-widest mt-1">
                Comparte el link en LinkedIn: "Completé un proyecto con DAKI EdTech — Python"
              </p>
            </motion.div>
          )}
        </AnimatePresence>

        <div className="flex flex-1 overflow-hidden">

          {/* Sidebar de pasos */}
          <div className="w-[200px] shrink-0 border-r border-[#00FF41]/10 overflow-y-auto py-4">
            {steps.map((step) => {
              const done = completedSteps.has(step.id)
              const active = activeStep === step.id
              return (
                <button
                  key={step.id}
                  onClick={() => setActiveStep(step.id)}
                  className="w-full text-left px-4 py-3 flex items-start gap-3 transition-colors"
                  style={{
                    background: active ? 'rgba(0,255,65,0.05)' : 'transparent',
                    borderLeft: active ? '2px solid #00FF41' : '2px solid transparent',
                  }}
                >
                  <div className="shrink-0 w-5 h-5 border flex items-center justify-center mt-0.5"
                    style={{
                      borderColor: done ? '#00FF41' : active ? '#00FF4160' : '#00FF4125',
                      background: done ? '#00FF4120' : 'transparent',
                    }}>
                    {done ? (
                      <span className="text-[#00FF41] text-[10px]">✓</span>
                    ) : (
                      <span className="text-[9px] text-[#00FF41]/40">{step.id + 1}</span>
                    )}
                  </div>
                  <div>
                    <div className="text-[9px] tracking-widest leading-4"
                      style={{ color: done ? '#00FF41' : active ? '#00FF41' : '#00FF4140' }}>
                      {step.title}
                    </div>
                  </div>
                </button>
              )
            })}
          </div>

          {/* Contenido del paso */}
          <div className="flex-1 overflow-y-auto px-6 py-6">
            {steps.map((step) => step.id === activeStep && (
              <motion.div
                key={step.id}
                initial={{ opacity: 0, x: 10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.2 }}
              >
                {/* Número y título */}
                <div className="mb-4">
                  <span className="text-[9px] tracking-[0.5em] text-[#00FF41]/30 uppercase">
                    PASO {step.id + 1} DE {steps.length}
                  </span>
                  <h2 className="text-sm font-bold tracking-[0.15em] text-white mt-1">
                    {step.title}
                  </h2>
                </div>

                {/* Instrucción */}
                <p className="text-[11px] text-[#C0C0C0]/60 leading-6 mb-5">
                  {step.instruction}
                </p>

                {/* Comando copyable */}
                {step.command && (
                  <div className="mb-5">
                    <div className="flex items-center justify-between mb-1.5">
                      <span className="text-[9px] text-[#00FF41]/30 tracking-widest uppercase">TERMINAL</span>
                      <button
                        onClick={() => handleCopy(step.command!, `cmd-${step.id}`)}
                        className="text-[9px] tracking-widest border border-[#00FF41]/25 px-2 py-0.5 text-[#00FF41]/50 hover:text-[#00FF41] hover:border-[#00FF41]/50 transition-colors"
                      >
                        {copied === `cmd-${step.id}` ? '✓ COPIADO' : '[ COPIAR ]'}
                      </button>
                    </div>
                    <div className="bg-black border border-[#00FF41]/15 px-4 py-3">
                      <pre className="text-[10px] text-[#00FF41]/70 leading-5 whitespace-pre-wrap font-mono">
                        {step.command}
                      </pre>
                    </div>
                  </div>
                )}

                {/* Link externo */}
                {step.isExternal && step.externalUrl && (
                  <div className="mb-5">
                    <a
                      href={step.externalUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-2 border border-[#00FF41]/40 bg-[#00FF41]/5 px-4 py-2.5 text-[10px] tracking-[0.3em] text-[#00FF41] hover:bg-[#00FF41]/12 hover:border-[#00FF41]/70 transition-all duration-150"
                    >
                      {step.externalLabel} ↗
                    </a>
                  </div>
                )}

                {/* Nota */}
                {step.note && (
                  <div className="border-l-2 border-[#FFB800]/40 pl-4 mb-6">
                    <p className="text-[10px] text-[#FFB800]/60 leading-5">
                      <span className="font-bold text-[#FFB800]/80">NOTA:</span> {step.note}
                    </p>
                  </div>
                )}

                {/* Botones de navegación */}
                <div className="flex items-center gap-3 mt-2">
                  {activeStep > 0 && (
                    <button
                      onClick={() => setActiveStep(s => s - 1)}
                      className="text-[10px] tracking-[0.3em] border border-[#00FF41]/20 text-[#00FF41]/40 px-4 py-2 hover:text-[#00FF41]/60 transition-colors"
                    >
                      ← ANTERIOR
                    </button>
                  )}
                  <button
                    onClick={() => markComplete(step.id)}
                    className="text-[10px] tracking-[0.3em] font-bold border border-[#00FF41]/60 text-[#00FF41] px-5 py-2 bg-[#00FF41]/5 hover:bg-[#00FF41]/15 hover:border-[#00FF41] transition-all duration-150"
                  >
                    {completedSteps.has(step.id)
                      ? '✓ COMPLETADO'
                      : step.id === steps.length - 1
                      ? '[[ MISIÓN CUMPLIDA ]]'
                      : '[ COMPLETADO → SIGUIENTE ]'}
                  </button>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </motion.div>
    </div>
  )
}
