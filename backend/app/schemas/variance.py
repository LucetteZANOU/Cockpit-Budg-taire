from decimal import Decimal

from pydantic import BaseModel


class CategorySummaryRead(BaseModel):
    categorie: str
    total_prevu: Decimal
    total_realise: Decimal
    ecart_valeur: Decimal
    ecart_pourcentage: Decimal | None


class VarianceSummaryRead(BaseModel):
    total_prevu: Decimal
    total_realise: Decimal
    ecart_valeur: Decimal
    ecart_pourcentage: Decimal | None
    par_categorie: list[CategorySummaryRead]
