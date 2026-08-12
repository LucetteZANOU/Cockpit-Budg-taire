import { useEffect, useState } from "react";

import {
  createBudgetLine,
  deleteBudgetLine,
  getSummary,
  listBudgetLines,
} from "../api/budgetLines";
import { createCentreCout, listCentresCout } from "../api/centreCouts";
import BudgetLineForm from "../components/BudgetLineForm";
import BudgetLineTable from "../components/BudgetLineTable";
import CentreCoutManager from "../components/CentreCoutManager";
import VarianceChart from "../components/VarianceChart";
import type {
  BudgetLine,
  BudgetLineCreate,
  CentreCout,
  VarianceSummary,
} from "../types/budgetLine";

type Status = "loading" | "ready" | "error";

export default function Dashboard() {
  const [lines, setLines] = useState<BudgetLine[]>([]);
  const [centresCout, setCentresCout] = useState<CentreCout[]>([]);
  const [summary, setSummary] = useState<VarianceSummary | null>(null);
  const [status, setStatus] = useState<Status>("loading");

  const refresh = async () => {
    setStatus("loading");
    try {
      const [linesData, summaryData, centresData] = await Promise.all([
        listBudgetLines(),
        getSummary(),
        listCentresCout(),
      ]);
      setLines(linesData);
      setSummary(summaryData);
      setCentresCout(centresData);
      setStatus("ready");
    } catch {
      setStatus("error");
    }
  };

  useEffect(() => {
    refresh();
  }, []);

  const handleCreateLine = async (payload: BudgetLineCreate) => {
    await createBudgetLine(payload);
    await refresh();
  };

  const handleCreateCentreCout = async (nom: string) => {
    await createCentreCout({ nom });
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
        <h2>Centres de coût</h2>
        <CentreCoutManager centresCout={centresCout} onCreate={handleCreateCentreCout} />
      </section>

      <section className="card">
        <h2>Ajouter une ligne budgétaire</h2>
        <BudgetLineForm centresCout={centresCout} onSubmit={handleCreateLine} />
      </section>

      <section className="card">
        <h2>Écarts par centre de coût</h2>
        {status === "loading" ? (
          <p>Chargement...</p>
        ) : (
          <VarianceChart centresCout={summary?.par_centre_cout ?? []} />
        )}
      </section>

      <section className="card">
        <h2>Lignes budgétaires</h2>
        {status === "loading" ? (
          <p>Chargement...</p>
        ) : (
          <BudgetLineTable lines={lines} onDelete={handleDelete} />
        )}
      </section>
    </div>
  );
}
