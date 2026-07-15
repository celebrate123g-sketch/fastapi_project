from fastapi import HTTPException

from sqlalchemy.orm import Session

from sqlalchemy import desc

from database.models import (
    QuoteHistoryModel,
    QuoteModel
)


def save_quote_history(
    db: Session,
    quote: QuoteModel
):

    history = QuoteHistoryModel(

        quote_id=quote.id,

        author=quote.author,

        text=quote.text,

        category=quote.category,

        image_url=quote.image_url

    )

    db.add(history)

    db.commit()

    db.refresh(history)

    return history



def get_all_history(
    db: Session
):

    return (

        db.query(
            QuoteHistoryModel
        )

        .order_by(
            desc(
                QuoteHistoryModel.created_at
            )
        )

        .all()

    )



def get_quote_history(
    db: Session,
    quote_id: int
):

    return (

        db.query(
            QuoteHistoryModel
        )

        .filter(
            QuoteHistoryModel.quote_id == quote_id
        )

        .order_by(
            desc(
                QuoteHistoryModel.created_at
            )
        )

        .all()

    )



def get_latest_history(
    db: Session,
    quote_id: int
):

    history = (

        db.query(
            QuoteHistoryModel
        )

        .filter(
            QuoteHistoryModel.quote_id == quote_id
        )

        .order_by(
            desc(
                QuoteHistoryModel.created_at
            )
        )

        .first()

    )

    if history is None:

        raise HTTPException(
            status_code=404,
            detail="History not found."
        )

    return history