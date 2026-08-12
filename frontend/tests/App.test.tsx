import { render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

import App from "../src/App";

describe("App", () => {
  beforeEach(() => {
    vi.stubGlobal(
      "fetch",
      vi.fn(() => Promise.resolve({ ok: true } as Response)),
    );
  });

  it("renders the app title", () => {
    render(<App />);
    expect(screen.getByText("BudgetRadar")).toBeInTheDocument();
  });
});
