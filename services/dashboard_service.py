
from sqlalchemy import func
from sqlalchemy.orm import Session

from database.models import (
    QuoteModel,
    CommentModel,
    ReportModel,
    QuoteRatingModel
)

from services.daily_quote import get_daily_quote


def get_dashboard(db: Session):

    total_quotes = (
        db.query(func.count(QuoteModel.id))
        .filter(QuoteModel.is_deleted.is_(False))
        .scalar()
    )

    total_authors = (
        db.query(func.count(func.distinct(QuoteModel.author)))
        .filter(QuoteModel.is_deleted.is_(False))
        .scalar()
    )

    total_comments = (
        db.query(func.count(CommentModel.id))
        .join(QuoteModel, CommentModel.quote_id == QuoteModel.id)
        .filter(QuoteModel.is_deleted.is_(False))
        .scalar()
    )

    total_reports = (
        db.query(func.count(ReportModel.id))
        .join(QuoteModel, ReportModel.quote_id == QuoteModel.id)
        .filter(QuoteModel.is_deleted.is_(False))
        .scalar()
    )

    total_ratings = (
        db.query(func.count(QuoteRatingModel.id))
        .join(QuoteModel, QuoteRatingModel.quote_id == QuoteModel.id)
        .filter(QuoteModel.is_deleted.is_(False))
        .scalar()
    )

    total_views = (
        db.query(
            func.coalesce(func.sum(QuoteModel.views), 0)
        )
        .filter(QuoteModel.is_deleted.is_(False))
        .scalar()
    )

    average_rating = (
        db.query(
            func.coalesce(func.avg(QuoteRatingModel.rating), 0.0)
        )
        .join(QuoteModel, QuoteRatingModel.quote_id == QuoteModel.id)
        .filter(QuoteModel.is_deleted.is_(False))
        .scalar()
    )

    return {
        "total_quotes": total_quotes,
        "total_authors": total_authors,
        "total_comments": total_comments,
        "total_views": total_views,
        "total_reports": total_reports,
        "total_ratings": total_ratings,
        "average_rating": round(float(average_rating), 2),
        "quote_of_the_day": get_daily_quote(db)
    }
