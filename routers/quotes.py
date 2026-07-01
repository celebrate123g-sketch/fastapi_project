from typing import Optional

from fastapi import APIRouter

from schemas.quote import Quote
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

router = APIRouter()


@router.get("/")
async def home():
    return {
        "message": "Quotes API is running"
    }


@router.get("/quotes")
async def get_quotes():
    return get_all_quotes()


@router.get("/quotes/random")
async def random_quote():
    return get_random_quote()


@router.get("/quotes/category/{category}")
async def quotes_by_category(category: str):
    return get_quotes_by_category(category)


@router.get("/quotes/favorites")
async def favorites():
    return get_favorite_quotes()


@router.get("/quotes/search")
async def search(
    author: Optional[str] = None,
    text: Optional[str] = None
):
    return search_quotes(author, text)


@router.get("/quotes/{quote_id}")
async def get_quote(quote_id: int):
    return get_quote_by_id(quote_id)


@router.post("/quotes")
async def create_new_quote(quote: Quote):
    return create_quote(
        author=quote.author,
        text=quote.text,
        category=quote.category
    )


@router.put("/quotes/{quote_id}")
async def update_existing_quote(
    quote_id: int,
    quote: Quote
):
    return update_quote(
        quote_id=quote_id,
        author=quote.author,
        text=quote.text,
        category=quote.category
    )


@router.put("/quotes/{quote_id}/favorite")
async def favorite_quote(quote_id: int):
    return add_to_favorites(quote_id)


@router.put("/quotes/{quote_id}/unfavorite")
async def unfavorite_quote(quote_id: int):
    return remove_from_favorites(quote_id)


@router.delete("/quotes/{quote_id}")
async def delete_existing_quote(quote_id: int):
    return delete_quote(quote_id)