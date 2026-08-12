import { render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { CallCard } from './CallCard'

const failedCall = {
  id: 2,
  patient_label: 'Patient Beta',
  reason: 'Post-discharge symptom review',
  scheduled_for: '2026-08-12T09:15',
  status: 'failed' as const,
  attempts: 1,
  last_error: 'Telephony provider timeout',
}

describe('CallCard', () => {
  it('shows failed call details', () => {
    render(<CallCard call={failedCall} onStatusChange={vi.fn()} onRetry={vi.fn()} />)

    expect(screen.getByText('Patient Beta')).toBeTruthy()
    expect(screen.getByText(/Telephony provider timeout/)).toBeTruthy()
    expect(screen.getByText('1 attempt')).toBeTruthy()
  })
})
