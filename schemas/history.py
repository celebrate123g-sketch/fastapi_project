from datetime import datetime

from pydantic import BaseModel, ConfigDict


class QuoteHistoryBase(BaseModel):

    quote_id: int

    author: str

    text: str

    category: str

    image_url: str | None = None



class QuoteHistoryResponse(QuoteHistoryBase):

    id: int

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )