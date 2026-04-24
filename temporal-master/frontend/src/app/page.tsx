import HeroSection        from '@/components/Landing/HeroSection'
import BlogPreviewSection  from '@/components/Landing/BlogPreviewSection'
import SolucionSection     from '@/components/Landing/SolucionSection'
import EbooksSection       from '@/components/Landing/EbooksSection'
import ActivacionSection   from '@/components/Landing/ActivacionSection'
import SiteNav             from '@/components/Landing/SiteNav'
import Footer              from '@/components/Landing/Footer'

export default function LandingPage() {
  return (
    <main className="bg-[#020202]">
      <SiteNav />
      <HeroSection />
      <BlogPreviewSection />
      <SolucionSection />
      <EbooksSection />
      <ActivacionSection />
      <Footer />
    </main>
  )
}
