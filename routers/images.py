
from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from database.database import get_db
from dependencies.auth import get_current_user
from database.models import QuoteModel, UserModel
from services.image_service import (
    upload_image,
    delete_image
)

router = APIRouter(
    tags=["Images"]
)


def check_quote_access(
    db: Session,
    quote_id: int,
    current_user: UserModel
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
        from fastapi import HTTPException
        raise HTTPException(
            status_code=404,
            detail="Quote not found."
        )

    if quote.user_id != current_user.id and current_user.role != "admin":
        from fastapi import HTTPException
        raise HTTPException(
            status_code=403,
            detail="You cannot modify this quote."
        )


@router.post("/quotes/{quote_id}/image")
def upload_quote_image(
    quote_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    check_quote_access(db, quote_id, current_user)

    return upload_image(
        db,
        quote_id,
        file
    )


@router.delete("/quotes/{quote_id}/image")
def delete_quote_image(
    quote_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    check_quote_access(db, quote_id, current_user)

    return delete_image(
        db,
        quote_id
    )
