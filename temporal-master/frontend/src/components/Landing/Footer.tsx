import Link from 'next/link'

export default function Footer() {
  return (
    <footer className="bg-[#0A0A0A] font-mono border-t border-white/[0.05] px-6 md:px-12 py-10">
      <div className="max-w-6xl mx-auto">

        {/* Fila principal */}
        <div className="flex flex-col md:flex-row items-center md:items-start justify-between gap-8 mb-8">

          {/* Brand */}
          <div>
            <p
              className="text-[#00FF41] text-sm font-bold tracking-[0.4em] uppercase mb-2"
              style={{ textShadow: '0 0 8px rgba(0,255,65,0.4)' }}
            >
              DAKIedtech
            </p>
            <p className="text-[#00FF41]/20 text-[10px] tracking-[0.25em] max-w-[220px] leading-5">
              Aprende Python como un Operador. Código real, sin teoría muerta.
            </p>
          </div>

          {/* Links */}
          <div className="flex flex-wrap justify-center md:justify-end gap-x-8 gap-y-3">
            {[
              { label: 'Iniciar sesión',  href: '/login'      },
              { label: 'Crear cuenta',   href: '/register'   },
              { label: 'Privacidad',     href: '/privacidad' },
              { label: 'Términos',       href: '/terminos'   },
            ].map(({ label, href }) => (
              <Link
                key={href}
                href={href}
                className="text-[#00FF41]/20 text-[10px] tracking-[0.3em] uppercase hover:text-[#00FF41]/55 transition-colors duration-200"
              >
                {label}
              </Link>
            ))}
          </div>

        </div>

        {/* Divisor */}
        <div className="h-px bg-gradient-to-r from-transparent via-[#00FF41]/08 to-transparent mb-6" />

        {/* Fila inferior */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-3">
          <p className="text-[#00FF41]/15 text-[10px] tracking-[0.3em]">
            © 2026 DAKIedtech · Todos los sistemas operativos.
          </p>
          <a
            href="mailto:systemsupport@dakiedtech.com"
            className="text-[#00FF41]/20 text-[10px] tracking-[0.25em] hover:text-[#00FF41]/50 transition-colors duration-200"
          >
            systemsupport@dakiedtech.com
          </a>
        </div>

      </div>
    </footer>
  )
}
