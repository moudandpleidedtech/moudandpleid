import type { Metadata } from 'next'
import { Suspense } from 'react'
import './globals.css'
import TopNav from '@/components/UI/TopNav'
import NeuralInstabilityEvent from '@/components/UI/NeuralInstabilityEvent'
import BunkerAtmosphere from '@/components/UI/BunkerAtmosphere'
import AffiliateTracker from '@/components/UI/AffiliateTracker'

export const metadata: Metadata = {
  title: 'Aprende Python desde Cero | DAKI EdTech — Gamificado en Español',
  description: 'Aprende Python desde cero con misiones reales, IA como instructora táctica y 100 niveles de código ejecutable. La plataforma gamificada de Python para Latinoamérica. Sin teoría muerta.',
  icons: {
    icon: '/icon.png',
    shortcut: '/icon.png',
    apple: '/icon.png',
  },
  openGraph: {
    title: 'Aprende Python desde Cero | DAKI EdTech — Gamificado en Español',
    description: 'Domina Python con misiones reales, IA táctica y certificación verificable. Para devs de LATAM que quieren trabajo en tech.',
    siteName: 'DAKI EdTech',
    locale: 'es_419',
    type: 'website',
    url: 'https://dakiedtech.com',
    images: [
      {
        url: 'https://dakiedtech.com/assets/demo.png',
        width: 1200,
        height: 630,
        alt: 'DAKI EdTech — Plataforma gamificada para aprender Python',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Aprende Python desde Cero | DAKI EdTech — Gamificado en Español',
    description: 'Domina Python con misiones reales e IA táctica. Para LATAM.',
    images: ['https://dakiedtech.com/assets/demo.png'],
  },
  alternates: {
    canonical: 'https://dakiedtech.com',
  },
  verification: {
    google: process.env.NEXT_PUBLIC_GSC_VERIFICATION ?? '',
  },
}

const schemaOrganization = {
  '@context': 'https://schema.org',
  '@type': 'Organization',
  name: 'DAKI EdTech',
  url: 'https://dakiedtech.com',
  logo: 'https://dakiedtech.com/icon.png',
  sameAs: [
    'https://www.instagram.com/dakiedtech',
    'https://www.tiktok.com/@dakiedtech',
    'https://www.youtube.com/@dakiedtech',
  ],
}

const schemaCourse = {
  '@context': 'https://schema.org',
  '@type': 'Course',
  name: 'Python Core — DAKI EdTech',
  description:
    'Aprende Python desde cero con misiones gamificadas, IA como instructora táctica y 100 niveles de código real. Plataforma para Latinoamérica en español.',
  provider: {
    '@type': 'Organization',
    name: 'DAKI EdTech',
    sameAs: 'https://dakiedtech.com',
  },
  educationalLevel: 'Beginner to Advanced',
  inLanguage: 'es',
  isAccessibleForFree: true,
  offers: [
    {
      '@type': 'Offer',
      price: '0',
      priceCurrency: 'USD',
      name: 'Plan Exploración — 10 misiones gratis',
      availability: 'https://schema.org/InStock',
    },
    {
      '@type': 'Offer',
      price: '19',
      priceCurrency: 'USD',
      name: 'Suscripción Mensual — acceso completo',
      url: 'https://go.hotmart.com/K105401308T',
      availability: 'https://schema.org/InStock',
    },
  ],
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(schemaOrganization) }}
        />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(schemaCourse) }}
        />
      </head>
      <body className="crt">
        <BunkerAtmosphere />
        <TopNav />
        <NeuralInstabilityEvent />
        <Suspense fallback={null}>
          <AffiliateTracker />
        </Suspense>
        {children}
      </body>
    </html>
  )
}
