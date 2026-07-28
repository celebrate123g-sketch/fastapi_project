from datetime import datetime

from pydantic import BaseModel, ConfigDict

from schemas.quote import QuoteResponse


class TrashQuoteResponse(BaseModel):

    id: int

    deleted_at: datetime

    quote: QuoteResponse

    model_config = ConfigDict(
        from_attributes=True
    )


class TrashResponse(BaseModel):

    message: str