from fastapi import HTTPException

from sqlalchemy import desc, func

from sqlalchemy.orm import Session

from sqlalchemy import func

from database.models import (
    QuoteModel,
    QuoteViewModel,
    QuoteRatingModel
)

from schemas.quote import (
    QuoteCreate,
    QuoteUpdate
)

from services.log_service import create_log

from services.history_service import save_quote_history

def get_all_quotes(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    sort: str = "newest"
):
    query = db.query(QuoteModel)

    if sort == "newest":
        query = query.order_by(
            desc(QuoteModel.created_at)
        )

    elif sort == "oldest":
        query = query.order_by(
            QuoteModel.created_at
        )

    elif sort == "likes":
        query = query.order_by(
            desc(QuoteModel.likes)
        )

    elif sort == "views":
        query = query.order_by(
            desc(QuoteModel.views)
        )

    elif sort == "rating":

        quotes = query.all()

        quotes = sorted(

            quotes,

            key=lambda quote: (

                    db.query(
                        func.avg(
                            QuoteRatingModel.rating
                        )
                    )
                    .filter(
                        QuoteRatingModel.quote_id == quote.id
                    )
                    .scalar()

                    or 0

            ),

            reverse=True

        )

        quotes = quotes[
                 skip:skip + limit
                 ]

        return [
            attach_rating(
                db,
                quote
            )
            for quote in quotes
        ]

    elif sort == "author":
        query = query.order_by(
            QuoteModel.author
        )

    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid sort type."
        )

    return (
        query
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_random_quote(
    db: Session
):
    quote = (
        db.query(QuoteModel)
        .order_by(func.random())
        .first()
    )

    if quote is None:
        raise HTTPException(
            status_code=404,
            detail="No quotes found."
        )

    return attach_rating(
    db,
    quote
)


def get_quote_by_id(
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
        raise HTTPException(
            status_code=404,
            detail="Quote not found."
        )

    return attach_rating(
    db,
    quote
)


def increment_views(
    db,
    quote_id
):
    quote = (
        db.query(QuoteModel)
        .filter(
            QuoteModel.id == quote_id
        )
        .first()
    )

    if not quote:
        return None

    quote.views += 1

    view = QuoteViewModel(
        quote_id=quote_id
    )

    quote.views += 1

    view = QuoteViewModel(
        quote_id=quote_id
    )

    db.add(
        view
    )

    db.commit()

    db.refresh(
        quote
    )

    save_quote_history(
        db,
        quote
    )

    return attach_rating(
    db,
    quote
)


def create_quote(
    db: Session,
    quote: QuoteCreate
):

    new_quote = QuoteModel(

        author=quote.author,

        text=quote.text,

        category=quote.category

    )

    db.add(
        new_quote
    )

    db.commit()

    db.refresh(
        new_quote
    )

    create_log(
        db,
        "Created quote",
        new_quote.id
    )

    return new_quote


def update_quote(
    db: Session,
    quote_id: int,
    quote_data: QuoteUpdate
):

    quote = get_quote_by_id(
        db,
        quote_id
    )

    save_quote_history(
        db,
        quote
    )

    quote.author = quote_data.author
    quote.text = quote_data.text
    quote.category = quote_data.category

    db.commit()

    db.refresh(
        quote
    )

    create_log(
        db,
        "Updated quote",
        quote.id
    )

    return attach_rating(
    db,
    quote
)


def delete_quote(
    db: Session,
    quote_id: int
):

    quote = get_quote_by_id(
        db,
        quote_id
    )

    save_quote_history(
        db,
        quote
    )

    db.delete(
        quote
    )

    db.commit()

    create_log(
        db,
        "Deleted quote",
        quote_id
    )

    return {
        "message": "Quote deleted successfully."
    }

    db.commit()

    create_log(
        db,
        "Deleted quote",
        quote_id
    )

    return {
        "message": "Quote deleted successfully."
    }


def get_quotes_by_category(
    db: Session,
    category: str
):

    return (

        db.query(
            QuoteModel
        )

        .filter(
            QuoteModel.category == category
        )

        .all()

    )


def get_favorite_quotes(
    db: Session
):

    return (

        db.query(
            QuoteModel
        )

        .filter(
            QuoteModel.favorite == True
        )

        .all()

    )


def add_to_favorites(
    db: Session,
    quote_id: int
):

    quote = get_quote_by_id(
        db,
        quote_id
    )

    quote.favorite = True

    db.commit()

    db.refresh(
        quote
    )

    create_log(
        db,
        "Added to favorites",
        quote.id
    )

    return attach_rating(
    db,
    quote
)


def remove_from_favorites(
    db: Session,
    quote_id: int
):

    quote = get_quote_by_id(
        db,
        quote_id
    )

    quote.favorite = False

    db.commit()

    db.refresh(
        quote
    )

    create_log(
        db,
        "Removed from favorites",
        quote.id
    )

    return attach_rating(
    db,
    quote
)


def like_quote(
    db: Session,
    quote_id: int
):

    quote = get_quote_by_id(
        db,
        quote_id
    )

    quote.likes += 1

    db.commit()

    db.refresh(
        quote
    )

    create_log(
        db,
        "Liked quote",
        quote.id
    )

    return attach_rating(
    db,
    quote
)


def unlike_quote(
    db: Session,
    quote_id: int
):

    quote = get_quote_by_id(
        db,
        quote_id
    )

    if quote.likes > 0:

        quote.likes -= 1

    db.commit()

    db.refresh(
        quote
    )

    create_log(
        db,
        "Removed like",
        quote.id
    )

    return attach_rating(
    db,
    quote
)


def get_popular_quotes(
    db: Session
):

    return (

        db.query(
            QuoteModel
        )

        .order_by(
            desc(
                QuoteModel.likes
            )
        )

        .all()

    )

def get_most_viewed_quotes(
    db: Session
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

        .all()

    )


def search_quotes(
    db: Session,
    author: str | None = None,
    text: str | None = None,
    category: str | None = None
):
    query = db.query(QuoteModel)

    if author:
        query = query.filter(
            QuoteModel.author.ilike(f"%{author}%")
        )

    if text:
        query = query.filter(
            QuoteModel.text.ilike(f"%{text}%")
        )

    if category:
        query = query.filter(
            QuoteModel.category == category
        )

    quotes = query.all()

    return [
        attach_rating(db, quote)
        for quote in quotes
    ]


def get_trending_quotes(
    db: Session
):

    quotes = (

        db.query(
            QuoteModel
        )

        .all()

    )

    quotes.sort(

        key=lambda quote: (

            quote.likes * 3

            + quote.views * 0.1

            + quote.comments_count * 5

        ),

        reverse=True

    )

    return attach_rating(
    db,
    quote
)

def attach_rating(
    db: Session,
    quote: QuoteModel
):

    average = (
        db.query(
            func.avg(
                QuoteRatingModel.rating
            )
        )
        .filter(
            QuoteRatingModel.quote_id == quote.id
        )
        .scalar()
    )

    count = (
        db.query(
            func.count(
                QuoteRatingModel.id
            )
        )
        .filter(
            QuoteRatingModel.quote_id == quote.id
        )
        .scalar()
    )

    quote.average_rating = round(
        average or 0,
        2
    )

    quote.ratings_count = count or 0

    return attach_rating(
    db,
    quote
)