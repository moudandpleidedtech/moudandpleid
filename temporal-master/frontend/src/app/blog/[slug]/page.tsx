import Link from 'next/link'
import { notFound } from 'next/navigation'
import type { Metadata } from 'next'
import { getAllPosts, getPostBySlug, formatDate } from '@/lib/posts'
import GiscusComments from '@/components/UI/GiscusComments'
import NewsletterForm  from '@/components/UI/NewsletterForm'
import SiteNav from '@/components/Landing/SiteNav'
import Footer  from '@/components/Landing/Footer'

interface Props {
  params: { slug: string }
}

export function generateStaticParams() {
  return getAllPosts().map((p) => ({ slug: p.slug }))
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const post = getPostBySlug(params.slug)
  if (!post) return {}

  const keywords = Array.from(new Set([post.categoryLabel, 'Python', 'LATAM', 'programacion', 'DAKI EdTech']))

  return {
    title: `${post.title} | DAKI EdTech`,
    description: post.description,
    keywords,
    alternates: { canonical: `https://dakiedtech.com/blog/${post.slug}` },
    openGraph: {
      title: post.title,
      description: post.description,
      type: 'article',
      publishedTime: post.publishedAt,
      siteName: 'DAKI EdTech',
      images: [
        {
          url: 'https://dakiedtech.com/assets/demo.png',
          width: 1200,
          height: 630,
          alt: post.title,
        },
      ],
    },
    twitter: {
      card: 'summary_large_image',
      title: post.title,
      description: post.description,
      images: ['https://dakiedtech.com/assets/demo.png'],
    },
  }
}

const CATEGORY_COLOR: Record<string, string> = {
  python:      '#00FF41',
  carrera:     '#06b6d4',
  metodologia: '#f59e0b',
}

export default function PostPage({ params }: Props) {
  const post = getPostBySlug(params.slug)
  if (!post) notFound()

  const color = CATEGORY_COLOR[post.category] ?? '#00FF41'

  return (
    <>
    <SiteNav />
    <main className="min-h-screen bg-[#020202] font-mono text-[#00FF41] pt-14">

      {/* Scanlines */}
      <div
        className="fixed inset-0 pointer-events-none z-0 opacity-[0.018]"
        style={{ backgroundImage: 'repeating-linear-gradient(0deg,transparent,transparent 3px,#00FF41 3px,#00FF41 4px)' }}
      />

      {/* Schema JSON-LD para Article */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            '@context': 'https://schema.org',
            '@type': 'Article',
            headline: post.title,
            description: post.description,
            keywords: [post.categoryLabel, 'Python', 'LATAM', 'programacion'].join(', '),
            datePublished: post.publishedAt,
            image: 'https://dakiedtech.com/assets/demo.png',
            author: {
              '@type': 'Organization',
              name: 'DAKI EdTech',
              url: 'https://dakiedtech.com',
            },
            publisher: {
              '@type': 'Organization',
              name: 'DAKI EdTech',
              url: 'https://dakiedtech.com',
              logo: {
                '@type': 'ImageObject',
                url: 'https://dakiedtech.com/icon.png',
              },
            },
            mainEntityOfPage: `https://dakiedtech.com/blog/${post.slug}`,
          }),
        }}
      />
      {/* BreadcrumbList */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            '@context': 'https://schema.org',
            '@type': 'BreadcrumbList',
            itemListElement: [
              { '@type': 'ListItem', position: 1, name: 'NEXO', item: 'https://dakiedtech.com' },
              { '@type': 'ListItem', position: 2, name: 'Intel Codex', item: 'https://dakiedtech.com/blog' },
              { '@type': 'ListItem', position: 3, name: post.title, item: `https://dakiedtech.com/blog/${post.slug}` },
            ],
          }),
        }}
      />

      <div className="relative z-10 max-w-2xl mx-auto px-6 py-16">

        {/* Breadcrumb */}
        <div className="flex items-center gap-2 mb-10 text-[8px] tracking-[0.35em] uppercase">
          <Link href="/" className="text-[#00FF41]/28 hover:text-[#00FF41]/55 transition-colors">
            NEXO
          </Link>
          <span className="text-[#00FF41]/15">›</span>
          <Link href="/blog" className="text-[#00FF41]/28 hover:text-[#00FF41]/55 transition-colors">
            INTEL CODEX
          </Link>
          <span className="text-[#00FF41]/15">›</span>
          <span className="text-[#00FF41]/40">{post.categoryLabel}</span>
        </div>

        {/* Header del post */}
        <header className="mb-10">
          <div className="flex items-center gap-3 mb-4">
            <span
              className="text-[7px] tracking-[0.4em] uppercase font-bold px-2 py-0.5 border"
              style={{ color, borderColor: `${color}30`, background: `${color}08` }}
            >
              {post.categoryLabel}
            </span>
            <span className="text-white/22 text-[8px] tracking-[0.25em]">{post.readTime}</span>
            <span className="text-[#00FF41]/15 text-[8px]">·</span>
            <span className="text-white/22 text-[8px] tracking-[0.2em]">{formatDate(post.publishedAt)}</span>
          </div>

          <h1 className="text-2xl sm:text-3xl font-black tracking-[0.05em] uppercase leading-tight text-white/90 mb-4">
            {post.title}
          </h1>

          <p className="text-sm text-white/40 leading-relaxed tracking-wide">
            {post.description}
          </p>

          <div className="mt-6 h-px bg-gradient-to-r from-[#00FF41]/20 via-transparent to-transparent" />
        </header>

        {/* Contenido del artículo */}
        <article
          className="prose-nexo"
          dangerouslySetInnerHTML={{ __html: post.content }}
        />

        {/* CTA integrado */}
        <div
          className="mt-12 p-6 border-l-2"
          style={{ borderColor: '#00FF41', background: 'rgba(0,255,65,0.03)' }}
        >
          <p className="text-[8px] tracking-[0.5em] text-[#00FF41]/30 uppercase mb-3">
            {'// SIGUIENTE PASO'}
          </p>
          <p className="text-sm font-bold text-white/75 tracking-wide uppercase leading-snug mb-2">
            ¿Querés practicar esto con código real?
          </p>
          <p className="text-[11px] text-white/38 leading-relaxed mb-4">
            DAKI tiene misiones diseñadas exactamente para este tema.
            Código ejecutable, feedback de IA en tiempo real, sin teoría muerta.
          </p>
          <div className="flex flex-col sm:flex-row gap-3">
            <Link
              href="/register"
              className="inline-block bg-[#00FF41] text-[#020202] text-[9px] tracking-[0.4em] uppercase font-black px-6 py-3 hover:bg-[#00FF41]/90 transition-colors duration-150 text-center"
            >
              EMPEZAR GRATIS — 10 MISIONES →
            </Link>
            <Link
              href="https://go.hotmart.com/K105401308T"
              target="_blank"
              rel="noopener noreferrer"
              className="text-[9px] tracking-[0.35em] uppercase text-[#00FF41]/35 hover:text-[#00FF41]/65 transition-colors py-3 text-center"
            >
              O suscribirse — $19/mes →
            </Link>
          </div>
        </div>

        {/* Newsletter */}
        <div className="mt-10">
          <NewsletterForm source={`blog-${post.slug}`} />
        </div>

        {/* Comentarios */}
        <GiscusComments term={post.slug} />

      </div>
    </main>
    <Footer />
    </>
  )
}
