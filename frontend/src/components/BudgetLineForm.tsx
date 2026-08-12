import { useState } from "react";
import type { ChangeEvent, FormEvent } from "react";

import type { BudgetLineCreate } from "../types/budgetLine";

interface Props {
  onSubmit: (payload: BudgetLineCreate) => Promise<void>;
}

const emptyForm: BudgetLineCreate = {
  categorie: "",
  montant_prevu: "",
  montant_realise: "",
  periode: "",
};

export default function BudgetLineForm({ onSubmit }: Props) {
  const [form, setForm] = useState<BudgetLineCreate>(emptyForm);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const handleChange = (field: keyof BudgetLineCreate) => (e: ChangeEvent<HTMLInputElement>) => {
    setForm((prev) => ({ ...prev, [field]: e.target.value }));
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!form.categorie || !form.montant_prevu || !form.periode) {
      setError("Catégorie, montant prévu et période sont requis.");
      return;
    }
    if (!/^\d{4}-(0[1-9]|1[0-2])$/.test(form.periode)) {
      setError("La période doit être au format AAAA-MM.");
      return;
    }

    setSubmitting(true);
    try {
      await onSubmit({ ...form, montant_realise: form.montant_realise || "0" });
      setForm(emptyForm);
    } catch {
      setError("Échec de la création de la ligne budgétaire.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form className="budget-line-form" onSubmit={handleSubmit}>
      <label>
        Catégorie
        <input value={form.categorie} onChange={handleChange("categorie")} required />
      </label>
      <label>
        Montant prévu
        <input
          type="number"
          step="0.01"
          value={form.montant_prevu}
          onChange={handleChange("montant_prevu")}
          required
        />
      </label>
      <label>
        Montant réalisé
        <input
          type="number"
          step="0.01"
          value={form.montant_realise}
          onChange={handleChange("montant_realise")}
        />
      </label>
      <label>
        Période (AAAA-MM)
        <input
          placeholder="2026-01"
          value={form.periode}
          onChange={handleChange("periode")}
          required
        />
      </label>
      <button type="submit" disabled={submitting}>
        {submitting ? "Ajout..." : "Ajouter"}
      </button>
      {error && (
        <p role="alert" className="ecart-depassement">
          {error}
        </p>
      )}
    </form>
  );
}
