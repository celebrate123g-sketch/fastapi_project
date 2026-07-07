import os
import shutil
from uuid import uuid4

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from database.models import QuoteModel


UPLOAD_DIR = "uploads/images"

os.makedirs(UPLOAD_DIR, exist_ok=True)


def upload_image(
    db: Session,
    quote_id: int,
    file: UploadFile
):
    quote = (
        db.query(QuoteModel)
        .filter(QuoteModel.id == quote_id)
        .first()
    )

    if quote is None:
        raise HTTPException(
            status_code=404,
            detail="Quote not found."
        )

    if file.content_type is None or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="File must be an image."
        )

    extension = os.path.splitext(file.filename)[1]

    filename = f"{uuid4().hex}{extension}"

    file_path = os.path.join(
        UPLOAD_DIR,
        filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    quote.image_url = file_path

    db.commit()
    db.refresh(quote)

    return {
        "message": "Image uploaded successfully.",
        "image_url": quote.image_url
    }


def delete_image(
    db: Session,
    quote_id: int
):
    quote = (
        db.query(QuoteModel)
        .filter(QuoteModel.id == quote_id)
        .first()
    )

    if quote is None:
        raise HTTPException(
            status_code=404,
            detail="Quote not found."
        )

    if quote.image_url and os.path.exists(quote.image_url):
        os.remove(quote.image_url)

    quote.image_url = None

    db.commit()

    return {
        "message": "Image deleted successfully."
    }