---
title: Customer Support Env
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: mit
app_port: 7860
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
