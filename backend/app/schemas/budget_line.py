from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.schemas.centre_cout import CentreCoutRead

PERIODE_PATTERN = r"^\d{4}-(0[1-9]|1[0-2])$"


class BudgetLineBase(BaseModel):
    centre_cout_id: int
    exercice: int = Field(ge=2000, le=2100)
    periode: str = Field(pattern=PERIODE_PATTERN, description="Format YYYY-MM")
    montant_prevu: Decimal = Field(ge=0)
    montant_reestime: Decimal | None = Field(default=None, ge=0)
    montant_realise: Decimal = Field(ge=0, default=Decimal(0))

    @model_validator(mode="after")
    def check_exercice_matches_periode(self) -> "BudgetLineBase":
        if int(self.periode[:4]) != self.exercice:
            raise ValueError("exercice doit correspondre à l'année de periode")
        return self


class BudgetLineCreate(BudgetLineBase):
    pass


class BudgetLineUpdate(BaseModel):
    centre_cout_id: int | None = None
    exercice: int | None = Field(default=None, ge=2000, le=2100)
    periode: str | None = Field(default=None, pattern=PERIODE_PATTERN)
    montant_prevu: Decimal | None = Field(default=None, ge=0)
    montant_reestime: Decimal | None = Field(default=None, ge=0)
    montant_realise: Decimal | None = Field(default=None, ge=0)


class BudgetLineRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    centre_cout: CentreCoutRead
    exercice: int
    periode: str
    montant_prevu: Decimal
    montant_reestime: Decimal | None
    montant_realise: Decimal
    created_at: datetime
    updated_at: datetime

    ecart_valeur: Decimal
    ecart_pourcentage: Decimal | None
    ecart_reestime_valeur: Decimal | None
    ecart_reestime_pourcentage: Decimal | None
