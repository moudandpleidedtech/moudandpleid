import type { Config } from 'tailwindcss'

const config: Config = {
  content: ['./src/**/*.{js,ts,jsx,tsx,mdx}'],
  theme: {
    extend: {
      colors: {
        // ── Legacy (no romper componentes existentes) ──────────────
        neon:     '#00FF41',
        terminal: '#0A0A0A',
        surface:  '#0D0D0D',
        border:   '#00FF41',

        // ── Nexo-V4 — Paleta Táctica Blindada ─────────────────────
        'nexo-deep-bg':        '#020617',   // negro casi absoluto — max contraste
        'nexo-bg':             '#0B1120',   // mantiene compatibilidad con SkillTree
        'nexo-text-primary':   '#F0F9FF',   // blanco azulado muy tenue
        'nexo-tactical-green': '#4ade80',   // verde radar — estado operativo

        // ── Neón nuclear — Skill Tree & UI activa ─────────────────
        'neon-cyan':    '#06b6d4',
        'neon-emerald': '#10b981',
        'neon-gold':    '#f59e0b',

        // Alias prefijados (acceso por token largo)
        'nexo-neon-cyan':    '#06b6d4',
        'nexo-neon-emerald': '#10b981',
        'nexo-neon-gold':    '#f59e0b',
      },

      fontFamily: {
        mono: ['"Fira Code"', '"Cascadia Code"', 'Consolas', 'monospace'],
      },

      dropShadow: {
        neon:    '0 0 12px #00FF41',
        'neon-lg': '0 0 30px #00FF41',
        cyan:    '0 0 8px rgba(6,182,212,0.85)',
        emerald: '0 0 8px rgba(16,185,129,0.85)',
      },

      boxShadow: {
        // ── Resplandores neón — nodos Skill Tree ──────────────────
        'glow-cyan':    '0 0 18px rgba(6,182,212,1),   0 0 40px rgba(6,182,212,0.55), inset 0 0 18px rgba(6,182,212,0.55)',
        'glow-emerald': '0 0 22px rgba(16,185,129,1),  0 0 50px rgba(16,185,129,0.60), inset 0 0 22px rgba(16,185,129,0.60)',
        'glow-gold':    '0 0 18px rgba(245,158,11,0.70), 0 0 36px rgba(245,158,11,0.30), inset 0 0 14px rgba(245,158,11,0.30)',

        // ── Nexo-V4 — Borde táctico con profundidad cian ──────────
        // Uso: className="shadow-neon-border"
        'neon-border':        '0 0 0 1px rgba(6,182,212,0.40), 0 0 10px rgba(6,182,212,0.25)',
        'neon-border-active': '0 0 0 1px rgba(6,182,212,0.75), 0 0 18px rgba(6,182,212,0.45), 0 0 36px rgba(6,182,212,0.15)',
        'neon-border-emerald': '0 0 0 1px rgba(16,185,129,0.45), 0 0 12px rgba(16,185,129,0.28)',
        'neon-border-gold':    '0 0 0 1px rgba(245,158,11,0.40), 0 0 10px rgba(245,158,11,0.22)',
      },

      animation: {
        'flicker':        'flicker 0.15s infinite',
        'scanline':       'scanline 8s linear infinite',
        // ── Skill Tree ─────────────────────────────────────────────
        'energy-pulse':   'energy-pulse 2s ease-in-out infinite',
        // ── Nexo-V4 — Latido neón lento (3s) ──────────────────────
        'neon-pulse':     'neonPulse 3s ease-in-out infinite',
        'neon-pulse-gold':'neonPulseGold 3s ease-in-out infinite',
      },

      keyframes: {
        flicker: {
          '0%, 100%': { opacity: '1' },
          '50%':       { opacity: '0.92' },
        },
        scanline: {
          '0%':   { transform: 'translateY(-100%)' },
          '100%': { transform: 'translateY(100vh)' },
        },
        // ── Skill Tree ─────────────────────────────────────────────
        'energy-pulse': {
          '0%, 100%': { opacity: '0.8', transform: 'scale(1.0)' },
          '50%':       { opacity: '1.0', transform: 'scale(1.2)' },
        },
        // ── Nexo-V4 — neonPulse: latido lento cyan/emerald ────────
        // Interpola: opacity + box-shadow exterior + fondo activo
        neonPulse: {
          '0%, 100%': {
            opacity: '0.70',
            'box-shadow': '0 0 6px rgba(6,182,212,0.25), 0 0 14px rgba(6,182,212,0.12), inset 0 0 8px rgba(6,182,212,0.06)',
            'background-color': 'rgba(6,182,212,0.04)',
          },
          '50%': {
            opacity: '1.0',
            'box-shadow': '0 0 22px rgba(6,182,212,0.85), 0 0 44px rgba(6,182,212,0.40), inset 0 0 20px rgba(6,182,212,0.18)',
            'background-color': 'rgba(6,182,212,0.10)',
          },
        },
        // ── Variante gold para contenedores de aviso/bloqueo ──────
        neonPulseGold: {
          '0%, 100%': {
            opacity: '0.70',
            'box-shadow': '0 0 6px rgba(245,158,11,0.25), 0 0 14px rgba(245,158,11,0.12), inset 0 0 8px rgba(245,158,11,0.06)',
            'background-color': 'rgba(245,158,11,0.04)',
          },
          '50%': {
            opacity: '1.0',
            'box-shadow': '0 0 20px rgba(245,158,11,0.75), 0 0 40px rgba(245,158,11,0.35), inset 0 0 18px rgba(245,158,11,0.14)',
            'background-color': 'rgba(245,158,11,0.09)',
          },
        },
      },
    },
  },
  plugins: [],
}

export default config
