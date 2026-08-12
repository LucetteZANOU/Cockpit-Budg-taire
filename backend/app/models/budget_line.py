from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class BudgetLine(Base):
    __tablename__ = "budget_lines"

    id: Mapped[int] = mapped_column(primary_key=True)
    categorie: Mapped[str] = mapped_column(String(100), index=True)
    montant_prevu: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    montant_realise: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    periode: Mapped[str] = mapped_column(String(7), index=True)  # format YYYY-MM

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
