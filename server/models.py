from typing import Annotated
from decimal import Decimal

from fastapi import Depends
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine


class CategoryBase(SQLModel):
    name: str
    description: str | None
    parent_category: int | None = Field(default=None, foreign_key="category.id")


class Category(CategoryBase, table=True):
    slug: str = Field(unique=True)
    id: int | None = Field(default=None, primary_key=True)


class CategoryPublic(CategoryBase):
    slug: str
    id: int


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    parent_category: int | None = None


class RecipeBase(SQLModel):
    name: str
    slug: str = Field(unique=True)
    description: str | None
    instructions: str
    ingredients: str  # json format
    calories: int
    prep_time: int
    servings: int


class Recipe(RecipeBase, table=True):
    id: int = Field(primary_key=True)


class RecipeUpdate:
    name: str | None = None
    slug: str | None = None
    description: str | None = None
    instructions: str | None = None
    ingredients: str | None = None
    calories: int | None = None
    prep_time: int | None = None
    servings: int | None = None


class CommentBase(SQLModel):
    title: str
    text: str
    rating: Decimal = Field(default=0, max_digits=2, decimal_places=1)
    user_id: int = Field(foreign_key="user.id")


class Comment(CommentBase, table=True):
    id: int = Field(primary_key=True)


class CommentUpdate:
    title: str | None = None
    text: str | None = None
    rating: Decimal | None = None
    user_id: int | None = None


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    username: str
    hashed_password: str
    role: str


class Message(BaseModel):
    message: str


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
