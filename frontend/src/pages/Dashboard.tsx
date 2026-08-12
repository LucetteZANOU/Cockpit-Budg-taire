import { useEffect, useState } from "react";

import {
  createBudgetLine,
  deleteBudgetLine,
  getSummary,
  listBudgetLines,
} from "../api/budgetLines";
import BudgetLineForm from "../components/BudgetLineForm";
import BudgetLineTable from "../components/BudgetLineTable";
import VarianceChart from "../components/VarianceChart";
import type { BudgetLine, BudgetLineCreate, VarianceSummary } from "../types/budgetLine";

type Status = "loading" | "ready" | "error";

export default function Dashboard() {
  const [lines, setLines] = useState<BudgetLine[]>([]);
  const [summary, setSummary] = useState<VarianceSummary | null>(null);
  const [status, setStatus] = useState<Status>("loading");

  const refresh = async () => {
    setStatus("loading");
    try {
      const [linesData, summaryData] = await Promise.all([listBudgetLines(), getSummary()]);
      setLines(linesData);
      setSummary(summaryData);
      setStatus("ready");
    } catch {
      setStatus("error");
    }
  };

  useEffect(() => {
    refresh();
  }, []);

  const handleCreate = async (payload: BudgetLineCreate) => {
    await createBudgetLine(payload);
    await refresh();
  };

  const handleDelete = async (id: number) => {
    await deleteBudgetLine(id);
    await refresh();
  };

  return (
    <div className="dashboard">
      <h1>BudgetRadar</h1>

      {status === "error" && (
        <p role="alert" className="ecart-depassement">
          Impossible de contacter le backend. Vérifie que l'API tourne sur{" "}
          {import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000"}.
        </p>
      )}

      <section className="card">
        <h2>Ajouter une ligne budgétaire</h2>
        <BudgetLineForm onSubmit={handleCreate} />
      </section>

      <section className="card">
        <h2>Écarts par catégorie</h2>
        {status === "loading" ? (
          <p>Chargement...</p>
        ) : (
          <VarianceChart categories={summary?.par_categorie ?? []} />
        )}
      </section>

      <section className="card">
        <h2>Lignes budgétaires</h2>
        {status === "loading" ? <p>Chargement...</p> : <BudgetLineTable lines={lines} onDelete={handleDelete} />}
      </section>
    </div>
  );
}
