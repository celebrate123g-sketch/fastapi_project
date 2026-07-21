from datetime import date

from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from database.models import (
    QuoteModel,
    QuoteViewModel
)


def save_quote_history(
    db: Session,
    quote: QuoteModel,
    user_id: int | None = None
):

    history = QuoteViewModel(
        quote_id=quote.id,
        user_id=user_id
    )

    db.add(history)
    db.commit()

    return history


def get_recent_history(
    db: Session,
    limit: int = 20
):

    return (

        db.query(
            QuoteViewModel
        )

        .order_by(
            desc(
                QuoteViewModel.created_at
            )
        )

        .limit(limit)

        .all()

    )


def get_user_history(
    db: Session,
    user_id: int
):

    history = (

        db.query(
            QuoteViewModel
        )

        .filter(
            QuoteViewModel.user_id == user_id
        )

        .order_by(
            desc(
                QuoteViewModel.created_at
            )
        )

        .all()

    )

    return {

        "user_id": user_id,

        "total_views": len(history),

        "history": history

    }


def get_last_viewed(
    db: Session
):

    history = (

        db.query(
            QuoteViewModel
        )

        .order_by(
            desc(
                QuoteViewModel.created_at
            )
        )

        .first()

    )

    if history is None:
        return None

    return {

        "quote": history.quote,

        "viewed_at": history.created_at

    }


def clear_user_history(
    db: Session,
    user_id: int
):

    (

        db.query(
            QuoteViewModel
        )

        .filter(
            QuoteViewModel.user_id == user_id
        )

        .delete()

    )

    db.commit()

    return {

        "message": "History cleared successfully."

    }


def get_most_viewed(
    db: Session,
    limit: int = 10
):

    return (

        db.query(
            QuoteModel
        )

        .order_by(
            desc(
                QuoteModel.views
            )
        )

        .limit(limit)

        .all()

    )


def get_history_statistics(
    db: Session
):

    total_views = (

        db.query(
            func.count(
                QuoteViewModel.id
            )
        )

        .scalar()

    )

    unique_users = (

        db.query(
            func.count(
                func.distinct(
                    QuoteViewModel.user_id
                )
            )
        )

        .scalar()

    )

    unique_quotes = (

        db.query(
            func.count(
                func.distinct(
                    QuoteViewModel.quote_id
                )
            )
        )

        .scalar()

    )

    today = date.today()

    today_views = (

        db.query(
            func.count(
                QuoteViewModel.id
            )
        )

        .filter(
            func.date(
                QuoteViewModel.created_at
            ) == today
        )

        .scalar()

    )

    return {

        "total_views": total_views,

        "unique_users": unique_users,

        "unique_quotes": unique_quotes,

        "today_views": today_views

    }