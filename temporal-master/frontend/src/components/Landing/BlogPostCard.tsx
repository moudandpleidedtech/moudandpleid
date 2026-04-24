'use client'

interface Props {
  color:    string
  children: React.ReactNode
}

export default function BlogPostCard({ color, children }: Props) {
  return (
    <div
      className="border p-5 transition-all duration-250"
      style={{ borderColor: 'rgba(0,255,65,0.10)', background: 'rgba(0,0,0,0.3)' }}
      onMouseEnter={e => {
        const el = e.currentTarget as HTMLDivElement
        el.style.borderColor = `${color}35`
        el.style.background  = `${color}04`
      }}
      onMouseLeave={e => {
        const el = e.currentTarget as HTMLDivElement
        el.style.borderColor = 'rgba(0,255,65,0.10)'
        el.style.background  = 'rgba(0,0,0,0.3)'
      }}
    >
      {children}
    </div>
  )
}
