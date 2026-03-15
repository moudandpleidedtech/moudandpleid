import { NextRequest, NextResponse } from 'next/server'

/**
 * Protección de rutas:
 * - Si el usuario tiene cookie `enigma_user` e intenta ir a `/` (login), redirige a /misiones
 */
export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl
  const isAuthenticated = request.cookies.has('enigma_user')

  // Usuario autenticado intenta acceder al login → Centro de Mando
  if (pathname === '/' && isAuthenticated) {
    return NextResponse.redirect(new URL('/misiones', request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/'],
}
