from contextlib import asynccontextmanager
from fastapi import FastAPI

from .models import create_db_and_tables
from .routes.categories import router as categories_router
from .routes.recipes import router as recipes_router
from .routes.comments import router as comments_router
from .routes.auth import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):  # pyright: ignore[reportUnusedParameter]
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(categories_router, prefix="/categories", tags=["categories"])
app.include_router(recipes_router, prefix="/recipes", tags=["recipes"])
app.include_router(comments_router, prefix="/comments", tags=["comments"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])
