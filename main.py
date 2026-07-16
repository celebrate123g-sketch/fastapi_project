from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from database.init_db import create_tables

from routers.quotes import router as quotes_router
from routers.comments import router as comments_router
from routers.logs import router as logs_router
from routers.images import router as images_router
from routers.export import router as export_router
from routers.imports import router as import_router
from routers.history import router as history_router
from routers.authors import router as authors_router
from routers.ratings import router as ratings_router
from routers import recommendations

app = FastAPI(
    title="Quotes API",
    version="4.0.0"
)


@app.on_event("startup")
def startup():
    create_tables()


app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)

app.include_router(quotes_router)
app.include_router(comments_router)
app.include_router(logs_router)
app.include_router(images_router)
app.include_router(export_router)
app.include_router(import_router)
app.include_router(history_router)
app.include_router(authors_router)
app.include_router(ratings_router)
app.include_router(recommendations.router)