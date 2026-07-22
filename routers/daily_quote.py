from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db

from schemas.daily_quote import DailyQuoteResponse

from services.daily_quote_service import (
    get_daily_quote,
    get_daily_quote_by_date
)

router = APIRouter(
    prefix="/daily-quote",
    tags=["Daily Quote"]
)


@router.get(
    "",
    response_model=DailyQuoteResponse
)
def daily_quote(
    db: Session = Depends(get_db)
):

    return get_daily_quote(db)


@router.get(
    "/{target_date}",
    response_model=DailyQuoteResponse
)
def daily_quote_by_date(
    target_date: date,
    db: Session = Depends(get_db)
):

    return get_daily_quote_by_date(
        db,
        target_date
    )