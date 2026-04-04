import type { Config } from 'tailwindcss'

const config: Config = {
  content: ['./src/**/*.{js,ts,jsx,tsx,mdx}'],
  theme: {
    extend: {
      colors: {
        neon: '#00FF41',
        terminal: '#0A0A0A',
        surface: '#0D0D0D',
        border: '#00FF41',
        // ── Skill Tree — Cyber-Táctica ───────────────
        'nexo-bg':      '#0B1120',
        'neon-cyan':    '#06b6d4',
        'neon-emerald': '#10b981',
        'neon-gold':    '#f59e0b',
      },
      fontFamily: {
        mono: ['"Fira Code"', '"Cascadia Code"', 'Consolas', 'monospace'],
      },
      dropShadow: {
        neon: '0 0 12px #00FF41',
        'neon-lg': '0 0 30px #00FF41',
      },
      boxShadow: {
        // ── Resplandores neón — Skill Tree ───────────
        'glow-cyan':    '0 0 15px rgba(6, 182, 212, 0.6), inset 0 0 10px rgba(6, 182, 212, 0.4)',
        'glow-emerald': '0 0 20px rgba(16, 185, 129, 0.8), inset 0 0 15px rgba(16, 185, 129, 0.5)',
        'glow-gold':    '0 0 15px rgba(245, 158, 11, 0.4), inset 0 0 10px rgba(245, 158, 11, 0.2)',
      },
      animation: {
        'flicker':      'flicker 0.15s infinite',
        'scanline':     'scanline 8s linear infinite',
        // ── Skill Tree ────────────────────────────────
        'energy-pulse': 'energy-pulse 2s ease-in-out infinite',
      },
      keyframes: {
        flicker: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.92' },
        },
        scanline: {
          '0%': { transform: 'translateY(-100%)' },
          '100%': { transform: 'translateY(100vh)' },
        },
        // ── Skill Tree ────────────────────────────────
        'energy-pulse': {
          '0%, 100%': { opacity: '0.8', transform: 'scale(1.0)' },
          '50%':       { opacity: '1.0', transform: 'scale(1.2)' },
        },
      },
    },
  },
  plugins: [],
}

export default config
