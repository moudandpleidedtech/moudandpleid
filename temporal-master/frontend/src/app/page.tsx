import HeroSection        from '@/components/Landing/HeroSection'
import VideoDemoSection   from '@/components/Landing/VideoDemoSection'
import SolucionSection    from '@/components/Landing/SolucionSection'
import ActivacionSection  from '@/components/Landing/ActivacionSection'
import CircuitBoard       from '@/components/UI/CircuitBoard'
import LandingSlider      from '@/components/Landing/LandingSlider'
import HubAudio           from '@/components/UI/HubAudio'
import type { Slide }     from '@/components/Landing/LandingSlider'

const SLIDES: Slide[] = [
  { name: 'NEXO CENTRAL',   content: <HeroSection /> },
  { name: 'DEMO EN VIVO',   content: <VideoDemoSection /> },
  { name: 'EL SISTEMA',     content: <SolucionSection /> },
  { name: 'ACCESO AL NEXO', content: <ActivacionSection /> },
]

export default function LandingPage() {
  return (
    <main
      className="relative"
      style={{
        backgroundImage:      'url(/assets/daki-bg.jpg)',
        backgroundAttachment: 'fixed',
        backgroundSize:       'cover',
        backgroundPosition:   'center',
      }}
    >
      <div
        className="fixed inset-0 pointer-events-none z-0"
        style={{ background: 'rgba(4,6,4,0.88)' }}
      />
      <HubAudio buttonClass="fixed top-3 right-4" />
      <CircuitBoard />
      <LandingSlider slides={SLIDES} />
    </main>
  )
}
