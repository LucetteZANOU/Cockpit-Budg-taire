import { useState } from "react";
import type { ChangeEvent, FormEvent } from "react";

import type { BudgetLineCreate, CentreCout } from "../types/budgetLine";

interface Props {
  centresCout: CentreCout[];
  onSubmit: (payload: BudgetLineCreate) => Promise<void>;
}

interface FormState {
  centre_cout_id: string;
  exercice: string;
  periode: string;
  montant_prevu: string;
  montant_reestime: string;
  montant_realise: string;
}

const emptyForm: FormState = {
  centre_cout_id: "",
  exercice: "",
  periode: "",
  montant_prevu: "",
  montant_reestime: "",
  montant_realise: "",
};

export default function BudgetLineForm({ centresCout, onSubmit }: Props) {
  const [form, setForm] = useState<FormState>(emptyForm);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const handleChange =
    (field: keyof FormState) => (e: ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
      setForm((prev) => ({ ...prev, [field]: e.target.value }));
    };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!form.centre_cout_id || !form.montant_prevu || !form.periode) {
      setError("Centre de coût, montant prévu et période sont requis.");
      return;
    }
    if (!/^\d{4}-(0[1-9]|1[0-2])$/.test(form.periode)) {
      setError("La période doit être au format AAAA-MM.");
      return;
    }

    setSubmitting(true);
    try {
      await onSubmit({
        centre_cout_id: Number(form.centre_cout_id),
        exercice: Number(form.periode.slice(0, 4)),
        periode: form.periode,
        montant_prevu: form.montant_prevu,
        montant_reestime: form.montant_reestime || null,
        montant_realise: form.montant_realise || "0",
      });
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
        Centre de coût
        <select value={form.centre_cout_id} onChange={handleChange("centre_cout_id")} required>
          <option value="">Choisir...</option>
          {centresCout.map((c) => (
            <option key={c.id} value={c.id}>
              {c.nom}
            </option>
          ))}
        </select>
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
        Montant réestimé
        <input
          type="number"
          step="0.01"
          value={form.montant_reestime}
          onChange={handleChange("montant_reestime")}
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
      <button type="submit" disabled={submitting || centresCout.length === 0}>
        {submitting ? "Ajout..." : "Ajouter"}
      </button>
      {centresCout.length === 0 && <p>Crée d'abord un centre de coût ci-dessus.</p>}
      {error && (
        <p role="alert" className="ecart-depassement">
          {error}
        </p>
      )}
    </form>
  );
}
