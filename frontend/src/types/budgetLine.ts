export interface BudgetLine {
  id: number;
  categorie: string;
  montant_prevu: string;
  montant_realise: string;
  periode: string;
  ecart_valeur: string;
  ecart_pourcentage: string | null;
  created_at: string;
  updated_at: string;
}

export interface BudgetLineCreate {
  categorie: string;
  montant_prevu: string;
  montant_realise: string;
  periode: string;
}

export interface CategorySummary {
  categorie: string;
  total_prevu: string;
  total_realise: string;
  ecart_valeur: string;
  ecart_pourcentage: string | null;
}

export interface VarianceSummary {
  total_prevu: string;
  total_realise: string;
  ecart_valeur: string;
  ecart_pourcentage: string | null;
  par_categorie: CategorySummary[];
}
