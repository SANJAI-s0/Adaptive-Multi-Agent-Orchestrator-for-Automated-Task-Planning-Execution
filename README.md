# 🧠 Adaptive Multi-Agent Orchestrator

A lightweight Planner → Executor → Reviewer AI pipeline (FastAPI + Python) — fully local, deterministic, and free (uses a MockLLM).

---

## 📑 Table of Contents

- [Overview](#Overview)
- [🧩 1. Primary Use Case](#-1-primary-use-case)
- [📂 2. Project Structure](#-2-project-structure)
- [🏗️ 3. System Architecture](#️-3-system-architecture)
- [⚙️ 4. Components](#️-4-components)
  - [MockLLM](#mockllm-appllmpy)
  - [Planner](#planner-appagentsplannerpy)
  - [Executor](#executor-appagentsexecutorpy)
  - [Reviewer](#reviewer-appagentsreviewerpy)
  - [Orchestrator](#orchestrator-apporchestratorpy)
  - [FastAPI Backend](#fastapi-backend-appmainpy)
- [📦 5. Requirements](#-5-requirements)
- [🛠️ 6. Installation](#️-6-installation)
- [🚀 7. Running the Project](#-7-running-the-project)
  - [Run the demo](#option-1--run-the-demo-no-api)
  - [Start FastAPI backend](#option-2--start-the-backend-fastapi)
- [8. API Workflow Example](#8-api-workflow-example)
- [📝 9. Example Full Output (Illustrative)](#-9-example-full-output-illustrative)
- [🏆 10. Why This Project Is Valuable](#-10-why-this-project-is-valuable)
- [✔️ 11. Extending the Project](#️-11-extending-the-project)
- [12. Contributing](#12-contributing)
- [13. License](#13-license)

---

## Overview

This repository implements a simple but complete multi-agent architecture where multiple autonomous agents collaborate to solve a user-defined goal. The pipeline includes:

- **Planner Agent** — converts a high-level goal into actionable, ordered steps.
- **Executor Agent** — performs each step and produces intermediate outputs.
- **Reviewer Agent** — evaluates the final result and issues a pass/fail review.
- **Orchestrator** — central coordinator that submits, runs and monitors tasks.
- **FastAPI backend** — exposes task APIs for submission and retrieval.
- **Demo script** — run the full pipeline locally without a frontend or external LLM.

All agents are wired to a `MockLLM` adapter so the whole system runs offline and deterministically with zero API cost.

---

## 🧩 1. Primary Use Case

A user submits a high-level goal, for example:

> "Analyze global water scarcity and propose 5 practical solutions."

The system will:

1. Break the goal into numbered steps (Planner).
2. Execute each step sequentially and record intermediate results (Executor).
3. Review and QA the consolidated result (Reviewer).
4. Return a structured task record including plan, execution outputs, and review.

Typical applications include research assistants, automated planning workflows, educational demonstrations of multi-agent collaboration, and experiments in task decomposition.

---

## 📂 2. Project Structure

```
agents-capstone/
├─ app/
│  ├─ main.py                # FastAPI endpoints
│  ├─ orchestrator.py        # Task management + agent loop
│  ├─ llm.py                 # MockLLM (offline), adapter layer
│  ├─ storage.py             # In-memory task storage
│  ├─ agents/
│  │  ├─ planner.py          # Planner agent
│  │  ├─ executor.py         # Executor agent
│  │  └─ reviewer.py         # Reviewer agent
├─ demo.py                   # CLI demo runner
├─ requirements.txt          # Python dependencies
├─ Dockerfile                # Backend container (optional)
└─ README.md                 # Documentation
```

---

## 🏗️ 3. System Architecture
```
                  ┌──────────────────────────┐
                  │          Client          │
                  │ (curl, frontend, demo.py)│
                  └─────────────┬────────────┘
                          POST /tasks
                                │
                                ▼
                  ┌─────────────────────────┐
                  │       FastAPI API       │
                  │  (app/main.py endpoints)│
                  └─────────────┬───────────┘
                                │
                                ▼
                  ┌─────────────────────────┐
                  │      Orchestrator       │
                  │ (Submit, run, monitor)  │
                  └─────────────┬───────────┘
       ┌────────────────────────┼──────────────────────────┐
       ▼                        ▼                          ▼
┌────────────┐           ┌─────────────┐            ┌─────────────┐
│  Planner   │           │  Executor   │            │  Reviewer   │
│  (steps)   │           │  (per step) │            │  (final QA) │
└────────────┘           └─────────────┘            └─────────────┘
                                ▼  
                        ┌────────────────┐
                        │  Task Storage  │
                        │ (in-memory)    │
                        └────────────────┘
```

---

## ⚙️ 4. Components

### MockLLM (`app/llm.py`)
A lightweight simulated LLM that returns predictable outputs. It avoids external API calls so tests are reproducible and free.

### Planner (`app/agents/planner.py`)
Parses the high-level goal and emits a clear, numbered list of instructions. Output is parsed into an ordered JSON list suitable for the Orchestrator to consume.

### Executor (`app/agents/executor.py`)
Processes each instruction, simulates working on the step (using `MockLLM`) and produces deterministic reasoning text which becomes part of the task's execution log.

### Reviewer (`app/agents/reviewer.py`)
Inspects the entire execution bundle, drafts a final review summary, and returns a boolean pass/fail along with comments.

### Orchestrator (`app/orchestrator.py`)
Manages task lifecycle: submission, execution, status updates, and result storage. Typical lifecycle statuses: `queued` → `executing` → `reviewing` → `done`.

### FastAPI Backend (`app/main.py`)
Exposes the following endpoints:

- `POST /tasks` — submit a new task with a `goal` JSON field.
- `GET /tasks/{task_id}` — retrieve task status & results.
- `GET /health` — basic health check.

Example POST body:

```json
{ "goal": "Analyze global water scarcity" }
```

Example POST response:

```json
{ "task_id": "abcd-1234", "status": "queued" }
```

---

## 📦 5. Requirements

- Python 3.11.x (Suggestion: 3.11.9 is a stable version for this project)

Packages `requirements.txt`:

```
fastapi==0.95.2
uvicorn==0.22.0
pydantic==1.10.11
python-multipart==0.0.6
numpy==1.26.4
scikit-learn==1.4.2
aiohttp==3.9.5
faiss-cpu==1.7.4  # optional
```

---

## 🛠️ 6. Installation

```bash
git clone https://github.com/SANJAI-s0/Adaptive-Multi-Agent-Orchestrator-for-Automated-Task-Planning-Execution.git
cd Adaptive-Multi-Agent-Orchestrator-for-Automated-Task-Planning-Execution
python -m venv .venv
source .venv/bin/activate #Linux,IOS
.venv\Scripts\Activate.ps1 # Windows PowerShell
pip install -r requirements.txt
```

---

## 🚀 7. Running the Project

### Option 1 — Run the demo (no API)

```bash
python demo.py
```

This will run the Planner → Executor → Reviewer loop locally and print structured, readable output to the console.

### Option 2 — Start the backend (FastAPI)

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open the interactive docs at: `http://127.0.0.1:8000/docs`

---

## 8. API Workflow Example

1. **Submit a Task**

```bash
curl -X POST "http://127.0.0.1:8000/tasks" \
     -H "Content-Type: application/json" \
     -d '{"goal":"Analyze global water scarcity"}'
```

Response:

```json
{"task_id":"abcd-1234","status":"queued"}
```

2. **Poll for Status**

```bash
curl "http://127.0.0.1:8000/tasks/abcd-1234"
```

---

## 📝 9. Example Full Output (Illustrative)

**Plan**

1. Research background and collect sources.
2. Extract key facts and statistics.
3. Analyze drivers and craft recommendations.
4. Produce final report with citations.

**Execution**

- Step 1: fetched sources
- Step 2: calculated trend
- Step 3: analyzed drivers
- Step 4: produced final report

**Review**

- Drafted a 600-word summary and a list of 5 proposed interventions.
- `passed`: `true`

---

## 🏆 10. Why This Project Is Valuable

- Demonstrates multi-agent collaboration and task decomposition.
- Shows chained reasoning in a reproducible, deterministic environment (no API costs).
- Clean architecture suitable for extension (real LLM adapters, persistent storage, UI).
- Good fit for educational demos and Kaggle Freestyle-style projects.

---

## ✔️ 11. Extending the Project

Ideas for improvements:

- Replace `MockLLM` with a real LLM adapter (OpenAI, Anthropic, etc.) for non-deterministic, high-quality outputs.
- Add persistent storage (database) instead of in-memory task storage.
- Add asynchronous/concurrent execution for independent steps.
- Add authentication and authorization for the API.
- Build a simple frontend to visualize plan, execution logs, and review results.

---

## 12. Contributing

Contributions are welcome. Suggested workflow:

1. Fork the repo
2. Create a feature branch
3. Open a pull request with clear description and tests/examples

---

## 13. License

MIT License

Copyright (c) 2025 SANJAI S

---
