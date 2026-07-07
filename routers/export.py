from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from database.database import get_db
from services.export_service import (
    export_json,
    export_csv
)

router = APIRouter(
    tags=["Export"]
)


@router.get("/export/json")
def export_quotes_json(
    db: Session = Depends(get_db)
):
    file_path = export_json(db)

    return FileResponse(
        path=file_path,
        filename="quotes.json",
        media_type="application/json"
    )


@router.get("/export/csv")
def export_quotes_csv(
    db: Session = Depends(get_db)
):
    file_path = export_csv(db)

    return FileResponse(
        path=file_path,
        filename="quotes.csv",
        media_type="text/csv"
    )