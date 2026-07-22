from datetime import date

from pydantic import BaseModel, ConfigDict

from schemas.quote import QuoteResponse


class DailyQuoteResponse(BaseModel):

    date: date

    quote: QuoteResponse

    model_config = ConfigDict(
        from_attributes=True
    )