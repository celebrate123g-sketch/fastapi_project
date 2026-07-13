from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db

from schemas.author import (
    AuthorResponse,
    AuthorShortResponse,
    AuthorCategoryResponse,
    RandomAuthorQuote
)

from schemas.quote import QuoteResponse

from services.author_service import (
    get_all_authors,
    get_top_authors,
    get_author,
    get_author_popular_quotes,
    get_author_random_quote,
    get_author_categories
)

router = APIRouter(
    prefix="/authors",
    tags=["Authors"]
)


@router.get(
    "",
    response_model=list[AuthorShortResponse]
)
def authors(
    db: Session = Depends(get_db)
):

    return get_all_authors(db)



@router.get(
    "/top",
    response_model=list[AuthorShortResponse]
)
def top_authors(
    sort: str = "likes",
    db: Session = Depends(get_db)
):

    return get_top_authors(
        db,
        sort
    )



@router.get(
    "/{author}",
    response_model=AuthorResponse
)
def author(
    author: str,
    db: Session = Depends(get_db)
):

    result = get_author(
        db,
        author
    )

    if result is None:

        raise HTTPException(
            status_code=404,
            detail="Author not found."
        )

    return result



@router.get(
    "/{author}/popular",
    response_model=list[QuoteResponse]
)
def popular_quotes(
    author: str,
    db: Session = Depends(get_db)
):

    return get_author_popular_quotes(
        db,
        author
    )



@router.get(
    "/{author}/random",
    response_model=RandomAuthorQuote
)
def random_quote(
    author: str,
    db: Session = Depends(get_db)
):

    quote = get_author_random_quote(
        db,
        author
    )

    if quote is None:

        raise HTTPException(
            status_code=404,
            detail="Author not found."
        )

    return {
        "quote": quote
    }



@router.get(
    "/{author}/categories",
    response_model=list[AuthorCategoryResponse]
)
def categories(
    author: str,
    db: Session = Depends(get_db)
):

    return get_author_categories(
        db,
        author
    )