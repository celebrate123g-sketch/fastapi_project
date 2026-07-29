from difflib import SequenceMatcher

from fastapi import HTTPException

from sqlalchemy.orm import Session

from database.models import QuoteModel

from services.quote_service import attach_rating


def calculate_similarity(
    text1: str,
    text2: str
) -> float:

    return round(
        SequenceMatcher(
            None,
            text1.lower(),
            text2.lower()
        ).ratio() * 100,
        2
    )


def get_similar_quotes(
    db: Session,
    quote_id: int,
    limit: int = 5,
    min_similarity: float = 30
):

    original = (
        db.query(QuoteModel)
        .filter(
            QuoteModel.id == quote_id,
            QuoteModel.is_deleted == False
        )
        .first()
    )

    if original is None:

        raise HTTPException(
            status_code=404,
            detail="Quote not found."
        )

    quotes = (
        db.query(QuoteModel)
        .filter(
            QuoteModel.id != quote_id,
            QuoteModel.is_deleted == False
        )
        .all()
    )

    result = []

    for quote in quotes:

        similarity = calculate_similarity(
            original.text,
            quote.text
        )

        if quote.category == original.category:
            similarity += 10

        if quote.author == original.author:
            similarity += 5

        similarity = min(
            similarity,
            100
        )

        if similarity >= min_similarity:

            rated_quote = attach_rating(
                db,
                quote
            )

            result.append(

                {
                    "id": rated_quote.id,
                    "author": rated_quote.author,
                    "text": rated_quote.text,
                    "category": rated_quote.category,
                    "similarity": round(
                        similarity,
                        2
                    )
                }

            )

    result.sort(
        key=lambda item: item["similarity"],
        reverse=True
    )

    return result[:limit]