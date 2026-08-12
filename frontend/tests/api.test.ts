import { afterEach, describe, expect, it, vi } from "vitest";

import { createBudgetLine, deleteBudgetLine, listBudgetLines } from "../src/api/budgetLines";

function mockFetch(response: Partial<Response>) {
  vi.stubGlobal(
    "fetch",
    vi.fn(() => Promise.resolve(response as Response)),
  );
}

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("budgetLines api client", () => {
  it("lists budget lines on success", async () => {
    mockFetch({ ok: true, json: () => Promise.resolve([{ id: 1 }]) });
    const result = await listBudgetLines();
    expect(result).toEqual([{ id: 1 }]);
  });

  it("throws when the response is not ok", async () => {
    mockFetch({ ok: false, status: 500, statusText: "Internal Server Error" });
    await expect(listBudgetLines()).rejects.toThrow("Request failed: 500");
  });

  it("posts a new budget line", async () => {
    const created = { id: 2, categorie: "Ventes" };
    mockFetch({ ok: true, json: () => Promise.resolve(created) });
    const result = await createBudgetLine({
      categorie: "Ventes",
      montant_prevu: "100",
      montant_realise: "0",
      periode: "2026-02",
    });
    expect(result).toEqual(created);
  });

  it("returns undefined on a 204 delete response", async () => {
    mockFetch({ ok: true, status: 204 });
    await expect(deleteBudgetLine(1)).resolves.toBeUndefined();
  });
});
