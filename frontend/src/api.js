const API_BASE = "/api";

async function parseJson(response) {
  const text = await response.text();

  try {
    return JSON.parse(text);
  } catch {
    throw new Error(`Invalid JSON response: ${text}`);
  }
}

export async function getBackendHealth() {
  const response = await fetch(`${API_BASE}/health`);
  if (!response.ok) {
    throw new Error(`Health request failed: ${response.status}`);
  }
  return parseJson(response);
}

export async function getOllamaHealth() {
  const response = await fetch(`${API_BASE}/ollama/health`);
  if (!response.ok) {
    throw new Error(`Ollama health request failed: ${response.status}`);
  }
  return parseJson(response);
}

export async function listTasks() {
  const response = await fetch(`${API_BASE}/tasks`);
  if (!response.ok) {
    throw new Error(`List tasks failed: ${response.status}`);
  }
  return parseJson(response);
}

export async function createTask(payload) {
  const response = await fetch(`${API_BASE}/tasks`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  const data = await parseJson(response);

  if (!response.ok) {
    throw new Error(data.detail || `Create task failed: ${response.status}`);
  }

  return data;
}