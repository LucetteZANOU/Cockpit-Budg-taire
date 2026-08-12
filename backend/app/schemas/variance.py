from decimal import Decimal

from pydantic import BaseModel


class CentreCoutSummaryRead(BaseModel):
    centre_cout: str
    total_prevu: Decimal
    total_reestime: Decimal | None
    total_realise: Decimal
    ecart_valeur: Decimal
    ecart_pourcentage: Decimal | None
    ecart_reestime_valeur: Decimal | None
    ecart_reestime_pourcentage: Decimal | None


class VarianceSummaryRead(BaseModel):
    total_prevu: Decimal
    total_reestime: Decimal | None
    total_realise: Decimal
    ecart_valeur: Decimal
    ecart_pourcentage: Decimal | None
    ecart_reestime_valeur: Decimal | None
    ecart_reestime_pourcentage: Decimal | None
    par_centre_cout: list[CentreCoutSummaryRead]
