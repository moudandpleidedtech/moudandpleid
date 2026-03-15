'use client'

import { useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

interface ToastProps {
  message: string
  visible: boolean
  onClose: () => void
  variant?: 'warning' | 'error' | 'success'
  duration?: number
}

const VARIANTS = {
  warning: { border: '#FFD700', text: '#FFD700', bg: '#0F0D00' },
  error:   { border: '#FF4444', text: '#FF4444', bg: '#0F0000' },
  success: { border: '#00FF41', text: '#00FF41', bg: '#000F03' },
}

export default function Toast({
  message,
  visible,
  onClose,
  variant = 'warning',
  duration = 4000,
}: ToastProps) {
  useEffect(() => {
    if (!visible) return
    const t = setTimeout(onClose, duration)
    return () => clearTimeout(t)
  }, [visible, onClose, duration])

  const c = VARIANTS[variant]

  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          className="fixed bottom-6 left-1/2 -translate-x-1/2 z-[300] font-mono text-xs tracking-[0.2em] px-5 py-3 border whitespace-nowrap cursor-pointer"
          style={{
            borderColor: c.border,
            color: c.text,
            backgroundColor: c.bg,
            boxShadow: `0 0 24px ${c.border}30`,
          }}
          initial={{ opacity: 0, y: 16, scale: 0.96 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: 8, scale: 0.96 }}
          transition={{ duration: 0.18 }}
          onClick={onClose}
        >
          {message}
        </motion.div>
      )}
    </AnimatePresence>
  )
}
