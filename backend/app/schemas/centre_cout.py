from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CentreCoutCreate(BaseModel):
    nom: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=255)


class CentreCoutRead(CentreCoutCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
