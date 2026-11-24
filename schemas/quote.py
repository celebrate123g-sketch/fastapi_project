
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


Language = Literal["ru", "en", "uz"]


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
    language: Language = "ru"


class QuoteUpdate(QuoteBase):
    language: Language = "ru"


class QuoteTranslationResponse(BaseModel):
    language: Language
    text: str

    model_config = ConfigDict(
        from_attributes=True
    )


class QuoteResponse(QuoteBase):
    id: int

    language: Language
    localized_text: str | None = None
    translations: list[QuoteTranslationResponse] = []

    favorite: bool

    likes: int
    views: int
    comments_count: int

    average_rating: float = 0
    ratings_count: int = 0

    image_url: str | None = None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
