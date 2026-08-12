import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import VarianceChart from "../src/components/VarianceChart";
import type { CategorySummary } from "../src/types/budgetLine";

describe("VarianceChart", () => {
  it("renders an empty state when there is no data", () => {
    render(<VarianceChart categories={[]} />);
    expect(screen.getByText(/pas encore de données/i)).toBeInTheDocument();
  });

  it("renders the legend and category labels when data is present", () => {
    const categories: CategorySummary[] = [
      {
        categorie: "Marketing",
        total_prevu: "1000.00",
        total_realise: "800.00",
        ecart_valeur: "-200.00",
        ecart_pourcentage: "-20.00",
      },
      {
        categorie: "Ventes",
        total_prevu: "500.00",
        total_realise: "600.00",
        ecart_valeur: "100.00",
        ecart_pourcentage: "20.00",
      },
    ];
    render(<VarianceChart categories={categories} />);
    expect(screen.getByText("Dépassement")).toBeInTheDocument();
    expect(screen.getByText("Économie")).toBeInTheDocument();
  });
});
