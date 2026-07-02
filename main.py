from fastapi import FastAPI

from database.init_db import create_tables
from routers.quotes import router

app = FastAPI(
    title="Quotes API",
    version="1.0.0"
)


@app.on_event("startup")
def startup():
    create_tables()


app.include_router(router)