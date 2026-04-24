'use client'

interface Props {
  color:    string
  children: React.ReactNode
}

export default function BlogFeaturedCard({ color, children }: Props) {
  return (
    <div
      className="relative border p-6 sm:p-8 overflow-hidden transition-all duration-300"
      style={{ borderColor: `${color}22`, background: `${color}04` }}
      onMouseEnter={e => {
        const el = e.currentTarget as HTMLDivElement
        el.style.borderColor = `${color}50`
        el.style.background  = `${color}07`
      }}
      onMouseLeave={e => {
        const el = e.currentTarget as HTMLDivElement
        el.style.borderColor = `${color}22`
        el.style.background  = `${color}04`
      }}
    >
      <div
        className="absolute top-0 left-0 right-0 h-px"
        style={{ background: `linear-gradient(90deg,transparent,${color}55,transparent)` }}
      />
      {children}
    </div>
  )
}
