from datetime import date

from fastapi import HTTPException
from sqlalchemy.orm import Session

from database.models import QuoteModel


def get_daily_quote(
    db: Session
):
    quotes = (
        db.query(QuoteModel)
        .order_by(QuoteModel.id)
        .all()
    )

    if not quotes:
        raise HTTPException(
            status_code=404,
            detail="No quotes found."
        )

    today = date.today()

    index = (
        today.toordinal()
        % len(quotes)
    )

    return {
        "date": today,
        "quote": quotes[index]
    }


def get_daily_quote_by_date(
    db: Session,
    target_date: date
):
    quotes = (
        db.query(QuoteModel)
        .order_by(QuoteModel.id)
        .all()
    )

    if not quotes:
        raise HTTPException(
            status_code=404,
            detail="No quotes found."
        )

    index = (
        target_date.toordinal()
        % len(quotes)
    )

    return {
        "date": target_date,
        "quote": quotes[index]
    }