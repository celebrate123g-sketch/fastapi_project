from fastapi import FastAPI

from database.init_db import create_tables

from routers.quotes import router as quotes_router
from routers.comments import router as comments_router
from routers.logs import router as logs_router

app = FastAPI(
    title="Quotes API",
    version="2.0.0"
)


@app.on_event("startup")
def startup():
    create_tables()


app.include_router(quotes_router)
app.include_router(comments_router)
app.include_router(logs_router)