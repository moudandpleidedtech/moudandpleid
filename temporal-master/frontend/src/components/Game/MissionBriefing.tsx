'use client'

import { useState, useCallback, useMemo } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

// ─── Parser de Markdown ligero ────────────────────────────────────────────────
// Soporta: ## heading, **bold**, `inline code`, ```code block```, - listas, párrafos

interface ParsedBlock {
  type: 'heading' | 'paragraph' | 'code' | 'list' | 'spacer'
  content: string
  lang?: string
  items?: string[]
}

function parseMarkdown(src: string): ParsedBlock[] {
  const blocks: ParsedBlock[] = []
  const lines = src.split('\n')
  let i = 0

  while (i < lines.length) {
    const line = lines[i]

    // Código block: ```lang\n...\n```
    if (line.trimStart().startsWith('```')) {
      const lang = line.trim().slice(3).trim() || 'text'
      const codeLines: string[] = []
      i++
      while (i < lines.length && !lines[i].trimStart().startsWith('```')) {
        codeLines.push(lines[i])
        i++
      }
      blocks.push({ type: 'code', content: codeLines.join('\n'), lang })
      i++
      continue
    }

    // Encabezado ## o ###
    if (line.startsWith('## ') || line.startsWith('### ')) {
      blocks.push({ type: 'heading', content: line.replace(/^#{2,3}\s/, '') })
      i++
      continue
    }

    // Lista - item
    if (line.trimStart().startsWith('- ')) {
      const items: string[] = []
      while (i < lines.length && lines[i].trimStart().startsWith('- ')) {
        items.push(lines[i].trimStart().slice(2))
        i++
      }
      blocks.push({ type: 'list', content: '', items })
      continue
    }

    // Línea vacía → spacer
    if (line.trim() === '') {
      // solo agrega spacer si no hay ya uno al final
      if (blocks.length > 0 && blocks[blocks.length - 1].type !== 'spacer') {
        blocks.push({ type: 'spacer', content: '' })
      }
      i++
      continue
    }

    // Párrafo (puede incluir | tabla | — renderizado simplificado)
    blocks.push({ type: 'paragraph', content: line })
    i++
  }

  return blocks
}

// Renderiza texto inline: **bold** y `code`
function InlineText({ text }: { text: string }) {
  const parts = text.split(/(\*\*[^*]+\*\*|`[^`]+`)/g)
  return (
    <>
      {parts.map((part, i) => {
        if (part.startsWith('**') && part.endsWith('**')) {
          return (
            <strong key={i} className="text-[#00FF41] font-bold">
              {part.slice(2, -2)}
            </strong>
          )
        }
        if (part.startsWith('`') && part.endsWith('`')) {
          return (
            <code
              key={i}
              className="font-mono text-[#FFD700] bg-[#1A1400] px-1 py-0.5 text-[11px]"
            >
              {part.slice(1, -1)}
            </code>
          )
        }
        // Tabla row (|...|) — simplificado como texto
        if (part.includes('|') && !part.startsWith('|---')) {
          return (
            <span key={i} className="text-[#00FF41]/60">
              {part.replace(/\|/g, '  ·  ').trim()}
            </span>
          )
        }
        return <span key={i}>{part}</span>
      })}
    </>
  )
}

// Botón de copiar para bloques de código
function CopyButton({ code }: { code: string }) {
  const [copied, setCopied] = useState(false)

  const handleCopy = useCallback(() => {
    navigator.clipboard.writeText(code).then(() => {
      setCopied(true)
      setTimeout(() => setCopied(false), 1800)
    })
  }, [code])

  return (
    <button
      onClick={handleCopy}
      className="absolute top-2 right-2 text-[10px] font-mono tracking-widest px-2 py-0.5 border transition-all duration-150"
      style={
        copied
          ? { borderColor: '#00FF41', color: '#00FF41', background: '#001A00' }
          : { borderColor: '#00FF41/30', color: '#00FF41', opacity: 0.4 }
      }
    >
      {copied ? 'COPIADO ✓' : 'COPIAR'}
    </button>
  )
}

// Renderiza un bloque parseado
function Block({ block }: { block: ParsedBlock }) {
  if (block.type === 'spacer') return <div className="h-3" />

  if (block.type === 'heading') {
    return (
      <div className="mb-3">
        <h2
          className="font-mono font-black text-sm tracking-[0.2em] text-[#00FF41] uppercase"
          style={{ textShadow: '0 0 10px #00FF4160' }}
        >
          {block.content}
        </h2>
        <div className="mt-1 h-px bg-[#00FF41]/20" />
      </div>
    )
  }

  if (block.type === 'code') {
    return (
      <div className="relative my-3 bg-[#030D05] border border-[#00FF41]/20 overflow-hidden">
        {/* Barra de título del código */}
        <div className="flex items-center justify-between px-3 py-1 bg-[#050F07] border-b border-[#00FF41]/10">
          <span className="text-[10px] font-mono text-[#00FF41]/30 tracking-widest">
            {block.lang || 'python'}
          </span>
          <CopyButton code={block.content} />
        </div>
        <pre className="p-3 text-[12px] leading-5 font-mono text-[#00FF41]/85 overflow-x-auto">
          <code>{block.content}</code>
        </pre>
        {/* Scanline sutil */}
        <div
          className="absolute inset-0 pointer-events-none opacity-[0.03]"
          style={{
            backgroundImage:
              'repeating-linear-gradient(0deg,transparent,transparent 2px,#00FF41 2px,#00FF41 3px)',
          }}
        />
      </div>
    )
  }

  if (block.type === 'list' && block.items) {
    return (
      <ul className="my-2 space-y-1">
        {block.items.map((item, i) => (
          <li key={i} className="flex items-start gap-2 text-xs text-[#00FF41]/70 leading-5">
            <span className="text-[#00FF41]/30 mt-0.5 shrink-0">▸</span>
            <span><InlineText text={item} /></span>
          </li>
        ))}
      </ul>
    )
  }

  // paragraph — ignora separadores de tabla (|---|)
  if (block.content.startsWith('|---') || block.content.startsWith('| ---')) return null

  return (
    <p className="text-xs leading-6 text-[#00FF41]/70 my-1">
      <InlineText text={block.content} />
    </p>
  )
}

// ─── Componente principal MissionBriefing ─────────────────────────────────────

interface Props {
  title: string
  theoryContent: string
  challengeId: string
  onInitialize: () => void
}

export default function MissionBriefing({ title, theoryContent, onInitialize }: Props) {
  // Divide el contenido en páginas usando --- como separador
  const pages = useMemo(
    () =>
      theoryContent
        .split(/\n---\n/)
        .map((p) => p.trim())
        .filter(Boolean),
    [theoryContent]
  )

  const [currentPage, setCurrentPage] = useState(0)
  const [exiting, setExiting] = useState(false)
  const isLastPage = currentPage === pages.length - 1

  const parsedBlocks = useMemo(
    () => parseMarkdown(pages[currentPage] ?? ''),
    [pages, currentPage]
  )

  const handleInit = useCallback(() => {
    setExiting(true)
    // Pequeño delay para que la animación de cortina empiece antes de la callback
    setTimeout(onInitialize, 550)
  }, [onInitialize])

  return (
    <AnimatePresence>
      {!exiting ? (
        <motion.div
          key="briefing"
          className="flex flex-col h-full bg-[#050A05] font-mono text-[#00FF41] overflow-hidden relative"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ y: '-100%', opacity: 0 }}
          transition={{ duration: 0.5, ease: [0.4, 0, 0.2, 1] }}
        >
          {/* Scanlines de fondo */}
          <div
            className="absolute inset-0 pointer-events-none z-0 opacity-[0.04]"
            style={{
              backgroundImage:
                'repeating-linear-gradient(0deg,transparent,transparent 3px,#00FF41 3px,#00FF41 4px)',
            }}
          />

          {/* Header — clasificado */}
          <div className="relative z-10 shrink-0 px-6 pt-5 pb-4 border-b border-[#00FF41]/15">
            <div className="flex items-center justify-between mb-1">
              <div className="flex items-center gap-3">
                <motion.span
                  className="text-[10px] tracking-[0.35em] text-red-400/70 border border-red-500/30 px-2 py-0.5"
                  animate={{ opacity: [0.5, 1, 0.5] }}
                  transition={{ duration: 2, repeat: Infinity }}
                >
                  DOCUMENTO CLASIFICADO
                </motion.span>
                <span className="text-[10px] tracking-widest text-[#00FF41]/20">
                  REGISTRO #{String(currentPage + 1).padStart(3, '0')}
                </span>
              </div>
              <span className="text-[10px] tracking-[0.3em] text-[#00FF41]/20">
                ENIGMA // SALA DE BRIEFING
              </span>
            </div>
            <h1
              className="text-base font-black tracking-[0.15em] text-[#00FF41] mt-1"
              style={{ textShadow: '0 0 12px #00FF4150' }}
            >
              {title}
            </h1>
          </div>

          {/* Contenido paginado */}
          <div className="relative z-10 flex-1 overflow-y-auto px-6 py-4">
            <AnimatePresence mode="wait">
              <motion.div
                key={currentPage}
                initial={{ opacity: 0, x: 12 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -12 }}
                transition={{ duration: 0.2 }}
              >
                {parsedBlocks.map((block, i) => (
                  <Block key={i} block={block} />
                ))}
              </motion.div>
            </AnimatePresence>
          </div>

          {/* Footer — controles de paginación */}
          <div className="relative z-10 shrink-0 px-6 py-4 border-t border-[#00FF41]/15 bg-[#030803]">
            {/* Indicador de página */}
            <div className="flex items-center gap-2 mb-3">
              {pages.map((_, i) => (
                <button
                  key={i}
                  onClick={() => setCurrentPage(i)}
                  className="h-px transition-all duration-200"
                  style={{
                    width: i === currentPage ? '24px' : '12px',
                    backgroundColor: i === currentPage ? '#00FF41' : '#00FF4130',
                  }}
                />
              ))}
              <span className="ml-auto text-[10px] tracking-widest text-[#00FF41]/30">
                PÁGINA {currentPage + 1} / {pages.length}
              </span>
            </div>

            {/* Botones */}
            <div className="flex items-center gap-3">
              {/* Anterior */}
              {currentPage > 0 && (
                <button
                  onClick={() => setCurrentPage((p) => p - 1)}
                  className="px-3 py-2 text-xs tracking-widest text-[#00FF41]/40 border border-[#00FF41]/15 hover:text-[#00FF41]/70 hover:border-[#00FF41]/35 transition-all duration-150"
                >
                  ← REGISTRO ANTERIOR
                </button>
              )}

              {/* Siguiente o Inicializar */}
              {!isLastPage ? (
                <button
                  onClick={() => setCurrentPage((p) => p + 1)}
                  className="flex-1 py-2 text-xs font-bold tracking-[0.2em] border border-[#00FF41]/30 text-[#00FF41]/70 hover:text-[#00FF41] hover:border-[#00FF41]/60 transition-all duration-150"
                >
                  SIGUIENTE REGISTRO →
                </button>
              ) : (
                <motion.button
                  onClick={handleInit}
                  className="flex-1 py-3 text-sm font-black tracking-[0.2em] bg-[#00FF41] text-black hover:bg-[#00FF41]/90 active:scale-[0.99] transition-all duration-100"
                  style={{ boxShadow: '0 0 30px #00FF4140' }}
                  animate={{
                    boxShadow: [
                      '0 0 20px #00FF4130',
                      '0 0 40px #00FF4160',
                      '0 0 20px #00FF4130',
                    ],
                  }}
                  transition={{ duration: 2, repeat: Infinity }}
                >
                  INICIALIZAR ENTORNO DE PRUEBAS ▶
                </motion.button>
              )}
            </div>
          </div>
        </motion.div>
      ) : (
        // Cortina de transición — barre hacia arriba revelando el editor
        <motion.div
          key="curtain"
          className="absolute inset-0 z-50 bg-[#00FF41]"
          initial={{ scaleY: 0, originY: 1 }}
          animate={{ scaleY: 1 }}
          transition={{ duration: 0.4, ease: [0.4, 0, 1, 1] }}
        />
      )}
    </AnimatePresence>
  )
}
