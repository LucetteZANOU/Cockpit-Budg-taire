export interface CentreCout {
  id: number;
  nom: string;
  description: string | null;
  created_at: string;
}

export interface CentreCoutCreate {
  nom: string;
  description?: string | null;
}

export interface BudgetLine {
  id: number;
  centre_cout: CentreCout;
  exercice: number;
  periode: string;
  montant_prevu: string;
  montant_reestime: string | null;
  montant_realise: string;
  created_at: string;
  updated_at: string;
  ecart_valeur: string;
  ecart_pourcentage: string | null;
  ecart_reestime_valeur: string | null;
  ecart_reestime_pourcentage: string | null;
}

export interface BudgetLineCreate {
  centre_cout_id: number;
  exercice: number;
  periode: string;
  montant_prevu: string;
  montant_reestime?: string | null;
  montant_realise: string;
}

export interface CentreCoutSummary {
  centre_cout: string;
  total_prevu: string;
  total_reestime: string | null;
  total_realise: string;
  ecart_valeur: string;
  ecart_pourcentage: string | null;
  ecart_reestime_valeur: string | null;
  ecart_reestime_pourcentage: string | null;
}

export interface VarianceSummary {
  total_prevu: string;
  total_reestime: string | null;
  total_realise: string;
  ecart_valeur: string;
  ecart_pourcentage: string | null;
  ecart_reestime_valeur: string | null;
  ecart_reestime_pourcentage: string | null;
  par_centre_cout: CentreCoutSummary[];
}
