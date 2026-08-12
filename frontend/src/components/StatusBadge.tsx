import type { CallStatus } from '../types'

export function StatusBadge({ status }: { status: CallStatus }) {
  return <span className={`badge badge-${status}`}>{status.replace('_', ' ')}</span>
}
