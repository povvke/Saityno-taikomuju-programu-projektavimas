from typing import Annotated
from decimal import Decimal

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Category(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    slug: str = Field(unique=True)
    description: str | None
    parent_category: int | None = Field(default=None, foreign_key="category.id")


class Recipe(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    slug: str = Field(unique=True)
    description: str | None
    instructions: str
    ingredients: str  # json format
    calories: int
    prep_time: int
    servings: int


class Comment(SQLModel, table=True):
    id: int = Field(primary_key=True)
    title: str
    text: str
    rating: Decimal = Field(default=0, max_digits=2, decimal_places=1)
    user_id: int = Field(foreign_key="user.id")


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    username: str
    hashed_password: str
    role: str


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
