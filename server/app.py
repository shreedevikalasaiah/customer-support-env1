import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from env import CustomerSupportEnv

app = FastAPI(title="Customer Support OpenEnv", version="1.0.0")
env = CustomerSupportEnv()

class StepRequest(BaseModel):
    action: dict

class ResetRequest(BaseModel):
    task_id: Optional[str] = None

@app.get("/")
def health():
    return {"status": "ok", "env": "customer-support-env"}

@app.post("/reset")
def reset(req: ResetRequest = ResetRequest()):
    return env.reset(task_id=req.task_id)

@app.post("/step")
def step(req: StepRequest):
    try:
        return env.step(req.action)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/state")
def state():
    return env.state()

@app.get("/tasks")
def list_tasks():
    return env.list_tasks()
