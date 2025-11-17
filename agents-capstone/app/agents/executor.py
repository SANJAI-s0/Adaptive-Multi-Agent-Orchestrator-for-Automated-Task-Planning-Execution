# app/agents/executor.py
from typing import Dict, Any, List
from app.llm import BaseLLM
from app.storage import InMemoryMemory
import asyncio

class ExecutorAgent:
    def __init__(self, llm: BaseLLM, memory: InMemoryMemory):
        self.llm = llm
        self.memory = memory

    async def execute_step(self, step: Dict[str,str]) -> Dict[str,Any]:
        instruction = step.get("instruction","")
        prompt = f"Execute step: {instruction}\nMemory: {self.memory.recent(5)}\nReturn an execution result summary."
        result = await self.llm.generate(prompt)
        # Save to memory
        self.memory.add(role="executor", content=result)
        # create a simple structured return
        return {"instruction": instruction, "result": result}
    
    async def execute_plan(self, steps: List[Dict[str,str]]):
        results = []
        for i, step in enumerate(steps):
            try:
                res = await self.execute_step(step)
            except Exception as e:
                res = {"instruction": step.get("instruction",""), "result": f"ERROR: {str(e)}"}
            results.append(res)
            # small pause to simulate processing
            await asyncio.sleep(0.05)
        return results
