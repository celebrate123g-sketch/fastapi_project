from fastapi import HTTPException
from sqlalchemy.orm import Session

from database.models import CommentModel, QuoteModel
from schemas.comment import CommentCreate


def get_comments(
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

    return (
        db.query(CommentModel)
        .filter(CommentModel.quote_id == quote_id)
        .all()
    )


def create_comment(
    db: Session,
    quote_id: int,
    comment: CommentCreate
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

    new_comment = CommentModel(
        quote_id=quote_id,
        author=comment.author,
        text=comment.text
    )

    db.add(new_comment)

    quote.comments_count += 1

    db.commit()
    db.refresh(new_comment)
    create_log(
        db,
        "Created comment",
        quote.id
    )

    return new_comment


def delete_comment(
    db: Session,
    comment_id: int
):
    comment = (
        db.query(CommentModel)
        .filter(CommentModel.id == comment_id)
        .first()
    )

    if comment is None:
        raise HTTPException(
            status_code=404,
            detail="Comment not found."
        )

    quote = (
        db.query(QuoteModel)
        .filter(QuoteModel.id == comment.quote_id)
        .first()
    )

    if quote.comments_count > 0:
        quote.comments_count -= 1

    db.delete(comment)
    create_log(
        db,
        "Deleted comment",
        quote.id
    )
    db.commit()

    return {
        "message": "Comment deleted successfully."
    }