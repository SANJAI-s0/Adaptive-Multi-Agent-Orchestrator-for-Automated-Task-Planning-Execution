import re
from typing import List, Dict, Any
from app.llm import BaseLLM

class PlannerAgent:
    def __init__(self, llm: BaseLLM):
        self.llm = llm

    async def plan(self, goal: str, context: List[Dict[str,Any]] = None) -> List[Dict[str,str]]:
        prompt = f"Plan steps to solve the goal:\\nGoal: {goal}\\nContext: {context}\\nProvide numbered steps."
        raw = await self.llm.generate(prompt)

        # Normalize whitespace
        raw = (raw or "").strip()

        # Split by numbered bullets like "1)", "2." etc.
        parts = re.split(r'\s*\d+[\)\.]\s*', raw)

        steps = []
        for part in parts:
            part = part.strip()
            if not part:
                continue
            # Remove trailing standalone digits (e.g., "collect sources. 2")
            part = re.sub(r'\s*\d+$', '', part).strip()
            if not part:
                continue
            steps.append({"instruction": part})
        
        # If nothing parsed (fallback), return the whole raw string as single instruction
        if not steps and raw:
            steps = [{"instruction": raw}]
        return steps
