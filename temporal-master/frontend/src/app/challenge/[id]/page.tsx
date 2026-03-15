import CodeWorkspace from '@/components/IDE/CodeWorkspace'

interface Props {
  params: { id: string }
}

export default function ChallengePage({ params }: Props) {
  return <CodeWorkspace challengeId={params.id} />
}
