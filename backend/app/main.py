from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .models import CallStatus, OutboundCall, OutboundCallCreate, OutboundCallUpdate
from .store import create_call, get_call, list_calls, retry_call, update_call

app = FastAPI(title="Outbound Call Monitor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5175"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/calls", response_model=list[OutboundCall])
def get_calls() -> list[OutboundCall]:
    return list_calls()


@app.get("/calls/{call_id}", response_model=OutboundCall)
def get_one_call(call_id: int) -> OutboundCall:
    call = get_call(call_id)
    if call is None:
        raise HTTPException(status_code=404, detail="Call not found")
    return call


@app.post("/calls", response_model=OutboundCall, status_code=201)
def post_call(payload: OutboundCallCreate) -> OutboundCall:
    return create_call(payload)


@app.patch("/calls/{call_id}", response_model=OutboundCall)
def patch_call(call_id: int, payload: OutboundCallUpdate) -> OutboundCall:
    call = update_call(call_id, payload)
    if call is None:
        raise HTTPException(status_code=404, detail="Call not found")
    return call


@app.post("/calls/{call_id}/retry", response_model=OutboundCall)
def retry(call_id: int) -> OutboundCall:
    call = get_call(call_id)
    if call is None:
        raise HTTPException(status_code=404, detail="Call not found")
    if call.status != CallStatus.failed:
        raise HTTPException(status_code=409, detail="Only failed calls can be retried")
    return retry_call(call_id)
