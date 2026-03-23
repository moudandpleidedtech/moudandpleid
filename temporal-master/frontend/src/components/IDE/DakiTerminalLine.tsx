'use client'

/**
 * DakiTerminalLine — Renderiza una línea de consola con tooltips interactivos.
 *
 * Detecta términos Python entre backticks (`` `for` ``, `` `range()` ``, etc.)
 * y los convierte en spans clickables. Al hacer clic, muestra un tooltip
 * cyberpunk con la definición táctica desde la Base de Conocimiento de DAKI.
 *
 * Solo activa el parser en líneas de tipo 'enigma' e 'intervention' (mensajes
 * de DAKI), no en stdout/stderr para evitar falsos positivos.
 */

import { useState, useEffect, useRef, useCallback } from 'react'
import { createPortal } from 'react-dom'
import { TACTICAL_KNOWLEDGE, TERM_TO_CONCEPT, type TacticalConcept } from '@/lib/tacticalKnowledge'

// ─── Tipos ─────────────────────────────────────────────────────────────────

interface Segment {
  text: string
  conceptId?: string
}

interface TooltipPos {
  x: number
  y: number
  concept: TacticalConcept
}

// ─── Parser ────────────────────────────────────────────────────────────────

/**
 * Divide el texto en segmentos. Los términos entre backticks que existan
 * en el knowledge base reciben un conceptId — se renderizan como clickables.
 */
function parseTerminalText(text: string): Segment[] {
  const segments: Segment[] = []
  const regex = /`([^`]+)`/g
  let last = 0
  let match: RegExpExecArray | null

  while ((match = regex.exec(text)) !== null) {
    // Texto literal antes del backtick
    if (match.index > last) {
      segments.push({ text: text.slice(last, match.index) })
    }

    const inner = match[1]
    const termKey = inner.toLowerCase().replace(/\(\)/g, '').trim()
    const conceptId = TERM_TO_CONCEPT[termKey]

    if (conceptId && TACTICAL_KNOWLEDGE[conceptId]) {
      segments.push({ text: `\`${inner}\``, conceptId })
    } else {
      segments.push({ text: `\`${inner}\`` })
    }

    last = regex.lastIndex
  }

  if (last < text.length) {
    segments.push({ text: text.slice(last) })
  }

  return segments.length > 0 ? segments : [{ text }]
}

// ─── Tooltip ───────────────────────────────────────────────────────────────

function ConceptTooltip({ pos, onClose }: { pos: TooltipPos; onClose: () => void }) {
  const ref = useRef<HTMLDivElement>(null)
  const { concept, x, y } = pos

  // Ajustar posición para no salir de la pantalla
  const [adjustedPos, setAdjustedPos] = useState({ x, y })

  useEffect(() => {
    if (!ref.current) return
    const rect = ref.current.getBoundingClientRect()
    const vw = window.innerWidth
    const vh = window.innerHeight
    let nx = x + 12
    let ny = y + 12
    if (nx + rect.width > vw - 8) nx = x - rect.width - 12
    if (ny + rect.height > vh - 8) ny = y - rect.height - 12
    setAdjustedPos({ x: Math.max(8, nx), y: Math.max(8, ny) })
  }, [x, y])

  // Cierra en clic fuera
  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        onClose()
      }
    }
    document.addEventListener('mousedown', handler)
    return () => document.removeEventListener('mousedown', handler)
  }, [onClose])

  return createPortal(
    <div
      ref={ref}
      className="fixed z-[200] w-80 font-mono text-xs shadow-2xl"
      style={{
        left: adjustedPos.x,
        top: adjustedPos.y,
        background: 'rgba(5, 5, 10, 0.97)',
        border: '1px solid rgba(189, 0, 255, 0.5)',
        boxShadow: '0 0 32px rgba(189, 0, 255, 0.12), inset 0 0 12px rgba(189, 0, 255, 0.04)',
      }}
    >
      {/* Header */}
      <div className="flex items-center justify-between px-3 py-2 border-b border-[#BD00FF]/20">
        <div>
          <div className="text-[#BD00FF] text-[10px] tracking-[0.3em] uppercase leading-none mb-0.5">
            BASE DE CONOCIMIENTO TÁCTICO
          </div>
          <div className="text-[#00FF41] text-[11px] font-semibold tracking-wide">
            {concept.tactical_name}
          </div>
          <div className="text-[#00FF41]/40 text-[9px] tracking-widest">
            python: {concept.python_term}
          </div>
        </div>
        <button
          onClick={onClose}
          className="text-[#ffffff20] hover:text-[#BD00FF] text-base leading-none transition-colors ml-2"
        >×</button>
      </div>

      {/* Definition */}
      <div className="px-3 pt-2.5 pb-1.5">
        <div className="text-[#00FF41]/80 text-[10px] leading-relaxed">
          {concept.definition}
        </div>
      </div>

      {/* Syntax */}
      <div className="px-3 pb-1.5">
        <div className="text-[#BD00FF]/60 text-[9px] tracking-[0.2em] uppercase mb-1">SINTAXIS</div>
        <pre className="text-[#FBBF24] text-[10px] leading-relaxed whitespace-pre-wrap bg-black/40 px-2 py-1.5">
          {concept.syntax}
        </pre>
      </div>

      {/* Example */}
      <div className="px-3 pb-1.5">
        <div className="text-[#BD00FF]/60 text-[9px] tracking-[0.2em] uppercase mb-1">EJEMPLO</div>
        <pre className="text-[#00FF41]/90 text-[10px] leading-relaxed whitespace-pre-wrap bg-black/40 px-2 py-1.5">
          {concept.example}
        </pre>
      </div>

      {/* Tactics */}
      <div className="px-3 pb-2.5 border-t border-[#BD00FF]/10 pt-2">
        <div className="text-[#BD00FF]/60 text-[9px] tracking-[0.2em] uppercase mb-1">TÁCTICA</div>
        <div className="text-[#00FF41]/60 text-[10px] leading-relaxed">
          {concept.tactics}
        </div>
      </div>
    </div>,
    document.body,
  )
}

// ─── Componente principal ──────────────────────────────────────────────────

interface DakiTerminalLineProps {
  text: string
  /** Only 'enigma', 'intervention', and 'daki-cli' lines get the keyword parser */
  kind: 'stdout' | 'stderr' | 'info' | 'success' | 'enigma' | 'intervention' | 'daki-cli'
}

const PARSEABLE_KINDS: Set<string> = new Set(['enigma', 'intervention', 'daki-cli'])

export default function DakiTerminalLine({ text, kind }: DakiTerminalLineProps) {
  const [tooltip, setTooltip] = useState<TooltipPos | null>(null)

  const handleKeywordClick = useCallback(
    (e: React.MouseEvent, conceptId: string) => {
      e.stopPropagation()
      const concept = TACTICAL_KNOWLEDGE[conceptId]
      if (!concept) return
      if (tooltip?.concept.concept_id === conceptId) {
        setTooltip(null)
        return
      }
      setTooltip({ x: e.clientX, y: e.clientY, concept })
    },
    [tooltip],
  )

  // Only parse enigma and intervention lines — other kinds render as plain text
  if (!PARSEABLE_KINDS.has(kind)) {
    return <>{text}</>
  }

  const segments = parseTerminalText(text)
  const hasKeywords = segments.some((s) => s.conceptId)

  if (!hasKeywords) {
    return <>{text}</>
  }

  return (
    <>
      {segments.map((seg, i) =>
        seg.conceptId ? (
          <span
            key={i}
            className="cursor-pointer underline decoration-dotted decoration-[#BD00FF]/70 text-[#BD00FF] hover:text-[#BD00FF] hover:decoration-solid transition-colors"
            style={{ textShadow: '0 0 6px #BD00FF40' }}
            title={`Concepto: ${TACTICAL_KNOWLEDGE[seg.conceptId]?.tactical_name}`}
            onClick={(e) => handleKeywordClick(e, seg.conceptId!)}
          >
            {seg.text}
          </span>
        ) : (
          <span key={i}>{seg.text}</span>
        ),
      )}
      {tooltip && (
        <ConceptTooltip pos={tooltip} onClose={() => setTooltip(null)} />
      )}
    </>
  )
}
