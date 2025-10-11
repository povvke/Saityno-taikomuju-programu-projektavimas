from typing import Annotated
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from ..models import (
    Category,
    CategoryCreate,
    CategoryPublic,
    CategoryUpdate,
    Message,
    SessionDep,
)
from ..utils import slugify


router = APIRouter()


@router.post(
    "/",
    status_code=201,
    response_model=CategoryPublic,
    responses={
        409: {"model": Message, "description": "Conflict Error"},
    },
)
async def create_category(cat: CategoryCreate, session: SessionDep):
    try:
        slug = slugify(cat.name)
        cat_db = Category(
            name=cat.name,
            description=cat.description,
            parent_category=cat.parent_category,
            slug=slug,
        )
        session.add(cat_db)
        session.commit()
        session.refresh(cat_db)
        return cat_db
    except IntegrityError as e:
        session.rollback()
        if "UNIQUE constraint failed" in str(e.orig):
            return JSONResponse(
                status_code=409,
                content={"message": "Category with this slug already exists"},
            )


@router.get(
    "/{id}",
    response_model=CategoryPublic,
    responses={
        404: {"model": Message, "description": "Not Found Error"},
    },
)
async def read_category(id: int, session: SessionDep):
    cat = session.get(Category, id)
    if not cat:
        return JSONResponse(status_code=404, content={"message": "Category not found"})
    return cat


@router.get("/", response_model=list[CategoryPublic])
async def read_categories(
    session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100
):
    categories = session.exec(select(Category).offset(offset).limit(limit)).all()
    return categories


@router.patch(
    "/{id}",
    response_model=CategoryPublic,
    responses={
        404: {"model": Message, "description": "Not Found Error"},
        409: {"model": Message, "description": "Conflict Error"},
    },
)
async def update_category(id: int, cat: CategoryUpdate, session: SessionDep):
    try:
        cat_db = session.get(Category, id)
        if not cat_db:
            return JSONResponse(
                status_code=404, content={"message": "Category not found"}
            )

        cat_data = cat.model_dump(exclude_unset=True)
        if cat.name:
            cat_data["slug"] = slugify(cat.name)

        _ = cat_db.sqlmodel_update(cat_data)
        session.add(cat_db)
        session.commit()
        session.refresh(cat_db)
        return cat_db

    except IntegrityError as e:
        session.rollback()
        if "UNIQUE constraint failed" in str(e.orig):
            return JSONResponse(
                status_code=409,
                content={"message": "Category with this slug already exists"},
            )


@router.delete(
    "/{id}",
    responses={
        404: {"model": Message, "description": "Not Found Error"},
    },
)
async def delete_category(
    id: int,
    session: SessionDep,
):
    cat = session.get(Category, id)
    if not cat:
        return JSONResponse(status_code=404, content={"message": "Category not found"})

    session.delete(cat)
    session.commit()
    return {"ok": True}
