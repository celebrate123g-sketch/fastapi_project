from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class QuoteBase(BaseModel):
    author: str = Field(
        min_length=2,
        max_length=100
    )

    text: str = Field(
        min_length=10,
        max_length=1000
    )

    category: Literal[
        "Motivation",
        "Business",
        "Philosophy",
        "Life",
        "Success"
    ]


class QuoteCreate(QuoteBase):
    pass


class QuoteUpdate(QuoteBase):
    pass


class QuoteResponse(QuoteBase):
    id: int

    favorite: bool

    likes: int
    views: int
    comments_count: int

    image_url: str | None = None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )