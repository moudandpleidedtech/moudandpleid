import type { Metadata } from 'next'
import './globals.css'
import TopNav from '@/components/UI/TopNav'

export const metadata: Metadata = {
  title: 'Moud & Pleind — Python Quest',
  description: 'Plataforma de retos de programación con gamificación',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <body className="crt">
        <TopNav />
        {children}
      </body>
    </html>
  )
}
