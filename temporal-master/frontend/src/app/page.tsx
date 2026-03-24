import HeroSection           from '@/components/Landing/HeroSection'
import SocialProofSection    from '@/components/Landing/SocialProofSection'
import ProblemSection        from '@/components/Landing/ProblemSection'
import ManifestoSection      from '@/components/Landing/ManifestoSection'
import NeuralDemoSection     from '@/components/Landing/NeuralDemoSection'
import MissionsSection       from '@/components/Landing/MissionsSection'
import FounderLicenseSection from '@/components/Landing/FounderLicenseSection'
import TestimonialsSection   from '@/components/Landing/TestimonialsSection'
import BetaProtocolSection   from '@/components/Landing/BetaProtocolSection'
import Footer                from '@/components/Landing/Footer'
import CircuitBoard          from '@/components/UI/CircuitBoard'
import ElectricDivider       from '@/components/UI/ElectricDivider'

/**
 * DAKI EdTech — Landing Page
 *
 * Funnel de conversión:
 *   Hero → Credibilidad → Problema → Solución → Demo → Operaciones →
 *   Distinción de Protocolo → Prueba Social → CTA Final
 */
export default function LandingPage() {
  return (
    <main>
      {/* Circuito eléctrico global — persiste en toda la página */}
      <CircuitBoard />

      {/* 1. EL PORTAL — Impacto inmediato, identidad */}
      <HeroSection />

      <ElectricDivider />

      {/* 2. CREDIBILIDAD RÁPIDA — Python Misión 01, stats */}
      <SocialProofSection />

      <ElectricDivider />

      {/* 3. EL PROBLEMA — Activa el dolor, valida la frustración */}
      <ProblemSection />

      <ElectricDivider />

      {/* 4. LA SOLUCIÓN — Anatomía del Nexo DAKI */}
      <ManifestoSection />

      <ElectricDivider />

      {/* 5. INTERFAZ NEURAL — Muestra antes de registrar */}
      <NeuralDemoSection />

      <ElectricDivider />

      {/* 6. ZONAS DE OPERACIÓN — Python Misión 01 activa */}
      <MissionsSection />

      <ElectricDivider />

      {/* 7. DISTINCIÓN DE PROTOCOLO — El paywall que convierte */}
      <FounderLicenseSection />

      <ElectricDivider />

      {/* 8. SEÑALES DEL CAMPO — Prueba social táctica */}
      <TestimonialsSection />

      {/* 9. PROTOCOLO DE ACCESO — Dicotomía final, sin ruido */}
      <BetaProtocolSection />

      <Footer />
    </main>
  )
}
