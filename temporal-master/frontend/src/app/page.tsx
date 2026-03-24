import HeroSection from '@/components/Landing/HeroSection'
import SocialProofSection from '@/components/Landing/SocialProofSection'
import ManifestoSection from '@/components/Landing/ManifestoSection'
import MissionsSection from '@/components/Landing/MissionsSection'
import BetaProtocolSection from '@/components/Landing/BetaProtocolSection'
import Footer from '@/components/Landing/Footer'

export default function LandingPage() {
  return (
    <main>
      <HeroSection />
      <SocialProofSection />
      <ManifestoSection />
      <MissionsSection />
      <BetaProtocolSection />
      <Footer />
    </main>
  )
}
