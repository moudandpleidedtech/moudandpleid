'use client'

import { useEffect, useState } from 'react'

type HealthResult = {
  status: string
  db_connected: boolean
} | null

export default function HealthCheckPage() {
  const [result, setResult] = useState<HealthResult>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? ''

    fetch(`${apiUrl}/api/v1/health`)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        return res.json()
      })
      .then((data: HealthResult) => setResult(data))
      .catch((err: Error) => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  return (
    <main style={{ fontFamily: 'monospace', padding: '2rem', background: '#0d0d0d', minHeight: '100vh', color: '#00FF41' }}>
      <h1>End-to-End Health Check</h1>
      <p>Target: <code>{process.env.NEXT_PUBLIC_API_URL ?? ''}/api/v1/health</code></p>
      <hr style={{ borderColor: '#00FF4130', margin: '1rem 0' }} />

      {loading && <p>⏳ Connecting...</p>}

      {error && (
        <div style={{ color: '#ff4444', background: '#1a0000', padding: '1rem', borderRadius: '4px' }}>
          <strong>❌ Error:</strong> {error}
          <p style={{ marginTop: '0.5rem', fontSize: '0.85rem', color: '#ff9999' }}>
            Possible causes: API not running, CORS blocked, wrong NEXT_PUBLIC_API_URL
          </p>
        </div>
      )}

      {result && (
        <div style={{ background: '#001a00', padding: '1rem', borderRadius: '4px' }}>
          <p>API Status: <strong style={{ color: result.status === 'ok' ? '#00FF41' : '#ff4444' }}>{result.status === 'ok' ? '✅ OK' : '❌ ' + result.status}</strong></p>
          <p>DB Connected: <strong style={{ color: result.db_connected ? '#00FF41' : '#ff4444' }}>{result.db_connected ? '✅ true' : '❌ false'}</strong></p>
          <pre style={{ marginTop: '1rem', color: '#ffffff80' }}>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </main>
  )
}
