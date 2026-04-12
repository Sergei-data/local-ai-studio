import { useEffect, useState } from "react";
import {
  createTask,
  getBackendHealth,
  getOllamaHealth,
  listTasks,
} from "./api";

const initialForm = {
  title: "",
  prompt: "",
  allowed_files: "",
  task_type: "generate",
};

function toAllowedFiles(value) {
  return value
    .split("\n")
    .map((item) => item.trim())
    .filter(Boolean);
}

export default function App() {
  const [backendHealth, setBackendHealth] = useState(null);
  const [ollamaHealth, setOllamaHealth] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [loadingTasks, setLoadingTasks] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [form, setForm] = useState(initialForm);

  async function loadHealth() {
    try {
      const [backend, ollama] = await Promise.all([
        getBackendHealth(),
        getOllamaHealth(),
      ]);
      setBackendHealth(backend);
      setOllamaHealth(ollama);
    } catch (err) {
      setError(String(err));
    }
  }

  async function loadTasks() {
    setLoadingTasks(true);
    try {
      const data = await listTasks();
      setTasks(data);
    } catch (err) {
      setError(String(err));
    } finally {
      setLoadingTasks(false);
    }
  }

  useEffect(() => {
    loadHealth();
    loadTasks();
  }, []);

  function updateField(field, value) {
    setForm((prev) => ({
      ...prev,
      [field]: value,
    }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setSubmitting(true);

    try {
      await createTask({
        title: form.title,
        prompt: form.prompt,
        allowed_files: toAllowedFiles(form.allowed_files),
        task_type: form.task_type,
      });

      setForm(initialForm);
      await loadTasks();
    } catch (err) {
      setError(String(err));
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div
      style={{
        fontFamily: "Inter, Arial, sans-serif",
        padding: 24,
        maxWidth: 1200,
        margin: "0 auto",
      }}
    >
      <h1>Local AI Studio</h1>
      <p>Локальная студия для генерации кода, тестов и оркестрации задач.</p>

      {error ? (
        <div
          style={{
            background: "#fee2e2",
            color: "#991b1b",
            padding: 12,
            borderRadius: 8,
            marginBottom: 16,
          }}
        >
          {error}
        </div>
      ) : null}

      <section style={{ marginBottom: 24 }}>
        <h2>Состояние сервисов</h2>
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1fr 1fr",
            gap: 16,
          }}
        >
          <div
            style={{
              border: "1px solid #ddd",
              borderRadius: 12,
              padding: 16,
            }}
          >
            <h3>Backend</h3>
            <pre style={{ whiteSpace: "pre-wrap" }}>
              {JSON.stringify(backendHealth, null, 2)}
            </pre>
          </div>

          <div
            style={{
              border: "1px solid #ddd",
              borderRadius: 12,
              padding: 16,
            }}
          >
            <h3>Ollama</h3>
            <pre style={{ whiteSpace: "pre-wrap" }}>
              {JSON.stringify(ollamaHealth, null, 2)}
            </pre>
          </div>
        </div>
      </section>

      <section style={{ marginBottom: 24 }}>
        <h2>Создать задачу</h2>

        <form
          onSubmit={handleSubmit}
          style={{
            display: "grid",
            gap: 12,
            border: "1px solid #ddd",
            borderRadius: 12,
            padding: 16,
          }}
        >
          <label style={{ display: "grid", gap: 6 }}>
            <span>Название</span>
            <input
              value={form.title}
              onChange={(e) => updateField("title", e.target.value)}
              placeholder="Например: Создать Product module"
              required
              style={{ padding: 10, borderRadius: 8, border: "1px solid #ccc" }}
            />
          </label>

          <label style={{ display: "grid", gap: 6 }}>
            <span>Описание задачи</span>
            <textarea
              value={form.prompt}
              onChange={(e) => updateField("prompt", e.target.value)}
              placeholder="Что нужно сгенерировать или исправить"
              required
              rows={6}
              style={{ padding: 10, borderRadius: 8, border: "1px solid #ccc" }}
            />
          </label>

          <label style={{ display: "grid", gap: 6 }}>
            <span>Тип задачи</span>
            <select
              value={form.task_type}
              onChange={(e) => updateField("task_type", e.target.value)}
              style={{ padding: 10, borderRadius: 8, border: "1px solid #ccc" }}
            >
              <option value="generate">generate</option>
              <option value="fix">fix</option>
              <option value="test">test</option>
            </select>
          </label>

          <label style={{ display: "grid", gap: 6 }}>
            <span>Разрешённые файлы, по одному на строку</span>
            <textarea
              value={form.allowed_files}
              onChange={(e) => updateField("allowed_files", e.target.value)}
              placeholder={"app/models/product.py\napp/schemas/product.py"}
              rows={5}
              style={{ padding: 10, borderRadius: 8, border: "1px solid #ccc" }}
            />
          </label>

          <div>
            <button
              type="submit"
              disabled={submitting}
              style={{
                padding: "10px 16px",
                borderRadius: 8,
                border: "none",
                cursor: "pointer",
              }}
            >
              {submitting ? "Создание..." : "Создать задачу"}
            </button>
          </div>
        </form>
      </section>

      <section>
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            marginBottom: 12,
          }}
        >
          <h2>Список задач</h2>
          <button
            onClick={loadTasks}
            disabled={loadingTasks}
            style={{
              padding: "10px 16px",
              borderRadius: 8,
              border: "1px solid #ccc",
              cursor: "pointer",
              background: "#fff",
            }}
          >
            {loadingTasks ? "Обновление..." : "Обновить"}
          </button>
        </div>

        <div style={{ display: "grid", gap: 12 }}>
          {tasks.length === 0 ? (
            <div
              style={{
                border: "1px dashed #ccc",
                borderRadius: 12,
                padding: 16,
              }}
            >
              Пока задач нет
            </div>
          ) : (
            tasks.map((task) => (
              <div
                key={task.id}
                style={{
                  border: "1px solid #ddd",
                  borderRadius: 12,
                  padding: 16,
                }}
              >
                <div style={{ display: "flex", justifyContent: "space-between" }}>
                  <strong>{task.title}</strong>
                  <span>{task.status}</span>
                </div>

                <div style={{ marginTop: 8, color: "#444" }}>{task.task_type}</div>

                <pre
                  style={{
                    marginTop: 12,
                    whiteSpace: "pre-wrap",
                    background: "#f8f8f8",
                    padding: 12,
                    borderRadius: 8,
                  }}
                >
                  {task.prompt}
                </pre>

                <div style={{ marginTop: 12 }}>
                  <strong>Allowed files:</strong>
                  <ul>
                    {task.allowed_files.length === 0 ? (
                      <li>Не указаны</li>
                    ) : (
                      task.allowed_files.map((file) => <li key={file}>{file}</li>)
                    )}
                  </ul>
                </div>

                <div style={{ marginTop: 12, fontSize: 14, color: "#666" }}>
                  <div>ID: {task.id}</div>
                  <div>Создано: {task.created_at}</div>
                  <div>Обновлено: {task.updated_at}</div>
                </div>
              </div>
            ))
          )}
        </div>
      </section>
    </div>
  );
}