
from sqlalchemy import func
from sqlalchemy.orm import Session

from database.models import (
    QuoteModel,
    CommentModel,
    QuoteLikeModel,
    QuoteRatingModel
)


BADGES = [
    {
        "name": "First Quote",
        "description": "Create your first quote.",
        "icon": "🌟",
        "type": "user"
    },
    {
        "name": "Collector",
        "description": "Create 100 quotes.",
        "icon": "📚",
        "type": "user"
    },
    {
        "name": "100 Likes",
        "description": "Receive 100 likes.",
        "icon": "❤️",
        "type": "user"
    },
    {
        "name": "1000 Views",
        "description": "Reach 1000 total views.",
        "icon": "👀",
        "type": "user"
    },
    {
        "name": "Top Rated",
        "description": "Average rating is at least 4.8.",
        "icon": "⭐",
        "type": "user"
    },
    {
        "name": "Active Author",
        "description": "Receive 50 comments.",
        "icon": "💬",
        "type": "user"
    },
    {
        "name": "Legend",
        "description": "Reach 10000 total views.",
        "icon": "🏆",
        "type": "user"
    }
]


QUOTE_BADGES = [
    {
        "name": "Popular",
        "description": "1000 views.",
        "icon": "👀"
    },
    {
        "name": "Loved",
        "description": "100 likes.",
        "icon": "❤️"
    },
    {
        "name": "Top Rated",
        "description": "Rating 4.8 or higher.",
        "icon": "⭐"
    },
    {
        "name": "Discussed",
        "description": "50 comments.",
        "icon": "💬"
    }
]


def get_all_badges():
    return [
        {key: value for key, value in badge.items() if key != "type"}
        for badge in BADGES
    ]


def get_user_badges(
    db: Session,
    user_id: int
):
    quotes_query = (
        db.query(QuoteModel)
        .filter(
            QuoteModel.user_id == user_id,
            QuoteModel.is_deleted.is_(False)
        )
    )

    total_quotes = quotes_query.count()

    total_views = (
        db.query(func.coalesce(func.sum(QuoteModel.views), 0))
        .filter(
            QuoteModel.user_id == user_id,
            QuoteModel.is_deleted.is_(False)
        )
        .scalar()
    )

    quote_ids = (
        db.query(QuoteModel.id)
        .filter(
            QuoteModel.user_id == user_id,
            QuoteModel.is_deleted.is_(False)
        )
        .subquery()
    )

    total_likes = (
        db.query(func.count(QuoteLikeModel.id))
        .filter(QuoteLikeModel.quote_id.in_(quote_ids))
        .scalar()
    )

    total_comments = (
        db.query(func.count(CommentModel.id))
        .filter(CommentModel.quote_id.in_(quote_ids))
        .scalar()
    )

    average_rating = (
        db.query(func.avg(QuoteRatingModel.rating))
        .filter(QuoteRatingModel.quote_id.in_(quote_ids))
        .scalar()
    )

    values = {
        "total_quotes": total_quotes,
        "total_views": total_views,
        "total_likes": total_likes,
        "total_comments": total_comments,
        "average_rating": average_rating
    }

    badges = []

    for badge in BADGES:
        unlocked = False

        if badge["name"] == "First Quote":
            unlocked = total_quotes >= 1
        elif badge["name"] == "Collector":
            unlocked = total_quotes >= 100
        elif badge["name"] == "100 Likes":
            unlocked = total_likes >= 100
        elif badge["name"] == "1000 Views":
            unlocked = total_views >= 1000
        elif badge["name"] == "Top Rated":
            unlocked = (
                average_rating is not None
                and average_rating >= 4.8
            )
        elif badge["name"] == "Active Author":
            unlocked = total_comments >= 50
        elif badge["name"] == "Legend":
            unlocked = total_views >= 10000

        badges.append({
            "name": badge["name"],
            "description": badge["description"],
            "icon": badge["icon"],
            "unlocked": unlocked
        })

    return badges


def get_quote_badges(
    db: Session,
    quote_id: int
):
    quote = (
        db.query(QuoteModel)
        .filter(
            QuoteModel.id == quote_id,
            QuoteModel.is_deleted.is_(False)
        )
        .first()
    )

    if quote is None:
        return None

    likes = (
        db.query(func.count(QuoteLikeModel.id))
        .filter(QuoteLikeModel.quote_id == quote_id)
        .scalar()
    )

    comments = (
        db.query(func.count(CommentModel.id))
        .filter(CommentModel.quote_id == quote_id)
        .scalar()
    )

    rating = (
        db.query(func.avg(QuoteRatingModel.rating))
        .filter(QuoteRatingModel.quote_id == quote_id)
        .scalar()
    )

    unlocked_values = {
        "Popular": quote.views >= 1000,
        "Loved": likes >= 100,
        "Top Rated": rating is not None and rating >= 4.8,
        "Discussed": comments >= 50
    }

    return [
        {
            **badge,
            "unlocked": unlocked_values[badge["name"]]
        }
        for badge in QUOTE_BADGES
    ]


def get_badge_statistics(
    db: Session,
    user_id: int
):
    badges = get_user_badges(db, user_id)

    unlocked = sum(
        1
        for badge in badges
        if badge["unlocked"]
    )

    return {
        "total_badges": len(badges),
        "unlocked_badges": unlocked,
        "locked_badges": len(badges) - unlocked
    }
