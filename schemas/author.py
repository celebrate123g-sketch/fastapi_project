from pydantic import BaseModel, ConfigDict

from schemas.quote import QuoteResponse


class AuthorStats(BaseModel):

    quotes: int

    likes: int

    views: int

    favorites: int

    comments: int



class AuthorResponse(BaseModel):

    author: str

    statistics: AuthorStats

    quotes: list[QuoteResponse]



class AuthorShortResponse(BaseModel):

    author: str

    quotes: int

    likes: int

    views: int

    favorites: int



class AuthorCategoryResponse(BaseModel):

    category: str

    quotes: int



class RandomAuthorQuote(BaseModel):

    quote: QuoteResponse

    model_config = ConfigDict(
        from_attributes=True
    )