'use client'

import Link from 'next/link'
import { getAllPosts, formatDate } from '@/lib/posts'

const CATEGORY_COLOR: Record<string, string> = {
  python:      '#00FF41',
  carrera:     '#06b6d4',
  metodologia: '#f59e0b',
}

export default function BlogPreviewSection() {
  const posts = getAllPosts().slice(0, 3)

  return (
    <section className="min-h-screen flex flex-col font-mono bg-[#020202] relative overflow-hidden">

      {/* Scanlines */}
      <div
        className="absolute inset-0 pointer-events-none opacity-[0.012]"
        style={{ backgroundImage: 'repeating-linear-gradient(0deg,transparent,transparent 3px,#00FF41 3px,#00FF41 4px)' }}
      />
      {/* Grid */}
      <div
        className="absolute inset-0 pointer-events-none"
        style={{
          backgroundImage: 'linear-gradient(rgba(0,255,65,0.03) 1px,transparent 1px),linear-gradient(90deg,rgba(0,255,65,0.03) 1px,transparent 1px)',
          backgroundSize: '72px 72px',
        }}
      />

      <div className="relative z-10 flex flex-col px-6 sm:px-10 py-16 gap-5">

        {/* Header */}
        <div>
          <p className="text-[8px] tracking-[0.6em] text-[#00FF41]/25 uppercase mb-2">
            {'// INTEL CODEX — TRANSMISIONES DEL NEXO'}
          </p>
          <div className="flex items-end justify-between gap-4">
            <h2 className="text-2xl sm:text-3xl font-black tracking-[0.08em] uppercase text-white/85 leading-tight">
              CONOCIMIENTO{' '}
              <span className="text-[#00FF41]" style={{ textShadow: '0 0 24px rgba(0,255,65,0.4)' }}>
                EN CAMPO
              </span>
            </h2>
            <Link
              href="/blog"
              className="text-[8px] tracking-[0.4em] uppercase text-[#00FF41]/30 hover:text-[#00FF41]/65 transition-colors shrink-0 hidden sm:block"
            >
              VER TODOS →
            </Link>
          </div>
        </div>

        {/* Post cards */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          {posts.map((post, i) => {
            const color = CATEGORY_COLOR[post.category] ?? '#00FF41'
            return (
              <Link key={post.slug} href={`/blog/${post.slug}`} className="group">
                <article
                  className="h-full flex flex-col border p-4 sm:p-5 relative overflow-hidden transition-all duration-250 cursor-pointer"
                  style={{ borderColor: `${color}15`, background: `${color}03` }}
                  onMouseEnter={(e) => {
                    const el = e.currentTarget as HTMLElement
                    el.style.borderColor = `${color}40`
                    el.style.background  = `${color}07`
                  }}
                  onMouseLeave={(e) => {
                    const el = e.currentTarget as HTMLElement
                    el.style.borderColor = `${color}15`
                    el.style.background  = `${color}03`
                  }}
                >
                  {/* Acento superior */}
                  <div
                    className="absolute top-0 left-0 right-0 h-px"
                    style={{ background: `linear-gradient(90deg,transparent,${color}45,transparent)` }}
                  />

                  {/* Número de transmisión */}
                  <div
                    className="text-[9px] font-black tracking-[0.3em] mb-3 opacity-20"
                    style={{ color }}
                  >
                    INFORME-{String(i + 1).padStart(2, '0')}
                  </div>

                  {/* Categoría + tiempo */}
                  <div className="flex items-center gap-2 mb-3">
                    <span
                      className="text-[7px] tracking-[0.4em] uppercase font-bold px-1.5 py-0.5 border"
                      style={{ color, borderColor: `${color}25`, background: `${color}06` }}
                    >
                      {post.categoryLabel}
                    </span>
                    <span className="text-white/20 text-[8px] tracking-wider">{post.readTime}</span>
                  </div>

                  {/* Título */}
                  <h3
                    className="text-sm font-black tracking-[0.05em] uppercase leading-snug mb-2 transition-colors duration-200"
                    style={{ color: 'rgba(255,255,255,0.78)' }}
                  >
                    {post.title}
                  </h3>

                  {/* Descripción */}
                  <p className="text-[10px] text-white/30 leading-relaxed flex-1 mb-4">
                    {post.description}
                  </p>

                  {/* Footer */}
                  <div className="flex items-center justify-between">
                    <span className="text-[7px] tracking-[0.3em] text-white/18">
                      {formatDate(post.publishedAt)}
                    </span>
                    <span
                      className="text-[7px] tracking-[0.35em] uppercase transition-colors duration-200"
                      style={{ color: `${color}45` }}
                    >
                      LEER →
                    </span>
                  </div>
                </article>
              </Link>
            )
          })}
        </div>

        {/* CTA strip */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-3 border-t border-[#00FF41]/10 pt-4">
          <p className="text-[11px] text-white/28 tracking-[0.15em] text-center sm:text-left">
            <span style={{ color: 'rgba(0,255,65,0.55)' }}>Python real.</span>
            {' · '}
            <span style={{ color: 'rgba(6,182,212,0.55)' }}>Carrera en LATAM.</span>
            {' · '}
            <span className="text-white/35">Sin teoría muerta.</span>
          </p>
          <div className="flex items-center gap-3">
            <Link
              href="/blog"
              className="border text-[9px] tracking-[0.35em] uppercase px-5 py-2.5 whitespace-nowrap transition-all duration-200"
              style={{ borderColor: 'rgba(0,255,65,0.30)', color: 'rgba(0,255,65,0.65)', background: 'rgba(0,255,65,0.04)' }}
              onMouseEnter={(e) => {
                const el = e.currentTarget as HTMLAnchorElement
                el.style.borderColor = 'rgba(0,255,65,0.65)'
                el.style.color       = '#00FF41'
                el.style.background  = 'rgba(0,255,65,0.09)'
              }}
              onMouseLeave={(e) => {
                const el = e.currentTarget as HTMLAnchorElement
                el.style.borderColor = 'rgba(0,255,65,0.30)'
                el.style.color       = 'rgba(0,255,65,0.65)'
                el.style.background  = 'rgba(0,255,65,0.04)'
              }}
            >
              {'[[ VER INTEL CODEX COMPLETO ]]'}
            </Link>
          </div>
        </div>

      </div>
    </section>
  )
}
