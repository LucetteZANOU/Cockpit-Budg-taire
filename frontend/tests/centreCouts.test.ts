import { afterEach, describe, expect, it, vi } from "vitest";

import { createCentreCout, listCentresCout } from "../src/api/centreCouts";

function mockFetch(response: Partial<Response>) {
  vi.stubGlobal(
    "fetch",
    vi.fn(() => Promise.resolve(response as Response)),
  );
}

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("centreCouts api client", () => {
  it("lists centres de coût", async () => {
    mockFetch({ ok: true, json: () => Promise.resolve([{ id: 1, nom: "Marketing" }]) });
    const result = await listCentresCout();
    expect(result).toEqual([{ id: 1, nom: "Marketing" }]);
  });

  it("creates a centre de coût", async () => {
    const created = { id: 1, nom: "Logistique", description: null };
    mockFetch({ ok: true, json: () => Promise.resolve(created) });
    const result = await createCentreCout({ nom: "Logistique" });
    expect(result).toEqual(created);
  });

  it("throws on conflict (duplicate nom)", async () => {
    mockFetch({ ok: false, status: 409, statusText: "Conflict" });
    await expect(createCentreCout({ nom: "Marketing" })).rejects.toThrow("Request failed: 409");
  });
});
