# app/orchestrator.py
from typing import Dict, Any
from app.llm import get_llm
from app.agents.planner import PlannerAgent
from app.agents.executor import ExecutorAgent
from app.agents.reviewer import ReviewerAgent
from app.storage import InMemoryMemory, VectorStore
import asyncio
import uuid

class Orchestrator:
    def __init__(self, use_mock: bool = True):
        self.llm = get_llm(use_mock=use_mock)
        self.memory = InMemoryMemory()
        self.vstore = VectorStore(dim=128)
        self.planner = PlannerAgent(self.llm)
        self.executor = ExecutorAgent(self.llm, self.memory)
        self.reviewer = ReviewerAgent(self.llm)
        self.tasks = {}  # simple in-memory task registry

    async def submit_task(self, goal: str) -> str:
        task_id = str(uuid.uuid4())
        self.tasks[task_id] = {"status": "queued", "goal": goal, "result": None}
        # start in background
        asyncio.create_task(self._run_task(task_id, goal))
        return task_id

    async def _run_task(self, task_id: str, goal: str):
        self.tasks[task_id]["status"] = "planning"
        steps = await self.planner.plan(goal, context=self.memory.recent(5))
        self.tasks[task_id]["plan"] = steps

        self.tasks[task_id]["status"] = "executing"
        exec_results = await self.executor.execute_plan(steps)
        self.tasks[task_id]["execution"] = exec_results

        self.tasks[task_id]["status"] = "reviewing"
        review = await self.reviewer.review(exec_results)
        self.tasks[task_id]["review"] = review

        self.tasks[task_id]["status"] = "done"
        self.tasks[task_id]["result"] = {
            "plan": steps,
            "execution": exec_results,
            "review": review
        }

    def get_task(self, task_id: str):
        return self.tasks.get(task_id)
