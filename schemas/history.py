from datetime import datetime

from pydantic import BaseModel, ConfigDict

from schemas.quote import QuoteResponse


class QuoteHistoryResponse(BaseModel):

    id: int

    quote_id: int

    user_id: int | None = None

    viewed_at: datetime

    quote: QuoteResponse

    model_config = ConfigDict(
        from_attributes=True
    )


class LastViewedQuote(BaseModel):

    quote: QuoteResponse

    viewed_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class HistoryStatistics(BaseModel):

    total_views: int

    unique_users: int

    unique_quotes: int

    today_views: int


class UserHistoryResponse(BaseModel):

    user_id: int

    total_views: int

    history: list[QuoteHistoryResponse]


class ClearHistoryResponse(BaseModel):

    message: str