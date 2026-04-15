'use client'

/**
 * /contratos/[id] — IDE de Contrato DAKI
 * ───────────────────────────────────────
 * Monaco editor + ejecución normal + "Enviar para Revisión DAKI"
 * Panel de revisión estructurado + Tutorial GitHub al validar.
 */

import { useEffect, useRef, useState, useCallback } from 'react'
import { useRouter } from 'next/navigation'
import dynamic from 'next/dynamic'
import { useUserStore } from '@/store/userStore'
import MobileGate from '@/components/UI/MobileGate'
import GitHubTutorial from '@/components/Contracts/GitHubTutorial'
import MisionDebriefModal from '@/components/Game/MisionDebriefModal'

// ── Real-world anchoring map ───────────────────────────────────────────────────
// Cada concepto Python mapeado a un caso de producción real.
const REAL_WORLD_MAP: Record<string, { company: string; use: string }> = {
  functions:    { company: 'Stripe',    use: 'Cada operación de cobro es una función: charge(), refund(), create_customer().' },
  def:          { company: 'Django',    use: 'Cada vista de Django es una función def que recibe request y retorna response.' },
  lists:        { company: 'Spotify',   use: 'Las listas de reproducción son listas de IDs de tracks en Python.' },
  dictionaries: { company: 'FastAPI',   use: 'Cada request JSON se convierte en un dict Python antes de procesarse.' },
  dicts:        { company: 'FastAPI',   use: 'Cada request JSON se convierte en un dict Python antes de procesarse.' },
  loops:        { company: 'Netflix',   use: 'El sistema de recomendaciones itera (for loop) sobre millones de perfiles.' },
  for:          { company: 'Netflix',   use: 'El sistema de recomendaciones itera (for loop) sobre millones de perfiles.' },
  classes:      { company: 'SQLAlchemy', use: 'Cada tabla de base de datos es una clase Python con atributos mapeados.' },
  oop:          { company: 'Anthropic', use: 'El SDK de Claude es una clase Client con métodos como messages.create().' },
  apis:         { company: 'OpenAI',    use: 'Toda la API de OpenAI se consume con requests Python contra endpoints REST.' },
  requests:     { company: 'GitHub',    use: 'La CLI de GitHub usa la librería requests para llamar a la GitHub API.' },
  exceptions:   { company: 'Airbnb',    use: 'try/except captura errores de pago fallido antes de notificar al usuario.' },
  try:          { company: 'Airbnb',    use: 'try/except captura errores de pago fallido antes de notificar al usuario.' },
  recursion:    { company: 'Google',    use: 'Los algoritmos de búsqueda en árboles (como el DOM del browser) usan recursión.' },
  generators:   { company: 'Twitter',   use: 'Los feeds infinitos de Twitter se implementan con generadores Python en el backend.' },
  decorators:   { company: 'FastAPI',   use: '@router.get() es un decorador Python que registra endpoints automáticamente.' },
  comprehension:{ company: 'Pandas',    use: 'List comprehensions procesan millones de filas de datos en una sola línea.' },
}

function getRealWorldContext(concepts: string[]): { company: string; use: string } | null {
  for (const c of concepts) {
    const key = c.toLowerCase().replace(/[^a-z]/g, '')
    const entry = REAL_WORLD_MAP[key]
    if (entry) return entry
    // partial match
    for (const mapKey of Object.keys(REAL_WORLD_MAP)) {
      if (key.includes(mapKey) || mapKey.includes(key)) return REAL_WORLD_MAP[mapKey]
    }
  }
  return null
}

const MonacoEditor = dynamic(() => import('@monaco-editor/react'), { ssr: false })
const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? ''

interface Contract {
  id: string
  level_order: number
  title: string
  description: string
  lore_briefing: string | null
  pedagogical_objective: string | null
  initial_code: string
  expected_output: string
  test_inputs: string[]
  concepts_taught: string[]
  base_xp_reward: number
}

interface CriterionResult {
  criterio: string
  estado: string
  detalle: string
}

interface ReviewResult {
  veredicto: string
  puntuacion: number
  fortalezas: string[]
  observaciones: CriterionResult[]
  sugerencias: string[]
  listo_para_github: boolean
  contract_title: string
}

interface ConsoleLine {
  text: string
  kind: 'stdout' | 'stderr' | 'info' | 'success' | 'review'
}

type Props = { params: { id: string } }

export default function ContractIDEPage({ params }: Props) {
  const router = useRouter()
  const { _hasHydrated, userId, level } = useUserStore()
  const consoleRef = useRef<HTMLDivElement>(null)

  const [contract, setContract] = useState<Contract | null>(null)
  const [code, setCode] = useState('')
  const [output, setOutput] = useState<ConsoleLine[]>([
    { text: '> Consola lista. Ejecuta o envía para revisión DAKI_', kind: 'info' },
  ])
  const [running, setRunning] = useState(false)
  const [reviewing, setReviewing] = useState(false)
  const [review, setReview] = useState<ReviewResult | null>(null)
  const [showGitHub, setShowGitHub] = useState(false)
  const [viewMode, setViewMode] = useState<'briefing' | 'editor'>('briefing')
  const [showDebrief, setShowDebrief] = useState(false)
  const attemptCountRef = useRef(0)

  const scrollConsole = useCallback(() => {
    setTimeout(() => {
      consoleRef.current?.scrollTo({ top: consoleRef.current.scrollHeight, behavior: 'smooth' })
    }, 50)
  }, [])

  useEffect(() => {
    if (!_hasHydrated) return
    if (!userId) { router.replace('/login'); return }
    fetch(`${API_BASE}/api/v1/challenges/${params.id}?user_id=${userId}`)
      .then(r => r.json())
      .then((data: Contract) => {
        setContract(data)
        setCode(data.initial_code || '')
      })
      .catch(() => router.push('/contratos'))
  }, [_hasHydrated, params.id, userId, router])

  // ── Ejecutar código (evaluación normal) ───────────────────────────────────
  const ejecutar = async () => {
    if (running || !contract) return
    attemptCountRef.current += 1
    setRunning(true)
    setOutput([{ text: '> Ejecutando secuencia...', kind: 'info' }])

    try {
      const res = await fetch(`${API_BASE}/api/v1/evaluate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          challenge_id: params.id,
          code,
          user_id: userId,
          daki_level: 1,
        }),
      })
      const data = await res.json()
      const lines: ConsoleLine[] = []

      if (data.stdout) {
        data.stdout.split('\n').forEach((l: string) =>
          lines.push({ text: l, kind: 'stdout' })
        )
      }
      if (data.stderr) {
        data.stderr.split('\n').forEach((l: string) =>
          lines.push({ text: l, kind: 'stderr' })
        )
      }
      if (data.status === 'success') {
        lines.push({ text: '', kind: 'info' })
        lines.push({ text: '[OK] Secuencia ejecutada sin errores.', kind: 'success' })
        lines.push({ text: '> Usa [[ ENVIAR PARA REVISIÓN DAKI ]] cuando estés listo.', kind: 'info' })
      } else {
        lines.push({ text: '', kind: 'info' })
        lines.push({ text: `[ERROR] ${data.status?.toUpperCase() ?? 'FALLO'}`, kind: 'stderr' })
      }

      setOutput(lines)
    } catch {
      setOutput([{ text: '[ERROR] No se pudo conectar con el servidor.', kind: 'stderr' }])
    } finally {
      setRunning(false)
      scrollConsole()
    }
  }

  // ── Enviar para revisión DAKI ─────────────────────────────────────────────
  const enviarRevision = async () => {
    if (reviewing || !contract || !userId) return
    setReviewing(true)
    setReview(null)
    setOutput([
      { text: '> Transmitiendo contrato al Nexo...', kind: 'info' },
      { text: '> DAKI iniciando análisis de criterios...', kind: 'info' },
    ])

    try {
      const res = await fetch(`${API_BASE}/api/v1/contracts/review`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId,
          challenge_id: params.id,
          code,
          operator_level: level ?? 1,
        }),
      })
      const data: ReviewResult = await res.json()
      setReview(data)

      const lines: ConsoleLine[] = [
        { text: '', kind: 'info' },
        { text: `[DAKI REVISOR] Análisis completado — ${data.contract_title}`, kind: 'review' },
        { text: `[VEREDICTO] ${data.veredicto} — Puntuación: ${data.puntuacion}/100`, kind: data.veredicto === 'CONTRATO_VALIDADO' ? 'success' : 'stderr' },
      ]
      setOutput(lines)
      scrollConsole()

      // Debrief metacognitivo si el contrato fue validado
      if (data.veredicto === 'CONTRATO_VALIDADO') {
        setTimeout(() => setShowDebrief(true), 1200)
      }
    } catch {
      setOutput([{ text: '[ERROR] Revisión no disponible. Intenta de nuevo.', kind: 'stderr' }])
    } finally {
      setReviewing(false)
    }
  }

  const levelOrder = contract?.level_order ?? 50
  const CONTRACT_ACCENT: Record<number, string> = {
    50:  '#00FF41',  // Sector 05 — verde operacional
    60:  '#FFB800',  // Sector 06 — ámbar
    70:  '#00BFFF',  // Sector 07 — cian
    130: '#FF6B00',  // Sector 13 — naranja
    175: '#CC00FF',  // Sector 17 — púrpura
  }
  const accentColor = CONTRACT_ACCENT[levelOrder] ?? '#FF4444'

  if (!contract) {
    return (
      <div className="h-screen bg-[#0A0A0A] font-mono text-[#00FF41] flex items-center justify-center">
        <span className="text-xs tracking-widest animate-pulse text-[#00FF41]/30">CARGANDO CONTRATO...</span>
      </div>
    )
  }

  return (
    <MobileGate>
    <div className="h-screen bg-[#0A0A0A] font-mono text-[#00FF41] flex flex-col overflow-hidden">

      {/* Debrief post-contrato */}
      <MisionDebriefModal
        visible={showDebrief}
        userId={userId ?? ''}
        challengeId={params.id}
        attemptCount={attemptCountRef.current}
        onClose={() => setShowDebrief(false)}
      />

      {/* CRT overlay */}
      <div className="fixed inset-0 pointer-events-none z-10"
        style={{ backgroundImage: 'repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,0.07) 2px,rgba(0,0,0,0.07) 4px)' }}
      />

      {/* Header */}
      <header className="relative z-20 shrink-0 flex items-center justify-between px-6 py-3 border-b bg-black/60"
        style={{ borderColor: `${accentColor}20` }}>
        <div className="flex items-center gap-3">
          <span className="w-1.5 h-1.5 rounded-full animate-pulse" style={{ background: accentColor }} />
          <span className="text-xs font-bold tracking-[0.3em] uppercase" style={{ color: accentColor }}>
            CONTRATO-{levelOrder} // {contract.title.replace(`CONTRATO-${levelOrder}: `, '')}
          </span>
        </div>
        <div className="flex items-center gap-3">
          <button onClick={() => router.push('/contratos')}
            className="text-[10px] tracking-[0.35em] uppercase border border-[#00FF41]/25 text-[#00FF41]/50 px-3 py-1.5 hover:border-[#00FF41]/50 hover:text-[#00FF41]/80 transition-all duration-150">
            {'[ SALA DE CONTRATOS ]'}
          </button>
        </div>
      </header>

      {/* Split layout */}
      <main className="relative z-20 flex-1 flex overflow-hidden">

        {/* Panel izquierdo — Briefing / Revisión */}
        <div className="w-[32%] shrink-0 flex flex-col border-r overflow-hidden"
          style={{ borderColor: `${accentColor}20` }}>

          {/* Tabs */}
          <div className="shrink-0 flex border-b" style={{ borderColor: `${accentColor}15` }}>
            {(['briefing', 'editor'] as const).map(mode => (
              <button key={mode} onClick={() => setViewMode(mode)}
                className="flex-1 py-2 text-[9px] tracking-[0.4em] uppercase transition-colors"
                style={{
                  color: viewMode === mode ? accentColor : `${accentColor}30`,
                  borderBottom: viewMode === mode ? `1px solid ${accentColor}` : '1px solid transparent',
                }}>
                {mode === 'briefing' ? 'MISIÓN' : 'REVISIÓN'}
              </button>
            ))}
          </div>

          {/* Contenido del panel */}
          <div className="flex-1 overflow-y-auto px-5 py-5 text-[10px] leading-6">
            {viewMode === 'briefing' ? (
              <>
                {/* Badge */}
                <div className="flex items-center gap-2 mb-4">
                  <span style={{ color: accentColor }}>{'▶'}</span>
                  <span className="text-[8px] tracking-[0.5em] uppercase"
                    style={{ color: `${accentColor}50` }}>CONTRATO DE CERTIFICACIÓN</span>
                </div>

                {/* Objetivo */}
                <h1 className="text-[11px] font-bold tracking-[0.2em] uppercase text-white mb-3 leading-5">
                  {contract.title.replace(`CONTRATO-${levelOrder}: `, '')}
                </h1>
                <div className="h-px mb-4" style={{ background: `${accentColor}20` }} />

                {/* Narrativa */}
                <p className="text-[#C0C0C0]/60 leading-5 mb-4">{contract.lore_briefing}</p>

                {/* Objetivo pedagógico */}
                <div className="border px-3 py-3 mb-4" style={{ borderColor: `${accentColor}20` }}>
                  <p className="text-[9px] tracking-[0.3em] uppercase mb-1.5"
                    style={{ color: `${accentColor}50` }}>OBJETIVO TÉCNICO</p>
                  <p className="text-[#C0C0C0]/55">{contract.pedagogical_objective}</p>
                </div>

                {/* Conceptos */}
                <div className="mb-4">
                  <p className="text-[9px] tracking-[0.3em] uppercase mb-2"
                    style={{ color: `${accentColor}40` }}>CONCEPTOS EVALUADOS</p>
                  <div className="flex flex-wrap gap-1.5">
                    {contract.concepts_taught.map(c => (
                      <span key={c} className="text-[9px] border px-2 py-0.5"
                        style={{ borderColor: `${accentColor}25`, color: `${accentColor}60` }}>
                        {c}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Recompensa */}
                <div className="border px-3 py-2 mb-4" style={{ borderColor: `${accentColor}15` }}>
                  <p className="text-[9px]" style={{ color: `${accentColor}40` }}>
                    <span className="font-bold">XP REWARD:</span>{' '}
                    <span style={{ color: accentColor }}>{contract.base_xp_reward.toLocaleString()} XP</span>
                    {' '}<span className="text-[#00FF41]/20">+</span>{' '}
                    <span style={{ color: accentColor }}>Tutorial GitHub desbloqueado</span>
                  </p>
                </div>

                {/* Contexto Real — Aplicación en producción */}
                {(() => {
                  const ctx = getRealWorldContext(contract.concepts_taught)
                  if (!ctx) return null
                  return (
                    <div className="border px-3 py-3" style={{ borderColor: `${accentColor}10`, background: `${accentColor}03` }}>
                      <p className="text-[8px] tracking-[0.4em] uppercase mb-2" style={{ color: `${accentColor}35` }}>
                        APLICACIÓN REAL — {ctx.company.toUpperCase()}
                      </p>
                      <p className="text-[9px] leading-5 tracking-wide" style={{ color: `${accentColor}50` }}>
                        {ctx.use}
                      </p>
                    </div>
                  )
                })()}
              </>
            ) : (
              /* Panel de Revisión */
              review ? (
                <>
                  {/* Veredicto */}
                  <div className={`border px-4 py-3 mb-5 ${review.veredicto === 'CONTRATO_VALIDADO' ? 'border-[#00FF41]/40 bg-[#00FF41]/5' : 'border-[#FF4444]/40 bg-[#FF4444]/5'}`}>
                    <div className="text-[10px] font-bold tracking-[0.2em] mb-1"
                      style={{ color: review.veredicto === 'CONTRATO_VALIDADO' ? '#00FF41' : '#FF4444' }}>
                      {review.veredicto === 'CONTRATO_VALIDADO' ? '✓ CONTRATO VALIDADO' : '⚠ REQUIERE AJUSTE'}
                    </div>
                    <div className="text-[9px] tracking-widest"
                      style={{ color: review.veredicto === 'CONTRATO_VALIDADO' ? '#00FF41' : '#FF4444' }}>
                      Puntuación: {review.puntuacion}/100
                    </div>
                  </div>

                  {/* Fortalezas */}
                  {review.fortalezas.length > 0 && (
                    <div className="mb-4">
                      <p className="text-[9px] tracking-[0.3em] text-[#00FF41]/40 uppercase mb-2">FORTALEZAS</p>
                      {review.fortalezas.map((f, i) => (
                        <div key={i} className="flex items-start gap-2 mb-1.5">
                          <span className="text-[#00FF41] shrink-0 mt-0.5">✓</span>
                          <p className="text-[10px] text-[#C0C0C0]/60">{f}</p>
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Criterios */}
                  <div className="mb-4">
                    <p className="text-[9px] tracking-[0.3em] text-[#00FF41]/40 uppercase mb-2">EVALUACIÓN POR CRITERIO</p>
                    {review.observaciones.map((obs, i) => (
                      <div key={i} className="border border-[#00FF41]/10 px-3 py-2 mb-2">
                        <div className="flex items-center justify-between mb-1">
                          <span className="text-[9px] font-bold text-[#00FF41]/60 tracking-widest">{obs.criterio}</span>
                          <span className={`text-[9px] font-bold tracking-widest ${obs.estado === 'OK' ? 'text-[#00FF41]' : obs.estado === 'MEJORA' ? 'text-[#FFB800]' : 'text-[#FF4444]'}`}>
                            {obs.estado}
                          </span>
                        </div>
                        <p className="text-[9px] text-[#C0C0C0]/50 leading-5">{obs.detalle}</p>
                      </div>
                    ))}
                  </div>

                  {/* Sugerencias */}
                  {review.sugerencias.length > 0 && (
                    <div className="mb-4">
                      <p className="text-[9px] tracking-[0.3em] text-[#FFB800]/40 uppercase mb-2">SUGERENCIAS</p>
                      {review.sugerencias.map((s, i) => (
                        <div key={i} className="flex items-start gap-2 mb-1.5">
                          <span className="text-[#FFB800]/60 shrink-0 mt-0.5">→</span>
                          <p className="text-[10px] text-[#C0C0C0]/55">{s}</p>
                        </div>
                      ))}
                    </div>
                  )}

                  {/* GitHub CTA */}
                  {review.listo_para_github && (
                    <button
                      onClick={() => setShowGitHub(true)}
                      className="w-full border border-[#00FF41]/50 bg-[#00FF41]/5 py-3 text-[10px] tracking-[0.3em] font-bold uppercase text-[#00FF41] hover:bg-[#00FF41]/12 hover:border-[#00FF41] transition-all duration-150 mt-3"
                    >
                      [[ TUTORIAL GITHUB → PUBLICAR ]]
                    </button>
                  )}
                </>
              ) : (
                <div className="flex flex-col items-center justify-center h-full text-center py-10">
                  <p className="text-[#00FF41]/20 text-[10px] tracking-widest leading-6">
                    Escribe tu solución en el editor.<br />
                    Cuando estés listo, envía para revisión DAKI.<br />
                    El análisis aparecerá aquí.
                  </p>
                </div>
              )
            )}
          </div>
        </div>

        {/* Panel derecho — Editor + Consola */}
        <div className="flex-1 flex flex-col overflow-hidden">

          {/* Monaco */}
          <div className="flex-1 min-h-0">
            <MonacoEditor
              height="100%"
              language="python"
              theme="vs-dark"
              value={code}
              onChange={v => setCode(v ?? '')}
              options={{
                fontSize: 13,
                fontFamily: "'Fira Code', 'Cascadia Code', Consolas, monospace",
                minimap: { enabled: false },
                scrollBeyondLastLine: false,
                lineNumbers: 'on',
                renderLineHighlight: 'line',
                tabSize: 4,
                wordWrap: 'on',
                padding: { top: 12 },
              }}
            />
          </div>

          {/* Controles */}
          <div className="shrink-0 flex items-center gap-3 px-4 py-2.5 border-t border-b border-[#00FF41]/10 bg-black/40">
            <button onClick={ejecutar} disabled={running || reviewing}
              className="text-[10px] tracking-[0.35em] uppercase border border-[#00FF41]/55 text-[#00FF41] px-4 py-2 bg-[#00FF41]/5 hover:bg-[#00FF41]/12 hover:border-[#00FF41] disabled:opacity-30 disabled:cursor-not-allowed transition-all duration-150">
              {running ? '[ EJECUTANDO... ]' : '[ EJECUTAR ]'}
            </button>
            <button
              onClick={() => { enviarRevision(); setViewMode('editor') }}
              disabled={running || reviewing}
              className="text-[10px] tracking-[0.35em] uppercase border px-5 py-2 font-bold disabled:opacity-30 disabled:cursor-not-allowed transition-all duration-150"
              style={{
                borderColor: `${accentColor}60`,
                color: accentColor,
                background: `${accentColor}08`,
              }}
            >
              {reviewing ? '[ DAKI ANALIZANDO... ]' : '[[ ENVIAR PARA REVISIÓN DAKI ]]'}
            </button>
            <span className="ml-auto text-[8px] tracking-[0.4em] text-[#00FF41]/20 uppercase">
              Python 3.12 · CONTRATO-{levelOrder}
            </span>
          </div>

          {/* Consola */}
          <div ref={consoleRef}
            className="shrink-0 h-[22%] bg-black border-t border-[#00FF41]/8 px-4 py-3 overflow-y-auto">
            <div className="text-[8px] tracking-[0.5em] text-[#00FF41]/20 uppercase mb-3">
              {'// TERMINAL DE SALIDA'}
            </div>
            {output.map((line, i) => (
              <div key={i} className={`text-[11px] leading-5 font-mono ${
                line.kind === 'stderr' ? 'text-[#FF4444]/80'
                : line.kind === 'success' ? 'text-[#00FF41]'
                : line.kind === 'review' ? 'text-[#FFB800]/80'
                : line.text === '' ? 'h-2'
                : 'text-[#00FF41]/35'
              }`}>
                {line.text || '\u00A0'}
              </div>
            ))}
            {(running || reviewing) && (
              <span className="text-[#00FF41]/40 text-[11px] animate-pulse">_</span>
            )}
          </div>
        </div>
      </main>

      {/* Tutorial GitHub Modal */}
      {showGitHub && contract && (
        <GitHubTutorial
          contractTitle={contract.title.replace(`CONTRATO-${levelOrder}: `, '')}
          code={code}
          onClose={() => setShowGitHub(false)}
        />
      )}
    </div>
    </MobileGate>
  )
}
