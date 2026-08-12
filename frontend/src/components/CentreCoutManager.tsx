import { useState } from "react";
import type { FormEvent } from "react";

import type { CentreCout } from "../types/budgetLine";

interface Props {
  centresCout: CentreCout[];
  onCreate: (nom: string) => Promise<void>;
}

export default function CentreCoutManager({ centresCout, onCreate }: Props) {
  const [nom, setNom] = useState("");
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);
    if (!nom.trim()) return;
    try {
      await onCreate(nom.trim());
      setNom("");
    } catch {
      setError("Ce centre de coût existe peut-être déjà.");
    }
  };

  return (
    <div>
      <ul>
        {centresCout.map((c) => (
          <li key={c.id}>{c.nom}</li>
        ))}
      </ul>
      <form className="budget-line-form" onSubmit={handleSubmit}>
        <label>
          Nouveau centre de coût
          <input value={nom} onChange={(e) => setNom(e.target.value)} placeholder="ex: Logistique" />
        </label>
        <button type="submit">Ajouter</button>
      </form>
      {error && (
        <p role="alert" className="ecart-depassement">
          {error}
        </p>
      )}
    </div>
  );
}
