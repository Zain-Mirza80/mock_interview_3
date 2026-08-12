import type { CallStatus, OutboundCall } from '../types'
import { StatusBadge } from './StatusBadge'

interface CallCardProps {
  call: OutboundCall
  onStatusChange: (id: number, status: CallStatus) => void
  onRetry: (id: number) => void
}

export function CallCard({ call, onStatusChange, onRetry }: CallCardProps) {
  return (
    <article className="card">
      <div className="card-header">
        <div>
          <h2>{call.patient_label}</h2>
          <p className="muted">{call.reason}</p>
        </div>
        <StatusBadge status={call.status} />
      </div>

      <div className="meta-row">
        <span>Scheduled {call.scheduled_for.replace('T', ' ')}</span>
        <span>{call.attempts} attempt{call.attempts === 1 ? '' : 's'}</span>
      </div>

      {call.last_error && <p className="error-note">Last error: {call.last_error}</p>}

      <div className="actions">
        {call.status === 'scheduled' && (
          <button onClick={() => onStatusChange(call.id, 'in_progress')}>Start call</button>
        )}
        {call.status === 'in_progress' && (
          <>
            <button onClick={() => onStatusChange(call.id, 'completed')}>Mark complete</button>
            <button className="secondary" onClick={() => onStatusChange(call.id, 'failed')}>Mark failed</button>
          </>
        )}
        {call.status === 'failed' && (
          <button onClick={() => onRetry(call.id)}>Retry call</button>
        )}
      </div>
    </article>
  )
}
