import random

from fastapi import HTTPException

from database.database import quotes


def get_all_quotes():
    return quotes


def get_random_quote():
    return random.choice(quotes)


def get_quote_by_id(quote_id: int):
    for quote in quotes:
        if quote["id"] == quote_id:
            return quote

    raise HTTPException(
        status_code=404,
        detail="Quote not found"
    )


def create_quote(author: str, text: str, category: str):
    new_quote = {
        "id": len(quotes) + 1,
        "author": author,
        "text": text,
        "category": category
    }

    quotes.append(new_quote)

    return new_quote


def delete_quote(quote_id: int):
    for quote in quotes:
        if quote["id"] == quote_id:
            quotes.remove(quote)

            return {
                "message": "Quote deleted"
            }

    raise HTTPException(
        status_code=404,
        detail="Quote not found"
    )


def update_quote(
    quote_id: int,
    author: str,
    text: str,
    category: str
):
    for quote in quotes:
        if quote["id"] == quote_id:
            quote["author"] = author
            quote["text"] = text
            quote["category"] = category

            return quote

    raise HTTPException(
        status_code=404,
        detail="Quote not found"
    )


def get_quotes_by_category(category: str):
    result = []

    for quote in quotes:
        if quote["category"].lower() == category.lower():
            result.append(quote)

    return result