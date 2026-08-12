from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

PERIODE_PATTERN = r"^\d{4}-(0[1-9]|1[0-2])$"


class BudgetLineBase(BaseModel):
    categorie: str = Field(min_length=1, max_length=100)
    montant_prevu: Decimal = Field(ge=0)
    montant_realise: Decimal = Field(ge=0, default=Decimal(0))
    periode: str = Field(pattern=PERIODE_PATTERN, description="Format YYYY-MM")


class BudgetLineCreate(BudgetLineBase):
    pass


class BudgetLineUpdate(BaseModel):
    categorie: str | None = Field(default=None, min_length=1, max_length=100)
    montant_prevu: Decimal | None = Field(default=None, ge=0)
    montant_realise: Decimal | None = Field(default=None, ge=0)
    periode: str | None = Field(default=None, pattern=PERIODE_PATTERN)


class BudgetLineRead(BudgetLineBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
    ecart_valeur: Decimal
    ecart_pourcentage: Decimal | None
