'use client'

/**
 * VideoDemoSection — Demo del Nexo en video · fit en 1 pantalla
 */

import { useRef, useState } from 'react'
import { motion } from 'framer-motion'

export default function VideoDemoSection() {
  const videoRef = useRef<HTMLVideoElement>(null)
  const [playing, setPlaying] = useState(false)
  const [showControls, setShowControls] = useState(false)

  const togglePlay = () => {
    if (!videoRef.current) return
    playing ? videoRef.current.pause() : videoRef.current.play()
    setPlaying(!playing)
  }

  return (
    <section className="relative bg-[#060606] font-mono overflow-hidden min-h-screen flex flex-col justify-center py-6 px-4">

      <div
        className="absolute inset-0 pointer-events-none z-0 opacity-[0.025]"
        style={{ backgroundImage: 'repeating-linear-gradient(0deg,transparent,transparent 3px,#00FF41 3px,#00FF41 4px)' }}
      />

      <div className="relative z-10 max-w-4xl mx-auto w-full">

        {/* Header compacto */}
        <motion.div
          className="text-center mb-4"
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.45 }}
        >
          <div className="text-[8px] tracking-[0.6em] text-[#00FF41]/28 uppercase mb-2">
            {'// TRANSMISIÓN EN VIVO DEL NEXO'}
          </div>
          <h2 className="text-xl sm:text-2xl font-black tracking-[0.1em] uppercase text-white">
            REPRODUCIR DEMO DEL{' '}
            <span className="text-[#00FF41]" style={{ textShadow: '0 0 20px rgba(0,255,65,0.5)' }}>
              NEXO
            </span>
          </h2>
        </motion.div>

        {/* Video */}
        <motion.div
          className="relative"
          initial={{ opacity: 0, scale: 0.98 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          onMouseEnter={() => setShowControls(true)}
          onMouseLeave={() => setShowControls(false)}
        >
          <div
            className="relative border-2 overflow-hidden"
            style={{
              borderColor: '#1a2a1a',
              boxShadow: '0 0 0 1px rgba(0,255,65,0.08), 0 0 40px rgba(0,255,65,0.06)',
            }}
          >
            <Corner pos="top-0 left-0" />
            <Corner pos="top-0 right-0" rotate />
            <Corner pos="bottom-0 left-0" flipY />
            <Corner pos="bottom-0 right-0" rotate flipY />

            <div className="flex items-center justify-between px-3 py-1.5 border-b" style={{ background: 'rgba(0,0,0,0.9)', borderColor: 'rgba(0,255,65,0.12)' }}>
              <div className="flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-[#00FF41] animate-pulse" />
                <span className="text-[7px] tracking-[0.5em] text-[#00FF41]/45 uppercase">NEXO · DAKI EDTECH</span>
              </div>
              <div className="flex items-center gap-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-[#FF0033]/40" />
                <span className="w-1.5 h-1.5 rounded-full bg-[#FFB800]/30" />
                <span className="w-1.5 h-1.5 rounded-full bg-[#00FF41]/20" />
              </div>
            </div>

            <div className="relative bg-black aspect-video cursor-pointer" onClick={togglePlay}>
              <video ref={videoRef} src="/assets/demo.mp4" className="w-full h-full object-cover" playsInline onEnded={() => setPlaying(false)} preload="metadata" />
              <div className="absolute inset-0 pointer-events-none" style={{ backgroundImage: 'repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,0.07) 2px,rgba(0,0,0,0.07) 4px)' }} />
              <div className="absolute inset-0 pointer-events-none" style={{ background: 'radial-gradient(ellipse at center, transparent 55%, rgba(0,0,0,0.7) 100%)' }} />

              {(!playing || showControls) && (
                <div className="absolute inset-0 flex items-center justify-center">
                  <motion.div
                    className="flex items-center justify-center w-16 h-16 border-2 rounded-full"
                    style={{ borderColor: playing ? 'rgba(0,255,65,0.4)' : '#00FF41', background: 'rgba(0,0,0,0.6)', boxShadow: playing ? '0 0 20px rgba(0,255,65,0.15)' : '0 0 40px rgba(0,255,65,0.4)' }}
                    whileHover={{ scale: 1.08 }} whileTap={{ scale: 0.95 }}
                  >
                    {playing ? (
                      <div className="flex gap-1"><div className="w-2 h-6 bg-[#00FF41]" /><div className="w-2 h-6 bg-[#00FF41]" /></div>
                    ) : (
                      <div className="ml-1" style={{ width:0, height:0, borderTop:'11px solid transparent', borderBottom:'11px solid transparent', borderLeft:'18px solid #00FF41' }} />
                    )}
                  </motion.div>
                </div>
              )}
              {!playing && (
                <div className="absolute bottom-4 left-0 right-0 text-center">
                  <span className="text-[8px] tracking-[0.5em] text-[#00FF41]/45 uppercase">CLICK PARA REPRODUCIR</span>
                </div>
              )}
            </div>

            <div className="flex items-center justify-between px-3 py-1.5 border-t" style={{ background: 'rgba(0,0,0,0.9)', borderColor: 'rgba(0,255,65,0.08)' }}>
              <span className="text-[7px] text-[#00FF41]/22 tracking-widest">DAKI.IA // TRANSMISIÓN SEGURA</span>
              <span className="text-[7px] text-[#00FF41]/22 tracking-widest">{playing ? '● EN VIVO' : '○ EN PAUSA'}</span>
            </div>
          </div>
        </motion.div>

        {/* Grilla D·A·K·I — compacta */}
        <motion.div
          className="grid grid-cols-4 gap-2 mt-3"
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.25 }}
        >
          {[
            { key: 'D', label: 'DESARROLLO REAL',      sub: 'Caos de producción',          color: '#00FF41' },
            { key: 'A', label: 'ARQUITECTURA ÉLITE',   sub: 'Infraestructura blindada',     color: '#00FF41' },
            { key: 'K', label: 'CONOCIMIENTO TÁCTICO', sub: 'Lógica, no memorización',      color: '#FFB800' },
            { key: 'I', label: 'INTELIGENCIA NEURONAL',sub: 'IA analiza tu código en vivo', color: '#FFB800' },
          ].map(({ key, label, sub, color }) => (
            <div key={key} className="border px-3 py-2" style={{ borderColor: `${color}15`, background: 'rgba(0,0,0,0.4)' }}>
              <div className="flex items-center gap-1.5 mb-0.5">
                <span className="font-black text-xs" style={{ color }}>{key} —</span>
                <span className="text-[9px] font-bold tracking-wider text-white/70 truncate">{label}</span>
              </div>
              <p className="text-[7px] tracking-widest uppercase truncate" style={{ color: `${color}35` }}>{sub}</p>
            </div>
          ))}
        </motion.div>

      </div>
    </section>
  )
}

function Corner({ pos, rotate, flipY }: { pos: string; rotate?: boolean; flipY?: boolean }) {
  return (
    <div className={`absolute ${pos} w-5 h-5 z-10 pointer-events-none`} style={{ transform: `${rotate ? 'scaleX(-1)' : ''} ${flipY ? 'scaleY(-1)' : ''}` }}>
      <div className="absolute top-0 left-0 w-full h-px bg-[#00FF41]/35" />
      <div className="absolute top-0 left-0 w-px h-full bg-[#00FF41]/35" />
    </div>
  )
}
