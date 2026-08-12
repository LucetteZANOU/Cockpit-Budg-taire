import { request } from "./client";
import type { BudgetLine, BudgetLineCreate, VarianceSummary } from "../types/budgetLine";

export function listBudgetLines(): Promise<BudgetLine[]> {
  return request<BudgetLine[]>("/api/budget-lines");
}

export function createBudgetLine(payload: BudgetLineCreate): Promise<BudgetLine> {
  return request<BudgetLine>("/api/budget-lines", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function updateBudgetLine(
  id: number,
  payload: Partial<BudgetLineCreate>,
): Promise<BudgetLine> {
  return request<BudgetLine>(`/api/budget-lines/${id}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
}

export function deleteBudgetLine(id: number): Promise<void> {
  return request<void>(`/api/budget-lines/${id}`, { method: "DELETE" });
}

export function getSummary(): Promise<VarianceSummary> {
  return request<VarianceSummary>("/api/budget-lines/summary");
}
