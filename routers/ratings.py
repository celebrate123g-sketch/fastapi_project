from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.rating_service import (
    rate_quote,
    get_quote_rating,
    get_top_rated_quotes
)

from database.database import get_db

from schemas.rating import (
    RatingCreate,
    RatingResponse,
    RatingStats
)

from services.rating_service import (
    rate_quote,
    get_quote_rating,
    get_top_rated_quotes
)

router = APIRouter(
    prefix="/ratings",
    tags=["Ratings"]
)


@router.post(
    "/quotes/{quote_id}",
    response_model=RatingResponse
)
def rate(
    quote_id: int,
    data: RatingCreate,
    db: Session = Depends(get_db)
):

    result = rate_quote(
        db,
        quote_id,
        data.user_id,
        data.rating
    )

    if result is None:

        raise HTTPException(
            status_code=404,
            detail="Quote not found."
        )

    return result


@router.get(
    "/quotes/{quote_id}",
    response_model=RatingStats
)
def rating(
    quote_id: int,
    db: Session = Depends(get_db)
):

    return get_quote_rating(
        db,
        quote_id
    )


@router.get("/top")
def top_rated(
    limit: int = 10,
    min_votes: int = 5,
    db: Session = Depends(get_db)
):

    return get_top_rated_quotes(
        db,
        limit,
        min_votes
    )