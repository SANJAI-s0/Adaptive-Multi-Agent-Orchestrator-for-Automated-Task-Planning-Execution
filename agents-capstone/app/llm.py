from typing import Dict, Any, Optional
import time
import random
import asyncio

class BaseLLM:
    async def generate(self, prompt: str, max_tokens: int = 256) -> str:
        raise NotImplementedError

class MockLLM(BaseLLM):
    """
    Lightweight mock LLM for local testing. Produces structured outputs,
    so Planner/Executor/Reviewer can operate even without real API keys.
    """
    async def generate(self, prompt: str, max_tokens: int = 256) -> str:
        # simulate latency
        await asyncio.sleep(0.1)

        prompt_low = prompt.lower()
        if "plan" in prompt_low or "break" in prompt_low or "steps" in prompt_low:
            return (
                "1) Research background and collect sources. "
                "2) Extract key facts and statistics. "
                "3) Analyze drivers and craft recommendations. "
                "4) Produce final report with citations."
            )
        if "execute step" in prompt_low or "fetch" in prompt_low or "analyze" in prompt_low:
            # Return a short 'execution' result
            outputs = [
                "Fetched 3 authoritative sources: un_water.org, who.int, worldbank.org.",
                "Calculated trend: water scarcity increasing in arid regions; key drivers: climate change, inefficient irrigation.",
                "Drafted a 600-word summary and a list of 5 proposed interventions."
            ]
            return random.choice(outputs)
        if "review" in prompt_low or "validate" in prompt_low:
            return "Checked outputs: Sources valid; minor factual mismatch on 'year' — corrected. Recommend adding regional case studies and quant metrics."
        # default
        return "Acknowledged. (MockLLM fallback response.)"

# Helper to choose LLM instance; swap easily to real API wrappers
def get_llm(use_mock: bool = True) -> BaseLLM:
    if use_mock:
        return MockLLM()
    # Example placeholder: replace with real LLM class that implements `.generate()`
    # from app.real_openai_adapter import OpenAIAdapter
    # return OpenAIAdapter(api_key=os.environ.get("OPENAI_API_KEY"))
    raise RuntimeError("No LLM configured. Set use_mock=True or implement a real adapter.")
