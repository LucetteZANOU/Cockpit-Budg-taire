import { useEffect, useState } from "react";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

function App() {
  const [backendStatus, setBackendStatus] = useState<"loading" | "ok" | "error">("loading");

  useEffect(() => {
    fetch(`${API_BASE_URL}/health`)
      .then((res) => (res.ok ? setBackendStatus("ok") : setBackendStatus("error")))
      .catch(() => setBackendStatus("error"));
  }, []);

  return (
    <main>
      <h1>BudgetRadar</h1>
      <p>Backend: {backendStatus}</p>
    </main>
  );
}

export default App;
