# demo.py
import asyncio
from app.orchestrator import Orchestrator
import time
import json

async def main():
    orch = Orchestrator(use_mock=True)
    goal = "Analyze global water scarcity and propose 5 practical solutions for policymakers."
    print("Submitting task:", goal)
    task_id = await orch.submit_task(goal)
    print("Task ID:", task_id)
    # poll until done (since we used asyncio.create_task inside orchestrator)
    for _ in range(50):
        task = orch.get_task(task_id)
        print("Status:", task["status"])
        if task["status"] == "done":
            print("Final result:")
            print(json.dumps(task["result"], indent=2))
            break
        await asyncio.sleep(0.2)
    else:
        print("Timed out waiting for task to complete.")
    
if __name__ == "__main__":
    asyncio.run(main())
