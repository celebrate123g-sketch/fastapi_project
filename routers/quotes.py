from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from schemas.quote import QuoteCreate, QuoteUpdate
from services.quote_service import (
    get_all_quotes,
    get_random_quote,
    get_quote_by_id,
    create_quote,
    update_quote,
    delete_quote,
    get_quotes_by_category,
    get_favorite_quotes,
    add_to_favorites,
    remove_from_favorites,
    search_quotes
)

router = APIRouter(
    tags=["Quotes"]
)


@router.get("/")
def home():
    return {
        "message": "Quotes API is running!"
    }


@router.get("/quotes")
def read_quotes(
    db: Session = Depends(get_db)
):
    return get_all_quotes(db)


@router.get("/quotes/random")
def random_quote(
    db: Session = Depends(get_db)
):
    return get_random_quote(db)


@router.get("/quotes/{quote_id}")
def read_quote(
    quote_id: int,
    db: Session = Depends(get_db)
):
    return get_quote_by_id(
        db,
        quote_id
    )


@router.post("/quotes")
def add_quote(
    quote: QuoteCreate,
    db: Session = Depends(get_db)
):
    return create_quote(
        db,
        quote
    )


@router.put("/quotes/{quote_id}")
def edit_quote(
    quote_id: int,
    quote: QuoteUpdate,
    db: Session = Depends(get_db)
):
    return update_quote(
        db,
        quote_id,
        quote
    )


@router.delete("/quotes/{quote_id}")
def remove_quote(
    quote_id: int,
    db: Session = Depends(get_db)
):
    return delete_quote(
        db,
        quote_id
    )


@router.get("/quotes/category/{category}")
def category_quotes(
    category: str,
    db: Session = Depends(get_db)
):
    return get_quotes_by_category(
        db,
        category
    )


@router.get("/quotes/favorites")
def favorites(
    db: Session = Depends(get_db)
):
    return get_favorite_quotes(db)


@router.put("/quotes/{quote_id}/favorite")
def favorite(
    quote_id: int,
    db: Session = Depends(get_db)
):
    return add_to_favorites(
        db,
        quote_id
    )


@router.put("/quotes/{quote_id}/unfavorite")
def unfavorite(
    quote_id: int,
    db: Session = Depends(get_db)
):
    return remove_from_favorites(
        db,
        quote_id
    )


@router.get("/quotes/search")
def search(
    author: Optional[str] = None,
    text: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return search_quotes(
        db,
        author,
        text,
        category
    )