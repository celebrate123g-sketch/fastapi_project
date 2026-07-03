from fastapi import HTTPException
from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from database.models import QuoteModel
from schemas.quote import QuoteCreate, QuoteUpdate


def get_all_quotes(db: Session):
    return db.query(QuoteModel).all()


def get_random_quote(db: Session):
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

    return quote


def get_quote_by_id(
    db: Session,
    quote_id: int
):
    quote = (
        db.query(QuoteModel)
        .filter(QuoteModel.id == quote_id)
        .first()
    )

    if quote is None:
        raise HTTPException(
            status_code=404,
            detail="Quote not found."
        )

    return quote

def increment_views(
    db: Session,
    quote_id: int
):
    quote = get_quote_by_id(
        db,
        quote_id
    )

    quote.views += 1

    db.commit()
    db.refresh(quote)

    return quote


def create_quote(
    db: Session,
    quote: QuoteCreate
):
    new_quote = QuoteModel(
        author=quote.author,
        text=quote.text,
        category=quote.category
    )

    db.add(new_quote)
    db.commit()
    db.refresh(new_quote)

    return new_quote


def update_quote(
    db: Session,
    quote_id: int,
    quote_data: QuoteUpdate
):
    quote = (
        db.query(QuoteModel)
        .filter(QuoteModel.id == quote_id)
        .first()
    )

    if quote is None:
        raise HTTPException(
            status_code=404,
            detail="Quote not found."
        )

    quote.author = quote_data.author
    quote.text = quote_data.text
    quote.category = quote_data.category

    db.commit()
    db.refresh(quote)

    return quote


def delete_quote(
    db: Session,
    quote_id: int
):
    quote = (
        db.query(QuoteModel)
        .filter(QuoteModel.id == quote_id)
        .first()
    )

    if quote is None:
        raise HTTPException(
            status_code=404,
            detail="Quote not found."
        )

    db.delete(quote)
    db.commit()

    return {
        "message": "Quote deleted successfully."
    }


def get_quotes_by_category(
    db: Session,
    category: str
):
    return (
        db.query(QuoteModel)
        .filter(QuoteModel.category == category)
        .all()
    )


def get_favorite_quotes(
    db: Session
):
    return (
        db.query(QuoteModel)
        .filter(QuoteModel.favorite == True)
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
    db.refresh(quote)

    return quote


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
    db.refresh(quote)

    return quote


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
    db.refresh(quote)

    return quote


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
    db.refresh(quote)

    return quote


def get_popular_quotes(
    db: Session
):
    return (
        db.query(QuoteModel)
        .order_by(desc(QuoteModel.likes))
        .all()
    )


def get_most_viewed_quotes(
    db: Session
):
    return (
        db.query(QuoteModel)
        .order_by(desc(QuoteModel.views))
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

    return query.all()