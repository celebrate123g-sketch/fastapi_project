from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from database.database import get_db
from services.image_service import (
    upload_image,
    delete_image
)

router = APIRouter(
    tags=["Images"]
)


@router.post("/quotes/{quote_id}/image")
def upload_quote_image(
    quote_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    return upload_image(
        db,
        quote_id,
        file
    )


@router.delete("/quotes/{quote_id}/image")
def delete_quote_image(
    quote_id: int,
    db: Session = Depends(get_db)
):
    return delete_image(
        db,
        quote_id
    )