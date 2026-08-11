from fastapi import HTTPException
from sqlalchemy.orm import Session

from database.models import CommentModel, QuoteModel
from schemas.comment import CommentCreate

from services.log_service import create_log
from services.notification_service import notify_user


def get_comments(
    db: Session,
    quote_id: int
):

    quote = (
        db.query(
            QuoteModel
        )
        .filter(
            QuoteModel.id == quote_id
        )
        .first()
    )

    if quote is None:

        raise HTTPException(
            status_code=404,
            detail="Quote not found."
        )

    return (
        db.query(
            CommentModel
        )
        .filter(
            CommentModel.quote_id == quote_id
        )
        .all()
    )


def create_comment(
    db: Session,
    quote_id: int,
    comment: CommentCreate
):

    quote = (
        db.query(
            QuoteModel
        )
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

    new_comment = CommentModel(
        quote_id=quote_id,
        author=comment.author,
        text=comment.text
    )

    db.add(
        new_comment
    )

    quote.comments_count += 1

    db.commit()

    db.refresh(
        new_comment
    )

    create_log(
        db,
        "Created comment",
        quote.id
    )

    # Уведомляем владельца цитаты.
    #
    # Важно:
    # QuoteModel должен иметь user_id.
    #
    # Если владелец существует и комментарий
    # оставлен не самим владельцем:

    if (
        quote.user_id is not None
        and quote.author != comment.author
    ):

        notify_user(
            db,
            quote.user_id,
            "Новый комментарий",
            f'К вашей цитате оставили комментарий: "{comment.text}"',
            "comment"
        )

    return new_comment


def delete_comment(
    db: Session,
    comment_id: int
):

    comment = (
        db.query(
            CommentModel
        )
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

    quote = (
        db.query(
            QuoteModel
        )
        .filter(
            QuoteModel.id == comment.quote_id
        )
        .first()
    )

    if quote is not None:

        if quote.comments_count > 0:

            quote.comments_count -= 1

        create_log(
            db,
            "Deleted comment",
            quote.id
        )

    db.delete(
        comment
    )

    db.commit()

    return {
        "message": "Comment deleted successfully."
    }
