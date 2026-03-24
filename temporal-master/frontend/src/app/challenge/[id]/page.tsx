import CodeWorkspace from '@/components/IDE/CodeWorkspace'
import MobileGate from '@/components/UI/MobileGate'

interface Props {
  params: { id: string }
}

export default function ChallengePage({ params }: Props) {
  return (
    <MobileGate>
      <CodeWorkspace challengeId={params.id} />
    </MobileGate>
  )
}
