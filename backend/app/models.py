from enum import Enum
from pydantic import BaseModel, Field


class CallStatus(str, Enum):
    scheduled = "scheduled"
    in_progress = "in_progress"
    failed = "failed"
    completed = "completed"


class OutboundCallBase(BaseModel):
    patient_label: str = Field(min_length=1, max_length=100)
    reason: str = Field(min_length=1, max_length=240)
    scheduled_for: str = Field(min_length=16, max_length=16)


class OutboundCallCreate(OutboundCallBase):
    pass


class OutboundCallUpdate(BaseModel):
    status: CallStatus | None = None
    scheduled_for: str | None = Field(default=None, min_length=16, max_length=16)
    last_error: str | None = Field(default=None, max_length=240)


class OutboundCall(OutboundCallBase):
    id: int
    status: CallStatus = CallStatus.scheduled
    attempts: int = Field(default=1, ge=1)
    last_error: str | None = None
