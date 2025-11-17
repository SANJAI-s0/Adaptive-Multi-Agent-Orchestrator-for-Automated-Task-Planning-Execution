from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.orchestrator import Orchestrator

# Create app
app = FastAPI(title="Adaptive Multi-Agent Orchestrator")

# CORS - allow the frontend dev server and localhost for convenience.
# For local dev it's OK to be permissive; tighten the origins for production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000", "http://127.0.0.1:3000", "http://localhost", "http://127.0.0.1", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = Orchestrator(use_mock=True)

class TaskRequest(BaseModel):
    goal: str

@app.post("/tasks")
async def create_task(req: TaskRequest):
    """
    Submit a new task (JSON body: {"goal": "..."})
    Returns: {"task_id": "...", "status": "queued"}
    """
    task_id = await orchestrator.submit_task(req.goal)
    return {"task_id": task_id, "status": "queued"}

@app.get("/tasks/{task_id}")
async def get_task(task_id: str):
    """
    Retrieve task status and results.
    """
    task = orchestrator.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.get("/health")
async def health():
    return {"status": "ok"}
