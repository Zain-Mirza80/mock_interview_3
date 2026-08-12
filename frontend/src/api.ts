import type { OutboundCall, OutboundCallUpdate } from './types'

const API_BASE = 'http://localhost:8000'

export async function fetchCalls(): Promise<OutboundCall[]> {
  const response = await fetch(`${API_BASE}/calls`)
  if (!response.ok) {
    throw new Error('Could not load calls')
  }
  return response.json()
}

export async function updateCall(id: number, update: OutboundCallUpdate): Promise<OutboundCall> {
  const response = await fetch(`${API_BASE}/calls/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(update),
  })

  if (!response.ok) {
    throw new Error('Could not update call')
  }

  return response.json()
}
