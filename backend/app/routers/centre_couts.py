from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.centre_cout import CentreCout
from app.schemas.centre_cout import CentreCoutCreate, CentreCoutRead

router = APIRouter(prefix="/api/centres-cout", tags=["centres-cout"])


@router.post("", response_model=CentreCoutRead, status_code=201)
def create_centre_cout(payload: CentreCoutCreate, db: Session = Depends(get_db)) -> CentreCoutRead:
    centre_cout = CentreCout(**payload.model_dump())
    db.add(centre_cout)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Ce centre de coût existe déjà") from exc
    db.refresh(centre_cout)
    return CentreCoutRead.model_validate(centre_cout)


@router.get("", response_model=list[CentreCoutRead])
def list_centres_cout(db: Session = Depends(get_db)) -> list[CentreCoutRead]:
    centres = db.execute(select(CentreCout).order_by(CentreCout.nom)).scalars().all()
    return [CentreCoutRead.model_validate(c) for c in centres]
