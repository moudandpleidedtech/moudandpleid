'use client'

/**
 * AffiliateTracker — captura el parámetro ?ref= de la URL y lo guarda
 * en la cookie daki_ref (30 días). Cuando el usuario llega al paywall,
 * PaywallModal lee esa cookie y la envía al backend como src= en la URL
 * de Hotmart, acreditando la comisión al afiliado correctamente.
 *
 * No renderiza nada visible. Se monta en el layout raíz.
 */

import { useEffect } from 'react'
import { useSearchParams } from 'next/navigation'

export default function AffiliateTracker() {
  const searchParams = useSearchParams()

  useEffect(() => {
    const ref = searchParams.get('ref')
    if (!ref) return
    const expires = new Date()
    expires.setDate(expires.getDate() + 30)
    document.cookie = `daki_ref=${encodeURIComponent(ref)};expires=${expires.toUTCString()};path=/;SameSite=Lax`
  }, [searchParams])

  return null
}
