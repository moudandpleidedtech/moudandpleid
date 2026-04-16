'use client'

import { Suspense, useEffect } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { useUserStore } from '@/store/userStore'

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? ''

function GoogleAuthHandler() {
  const router      = useRouter()
  const params      = useSearchParams()
  const { setUser } = useUserStore()

  useEffect(() => {
    // El token NO viaja en la URL — está en la cookie httpOnly seteada por el backend.
    // Llamamos a /auth/me con credentials:'include' para obtener el perfil del operador.
    const isNew = params.get('new') === '1'

    fetch(`${API_BASE}/api/v1/auth/me`, { credentials: 'include' })
      .then(res => {
        if (!res.ok) throw new Error('auth_failed')
        return res.json() as Promise<{
          user_id: string; callsign: string; level: number
          is_licensed: boolean; role: string
        }>
      })
      .then(profile => {
        // Guardamos perfil (sin token) en localStorage solo para display
        localStorage.setItem('daki_user_id',  profile.user_id)
        localStorage.setItem('daki_callsign', profile.callsign)
        localStorage.setItem('daki_level',    String(profile.level))
        localStorage.setItem('daki_licensed', String(profile.is_licensed))
        // NO guardamos daki_token — la autenticación usa la cookie httpOnly

        setUser({
          id:            profile.user_id,
          username:      profile.callsign,
          current_level: profile.level,
          total_xp:      0,
          streak_days:   0,
          is_paid:       profile.is_licensed,
          role:          profile.role ?? 'USER',
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
      })
      .catch(() => {
        router.replace('/login?google_error=auth_failed')
      })
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
