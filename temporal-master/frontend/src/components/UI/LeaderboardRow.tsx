'use client'

interface Props {
  tierColor: string
  isTop3:    boolean
  children:  React.ReactNode
  style?:    React.CSSProperties
  className?: string
}

export default function LeaderboardRow({ tierColor, isTop3, children, style, className }: Props) {
  const base = isTop3 ? `${tierColor}06` : 'transparent'
  return (
    <div
      className={className}
      style={{ ...style, background: base }}
      onMouseEnter={e => { (e.currentTarget as HTMLDivElement).style.background = 'rgba(0,255,65,0.04)' }}
      onMouseLeave={e => { (e.currentTarget as HTMLDivElement).style.background = base }}
    >
      {children}
    </div>
  )
}
