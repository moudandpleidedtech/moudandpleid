'use client'

import Link from 'next/link'
import { getAllPosts, formatDate } from '@/lib/posts'

const CATEGORY_COLOR: Record<string, string> = {
  python:      '#00FF41',
  carrera:     '#06b6d4',
  metodologia: '#f59e0b',
}

export default function BlogPreviewSection() {
  const all     = getAllPosts()
  const featured = all[0]
  const rest     = all.slice(1, 4)

  if (!featured) return null

  const featuredColor = CATEGORY_COLOR[featured.category] ?? '#00FF41'

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

      <div className="relative z-10 flex flex-col px-6 sm:px-10 py-16 gap-6">

        {/* Header */}
        <div className="flex items-end justify-between gap-4">
          <div>
            <p className="text-[8px] tracking-[0.6em] text-[#00FF41]/25 uppercase mb-2">
              {'// INTEL CODEX — TRANSMISIONES DEL NEXO'}
            </p>
            <h2 className="text-2xl sm:text-3xl font-black tracking-[0.08em] uppercase text-white/85 leading-tight">
              ÚLTIMAS{' '}
              <span className="text-[#00FF41]" style={{ textShadow: '0 0 24px rgba(0,255,65,0.4)' }}>
                TRANSMISIONES
              </span>
            </h2>
          </div>
          <div className="hidden sm:flex flex-col items-end gap-1 shrink-0">
            <span className="text-[8px] tracking-[0.3em] text-[#00FF41]/20 uppercase">
              última transmisión
            </span>
            <span className="text-[9px] tracking-[0.2em] text-[#00FF41]/45">
              {formatDate(featured.publishedAt)}
            </span>
          </div>
        </div>

        {/* Featured post — hero card */}
        <Link href={`/blog/${featured.slug}`} className="group block">
          <article
            className="relative border p-6 sm:p-8 overflow-hidden transition-all duration-300 cursor-pointer"
            style={{ borderColor: `${featuredColor}20`, background: `${featuredColor}04` }}
            onMouseEnter={(e) => {
              const el = e.currentTarget as HTMLElement
              el.style.borderColor = `${featuredColor}45`
              el.style.background  = `${featuredColor}07`
            }}
            onMouseLeave={(e) => {
              const el = e.currentTarget as HTMLElement
              el.style.borderColor = `${featuredColor}20`
              el.style.background  = `${featuredColor}04`
            }}
          >
            {/* Accent line */}
            <div
              className="absolute top-0 left-0 right-0 h-px"
              style={{ background: `linear-gradient(90deg,transparent,${featuredColor}60,transparent)` }}
            />

            <div className="flex flex-col sm:flex-row sm:items-start gap-4 sm:gap-8">
              <div className="flex-1 min-w-0">
                {/* Meta */}
                <div className="flex items-center gap-3 mb-4">
                  <span
                    className="text-[7px] tracking-[0.45em] uppercase font-bold px-2 py-0.5 border"
                    style={{ color: featuredColor, borderColor: `${featuredColor}30`, background: `${featuredColor}08` }}
                  >
                    {featured.categoryLabel}
                  </span>
                  <span className="text-white/25 text-[8px] tracking-wide">{featured.readTime}</span>
                  <span style={{ color: `${featuredColor}30` }} className="text-[8px]">·</span>
                  <span className="text-white/22 text-[8px] tracking-[0.2em]">{formatDate(featured.publishedAt)}</span>
                </div>

                {/* Title */}
                <h3
                  className="text-xl sm:text-2xl font-black tracking-[0.04em] uppercase leading-snug mb-3 transition-colors duration-200 group-hover:text-white/95"
                  style={{ color: 'rgba(255,255,255,0.85)' }}
                >
                  {featured.title}
                </h3>

                {/* Description */}
                <p className="text-[11px] sm:text-xs text-white/38 leading-relaxed max-w-2xl">
                  {featured.description}
                </p>
              </div>

              {/* CTA badge */}
              <div className="shrink-0 flex sm:flex-col items-center sm:items-end gap-2">
                <span
                  className="text-[8px] tracking-[0.4em] uppercase font-bold transition-colors duration-200"
                  style={{ color: `${featuredColor}50` }}
                >
                  ÚLTIMA TRANSMISIÓN
                </span>
                <span
                  className="text-[9px] tracking-[0.35em] uppercase transition-colors duration-200 group-hover:opacity-100 opacity-60"
                  style={{ color: featuredColor }}
                >
                  LEER →
                </span>
              </div>
            </div>
          </article>
        </Link>

        {/* Secondary posts */}
        {rest.length > 0 && (
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            {rest.map((post, i) => {
              const color = CATEGORY_COLOR[post.category] ?? '#00FF41'
              return (
                <Link key={post.slug} href={`/blog/${post.slug}`} className="group">
                  <article
                    className="h-full flex flex-col border p-4 sm:p-5 relative overflow-hidden transition-all duration-250 cursor-pointer"
                    style={{ borderColor: `${color}12`, background: `${color}02` }}
                    onMouseEnter={(e) => {
                      const el = e.currentTarget as HTMLElement
                      el.style.borderColor = `${color}35`
                      el.style.background  = `${color}06`
                    }}
                    onMouseLeave={(e) => {
                      const el = e.currentTarget as HTMLElement
                      el.style.borderColor = `${color}12`
                      el.style.background  = `${color}02`
                    }}
                  >
                    <div
                      className="absolute top-0 left-0 right-0 h-px"
                      style={{ background: `linear-gradient(90deg,transparent,${color}35,transparent)` }}
                    />

                    <div className="text-[9px] font-black tracking-[0.3em] mb-3 opacity-15" style={{ color }}>
                      TRANS-{String(i + 2).padStart(2, '0')}
                    </div>

                    <div className="flex items-center gap-2 mb-3">
                      <span
                        className="text-[7px] tracking-[0.4em] uppercase font-bold px-1.5 py-0.5 border"
                        style={{ color, borderColor: `${color}25`, background: `${color}06` }}
                      >
                        {post.categoryLabel}
                      </span>
                      <span className="text-white/20 text-[8px] tracking-wider">{post.readTime}</span>
                    </div>

                    <h3
                      className="text-sm font-black tracking-[0.05em] uppercase leading-snug mb-2 transition-colors duration-200"
                      style={{ color: 'rgba(255,255,255,0.72)' }}
                    >
                      {post.title}
                    </h3>

                    <p className="text-[10px] text-white/28 leading-relaxed flex-1 mb-4">
                      {post.description}
                    </p>

                    <div className="flex items-center justify-between">
                      <span className="text-[7px] tracking-[0.3em] text-white/18">
                        {formatDate(post.publishedAt)}
                      </span>
                      <span
                        className="text-[7px] tracking-[0.35em] uppercase opacity-50 group-hover:opacity-100 transition-opacity duration-200"
                        style={{ color }}
                      >
                        LEER →
                      </span>
                    </div>
                  </article>
                </Link>
              )
            })}
          </div>
        )}

        {/* Footer strip */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-3 border-t border-[#00FF41]/10 pt-4">
          <p className="text-[11px] text-white/22 tracking-[0.18em] text-center sm:text-left">
            <span style={{ color: 'rgba(0,255,65,0.50)' }}>Python real.</span>
            {' · '}
            <span style={{ color: 'rgba(6,182,212,0.50)' }}>Análisis con código.</span>
            {' · '}
            <span className="text-white/28">Para devs de LATAM.</span>
          </p>
          <Link
            href="/blog"
            className="border text-[9px] tracking-[0.35em] uppercase px-5 py-2.5 whitespace-nowrap transition-all duration-200"
            style={{ borderColor: 'rgba(0,255,65,0.25)', color: 'rgba(0,255,65,0.60)', background: 'transparent' }}
            onMouseEnter={(e) => {
              const el = e.currentTarget as HTMLAnchorElement
              el.style.borderColor = 'rgba(0,255,65,0.60)'
              el.style.color       = '#00FF41'
              el.style.background  = 'rgba(0,255,65,0.05)'
            }}
            onMouseLeave={(e) => {
              const el = e.currentTarget as HTMLAnchorElement
              el.style.borderColor = 'rgba(0,255,65,0.25)'
              el.style.color       = 'rgba(0,255,65,0.60)'
              el.style.background  = 'transparent'
            }}
          >
            {'[[ VER INTEL CODEX COMPLETO ]]'}
          </Link>
        </div>

      </div>
    </section>
  )
}
