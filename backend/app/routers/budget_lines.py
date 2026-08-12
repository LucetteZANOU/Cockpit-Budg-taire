from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.budget_line import BudgetLine
from app.schemas.budget_line import BudgetLineCreate, BudgetLineRead, BudgetLineUpdate
from app.schemas.variance import VarianceSummaryRead
from app.services.variance import (
    compute_ecart_pourcentage,
    compute_ecart_valeur,
    summarize_variances,
)

router = APIRouter(prefix="/api/budget-lines", tags=["budget-lines"])


def _to_read(line: BudgetLine) -> BudgetLineRead:
    return BudgetLineRead(
        id=line.id,
        categorie=line.categorie,
        montant_prevu=line.montant_prevu,
        montant_realise=line.montant_realise,
        periode=line.periode,
        created_at=line.created_at,
        updated_at=line.updated_at,
        ecart_valeur=compute_ecart_valeur(line.montant_prevu, line.montant_realise),
        ecart_pourcentage=compute_ecart_pourcentage(line.montant_prevu, line.montant_realise),
    )


@router.post("", response_model=BudgetLineRead, status_code=201)
def create_budget_line(payload: BudgetLineCreate, db: Session = Depends(get_db)) -> BudgetLineRead:
    line = BudgetLine(**payload.model_dump())
    db.add(line)
    db.commit()
    db.refresh(line)
    return _to_read(line)


@router.get("", response_model=list[BudgetLineRead])
def list_budget_lines(
    categorie: str | None = None,
    periode: str | None = None,
    db: Session = Depends(get_db),
) -> list[BudgetLineRead]:
    stmt = select(BudgetLine)
    if categorie is not None:
        stmt = stmt.where(BudgetLine.categorie == categorie)
    if periode is not None:
        stmt = stmt.where(BudgetLine.periode == periode)
    lines = db.execute(stmt.order_by(BudgetLine.periode, BudgetLine.categorie)).scalars().all()
    return [_to_read(line) for line in lines]


@router.get("/summary", response_model=VarianceSummaryRead)
def get_summary(
    periode: str | None = None,
    db: Session = Depends(get_db),
) -> VarianceSummaryRead:
    stmt = select(BudgetLine)
    if periode is not None:
        stmt = stmt.where(BudgetLine.periode == periode)
    lines = db.execute(stmt).scalars().all()
    return VarianceSummaryRead.model_validate(summarize_variances(lines), from_attributes=True)


def _get_or_404(db: Session, line_id: int) -> BudgetLine:
    line = db.get(BudgetLine, line_id)
    if line is None:
        raise HTTPException(status_code=404, detail="Budget line not found")
    return line


@router.get("/{line_id}", response_model=BudgetLineRead)
def get_budget_line(line_id: int, db: Session = Depends(get_db)) -> BudgetLineRead:
    return _to_read(_get_or_404(db, line_id))


@router.patch("/{line_id}", response_model=BudgetLineRead)
def update_budget_line(
    line_id: int, payload: BudgetLineUpdate, db: Session = Depends(get_db)
) -> BudgetLineRead:
    line = _get_or_404(db, line_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(line, field, value)
    db.commit()
    db.refresh(line)
    return _to_read(line)


@router.delete("/{line_id}", status_code=204)
def delete_budget_line(line_id: int, db: Session = Depends(get_db)) -> None:
    line = _get_or_404(db, line_id)
    db.delete(line)
    db.commit()
