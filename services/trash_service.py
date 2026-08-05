from datetime import datetime

from sqlalchemy.orm import Session

from database.models import QuoteModel

from datetime import timedelta

def get_trash(
    db: Session
):

    return (
        db.query(QuoteModel)
        .filter(
            QuoteModel.is_deleted == True
        )
        .order_by(
            QuoteModel.deleted_at.desc()
        )
        .all()
    )


def get_deleted_quote(
    db: Session,
    quote_id: int
):

    return (
        db.query(QuoteModel)
        .filter(
            QuoteModel.id == quote_id,
            QuoteModel.is_deleted == True
        )
        .first()
    )


def move_to_trash(
    db: Session,
    quote_id: int
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
        return None

    quote.is_deleted = True
    quote.deleted_at = datetime.utcnow()

    db.commit()
    db.refresh(quote)

    return quote


def restore_quote(
    db: Session,
    quote_id: int
):

    quote = get_deleted_quote(
        db,
        quote_id
    )

    if quote is None:
        return None

    quote.is_deleted = False
    quote.deleted_at = None

    db.commit()
    db.refresh(quote)

    return quote


def delete_forever(
    db: Session,
    quote_id: int
):

    quote = get_deleted_quote(
        db,
        quote_id
    )

    if quote is None:
        return False

    db.delete(quote)
    db.commit()

    return True


def empty_trash(
    db: Session
):

    (
        db.query(QuoteModel)
        .filter(
            QuoteModel.is_deleted == True
        )
        .delete()
    )

    db.commit()

    return {
        "message": "Trash emptied successfully."
    }

AUTO_DELETE_DAYS = 30


def auto_delete_old_quotes(
    db: Session,
    days: int = AUTO_DELETE_DAYS
):

    border = datetime.utcnow() - timedelta(
        days=days
    )

    quotes = (
        db.query(QuoteModel)
        .filter(
            QuoteModel.is_deleted == True,
            QuoteModel.deleted_at != None,
            QuoteModel.deleted_at <= border
        )
        .all()
    )

    deleted = 0

    for quote in quotes:

        db.delete(
            quote
        )

        deleted += 1

    db.commit()

    return {
        "deleted": deleted,
        "days": days
    }