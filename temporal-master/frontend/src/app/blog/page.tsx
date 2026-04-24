import Link from 'next/link'
import type { Metadata } from 'next'
import { getAllPosts, formatDate } from '@/lib/posts'
import BlogPostCard from '@/components/Landing/BlogPostCard'
import BlogFeaturedCard from '@/components/Landing/BlogFeaturedCard'
import SiteNav from '@/components/Landing/SiteNav'
import Footer  from '@/components/Landing/Footer'

export const metadata: Metadata = {
  title: 'Intel Codex | DAKI EdTech — Python, Carrera y Programación en LATAM',
  description: 'Transmisiones sobre Python, carrera tech en Latinoamérica y análisis con código. Sin teoría muerta — solo código que corre y conocimiento del campo.',
  alternates: { canonical: 'https://dakiedtech.com/blog' },
}

const CATEGORY_COLOR: Record<string, string> = {
  python:      '#00FF41',
  carrera:     '#06b6d4',
  metodologia: '#f59e0b',
}

export default function BlogPage() {
  const allPosts = getAllPosts()
  const featured = allPosts[0]
  const rest     = allPosts.slice(1)

  return (
    <>
    <SiteNav />
    <main className="min-h-screen bg-[#020202] font-mono text-[#00FF41] pt-14">

      <div
        className="fixed inset-0 pointer-events-none z-0 opacity-[0.018]"
        style={{ backgroundImage: 'repeating-linear-gradient(0deg,transparent,transparent 3px,#00FF41 3px,#00FF41 4px)' }}
      />

      <div className="relative z-10 max-w-3xl mx-auto px-6 py-16">

        {/* Header — publication masthead */}
        <div className="mb-10">
          <div className="flex items-start justify-between gap-4 mb-4">
            <div>
              <p className="text-[8px] tracking-[0.6em] text-[#00FF41]/25 uppercase mb-3">
                {'// TRANSMISIONES DEL NEXO'}
              </p>
              <h1 className="text-3xl sm:text-4xl font-black tracking-[0.08em] uppercase leading-tight text-white/90">
                INTEL{' '}
                <span className="text-[#00FF41]" style={{ textShadow: '0 0 24px rgba(0,255,65,0.4)' }}>
                  CODEX
                </span>
              </h1>
            </div>
            {featured && (
              <div className="hidden sm:flex flex-col items-end gap-1 shrink-0 pt-6">
                <span className="text-[8px] tracking-[0.3em] text-[#00FF41]/20 uppercase">última transmisión</span>
                <span className="text-[9px] tracking-[0.2em] text-[#00FF41]/45">{formatDate(featured.publishedAt)}</span>
                <span className="text-[8px] tracking-[0.25em] text-white/20">{allPosts.length} transmisiones</span>
              </div>
            )}
          </div>
          <p className="text-sm text-white/32 tracking-wide max-w-xl">
            Python, carrera tech en LATAM y análisis con código real.
            Publicaciones para Operadores que leen con atención.
          </p>
          <div className="mt-6 h-px bg-gradient-to-r from-[#00FF41]/20 via-transparent to-transparent" />
        </div>

        {/* Featured post */}
        {featured && (() => {
          const color = CATEGORY_COLOR[featured.category] ?? '#00FF41'
          return (
            <div className="mb-10">
              <p className="text-[7px] tracking-[0.5em] text-[#00FF41]/20 uppercase mb-3">
                — TRANSMISIÓN DESTACADA
              </p>
              <Link href={`/blog/${featured.slug}`} className="group block">
                <BlogFeaturedCard color={color}>
                  <div className="flex items-center gap-3 mb-4">
                    <span
                      className="text-[7px] tracking-[0.4em] uppercase font-bold px-2 py-0.5 border"
                      style={{ color, borderColor: `${color}30`, background: `${color}08` }}
                    >
                      {featured.categoryLabel}
                    </span>
                    <span className="text-white/25 text-[8px] tracking-wider">{featured.readTime}</span>
                    <span style={{ color: `${color}30` }} className="text-[8px]">·</span>
                    <span className="text-white/22 text-[8px] tracking-[0.2em]">{formatDate(featured.publishedAt)}</span>
                  </div>
                  <h2
                    className="text-xl sm:text-2xl font-black tracking-[0.04em] uppercase leading-snug mb-3 group-hover:text-white/95 transition-colors duration-200"
                    style={{ color: 'rgba(255,255,255,0.88)' }}
                  >
                    {featured.title}
                  </h2>
                  <p className="text-xs text-white/38 leading-relaxed tracking-wide mb-4">
                    {featured.description}
                  </p>
                  <span
                    className="text-[8px] tracking-[0.4em] uppercase"
                    style={{ color: `${color}60` }}
                  >
                    LEER TRANSMISIÓN COMPLETA →
                  </span>
                </BlogFeaturedCard>
              </Link>
            </div>
          )
        })()}

        {/* Archive */}
        {rest.length > 0 && (
          <>
            <p className="text-[7px] tracking-[0.5em] text-[#00FF41]/20 uppercase mb-5">
              — ARCHIVO DE TRANSMISIONES
            </p>
            <div className="space-y-4">
              {rest.map((post) => {
                const color = CATEGORY_COLOR[post.category] ?? '#00FF41'
                return (
                  <article key={post.slug}>
                    <Link href={`/blog/${post.slug}`} className="group block">
                      <BlogPostCard color={color}>
                        <div className="flex items-center gap-3 mb-2.5">
                          <span
                            className="text-[7px] tracking-[0.4em] uppercase font-bold px-2 py-0.5 border"
                            style={{ color, borderColor: `${color}30`, background: `${color}08` }}
                          >
                            {post.categoryLabel}
                          </span>
                          <span className="text-[#00FF41]/18 text-[8px]">·</span>
                          <span className="text-white/22 text-[8px] tracking-[0.25em]">{post.readTime}</span>
                          <span className="text-[#00FF41]/18 text-[8px]">·</span>
                          <span className="text-white/18 text-[8px] tracking-[0.2em]">{formatDate(post.publishedAt)}</span>
                        </div>
                        <h2 className="text-sm sm:text-base font-black tracking-[0.04em] uppercase leading-snug mb-2 text-white/72 group-hover:text-white/90 transition-colors duration-200">
                          {post.title}
                        </h2>
                        <div className="flex items-center justify-between">
                          <p className="text-[10px] text-white/30 leading-relaxed tracking-wide max-w-lg">
                            {post.description}
                          </p>
                          <span
                            className="text-[8px] tracking-[0.35em] uppercase shrink-0 ml-4 opacity-40 group-hover:opacity-80 transition-opacity duration-200"
                            style={{ color }}
                          >
                            LEER →
                          </span>
                        </div>
                      </BlogPostCard>
                    </Link>
                  </article>
                )
              })}
            </div>
          </>
        )}

        {/* Newsletter CTA */}
        <div
          className="mt-12 p-6 border-l-2"
          style={{ borderColor: '#00FF41', background: 'rgba(0,255,65,0.02)' }}
        >
          <p className="text-[8px] tracking-[0.5em] text-[#00FF41]/25 uppercase mb-2">
            {'// TRANSMISIONES DEL NEXO'}
          </p>
          <p className="text-sm font-black text-white/75 uppercase tracking-wide mb-1">
            Próxima transmisión: Python en producción.
          </p>
          <p className="text-[11px] text-white/35 mb-4">
            Cada semana un análisis nuevo. Código real. Sin spam.
          </p>
          <Link
            href="/register"
            className="inline-block text-[9px] tracking-[0.4em] uppercase border border-[#00FF41]/40 px-6 py-3 text-[#00FF41] hover:bg-[#00FF41]/06 hover:border-[#00FF41]/65 transition-all duration-200"
          >
            {'[[ UNIRSE AL NEXO — GRATIS ]]'}
          </Link>
        </div>

      </div>
    </main>
    <Footer />
    </>
  )
}
