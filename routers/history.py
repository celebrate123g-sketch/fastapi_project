from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from database.database import get_db

from schemas.history import QuoteHistoryResponse

from services.history_service import (
    get_all_history,
    get_quote_history,
    get_latest_history
)


router = APIRouter(
    prefix="/history",
    tags=["History"]
)


@router.get(
    "",
    response_model=list[QuoteHistoryResponse]
)
def history(
    db: Session = Depends(get_db)
):

    return get_all_history(db)



@router.get(
    "/{quote_id}",
    response_model=list[QuoteHistoryResponse]
)
def quote_history(
    quote_id: int,
    db: Session = Depends(get_db)
):

    return get_quote_history(
        db,
        quote_id
    )



@router.get(
    "/{quote_id}/latest",
    response_model=QuoteHistoryResponse
)
def latest_history(
    quote_id: int,
    db: Session = Depends(get_db)
):

    return get_latest_history(
        db,
        quote_id
    )