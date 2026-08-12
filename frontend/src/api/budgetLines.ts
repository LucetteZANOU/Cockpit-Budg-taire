import type { BudgetLine, BudgetLineCreate, VarianceSummary } from "../types/budgetLine";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status} ${response.statusText}`);
  }
  if (response.status === 204) {
    return undefined as T;
  }
  return response.json() as Promise<T>;
}

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
