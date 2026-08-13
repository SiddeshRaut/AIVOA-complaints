from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.extraction import DuplicateCandidate
from app.services.duplicate_service import find_duplicates

router = APIRouter()


class DuplicateCheckIn(BaseModel):
    product_name: str = ""
    batch_number: str = ""
    complaint_type: str = ""
    description: str = ""
    exclude_id: int | None = None


@router.post("/check-duplicates", response_model=list[DuplicateCandidate])
def check_duplicates(payload: DuplicateCheckIn, db: Session = Depends(get_db)) -> list[dict]:
    return find_duplicates(
        db,
        product_name=payload.product_name,
        batch_number=payload.batch_number,
        complaint_type=payload.complaint_type,
        description=payload.description,
        exclude_id=payload.exclude_id,
    )
