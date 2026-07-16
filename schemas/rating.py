from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class RatingCreate(BaseModel):

    user_id: int

    rating: int = Field(
        ge=1,
        le=5
    )


class RatingResponse(BaseModel):

    id: int

    user_id: int

    quote_id: int

    rating: int

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class RatingStats(BaseModel):

    average_rating: float

    votes: int

    five_stars: int

    four_stars: int

    three_stars: int

    two_stars: int

    one_star: int