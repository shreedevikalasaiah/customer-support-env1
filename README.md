# Customer Support OpenEnv
An RL environment for customer support tasks.

## Tasks
- classify_ticket (easy)
- draft_response (medium)
- resolve_escalation (hard)

## API
- POST /reset
- POST /step
- GET /state
- GET /tasks

## Run
```bash
uv sync
uv run uvicorn server.app:app --host 0.0.0.0 --port 7860
```
