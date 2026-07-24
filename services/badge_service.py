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
        "icon": "🌟"
    },
    {
        "name": "Collector",
        "description": "Create 100 quotes.",
        "icon": "📚"
    },
    {
        "name": "100 Likes",
        "description": "Receive 100 likes.",
        "icon": "❤️"
    },
    {
        "name": "1000 Views",
        "description": "Reach 1000 total views.",
        "icon": "👀"
    },
    {
        "name": "Top Rated",
        "description": "Average rating is at least 4.8.",
        "icon": "⭐"
    },
    {
        "name": "Active Author",
        "description": "Receive 50 comments.",
        "icon": "💬"
    },
    {
        "name": "Legend",
        "description": "Reach 10000 total views.",
        "icon": "🏆"
    }
]


def get_all_badges():
    return BADGES


def get_user_badges(
    db: Session,
    user_id: int
):

    quotes = (
        db.query(QuoteModel)
        .filter(
            QuoteModel.user_id == user_id
        )
        .all()
    )

    quote_ids = [
        quote.id
        for quote in quotes
    ]

    total_quotes = len(quotes)

    total_views = sum(
        quote.views
        for quote in quotes
    )

    total_likes = (
        db.query(
            func.count(
                QuoteLikeModel.id
            )
        )
        .filter(
            QuoteLikeModel.quote_id.in_(quote_ids)
        )
        .scalar()
        if quote_ids else 0
    )

    total_comments = (
        db.query(
            func.count(
                CommentModel.id
            )
        )
        .filter(
            CommentModel.quote_id.in_(quote_ids)
        )
        .scalar()
        if quote_ids else 0
    )

    average_rating = (
        db.query(
            func.avg(
                QuoteRatingModel.rating
            )
        )
        .filter(
            QuoteRatingModel.quote_id.in_(quote_ids)
        )
        .scalar()
        if quote_ids else None
    )

    badges = [

        {
            "name": "First Quote",
            "description": "Create your first quote.",
            "icon": "🌟",
            "unlocked": total_quotes >= 1
        },

        {
            "name": "Collector",
            "description": "Create 100 quotes.",
            "icon": "📚",
            "unlocked": total_quotes >= 100
        },

        {
            "name": "100 Likes",
            "description": "Receive 100 likes.",
            "icon": "❤️",
            "unlocked": total_likes >= 100
        },

        {
            "name": "1000 Views",
            "description": "Reach 1000 total views.",
            "icon": "👀",
            "unlocked": total_views >= 1000
        },

        {
            "name": "Top Rated",
            "description": "Average rating is at least 4.8.",
            "icon": "⭐",
            "unlocked": (
                average_rating is not None
                and average_rating >= 4.8
            )
        },

        {
            "name": "Active Author",
            "description": "Receive 50 comments.",
            "icon": "💬",
            "unlocked": total_comments >= 50
        },

        {
            "name": "Legend",
            "description": "Reach 10000 total views.",
            "icon": "🏆",
            "unlocked": total_views >= 10000
        }

    ]

    return badges


def get_quote_badges(
    db: Session,
    quote_id: int
):

    quote = (
        db.query(QuoteModel)
        .filter(
            QuoteModel.id == quote_id
        )
        .first()
    )

    if quote is None:
        return None

    likes = (
        db.query(
            func.count(
                QuoteLikeModel.id
            )
        )
        .filter(
            QuoteLikeModel.quote_id == quote_id
        )
        .scalar()
    )

    comments = (
        db.query(
            func.count(
                CommentModel.id
            )
        )
        .filter(
            CommentModel.quote_id == quote_id
        )
        .scalar()
    )

    rating = (
        db.query(
            func.avg(
                QuoteRatingModel.rating
            )
        )
        .filter(
            QuoteRatingModel.quote_id == quote_id
        )
        .scalar()
    )

    return [

        {
            "name": "Popular",
            "description": "1000 views.",
            "icon": "👀",
            "unlocked": quote.views >= 1000
        },

        {
            "name": "Loved",
            "description": "100 likes.",
            "icon": "❤️",
            "unlocked": likes >= 100
        },

        {
            "name": "Top Rated",
            "description": "Rating 4.8 or higher.",
            "icon": "⭐",
            "unlocked": (
                rating is not None
                and rating >= 4.8
            )
        },

        {
            "name": "Discussed",
            "description": "50 comments.",
            "icon": "💬",
            "unlocked": comments >= 50
        }

    ]


def get_badge_statistics(
    db: Session,
    user_id: int
):

    badges = get_user_badges(
        db,
        user_id
    )

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