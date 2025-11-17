import React, { useState, useEffect, useRef } from "react"
import { createTask, getTask } from "./api"

export default function App() {
  const [goal, setGoal] = useState("Analyze global water scarcity and propose 5 practical solutions for policymakers.")
  const [taskId, setTaskId] = useState("")
  const [task, setTask] = useState(null)
  const [status, setStatus] = useState("")
  const [error, setError] = useState("")
  const pollingRef = useRef(null)

  useEffect(() => {
    return () => {
      if (pollingRef.current) clearInterval(pollingRef.current)
    }
  }, [])

  async function handleSubmit(e) {
    e?.preventDefault()
    setError("")
    setTask(null)
    setStatus("creating")
    try {
      const data = await createTask(goal)
      setTaskId(data.task_id)
      setStatus(data.status || "queued")
      // start polling
      startPolling(data.task_id)
    } catch (err) {
      setError(err.message)
      setStatus("error")
    }
  }

  function startPolling(id) {
    if (pollingRef.current) clearInterval(pollingRef.current)
    pollingRef.current = setInterval(async () => {
      try {
        const t = await getTask(id)
        setTask(t)
        setStatus(t.status)
        if (t.status === "done") {
          clearInterval(pollingRef.current)
          pollingRef.current = null
        }
      } catch (err) {
        setError(err.message)
        clearInterval(pollingRef.current)
        pollingRef.current = null
      }
    }, 1000)
  }

  async function handleFetchOnce() {
    setError("")
    if (!taskId) { setError("No task id"); return }
    try {
      const t = await getTask(taskId)
      setTask(t)
      setStatus(t.status)
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div className="container">
      <header>
        <h1>Agents Capstone — Controller</h1>
        <p className="muted">Submit a goal, watch the Planner → Executor → Reviewer pipeline.</p>
      </header>

      <section className="card">
        <form onSubmit={handleSubmit}>
          <label>Goal</label>
          <textarea value={goal} onChange={(e) => setGoal(e.target.value)} rows={4} />
          <div className="row">
            <button type="submit" className="primary">Submit Task</button>
            <input placeholder="Or paste task id" value={taskId} onChange={(e)=>setTaskId(e.target.value)} />
            <button type="button" onClick={handleFetchOnce}>Fetch</button>
            <button type="button" onClick={() => { navigator.clipboard?.writeText(taskId) }}>Copy ID</button>
          </div>
          <div className="row small">
            <span>Status: <strong>{status || "idle"}</strong></span>
            {error && <span className="error">Error: {error}</span>}
          </div>
        </form>
      </section>

      <section className="card">
        <h2>Task Result</h2>
        {!task && <p className="muted">No result yet. Submit a task to see the plan, execution and review.</p>}
        {task && (
          <div>
            <h3>Goal</h3>
            <pre className="box">{task.goal}</pre>

            <h3>Plan</h3>
            <ol>
              {task.plan?.map((s, i) => <li key={i}><pre className="inline">{s.instruction}</pre></li>)}
            </ol>

            <h3>Execution</h3>
            <div className="grid">
              {task.execution?.map((ex, i) => (
                <div key={i} className="trace">
                  <div className="trace-head">Step {i+1}</div>
                  <div className="trace-instr">{ex.instruction}</div>
                  <div className="trace-res">{ex.result}</div>
                </div>
              ))}
            </div>

            <h3>Review</h3>
            <pre className="box">{task.review?.review}</pre>
            <div className="row small muted">Passed: {String(task.review?.passed)}</div>
          </div>
        )}
      </section>

      <footer className="muted">Frontend: Vite + React • Backend: FastAPI</footer>
    </div>
  )
}

