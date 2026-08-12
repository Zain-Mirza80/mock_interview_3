from .models import CallStatus, OutboundCall, OutboundCallCreate, OutboundCallUpdate

_calls: dict[int, OutboundCall] = {
    1: OutboundCall(
        id=1,
        patient_label="Patient Alpha",
        reason="Medication tolerance check",
        scheduled_for="2026-08-12T10:30",
        status="scheduled",
        attempts=1,
    ),
    2: OutboundCall(
        id=2,
        patient_label="Patient Beta",
        reason="Post-discharge symptom review",
        scheduled_for="2026-08-12T09:15",
        status="failed",
        attempts=1,
        last_error="Telephony provider timeout",
    ),
    3: OutboundCall(
        id=3,
        patient_label="Patient Gamma",
        reason="Confirm follow-up appointment",
        scheduled_for="2026-08-12T11:00",
        status="in_progress",
        attempts=1,
    ),
    4: OutboundCall(
        id=4,
        patient_label="Patient Delta",
        reason="Review home blood pressure readings",
        scheduled_for="2026-08-11T16:00",
        status="completed",
        attempts=2,
    ),
}
_next_id = 5


def list_calls() -> list[OutboundCall]:
    return list(_calls.values())


def get_call(call_id: int) -> OutboundCall | None:
    return _calls.get(call_id)


def create_call(data: OutboundCallCreate) -> OutboundCall:
    global _next_id
    call = OutboundCall(id=_next_id, **data.model_dump())
    _calls[_next_id] = call
    _next_id += 1
    return call


def update_call(call_id: int, data: OutboundCallUpdate) -> OutboundCall | None:
    existing = _calls.get(call_id)
    if existing is None:
        return None

    updated = existing.model_copy(update=data.model_dump(exclude_unset=True))
    _calls[call_id] = updated
    return updated


def retry_call(call_id: int) -> OutboundCall | None:
    existing = _calls.get(call_id)
    if existing is None:
        return None

    updated = existing.model_copy(update={
        "status": CallStatus.scheduled,
        "attempts": existing.attempts + 1,
        "last_error": None,
    })
    _calls[call_id] = updated
    return updated
