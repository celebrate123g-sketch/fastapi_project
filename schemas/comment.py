
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CommentCreate(BaseModel):
    text: str = Field(min_length=1, max_length=1000)


class CommentResponse(BaseModel):
    id: int
    author: str
    text: str
    quote_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
