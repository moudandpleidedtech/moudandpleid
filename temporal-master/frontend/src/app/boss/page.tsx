'use client'

/**
 * /boss — Página del Boss Fight: TheInfiniteLooper.
 *
 * Requiere que el usuario esté autenticado (user_id en localStorage).
 * Si no hay sesión, redirige a /misiones.
 */

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import dynamic from 'next/dynamic'

// Carga dinámica para evitar SSR (Monaco + framer-motion lo requieren)
const TheInfiniteLooper = dynamic(
  () => import('@/components/Boss/TheInfiniteLooper'),
  { ssr: false, loading: () => <BossLoading /> }
)

function BossLoading() {
  return (
    <div className="min-h-screen bg-black flex items-center justify-center">
      <div className="font-mono text-red-500 tracking-[0.3em] animate-pulse">
        CARGANDO MÓDULO DEL JEFE...
      </div>
    </div>
  )
}

export default function BossPage() {
  const router = useRouter()
  const [userId, setUserId] = useState<string | null>(null)
  const [ready, setReady] = useState(false)

  useEffect(() => {
    const stored = localStorage.getItem('userId')
    if (!stored) {
      router.replace('/misiones')
      return
    }
    setUserId(stored)
    setReady(true)
  }, [router])

  if (!ready || !userId) return <BossLoading />

  return (
    <TheInfiniteLooper
      userId={userId}
      onVictory={(result) => {
        // Actualiza XP total en localStorage para que el header lo refleje
        localStorage.setItem('totalXP', String(result.new_total_xp))
        localStorage.setItem('currentLevel', String(result.new_level))
      }}
      onDefeat={() => {
        // Sin efecto secundario adicional — el componente muestra la pantalla de derrota
      }}
    />
  )
}
