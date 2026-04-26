'use client'

import Link from 'next/link'
import { getAllPosts, formatDate } from '@/lib/posts'

const CATEGORY_COLOR: Record<string, string> = {
  python:      '#00FF41',
  carrera:     '#06b6d4',
  metodologia: '#f59e0b',
}

export default function BlogPreviewSection() {
  const all      = getAllPosts()
  const featured = all[0]
  const sidebar  = all.slice(1, 4)

  if (!featured) return null

  const fc = CATEGORY_COLOR[featured.category] ?? '#00FF41'

  return (
    <section className="font-mono bg-[#020202] relative overflow-hidden border-t border-[#00FF41]/08">

      <div
        className="absolute inset-0 pointer-events-none opacity-[0.010]"
        style={{ backgroundImage: 'repeating-linear-gradient(0deg,transparent,transparent 3px,#00FF41 3px,#00FF41 4px)' }}
      />

      <div className="relative z-10 px-6 sm:px-10 py-14">

        {/* Masthead */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-4">
            <div>
              <p className="text-[7px] tracking-[0.6em] text-[#00FF41]/25 uppercase mb-1">
                {'// INTEL CODEX'}
              </p>
              <h2 className="text-xl sm:text-2xl font-black tracking-[0.1em] uppercase text-white/85">
                ÚLTIMAS{' '}
                <span className="text-[#00FF41]" style={{ textShadow: '0 0 20px rgba(0,255,65,0.4)' }}>
                  TRANSMISIONES
                </span>
              </h2>
            </div>
            <div className="hidden sm:flex items-center gap-1.5 ml-4">
              <span className="w-1.5 h-1.5 rounded-full bg-[#00FF41] animate-pulse" style={{ boxShadow: '0 0 5px #00FF41' }} />
              <span className="text-[8px] tracking-[0.35em] text-[#00FF41]/45 uppercase">{all.length} transmisiones</span>
            </div>
          </div>
          <Link
            href="/blog"
            className="hidden sm:block text-[8px] tracking-[0.4em] uppercase text-[#00FF41]/40 hover:text-[#00FF41]/75 transition-colors border border-[#00FF41]/15 px-4 py-1.5 hover:border-[#00FF41]/35"
          >
            VER TODAS →
          </Link>
        </div>

        {/* Magazine grid: featured (2/3) + sidebar (1/3) */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-8">

          {/* Featured — spans 2 cols */}
          <Link href={`/blog/${featured.slug}`} className="group lg:col-span-2 block">
            <article
              className="h-full relative border p-6 sm:p-8 overflow-hidden transition-all duration-300 cursor-pointer flex flex-col"
              style={{ borderColor: `${fc}25`, background: `${fc}04` }}
              onMouseEnter={e => {
                const el = e.currentTarget as HTMLElement
                el.style.borderColor = `${fc}55`
                el.style.background  = `${fc}08`
              }}
              onMouseLeave={e => {
                const el = e.currentTarget as HTMLElement
                el.style.borderColor = `${fc}25`
                el.style.background  = `${fc}04`
              }}
            >
              {/* Top accent */}
              <div className="absolute top-0 left-0 right-0 h-[2px]"
                style={{ background: `linear-gradient(90deg,transparent,${fc},transparent)` }} />

              {/* Left accent bar */}
              <div className="absolute top-0 left-0 bottom-0 w-[2px]" style={{ background: `${fc}40` }} />

              {/* Label */}
              <div className="flex items-center gap-3 mb-5">
                <div className="flex items-center gap-1.5">
                  <span className="w-1 h-1 rounded-full animate-pulse" style={{ background: fc }} />
                  <span className="text-[7px] tracking-[0.5em] uppercase font-black" style={{ color: `${fc}80` }}>
                    ÚLTIMA TRANSMISIÓN
                  </span>
                </div>
                <span className="text-[#00FF41]/15 text-[8px]">·</span>
                <span
                  className="text-[7px] tracking-[0.4em] uppercase font-bold px-2 py-0.5 border"
                  style={{ color: fc, borderColor: `${fc}30`, background: `${fc}08` }}
                >
                  {featured.categoryLabel}
                </span>
                <span className="text-white/22 text-[8px] tracking-wide">{featured.readTime}</span>
              </div>

              {/* Title — large */}
              <h3
                className="text-2xl sm:text-3xl font-black tracking-[0.03em] uppercase leading-tight mb-4 transition-colors duration-200 group-hover:text-white flex-1"
                style={{ color: 'rgba(255,255,255,0.90)' }}
              >
                {featured.title}
              </h3>

              <p className="text-sm text-white/40 leading-relaxed mb-6 max-w-xl">
                {featured.description}
              </p>

              {/* CTA */}
              <div className="flex items-center justify-between">
                <span className="text-[8px] tracking-[0.3em] text-white/20">{formatDate(featured.publishedAt)}</span>
                <span
                  className="text-[9px] tracking-[0.4em] uppercase font-bold opacity-60 group-hover:opacity-100 transition-opacity"
                  style={{ color: fc }}
                >
                  LEER TRANSMISIÓN →
                </span>
              </div>
            </article>
          </Link>

          {/* Sidebar — 3 cards */}
          <div className="flex flex-col gap-3">
            {sidebar.map((post, i) => {
              const color = CATEGORY_COLOR[post.category] ?? '#00FF41'
              return (
                <Link key={post.slug} href={`/blog/${post.slug}`} className="group flex-1">
                  <article
                    className="h-full flex flex-col border p-4 relative overflow-hidden transition-all duration-200 cursor-pointer"
                    style={{ borderColor: `${color}12`, background: `${color}02` }}
                    onMouseEnter={e => {
                      const el = e.currentTarget as HTMLElement
                      el.style.borderColor = `${color}35`
                      el.style.background  = `${color}06`
                    }}
                    onMouseLeave={e => {
                      const el = e.currentTarget as HTMLElement
                      el.style.borderColor = `${color}12`
                      el.style.background  = `${color}02`
                    }}
                  >
                    <div className="absolute top-0 left-0 right-0 h-px"
                      style={{ background: `linear-gradient(90deg,transparent,${color}30,transparent)` }} />

                    <div className="flex items-center gap-2 mb-2">
                      <span
                        className="text-[6px] tracking-[0.4em] uppercase font-bold px-1.5 py-0.5 border"
                        style={{ color, borderColor: `${color}25`, background: `${color}06` }}
                      >
                        {post.categoryLabel}
                      </span>
                      <span className="text-white/18 text-[7px]">{post.readTime}</span>
                    </div>

                    <h4
                      className="text-[11px] font-black tracking-[0.04em] uppercase leading-snug flex-1 mb-2 group-hover:text-white/90 transition-colors"
                      style={{ color: 'rgba(255,255,255,0.68)' }}
                    >
                      {post.title}
                    </h4>

                    <span
                      className="text-[7px] tracking-[0.3em] uppercase opacity-40 group-hover:opacity-80 transition-opacity"
                      style={{ color }}
                    >
                      LEER →
                    </span>
                  </article>
                </Link>
              )
            })}
          </div>
        </div>

        {/* Bottom strip */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 border-t border-[#00FF41]/08 pt-5">
          <p className="text-[10px] text-white/22 tracking-[0.18em]">
            <span style={{ color: 'rgba(0,255,65,0.50)' }}>Python real.</span>
            {'  ·  '}
            <span style={{ color: 'rgba(6,182,212,0.50)' }}>Análisis con código.</span>
            {'  ·  '}
            <span>Para devs de LATAM.</span>
          </p>
          <Link
            href="/blog"
            className="text-[9px] tracking-[0.35em] uppercase px-6 py-2.5 font-bold transition-all duration-200 border border-[#00FF41]/30 text-[#00FF41]/70 hover:bg-[#00FF41] hover:text-[#020202] hover:border-[#00FF41]"
          >
            VER INTEL CODEX COMPLETO →
          </Link>
        </div>

      </div>
    </section>
  )
}
