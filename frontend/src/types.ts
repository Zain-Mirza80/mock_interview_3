export type CallStatus = 'scheduled' | 'in_progress' | 'failed' | 'completed'

export interface OutboundCall {
  id: number
  patient_label: string
  reason: string
  scheduled_for: string
  status: CallStatus
  attempts: number
  last_error: string | null
}

export interface OutboundCallUpdate {
  status?: CallStatus
  scheduled_for?: string
  last_error?: string | null
}
