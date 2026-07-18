from fastapi import HTTPException
from sqlalchemy.orm import Session

from database.models import (
    QuoteModel,
    TagModel,
)


def get_tag_by_id(
    db: Session,
    tag_id: int
):
    tag = (
        db.query(TagModel)
        .filter(
            TagModel.id == tag_id
        )
        .first()
    )

    if tag is None:
        raise HTTPException(
            status_code=404,
            detail="Tag not found."
        )

    return tag


def create_tag(
    db: Session,
    name: str
):
    exists = (
        db.query(TagModel)
        .filter(
            TagModel.name == name
        )
        .first()
    )

    if exists:
        raise HTTPException(
            status_code=400,
            detail="Tag already exists."
        )

    tag = TagModel(
        name=name
    )

    db.add(tag)
    db.commit()
    db.refresh(tag)

    return tag


def get_all_tags(
    db: Session
):
    return (
        db.query(TagModel)
        .order_by(TagModel.name)
        .all()
    )


def delete_tag(
    db: Session,
    tag_id: int
):
    tag = get_tag_by_id(
        db,
        tag_id
    )

    db.delete(tag)
    db.commit()

    return {
        "message": "Tag deleted successfully."
    }

def add_tag_to_quote(
    db: Session,
    quote_id: int,
    tag_id: int
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

    tag = get_tag_by_id(
        db,
        tag_id
    )

    if tag in quote.tags:
        raise HTTPException(
            status_code=400,
            detail="Tag already added."
        )

    quote.tags.append(tag)

    db.commit()
    db.refresh(quote)

    return attach_rating(
    db,
    quote
)


def remove_tag_from_quote(
    db: Session,
    quote_id: int,
    tag_id: int
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

    tag = get_tag_by_id(
        db,
        tag_id
    )

    if tag not in quote.tags:
        raise HTTPException(
            status_code=400,
            detail="Tag is not attached."
        )

    quote.tags.remove(tag)

    db.commit()
    db.refresh(quote)

    return attach_rating(
    db,
    quote
)


def get_quote_tags(
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
).tags