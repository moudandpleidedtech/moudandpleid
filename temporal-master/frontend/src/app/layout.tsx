import type { Metadata } from 'next'
import { Suspense } from 'react'
import './globals.css'
import TopNav from '@/components/UI/TopNav'
import NeuralInstabilityEvent from '@/components/UI/NeuralInstabilityEvent'
import BunkerAtmosphere from '@/components/UI/BunkerAtmosphere'
import AffiliateTracker from '@/components/UI/AffiliateTracker'

export const metadata: Metadata = {
  title: 'DAKI EdTech — Aprende Python jugando',
  description: 'DAKI EdTech es la plataforma EdTech gamificada donde aprendes Python guiado por DAKI, tu instructora de IA táctica.',
  icons: {
    icon: '/icon.png',
    shortcut: '/icon.png',
    apple: '/icon.png',
  },
  openGraph: {
    title: 'DAKI EdTech',
    description: 'Aprende Python en 100 niveles con mecánicas de videojuego y la guía de DAKI.',
    siteName: 'DAKI EdTech',
    locale: 'es_AR',
    type: 'website',
  },
  // Google Search Console domain verification
  // Reemplazar el valor con el código real desde: Search Console → Add property → HTML tag
  verification: {
    google: process.env.NEXT_PUBLIC_GSC_VERIFICATION ?? '',
  },
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
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
