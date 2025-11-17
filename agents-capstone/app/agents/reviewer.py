# app/agents/reviewer.py
from typing import List, Dict, Any
from app.llm import BaseLLM

class ReviewerAgent:
    def __init__(self, llm: BaseLLM):
        self.llm = llm

    async def review(self, execution_results: List[Dict[str,Any]]) -> Dict[str,Any]:
        prompt = f"Review these execution results and suggest corrections or improvements:\n{execution_results}"
        review_text = await self.llm.generate(prompt)
        # simple heuristic: return textual review and boolean pass/fail
        passed = "error" not in review_text.lower()
        return {"passed": passed, "review": review_text}
