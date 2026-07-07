from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from database.database import get_db
from services.import_service import (
    import_json,
    import_csv
)

router = APIRouter(
    tags=["Import"]
)


@router.post("/import/json")
def import_quotes_json(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(".json"):
        return {
            "message": "Please upload a JSON file."
        }

    return import_json(
        db,
        file
    )


@router.post("/import/csv")
def import_quotes_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(".csv"):
        return {
            "message": "Please upload a CSV file."
        }

    return import_csv(
        db,
        file
    )