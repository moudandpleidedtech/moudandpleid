'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useUserStore } from '@/store/userStore'
import NeuralBoot from '@/components/UI/NeuralBoot'
import MobileGate from '@/components/UI/MobileGate'

export default function BootSequencePage() {
  const router = useRouter()
  const { _hasHydrated, userId, username, dakiLevel } = useUserStore()

  // Guard: sin sesión → login
  useEffect(() => {
    if (!_hasHydrated) return
    if (!userId) router.replace('/login')
  }, [_hasHydrated, userId, router])

  const handleComplete = () => {
    localStorage.setItem('boot_seen', '1')
    router.push('/hub')
  }

  if (!_hasHydrated || !userId) return null

  return (
    <MobileGate>
      <NeuralBoot
        username={username}
        dakiLevel={dakiLevel}
        onComplete={handleComplete}
      />
    </MobileGate>
  )
}
