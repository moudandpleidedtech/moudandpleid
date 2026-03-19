'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useUserStore } from '@/store/userStore'
import NeuralBoot from '@/components/UI/NeuralBoot'

export default function BootSequencePage() {
  const router = useRouter()
  const { userId, username, dakiLevel } = useUserStore()

  // Guard: sin sesión → login
  useEffect(() => {
    if (!userId) router.replace('/')
  }, [userId, router])

  const handleComplete = () => {
    localStorage.setItem('boot_seen', '1')
    // Navega a misiones: el Nivel 01 ("Hola Mundo") es el primero de la lista
    router.push('/misiones')
  }

  if (!userId) return null

  return (
    <NeuralBoot
      username={username}
      dakiLevel={dakiLevel}
      onComplete={handleComplete}
    />
  )
}
