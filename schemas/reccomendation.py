from pydantic import BaseModel


class RecommendationResponse(BaseModel):

    id: int

    text: str

    author: str

    category: str

    score: int

    reason: str



class SimilarQuoteResponse(BaseModel):

    id: int

    text: str

    author: str

    category: str

    similarity: int