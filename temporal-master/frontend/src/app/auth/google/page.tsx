'use client'

/**
 * /auth/google — Página puente post-OAuth Google
 *
 * El backend no puede setear cookies en dakiedtech.com (dominio diferente),
 * así que redirige aquí con el JWT en la URL:
 *   GET /auth/google?token=<jwt>&new=0|1
 *
 * Esta página:
 *   1. Lee el token de los query params
 *   2. Decodifica el payload JWT (base64, sin verificar — viene de HTTPS + dominio propio)
 *   3. Persiste datos en localStorage + Zustand
 *   4. Setea cookie enigma_user para el middleware de Next.js
 *   5. Redirige a /hub, /boot-sequence u /onboarding según corresponda
 */

import { useEffect } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { useUserStore } from '@/store/userStore'

export default function GoogleAuthCallback() {
  const router    = useRouter()
  const params    = useSearchParams()
  const { setUser } = useUserStore()

  useEffect(() => {
    const token  = params.get('token')
    const isNew  = params.get('new') === '1'

    if (!token) {
      router.replace('/login?google_error=missing_token')
      return
    }

    try {
      // Decodificar payload JWT (base64url → JSON)
      const payloadB64 = token.split('.')[1]
      const payload = JSON.parse(atob(payloadB64.replace(/-/g, '+').replace(/_/g, '/')))
      // payload: { sub, callsign, level, is_licensed, role, exp }

      // Persistir en localStorage (mismo esquema que login normal)
      localStorage.setItem('daki_user_id',  payload.sub)
      localStorage.setItem('daki_callsign', payload.callsign)
      localStorage.setItem('daki_level',    String(payload.level))
      localStorage.setItem('daki_licensed', String(payload.is_licensed))
      localStorage.setItem('daki_token',    token)

      // Actualizar Zustand store
      setUser({
        id:            payload.sub,
        username:      payload.callsign,
        current_level: payload.level,
        total_xp:      0,
        streak_days:   0,
        is_paid:       payload.is_licensed,
        role:          payload.role ?? 'USER',
      })

      // Cookie para el middleware de Next.js (protección de rutas)
      document.cookie = 'enigma_user=1; path=/; max-age=604800; SameSite=Lax'

      // Decidir destino
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

  return (
    <div className="min-h-screen bg-[#0A0A0A] font-mono text-[#00FF41] flex items-center justify-center">
      <div className="text-center space-y-2">
        <p className="text-xs tracking-[0.4em] animate-pulse">&gt; AUTENTICANDO CON GOOGLE...</p>
        <p className="text-[10px] tracking-[0.3em] text-[#00FF41]/30">&gt; ESTABLECIENDO SESIÓN DE OPERADOR</p>
      </div>
    </div>
  )
}
