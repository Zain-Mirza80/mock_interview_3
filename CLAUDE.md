# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Outbound Call Monitor: a small full-stack app for monitoring scheduled patient outreach calls. FastAPI backend + React/TypeScript frontend, with an in-memory data store (no database).

## Commands

### Backend (`backend/`)

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload   # serves http://localhost:8000
```

Run tests:
```bash
cd backend
pytest                          # all tests
pytest tests/test_calls.py::test_patch_call_status   # single test
```

### Frontend (`frontend/`)

```bash
cd frontend
npm install
npm run dev     # serves http://localhost:5173
npm run build   # tsc typecheck + vite build
npm test        # vitest run
```

There is no lint script configured in either package.

## Architecture

- **Backend** (`backend/app/`): FastAPI app with three files:
  - `main.py` — route handlers only (`/health`, `/calls`, `/calls/{id}`).
  - `models.py` — Pydantic models: `OutboundCallCreate` (POST body), `OutboundCallUpdate` (PATCH body, all fields optional), `OutboundCall` (full record, response model). `CallStatus` enum: `scheduled` → `in_progress` → `failed`/`completed`.
  - `store.py` — in-memory `dict[int, OutboundCall]` acting as the persistence layer, seeded with 4 sample calls at import time. State resets on every process restart; `update_call` uses `model_copy(update=...)` with `exclude_unset=True` so PATCH only overwrites fields explicitly sent.

- **Frontend** (`frontend/src/`): flat structure, no router or state library.
  - `App.tsx` — owns all state (`calls`, `loading`, `error`) via `useState`/`useEffect`, fetches calls on mount, derives `activeCalls`/`failedCalls` counts inline.
  - `api.ts` — thin fetch wrapper; `API_BASE` is hardcoded to `http://localhost:8000` (not env-configurable).
  - `types.ts` — TS types mirroring the backend Pydantic models exactly; keep these in sync manually when backend models change.
  - `components/CallCard.tsx` — renders one call, exposes status-transition buttons (`Start call`, `Mark complete`, `Mark failed`) that call back up to `App.handleStatusChange`, which PATCHes and merges the response into local state.
  - `components/StatusBadge.tsx` — pure status-to-badge-class mapping.

- **Call status flow**: `scheduled` → (Start call) → `in_progress` → (Mark complete / Mark failed) → `completed` / `failed`. Enforced only in the UI (`CallCard` conditionally renders buttons); the backend accepts any status transition via PATCH.

- CORS on the backend is locked to `http://localhost:5173` (see `main.py`), so if the frontend dev port changes, update `allow_origins` too.
