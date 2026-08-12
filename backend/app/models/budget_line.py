from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.centre_cout import CentreCout


class BudgetLine(Base):
    __tablename__ = "budget_lines"

    id: Mapped[int] = mapped_column(primary_key=True)
    centre_cout_id: Mapped[int] = mapped_column(ForeignKey("centres_cout.id"), index=True)
    centre_cout: Mapped["CentreCout"] = relationship()

    exercice: Mapped[int] = mapped_column(index=True)  # année budgétaire, ex: 2026
    periode: Mapped[str] = mapped_column(String(7), index=True)  # format YYYY-MM

    montant_prevu: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    montant_reestime: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), default=None)
    montant_realise: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
