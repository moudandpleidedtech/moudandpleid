import HeroSection         from '@/components/Landing/HeroSection'
import SocialProofSection  from '@/components/Landing/SocialProofSection'
import ManifestoSection    from '@/components/Landing/ManifestoSection'
import MissionsSection     from '@/components/Landing/MissionsSection'
import BetaProtocolSection from '@/components/Landing/BetaProtocolSection'
import Footer              from '@/components/Landing/Footer'
import CircuitBoard        from '@/components/UI/CircuitBoard'
import ElectricDivider     from '@/components/UI/ElectricDivider'

export default function LandingPage() {
  return (
    <main>
      {/* Overlay de circuito eléctrico — persiste en todas las secciones */}
      <CircuitBoard />

      <HeroSection />
      <ElectricDivider />
      <SocialProofSection />
      <ElectricDivider />
      <ManifestoSection />
      <ElectricDivider />
      <MissionsSection />
      <ElectricDivider />
      <BetaProtocolSection />
      <Footer />
    </main>
  )
}
