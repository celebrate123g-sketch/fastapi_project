from fastapi import APIRouter

from schemas.quote import Quote
from services.quote_service import (
    get_all_quotes,
    get_random_quote,
    get_quote_by_id,
    create_quote,
    delete_quote,
    update_quote
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


@router.get("/quotes/{quote_id}")
async def get_quote(quote_id: int):
    return get_quote_by_id(quote_id)


@router.post("/quotes")
async def create_new_quote(quote: Quote):
    return create_quote(
        author=quote.author,
        text=quote.text
    )


@router.put("/quotes/{quote_id}")
async def update_existing_quote(
    quote_id: int,
    quote: Quote
):
    return update_quote(
        quote_id=quote_id,
        author=quote.author,
        text=quote.text
    )


@router.delete("/quotes/{quote_id}")
async def delete_existing_quote(
    quote_id: int
):
    return delete_quote(quote_id)