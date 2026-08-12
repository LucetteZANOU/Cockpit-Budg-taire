import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import VarianceChart from "../src/components/VarianceChart";
import type { CentreCoutSummary } from "../src/types/budgetLine";

describe("VarianceChart", () => {
  it("renders an empty state when there is no data", () => {
    render(<VarianceChart centresCout={[]} />);
    expect(screen.getByText(/pas encore de données/i)).toBeInTheDocument();
  });

  it("renders the legend when data is present", () => {
    const centresCout: CentreCoutSummary[] = [
      {
        centre_cout: "Marketing",
        total_prevu: "1000.00",
        total_reestime: null,
        total_realise: "800.00",
        ecart_valeur: "-200.00",
        ecart_pourcentage: "-20.00",
        ecart_reestime_valeur: null,
        ecart_reestime_pourcentage: null,
      },
      {
        centre_cout: "Ventes",
        total_prevu: "500.00",
        total_reestime: null,
        total_realise: "600.00",
        ecart_valeur: "100.00",
        ecart_pourcentage: "20.00",
        ecart_reestime_valeur: null,
        ecart_reestime_pourcentage: null,
      },
    ];
    render(<VarianceChart centresCout={centresCout} />);
    expect(screen.getByText("Dépassement")).toBeInTheDocument();
    expect(screen.getByText("Économie")).toBeInTheDocument();
  });
});
