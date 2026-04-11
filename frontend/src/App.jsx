import { useEffect, useState } from "react";

export default function App() {
  const [backendHealth, setBackendHealth] = useState(null);
  const [ollamaHealth, setOllamaHealth] = useState(null);

  useEffect(() => {
    fetch("/api/health")
      .then((r) => r.json())
      .then(setBackendHealth)
      .catch((e) => setBackendHealth({ status: "error", detail: String(e) }));

    fetch("/api/ollama/health")
      .then((r) => r.json())
      .then(setOllamaHealth)
      .catch((e) => setOllamaHealth({ status: "error", detail: String(e) }));
  }, []);

  return (
    <div style={{ fontFamily: "sans-serif", padding: 24 }}>
      <h1>Local AI Studio</h1>
      <p>Локальная студия для генерации кода, тестов и оркестрации задач.</p>

      <h2>Backend</h2>
      <pre>{JSON.stringify(backendHealth, null, 2)}</pre>

      <h2>Ollama</h2>
      <pre>{JSON.stringify(ollamaHealth, null, 2)}</pre>
    </div>
  );
}