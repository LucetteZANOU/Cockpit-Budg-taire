import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import BudgetLineTable from "../src/components/BudgetLineTable";
import type { BudgetLine } from "../src/types/budgetLine";

const baseLine: BudgetLine = {
  id: 1,
  categorie: "Marketing",
  montant_prevu: "1000.00",
  montant_realise: "800.00",
  periode: "2026-01",
  ecart_valeur: "-200.00",
  ecart_pourcentage: "-20.00",
  created_at: "2026-01-01T00:00:00Z",
  updated_at: "2026-01-01T00:00:00Z",
};

describe("BudgetLineTable", () => {
  it("renders an empty state when there are no lines", () => {
    render(<BudgetLineTable lines={[]} onDelete={vi.fn()} />);
    expect(screen.getByText(/aucune ligne budgétaire/i)).toBeInTheDocument();
  });

  it("renders a negative écart (économie)", () => {
    render(<BudgetLineTable lines={[baseLine]} onDelete={vi.fn()} />);
    expect(screen.getByText("Marketing")).toBeInTheDocument();
    expect(screen.getByText("-20.00%")).toBeInTheDocument();
  });

  it("shows N/A when ecart_pourcentage is null", () => {
    const line: BudgetLine = { ...baseLine, ecart_pourcentage: null };
    render(<BudgetLineTable lines={[line]} onDelete={vi.fn()} />);
    expect(screen.getByText("N/A")).toBeInTheDocument();
  });
});
