
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import CommentModel, QuoteModel, UserModel
from dependencies.auth import get_current_user


router = APIRouter(tags=["Comments"])


@router.get("/quotes/{quote_id}/comments")
def get_comments(
    quote_id: int,
    db: Session = Depends(get_db)
):
    quote = (
        db.query(QuoteModel)
        .filter(
            QuoteModel.id == quote_id,
            QuoteModel.is_deleted == False
        )
        .first()
    )

    if quote is None:
        raise HTTPException(
            status_code=404,
            detail="Quote not found."
        )

    comments = (
        db.query(CommentModel)
        .filter(
            CommentModel.quote_id == quote_id
        )
        .order_by(CommentModel.created_at.asc())
        .all()
    )

    return [
        {
            "id": comment.id,
            "quote_id": comment.quote_id,
            "author": comment.author,
            "text": comment.text,
            "created_at": comment.created_at
        }
        for comment in comments
    ]


@router.post("/quotes/{quote_id}/comments")
def add_comment(
    quote_id: int,
    data: dict,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    text = data.get("text")

    if not isinstance(text, str) or not text.strip():
        raise HTTPException(
            status_code=400,
            detail="Comment text cannot be empty."
        )

    if len(text) > 1000:
        raise HTTPException(
            status_code=400,
            detail="Comment is too long."
        )

    quote = (
        db.query(QuoteModel)
        .filter(
            QuoteModel.id == quote_id,
            QuoteModel.is_deleted == False
        )
        .first()
    )

    if quote is None:
        raise HTTPException(
            status_code=404,
            detail="Quote not found."
        )

    comment = CommentModel(
        quote_id=quote_id,
        author=current_user.username,
        text=text.strip()
    )

    db.add(comment)
    quote.comments_count += 1
    db.commit()
    db.refresh(comment)

    return {
        "id": comment.id,
        "quote_id": comment.quote_id,
        "author": comment.author,
        "text": comment.text,
        "created_at": comment.created_at
    }


@router.delete("/comments/{comment_id}")
def delete_comment(
    comment_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    comment = (
        db.query(CommentModel)
        .filter(
            CommentModel.id == comment_id
        )
        .first()
    )

    if comment is None:
        raise HTTPException(
            status_code=404,
            detail="Comment not found."
        )

    if comment.author != current_user.username:
        raise HTTPException(
            status_code=403,
            detail="You can only delete your own comments."
        )

    quote = (
        db.query(QuoteModel)
        .filter(
            QuoteModel.id == comment.quote_id
        )
        .first()
    )

    if quote and quote.comments_count > 0:
        quote.comments_count -= 1

    db.delete(comment)
    db.commit()

    return {
        "message": "Comment deleted successfully."
    }
