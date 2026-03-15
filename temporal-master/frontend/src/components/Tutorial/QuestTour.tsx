'use client'

import dynamic from 'next/dynamic'
import { useState, useEffect } from 'react'
import { useUserStore } from '@/store/userStore'
import type { Step, CallBackProps, STATUS } from 'react-joyride'

// Importación dinámica para evitar SSR (react-joyride usa APIs del DOM)
const Joyride = dynamic(() => import('react-joyride'), { ssr: false })

const STEPS: Step[] = [
  {
    target: '#code-editor-panel',
    title: 'EDITOR DE SECUENCIAS',
    content: 'Escriba aquí la secuencia de arranque. Python es tu lenguaje de interfaz con el sistema.',
    placement: 'left',
    disableBeacon: true,
  },
  {
    target: '#execute-button',
    title: 'COMPILAR Y EJECUTAR',
    content: 'Inicie la compilación. El sistema evaluará tu código contra los tests de misión.',
    placement: 'bottom',
    disableBeacon: true,
  },
]

const JOYRIDE_STYLES = {
  options: {
    backgroundColor: '#0D0D0D',
    primaryColor: '#00FF41',
    textColor: '#00FF41',
    arrowColor: '#0D0D0D',
    overlayColor: 'rgba(0,0,0,0.72)',
    zIndex: 999,
  },
  tooltip: {
    border: '1px solid rgba(0,255,65,0.25)',
    borderRadius: 0,
    fontFamily: '"Fira Code", Consolas, monospace',
    padding: '16px 20px',
  },
  tooltipTitle: {
    color: '#00FF41',
    fontSize: '10px',
    letterSpacing: '0.25em',
    fontWeight: 900,
    marginBottom: '8px',
  },
  tooltipContent: {
    color: 'rgba(0,255,65,0.72)',
    fontSize: '12px',
    lineHeight: '1.65',
    padding: 0,
  },
  buttonNext: {
    backgroundColor: '#00FF41',
    color: '#000',
    fontFamily: '"Fira Code", Consolas, monospace',
    fontSize: '10px',
    fontWeight: 900,
    letterSpacing: '0.15em',
    borderRadius: 0,
    padding: '8px 16px',
  },
  buttonBack: {
    color: 'rgba(0,255,65,0.45)',
    fontFamily: '"Fira Code", Consolas, monospace',
    fontSize: '10px',
    letterSpacing: '0.1em',
  },
  buttonSkip: {
    color: 'rgba(0,255,65,0.25)',
    fontFamily: '"Fira Code", Consolas, monospace',
    fontSize: '10px',
    letterSpacing: '0.1em',
  },
  buttonClose: {
    color: 'rgba(0,255,65,0.4)',
    top: '10px',
    right: '10px',
  },
}

export default function QuestTour() {
  const { level } = useUserStore()
  const [run, setRun] = useState(false)

  useEffect(() => {
    // Solo para jugadores en nivel 1 que no han visto el tutorial
    if (level === 1 && typeof window !== 'undefined' && !localStorage.getItem('quest_tour_done')) {
      const t = setTimeout(() => setRun(true), 1600)
      return () => clearTimeout(t)
    }
  }, [level])

  const handleCallback = ({ status }: CallBackProps) => {
    const finished = status as typeof STATUS[keyof typeof STATUS]
    if (finished === 'finished' || finished === 'skipped') {
      localStorage.setItem('quest_tour_done', '1')
      setRun(false)
    }
  }

  return (
    <Joyride
      steps={STEPS}
      run={run}
      continuous
      showSkipButton
      showProgress
      disableScrolling
      callback={handleCallback}
      styles={JOYRIDE_STYLES}
      locale={{
        back: 'ATRAS',
        close: 'CERRAR',
        last: 'INICIAR',
        next: 'SIGUIENTE',
        skip: 'OMITIR',
        open: 'ABRIR',
      }}
    />
  )
}
