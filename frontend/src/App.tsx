import { useEffect, useState } from 'react'
import { fetchCalls, updateCall } from './api'
import { CallCard } from './components/CallCard'
import type { CallStatus, OutboundCall } from './types'
import './styles.css'

export default function App() {
  const [calls, setCalls] = useState<OutboundCall[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchCalls()
      .then(setCalls)
      .catch((err) => setError(err instanceof Error ? err.message : 'Something went wrong'))
      .finally(() => setLoading(false))
  }, [])

  async function handleStatusChange(id: number, status: CallStatus) {
    const updated = await updateCall(id, { status })
    setCalls((current) => current.map((call) => (call.id === id ? updated : call)))
  }

  if (loading) {
    return <main className="page"><p>Loading outbound calls…</p></main>
  }

  if (error) {
    return <main className="page"><p className="error">{error}</p></main>
  }

  const activeCalls = calls.filter((call) => call.status !== 'completed')
  const failedCalls = calls.filter((call) => call.status === 'failed')

  return (
    <main className="page">
      <header className="page-header">
        <div>
          <p className="eyebrow">Clinical operations</p>
          <h1>Outbound call monitor</h1>
          <p className="muted">Monitor scheduled patient outreach and call outcomes.</p>
        </div>
        <div className="summary">
          <strong>{activeCalls.length}</strong><span>active</span>
          <strong>{failedCalls.length}</strong><span>failed</span>
        </div>
      </header>

      <section className="grid">
        {calls.map((call) => (
          <CallCard key={call.id} call={call} onStatusChange={handleStatusChange} />
        ))}
      </section>
    </main>
  )
}
