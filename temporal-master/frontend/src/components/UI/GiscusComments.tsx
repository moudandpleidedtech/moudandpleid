'use client'

import { useEffect, useRef } from 'react'

const REPO      = process.env.NEXT_PUBLIC_GISCUS_REPO      ?? ''
const REPO_ID   = process.env.NEXT_PUBLIC_GISCUS_REPO_ID   ?? ''
const CAT_ID    = process.env.NEXT_PUBLIC_GISCUS_CATEGORY_ID ?? ''

export default function GiscusComments({ term }: { term: string }) {
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!ref.current || !REPO || !REPO_ID || !CAT_ID) return
    if (ref.current.querySelector('iframe')) return

    const script = document.createElement('script')
    script.src               = 'https://giscus.app/client.js'
    script.setAttribute('data-repo',             REPO)
    script.setAttribute('data-repo-id',          REPO_ID)
    script.setAttribute('data-category',         'General')
    script.setAttribute('data-category-id',      CAT_ID)
    script.setAttribute('data-mapping',          'specific')
    script.setAttribute('data-term',             term)
    script.setAttribute('data-strict',           '0')
    script.setAttribute('data-reactions-enabled','1')
    script.setAttribute('data-emit-metadata',    '0')
    script.setAttribute('data-input-position',   'top')
    script.setAttribute('data-theme',            'dark')
    script.setAttribute('data-lang',             'es')
    script.setAttribute('data-loading',          'lazy')
    script.crossOrigin = 'anonymous'
    script.async       = true

    ref.current.appendChild(script)
  }, [term])

  if (!REPO || !REPO_ID || !CAT_ID) return null

  return (
    <div className="mt-12">
      <p className="text-[8px] tracking-[0.55em] text-[#00FF41]/25 uppercase mb-6">
        {'// COMENTARIOS DEL NEXO'}
      </p>
      <div ref={ref} />
    </div>
  )
}
