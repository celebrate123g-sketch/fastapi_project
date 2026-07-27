from sqlalchemy import func
from sqlalchemy.orm import Session

from database.models import (
    QuoteModel,
    AuthorModel,
    CommentModel,
    ReportModel,
    QuoteRatingModel
)

from services.daily_quote_service import get_daily_quote


def get_dashboard(
    db: Session
):

    total_quotes = (
        db.query(
            func.count(
                QuoteModel.id
            )
        )
        .scalar()
    )

    total_authors = (
        db.query(
            func.count(
                AuthorModel.id
            )
        )
        .scalar()
    )

    total_comments = (
        db.query(
            func.count(
                CommentModel.id
            )
        )
        .scalar()
    )

    total_reports = (
        db.query(
            func.count(
                ReportModel.id
            )
        )
        .scalar()
    )

    total_ratings = (
        db.query(
            func.count(
                QuoteRatingModel.id
            )
        )
        .scalar()
    )

    total_views = (
        db.query(
            func.coalesce(
                func.sum(
                    QuoteModel.views
                ),
                0
            )
        )
        .scalar()
    )

    average_rating = (
        db.query(
            func.avg(
                QuoteRatingModel.rating
            )
        )
        .scalar()
    )

    if average_rating is None:
        average_rating = 0.0

    dashboard = {

        "total_quotes": total_quotes,

        "total_authors": total_authors,

        "total_comments": total_comments,

        "total_views": total_views,

        "total_reports": total_reports,

        "total_ratings": total_ratings,

        "average_rating": round(
            float(average_rating),
            2
        ),

        "quote_of_the_day": get_daily_quote(db)

    }

    return dashboard