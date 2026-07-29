from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from database.database import get_db

from schemas.similar import (
    SimilarQuoteResponse
)

from services.similar_service import (
    get_similar_quotes
)

router = APIRouter(
    prefix="/similar",
    tags=["Similar Quotes"]
)


@router.get(
    "/{quote_id}",
    response_model=list[SimilarQuoteResponse]
)
def similar_quotes(
    quote_id: int,
    limit: int = 5,
    min_similarity: float = 30,
    db: Session = Depends(get_db)
):

    return get_similar_quotes(
        db=db,
        quote_id=quote_id,
        limit=limit,
        min_similarity=min_similarity
    )