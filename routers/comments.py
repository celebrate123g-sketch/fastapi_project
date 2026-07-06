from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from schemas.comment import CommentCreate
from services.comment_service import (
    get_comments,
    create_comment,
    delete_comment
)

router = APIRouter(
    tags=["Comments"]
)


@router.get("/quotes/{quote_id}/comments")
def read_comments(
    quote_id: int,
    db: Session = Depends(get_db)
):
    return get_comments(
        db,
        quote_id
    )


@router.post("/quotes/{quote_id}/comments")
def add_comment(
    quote_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db)
):
    return create_comment(
        db,
        quote_id,
        comment
    )


@router.delete("/comments/{comment_id}")
def remove_comment(
    comment_id: int,
    db: Session = Depends(get_db)
):
    return delete_comment(
        db,
        comment_id
    )