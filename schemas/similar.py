from pydantic import BaseModel


class SimilarQuoteResponse(BaseModel):

    id: int

    author: str

    text: str

    category: str

    similarity: float