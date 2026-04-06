'use client'

import { Suspense, useEffect } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { useUserStore } from '@/store/userStore'

function GoogleAuthHandler() {
  const router      = useRouter()
  const params      = useSearchParams()
  const { setUser } = useUserStore()

  useEffect(() => {
    const token = params.get('token')
    const isNew = params.get('new') === '1'

    if (!token) {
      router.replace('/login?google_error=missing_token')
      return
    }

    try {
      const payloadB64 = token.split('.')[1]
      const payload = JSON.parse(atob(payloadB64.replace(/-/g, '+').replace(/_/g, '/')))

      localStorage.setItem('daki_user_id',  payload.sub)
      localStorage.setItem('daki_callsign', payload.callsign)
      localStorage.setItem('daki_level',    String(payload.level))
      localStorage.setItem('daki_licensed', String(payload.is_licensed))
      localStorage.setItem('daki_token',    token)

      setUser({
        id:            payload.sub,
        username:      payload.callsign,
        current_level: payload.level,
        total_xp:      0,
        streak_days:   0,
        is_paid:       payload.is_licensed,
        role:          payload.role ?? 'USER',
      })

      document.cookie = 'enigma_user=1; path=/; max-age=604800; SameSite=Lax'

      const onboardingDone = localStorage.getItem('onboarding_done') === 'true'
      const bootSeen       = !!localStorage.getItem('boot_seen')

      let destination: string
      if (isNew) {
        destination = !onboardingDone ? '/onboarding' : bootSeen ? '/hub' : '/boot-sequence'
      } else {
        destination = bootSeen ? '/hub' : '/boot-sequence'
      }

      router.replace(destination)
    } catch {
      router.replace('/login?google_error=invalid_token')
    }
  }, []) // eslint-disable-line react-hooks/exhaustive-deps

  return null
}

export default function GoogleAuthCallback() {
  return (
    <div className="min-h-screen bg-[#0A0A0A] font-mono text-[#00FF41] flex items-center justify-center">
      <div className="text-center space-y-2">
        <p className="text-xs tracking-[0.4em] animate-pulse">&gt; AUTENTICANDO CON GOOGLE...</p>
        <p className="text-[10px] tracking-[0.3em] text-[#00FF41]/30">&gt; ESTABLECIENDO SESIÓN DE OPERADOR</p>
      </div>
      <Suspense>
        <GoogleAuthHandler />
      </Suspense>
    </div>
  )
}
