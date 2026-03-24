'use client'

import { use } from 'react'
import SectorMap from '@/components/Game/SectorMap'
import MobileGate from '@/components/UI/MobileGate'

export default function SectorPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params)
  const sectorId = parseInt(id, 10)

  if (isNaN(sectorId) || sectorId < 1) {
    return (
      <div
        className="min-h-screen flex items-center justify-center"
        style={{ background: '#0A0A0A', fontFamily: 'monospace', color: '#FF2D78' }}
      >
        [ ERROR: SECTOR_ID INVÁLIDO ]
      </div>
    )
  }

  return (
    <MobileGate>
      <SectorMap sectorId={sectorId} challengeBasePath="/challenge" />
    </MobileGate>
  )
}
