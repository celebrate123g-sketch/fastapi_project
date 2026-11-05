
from pydantic import BaseModel


class SimilarQuoteResponse(BaseModel):
    id: int
    author: str
    text: str
    category: str
    likes: int
    views: int
    similarity: float
