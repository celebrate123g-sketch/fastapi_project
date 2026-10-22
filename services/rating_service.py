
from sqlalchemy import func
from sqlalchemy.orm import Session

from database.models import QuoteModel, QuoteRatingModel
from services.notification_service import notify_user


def rate_quote(
    db: Session,
    quote_id: int,
    user_id: int,
    rating: int
):
    if rating < 1 or rating > 5:
        raise ValueError("Rating must be between 1 and 5.")

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

    existing = (
        db.query(QuoteRatingModel)
        .filter(
            QuoteRatingModel.quote_id == quote_id,
            QuoteRatingModel.user_id == user_id
        )
        .first()
    )

    is_new_rating = existing is None

    if existing:
        existing.rating = rating
    else:
        db.add(
            QuoteRatingModel(
                user_id=user_id,
                quote_id=quote_id,
                rating=rating
            )
        )

    db.commit()

    if (
        is_new_rating
        and quote.user_id is not None
        and quote.user_id != user_id
    ):
        notify_user(
            db,
            quote.user_id,
            "Новая оценка",
            f"Вашу цитату оценили на {rating}/5.",
            "rating"
        )

    return get_quote_rating(db, quote_id)


def get_quote_rating(
    db: Session,
    quote_id: int
):
    result = (
        db.query(
            func.avg(QuoteRatingModel.rating),
            func.count(QuoteRatingModel.id),
            func.sum(
                (QuoteRatingModel.rating == 5).cast(db.bind.dialect.type_descriptor(func.count(QuoteRatingModel.id).type))
            )
        )
        .filter(QuoteRatingModel.quote_id == quote_id)
        .first()
    )

    ratings = (
        db.query(QuoteRatingModel.rating)
        .filter(QuoteRatingModel.quote_id == quote_id)
        .all()
    )

    values = [item.rating for item in ratings]
    votes = len(values)

    return {
        "average_rating": round(sum(values) / votes, 2) if votes else 0.0,
        "votes": votes,
        "five_stars": values.count(5),
        "four_stars": values.count(4),
        "three_stars": values.count(3),
        "two_stars": values.count(2),
        "one_star": values.count(1)
    }


def get_top_rated_quotes(
    db: Session,
    limit: int = 10
):
    result = (
        db.query(
            QuoteModel,
            func.avg(QuoteRatingModel.rating).label("avg_rating"),
            func.count(QuoteRatingModel.id).label("votes")
        )
        .join(
            QuoteRatingModel,
            QuoteRatingModel.quote_id == QuoteModel.id
        )
        .filter(QuoteModel.is_deleted == False)
        .group_by(QuoteModel.id)
        .order_by(
            func.avg(QuoteRatingModel.rating).desc(),
            func.count(QuoteRatingModel.id).desc()
        )
        .limit(limit)
        .all()
    )

    return [
        {
            "quote": quote,
            "average_rating": round(float(avg_rating), 2),
            "votes": votes
        }
        for quote, avg_rating, votes in result
    ]


def get_top_rated_quotes_min_votes(
    db: Session,
    limit: int = 10,
    min_votes: int = 5
):
    result = (
        db.query(
            QuoteModel,
            func.avg(QuoteRatingModel.rating).label("avg_rating"),
            func.count(QuoteRatingModel.id).label("votes")
        )
        .join(
            QuoteRatingModel,
            QuoteRatingModel.quote_id == QuoteModel.id
        )
        .filter(QuoteModel.is_deleted == False)
        .group_by(QuoteModel.id)
        .having(
            func.count(QuoteRatingModel.id) >= min_votes
        )
        .order_by(
            func.avg(QuoteRatingModel.rating).desc(),
            func.count(QuoteRatingModel.id).desc()
        )
        .limit(limit)
        .all()
    )

    return [
        {
            "quote": quote,
            "average_rating": round(float(avg_rating), 2),
            "votes": votes
        }
        for quote, avg_rating, votes in result
    ]
