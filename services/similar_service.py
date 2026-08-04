from fastapi import HTTPException

from sqlalchemy.orm import Session

from database.models import QuoteModel

from services.duplicate_service import calculate_similarity


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

            result.append(
                {
                    "id": quote.id,
                    "author": quote.author,
                    "text": quote.text,
                    "category": quote.category,
                    "likes": quote.likes,
                    "views": quote.views,
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