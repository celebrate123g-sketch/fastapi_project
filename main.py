from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random

app = FastAPI(title="Quotes API")

class Quote(BaseModel):
    author: str
    text: str

quotes = [
    {
        "id": 1,
        "author": "Albert Einstein",
        "text": "Life is like riding a bicycle. To keep your balance you must keep moving."
    },
    {
        "id": 2,
        "author": "Steve Jobs",
        "text": "Stay hungry, stay foolish."
    }
]

@app.get("/")
async def home():
    return {"message": "Quotes API is running"}

@app.get("/quotes")
async def get_quotes():
    return quotes

@app.get("/quotes/random")
async def random_quote():
    return random.choice(quotes)

@app.get("/quotes/{quote_id}")
async def get_quote(quote_id: int):
    for quote in quotes:
        if quote["id"] == quote_id:
            return quote

    raise HTTPException(
        status_code=404,
        detail="Quote not found"
    )

@app.post("/quotes")
async def create_quote(quote: Quote):
    new_quote = {
        "id": len(quotes) + 1,
        "author": quote.author,
        "text": quote.text
    }

    quotes.append(new_quote)
    return new_quote

@app.delete("/quotes/{quote_id}")
async def delete_quote(quote_id: int):
    for quote in quotes:
        if quote["id"] == quote_id:
            quotes.remove(quote)
            return {"message": "Quote deleted"}

    raise HTTPException(
        status_code=404,
        detail="Quote not found"
    )