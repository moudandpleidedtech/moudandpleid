'use client'

import Link from 'next/link'
import { usePathname, useRouter } from 'next/navigation'
import { motion } from 'framer-motion'
import { useUserStore } from '@/store/userStore'

// Páginas donde el nav NO aparece (login + boot + hub)
// El /hub tiene su propio contexto de navegación DAKI — la TopNav duplicaría la UI
const HIDE_ON = new Set(['/', '/boot-sequence', '/hub'])

function getTitleForLevel(level: number): string {
  if (level <= 2) return 'ESTUDIANTE'
  if (level <= 4) return 'CÓDIGO JOVEN'
  if (level <= 7) return 'ARQUITECTO'
  if (level <= 11) return 'MAESTRO'
  return 'LEYENDA ENIGMA'
}

export default function TopNav() {
  const pathname = usePathname()
  const router = useRouter()
  const { userId, username, level, clearUser } = useUserStore()

  const handleLogout = () => {
    clearUser()
    document.cookie = 'enigma_user=; path=/; max-age=0; SameSite=Lax'
    router.push('/')
  }

  const isVisible = !HIDE_ON.has(pathname) && !!userId

  if (!isVisible) return null

  return (
    <>
    {/* Espaciador en el flujo del DOM: empuja el contenido 32px hacia abajo */}
    <div className="h-8" aria-hidden="true" />
    <motion.nav
      className="fixed top-0 left-0 right-0 z-[100] h-8 flex items-center justify-between px-4 font-mono bg-[#080808]/96 border-b border-[#00FF41]/15 backdrop-blur-sm"
      initial={{ y: -32, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.3, ease: 'easeOut' }}
    >
      {/* Logo */}
      <Link href="/misiones" className="flex items-center gap-2.5 group select-none">
        <span
          className="text-[#00FF41] font-black text-xs tracking-[0.25em] transition-all duration-150"
          style={{ textShadow: '0 0 6px #00FF4155' }}
        >
          M&P
        </span>
        <span className="hidden sm:inline text-[#00FF41]/25 text-[10px] tracking-[0.3em]">
          PYTHON QUEST
        </span>
      </Link>

      {/* Player info + botón de pánico */}
      <div className="flex items-center gap-4 text-[10px] tracking-widest">
        <span className="text-[#00FF41]/30 hidden md:inline">{username}</span>
        <span className="text-[#00FF41]/55 hidden sm:inline">{getTitleForLevel(level)}</span>
        <span
          className="text-[#00FF41] font-bold"
          style={{ textShadow: '0 0 6px #00FF4180' }}
        >
          NVL {level}
        </span>
        {/* Botón de pánico — siempre visible, a la derecha del NVL */}
        <button
          onClick={handleLogout}
          className="ml-4 text-red-500 hover:text-red-400 hover:bg-red-950/30 border border-red-800 px-3 py-1 text-xs font-mono tracking-widest cursor-pointer transition-all"
        >
          [ ABORTAR CONEXIÓN ]
        </button>
      </div>

      {/* Accesos rápidos */}
      <div className="flex items-center gap-2">
        <Link
          href="/bounty"
          className="text-[10px] tracking-[0.18em] text-[#FFD700]/45 hover:text-[#FFD700] border border-[#FFD700]/15 hover:border-[#FFD700]/55 px-2.5 py-0.5 transition-all duration-150 hidden lg:inline-flex"
        >
          BOUNTY
        </Link>
        <Link
          href="/arena"
          className="text-[10px] tracking-[0.18em] text-[#FF0040]/45 hover:text-[#FF0040] border border-[#FF0040]/15 hover:border-[#FF0040]/55 px-2.5 py-0.5 transition-all duration-150 hidden lg:inline-flex"
        >
          ARENA
        </Link>
        <Link
          href="/leaderboard"
          className="text-[10px] tracking-[0.18em] text-[#7DF9FF]/45 hover:text-[#7DF9FF] border border-[#7DF9FF]/15 hover:border-[#7DF9FF]/55 px-2.5 py-0.5 transition-all duration-150 hidden lg:inline-flex"
        >
          RANKING
        </Link>
        <Link
          href="/codice"
          className="text-[10px] tracking-[0.18em] text-[#FFD700]/45 hover:text-[#FFD700] border border-[#FFD700]/15 hover:border-[#FFD700]/55 px-2.5 py-0.5 transition-all duration-150 hidden lg:inline-flex"
        >
          CÓDICE
        </Link>
        <Link
          href="/hub"
          className="text-[10px] tracking-[0.18em] text-[#00FF41]/45 hover:text-[#00FF41] border border-[#00FF41]/15 hover:border-[#00FF41]/55 px-2.5 py-0.5 transition-all duration-150 hidden sm:inline-flex"
        >
          CENTRO DE MANDO
        </Link>
      </div>
    </motion.nav>
    </>
  )
}
