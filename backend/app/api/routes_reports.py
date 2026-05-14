from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os

from app.core.database import get_db
from app.services.report_generator import generate_report

router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.get("/{run_id}")
def get_report(
    run_id: str,
    format: str = Query(default="html", pattern="^(html|md|json)$"),
    db: Session = Depends(get_db),
):
    try:
        path = generate_report(run_id, format, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not os.path.exists(path):
        raise HTTPException(status_code=500, detail="Report file not generated")

    media_types = {"html": "text/html", "md": "text/markdown", "json": "application/json"}
    return FileResponse(path, media_type=media_types.get(format, "text/plain"))
