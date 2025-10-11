from fastapi import FastAPI

from .models import create_db_and_tables
from .routes.categories import router as categories_router

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(categories_router, prefix="/categories", tags=["categories"])
