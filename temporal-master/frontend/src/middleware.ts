import { NextRequest, NextResponse } from 'next/server'

/**
 * Protección de rutas:
 * - /        → Si autenticado, redirige a /hub
 * - /login   → Si autenticado, redirige a /hub
 * - /register → Si autenticado, redirige a /hub
 * - Rutas privadas sin cookie → redirige a /login
 */

const PRIVATE_ROUTES = ['/hub', '/misiones', '/challenge', '/enigma', '/boss', '/leaderboard', '/arena', '/codice']

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl
  const isAuthenticated = request.cookies.has('enigma_user')

  // Usuario autenticado intenta acceder a rutas públicas → Centro de Mando
  if ((pathname === '/' || pathname === '/login' || pathname === '/register') && isAuthenticated) {
    return NextResponse.redirect(new URL('/hub', request.url))
  }

  // Ruta privada sin sesión → login
  const isPrivate = PRIVATE_ROUTES.some(r => pathname === r || pathname.startsWith(r + '/'))
  if (isPrivate && !isAuthenticated) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: [
    '/',
    '/login',
    '/register',
    '/hub',
    '/misiones',
    '/challenge/:path*',
    '/enigma',
    '/boss',
    '/leaderboard',
    '/arena',
    '/codice',
  ],
}
