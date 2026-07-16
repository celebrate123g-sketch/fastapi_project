from sqlalchemy import func
from sqlalchemy.orm import Session

from database.models import (
    QuoteModel,
    QuoteRatingModel
)


def rate_quote(
    db: Session,
    quote_id: int,
    user_id: int,
    rating: int
):

    quote = (
        db.query(QuoteModel)
        .filter(QuoteModel.id == quote_id)
        .first()
    )

    if not quote:
        return None

    existing = (
        db.query(QuoteRatingModel)
        .filter(
            QuoteRatingModel.quote_id == quote_id,
            QuoteRatingModel.user_id == user_id
        )
        .first()
    )

    if existing:

        existing.rating = rating

        db.commit()

        db.refresh(existing)

        return existing

    new_rating = QuoteRatingModel(
        user_id=user_id,
        quote_id=quote_id,
        rating=rating
    )

    db.add(new_rating)

    db.commit()

    db.refresh(new_rating)

    return new_rating


def get_quote_rating(
    db: Session,
    quote_id: int
):

    ratings = (
        db.query(QuoteRatingModel)
        .filter(QuoteRatingModel.quote_id == quote_id)
        .all()
    )

    if not ratings:

        return {
            "average_rating": 0.0,
            "votes": 0,
            "five_stars": 0,
            "four_stars": 0,
            "three_stars": 0,
            "two_stars": 0,
            "one_star": 0
        }

    total = sum(item.rating for item in ratings)

    votes = len(ratings)

    return {
        "average_rating": round(total / votes, 2),
        "votes": votes,
        "five_stars": sum(1 for item in ratings if item.rating == 5),
        "four_stars": sum(1 for item in ratings if item.rating == 4),
        "three_stars": sum(1 for item in ratings if item.rating == 3),
        "two_stars": sum(1 for item in ratings if item.rating == 2),
        "one_star": sum(1 for item in ratings if item.rating == 1)
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
        .group_by(QuoteModel.id)
        .having(func.count(QuoteRatingModel.id) >= 1)
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
            "average_rating": round(avg_rating, 2),
            "votes": votes
        }
        for quote, avg_rating, votes in result
    ]