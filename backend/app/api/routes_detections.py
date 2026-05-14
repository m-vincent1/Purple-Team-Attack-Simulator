from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.detection import CoverageOut
from app.services.coverage_calculator import calculate_coverage

router = APIRouter(prefix="/api", tags=["detections"])


@router.get("/coverage", response_model=CoverageOut)
def get_coverage(db: Session = Depends(get_db)):
    return calculate_coverage(db)
