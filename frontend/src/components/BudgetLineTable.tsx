import type { BudgetLine } from "../types/budgetLine";

interface Props {
  lines: BudgetLine[];
  onDelete: (id: number) => void;
}

function formatAmount(value: string): string {
  return new Intl.NumberFormat("fr-FR", { style: "currency", currency: "XOF" }).format(
    Number(value),
  );
}

function formatPercentage(value: string | null): string {
  return value === null ? "N/A" : `${value}%`;
}

export default function BudgetLineTable({ lines, onDelete }: Props) {
  if (lines.length === 0) {
    return <p>Aucune ligne budgétaire pour l'instant.</p>;
  }

  return (
    <table aria-label="Lignes budgétaires">
      <thead>
        <tr>
          <th>Centre de coût</th>
          <th>Exercice</th>
          <th>Période</th>
          <th>Prévu</th>
          <th>Réestimé</th>
          <th>Réalisé</th>
          <th>Écart</th>
          <th>Écart %</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        {lines.map((line) => {
          const isOverBudget = Number(line.ecart_valeur) >= 0;
          return (
            <tr key={line.id}>
              <td>{line.centre_cout.nom}</td>
              <td>{line.exercice}</td>
              <td>{line.periode}</td>
              <td>{formatAmount(line.montant_prevu)}</td>
              <td>{line.montant_reestime ? formatAmount(line.montant_reestime) : "N/A"}</td>
              <td>{formatAmount(line.montant_realise)}</td>
              <td className={isOverBudget ? "ecart-depassement" : "ecart-economie"}>
                {formatAmount(line.ecart_valeur)}
              </td>
              <td className={isOverBudget ? "ecart-depassement" : "ecart-economie"}>
                {formatPercentage(line.ecart_pourcentage)}
              </td>
              <td>
                <button type="button" onClick={() => onDelete(line.id)}>
                  Supprimer
                </button>
              </td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}
