
import os
from uuid import uuid4

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from database.models import QuoteModel


UPLOAD_DIR = "uploads/images"
MAX_FILE_SIZE = 5 * 1024 * 1024

ALLOWED_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp"
}

os.makedirs(UPLOAD_DIR, exist_ok=True)


def upload_image(
    db: Session,
    quote_id: int,
    file: UploadFile
):
    quote = (
        db.query(QuoteModel)
        .filter(
            QuoteModel.id == quote_id,
            QuoteModel.is_deleted.is_(False)
        )
        .first()
    )

    if quote is None:
        raise HTTPException(
            status_code=404,
            detail="Quote not found."
        )

    extension = ALLOWED_TYPES.get(file.content_type)

    if extension is None:
        raise HTTPException(
            status_code=400,
            detail="Only JPEG, PNG and WebP images are allowed."
        )

    filename = f"{uuid4().hex}{extension}"

    file_path = os.path.join(
        UPLOAD_DIR,
        filename
    )

    old_image = quote.image_url
    file_size = 0

    try:
        with open(file_path, "wb") as buffer:
            while True:
                chunk = file.file.read(1024 * 1024)

                if not chunk:
                    break

                file_size += len(chunk)

                if file_size > MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=413,
                        detail="Image size must not exceed 5 MB."
                    )

                buffer.write(chunk)

        if file_size == 0:
            raise HTTPException(
                status_code=400,
                detail="File is empty."
            )

        quote.image_url = file_path

        db.commit()
        db.refresh(quote)

    except Exception:
        db.rollback()

        if os.path.exists(file_path):
            os.remove(file_path)

        raise

    if old_image and old_image != file_path and os.path.exists(old_image):
        os.remove(old_image)

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
        .filter(
            QuoteModel.id == quote_id,
            QuoteModel.is_deleted.is_(False)
        )
        .first()
    )

    if quote is None:
        raise HTTPException(
            status_code=404,
            detail="Quote not found."
        )

    old_image = quote.image_url

    quote.image_url = None

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    if old_image and os.path.exists(old_image):
        os.remove(old_image)

    return {
        "message": "Image deleted successfully."
    }
