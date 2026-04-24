'use client'

import Link from 'next/link'
import { useState } from 'react'
import { useUserStore } from '@/store/userStore'

const NAV_LINKS = [
  { href: '/blog',      label: 'Blog'      },
  { href: '/plataforma', label: 'Plataforma' },
  { href: '/comunidad', label: 'Comunidad' },
  { href: '/precios',   label: 'Precios'   },
]

export default function SiteNav() {
  const [open, setOpen] = useState(false)
  const { userId } = useUserStore()

  if (userId) return null

  return (
    <nav
      className="fixed top-0 left-0 right-0 z-50 font-mono border-b border-[#00FF41]/10"
      style={{ background: 'rgba(2,2,2,0.92)', backdropFilter: 'blur(8px)' }}
    >
      <div className="max-w-7xl mx-auto px-6 md:px-10 h-14 flex items-center justify-between">

        {/* Logo */}
        <Link
          href="/"
          className="text-[#00FF41] text-sm font-bold tracking-[0.4em] uppercase"
          style={{ textShadow: '0 0 8px rgba(0,255,65,0.35)' }}
        >
          DAKIedtech
        </Link>

        {/* Desktop nav */}
        <div className="hidden md:flex items-center gap-8">
          {NAV_LINKS.map(({ href, label }) => (
            <Link
              key={href}
              href={href}
              className="text-[10px] tracking-[0.38em] uppercase text-[#00FF41]/40 hover:text-[#00FF41]/80 transition-colors duration-200"
            >
              {label}
            </Link>
          ))}
        </div>

        {/* Auth */}
        <div className="hidden md:flex items-center gap-3">
          <Link
            href="/login"
            className="text-[10px] tracking-[0.3em] uppercase text-white/30 hover:text-white/60 transition-colors duration-200"
          >
            Ingresar
          </Link>
          <Link
            href="/register"
            className="border border-[#00FF41]/35 text-[10px] tracking-[0.3em] uppercase text-[#00FF41] px-4 py-1.5 transition-all duration-200 hover:border-[#00FF41]/65"
            style={{ background: 'rgba(0,255,65,0.03)' }}
            onMouseEnter={e => { (e.currentTarget as HTMLAnchorElement).style.background = 'rgba(0,255,65,0.07)' }}
            onMouseLeave={e => { (e.currentTarget as HTMLAnchorElement).style.background = 'rgba(0,255,65,0.03)' }}
          >
            Ser Operador
          </Link>
        </div>

        {/* Mobile toggle */}
        <button
          onClick={() => setOpen(o => !o)}
          className="md:hidden text-[#00FF41]/50 hover:text-[#00FF41] transition-colors"
          aria-label="Menú"
        >
          {open ? (
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-5 h-5">
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          ) : (
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5} className="w-5 h-5">
              <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5M3.75 17.25h16.5" />
            </svg>
          )}
        </button>
      </div>

      {/* Mobile menu */}
      {open && (
        <div
          className="md:hidden border-t border-[#00FF41]/10 px-6 py-5 flex flex-col gap-4"
          style={{ background: 'rgba(2,2,2,0.97)' }}
        >
          {NAV_LINKS.map(({ href, label }) => (
            <Link
              key={href}
              href={href}
              onClick={() => setOpen(false)}
              className="text-[11px] tracking-[0.42em] uppercase text-[#00FF41]/50 hover:text-[#00FF41]/85 transition-colors"
            >
              {label}
            </Link>
          ))}
          <div className="border-t border-[#00FF41]/08 pt-4 flex flex-col gap-3">
            <Link
              href="/login"
              onClick={() => setOpen(false)}
              className="text-[11px] tracking-[0.35em] uppercase text-white/35 hover:text-white/65 transition-colors"
            >
              Ingresar
            </Link>
            <Link
              href="/register"
              onClick={() => setOpen(false)}
              className="border border-[#00FF41]/40 text-[11px] tracking-[0.35em] uppercase text-[#00FF41] px-4 py-2 text-center hover:bg-[#00FF41]/07 transition-all"
            >
              Ser Operador
            </Link>
          </div>
        </div>
      )}
    </nav>
  )
}
