import { request } from "./client";
import type { CentreCout, CentreCoutCreate } from "../types/budgetLine";

export function listCentresCout(): Promise<CentreCout[]> {
  return request<CentreCout[]>("/api/centres-cout");
}

export function createCentreCout(payload: CentreCoutCreate): Promise<CentreCout> {
  return request<CentreCout>("/api/centres-cout", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}
