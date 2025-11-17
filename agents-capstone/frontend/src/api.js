// minimal API helper; set API_URL to your backend
export const API_URL = (import.meta.env.VITE_API_URL || "http://127.0.0.1:8000").replace(/\/$/, "")

export async function createTask(goal) {
  const res = await fetch(`${API_URL}/tasks`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ goal })
  })
  if (!res.ok) throw new Error(`Create task failed: ${res.status}`)
  return res.json()
}

export async function getTask(taskId) {
  const res = await fetch(`${API_URL}/tasks/${taskId}`)
  if (!res.ok) throw new Error(`Get task failed: ${res.status}`)
  return res.json()
}

