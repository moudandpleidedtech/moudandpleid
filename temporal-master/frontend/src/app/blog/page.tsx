import Link from 'next/link'
import type { Metadata } from 'next'
import { getAllPosts, formatDate } from '@/lib/posts'
import BlogPostCard from '@/components/Landing/BlogPostCard'
import SiteNav from '@/components/Landing/SiteNav'
import Footer  from '@/components/Landing/Footer'

export const metadata: Metadata = {
  title: 'Blog | DAKI EdTech — Python, Carrera y Programación en LATAM',
  description: 'Artículos sobre Python, carrera tech en Latinoamérica y metodología de aprendizaje. Sin teoría muerta — solo código que corre y conocimiento que sirve.',
  alternates: { canonical: 'https://dakiedtech.com/blog' },
}

const CATEGORY_COLOR: Record<string, string> = {
  python:      '#00FF41',
  carrera:     '#06b6d4',
  metodologia: '#f59e0b',
}

export default function BlogPage() {
  const posts = getAllPosts()

  return (
    <>
    <SiteNav />
    <main className="min-h-screen bg-[#020202] font-mono text-[#00FF41] pt-14">

      <div
        className="fixed inset-0 pointer-events-none z-0 opacity-[0.018]"
        style={{ backgroundImage: 'repeating-linear-gradient(0deg,transparent,transparent 3px,#00FF41 3px,#00FF41 4px)' }}
      />

      <div className="relative z-10 max-w-3xl mx-auto px-6 py-16">

        {/* Header */}
        <div className="mb-12">
          <p className="text-[8px] tracking-[0.6em] text-[#00FF41]/25 uppercase mb-3">
            {'// INTEL CODEX — TRANSMISIONES DEL NEXO'}
          </p>
          <h1 className="text-3xl sm:text-4xl font-black tracking-[0.08em] uppercase leading-tight text-white/90 mb-3">
            INTEL{' '}
            <span className="text-[#00FF41]" style={{ textShadow: '0 0 24px rgba(0,255,65,0.4)' }}>
              CODEX
            </span>
          </h1>
          <p className="text-sm text-white/35 tracking-wide max-w-lg">
            Python, carrera tech en LATAM y metodología de aprendizaje real.
            Sin teoría muerta — solo código que corre.
          </p>
          <div className="mt-6 h-px bg-gradient-to-r from-[#00FF41]/20 via-transparent to-transparent" />
        </div>

        {/* Posts */}
        <div className="space-y-6">
          {posts.map((post) => {
            const color = CATEGORY_COLOR[post.category] ?? '#00FF41'
            return (
              <article key={post.slug}>
                <Link href={`/blog/${post.slug}`} className="group block">
                  <BlogPostCard color={color}>
                    <div className="flex items-center gap-3 mb-3">
                      <span
                        className="text-[7px] tracking-[0.4em] uppercase font-bold px-2 py-0.5 border"
                        style={{ color, borderColor: `${color}30`, background: `${color}08` }}
                      >
                        {post.categoryLabel}
                      </span>
                      <span className="text-[#00FF41]/20 text-[8px] tracking-widest">·</span>
                      <span className="text-white/22 text-[8px] tracking-[0.25em]">{post.readTime}</span>
                      <span className="text-[#00FF41]/20 text-[8px] tracking-widest">·</span>
                      <span className="text-white/22 text-[8px] tracking-[0.2em]">{formatDate(post.publishedAt)}</span>
                    </div>

                    <h2 className="text-base sm:text-lg font-black tracking-[0.04em] uppercase leading-snug mb-2 text-white/80 group-hover:text-white/95 transition-colors duration-200">
                      {post.title}
                    </h2>

                    <p className="text-[11px] text-white/35 leading-relaxed tracking-wide mb-3">
                      {post.description}
                    </p>

                    <span
                      className="text-[8px] tracking-[0.35em] uppercase transition-colors duration-200"
                      style={{ color: `${color}55` }}
                    >
                      LEER INFORME →
                    </span>
                  </BlogPostCard>
                </Link>
              </article>
            )
          })}
        </div>

      </div>
    </main>
    <Footer />
    </>
  )
}
