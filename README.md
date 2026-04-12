---
title: Customer Support Env
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: mit
---

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

## Environment Variables
| Variable | Description |
|----------|-------------|
| API_BASE_URL | LLM API base URL |
| MODEL_NAME | Model identifier |
| HF_TOKEN | Hugging Face API key |

## Run
```bash
uv sync
uv run uvicorn server.app:app --host 0.0.0.0 --port 7860
```
