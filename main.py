from fastapi import FastAPI
from routers.quotes import router

app = FastAPI(title="Quotes API")

app.include_router(router)