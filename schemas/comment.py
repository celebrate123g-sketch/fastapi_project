from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CommentBase(BaseModel):
    author: str = Field(
        min_length=2,
        max_length=100
    )

    text: str = Field(
        min_length=1,
        max_length=1000
    )


class CommentCreate(CommentBase):
    pass


class CommentResponse(CommentBase):
    id: int

    quote_id: int

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )